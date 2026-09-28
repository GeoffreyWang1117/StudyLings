import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

from studylings.probe import free_port, run, start

SRV_IP = "10.9.0.2"  # 见 conftest.py 的 pair fixture
NS_PORT = 5202


def _available() -> set[str]:
    p = Path("/proc/sys/net/ipv4/tcp_available_congestion_control")
    return set(p.read_text().split()) if p.exists() else set()


def _allowed() -> set[str]:
    p = Path("/proc/sys/net/ipv4/tcp_allowed_congestion_control")
    return set(p.read_text().split()) if p.exists() else set()


def _need(algo: str):
    if algo not in _available():
        r = subprocess.run(["modprobe", f"tcp_{algo}"], capture_output=True)
        if r.returncode != 0 and algo not in _available():
            pytest.skip(f"内核没有 {algo} 拥塞控制模块：真实机器上 sudo modprobe tcp_{algo}")
    if os.geteuid() != 0 and algo not in _allowed():
        pytest.skip(f"非 root 只能用 net.ipv4.tcp_allowed_congestion_control 里的算法（{sorted(_allowed())}）；"
                    f"用 sudo 运行，或 sysctl -w net.ipv4.tcp_allowed_congestion_control='... {algo}'")


def _ss_algo(port: int) -> str | None:
    """从外部（ss -tin）看这条连接实际用的拥塞控制算法。"""
    if shutil.which("ss") is None:
        return None
    out = subprocess.run(["ss", "-tinH", "state", "established", f"( dport = :{port} )"],
                         capture_output=True, text=True, timeout=10).stdout
    lines = out.splitlines()
    for i, ln in enumerate(lines):
        if f":{port}" in ln and i + 1 < len(lines):
            words = lines[i + 1].split()
            if words:
                return words[0]
    return None


@pytest.mark.parametrize("algo", ["bbr", "cubic"])
def test_per_socket_algorithm(exe, algo):
    _need(algo)
    port = free_port()
    with start(exe, "server", port) as srv:
        srv.expect(r"listening on port", timeout=10)
        with start(exe, "client", "127.0.0.1", port, 2, algo) as cli:
            m = cli.expect(r"algo=(\S+)", timeout=10)
            seen_by_ss = _ss_algo(port)
            rc = cli.wait(timeout=20)
        assert rc == 0, f"客户端 exit {rc}\n{cli.describe()}"
    assert m.group(1) == algo, (
        f"请求 {algo}，getsockopt(TCP_CONGESTION) 读回的却是 {m.group(1)!r} —— setsockopt 没生效"
        f"（level 用对了吗？返回值检查了吗？）")
    if seen_by_ss is not None:
        assert seen_by_ss == algo, f"`ss -tin` 看到这条连接用的是 {seen_by_ss!r}，而不是 {algo}"
    assert "goodput_mbps=" in cli.stdout, f"最后应打印 goodput_mbps=<x>\n{cli.describe()}"


def test_unknown_algorithm_reports_enoent(exe):
    port = free_port()
    with start(exe, "server", port) as srv:  # 有服务器在听：失败只能来自 TCP_CONGESTION 本身
        srv.expect(r"listening on port", timeout=10)
        r = run(exe, "client", "127.0.0.1", port, 1, "no_such_cc", timeout=20)
    assert r.returncode != 0, (
        f"请求不存在的算法 no_such_cc 必须失败（setsockopt 返回 ENOENT），程序却 exit 0：\n{r.stdout}{r.stderr}")
    assert os.strerror(2) in r.stderr or "ENOENT" in r.stderr, (
        f"错误信息里应包含 ENOENT 的描述 {os.strerror(2)!r}，实际 stderr：\n{r.stderr}")


def _goodput(exe, lab, cli, srv, algo, seconds):
    with lab.start(srv, exe, "server", NS_PORT) as s:
        s.expect(r"listening on port", timeout=10)
        r = lab.run(cli, exe, "client", SRV_IP, NS_PORT, seconds, algo, timeout=seconds + 30, check=False)
    if r.returncode != 0:
        pytest.fail(f"[{algo}] 客户端 exit {r.returncode}\n{r.stdout}\n{r.stderr}", pytrace=False)
    a = re.search(r"algo=(\S+)", r.stdout)
    g = re.search(r"goodput_mbps=([0-9.]+)", r.stdout)
    assert a and g, f"输出应包含 algo=<名字> 和 goodput_mbps=<x>：\n{r.stdout}"
    assert a.group(1) == algo, f"请求 {algo}，实际 {a.group(1)}"
    return float(g.group(1))


@pytest.mark.parametrize("algo", ["bbr", "cubic"])
def test_goodput_under_tbf(exe, pair, algo):
    _need(algo)
    lab, cli, srv, dev = pair
    lab.qdisc(cli, dev, "tbf rate 50mbit burst 32kbit latency 50ms")
    g = _goodput(exe, lab, cli, srv, algo, 3)
    assert 30 <= g <= 60, f"tbf 50mbit 瓶颈下 {algo} 的 goodput 应在 30~60 Mbit/s，实际 {g:.1f}"


def test_bbr_beats_cubic_under_random_loss(exe, pair, need_netem):
    """真实机器：1% 随机丢包 + 20ms 延迟。CUBIC 把丢包当拥塞信号（吞吐 ~ MSS/RTT/sqrt(p)），
    BBR 按测得的带宽和 min RTT 发送，基本不受随机丢包影响。"""
    _need("bbr")
    _need("cubic")
    lab, cli, srv, dev = pair
    lab.qdisc(cli, dev, "netem delay 20ms loss 1% rate 100mbit limit 10000")
    bbr = _goodput(exe, lab, cli, srv, "bbr", 5)
    cubic = _goodput(exe, lab, cli, srv, "cubic", 5)
    assert bbr > 1.5 * cubic, f"1% 丢包下 BBR ({bbr:.1f} Mbit/s) 应明显快于 CUBIC ({cubic:.1f} Mbit/s)"
