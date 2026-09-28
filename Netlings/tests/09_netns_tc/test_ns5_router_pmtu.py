import re

import pytest

PORT = 6000
TOTAL = 200000


@pytest.fixture
def routed(netlab):
    """client ──(10.1.0.0/24, MTU 1500)── router ──(10.2.0.0/24, MTU 1400)── server"""
    cli, rtr, srv = netlab.ns("cli"), netlab.ns("rtr"), netlab.ns("srv")
    netlab.link(cli, rtr, "10.1.0.2/24", "10.1.0.1/24")
    netlab.link(rtr, srv, "10.2.0.1/24", "10.2.0.2/24", mtu=1400)
    netlab.route(cli, "10.2.0.0/24", "10.1.0.1")
    netlab.route(srv, "10.1.0.0/24", "10.2.0.1")
    netlab.forwarding(rtr)
    return netlab, cli, srv


def test_pmtu_discovery_through_router(exe, routed):
    lab, cli, srv = routed
    with lab.start(srv, exe, "server", PORT) as s:
        s.expect(r"listening on port", timeout=10)
        r = lab.run(cli, exe, "client", "10.2.0.2", PORT, TOTAL, timeout=60, check=False)
        got = None
        if r.returncode == 0:
            got = s.expect(r"received (\d+) bytes", timeout=10)
    out = f"--- stdout ---\n{r.stdout}\n--- stderr ---\n{r.stderr}"
    if r.returncode != 0:
        pytest.fail(f"客户端 exit {r.returncode}。第一个 1500 字节的数据报被 router 丢弃并回了 ICMP "
                    f"Fragmentation Needed，之后 send/recv 会得到 EMSGSIZE —— 要读 IP_MTU 重新切片再重发。\n{out}",
                    pytrace=False)
    m = re.search(r"path_mtu=(-?\d+)", r.stdout)
    assert m, f"应打印 path_mtu=<n>\n{out}"
    assert int(m.group(1)) == 1400, f"路径上最小的 MTU 是 1400，getsockopt(IP_MTU) 应读到 1400，实际 {m.group(1)}\n{out}"
    d = re.search(r"delivered (\d+)", r.stdout)
    assert d and int(d.group(1)) == TOTAL, f"应全部送达 delivered {TOTAL}\n{out}"
    assert int(got.group(1)) == TOTAL, f"服务器应收到 {TOTAL} 字节，实际 {got.group(1)}"

    # 独立核对：客户端内核的路由缓存里记下了 router 通过 ICMP 告知的 PMTU。
    rg = lab.run(cli, "ip", "route", "get", "10.2.0.2").stdout
    assert re.search(r"\bmtu 1400\b", rg), (
        f"客户端的路由缓存里应出现 'mtu 1400'（来自 router 的 ICMP Fragmentation Needed）。"
        f"如果你一开始就硬编码了小包，就没有真正做 PMTU 发现：\n{rg}")
