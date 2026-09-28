## 提示 1
读者：`pthread_rwlock_rdlock(&c->lock); v = c->slots[k]; pthread_rwlock_unlock(&c->lock);`
写者：`pthread_rwlock_wrlock` … 两个字段都写完 … `pthread_rwlock_unlock`。

## 提示 2
锁要覆盖"整个不变式"：只锁住 a 的写、不锁 b 的写，读者照样会看到 a 和 b 对不上。
临界区里只做拷贝，别在持锁时做耗时操作（I/O、日志）——读锁持有越久，写者等得越久。

## 提示 3
TSan 报告里 "Write of size 8 … by thread T5" / "Previous read … by thread T1" 指出了冲突的两处代码。
想想为什么即使读写在时间上"没撞上"，TSan 也会报：它检查的是 happens-before 关系，而不是运气。
