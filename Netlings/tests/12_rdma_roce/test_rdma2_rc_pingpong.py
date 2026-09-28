import re

import pytest

from studylings.probe import assert_ok, run, start


def test_selftest(exe, rdma_env):
    assert_ok(run(exe, "--selftest", env=rdma_env), "ALL CHECKS PASSED",
              "纯函数自测（INIT/RTR/RTS 的 attr 与 attr_mask、连接信息序列化）")


def test_no_device_message(exe, no_rdma_device, port, rdma_env):
    r = run(exe, "server", port, env=rdma_env)
    assert r.returncode == 2, f"没有 RDMA 设备时应 exit 2（不是崩溃/挂住），实际 {r.returncode}\n{r.stderr}"
    assert "no RDMA device: load rdma_rxe or use ConnectX" in r.stderr, r.stderr


def _pingpong(exe, port, env, iters, *extra):
    with start(exe, "server", port, "--iters", iters, *extra, env=env) as srv:
        m = srv.expect(r"listening on port \d+|no RDMA device", timeout=20)
        if "no RDMA device" in m.group(0):
            pytest.skip("程序报告 no RDMA device（ib_uverbs 没加载？）\n" + srv.describe())
        cli = run(exe, "client", "127.0.0.1", port, "--iters", iters, *extra, env=env, timeout=120)
        rc = srv.wait(timeout=30)
        assert_ok(cli, "avg_rtt_us=", "client")
        assert rc == 0, f"server exit {rc}\n" + srv.describe()
        assert f"server done iters={iters}" in srv.stdout, srv.describe()
    m = re.search(r"iters=(\d+) size=\d+ avg_rtt_us=([\d.]+) avg_lat_us=([\d.]+)", cli.stdout)
    assert m and int(m.group(1)) == iters, cli.stdout
    print(cli.stdout)
    return float(m.group(3))


def test_pingpong_busy_poll(exe, rdma_dev, port, rdma_env):
    lat = _pingpong(exe, port, dict(rdma_env, NETLINGS_RDMA_DEV=rdma_dev), 1000)
    assert lat > 0


def test_pingpong_events(exe, rdma_dev, port, rdma_env):
    lat = _pingpong(exe, port, dict(rdma_env, NETLINGS_RDMA_DEV=rdma_dev), 200, "--events")
    assert lat > 0
