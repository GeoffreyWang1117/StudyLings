"""
解答: 梯度老虎机算法

这是 ex03_gradient_bandit.py 的完整实现解答
"""

import numpy as np


class GradientBandit:
    """梯度老虎机算法实现"""

    def __init__(self, k_arms=10, alpha=0.1, true_values=None):
        self.k = k_arms
        self.alpha = alpha
        self.preferences = np.zeros(k_arms)
        self.action_probs = np.ones(k_arms) / k_arms
        self.avg_reward = 0.0
        self.t = 0

        if true_values is None:
            self.true_values = np.random.randn(k_arms)
        else:
            self.true_values = true_values

    def softmax(self, preferences):
        """计算softmax概率分布"""
        # 数值稳定性：减去最大值
        exp_prefs = np.exp(preferences - np.max(preferences))
        probabilities = exp_prefs / np.sum(exp_prefs)
        return probabilities

    def select_action(self):
        """根据当前偏好选择动作"""
        # 计算概率分布
        self.action_probs = self.softmax(self.preferences)

        # 按概率采样动作
        action = np.random.choice(self.k, p=self.action_probs)
        return action

    def update(self, action, reward):
        """更新偏好值"""
        self.t += 1

        # 基线偏差
        baseline = reward - self.avg_reward

        # 更新选中动作的偏好
        self.preferences[action] += self.alpha * baseline * (1 - self.action_probs[action])

        # 更新其他动作的偏好
        for a in range(self.k):
            if a != action:
                self.preferences[a] -= self.alpha * baseline * self.action_probs[a]

        # 更新平均奖励（基线）
        self.avg_reward += (reward - self.avg_reward) / self.t

    def get_reward(self, action):
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
    print("测试梯度老虎机算法 [解答版本]")
    print("=" * 60)

    np.random.seed(42)

    n_runs = 100
    avg_rewards = []
    optimal_action_pcts = []

    print(f"\n运行 {n_runs} 次实验...")

    for run in range(n_runs):
        result = run_experiment(alpha=0.1, steps=2000, k_arms=10)
        avg_rewards.append(result['avg_reward'])
        optimal_action_pcts.append(result['optimal_action_pct'])

    final_avg_reward = np.mean(avg_rewards)
    final_optimal_pct = np.mean(optimal_action_pcts)

    print(f"\n结果:")
    print(f"  平均奖励: {final_avg_reward:.4f}")
    print(f"  最优动作选择率: {final_optimal_pct:.2%}")

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

    print(f"\n✅ 解答说明:")
    print(f"  1. softmax(): exp(H)/Σexp(H)，数值稳定处理")
    print(f"  2. select_action(): 按softmax概率采样")
    print(f"  3. update(): 梯度上升，使用基线减少方差")
    print(f"  4. H(A) += α(R-R̄)(1-π(A)), H(a) -= α(R-R̄)π(a)")
