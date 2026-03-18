# Exercise 1: 分析 Core Dump

学习分析程序崩溃后的 core dump。

## 步骤
```bash
ulimit -c unlimited      # 启用 core dump
./crash                  # 程序会崩溃
gdb ./crash core         # 加载 core dump
(gdb) bt                 # 查看崩溃位置
```
