import os
import re
import signal
import subprocess
import sys

import pytest

from studylings.probe import start

PAYLOAD = 1000
FRAME = PAYLOAD + 8 + 20 + 14   # UDP + IPv4 + Ethernet
N_BIG, N_SMALL = 300, 100
BIG, SMALL = "10.79.0.2", "10.79.0.3"
PORT = 5555

SENDER = r"""
import socket, sys, time
payload, port = int(sys.argv[1]), int(sys.argv[2])
plan = [(sys.argv[i], int(sys.argv[i + 1])) for i in range(3, len(sys.argv), 2)]
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
left = dict(plan)
while any(left.values()):
    for dst in left:
        if left[dst]:
            s.sendto(b"t" * payload, (dst, port))
            left[dst] -= 1
    time.sleep(0.002)
print("sent")
"""

# 在对端数收到的包，证明 tc 程序放行了流量（TC_ACT_OK），而不是丢掉
RECEIVER = r"""
import selectors, socket, sys, time
sel = selectors.DefaultSelector()
counts = {}
for a in sys.argv[2:]:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((a, int(sys.argv[1])))
    sel.register(s, selectors.EVENT_READ, a)
    counts[a] = 0
print("receiver ready", flush=True)
deadline = time.monotonic() + 8
idle_until = None
while time.monotonic() < deadline:
    ev = sel.select(timeout=0.2)
    for key, _ in ev:
        key.fileobj.recv(4096)
        counts[key.data] += 1
    if sum(counts.values()) and not ev:
        idle_until = idle_until or time.monotonic() + 1.0
        if time.monotonic() > idle_until:
            break
    elif ev:
        idle_until = None
for a, n in counts.items():
    print(f"got {a} {n}", flush=True)
"""

ROW = re.compile(r"^(\d+\.\d+\.\d+\.\d+) bytes=(\d+) packets=(\d+)\s*$", re.M)


def _rows(out):
    return [(m[1], int(m[2]), int(m[3])) for m in ROW.finditer(out)]


def _wait_ready(p):
    try:
        p.expect(r"^ready", timeout=30)
    except pytest.fail.Exception:
        pytest.fail("loader 没有打印 ready（加载 / bpf_tc_hook_create / bpf_tc_attach 失败？看 stderr）\n"
                    + p.describe(), pytrace=False)


def test_top_talkers(exe, netlab):
    src, dst = netlab.ns("src"), netlab.ns("dst")
    dev, peer_dev = netlab.link(src, dst, "10.79.0.1/24", BIG + "/24")
    netlab.run(dst, "ip", "addr", "add", SMALL + "/24", "dev", peer_dev)

    with netlab.start(src, exe, dev, 0) as p:
        _wait_ready(p)
        with netlab.start(dst, sys.executable, "-c", RECEIVER, PORT, BIG, SMALL) as rcv:
            rcv.expect("receiver ready", timeout=15)
            netlab.run(src, sys.executable, "-c", SENDER, PAYLOAD, PORT, BIG, N_BIG, SMALL, N_SMALL, timeout=60)
            rcv.wait(timeout=30)
        p.signal(signal.SIGINT)
        rc = p.wait(timeout=15)
        assert rc == 0, f"收到 SIGINT 后应 detach、打印排行并 exit 0，实际 exit {rc}\n{p.describe()}"

    filt = netlab.run(src, "tc", "filter", "show", "dev", dev, "egress").stdout
    assert "bpf" not in filt, f"loader 退出后 {dev} egress 上还残留 bpf 过滤器（bpf_tc_detach）：\n{filt}"
    qd = netlab.run(src, "tc", "qdisc", "show", "dev", dev).stdout
    assert "clsact" not in qd, f"clsact qdisc 是 loader 自己创建的，退出时应删除（bpf_tc_hook_destroy）：\n{qd}"

    got = {m[1]: int(m[2]) for m in re.finditer(r"got (\S+) (\d+)", rcv.stdout)}
    if got.get(BIG, 0) < N_BIG * 0.9 or got.get(SMALL, 0) < N_SMALL * 0.9:
        pytest.fail(f"对端几乎没收到包（{got}）：tc 程序把流量丢了？只统计的程序应返回 TC_ACT_OK，"
                    f"TC_ACT_SHOT 会丢弃包（连 ARP 也丢，邻居都解析不了）\n{p.describe()}", pytrace=False)

    rows = _rows(p.stdout)
    assert "top talkers:" in p.stdout and rows, f"输出里没有 \"top talkers:\" 和 \"IP bytes=N packets=M\" 行\n{p.describe()}"
    table = {ip: (b, n) for ip, b, n in rows}
    if "10.79.0.1" in table and BIG not in table:
        pytest.fail(f"统计的 key 是本机源地址 10.79.0.1 —— 要按**目的**地址（ip->daddr）统计\n{p.describe()}",
                    pytrace=False)
    for ip, n in ((BIG, N_BIG), (SMALL, N_SMALL)):
        assert ip in table, f"排行里没有 {ip}\n{p.describe()}"
        b, k = table[ip]
        assert k == n and b == n * FRAME, (f"{ip}: bytes={b} packets={k}，应为 bytes={n * FRAME} packets={n}"
                                           f"（skb->len 含以太网头）\n{p.describe()}")
    assert rows[0][0] == BIG, f"排行应按字节数降序，第一名应是 {BIG}，实际是 {rows[0][0]}\n{p.describe()}"


def test_real_nic_egress(exe, bpf_root):
    """可选：真实机器上挂到 ConnectX 网卡 egress，向对端发 UDP，检查对端地址的计数。"""
    iface, peer_ip = os.environ.get("NETLINGS_IFACE"), os.environ.get("NETLINGS_PEER_IP")
    if not iface or not peer_ip:
        pytest.skip("未设置 NETLINGS_IFACE / NETLINGS_PEER_IP：真实网卡 tc egress 测试跳过")
    with start(exe, iface, 0) as p:
        _wait_ready(p)
        subprocess.run([sys.executable, "-c", SENDER, str(PAYLOAD), str(PORT), peer_ip, "200"], capture_output=True, timeout=60)
        p.signal(signal.SIGINT)
        assert p.wait(timeout=15) == 0, p.describe()
    table = {ip: (b, n) for ip, b, n in _rows(p.stdout)}
    assert peer_ip in table and table[peer_ip][1] >= 200, f"对端 {peer_ip} 的计数不足 200 包\n{p.describe()}"
    filt = subprocess.run(["tc", "filter", "show", "dev", iface, "egress"], capture_output=True, text=True).stdout
    assert "tc_egress" not in filt, f"退出后 {iface} egress 上还残留过滤器：\n{filt}"
