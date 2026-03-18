# Exercise 2: 断点命令自动化

## 目标
学习使用断点命令实现自动化调试。

## 任务
设置断点命令，在每次触发时自动执行操作而不需要手动输入。

## GDB 示例
```bash
(gdb) break process_item
(gdb) commands
>silent
>printf "Processing item: %d\n", item
>backtrace 2
>continue
>end
(gdb) run
```

这会在每次调用 `process_item` 时自动打印信息并继续执行。

## 练习
1. 设置断点命令记录每次调用的参数
2. 只在特定条件下打印信息
3. 组合使用 `silent` 避免默认断点消息
