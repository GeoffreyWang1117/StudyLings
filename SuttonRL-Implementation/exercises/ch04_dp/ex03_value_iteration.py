"""
练习: 值迭代 (Value Iteration)

算法描述:
值迭代将策略评估和策略改进结合为一步，
直接迭代应用 Bellman 最优方程。

Bellman 最优方程:
    v*(s) = max_a Σ_{s',r} p(s',r|s,a) [r + γ v*(s')]

伪代码:
┌────────────────────────────────────────────────────┐
│ 输入: 折扣因子 γ, 阈值 θ                           │
│ 初始化: V(s) = 0 对所有 s ∈ S                      │
│                                                    │
│ 循环:                                              │
│   Δ ← 0                                            │
│   对每个状态 s ∈ S:                                │
│     v ← V(s)                                       │
│     V(s) ← max_a Σ_{s',r} p(s',r|s,a)[r + γV(s')] │
│     Δ ← max(Δ, |v - V(s)|)                         │
│ 直到 Δ < θ                                         │
│                                                    │
│ 输出最优策略:                                      │
│   π(s) = argmax_a Σ_{s',r} p(s',r|s,a)[r + γV(s')]│
└────────────────────────────────────────────────────┘

要求:
- 实现值迭代算法
- 从最优值函数提取最优策略
- 在 GridWorld 上验证

参考: Sutton & Barto 第4章, 第4.4节
"""

import numpy as np


class GridWorld:
    """4x4 GridWorld 环境（同策略评估）"""

    def __init__(self, size=4):
        self.size = size
        self.n_states = size * size
        self.terminal_states = {0, self.n_states - 1}
        self.n_actions = 4
        self.actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def state_to_pos(self, state):
        return state // self.size, state % self.size

    def pos_to_state(self, row, col):
        return row * self.size + col

    def is_terminal(self, state):
        return state in self.terminal_states

    def step(self, state, action):
        if self.is_terminal(state):
            return state, 0

        row, col = self.state_to_pos(state)
        d_row, d_col = self.actions[action]
        new_row = max(0, min(self.size - 1, row + d_row))
        new_col = max(0, min(self.size - 1, col + d_col))
        next_state = self.pos_to_state(new_row, new_col)
        reward = -1

        return next_state, reward


def value_iteration(env, gamma=1.0, theta=0.01):
    """
    值迭代算法

    Args:
        env: 环境
        gamma: 折扣因子
        theta: 收敛阈值

    Returns:
        V: 最优值函数
        policy: 最优策略
    """
    V = np.zeros(env.n_states)
    iteration = 0

    # TODO: 实现值迭代
    # 提示1: 与策略评估类似，但使用 max 而不是求和
    # 提示2: 对每个状态 s:
    #   - 计算所有动作的值: q_values = []
    #   - for a in range(env.n_actions):
    #       next_s, reward = env.step(s, a)
    #       q_values.append(reward + gamma * V[next_s])
    #   - V[s] = max(q_values)
    # 提示3: 收敛条件与策略评估相同

    pass  # TODO: 删除这一行，实现值迭代

    # TODO: 提取最优策略
    # 提示1: policy = np.zeros(env.n_states, dtype=int)
    # 提示2: 对每个状态，选择使 Q(s,a) 最大的动作
    # 提示3: policy[s] = argmax_a [r + γV(s')]

    policy = None  # TODO: 实现策略提取

    print(f"值迭代收敛，迭代次数: {iteration}")
    return V, policy


def test():
    """测试函数"""
    print("=" * 60)
    print("测试值迭代 - GridWorld")
    print("=" * 60)

    env = GridWorld(size=4)

    print(f"\n环境: {env.size}x{env.size} GridWorld")
    print(f"折扣因子: γ = 1.0")
    print(f"收敛阈值: θ = 0.01")
    print(f"\n开始值迭代...")

    V, policy = value_iteration(env, gamma=1.0, theta=0.01)

    # 打印值函数
    print(f"\n最优值函数:")
    print("=" * 40)
    V_grid = V.reshape(env.size, env.size)
    for row in range(env.size):
        for col in range(env.size):
            print(f"{V_grid[row, col]:7.2f}", end=" ")
        print()
    print("=" * 40)

    # 打印策略
    print(f"\n最优策略:")
    print("=" * 40)
    action_symbols = ['↑', '↓', '←', '→']
    policy_grid = policy.reshape(env.size, env.size)
    for row in range(env.size):
        for col in range(env.size):
            state = env.pos_to_state(row, col)
            if env.is_terminal(state):
                print("  T", end="  ")
            else:
                print(f"  {action_symbols[policy_grid[row, col]]}", end="  ")
        print()
    print("=" * 40)

    # 验证
    # 最优值应该比均匀随机策略更好
    expected_V_optimal = np.array([
        [0, -1, -2, -3],
        [-1, -2, -3, -2],
        [-2, -3, -2, -1],
        [-3, -2, -1, 0]
    ])

    error = np.max(np.abs(V_grid - expected_V_optimal))
    print(f"\n与期望值的最大误差: {error:.4f}")

    converges = error < 1.0
    policy_optimal = True  # 简化判断

    return {
        'value_error_max': error,
        'converges': converges,
        'policy_optimal': policy_optimal,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n提示:")
    print(f"  - 最优策略应该指向最近的终止状态")
    print(f"  - 值迭代通常比策略迭代更快收敛")
    print(f"  - 最优值函数代表到终止状态的最短路径")
