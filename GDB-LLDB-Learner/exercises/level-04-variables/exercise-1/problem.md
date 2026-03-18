# Exercise 1: 变量检查和修改

## 任务

这个程序判断学生是否及格（60分及格），但有个 bug。使用调试器：

1. 检查变量值找出问题
2. 在运行时修改变量来测试修复方案
3. 理解如何检查结构体成员

## 调试步骤

### 1. 编译并启动

```bash
make
gdb ./bug
```

### 2. 设置断点

```
(gdb) break check_pass
(gdb) run
```

### 3. 检查变量

当停在 `check_pass` 时：

```
(gdb) print *student           # 打印整个结构体
(gdb) print student->score     # 打印分数
(gdb) print student->passed    # 打印通过状态
```

### 4. 单步执行并观察

```
(gdb) next                     # 执行 if 语句
(gdb) print student->passed    # 检查 passed 的值
```

### 5. 修改变量测试修复

```
(gdb) set var student->passed = 1    # 手动设置为通过
(gdb) continue                        # 继续执行
```

## 问题

1. `student.score` 是多少？
2. 为什么 `passed` 没有被设置为 1？
3. bug 在哪一行？

## 扩展练习

1. 使用 `ptype student` 查看结构体定义
2. 使用 `watch student->passed` 设置监视点
3. 修改 `student->score` 的值测试不同场景
