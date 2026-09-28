import os
import re
import signal

import pytest

from studylings.probe import run, start

SECONDS = 1.5


def _kv(line: str) -> dict[str, float]:
    return {k: float(v) for k, v in re.findall(r"(\w+)=([\d.]+)", line)}


def _session(exe, port, send_flags=(), recv_flags=()):
    with start(exe, "recv", port, "--bind", "127.0.0.1", *recv_flags) as rx:
        rx.expect(r"listening on port \d+", timeout=10)
        s = run(exe, "send", "127.0.0.1", port, SECONDS, *send_flags, timeout=60)
        if s.returncode != 0:
            pytest.fail(f"发送端 exit {s.returncode}\n--- stdout ---\n{s.stdout}\n--- stderr ---\n{s.stderr}",
                        pytrace=False)
        m = re.search(r"^sent .*$", s.stdout, re.M)
        assert m, f"发送端应打印 'sent bytes=... datagrams=...'\n{s.stdout}"
        sent = _kv(m.group(0))
        try:
            got = rx.expect(r"^recv .*", timeout=15).group(0)
        except BaseException:
            rx.signal(signal.SIGTERM)
            raise
        assert rx.wait(timeout=10) == 0, "接收端收到 END 后应 exit 0\n" + rx.describe()
    return sent, _kv(got), s.stdout + "\n" + rx.stdout


def _check(sent, recv, out, what):
    assert sent["datagrams"] > 0 and sent["syscalls"] > 0, f"{what}: 发送端一个包也没发出去\n{out}"
    assert sent["refused"] == 0, f"{what}: 发送时收到 ECONNREFUSED（接收端没在监听？）\n{out}"
    assert recv["bad"] == 0, f"{what}: 接收端发现 {int(recv['bad'])} 个头部损坏/截断的数据报\n{out}"
    assert recv["sender_datagrams"] == sent["datagrams"], (
        f"{what}: 接收端从 END 包里读到 sender_datagrams={int(recv['sender_datagrams'])}，"
        f"发送端报告 datagrams={int(sent['datagrams'])}\n{out}")
    assert recv["datagrams"] <= sent["datagrams"], f"{what}: 收到的数据报比发出的还多（计数错误）\n{out}"
    ratio = recv["datagrams"] / sent["datagrams"]
    assert ratio >= 0.2, (
        f"{what}: 只收到 {ratio:.1%} 的数据报（{int(recv['datagrams'])}/{int(sent['datagrams'])}）。"
        "loopback 上允许少量丢包，但丢这么多说明发送的不是一个个 1472 字节的数据报"
        "（UDP_SEGMENT 没设？），或者接收端没有按 GRO 段大小切分计数\n" + out)


def test_plain_sendmmsg(exe, udp_port):
    sent, recv, out = _session(exe, udp_port)
    _check(sent, recv, out, "sendmmsg")
    assert "gso=off" in out
    assert sent["datagrams"] / sent["syscalls"] > 8, (
        f"平均每次系统调用只发了 {sent['datagrams'] / sent['syscalls']:.1f} 个数据报，sendmmsg 应一次发一批\n{out}")


def test_gso(exe, udp_port):
    sent, recv, out = _session(exe, udp_port, send_flags=("--gso",))
    _check(sent, recv, out, "--gso")
    assert sent["datagrams"] / sent["syscalls"] > 44, (
        f"--gso 时每次 sendmmsg 应交出多个 44 段的超级包（实际平均 {sent['datagrams'] / sent['syscalls']:.1f} 个数据报/调用）\n{out}")


def test_gso_gro(exe, udp_port):
    sent, recv, out = _session(exe, udp_port, send_flags=("--gso",), recv_flags=("--gro",))
    _check(sent, recv, out, "--gso + --gro")
    assert recv["gro_batches"] > 0, (
        "开了 UDP_GRO 后 loopback 上会直接收到合并的大 buffer（cmsg 里有 gso_size），gro_batches 应 > 0\n" + out)


def test_real_peer_throughput(exe):
    peer = os.environ.get("NETLINGS_PEER_IP")
    if not peer:
        pytest.skip("未设置 NETLINGS_PEER_IP：25G 双机吞吐只在真实机器上报告。对端先运行 "
                    "`nic5_udp_gso_throughput recv 5201 --gro`，本机 export NETLINGS_PEER_IP=<对端 IP>")
    port = os.environ.get("NETLINGS_PEER_PORT", "5201")
    for flags in ((), ("--gso",)):
        r = run(exe, "send", peer, port, 5, *flags, timeout=60)
        print(r.stdout, r.stderr)
        assert r.returncode == 0, f"发送失败：{r.stderr}"
        assert "refused=0" in r.stdout, f"对端 {peer}:{port} 没有在运行 recv（ECONNREFUSED）\n{r.stdout}"
