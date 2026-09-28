## 提示 1
三个函数的分工：
- `on_readable`：read 一块 → `out_append` → `flush_out`（能写多少写多少）
- `flush_out`：从 `out + off` 开始写，`EAGAIN` 就停，写空就把 off/len 归零
- `update_interest`：只看 `pending(c)` 算出该要哪些事件，main 循环每处理完一个事件就调用它

## 提示 2
```c
uint32_t want = 0;
if (pending(c) <= HIGH_WATER) want |= EPOLLIN;
if (pending(c) > 0)           want |= EPOLLOUT;
if (want != c->events) { epoll_ctl(epfd, EPOLL_CTL_MOD, c->fd, &(struct epoll_event){.events = want, .data.ptr = c}); c->events = want; }
```
LT 模式下 EPOLLOUT 是"一直就绪"的，没数据要发还开着它，epoll_wait 会不停返回 → 100% CPU。

## 提示 3
关掉 EPOLLIN 之后，数据会堆在：服务器的接收缓冲区 → A 的发送缓冲区 → A 的 send() 阻塞。
这就是 TCP 的流控把背压一路传回了发送方 —— 服务器自己的内存保持有界。
Node.js 里对应的是 `readable.pause()` / `writable.write() === false` / `'drain'`，
Redis 里对应的是 `client-output-buffer-limit`（超限直接断开连接）。
