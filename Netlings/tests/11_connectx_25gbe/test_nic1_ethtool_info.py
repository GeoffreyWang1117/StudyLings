from pathlib import Path

import pytest

from studylings.netlab import netlab  # noqa: F401  (fixture)
from studylings.probe import assert_ok, run


def _check_common(kv: dict, what: str):
    for key in ("driver", "version", "firmware", "bus_info", "speed_mbps", "duplex", "autoneg", "port",
                "link_mode_nwords", "mtu", "numa_node"):
        assert key in kv, f"{what}: 输出里缺少 {key}=...\n实际输出：{kv}"
    assert int(kv["link_mode_nwords"]) > 0, (
        f"{what}: link_mode_nwords={kv['link_mode_nwords']}，应为正数 N —— 第一次调用内核返回的是 -N，"
        "要把它取反后作为第二次调用的 nwords")


def test_veth_fields(exe, netlab, parse_kv):
    a = netlab.ns("nic1")
    b = netlab.ns("nic1p")
    dev, _ = netlab.link(a, b, "10.71.0.1/24", "10.71.0.2/24", mtu=1400)
    r = netlab.run(a, exe, dev, check=False)
    assert_ok(r, "driver=", "nic1_ethtool_info <veth>")
    kv = parse_kv(r.stdout)
    _check_common(kv, "veth")
    assert kv["driver"] == "veth", f"driver={kv['driver']!r}，veth 的驱动名应为 'veth'（ETHTOOL_GDRVINFO）"
    sys_speed = int(netlab.run(a, "cat", f"/sys/class/net/{dev}/speed").stdout.strip())
    assert int(kv["speed_mbps"]) == sys_speed, (
        f"speed_mbps={kv['speed_mbps']}，/sys/class/net/{dev}/speed = {sys_speed}。"
        "读到 0？ETHTOOL_GLINKSETTINGS 第一次调用只是握手（nwords=0 → 内核回填 -N），"
        "要用 +N 再调一次才有数据")
    assert kv["duplex"] == "full", f"duplex={kv['duplex']}，veth 应为 full"
    assert kv["mtu"] == "1400", f"mtu={kv['mtu']}，这对 veth 的 MTU 被设成了 1400（SIOCGIFMTU）"
    assert kv["numa_node"] == "-1", f"numa_node={kv['numa_node']}，veth 没有 device/numa_node，应打印 -1"


def test_missing_iface(exe):
    r = run(exe, "nosuchnic0")
    assert r.returncode != 0, "不存在的网卡应该以非 0 退出\n" + r.stdout
    assert "No such device" in r.stderr, (
        f"错误信息里应带 strerror(errno)（ENODEV → 'No such device'），实际 stderr：{r.stderr!r}")


def test_real_connectx(exe, real_iface, parse_kv):
    r = run(exe, real_iface)
    assert_ok(r, "driver=", f"nic1_ethtool_info {real_iface}")
    kv = parse_kv(r.stdout)
    _check_common(kv, real_iface)
    print(r.stdout)
    assert kv["driver"] == "mlx5_core", f"driver={kv['driver']}，NETLINGS_IFACE 应指向 ConnectX（mlx5_core）"
    assert kv["firmware"], "firmware 为空：ConnectX 的 ETHTOOL_GDRVINFO 应返回 fw 版本（如 26.36.1010 (MT_0000000531)）"
    sys_speed = int(Path(f"/sys/class/net/{real_iface}/speed").read_text().strip() or -1)
    assert int(kv["speed_mbps"]) == sys_speed, f"speed_mbps={kv['speed_mbps']} 与 sysfs {sys_speed} 不一致"
    if sys_speed != 25000:
        print(f"注意：{real_iface} 当前速率 {sys_speed} Mb/s（25GbE 满速应为 25000；链路没起来时为 -1）")
    numa = Path(f"/sys/class/net/{real_iface}/device/numa_node")
    if numa.exists():
        assert kv["numa_node"] == numa.read_text().strip(), f"numa_node={kv['numa_node']} 与 sysfs 不一致"
    bus = Path(f"/sys/class/net/{real_iface}/device").resolve().name
    assert kv["bus_info"] == bus, f"bus_info={kv['bus_info']}，应为 PCI 地址 {bus}"
