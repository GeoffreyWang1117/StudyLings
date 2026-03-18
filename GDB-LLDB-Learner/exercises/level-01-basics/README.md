# Level 1: 调试器入门

欢迎来到 GDB/LLDB 学习之旅的第一关！

## 学习目标

- 启动和退出调试器
- 了解调试器的基本界面
- 运行程序
- 查看源代码
- 获取帮助信息

## 核心命令

### GDB 命令
```bash
gdb program          # 启动 GDB 调试程序
(gdb) help          # 查看帮助
(gdb) list          # 列出源代码（简写：l）
(gdb) run           # 运行程序（简写：r）
(gdb) run arg1 arg2 # 带参数运行
(gdb) quit          # 退出（简写：q）
```

### LLDB 命令
```bash
lldb program         # 启动 LLDB 调试程序
(lldb) help         # 查看帮助
(lldb) source list  # 列出源代码（简写：l）
(lldb) run          # 运行程序（简写：r）
(lldb) run arg1 arg2 # 带参数运行
(lldb) quit         # 退出（简写：q）
```

## 练习列表

### Exercise 1: 第一个调试会话
**难度**: ⭐ 入门

学习如何启动调试器、查看代码和运行简单程序。

**技能点**:
- 启动调试器
- 使用 `list` 命令查看源代码
- 使用 `run` 命令运行程序
- 使用 `quit` 命令退出

### Exercise 2: 带参数运行程序
**难度**: ⭐ 入门

学习如何向程序传递命令行参数。

**技能点**:
- 使用参数运行程序
- 查看程序输出
- 理解参数传递

### Exercise 3: 探索帮助系统
**难度**: ⭐ 入门

学习如何使用调试器的内置帮助系统。

**技能点**:
- 使用 `help` 命令
- 查找特定命令的帮助
- 了解命令分类

## 学习提示

1. **Tab 补全是你的朋友**
   - 在 GDB 和 LLDB 中，按 Tab 键可以自动补全命令和符号
   - 例如：输入 `bre` 然后按 Tab，会自动补全为 `break`

2. **命令可以缩写**
   - `run` 可以简写为 `r`
   - `list` 可以简写为 `l`
   - `quit` 可以简写为 `q`
   - `help` 可以简写为 `h`

3. **查看更多代码**
   - 直接按回车键会重复上一个 `list` 命令，继续显示后面的代码
   - `list 10` 会显示第 10 行附近的代码
   - `list main` 会显示 main 函数的代码

4. **运行多次**
   - 可以多次使用 `run` 命令重新运行程序
   - 每次运行都会重新开始

## 常见问题

**Q: 为什么看不到源代码？**
A: 需要使用 `-g` 选项编译程序以包含调试信息：`gcc -g program.c -o program`

**Q: GDB 和 LLDB 有什么区别？**
A: 两者功能相似，但命令语法有所不同。GDB 主要用于 Linux，LLDB 主要用于 macOS，但都是跨平台的。

**Q: 如何退出调试器？**
A: 使用 `quit` 或 `q` 命令，或按 Ctrl+D。

## 下一步

完成所有练习后，继续学习 [Level 2: 断点管理](../level-02-breakpoints/README.md)

## 快速参考

| 功能 | GDB | LLDB |
|------|-----|------|
| 启动 | `gdb program` | `lldb program` |
| 帮助 | `help` | `help` |
| 查看代码 | `list` / `l` | `source list` / `l` |
| 运行 | `run` / `r` | `run` / `r` |
| 退出 | `quit` / `q` | `quit` / `q` |
