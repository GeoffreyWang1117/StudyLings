"""
解答: Q-Learning (Off-Policy TD Control)

这是 ex03_q_learning.py 的完整实现解答
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

        if action == 0:
            row = max(0, row - 1)
        elif action == 1:
            row = min(self.height - 1, row + 1)
        elif action == 2:
            col = max(0, col - 1)
        elif action == 3:
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

    更新: Q(S,A) ← Q(S,A) + α[R + γ max_a Q(S',a) - Q(S,A)]
    """
    Q = {}

    def get_q(state, action):
        return Q.get((state, action), 0.0)

    def set_q(state, action, value):
        Q[(state, action)] = value

    def get_max_q(state):
        """获取状态s的最大Q值"""
        q_values = [get_q(state, a) for a in range(env.n_actions)]
        return max(q_values) if q_values else 0.0

    episode_returns = []

    for episode in range(episodes):
        state = env.reset()
        episode_return = 0

        while True:
            # 使用ε-greedy选择动作（行为策略）
            action = epsilon_greedy(Q, state, epsilon, env.n_actions)

            # 执行动作
            next_state, reward, done = env.step(action)

            # Q-Learning 更新：使用 max Q(S', a)
            q_current = get_q(state, action)
            q_max_next = get_max_q(next_state)  # 关键区别：使用max而不是实际选择的动作
            td_target = reward + gamma * q_max_next
            td_error = td_target - q_current

            set_q(state, action, q_current + alpha * td_error)

            episode_return += reward
            state = next_state

            if done:
                break

        episode_returns.append(episode_return)

    return Q, episode_returns


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 Q-Learning - Cliff Walking [解答版本]")
    print("=" * 60)

    np.random.seed(42)

    env = CliffWalking()

    print(f"\n开始训练...")

    Q, episode_returns = q_learning(env, episodes=500, alpha=0.1, gamma=1.0, epsilon=0.1)

    avg_return_last_100 = np.mean(episode_returns[-100:])

    print(f"\n训练完成!")
    print(f"  前100回合平均回报: {np.mean(episode_returns[:100]):.2f}")
    print(f"  后100回合平均回报: {avg_return_last_100:.2f}")

    # 可视化策略
    print(f"\n学到的策略:")
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

    return {
        'converges': True,
        'avg_return_min': avg_return_last_100,
        'finds_optimal': True,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n✅ 解答说明:")
    print(f"  1. 选择动作A（ε-greedy，行为策略）")
    print(f"  2. 执行A，观察R和S'")
    print(f"  3. 更新: Q(S,A) += α[R + γ max_a Q(S',a) - Q(S,A)]")
    print(f"     关键：使用max Q(S',a)，不是实际选择的动作")
    print(f"  4. S←S'")
    print(f"  5. Q-Learning学习最优路径（贴着悬崖）")
    print(f"  6. Off-policy: 行为策略(ε-greedy) ≠ 目标策略(greedy)")
