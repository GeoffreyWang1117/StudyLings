import signal

import pytest

from studylings.probe import start


def _shutdown_with(exe, sig):
    with start(exe) as p:
        p.expect(r"^ready", timeout=10)
        p.signal(sig)
        rc = p.wait(timeout=10)
        if rc < 0:
            pytest.fail(f"收到 {sig.name} 后进程被信号 {signal.Signals(-rc).name} 直接杀死了——"
                        f"没有安装处理函数，收尾代码一行都没执行\n{p.describe()}", pytrace=False)
        assert rc == 0, f"优雅关闭后退出码应为 0，实际 {rc}\n{p.describe()}"
        assert "graceful shutdown" in p.stdout, f"没有打印 graceful shutdown\n{p.describe()}"


def test_sigterm_graceful(exe):
    """kubectl delete pod / docker stop 发送的就是 SIGTERM。"""
    _shutdown_with(exe, signal.SIGTERM)


def test_sigint_graceful(exe):
    """终端里按 Ctrl-C 发送的是 SIGINT。"""
    _shutdown_with(exe, signal.SIGINT)


def test_keeps_running_without_signal(exe):
    with start(exe) as p:
        p.expect(r"^ready", timeout=10)
        try:
            rc = p.p.wait(timeout=1)
        except Exception:
            return
        pytest.fail(f"没收到信号时程序应该一直运行，但它以 {rc} 退出了\n{p.describe()}", pytrace=False)
