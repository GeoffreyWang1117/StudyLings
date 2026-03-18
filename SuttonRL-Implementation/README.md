# Sutton RL Implementation - 交互式练习

<div align="center">

**一个交互式的强化学习算法实现练习平台**

基于 Richard S. Sutton 和 Andrew G. Barto 的《Reinforcement Learning: An Introduction (2nd Edition)》

[English](#english) | [中文](#中文)

</div>

---

## 中文

### 📚 项目简介

这是一个类似 **Rustlings** 的交互式学习项目，帮助你通过实践掌握 Sutton RL 书中的所有经典算法。

**特点：**
- 🎯 **填空式学习**：关键算法部分留空，让你亲手实现
- ✅ **自动批改**：运行代码后自动验证结果是否在预设范围内
- 📖 **循序渐进**：按照书本章节组织，从简单到复杂
- 🔄 **即时反馈**：类似 Rustlings 的 watch 模式，实时检查你的实现

### 🚀 快速开始

#### 安装

```bash
# 克隆仓库
git clone https://github.com/GeoffreyWang1117/SuttonRL-Implementation.git
cd SuttonRL-Implementation

# 安装依赖
pip install -r requirements.txt

# 或使用 pip install -e .
pip install -e .
```

#### 运行练习

```bash
# 查看所有练习
python -m sutton_rl list

# 运行特定练习
python -m sutton_rl run ch02_ex01

# Watch 模式（自动检测文件变化）
python -m sutton_rl watch

# 验证所有练习
python -m sutton_rl verify

# 查看提示
python -m sutton_rl hint ch02_ex01
```

### 📖 练习结构

```
exercises/
├── ch02_bandits/              # 第2章：多臂老虎机
│   ├── ex01_epsilon_greedy.py      # ε-贪心算法
│   ├── ex02_ucb.py                 # UCB 算法
│   ├── ex03_gradient_bandit.py     # 梯度老虎机
│   └── ex04_optimistic_initial.py  # 乐观初始值
│
├── ch04_dp/                   # 第4章：动态规划
│   ├── ex01_policy_evaluation.py   # 策略评估
│   ├── ex02_policy_iteration.py    # 策略迭代
│   ├── ex03_value_iteration.py     # 值迭代
│   └── ex04_gamblers_problem.py    # 赌徒问题
│
├── ch05_mc/                   # 第5章：蒙特卡洛方法
│   ├── ex01_first_visit_mc.py      # 首次访问 MC
│   ├── ex02_mc_es.py               # MC with ES
│   ├── ex03_off_policy_mc.py       # 离策略 MC
│   └── ex04_importance_sampling.py # 重要性采样
│
├── ch06_td/                   # 第6章：时序差分学习
│   ├── ex01_td0.py                 # TD(0)
│   ├── ex02_sarsa.py               # SARSA
│   ├── ex03_q_learning.py          # Q-Learning
│   └── ex04_expected_sarsa.py      # Expected SARSA
│
├── ch07_nstep/                # 第7章：n步自举法
│   ├── ex01_n_step_td.py           # n步TD
│   ├── ex02_n_step_sarsa.py        # n步SARSA
│   └── ex03_tree_backup.py         # 树回溯算法
│
├── ch09_approximation/        # 第9章：函数近似
│   ├── ex01_gradient_mc.py         # 梯度MC
│   └── ex02_semi_gradient_td.py    # 半梯度TD
│
├── ch10_control/              # 第10章：on-policy 控制
│   ├── ex01_episodic_sarsa.py      # 分节式SARSA
│   └── ex02_differential_sarsa.py  # 差分SARSA
│
├── ch12_eligibility/          # 第12章：资格迹
│   ├── ex01_td_lambda.py           # TD(λ)
│   ├── ex02_sarsa_lambda.py        # SARSA(λ)
│   └── ex03_true_online_td.py      # True Online TD(λ)
│
└── ch13_policy_gradient/      # 第13章：策略梯度
    ├── ex01_reinforce.py           # REINFORCE
    ├── ex02_reinforce_baseline.py  # REINFORCE with Baseline
    └── ex03_actor_critic.py        # Actor-Critic
```

### 🎓 如何使用

1. **选择一个练习**：从 `exercises/` 目录中选择一个练习文件
2. **阅读说明**：每个文件顶部有详细的算法说明和要求
3. **填写代码**：找到 `# TODO: 实现这部分` 的标记，填写你的实现
4. **运行验证**：使用 `python -m sutton_rl run <练习名>` 验证你的实现
5. **查看反馈**：系统会告诉你是否通过，以及性能指标

### 📝 练习示例

每个练习文件结构如下：

```python
"""
练习：ε-贪心算法

算法描述：
在每一步中，以概率 1-ε 选择当前最优动作，
以概率 ε 随机选择动作。

要求：
- 实现 epsilon-greedy 动作选择
- 实现动作值更新
- 平均奖励应达到 1.3 ± 0.2

参考：Sutton & Barto 第2章，第2.3节
"""

import numpy as np

class EpsilonGreedyBandit:
    def __init__(self, k_arms=10, epsilon=0.1):
        self.k = k_arms
        self.epsilon = epsilon
        self.q_values = np.zeros(k_arms)  # 动作值估计
        self.action_counts = np.zeros(k_arms)  # 动作计数

    def select_action(self):
        """选择动作：ε-贪心策略"""
        # TODO: 实现 epsilon-greedy 动作选择
        # 提示：以概率 epsilon 随机探索，否则利用当前最佳动作
        pass

    def update(self, action, reward):
        """更新动作值估计"""
        # TODO: 实现增量式动作值更新
        # 提示：使用样本平均方法
        pass

# 测试代码（不要修改）
def test_bandit():
    # ... 自动测试代码 ...
    pass
```

### ✅ 验证标准

每个练习都有自动验证标准：
- **正确性**：算法逻辑正确
- **性能**：结果在预设范围内（如平均奖励、收敛速度等）
- **代码风格**：遵循 Python 规范

### 🎯 学习路径

**初学者路径**（推荐顺序）：
1. Ch02: Multi-armed Bandits - 理解探索与利用
2. Ch04: Dynamic Programming - 理解贝尔曼方程
3. Ch06: TD Learning - 掌握在线学习
4. Ch05: Monte Carlo - 理解无模型方法
5. Ch07: n-step Methods - 统一视角

**进阶路径**：
6. Ch09-10: Function Approximation - 处理大规模问题
7. Ch12: Eligibility Traces - 高效信用分配
8. Ch13: Policy Gradient - 策略优化方法

### 🛠️ 开发

```bash
# 运行所有测试
pytest tests/

# 添加新练习
python scripts/create_exercise.py --chapter 6 --name td_learning

# 生成解答
python scripts/generate_solutions.py
```

### 📚 参考资源

- **教材**: [Reinforcement Learning: An Introduction (2nd Edition)](http://incompleteideas.net/book/the-book-2nd.html)
- **代码参考**: [ShangtongZhang/reinforcement-learning-an-introduction](https://github.com/ShangtongZhang/reinforcement-learning-an-introduction)

### 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)

### 📄 许可证

MIT License

---

## English

### 📚 About

An interactive learning platform for implementing reinforcement learning algorithms from **Sutton & Barto's RL Book (2nd Edition)**, inspired by **Rustlings**.

**Features:**
- 🎯 **Fill-in-the-blank**: Implement key algorithm components yourself
- ✅ **Auto-grading**: Automatic verification of results
- 📖 **Progressive**: Organized by book chapters, from simple to complex
- 🔄 **Instant feedback**: Rustlings-style watch mode

### 🚀 Quick Start

```bash
# Clone and install
git clone https://github.com/GeoffreyWang1117/SuttonRL-Implementation.git
cd SuttonRL-Implementation
pip install -r requirements.txt

# Run exercises
python -m sutton_rl list        # List all exercises
python -m sutton_rl run ch02_ex01  # Run specific exercise
python -m sutton_rl watch       # Watch mode
python -m sutton_rl verify      # Verify all
```

### 📖 Contents

- **Ch02**: Multi-armed Bandits (ε-greedy, UCB, Gradient Bandit)
- **Ch04**: Dynamic Programming (Policy/Value Iteration)
- **Ch05**: Monte Carlo Methods
- **Ch06**: Temporal-Difference Learning (TD(0), SARSA, Q-Learning)
- **Ch07**: n-step Bootstrapping
- **Ch09-10**: Function Approximation
- **Ch12**: Eligibility Traces (TD(λ), SARSA(λ))
- **Ch13**: Policy Gradient (REINFORCE, Actor-Critic)

### 🎓 How It Works

1. Choose an exercise from `exercises/`
2. Read the algorithm description
3. Fill in the `# TODO` sections
4. Run verification: `python -m sutton_rl run <exercise>`
5. Get instant feedback on correctness and performance

### 📝 Example Exercise

```python
"""
Exercise: ε-Greedy Algorithm

Implement epsilon-greedy action selection for k-armed bandits.

Requirements:
- Implement epsilon-greedy policy
- Average reward should reach 1.3 ± 0.2

Reference: Sutton & Barto, Chapter 2, Section 2.3
"""

class EpsilonGreedyBandit:
    def select_action(self):
        # TODO: Implement epsilon-greedy action selection
        pass

    def update(self, action, reward):
        # TODO: Implement incremental action-value update
        pass
```

### 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

### 📄 License

MIT License

---

<div align="center">
Made with ❤️ for RL learners
</div>
