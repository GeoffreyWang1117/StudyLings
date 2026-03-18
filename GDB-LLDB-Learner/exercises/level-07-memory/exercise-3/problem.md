# Exercise 3: 调试缓冲区溢出

## 目标
学习使用调试器检测和调试缓冲区溢出问题。

## 任务
1. 运行程序观察行为
2. 使用 `x` 命令检查 buffer 内存
3. 观察溢出覆盖了什么
4. 找出安全的字符串长度

## 命令
```bash
(gdb) break main
(gdb) run
(gdb) next
(gdb) x/20xb buffer
(gdb) x/20c buffer
```
