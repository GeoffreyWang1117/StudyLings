## 提示 1
`struct ucred`（需要 `_GNU_SOURCE`，CMake 已经定义）有三个字段：`pid`、`uid`、`gid`。
它描述的是**连接对端**在 connect()（或 socketpair()）那一刻的身份。

## 提示 2
`socklen_t len = sizeof(*out); getsockopt(fd, SOL_SOCKET, SO_PEERCRED, out, &len);`
注意要对**已连接的** socket（accept 返回的 fd）调用，而不是监听 socket。

## 提示 3
`ss -xp` 可以看到每个 UDS 连接两端的进程。PostgreSQL 的 peer 认证只用到 uid：
`getpwuid(cred.uid)->pw_name` 与请求登录的数据库用户名比较。
