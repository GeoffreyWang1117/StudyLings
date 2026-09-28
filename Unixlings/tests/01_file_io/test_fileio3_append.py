import re
from collections import Counter

from studylings.probe import assert_ok, run

NPROC, NLINES = 8, 3000


def test_no_lost_lines(exe, tmp_path):
    log = tmp_path / "access.log"
    for attempt in range(3):  # 竞态是概率性的：多跑几轮，任何一轮丢行都算失败
        log.unlink(missing_ok=True)
        assert_ok(run(exe, log, NPROC, NLINES, timeout=60))
        lines = log.read_text().splitlines()
        bad = [l for l in lines if not re.fullmatch(r"worker \d+ line \d+", l)]
        assert not bad, f"第 {attempt + 1} 轮出现被截断/交错的行，例如 {bad[:3]}"
        counts = Counter(l.split()[1] for l in lines)
        lost = NPROC * NLINES - len(lines)
        assert lost == 0, (f"第 {attempt + 1} 轮丢了 {lost} 行（共应 {NPROC * NLINES} 行），"
                           f"各 worker 实际行数: {dict(sorted(counts.items()))}")
