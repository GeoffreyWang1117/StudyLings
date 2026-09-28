## 提示 1
provided buffer ring 是一个"缓冲区编号的环"：你往里放（`io_uring_buf_ring_add` + `io_uring_buf_ring_advance`），
内核在数据到达时从里面取。recv CQE 的 `cqe->flags` 带 `IORING_CQE_F_BUFFER`，
缓冲区编号是 `cqe->flags >> IORING_CQE_BUFFER_SHIFT`。数据拷走后立刻还回去：
```c
append(c, bufs + bid * BUF_SZ, res);
recycle_buffer(bid);   // = io_uring_buf_ring_add(br, addr, BUF_SZ, bid, mask, 0) + advance(br, 1)
```

## 提示 2
multishot 请求不是"永远有效"的。每个 CQE 都要看 `IORING_CQE_F_MORE`：
没有它，说明请求已经结束。结束原因可能是 EOF（res == 0）、错误、缓冲区用光（`-ENOBUFS`），
也可能是内核为了公平性主动结束。连接还活着就重新挂上：
```c
if (!(flags & IORING_CQE_F_MORE)) {
    c->recv_armed = false;
    if (!c->eof) arm_recv(ring, fd);
}
```
multishot accept 同理（本题 `on_accept` 已经写好了，照着它做）。

## 提示 3
`-ENOBUFS` 不是连接的错误，只是"此刻 16 块缓冲区都在用"；不要因此关闭连接。
为什么 close 之前要确认 `recv_armed == false` 且没有 SEND 在飞？内核的请求持有 socket 的引用，
过早 close 后 fd 号可能被新连接复用，之后到达的旧 CQE 就会被错当成新连接的。
调试：`strace -f -e trace=io_uring_enter,io_uring_register` 能看到缓冲区环的注册（IORING_REGISTER_PBUF_RING）。
