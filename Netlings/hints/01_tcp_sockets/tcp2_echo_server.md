## 提示 1
先亲手看一眼 TIME_WAIT：跑起起始代码，用 `nc 127.0.0.1 PORT` 发一行 `quit`，然后
`ss -tan | grep PORT`（或 `cat /proc/net/tcp`，状态 06），再 Ctrl-C 服务器立刻重启——`bind: Address already in use`。

## 提示 2
两个 `setsockopt` 都要在 `bind` 之前：
`int on = 1, off = 0;`
`setsockopt(fd, IPPROTO_IPV6, IPV6_V6ONLY, &off, sizeof off);`（只在 family == AF_INET6 时）
`setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &on, sizeof on);`

## 提示 3
`listen(fd, SOMAXCONN)`；`accept4(lfd, nullptr, nullptr, SOCK_CLOEXEC)`。
可以用 `ls -l /proc/<pid>/fd` 与 `grep flags /proc/<pid>/fdinfo/<fd>` 检查 O_CLOEXEC（八进制 02000000 位）。
