import os
import signal
import subprocess

import pytest

from studylings.probe import sanitizer_env

HANG_HINT = ("管道没有结束（超时）：读端等不到 EOF，说明还有进程持有管道写端。"
             "父进程 fork 完两个子进程后要 close 管道两端；exec 出来的命令也不该继承原始的 pipe fd"
             "（pipe2(..., O_CLOEXEC)）")


def pipeline(exe, *argv, timeout=5):
    """Run the pipeline in its own process group so a hung pipeline can be killed entirely."""
    p = subprocess.Popen([str(exe), *argv], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, text=True, env=sanitizer_env(),
                         start_new_session=True)
    try:
        out, err = p.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        out, err = p.communicate()
        pytest.fail(f"{HANG_HINT}\n命令: {' '.join(argv)}\n--- stdout ---\n{out}--- stderr ---\n{err}",
                    pytrace=False)
    return p.returncode, out, err


def test_wc_sees_eof(exe):
    rc, out, err = pipeline(exe, "printf", r"a\nb\nc\n", "|", "wc", "-l")
    assert out.strip() == "3", f"printf 'a\\nb\\nc\\n' | wc -l 应输出 3，实际 {out!r}\nstderr: {err}"
    assert rc == 0, f"wc 成功时应以 0 退出，实际 {rc}\nstderr: {err}"


def test_large_data(exe):
    rc, out, err = pipeline(exe, "head", "-c", "1000000", "/dev/zero", "|", "wc", "-c")
    assert out.strip() == "1000000", f"应传输 1000000 字节，wc -c 输出 {out!r}\nstderr: {err}"
    assert rc == 0


def test_writer_gets_sigpipe_when_reader_exits(exe):
    # yes 永远写；head 读 3 行后退出。只有当 yes 是唯一持有写端、且没有别人持有读端时，
    # yes 才会收到 SIGPIPE 结束 —— 否则整个管道挂住。
    rc, out, err = pipeline(exe, "yes", "|", "head", "-n", "3")
    assert out == "y\ny\ny\n", f"yes | head -n 3 输出不对：{out!r}"
    assert rc == 0, f"应以 head 的退出码 0 退出，实际 {rc}"


@pytest.mark.parametrize("code", [0, 7, 42])
def test_exit_status_is_cmd2s(exe, code):
    rc, out, err = pipeline(exe, "true", "|", "sh", "-c", f"cat >/dev/null; exit {code}")
    assert rc == code, f"应像 sh 一样以 cmd2 的退出码 {code} 退出，实际 {rc}（用 WEXITSTATUS 解码）"


def test_exit_status_ignores_cmd1(exe):
    rc, out, err = pipeline(exe, "false", "|", "cat")
    assert rc == 0, f"false | cat 的退出码应是 cat 的 0，实际 {rc}"


def test_signaled_cmd2_is_128_plus_sig(exe):
    rc, out, err = pipeline(exe, "true", "|", "sh", "-c", "kill -TERM $$")
    assert rc == 128 + signal.SIGTERM, f"cmd2 被 SIGTERM 杀死时退出码应为 {128 + signal.SIGTERM}，实际 {rc}"


def test_command_not_found(exe):
    rc, out, err = pipeline(exe, "true", "|", "no-such-cmd-sl")
    assert rc == 127, f"cmd2 不存在时退出码应为 127，实际 {rc}\nstderr: {err}"
    assert "no-such-cmd-sl" in err, f"stderr 应报告找不到的命令名，实际 {err!r}"


def test_no_fd_leak_into_commands(exe):
    # cmd2 列出自己打开的 fd：只应有 0/1/2，外加 ls 打开 /proc/self/fd 目录用的那一个
    rc, out, err = pipeline(exe, "true", "|", "ls", "/proc/self/fd")
    fds = sorted(int(x) for x in out.split())
    assert len(fds) <= 4 and fds[:3] == [0, 1, 2], (
        f"cmd2 继承了多余的 fd：{fds}。原始的 pipe fd 应带 O_CLOEXEC（pipe2），exec 时自动关闭")
