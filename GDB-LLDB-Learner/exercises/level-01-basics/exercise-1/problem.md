# Exercise 1: 第一个调试会话

## 目标

通过这个练习，你将学会：
1. 启动 GDB 或 LLDB 调试器
2. 使用 `list` 命令查看源代码
3. 使用 `run` 命令运行程序
4. 观察程序输出
5. 使用 `quit` 命令退出调试器

## 背景

你有一个简单的 C 程序 `hello.c`，它会打印一些信息。你的任务是使用调试器来运行这个程序并观察它的行为。

## 任务

### 步骤 1: 编译程序

首先，编译程序（带调试信息）：

```bash
make
# 或者手动编译：
# gcc -g hello.c -o hello
```

### 步骤 2: 启动调试器

使用 GDB 或 LLDB 启动调试器：

**使用 GDB:**
```bash
gdb ./hello
```

**使用 LLDB:**
```bash
lldb ./hello
```

### 步骤 3: 查看源代码

在调试器提示符下，使用 `list` 命令（或简写 `l`）查看源代码：

**GDB:**
```
(gdb) list
```

**LLDB:**
```
(lldb) source list
# 或简写
(lldb) l
```

### 步骤 4: 运行程序

使用 `run` 命令（或简写 `r`）运行程序：

**GDB:**
```
(gdb) run
```

**LLDB:**
```
(lldb) run
```

观察程序的输出。

### 步骤 5: 退出调试器

使用 `quit` 命令（或简写 `q`）退出调试器：

**GDB:**
```
(gdb) quit
```

**LLDB:**
```
(lldb) quit
```

## 预期输出

程序应该输出：
```
Hello from the debugger!
Learning GDB and LLDB is fun!
This is line 3 of output.
```

## 问题思考

1. `list` 命令显示了多少行代码？
2. 如果再次按回车键会发生什么？
3. 程序正常结束时，调试器显示了什么信息？

## 扩展挑战

1. 尝试 `list main` 命令，看看会发生什么
2. 尝试 `list 5` 命令，看看会显示什么
3. 使用 `help list` 查看 list 命令的详细帮助
4. 尝试使用命令缩写 `l` 和 `r`

## 提示

- 在 GDB/LLDB 中，按 Tab 键可以自动补全命令
- 大多数命令都有缩写形式
- 按回车键会重复上一个命令（对于 list 特别有用）
- 使用 Ctrl+D 也可以退出调试器

## 验证

运行验证脚本检查你是否正确完成了练习：

```bash
python3 verify.py
```

（注意：这个练习主要是交互式的，验证脚本会检查程序是否正确编译并能够运行）
