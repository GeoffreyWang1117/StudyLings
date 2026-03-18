# Exercise 2: 解决方案

## GDB 完整示例

```bash
gdb ./breakpoint_commands

# 基本断点命令
(gdb) break process_item
Breakpoint 1 at 0x1149

(gdb) commands 1
Type commands for breakpoint(s) 1, one per line.
End with a line saying just "end".
>silent
>printf "Processing: item=%d\n", item
>continue
>end

(gdb) run
自动化断点命令演示

Processing: item=1
Item 1 -> 2
Processing: item=2
Item 2 -> 4
...
```

## 高级示例：条件输出

```bash
(gdb) break process_item
(gdb) commands
>silent
>if item > 5
>  printf "Large item: %d\n", item
>  backtrace 1
>end
>continue
>end
```

## 断点命令用途

1. **调试日志**：自动记录函数调用
2. **性能分析**：统计函数调用次数
3. **数据收集**：导出变量值到文件
4. **条件检查**：只在特定情况下停止

## Python 脚本增强

```bash
(gdb) python
>class ProcessBreakpoint(gdb.Breakpoint):
>    def stop(self):
>        frame = gdb.selected_frame()
>        item = frame.read_var("item")
>        print(f"Item: {item}")
>        return False  # 不停止
>
>ProcessBreakpoint("process_item")
>end
```

## 保存断点命令

```bash
(gdb) save breakpoints my_breakpoints.gdb
# 文件内容包含断点和命令
```

## 技巧总结
- `silent`: 抑制默认断点消息
- `continue`: 自动继续执行
- 组合使用条件和命令实现强大功能
- 使用 Python 实现更复杂的逻辑
