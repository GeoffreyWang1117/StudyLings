"""
解答: 汤普森采样 (Thompson Sampling)

这是 ex05_thompson_sampling.py 的完整实现解答
"""

import numpy as np


class ThompsonSamplingBandit:
    """Thompson Sampling算法"""

    def __init__(self, k_arms=10, true_values=None):
        """
        初始化

        Args:
            k_arms: 动作数量
            true_values: 真实动作值（用于生成伯努利奖励）
        """
        self.k = k_arms

        # Beta分布参数（α: 成功次数+1, β: 失败次数+1）
        # 初始化为Beta(1,1)，即均匀分布
        self.alpha = np.ones(k_arms)
        self.beta = np.ones(k_arms)

        # 真实动作值（转换为伯努利成功概率）
        if true_values is None:
            # 将奖励映射到[0,1]区间作为成功概率
            self.true_values = np.random.uniform(0.3, 0.7, k_arms)
        else:
            # 假设true_values在[-2, 2]范围，映射到[0,1]
            self.true_values = (np.array(true_values) + 2) / 4
            self.true_values = np.clip(self.true_values, 0.1, 0.9)

    def select_action(self):
        """
        选择动作: Thompson Sampling

        Returns:
            选择的动作索引
        """
        # 从每个动作的Beta后验中采样
        theta_samples = np.random.beta(self.alpha, self.beta)

        # 选择采样值最大的动作
        action = np.argmax(theta_samples)

        return action

    def update(self, action, reward):
        """
        更新后验分布

        Args:
            action: 执行的动作
            reward: 获得的奖励（0或1）
        """
        # Beta分布的贝叶斯更新
        if reward == 1:
            self.alpha[action] += 1  # 观察到成功
        else:
            self.beta[action] += 1   # 观察到失败

    def get_reward(self, action):
        """
        获取奖励（伯努利分布）

        Args:
            action: 执行的动作

        Returns:
            reward: 0或1
        """
        # 根据成功概率生成伯努利奖励
        success_prob = self.true_values[action]
        return 1 if np.random.random() < success_prob else 0


def run_experiment(steps=2000, k_arms=10):
    """运行一次实验"""
    bandit = ThompsonSamplingBandit(k_arms=k_arms)

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
        'final_alpha': bandit.alpha,
        'final_beta': bandit.beta,
    }


def test():
    """测试函数"""
    print("=" * 60)
    print("测试Thompson Sampling [解答版本]")
    print("=" * 60)

    np.random.seed(42)

    n_runs = 100
    avg_rewards = []
    optimal_action_pcts = []

    print(f"\n运行 {n_runs} 次实验，每次 2000 步...")
    print(f"算法: Thompson Sampling (Beta分布)")

    for run in range(n_runs):
        result = run_experiment(steps=2000, k_arms=10)
        avg_rewards.append(result['avg_reward'])
        optimal_action_pcts.append(result['optimal_action_pct'])

    final_avg_reward = np.mean(avg_rewards)
    final_optimal_pct = np.mean(optimal_action_pcts)

    print(f"\n" + "=" * 60)
    print(f"结果:")
    print(f"  平均奖励: {final_avg_reward:.4f}")
    print(f"  最优动作选择率: {final_optimal_pct:.2%}")
    print(f"=" * 60)

    # 显示最后一次运行的后验
    print(f"\n示例后验分布 (α, β):")
    for i in range(min(5, len(result['final_alpha']))):
        alpha = result['final_alpha'][i]
        beta = result['final_beta'][i]
        mean = alpha / (alpha + beta)
        print(f"  动作{i}: Beta({alpha:.0f}, {beta:.0f}), 均值={mean:.3f}")

    return {
        'avg_reward': final_avg_reward,
        'optimal_action_pct': final_optimal_pct,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n✅ 解答说明:")
    print(f"  1. 初始化: α=1, β=1 (均匀先验)")
    print(f"  2. 采样: θ ~ Beta(α, β) 对每个动作")
    print(f"  3. 选择: a = argmax θ")
    print(f"  4. 更新: 成功α+1，失败β+1")
    print(f"\n贝叶斯解释:")
    print(f"  - Beta分布是Bernoulli的共轭先验")
    print(f"  - α-1 = 成功次数, β-1 = 失败次数")
    print(f"  - 后验均值 = α/(α+β) = 经验成功率")
    print(f"  - 后验方差随观测增多而减小")
    print(f"\n优势:")
    print(f"  - 无需调参（vs ε-greedy的ε, UCB的c）")
    print(f"  - 理论最优（贝叶斯regret最小）")
    print(f"  - 自适应探索（不确定性驱动）")
    print(f"  - 2025年在推荐系统、A/B测试中广泛应用")
