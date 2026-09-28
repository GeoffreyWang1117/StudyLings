import os
import re

from studylings.probe import assert_ok, run, strace_run


def test_copies_files_in_order(exe, tmp_path):
    a, b = tmp_path / "a.txt", tmp_path / "b.bin"
    a.write_text("hello\n")
    b.write_bytes(os.urandom(300_000))
    r = run(exe, a, b, input=b"")
    assert_ok(r)
    assert r.stdout == a.read_bytes() + b.read_bytes(), "输出内容与文件不一致"


def test_reads_stdin_without_args(exe):
    data = os.urandom(100_000)
    r = run(exe, input=data)
    assert_ok(r)
    assert r.stdout == data, "没有文件参数时应该把 stdin 拷贝到 stdout"


def test_missing_file_reports_and_continues(exe, tmp_path):
    ok = tmp_path / "ok.txt"
    ok.write_text("still printed\n")
    r = run(exe, tmp_path / "nope", ok)
    assert r.returncode == 1, "有文件打不开时退出码应为 1"
    assert "still printed" in r.stdout, "打不开一个文件后应该继续处理后面的文件"
    assert re.search(r"nope: No such file or directory", r.stderr), f"stderr 应包含错误原因，实际: {r.stderr!r}"


def test_bufsize_controls_read_count(exe, tmp_path):
    """复现 APUE 图 3.6 的"read 次数"一列：次数 ≈ 文件大小 / BUFSIZE + 1（最后一次读到 EOF）。"""
    f = tmp_path / "data.bin"
    f.write_bytes(os.urandom(64 * 1024))
    for bufsize, expected in [(4096, 17), (512, 129), (65536, 2)]:
        r, lines = strace_run(exe, "-b", bufsize, f, trace="read")
        assert_ok(r)
        reads = [l for l in lines if re.search(r"read\(\d+</.*data\.bin>", l)]
        assert len(reads) == expected, (
            f"-b {bufsize} 时应恰好 read 该文件 {expected} 次，实际 {len(reads)} 次")
