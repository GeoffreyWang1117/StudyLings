from studylings.probe import assert_ok, run


def test_lines_go_to_the_right_place(exe, tmp_path):
    out = tmp_path / "captured.txt"
    r = run(exe, out)  # stdout 是管道 → 全缓冲
    assert_ok(r)
    assert r.stdout == "line 1: original stdout\nline 3: original stdout again\n", (
        f"原 stdout 应只有第 1、3 行，实际:\n{r.stdout!r}")
    assert out.exists(), "没有创建输出文件"
    assert out.read_text() == "line 2: redirected into file\n", (
        f"文件里应只有第 2 行，实际:\n{out.read_text()!r}\n"
        "（第 1 行跑进文件 → 切换前没 fflush；第 3 行跑进文件 → 恢复前没 fflush 或没恢复）")
