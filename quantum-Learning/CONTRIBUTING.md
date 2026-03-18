# 贡献指南

感谢你对 Quantum Rustlings 项目的兴趣！

## 如何贡献

### 报告问题

如果你发现了 bug 或有改进建议：

1. 检查 [Issues](https://github.com/yourusername/quantum-Learning/issues) 是否已存在相关问题
2. 如果没有，创建新的 Issue，提供：
   - 清晰的标题和描述
   - 重现步骤（如果是 bug）
   - 预期行为和实际行为
   - 环境信息（Python版本、Qiskit版本等）

### 添加新练习

想要添加新的练习题？太好了！

1. **规划练习**：
   - 确定练习的难度级别
   - 明确学习目标
   - 设计测试用例

2. **创建练习文件**：
   ```python
   """
   练习 XX: 标题
   ==================

   目标：简短描述

   知识点：
   - 要点1
   - 要点2

   任务：具体任务描述
   """

   # 导入必要的库

   def main_function():
       """练习的主要函数"""
       # TODO: 待完成的代码
       pass

   def test_function():
       """测试函数"""
       # 测试代码
       pass

   if __name__ == '__main__':
       try:
           test_function()
           print("🎉 恭喜！")
       except AssertionError as e:
           print(f"❌ 测试失败: {e}")
           exit(1)
   ```

3. **更新配置**：
   - 在 `info.toml` 中添加练习信息
   - 包括 name, path, mode, hint

4. **提供解决方案**（可选）：
   - 在 `solutions/` 目录下提供参考答案

### 改进文档

文档改进包括：
- 修正拼写错误
- 改进说明
- 添加示例
- 翻译（欢迎其他语言）

### 代码风格

- 遵循 PEP 8 Python代码风格
- 使用有意义的变量名
- 添加适当的注释
- 保持代码简洁清晰

### 提交 Pull Request

1. Fork 本仓库
2. 创建你的特性分支：`git checkout -b feature/my-new-feature`
3. 提交你的改动：`git commit -am 'Add some feature'`
4. 推送到分支：`git push origin feature/my-new-feature`
5. 创建新的 Pull Request

### Pull Request 指南

- 提供清晰的标题和描述
- 如果解决了某个 Issue，在描述中引用它
- 确保所有测试通过
- 保持提交历史清晰

## 练习题设计原则

1. **渐进式难度**：从简单到复杂
2. **清晰的目标**：每个练习有明确的学习目标
3. **实践导向**：动手编码，而非纯理论
4. **即时反馈**：测试能快速验证答案
5. **有用的提示**：卡住时能获得帮助
6. **真实场景**：尽可能联系实际应用

## 需要帮助？

- 加入讨论：[GitHub Discussions](https://github.com/yourusername/quantum-Learning/discussions)
- 查看现有的 Issues 和 PRs
- 阅读项目文档

再次感谢你的贡献！🎉
