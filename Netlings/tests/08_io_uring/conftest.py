"""本章共享的 fixture：IPv4 端口、以及"本机 io_uring 不可用就 skip"。

约定：每个练习在 io_uring_queue_init 返回 -EPERM / -ENOSYS / -EACCES 时（Docker 默认 seccomp、
sysctl kernel.io_uring_disabled=1/2、或太老的内核）打印一行
    io_uring unavailable: <原因>
并以退出码 77 结束（autotools 的 "skipped" 约定）。probe 看到它就 pytest.skip，而不是判失败。
"""
import contextlib
import re
import socket
import time

import pytest

from studylings.probe import run, start

UNAVAILABLE_RC = 77
UNAVAILABLE_MARK = "io_uring unavailable"
SKIP_REASON = ("本机 io_uring 不可用（{why}）。常见原因：Docker 默认 seccomp 拦截 io_uring_setup"
               "（docker run --security-opt seccomp=unconfined 可放行），或 sysctl kernel.io_uring_disabled=1/2"
               "（sysctl -w kernel.io_uring_disabled=0）。请在允许 io_uring 的 Linux ≥ 6.1 上运行本章")


def _skip_if_unavailable(rc, out: str, err: str):
    text = (out or "") + (err or "")
    if rc == UNAVAILABLE_RC and UNAVAILABLE_MARK in text:
        why = next((l for l in text.splitlines() if UNAVAILABLE_MARK in l), "").strip()
        pytest.skip(SKIP_REASON.format(why=why))


@pytest.fixture
def port() -> int:
    """一个在 127.0.0.1 上空闲的 TCP 端口（本章只用 IPv4）。"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture
def urun():
    """像 probe.run 一样运行到结束；程序报告 io_uring 不可用（exit 77）时 skip。"""
    def _run(exe, *args, **kw):
        r = run(exe, *args, **kw)
        out = r.stdout.decode(errors="replace") if isinstance(r.stdout, bytes) else r.stdout
        err = r.stderr.decode(errors="replace") if isinstance(r.stderr, bytes) else r.stderr
        _skip_if_unavailable(r.returncode, out, err)
        return r
    return _run


@pytest.fixture
def userver():
    """启动服务器并等到 "listening on port N"；io_uring 不可用（exit 77）时 skip。

        with userver(exe, port) as p: ...
    """
    @contextlib.contextmanager
    def _serve(exe, *args, ready=r"listening on port \d+", timeout=10):
        with start(exe, *args) as p:
            rx = re.compile(ready)
            deadline = time.monotonic() + timeout
            while True:
                if any(rx.search(l) for l in list(p.out)):
                    break
                if p.p.poll() is not None:
                    p.wait(timeout=5)
                    _skip_if_unavailable(p.p.returncode, p.stdout, p.stderr)
                    pytest.fail(f"服务器还没打印就绪行就退出了 (exit {p.p.returncode})\n{p.describe()}",
                                pytrace=False)
                if time.monotonic() > deadline:
                    pytest.fail(f"{timeout}s 内没有等到 /{ready}/\n{p.describe()}", pytrace=False)
                time.sleep(0.02)
            yield p
    return _serve
