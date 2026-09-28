import os
import re
import signal
import subprocess
import sys

import pytest

from studylings.probe import start

N_ICMP, ICMP_PAYLOAD = 24, 56
N_UDP, UDP_PAYLOAD = 40, 200
N_TCP = 8
UDP_PORT, TCP_PORT = 7777, 7778
ETH_IP = 14 + 20

# 在对端 namespace 里运行：发 ICMP echo、UDP、TCP SYN（没人监听 → 对方回 RST），
# 每个包之前把自己迁到下一个 CPU，让 PERCPU map 的各个 CPU 槽都有数据。
SENDER = r"""
import os, socket, struct, sys, time
dst = sys.argv[1]
n_icmp, icmp_payload, n_udp, udp_payload, n_tcp, udp_port, tcp_port = map(int, sys.argv[2:9])
cpus = sorted(os.sched_getaffinity(0))
step = 0
def hop():
    global step
    os.sched_setaffinity(0, {cpus[step % len(cpus)]})
    step += 1
def csum(b):
    if len(b) % 2:
        b += b"\0"
    s = sum(struct.unpack(f"!{len(b)//2}H", b))
    s = (s >> 16) + (s & 0xffff)
    s += s >> 16
    return ~s & 0xffff
icmp = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
for seq in range(n_icmp):
    hop()
    body = bytes(range(icmp_payload))
    hdr = struct.pack("!BBHHH", 8, 0, 0, 0x5151, seq)
    pkt = struct.pack("!BBHHH", 8, 0, csum(hdr + body), 0x5151, seq) + body
    icmp.sendto(pkt, (dst, 0))
    time.sleep(0.004)
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
for i in range(n_udp):
    hop()
    udp.sendto(b"u" * udp_payload, (dst, udp_port))
    time.sleep(0.004)
for i in range(n_tcp):
    hop()
    s = socket.socket()
    s.settimeout(5)
    try:
        s.connect((dst, tcp_port))
    except ConnectionRefusedError:
        pass
    finally:
        s.close()
print("sent", step)
"""

LINE = re.compile(r"^(TCP|UDP|ICMP|OTHER)\s+packets=(\d+)\s+bytes=(\d+)\s*$", re.M)


def _totals(out: str) -> dict:
    return {m[1]: (int(m[2]), int(m[3])) for m in LINE.finditer(out)}


def _wait_ready(p):
    try:
        p.expect(r"^ready", timeout=30)
    except pytest.fail.Exception:
        pytest.fail("loader 没有打印 ready。若 stderr 里有 verifier log（如 \"invalid access to packet\"），"
                    "说明读包头之前缺少与 data_end 的边界检查，验证器拒绝了程序。\n" + p.describe(),
                    pytrace=False)


def _assert_detached(netlab, ns, dev):
    out = netlab.run(ns, "ip", "link", "show", "dev", dev).stdout
    assert "xdp" not in out, f"loader 退出后 {dev} 上还挂着 XDP 程序（应该关闭 bpf_link / detach）：\n{out}"


def _lab(netlab):
    xdp, peer = netlab.ns("xdp"), netlab.ns("peer")
    dev, _ = netlab.link(xdp, peer, "10.77.0.1/24", "10.77.0.2/24")
    return xdp, peer, dev


def test_counts_per_protocol(exe, netlab):
    xdp, peer, dev = _lab(netlab)
    with netlab.start(xdp, exe, dev, 0) as p:
        _wait_ready(p)
        r = netlab.run(peer, sys.executable, "-c", SENDER, "10.77.0.1", N_ICMP, ICMP_PAYLOAD, N_UDP,
                       UDP_PAYLOAD, N_TCP, UDP_PORT, TCP_PORT, timeout=60)
        p.signal(signal.SIGINT)
        rc = p.wait(timeout=15)
        assert rc == 0, f"收到 SIGINT 后应打印统计并 exit 0，实际 exit {rc}\n{p.describe()}"
        _assert_detached(netlab, xdp, dev)

    got = _totals(p.stdout)
    missing = {"TCP", "UDP", "ICMP", "OTHER"} - got.keys()
    assert not missing, f"输出里缺少 {sorted(missing)} 行（格式：\"UDP packets=N bytes=M\"）\n{p.describe()}"
    ncpu = len(os.sched_getaffinity(0))
    want = {
        "ICMP": (N_ICMP, N_ICMP * (ETH_IP + 8 + ICMP_PAYLOAD)),
        "UDP": (N_UDP, N_UDP * (ETH_IP + 8 + UDP_PAYLOAD)),
    }
    for proto, (pk, by) in want.items():
        gp, gb = got[proto]
        if gp != pk:
            hint = ""
            if 0 < gp < pk:
                hint = (f"（偏少：发送方分散在 {ncpu} 个 CPU 上，PERCPU map 每个 CPU 一份，"
                        "用户态必须把 libbpf_num_possible_cpus() 份 value 全部加起来）")
            elif gp == 0:
                hint = "（是 0：协议分类错了？ip->protocol 与 IPPROTO_* 比较了吗？）"
            pytest.fail(f"{proto} 包数 {gp}，应为 {pk}{hint}\n{p.describe()}\n对端输出: {r.stdout}",
                        pytrace=False)
        assert gb == by, (f"{proto} 字节数 {gb}，应为 {by}（每包 = data_end - data，含以太网头）"
                          f"\n{p.describe()}")
    assert got["TCP"][0] == N_TCP, f"TCP 包数 {got['TCP'][0]}，应为 {N_TCP}（每次 connect 一个 SYN）\n{p.describe()}"


def test_duration_argument_exits_and_detaches(exe, netlab):
    xdp, peer, dev = _lab(netlab)
    with netlab.start(xdp, exe, dev, 2) as p:
        _wait_ready(p)
        rc = p.wait(timeout=20)
        assert rc == 0, f"SECONDS=2 时应在约 2 秒后自己退出（exit 0），实际 exit {rc}\n{p.describe()}"
    assert "ICMP" in _totals(p.stdout), f"到时退出时也要打印统计\n{p.describe()}"
    _assert_detached(netlab, xdp, dev)


def test_real_nic_native_mode(exe, bpf_root):
    """可选：真实机器上以 native（drv）模式挂到 ConnectX 网卡，ping 对端，看 ICMP 回包被计数。"""
    iface, peer_ip = os.environ.get("NETLINGS_IFACE"), os.environ.get("NETLINGS_PEER_IP")
    if not iface or not peer_ip:
        pytest.skip("未设置 NETLINGS_IFACE / NETLINGS_PEER_IP：真实网卡 native XDP 测试跳过"
                    "（在 ConnectX 机器上 export NETLINGS_IFACE=enp… NETLINGS_PEER_IP=…）")
    with start(exe, iface, 0, env={"NETLINGS_XDP_MODE": os.environ.get("NETLINGS_XDP_MODE", "drv")}) as p:
        _wait_ready(p)
        subprocess.run(["ping", "-c", "20", "-i", "0.05", "-W", "2", peer_ip], capture_output=True, timeout=30)
        p.signal(signal.SIGINT)
        assert p.wait(timeout=15) == 0, p.describe()
    icmp = _totals(p.stdout).get("ICMP", (0, 0))[0]
    assert icmp >= 20, f"ping 了对端 20 次，ICMP 回包计数只有 {icmp}\n{p.describe()}"
    out = subprocess.run(["ip", "link", "show", "dev", iface], capture_output=True, text=True).stdout
    assert "xdp" not in out, f"退出后 {iface} 上还挂着 XDP：\n{out}"
