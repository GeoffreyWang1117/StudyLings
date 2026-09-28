import contextlib
import os
import socket
import struct
import time

import pytest

from studylings.probe import start


@contextlib.contextmanager
def peer_must_stay(what: str):
    """服务器中途关掉/重置连接时给出可读的失败信息，而不是 Python 异常栈。"""
    try:
        yield
    except (BrokenPipeError, ConnectionResetError) as e:
        pytest.fail(f"{what}：服务器中途关闭了连接（{e.strerror}）。"
                    "read 返回的字节数少于请求数不是错误，要循环读满。", pytrace=False)


def frame(payload: bytes) -> bytes:
    return struct.pack("!I", len(payload)) + payload


def recv_exact(c: socket.socket, n: int, what: str) -> bytes:
    buf = bytearray()
    while len(buf) < n:
        try:
            d = c.recv(min(n - len(buf), 1 << 20))
        except socket.timeout:
            pytest.fail(f"{what}：等待回复超时，已收到 {len(buf)}/{n} 字节"
                        "（服务器是不是在等一次 read 读满整帧？）", pytrace=False)
        if not d:
            pytest.fail(f"{what}：服务器提前关闭了连接，已收到 {len(buf)}/{n} 字节"
                        "（read 短读被当成错误了？）", pytrace=False)
        buf += d
    return bytes(buf)


def recv_frame(c: socket.socket, what: str) -> bytes:
    (n,) = struct.unpack("!I", recv_exact(c, 4, what + "（长度头）"))
    return recv_exact(c, n, what + "（负载）")


@pytest.fixture
def server(exe, port):
    with start(exe, port) as p:
        p.expect(rf"listening on port {port}\b", timeout=10)
        yield port


def connect(port) -> socket.socket:
    c = socket.create_connection(("127.0.0.1", port), timeout=10)
    c.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # 让每个字节真的单独成段
    return c


def test_simple_roundtrip(server):
    with connect(server) as c, peer_must_stay("单帧"):
        c.sendall(frame(b"hello, framing"))
        assert recv_frame(c, "单帧") == b"gnimarf ,olleh", "回复应为负载的逆序"


def test_fragmented_one_byte_at_a_time(server):
    with connect(server) as c, peer_must_stay("逐字节发送"):
        for b in frame(b"fragmented!"):
            c.sendall(bytes([b]))
            time.sleep(0.003)
        got = recv_frame(c, "逐字节发送的帧")
        assert got == b"!detnemgarf", f"分片到达的帧没有被正确拼起来，收到 {got!r}"


def test_coalesced_frames(server):
    msgs = [b"one", b"", b"three", b"x" * 1000]
    with connect(server) as c, peer_must_stay("合并发送"):
        c.sendall(b"".join(frame(m) for m in msgs))  # 多帧挤在一次发送里
        for i, m in enumerate(msgs):
            got = recv_frame(c, f"合并发送的第 {i + 1} 帧")
            assert got == m[::-1], f"第 {i + 1} 帧回复错误：期望 {m[::-1][:20]!r}…，收到 {got[:20]!r}…"


def test_one_mebibyte_frame(server):
    payload = os.urandom(1 << 20)
    with connect(server) as c, peer_must_stay("1 MiB 大帧"):
        c.sendall(frame(payload))
        got = recv_frame(c, "1 MiB 大帧")
        assert got == payload[::-1], "1 MiB 帧的回复内容不正确"


def test_oversized_length_is_rejected_and_server_survives(server):
    with connect(server) as c:
        c.sendall(struct.pack("!I", 0xFFFFFFFF))
        try:
            d = c.recv(16)
        except socket.timeout:
            pytest.fail("收到非法长度 0xFFFFFFFF 后服务器应立即关闭连接", pytrace=False)
        except ConnectionResetError:
            d = b""
        assert d == b"", f"非法长度的帧不应得到回复，收到 {d!r}"
    with connect(server) as c, peer_must_stay("非法帧之后的新连接"):
        c.sendall(frame(b"still alive"))
        assert recv_frame(c, "非法帧之后的新连接") == b"evila llits"
