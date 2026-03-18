# Exercise 2: 使用监视点(Watchpoints)

## 目标
学习使用 watchpoints 监控变量何时被修改。

## 任务
设置监视点，找出变量在何处被修改。

## 命令
**GDB:**
```
(gdb) watch local_var
(gdb) watch global_var
(gdb) info watchpoints
```

**LLDB:**
```
(lldb) watchpoint set variable local_var
(lldb) watchpoint list
```
