import re
import socket
import struct
import threading

import pytest

from studylings.probe import assert_ok, run

ROUNDS = 30  # 前几轮内核处于 quickack 模式不会卡，轮数多一些才能看出平均值


class HeaderThenBodyServer:
    """先读 4 字节长度头，再读 body，然后回 1 字节 —— 和很多 RPC 服务器的读法一样。"""

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("127.0.0.1", 0))
        self.sock.listen(4)
        self.sock.settimeout(15)
        self.port = self.sock.getsockname()[1]
        self.rounds = 0
        self.bad = None
        self.t = threading.Thread(target=self._serve, daemon=True)
        self.t.start()

    @staticmethod
    def _exact(c, n):
        buf = b""
        while len(buf) < n:
            d = c.recv(n - len(buf))
            if not d:
                return None
            buf += d
        return buf

    def _serve(self):
        try:
            c, _ = self.sock.accept()
        except OSError:
            return
        with c:
            c.settimeout(10)
            try:
                while True:
                    hdr = self._exact(c, 4)
                    if hdr is None:
                        return
                    (n,) = struct.unpack("!I", hdr)
                    if not 0 < n < 4096:
                        self.bad = f"长度头不合理: {n}"
                        return
                    if self._exact(c, n) is None:
                        self.bad = "body 没读完连接就断了"
                        return
                    self.rounds += 1
                    c.sendall(b"k")
            except OSError as e:
                self.bad = str(e)

    def close(self):
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        self.sock.close()
        self.t.join(timeout=10)


def test_write_write_read_is_fast(exe):
    srv = HeaderThenBodyServer()
    try:
        r = run(exe, "127.0.0.1", srv.port, ROUNDS, timeout=20)
    finally:
        srv.close()
    assert_ok(r, "avg_ms=")
    assert srv.bad is None, f"服务器看到的请求格式不对：{srv.bad}"
    assert srv.rounds == ROUNDS, f"服务器应收到 {ROUNDS} 个请求，实际 {srv.rounds}"
    m = re.search(r"avg_ms=([0-9.]+)", r.stdout)
    assert m, f"输出格式应为 avg_ms=<数字>，实际 {r.stdout!r}"
    avg = float(m.group(1))
    if avg >= 10:
        pytest.fail(f"每轮平均 {avg:.1f} ms —— 这就是 Nagle 与延迟 ACK 互相等待的卡顿（Linux 上约 40ms）。\n"
                    "设置 TCP_NODELAY（或把头和 body 合成一次 write / writev）后应远小于 10 ms。",
                    pytrace=False)
