# Exercise 1: 解决方案

## 完整操作步骤

### 方法 1: 使用 GDB

```bash
# 1. 编译程序
make

# 2. 启动 GDB
gdb ./hello

# 3. 在 GDB 提示符下执行以下命令：
(gdb) list              # 查看源代码
(gdb) run               # 运行程序
(gdb) quit              # 退出
```

### 方法 2: 使用 LLDB

```bash
# 1. 编译程序
make

# 2. 启动 LLDB
lldb ./hello

# 3. 在 LLDB 提示符下执行以下命令：
(lldb) source list      # 查看源代码（或简写 l）
(lldb) run              # 运行程序（或简写 r）
(lldb) quit             # 退出（或简写 q）
```

## 详细说明

### 查看源代码

当你使用 `list` 命令时，调试器会显示源代码。默认情况下：
- 显示大约 10 行代码
- 以当前位置（通常是 main 函数）为中心
- 左边显示行号

**GDB 输出示例：**
```
1	#include <stdio.h>
2
3	/*
4	 * 这是你的第一个调试程序！
5	 * 编译时使用 -g 选项以包含调试信息：
6	 * gcc -g hello.c -o hello
7	 */
8
9	int main() {
10	    printf("Hello from the debugger!\n");
```

### 运行程序

当你使用 `run` 命令时：
1. 程序从头开始执行
2. 你会看到程序的标准输出
3. 程序正常结束后，调试器会显示退出状态

**GDB 输出示例：**
```
(gdb) run
Starting program: /path/to/hello
Hello from the debugger!
Learning GDB and LLDB is fun!
This is line 3 of output.
[Inferior 1 (process 12345) exited normally]
```

**LLDB 输出示例：**
```
(lldb) run
Process 12345 launched: '/path/to/hello' (x86_64)
Hello from the debugger!
Learning GDB and LLDB is fun!
This is line 3 of output.
Process 12345 exited with status = 0 (0x00000000)
```

## 问题答案

**1. `list` 命令显示了多少行代码？**

默认显示 10 行代码。你可以使用 `show listsize` (GDB) 或 `settings show stop-line-count-after` (LLDB) 查看和修改这个设置。

**2. 如果再次按回车键会发生什么？**

按回车键会重复上一个命令。对于 `list` 命令，它会继续显示后续的代码行。这是快速浏览整个文件的便捷方式。

**3. 程序正常结束时，调试器显示了什么信息？**

- **GDB**: 显示 `[Inferior 1 (process PID) exited normally]`
- **LLDB**: 显示 `Process PID exited with status = 0 (0x00000000)`

这表示程序以状态码 0（成功）退出。

## 扩展挑战答案

**1. `list main` 命令**

这会显示 main 函数的代码。调试器会定位到 main 函数的定义并显示周围的代码。

```
(gdb) list main
```

**2. `list 5` 命令**

这会显示第 5 行附近的代码（通常是第 5 行前后各 5 行）。

```
(gdb) list 5
```

**3. `help list` 命令**

**GDB:**
```
(gdb) help list
List specified function or line.
With no argument, lists ten more lines after or around previous listing.
"list -" lists the ten lines before a previous ten-line listing.
One argument specifies a line, and ten lines are listed around that line.
Two arguments with comma between specify starting and ending lines to list.
...
```

**LLDB:**
```
(lldb) help source list
List relevant source code using one of several shorthand formats.
...
```

## 关键概念

1. **调试信息**: `-g` 编译选项是必需的，它告诉编译器在可执行文件中包含调试符号
2. **交互式环境**: 调试器提供了一个交互式的 shell，你可以在其中执行各种命令
3. **命令缩写**: 几乎所有常用命令都有简短形式（如 `l`, `r`, `q`）
4. **命令重复**: 按回车键重复上一个命令，提高效率

## 下一步

继续学习 [Exercise 2: 带参数运行程序](../exercise-2/problem.md)

## 常见错误

1. **忘记使用 -g 编译**: 如果没有调试信息，`list` 命令会显示 "No symbol table is loaded"

   **解决方法**: 重新编译：`gcc -g hello.c -o hello`

2. **输入错误的程序名**: 确保使用正确的路径和文件名

   **解决方法**: 使用 `ls` 确认文件存在，使用 `./hello` 而不是 `hello`

3. **混淆 GDB 和 LLDB 命令**: 虽然很多命令相同，但有些语法不同

   **解决方法**: 参考 [命令对照表](../../../docs/gdb-lldb-commands.md)
