"""
练习: 策略评估 (Iterative Policy Evaluation)

算法描述:
策略评估用于计算给定策略 π 的状态值函数 v_π(s)。
通过迭代应用 Bellman 期望方程，直到值函数收敛。

Bellman 期望方程:
    v_π(s) = Σ_a π(a|s) Σ_{s',r} p(s',r|s,a) [r + γ v_π(s')]

伪代码:
┌────────────────────────────────────────────────────┐
│ 输入: 策略 π, 折扣因子 γ, 阈值 θ                   │
│ 初始化: V(s) = 0 对所有 s ∈ S                      │
│                                                    │
│ 循环:                                              │
│   Δ ← 0                                            │
│   对每个状态 s ∈ S:                                │
│     v ← V(s)                                       │
│     V(s) ← Σ_a π(a|s) Σ_{s',r} p(s',r|s,a)[r+γV(s')]│
│     Δ ← max(Δ, |v - V(s)|)                         │
│ 直到 Δ < θ                                         │
│                                                    │
│ 输出: V ≈ v_π                                      │
└────────────────────────────────────────────────────┘

本练习使用 GridWorld 环境:
- 4x4 网格
- 左上角和右下角是终止状态
- 每步奖励 -1
- 四个动作: 上、下、左、右
- 撞墙则留在原地

要求:
- 实现迭代策略评估
- 使用均匀随机策略（每个动作概率 0.25）
- 收敛阈值 θ = 0.01
- 折扣因子 γ = 1.0

参考: Sutton & Barto 第4章, 第4.1节, 示例4.1
"""

import numpy as np


class GridWorld:
    """4x4 GridWorld 环境"""

    def __init__(self, size=4):
        self.size = size
        self.n_states = size * size

        # 终止状态: 左上角(0,0)和右下角(3,3)
        self.terminal_states = {0, self.n_states - 1}

        # 动作: 0=上, 1=下, 2=左, 3=右
        self.n_actions = 4
        self.actions = [(- 1, 0), (1, 0), (0, -1), (0, 1)]

    def state_to_pos(self, state):
        """状态索引转坐标"""
        return state // self.size, state % self.size

    def pos_to_state(self, row, col):
        """坐标转状态索引"""
        return row * self.size + col

    def is_terminal(self, state):
        """判断是否为终止状态"""
        return state in self.terminal_states

    def step(self, state, action):
        """
        执行动作，返回下一状态和奖励

        Args:
            state: 当前状态
            action: 动作 (0-3)

        Returns:
            next_state: 下一状态
            reward: 奖励
        """
        if self.is_terminal(state):
            return state, 0

        row, col = self.state_to_pos(state)
        d_row, d_col = self.actions[action]

        # 计算新位置
        new_row = max(0, min(self.size - 1, row + d_row))
        new_col = max(0, min(self.size - 1, col + d_col))

        next_state = self.pos_to_state(new_row, new_col)
        reward = -1  # 每步奖励 -1

        return next_state, reward


def policy_evaluation(env, policy, gamma=1.0, theta=0.01):
    """
    迭代策略评估

    Args:
        env: 环境
        policy: 策略 policy[s, a] = π(a|s)
        gamma: 折扣因子
        theta: 收敛阈值

    Returns:
        V: 状态值函数
    """
    # 初始化值函数
    V = np.zeros(env.n_states)

    iteration = 0

    # TODO: 实现策略评估循环
    # 提示1: 使用 while True 循环
    # 提示2: 在每次迭代中:
    #   - 初始化 delta = 0
    #   - 对每个非终止状态 s:
    #       - 保存旧值 v = V[s]
    #       - 计算新值: V[s] = Σ_a π(a|s) Σ_{s',r} p(s',r|s,a)[r + γV(s')]
    #         即: for a in range(env.n_actions):
    #               next_s, reward = env.step(s, a)
    #               V[s] += policy[s, a] * (reward + gamma * V[next_s])
    #       - 更新 delta = max(delta, |v - V[s]|)
    #   - 如果 delta < theta，break
    # 提示3: 记得先将 V[s] 清零再累加

    pass  # TODO: 删除这一行，实现策略评估

    print(f"策略评估收敛，迭代次数: {iteration}")
    return V


def test():
    """测试函数"""
    print("=" * 60)
    print("测试策略评估 - GridWorld")
    print("=" * 60)

    env = GridWorld(size=4)

    # 创建均匀随机策略
    policy = np.ones((env.n_states, env.n_actions)) / env.n_actions

    print(f"\n环境: {env.size}x{env.size} GridWorld")
    print(f"终止状态: {env.terminal_states}")
    print(f"策略: 均匀随机 (每个动作概率 0.25)")
    print(f"折扣因子: γ = 1.0")
    print(f"收敛阈值: θ = 0.01")
    print(f"\n开始策略评估...")

    # 运行策略评估
    V = policy_evaluation(env, policy, gamma=1.0, theta=0.01)

    # 打印值函数
    print(f"\n值函数 (4x4 网格):")
    print("=" * 40)
    V_grid = V.reshape(env.size, env.size)
    for row in range(env.size):
        for col in range(env.size):
            print(f"{V_grid[row, col]:7.2f}", end=" ")
        print()
    print("=" * 40)

    # 期望结果（参考书中图4.1）
    expected_V = np.array([
        [0, -14, -20, -22],
        [-14, -18, -20, -20],
        [-20, -20, -18, -14],
        [-22, -20, -14, 0]
    ])

    # 验证
    error = np.max(np.abs(V_grid - expected_V))
    print(f"\n与期望值的最大误差: {error:.4f}")

    converges = error < 1.0  # 允许一定误差
    value_error_max = error

    return {
        'converges': converges,
        'value_error_max': value_error_max,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n提示:")
    print(f"  - 终止状态的值应该是 0")
    print(f"  - 最差的状态应该在中间位置（离终止状态最远）")
    print(f"  - 值函数应该关于对角线对称")
