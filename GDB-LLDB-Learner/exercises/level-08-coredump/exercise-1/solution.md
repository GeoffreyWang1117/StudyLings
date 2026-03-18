# 解决方案

```bash
ulimit -c unlimited
./crash
Segmentation fault (core dumped)

gdb ./crash core
(gdb) bt
#0  0x... in buggy_function (ptr=0x0) at crash.c:5
#1  0x... in main () at crash.c:10

(gdb) frame 0
(gdb) print ptr
$1 = (int *) 0x0

(gdb) frame 1
(gdb) print bad_ptr
$2 = (int *) 0x0
```

通过 core dump 可以看到崩溃时的完整状态。
