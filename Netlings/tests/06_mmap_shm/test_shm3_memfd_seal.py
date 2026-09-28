import re

import pytest

from studylings.probe import run


def test_sealed_memfd_is_immutable(exe):
    r = run(exe, timeout=20)
    out = r.stdout
    m = re.search(r"seals=0x([0-9a-f]+)", out)
    assert m, f"应先打印 seals=0x...，实际输出：\n{out}\n{r.stderr}"
    seals = int(m[1], 16)
    want = 0x1 | 0x2 | 0x4 | 0x8  # SEAL | SHRINK | GROW | WRITE
    assert seals & want == want, (
        f"封印不全：seals=0x{seals:x}，应包含 F_SEAL_WRITE|SHRINK|GROW|SEAL (0x{want:x})")
    assert "content: ok" in out, f"子进程通过只读映射看到的内容不对：\n{out}"
    for what in ["write", "ftruncate-shrink", "ftruncate-grow", "mmap-write", "add-seal"]:
        mm = re.search(rf"^{what}: (.*)$", out, re.M)
        assert mm, f"子进程没有报告 {what} 的结果：\n{out}"
        assert mm[1] == "EPERM", f"封印后 {what} 应当失败且 errno=EPERM，实际：{mm[1]}"
    assert "after attacks: intact" in out, f"内容被改了：\n{out}"
    assert "child exit 0" in out and r.returncode == 0, f"exit {r.returncode}\n{out}\n{r.stderr}"
