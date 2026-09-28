import select
import socket
import time

import pytest

from studylings.probe import run


def _check(r, expect_out: str, expect_rc: int, what: str):
    if r.stdout.strip() != expect_out or r.returncode != expect_rc:
        pytest.fail(f"{what}：应打印 {expect_out!r} 并以 {expect_rc} 退出，"
                    f"实际 stdout={r.stdout.strip()!r} exit={r.returncode}\n--- stderr ---\n{r.stderr}",
                    pytrace=False)


def test_connected(exe):
    with socket.socket() as lst:
        lst.bind(("127.0.0.1", 0))
        lst.listen(8)
        port = lst.getsockname()[1]
        r = run(exe, "127.0.0.1", port, 2000, timeout=15)
        _check(r, "connected", 0, "连接正在监听的端口")
        lst.settimeout(2)
        try:
            conn, _ = lst.accept()
            conn.close()
        except socket.timeout:
            pytest.fail("程序说 connected，但监听端并没有收到连接", pytrace=False)


def test_refused(exe, port):
    # port 上没有任何人监听 → 内核直接回 RST
    r = run(exe, "127.0.0.1", port, 2000, timeout=15)
    _check(r, "refused", 2, "连接没人监听的端口")


def _make_black_hole():
    """一个 SYN 会被默默丢弃的本机地址：accept 队列已满的监听 socket。

    listen(0) 的 accept 队列能放 1 个已完成握手的连接。我们用一个"填充"连接占满它，
    且永远不 accept。之后新来的 SYN 会被 Linux 直接丢弃（net.ipv4.tcp_abort_on_overflow=0，默认），
    客户端看到的就和远端防火墙丢包一样：没有 SYN-ACK，也没有 RST。
    """
    lst = socket.socket()
    lst.bind(("127.0.0.1", 0))
    lst.listen(0)
    port = lst.getsockname()[1]
    filler = socket.socket()
    filler.settimeout(2)
    filler.connect(("127.0.0.1", port))  # 占满 accept 队列
    # 自检：再来一个非阻塞 connect，1s 内必须既不成功也不失败，否则这个内核上黑洞不成立
    probe = socket.socket()
    probe.setblocking(False)
    probe.connect_ex(("127.0.0.1", port))
    _, w, _ = select.select([], [probe], [], 1.0)
    probe.close()
    if w:
        filler.close()
        lst.close()
        pytest.skip("本机内核没有丢弃 accept 队列溢出时的 SYN（tcp_abort_on_overflow=1？），无法构造黑洞")
    return lst, filler, port


def test_timeout_black_hole(exe):
    lst, filler, port = _make_black_hole()
    try:
        t0 = time.monotonic()
        try:
            r = run(exe, "127.0.0.1", port, 500, timeout=10)
        except pytest.fail.Exception:
            r = None
        elapsed = time.monotonic() - t0
    finally:
        filler.close()
        lst.close()
    if r is None:
        pytest.fail("TIMEOUT_MS=500，程序 10s 后还卡着：阻塞的 connect 会一直重传 SYN（约 2 分钟）。"
                    "要用非阻塞 socket + poll(POLLOUT, timeout) 自己控制超时", pytrace=False)
    _check(r, "timeout", 3, "连接一个丢弃 SYN 的黑洞（500ms 超时）")
    assert elapsed >= 0.45, f"超时设为 500ms，程序却在 {elapsed:.2f}s 就放弃了"
    assert elapsed < 5, f"超时设为 500ms，程序却用了 {elapsed:.2f}s 才返回"
