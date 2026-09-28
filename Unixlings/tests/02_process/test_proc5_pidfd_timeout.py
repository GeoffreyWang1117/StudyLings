import time
from pathlib import Path

import pytest

from studylings.probe import start


def _gone(pid: int, timeout: float = 5) -> bool:
    """True once `pid` no longer exists (or is only a zombie waiting for init to reap it)."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            state = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[0]
        except OSError:
            return True
        if state == "Z":
            return True
        time.sleep(0.05)
    return False


def _run(exe, *args, limit: float):
    """Start the program, return (exit code, elapsed seconds, child pid)."""
    with start(exe, *args, stdin=None) as p:
        t0 = time.monotonic()
        m = p.expect(r"^spawned (\d+)$", timeout=5)
        deadline = t0 + limit
        while p.p.poll() is None and time.monotonic() < deadline:
            time.sleep(0.02)
        elapsed = time.monotonic() - t0
        if p.p.poll() is None:
            pytest.fail(f"{limit:.0f}s 内程序没有退出：超时后应 pidfd_send_signal(SIGTERM) 杀掉子进程并回收\n"
                        f"{p.describe()}", pytrace=False)
        rc = p.wait()
        if rc == 125 and "not supported" in p.stderr:
            pytest.skip("内核不支持 pidfd_open（需要 Linux 5.3+）")
        return rc, elapsed, int(m.group(1)), p.describe()


def test_fast_command_passes_through(exe):
    rc, elapsed, pid, info = _run(exe, "10", "sleep", "0.1", limit=8)
    assert rc == 0, f"sleep 0.1 在 10s 限时内正常结束，应以 0 退出，实际 {rc}\n{info}"
    assert elapsed < 5, f"子进程 0.1s 就结束了，程序却用了 {elapsed:.1f}s：应 poll pidfd 而不是傻等满 SECONDS\n{info}"


def test_exit_code_propagates(exe):
    rc, _, _, info = _run(exe, "10", "sh", "-c", "exit 3", limit=8)
    assert rc == 3, f"子进程 exit 3，应以 3 退出，实际 {rc}\n{info}"


def test_timeout_kills_child(exe):
    rc, elapsed, pid, info = _run(exe, "1", "sleep", "30", limit=8)
    assert rc == 124, f"超时应以 124 退出（和 timeout(1) 一致），实际 {rc}\n{info}"
    assert elapsed >= 0.9, f"限时 1s，程序却 {elapsed:.2f}s 就退出了\n{info}"
    assert _gone(pid), f"超时后子进程 {pid}（sleep 30）应被杀掉，但它还活着\n{info}"


def test_escalates_to_sigkill(exe):
    # 子进程忽略 SIGTERM（SIG_IGN 会跨 exec 保留）：必须在宽限期后升级为 SIGKILL
    rc, elapsed, pid, info = _run(exe, "0.5", "sh", "-c", "trap '' TERM; exec sleep 30", limit=15)
    assert rc == 124, f"超时应以 124 退出，实际 {rc}\n{info}"
    assert _gone(pid), f"子进程 {pid} 忽略了 SIGTERM，宽限期后应该用 SIGKILL 杀掉\n{info}"

