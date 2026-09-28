## 提示 1
`cat /proc/sys/net/ipv4/tcp_available_congestion_control` 看内核有哪些算法，
`tcp_allowed_congestion_control` 是非 root 可以按 socket 选择的那部分。先想一想：为什么请求 cubic
读回来却是系统默认值？setsockopt 的返回值是多少？

## 提示 2
TCP 层的选项要用 `IPPROTO_TCP`（也可以写 `SOL_TCP`）作为 level；`SOL_SOCKET` 是通用 socket 层，
那一层的 13 号选项是 SO_LINGER，和 TCP_CONGESTION 同号纯属巧合。

## 提示 3
```c
return setsockopt(fd, IPPROTO_TCP, TCP_CONGESTION, algo, (socklen_t)strlen(algo));
```
调用处已经会在失败时打印 `TCP_CONGESTION '<algo>': <strerror>` 并 exit 1 —— 前提是你把错误返回出去。
