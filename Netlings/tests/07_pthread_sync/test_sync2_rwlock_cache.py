import re

import pytest

from studylings.probe import assert_ok, run


@pytest.mark.parametrize("readers,iters", [(1, 20_000), (4, 20_000), (8, 10_000)])
def test_readers_never_see_torn_values(exe, readers, iters):
    r = run(exe, readers, iters, timeout=60)
    assert_ok(r, what=f"READERS={readers} ITERS={iters}")
    m = re.search(r"reads=(\d+) writes=(\d+) torn=(\d+)", r.stdout)
    assert m, f"输出应为 'reads=<n> writes=<n> torn=<n>'，实际 {r.stdout!r}"
    reads, writes, torn = map(int, m.groups())
    assert torn == 0, f"读者看到了 {torn} 个不一致（撕裂）的值：读写都要在锁内完成"
    assert reads == readers * iters, f"reads 应为 {readers * iters}，实际 {reads}"
    assert writes == iters // 10 + 1, f"writes 应为 {iters // 10 + 1}，实际 {writes}"
