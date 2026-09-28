## 提示 1
把程序接到管道上跑一次：`./proc6_exit_vs__exit /tmp/x.pid | cat`。数数 "cleanup" 和 "starting" 各出现几次，
再想想：子进程是谁的复制品？它继承了哪些"只属于父进程"的东西？

## 提示 2
`exit()` = 运行 atexit 处理函数 + flush/关闭所有 FILE* + `_exit()`。
fork 出来的子进程继承了父进程的 atexit 列表和 stdio 缓冲区，所以子进程应该用 `_exit()` 结束。

## 提示 3
两处修改：fork 之前 `fflush(stdout)`（否则 "starting" 在两个进程的缓冲区里各有一份）；
子进程里 `child_work()` 之后先 `fflush(stdout)`（否则 `_exit` 会丢掉 "child working"），再 `_exit(0)`。
