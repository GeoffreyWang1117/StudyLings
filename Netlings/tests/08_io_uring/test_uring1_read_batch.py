import errno
import os
import re

import pytest

from studylings.probe import strace_run

CHUNK = 64 * 1024
SIZES = [0, 1, CHUNK - 1, (1 << 20) + 123]


@pytest.mark.parametrize("size", SIZES, ids=lambda n: f"{n}B")
def test_content_matches(exe, tmp_path, urun, size):
    data = os.urandom(size)
    f = tmp_path / "input.bin"
    f.write_bytes(data)
    r = urun(exe, f, input=b"", timeout=20)
    if r.returncode != 0:
        pytest.fail(f"exit {r.returncode}（23 = ASan/LSan 报错）\n--- stderr ---\n"
                    f"{r.stderr.decode(errors='replace')}", pytrace=False)
    if r.stdout != data:
        first_bad = next((i for i, (a, b) in enumerate(zip(r.stdout, data)) if a != b),
                         min(len(r.stdout), len(data)))
        pytest.fail(f"{size} 字节的文件：输出 {len(r.stdout)} 字节，内容从偏移 {first_bad}"
                    f"（第 {first_bad // CHUNK} 块）开始不一致。\n"
                    "块要按块号顺序输出（CQE 可能乱序完成）；短读要把剩余部分重新提交；"
                    "最后一块长度是 size - k*64K", pytrace=False)


def test_uses_io_uring_not_read(exe, tmp_path, urun):
    size = 8 << 20  # 128 块
    data = os.urandom(size)
    f = tmp_path / "strace_input.bin"
    f.write_bytes(data)
    urun(exe, f, input=b"", timeout=20)  # 先确认 io_uring 可用（否则 skip），顺便把文件读进 page cache
    r, lines = strace_run(exe, f, trace="io_uring_enter,read,pread64,readv,preadv,preadv2",
                          input=b"", timeout=60)
    if r.returncode != 0 or r.stdout != data:
        pytest.fail(f"strace 下运行失败或输出不对 (exit {r.returncode})\n"
                    f"{r.stderr.decode(errors='replace')[-2000:]}", pytrace=False)
    path = str(f)
    direct = [l for l in lines if re.search(r"\b(read|pread64|readv|preadv2?)\(\d+<", l) and path in l]
    assert not direct, ("文件应该全部通过 io_uring 读取，但 strace 看到了直接的 read 系统调用：\n"
                        + "\n".join(direct[:5]))
    enters = [l for l in lines if "io_uring_enter(" in l]
    nchunks = size // CHUNK
    assert enters, "strace 没看到任何 io_uring_enter —— 真的在用 io_uring 吗？"
    assert len(enters) <= nchunks // 2, (
        f"{nchunks} 个块用了 {len(enters)} 次 io_uring_enter。"
        f"应该一次提交整批（最多 8 个）SQE、一次收割所有已完成的 CQE，而不是每块一次系统调用")


def test_negative_res_is_errno(exe, tmp_path, urun):
    # 目录可以 open(O_RDONLY)，但 read 会失败：io_uring 把 -EISDIR 放进 cqe->res
    d = tmp_path / "a_directory"
    d.mkdir()
    if os.stat(d).st_size == 0:
        pytest.skip("此文件系统上目录的 st_size 为 0，程序不会发起读，无法构造 -EISDIR")
    r = urun(exe, d, input=b"", timeout=20)
    err = r.stderr.decode(errors="replace")
    assert r.returncode not in (0, 23) and r.returncode > 0, (
        f"读目录应该失败并以非 0 退出，实际 exit {r.returncode}，输出了 {len(r.stdout)} 字节。"
        f"cqe->res < 0 就是 -errno，不能当成读到的字节数\n{err}")
    assert os.strerror(errno.EISDIR) in err, (f"错误信息里应包含 strerror(-cqe->res)，即 {os.strerror(errno.EISDIR)!r}：\n{err}")
