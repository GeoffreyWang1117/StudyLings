# Exercise 2: 解决方案

## GDB 操作
```bash
gdb ./nested
(gdb) break level1
(gdb) run

# 进入 level2
(gdb) step
# 现在在 level2 中

# 不想逐步执行，快速返回
(gdb) finish
Run till exit from #0  level2 (x=6) at nested.c:9
0x0000555555555199 in level1 (x=5) at nested.c:16
16	    return result + 10;
Value returned is $1 = 42

# 查看返回值
(gdb) print $retval  # GDB 特有
$2 = 42
```

## LLDB 操作
```bash
(lldb) b level1
(lldb) run
(lldb) step
(lldb) finish
# 返回值会自动显示

(lldb) frame variable
# 查看当前帧的所有变量
```

## finish vs continue
- `finish`: 执行完当前函数
- `continue`: 执行到下一个断点
- `return`: 立即返回（可指定返回值）

## 技巧
使用 `finish` 可以快速跳出深层函数调用，避免逐步执行。
