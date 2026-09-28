## 提示 1
属性两件套：`pthread_mutexattr_setpshared(&attr, PTHREAD_PROCESS_SHARED)` 让锁可以放在共享内存里跨进程用，
`pthread_mutexattr_setrobust(&attr, PTHREAD_MUTEX_ROBUST)` 让内核在持有者死亡时"通知"下一个加锁者。

## 提示 2
`pthread_mutex_lock` 返回 `EOWNERDEAD` 时**你已经持有锁**。流程：修复数据 → `pthread_mutex_consistent` →
正常使用 → `pthread_mutex_unlock`。如果修不好，直接 unlock（不调用 consistent），锁会进入
`ENOTRECOVERABLE` 状态，所有人都会知道这份数据坏了。

## 提示 3
原理：glibc 把当前线程持有的 robust mutex 挂在一个链表上并通过 `set_robust_list(2)` 告诉内核；
线程退出时内核遍历这个链表，给锁字（futex word）打上 `FUTEX_OWNER_DIED` 位并唤醒等待者。
卡住时 `cat /proc/<pid>/wchan` 会看到 `futex_wait_queue`（或类似）。
