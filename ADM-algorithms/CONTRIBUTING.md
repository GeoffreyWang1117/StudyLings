# 贡献指南

感谢您对 ADM Judge 项目的关注！

## 如何贡献

### 报告问题

如果您发现了 bug 或有功能建议：

1. 在 GitHub Issues 中搜索是否已有相关问题
2. 如果没有，创建新的 Issue，详细描述：
   - 问题的复现步骤
   - 预期行为和实际行为
   - 您的环境信息（操作系统、编译器版本等）

### 提交练习改进

如果您想改进现有练习或添加新练习：

1. Fork 本仓库
2. 创建新分支: `git checkout -b feature/your-feature-name`
3. 进行修改
4. 确保代码符合项目规范（见下文）
5. 提交 Pull Request

### 练习编写规范

每个练习应该包含：

```cpp
/*
 * 练习: exercise_name
 * 难度: Easy/Medium/Hard
 * 主题: 主题名称
 *
 * 描述:
 * 详细的问题描述
 *
 * 学习目标:
 * - 目标1
 * - 目标2
 *
 * 参考: ADM 3rd Edition - Chapter X
 */

#include <iostream>
#include <cassert>

// TODO: 函数签名和提示

// I AM NOT DONE

// ===== 测试代码 =====

void test_basic() {
    // 基本测试用例
    std::cout << "✓ Basic test passed\n";
}

void test_edge_cases() {
    // 边界情况测试
    std::cout << "✓ Edge cases test passed\n";
}

int main() {
    std::cout << "Running [Exercise Name] Tests...\n";
    std::cout << "================================\n";

    test_basic();
    test_edge_cases();

    std::cout << "\n✅ All tests passed!\n";
    return 0;
}
```

### 代码风格

- 使用 C++17 标准
- 遵循现代 C++ 最佳实践
- 函数和变量命名使用 camelCase
- 类名使用 PascalCase
- 适当添加注释，特别是算法关键步骤
- 测试用例要全面，包括边界情况

### 提交信息规范

提交信息应清晰描述变更内容：

```
类型: 简短描述

详细描述（可选）

示例:
feat: 添加二叉搜索树练习
fix: 修复归并排序的边界条件bug
docs: 更新README中的安装说明
```

类型包括：
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具相关

## 开发设置

1. 克隆仓库:
```bash
git clone https://github.com/GeoffreyWang1117/ADM-algorithms.git
cd ADM-algorithms
```

2. 构建项目:
```bash
mkdir build && cd build
cmake ..
make
```

3. 运行测试:
```bash
./adm-judge list
./adm-judge run ds01
```

## 问题和建议

如有任何问题或建议，请通过以下方式联系：

- GitHub Issues
- Pull Request 讨论

感谢您的贡献！
