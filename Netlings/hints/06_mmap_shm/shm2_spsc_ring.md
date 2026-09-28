## 提示 1
head 和 tail 是"只增不减"的计数，不是下标。元素个数 = `head - tail`（无符号减法回绕也没问题）。
空：`head - tail == 0`；满：`head - tail == CAP`。写成 `> CAP` 会多写一个，覆盖还没读的数据。

## 提示 2
把 `size_t head, tail` 改成 `_Atomic size_t`。每一方读**自己**的计数器用 `memory_order_relaxed`
（没人跟你抢着写），读**对方**的计数器用 `memory_order_acquire`，更新自己的计数器用 `memory_order_release`。

## 提示 3
release/acquire 成对出现：生产者"写槽位 → release 写 head"，消费者"acquire 读 head → 读槽位"，
于是消费者看到新 head 时一定能看到槽位里的新数据。反方向（消费者 release tail，生产者 acquire tail）
保证生产者不会在消费者读完之前覆盖槽位。io_uring 的 `io_uring_smp_store_release` / `io_uring_smp_load_acquire`
就是一模一样的用法。用 `-O2` 编译（nosan preset）时，非原子的 `while (r->head == t)` 可能被编译器
提升成死循环 —— 这就是"卡死"的来源。
