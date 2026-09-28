import re

from studylings.probe import assert_ok, run


def _parse(r):
    assert_ok(r, what="run_capture 成功时程序应以 0 退出")
    m = re.fullmatch(r"exit=(-?\d+) output=(.*)\n", r.stdout, re.S)
    assert m, f"输出格式应为 'exit=<code> output=<...>'，实际 {r.stdout!r}"
    return int(m.group(1)), m.group(2)


def test_captures_echo(exe):
    code, out = _parse(run(exe, "echo", "hello", "spawn"))
    assert out == "hello spawn", f"应捕获到子进程 stdout 'hello spawn'，实际 {out!r}"
    assert code == 0


def test_uses_path_lookup_and_passes_args(exe):
    code, out = _parse(run(exe, "printf", "%s-%s", "a b", "c"))
    assert out == "a b-c", f"参数应原样传给子进程，实际输出 {out!r}"


def test_failing_command_exit_code(exe):
    code, out = _parse(run(exe, "sh", "-c", "echo partial; echo to-stderr >&2; exit 5"))
    assert code == 5, f"子进程 exit 5，应打印 exit=5，实际 exit={code}"
    assert out == "partial", f"只捕获 stdout（stderr 不捕获），实际 {out!r}"


def test_output_larger_than_pipe_buffer(exe):
    # ~290KB 输出，远超 64KiB 管道容量：先 waitpid 再 read 会死锁
    r = run(exe, "seq", "1", "50000", timeout=10)
    code, out = _parse(r)
    lines = out.split("\n")
    assert code == 0 and len(lines) == 50000 and lines[-1] == "50000", (
        f"应完整捕获 50000 行输出，实际 {len(lines)} 行（末行 {lines[-1]!r}）")


def test_nonexistent_command(exe):
    r = run(exe, "definitely-not-a-cmd-sl", "x")
    assert r.returncode == 127, f"命令不存在时程序应以 127 退出，实际 {r.returncode}\nstderr: {r.stderr}"
    assert "No such file or directory" in r.stderr, (
        f"posix_spawnp 直接**返回**错误码 ENOENT（不设置 errno），应用 strerror(返回值) 报告，"
        f"实际 stderr: {r.stderr!r}")
    assert r.stdout == "", f"启动失败时不应打印 exit=...，实际 {r.stdout!r}"
