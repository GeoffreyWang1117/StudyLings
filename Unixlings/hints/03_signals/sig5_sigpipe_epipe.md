## 提示 1
试试 `./build/dev/bin/sig5_sigpipe_epipe | head -n 3; echo "${PIPESTATUS[@]}"`：第一个数字是 141 = 128 + 13，
13 就是 SIGPIPE。进程被杀死时没有机会打印任何东西。

## 提示 2
`struct sigaction sa = {0}; sa.sa_handler = SIG_IGN; sigemptyset(&sa.sa_mask); sigaction(SIGPIPE, &sa, nullptr);`
忽略之后，write 会返回 -1 并设置 `errno = EPIPE`。

## 提示 3
在 write_all 失败的分支里判断 `errno == EPIPE`：`fprintf(stderr, "peer closed\n"); return 0;`。
socket 上还可以不改全局信号处置，而是对每次发送用 `send(fd, buf, n, MSG_NOSIGNAL)`。
