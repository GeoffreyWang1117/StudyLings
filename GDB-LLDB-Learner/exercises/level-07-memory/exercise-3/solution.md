# Exercise 3: 解决方案

```bash
gdb ./buffer
(gdb) break main
(gdb) run
(gdb) next  # 执行第一个 strcpy

(gdb) x/10c buffer
0x7fffffffddf0: 72 'H'  101 'e' 108 'l' 108 'l' 111 'o' 0 '\000' ...

(gdb) next  # 执行第二个 strcpy (溢出)

(gdb) x/30xb buffer
# 可以看到数据超出了 buffer 边界

(gdb) print sizeof(buffer)
$1 = 10
```

## 教训
- 总是检查缓冲区大小
- 使用 `strncpy` 而不是 `strcpy`
- 使用调试器检查内存布局
- 编译时启用 `-fstack-protector` 检测溢出

## 正确做法
```c
strncpy(buffer, source, sizeof(buffer) - 1);
buffer[sizeof(buffer) - 1] = '\0';
```
