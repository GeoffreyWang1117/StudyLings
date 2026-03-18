"""
练习: Expected SARSA

算法描述:
Expected SARSA是SARSA的改进版本，使用期望值而不是采样的下一个动作值。
它比SARSA更稳定，且在某些情况下收敛更快。

核心思想:
- SARSA使用: Q(S,A) ← Q(S,A) + α[R + γQ(S',A') - Q(S,A)]
  其中A'是实际采样的动作
- Expected SARSA使用: Q(S,A) ← Q(S,A) + α[R + γE_π[Q(S',·)] - Q(S,A)]
  其中期望是对所有可能的A'

期望计算（ε-greedy策略）:
E_π[Q(S',a)] = Σ_a π(a|S')Q(S',a)
             = ε/|A| Σ_a Q(S',a) + (1-ε)max_a Q(S',a)

优势:
- 比SARSA方差更小（使用期望而非采样）
- 比Q-learning更稳定（考虑策略分布）
- 可以使用与行为策略不同的目标策略

伪代码:
┌────────────────────────────────────────────────────┐
│ 初始化: Q(s,a) 任意值，Q(terminal,·) = 0           │
│                                                    │
│ 循环（对每个回合）:                                │
│   初始化 S                                         │
│   循环（对回合中的每一步）:                        │
│     用ε-greedy从Q选择动作 A                        │
│     执行 A，观察 R, S'                             │
│                                                    │
│     if S' 是终止:                                  │
│       Q(S,A) ← Q(S,A) + α[R - Q(S,A)]              │
│     else:                                          │
│       V ← Σ_a π(a|S')Q(S',a)  [期望值]             │
│       Q(S,A) ← Q(S,A) + α[R + γV - Q(S,A)]         │
│                                                    │
│     S ← S'                                         │
│   直到 S 是终止状态                                │
└────────────────────────────────────────────────────┘

使用 Cliff Walking 环境

要求:
- 实现Expected SARSA
- 正确计算期望值
- 观察与SARSA/Q-learning的差异
- 平均回报应大于 -100

参考: Sutton & Barto 第6章, 第6.6节
"""

import numpy as np


class CliffWalking:
    """悬崖行走环境"""

    def __init__(self, height=4, width=12):
        """
        初始化

        Args:
            height: 网格高度
            width: 网格宽度
        """
        self.height = height
        self.width = width
        self.n_states = height * width
        self.n_actions = 4  # 上、下、左、右

        # 起点和终点
        self.start = (height - 1, 0)
        self.goal = (height - 1, width - 1)

        # 悬崖位置
        self.cliff = [(height - 1, i) for i in range(1, width - 1)]

    def reset(self):
        """重置环境"""
        self.pos = self.start
        return self._state_index(self.pos)

    def step(self, action):
        """
        执行动作

        Args:
            action: 0=上, 1=下, 2=左, 3=右

        Returns:
            next_state, reward, done
        """
        row, col = self.pos

        # 执行动作
        if action == 0:  # 上
            row = max(0, row - 1)
        elif action == 1:  # 下
            row = min(self.height - 1, row + 1)
        elif action == 2:  # 左
            col = max(0, col - 1)
        elif action == 3:  # 右
            col = min(self.width - 1, col + 1)

        self.pos = (row, col)

        # 检查是否掉下悬崖
        if self.pos in self.cliff:
            return self._state_index(self.start), -100, False

        # 检查是否到达终点
        if self.pos == self.goal:
            return self._state_index(self.pos), -1, True

        # 正常步骤
        return self._state_index(self.pos), -1, False

    def _state_index(self, pos):
        """将位置转换为状态索引"""
        row, col = pos
        return row * self.width + col


def expected_sarsa(env, episodes=500, alpha=0.5, gamma=1.0, epsilon=0.1):
    """
    Expected SARSA算法

    Args:
        env: 环境
        episodes: 回合数
        alpha: 学习率
        gamma: 折扣因子
        epsilon: 探索率

    Returns:
        Q: 学到的动作值函数
        episode_returns: 每回合的总回报
    """
    # 初始化Q值
    Q = np.zeros((env.n_states, env.n_actions))

    episode_returns = []

    # TODO: 实现Expected SARSA主循环
    # 提示1: for episode in range(episodes):
    # 提示2:   state = env.reset()
    # 提示3:   episode_return = 0
    # 提示4:   done = False
    # 提示5:
    # 提示6:   while not done:
    # 提示7:     # ε-greedy动作选择
    # 提示8:     if np.random.random() < epsilon:
    # 提示9:       action = np.random.randint(env.n_actions)
    # 提示10:    else:
    # 提示11:      action = np.argmax(Q[state])
    # 提示12:
    # 提示13:    next_state, reward, done = env.step(action)
    # 提示14:    episode_return += reward
    # 提示15:
    # 提示16:    # 计算期望值
    # 提示17:    if done:
    # 提示18:      expected_q = 0
    # 提示19:    else:
    # 提示20:      # Expected value = Σ_a π(a|s)Q(s,a)
    # 提示21:      # 对ε-greedy: π(a|s) = ε/n + (1-ε)·I(a=argmax)
    # 提示22:      best_action = np.argmax(Q[next_state])
    # 提示23:      expected_q = 0
    # 提示24:      for a in range(env.n_actions):
    # 提示25:        if a == best_action:
    # 提示26:          prob = (1 - epsilon) + epsilon / env.n_actions
    # 提示27:        else:
    # 提示28:          prob = epsilon / env.n_actions
    # 提示29:        expected_q += prob * Q[next_state, a]
    # 提示30:
    # 提示31:    # Expected SARSA更新
    # 提示32:    td_target = reward + gamma * expected_q
    # 提示33:    Q[state, action] += alpha * (td_target - Q[state, action])
    # 提示34:
    # 提示35:    state = next_state
    # 提示36:
    # 提示37:  episode_returns.append(episode_return)

    pass  # TODO: 删除这一行

    return Q, episode_returns


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 Expected SARSA - Cliff Walking")
    print("=" * 60)

    np.random.seed(42)

    env = CliffWalking(height=4, width=12)

    print(f"\n环境: Cliff Walking")
    print(f"  网格: 4x12")
    print(f"  起点: 左下角")
    print(f"  终点: 右下角")
    print(f"  悬崖: 底部中间区域（奖励-100）")

    print(f"\n开始训练 (500回合)...")

    Q, episode_returns = expected_sarsa(env, episodes=500, alpha=0.5, epsilon=0.1)

    # 分析结果
    early_avg = np.mean(episode_returns[:50])
    late_avg = np.mean(episode_returns[-50:])

    print(f"\n训练完成!")
    print(f"  前50回合平均回报: {early_avg:.2f}")
    print(f"  后50回合平均回报: {late_avg:.2f}")
    print(f"  改进: {late_avg - early_avg:.2f}")

    # 显示学到的策略
    print(f"\n学到的策略（选择频率最高的动作）:")
    action_symbols = ['↑', '↓', '←', '→']
    for row in range(env.height):
        line = ""
        for col in range(env.width):
            state = row * env.width + col
            if (row, col) == env.start:
                line += "S "
            elif (row, col) == env.goal:
                line += "G "
            elif (row, col) in env.cliff:
                line += "X "
            else:
                action = np.argmax(Q[state])
                line += action_symbols[action] + " "
        print(f"  {line}")

    return {
        'avg_return': late_avg,
        'improves': late_avg > -100,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n提示:")
    print(f"  - Expected SARSA使用期望而非采样")
    print(f"  - 比SARSA方差更小，更稳定")
    print(f"  - 计算期望需要遍历所有动作")
    print(f"  - 在确定性环境中与Q-learning相同")
    print(f"\n对比:")
    print(f"  - SARSA: 采样A'，使用Q(S',A')")
    print(f"  - Expected SARSA: 使用E[Q(S',·)]")
    print(f"  - Q-learning: 使用max Q(S',·)")
