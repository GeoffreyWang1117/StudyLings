# Level 8: Core Dump 分析

## 学习目标

- 理解什么是 core dump
- 生成 core dump 文件
- 加载和分析 core dump
- 事后调试崩溃程序

## 什么是 Core Dump？

Core dump 是程序崩溃时的内存快照，包含：
- 程序状态
- 寄存器值
- 调用栈
- 内存内容

## 启用 Core Dump

```bash
# Linux 启用 core dump
ulimit -c unlimited

# 查看设置
ulimit -c

# 设置 core 文件位置（可选）
echo "core.%e.%p" > /proc/sys/kernel/core_pattern
```

## 加载 Core Dump

### GDB
```bash
gdb ./program core
# 或
gdb ./program
(gdb) core-file core
```

### LLDB
```bash
lldb -c core ./program
# 或
lldb ./program
(lldb) target create --core core
```

## 分析 Core Dump

```bash
# 查看崩溃位置
(gdb) where / bt

# 查看变量
(gdb) info locals

# 查看寄存器
(gdb) info registers

# 检查内存
(gdb) x/10x $sp
```

## 练习

学习如何分析崩溃的程序并找出根本原因。
