import os
import signal
import subprocess

import pytest

from studylings.probe import sanitizer_env


def test_reader_goes_away(exe):
    p = subprocess.Popen([str(exe)], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, env=sanitizer_env(), start_new_session=True)
    try:
        for i in range(1, 6):
            line = p.stdout.readline()
            assert line == f"line {i}\n".encode(), f"第 {i} 行应为 'line {i}'，实际 {line!r}"
        p.stdout.close()  # 读者走了：管道读端关闭
        try:
            rc = p.wait(timeout=10)
        except subprocess.TimeoutExpired:
            pytest.fail("读端关闭 10 秒后程序仍未退出（write 失败后还在死循环？）", pytrace=False)
        err = p.stderr.read().decode(errors="replace")
    finally:
        if p.poll() is None:
            os.killpg(p.pid, signal.SIGKILL)
            p.wait()
        p.stderr.close()
    if rc < 0:
        pytest.fail(f"程序被信号 {signal.Signals(-rc).name} 无声无息地杀死了（退出状态 {rc}）。\n"
                    "往读端已关闭的管道/socket 写数据会收到 SIGPIPE，默认动作是终止进程——"
                    "应该忽略 SIGPIPE，然后处理 write 返回的 EPIPE。\n--- stderr ---\n" + err,
                    pytrace=False)
    assert rc == 0, f"读者离开后应以 0 退出，实际 {rc}\n--- stderr ---\n{err}"
    assert "peer closed" in err, f"stderr 应包含 peer closed，实际: {err!r}"
