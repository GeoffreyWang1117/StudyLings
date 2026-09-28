## 提示 1
fork 之后子进程里只有一个线程（调用 fork 的那个），但内存是整份复制的。
fork 那一刻 g_log_lock 被 flusher 线程持有 → 子进程里这把锁也是"已上锁"，而 flusher 在子进程中不存在。
子进程调用 `log_msg` → `pthread_mutex_lock` → 永远等待。父进程则卡在 waitpid。

## 提示 2（修法 A：最简单、最推荐）
多线程程序 fork 后、exec 前，子进程只能调用异步信号安全的函数（`man 7 signal-safety`）：
`write`、`dup2`、`close`、`execve`/`execvp`、`_exit` ……。`printf`、`malloc`、以及任何会加锁的库函数都不行。
把子进程里的 `log_msg` 去掉（真要输出就直接 `write(STDERR_FILENO, ...)`），直接 `execlp`。
更现代的做法：`posix_spawn` 把 fork+exec 合成一步，根本不给你在中间犯错的机会。

## 提示 3（修法 B：pthread_atfork）
```c
static void before_fork(void) { pthread_mutex_lock(&g_log_lock); }
static void after_fork(void)  { pthread_mutex_unlock(&g_log_lock); }
pthread_atfork(before_fork, after_fork, after_fork);   // prepare, parent, child
```
prepare 在 fork 之前执行：它会等 flusher 释放锁后自己拿到锁，于是 fork 时锁的持有者是"调用 fork 的线程"，
子进程里这个线程还在，可以正常解锁。glibc 就是用这种方式保证 fork 后 malloc 还能用。
注意 atfork 只能保护你知道的锁，第三方库内部的锁它管不到 —— 所以修法 A 才是首选。
