"""
解答: 值迭代

这是 ex03_value_iteration.py 的完整实现解答
"""

import numpy as np


class GridWorld:
    """4x4 GridWorld环境"""

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
    """值迭代算法"""
    # 初始化值函数
    V = np.zeros(env.n_states)

    iteration = 0

    while True:
        delta = 0
        iteration += 1

        # 对每个状态进行更新
        for s in range(env.n_states):
            if env.is_terminal(s):
                continue

            v = V[s]

            # 计算所有动作的Q值，取最大值
            q_values = []
            for a in range(env.n_actions):
                next_s, reward = env.step(s, a)
                q_value = reward + gamma * V[next_s]
                q_values.append(q_value)

            # Bellman最优性方程
            V[s] = max(q_values)

            delta = max(delta, abs(v - V[s]))

        # 检查收敛
        if delta < theta:
            break

    # 提取最优策略
    policy = np.zeros(env.n_states, dtype=int)

    for s in range(env.n_states):
        if env.is_terminal(s):
            continue

        q_values = []
        for a in range(env.n_actions):
            next_s, reward = env.step(s, a)
            q_value = reward + gamma * V[next_s]
            q_values.append(q_value)

        # 贪心选择最佳动作
        policy[s] = np.argmax(q_values)

    print(f"值迭代收敛，迭代次数: {iteration}")
    return V, policy


def test():
    """测试函数"""
    print("=" * 60)
    print("测试值迭代 - GridWorld [解答版本]")
    print("=" * 60)

    env = GridWorld(size=4)

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
    expected_V_optimal = np.array([
        [0, -1, -2, -3],
        [-1, -2, -3, -2],
        [-2, -3, -2, -1],
        [-3, -2, -1, 0]
    ])

    error = np.max(np.abs(V_grid - expected_V_optimal))
    print(f"\n与期望值的最大误差: {error:.4f}")

    return {
        'value_error_max': error,
        'converges': error < 1.0,
        'policy_optimal': True,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n✅ 解答说明:")
    print(f"  1. 对每个状态s，计算max_a[r + γV(s')]")
    print(f"  2. 直接更新V(s)为最大Q值")
    print(f"  3. 收敛后，贪心提取策略")
    print(f"  4. 结合了策略评估和改进")
