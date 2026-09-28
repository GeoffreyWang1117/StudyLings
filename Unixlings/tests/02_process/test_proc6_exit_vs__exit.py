import re

from studylings.probe import assert_ok, run


def test_child_does_not_run_parent_cleanup(exe, tmp_path):
    pidfile = tmp_path / "daemon.pid"
    r = run(exe, pidfile)
    assert_ok(r)
    lines = r.stdout.splitlines()
    show = f"\n--- stdout ---\n{r.stdout}--- stderr ---\n{r.stderr}"

    n_cleanup = lines.count("cleanup")
    assert n_cleanup == 1, (
        f"'cleanup' 出现了 {n_cleanup} 次（应为 1 次）：子进程用 exit() 结束时会运行父进程注册的 "
        f"atexit 处理函数，应改用 _exit(){show}")
    starting = [l for l in lines if re.fullmatch(r"starting \d+", l)]
    assert len(starting) == 1, (
        f"'starting' 出现了 {len(starting)} 次（应为 1 次）：fork 复制了没 flush 的 stdio 缓冲区，"
        f"fork 前要 fflush(stdout){show}")
    n_child = lines.count("child working")
    assert n_child == 1, (
        f"'child working' 出现了 {n_child} 次（应为 1 次）：子进程用 _exit 之前要先 fflush 自己的输出{show}")
    assert "pidfile ok" in lines, f"子进程结束后父进程的 pidfile 被删掉了（应打印 'pidfile ok'）{show}"
    assert not pidfile.exists(), f"父进程退出时 cleanup 应该删除 pidfile{show}"
    assert lines[-1] == "cleanup", f"'cleanup' 应该是父进程退出时最后一行输出{show}"
