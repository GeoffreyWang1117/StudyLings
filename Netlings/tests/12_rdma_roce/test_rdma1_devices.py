import re
from pathlib import Path

from studylings.probe import assert_ok, run


def _fake_port(root: Path, dev: str, entries: dict[int, tuple[str, str | None, str]]):
    """entries: index → (sysfs GID 文本, 类型文本或 None（空表项读不出类型）, ndev)"""
    base = root / dev / "ports" / "1"
    for sub in ("gids", "gid_attrs/types", "gid_attrs/ndevs"):
        (base / sub).mkdir(parents=True)
    for i, (gid, typ, ndev) in entries.items():
        (base / "gids" / str(i)).write_text(gid + "\n")
        if typ is not None:
            (base / "gid_attrs/types" / str(i)).write_text(typ + "\n")
            (base / "gid_attrs/ndevs" / str(i)).write_text(ndev + "\n")


ZERO = "0000:0000:0000:0000:0000:0000:0000:0000"
LL = "fe80:0000:0000:0000:0e42:a1ff:fe12:3456"
V4 = "0000:0000:0000:0000:0000:ffff:c0a8:010a"   # ::ffff:192.168.1.10
V6 = "2001:0db8:0000:0000:0000:0000:0000:0001"


def test_selftest(exe, rdma_env):
    assert_ok(run(exe, "--selftest", env=rdma_env), "ALL CHECKS PASSED", "纯函数自测（GID 解析 / IPv4 映射 / 类型）")


def test_fake_sysfs_pick(exe, tmp_path, rdma_env):
    # 典型 ConnectX：每个地址一对 v1/v2 表项；IPv6 的 v2 排在 IPv4 的 v2 前面；中间有空表项
    _fake_port(tmp_path, "mlx5_9", {
        0: (LL, "IB/RoCE v1", "enp1s0"), 1: (LL, "RoCE v2", "enp1s0"),
        2: (V6, "IB/RoCE v1", "enp1s0"), 3: (V6, "RoCE v2", "enp1s0"),
        4: (ZERO, None, ""),
        5: (V4, "IB/RoCE v1", "enp1s0"), 6: (V4, "RoCE v2", "enp1s0"),
    })
    r = run(exe, "--sysfs-root", tmp_path, "mlx5_9", 1, env=rdma_env)
    assert_ok(r, "roce_v2_gid_index=", "扫描假 sysfs")
    assert re.search(r"^roce_v2_gid_index=6$", r.stdout, re.M), (
        "应挑出下标 6：类型为 'RoCE v2' 且 GID 是 IPv4 映射地址（::ffff:a.b.c.d）的表项。"
        "下标 1/3 是 v2 但不是 IPv4，下标 5 是 IPv4 但是 v1\n" + r.stdout)
    assert re.search(r"^gid index=6 gid=::ffff:192\.168\.1\.10 type=roce_v2 ndev=enp1s0$", r.stdout, re.M), (
        "GID 6 应显示为 ::ffff:192.168.1.10（sysfs 的 8 组十六进制 → 16 字节 → inet_ntop）\n" + r.stdout)
    assert "gid index=4 " not in r.stdout, "全 0 的空表项应跳过\n" + r.stdout

    _fake_port(tmp_path / "b", "rxe0", {0: (LL, "IB/RoCE v1", "eth0"), 1: (LL, "RoCE v2", "eth0")})
    r = run(exe, "--sysfs-root", tmp_path / "b", "rxe0", 1, env=rdma_env)
    assert r.returncode == 1 and "roce_v2_gid_index=-1" in r.stdout, (
        "没有 IPv4 的 RoCE v2 GID 时应打印 roce_v2_gid_index=-1 并以 1 退出\n" + r.stdout + r.stderr)


def test_no_device_message(exe, no_rdma_device, rdma_env):
    r = run(exe, env=rdma_env)
    assert r.returncode == 2, f"没有 RDMA 设备时应 exit 2（不是崩溃），实际 {r.returncode}\n{r.stderr}"
    assert "no RDMA device: load rdma_rxe or use ConnectX" in r.stderr, r.stderr


def test_real_device(exe, rdma_dev, rdma_run):
    r = rdma_run(exe, rdma_dev)
    assert_ok(r, f"device={rdma_dev}", f"rdma1_devices {rdma_dev}")
    print(r.stdout)
    ports = re.findall(r"^port=(\d+) state=(\S+) .*link_layer=(\S+)", r.stdout, re.M)
    assert ports, "应至少打印一行 port=..." + r.stdout
    port, state, ll = ports[0]
    assert state == "PORT_ACTIVE", f"{rdma_dev} 端口 {port} 状态 {state}：链路没起来（ip link / rdma link）"
    if ll == "Ethernet":
        idx = int(re.search(r"^roce_v2_gid_index=(-?\d+)$", r.stdout, re.M).group(1))
        types = Path(f"/sys/class/infiniband/{rdma_dev}/ports/{port}/gid_attrs/types/{idx}")
        assert idx >= 0, "以太网端口应能找到 RoCE v2 IPv4 GID（给网卡配 IPv4）"
        assert types.read_text().strip() == "RoCE v2", f"GID {idx} 在 sysfs 里的类型不是 RoCE v2"
