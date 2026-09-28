import time

import pytest

from studylings.probe import start

HANG_TIMEOUT = 15


def test_recovers_from_dead_owner(exe):
    with start(exe) as p:
        deadline = time.monotonic() + HANG_TIMEOUT
        while p.p.poll() is None and time.monotonic() < deadline:
            time.sleep(0.05)
        if p.p.poll() is None:
            pytest.fail(
                f"父进程 {HANG_TIMEOUT}s 内没有结束：它在等一把主人已经死掉的锁（普通互斥量永远等不到解锁）。"
                f"需要 PTHREAD_MUTEX_ROBUST，并处理 EOWNERDEAD。\n{p.describe()}", pytrace=False)
        rc = p.wait(timeout=5)
        out = p.stdout
        assert rc == 0, f"exit {rc}（66 = ThreadSanitizer 报错）\n{p.describe()}"
    assert "EOWNERDEAD" in out, f"父进程加锁时应当收到 EOWNERDEAD：\n{out}"
    assert "recovered balance=1000" in out, f"修复后不变式 a+b == 1000 应成立：\n{out}"
