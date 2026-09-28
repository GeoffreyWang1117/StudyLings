"""N12 共享 fixture。

真实机器上的环境变量：
  NETLINGS_RDMA_DEV        RDMA 设备名（mlx5_0 / rxe0）；不设则用 /sys/class/infiniband 下的第一个
  NETLINGS_RDMA_GID_INDEX  RoCE v2 GID 下标；不设则程序自动挑 RoCE v2 + IPv4 映射的 GID
  NETLINGS_RDMA_IP         rdma4（librdmacm）用的本机 IP；不设则从 RoCE v2 GID 里取 IPv4
没有 RDMA 设备时，需要设备的测试全部跳过：
  sudo modprobe rdma_rxe && sudo rdma link add rxe0 type rxe netdev <iface>   （Soft-RoCE）
"""
import os
import socket
from pathlib import Path

import pytest

from studylings.probe import run

IB_SYSFS = Path("/sys/class/infiniband")
NO_DEV_REASON = ("no RDMA device: load rdma_rxe or use ConnectX —— 本机没有 RDMA 设备，需要设备的测试跳过。"
                 "在真实机器上设置 NETLINGS_RDMA_DEV=mlx5_0，或用 Soft-RoCE："
                 "sudo modprobe rdma_rxe && sudo rdma link add rxe0 type rxe netdev <iface>")
LSAN_ENV = {"LSAN_OPTIONS": f"suppressions={Path(__file__).with_name('lsan.supp')}:print_suppressions=0"}


def _devices() -> list[str]:
    try:
        return sorted(p.name for p in IB_SYSFS.iterdir())
    except OSError:
        return []


@pytest.fixture
def rdma_env() -> dict:
    """传给 run/start 的额外环境变量（LSan 抑制 rdma-core 内部的常驻分配）。"""
    env = dict(LSAN_ENV)
    for k in ("NETLINGS_RDMA_DEV", "NETLINGS_RDMA_GID_INDEX"):
        if os.environ.get(k):
            env[k] = os.environ[k]
    return env


@pytest.fixture
def rdma_dev() -> str:
    devs = _devices()
    want = os.environ.get("NETLINGS_RDMA_DEV")
    if want:
        if want not in devs:
            pytest.skip(f"NETLINGS_RDMA_DEV={want} 不存在（现有设备：{devs or '无'}；rdma link 查看）")
        return want
    if not devs:
        pytest.skip(NO_DEV_REASON)
    return devs[0]


@pytest.fixture
def no_rdma_device():
    """只在没有 RDMA 设备的机器上运行（验证程序给出清楚的提示而不是崩溃）。"""
    if _devices():
        pytest.skip("本机有 RDMA 设备，'无设备' 提示路径不需要测试")


def _roce_v2_ipv4(dev: str, port: int = 1) -> str | None:
    base = IB_SYSFS / dev / "ports" / str(port)
    try:
        idxs = sorted(int(p.name) for p in (base / "gids").iterdir())
    except OSError:
        return None
    for i in idxs:
        try:
            gid = (base / "gids" / str(i)).read_text().strip()
            typ = (base / "gid_attrs" / "types" / str(i)).read_text().strip()
        except OSError:
            continue  # 空表项读 types 会 EINVAL
        if typ == "RoCE v2" and gid.startswith("0000:0000:0000:0000:0000:ffff:"):
            h = gid.split(":")[6:8]
            raw = bytes.fromhex(h[0] + h[1])
            return socket.inet_ntoa(raw)
    return None


@pytest.fixture
def rdma_ipv4(rdma_dev) -> str:
    ip = os.environ.get("NETLINGS_RDMA_IP") or _roce_v2_ipv4(rdma_dev)
    if not ip:
        pytest.skip(f"{rdma_dev} 没有 RoCE v2 IPv4 GID（给对应网卡配一个 IPv4 地址，或设置 NETLINGS_RDMA_IP）")
    return ip


@pytest.fixture
def port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def skip_if_no_device(r) -> None:
    """程序自己报告 'no RDMA device' 时跳过（例如设备存在但 ib_uverbs 没加载）。"""
    text = (r.stdout or "") + (r.stderr or "")
    if "no RDMA device" in text:
        pytest.skip(NO_DEV_REASON + f"\n程序输出：{text.strip()[:300]}")


@pytest.fixture
def rdma_run(rdma_env):
    """run() 的包装：带上 rdma_env，并在程序报告无设备时跳过。"""
    def _run(exe, *args, timeout=30):
        r = run(exe, *args, env=rdma_env, timeout=timeout)
        skip_if_no_device(r)
        return r
    return _run
