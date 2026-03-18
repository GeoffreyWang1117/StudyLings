"""
练习: Double Q-Learning

算法描述:
Double Q-Learning通过维护两个独立的Q值函数来解决Q-learning的最大化偏差问题。
这是一个重要的改进，被广泛应用于现代深度RL（如Double DQN）。

问题背景：
Q-learning的更新: Q(S,A) ← Q(S,A) + α[R + γ max_a Q(S',a) - Q(S,A)]
使用同一个Q值来选择和评估动作会导致过估计（overestimation）

Double Q-Learning的解决方案:
- 维护两个Q值函数: Q1和Q2
- 使用Q1选择动作，用Q2评估
- 或者反过来，随机决定

核心思想:
- Q1选择最佳动作: A* = argmax_a Q1(S',a)
- Q2评估该动作: Q2(S',A*)
- 解耦选择和评估，减少过估计偏差

伪代码:
┌────────────────────────────────────────────────────┐
│ 初始化: Q1(s,a), Q2(s,a) 任意值                    │
│        Q1(terminal,·) = Q2(terminal,·) = 0         │
│                                                    │
│ 循环（对每个回合）:                                │
│   初始化 S                                         │
│   循环（对回合中的每一步）:                        │
│     A ← ε-greedy(Q1 + Q2)  [使用两者的和]          │
│     执行 A，观察 R, S'                             │
│                                                    │
│     以0.5概率:                                     │
│       A* ← argmax_a Q1(S',a)                       │
│       Q1(S,A) ← Q1(S,A) + α[R+γQ2(S',A*)-Q1(S,A)]  │
│     否则:                                          │
│       A* ← argmax_a Q2(S',a)                       │
│       Q2(S,A) ← Q2(S,A) + α[R+γQ1(S',A*)-Q2(S,A)]  │
│                                                    │
│     S ← S'                                         │
│   直到 S 是终止状态                                │
└────────────────────────────────────────────────────┘

使用 Maximization Bias 示例环境

要求:
- 实现Double Q-Learning
- 观察减少过估计的效果
- 与标准Q-learning对比
- 学习到正确的策略

参考: Hado van Hasselt (2010), Sutton & Barto 第6章
"""

import numpy as np


class MaxBiasEnv:
    """
    最大化偏差环境
    
    状态A: 可以选择左（到终止）或右（到状态B）
    状态B: 有多个动作，奖励均值为负但有噪声
    
    最优策略应该选择左（确定的0），而不是右（期望为负）
    但Q-learning由于过估计可能错误地选择右
    """

    def __init__(self, n_actions_B=10):
        """
        初始化

        Args:
            n_actions_B: 状态B的动作数量
        """
        self.n_actions_B = n_actions_B
        self.n_states = 3  # A, B, Terminal
        
        self.state_A = 0
        self.state_B = 1
        self.terminal = 2

    def reset(self):
        """重置到状态A"""
        self.state = self.state_A
        return self.state

    def step(self, action):
        """
        执行动作

        状态A:
          action=0 (左): 到终止，奖励0
          action=1 (右): 到B，奖励0
        
        状态B:
          任何动作: 到终止，奖励 N(-0.1, 1.0)
        
        Returns:
            next_state, reward, done
        """
        if self.state == self.state_A:
            if action == 0:  # 左：到终止
                return self.terminal, 0, True
            else:  # 右：到B
                self.state = self.state_B
                return self.state, 0, False
        
        elif self.state == self.state_B:
            # 任何动作都到终止，奖励有噪声且期望为负
            reward = np.random.normal(-0.1, 1.0)
            return self.terminal, reward, True
        
        else:  # terminal
            return self.terminal, 0, True


def double_q_learning(env, episodes=300, alpha=0.1, gamma=1.0, epsilon=0.1):
    """
    Double Q-Learning算法

    Args:
        env: 环境
        episodes: 回合数
        alpha: 学习率
        gamma: 折扣因子
        epsilon: 探索率

    Returns:
        Q1, Q2: 两个Q值函数
        left_action_pct: 在状态A选择左动作的百分比（应该接近100%）
    """
    # 初始化两个Q值函数
    # 状态A有2个动作（左、右），状态B有n_actions_B个动作
    max_actions = max(2, env.n_actions_B)
    Q1 = np.zeros((env.n_states, max_actions))
    Q2 = np.zeros((env.n_states, max_actions))

    left_actions = []

    # TODO: 实现Double Q-Learning主循环
    # 提示1: for episode in range(episodes):
    # 提示2:   state = env.reset()
    # 提示3:   done = False
    # 提示4:
    # 提示5:   while not done:
    # 提示6:     # 决定可用动作数
    # 提示7:     if state == env.state_A:
    # 提示8:       n_actions = 2
    # 提示9:     elif state == env.state_B:
    # 提示10:      n_actions = env.n_actions_B
    # 提示11:    else:
    # 提示12:      break
    # 提示13:
    # 提示14:    # ε-greedy基于Q1+Q2
    # 提示15:    if np.random.random() < epsilon:
    # 提示16:      action = np.random.randint(n_actions)
    # 提示17:    else:
    # 提示18:      Q_sum = Q1[state, :n_actions] + Q2[state, :n_actions]
    # 提示19:      action = np.argmax(Q_sum)
    # 提示20:
    # 提示21:    # 记录状态A的动作选择
    # 提示22:    if state == env.state_A:
    # 提示23:      left_actions.append(1 if action == 0 else 0)
    # 提示24:
    # 提示25:    next_state, reward, done = env.step(action)
    # 提示26:
    # 提示27:    # 随机选择更新Q1或Q2
    # 提示28:    if np.random.random() < 0.5:
    # 提示29:      # 用Q1选择，Q2评估
    # 提示30:      if not done:
    # 提示31:        best_action = np.argmax(Q1[next_state])
    # 提示32:        td_target = reward + gamma * Q2[next_state, best_action]
    # 提示33:      else:
    # 提示34:        td_target = reward
    # 提示35:      Q1[state, action] += alpha * (td_target - Q1[state, action])
    # 提示36:    else:
    # 提示37:      # 用Q2选择，Q1评估
    # 提示38:      if not done:
    # 提示39:        best_action = np.argmax(Q2[next_state])
    # 提示40:        td_target = reward + gamma * Q1[next_state, best_action]
    # 提示41:      else:
    # 提示42:        td_target = reward
    # 提示43:      Q2[state, action] += alpha * (td_target - Q2[state, action])
    # 提示44:
    # 提示45:    state = next_state

    pass  # TODO: 删除这一行

    left_action_pct = np.mean(left_actions) if left_actions else 0

    return Q1, Q2, left_action_pct


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 Double Q-Learning - Maximization Bias")
    print("=" * 60)

    np.random.seed(42)

    env = MaxBiasEnv(n_actions_B=10)

    print(f"\n环境说明:")
    print(f"  状态A: 可选左（奖励0）或右（到状态B）")
    print(f"  状态B: {env.n_actions_B}个动作，奖励 N(-0.1, 1.0)")
    print(f"  最优策略: 在A选择左（期望0 > -0.1）")

    print(f"\n开始训练 (300回合)...")

    Q1, Q2, left_pct = double_q_learning(env, episodes=300, alpha=0.1, epsilon=0.1)

    print(f"\n训练完成!")
    print(f"  在状态A选择左的比例: {left_pct:.1%}")

    # 显示Q值
    Q_avg = (Q1 + Q2) / 2
    print(f"\nQ值（平均）:")
    print(f"  状态A, 动作左: {Q_avg[env.state_A, 0]:.3f}")
    print(f"  状态A, 动作右: {Q_avg[env.state_A, 1]:.3f}")
    print(f"  状态B, 最大Q值: {np.max(Q_avg[env.state_B]):.3f}")

    # 验证
    learns_correct = left_pct > 0.5

    return {
        'left_action_pct': left_pct,
        'learns_correct': learns_correct,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n提示:")
    print(f"  - Double Q-Learning减少过估计偏差")
    print(f"  - 解耦动作选择和评估")
    print(f"  - 应该学会在A选择左（安全选项）")
    print(f"  - 标准Q-learning可能错误选择右（过估计B的值）")
    print(f"\n应用:")
    print(f"  - Double DQN (2015): 将此思想应用于深度RL")
    print(f"  - 2025年几乎所有DQN变体都使用此技术")
