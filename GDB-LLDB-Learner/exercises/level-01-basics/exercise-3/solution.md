# Exercise 3: 解决方案

## 问题答案

### GDB 问题答案

**1. `break` 命令有哪些缩写形式？**

```
(gdb) help break
Set breakpoint at specified location.
break [PROBE_MODIFIER] [LOCATION] [thread THREADNUM] [if CONDITION]
...
Convenience variable "$bpnum" contains the number of the last breakpoint set.

Aliases: b, br
```

**答案**: `b` 和 `br`

**2. 如何设置一个临时断点？**

```
(gdb) apropos temporary
tbreak -- Set a temporary breakpoint
...

(gdb) help tbreak
Set a temporary breakpoint.
Like "break" except the breakpoint is only enabled once;
it is disabled after the first time it is hit.
```

**答案**: 使用 `tbreak` 命令

**3. `print` 命令的 `/x` 选项是什么意思？**

```
(gdb) help print
Print value of expression EXP.
...
By default the value is printed in a format appropriate to its data type;
you can choose a different format by specifying /FMT, where FMT is a letter
specifying the format; see "Output Formats" in the manual.
...

Available formats:
x - print in hexadecimal
d - print in decimal
...
```

**答案**: `/x` 表示以十六进制格式打印

**4. 如何查看所有线程的信息？**

```
(gdb) help info
Generic command for showing things about the program being debugged.

(gdb) help info threads
Display currently known threads.
Usage: info threads [OPTION]... [ID]...
```

**答案**: `info threads`

**5. `step` 和 `next` 的区别是什么？**

```
(gdb) help step
Step program until it reaches a different source line, stepping into functions.

(gdb) help next
Step program, proceeding through subroutine calls.
Unlike "step", if the current source line calls a subroutine,
this command does not enter the subroutine, but instead steps over
the call, in effect treating it as a single source line.
```

**答案**:
- `step`: 进入函数内部
- `next`: 跳过函数调用，将其视为一行

---

### LLDB 问题答案

**1. `breakpoint set` 命令的 `-n` 选项是什么意思？**

```
(lldb) help breakpoint set
Sets a breakpoint or set of breakpoints in the executable.

...
-n <function-name> ( --name <function-name> )
    Set the breakpoint by function name.  Can be repeated multiple times to make
    one breakpoint for multiple names.
```

**答案**: `-n` 指定按函数名设置断点

**2. 如何列出所有断点？**

```
(lldb) help breakpoint list
List some or all breakpoints at configurable levels of detail.

Syntax: breakpoint list [<breakpt-id>]

Aliases: br l
```

**答案**: `breakpoint list` 或简写 `br l`

**3. `frame variable` 和 `print` 有什么区别？**

```
(lldb) help frame variable
Show variables for the current stack frame. Defaults to all arguments and local
variables in scope.
...
This command does not use the expression evaluator; it uses the variable information
from the debug information.

(lldb) help print
Evaluate an expression on the current thread.  Displays any returned value with
LLDB's default formatting.
Expects 'raw' input (see 'help raw-input'.)

Syntax: print <expr>

Aliases: call, p
```

**答案**:
- `frame variable`: 直接从调试信息读取变量，速度快但功能有限
- `print`: 使用表达式求值器，可以计算复杂表达式

**4. 如何查看当前线程的调用栈？**

```
(lldb) help thread backtrace
Show thread call stacks.  Defaults to the current thread, thread indexes can be
specified as arguments.
...

Syntax: thread backtrace [<thread-index>]

Aliases: bt
```

**答案**: `thread backtrace` 或简写 `bt`

**5. `thread step-over` 的别名是什么？**

```
(lldb) help thread step-over
Source level single step, stepping over calls.  Defaults to current thread unless
specified.

Syntax: thread step-over

Aliases: next, n
```

**答案**: `next` 或 `n`

---

## 实践练习解答

### GDB 会话：

```bash
$ gdb ./help_demo
(gdb) help break                    # 1. 查找断点命令
(gdb) break main                    # 在 main 设置断点
Breakpoint 1 at 0x1189: file help_demo.c, line 14.

(gdb) help run                      # 2. 查找运行命令
(gdb) run                           # 运行到断点
Starting program: /path/to/help_demo

Breakpoint 1, main () at help_demo.c:14
14	    const char *message = "学习使用调试器帮助系统！";

(gdb) help print                    # 3. 查找打印命令
(gdb) print message                 # 打印变量
$1 = 0x555555556004 "学习使用调试器帮助系统！"

(gdb) help list                     # 4. 查找列表命令
(gdb) list                          # 查看源代码
9	void print_message(const char *msg) {
10	    printf("消息: %s\n", msg);
11	}
12
13	int main() {
14	    const char *message = "学习使用调试器帮助系统！";
15	    int counter = 0;
16
17	    printf("帮助系统演示程序\n");
18	    printf("=================\n\n");

(gdb) help continue                 # 5. 查找继续命令
(gdb) continue                      # 继续执行
Continuing.
帮助系统演示程序
=================

消息: 学习使用调试器帮助系统！
消息: 学习使用调试器帮助系统！
消息: 学习使用调试器帮助系统！

循环执行了 3 次
[Inferior 1 (process 12345) exited normally]
```

### LLDB 会话：

```bash
$ lldb ./help_demo
(lldb) help breakpoint              # 1. 查找断点命令
(lldb) b main                       # 在 main 设置断点
Breakpoint 1: where = help_demo`main + 15 at help_demo.c:14

(lldb) help process                 # 2. 查找进程命令
(lldb) run                          # 运行到断点
Process 12345 launched: '/path/to/help_demo' (x86_64)
Process 12345 stopped
* thread #1, queue = 'com.apple.main-thread', stop reason = breakpoint 1.1
    frame #0: 0x0000000100003f0f help_demo`main at help_demo.c:14

(lldb) help print                   # 3. 查找打印命令
(lldb) p message                    # 打印变量
(const char *) $0 = 0x0000000100003f98 "学习使用调试器帮助系统！"

(lldb) help source                  # 4. 查找源代码命令
(lldb) source list                  # 查看源代码
   9   	void print_message(const char *msg) {
   10  	    printf("消息: %s\n", msg);
   11  	}
   12
   13  	int main() {
   14  	    const char *message = "学习使用调试器帮助系统！";
   15  	    int counter = 0;
   16
   17  	    printf("帮助系统演示程序\n");
   18  	    printf("=================\n\n");

(lldb) help continue                # 5. 查找继续命令
(lldb) continue                     # 继续执行
Process 12345 resuming
帮助系统演示程序
=================

消息: 学习使用调试器帮助系统！
消息: 学习使用调试器帮助系统！
消息: 学习使用调试器帮助系统！

循环执行了 3 次
Process 12345 exited with status = 0 (0x00000000)
```

---

## 扩展挑战答案

### 1. 查看所有可用的寄存器

**GDB:**
```
(gdb) help info registers
List of integer registers and their contents, for selected stack frame.
```
使用: `info registers`

**LLDB:**
```
(lldb) help register read
Dump the contents of one or more register values from the current frame.
```
使用: `register read`

### 2. 反汇编一个函数

**GDB:**
```
(gdb) help disassemble
Disassemble a specified section of memory.
```
使用: `disassemble main`

**LLDB:**
```
(lldb) help disassemble
Disassemble specified instructions in the current target.
```
使用: `disassemble -n main`

### 3. 加载 Python 脚本

**GDB:**
```
(gdb) help source
Read commands from a file named FILE.
```
对于 Python：
```
(gdb) help python
Evaluate a Python command.

(gdb) python
>import sys
>print(sys.version)
>end
```

**LLDB:**
```
(lldb) help command script import
Import a scripting module in LLDB.
```
使用: `command script import /path/to/script.py`

### 4. 保存断点到文件

**GDB:**
```
(gdb) help save breakpoints
Save current breakpoint definitions as a script.

Usage: save breakpoints [FILENAME]
```
使用: `save breakpoints my_breakpoints.gdb`

**LLDB:**
```
(lldb) apropos save
breakpoint write -- Export the breakpoints listed to a file that can be read in.
```
使用: `breakpoint write -f breakpoints.lldb`

### 5. 设置条件断点

**GDB:**
```
(gdb) help break
...
break [LOCATION] [thread THREADNUM] [if CONDITION]
```
使用: `break main if x > 10`

**LLDB:**
```
(lldb) help breakpoint set
...
-c <expr> ( --condition <expr> )
    The breakpoint stops only if this condition expression evaluates to true.
```
使用: `breakpoint set -n main -c 'x > 10'`

---

## 关键技巧总结

### 使用帮助系统的最佳实践

1. **从顶层开始**: 使用 `help` 查看所有类别
2. **类别浏览**: 查看感兴趣类别的所有命令
3. **命令详情**: 查看特定命令的详细帮助
4. **搜索功能**: 使用 `apropos` 搜索关键词
5. **Tab 补全**: 不确定命令名时使用 Tab

### 帮助命令对照表

| 功能 | GDB | LLDB |
|------|-----|------|
| 主帮助 | `help` | `help` |
| 类别帮助 | `help <category>` | `help <category>` |
| 命令帮助 | `help <command>` | `help <command>` |
| 搜索命令 | `apropos <keyword>` | `apropos <keyword>` |
| 查看选项 | `show <option>` | `settings show <option>` |

### 常用帮助命令

**GDB:**
```bash
help                    # 显示所有类别
help breakpoints        # 断点相关命令
help running           # 程序执行命令
help data              # 数据检查命令
help stack             # 调用栈命令
apropos <keyword>      # 搜索包含关键词的命令
show commands          # 查看命令历史
```

**LLDB:**
```bash
help                    # 显示所有命令和类别
help breakpoint        # 断点相关命令
help process           # 进程控制命令
help frame             # 栈帧相关命令
help thread            # 线程相关命令
apropos <keyword>      # 搜索命令
```

## 学习要点

1. **帮助系统很强大**: 几乎所有问题都可以通过帮助系统找到答案
2. **层次化结构**: 从类别到命令，逐步深入
3. **搜索功能**: `apropos` 是你的好朋友
4. **实践学习**: 边用边学，不要只看文档
5. **建立习惯**: 遇到不确定的命令，先用 `help` 查看

## 下一步

恭喜完成 Level 1 的所有练习！你已经掌握了调试器的基础知识。

继续学习 [Level 2: 断点管理](../../level-02-breakpoints/README.md)
