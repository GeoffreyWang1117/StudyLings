## 提示 1
UDP 的 `recvfrom` 一次取走一整个数据报，缓冲区装不下的部分直接丢弃。缓冲区要按 64 KiB 开
（UDP 长度字段是 16 位）。可以用 `recvmsg` 看 `MSG_TRUNC` 标志确认有没有被截断。

## 提示 2
`recvfrom` 返回 0 表示收到了一个空数据报，这不是 EOF（UDP 没有 EOF），同样要回显。
只有 `n < 0` 才是错误；`EINTR` 时重试。

## 提示 3
回复地址用 `struct sockaddr_storage peer; socklen_t peer_len = sizeof peer;`，每次循环都重新赋值 `peer_len`，
然后 `sendto(fd, buf, n, 0, (struct sockaddr *)&peer, peer_len)`。
