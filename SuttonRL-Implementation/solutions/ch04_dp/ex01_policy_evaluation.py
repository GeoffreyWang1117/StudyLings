"""
解答: 策略评估 (Policy Evaluation)

这是 ex01_policy_evaluation.py 的完整实现解答
"""

import numpy as np


class GridWorld:
    """4x4 GridWorld 环境"""

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


def policy_evaluation(env, policy, gamma=1.0, theta=0.01):
    """
    迭代策略评估

    应用 Bellman 期望方程直到收敛:
    V(s) ← Σ_a π(a|s) Σ_{s',r} p(s',r|s,a)[r + γV(s')]
    """
    # 初始化值函数
    V = np.zeros(env.n_states)

    iteration = 0

    while True:
        delta = 0
        iteration += 1

        # 对每个状态进行更新
        for s in range(env.n_states):
            # 跳过终止状态
            if env.is_terminal(s):
                continue

            # 保存旧值
            v = V[s]

            # 计算新值
            V[s] = 0
            for a in range(env.n_actions):
                # 获取转移
                next_s, reward = env.step(s, a)

                # 期望：Σ_a π(a|s) * [r + γV(s')]
                V[s] += policy[s, a] * (reward + gamma * V[next_s])

            # 更新最大变化
            delta = max(delta, abs(v - V[s]))

        # 检查收敛
        if delta < theta:
            break

    print(f"策略评估收敛，迭代次数: {iteration}")
    return V


def test():
    """测试函数"""
    print("=" * 60)
    print("测试策略评估 - GridWorld [解答版本]")
    print("=" * 60)

    env = GridWorld(size=4)

    # 创建均匀随机策略
    policy = np.ones((env.n_states, env.n_actions)) / env.n_actions

    print(f"\n开始策略评估...")

    V = policy_evaluation(env, policy, gamma=1.0, theta=0.01)

    # 打印值函数
    print(f"\n值函数:")
    print("=" * 40)
    V_grid = V.reshape(env.size, env.size)
    for row in range(env.size):
        for col in range(env.size):
            print(f"{V_grid[row, col]:7.2f}", end=" ")
        print()
    print("=" * 40)

    # 期望结果
    expected_V = np.array([
        [0, -14, -20, -22],
        [-14, -18, -20, -20],
        [-20, -20, -18, -14],
        [-22, -20, -14, 0]
    ])

    error = np.max(np.abs(V_grid - expected_V))
    print(f"\n与期望值的最大误差: {error:.4f}")

    return {
        'converges': error < 1.0,
        'value_error_max': error,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n✅ 解答说明:")
    print(f"  1. 初始化V(s)=0")
    print(f"  2. 对每个状态s:")
    print(f"     V(s) = Σ_a π(a|s) [r + γV(s')]")
    print(f"  3. 重复直到 max|V_new - V_old| < θ")
    print(f"  4. 注意终止状态值保持为0")
