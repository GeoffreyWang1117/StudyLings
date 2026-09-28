import re
import statistics

import pytest


SRV_IP = "10.9.0.2"  # 见 conftest.py 的 pair fixture
PORT = 5201  # 每个用例都是全新的 netns，固定端口不会冲突
SECONDS = 3

SAMPLE_RX = re.compile(r"t=([0-9.]+) rtt_us=(\d+) cwnd=(\d+) retrans=(\d+) "
                       r"delivery_mbps=([0-9.]+) pacing_mbps=([0-9.]+) acked=(\d+)")
SUMMARY_RX = re.compile(r"goodput_mbps=([0-9.]+) retrans=(\d+)")


def _transfer(exe, pair, seconds=SECONDS):
    lab, cli, srv, _ = pair
    with lab.start(srv, exe, "server", PORT) as s:
        s.expect(r"listening on port", timeout=10)
        r = lab.run(cli, exe, "client", SRV_IP, PORT, seconds, timeout=seconds + 30, check=False)
    if r.returncode != 0:
        pytest.fail(f"客户端 exit {r.returncode}\n--- stdout ---\n{r.stdout}\n--- stderr ---\n{r.stderr}",
                    pytrace=False)
    samples = [dict(zip(("t", "rtt", "cwnd", "retrans", "deliv", "pacing", "acked"),
                        map(float, m.groups()))) for m in SAMPLE_RX.finditer(r.stdout)]
    m = SUMMARY_RX.search(r.stdout)
    assert m, f"最后应打印 goodput_mbps=<x> retrans=<n>，实际输出：\n{r.stdout}"
    assert len(samples) >= seconds * 3, (
        f"{seconds} 秒内应每 200ms 打印一行采样（至少 {seconds * 3} 行），实际 {len(samples)} 行：\n{r.stdout}")
    return samples, float(m.group(1)), int(m.group(2)), r.stdout


def test_tcp_info_under_tbf_bottleneck(exe, pair):
    lab, cli, srv, dev = pair
    lab.qdisc(cli, dev, "tbf rate 50mbit burst 32kbit latency 50ms")
    samples, goodput, _, out = _transfer(exe, pair)

    later = samples[len(samples) // 2:]
    assert all(s["rtt"] > 0 for s in later), f"rtt_us 应为正数（tcpi_rtt，单位微秒）：\n{out}"
    assert all(s["cwnd"] >= 2 for s in later), f"cwnd 应 >= 2 个段（tcpi_snd_cwnd）：\n{out}"
    assert any(s["pacing"] > 0 for s in later), f"pacing_mbps 应为正（tcpi_pacing_rate 字节/秒 → Mbit/s）：\n{out}"
    assert later[-1]["acked"] > later[0]["acked"] > 0, f"acked（tcpi_bytes_acked）应持续增长：\n{out}"
    deliv = statistics.median(s["deliv"] for s in later)
    assert 10 <= deliv <= 70, (
        f"瓶颈是 tbf 50mbit，交付速率中位数应在 10~70 Mbit/s，实际 {deliv:.1f}"
        f"（tcpi_delivery_rate 单位是 字节/秒，别忘了 ×8/1e6）：\n{out}")
    assert 30 <= goodput <= 60, (
        f"tbf 50mbit 下 goodput 应在 30~60 Mbit/s，实际 {goodput:.1f}。"
        f"goodput 要用对端确认的字节数（tcpi_bytes_acked）/ 时间 计算：\n{out}")


def test_rtt_reflects_netem_delay(exe, pair, need_netem):
    """真实机器：单向 40ms 延迟 → 平滑 RTT >= 40ms。"""
    lab, cli, srv, dev = pair
    lab.qdisc(cli, dev, "netem delay 40ms rate 50mbit limit 10000")
    samples, _, _, out = _transfer(exe, pair)
    later = samples[len(samples) // 2:]
    rtt = statistics.median(s["rtt"] for s in later)
    assert rtt >= 40000, f"加了 40ms 单向延迟，rtt_us 中位数应 >= 40000，实际 {rtt:.0f}：\n{out}"


def test_retrans_reflects_netem_loss(exe, pair, need_netem):
    """真实机器：1% 随机丢包 → 3 秒内必然有重传。"""
    lab, cli, srv, dev = pair
    lab.qdisc(cli, dev, "netem delay 5ms loss 1% rate 100mbit limit 10000")
    _, _, retrans, out = _transfer(exe, pair)
    assert retrans > 0, f"1% 丢包下 retrans（tcpi_total_retrans）应 > 0，实际 {retrans}：\n{out}"
