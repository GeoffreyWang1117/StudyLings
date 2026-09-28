## 提示 1
`IOSQE_IO_LINK` 设在**前一个** SQE 上，意思是"下一个 SQE 依赖我"。
`IORING_OP_LINK_TIMEOUT` 永远作用于链上紧挨在它前面的那个请求——所以前面那个请求必须带 `IOSQE_IO_LINK`。

## 提示 2
在 `prep_recv_with_timeout` 里：
```c
io_uring_prep_recv(sqe, fd, buf, cap, 0);
sqe->flags |= IOSQE_IO_LINK;
```
一个链在一次 `io_uring_enter` 里提交，每个 SQE 都会产生自己的 CQE（被取消的也会），所以本轮要收齐 3 个（或 2 个）CQE。

## 提示 3
三种结局对应的 CQE：

| 情况 | CONNECT | RECV | LINK_TIMEOUT |
|---|---|---|---|
| 收到数据 | 0 | >0 | -ECANCELED（定时器被取消） |
| 超时 | 0 | -ECANCELED | -ETIME |
| 被拒绝 | -ECONNREFUSED | -ECANCELED | -ECANCELED |

`strace -f -e trace=io_uring_enter` 可以看到第一轮三个 SQE 只用了一次系统调用。
