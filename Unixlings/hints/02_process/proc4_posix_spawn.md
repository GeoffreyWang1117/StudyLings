## 提示 1
posix_spawn 用"文件动作表"描述子进程启动前要做的 fd 操作，代替 fork 后手写的 dup2/close：
```c
posix_spawn_file_actions_t fa;
posix_spawn_file_actions_init(&fa);
posix_spawn_file_actions_adddup2(&fa, fds[1], STDOUT_FILENO);
int err = posix_spawnp(&pid, argv[0], &fa, nullptr, argv, environ);
posix_spawn_file_actions_destroy(&fa);
```
`err != 0` 就是失败，`err` 本身就是错误码（ENOENT 等）。

## 提示 2
管道用 `pipe2(fds, O_CLOEXEC)` 创建：子进程 exec 时原始的两个 fd 自动关闭，只留下 dup2 出来的 stdout。
父进程 spawn 之后立刻 `close(fds[1])`，否则读端永远等不到 EOF。

## 提示 3
先读到 EOF，再 `waitpid` —— 顺序反了，子进程写满 64KiB 管道后阻塞，父进程在 waitpid 里等它，死锁。
缓冲区满了也要继续 read（读进一个临时数组丢掉），否则同样会卡住子进程。
