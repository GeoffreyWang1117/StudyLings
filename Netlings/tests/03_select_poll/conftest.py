"""本章共享的 `port` fixture。

studylings.probe.free_port() 会顺带检查 ::1 —— 在禁用了 IPv6 的容器/VM 里（Docker 默认、
部分 CI）它会失败。本章只用 127.0.0.1，所以只要求 IPv4 端口空闲。
"""
import socket

import pytest


@pytest.fixture
def port() -> int:
    """一个在 127.0.0.1 上空闲的 TCP 端口。"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]
