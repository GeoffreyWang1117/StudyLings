# Exercise 2: 解决方案

## 完整操作步骤

### 方法 1: 使用 GDB

```bash
# 1. 编译程序
make

# 2. 启动 GDB
gdb ./args_demo

# 3. 在 GDB 中执行：
(gdb) break main                # 在 main 设置断点
(gdb) run 10 20                 # 运行并传递参数
(gdb) print argc                # 查看参数数量
(gdb) print argv[0]             # 查看程序名
(gdb) print argv[1]             # 查看第一个参数
(gdb) print argv[2]             # 查看第二个参数
(gdb) continue                  # 继续执行

# 4. 使用不同参数重新运行
(gdb) run 100 200               # 重新运行

# 5. 使用 set args 设置参数
(gdb) set args 50 75
(gdb) show args
(gdb) run
```

### 方法 2: 使用 LLDB

```bash
# 1. 编译程序
make

# 2. 启动 LLDB
lldb ./args_demo

# 3. 在 LLDB 中执行：
(lldb) b main                   # 在 main 设置断点
(lldb) run 10 20                # 运行并传递参数
(lldb) p argc                   # 查看参数数量
(lldb) p argv[0]                # 查看程序名
(lldb) p argv[1]                # 查看第一个参数
(lldb) p argv[2]                # 查看第二个参数
(lldb) continue                 # 继续执行

# 4. 使用不同参数重新运行
(lldb) run 100 200              # 重新运行

# 5. 使用 settings 设置参数
(lldb) settings set target.run-args 50 75
(lldb) settings show target.run-args
(lldb) run
```

## 详细说明

### 命令行参数的结构

在 C 程序中：
- `argc`: 参数数量（包括程序名）
- `argv`: 字符串数组，包含所有参数
- `argv[0]`: 总是程序名
- `argv[1]`, `argv[2]`, ...: 实际的命令行参数

### 参数传递方式对比

| 场景 | GDB | LLDB |
|------|-----|------|
| 运行时传递 | `run arg1 arg2` | `run arg1 arg2` |
| 预先设置 | `set args arg1 arg2` | `settings set target.run-args arg1 arg2` |
| 查看参数 | `show args` | `settings show target.run-args` |
| 清除参数 | `set args` | `settings clear target.run-args` |

### 调试会话示例

**GDB 完整会话:**
```
$ gdb ./args_demo
(gdb) break main
Breakpoint 1 at 0x1189: file args_demo.c, line 11.
(gdb) run 10 20
Starting program: /path/to/args_demo 10 20

Breakpoint 1, main (argc=3, argv=0x7fffffffddf8) at args_demo.c:11
11	    printf("程序名: %s\n", argv[0]);
(gdb) print argc
$1 = 3
(gdb) print argv[0]
$2 = 0x7fffffffe1ab "./args_demo"
(gdb) print argv[1]
$3 = 0x7fffffffe1b7 "10"
(gdb) print argv[2]
$4 = 0x7fffffffe1ba "20"
(gdb) continue
Continuing.
程序名: ./args_demo
参数数量: 2
参数 1: 10
参数 2: 20
结果: 10 + 20 = 30
[Inferior 1 (process 12345) exited normally]
```

**LLDB 完整会话:**
```
$ lldb ./args_demo
(lldb) b main
Breakpoint 1: where = args_demo`main + 15 at args_demo.c:11, address = 0x0000000100003f0f
(lldb) run 10 20
Process 12345 launched: '/path/to/args_demo' (x86_64)
Process 12345 stopped
* thread #1, queue = 'com.apple.main-thread', stop reason = breakpoint 1.1
    frame #0: 0x0000000100003f0f args_demo`main(argc=3, argv=0x00007ffeefbff4c8) at args_demo.c:11
   8   	 */
   9
   10  	int main(int argc, char *argv[]) {
-> 11  	    printf("程序名: %s\n", argv[0]);
   12  	    printf("参数数量: %d\n", argc - 1);
   13
   14  	    // 检查参数数量
(lldb) p argc
(int) $0 = 3
(lldb) p argv[0]
(char *) $1 = 0x00007ffeefbff680 "./args_demo"
(lldb) p argv[1]
(char *) $2 = 0x00007ffeefbff68c "10"
(lldb) p argv[2]
(char *) $3 = 0x00007ffeefbff68f "20"
(lldb) continue
Process 12345 resuming
程序名: ./args_demo
参数数量: 2
参数 1: 10
参数 2: 20
结果: 10 + 20 = 30
Process 12345 exited with status = 0 (0x00000000)
```

## 问题答案

**1. `argc` 的值是多少？为什么？**

当运行 `./args_demo 10 20` 时，`argc` 的值是 **3**。

原因：
- `argv[0]` = "./args_demo" (程序名)
- `argv[1]` = "10" (第一个参数)
- `argv[2]` = "20" (第二个参数)
- 总共 3 个参数

**2. `argv[0]` 包含什么？**

`argv[0]` 包含**程序的路径/名称**，在这个例子中是 `"./args_demo"`。

操作系统总是将程序名作为第一个参数传递。

**3. 如果不提供参数会发生什么？**

```bash
$ gdb ./args_demo
(gdb) run
```

程序会检测到 `argc != 3`，打印用法信息并返回：
```
程序名: ./args_demo
参数数量: 0
用法: ./args_demo <num1> <num2>
示例: ./args_demo 10 20
```

**4. 如何在调试会话中改变参数而不退出调试器？**

**GDB:**
```
(gdb) set args 50 75
(gdb) run
```

**LLDB:**
```
(lldb) settings set target.run-args 50 75
(lldb) run
```

每次使用 `run` 命令时，程序都会用新的参数重新启动。

## 扩展挑战答案

**1. 传递不同数量的参数**

```bash
# 0 个参数
(gdb) run
# argc = 1, argv[0] = "./args_demo"

# 1 个参数
(gdb) run 10
# argc = 2, 程序会显示用法信息

# 3 个参数
(gdb) run 10 20 30
# argc = 4, 程序会显示用法信息
```

**2. 传递非数字参数**

```bash
(gdb) run hello world
```

`atoi()` 会将非数字字符串转换为 0，所以结果是：
```
结果: 0 + 0 = 0
```

**3. 查看所有参数**

**GDB:**
```
(gdb) info args
argc = 3
argv = 0x7fffffffddf8
```

**LLDB:**
```
(lldb) frame variable -a
(int) argc = 3
(char **) argv = 0x00007ffeefbff4c8
```

**4. 单步执行参数解析**

```bash
(gdb) break main
(gdb) run 10 20
(gdb) next          # 跳过 printf
(gdb) next          # 跳过 printf
(gdb) next          # 跳过 if 检查
(gdb) next          # 跳过 printf
(gdb) next          # 到达 atoi(argv[1])
(gdb) step          # 进入 atoi (或使用 next 跳过)
```

## 关键概念

1. **argc 和 argv**: C 程序接收命令行参数的标准方式
2. **argv[0]**: 始终是程序名，这是操作系统的约定
3. **字符串到数字**: `atoi()` 函数将字符串转换为整数
4. **调试器参数传递**: 两种方式
   - 直接在 `run` 命令后指定
   - 使用 `set args` 或 `settings set` 预先设置

## 实用技巧

1. **处理带空格的参数**:
   ```bash
   (gdb) run "hello world" test
   # argv[1] = "hello world", argv[2] = "test"
   ```

2. **清空参数**:
   ```bash
   (gdb) set args
   (gdb) show args
   # 输出: Argument list to give program being debugged when it is started is "".
   ```

3. **查看原始命令行**:
   ```bash
   (gdb) show args
   ```

## 下一步

继续学习 [Exercise 3: 探索帮助系统](../exercise-3/problem.md)
