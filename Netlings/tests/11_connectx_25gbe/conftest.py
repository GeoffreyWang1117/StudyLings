"""N11 共享 fixture。

真实机器上的环境变量（在 veth/lo 上能测的部分不需要它们）：
  NETLINGS_IFACE     ConnectX 网卡名（例如 enp65s0f0np0）
  NETLINGS_PEER_IP   同一链路上对端主机的 IP（nic5 双机吞吐）
"""
import os
import re
import socket

import pytest


@pytest.fixture
def port() -> int:
    """一个在 127.0.0.1 上空闲的 TCP 端口（本章只用 IPv4）。"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture
def udp_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture
def real_iface() -> str:
    """真实网卡（NETLINGS_IFACE）。没设置就跳过。"""
    iface = os.environ.get("NETLINGS_IFACE")
    if not iface:
        pytest.skip("未设置 NETLINGS_IFACE：这部分要在装有 ConnectX 网卡的机器上验证，"
                    "例如 export NETLINGS_IFACE=enp65s0f0np0")
    if not os.path.exists(f"/sys/class/net/{iface}"):
        pytest.skip(f"NETLINGS_IFACE={iface} 不存在（ip -br link 查看网卡名）")
    return iface


def _parse_kv(text: str) -> dict[str, str]:
    out = {}
    for line in text.splitlines():
        m = re.match(r"^([a-z_0-9]+)=(.*)$", line.strip())
        if m:
            out[m.group(1)] = m.group(2)
    return out


@pytest.fixture
def parse_kv():
    """函数：把 key=value 行解析成 dict（同一个 key 出现多次时保留最后一个）。"""
    return _parse_kv
