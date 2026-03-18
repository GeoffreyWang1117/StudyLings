# Exercise 2: 使用 finish 命令

## 目标
学习使用 `finish` 命令快速执行完当前函数并返回到调用者。

## 任务
调试一个嵌套函数调用的程序，练习：
1. 使用 `step` 进入函数
2. 使用 `finish` 快速返回
3. 查看函数返回值

## 步骤
```bash
make
gdb ./nested
(gdb) break main
(gdb) run
(gdb) step          # 进入函数
(gdb) finish        # 执行到返回
(gdb) print $retval # 查看返回值 (GDB)
```
