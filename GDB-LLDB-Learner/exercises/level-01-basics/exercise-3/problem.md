# Exercise 3: 探索帮助系统

## 目标

学习如何使用调试器的内置帮助系统来查找和学习命令。

## 背景

GDB 和 LLDB 都有强大的内置帮助系统。掌握如何使用帮助系统可以让你在调试时快速找到需要的命令和选项，而不需要频繁查阅外部文档。

## 任务

通过探索帮助系统来回答一系列问题，并学会自己查找命令用法。

## 步骤

### 1. 编译程序

```bash
make
```

这个程序很简单，主要用于练习帮助系统。

### 2. 启动调试器

**使用 GDB:**
```bash
gdb ./help_demo
```

**使用 LLDB:**
```bash
lldb ./help_demo
```

### 3. 探索主帮助

**GDB:**
```
(gdb) help
```

这会显示所有命令类别。

**LLDB:**
```
(lldb) help
```

### 4. 查看特定类别的帮助

**GDB:**
```
(gdb) help breakpoints
(gdb) help running
(gdb) help data
```

**LLDB:**
```
(lldb) help breakpoint
(lldb) help process
(lldb) help frame
```

### 5. 查看特定命令的帮助

**GDB:**
```
(gdb) help break
(gdb) help print
(gdb) help backtrace
```

**LLDB:**
```
(lldb) help breakpoint set
(lldb) help print
(lldb) help thread backtrace
```

### 6. 使用 apropos 搜索命令

**GDB:**
```
(gdb) apropos breakpoint
(gdb) apropos variable
(gdb) apropos thread
```

**LLDB:**
```
(lldb) apropos breakpoint
(lldb) apropos variable
```

### 7. 查看命令别名

**GDB:**
```
(gdb) help aliases
(gdb) show commands
```

**LLDB:**
```
(lldb) help
# 在输出中查找 "Command aliases:"
```

## 问题任务

使用帮助系统回答以下问题（不要查看解决方案！）：

### GDB 问题：

1. `break` 命令有哪些缩写形式？
2. 如何设置一个临时断点？（提示：使用 `apropos temporary`）
3. `print` 命令的 `/x` 选项是什么意思？
4. 如何查看所有线程的信息？（提示：使用 `help info`）
5. `step` 和 `next` 的区别是什么？

### LLDB 问题：

1. `breakpoint set` 命令的 `-n` 选项是什么意思？
2. 如何列出所有断点？
3. `frame variable` 和 `print` 有什么区别？
4. 如何查看当前线程的调用栈？
5. `thread step-over` 的别名是什么？

## 实践练习

1. 在 `main` 函数设置断点（查找正确的命令）
2. 运行程序到断点
3. 打印 `message` 变量
4. 查看源代码列表
5. 继续执行程序

所有操作都通过帮助系统查找命令！

## 验证

运行程序并使用你学到的命令：

```bash
# 编译
make

# 使用 GDB
gdb ./help_demo

# 或使用 LLDB
lldb ./help_demo
```

## 提示

- 使用 Tab 键自动补全命令
- `help` 命令本身也有帮助：`help help`
- 如果不确定命令类别，使用 `apropos` 搜索关键词
- 大多数命令都有简写形式
- 在帮助文本中，`<>` 表示必需参数，`[]` 表示可选参数

## 扩展挑战

1. 找出如何查看所有可用的寄存器
2. 找出如何反汇编一个函数
3. 找出如何加载 Python 脚本到调试器
4. 找出如何保存断点到文件
5. 找出如何设置条件断点

记住：不要直接看解决方案，使用帮助系统自己探索！
