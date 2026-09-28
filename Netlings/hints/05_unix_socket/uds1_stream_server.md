## 提示 1
陈旧文件：`bind` 之前 `if (unlink(path) < 0 && errno != ENOENT) sl_die("unlink");`。
想一想为什么不能"先 connect 试试看有没有人在用"再决定？（有，但那是 systemd 这类管理者的事；
一般服务器在启动时认定这个路径归自己。）

## 提示 2
优雅退出：主循环因为 `g_stop` 结束后，`close(lfd)`，然后 `unlink(path)`。
抽象地址（`@name`）没有文件，两处 unlink 都要跳过。

## 提示 3
抽象地址的 addrlen：`offsetof(struct sockaddr_un, sun_path) + 1 + strlen(name)`。
用 `ss -xlp` 看看：写错长度时名字后面会跟着一长串 `@`（每个 `\0` 显示成一个 `@`）。
