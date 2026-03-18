# 解决方案

```
(gdb) break process
(gdb) run
(gdb) backtrace
#0  process (data=0x0) at error.c:6
#1  caller () at error.c:14
#2  main () at error.c:19

(gdb) frame 1
(gdb) print ptr
$1 = (int *) 0x0
```

通过栈回溯找到 caller() 传递了 NULL。
