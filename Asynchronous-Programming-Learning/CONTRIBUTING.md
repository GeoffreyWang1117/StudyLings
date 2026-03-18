# 贡献指南

首先，感谢你考虑为 Async Learnings 做出贡献！🎉

这个文档提供了贡献的指南和最佳实践。

## 目录

- [行为准则](#行为准则)
- [如何贡献](#如何贡献)
- [开发设置](#开发设置)
- [提交指南](#提交指南)
- [练习题编写指南](#练习题编写指南)
- [文档贡献](#文档贡献)
- [报告问题](#报告问题)

## 行为准则

我们致力于提供一个友好、安全和包容的环境。请：

- 尊重不同的观点和经验
- 接受建设性的批评
- 关注对社区最有利的事情
- 对他人保持同理心

## 如何贡献

### 你可以贡献什么？

1. **新的练习题**
   - 填补现有内容的空白
   - 添加更高级的话题
   - 创建真实世界的场景

2. **改进现有练习**
   - 更清晰的说明
   - 更好的提示
   - 修复错误

3. **文档**
   - 改进学习指南
   - 添加更多示例
   - 翻译成其他语言

4. **框架功能**
   - CLI 改进
   - 新的命令
   - 更好的用户体验

5. **工具函数**
   - 添加新的实用函数
   - 改进现有实现
   - 添加更多文档

## 开发设置

### 1. Fork 和克隆

```bash
# Fork 这个仓库到你的 GitHub 账户，然后：
git clone https://github.com/YOUR_USERNAME/Asynchronous-Programming-Learning.git
cd Asynchronous-Programming-Learning
```

### 2. 安装依赖

```bash
npm install
```

### 3. 创建分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-fix-name
```

### 4. 进行更改

按照下面的指南进行更改。

### 5. 测试

```bash
# 测试现有练习
npm run verify

# 测试所有答案
npm run test:solutions

# 测试你的新练习
npm run run your-exercise-name
```

### 6. 提交和推送

```bash
git add .
git commit -m "feat: 添加新的练习..."
git push origin feature/your-feature-name
```

### 7. 创建 Pull Request

在 GitHub 上创建 Pull Request，详细描述你的更改。

## 提交指南

我们使用[约定式提交](https://www.conventionalcommits.org/)格式：

```
<类型>(<范围>): <描述>

[可选的正文]

[可选的脚注]
```

### 类型

- `feat`: 新功能
- `fix`: 错误修复
- `docs`: 文档更改
- `style`: 代码格式（不影响代码运行）
- `refactor`: 重构
- `test`: 添加测试
- `chore`: 构建过程或辅助工具的变动

### 示例

```
feat(exercises): 添加 WebSocket 相关练习

添加了 3 个关于 WebSocket 异步通信的练习题：
- WebSocket 连接建立
- 消息发送和接收
- 错误处理和重连

Closes #42
```

## 练习题编写指南

### 文件命名

```
exercises/<章节>/<编号>_<名称>.ts
```

例如：`exercises/03_async_await/01_async_intro.ts`

### 练习题结构

```typescript
// 练习 <编号>: <标题>
//
// <详细说明，解释这个练习要学习的概念>
//
// <学习要点>

// 辅助函数（已实现）
function helperFunction() {
  // ...
}

// TODO: <清晰的任务描述>
function exerciseFunction() {
  // 在这里实现代码
  // 提示：<有用的提示>
}

// 测试代码（已实现）
exerciseFunction();

// 预期输出或验证
```

### 练习题最佳实践

1. **清晰的目标**：每个练习应该专注于一个概念
2. **渐进式难度**：从简单到复杂
3. **实用的例子**：使用真实世界的场景
4. **有用的提示**：提供足够的指导，但不要直接给出答案
5. **完整的测试**：确保练习可以被验证
6. **详细的注释**：解释为什么，而不仅仅是怎么做

### 配置练习

在 `src/config.ts` 中添加练习配置：

```typescript
{
  name: 'exercise_name',
  path: 'exercises/section/file.ts',
  mode: 'test', // 或 'run'
  hint: '简短的提示'
}
```

### 提供答案

在 `solutions/` 目录中提供完整的参考答案：

```typescript
// 练习 <编号>: <标题> - 答案

// 完整的实现
function exerciseFunction() {
  // 实现代码
}

// 测试代码
```

## 文档贡献

### 文档类型

1. **学习指南** (`docs/GUIDE.md`)
   - 概念解释
   - 代码示例
   - 最佳实践

2. **API 文档** (`docs/UTILS.md`)
   - 函数签名
   - 参数说明
   - 使用示例

3. **快速参考** (`docs/CHEATSHEET.md`)
   - 简洁的代码片段
   - 常见模式
   - 快速查找

### 文档最佳实践

- 使用清晰、简洁的语言
- 提供完整的代码示例
- 使用代码高亮
- 添加目录便于导航
- 保持格式一致

## 报告问题

### 报告 Bug

使用 Bug 报告模板，包含：

- 清晰的标题
- 复现步骤
- 预期行为
- 实际行为
- 环境信息（OS、Node 版本等）
- 相关代码或截图

### 功能请求

使用功能请求模板，包含：

- 清晰的标题
- 问题描述（当前的痛点）
- 建议的解决方案
- 替代方案
- 额外的上下文

## 代码审查

所有贡献都需要经过代码审查。我们会：

- 检查代码质量
- 验证测试
- 确保文档完整
- 提供建设性的反馈

请耐心等待审查，并对反馈保持开放态度。

## 许可证

通过贡献，你同意你的贡献将按照项目的 MIT 许可证进行许可。

## 问题？

如果你有任何问题，可以：

- 开一个 Issue
- 在讨论区提问
- 联系维护者

---

再次感谢你的贡献！每一个贡献，无论大小，都让这个项目变得更好。🚀
