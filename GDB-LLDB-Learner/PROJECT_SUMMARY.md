# GDB/LLDB 学习系统 - 项目总结

## 项目完成状态

✅ **项目已完成** - 所有练习和文档已创建并提交到 Git 仓库

## 项目统计

- **总练习数**: 39 个（13个级别 × 3个练习）
- **源代码文件**: 39 个 C 程序
- **文档文件**: 90+ 个 Markdown 文件
- **总代码行数**: 11000+ 行（代码 + 文档）

## 级别概览

### Level 1: 调试器入门 ⭐
- **Exercise 1**: 第一个调试会话（启动、运行、退出）
- **Exercise 2**: 带参数运行程序（命令行参数调试）
- **Exercise 3**: 探索帮助系统（使用 help 和 apropos）

### Level 2: 断点管理 ⭐⭐
- **Exercise 1**: 基本断点操作（设置、查看、删除）
- **Exercise 2**: 条件断点（调试质数查找器）
- **Exercise 3**: 断点管理（启用、禁用、临时断点）

### Level 3: 程序执行控制 ⭐⭐
- **Exercise 1**: Step vs Next（理解进入和跳过函数）
- **Exercise 2**: 使用 finish 命令（嵌套函数调用）
- **Exercise 3**: 调试递归函数（斐波那契数列）

### Level 4: 变量检查与修改 ⭐⭐⭐
- **Exercise 1**: 变量检查和修改（结构体调试）
- **Exercise 2**: 使用监视点 Watchpoints（追踪变量变化）
- **Exercise 3**: 数组和指针调试（多维数组）

### Level 5: 调用栈分析 ⭐⭐⭐
- **Exercise 1**: 查看调用栈（backtrace, frame）
- **Exercise 2**: 查看函数参数（info args）
- **Exercise 3**: 使用调用栈追踪错误（NULL指针调试）

### Level 6: 多线程调试 ⭐⭐⭐⭐
- **Exercise 1**: 基本线程调试（线程切换和查看）
- **Exercise 2**: 调试竞态条件（counter 增加竞争）
- **Exercise 3**: 检测死锁（mutex 死锁场景）

### Level 7: 内存和数据结构 ⭐⭐⭐⭐
- **Exercise 1**: 检查内存（x 命令使用）
- **Exercise 2**: 指针和解引用（指针链调试）
- **Exercise 3**: 调试缓冲区溢出（strcpy 溢出）

### Level 8: Core Dump 分析 ⭐⭐⭐⭐
- **Exercise 1**: 分析 Core Dump（NULL指针崩溃）
- **Exercise 2**: 段错误分析（segfault 调试）
- **Exercise 3**: Assertion 失败分析（assert 调试）

### Level 9: 高级调试技巧 ⭐⭐⭐⭐⭐
- **Exercise 1**: 调试优化代码（-Og vs -O2）
- **Exercise 2**: 断点命令自动化（自动化调试流程）
- **Exercise 3**: Python 脚本和自定义命令（扩展调试器）

## 文件结构

```
GDB-LLDB-Learner/
├── README.md                       # 项目主文档
├── LICENSE                         # MIT 许可证
├── CONTRIBUTING.md                 # 贡献指南
├── PROJECT_SUMMARY.md             # 项目总结（本文件）
├── quickstart.sh                  # 快速开始脚本
├── create_exercises.sh            # 练习创建辅助脚本
│
├── docs/                          # 文档目录
│   ├── gdb-lldb-commands.md      # 完整命令对照表
│   ├── installation.md            # 安装指南
│   └── best-practices.md          # 调试最佳实践
│
├── tools/                         # 辅助工具
│   ├── learn.py                   # 交互式学习助手
│   ├── progress.py                # 进度追踪工具
│   └── checker.py                 # 练习验证脚本
│
├── exercises/                     # 练习目录
│   ├── level-01-basics/          # Level 1-9
│   │   ├── README.md
│   │   ├── exercise-1/
│   │   │   ├── problem.md
│   │   │   ├── source.c
│   │   │   ├── Makefile
│   │   │   └── solution.md
│   │   ├── exercise-2/
│   │   └── exercise-3/
│   ├── level-02-breakpoints/
│   ├── level-03-execution/
│   ├── level-04-variables/
│   ├── level-05-callstack/
│   ├── level-06-threads/
│   ├── level-07-memory/
│   ├── level-08-coredump/
│   └── level-09-advanced/
│
└── examples/                      # 额外示例（预留）
```

## 核心功能

### 1. 渐进式学习路径
- 从零基础到高级技巧
- 每个级别难度递增
- 涵盖实际调试场景

### 2. 双调试器支持
- GDB 和 LLDB 命令对照
- 每个练习都提供两种解决方案
- 详细的命令对比表

### 3. 实战导向
- 真实的 C 代码示例
- 常见的调试场景
- 实用的错误案例

### 4. 完整的解决方案
- 每个练习都有详细的 solution.md
- 逐步操作说明
- GDB 和 LLDB 双版本

### 5. 辅助工具
- 交互式学习工具（learn.py）
- 进度追踪（progress.py）
- 自动验证（checker.py）
- 快速启动脚本（quickstart.sh）

## 练习特色

### 真实场景覆盖

1. **内存问题**
   - 缓冲区溢出
   - NULL 指针解引用
   - 指针链调试

2. **并发问题**
   - 竞态条件
   - 死锁检测
   - 线程切换

3. **性能调试**
   - 优化代码调试
   - 函数调用分析
   - 性能瓶颈定位

4. **崩溃分析**
   - Core dump 分析
   - 段错误调试
   - Assertion 失败

### 教学质量

- ✅ 清晰的问题描述
- ✅ 逐步的操作指导
- ✅ 详细的解决方案
- ✅ 实用的技巧总结
- ✅ 常见错误警示
- ✅ 扩展挑战任务

## 技术栈

- **语言**: C (C99标准)
- **调试器**: GDB 7.0+, LLDB 10.0+
- **编译器**: GCC 7.0+, Clang 10.0+
- **脚本**: Python 3.6+, Bash
- **构建工具**: Make
- **版本控制**: Git

## 适用人群

1. **初学者**: 从 Level 1 开始系统学习
2. **中级开发者**: 直接学习 Level 4-6
3. **高级开发者**: 关注 Level 7-9 高级技巧
4. **教师**: 作为教学材料使用
5. **培训机构**: 作为调试课程基础

## 学习建议

1. **顺序学习**: 按 Level 1-9 顺序完成
2. **动手实践**: 每个命令都要亲自尝试
3. **对比学习**: 同时学习 GDB 和 LLDB
4. **记录笔记**: 记录常用命令和技巧
5. **实际应用**: 在自己的项目中应用所学

## 使用指南

### 快速开始

```bash
# 1. 克隆仓库
git clone <repository-url>
cd GDB-LLDB-Learner

# 2. 运行快速开始脚本
./quickstart.sh

# 3. 启动交互式学习工具
python3 tools/learn.py

# 4. 或直接开始 Level 1
cd exercises/level-01-basics/exercise-1
cat problem.md
make
gdb ./hello
```

### 学习流程

1. **阅读 README.md**: 了解级别概览
2. **阅读 problem.md**: 理解练习目标
3. **编译运行**: 使用 make 编译程序
4. **动手调试**: 使用 GDB/LLDB 完成任务
5. **查看答案**: 参考 solution.md
6. **追踪进度**: 使用 progress.py 记录

## 贡献

欢迎贡献！详见 [CONTRIBUTING.md](CONTRIBUTING.md)

可以贡献：
- 新的练习题目
- 文档改进
- Bug 修复
- 翻译工作
- 工具增强

## 后续计划

### 短期计划（已完成）
- ✅ 完成所有 9 个级别
- ✅ 每个级别 3 个练习
- ✅ 完整的解决方案
- ✅ 辅助工具开发

### 中期计划（待实现）
- [ ] 添加视频教程
- [ ] 创建在线练习平台
- [ ] 多语言版本（英文、日文）
- [ ] GUI 调试器对比

### 长期计划（规划中）
- [ ] 集成 CI/CD 自动测试
- [ ] 开发 Web 版本
- [ ] 添加更多语言示例（C++, Rust）
- [ ] 创建认证系统

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 致谢

感谢所有为调试工具发展做出贡献的开发者。

## 联系方式

- GitHub Issues: 报告问题和建议
- Pull Requests: 欢迎贡献代码
- Discussions: 技术讨论和经验分享

---

**开始你的调试之旅吧！** 🚀

_最后更新: 2024-11-18_
_版本: 3.0.0_
_状态: 完成_

### Level 10: 数据结构调试 ⭐⭐⭐⭐⭐
- **Exercise 1**: 链表调试（单链表、双链表、循环链表）
- **Exercise 2**: 二叉树调试（BST 结构和遍历）
- **Exercise 3**: 哈希表调试（冲突解决和分布分析）

### Level 11: 多级指针 ⭐⭐⭐⭐⭐
- **Exercise 1**: 多级指针（一级、二级、三级指针）
- **Exercise 2**: 指针数组 vs 数组指针（理解 argv 结构）
- **Exercise 3**: 函数指针与回调（PLT/GOT 原理）

### Level 12: 内存布局和对齐 ⭐⭐⭐⭐⭐
- **Exercise 1**: 结构体对齐和Padding（优化内存布局）
- **Exercise 2**: Union 和位域（内存共享和压缩）
- **Exercise 3**: 内存段分析（代码段、数据段、栈、堆）

### Level 13: 链接器与符号解析 ⭐⭐⭐⭐⭐ 🆕
- **Exercise 1**: 静态链接 vs 动态链接（库的创建和使用）
- **Exercise 2**: 符号表和符号解析（强符号、弱符号、可见性）
- **Exercise 3**: PLT/GOT 和延迟绑定（动态链接机制和 LD_PRELOAD）

## 版本历史

### v3.0 (2024)
- 新增 Level 13: 链接器与符号解析
- 添加 PLT/GOT 延迟绑定机制详解
- 添加 LD_PRELOAD 函数劫持示例
- 总练习数增至 39 个

### v2.0 (2024)
- 新增 Level 10-12: 高级主题
- 添加数据结构调试
- 添加多级指针分析
- 添加内存布局和对齐

### v1.0 (2024)
- 初始版本，Level 1-9
- 27 个基础和进阶练习
