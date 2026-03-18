"""
练习: 策略迭代 (Policy Iteration)

算法描述:
策略迭代是动态规划的核心算法之一。它通过策略评估和策略改进的交替迭代来找到最优策略。
相比值迭代，策略迭代通常收敛更快，但每次迭代成本更高。

核心思想:
1. 策略评估: 计算当前策略π的值函数V^π
2. 策略改进: 对每个状态，贪心选择最佳动作

算法保证:
- 每次策略改进都至少和之前一样好（策略改进定理）
- 在有限MDP中，有限步内收敛到最优策略

伪代码:
┌────────────────────────────────────────────────────┐
│ 1. 初始化:                                         │
│    V(s) ∈ ℝ, π(s) ∈ A(s) 任意，对所有 s ∈ S       │
│                                                    │
│ 2. 策略评估:                                       │
│    循环:                                           │
│      Δ ← 0                                         │
│      对每个 s ∈ S:                                 │
│        v ← V(s)                                    │
│        V(s) ← Σ_{s',r} p(s',r|s,π(s))[r+γV(s')]   │
│        Δ ← max(Δ, |v - V(s)|)                      │
│    直到 Δ < θ                                      │
│                                                    │
│ 3. 策略改进:                                       │
│    policy-stable ← true                            │
│    对每个 s ∈ S:                                   │
│      old-action ← π(s)                             │
│      π(s) ← argmax_a Σ p(s',r|s,a)[r+γV(s')]      │
│      if old-action ≠ π(s):                         │
│        policy-stable ← false                       │
│                                                    │
│ 4. 如果 policy-stable, 停止并返回 V ≈ V*, π ≈ π*  │
│    否则跳到步骤2                                   │
└────────────────────────────────────────────────────┘

使用 Gridworld 环境

要求:
- 实现完整的策略迭代算法
- 包含策略评估和策略改进
- 观察策略迭代的快速收敛
- 与值迭代对比迭代次数

参考: Sutton & Barto 第4章, 第4.3节
"""

import numpy as np


class GridWorld:
    """GridWorld环境（4x4网格）"""

    def __init__(self, size=4):
        """
        初始化

        Args:
            size: 网格大小
        """
        self.size = size
        self.n_states = size * size
        self.n_actions = 4  # 上下左右

        # 终止状态
        self.terminal_states = [0, self.n_states - 1]

    def is_terminal(self, state):
        """判断是否为终止状态"""
        return state in self.terminal_states

    def step(self, state, action):
        """
        确定性状态转移

        Args:
            state: 当前状态
            action: 动作 (0=上, 1=下, 2=左, 3=右)

        Returns:
            next_state: 下一状态
            reward: 奖励
        """
        if self.is_terminal(state):
            return state, 0

        row = state // self.size
        col = state % self.size

        # 执行动作
        if action == 0:  # 上
            row = max(row - 1, 0)
        elif action == 1:  # 下
            row = min(row + 1, self.size - 1)
        elif action == 2:  # 左
            col = max(col - 1, 0)
        elif action == 3:  # 右
            col = min(col + 1, self.size - 1)

        next_state = row * self.size + col
        reward = -1  # 每步奖励-1（鼓励快速到达终点）

        return next_state, reward


def policy_evaluation(env, policy, V, gamma=1.0, theta=0.01):
    """
    策略评估

    Args:
        env: 环境
        policy: 当前策略（数组，每个状态对应一个动作）
        V: 值函数
        gamma: 折扣因子
        theta: 收敛阈值

    Returns:
        V: 评估后的值函数
    """
    # TODO: 实现策略评估
    # 提示1: while True:
    # 提示2:   delta = 0
    # 提示3:   for s in range(env.n_states):
    # 提示4:     if env.is_terminal(s):
    # 提示5:       continue
    # 提示6:     v = V[s]
    # 提示7:     # 计算新的值函数
    # 提示8:     action = policy[s]
    # 提示9:     next_state, reward = env.step(s, action)
    # 提示10:    V[s] = reward + gamma * V[next_state]
    # 提示11:    delta = max(delta, abs(v - V[s]))
    # 提示12:  if delta < theta:
    # 提示13:    break

    pass  # TODO: 删除这一行

    return V


def policy_improvement(env, V, gamma=1.0):
    """
    策略改进

    Args:
        env: 环境
        V: 当前值函数
        gamma: 折扣因子

    Returns:
        policy: 改进后的策略
        policy_stable: 策略是否稳定
    """
    policy = np.zeros(env.n_states, dtype=int)
    policy_stable = True

    # TODO: 实现策略改进
    # 提示1: for s in range(env.n_states):
    # 提示2:   if env.is_terminal(s):
    # 提示3:     continue
    # 提示4:   # 计算所有动作的值
    # 提示5:   action_values = []
    # 提示6:   for a in range(env.n_actions):
    # 提示7:     next_state, reward = env.step(s, a)
    # 提示8:     action_value = reward + gamma * V[next_state]
    # 提示9:     action_values.append(action_value)
    # 提示10:  # 贪心选择最佳动作
    # 提示11:  best_action = np.argmax(action_values)
    # 提示12:  if policy[s] != best_action:
    # 提示13:    policy_stable = False
    # 提示14:  policy[s] = best_action

    pass  # TODO: 删除这一行

    return policy, policy_stable


def policy_iteration(env, gamma=1.0, theta=0.01):
    """
    策略迭代算法

    Args:
        env: 环境
        gamma: 折扣因子
        theta: 收敛阈值

    Returns:
        V: 最优值函数
        policy: 最优策略
        iterations: 迭代次数
    """
    # 初始化
    V = np.zeros(env.n_states)
    policy = np.random.randint(0, env.n_actions, env.n_states)

    iterations = 0

    # TODO: 实现策略迭代主循环
    # 提示1: while True:
    # 提示2:   iterations += 1
    # 提示3:   # 策略评估
    # 提示4:   V = policy_evaluation(env, policy, V, gamma, theta)
    # 提示5:   # 策略改进
    # 提示6:   policy, policy_stable = policy_improvement(env, V, gamma)
    # 提示7:   # 如果策略稳定，停止
    # 提示8:   if policy_stable:
    # 提示9:     break

    pass  # TODO: 删除这一行

    return V, policy, iterations


def test():
    """测试函数"""
    print("=" * 60)
    print("测试策略迭代 - GridWorld")
    print("=" * 60)

    np.random.seed(42)

    env = GridWorld(size=4)

    print(f"\n环境: 4x4 GridWorld")
    print(f"  起点: 任意")
    print(f"  终点: 左上角(0)和右下角(15)")
    print(f"  每步奖励: -1")

    print(f"\n开始策略迭代...")

    V, policy, iterations = policy_iteration(env, gamma=1.0, theta=0.01)

    print(f"\n收敛!")
    print(f"  迭代次数: {iterations}")

    # 显示值函数
    print(f"\n最优值函数:")
    for row in range(env.size):
        line = ""
        for col in range(env.size):
            state = row * env.size + col
            line += f"{V[state]:6.1f} "
        print(f"  {line}")

    # 显示策略
    print(f"\n最优策略:")
    action_symbols = ['↑', '↓', '←', '→']
    for row in range(env.size):
        line = ""
        for col in range(env.size):
            state = row * env.size + col
            if env.is_terminal(state):
                line += "T "
            else:
                line += action_symbols[policy[state]] + " "
        print(f"  {line}")

    return {
        'iterations': iterations,
        'converges': iterations < 20,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n提示:")
    print(f"  - 策略迭代通常比值迭代收敛更快")
    print(f"  - 但每次迭代需要完整的策略评估（成本更高）")
    print(f"  - 策略改进定理保证每次改进不会变差")
    print(f"  - 有限MDP中保证有限步收敛")
