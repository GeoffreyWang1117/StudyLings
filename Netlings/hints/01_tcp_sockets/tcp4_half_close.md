## 提示 1
先跑起始代码看它卡住：客户端在 `read` 等回复，服务器在 `recv` 等更多数据（或 EOF）。谁也不让步。
`strace -f -e trace=read,write,shutdown,close` 能直观看到它停在哪。

## 提示 2
`shutdown(fd, SHUT_WR)` 会让内核发 FIN：对端 `read` 返回 0，但这个 fd 仍然可以 `read`。
`close(fd)` 则把读方向也关了，之后到达的数据会触发 RST。

## 提示 3
一行就够：上传循环结束后 `if (shutdown(fd, SHUT_WR) < 0) sl_die("shutdown");`，然后照常读到 EOF。
命令行对照：`nc -N host port < file`（OpenBSD nc）就是 stdin EOF 后调用 shutdown(SHUT_WR)。
