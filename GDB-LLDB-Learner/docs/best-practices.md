# 调试最佳实践

本文档总结了使用 GDB 和 LLDB 进行高效调试的最佳实践。

## 编译时的最佳实践

### 1. 始终使用调试符号

```bash
# 正确：包含调试信息
gcc -g program.c -o program

# 更好：包含更多调试信息
gcc -g3 program.c -o program

# 最佳：调试优化级别
gcc -Og -g3 program.c -o program
```

### 2. 启用警告

```bash
# 启用所有警告
gcc -Wall -Wextra -g program.c -o program

# 将警告视为错误
gcc -Wall -Wextra -Werror -g program.c -o program
```

### 3. 禁用优化（调试时）

```bash
# 调试时禁用优化
gcc -O0 -g program.c -o program

# 或使用调试优化级别
gcc -Og -g program.c -o program
```

### 4. 保留调试符号

```bash
# 不要 strip 可执行文件
# 错误：
strip program

# 如果需要发布版本，单独保留调试符号
objcopy --only-keep-debug program program.debug
strip program
objcopy --add-gnu-debuglink=program.debug program
```

## 调试会话的最佳实践

### 1. 使用配置文件

创建 `~/.gdbinit` 或 `~/.lldbinit`：

```bash
# ~/.gdbinit
set history save on
set history filename ~/.gdb_history
set print pretty on
set print array on
set pagination off
```

### 2. 使用命令缩写

```bash
# 常用缩写
b    # break
r    # run
c    # continue
n    # next
s    # step
p    # print
bt   # backtrace
l    # list
```

### 3. 利用命令历史

- 使用上下箭头浏览历史
- `Ctrl-R` 搜索历史（在某些配置下）
- 按回车重复上一个命令（特别适合 step/next）

### 4. 设置有意义的断点

```bash
# 不好：在 main 设置断点然后一步步走
break main
run
next
next
next
...

# 好：直接在问题附近设置断点
break problematic_function
run
```

### 5. 使用条件断点

```bash
# 不好：手动检查每次循环
break loop_body
run
print i
continue
print i
continue
...

# 好：使用条件断点
break loop_body if i == 100
run
```

### 6. 使用监视点（watchpoint）

```bash
# 当变量改变时自动中断
watch important_variable

# 只在特定条件下监视
watch important_variable if important_variable > 100
```

## 高效调试策略

### 1. 二分查找法

当程序很大时，使用二分查找定位问题：

```bash
# 在中间设置断点
break middle_function
run

# 检查状态是否正常
# 如果正常，问题在后半部分
# 如果异常，问题在前半部分

# 重复这个过程
```

### 2. 断点命令

自动化重复任务：

```bash
break function
commands
silent
printf "x=%d, y=%d\n", x, y
continue
end
```

### 3. 使用 printf 调试与断点结合

```bash
# 不好：到处添加 printf 然后重新编译
printf("Debug: x=%d\n", x);  # 添加到代码中

# 好：使用断点命令
break function
commands
silent
printf "x=%d\n", x
continue
end
```

### 4. 分层调试

先调试高层逻辑，再深入细节：

```bash
# 第一步：确认函数调用顺序
break func1
break func2
break func3
run

# 第二步：在问题函数内部调试
delete  # 删除所有断点
break problematic_func
run
step
step
...
```

## 多线程调试

### 1. 锁定调度器

```bash
# GDB: 只运行当前线程
set scheduler-locking on

# 调试完成后恢复
set scheduler-locking off
```

### 2. 线程特定断点

```bash
# 只在线程 2 中断
break function thread 2
```

### 3. 查看所有线程状态

```bash
# GDB
thread apply all bt

# LLDB
thread backtrace all
```

## 调试技巧

### 1. 反向调试（GDB）

```bash
# 启用记录
record

# 反向执行
reverse-step
reverse-next
reverse-continue
```

### 2. TUI 模式（GDB）

```bash
# 启动 TUI
gdb -tui program

# 或在 GDB 中
layout src    # 源码视图
layout asm    # 汇编视图
layout split  # 分屏视图
layout regs   # 寄存器视图
```

### 3. 保存断点

```bash
# GDB: 保存断点到文件
save breakpoints my_breakpoints.gdb

# 加载断点
source my_breakpoints.gdb
```

### 4. 调试宏

```bash
# 使用 -g3 编译以包含宏信息
gcc -g3 program.c -o program

# 展开宏
(gdb) macro expand SOME_MACRO
```

### 5. 查找内存泄漏

结合 Valgrind：

```bash
# 使用 Valgrind 运行
valgrind --leak-check=full ./program

# 在有问题的地方设置断点
gdb ./program
break suspected_leak_location
```

## 避免常见错误

### 1. 不要过度使用 step

```bash
# 不好：进入每个函数
step
step
step

# 好：只在需要时使用 step，其他时候用 next
next
next
step  # 只在这里进入函数
```

### 2. 不要忘记编译优化的影响

```bash
# 优化后的代码可能难以调试
gcc -O2 -g program.c -o program  # 变量可能被优化掉

# 调试时使用 -Og 或 -O0
gcc -Og -g program.c -o program
```

### 3. 使用符号链接时要小心

```bash
# 如果使用符号链接，确保调试器能找到源码
set substitute-path /old/path /new/path  # GDB
settings set target.source-map /old/path /new/path  # LLDB
```

### 4. 注意多线程的竞态条件

```bash
# 不要假设断点会按预期顺序触发
# 使用线程锁定和条件断点
```

## 性能优化

### 1. 限制断点数量

太多断点会降低性能：

```bash
# 不好：设置 100 个断点
break line1
break line2
...
break line100

# 好：使用条件断点或临时断点
tbreak important_spot
```

### 2. 使用硬件断点

对于频繁访问的位置：

```bash
# GDB
hbreak function  # 硬件断点
```

### 3. 禁用分页

对于脚本化调试：

```bash
set pagination off
```

## 调试脚本示例

### GDB 脚本示例

```bash
# debug_script.gdb
file ./program
break main
run

# 自动执行一系列命令
next
next
print variable
backtrace

# 继续调试
continue
```

运行：
```bash
gdb -x debug_script.gdb
```

### Python 脚本示例

```python
# pretty_printer.py
import gdb

class MyStructPrinter:
    def __init__(self, val):
        self.val = val

    def to_string(self):
        return f"MyStruct {{ x={self.val['x']}, y={self.val['y']} }}"

# 在 .gdbinit 中
# python
# import sys
# sys.path.insert(0, '/path/to/scripts')
# import pretty_printer
# end
```

## 总结

1. **准备工作**：使用正确的编译选项
2. **策略**：先整体后局部，使用二分查找
3. **效率**：使用条件断点、命令别名、自动化脚本
4. **工具**：熟悉 TUI、Python 脚本、配置文件
5. **习惯**：保存工作、记录笔记、善用帮助系统

记住：调试是一门艺术，需要实践和经验。坚持练习，你会越来越熟练！
