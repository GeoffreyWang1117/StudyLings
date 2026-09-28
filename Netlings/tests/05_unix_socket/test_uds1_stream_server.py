import os
import shutil
import signal
import socket
import tempfile
import uuid

import pytest

from studylings.probe import start


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


def echo_roundtrip(addr: str, payload: bytes):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as c:
        c.settimeout(5)
        try:
            c.connect(addr)
        except OSError as e:
            pytest.fail(f"connect({addr!r}) 失败：{e}", pytrace=False)
        c.sendall(payload)
        c.shutdown(socket.SHUT_WR)
        got = b""
        while chunk := c.recv(65536):
            got += chunk
    assert got == payload, f"回显内容不一致：发送 {len(payload)} 字节，收到 {len(got)} 字节"


def test_path_echo_and_graceful_unlink(exe, sock_dir):
    path = os.path.join(sock_dir, "echo.sock")
    with start(exe, path) as p:
        p.expect(r"listening", timeout=10)
        assert os.path.exists(path), "bind 之后应当出现 socket 文件"
        echo_roundtrip(path, b"hello over AF_UNIX\n")
        echo_roundtrip(path, os.urandom(200_000))
        p.signal(signal.SIGTERM)
        rc = p.wait(timeout=10)
        assert rc == 0, f"收到 SIGTERM 应优雅退出 (exit 0)，实际 exit {rc}\n{p.describe()}"
    assert not os.path.exists(path), "SIGTERM 优雅退出后应当 unlink 自己的 socket 文件（否则留下陈旧文件）"


def test_stale_socket_file_is_replaced(exe, sock_dir):
    path = os.path.join(sock_dir, "stale.sock")
    # 模拟"上次运行崩溃"：bind 一个 socket 然后直接关闭，文件留在磁盘上
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.bind(path)
    s.close()
    assert os.path.exists(path)
    with start(exe, path) as p:
        p.expect(r"listening", timeout=10)
        echo_roundtrip(path, b"after crash\n")


def test_abstract_namespace(exe, sock_dir):
    name = f"netlings-uds1-{os.getpid()}-{uuid.uuid4().hex[:8]}"
    before = set(os.listdir(sock_dir))
    with start(exe, "@" + name, cwd=sock_dir) as p:
        p.expect(r"listening", timeout=10)
        # Python 用 "\0name" 表示抽象地址，addrlen = 2 + 1 + len(name)，精确到名字末尾
        echo_roundtrip("\0" + name, b"abstract hello\n")
        p.signal(signal.SIGTERM)
        assert p.wait(timeout=10) == 0, f"SIGTERM 后应 exit 0\n{p.describe()}"
    assert set(os.listdir(sock_dir)) == before, "抽象地址不应该在文件系统里创建任何文件"
