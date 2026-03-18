# Exercise 3: 解决方案

## 调试递归函数

```bash
gdb ./recursion
(gdb) break fibonacci if n == 3
(gdb) run
(gdb) backtrace
#0  fibonacci (n=3) at recursion.c:4
#1  fibonacci (n=4) at recursion.c:5
#2  fibonacci (n=5) at recursion.c:5
#3  main () at recursion.c:11

(gdb) frame 1
(gdb) print n
$1 = 4

(gdb) finish  # 返回到上一层
```

## 技巧
- 递归深度可能很大，使用条件断点
- 使用 `bt` 理解调用关系
- 使用 `finish` 快速返回上层
