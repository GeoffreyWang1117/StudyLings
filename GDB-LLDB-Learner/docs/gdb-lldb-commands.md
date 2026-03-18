# GDB 和 LLDB 命令完整对照表

## 启动和退出

| 功能 | GDB | LLDB |
|------|-----|------|
| 启动调试器 | `gdb program` | `lldb program` |
| 附加到进程 | `gdb -p <pid>` | `lldb -p <pid>` |
| 加载 core dump | `gdb program core` | `lldb -c core program` |
| 退出 | `quit` / `q` | `quit` / `q` |
| 获取帮助 | `help` | `help` |
| 命令帮助 | `help command` | `help command` |

## 运行程序

| 功能 | GDB | LLDB |
|------|-----|------|
| 运行程序 | `run` / `r` | `run` / `r` |
| 带参数运行 | `run arg1 arg2` | `run arg1 arg2` |
| 设置参数 | `set args arg1 arg2` | `settings set target.run-args arg1 arg2` |
| 显示参数 | `show args` | `settings show target.run-args` |
| 重新运行 | `run` | `run` |

## 断点

| 功能 | GDB | LLDB |
|------|-----|------|
| 在函数设置断点 | `break main` / `b main` | `breakpoint set -n main` / `b main` |
| 在文件:行设置断点 | `break file.c:10` | `breakpoint set -f file.c -l 10` / `b file.c:10` |
| 在地址设置断点 | `break *0x400000` | `breakpoint set -a 0x400000` |
| 条件断点 | `break main if x > 5` | `breakpoint set -n main -c 'x > 5'` |
| 临时断点 | `tbreak main` | `breakpoint set -n main -o true` |
| 列出断点 | `info breakpoints` / `i b` | `breakpoint list` / `br l` |
| 删除断点 | `delete 1` / `d 1` | `breakpoint delete 1` / `br del 1` |
| 删除所有断点 | `delete` | `breakpoint delete` |
| 禁用断点 | `disable 1` | `breakpoint disable 1` |
| 启用断点 | `enable 1` | `breakpoint enable 1` |
| 忽略断点 N 次 | `ignore 1 10` | `breakpoint modify -i 10 1` |

## 观察点（Watchpoints）

| 功能 | GDB | LLDB |
|------|-----|------|
| 设置写观察点 | `watch variable` | `watchpoint set variable variable` / `wa s v variable` |
| 设置读观察点 | `rwatch variable` | `watchpoint set variable -w read variable` |
| 设置读写观察点 | `awatch variable` | `watchpoint set variable -w read_write variable` |
| 列出观察点 | `info watchpoints` | `watchpoint list` |
| 删除观察点 | `delete 1` | `watchpoint delete 1` |

## 执行控制

| 功能 | GDB | LLDB |
|------|-----|------|
| 继续执行 | `continue` / `c` | `continue` / `c` |
| 单步进入 | `step` / `s` | `step` / `s` |
| 单步跳过 | `next` / `n` | `next` / `n` |
| 步进汇编指令 | `stepi` / `si` | `thread step-inst` / `si` |
| 跳过汇编指令 | `nexti` / `ni` | `thread step-inst-over` / `ni` |
| 执行到函数返回 | `finish` / `fin` | `thread step-out` / `finish` |
| 执行到指定行 | `until 10` | `thread until 10` |
| 跳转到指定行 | `jump 10` | `thread jump -l 10` |

## 查看代码

| 功能 | GDB | LLDB |
|------|-----|------|
| 列出源代码 | `list` / `l` | `source list` / `l` |
| 列出函数代码 | `list main` | `source list -n main` |
| 列出文件:行代码 | `list file.c:10` | `source list -f file.c -l 10` |
| 反汇编函数 | `disassemble main` | `disassemble -n main` / `di -n main` |
| 反汇编当前位置 | `disassemble` | `disassemble -p` / `di -p` |

## 变量和内存

| 功能 | GDB | LLDB |
|------|-----|------|
| 打印变量 | `print var` / `p var` | `print var` / `p var` / `expr var` |
| 打印数组 | `print arr[0]@10` | `parray 10 arr` |
| 打印表达式 | `print x + y` | `expr x + y` |
| 查看变量类型 | `ptype var` | `type lookup var` |
| 查看变量信息 | `whatis var` | `frame variable var` / `v var` |
| 显示所有局部变量 | `info locals` | `frame variable` / `fr v` |
| 显示所有参数 | `info args` | `frame variable -a` |
| 修改变量值 | `set var x = 10` | `expr x = 10` |
| 自动显示变量 | `display var` | `target stop-hook add -o "p var"` |
| 查看显示列表 | `info display` | - |
| 删除自动显示 | `undisplay 1` | - |

## 内存检查

| 功能 | GDB | LLDB |
|------|-----|------|
| 检查内存（十六进制） | `x/10x 0x400000` | `memory read -c 10 -fx 0x400000` / `x/10x 0x400000` |
| 检查内存（字符串） | `x/s 0x400000` | `memory read -c 10 -fs 0x400000` / `x/s 0x400000` |
| 检查内存（指令） | `x/10i 0x400000` | `disassemble -s 0x400000` |
| 写入内存 | `set {int}0x400000 = 123` | `memory write 0x400000 123` |
| 查找内存 | `find 0x400000, +1000, 'text'` | `memory find 0x400000 0x400400 'text'` |

格式说明：
- `x/Nfu addr`：N=数量, f=格式(x十六进制/d十进制/u无符号/o八进制/t二进制/a地址/c字符/s字符串/i指令), u=单位(b字节/h半字/w字/g双字)

## 调用栈

| 功能 | GDB | LLDB |
|------|-----|------|
| 查看调用栈 | `backtrace` / `bt` | `thread backtrace` / `bt` |
| 查看所有线程栈 | `thread apply all bt` | `thread backtrace all` / `bt all` |
| 查看栈帧 | `frame` / `f` | `frame select` / `f` |
| 切换栈帧 | `frame 2` / `f 2` | `frame select 2` / `f 2` |
| 上一帧 | `up` | `up` |
| 下一帧 | `down` | `down` |
| 栈帧信息 | `info frame` | `frame info` |

## 线程

| 功能 | GDB | LLDB |
|------|-----|------|
| 列出线程 | `info threads` | `thread list` |
| 切换线程 | `thread 2` | `thread select 2` / `t 2` |
| 对所有线程执行命令 | `thread apply all command` | `thread apply all command` |
| 查看当前线程 | `thread` | `thread info` |

## 信号

| 功能 | GDB | LLDB |
|------|-----|------|
| 查看信号处理 | `info signals` | `process handle` |
| 设置信号处理 | `handle SIGINT stop` | `process handle SIGINT -s true` |
| 发送信号 | `signal SIGINT` | `process signal SIGINT` |

## 寄存器

| 功能 | GDB | LLDB |
|------|-----|------|
| 查看所有寄存器 | `info registers` / `i r` | `register read` / `re r` |
| 查看特定寄存器 | `info registers rax` | `register read rax` / `re r rax` |
| 修改寄存器 | `set $rax = 0` | `register write rax 0` |

## 符号和调试信息

| 功能 | GDB | LLDB |
|------|-----|------|
| 查看函数列表 | `info functions` | `image lookup -r -n .` |
| 查看变量列表 | `info variables` | `target variable` |
| 查看符号信息 | `info symbol 0x400000` | `image lookup -a 0x400000` |
| 加载符号文件 | `symbol-file file` | `target symbols add file` |
| 查看共享库 | `info sharedlibrary` | `image list` |

## 进程信息

| 功能 | GDB | LLDB |
|------|-----|------|
| 查看进程信息 | `info proc` | `process status` |
| 查看内存映射 | `info proc mappings` | `image list` |
| 生成 core dump | `generate-core-file` | `process save-core` |

## 脚本和自动化

| 功能 | GDB | LLDB |
|------|-----|------|
| 执行命令文件 | `source script.gdb` | `command source script.lldb` |
| 定义命令 | `define mycommand` | `command script add -f module.func mycommand` |
| Python 脚本 | `python print("hello")` | `script print("hello")` |
| 命令别名 | `alias shortname = longcommand` | `command alias shortname longcommand` |

## 设置选项

| 功能 | GDB | LLDB |
|------|-----|------|
| 设置选项 | `set option value` | `settings set option value` |
| 查看选项 | `show option` | `settings show option` |
| 列出所有选项 | `show` | `settings list` |
| 设置打印长度 | `set print elements 100` | `settings set target.max-string-summary-length 100` |

## 常用配置

### GDB 配置（~/.gdbinit）

```gdb
# 启用历史记录
set history save on
set history size 10000

# 美化输出
set print pretty on
set print array on
set print array-indexes on

# 显示完整字符串
set print elements 0

# Intel 汇编语法
set disassembly-flavor intel
```

### LLDB 配置（~/.lldbinit）

```lldb
# 设置命令别名
command alias bfl breakpoint set -f %1 -l %2

# 显示更多信息
settings set target.max-string-summary-length 0
settings set target.process.thread.step-avoid-regexp ^std::

# Intel 汇编语法
settings set target.x86-disassembly-flavor intel
```

## 技巧和最佳实践

1. **使用 Tab 补全**：两个调试器都支持命令和符号的自动补全
2. **命令缩写**：大部分命令可以使用首字母缩写，如 `b` 代替 `break`
3. **历史记录**：使用上下箭头键浏览命令历史
4. **回车重复**：按回车键重复上一条命令（适用于 step/next）
5. **使用 TUI 模式**：GDB 的 `layout src` 可以显示源码窗口

## 调试示例工作流

```bash
# GDB 示例
gdb ./program
(gdb) break main
(gdb) run arg1 arg2
(gdb) next
(gdb) print variable
(gdb) continue
(gdb) quit

# LLDB 示例
lldb ./program
(lldb) b main
(lldb) run arg1 arg2
(lldb) n
(lldb) p variable
(lldb) c
(lldb) quit
```

## 参考资源

- GDB 官方文档：https://www.gnu.org/software/gdb/documentation/
- LLDB 官方文档：https://lldb.llvm.org/
- GDB to LLDB 命令映射：https://lldb.llvm.org/use/map.html
