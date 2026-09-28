import re

import pytest

from studylings.probe import assert_ok, run


@pytest.mark.parametrize("n", [1, 100, 256, 257, 10_000, 1_000_000])
def test_sum_matches(exe, n):
    r = run(exe, n, timeout=60)
    assert_ok(r, what=f"N={n}")
    m = re.search(r"sum=(\d+)", r.stdout)
    assert m, f"输出里应有 sum=<n>，实际 {r.stdout!r}"
    expected = n * (n + 1) // 2
    assert int(m[1]) == expected, (
        f"N={n}: sum 应为 {expected}，实际 {m[1]} —— 有元素被覆盖或读到了还没写好的槽位（检查满/空判定和内存序）")
