# Exercise 3: 断点管理

## 目标

学习管理多个断点，包括启用、禁用、删除和临时断点。

## 任务

这个程序有多个函数调用。练习：
1. 设置多个断点
2. 启用和禁用断点
3. 使用临时断点
4. 一次性删除多个断点
5. 查看断点命中次数

## 步骤

### 设置多个断点

**GDB:**
```bash
(gdb) break main
(gdb) break process_data
(gdb) break calculate
(gdb) info breakpoints
```

### 禁用/启用断点

```bash
(gdb) disable 2        # 禁用断点 2
(gdb) enable 2         # 启用断点 2
(gdb) disable 1-3      # 禁用 1 到 3
```

### 临时断点

```bash
(gdb) tbreak calculate # 只触发一次
```

**LLDB:**
```bash
(lldb) breakpoint set -n calculate -o true
```

## 练习目标

完成后你应该能够回答：
- 如何一次禁用所有断点？
- 如何查看断点被命中了多少次？
- 临时断点和普通断点的区别？
