import re

import pytest

from studylings.probe import assert_ok, run

NBUCKETS, WIDTH = 10, 500


def expected(threads: int, requests: int):
    total_bytes = 0
    hist = [0] * NBUCKETS
    for t in range(threads):
        for i in range(requests):
            total_bytes += i % 1000 + 1
            lat = (i * 7919 + t * 104729) % 5000
            hist[min(lat // WIDTH, NBUCKETS - 1)] += 1
    return threads * requests, total_bytes, hist


@pytest.mark.parametrize("threads,requests", [(1, 1000), (4, 20_000), (8, 5_000)])
def test_exact_counts_without_races(exe, threads, requests):
    r = run(exe, threads, requests, timeout=60)
    assert_ok(r, what=f"THREADS={threads} REQUESTS={requests}")
    m = re.search(r"requests=(\d+) bytes=(\d+) hist=([\d,]+) config=(\S+)", r.stdout)
    assert m, f"输出格式不对：{r.stdout!r}"
    req, nbytes, hist = expected(threads, requests)
    assert int(m[1]) == req, f"requests 应为 {req}，实际 {m[1]}（丢计数 = 非原子的 ++）"
    assert int(m[2]) == nbytes, f"bytes 应为 {nbytes}，实际 {m[2]}"
    got_hist = [int(x) for x in m[3].split(",")]
    assert got_hist == hist, f"直方图应为 {hist}，实际 {got_hist}"
    assert m[4] == "latency-v2", f"config 名字不对：{m[4]!r}"
