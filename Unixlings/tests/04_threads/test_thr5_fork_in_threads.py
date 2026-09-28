import subprocess

import pytest

from studylings.probe import start

TIMEOUT = 15


def test_child_execs_and_parent_reaps(exe):
    # die_after_fork=0：TSan 默认不允许多线程 fork 后的子进程再创建线程；这里子进程只 exec，设置它只是保险。
    with start(exe, env={"TSAN_OPTIONS": "halt_on_error=1:exitcode=66:die_after_fork=0"}) as p:
        try:
            rc = p.p.wait(timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            pytest.fail(
                f"{TIMEOUT}s 内没有结束 —— 子进程多半死锁了：fork 时后台线程正持有 g_log_lock，\n"
                "子进程继承了一把\"已上锁\"的锁，而持锁的线程在子进程里并不存在，没人会解锁。\n"
                "修法：子进程在 exec 前只调用异步信号安全函数（别调用 log_msg/printf/malloc），\n"
                "或者用 pthread_atfork 在 fork 前加锁、fork 后在父子进程中各自解锁。\n"
                f"{p.describe()}", pytrace=False)
        p.wait()
        if rc != 0:
            extra = "（ThreadSanitizer 报错）" if rc == 66 else ""
            pytest.fail(f"exit {rc}{extra}\n{p.describe()}", pytrace=False)
        lines = [l.strip() for l in p.out]
        assert "child-ok" in lines, f"子进程应 exec `echo child-ok`，stdout 里没有 child-ok\n{p.describe()}"
        assert "parent-ok" in lines, f"父进程 waitpid 成功后应打印 parent-ok\n{p.describe()}"
        assert lines.index("child-ok") < lines.index("parent-ok"), (
            "parent-ok 应在子进程结束（waitpid 返回）之后才打印")
