## 提示 1
`signal(2)` 在不同 UNIX 上语义不同（处理函数是否被重置、系统调用是否自动重启），现代代码一律用 `sigaction(2)`：
`struct sigaction sa = {0}; sa.sa_handler = on_signal; sigemptyset(&sa.sa_mask);` 然后分别对 SIGTERM、SIGINT 调用 `sigaction`。

## 提示 2
处理函数里只写 `g_stop = 1;`。`volatile` 防止编译器把 `while (!g_stop)` 里的读优化掉，
`sig_atomic_t` 保证这次写入不会被信号"撕裂"。不要在处理函数里 `printf`/`exit`——见 `man 7 signal-safety`。

## 提示 3
`sa_flags` 设为 0（不带 SA_RESTART）：这样主循环里的 `nanosleep` 会被信号打断、返回 EINTR，
程序立刻回到 `while` 判断，而不是再睡完剩下的时间。
