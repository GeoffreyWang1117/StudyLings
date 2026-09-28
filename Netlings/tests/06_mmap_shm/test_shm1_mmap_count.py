import os
import random
import re

from studylings.probe import assert_ok, run, strace_run


def expect_counts(exe, path, lines, size):
    r = run(exe, path, timeout=30)
    assert_ok(r, what=f"统计 {os.path.basename(path)}")
    m = re.search(r"lines=(\d+) bytes=(\d+)", r.stdout)
    assert m, f"输出格式应为 'lines=<n> bytes=<n>'，实际 {r.stdout!r}"
    got = (int(m[1]), int(m[2]))
    assert got == (lines, size), f"{os.path.basename(path)}: 应为 lines={lines} bytes={size}，实际 lines={got[0]} bytes={got[1]}"


def test_small_file(exe, tmp_path):
    f = tmp_path / "small.txt"
    data = b"alpha\nbeta\n\ngamma without newline"
    f.write_bytes(data)
    expect_counts(exe, f, 3, len(data))


def test_empty_file(exe, tmp_path):
    f = tmp_path / "empty.txt"
    f.write_bytes(b"")
    expect_counts(exe, f, 0, 0)  # mmap(len=0) 会 EINVAL，要特殊处理


def test_20mib_file(exe, tmp_path):
    f = tmp_path / "big.txt"
    rnd = random.Random(42)
    chunk = bytes(rnd.choice(b"abcdefghij\n") for _ in range(1 << 20))
    data = chunk * 20
    f.write_bytes(data)
    expect_counts(exe, f, data.count(b"\n"), len(data))


def test_no_read_syscalls_on_file(exe, tmp_path):
    f = tmp_path / "mapped.txt"
    data = b"line\n" * 100_000
    f.write_bytes(data)
    r, lines = strace_run(exe, f, trace="read,pread64,readv,mmap")
    assert_ok(r)
    assert "lines=100000 " in r.stdout, f"strace 下输出不对：{r.stdout!r}"
    reads = [l for l in lines if re.search(r"\b(p?read(64|v)?)\(\d+</.*mapped\.txt>", l)]
    assert not reads, "不应该用 read(2) 读这个文件，而应该 mmap 它。strace 看到:\n" + "\n".join(reads[:5])
    maps = [l for l in lines if re.search(r"mmap\(.*\d+</.*mapped\.txt>", l)]
    assert maps, "strace 没有看到对该文件的 mmap 调用"
