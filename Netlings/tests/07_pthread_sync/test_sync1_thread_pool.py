import re

import pytest

from studylings.probe import assert_ok, run


@pytest.mark.parametrize("n,m,idle_ms", [
    (1, 50, 0),
    (4, 2000, 0),
    (8, 500, 0),
    (16, 3000, 0),
    (4, 10, 300),   # 提交后主线程先睡 300ms：关闭时所有 worker 都睡在条件变量上
    (6, 0, 100),    # 没有任务的池也要能关闭
])
def test_pool_runs_all_tasks_and_shuts_down(exe, n, m, idle_ms):
    r = run(exe, n, m, idle_ms, timeout=20)
    assert_ok(r, what=f"N={n} M={m} IDLE_MS={idle_ms}")
    mm = re.search(r"done=(\d+) total=(\d+)", r.stdout)
    assert mm, f"输出应为 'done=<M> total=<sum>'，实际 {r.stdout!r}"
    done, total = int(mm[1]), int(mm[2])
    assert done == m, f"N={n} M={m}: 只执行了 {done} 个任务 —— 关闭时要先把队列里剩下的任务做完再让 worker 退出"
    assert total == m * (m + 1) // 2, f"total 应为 {m * (m + 1) // 2}，实际 {total}"
