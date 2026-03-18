# Exercise 3: 解决方案

## GDB 完整会话

```bash
gdb ./multi_break

# 1. 设置多个断点
(gdb) break main
(gdb) break process_data
(gdb) break calculate
(gdb) break display_results

# 2. 查看所有断点
(gdb) info breakpoints
Num     Type           Disp Enb Address
1       breakpoint     keep y   0x00001199 in main
2       breakpoint     keep y   0x00001165 in process_data
3       breakpoint     keep y   0x00001149 in calculate
4       breakpoint     keep y   0x0000118d in display_results

# 3. 运行程序
(gdb) run
Breakpoint 1, main () at multi_break.c:22
(gdb) continue

# calculate 会被调用多次，断点会多次触发
Breakpoint 3, calculate (a=1, b=0) at multi_break.c:4
(gdb) continue
Breakpoint 3, calculate (a=2, b=1) at multi_break.c:4

# 4. 禁用频繁触发的断点
(gdb) disable 3
(gdb) continue
# 现在 calculate 不会停止

# 5. 使用临时断点
(gdb) delete              # 删除所有断点
(gdb) break main
(gdb) tbreak calculate    # 临时断点，只触发一次
(gdb) run

# 6. 查看断点命中次数
(gdb) info breakpoints
Num     Type           Disp Enb Address            What
1       breakpoint     keep y   0x00001199 in main
        breakpoint already hit 1 time
```

## LLDB 完整会话

```bash
lldb ./multi_break

# 设置断点
(lldb) b main
(lldb) b process_data
(lldb) b calculate
(lldb) breakpoint list

# 禁用断点
(lldb) breakpoint disable 3
(lldb) run

# 启用断点
(lldb) breakpoint enable 3

# 临时断点
(lldb) breakpoint set -n calculate -o true

# 查看统计信息
(lldb) breakpoint list
Current breakpoints:
1: name = 'main', locations = 1, resolved = 1, hit count = 1
```

## 断点管理命令对照

| 操作 | GDB | LLDB |
|------|-----|------|
| 列出断点 | `info breakpoints` | `breakpoint list` |
| 禁用断点 | `disable N` | `br disable N` |
| 启用断点 | `enable N` | `br enable N` |
| 删除断点 | `delete N` | `br delete N` |
| 删除所有 | `delete` | `br delete` |
| 临时断点 | `tbreak func` | `br set -n func -o true` |
| 禁用所有 | `disable` | `br disable` |
| 启用所有 | `enable` | `br enable` |

## 高级技巧

### 1. 忽略断点 N 次

**GDB:**
```bash
(gdb) ignore 3 10     # 忽略断点 3 前 10 次触发
```

**LLDB:**
```bash
(lldb) breakpoint modify 3 -i 10
```

### 2. 断点命令

**GDB:**
```bash
(gdb) break calculate
(gdb) commands
>silent
>printf "a=%d, b=%d\n", a, b
>continue
>end
```

### 3. 保存和加载断点

**GDB:**
```bash
(gdb) save breakpoints my_breaks.gdb
(gdb) source my_breaks.gdb
```

**LLDB:**
```bash
(lldb) breakpoint write -f breaks.lldb
(lldb) breakpoint read -f breaks.lldb
```

## 常见场景

1. **调试循环**: 使用忽略次数跳到特定迭代
2. **多函数调试**: 设置多个断点，选择性禁用
3. **一次性检查**: 使用临时断点
4. **自动化**: 使用断点命令自动执行操作
