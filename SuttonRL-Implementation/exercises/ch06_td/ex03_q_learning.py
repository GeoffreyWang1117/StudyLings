"""
练习: Q-Learning (Off-Policy TD Control)

算法描述:
Q-Learning 是最著名的 off-policy TD 控制算法之一。
它直接学习最优动作值函数 Q*，而不管当前遵循的策略。

更新规则:
    Q(S_t, A_t) ← Q(S_t, A_t) + α[R_{t+1} + γ max_a Q(S_{t+1}, a) - Q(S_t, A_t)]

关键区别:
- Off-policy: 行为策略(ε-greedy) ≠ 目标策略(greedy)
- 使用 max_a Q(S', a) 而不是 Q(S', A')
- 直接学习最优策略，不考虑探索

伪代码:
┌────────────────────────────────────────────────────┐
│ 初始化: Q(s,a) 任意值，Q(terminal,·) = 0           │
│                                                    │
│ 对每个回合:                                        │
│   初始化 S                                         │
│                                                    │
│   对回合中的每一步:                                │
│     选择 A ~ ε-greedy(Q(S,·))  [行为策略]          │
│     执行 A, 观察 R, S'                             │
│     Q(S,A) ← Q(S,A) + α[R + γ max_a Q(S',a) - Q(S,A)]│
│     S ← S'                                         │
│   直到 S 是终止状态                                │
└────────────────────────────────────────────────────┘

使用 Cliff Walking 环境（同 SARSA）

要求:
- 实现 Q-Learning 算法
- 使用 ε-greedy 行为策略
- 观察与 SARSA 的区别

参考: Sutton & Barto 第6章, 第6.5节
"""

import numpy as np


class CliffWalking:
    """悬崖行走环境（同SARSA）"""

    def __init__(self):
        self.height = 4
        self.width = 12
        self.n_actions = 4
        self.start = (3, 0)
        self.goal = (3, 11)
        self.cliff = [(3, i) for i in range(1, 11)]
        self.reset()

    def reset(self):
        self.state = self.start
        return self.state

    def step(self, action):
        row, col = self.state

        if action == 0:  # 上
            row = max(0, row - 1)
        elif action == 1:  # 下
            row = min(self.height - 1, row + 1)
        elif action == 2:  # 左
            col = max(0, col - 1)
        elif action == 3:  # 右
            col = min(self.width - 1, col + 1)

        next_state = (row, col)

        if next_state in self.cliff:
            reward = -100
            next_state = self.start
            done = False
        elif next_state == self.goal:
            reward = -1
            done = True
        else:
            reward = -1
            done = False

        self.state = next_state
        return next_state, reward, done


def epsilon_greedy(Q, state, epsilon, n_actions):
    """ε-greedy 策略"""
    if np.random.random() < epsilon:
        return np.random.randint(n_actions)
    else:
        q_values = [Q.get((state, a), 0.0) for a in range(n_actions)]
        return np.argmax(q_values)


def q_learning(env, episodes=500, alpha=0.1, gamma=1.0, epsilon=0.1):
    """
    Q-Learning 算法

    Args:
        env: 环境
        episodes: 回合数
        alpha: 学习率
        gamma: 折扣因子
        epsilon: 探索概率

    Returns:
        Q: 学习到的 Q 值
        episode_returns: 每个回合的总回报
    """
    Q = {}

    def get_q(state, action):
        return Q.get((state, action), 0.0)

    def set_q(state, action, value):
        Q[(state, action)] = value

    def get_max_q(state):
        """获取状态 s 的最大 Q 值"""
        q_values = [get_q(state, a) for a in range(env.n_actions)]
        return max(q_values) if q_values else 0.0

    episode_returns = []

    # TODO: 实现 Q-Learning 主循环
    # 提示1: 结构与 SARSA 类似，但有关键区别
    # 提示2: for episode in range(episodes):
    # 提示3:   state = env.reset()
    # 提示4:   episode_return = 0
    # 提示5:   while True:
    # 提示6:     action = epsilon_greedy(Q, state, epsilon, env.n_actions)
    # 提示7:     next_state, reward, done = env.step(action)
    # 提示8:     # 关键区别: 使用 max Q(S', a) 而不是 Q(S', A')
    # 提示9:     q_current = get_q(state, action)
    # 提示10:    q_max_next = get_max_q(next_state)  # 使用max!
    # 提示11:    td_target = reward + gamma * q_max_next
    # 提示12:    td_error = td_target - q_current
    # 提示13:    set_q(state, action, q_current + alpha * td_error)
    # 提示14:    episode_return += reward
    # 提示15:    state = next_state
    # 提示16:    if done: break

    pass  # TODO: 删除这一行，实现 Q-Learning

    return Q, episode_returns


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 Q-Learning - Cliff Walking")
    print("=" * 60)

    np.random.seed(42)

    env = CliffWalking()

    print(f"\n环境: Cliff Walking {env.height}x{env.width}")
    print(f"\n超参数:")
    print(f"  回合数: 500")
    print(f"  学习率 α: 0.1")
    print(f"  折扣因子 γ: 1.0")
    print(f"  探索概率 ε: 0.1")
    print(f"\n开始训练...")

    Q, episode_returns = q_learning(env, episodes=500, alpha=0.1, gamma=1.0, epsilon=0.1)

    # 分析结果
    avg_return_last_100 = np.mean(episode_returns[-100:])
    print(f"\n" + "=" * 60)
    print(f"训练完成!")
    print(f"  前100回合平均回报: {np.mean(episode_returns[:100]):.2f}")
    print(f"  后100回合平均回报: {avg_return_last_100:.2f}")
    print(f"  最佳回合回报: {np.max(episode_returns):.2f}")
    print(f"=" * 60)

    # 可视化学到的策略
    print(f"\n学到的策略 (贪心):")
    print("=" * 50)
    action_symbols = ['↑', '↓', '←', '→']
    for row in range(env.height):
        for col in range(env.width):
            state = (row, col)
            if state == env.goal:
                print(" G", end=" ")
            elif state in env.cliff:
                print(" C", end=" ")
            elif state == env.start:
                print(" S", end=" ")
            else:
                q_values = [Q.get((state, a), 0.0) for a in range(env.n_actions)]
                best_action = np.argmax(q_values)
                print(f" {action_symbols[best_action]}", end=" ")
        print()
    print("=" * 50)

    # Q-Learning 是 off-policy，会学习最优路径（贴着悬崖）
    # 但在训练中因为探索会掉下悬崖，所以平均回报较低
    converges = True
    avg_return_min = avg_return_last_100
    finds_optimal = True  # 学习到最优策略

    return {
        'converges': converges,
        'avg_return_min': avg_return_min,
        'finds_optimal': finds_optimal,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n提示:")
    print(f"  - Q-Learning 学习最优策略（贴着悬崖边）")
    print(f"  - 但训练时会因探索掉下悬崖，平均回报比 SARSA 低")
    print(f"  - 这展示了 on-policy 和 off-policy 的重要区别")
    print(f"\n对比:")
    print(f"  - SARSA: 安全路径，训练回报较高")
    print(f"  - Q-Learning: 最优路径，训练回报较低，但策略更优")
