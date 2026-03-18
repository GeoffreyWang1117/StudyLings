"""
练习: ε-贪心算法 (ε-Greedy Algorithm)

算法描述:
ε-greedy 是最简单的平衡探索与利用的策略。在每一步中：
- 以概率 ε 随机选择一个动作（探索）
- 以概率 1-ε 选择当前估计值最大的动作（利用）

伪代码:
┌────────────────────────────────────────────────────┐
│ 初始化:                                            │
│   对所有 a, Q(a) ← 0, N(a) ← 0                     │
│                                                    │
│ 循环每一步 t:                                      │
│   if 随机数 < ε:                                   │
│       A ← 随机选择一个动作                         │
│   else:                                            │
│       A ← argmax_a Q(a)                            │
│                                                    │
│   R ← 执行动作 A 得到的奖励                        │
│   N(A) ← N(A) + 1                                  │
│   Q(A) ← Q(A) + [R - Q(A)] / N(A)                  │
└────────────────────────────────────────────────────┘

要求:
- 实现 epsilon-greedy 动作选择策略
- 实现增量式动作值更新
- 在10臂老虎机上运行2000步
- 平均奖励应达到 1.2 ~ 1.6
- 最优动作选择率应达到 70% 以上

参考: Sutton & Barto 第2章, 第2.2-2.3节
"""

import numpy as np


class EpsilonGreedyBandit:
    """ε-贪心算法实现"""

    def __init__(self, k_arms=10, epsilon=0.1, true_values=None):
        """
        初始化 k-臂老虎机

        Args:
            k_arms: 动作数量
            epsilon: 探索概率
            true_values: 每个动作的真实期望奖励（用于测试）
        """
        self.k = k_arms
        self.epsilon = epsilon

        # 动作值估计 Q(a)
        self.q_values = np.zeros(k_arms)

        # 动作选择次数 N(a)
        self.action_counts = np.zeros(k_arms)

        # 真实的动作值（用于测试）
        if true_values is None:
            self.true_values = np.random.randn(k_arms)
        else:
            self.true_values = true_values

    def select_action(self):
        """
        选择动作: ε-贪心策略

        Returns:
            选择的动作索引 (0 到 k-1)
        """
        # TODO: 实现 epsilon-greedy 动作选择
        # 提示1: 使用 np.random.random() 生成 [0,1) 的随机数
        # 提示2: 如果随机数 < epsilon，随机探索
        # 提示3: 否则，选择当前 Q 值最大的动作（利用）
        # 提示4: 使用 np.argmax(self.q_values) 找到最大值的索引
        # 提示5: 使用 np.random.randint(self.k) 随机选择动作

        pass  # TODO: 删除这一行，填写你的代码

    def update(self, action, reward):
        """
        更新动作值估计: 增量式样本平均

        Args:
            action: 执行的动作
            reward: 获得的奖励
        """
        # TODO: 实现增量式动作值更新
        # 提示1: 更新动作计数 N(a)
        # 提示2: 使用增量式更新公式:
        #        Q(a) = Q(a) + α[R - Q(a)]
        #        其中 α = 1/N(a) (样本平均)
        # 提示3: 也可以直接用: NewEstimate = OldEstimate + StepSize * (Target - OldEstimate)

        pass  # TODO: 删除这一行，填写你的代码

    def get_reward(self, action):
        """
        模拟执行动作获得奖励
        奖励 = 真实值 + 噪声

        Args:
            action: 动作索引

        Returns:
            该动作的奖励（带噪声）
        """
        # 从正态分布 N(q*(a), 1) 采样奖励
        return self.true_values[action] + np.random.randn()


def run_experiment(epsilon=0.1, steps=2000, k_arms=10):
    """
    运行一次实验

    Args:
        epsilon: 探索概率
        steps: 总步数
        k_arms: 动作数量

    Returns:
        结果字典，包含平均奖励和最优动作百分比
    """
    bandit = EpsilonGreedyBandit(k_arms=k_arms, epsilon=epsilon)

    # 记录数据
    rewards = []
    optimal_actions = []
    optimal_action = np.argmax(bandit.true_values)

    for step in range(steps):
        # 选择动作
        action = bandit.select_action()

        # 获得奖励
        reward = bandit.get_reward(action)

        # 更新估计
        bandit.update(action, reward)

        # 记录
        rewards.append(reward)
        optimal_actions.append(1 if action == optimal_action else 0)

    avg_reward = np.mean(rewards)
    optimal_action_pct = np.mean(optimal_actions)

    return {
        'avg_reward': avg_reward,
        'optimal_action_pct': optimal_action_pct,
        'rewards': rewards,
        'q_values': bandit.q_values,
        'true_values': bandit.true_values,
    }


def test():
    """
    测试函数 - 会被自动调用验证你的实现

    Returns:
        结果字典
    """
    print("=" * 60)
    print("测试 ε-贪心算法")
    print("=" * 60)

    # 设置随机种子以便复现
    np.random.seed(42)

    # 运行多次实验取平均
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

    # 显示一个示例运行
    print(f"\n示例运行 (最后一次):")
    print(f"  真实动作值: {result['true_values']}")
    print(f"  估计动作值: {result['q_values']}")
    print(f"  最优动作: {np.argmax(result['true_values'])}")
    print(f"  估计最优: {np.argmax(result['q_values'])}")

    # 返回结果供检查器验证
    return {
        'avg_reward': final_avg_reward,
        'optimal_action_pct': final_optimal_pct,
    }


if __name__ == '__main__':
    # 运行测试
    result = test()

    print(f"\n提示:")
    print(f"  - 如果平均奖励 < 1.2, 检查动作选择和更新逻辑")
    print(f"  - 如果最优动作选择率 < 70%, 可能 epsilon 值太大或更新有误")
    print(f"  - 尝试调整 epsilon 值观察性能变化")
