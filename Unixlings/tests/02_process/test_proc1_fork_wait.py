import re
import time

import pytest

from studylings.probe import start, zombies_of


def _collect(p, n):
    forked = {}
    for _ in range(n):
        m = p.expect(r"^forked (\d+) code (\d+)$")
        forked[int(m.group(1))] = int(m.group(2))
    return forked


@pytest.mark.parametrize("n", [1, 5, 12])
def test_reaps_all_children_and_decodes_status(exe, n):
    with start(exe, n) as p:
        forked = _collect(p, n)
        p.expect(r"^done$", timeout=10)
        exited = {}
        for line in p.out:
            m = re.match(r"^child (-?\d+) exited (-?\d+)$", line.strip())
            if m:
                exited[int(m.group(1))] = int(m.group(2))
        assert len(exited) == n, f"应回收全部 {n} 个子进程（每个一行 'child <pid> exited <code>'），实际 {len(exited)} 行\n{p.describe()}"
        for pid, code in forked.items():
            assert pid in exited, f"子进程 {pid} 没有被回收\n{p.describe()}"
            assert exited[pid] == code, (
                f"子进程 {pid} 用 _exit({code}) 退出，你打印的是 {exited[pid]} —— "
                f"waitpid 的 status 要用 WEXITSTATUS 解码\n{p.describe()}")
        totals = [l.strip() for l in p.out if l.startswith("total ")]
        assert totals == [f"total {n * (n + 1) // 2}"], f"total 行不对：{totals}\n{p.describe()}"

        # 打印 done 之后程序还活着（阻塞在读 stdin），此时不应有任何僵尸子进程
        zs = []
        for _ in range(10):
            zs = zombies_of(p.pid)
            if not zs:
                break
            time.sleep(0.1)
        assert not zs, f"打印 done 后仍有僵尸子进程 {zs}：没有 waitpid 回收全部子进程"
        p.close_stdin()
        assert p.wait() == 0, f"stdin 关闭后应以 0 退出\n{p.describe()}"
