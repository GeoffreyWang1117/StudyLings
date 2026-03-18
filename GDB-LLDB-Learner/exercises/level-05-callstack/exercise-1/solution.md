# Exercise 1: 解决方案

```bash
gdb ./callstack
(gdb) break func_c
(gdb) run

(gdb) backtrace
#0  func_c (x=22) at callstack.c:4
#1  0x555555555175 in func_b (y=11) at callstack.c:9
#2  0x55555555518d in func_a (z=10) at callstack.c:14
#3  0x55555555519f in main () at callstack.c:19

(gdb) frame 2
#2  0x55555555518d in func_a (z=10) at callstack.c:14
(gdb) info locals
a = 11

(gdb) up
#3  0x55555555519f in main ()
(gdb) down
#2  func_a (z=10)
```

理解栈帧编号：
- #0: 当前函数（最深层）
- #1, #2...: 调用者
- 最大编号: main 函数
