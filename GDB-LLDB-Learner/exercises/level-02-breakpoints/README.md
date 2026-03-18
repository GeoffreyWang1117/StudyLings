# Level 2: 断点管理

## 学习目标

- 设置和删除断点
- 使用条件断点
- 理解临时断点
- 管理多个断点
- 在断点处检查程序状态

## 核心命令

### GDB 命令
```bash
break main              # 在 main 函数设置断点（简写：b）
break file.c:10         # 在文件的第 10 行设置断点
break func if x > 5     # 设置条件断点
tbreak main             # 设置临时断点（执行一次后自动删除）
info breakpoints        # 列出所有断点（简写：i b）
delete 1                # 删除断点 1（简写：d 1）
delete                  # 删除所有断点
disable 1               # 禁用断点 1
enable 1                # 启用断点 1
```

### LLDB 命令
```bash
breakpoint set -n main          # 在 main 函数设置断点（简写：b main）
breakpoint set -f file.c -l 10  # 在文件的第 10 行设置断点
breakpoint set -n func -c 'x>5' # 设置条件断点
breakpoint set -n main -o true  # 设置临时断点
breakpoint list                 # 列出所有断点（简写：br l）
breakpoint delete 1             # 删除断点 1（简写：br del 1）
breakpoint disable 1            # 禁用断点 1
breakpoint enable 1             # 启用断点 1
```

## 练习列表

### Exercise 1: 基本断点操作
**难度**: ⭐⭐ 初级

学习如何设置断点、运行到断点、查看断点列表。

**技能点**:
- 在函数上设置断点
- 在行号上设置断点
- 查看和管理断点

### Exercise 2: 条件断点
**难度**: ⭐⭐⭐ 中级

学习使用条件断点只在特定条件满足时停止。

**技能点**:
- 设置条件断点
- 理解条件表达式
- 调试循环问题

### Exercise 3: 断点管理
**难度**: ⭐⭐ 初级

学习管理多个断点，包括启用、禁用和删除。

**技能点**:
- 禁用和启用断点
- 删除断点
- 临时断点

## 快速参考

| 功能 | GDB | LLDB |
|------|-----|------|
| 函数断点 | `break main` | `b main` |
| 行号断点 | `break file.c:10` | `b file.c:10` |
| 条件断点 | `break func if x>5` | `b func -c 'x>5'` |
| 临时断点 | `tbreak main` | `b main -o true` |
| 列出断点 | `info breakpoints` | `br list` |
| 删除断点 | `delete 1` | `br del 1` |
| 禁用断点 | `disable 1` | `br dis 1` |
| 启用断点 | `enable 1` | `br en 1` |
