"""
练习: 乐观初始值 (Optimistic Initial Values)

算法描述:
乐观初始值是一种简单但有效的鼓励探索的技术。
通过将初始动作值估计设置得很高（比实际可能的奖励都高），
贪心算法会因为"失望"（实际奖励低于预期）而自然地探索各个动作。

例如：如果实际奖励在 [-1, 1] 范围内，可以将初始值设为 +5。

优点:
- 简单易实现
- 在早期强制探索
- 适合平稳问题

缺点:
- 只在开始时有效（有限的探索）
- 不适合非平稳问题
- 需要先验知识设置合适的初始值

伪代码:
┌────────────────────────────────────────────────────┐
│ 初始化:                                            │
│   对所有 a, Q(a) ← Q_init (乐观值，如 +5)          │
│   对所有 a, N(a) ← 0                               │
│                                                    │
│ 循环每一步 t:                                      │
│   A ← argmax_a Q(a)  (贪心选择)                    │
│   R ← 执行动作 A 得到的奖励                        │
│   N(A) ← N(A) + 1                                  │
│   Q(A) ← Q(A) + [R - Q(A)] / N(A)                  │
└────────────────────────────────────────────────────┘

要求:
- 使用乐观初始值（如 +5）
- 使用纯贪心策略（epsilon = 0）
- 观察早期的探索行为
- 平均奖励应达到 1.2 ~ 1.6

参考: Sutton & Barto 第2章, 第2.6节
"""

import numpy as np


class OptimisticGreedyBandit:
    """使用乐观初始值的贪心算法"""

    def __init__(self, k_arms=10, initial_value=5.0, true_values=None):
        """
        初始化

        Args:
            k_arms: 动作数量
            initial_value: 乐观初始值
            true_values: 真实动作值
        """
        self.k = k_arms
        self.initial_value = initial_value

        # 动作值估计（乐观初始化）
        # TODO: 将所有动作值初始化为 initial_value
        self.q_values = None  # TODO: 修改这一行

        # 动作选择次数
        self.action_counts = np.zeros(k_arms)

        # 真实动作值
        if true_values is None:
            self.true_values = np.random.randn(k_arms)
        else:
            self.true_values = true_values

    def select_action(self):
        """
        选择动作: 纯贪心策略（epsilon = 0）

        Returns:
            选择的动作索引
        """
        # TODO: 实现贪心动作选择
        # 提示1: 选择 Q 值最大的动作
        # 提示2: 使用 np.argmax(self.q_values)
        # 提示3: 由于乐观初始值，未尝试的动作会优先被选择

        pass  # TODO: 删除这一行，填写你的代码

    def update(self, action, reward):
        """
        更新动作值估计

        Args:
            action: 执行的动作
            reward: 获得的奖励
        """
        # TODO: 实现增量式更新
        # 提示: 与之前的练习相同

        pass  # TODO: 删除这一行，填写你的代码

    def get_reward(self, action):
        """获取奖励"""
        return self.true_values[action] + np.random.randn()


def run_experiment(initial_value=5.0, steps=2000, k_arms=10):
    """运行一次实验"""
    bandit = OptimisticGreedyBandit(k_arms=k_arms, initial_value=initial_value)

    rewards = []
    optimal_actions = []
    action_sequence = []  # 记录动作序列
    optimal_action = np.argmax(bandit.true_values)

    for step in range(steps):
        action = bandit.select_action()
        reward = bandit.get_reward(action)
        bandit.update(action, reward)

        rewards.append(reward)
        optimal_actions.append(1 if action == optimal_action else 0)
        action_sequence.append(action)

    return {
        'avg_reward': np.mean(rewards),
        'optimal_action_pct': np.mean(optimal_actions),
        'early_exploration': len(set(action_sequence[:100])),  # 前100步尝试了多少不同动作
        'action_counts': bandit.action_counts,
    }


def test():
    """测试函数"""
    print("=" * 60)
    print("测试乐观初始值")
    print("=" * 60)

    np.random.seed(42)

    n_runs = 100
    avg_rewards = []
    optimal_action_pcts = []
    early_explorations = []

    print(f"\n运行 {n_runs} 次实验，每次 2000 步...")
    print(f"初始值 Q_init = 5.0 (乐观)")
    print(f"策略: 纯贪心 (ε = 0)")

    for run in range(n_runs):
        result = run_experiment(initial_value=5.0, steps=2000, k_arms=10)
        avg_rewards.append(result['avg_reward'])
        optimal_action_pcts.append(result['optimal_action_pct'])
        early_explorations.append(result['early_exploration'])

    final_avg_reward = np.mean(avg_rewards)
    final_optimal_pct = np.mean(optimal_action_pcts)
    avg_early_exploration = np.mean(early_explorations)

    print(f"\n" + "=" * 60)
    print(f"结果:")
    print(f"  平均奖励: {final_avg_reward:.4f}")
    print(f"  最优动作选择率: {final_optimal_pct:.2%}")
    print(f"  前100步平均探索动作数: {avg_early_exploration:.1f}/10")
    print(f"=" * 60)

    print(f"\n示例运行 - 动作选择次数:")
    print(f"  {result['action_counts']}")

    # 验证早期探索
    exploration_early = avg_early_exploration >= 8

    return {
        'avg_reward': final_avg_reward,
        'optimal_action_pct': final_optimal_pct,
        'exploration_early': exploration_early,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n提示:")
    print(f"  - 乐观初始值在早期强制探索所有动作")
    print(f"  - 随着时间推移，估计值会收敛到真实值")
    print(f"  - 这种方法不适合非平稳问题")
    print(f"\n对比实验:")
    print(f"  试试将 initial_value 改为 0.0，观察性能变化")
    print(f"  （纯贪心 + 零初始值 = 很差的探索）")
