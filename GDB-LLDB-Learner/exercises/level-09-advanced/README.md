# Level 9: 高级调试技巧

## 学习目标

- 调试优化代码
- 远程调试
- 使用条件表达式和命令
- 编写调试器脚本
- 自定义命令

## 高级技巧

### 1. 调试优化代码

优化代码的挑战：
- 变量可能被优化掉
- 执行顺序可能改变
- 内联函数

技巧：
```bash
# 编译时使用 -Og（调试优化）而不是 -O0 或 -O2
gcc -Og -g program.c

# 在 GDB 中查看汇编
(gdb) disassemble
(gdb) layout asm
```

### 2. 条件断点高级用法

```bash
# 复杂条件
(gdb) break func if (x > 10 && y < 20)

# 断点命令
(gdb) break main
(gdb) commands
>silent
>printf "x = %d\n", x
>continue
>end
```

### 3. 自定义命令

**GDB:**
```bash
# ~/.gdbinit
define print_array
    set $i = 0
    while $i < $arg1
        print $arg0[$i]
        set $i = $i + 1
    end
end
```

**LLDB:**
```bash
# ~/.lldbinit
command script import ~/lldb_scripts.py
```

### 4. Python 脚本

**GDB Python:**
```python
(gdb) python
>import gdb
>print("Hello from Python!")
>end
```

**LLDB Python:**
```python
(lldb) script
>>> import lldb
>>> print("Hello from Python!")
```

### 5. 远程调试

**GDB Server:**
```bash
# 远程机器
gdbserver :1234 ./program

# 本地机器
gdb ./program
(gdb) target remote remote-ip:1234
```

**LLDB Server:**
```bash
# 远程机器
lldb-server platform --listen *:1234

# 本地机器
(lldb) platform select remote-linux
(lldb) platform connect connect://remote-ip:1234
```

## 实用脚本示例

### GDB 美化输出
```bash
# .gdbinit
set print pretty on
set print array on
set print array-indexes on
set pagination off
```

### 断点日志
```bash
break important_function
commands
silent
printf "Called with arg=%d\n", arg
backtrace 3
continue
end
```

## 调试技巧总结

1. **使用 TUI 模式**: `layout src` (GDB) 查看源码窗口
2. **记录执行**: `record` (GDB) 可以反向执行
3. **查找内存泄漏**: 结合 Valgrind 使用
4. **性能分析**: 结合 gprof、perf 使用
5. **自动化**: 编写脚本自动化重复任务
