## 提示 1
先手动试试：`./build/dev/bin/sig2_eintr_timeout 1`，什么也不输入。1 秒后发生了什么？
用 `strace -e trace=read,rt_sigaction,rt_sigreturn` 观察：`rt_sigaction` 的 flags 里有没有 `SA_RESTART`？
read 被打断后是不是又被调用了一次（`restart_syscall` / `ERESTARTSYS`）？

## 提示 2
有两处问题：`sa_flags` 不应带 `SA_RESTART`；read 返回 -1 且 `errno == EINTR` 时不能 `continue`，
这正是"超时"的信号——打印 `timeout` 并 `return 3`。

## 提示 3
读到数据后记得 `alarm(0)` 取消闹钟。现代替代方案：`poll(fds, 1, ms)` 的超时参数、`timerfd_create`、
或 socket 上的 `SO_RCVTIMEO`——都不需要依赖"信号打断系统调用"这种全局副作用。
