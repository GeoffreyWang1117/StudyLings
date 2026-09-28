## 提示 1
和 epoll 的 `accept` 不同，一个 `IORING_OP_ACCEPT` 请求只产生**一个** CQE。想继续接受新连接，
就得在每次 ACCEPT 完成时再挂一个新的——在 `on_accept` 的第一行调用 `submit_accept(ring, lfd)`。
（Linux 5.19+ 的 multishot accept 可以"挂一次、完成多次"，见 uring3。）

## 提示 2
SEND 的 `cqe->res` 是"这次实际发出去的字节数"，可能小于你请求的长度（本题把 SO_SNDBUF 设小了，
64 KiB 的 send 几乎总是短写）。记账方式：
```c
c->sent += res;
if (c->sent < c->len) { submit_send(ring, fd, bidx); return; }  // 从 buf + sent 继续发
submit_recv(ring, fd, bidx);
```
`submit_send` 已经按 `buf + sent`、`len - sent` 准备请求了。

## 提示 3
为什么"全部发完才能再 RECV"？因为 RECV 会把新数据写进同一块缓冲区；如果旧数据还没发完，
就会被覆盖。每个连接同一时刻只有一个请求在飞，是最简单的"缓冲区所有权"规则。
想看解码：`printf("%#llx\n", ud)`，高 8 位是 op，接着 16 位是 bidx，低 32 位是 fd。
