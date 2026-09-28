import os
import shutil
import socket
import tempfile
import threading

import pytest

from studylings.probe import assert_ok, run, start


@pytest.fixture
def sock_dir(tmp_path):
    """sun_path 只有 108 字节：tmp_path 太长时换一个短目录。"""
    if len(str(tmp_path)) < 80:
        yield tmp_path
        return
    d = tempfile.mkdtemp(prefix="sl-uds-")
    try:
        yield d
    finally:
        shutil.rmtree(d, ignore_errors=True)


def receiver_output(p) -> tuple[str, str]:
    rc = p.wait(timeout=10)
    assert rc == 0, f"recv 端应当 exit 0，实际 exit {rc}\n{p.describe()}"
    out = p.stdout
    first, _, rest = out.partition("\n")
    return rest, p.stderr


def test_program_to_program(exe, sock_dir, tmp_path):
    sock = os.path.join(sock_dir, "pass.sock")
    f = tmp_path / "payload.txt"
    content = "".join(f"line {i}: descriptor passing\n" for i in range(3000))
    f.write_text(content)
    with start(exe, "recv", sock) as p:
        p.expect(r"listening", timeout=10)
        r = run(exe, "send", sock, f)
        assert_ok(r, what="send 端")
        got, err = receiver_output(p)
    assert got == content, f"recv 端输出的内容与文件不一致（收到 {len(got)} 字节，应为 {len(content)}）"


def test_receiver_gets_real_fd_even_if_file_deleted(exe, sock_dir, tmp_path):
    """由探针当发送方：打开文件后立刻删除它，再把 fd 发过去 —— 只有真正收到 fd 才能读到内容。"""
    sock = os.path.join(sock_dir, "pass2.sock")
    f = tmp_path / "secret.txt"
    content = "only reachable through the fd\n" * 50
    f.write_text(content)
    fd = os.open(f, os.O_RDONLY)
    os.unlink(f)
    try:
        with start(exe, "recv", sock) as p:
            p.expect(r"listening", timeout=10)
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as c:
                c.connect(sock)
                socket.send_fds(c, [b"F"], [fd])
            got, err = receiver_output(p)
    finally:
        os.close(fd)
    assert got == content, "recv 端没有通过收到的 fd 读出（已被删除的）文件内容 —— 真的从 cmsg 里取出 fd 了吗？"
    assert "cloexec=1" in err, f"收到的 fd 应当带 FD_CLOEXEC（recvmsg 加 MSG_CMSG_CLOEXEC），stderr: {err!r}"


def test_sender_sends_real_fd(exe, sock_dir, tmp_path):
    """由探针当接收方：用 recv_fds 检查发送方的消息里确实带着一个 SCM_RIGHTS fd。"""
    sock = os.path.join(sock_dir, "pass3.sock")
    f = tmp_path / "data.txt"
    content = "sent by descriptor\n"
    f.write_text(content)
    result = {}
    srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    srv.bind(sock)
    srv.listen(1)
    srv.settimeout(10)

    def serve():
        try:
            conn, _ = srv.accept()
            with conn:
                conn.settimeout(10)
                result["msg"] = socket.recv_fds(conn, 16, 4)
        except OSError as e:
            result["err"] = e

    t = threading.Thread(target=serve, daemon=True)
    t.start()
    try:
        r = run(exe, "send", sock, f)
        assert_ok(r, what="send 端")
        t.join(timeout=10)
    finally:
        srv.close()
    if "err" in result or "msg" not in result:
        pytest.fail(f"探针接收失败：{result.get('err')!r}", pytrace=False)
    data, fds, flags, _ = result["msg"]
    try:
        assert len(data) >= 1, "sendmsg 至少要带 1 字节普通数据"
        assert len(fds) == 1, f"消息里应当恰好带 1 个 SCM_RIGHTS fd，实际 {len(fds)} 个（控制数据构造对了吗？）"
        os.unlink(f)  # 发送方已退出、文件已删除，fd 仍然有效
        os.lseek(fds[0], 0, os.SEEK_SET)
        assert os.read(fds[0], 4096).decode() == content, "收到的 fd 读出的内容不对"
    finally:
        for fd in fds:
            os.close(fd)
