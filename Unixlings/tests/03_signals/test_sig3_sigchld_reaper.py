import time

import pytest

from studylings.probe import children_of, start, zombies_of


def test_no_zombies_after_burst(exe):
    n = 64
    with start(exe, n) as p:
        p.expect(r"^ready", timeout=20)
        deadline = time.monotonic() + 5
        while True:
            zs = zombies_of(p.pid)
            if not zs or time.monotonic() > deadline:
                break
            time.sleep(0.1)
        if zs:
            pytest.fail(f"{n} 个子进程退出后，仍有 {len(zs)} 个僵尸没被回收。\n"
                        "标准信号不排队：这么多子进程只换来一次 SIGCHLD，处理函数必须循环 "
                        "waitpid(-1, &st, WNOHANG) 直到它返回 <= 0。\n" + p.describe(), pytrace=False)
        assert children_of(p.pid) == [], "所有子进程都应该已经退出并被回收"
        p.close_stdin()
        rc = p.wait(timeout=10)
        assert rc == 0, f"stdin EOF 后退出码应为 0，实际 {rc}\n{p.describe()}"
        assert f"reaped {n}" in p.stdout, f"应打印 reaped {n}\n{p.describe()}"
