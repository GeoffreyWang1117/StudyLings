# Level 3: 程序执行控制

## 学习目标

- 单步执行代码（逐行）
- 单步进入和跳过函数
- 继续执行到函数返回
- 精确控制程序流程

## 核心命令

### GDB 命令
```bash
step / s                # 单步执行（进入函数）
next / n                # 单步执行（跳过函数）
stepi / si              # 单步执行一条机器指令
nexti / ni              # 执行一条机器指令（跳过函数调用）
finish / fin            # 执行到当前函数返回
until 10                # 执行到第 10 行
continue / c            # 继续执行到下一个断点
```

### LLDB 命令
```bash
step / s                # 单步执行（进入函数）
next / n                # 单步执行（跳过函数）
thread step-inst / si   # 单步执行一条机器指令
thread step-inst-over / ni  # 执行一条机器指令（跳过函数调用）
thread step-out / finish    # 执行到当前函数返回
thread until 10         # 执行到第 10 行
continue / c            # 继续执行到下一个断点
```

## Step vs Next 的区别

- **step (s)**: 进入函数内部，逐行执行
- **next (n)**: 将函数调用视为一条语句，不进入内部

示例：
```c
int result = calculate(5);  // 在这一行
```

- 使用 `step`: 会进入 `calculate` 函数内部
- 使用 `next`: 执行整个函数，停在下一行

## 练习列表

### Exercise 1: Step vs Next
**难度**: ⭐⭐ 初级

理解单步进入（step）和单步跳过（next）的区别。

**技能点**:
- 使用 step 进入函数
- 使用 next 跳过函数
- 观察执行流程

### Exercise 2: 函数执行控制
**难度**: ⭐⭐ 初级

学习如何快速执行到函数返回。

**技能点**:
- 使用 finish 返回到调用者
- 使用 until 执行到指定位置
- 组合使用多个命令

### Exercise 3: 调试递归函数
**难度**: ⭐⭐⭐ 中级

使用执行控制命令调试递归函数。

**技能点**:
- 在递归中使用 step/next
- 理解调用栈深度
- 使用 finish 快速返回

## 快速参考

| 功能 | GDB | LLDB | 说明 |
|------|-----|------|------|
| 单步进入 | `step` / `s` | `step` / `s` | 进入函数内部 |
| 单步跳过 | `next` / `n` | `next` / `n` | 跳过函数调用 |
| 执行到返回 | `finish` | `finish` | 执行到函数返回 |
| 继续执行 | `continue` / `c` | `continue` / `c` | 到下一个断点 |
| 执行到行 | `until 10` | `thread until 10` | 执行到第10行 |

## 技巧

1. **快速重复命令**: 按回车键重复上一个命令（对 step/next 特别有用）
2. **查看位置**: 使用 `list` 或 `where` 查看当前位置
3. **查看调用栈**: 使用 `backtrace` 了解你在调用链的哪个位置
4. **避免陷入库函数**: 使用 `next` 而不是 `step` 来跳过标准库函数
