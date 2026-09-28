import re

import pytest

from studylings.probe import assert_ok, run

LIMIT = 10_000_000
EXPECTED = LIMIT * (LIMIT + 1) // 2


@pytest.mark.parametrize("nthreads", [1, 4, 7])
def test_parallel_sum(exe, nthreads):
    r = run(exe, nthreads, timeout=60)
    assert_ok(r, what=f"NTHREADS={nthreads}")
    m = re.search(r"sum=(-?\d+)", r.stdout)
    assert m, f"输出里应有一行 sum=<n>，实际: {r.stdout!r}"
    got = int(m.group(1))
    assert got == EXPECTED, (
        f"NTHREADS={nthreads} 时 sum 应为 {EXPECTED}，实际 {got}。"
        f"检查每个线程是否拿到了自己独立的区间（是不是把 &i 传给了所有线程？最后一段有没有收掉余数？）")
