## 提示 1
hints 里 `ai_family = AF_UNSPEC` 表示"v4 和 v6 都要"，`ai_socktype = SOCK_STREAM` 让每个地址只返回一条 TCP 结果。
可以先用 `getent ahosts localhost` 看看本机 localhost 解析出哪些地址、什么顺序。

## 提示 2
循环骨架：
`for (ai = res; ai; ai = ai->ai_next) { fd = socket(ai->ai_family, ai->ai_socktype | SOCK_CLOEXEC, ai->ai_protocol); ... if (connect(fd, ai->ai_addr, ai->ai_addrlen) == 0) break; close(fd); fd = -1; }`
注意 `socket()` 的参数全部来自 `ai`，这样代码里不会出现任何 AF_INET/AF_INET6 字样。

## 提示 3
`close()` 可能会改写 errno，所以要在 close 之前把 connect 的 errno 存到 `last_err`，
循环结束、全部失败时再 `errno = last_err`。别忘了在返回前 `freeaddrinfo(res)`（否则 LeakSanitizer 会报泄漏）。
