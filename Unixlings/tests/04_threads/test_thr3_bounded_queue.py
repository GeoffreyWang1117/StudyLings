import re
import subprocess

import pytest

from studylings.probe import start

ITEMS = 5000
TIMEOUT = 15


@pytest.mark.parametrize("producers,consumers", [(1, 1), (4, 1), (1, 4), (3, 3), (6, 2), (0, 4)])
def test_all_items_consumed_exactly_once(exe, producers, consumers):
    with start(exe, producers, consumers, ITEMS) as p:
        try:
            rc = p.p.wait(timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            pytest.fail(
                f"P={producers} C={consumers}: {TIMEOUT}s 内没有结束 —— 有线程睡在条件变量上再也没人叫醒。\n"
                "检查：push 之后通知的是 not_empty 吗？queue_close 有没有 broadcast 叫醒所有消费者？\n"
                f"{p.describe()}", pytrace=False)
        p.wait()
        if rc != 0:
            extra = "（ThreadSanitizer 发现数据竞争）" if rc == 66 else ""
            pytest.fail(f"P={producers} C={consumers}: exit {rc}{extra}\n{p.describe()}", pytrace=False)
        m = re.search(r"consumed=(-?\d+) sum=(-?\d+)", p.stdout)
        assert m, f"输出应为 consumed=<n> sum=<n>，实际: {p.stdout!r}"
        n = producers * ITEMS
        count, total = int(m.group(1)), int(m.group(2))
        assert count == n and total == n * (n + 1) // 2, (
            f"P={producers} C={consumers}: 应为 consumed={n} sum={n * (n + 1) // 2}，实际 consumed={count} sum={total}。"
            "元素丢了或被重复取/凭空取出 —— pthread_cond_wait 返回后有没有用 while 重新检查条件？")
