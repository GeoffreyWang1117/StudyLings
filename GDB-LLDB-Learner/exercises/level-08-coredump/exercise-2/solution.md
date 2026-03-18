# Exercise 2: 解决方案

```bash
# 生成 core dump
ulimit -c unlimited
./segfault
Segmentation fault (core dumped)

# 分析 core dump
gdb ./segfault core

(gdb) bt
#0  0x... in process_user (user=0x0) at segfault.c:10
#1  0x... in main (argc=1, argv=...) at segfault.c:22

(gdb) frame 0
(gdb) print user
$1 = (User *) 0x0    # NULL 指针!

(gdb) frame 1
(gdb) list
# 可以看到因为 argc == 1, u 没有被初始化

(gdb) print u
$2 = (User *) 0x0

(gdb) print argc
$3 = 1
```

## 根本原因
`main` 函数中 `u` 初始化为 `NULL`，只有当提供命令行参数时才会被赋值。

## 修复方法
```c
if (u == NULL) {
    fprintf(stderr, "Error: user is NULL\n");
    return 1;
}
process_user(u);
```

## Core Dump 的价值
- 不需要重现崩溃
- 保存崩溃瞬间的所有状态
- 可以事后分析（生产环境很有用）
