import os
import socket
import time
from pathlib import Path

import pytest

from studylings.probe import start


class Client:
    def __init__(self, port):
        self.s = socket.create_connection(("127.0.0.1", port), timeout=5)
        self.buf = b""

    def _readline(self, timeout: float) -> str | None:
        """读一整行；超时抛 TimeoutError；对端关闭返回 None。"""
        deadline = time.monotonic() + timeout
        while b"\n" not in self.buf:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError
            self.s.settimeout(remaining)
            try:
                chunk = self.s.recv(4096)
            except socket.timeout:
                raise TimeoutError from None
            if not chunk:
                return None
            self.buf += chunk
        ln, self.buf = self.buf.split(b"\n", 1)
        return ln.decode(errors="replace")

    def line(self, what: str) -> str:
        try:
            ln = self._readline(5)
        except TimeoutError:
            pytest.fail(f"5s 内没有收到 {what}", pytrace=False)
        if ln is None:
            pytest.fail(f"连接被服务器关闭了，没有收到 {what}", pytrace=False)
        return ln

    def say(self, text: str):
        self.s.sendall(text.encode() + b"\n")

    def nothing_pending(self, wait=0.3) -> str | None:
        """确认 wait 秒内没有收到任何行；如果收到了，返回那一行。"""
        try:
            return self._readline(wait)
        except TimeoutError:
            return None

    def close(self):
        self.s.close()


def _cpu_ticks(pid: int) -> int:
    fields = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()
    return int(fields[11]) + int(fields[12])  # utime + stime


def _join(port, p, expected_id):
    c = Client(port)
    hello = c.line("欢迎行 hello <id>")
    assert hello == f"hello {expected_id}", f"第 {expected_id} 个连接应该收到 'hello {expected_id}'，实际 {hello!r}"
    p.expect(rf"^join {expected_id}$", timeout=5)
    return c


def test_chat_broadcast_and_disconnect(exe, port):
    with start(exe, port) as p:
        p.expect(r"listening on port \d+", timeout=10)
        a, b, c = (_join(port, p, i) for i in (1, 2, 3))

        a.say("hi from a")
        assert b.line("A 的消息") == "1: hi from a", "B 应收到 '1: hi from a'"
        assert c.line("A 的消息") == "1: hi from a", "C 应收到 '1: hi from a'"
        own = a.nothing_pending()
        assert own is None, f"发送者不应该收到自己的消息，A 却收到了 {own!r}"

        b.say("b here")
        c.say("c here")
        got_a = {a.line("B/C 的消息"), a.line("B/C 的消息")}
        assert got_a == {"2: b here", "3: c here"}, f"A 应收到 B、C 的消息，实际 {got_a}"
        assert b.line("C 的消息") == "3: c here", "B 应收到 C 的消息，且收不到自己的"
        assert c.line("B 的消息") == "2: b here", "C 应收到 B 的消息，且收不到自己的"

        # C 断开
        c.close()
        p.expect(r"^leave 3$", timeout=5)
        time.sleep(0.2)
        t0 = _cpu_ticks(p.pid)
        time.sleep(1.5)
        burned = (_cpu_ticks(p.pid) - t0) / os.sysconf("SC_CLK_TCK")
        assert burned < 0.5, (
            f"C 断开后服务器在 1.5s 空闲期间消耗了 {burned:.2f}s CPU —— 事件循环在空转。"
            "关闭的 fd 必须从 pollfd 数组里删掉，否则 poll 会一直立刻返回（POLLNVAL/POLLHUP）")

        a.say("c is gone")
        assert b.line("A 在 C 离开后的消息") == "1: c is gone", "C 断开后 A、B 应该还能继续聊天"
        b.say("yes")
        assert a.line("B 在 C 离开后的消息") == "2: yes", "C 断开后 A、B 应该还能继续聊天"

        # 新人加入，编号继续递增，且能收到消息
        d = _join(port, p, 4)
        a.say("welcome d")
        assert d.line("A 的消息") == "1: welcome d"
        assert b.line("A 的消息") == "1: welcome d"
        assert p.p.poll() is None, "服务器不应该退出\n" + p.describe()
        for x in (a, b, d):
            x.close()


def test_partial_lines_are_buffered(exe, port):
    with start(exe, port) as p:
        p.expect(r"listening on port \d+", timeout=10)
        a, b = (_join(port, p, i) for i in (1, 2))
        a.s.sendall(b"hel")
        time.sleep(0.2)
        a.s.sendall(b"lo\nsecond li")
        time.sleep(0.2)
        a.s.sendall(b"ne\n")
        assert b.line("拼好的第一行") == "1: hello", "一行可能分多次到达，要攒够 '\\n' 再广播"
        assert b.line("拼好的第二行") == "1: second line"
        a.close()
        b.close()
