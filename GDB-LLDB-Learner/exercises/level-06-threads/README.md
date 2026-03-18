# Level 6: 多线程调试

## 学习目标

- 查看和切换线程
- 为特定线程设置断点
- 调试竞态条件
- 理解线程同步问题

## 核心命令

### GDB 命令
```bash
info threads            # 列出所有线程
thread 2                # 切换到线程 2
thread apply all bt     # 所有线程的调用栈
break file.c:10 thread 2  # 线程特定断点
set scheduler-locking on  # 锁定调度器（只运行当前线程）
```

### LLDB 命令
```bash
thread list             # 列出所有线程
thread select 2         # 切换到线程 2（简写：t 2）
thread backtrace all    # 所有线程的调用栈（简写：bt all）
breakpoint set -n func -T 2  # 线程特定断点
```

## 练习列表

### Exercise 1: 基本线程调试
学习查看、切换线程和检查线程状态。

### Exercise 2: 竞态条件
调试常见的多线程竞态条件问题。

### Exercise 3: 死锁检测
识别和调试死锁问题。
