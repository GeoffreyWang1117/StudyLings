import time

import pytest

from studylings.probe import start


def test_times_out_when_no_input(exe):
    # stdin 是一个保持打开、但永远没有数据的管道：read 会一直阻塞，只有 SIGALRM 能把它"叫醒"
    with start(exe, 1) as p:
        t0 = time.monotonic()
        try:
            rc = p.p.wait(timeout=8)
        except Exception:
            pytest.fail("超时 1 秒，但 8 秒后程序仍阻塞在 read 里。\n"
                        "read 被 SIGALRM 打断后被自动重启了（SA_RESTART？），或者 EINTR 被忽略了。\n"
                        + p.describe(), pytrace=False)
        p.wait(timeout=5)
        elapsed = time.monotonic() - t0
        assert rc == 3, f"超时时退出码应为 3，实际 {rc}\n{p.describe()}"
        assert "timeout" in p.stdout, f"超时时应打印 timeout\n{p.describe()}"
        assert elapsed >= 0.5, f"超时 1 秒，程序却在 {elapsed:.2f}s 就退出了\n{p.describe()}"


def test_reads_line_before_timeout(exe):
    with start(exe, 20) as p:
        p.write("hello signals\n")
        p.expect(r"^got: hello signals$", timeout=10)
        rc = p.wait(timeout=10)
        assert rc == 0, f"读到输入后退出码应为 0，实际 {rc}\n{p.describe()}"
        assert "timeout" not in p.stdout, f"读到了输入就不应再打印 timeout\n{p.describe()}"
