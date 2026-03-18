# 贡献指南 Contributing Guide

感谢你对 Sutton RL Implementation 项目的兴趣！

## 如何贡献

### 报告问题

如果你发现了 bug 或有功能建议：

1. 查看 [Issues](https://github.com/GeoffreyWang1117/SuttonRL-Implementation/issues) 确认问题未被报告
2. 创建新 Issue，提供详细信息：
   - Bug: 复现步骤、预期行为、实际行为
   - 功能: 详细描述和使用场景

### 添加新练习

我们欢迎为书中其他算法添加练习！

#### 练习文件结构

```python
"""
练习: [算法名称]

算法描述:
[清晰的算法描述]

伪代码:
┌────────────────────────────────────┐
│ [算法的伪代码]                      │
└────────────────────────────────────┘

要求:
- [要求1]
- [要求2]

参考: Sutton & Barto 第X章, 第X.X节
"""

import numpy as np

class YourAlgorithm:
    def __init__(self, ...):
        # TODO: 初始化

    def method(self):
        # TODO: 实现这个方法
        pass

def test():
    """测试函数 - 会被自动调用"""
    # 测试代码
    return {
        'metric1': value1,
        'metric2': value2,
    }

if __name__ == '__main__':
    test()
```

#### 添加步骤

1. **创建练习文件**
   ```bash
   # 在相应章节目录下创建
   touch exercises/chXX_topic/exYY_algorithm_name.py
   ```

2. **更新练习信息**
   在 `sutton_rl/exercise_info.py` 中添加：
   ```python
   {
       'id': 'chXX_exYY_algorithm_name',
       'chapter': 'chXX',
       'chapter_name': '第XX章: Topic Name',
       'name': 'Algorithm Name',
       'path': 'chXX_topic/exYY_algorithm_name.py',
       'difficulty': 'easy|medium|hard|expert',
       'test_func': 'test',
       'reference': 'Sutton & Barto, Chapter XX, Section XX.XX',
       'hints': [
           '提示1',
           '提示2',
       ],
       'learning_points': [
           '学习要点1',
           '学习要点2',
       ],
   }
   ```

3. **添加验证标准**
   在 `sutton_rl/checker.py` 的 `criteria` 字典中添加：
   ```python
   'chXX_exYY_algorithm_name': {
       'metric1_min': value,
       'metric2_max': value,
       'converges': True,
   }
   ```

4. **测试练习**
   ```bash
   python -m sutton_rl run chXX_exYY_algorithm_name
   ```

### 练习设计原则

1. **留空原则**
   - 留下算法的核心部分让学习者实现
   - 提供足够的提示和伪代码
   - 环境、测试代码应完整提供

2. **难度梯度**
   - 从简单到复杂
   - 每个练习聚焦一个核心概念
   - 提供详细的提示

3. **自动验证**
   - 定义明确的验证标准
   - 返回可量化的指标
   - 允许合理的误差范围

4. **文档质量**
   - 清晰的算法描述
   - 规范的伪代码
   - 准确的参考文献

### 代码风格

遵循 PEP 8 规范：

```bash
# 使用 black 格式化
pip install black
black sutton_rl/ exercises/

# 使用 flake8 检查
pip install flake8
flake8 sutton_rl/ exercises/
```

### 提交 Pull Request

1. Fork 本仓库
2. 创建特性分支
   ```bash
   git checkout -b feature/add-exercise-xxx
   ```
3. 提交更改
   ```bash
   git commit -m "Add exercise: XXX"
   ```
4. 推送到你的 Fork
   ```bash
   git push origin feature/add-exercise-xxx
   ```
5. 创建 Pull Request

#### PR 描述模板

```markdown
## 描述
简要描述本 PR 的内容

## 变更类型
- [ ] 新增练习
- [ ] Bug 修复
- [ ] 文档改进
- [ ] 功能增强

## 练习信息（如适用）
- 章节: 第X章
- 算法: XXX
- 难度: Easy/Medium/Hard/Expert

## 测试
- [ ] 练习可以正常运行
- [ ] 测试函数返回正确格式
- [ ] 验证标准合理
- [ ] 文档完整

## 相关 Issue
Closes #XXX
```

### 需要帮助的领域

我们特别欢迎以下贡献：

- [ ] **第5章**: Monte Carlo 方法练习
- [ ] **第7章**: n-step Bootstrapping 练习
- [ ] **第8章**: Planning and Learning 练习
- [ ] **第9-10章**: Function Approximation 练习
- [ ] **第11章**: Off-policy Methods 练习
- [ ] **第12章**: Eligibility Traces 练习
- [ ] **第13章**: Policy Gradient 完整实现
- [ ] **可视化**: 添加学习曲线、策略可视化
- [ ] **环境**: 更多经典 RL 环境
- [ ] **测试**: 单元测试覆盖
- [ ] **文档**: 中英文翻译

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/GeoffreyWang1117/SuttonRL-Implementation.git
cd SuttonRL-Implementation

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/

# 运行示例练习
python -m sutton_rl list
python -m sutton_rl run ch02_ex01_epsilon_greedy
```

## 行为准则

- 尊重所有贡献者
- 建设性的反馈
- 专注于教育价值
- 保持代码质量

## 问题？

如有任何问题，请：
- 创建 Issue
- 发送邮件至 [your-email]
- 加入讨论区

---

再次感谢你的贡献！🎉
