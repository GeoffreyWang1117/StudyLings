import re

import pytest

from studylings.probe import assert_ok, run, start


def test_selftest(exe, rdma_env):
    assert_ok(run(exe, "--selftest", env=rdma_env), "ALL CHECKS PASSED",
              "纯函数自测（MR/QP 访问标志、单边 WR 的 remote_addr/rkey/imm、{addr,rkey} 序列化）")


def test_no_device_message(exe, no_rdma_device, port, rdma_env):
    r = run(exe, "client", "127.0.0.1", port, env=rdma_env)
    assert r.returncode == 2, f"没有 RDMA 设备时应 exit 2（不是崩溃/挂住），实际 {r.returncode}\n{r.stderr}"
    assert "no RDMA device: load rdma_rxe or use ConnectX" in r.stderr, r.stderr


def _session(exe, port, env, server_extra=()):
    with start(exe, "server", port, *server_extra, env=env) as srv:
        m = srv.expect(r"listening on port \d+|no RDMA device", timeout=20)
        if "no RDMA device" in m.group(0):
            pytest.skip("程序报告 no RDMA device（ib_uverbs 没加载？）\n" + srv.describe())
        cli = run(exe, "client", "127.0.0.1", port, "--bulk", 2000, env=env, timeout=120)
        rc = srv.wait(timeout=40)
        return cli, rc, srv.stdout + srv.stderr


def test_write_imm_read_bulk(exe, rdma_dev, port, rdma_env):
    cli, rc, srv_out = _session(exe, port, dict(rdma_env, NETLINGS_RDMA_DEV=rdma_dev))
    if cli.returncode != 0 and "remote access error" in cli.stderr:
        pytest.fail("client 收到 'remote access error'：server 的 MR 没有 IBV_ACCESS_REMOTE_WRITE/READ\n"
                    + cli.stderr, pytrace=False)
    assert_ok(cli, "write ok read ok", "client")
    assert rc == 0, f"server exit {rc}\n{srv_out}"
    assert "server verified imm=0x4e4c3132" in srv_out, "server 应收到 WRITE_WITH_IMM 的完成并校验数据\n" + srv_out
    m = re.search(r"bw_gbps=([\d.]+)", cli.stdout)
    print(cli.stdout)
    assert m and float(m.group(1)) > 0, cli.stdout


def test_remote_access_error_is_reported(exe, rdma_dev, port, rdma_env):
    cli, rc, srv_out = _session(exe, port, dict(rdma_env, NETLINGS_RDMA_DEV=rdma_dev),
                                server_extra=("--no-remote-access",))
    assert cli.returncode != 0, "server 的 MR 没有远端权限，client 的 RDMA WRITE 必须失败\n" + cli.stdout
    assert re.search(r"wc error: remote (access|invalid request) error \(status=\d+\)", cli.stderr), (
        "client 应把失败的完成打印为 'wc error: <ibv_wc_status_str(wc.status)> (status=N) ...'，"
        f"期望 'remote access error'\n--- client stderr ---\n{cli.stderr}")
    assert rc != 0, "server 也应以非 0 退出（它的 RECV 被冲刷或等待超时）\n" + srv_out
