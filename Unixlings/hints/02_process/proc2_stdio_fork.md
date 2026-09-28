## 提示 1
先亲眼看看现象：`./proc2_stdio_fork 3` 和 `./proc2_stdio_fork 3 | cat` 的输出有什么不同？
stdout 连终端时是**行缓冲**，连管道/文件时是**全缓冲**（APUE §5.4）。

## 提示 2
`printf` 只是把字节放进进程内存里的缓冲区，真正 `write(2)` 要等缓冲区满、`fflush` 或进程 `exit`。
fork 会复制整个用户态内存 —— 包括这块缓冲区。所以在 fork **之前** `fflush(stdout)`。

## 提示 3
子进程里：自己 printf 的内容先 `fflush(stdout)`，然后 `_exit(0)`。
`exit()` 会 flush 所有 FILE* 并运行 atexit 处理函数，而它们都是从父进程"复制"来的状态，
不该由子进程再执行一遍（proc6 会更深入地讨论这一点）。
