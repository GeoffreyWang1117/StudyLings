## 提示 1
`accept4(lfd, nullptr, nullptr, SOCK_NONBLOCK | SOCK_CLOEXEC)` 一步到位，
省掉 `accept` + 两次 `fcntl`，也没有"accept 之后、设置 CLOEXEC 之前另一个线程 fork 了"的竞态。

## 提示 2
注册新连接：
```c
struct epoll_event ev = {.events = EPOLLIN, .data.fd = cfd};
if (epoll_ctl(epfd, EPOLL_CTL_ADD, cfd, &ev) < 0) { perror("epoll_ctl ADD"); close(cfd); }
```
`data` 是一个 union，内核原样还给你；真实服务器常放 `data.ptr = conn`（指向连接结构体）。

## 提示 3
`close_conn`：`epoll_ctl(epfd, EPOLL_CTL_DEL, fd, nullptr)` 然后 `close(fd)`。
（Linux 2.6.9 以后 DEL 的 event 参数可以是 nullptr。）
检查自己的 fd 标志：`cat /proc/$(pgrep epoll1_lt_echo)/fdinfo/4`，`flags:` 是八进制，
`02000000` 是 O_CLOEXEC，`04000` 是 O_NONBLOCK。
