import shutil

import pytest

from studylings.probe import assert_ok, run


def test_child_does_not_inherit_fds(exe, tmp_path):
    if shutil.which("ls") is None:
        pytest.skip("需要 ls")
    secret = tmp_path / "private.key"
    secret.write_text("-----BEGIN PRIVATE KEY-----\n")
    r = run(exe, secret, "ls", "-l", "/proc/self/fd")
    assert_ok(r, "loaded")
    listing = r.stdout
    assert str(secret) not in listing, f"子进程继承了敏感文件的 fd:\n{listing}"
    assert "eventfd" not in listing, f"子进程继承了 eventfd:\n{listing}"


def test_exit_status_is_propagated(exe, tmp_path):
    secret = tmp_path / "s"
    secret.write_text("x")
    r = run(exe, secret, "sh", "-c", "exit 7")
    assert r.returncode == 7, f"应返回子命令的退出码 7，实际 {r.returncode}"
