import os
import re

import pytest

from studylings.probe import assert_ok, run, strace_run


def test_content_replaced_and_no_leftovers(exe, tmp_path):
    cfg = tmp_path / "app.conf"
    cfg.write_text("old = 1\n")
    new = os.urandom(200_000)
    assert_ok(run(exe, cfg, input=new))
    assert cfg.read_bytes() == new, "文件内容与 stdin 不一致"
    leftovers = [p.name for p in tmp_path.iterdir() if p.name != "app.conf"]
    assert not leftovers, f"目录里残留了临时文件: {leftovers}"
    assert (cfg.stat().st_mode & 0o777) == 0o644, f"新文件权限应为 0644，实际 {oct(cfg.stat().st_mode & 0o777)}"


def test_syscall_sequence(exe, tmp_path):
    cfg = tmp_path / "app.conf"
    cfg.write_text("old\n")
    r, lines = strace_run(exe, cfg, input=b"new content\n",
                          trace="openat,open,creat,rename,renameat,renameat2,fsync,fdatasync")
    assert_ok(r)
    target = re.escape(str(cfg))
    trunc = [l for l in lines if re.search(rf'open(at)?\(.*"{target}".*O_TRUNC', l)]
    assert not trunc, f"不能以 O_TRUNC 直接打开目标文件（读者会看到半截文件）:\n{trunc[0]}"
    idx_rename = next((i for i, l in enumerate(lines)
                       if re.search(rf'rename(at2?)?\(.*"{target}"', l) and "= 0" in l), None)
    assert idx_rename is not None, "没有看到 rename(临时文件, 目标) 调用"
    assert any(re.match(r"(\d+ +)?f(data)?sync\(", l) for l in lines[:idx_rename]), \
        "rename 之前必须 fsync 临时文件，否则断电后可能得到一个空的新文件"
    assert any(re.match(r"(\d+ +)?fsync\(\d+<.*>", l) and "/" in l for l in lines[idx_rename:]), \
        "rename 之后应 fsync 所在目录，让 rename 本身持久化"


def test_failure_leaves_original(exe, tmp_path):
    missing_dir = tmp_path / "no" / "such" / "dir" / "app.conf"
    r = run(exe, missing_dir, input="x")
    assert r.returncode != 0, "目标目录不存在时应失败"
