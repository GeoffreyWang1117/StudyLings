import re
import signal
import sys

import pytest

BLOCKED = 9000     # 0x2328
ALLOWED = 10275    # 0x2823 —— BLOCKED 的字节交换：忘了 bpf_ntohs 就会封错端口
N = 30

# 防火墙所在 namespace 里的 UDP 服务器：同时收两个端口，直到放行端口收到 END（或超时）
SERVER = r"""
import selectors, socket, sys, time
ports = [int(a) for a in sys.argv[1:]]
sel = selectors.DefaultSelector()
counts = {}
for p in ports:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", p))
    sel.register(s, selectors.EVENT_READ, p)
    counts[p] = 0
print("server ready", flush=True)
deadline = time.monotonic() + 10
done = False
while not done and time.monotonic() < deadline:
    for key, _ in sel.select(timeout=0.2):
        data = key.fileobj.recv(2048)
        if data == b"END":
            done = True
        else:
            counts[key.data] += 1
for p in ports:
    print(f"recv {p} {counts[p]}", flush=True)
print("end seen" if done else "end missing", flush=True)
"""

CLIENT = r"""
import socket, sys, time
dst, blocked, allowed, n = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
for i in range(n):
    s.sendto(b"to-blocked %d" % i, (dst, blocked))
    s.sendto(b"to-allowed %d" % i, (dst, allowed))
    time.sleep(0.005)
time.sleep(0.2)
for _ in range(3):
    s.sendto(b"END", (dst, allowed))
    time.sleep(0.05)
"""


def test_blocks_only_listed_port(exe, netlab):
    fw, cli = netlab.ns("fw"), netlab.ns("cli")
    dev, _ = netlab.link(fw, cli, "10.78.0.1/24", "10.78.0.2/24")

    with netlab.start(fw, exe, dev, BLOCKED) as p:
        try:
            p.expect(r"^ready", timeout=30)
        except pytest.fail.Exception:
            pytest.fail("loader 没有打印 ready（加载/挂载失败？看 stderr 里的 verifier log）\n" + p.describe(),
                        pytrace=False)
        with netlab.start(fw, sys.executable, "-c", SERVER, BLOCKED, ALLOWED) as srv:
            srv.expect(r"server ready", timeout=15)
            netlab.run(cli, sys.executable, "-c", CLIENT, "10.78.0.1", BLOCKED, ALLOWED, N, timeout=60)
            assert srv.wait(timeout=30) == 0, srv.describe()
        p.signal(signal.SIGINT)
        rc = p.wait(timeout=15)
        assert rc == 0, f"收到 SIGINT 后应 detach、打印统计并 exit 0，实际 exit {rc}\n{p.describe()}"

    link = netlab.run(fw, "ip", "link", "show", "dev", dev).stdout
    assert "xdp" not in link, f"loader 退出后 {dev} 上还挂着 XDP 程序：\n{link}"

    recv = {int(m[1]): int(m[2]) for m in re.finditer(r"recv (\d+) (\d+)", srv.stdout)}
    got_blocked, got_allowed = recv.get(BLOCKED, -1), recv.get(ALLOWED, -1)
    if got_allowed == 0 and got_blocked == N:
        pytest.fail(f"封错了端口：{BLOCKED} 全部送达，而 {ALLOWED}（= {BLOCKED} 的字节交换 "
                    f"0x{ALLOWED:04x}/0x{BLOCKED:04x}）一个都没收到。udp->dest 是网络字节序，"
                    "和主机序的 map key 比较之前要 bpf_ntohs()", pytrace=False)
    assert got_blocked == 0, (f"被封端口 {BLOCKED} 仍收到 {got_blocked}/{N} 个包：XDP 程序没有 XDP_DROP 它们"
                              f"（端口比较/字节序/map key 类型？）\n{p.describe()}")
    assert got_allowed == N, (f"放行端口 {ALLOWED} 只收到 {got_allowed}/{N} 个包：不在黑名单里的包应 XDP_PASS"
                              f"\n{p.describe()}\n服务器: {srv.stdout}")

    m = re.search(rf"port {BLOCKED} dropped (\d+)", p.stdout)
    t = re.search(r"total dropped (\d+)", p.stdout)
    assert m and t, f"输出里缺少 \"port {BLOCKED} dropped N\" / \"total dropped N\"\n{p.describe()}"
    assert int(m[1]) == N and int(t[1]) == N, (
        f"丢弃计数应恰好为 {N}（每丢一个包 map value 原子 +1），实际 port={m[1]} total={t[1]}\n{p.describe()}")
