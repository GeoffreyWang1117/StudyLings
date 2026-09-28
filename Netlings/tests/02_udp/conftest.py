"""本章共享的小工具：IPv4/IPv6 端口与 IPv6 可用性检测。

studylings.probe.free_port() 会顺带检查 ::1 —— 在禁用了 IPv6 的容器/VM 里（Docker 默认、
部分 CI）它会失败。本章的 `port` fixture 在没有 IPv6 时退回只检查 127.0.0.1。
"""
import socket

import pytest


def _ipv6_available() -> bool:
    try:
        with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s:
            s.bind(("::1", 0))
        return True
    except OSError:
        return False


HAS_IPV6 = _ipv6_available()


@pytest.fixture
def has_ipv6() -> bool:
    return HAS_IPV6


@pytest.fixture
def need_ipv6():
    if not HAS_IPV6:
        pytest.skip("本机没有 IPv6（::1 不可用），跳过 IPv6 用例")


def _pick_port() -> int:
    for _ in range(50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 0))
            port = s.getsockname()[1]
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as u:
                u.bind(("127.0.0.1", port))
            if HAS_IPV6:
                for kind in (socket.SOCK_STREAM, socket.SOCK_DGRAM):
                    with socket.socket(socket.AF_INET6, kind) as s6:
                        s6.bind(("::1", port))
        except OSError:
            continue
        return port
    pytest.fail("找不到空闲端口")


@pytest.fixture
def port() -> int:
    """一个在 127.0.0.1（以及可用时 ::1）上 TCP/UDP 都空闲的端口。"""
    return _pick_port()
