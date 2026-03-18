"""
练习: UCB算法 (Upper-Confidence-Bound Action Selection)

算法描述:
UCB 通过为每个动作计算置信上界来平衡探索与利用。
选择具有最高上界的动作：

    A_t = argmax_a [Q_t(a) + c * sqrt(ln(t) / N_t(a))]

其中:
- Q_t(a): 动作 a 在时刻 t 的值估计
- N_t(a): 到时刻 t 为止选择动作 a 的次数
- c: 控制探索程度的参数 (通常取 sqrt(2))
- t: 当前时间步

伪代码:
┌────────────────────────────────────────────────────┐
│ 初始化:                                            │
│   对所有 a, Q(a) ← 0, N(a) ← 0                     │
│                                                    │
│ 循环每一步 t:                                      │
│   if 存在 N(a) = 0 的动作:                         │
│       A ← 选择任一 N(a) = 0 的动作                 │
│   else:                                            │
│       A ← argmax_a [Q(a) + c*sqrt(ln(t)/N(a))]     │
│                                                    │
│   R ← 执行动作 A 得到的奖励                        │
│   N(A) ← N(A) + 1                                  │
│   Q(A) ← Q(A) + [R - Q(A)] / N(A)                  │
└────────────────────────────────────────────────────┘

要求:
- 实现 UCB 动作选择策略
- 处理 N(a) = 0 的情况（避免除零）
- 平均奖励应达到 1.3 ~ 1.7
- 最优动作选择率应达到 75% 以上

参考: Sutton & Barto 第2章, 第2.7节
"""

import numpy as np


class UCBBandit:
    """UCB算法实现"""

    def __init__(self, k_arms=10, c=2.0, true_values=None):
        """
        初始化 k-臂老虎机

        Args:
            k_arms: 动作数量
            c: UCB 参数，控制探索程度
            true_values: 每个动作的真实期望奖励
        """
        self.k = k_arms
        self.c = c

        # 动作值估计
        self.q_values = np.zeros(k_arms)

        # 动作选择次数
        self.action_counts = np.zeros(k_arms)

        # 当前时间步
        self.t = 0

        # 真实的动作值
        if true_values is None:
            self.true_values = np.random.randn(k_arms)
        else:
            self.true_values = true_values

    def select_action(self):
        """
        选择动作: UCB 策略

        Returns:
            选择的动作索引
        """
        self.t += 1

        # TODO: 实现 UCB 动作选择
        # 提示1: 首先检查是否有从未尝试过的动作 (N(a) = 0)
        # 提示2: 如果有，优先选择这些动作
        # 提示3: 否则，计算每个动作的 UCB 值:
        #        UCB(a) = Q(a) + c * sqrt(ln(t) / N(a))
        # 提示4: 选择 UCB 值最大的动作
        # 提示5: 使用 np.log(self.t) 计算 ln(t)

        pass  # TODO: 删除这一行，填写你的代码

    def update(self, action, reward):
        """
        更新动作值估计

        Args:
            action: 执行的动作
            reward: 获得的奖励
        """
        # TODO: 实现增量式动作值更新
        # 提示: 与 epsilon-greedy 相同的更新规则

        pass  # TODO: 删除这一行，填写你的代码

    def get_reward(self, action):
        """获取奖励"""
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
    print("测试 UCB 算法")
    print("=" * 60)

    np.random.seed(42)

    n_runs = 100
    avg_rewards = []
    optimal_action_pcts = []

    print(f"\n运行 {n_runs} 次实验，每次 2000 步...")
    print(f"UCB 参数 c = 2.0")

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

    print(f"\n示例运行 - 动作选择次数分布:")
    print(f"  {result['action_counts']}")
    print(f"  (注意: UCB 倾向于更均匀地探索)")

    return {
        'avg_reward': final_avg_reward,
        'optimal_action_pct': final_optimal_pct,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n提示:")
    print(f"  - UCB 比 ε-贪心更有效，因为它智能地选择探索对象")
    print(f"  - 参数 c 越大，探索越多")
    print(f"  - UCB 确保所有动作最终都会被多次尝试")
