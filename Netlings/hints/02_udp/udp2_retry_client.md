## 提示 1
先观察：对一个没人监听的 UDP 端口发包，`tcpdump -i lo -nn icmp` 能看到 ICMP port unreachable 回来了，
但未连接的 socket 永远收不到这个错误，只能超时。

## 提示 2
`connect(fd, res->ai_addr, res->ai_addrlen)` 之后就可以 `freeaddrinfo(res)`，并把 `sendto` 换成 `send`。
之后 `recv`（或 `send`）返回 -1 且 `errno == ECONNREFUSED` → 打印 refused，exit 2。

## 提示 3
重传循环：`for (attempt = 0; attempt < MAX_TRIES; attempt++) { send; poll(&pfd, 1, TIMEOUT_MS); if (n == 0) continue; recv...; }`，
循环结束还没拿到回复就打印 timeout，exit 3。poll 返回 POLLERR 时直接去 recv 就能取到错误码。
