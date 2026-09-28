## 提示 1
注册只做一次，放在进入主循环之前：
```c
int fds[2] = {[FIX_SRC] = src, [FIX_DST] = dst};
int r = io_uring_register_files(ring, fds, 2);          // 之后 SQE 里用下标 0/1 + IOSQE_FIXED_FILE
r = io_uring_register_buffers(ring, iov, QD);           // 之后 read_fixed/write_fixed 用 buf_index 0..QD-1
```
返回值同样是 `-errno`。注册缓冲区会 pin 内存，计入 `RLIMIT_MEMLOCK`（`ulimit -l`），太小会得到 `-ENOMEM`。

## 提示 2
写阶段和读阶段对称：
```c
io_uring_prep_write_fixed(sqe, FIX_DST, buf, n, off, i);
```
`buf` 可以指向已注册缓冲区内部的任意位置（短写后从 `pos` 继续），但 `buf_index` 必须是它所属的那块。

## 提示 3
SQPOLL 下"零系统调用"的原理：`io_uring_submit` 只写共享内存并推进 SQ tail，内核线程
`iou-sqp-<pid>`（`ps -eLf | grep iou-sqp` 可见）会取走；只有它睡着了（`IORING_SQ_NEED_WAKEUP`）
才 enter 一次叫醒。等待完成也要避开 `io_uring_wait_cqe`——本题用 `io_uring_peek_cqe` 轮询 CQ。
对比：`strace -f -c -e trace=io_uring_enter ./uring5_fixed_sqpoll [--sqpoll] big.bin out.bin`。
