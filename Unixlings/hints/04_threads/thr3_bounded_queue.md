## 提示 1
每个条件变量对应一个"谓词"：not_empty ↔ `count > 0 || closed`，not_full ↔ `count < CAP`。
改变了哪个谓词，就通知对应的条件变量：push 让队列"非空" → signal `not_empty`；pop 让队列"不满" → signal `not_full`。

## 提示 2
`pthread_cond_wait` 返回只说明"有人叫过你"，不说明条件现在成立：可能是虚假唤醒，
也可能在你重新拿到锁之前另一个消费者已经把元素取走了。所以永远写成
`while (!条件) pthread_cond_wait(&cv, &mu);`

## 提示 3
关闭时 `closed = true` 之后要 `pthread_cond_broadcast(&q->not_empty)`：每个睡着的消费者都得醒来，
在 while 里看到 `closed` 再退出。`signal` 只保证至少叫醒一个，其余的会永远睡下去 ——
这正是 Go 里 `close(ch)` 会让所有 `range ch` 的 goroutine 一起退出的原因。
