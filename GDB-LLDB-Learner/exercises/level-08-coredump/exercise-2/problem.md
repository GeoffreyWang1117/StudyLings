# Exercise 2: 段错误分析

## 目标
学习通过 core dump 分析段错误(Segmentation Fault)。

## 步骤
1. 启用 core dump: `ulimit -c unlimited`
2. 运行程序不带参数（会崩溃）: `./segfault`
3. 加载 core dump: `gdb ./segfault core`
4. 分析崩溃原因

## 分析任务
- 在哪个函数崩溃的？
- 什么值导致了崩溃？
- 从哪里传递的这个值？
