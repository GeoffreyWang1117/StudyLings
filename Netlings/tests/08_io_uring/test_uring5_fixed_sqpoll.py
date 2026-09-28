import os
import re

import pytest

from studylings.probe import strace_run

CHUNK = 128 * 1024
SIZES = [0, 1, CHUNK - 1, CHUNK, (3 << 20) + 7]
TRACE = "io_uring_setup,io_uring_enter,io_uring_register,read,write,pread64,pwrite64,readv,writev,preadv,pwritev"


def _copy_and_check(exe, tmp_path, urun, size, *flags):
    data = os.urandom(size)
    src = tmp_path / f"src_{size}.bin"
    dst = tmp_path / f"dst_{size}.bin"
    src.write_bytes(data)
    dst.write_bytes(b"stale content that must be truncated" * 1000)
    r = urun(exe, *flags, src, dst, timeout=30)
    if r.returncode != 0:
        pytest.fail(f"拷贝 {size} 字节失败：exit {r.returncode}"
                    f"{'（ASan/LSan 报错）' if r.returncode == 23 else ''}\n--- stdout ---\n{r.stdout}"
                    f"--- stderr ---\n{r.stderr}\n"
                    "-EBADF：固定文件没注册，或 SQE 没有设置 IOSQE_FIXED_FILE；"
                    "-EFAULT：缓冲区没注册或 buf_index 不对", pytrace=False)
    got = dst.read_bytes()
    if got != data:
        bad = next((i for i, (a, b) in enumerate(zip(got, data)) if a != b), min(len(got), len(data)))
        pytest.fail(f"拷贝 {size} 字节：DST 有 {len(got)} 字节，从偏移 {bad} 起与 SRC 不同", pytrace=False)
    return r


@pytest.mark.parametrize("size", SIZES, ids=lambda n: f"{n}B")
def test_copy(exe, tmp_path, urun, size):
    _copy_and_check(exe, tmp_path, urun, size)


@pytest.mark.parametrize("size", [1, (3 << 20) + 7], ids=lambda n: f"{n}B")
def test_copy_sqpoll(exe, tmp_path, urun, size):
    _copy_and_check(exe, tmp_path, urun, size, "--sqpoll")


def _strace_copy(exe, tmp_path, urun, *flags):
    size = 8 << 20
    r0 = _copy_and_check(exe, tmp_path, urun, size, *flags)  # io_uring 不可用则在这里 skip
    src = tmp_path / f"src_{size}.bin"
    dst = tmp_path / f"dst_{size}.bin"
    r, lines = strace_run(exe, *flags, src, dst, trace=TRACE, timeout=60)
    if r.returncode != 0 or dst.read_bytes() != src.read_bytes():
        pytest.fail(f"strace 下拷贝失败 (exit {r.returncode})\n{r.stderr[-2000:]}", pytrace=False)
    return r0, r, lines, str(src), str(dst)


def test_registered_files_and_buffers(exe, tmp_path, urun):
    _, _, lines, src, dst = _strace_copy(exe, tmp_path, urun)
    reg = "\n".join(l for l in lines if "io_uring_register(" in l)
    assert "IORING_REGISTER_FILES" in reg, "strace 没看到 io_uring_register(..., IORING_REGISTER_FILES, ...)：固定文件没有注册"
    assert "IORING_REGISTER_BUFFERS" in reg, "strace 没看到 io_uring_register(..., IORING_REGISTER_BUFFERS, ...)：缓冲区没有注册"
    direct = [l for l in lines if re.search(r"\b(read|write|pread64|pwrite64|readv|writev|preadv|pwritev)\(\d+<", l)
              and (src in l or dst in l)]
    assert not direct, "SRC/DST 应该只通过 io_uring 读写，但 strace 看到了：\n" + "\n".join(direct[:5])


def test_sqpoll_avoids_io_uring_enter(exe, tmp_path, urun):
    r0, r, lines, _, _ = _strace_copy(exe, tmp_path, urun, "--sqpoll")
    out = r0.stdout + r.stdout
    if "SQPOLL unavailable" in out:
        pytest.skip("本机不允许 IORING_SETUP_SQPOLL（程序已退回普通模式）。在 Linux ≥ 5.11 上"
                    "（或以 root 运行）可验证 SQPOLL 的零系统调用提交")
    setup = [l for l in lines if "io_uring_setup(" in l]
    assert any("IORING_SETUP_SQPOLL" in l for l in setup), (
        "--sqpoll 模式下 io_uring_setup 的 flags 里没有 IORING_SETUP_SQPOLL：\n" + "\n".join(setup))
    enters = [l for l in lines if "io_uring_enter(" in l]
    nchunks = (8 << 20) // CHUNK
    assert len(enters) <= 8, (
        f"SQPOLL 模式拷贝 {nchunks} 段用了 {len(enters)} 次 io_uring_enter（应几乎为 0）。"
        "提交由内核线程轮询 SQ 完成；等待完成要轮询 CQ（io_uring_peek_cqe），"
        "不要用 io_uring_wait_cqe / submit_and_wait（它们会 enter 内核）\n" + "\n".join(enters[:5]))
