## 提示 1
`int pidfd = sl_pidfd_open(pid, 0);` 之后，子进程一退出 pidfd 就变成"可读"。
所以限时等待就是 `poll(&(struct pollfd){.fd = pidfd, .events = POLLIN}, 1, timeout_ms)`：
返回 1 表示子进程结束了，返回 0 表示超时。注意 pidfd 可读**不等于**已回收，之后仍要 `waitpid(pid, ...)`。

## 提示 2
超时后 `sl_pidfd_send_signal(pidfd, SIGTERM)`，再 `wait_readable(pidfd, KILL_AFTER_MS)`；
还没退出就 `sl_pidfd_send_signal(pidfd, SIGKILL)`。最后 `waitpid` 回收、`close(pidfd)`、返回 124。
信号发出时进程恰好已经退出，会得到 `ESRCH` —— 这不是错误。

## 提示 3
poll 被信号打断会返回 -1/EINTR。记下 `deadline = now_ms() + timeout_ms`，
每次重试用 `deadline - now_ms()` 作为新的超时。`pidfd_open` 返回 ENOSYS 时按说明打印并返回 125。
