# Exercise 1: 基本断点操作

## 目标

学习如何使用断点来暂停程序执行并检查程序状态。

## 任务

你有一个计算阶乘的程序。使用断点来：

1. 在 `main` 函数开始处设置断点
2. 在 `factorial` 函数设置断点
3. 运行程序到断点
4. 查看所有断点
5. 继续执行到下一个断点
6. 检查变量值

## 步骤

### 1. 编译并启动调试器

```bash
make
gdb ./factorial
# 或
lldb ./factorial
```

### 2. 设置断点

**GDB:**
```
(gdb) break main          # 在 main 函数设置断点
(gdb) break factorial     # 在 factorial 函数设置断点
(gdb) info breakpoints    # 查看断点列表
```

**LLDB:**
```
(lldb) b main             # 在 main 函数设置断点
(lldb) b factorial        # 在 factorial 函数设置断点
(lldb) br list            # 查看断点列表
```

### 3. 运行程序

```
(gdb) run
# 或
(lldb) run
```

程序会在第一个断点（main）处停止。

### 4. 查看当前位置和变量

**GDB:**
```
(gdb) list              # 查看当前代码
(gdb) info locals       # 查看局部变量
(gdb) continue          # 继续执行到下一个断点
```

**LLDB:**
```
(lldb) l                # 查看当前代码
(lldb) frame variable   # 查看局部变量
(lldb) continue         # 继续执行到下一个断点
```

### 5. 在 factorial 函数中检查

当停在 factorial 函数时，检查参数值：

**GDB:**
```
(gdb) print n           # 打印参数 n 的值
(gdb) backtrace         # 查看调用栈
```

**LLDB:**
```
(lldb) p n              # 打印参数 n 的值
(lldb) bt               # 查看调用栈
```

## 预期行为

- 程序应该首先在 `main` 函数停止
- 使用 `continue` 后，应该在 `factorial` 函数停止
- 你应该能看到传递给 `factorial` 的参数值

## 问题思考

1. 断点 1 和断点 2 分别在哪里？
2. `factorial` 函数被调用了几次？
3. 如何查看函数的参数值？

## 扩展挑战

1. 在 `factorial` 函数的 `return` 语句处设置断点
2. 使用 `delete` 命令删除某个断点
3. 尝试在具体行号设置断点：`break factorial.c:15`
