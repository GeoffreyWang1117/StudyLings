"""
解答: SARSA (On-Policy TD Control)

这是 ex02_sarsa.py 的完整实现解答
"""

import numpy as np


class CliffWalking:
    """悬崖行走环境"""

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


def sarsa(env, episodes=500, alpha=0.1, gamma=1.0, epsilon=0.1):
    """
    SARSA 算法

    更新: Q(S,A) ← Q(S,A) + α[R + γQ(S',A') - Q(S,A)]
    """
    Q = {}

    def get_q(state, action):
        return Q.get((state, action), 0.0)

    def set_q(state, action, value):
        Q[(state, action)] = value

    episode_returns = []

    for episode in range(episodes):
        state = env.reset()
        action = epsilon_greedy(Q, state, epsilon, env.n_actions)

        episode_return = 0

        while True:
            # 执行动作
            next_state, reward, done = env.step(action)

            # 选择下一个动作（使用当前策略）
            next_action = epsilon_greedy(Q, next_state, epsilon, env.n_actions)

            # SARSA 更新
            q_current = get_q(state, action)
            q_next = get_q(next_state, next_action)  # 使用 Q(S', A')
            td_target = reward + gamma * q_next
            td_error = td_target - q_current

            set_q(state, action, q_current + alpha * td_error)

            episode_return += reward
            state = next_state
            action = next_action  # 重要：使用已选择的动作

            if done:
                break

        episode_returns.append(episode_return)

    return Q, episode_returns


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 SARSA - Cliff Walking [解答版本]")
    print("=" * 60)

    np.random.seed(42)

    env = CliffWalking()

    print(f"\n开始训练...")

    Q, episode_returns = sarsa(env, episodes=500, alpha=0.1, gamma=1.0, epsilon=0.1)

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
        'converges': avg_return_last_100 > -100,
        'avg_return_min': avg_return_last_100,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n✅ 解答说明:")
    print(f"  1. 选择动作A（ε-greedy）")
    print(f"  2. 执行A，观察R和S'")
    print(f"  3. 选择下一个动作A'（ε-greedy）")
    print(f"  4. 更新: Q(S,A) += α[R + γQ(S',A') - Q(S,A)]")
    print(f"  5. S←S', A←A'（使用已选择的A'）")
    print(f"  6. SARSA学习安全路径（远离悬崖）")
