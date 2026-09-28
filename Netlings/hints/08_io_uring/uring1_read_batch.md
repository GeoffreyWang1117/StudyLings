## 提示 1
io_uring 的基本节奏只有三步：
1. `io_uring_get_sqe(&ring)` 拿一个空的 SQE（提交队列项），用 `io_uring_prep_*` 填好，`io_uring_sqe_set_data64` 贴上"这是谁"的标签；
2. `io_uring_submit_and_wait(&ring, 1)` —— **一次系统调用**把所有准备好的 SQE 交给内核，并至少等 1 个完成；
3. `io_uring_for_each_cqe` 遍历 CQE（完成队列项），处理完用 `io_uring_cq_advance(&ring, n)` 一次性归还。

和 epoll 不同，你拿到的不是"可以读了"，而是"已经读完了，结果是 `cqe->res`"。

## 提示 2
`prep_chunk` 只需三行：
```c
struct io_uring_sqe *sqe = io_uring_get_sqe(ring);
if (!sqe) return false;
io_uring_prep_read(sqe, fd, s->buf + s->got, s->len - s->got, s->off + s->got);
io_uring_sqe_set_data64(sqe, idx);
```
把 `got` 算进地址、长度和偏移里，短读后重新调用它就只会读剩下的部分。

## 提示 3
`cqe->res` 的约定：`>= 0` 是字节数，`< 0` 是 **负的 errno**（io_uring 从不设置全局 `errno`；
liburing 函数的返回值也是同样的约定）。所以要 `strerror(-res)`。
读目录时内核返回 `-EISDIR`；把它当字节数用就会把未初始化的缓冲区输出出去。
用 `strace -f -e trace=io_uring_enter ./uring1_read_batch big.bin > /dev/null` 数一数系统调用次数。
