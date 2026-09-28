import re
from pathlib import Path

import pytest

from studylings.netlab import netlab  # noqa: F401  (fixture)
from studylings.probe import assert_ok, run

BUS = "0000:41:00.0"


def _cpulist(s: str) -> set[int]:
    out: set[int] = set()
    for part in s.strip().split(","):
        if part:
            lo, _, hi = part.partition("-")
            out.update(range(int(lo), int(hi or lo) + 1))
    return out


def _plan_lines(out: str) -> list[dict]:
    rx = re.compile(r"^irq=(\d+) name=(\S+) queue=(\d+) current=(\S+) plan=(\d+)$", re.M)
    return [dict(irq=int(m[1]), name=m[2], queue=int(m[3]), current=m[4], plan=int(m[5])) for m in rx.finditer(out)]


def _fake_root(tmp: Path, nq: int, local: str) -> Path:
    """合成一台"有 ConnectX 的机器"：msi_irqs、numa_node、local_cpulist、/proc/interrupts、/proc/irq/N/。"""
    dev = tmp / "sys/class/net/fake0/device"
    (dev / "msi_irqs").mkdir(parents=True)
    (dev / "numa_node").write_text("1\n")
    (dev / "local_cpulist").write_text(local + "\n")
    lines = ["            CPU0       CPU1       CPU2       CPU3"]
    irqs = [100]  # mlx5_async0：不是数据队列
    lines.append(f" 100:  0  0  0  0  IR-PCI-MSIX-{BUS}  0-edge  mlx5_async0@pci:{BUS}")
    for q in reversed(range(nq)):  # 倒序写入，程序应按队列号排序
        irq = 101 + q
        irqs.append(irq)
        lines.append(f" {irq}:  {q}  0  0  0  IR-PCI-MSIX-{BUS}  {q + 1}-edge  mlx5_comp{q}@pci:{BUS}")
    lines.append(" 300:  0  0  0  0  IR-PCI-MSIX-0000:42:00.0  1-edge  mlx5_comp0@pci:0000:42:00.0")  # 别的卡
    lines.append(" NMI:  0  0  0  0  Non-maskable interrupts")
    (tmp / "proc").mkdir()
    (tmp / "proc/interrupts").write_text("\n".join(lines) + "\n")
    for irq in irqs:
        (dev / "msi_irqs" / str(irq)).write_text("msix\n")
    for irq in irqs + [300]:
        d = tmp / f"proc/irq/{irq}"
        d.mkdir(parents=True)
        (d / "smp_affinity_list").write_text("0-63\n")
    return tmp


def test_selftest(exe):
    assert_ok(run(exe, "--selftest"), "ALL CHECKS PASSED", "纯函数自测（cpulist / 中断名 / /proc/interrupts / 方案）")


def test_fake_machine_plan_and_apply(exe, tmp_path):
    root = _fake_root(tmp_path, nq=6, local="8-11,40")
    env = {"NETLINGS_NIC4_ROOT": str(root)}
    r = run(exe, "fake0", env=env)
    assert_ok(r, "plan_irqs=", "nic4_irq_affinity_plan（合成的 sysfs/procfs）")
    assert re.search(r"^iface=fake0 numa_node=1 local_cpus=8-11,40 nlocal=5 ", r.stdout, re.M), (
        "第一行应为 'iface=fake0 numa_node=1 local_cpus=8-11,40 nlocal=5 ...'\n" + r.stdout)
    plan = _plan_lines(r.stdout)
    assert [p["queue"] for p in plan] == list(range(6)), (
        "方案应只包含 mlx5_comp0..5（不含 mlx5_async、不含别的 PCI 设备的中断），并按队列号排序\n" + r.stdout)
    local = [8, 9, 10, 11, 40]
    for p in plan:
        assert p["irq"] == 101 + p["queue"], f"队列 {p['queue']} 的中断号应为 {101 + p['queue']}\n{r.stdout}"
        assert p["plan"] == local[p["queue"] % 5], (
            f"队列 {p['queue']} → CPU {p['plan']}，应为 local_cpus[{p['queue']} % 5] = {local[p['queue'] % 5]}")
        assert p["current"] == "0-63"
    assert "plan_irqs=6" in r.stdout
    assert "echo 8 > /proc/irq/101/smp_affinity_list" in r.stdout, "应打印可以直接执行的 echo 命令\n" + r.stdout

    r = run(exe, "fake0", "--apply", env=env)
    assert_ok(r, "applied=6 failed=0", "--apply（写入假根目录）")
    for q in range(6):
        got = (root / f"proc/irq/{101 + q}/smp_affinity_list").read_text().strip()
        assert got == str(local[q % 5]), f"--apply 后 /proc/irq/{101 + q}/smp_affinity_list = {got!r}"
    assert (root / "proc/irq/100/smp_affinity_list").read_text().strip() == "0-63", "mlx5_async 不应被改动"


def test_veth_has_no_irqs(exe, netlab):
    a = netlab.ns("nic4")
    b = netlab.ns("nic4p")
    dev, _ = netlab.link(a, b)
    r = netlab.run(a, exe, dev, check=False)
    assert r.returncode == 2, f"veth 没有 msi_irqs，应以 exit 2 报错，实际 {r.returncode}\n{r.stdout}{r.stderr}"
    assert "msi_irqs" in r.stderr, f"错误信息应说明缺少 device/msi_irqs：{r.stderr!r}"


def test_real_connectx_plan(exe, real_iface):
    dev = Path(f"/sys/class/net/{real_iface}/device")
    if not (dev / "msi_irqs").is_dir():
        pytest.skip(f"{real_iface} 没有 device/msi_irqs（不是 PCI 网卡？）")
    bus = dev.resolve().name
    r = run(exe, real_iface)
    assert_ok(r, "plan_irqs=", f"nic4_irq_affinity_plan {real_iface}")
    print(r.stdout)
    comp = [l for l in Path("/proc/interrupts").read_text().splitlines()
            if re.search(rf"mlx5_comp\d+@pci:{re.escape(bus)}\s*$", l)]
    plan = _plan_lines(r.stdout)
    assert len(plan) == len(comp) > 0, (
        f"/proc/interrupts 里 {bus} 有 {len(comp)} 个 mlx5_comp 中断，方案里有 {len(plan)} 个")
    local = _cpulist((dev / "local_cpulist").read_text())
    for p in plan:
        assert p["plan"] in local, f"irq {p['irq']} 被安排到 CPU {p['plan']}，不在本地 CPU {sorted(local)} 里"
    assert len({p["queue"] for p in plan}) == len(plan), "队列号不应重复"
