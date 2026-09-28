import socket
import threading
import time

import pytest


class Server:
    """127.0.0.1 上的测试服务器。behaviour(conn) 在 accept 之后运行。"""

    def __init__(self, behaviour):
        self.ls = socket.socket()
        self.ls.bind(("127.0.0.1", 0))
        self.ls.listen(8)
        self.port = self.ls.getsockname()[1]
        self.behaviour = behaviour
        self.conns = []
        self.stop = threading.Event()
        self.t = threading.Thread(target=self._run, daemon=True)
        self.t.start()

    def _run(self):
        self.ls.settimeout(0.2)
        while not self.stop.is_set():
            try:
                c, _ = self.ls.accept()
            except (socket.timeout, TimeoutError):
                continue
            except OSError:
                return
            self.conns.append(c)
            try:
                self.behaviour(c)
            except OSError:
                pass

    def close(self):
        self.stop.set()
        self.t.join(timeout=5)
        for c in self.conns:
            c.close()
        self.ls.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


def _check(r, want_rc, want_out, what):
    if r.returncode != want_rc or r.stdout.strip() != want_out:
        pytest.fail(f"{what}：期望输出 {want_out!r} 并 exit {want_rc}，"
                    f"实际输出 {r.stdout.strip()!r}，exit {r.returncode}"
                    f"{'（ASan/LSan 报错）' if r.returncode == 23 else ''}\n--- stderr ---\n{r.stderr}",
                    pytrace=False)


def test_server_replies(exe, urun):
    def talk(c):
        c.sendall(b"hel")
        time.sleep(0.1)
        c.sendall(b"lo io_uring\nsecond line\n")

    with Server(talk) as srv:
        r = urun(exe, "127.0.0.1", srv.port, 3000, timeout=15)
    _check(r, 0, "hello io_uring", "服务器分两次发来一行")


def test_silent_server_times_out(exe, urun):
    with Server(lambda c: None) as srv:  # accept 之后一言不发
        t0 = time.monotonic()
        r = urun(exe, "127.0.0.1", srv.port, 500, timeout=15)
        elapsed = time.monotonic() - t0
    _check(r, 3, "timeout", "服务器不说话")
    assert elapsed >= 0.45, f"超时 500ms，但 {elapsed:.3f}s 就报告 timeout 了：定时器不应提前触发"
    assert elapsed < 8, (f"超时 500ms，却过了 {elapsed:.1f}s 才结束。"
                         "LINK_TIMEOUT 只作用于前一个带 IOSQE_IO_LINK 的 SQE")


def test_partial_line_then_silence(exe, urun):
    with Server(lambda c: c.sendall(b"no newline yet")) as srv:
        t0 = time.monotonic()
        r = urun(exe, "127.0.0.1", srv.port, 400, timeout=15)
        elapsed = time.monotonic() - t0
    _check(r, 3, "timeout", "服务器发了半行就不说话了（后续 RECV 也要带 LINK_TIMEOUT）")
    assert elapsed < 8, f"超时 400ms，却过了 {elapsed:.1f}s 才结束"


def test_refused(exe, urun):
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()  # 端口没人监听 → RST → ECONNREFUSED
    r = urun(exe, "127.0.0.1", port, 2000, timeout=15)
    _check(r, 2, "refused", "端口没有人监听（CONNECT 的 cqe->res == -ECONNREFUSED）")
