"""
练习: n步TD预测 (n-step TD Prediction)

算法描述:
n步TD方法统一了蒙特卡洛和TD方法。它使用未来n步的奖励，
然后自举（bootstrap）到第n步之后的状态值。

核心公式:
n步回报:
    G_t^{(n)} = R_{t+1} + γR_{t+2} + ... + γ^{n-1}R_{t+n} + γ^n V(S_{t+n})

更新规则:
    V(S_t) ← V(S_t) + α[G_t^{(n)} - V(S_t)]

特殊情况:
- n=1: TD(0)
- n=∞: Monte Carlo

伪代码:
┌────────────────────────────────────────────────────┐
│ 输入: 策略 π, 步数 n                               │
│ 初始化: V(s) 任意值，对所有 s ∈ S                  │
│                                                    │
│ 对每个回合:                                        │
│   初始化 S_0                                       │
│   T ← ∞                                            │
│   对 t = 0, 1, 2, ...:                             │
│     if t < T:                                      │
│       执行 A_t ~ π(·|S_t)                          │
│       观察 R_{t+1}, S_{t+1}                        │
│       if S_{t+1} 是终止:                           │
│         T ← t + 1                                  │
│                                                    │
│     τ ← t - n + 1  (τ是要更新的时间步)             │
│     if τ >= 0:                                     │
│       G ← Σ_{i=τ+1}^{min(τ+n,T)} γ^{i-τ-1}R_i     │
│       if τ + n < T:                                │
│         G ← G + γ^n V(S_{τ+n})                     │
│       V(S_τ) ← V(S_τ) + α[G - V(S_τ)]              │
│                                                    │
│     if τ == T - 1:                                 │
│       break                                        │
└────────────────────────────────────────────────────┘

使用 Random Walk 环境:
- 状态: 0, 1, 2, 3, 4, 5, 6 (1-5是非终止，0和6是终止)
- 起始: 状态3
- 动作: 左或右（等概率）
- 奖励: 到达状态6获得+1，其他0
- 真实值: V(i) = i/6 for i=1,2,3,4,5

要求:
- 实现 n步TD预测
- 比较不同 n 值的性能
- 验证收敛性

参考: Sutton & Barto 第7章, 第7.1节
"""

import numpy as np


class RandomWalk:
    """随机游走环境"""

    def __init__(self, n_states=7):
        """
        初始化

        Args:
            n_states: 状态数（包括两个终止状态）
        """
        self.n_states = n_states
        self.start_state = n_states // 2  # 中间状态

    def reset(self):
        """重置环境"""
        self.state = self.start_state
        return self.state

    def step(self, action):
        """
        执行动作

        Args:
            action: 0=左, 1=右

        Returns:
            next_state, reward, done
        """
        if action == 0:  # 左
            self.state -= 1
        else:  # 右
            self.state += 1

        # 检查终止
        if self.state == 0:
            return self.state, 0, True  # 左边终止
        elif self.state == self.n_states - 1:
            return self.state, 1, True  # 右边终止，奖励+1
        else:
            return self.state, 0, False


def random_policy():
    """随机策略：等概率选择左或右"""
    return np.random.randint(0, 2)


def n_step_td_prediction(env, n=1, episodes=100, alpha=0.1, gamma=1.0):
    """
    n步TD预测

    Args:
        env: 环境
        n: 步数
        episodes: 回合数
        alpha: 学习率
        gamma: 折扣因子

    Returns:
        V: 学习到的状态值函数
    """
    # 初始化值函数
    V = np.zeros(env.n_states)

    # TODO: 实现 n步TD预测
    # 提示1: for episode in range(episodes):
    # 提示2:   state = env.reset()
    # 提示3:   # 存储状态、奖励序列
    # 提示4:   states = [state]
    # 提示5:   rewards = [0]  # R_0 不存在，占位
    # 提示6:   T = float('inf')  # 终止时间
    # 提示7:   t = 0
    # 提示8:   while True:
    # 提示9:     if t < T:
    # 提示10:      # 采取动作
    # 提示11:      action = random_policy()
    # 提示12:      next_state, reward, done = env.step(action)
    # 提示13:      states.append(next_state)
    # 提示14:      rewards.append(reward)
    # 提示15:      if done:
    # 提示16:        T = t + 1
    # 提示17:
    # 提示18:    # 更新时间步 τ = t - n + 1
    # 提示19:    tau = t - n + 1
    # 提示20:    if tau >= 0:
    # 提示21:      # 计算 n步回报 G
    # 提示22:      G = 0.0
    # 提示23:      for i in range(tau + 1, min(tau + n, T) + 1):
    # 提示24:        G += (gamma ** (i - tau - 1)) * rewards[i]
    # 提示25:      # 如果未到终止，加上自举项
    # 提示26:      if tau + n < T:
    # 提示27:        G += (gamma ** n) * V[states[tau + n]]
    # 提示28:      # 更新值函数
    # 提示29:      V[states[tau]] += alpha * (G - V[states[tau]])
    # 提示30:
    # 提示31:    if tau == T - 1:
    # 提示32:      break
    # 提示33:    t += 1

    pass  # TODO: 删除这一行，实现 n步TD

    return V


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 n步TD预测 - Random Walk")
    print("=" * 60)

    np.random.seed(42)

    env = RandomWalk(n_states=7)

    # 真实值函数
    true_V = np.array([0, 1/6, 2/6, 3/6, 4/6, 5/6, 0])

    print(f"\n环境: Random Walk (7状态)")
    print(f"真实值函数: {true_V}")
    print(f"\n测试不同的 n 值...")

    # 测试不同 n
    n_values = [1, 2, 4, 8]
    errors = {}

    for n in n_values:
        print(f"\nn = {n}:")
        V = n_step_td_prediction(env, n=n, episodes=100, alpha=0.1, gamma=1.0)

        error = np.sqrt(np.mean((V - true_V) ** 2))
        errors[n] = error

        print(f"  学习值: {V}")
        print(f"  RMSE: {error:.4f}")

    # 找出最佳 n
    best_n = min(errors, key=errors.get)
    print(f"\n最佳 n: {best_n}, RMSE: {errors[best_n]:.4f}")

    # 验证
    converges = errors[best_n] < 0.3
    value_error_max = errors[best_n]

    return {
        'converges': converges,
        'value_error_max': value_error_max,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n提示:")
    print(f"  - n=1 是 TD(0), n=∞ 是 MC")
    print(f"  - 中等的 n 通常表现最好")
    print(f"  - n 越大，更新延迟越长，但方差越小")
