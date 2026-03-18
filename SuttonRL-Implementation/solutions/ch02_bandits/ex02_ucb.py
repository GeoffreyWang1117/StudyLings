"""
解答: UCB算法 (Upper-Confidence-Bound)

这是 ex02_ucb.py 的完整实现解答
"""

import numpy as np


class UCBBandit:
    """UCB算法实现"""

    def __init__(self, k_arms=10, c=2.0, true_values=None):
        self.k = k_arms
        self.c = c
        self.q_values = np.zeros(k_arms)
        self.action_counts = np.zeros(k_arms)
        self.t = 0

        if true_values is None:
            self.true_values = np.random.randn(k_arms)
        else:
            self.true_values = true_values

    def select_action(self):
        """
        UCB 动作选择

        A_t = argmax_a [Q_t(a) + c * sqrt(ln(t) / N_t(a))]
        """
        self.t += 1

        # 首先选择所有未尝试的动作
        for a in range(self.k):
            if self.action_counts[a] == 0:
                return a

        # 计算所有动作的 UCB 值
        ucb_values = np.zeros(self.k)
        for a in range(self.k):
            exploration_bonus = self.c * np.sqrt(np.log(self.t) / self.action_counts[a])
            ucb_values[a] = self.q_values[a] + exploration_bonus

        # 选择 UCB 值最大的动作
        return np.argmax(ucb_values)

    def update(self, action, reward):
        """增量式更新"""
        self.action_counts[action] += 1
        step_size = 1.0 / self.action_counts[action]
        self.q_values[action] += step_size * (reward - self.q_values[action])

    def get_reward(self, action):
        return self.true_values[action] + np.random.randn()


def run_experiment(c=2.0, steps=2000, k_arms=10):
    """运行一次实验"""
    bandit = UCBBandit(k_arms=k_arms, c=c)

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
        'action_counts': bandit.action_counts,
    }


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 UCB 算法 [解答版本]")
    print("=" * 60)

    np.random.seed(42)

    n_runs = 100
    avg_rewards = []
    optimal_action_pcts = []

    print(f"\n运行 {n_runs} 次实验，每次 2000 步...")

    for run in range(n_runs):
        result = run_experiment(c=2.0, steps=2000, k_arms=10)
        avg_rewards.append(result['avg_reward'])
        optimal_action_pcts.append(result['optimal_action_pct'])

    final_avg_reward = np.mean(avg_rewards)
    final_optimal_pct = np.mean(optimal_action_pcts)

    print(f"\n" + "=" * 60)
    print(f"结果:")
    print(f"  平均奖励: {final_avg_reward:.4f}")
    print(f"  最优动作选择率: {final_optimal_pct:.2%}")
    print(f"=" * 60)

    print(f"\n示例运行 - 动作选择次数:")
    print(f"  {result['action_counts']}")

    return {
        'avg_reward': final_avg_reward,
        'optimal_action_pct': final_optimal_pct,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n✅ 解答说明:")
    print(f"  1. 优先选择未尝试的动作（N(a)=0）")
    print(f"  2. UCB值 = Q(a) + c*sqrt(ln(t)/N(a))")
    print(f"  3. 探索奖励随时间衰减，确保收敛")
