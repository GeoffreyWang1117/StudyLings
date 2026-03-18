# Exercise 3: 分析 Assertion 失败

## 目标
学习分析由 assertion 失败导致的 core dump。

## 任务
1. 运行程序（会因 assertion 失败而崩溃）
2. 分析 core dump
3. 找出 assertion 失败的位置和原因

## 命令
```bash
ulimit -c unlimited
./assert_fail
gdb ./assert_fail core
(gdb) bt
(gdb) frame N  # 找到 divide 函数
```
