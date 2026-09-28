import socket
import threading
import time

from studylings.probe import run


class FlakyUdpServer:
    """忽略前 `ignore` 个数据报（模拟丢包），之后对每个数据报回复 "pong:<内容>"。"""

    def __init__(self, ignore: int):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("127.0.0.1", 0))
        self.sock.settimeout(0.1)
        self.port = self.sock.getsockname()[1]
        self.ignore = ignore
        self.received: list[bytes] = []
        self._stop = threading.Event()
        self.t = threading.Thread(target=self._serve, daemon=True)
        self.t.start()

    def _serve(self):
        while not self._stop.is_set():
            try:
                data, peer = self.sock.recvfrom(65536)
            except socket.timeout:
                continue
            except OSError:
                return
            self.received.append(data)
            if len(self.received) > self.ignore:
                self.sock.sendto(b"pong:" + data, peer)

    def close(self):
        time.sleep(0.2)  # 收齐可能在路上的数据报
        self._stop.set()
        self.t.join(timeout=5)
        self.sock.close()


def test_refused_when_no_server(exe, port):
    t0 = time.monotonic()
    r = run(exe, "127.0.0.1", port, "anyone?", timeout=10)
    elapsed = time.monotonic() - t0
    assert r.stdout.strip() == "refused" and r.returncode == 2, (
        f"没有进程监听该 UDP 端口时应打印 refused 并 exit 2，实际 exit {r.returncode}, "
        f"stdout {r.stdout!r}。\n只有 connect() 过的 UDP socket 才能从 recv/send 拿到 ECONNREFUSED。")
    assert elapsed < 0.9 * 3, f"refused 应该很快得知（ICMP 几乎立即返回），实际用了 {elapsed:.2f}s"


def test_retries_until_reply(exe):
    srv = FlakyUdpServer(ignore=2)
    try:
        r = run(exe, "127.0.0.1", srv.port, "query-42", timeout=10)
    finally:
        srv.close()
    assert r.returncode == 0 and r.stdout == "pong:query-42\n", (
        f"服务器丢弃了前 2 个数据报，第 3 次发送应得到回复。实际 exit {r.returncode}, stdout {r.stdout!r}\n"
        f"服务器共收到 {len(srv.received)} 个数据报（超时后要重传，最多发 3 次）")
    assert srv.received == [b"query-42"] * 3, f"应恰好发送 3 次，服务器收到 {srv.received!r}"


def test_timeout_after_three_tries(exe):
    srv = FlakyUdpServer(ignore=10**9)
    try:
        t0 = time.monotonic()
        r = run(exe, "127.0.0.1", srv.port, "hello?", timeout=10)
        elapsed = time.monotonic() - t0
    finally:
        srv.close()
    assert r.stdout.strip() == "timeout" and r.returncode == 3, (
        f"服务器从不回复时应打印 timeout 并 exit 3，实际 exit {r.returncode}, stdout {r.stdout!r}")
    assert len(srv.received) == 3, f"放弃之前应恰好发送 3 次，服务器收到 {len(srv.received)} 个数据报"
    assert elapsed >= 0.8, f"3 次 × 300ms 的等待至少约 0.9s，实际只用了 {elapsed:.2f}s"
