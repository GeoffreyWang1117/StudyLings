## 提示 1
`static pthread_mutex_t g_lock = PTHREAD_MUTEX_INITIALIZER;` 就能得到一个可用的互斥量，
不需要 `pthread_mutex_init` / `destroy`（静态存储期的互斥量用宏初始化即可）。

## 提示 2
"检查余额够不够" 和 "扣款/入账" 必须在同一次加锁里完成，否则两个线程可能同时看到余额 = 1，
然后都扣款，余额变成 -1 —— 这叫 check-then-act 竞争。`g_attempts++` 也要在锁内。

## 提示 3
临界区只放读写共享变量的那几行：`pthread_mutex_lock` → if/扣款/入账/计数 → `pthread_mutex_unlock`。
`risk_score()` 这种纯计算放在锁外，锁持有时间越短，线程之间的串行化越少。
（进阶：如果每个账户一把锁，转账要同时拿两把 —— 必须按固定顺序加锁才能避免死锁，见 APUE §11.6.2。）
