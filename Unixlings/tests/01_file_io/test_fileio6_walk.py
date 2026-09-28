import os

from studylings.probe import assert_ok, run


def build_tree(root):
    (root / "src" / "net" / "deep" / "er").mkdir(parents=True)
    (root / "empty").mkdir()
    (root / "README.md").write_text("hello\n")
    (root / "src" / "main.c").write_text("int main(void){}\n")
    (root / "src" / "net" / "deep" / "er" / "x.bin").write_bytes(b"\0" * 1000)
    os.symlink("..", root / "src" / "net" / "parent")          # 指向父目录：跟随就会无限递归
    os.symlink("/nonexistent/target", root / "dangling")        # 悬空链接：stat 会失败，lstat 不会
    os.mkfifo(root / "fifo")
    return sorted([
        "f 6 README.md",
        "d - empty",
        "d - src",
        "f 17 src/main.c",
        "d - src/net",
        "l 2 src/net/parent",
        "d - src/net/deep",
        "d - src/net/deep/er",
        "f 1000 src/net/deep/er/x.bin",
        "l 19 dangling",
        "o - fifo",
    ])


def test_walk_tree(exe, tmp_path):
    root = tmp_path / "tree"
    root.mkdir()
    expected = build_tree(root)
    r = run(exe, root, timeout=10)
    assert_ok(r)
    got = sorted(r.stdout.splitlines())
    missing = set(expected) - set(got)
    extra = set(got) - set(expected)
    assert not missing and not extra, (
        f"缺少: {sorted(missing)}\n多余: {sorted(extra)[:10]}"
        + ("\n（出现 parent/... 说明跟随了符号链接）" if any("parent/" in l for l in extra) else ""))


def test_missing_dir_fails(exe, tmp_path):
    r = run(exe, tmp_path / "nope")
    assert r.returncode != 0
