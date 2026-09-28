import socket
import threading

import pytest

from studylings.probe import assert_ok, run


class LineServer:
    """只监听一个地址（127.0.0.1 或 ::1）的 Python 服务器：读一行，回 "echo:<行>"。"""

    def __init__(self, family, addr, port):
        self.sock = socket.socket(family, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if family == socket.AF_INET6:
            self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
        self.sock.bind((addr, port))
        self.sock.listen(8)
        self.sock.settimeout(10)
        self.got: list[bytes] = []
        self.t = threading.Thread(target=self._serve, daemon=True)
        self.t.start()

    def _serve(self):
        try:
            c, _ = self.sock.accept()
        except OSError:
            return
        with c:
            c.settimeout(10)
            buf = b""
            while not buf.endswith(b"\n"):
                d = c.recv(4096)
                if not d:
                    break
                buf += d
            self.got.append(buf)
            c.sendall(b"echo:" + buf)

    def close(self):
        try:
            self.sock.shutdown(socket.SHUT_RDWR)  # 唤醒阻塞在 accept 的线程
        except OSError:
            pass
        self.sock.close()
        self.t.join(timeout=5)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


def _localhost_families() -> list[int]:
    try:
        return [ai[0] for ai in socket.getaddrinfo("localhost", 80, socket.AF_UNSPEC, socket.SOCK_STREAM)]
    except socket.gaierror:
        return []


def test_numeric_ipv4(exe, port):
    with LineServer(socket.AF_INET, "127.0.0.1", port) as srv:
        r = run(exe, "127.0.0.1", port, "hello v4")
    assert_ok(r, what="连接 127.0.0.1")
    assert r.stdout == "echo:hello v4\n", f"应打印服务器回的一行，实际 {r.stdout!r}"
    assert srv.got == [b"hello v4\n"], f"服务器应收到 'hello v4\\n'，实际 {srv.got!r}"


def test_localhost_when_server_is_ipv4_only(exe, port):
    """服务只监听 127.0.0.1；若 localhost 先解析出 ::1，只试第一个地址就会失败。"""
    fams = _localhost_families()
    if socket.AF_INET not in fams:
        pytest.skip("本机 localhost 解析不出 127.0.0.1")
    with LineServer(socket.AF_INET, "127.0.0.1", port):
        r = run(exe, "localhost", port, "via localhost")
    hint = ""
    if fams and fams[0] == socket.AF_INET6:
        hint = "（本机 localhost 先解析出 ::1 —— 你是不是只试了第一个地址？）"
    assert_ok(r, what="服务只监听 127.0.0.1，客户端用 localhost 连接" + hint)
    assert r.stdout == "echo:via localhost\n", f"实际输出 {r.stdout!r}"


def test_numeric_ipv6(exe, port, need_ipv6):
    with LineServer(socket.AF_INET6, "::1", port):
        r = run(exe, "::1", port, "hello v6")
    assert_ok(r, what="连接 ::1（hints.ai_family 是不是写死成 AF_INET 了？）")
    assert r.stdout == "echo:hello v6\n", f"实际输出 {r.stdout!r}"


def test_localhost_when_server_is_ipv6_only(exe, port, need_ipv6):
    if socket.AF_INET6 not in _localhost_families():
        pytest.skip("本机 localhost 没有解析出 ::1（/etc/hosts 里没有 ::1 localhost）")
    with LineServer(socket.AF_INET6, "::1", port):
        r = run(exe, "localhost", port, "v6 only")
    assert_ok(r, what="服务只监听 ::1，客户端用 localhost 连接（要用 AF_UNSPEC 并逐个尝试）")
    assert r.stdout == "echo:v6 only\n", f"实际输出 {r.stdout!r}"


def test_refused_reports_error(exe, port):
    r = run(exe, "127.0.0.1", port, "nobody home")
    assert r.returncode == 1, f"没有服务器监听时应 exit 1，实际 exit {r.returncode}\nstderr: {r.stderr}"
    assert "Connection refused" in r.stderr, f"stderr 应包含 connect 的错误原因，实际 {r.stderr!r}"
