## 提示 1
`wait`/`waitpid` 每次只回收**一个**子进程。要回收 N 个，就要循环 N 次：
`for (int reaped = 0; reaped < n;) { pid_t pid = waitpid(-1, &status, 0); ... reaped++; }`
`waitpid(-1, ...)` 表示"任意一个子进程"。

## 提示 2
`status` 是打包过的：正常退出时 `WIFEXITED(status)` 为真，退出码是 `WEXITSTATUS(status)`；
被信号杀死时 `WIFSIGNALED(status)` 为真，信号是 `WTERMSIG(status)`（shell 把它记成 128+信号）。
`_exit(2)` 的原始 status 在 Linux 上是 `2 << 8 == 512`。

## 提示 3
`waitpid` 返回 -1 且 `errno == EINTR` 时（被信号打断）应重试，不要当成错误。
可以在程序阻塞时另开终端 `ps -o pid,stat,cmd --ppid <pid>` 看看有没有 `Z` 状态的僵尸。
