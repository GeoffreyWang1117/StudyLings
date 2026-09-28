## 提示 1
运行 `sig3_sigchld_reaper 64`，在另一个终端 `ps -o pid,stat,cmd --ppid <pid>`，数一数有几个 `Z`（defunct）。
64 个子进程退出，处理函数却只运行了一次——因为待决的标准信号只记一个"位"，不计数。

## 提示 2
把 `if (waitpid(...) > 0)` 改成 `while (waitpid(-1, &status, WNOHANG) > 0)`。
`WNOHANG` 很关键：没有已退出的子进程时立刻返回 0，而不是在信号处理函数里阻塞。

## 提示 3
循环最后一次 `waitpid` 返回 -1 并把 errno 设成 `ECHILD`。处理函数开头 `int saved = errno;`，结尾 `errno = saved;`，
否则可能篡改主程序中被打断位置刚设置、还没来得及检查的 errno。
