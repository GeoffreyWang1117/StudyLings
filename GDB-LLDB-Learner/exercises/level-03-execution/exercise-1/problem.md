# Exercise 1: Step vs Next

## 目标

理解 `step` 和 `next` 命令的区别，掌握程序执行控制。

## 背景

这个程序包含多个函数调用。你需要使用 `step` 和 `next` 命令来观察不同的执行行为。

## 任务

1. 在 `main` 函数设置断点并运行
2. 使用 `step` 命令进入 `add` 函数
3. 使用 `next` 命令跳过 `multiply` 函数
4. 观察两者的区别

## 详细步骤

### 1. 编译并启动

```bash
make
gdb ./calculator
# 或
lldb ./calculator
```

### 2. 设置断点在 main

**GDB:**
```
(gdb) break main
(gdb) run
```

**LLDB:**
```
(lldb) b main
(lldb) run
```

### 3. 使用 next 跳过第一个函数调用

```
(gdb) next      # 跳过 printf
(gdb) list      # 查看当前位置
```

### 4. 使用 step 进入 add 函数

```
(gdb) step      # 进入 add 函数内部
(gdb) list      # 你现在应该在 add 函数内
(gdb) print a   # 查看参数 a
(gdb) print b   # 查看参数 b
```

### 5. 使用 finish 返回到 main

```
(gdb) finish    # 执行完当前函数并返回
```

### 6. 使用 next 跳过 multiply 函数

```
(gdb) next      # 跳过整个 multiply 函数调用
```

### 7. 对比观察

- `step` 会进入函数内部，你可以看到函数的每一行
- `next` 会将整个函数调用作为一步执行
- `finish` 会执行完当前函数并返回

## 预期行为

使用 `step`:
```
main() -> 进入 add() -> 看到 add 内部的代码
```

使用 `next`:
```
main() -> 执行 multiply() -> 停在 multiply() 之后的下一行
```

## 问题思考

1. 什么时候应该使用 `step`？
2. 什么时候应该使用 `next`？
3. 如果你在函数内部想快速返回到调用者，应该用什么命令？

## 回答

1. **使用 step 的场景**:
   - 需要调试函数内部逻辑
   - 怀疑函数内部有 bug
   - 想详细了解函数如何工作

2. **使用 next 的场景**:
   - 函数是标准库函数或已知正确的函数
   - 不关心函数内部细节
   - 想快速执行到下一行

3. **快速返回**: 使用 `finish` 命令

## 扩展挑战

1. 尝试多次使用 `step` 进入嵌套的函数调用
2. 使用 `backtrace` 查看调用栈
3. 尝试 `stepi` 和 `nexti` 命令（单步执行机器指令）
4. 使用 `until` 命令执行到指定行
