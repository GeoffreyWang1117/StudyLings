# 贡献指南

感谢你考虑为 GDB-LLDB-Learner 项目做出贡献！

## 如何贡献

### 报告问题

如果你发现了问题：

1. 检查 [Issues](https://github.com/yourusername/GDB-LLDB-Learner/issues) 确认问题是否已被报告
2. 如果没有，创建新的 Issue
3. 清晰地描述问题：
   - 操作系统和版本
   - GDB/LLDB 版本
   - 重现步骤
   - 预期行为 vs 实际行为

### 建议新功能

1. 创建一个 Issue 描述你的想法
2. 说明为什么这个功能有用
3. 如果可能，提供使用示例

### 提交代码

1. Fork 这个仓库
2. 创建你的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交你的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启一个 Pull Request

## 添加新练习

如果你想添加新的练习：

### 练习结构

每个练习应包含：

```
level-XX-name/
└── exercise-N/
    ├── problem.md       # 问题描述（必需）
    ├── program.c        # 示例代码（必需）
    ├── Makefile         # 编译脚本（必需）
    ├── solution.md      # 参考答案（推荐）
    └── verify.py        # 验证脚本（可选）
```

### 练习指南

1. **清晰的学习目标**：每个练习应该有明确的学习目标
2. **渐进式难度**：从简单到复杂
3. **实用性**：模拟真实的调试场景
4. **完整的文档**：
   - 清晰的问题描述
   - 详细的步骤说明
   - GDB 和 LLDB 两种命令
   - 参考答案

### 代码示例要求

```c
#include <stdio.h>

/*
 * 简短描述程序的目的
 * 说明这个练习要学习什么
 */

// 代码应该：
// 1. 简洁明了
// 2. 有适当的注释
// 3. 使用有意义的变量名
// 4. 符合 C 标准（C99 或更新）
```

### Problem.md 模板

```markdown
# Exercise N: 练习标题

## 目标

简短描述这个练习的学习目标。

## 背景

提供必要的背景信息。

## 任务

列出学生需要完成的任务。

## 步骤

### 1. 编译并启动
...

### 2. 设置断点
...

## 问题思考

提出 2-3 个思考题。

## 扩展挑战

提供额外的挑战（可选）。
```

## 代码风格

### C 代码

- 使用 4 空格缩进
- 遵循 Linux 内核代码风格
- 函数名使用 snake_case
- 常量使用 UPPER_CASE

### Python 代码

- 遵循 PEP 8
- 使用 4 空格缩进
- 添加文档字符串
- 类型提示（Python 3.6+）

### Markdown

- 使用中文撰写
- 代码块指定语言
- 保持一致的标题层级

## 测试

在提交之前：

1. 确保所有代码能够编译
2. 在 GDB 和 LLDB 中都测试过
3. 验证脚本能正常工作
4. 检查文档的准确性

```bash
# 测试编译
make

# 测试 GDB
gdb ./program

# 测试 LLDB
lldb ./program

# 运行验证脚本
python3 verify.py
```

## 文档

### 更新 README

如果你添加了新的级别或重要功能：

1. 更新主 README.md
2. 更新相应级别的 README.md
3. 更新命令对照表（如果需要）

### 保持一致性

- 使用与现有文档相同的格式和风格
- 保持术语的一致性
- 确保示例代码的风格一致

## Pull Request 指南

### PR 标题

使用清晰的标题：

- `Add: 添加 Level X Exercise Y`
- `Fix: 修复 Level X Exercise Y 的问题`
- `Doc: 更新安装文档`
- `Improve: 改进 Level X 的说明`

### PR 描述

包含：

1. 更改的摘要
2. 更改的动机和上下文
3. 测试结果
4. 相关 Issue（如果有）

示例：

```markdown
## 摘要
添加了 Level 4 Exercise 3，关于使用 watchpoints。

## 动机
填补了变量监控这个重要主题的空白。

## 测试
- ✓ 在 Ubuntu 20.04 + GDB 9.2 上测试
- ✓ 在 macOS 12 + LLDB 13 上测试
- ✓ 代码能够正确编译和运行
- ✓ 验证脚本通过

## 相关 Issue
Closes #42
```

## 版权和许可

- 你提交的所有代码将在 MIT 许可下发布
- 确保你有权利贡献你提交的代码
- 不要包含受版权保护的代码

## 行为准则

- 尊重其他贡献者
- 接受建设性的批评
- 关注对项目最有利的事情
- 对社区成员表示同理心

## 问题？

如果你有任何问题，可以：

1. 查看现有的 Issues
2. 创建新的 Issue
3. 加入讨论

感谢你的贡献！ 🎉
