# GDB & LLDB 调试器学习系统

一个渐进式的 GDB 和 LLDB 调试器学习平台，通过实践练习帮助你掌握调试技能。

## 🎯 项目目标

通过一系列精心设计的实战练习，从零开始系统学习 GDB 和 LLDB 调试器，涵盖从基础命令到高级调试技巧。

## 📚 学习路径

本课程分为 13 个级别，每个级别包含多个实战练习：

### 基础级别 (Level 1-3)

### Level 1: 调试器入门
- 启动调试器和加载程序
- 基本命令：run, quit, help
- 查看源代码：list
- **目标**：熟悉调试器环境

### Level 2: 断点管理
- 设置和删除断点
- 条件断点
- 临时断点
- 断点列表和管理
- **目标**：掌握程序执行控制

### Level 3: 程序执行控制
- 单步执行：step, next
- 继续执行：continue
- 执行到指定位置：until
- 函数级别跳过：finish
- **目标**：精确控制程序执行流程

### Level 4: 变量检查与修改
- 打印变量：print, display
- 查看变量类型：ptype, whatis
- 修改变量值：set variable
- 监视点：watch
- **目标**：实时观察和修改程序状态

### Level 5: 调用栈分析
- 查看调用栈：backtrace
- 切换栈帧：frame, up, down
- 查看栈帧信息：info frame
- 函数参数和局部变量
- **目标**：理解程序调用关系

### Level 6: 多线程调试
- 线程列表：info threads
- 切换线程：thread
- 线程特定断点
- 所有线程操作
- **目标**：调试并发程序

### Level 7: 内存和数据结构
- 内存检查：x (examine)
- 数组和指针调试
- 结构体和类
- 内存布局分析
- **目标**：深入理解内存模型

### Level 8: Core Dump 分析
- 生成 core dump
- 加载和分析 core 文件
- 事后调试技巧
- **目标**：分析崩溃原因

### Level 9: 高级技巧
- 调试优化代码
- 远程调试
- 调试宏和内联函数
- 自定义命令
- **目标**：掌握专业调试技能

### 专题级别 (Level 10-12)

### Level 10: 数据结构调试 🆕
- 链表调试（单链表、双链表、循环链表）
- 树结构调试（二叉树、BST）
- 哈希表调试
- 环检测算法
- **目标**：掌握数据结构的可视化和调试

### Level 11: 多级指针调试 🆕
- 一级、二级、三级指针深度解析
- 指针数组 vs 数组指针
- 函数指针与回调机制
- `char **argv` 的内存结构
- **目标**：彻底理解指针在内存中的表现

### Level 12: 内存布局和对齐 🆕
- 结构体对齐规则
- Padding 和 Packing
- Union 和位域
- 内存段分析（代码段、数据段、栈、堆）
- **目标**：理解编译器如何组织内存

### Level 13: 链接器与符号解析 🆕
- 静态链接 vs 动态链接
- 符号表分析（强符号、弱符号）
- PLT/GOT 和延迟绑定机制
- LD_PRELOAD 函数劫持
- **目标**：掌握链接过程和符号解析原理

## 🚀 快速开始

### 前置要求

```bash
# 安装 GDB (Linux)
sudo apt-get install gdb

# 安装 LLDB (macOS 自带, Linux 需安装)
sudo apt-get install lldb

# 安装 Python 3 (用于验证脚本)
sudo apt-get install python3
```

### 开始学习

1. 克隆仓库
```bash
git clone <repository-url>
cd GDB-LLDB-Learner
```

2. 从 Level 1 开始
```bash
cd exercises/level-01-basics
cat README.md
```

3. 完成每个练习
- 阅读 README.md 了解任务
- 编译和运行示例代码
- 使用 GDB/LLDB 完成调试任务
- 运行验证脚本检查答案

## 📖 使用方法

每个练习目录包含：

```
level-XX-name/
├── README.md           # 练习说明和学习目标
├── exercise-N/         # 具体练习
│   ├── problem.md      # 问题描述
│   ├── buggy.c         # 有问题的代码
│   ├── Makefile        # 编译脚本
│   ├── solution.md     # 参考答案
│   └── verify.py       # 自动验证脚本
└── cheatsheet.md       # 命令速查表
```

### 练习流程

1. **阅读问题**：了解需要调试的问题
2. **编译代码**：`make`
3. **启动调试器**：`gdb ./program` 或 `lldb ./program`
4. **完成任务**：根据问题描述使用调试命令
5. **验证答案**：`python3 verify.py`（可选）

## 🎓 学习建议

1. **循序渐进**：按级别顺序学习，打好基础
2. **动手实践**：每个命令都要亲自尝试
3. **对比学习**：同时练习 GDB 和 LLDB，理解异同
4. **记录笔记**：记录常用命令和技巧
5. **解决实际问题**：将学到的技能应用到实际项目

## 🔧 GDB vs LLDB 命令对照

| 功能 | GDB | LLDB |
|------|-----|------|
| 启动 | `gdb program` | `lldb program` |
| 运行 | `run` / `r` | `run` / `r` |
| 断点 | `break main` / `b main` | `breakpoint set -n main` / `b main` |
| 单步 | `step` / `s` | `step` / `s` |
| 下一步 | `next` / `n` | `next` / `n` |
| 继续 | `continue` / `c` | `continue` / `c` |
| 打印 | `print var` / `p var` | `print var` / `p var` |
| 栈回溯 | `backtrace` / `bt` | `thread backtrace` / `bt` |
| 退出 | `quit` / `q` | `quit` / `q` |

完整对照表请参考：[docs/gdb-lldb-commands.md](docs/gdb-lldb-commands.md)

## 📂 项目结构

```
GDB-LLDB-Learner/
├── README.md                   # 项目主文档
├── PROJECT_SUMMARY.md          # 项目总结
├── UPDATE_LOG.md              # 更新日志 🆕
├── docs/                       # 文档和参考资料
│   ├── gdb-lldb-commands.md   # 命令对照表
│   ├── installation.md         # 安装指南
│   └── best-practices.md       # 最佳实践
├── exercises/                  # 练习目录
│   ├── level-01-basics/        # 基础级别
│   ├── level-02-breakpoints/
│   ├── level-03-execution/
│   ├── level-04-variables/     # 中级级别
│   ├── level-05-callstack/
│   ├── level-06-threads/
│   ├── level-07-memory/        # 高级级别
│   ├── level-08-coredump/
│   ├── level-09-advanced/
│   ├── level-10-datastructures/  # 专题级别 🆕
│   ├── level-11-pointers/        # 专题级别 🆕
│   └── level-12-memory-layout/   # 专题级别 🆕
├── tools/                      # 辅助工具
│   ├── learn.py               # 交互式学习助手
│   ├── checker.py             # 通用验证工具
│   └── progress.py            # 学习进度追踪
└── examples/                   # 额外示例代码
```

## 🤝 贡献

欢迎提交问题和改进建议！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何贡献。

## 📄 许可证

MIT License

## 🌟 致谢

感谢所有为调试工具发展做出贡献的开发者们。

---

**开始你的调试之旅吧！** 🚀

如有问题，请查看 [docs/faq.md](docs/faq.md) 或提交 Issue。
