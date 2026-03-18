"""
解答: ε-贪心算法 (ε-Greedy Algorithm)

这是 ex01_epsilon_greedy.py 的完整实现解答
"""

import numpy as np


class EpsilonGreedyBandit:
    """ε-贪心算法实现"""

    def __init__(self, k_arms=10, epsilon=0.1, true_values=None):
        self.k = k_arms
        self.epsilon = epsilon
        self.q_values = np.zeros(k_arms)
        self.action_counts = np.zeros(k_arms)

        if true_values is None:
            self.true_values = np.random.randn(k_arms)
        else:
            self.true_values = true_values

    def select_action(self):
        """
        ε-贪心动作选择

        Returns:
            选择的动作索引
        """
        # 生成 [0, 1) 的随机数
        if np.random.random() < self.epsilon:
            # 探索：随机选择动作
            return np.random.randint(self.k)
        else:
            # 利用：选择当前最优动作
            return np.argmax(self.q_values)

    def update(self, action, reward):
        """
        增量式更新动作值

        使用样本平均方法:
        Q_n = Q_{n-1} + 1/n [R_n - Q_{n-1}]
        """
        # 更新动作计数
        self.action_counts[action] += 1

        # 计算步长 α = 1/n
        step_size = 1.0 / self.action_counts[action]

        # 增量式更新：NewEstimate = OldEstimate + StepSize * (Target - OldEstimate)
        self.q_values[action] += step_size * (reward - self.q_values[action])

    def get_reward(self, action):
        """从 N(q*(a), 1) 采样奖励"""
        return self.true_values[action] + np.random.randn()


def run_experiment(epsilon=0.1, steps=2000, k_arms=10):
    """运行一次实验"""
    bandit = EpsilonGreedyBandit(k_arms=k_arms, epsilon=epsilon)

    rewards = []
    optimal_actions = []
    optimal_action = np.argmax(bandit.true_values)

    for step in range(steps):
        action = bandit.select_action()
        reward = bandit.get_reward(action)
        bandit.update(action, reward)

        rewards.append(reward)
        optimal_actions.append(1 if action == optimal_action else 0)

    return {
        'avg_reward': np.mean(rewards),
        'optimal_action_pct': np.mean(optimal_actions),
        'rewards': rewards,
        'q_values': bandit.q_values,
        'true_values': bandit.true_values,
    }


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 ε-贪心算法 [解答版本]")
    print("=" * 60)

    np.random.seed(42)

    n_runs = 100
    avg_rewards = []
    optimal_action_pcts = []

    print(f"\n运行 {n_runs} 次实验，每次 2000 步...")

    for run in range(n_runs):
        result = run_experiment(epsilon=0.1, steps=2000, k_arms=10)
        avg_rewards.append(result['avg_reward'])
        optimal_action_pcts.append(result['optimal_action_pct'])

    final_avg_reward = np.mean(avg_rewards)
    final_optimal_pct = np.mean(optimal_action_pcts)

    print(f"\n" + "=" * 60)
    print(f"结果:")
    print(f"  平均奖励: {final_avg_reward:.4f}")
    print(f"  最优动作选择率: {final_optimal_pct:.2%}")
    print(f"=" * 60)

    print(f"\n示例运行 (最后一次):")
    print(f"  真实动作值: {result['true_values']}")
    print(f"  估计动作值: {result['q_values']}")
    print(f"  最优动作: {np.argmax(result['true_values'])}")
    print(f"  估计最优: {np.argmax(result['q_values'])}")

    return {
        'avg_reward': final_avg_reward,
        'optimal_action_pct': final_optimal_pct,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n✅ 解答说明:")
    print(f"  1. select_action(): ε概率随机，1-ε概率选最优")
    print(f"  2. update(): 使用样本平均的增量式更新")
    print(f"  3. 步长 α = 1/n 确保收敛到真实值")
