## 提示 1
非阻塞 connect 的三种结果：
- 返回 0：已经连上（回环地址上偶尔会立即完成）
- 返回 -1 且 `errno == EINPROGRESS`：握手进行中，去 poll
- 返回 -1 且其他 errno（比如立刻就 ECONNREFUSED）：直接出结果

## 提示 2
`poll(&(struct pollfd){.fd = fd, .events = POLLOUT}, 1, timeout_ms)`：
返回 0 就是超时；返回 1 只说明"握手结束了"，成功还是失败要看
`getsockopt(fd, SOL_SOCKET, SO_ERROR, &err, &len)` 里的 `err`（0 表示成功）。
失败时 revents 里常常同时有 POLLOUT|POLLERR|POLLHUP，不能只凭 revents 判断。

## 提示 3
poll 被信号打断（EINTR）时不要用原来的 timeout 重新等，否则总等待时间会超过预期：
先算出 `deadline = now_ms() + timeout_ms`，每次重试用 `deadline - now_ms()`。
自己造一个黑洞试试：`python3 -c "import socket,time; s=socket.socket(); s.bind(('127.0.0.1',9999)); s.listen(0); c=socket.create_connection(('127.0.0.1',9999)); time.sleep(600)"`，
然后 `time ./build/dev/bin/poll3_connect_timeout 127.0.0.1 9999 300`。
