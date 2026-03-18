# Exercise 2: 条件断点

## 目标

学习使用条件断点只在特定条件满足时停止程序，这对于调试循环和复杂逻辑非常有用。

## 背景

普通断点会在每次执行到该位置时停止，但有时我们只想在特定条件下停止（比如循环的第100次迭代）。条件断点可以大大提高调试效率。

## 任务

这个程序在数组中查找质数。使用条件断点来：
1. 只在找到质数时停止
2. 只在特定迭代次数时停止
3. 只在特定变量值时停止

## 步骤

### 基本条件断点

**GDB:**
```bash
gdb ./prime_finder
(gdb) break check_prime if num == 17
(gdb) run
```

**LLDB:**
```bash
lldb ./prime_finder
(lldb) breakpoint set -n check_prime -c 'num == 17'
(lldb) run
```

### 复杂条件

```bash
# 多个条件
(gdb) break find_primes if i > 10 && i < 20

# 字符串比较（需要使用函数）
(gdb) break process_data if strcmp(name, "target") == 0
```

## 练习任务

1. 在 `check_prime` 设置条件断点，只在 `num > 10` 时停止
2. 在循环中设置断点，只在 `i == 15` 时停止
3. 修改条件断点的条件
4. 查看所有断点及其条件

## 预期行为

程序会找出 1-30 之间的所有质数，但只在满足条件时停止。
