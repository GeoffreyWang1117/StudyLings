import os
import re
import signal
import socket
import subprocess
import time

import pytest

from studylings.probe import start

TRACEFS = "/sys/kernel/tracing"
EVENT = f"{TRACEFS}/events/sock/inet_sock_set_state"


@pytest.fixture
def tracefs(bpf_root):
    if not os.path.isdir(f"{TRACEFS}/events"):
        r = subprocess.run(["mount", "-t", "tracefs", "tracefs", TRACEFS], capture_output=True, text=True)
        if r.returncode != 0 or not os.path.isdir(f"{TRACEFS}/events"):
            pytest.skip(f"tracefs 未挂载且挂载失败（{r.stderr.strip()}）："
                        "在真实机器上 mount -t tracefs tracefs /sys/kernel/tracing")
    if not os.path.isdir(EVENT):
        pytest.skip("内核没有 tracepoint sock/inet_sock_set_state（需要 4.16+）")


@pytest.fixture
def port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _lifecycle(port):
    """listen → connect → accept → 客户端先 close → 服务端读到 EOF 再 close。返回客户端本地端口。"""
    lst = socket.socket()
    lst.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lst.bind(("127.0.0.1", port))
    lst.listen()
    cli = socket.create_connection(("127.0.0.1", port), timeout=5)
    cport = cli.getsockname()[1]
    srv, _ = lst.accept()
    srv.settimeout(5)
    cli.close()
    assert srv.recv(16) == b""
    time.sleep(0.05)
    srv.close()
    lst.close()
    return cport


def test_tcp_lifecycle(exe, tracefs, port):
    with start(exe, port, 0) as p:
        try:
            p.expect(r"^ready", timeout=30)
        except pytest.fail.Exception:
            pytest.fail("追踪器没有打印 ready（加载或挂载 tracepoint 失败？看 stderr）\n" + p.describe(),
                        pytrace=False)
        cport = _lifecycle(port)
        server_side = rf"127\.0\.0\.1:{port} -> 127\.0\.0\.1:{cport} "
        try:
            p.expect(server_side + r"LAST_ACK -> CLOSE", timeout=10)
        except pytest.fail.Exception:
            pass  # 下面给出更具体的诊断
        time.sleep(0.3)
        p.signal(signal.SIGINT)
        rc = p.wait(timeout=15)
        assert rc == 0, f"收到 SIGINT 后应 detach 并 exit 0，实际 exit {rc}\n{p.describe()}"

    out = p.stdout
    events = re.findall(r"^(\S+):(\d+) -> (\S+):(\d+) (\w+) -> (\w+)\s*$", out, re.M)
    if not events:
        pytest.fail(f"没有输出任何 \"saddr:sport -> daddr:dport OLD -> NEW\" 事件行。端口过滤对了吗？"
                    f"（tracepoint 里的 sport/dport 已经是主机字节序，不要再 bpf_htons）\n{p.describe()}",
                    pytrace=False)
    client_side = rf"127\.0\.0\.1:{cport} -> 127\.0\.0\.1:{port} "
    server_side = rf"127\.0\.0\.1:{port} -> 127\.0\.0\.1:{cport} "
    expected = [
        (rf"127\.0\.0\.1:{port} -> \S+ CLOSE -> LISTEN", "监听 socket CLOSE -> LISTEN"),
        (rf"127\.0\.0\.1:\d+ -> 127\.0\.0\.1:{port} CLOSE -> SYN_SENT", "客户端 CLOSE -> SYN_SENT"),
        (client_side + "SYN_SENT -> ESTABLISHED", "客户端 SYN_SENT -> ESTABLISHED"),
        (server_side + "SYN_RECV -> ESTABLISHED", "服务端 SYN_RECV -> ESTABLISHED"),
        (client_side + "ESTABLISHED -> FIN_WAIT1", "客户端（先关闭方）ESTABLISHED -> FIN_WAIT1"),
        (client_side + "FIN_WAIT1 -> (FIN_WAIT2|CLOSING)", "客户端 FIN_WAIT1 -> FIN_WAIT2"),
        (client_side + r"\w+ -> CLOSE$", "客户端最终 -> CLOSE（进入 TIME_WAIT 由 timewait sock 接管）"),
        (server_side + "ESTABLISHED -> CLOSE_WAIT", "服务端（被动关闭方）ESTABLISHED -> CLOSE_WAIT"),
        (server_side + "CLOSE_WAIT -> LAST_ACK", "服务端 CLOSE_WAIT -> LAST_ACK"),
        (server_side + "LAST_ACK -> CLOSE", "服务端 LAST_ACK -> CLOSE"),
    ]
    missing = [desc for rx, desc in expected if not re.search(rf"^{rx}", out, re.M)]
    if missing:
        zero = re.search(r"0\.0\.0\.0:0 -> 0\.0\.0\.0:0", out)
        hint = ("（地址/端口全是 0：事件结构体的 saddr/daddr/sport/dport 没有从 ctx 填进去）" if zero else
                f"（客户端本地端口是 {cport}，检查 saddr/daddr 的方向和端口字段是否填对）")
        pytest.fail("缺少这些状态转换：\n  " + "\n  ".join(missing) + f"\n{hint}\n{p.describe()}", pytrace=False)

    unrelated = [e for e in events if int(e[1]) != port and int(e[3]) != port]
    assert not unrelated, f"输出了与端口 {port} 无关的事件（过滤失效）：{unrelated[:3]}"
