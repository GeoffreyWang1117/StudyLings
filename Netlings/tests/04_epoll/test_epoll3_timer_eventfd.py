import re
import time

import pytest

from studylings.probe import assert_ok, run


def test_ticks_and_wakeups(exe):
    t0 = time.monotonic()
    try:
        r = run(exe, timeout=10)
    except pytest.fail.Exception:
        r = None
    elapsed = time.monotonic() - t0
    if r is None:
        pytest.fail("程序 10s 内没有结束（工作线程 ~0.6s 就写完 5 次 eventfd 了）。\n"
                    "多半是没有 read 出 timerfd/eventfd 的 8 字节计数器：LT 模式下 fd 一直可读，"
                    "epoll_wait 立即返回、事件循环空转，wakeup 永远数不到 5", pytrace=False)
    assert_ok(r, what="epoll3_timer_eventfd")

    wakeups = [int(m) for m in re.findall(r"^wakeup (\d+)$", r.stdout, re.M)]
    ticks = [int(m) for m in re.findall(r"^tick (\d+)$", r.stdout, re.M)]
    assert wakeups, f"没有任何 'wakeup <n>' 行\n--- stdout ---\n{r.stdout}"
    assert all(w >= 1 for w in wakeups), f"wakeup 的值应 >= 1（eventfd 计数器），实际 {wakeups}"
    assert sum(wakeups) == 5, f"wakeup 值之和应恰为 5（工作线程写了 5 次 1），实际 {wakeups} 和为 {sum(wakeups)}"
    assert ticks, f"没有任何 'tick <n>' 行：50ms 周期的 timerfd 在 ~0.6s 内至少应到期一次\n--- stdout ---\n{r.stdout}"
    assert all(t >= 1 for t in ticks), f"tick 的值是到期次数，应 >= 1，实际 {ticks}"
    # 0.6s 左右 / 50ms ≈ 12 次；忙等打印 tick 0 或空转会远超这个数量级
    assert len(ticks) < 200, f"打印了 {len(ticks)} 行 tick，太多了：事件循环在空转？"
    assert elapsed < 8, f"用时 {elapsed:.1f}s，太慢了"
