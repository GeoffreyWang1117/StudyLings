# Exercise 2: 带参数运行程序

## 目标

学习如何在调试器中向程序传递命令行参数。

## 背景

很多程序需要命令行参数才能正常运行。在调试这类程序时，你需要知道如何在调试器中传递参数。

## 任务

你有一个计算器程序，它接受两个数字作为参数并进行加法运算。你需要：

1. 使用调试器运行程序并传递参数
2. 在 `main` 函数中检查 `argc` 和 `argv` 的值
3. 观察程序如何处理参数

## 步骤

### 1. 编译程序

```bash
make
```

### 2. 启动调试器

**使用 GDB:**
```bash
gdb ./args_demo
```

**使用 LLDB:**
```bash
lldb ./args_demo
```

### 3. 在 main 设置断点

**GDB:**
```
(gdb) break main
(gdb) run 10 20
```

**LLDB:**
```
(lldb) b main
(lldb) run 10 20
```

程序会在 `main` 函数入口处停止。

### 4. 检查参数

**GDB:**
```
(gdb) print argc
(gdb) print argv[0]
(gdb) print argv[1]
(gdb) print argv[2]
```

**LLDB:**
```
(lldb) p argc
(lldb) p argv[0]
(lldb) p argv[1]
(lldb) p argv[2]
```

### 5. 继续执行

```
(gdb) continue
# 或
(lldb) continue
```

观察程序输出。

### 6. 使用不同参数重新运行

**GDB:**
```
(gdb) run 100 200
```

**LLDB:**
```
(lldb) run 100 200
```

### 7. 设置参数（不运行）

**GDB:**
```
(gdb) set args 50 75
(gdb) show args
(gdb) run
```

**LLDB:**
```
(lldb) settings set target.run-args 50 75
(lldb) settings show target.run-args
(lldb) run
```

## 预期输出

当使用参数 `10 20` 运行时：
```
程序名: ./args_demo
参数 1: 10
参数 2: 20
结果: 10 + 20 = 30
```

## 问题思考

1. `argc` 的值是多少？为什么？
2. `argv[0]` 包含什么？
3. 如果不提供参数会发生什么？
4. 如何在调试会话中改变参数而不退出调试器？

## 扩展挑战

1. 尝试传递不同数量的参数（0个、1个、3个）
2. 传递非数字参数，观察程序行为
3. 使用 `info args` (GDB) 或 `frame variable -a` (LLDB) 查看所有参数
4. 在参数解析的地方设置断点，单步执行观察转换过程

## 验证

运行验证脚本：
```bash
python3 ../../../tools/checker.py args_demo.c args_demo
```
