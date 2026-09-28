import re

import pytest

from studylings.probe import assert_ok, run


@pytest.mark.parametrize("nthreads,iters", [(1, 20000), (2, 20000), (4, 50000), (8, 10000)])
def test_transfers_are_consistent(exe, nthreads, iters):
    r = run(exe, nthreads, iters, timeout=60)
    assert_ok(r, what=f"NTHREADS={nthreads} ITERS={iters}")
    m = re.search(r"total=(-?\d+) attempts=(-?\d+) min=(-?\d+)", r.stdout)
    assert m, f"输出应为 total=<n> attempts=<n> min=<n>，实际: {r.stdout!r}"
    total, attempts, low = map(int, m.groups())
    assert total == 4000, f"转账不会凭空造钱或丢钱：total 应为 4000，实际 {total}（有丢失的更新？）"
    assert attempts == nthreads * iters, (
        f"attempts 应为 {nthreads}*{iters}={nthreads * iters}，实际 {attempts}（g_attempts++ 没被保护？）")
    assert low >= 0, f"余额不能为负，实际最小余额 {low}（检查余额和扣款必须在同一个临界区里）"
