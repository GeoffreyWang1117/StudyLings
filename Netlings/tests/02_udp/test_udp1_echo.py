import os
import socket

import pytest

from studylings.probe import start


@pytest.fixture
def server(exe, port):
    with start(exe, port) as p:
        p.expect(rf"listening on port {port}\b", timeout=10)
        yield port


def echo(family, addr, port, payload: bytes, what: str) -> bytes:
    with socket.socket(family, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1 << 18)
        s.settimeout(3)
        s.sendto(payload, (addr, port))
        try:
            data, src = s.recvfrom(1 << 17)
        except socket.timeout:
            pytest.fail(f"{what}：3 秒内没有收到回显（{len(payload)} 字节的数据报）", pytrace=False)
        return data


def test_ipv4_datagrams(server):
    for msg in (b"hello", b"second datagram", b"a\nb\n\x00binary\xff"):
        got = echo(socket.AF_INET, "127.0.0.1", server, msg, "IPv4 客户端")
        assert got == msg, f"回显内容不同：发送 {msg!r}，收到 {got!r}"


def test_ipv6_datagrams(server, need_ipv6):
    got = echo(socket.AF_INET6, "::1", server, b"over v6", "IPv6 客户端")
    assert got == b"over v6", f"收到 {got!r}"


def test_replies_go_to_each_sender(server):
    socks = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for _ in range(3)]
    try:
        for i, s in enumerate(socks):
            s.settimeout(3)
            s.sendto(f"client-{i}".encode(), ("127.0.0.1", server))
        for s in reversed(socks):
            s.sendto(b"again", ("127.0.0.1", server))
        for i, s in enumerate(socks):
            got = []
            for _ in range(2):
                try:
                    got.append(s.recv(100))
                except socket.timeout:
                    pytest.fail(f"客户端 {i} 没收到发给它的回显（回复要发给 recvfrom 得到的地址）",
                                pytrace=False)
            assert got == [f"client-{i}".encode(), b"again"], f"客户端 {i} 收到 {got!r}"
    finally:
        for s in socks:
            s.close()


def test_empty_datagram(server):
    got = echo(socket.AF_INET, "127.0.0.1", server, b"",
               "空数据报（recvfrom 返回 0 是合法的空消息，不是 EOF）")
    assert got == b"", f"空数据报的回显应为空，收到 {got!r}"


def test_large_datagram_boundaries(server):
    big = os.urandom(60000)
    got = echo(socket.AF_INET, "127.0.0.1", server, big, "60000 字节数据报")
    if len(got) != len(big):
        pytest.fail(f"60000 字节的数据报只回来了 {len(got)} 字节 —— recvfrom 缓冲区太小，"
                    "多余部分被静默截断了（UDP 最大负载约 64 KiB）", pytrace=False)
    if got != big:
        pytest.fail("大数据报的回显内容不一致", pytrace=False)
    small = echo(socket.AF_INET, "127.0.0.1", server, b"tail", "大数据报之后的小数据报")
    assert small == b"tail", f"消息边界被破坏：收到 {small[:40]!r}"
