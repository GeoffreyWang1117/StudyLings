# Exercise 1: 多级指针深度解析

## 目标
深入理解一级、二级、三级指针在内存中的实际布局和调试方法。

## 调试任务

### 1. 查看指针链的完整内存布局

```bash
gdb ./multilevel
(gdb) break demonstrate_pointers
(gdb) run
(gdb) next  # 执行到所有指针初始化后

# 打印各级指针
(gdb) print &value
(gdb) print value
(gdb) print &p1
(gdb) print p1
(gdb) print *p1
(gdb) print &p2
(gdb) print p2
(gdb) print *p2
(gdb) print **p2
(gdb) print &p3
(gdb) print p3
(gdb) print *p3
(gdb) print **p3
(gdb) print ***p3

# 查看连续内存
(gdb) x/gx &value  # value 的内存
(gdb) x/gx &p1     # p1 的内存（存储 &value）
(gdb) x/gx &p2     # p2 的内存（存储 &p1）
(gdb) x/gx &p3     # p3 的内存（存储 &p2）
```

### 2. 追踪修改操作

在每次修改 value 的语句设置断点，观察内存变化。

### 3. 画出内存布局图

记录所有地址，画出完整的指针链图。
