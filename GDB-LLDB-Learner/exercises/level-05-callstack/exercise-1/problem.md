# Exercise 1: 查看调用栈

## 目标
学习使用 backtrace 查看函数调用栈。

## 任务
1. 在 func_c 设置断点
2. 查看完整调用栈
3. 切换到不同栈帧
4. 查看每个栈帧的局部变量

## 命令
```
(gdb) backtrace / bt
(gdb) frame 1
(gdb) info locals
(gdb) up / down
```
