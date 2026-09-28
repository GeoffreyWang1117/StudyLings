import re
import shutil

import pytest

from studylings.netlab import netlab  # noqa: F401  (fixture)
from studylings.probe import assert_ok, run


def _channels(out: str, prefix: str) -> dict[str, int]:
    m = re.search(rf"^{prefix} rx=(\d+) tx=(\d+) other=(\d+) combined=(\d+)$", out, re.M)
    if not m:
        pytest.fail(f"输出里没有形如 '{prefix} rx=R tx=T other=O combined=C' 的行\n{out}", pytrace=False)
    return dict(zip(("rx", "tx", "other", "combined"), map(int, m.groups())))


def test_selftest(exe):
    assert_ok(run(exe, "--selftest"), "ALL CHECKS PASSED", "纯函数自测（间接表分布 / 哈希字段）")


def test_veth_channels(exe, netlab):
    a = netlab.ns("nic2")
    b = netlab.ns("nic2p")
    dev, _ = netlab.link(a, b, "10.72.0.1/24", "10.72.0.2/24")
    want_rx = want_tx = 1
    if shutil.which("ethtool"):
        r = netlab.run(a, "ethtool", "-L", dev, "rx", "2", "tx", "3", check=False)
        if r.returncode == 0:
            want_rx, want_tx = 2, 3
    # 与 sysfs 的队列目录数对照（不依赖 ethtool）
    queues = netlab.run(a, "ls", f"/sys/class/net/{dev}/queues").stdout.split()
    sys_rx = sum(q.startswith("rx-") for q in queues)
    sys_tx = sum(q.startswith("tx-") for q in queues)
    assert (sys_rx, sys_tx) == (want_rx, want_tx), f"测试环境异常：sysfs 队列 {queues}"

    r = netlab.run(a, exe, dev, check=False)
    assert_ok(r, "channels ", "nic2_queues_rss <veth>")
    cur = _channels(r.stdout, "channels")
    mx = _channels(r.stdout, "channels_max")
    assert (cur["rx"], cur["tx"]) == (sys_rx, sys_tx), (
        f"channels rx={cur['rx']} tx={cur['tx']}，而这对 veth 当前有 {sys_rx} 个 RX、{sys_tx} 个 TX 队列"
        "（ETHTOOL_GCHANNELS 的 rx_count/tx_count）")
    assert mx["rx"] >= cur["rx"] and mx["rx"] > 0, f"channels_max rx={mx['rx']}，应 >= 当前值且 > 0"
    for what in ("rss", "rings", "rxfh_tcp4"):
        assert re.search(rf"^{what} unsupported$", r.stdout, re.M), (
            f"veth 不支持 {what}（ioctl 返回 EOPNOTSUPP），应打印 '{what} unsupported' 并继续\n{r.stdout}")


def test_real_connectx_rss(exe, real_iface):
    r = run(exe, real_iface)
    assert_ok(r, "channels ", f"nic2_queues_rss {real_iface}")
    print(r.stdout)
    cur = _channels(r.stdout, "channels")
    assert cur["combined"] > 1, (
        f"combined={cur['combined']}：ConnectX 应有多个 combined 通道（ethtool -L {real_iface} combined N）")
    m = re.search(r"^rss indir_size=(\d+) key_size=(\d+) hfunc=(\S+) key=([0-9a-f]*)$", r.stdout, re.M)
    assert m, f"ConnectX 支持 RSS，应打印 'rss indir_size=N key_size=K hfunc=... key=...'\n{r.stdout}"
    indir_size, key_size = int(m.group(1)), int(m.group(2))
    assert indir_size > 0 and key_size > 0, "间接表 / key 不应为空（ETHTOOL_GRSSH 两步：先取尺寸再取内容）"
    assert len(m.group(4)) == 2 * key_size, "key 的十六进制长度应为 2*key_size"
    used = int(re.search(r"^rss_queues_used=(\d+)$", r.stdout, re.M).group(1))
    nq = cur["combined"] + cur["rx"]
    assert used == nq, (f"间接表只覆盖了 {used}/{nq} 个队列。若是有意配置（ethtool -X {real_iface} equal N）"
                        f"请先恢复默认：ethtool -X {real_iface} default")
    assert re.search(r"^rss_out_of_range=0$", r.stdout, re.M), "间接表里有指向不存在队列的表项"
    assert re.search(r"^rxfh_tcp4 .*ip-src.*ip-dst.*l4-b-0-1.*l4-b-2-3", r.stdout, re.M), (
        "ConnectX 对 TCP4 默认哈希 4 元组（ip-src,ip-dst,l4-b-0-1,l4-b-2-3）")
