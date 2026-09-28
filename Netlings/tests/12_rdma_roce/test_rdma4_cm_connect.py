import re

import pytest

from studylings.probe import assert_ok, run, start


def test_selftest(exe, rdma_env):
    assert_ok(run(exe, "--selftest", env=rdma_env), "ALL CHECKS PASSED",
              "纯函数自测（CM 事件 → 下一步动作，尤其 ROUTE_RESOLVED → connect；私有数据编解码）")


def test_no_device_message(exe, no_rdma_device, port, rdma_env):
    r = run(exe, "client", "127.0.0.1", port, env=rdma_env)
    assert r.returncode == 2, f"没有 RDMA 设备时应 exit 2（不是崩溃/挂住），实际 {r.returncode}\n{r.stderr}"
    assert "no RDMA device: load rdma_rxe or use ConnectX" in r.stderr, r.stderr


def test_cm_pingpong(exe, rdma_dev, rdma_ipv4, port, rdma_env):
    env = dict(rdma_env, NETLINGS_RDMA_DEV=rdma_dev)
    with start(exe, "server", port, "--iters", 500, env=env) as srv:
        m = srv.expect(r"listening on port \d+|no RDMA device", timeout=20)
        if "no RDMA device" in m.group(0):
            pytest.skip("程序报告 no RDMA device\n" + srv.describe())
        cli = run(exe, "client", rdma_ipv4, port, "--iters", 500, env=env, timeout=120)
        rc = srv.wait(timeout=30)
        if cli.returncode != 0 and "等待 CM 事件超时" in cli.stderr:
            pytest.fail("client 等 CM 事件超时：ADDR_RESOLVED 之后要 rdma_resolve_route，"
                        "ROUTE_RESOLVED 之后要建 QP 并 rdma_connect\n" + cli.stderr, pytrace=False)
        assert_ok(cli, "avg_rtt_us=", f"client {rdma_ipv4}:{port}")
        assert rc == 0, "server 应在 DISCONNECTED 后 exit 0\n" + srv.describe()
    assert "connected: server hello version=1 msg_size=64" in cli.stdout, "client 应解析出 server 的私有数据\n" + cli.stdout
    assert "connect request: client hello version=1" in srv.stdout, "server 应解析出 client 的私有数据\n" + srv.stdout
    assert "server done iters=500" in srv.stdout, srv.stdout
    print(cli.stdout)
    assert re.search(r"iters=500 size=64 avg_rtt_us=[\d.]+", cli.stdout)
