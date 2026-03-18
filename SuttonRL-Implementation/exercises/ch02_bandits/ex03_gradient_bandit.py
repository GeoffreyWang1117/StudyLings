"""
练习: 梯度老虎机算法 (Gradient Bandit Algorithm)

算法描述:
梯度老虎机算法学习的是每个动作的数值偏好 H_t(a)，而不是动作值估计。
偏好值通过 softmax 函数转换为动作概率：

    Pr{A_t = a} = exp(H_t(a)) / Σ_b exp(H_t(b)) = π_t(a)

更新规则基于梯度上升：
    H_{t+1}(A_t) = H_t(A_t) + α(R_t - R̄_t)(1 - π_t(A_t))     (选中的动作)
    H_{t+1}(a)   = H_t(a) - α(R_t - R̄_t)π_t(a)               (其他动作)

其中 R̄_t 是到时刻 t 的平均奖励（作为基线）。

伪代码:
┌────────────────────────────────────────────────────┐
│ 初始化:                                            │
│   对所有 a, H(a) ← 0                               │
│   R̄ ← 0                                            │
│                                                    │
│ 循环每一步 t:                                      │
│   计算所有动作的概率: π(a) = softmax(H(a))        │
│   根据概率 π 采样动作 A                            │
│   R ← 执行动作 A 得到的奖励                        │
│                                                    │
│   更新偏好:                                        │
│     H(A) ← H(A) + α(R - R̄)(1 - π(A))              │
│     对所有 a ≠ A: H(a) ← H(a) - α(R - R̄)π(a)      │
│                                                    │
│   更新平均奖励: R̄ ← R̄ + β(R - R̄)                  │
└────────────────────────────────────────────────────┘

要求:
- 实现 softmax 动作选择
- 实现基于梯度的偏好更新
- 使用基线（平均奖励）
- 平均奖励应达到 1.2 ~ 1.6

参考: Sutton & Barto 第2章, 第2.8节
"""

import numpy as np


class GradientBandit:
    """梯度老虎机算法实现"""

    def __init__(self, k_arms=10, alpha=0.1, true_values=None):
        """
        初始化

        Args:
            k_arms: 动作数量
            alpha: 学习率
            true_values: 真实动作值
        """
        self.k = k_arms
        self.alpha = alpha

        # 动作偏好值 H(a)
        self.preferences = np.zeros(k_arms)

        # 动作概率 π(a)
        self.action_probs = np.ones(k_arms) / k_arms

        # 平均奖励（基线）
        self.avg_reward = 0.0
        self.t = 0

        # 真实动作值
        if true_values is None:
            self.true_values = np.random.randn(k_arms)
        else:
            self.true_values = true_values

    def softmax(self, preferences):
        """
        计算 softmax 概率分布

        Args:
            preferences: 偏好值数组

        Returns:
            概率分布（和为1）
        """
        # TODO: 实现 softmax 函数
        # 提示1: exp_prefs = np.exp(preferences - np.max(preferences))
        #       (减去最大值是为了数值稳定性)
        # 提示2: 归一化: probabilities = exp_prefs / np.sum(exp_prefs)
        # 提示3: 返回概率分布

        pass  # TODO: 删除这一行，填写你的代码

    def select_action(self):
        """
        根据当前偏好选择动作

        Returns:
            选择的动作索引
        """
        # TODO: 实现动作选择
        # 提示1: 首先使用 softmax 计算概率分布
        # 提示2: 使用 np.random.choice(self.k, p=probabilities) 按概率采样
        # 提示3: 保存概率分布到 self.action_probs（更新时需要）

        pass  # TODO: 删除这一行，填写你的代码

    def update(self, action, reward):
        """
        更新偏好值

        Args:
            action: 执行的动作
            reward: 获得的奖励
        """
        self.t += 1

        # TODO: 实现梯度更新
        # 提示1: 计算基线偏差: baseline = reward - self.avg_reward
        # 提示2: 更新选中动作的偏好:
        #        self.preferences[action] += self.alpha * baseline * (1 - self.action_probs[action])
        # 提示3: 更新其他动作的偏好:
        #        for a in range(self.k):
        #            if a != action:
        #                self.preferences[a] -= self.alpha * baseline * self.action_probs[a]
        # 提示4: 更新平均奖励:
        #        self.avg_reward += (reward - self.avg_reward) / self.t

        pass  # TODO: 删除这一行，填写你的代码

    def get_reward(self, action):
        """获取奖励"""
        return self.true_values[action] + np.random.randn()


def run_experiment(alpha=0.1, steps=2000, k_arms=10):
    """运行一次实验"""
    bandit = GradientBandit(k_arms=k_arms, alpha=alpha)

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
        'preferences': bandit.preferences,
        'action_probs': bandit.action_probs,
    }


def test():
    """测试函数"""
    print("=" * 60)
    print("测试梯度老虎机算法")
    print("=" * 60)

    np.random.seed(42)

    n_runs = 100
    avg_rewards = []
    optimal_action_pcts = []

    print(f"\n运行 {n_runs} 次实验，每次 2000 步...")
    print(f"学习率 α = 0.1")

    for run in range(n_runs):
        result = run_experiment(alpha=0.1, steps=2000, k_arms=10)
        avg_rewards.append(result['avg_reward'])
        optimal_action_pcts.append(result['optimal_action_pct'])

    final_avg_reward = np.mean(avg_rewards)
    final_optimal_pct = np.mean(optimal_action_pcts)

    print(f"\n" + "=" * 60)
    print(f"结果:")
    print(f"  平均奖励: {final_avg_reward:.4f}")
    print(f"  最优动作选择率: {final_optimal_pct:.2%}")
    print(f"=" * 60)

    print(f"\n示例运行 - 最终偏好值:")
    print(f"  {result['preferences']}")
    print(f"\n示例运行 - 最终动作概率:")
    print(f"  {result['action_probs']}")

    return {
        'avg_reward': final_avg_reward,
        'optimal_action_pct': final_optimal_pct,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n提示:")
    print(f"  - 梯度方法直接优化动作概率")
    print(f"  - 基线（平均奖励）有助于减小方差")
    print(f"  - 最终的动作概率应该集中在最优动作上")
