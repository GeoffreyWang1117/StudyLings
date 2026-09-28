import re
import subprocess

import pytest

from studylings.probe import assert_ok, run, sanitizer_env


def _check(out: str, n: int):
    lines = out.splitlines()
    before = lines.count("before fork")
    assert before == 1, (
        f"stdout 是管道/文件时 'before fork' 出现了 {before} 次（应为 1 次）：fork 复制了还没 flush 的 "
        f"stdio 缓冲区。fork 前要 fflush(stdout)\n--- stdout ---\n{out}")
    assert lines[0] == "before fork", f"第一行应是 'before fork'\n--- stdout ---\n{out}"
    for i in range(1, n + 1):
        got = [l for l in lines if re.fullmatch(rf"child {i} pid \d+", l)]
        assert len(got) == 1, f"'child {i} pid ...' 应恰好出现 1 次，实际 {len(got)} 次\n--- stdout ---\n{out}"
    assert lines.count(f"parent reaped {n}") == 1, f"'parent reaped {n}' 应恰好出现 1 次\n--- stdout ---\n{out}"
    assert len(lines) == n + 2, f"输出应恰好 {n + 2} 行，实际 {len(lines)} 行\n--- stdout ---\n{out}"


@pytest.mark.parametrize("n", [1, 3])
def test_stdout_to_pipe(exe, n):
    r = run(exe, n)
    assert_ok(r)
    _check(r.stdout, n)


def test_stdout_to_file(exe, tmp_path):
    out = tmp_path / "out.txt"
    with open(out, "w") as f:
        rc = subprocess.run([str(exe), "4"], stdout=f, stderr=subprocess.PIPE, text=True,
                            timeout=10, env=sanitizer_env()).returncode
    assert rc == 0, f"stdout 重定向到文件时程序以 {rc} 退出"
    _check(out.read_text(), 4)
