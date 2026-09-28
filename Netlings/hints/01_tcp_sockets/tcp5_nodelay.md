## 提示 1
先不改代码，跑一下探针或自己起个服务器，看到 avg_ms≈40。用 `tcpdump -i lo -nn port PORT` 观察：
头部段发出后，body 段要等到约 40ms 后对端的 ACK 回来才发。

## 提示 2
`#include <netinet/tcp.h>`，然后在 connect 之后：
`int one = 1; setsockopt(fd, IPPROTO_TCP, TCP_NODELAY, &one, sizeof one);`

## 提示 3
另一种（通常更好的）修法是根本不发两个小段：把头和 body 拷进一个缓冲区一次 write，
或用 `writev(fd, (struct iovec[]){{&be_len, 4}, {body, len}}, 2)`。很多服务器两者都做：
TCP_NODELAY 保证低延迟，同时自己合并写以减少系统调用和小包。
