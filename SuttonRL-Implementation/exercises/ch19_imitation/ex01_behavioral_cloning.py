"""
练习: Behavioral Cloning (BC) - 行为克隆

算法描述:
Behavioral Cloning是最简单的模仿学习方法，将模仿学习转化为监督学习问题。
这是RLHF中Supervised Fine-Tuning (SFT)阶段的理论基础。

核心思想:
- 收集专家演示数据 D = {(s_i, a_i)}
- 训练策略 π_θ 预测专家动作
- 目标: min_θ E[(π_θ(s) - a_expert)²]  (连续动作)
  或: min_θ E[-log π_θ(a_expert|s)]  (离散动作)

数学公式:
1. 监督学习目标:
   L(θ) = E_{(s,a)~D}[-log π_θ(a|s)]

2. 梯度下降:
   θ ← θ - α∇_θ L(θ)

优势:
- 简单直接
- 不需要奖励函数
- 不需要环境交互
- 快速训练

局限:
- Covariate shift: 训练分布 ≠ 测试分布
- 缺乏泛化能力
- 需要大量专家数据
- 误差累积（分布漂移）

在RLHF中的应用:
- SFT阶段: 在人类标注数据上进行BC
- 初始化策略用于后续RL训练
- ChatGPT等LLM的第一步训练

参考: Pomerleau (1991) "Efficient Training of Artificial Neural Networks for Autonomous Navigation"
"""

import numpy as np
from collections import deque

class BehavioralCloning:
    """行为克隆智能体"""
    def __init__(self, state_dim, action_dim, learning_rate=0.001):
        """
        初始化

        Args:
            state_dim: 状态维度
            action_dim: 动作维度（离散动作数或连续动作维度）
            learning_rate: 学习率
        """
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.lr = learning_rate

        # 策略网络参数 π_θ(a|s)
        self.weights = np.random.randn(state_dim, action_dim) * 0.01
        self.bias = np.zeros(action_dim)

    def get_action_probs(self, state):
        """
        获取动作概率分布（离散动作）

        Args:
            state: 状态向量

        Returns:
            probs: 动作概率分布
        """
        # TODO: 实现softmax策略
        # 提示1: logits = state @ weights + bias
        # 提示2: probs = softmax(logits)
        # 提示3: softmax(x) = exp(x) / sum(exp(x))
        pass  # TODO

    def predict_action(self, state, deterministic=False):
        """
        预测动作

        Args:
            state: 状态
            deterministic: 是否确定性选择

        Returns:
            action: 选择的动作
        """
        # TODO: 实现动作预测
        # 提示1: 获取动作概率
        # 提示2: 确定性: 选择最大概率动作
        # 提示3: 随机性: 从分布采样
        pass  # TODO

    def train_on_batch(self, states, actions):
        """
        在一个batch上训练

        Args:
            states: 状态batch [batch_size, state_dim]
            actions: 专家动作batch [batch_size]

        Returns:
            loss: 平均损失
        """
        # TODO: 实现批量训练
        # 提示1: 计算预测概率
        # 提示2: 计算交叉熵损失: -log π(a|s)
        # 提示3: 计算梯度: ∇L = E[state^T (pred_probs - one_hot)]
        # 提示4: 更新参数: weights -= lr * grad
        pass  # TODO

    def train(self, expert_data, epochs=100, batch_size=32):
        """
        训练BC智能体

        Args:
            expert_data: 专家数据 [(state, action), ...]
            epochs: 训练轮数
            batch_size: 批大小

        Returns:
            training_history: 训练历史
        """
        # TODO: 实现完整训练循环
        # 提示1: 对每个epoch:
        # 提示2:   打乱数据
        # 提示3:   分批训练
        # 提示4:   记录loss
        pass  # TODO

    def evaluate(self, env, n_episodes=10):
        """
        评估策略性能

        Args:
            env: 环境
            n_episodes: 评估轮数

        Returns:
            avg_reward: 平均回报
        """
        # TODO: 实现评估
        # 提示1: 运行n_episodes个episodes
        # 提示2: 使用确定性策略
        # 提示3: 记录总回报
        pass  # TODO


def collect_expert_data(env, expert_policy, n_episodes=100):
    """
    收集专家演示数据

    Args:
        env: 环境
        expert_policy: 专家策略
        n_episodes: 收集的episodes数

    Returns:
        expert_data: [(state, action), ...]
    """
    # TODO: 实现数据收集
    # 提示1: 对每个episode:
    # 提示2:   重置环境
    # 提示3:   专家决策并记录(state, action)
    # 提示4:   执行动作
    pass  # TODO


def demonstrate_covariate_shift():
    """
    演示covariate shift问题

    BC的主要问题: 训练时看到的状态分布 ≠ 测试时遇到的状态分布
    """
    print("\n=== Covariate Shift演示 ===")
    print("问题: BC在训练数据外的状态泛化差")
    print("\n例子: 自动驾驶")
    print("  训练: 专家总是在车道中心 -> 只见过中心状态")
    print("  测试: 偶然偏离 -> 没见过偏离状态 -> 不知如何纠正 -> 持续偏离")
    print("\n数学:")
    print("  训练分布: p_expert(s)")
    print("  测试分布: p_BC(s) ≠ p_expert(s)")
    print("  误差累积: ε_T ~ O(T²)  (T是时间步数)")
    print("\n解决方案:")
    print("  1. DAgger: 迭代收集更多数据")
    print("  2. 加入噪声: 增强数据鲁棒性")
    print("  3. RL fine-tuning: 在环境中进一步优化")


def compare_with_rl():
    """比较BC和RL的区别"""
    print("\n=== BC vs RL ===")
    print("\nBehavioral Cloning:")
    print("  ✓ 不需要奖励函数")
    print("  ✓ 不需要环境交互（离线）")
    print("  ✓ 训练快速")
    print("  ✗ 需要大量专家数据")
    print("  ✗ Covariate shift问题")
    print("  ✗ 无法超越专家")
    print("\nReinforcement Learning:")
    print("  ✓ 可以超越演示数据")
    print("  ✓ 自动探索改进")
    print("  ✗ 需要环境交互")
    print("  ✗ 需要奖励函数")
    print("  ✗ 训练慢，样本效率低")
    print("\nRLHF的策略:")
    print("  1. BC (SFT): 快速初始化策略")
    print("  2. RL (PPO): 根据奖励模型进一步优化")


# 简单环境用于测试
class SimpleNavigationEnv:
    """简单导航环境"""
    def __init__(self):
        self.state_dim = 4  # [x, y, goal_x, goal_y]
        self.action_dim = 4  # [上, 下, 左, 右]
        self.reset()

    def reset(self):
        self.pos = np.random.rand(2) * 10  # 随机起点
        self.goal = np.random.rand(2) * 10  # 随机目标
        return self._get_state()

    def _get_state(self):
        return np.concatenate([self.pos, self.goal])

    def step(self, action):
        # 动作: 0=上, 1=下, 2=左, 3=右
        move = {0: [0, 1], 1: [0, -1], 2: [-1, 0], 3: [1, 0]}
        self.pos += move[action]
        self.pos = np.clip(self.pos, 0, 10)

        # 奖励: 接近目标
        dist = np.linalg.norm(self.pos - self.goal)
        reward = -dist
        done = dist < 0.5

        return self._get_state(), reward, done


def expert_policy(state):
    """简单专家策略: 朝目标移动"""
    pos, goal = state[:2], state[2:]
    diff = goal - pos

    # 选择最大差异的维度
    if abs(diff[0]) > abs(diff[1]):
        return 2 if diff[0] < 0 else 3  # 左/右
    else:
        return 1 if diff[1] < 0 else 0  # 下/上


if __name__ == "__main__":
    print("练习: Behavioral Cloning - 行为克隆")
    print("核心: 监督学习模仿专家策略")
    print("\n目标函数:")
    print("  L(θ) = E_{(s,a)~D}[-log π_θ(a|s)]")
    print("\n应用: RLHF的SFT阶段")

    demonstrate_covariate_shift()
    compare_with_rl()

    print("\n" + "="*50)
    print("训练示例...")

    env = SimpleNavigationEnv()

    # 收集专家数据
    print("\n1. 收集专家演示数据...")
    expert_data = collect_expert_data(env, expert_policy, n_episodes=50)

    # 训练BC
    print("2. 训练BC智能体...")
    agent = BehavioralCloning(state_dim=4, action_dim=4)
    agent.train(expert_data, epochs=50)

    # 评估
    print("3. 评估BC策略...")
    avg_reward = agent.evaluate(env, n_episodes=10)
    print(f"平均回报: {avg_reward:.2f}")
