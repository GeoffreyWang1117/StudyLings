import os
import socket
import threading
import time
from pathlib import Path

import pytest

from studylings.probe import start


def _recv_exact(s, n, deadline):
    buf = bytearray()
    while len(buf) < n:
        s.settimeout(max(0.01, deadline - time.monotonic()))
        try:
            chunk = s.recv(min(1 << 20, n - len(buf)))
        except (socket.timeout, TimeoutError):
            break
        if not chunk:
            break
        buf += chunk
    return bytes(buf)


def _rss_kib(pid) -> int:
    for line in Path(f"/proc/{pid}/status").read_text().splitlines():
        if line.startswith("VmRSS:"):
            return int(line.split()[1])
    return 0


class Hog:
    """客户端 A：大量发送，但暂时一个字节都不读。"""

    def __init__(self, port, data: bytes):
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 32 * 1024)  # 小接收窗口：服务器很快就写不进去
        self.s.settimeout(60)
        self.s.connect(("127.0.0.1", port))
        self.data = data
        self.sent = 0
        self.err = None
        self.t = threading.Thread(target=self._send, daemon=True)
        self.t.start()

    def _send(self):
        try:
            mv = memoryview(self.data)
            while self.sent < len(self.data):
                self.sent += self.s.send(mv[self.sent:self.sent + 65536])
        except OSError as e:
            self.err = e

    def read_all_back(self, p, timeout=60):
        got = _recv_exact(self.s, len(self.data), time.monotonic() + timeout)
        if len(got) != len(self.data):
            pytest.fail(f"A 开始读之后，{timeout}s 内只收回了 {len(got)}/{len(self.data)} 字节。"
                        "EPOLLOUT 就绪时要继续发送输出缓冲区；缓冲区降下来后要重新打开 EPOLLIN\n"
                        + p.describe(), pytrace=False)
        assert got == self.data, "A 收回的数据与发送的不一致（缓冲区的顺序/偏移有问题？）"
        self.t.join(timeout=10)
        assert self.err is None, f"A 发送出错：{self.err!r}"

    def close(self):
        self.s.close()


def _small_echo_ok(port, timeout=3.0) -> bool:
    with socket.create_connection(("127.0.0.1", port), timeout=timeout) as b:
        msg = b"hello from B\n"
        b.sendall(msg)
        return _recv_exact(b, len(msg), time.monotonic() + timeout) == msg


def test_slow_reader_does_not_starve_others(exe, port):
    with start(exe, port) as p:
        p.expect(r"listening on port \d+", timeout=10)
        a = Hog(port, os.urandom(8 << 20))
        try:
            time.sleep(1.0)  # 让 A 把服务器→A 方向的 socket 缓冲区塞满
            if not _small_echo_ok(port):
                pytest.fail(
                    "客户端 A 发了大量数据但不读；此时客户端 B 的小消息 3s 内没有得到回显。\n"
                    "服务器卡在给 A 的 write 上了（EAGAIN 时原地重试 = 阻塞整个事件循环）。"
                    "写不完的数据要放进 A 的输出缓冲区，注册 EPOLLOUT 以后再写。\n" + p.describe(),
                    pytrace=False)
            a.read_all_back(p)
        finally:
            a.close()
        # A 走了以后服务器还要正常工作，且不能在空闲时因为 EPOLLOUT 一直开着而空转
        with socket.create_connection(("127.0.0.1", port), timeout=5) as idle:
            idle.sendall(b"x" * 1000)
            assert _recv_exact(idle, 1000, time.monotonic() + 5) == b"x" * 1000, "A 断开后，新客户端得不到回显"
            time.sleep(0.2)
            t0 = _cpu_ticks(p.pid)
            time.sleep(1.0)
            burned = (_cpu_ticks(p.pid) - t0) / os.sysconf("SC_CLK_TCK")
            assert burned < 0.5, (
                f"只有一个空闲连接时服务器 1s 内消耗了 {burned:.2f}s CPU。输出缓冲区写空后要关掉 EPOLLOUT："
                "LT 模式下 socket 几乎总是可写，EPOLLOUT 开着 epoll_wait 就会不停返回")
        assert p.p.poll() is None, "服务器不应该退出\n" + p.describe()


def _cpu_ticks(pid: int) -> int:
    fields = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()
    return int(fields[11]) + int(fields[12])


def test_output_buffer_is_capped(exe, port):
    """A 发 64 MiB 不读：服务器应停止从 A 读取（关掉 EPOLLIN），而不是把 64 MiB 都攒进内存。"""
    with start(exe, port) as p:
        p.expect(r"listening on port \d+", timeout=10)
        assert _small_echo_ok(port), "基本的回显都不工作\n" + p.describe()
        base = _rss_kib(p.pid)
        a = Hog(port, os.urandom(64 << 20))
        try:
            time.sleep(1.5)
            if not _small_echo_ok(port):
                pytest.fail("A 不读时，B 的回显 3s 内没回来（事件循环被 A 阻塞了）\n" + p.describe(),
                            pytrace=False)
            grown = (_rss_kib(p.pid) - base) / 1024
            assert grown < 24, (
                f"A 发送 64 MiB 且不读的情况下，服务器内存增长了 {grown:.0f} MiB。"
                "待发送数据超过 1 MiB 时应关掉该连接的 EPOLLIN（背压），让数据留在内核/对端")
            # 此时 A 被背压：服务器既不应空转（EPOLLOUT 一直就绪却写不出？EPOLLIN 关不掉？）
            t0 = _cpu_ticks(p.pid)
            time.sleep(1.0)
            burned = (_cpu_ticks(p.pid) - t0) / os.sysconf("SC_CLK_TCK")
            assert burned < 0.5, f"A 被背压期间服务器 1s 内消耗了 {burned:.2f}s CPU —— 事件循环在空转"
            a.read_all_back(p, timeout=120)
        finally:
            a.close()
