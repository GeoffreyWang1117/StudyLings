import os
import socket
import time
from pathlib import Path

import pytest

from studylings.probe import start

O_CLOEXEC = 0o2000000


def _talk(family, addr, port, payload: bytes, timeout=5) -> bytes:
    """发 payload，然后读到对端关闭（EOF）为止。"""
    with socket.socket(family, socket.SOCK_STREAM) as c:
        c.settimeout(timeout)
        c.connect((addr, port))
        c.sendall(payload)
        out = b""
        while True:
            try:
                d = c.recv(65536)
            except socket.timeout:
                pytest.fail(f"{timeout}s 内服务器既没回完数据也没关闭连接。已收到 {out!r}\n"
                            "（收到 \"quit\" 那一行并回显后，服务器要主动 close）", pytrace=False)
            if not d:
                return out
            out += d


def _server(exe, port):
    p = start(exe, port)
    p.expect(rf"listening on port {port}\b", timeout=10)
    return p


def test_ipv4_client_echo(exe, port):
    with _server(exe, port):
        out = _talk(socket.AF_INET, "127.0.0.1", port, b"hello\nworld\nquit\n")
    assert out == b"hello\nworld\nquit\n", f"逐行回显不正确，收到 {out!r}"


def test_ipv6_client_echo(exe, port, need_ipv6):
    with _server(exe, port):
        out = _talk(socket.AF_INET6, "::1", port, b"over v6\nquit\n")
    assert out == b"over v6\nquit\n", f"IPv6 客户端回显不正确，收到 {out!r}"


def test_split_lines_and_sequential_clients(exe, port):
    with _server(exe, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
            c.settimeout(5)
            c.connect(("127.0.0.1", port))
            for piece in (b"he", b"llo wo", b"rld\nsecond", b" line\n"):
                c.sendall(piece)
                time.sleep(0.02)
            want = b"hello world\nsecond line\n"
            got = b""
            while len(got) < len(want):
                d = c.recv(4096)
                if not d:
                    break
                got += d
            assert got == want, f"一行被拆成多次发送时应拼起来再回显，收到 {got!r}"
        # 上一个客户端先关闭（没有 quit），服务器应继续 accept 下一个
        out = _talk(socket.AF_INET, "127.0.0.1", port, b"next\nquit\n")
        assert out == b"next\nquit\n", f"第二个连接的回显不正确，收到 {out!r}"


def _time_wait_on(port: int) -> bool:
    hexport = f":{port:04X}"
    for f in ("/proc/net/tcp", "/proc/net/tcp6"):
        try:
            lines = Path(f).read_text().splitlines()[1:]
        except OSError:
            continue
        for line in lines:
            cols = line.split()
            if cols[1].endswith(hexport) and cols[3] == "06":  # 06 = TCP_TIME_WAIT
                return True
    return False


def test_quit_is_active_close_and_restart_binds(exe, port):
    p = _server(exe, port)
    with p:
        out = _talk(socket.AF_INET, "127.0.0.1", port, b"bye\nquit\n")
        assert out == b"bye\nquit\n", f"收到 {out!r}"
    # 现在服务器被 SIGKILL 了；它主动关闭的那条连接应该还在 TIME_WAIT
    if not _time_wait_on(port):
        pytest.fail(f"服务器端口 {port} 上没有看到 TIME_WAIT 连接：收到 \"quit\" 后应由服务器先 close"
                    "（主动关闭方进入 TIME_WAIT）", pytrace=False)
    with start(exe, port) as p2:
        restarted = True
        try:
            p2.expect(rf"listening on port {port}\b", timeout=10)
        except pytest.fail.Exception:
            restarted = False
        if not restarted:
            pytest.fail("服务器被 kill 后立刻在同一端口重启失败（TIME_WAIT 还在）。\n"
                        "bind 之前要 setsockopt(SO_REUSEADDR)。\n" + p2.describe(), pytrace=False)
        out = _talk(socket.AF_INET, "127.0.0.1", port, b"again\nquit\n")
        assert out == b"again\nquit\n", f"重启后的回显不正确，收到 {out!r}"


def _socket_fd_flags(pid: int) -> dict[int, int]:
    res = {}
    for fd in os.listdir(f"/proc/{pid}/fd"):
        try:
            if not os.readlink(f"/proc/{pid}/fd/{fd}").startswith("socket:"):
                continue
            for line in Path(f"/proc/{pid}/fdinfo/{fd}").read_text().splitlines():
                if line.startswith("flags:"):
                    res[int(fd)] = int(line.split()[1], 8)
        except OSError:
            pass
    return res


def test_fds_are_cloexec(exe, port):
    with _server(exe, port) as p:
        with socket.create_connection(("127.0.0.1", port), timeout=5) as c:
            c.sendall(b"ping\n")
            assert c.recv(100) == b"ping\n", "回显不正确"
            flags = _socket_fd_flags(p.pid)
            assert len(flags) >= 2, f"服务器进程里应至少有监听 fd 和已连接 fd，实际 {flags}"
            bad = [fd for fd, fl in flags.items() if not fl & O_CLOEXEC]
            assert not bad, (f"这些 socket fd 没有 O_CLOEXEC：{bad}。"
                             "socket() 要加 SOCK_CLOEXEC，accept 要换成 accept4(..., SOCK_CLOEXEC)")
