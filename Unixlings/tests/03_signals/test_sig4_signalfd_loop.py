import signal

import pytest

from studylings.probe import start


def _check_alive(p, what):
    if p.p.poll() is not None:
        rc = p.p.returncode
        why = f"被信号 {signal.Signals(-rc).name} 杀死" if rc < 0 else f"exit {rc}"
        pytest.fail(f"{what}后进程{why}——信号没有在创建 signalfd 之前被 sigprocmask 阻塞？\n"
                    + p.describe(), pytrace=False)


def test_reload_echo_and_term(exe):
    with start(exe) as p:
        p.expect(r"^ready", timeout=10)
        for i in range(2):
            p.signal(signal.SIGHUP)
            try:
                p.expect(r"^reload$", timeout=10)
            except BaseException:
                _check_alive(p, f"第 {i + 1} 次 SIGHUP ")
                raise
        p.write("hello loop\n")
        p.expect(r"^echo: hello loop$", timeout=10)
        p.signal(signal.SIGTERM)
        try:
            p.expect(r"^bye$", timeout=10)
        except BaseException:
            _check_alive(p, "SIGTERM ")
            raise
        rc = p.wait(timeout=10)
        assert rc == 0, f"收到 SIGTERM 后应以 0 退出，实际 {rc}\n{p.describe()}"
        assert p.stdout.count("reload") == 2, f"两次 SIGHUP 应恰好打印两行 reload\n{p.describe()}"


def test_sigint_and_multiple_lines(exe):
    with start(exe) as p:
        p.expect(r"^ready", timeout=10)
        p.write("a\nb\n")
        p.expect(r"^echo: a$", timeout=10)
        p.expect(r"^echo: b$", timeout=10)
        p.signal(signal.SIGINT)
        try:
            p.expect(r"^bye$", timeout=10)
        except BaseException:
            _check_alive(p, "SIGINT ")
            raise
        assert p.wait(timeout=10) == 0, p.describe()
