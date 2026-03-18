"""
练习: 汤普森采样 (Thompson Sampling)

算法描述:
Thompson Sampling是一种基于贝叶斯方法的探索策略，也称为后验采样。
它通过维护每个动作奖励分布的后验分布，并从后验中采样来选择动作。

核心思想:
- 对每个动作维护一个奖励分布的后验
- 每次从后验中采样，选择采样值最大的动作
- 根据观察到的奖励更新后验分布
- 天然地平衡探索与利用

对于伯努利赌博机（奖励为0或1）：
- 使用Beta分布作为先验和后验: Beta(α, β)
- 观察到成功（r=1）: α ← α+1
- 观察到失败（r=0）: β ← β+1

优点:
- 理论保证（贝叶斯最优）
- 不需要调参
- 探索效率高
- 适应非平稳问题

伪代码:
┌────────────────────────────────────────────────────┐
│ 初始化:                                            │
│   对所有 a, α(a) ← 1, β(a) ← 1                     │
│                                                    │
│ 循环每一步 t:                                      │
│   对所有 a:                                        │
│     从 Beta(α(a), β(a)) 采样得到 θ(a)              │
│   A ← argmax_a θ(a)                                │
│   R ← 执行动作 A 得到的奖励                        │
│                                                    │
│   如果 R = 1:                                      │
│     α(A) ← α(A) + 1                                │
│   否则:                                            │
│     β(A) ← β(A) + 1                                │
└────────────────────────────────────────────────────┘

要求:
- 实现Thompson Sampling
- 使用Beta分布
- 观察贝叶斯探索的效果
- 平均奖励应达到 1.2 ~ 1.6

参考: Thompson (1933), Russo et al. (2018) "A Tutorial on Thompson Sampling"
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
        # TODO: 初始化为Beta(1,1)，即均匀分布
        self.alpha = None  # TODO: 修改这一行
        self.beta = None   # TODO: 修改这一行

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
        # TODO: 实现Thompson Sampling动作选择
        # 提示1: 从每个动作的Beta后验中采样
        #   theta_samples = np.random.beta(self.alpha, self.beta)
        # 提示2: 选择采样值最大的动作
        #   action = np.argmax(theta_samples)
        # 提示3: return action

        pass  # TODO: 删除这一行，填写你的代码

    def update(self, action, reward):
        """
        更新后验分布

        Args:
            action: 执行的动作
            reward: 获得的奖励（0或1）
        """
        # TODO: 实现Beta分布的贝叶斯更新
        # 提示1: if reward == 1:
        #          self.alpha[action] += 1  # 观察到成功
        # 提示2: else:
        #          self.beta[action] += 1   # 观察到失败

        pass  # TODO: 删除这一行，填写你的代码

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
    print("测试Thompson Sampling")
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

    print(f"\n提示:")
    print(f"  - Thompson Sampling是贝叶斯最优策略")
    print(f"  - 通过采样自然地平衡探索与利用")
    print(f"  - 不需要调整超参数（如ε或c）")
    print(f"  - 后验分布反映了我们对每个动作的不确定性")
    print(f"\n理论:")
    print(f"  - Beta(α,β)的均值 = α/(α+β)")
    print(f"  - 方差随着观测增多而减小")
    print(f"  - 自适应探索：不确定性高的动作更可能被选择")
