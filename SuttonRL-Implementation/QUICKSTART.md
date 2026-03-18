# 快速开始 Quick Start

5分钟上手 Sutton RL Implementation！

## 安装

### 1. 克隆仓库

```bash
git clone https://github.com/GeoffreyWang1117/SuttonRL-Implementation.git
cd SuttonRL-Implementation
```

### 2. 安装依赖

```bash
# 使用 pip
pip install -r requirements.txt

# 或安装为可编辑包
pip install -e .
```

### 3. 验证安装

```bash
python -m sutton_rl list
```

你应该看到所有可用练习的列表。

## 第一个练习

### 1. 查看练习列表

```bash
python -m sutton_rl list
```

输出示例：
```
======================================================================
Sutton RL Exercises - 强化学习算法练习
======================================================================

第2章: Multi-armed Bandits (多臂老虎机)
------------------------------------------------------------
 1. [○] ch02_ex01_epsilon_greedy  - ε-贪心算法 (ε-Greedy)
 2. [○] ch02_ex02_ucb             - UCB算法 (Upper-Confidence-Bound)
 ...
```

### 2. 打开练习文件

```bash
# 使用你喜欢的编辑器
vim exercises/ch02_bandits/ex01_epsilon_greedy.py
# 或
code exercises/ch02_bandits/ex01_epsilon_greedy.py
```

### 3. 阅读说明

每个练习文件包含：
- 📖 算法描述
- 📋 伪代码
- ✅ 要求
- 💡 提示
- 📚 参考文献

### 4. 填写代码

找到 `# TODO:` 标记，填写你的实现：

```python
def select_action(self):
    """选择动作: ε-greedy 策略"""
    # TODO: 实现 epsilon-greedy 动作选择
    # 提示1: 使用 np.random.random() 生成随机数
    # 提示2: 如果随机数 < epsilon，随机探索
    # 提示3: 否则，选择当前 Q 值最大的动作

    # 你的代码在这里
    if np.random.random() < self.epsilon:
        return np.random.randint(self.k)
    else:
        return np.argmax(self.q_values)
```

### 5. 运行测试

```bash
python -m sutton_rl run ch02_ex01_epsilon_greedy
```

### 6. 查看结果

如果实现正确，你会看到：
```
======================================================================
✓ 练习通过！
======================================================================

📚 学习要点:
  • 理解探索与利用的权衡 (Exploration vs. Exploitation)
  • 掌握增量式更新公式
  • 了解 ε 参数对性能的影响
```

如果有问题，查看提示：
```bash
python -m sutton_rl hint ch02_ex01_epsilon_greedy
```

## 工作流程

### Watch 模式（推荐）

```bash
python -m sutton_rl watch
```

Watch 模式会监控文件变化，自动运行测试。修改代码保存后即刻看到结果！

### 手动模式

```bash
# 运行特定练习
python -m sutton_rl run ch02_ex01_epsilon_greedy

# 查看提示
python -m sutton_rl hint ch02_ex01_epsilon_greedy

# 验证所有练习
python -m sutton_rl verify
```

## 学习路径

### 初学者（推荐顺序）

1. **第2章: Multi-armed Bandits** ⭐⭐
   - 理解 RL 的基本概念
   - 掌握探索与利用的权衡
   ```bash
   python -m sutton_rl run ch02_ex01_epsilon_greedy
   python -m sutton_rl run ch02_ex02_ucb
   ```

2. **第4章: Dynamic Programming** ⭐⭐⭐
   - 理解 Bellman 方程
   - 掌握策略评估和改进
   ```bash
   python -m sutton_rl run ch04_ex01_policy_evaluation
   python -m sutton_rl run ch04_ex03_value_iteration
   ```

3. **第6章: TD Learning** ⭐⭐⭐⭐
   - 掌握核心 RL 算法
   - 理解 on-policy 和 off-policy
   ```bash
   python -m sutton_rl run ch06_ex02_sarsa
   python -m sutton_rl run ch06_ex03_q_learning
   ```

### 进阶学习者

4. **第5章: Monte Carlo Methods**
5. **第7章: n-step Bootstrapping**
6. **第9-10章: Function Approximation**
7. **第12章: Eligibility Traces**
8. **第13章: Policy Gradient Methods**

## 常见问题

### Q: 练习有答案吗？

A: `solutions/` 目录包含完整实现供参考。但建议先自己尝试！

### Q: 测试失败怎么办？

1. 仔细阅读提示
2. 检查伪代码实现
3. 使用 `python -m sutton_rl hint <exercise>` 获取帮助
4. 参考 Sutton & Barto 书中的相关章节
5. 查看 `solutions/` 中的参考实现

### Q: 如何调试？

```python
# 在你的代码中添加打印语句
def select_action(self):
    print(f"Q values: {self.q_values}")
    print(f"Epsilon: {self.epsilon}")
    # ...
```

### Q: 可以修改测试代码吗？

不建议。测试代码用于验证你的实现。如果你想实验：
```bash
# 复制练习文件
cp exercises/ch02_bandits/ex01_epsilon_greedy.py my_experiment.py
# 随意修改 my_experiment.py
python my_experiment.py
```

### Q: 需要什么预备知识？

- Python 基础
- NumPy 基础
- 强化学习基础（建议先阅读 Sutton & Barto 书相应章节）

## 进阶用法

### 自定义参数

直接修改练习文件中的参数实验：
```python
# 在 test() 函数中修改
result = run_experiment(
    epsilon=0.2,  # 增加探索
    steps=5000,   # 更多步数
    k_arms=20     # 更多动作
)
```

### 可视化

```python
import matplotlib.pyplot as plt

# 在 test() 函数中添加
plt.plot(rewards)
plt.xlabel('Steps')
plt.ylabel('Reward')
plt.title('Learning Curve')
plt.show()
```

### 比较算法

```python
# 运行多个算法并比较
results_epsilon = run_experiment(epsilon=0.1)
results_ucb = run_ucb_experiment(c=2.0)

print(f"ε-greedy: {results_epsilon['avg_reward']:.2f}")
print(f"UCB: {results_ucb['avg_reward']:.2f}")
```

## 获取帮助

- 📖 阅读 [README.md](README.md)
- 🤝 查看 [CONTRIBUTING.md](CONTRIBUTING.md)
- 💬 提交 [Issue](https://github.com/GeoffreyWang1117/SuttonRL-Implementation/issues)
- 📚 参考 [Sutton & Barto 书](http://incompleteideas.net/book/the-book-2nd.html)

## 下一步

1. 完成第2章所有练习
2. 尝试实现第4章的动态规划算法
3. 挑战第6章的 TD 学习方法
4. 贡献新练习！

祝学习愉快！🚀
