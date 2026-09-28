## 提示 1
worker 醒来后有三种情况：队列有任务（不管是否在关闭，都先干活）；队列空且在关闭（退出）；
队列空且没关闭（继续等 —— while 循环已经处理了）。所以退出判断应该看 `p->head == nullptr`。

## 提示 2
`pthread_cond_signal` 至少唤醒一个等待者，`pthread_cond_broadcast` 唤醒全部。
"状态变化对所有等待者都有意义"（比如关闭）时必须用 broadcast。

## 提示 3
卡住时用 `gdb -p <pid>` 然后 `thread apply all bt`，会看到几个 worker 停在 `pthread_cond_wait`，
主线程停在 `pthread_join`。这种"丢失的唤醒"是线程池最常见的关停 bug。
