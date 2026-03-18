# 解决方案

```
(gdb) run
^C  # 程序挂起，按 Ctrl+C
(gdb) thread apply all bt
Thread 3:
#0  pthread_mutex_lock
Thread 2:
#0  pthread_mutex_lock

(gdb) thread 2
(gdb) backtrace
# 查看每个线程等待的锁
```
