import re
import zlib

from studylings.probe import assert_ok, run

NTHREADS = 8


def test_once_and_thread_local(exe):
    r = run(exe, timeout=30)
    assert_ok(r, what="thr4_once_tls")

    m = re.search(r"init_count=(-?\d+)", r.stdout)
    assert m, f"输出应包含 init_count=<n>，实际: {r.stdout!r}"
    assert int(m.group(1)) == 1, (
        f"CRC 表应当恰好构建 1 次，实际 {m.group(1)} 次 —— 用 pthread_once 代替 if (!initialized)")

    rows = {int(t): (int(req), crc, int(err)) for t, req, crc, err in re.findall(
        r"thread (\d+) req=(-?\d+) crc=([0-9a-fA-F]{8}) last_error=(-?\d+)", r.stdout)}
    assert sorted(rows) == list(range(NTHREADS)), f"应有 thread 0..{NTHREADS - 1} 各一行，实际: {r.stdout!r}"
    for t, (req, crc, err) in rows.items():
        assert req == 100 + t, (
            f"thread {t} 读回的请求 id 应为 {100 + t}，实际 {req} —— 被别的线程覆盖了？它需要是 thread_local")
        assert err == (100 + t) % 7, (
            f"thread {t} 的 last_error 应为 {(100 + t) % 7}，实际 {err} —— last_error 也要每线程一份（就像 errno）")
        want = zlib.crc32(f"request-{t}".encode())
        assert int(crc, 16) == want, (
            f"thread {t} 的 CRC 应为 {want:08x}，实际 {crc} —— 是否在表还没建好时就读了它？")
