import errno
import os

import pytest

from studylings.probe import assert_ok, run

OFFSET = 16 * 1024 * 1024


def python_map(path):
    lines = []
    with open(path, "rb") as f:
        fd, pos = f.fileno(), 0
        while True:
            try:
                start = os.lseek(fd, pos, os.SEEK_DATA)
            except OSError as e:
                if e.errno == errno.ENXIO:
                    break
                raise
            end = os.lseek(fd, start, os.SEEK_HOLE)
            lines.append(f"data {start} {end}")
            pos = end
    lines.append(f"size {os.path.getsize(path)}")
    return lines


def test_create_makes_sparse_file(exe, tmp_path):
    f = tmp_path / "disk.img"
    assert_ok(run(exe, "create", f, OFFSET))
    st = f.stat()
    assert st.st_size == OFFSET + 4, f"文件大小应为 OFFSET+4 = {OFFSET + 4}，实际 {st.st_size}（忘了 lseek？）"
    data = f.read_bytes()
    assert data[:4] == b"head" and data[-4:] == b"tail", "开头应是 head，结尾应是 tail"
    assert data[4:OFFSET].count(0) == OFFSET - 4, "空洞部分读出来应该全是 0"
    if st.st_blocks * 512 >= OFFSET:
        pytest.skip("当前文件系统不支持稀疏文件（st_blocks 没有变小），无法验证空洞不占磁盘")


def test_map_matches_seek_data_hole(exe, tmp_path):
    f = tmp_path / "disk.img"
    with open(f, "wb") as fh:
        fh.write(b"head")
        fh.seek(OFFSET)
        fh.write(b"tail")
    r = run(exe, "map", f)
    assert_ok(r)
    expected = python_map(f)
    assert r.stdout.split("\n")[:-1] == expected, f"期望输出:\n" + "\n".join(expected) + f"\n实际输出:\n{r.stdout}"


def test_map_of_empty_file(exe, tmp_path):
    f = tmp_path / "empty"
    f.write_bytes(b"")
    r = run(exe, "map", f)
    assert_ok(r)
    assert r.stdout.strip() == "size 0", "空文件没有数据区间，只应打印 size 0"
