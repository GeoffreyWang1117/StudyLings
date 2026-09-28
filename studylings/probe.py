"""
Helpers for BUILD_AND_PROBE pytest probes (Unixlings / Netlings).

A probe drives the learner's compiled program from the outside — the way a
shell, a peer process or a network client would — and asserts on observable
behaviour: exit status, output, file descriptors, zombies, syscalls, sockets.

Import from a project's tests/conftest.py:

    from studylings.probe import *  # noqa: F401,F403  (re-exports the `exe` fixture)
"""

from __future__ import annotations

import errno
import os
import queue
import re
import shutil
import signal
import socket
import subprocess
import tempfile
import threading
import time
from pathlib import Path
from typing import Optional, Union

import pytest

__all__ = [
    "exe", "run", "start", "Proc", "free_port", "wait_port", "strace_run",
    "zombies_of", "children_of", "fd_targets", "sanitizer_env", "assert_ok",
]

# Sanitizer defaults: make any report turn into a non-zero exit code.
_SANITIZER_ENV = {
    "ASAN_OPTIONS": "detect_leaks=1:abort_on_error=0:exitcode=23",
    "UBSAN_OPTIONS": "print_stacktrace=1:halt_on_error=1",
    "TSAN_OPTIONS": "halt_on_error=1:exitcode=66:second_deadlock_stack=1",
}


def sanitizer_env(extra: Optional[dict] = None) -> dict:
    env = dict(os.environ)
    for k, v in _SANITIZER_ENV.items():
        env.setdefault(k, v)
    if extra:
        env.update(extra)
    return env


def _build_dir(project_root: Path) -> Path:
    if os.environ.get("SL_BUILD_DIR"):
        return Path(os.environ["SL_BUILD_DIR"])
    return project_root / "build" / os.environ.get("STUDYLINGS_PRESET", "dev")


@pytest.fixture
def exe(request) -> Path:
    """Path of the binary under test, derived from the probe name test_<target>.py."""
    module_path = Path(request.module.__file__)
    name = module_path.stem.removeprefix("test_")
    project_root = module_path.parents[2]  # <project>/tests/<chapter>/test_x.py
    path = _build_dir(project_root) / "bin" / name
    if not path.exists():
        pytest.fail(f"找不到可执行文件 {path}\n先编译：cmake --preset dev && cmake --build --preset dev --target {name}")
    return path


def run(exe: Union[Path, str], *args, input: Union[str, bytes, None] = None, timeout: float = 10,
        env: Optional[dict] = None, cwd: Union[Path, str, None] = None) -> subprocess.CompletedProcess:
    """Run to completion. Text mode unless `input` is bytes."""
    text = not isinstance(input, bytes)
    try:
        return subprocess.run(
            [str(exe), *map(str, args)], input=input, capture_output=True, text=text,
            errors="replace" if text else None, timeout=timeout, env=sanitizer_env(env), cwd=cwd,
        )
    except subprocess.TimeoutExpired as e:
        pytest.fail(f"程序在 {timeout}s 内没有结束（死锁？忘记关闭管道写端？阻塞在 read/accept？）\n"
                    f"stdout: {e.stdout!r}\nstderr: {e.stderr!r}")


def assert_ok(r: subprocess.CompletedProcess, stdout_contains: Optional[str] = None, what: str = ""):
    """Fail cleanly (no Python traceback) unless the program exited 0 [and printed `stdout_contains`]."""
    if r.returncode == 0 and (stdout_contains is None or stdout_contains in r.stdout):
        return
    why = f"exit {r.returncode}" if r.returncode != 0 else f"输出中没有 {stdout_contains!r}"
    if r.returncode == 23:
        why += "（AddressSanitizer/LeakSanitizer 报错，见 stderr）"
    elif r.returncode == 66:
        why += "（ThreadSanitizer 发现数据竞争，见 stderr）"
    elif r.returncode < 0:
        why += f"（被信号 {signal.Signals(-r.returncode).name} 杀死）"
    pytest.fail(f"{what + ': ' if what else ''}{why}\n--- stdout ---\n{r.stdout}\n--- stderr ---\n{r.stderr}",
                pytrace=False)


class Proc:
    """A background process whose stdout/stderr are collected line by line."""

    def __init__(self, exe, *args, env: Optional[dict] = None, cwd=None, stdin=subprocess.PIPE):
        self.argv = [str(exe), *map(str, args)]
        self.p = subprocess.Popen(
            self.argv, stdin=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, errors="replace", bufsize=1, env=sanitizer_env(env), cwd=cwd,
            start_new_session=True,
        )
        self._lines: "queue.Queue[str]" = queue.Queue()
        self.out: list[str] = []
        self.err: list[str] = []
        self._readers = [
            threading.Thread(target=self._pump, args=(self.p.stdout, self.out, True), daemon=True),
            threading.Thread(target=self._pump, args=(self.p.stderr, self.err, False), daemon=True),
        ]
        for t in self._readers:
            t.start()

    def _pump(self, stream, sink, to_queue):
        for line in stream:
            sink.append(line)
            if to_queue:
                self._lines.put(line)

    @property
    def pid(self) -> int:
        return self.p.pid

    def describe(self) -> str:
        return (f"命令: {' '.join(self.argv)}\n--- stdout ---\n{''.join(self.out)}"
                f"--- stderr ---\n{''.join(self.err)}")

    def expect(self, pattern: str, timeout: float = 5) -> re.Match:
        """Wait until a stdout line matches `pattern` (regex search)."""
        deadline = time.monotonic() + timeout
        rx = re.compile(pattern)
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                pytest.fail(f"等待输出 /{pattern}/ 超时 ({timeout}s)\n{self.describe()}")
            try:
                line = self._lines.get(timeout=min(remaining, 0.1))
            except queue.Empty:
                if self.p.poll() is not None and self._lines.empty():
                    for t in self._readers:
                        t.join(timeout=1)
                    if self._lines.empty():
                        pytest.fail(f"进程已退出 (exit {self.p.returncode})，没有等到 /{pattern}/\n{self.describe()}")
                continue
            m = rx.search(line)
            if m:
                return m

    def write(self, data: str):
        self.p.stdin.write(data)
        self.p.stdin.flush()

    def close_stdin(self):
        if self.p.stdin and not self.p.stdin.closed:
            self.p.stdin.close()

    def signal(self, sig: int):
        self.p.send_signal(sig)

    def wait(self, timeout: float = 5) -> int:
        try:
            rc = self.p.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            pytest.fail(f"进程 {timeout}s 内没有退出\n{self.describe()}")
        for t in self._readers:
            t.join(timeout=2)
        return rc

    @property
    def stdout(self) -> str:
        return "".join(self.out)

    @property
    def stderr(self) -> str:
        return "".join(self.err)

    def kill(self):
        if self.p.poll() is None:
            try:
                os.killpg(self.p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            self.p.wait(timeout=5)
        self.close_stdin()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.kill()


def start(exe, *args, **kw) -> Proc:
    return Proc(exe, *args, **kw)


def free_port() -> int:
    """A TCP port that is currently free on 127.0.0.1 and (when the host has IPv6) on ::1."""
    for _ in range(50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 0))
            port = s.getsockname()[1]
        try:
            with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s6:
                s6.bind(("::1", port))
        except OSError as e:
            if e.errno in (errno.EAFNOSUPPORT, errno.EADDRNOTAVAIL):
                return port  # no IPv6 on this host (common in containers): the v4 check is enough
            continue
        return port
    pytest.fail("找不到空闲端口")


def wait_port(port: int, host: str = "127.0.0.1", timeout: float = 5):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.2):
                return
        except OSError:
            time.sleep(0.05)
    pytest.fail(f"{timeout}s 内 {host}:{port} 没有开始监听")


def strace_run(exe, *args, trace: str, input=None, timeout: float = 20,
               env: Optional[dict] = None) -> tuple[subprocess.CompletedProcess, list[str]]:
    """Run under `strace -f -y` and return (result, syscall lines). Skips if strace is unusable."""
    if shutil.which("strace") is None:
        pytest.skip("需要 strace（apt install strace）")
    env = dict(env or {})
    env.setdefault("ASAN_OPTIONS", "detect_leaks=0:exitcode=23")  # LSan cannot run under ptrace
    with tempfile.NamedTemporaryFile(prefix="sl-strace-", suffix=".log", delete=False) as log:
        log_path = log.name
    try:
        r = run("strace", "-f", "-y", "-qq", "-s", "64", "-e", f"trace={trace}", "-o", log_path,
                str(exe), *args, input=input, timeout=timeout, env=env)
        err = r.stderr.decode(errors="replace") if isinstance(r.stderr, bytes) else r.stderr
        if "PTRACE_TRACEME" in err or "ptrace(PTRACE_SEIZE" in err:
            pytest.skip("当前环境禁止 ptrace（容器需加 --cap-add SYS_PTRACE）")
        lines = Path(log_path).read_text(errors="replace").splitlines()
    finally:
        os.unlink(log_path)
    return r, lines


def _proc_stat(pid: int) -> Optional[tuple[str, int]]:
    try:
        data = Path(f"/proc/{pid}/stat").read_text()
    except OSError:
        return None
    rest = data[data.rfind(")") + 2:].split()
    return rest[0], int(rest[1])  # state, ppid


def children_of(pid: int) -> list[int]:
    kids = []
    for d in Path("/proc").iterdir():
        if d.name.isdigit():
            st = _proc_stat(int(d.name))
            if st and st[1] == pid:
                kids.append(int(d.name))
    return kids


def zombies_of(pid: int) -> list[int]:
    return [k for k in children_of(pid) if (_proc_stat(k) or ("?", 0))[0] == "Z"]


def fd_targets(pid: int) -> dict[int, str]:
    out = {}
    fd_dir = Path(f"/proc/{pid}/fd")
    for fd in fd_dir.iterdir():
        try:
            out[int(fd.name)] = os.readlink(fd)
        except OSError:
            pass
    return out
