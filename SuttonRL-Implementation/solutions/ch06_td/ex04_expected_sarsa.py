"""
解答: Expected SARSA

这是 ex04_expected_sarsa.py 的完整实现解答
"""

import numpy as np


class CliffWalking:
    """悬崖行走环境"""

    def __init__(self, height=4, width=12):
        self.height = height
        self.width = width
        self.n_states = height * width
        self.n_actions = 4
        self.start = (height - 1, 0)
        self.goal = (height - 1, width - 1)
        self.cliff = [(height - 1, i) for i in range(1, width - 1)]

    def reset(self):
        self.pos = self.start
        return self._state_index(self.pos)

    def step(self, action):
        row, col = self.pos
        if action == 0: row = max(0, row - 1)
        elif action == 1: row = min(self.height - 1, row + 1)
        elif action == 2: col = max(0, col - 1)
        elif action == 3: col = min(self.width - 1, col + 1)
        
        self.pos = (row, col)
        if self.pos in self.cliff:
            return self._state_index(self.start), -100, False
        if self.pos == self.goal:
            return self._state_index(self.pos), -1, True
        return self._state_index(self.pos), -1, False

    def _state_index(self, pos):
        row, col = pos
        return row * self.width + col


def expected_sarsa(env, episodes=500, alpha=0.5, gamma=1.0, epsilon=0.1):
    Q = np.zeros((env.n_states, env.n_actions))
    episode_returns = []

    for episode in range(episodes):
        state = env.reset()
        episode_return = 0
        done = False

        while not done:
            # ε-greedy动作选择
            if np.random.random() < epsilon:
                action = np.random.randint(env.n_actions)
            else:
                action = np.argmax(Q[state])

            next_state, reward, done = env.step(action)
            episode_return += reward

            # 计算期望值
            if done:
                expected_q = 0
            else:
                # Expected value = Σ_a π(a|s)Q(s,a)
                best_action = np.argmax(Q[next_state])
                expected_q = 0
                for a in range(env.n_actions):
                    if a == best_action:
                        prob = (1 - epsilon) + epsilon / env.n_actions
                    else:
                        prob = epsilon / env.n_actions
                    expected_q += prob * Q[next_state, a]

            # Expected SARSA更新
            td_target = reward + gamma * expected_q
            Q[state, action] += alpha * (td_target - Q[state, action])

            state = next_state

        episode_returns.append(episode_return)

    return Q, episode_returns


def test():
    print("=" * 60)
    print("测试 Expected SARSA - Cliff Walking [解答版本]")
    print("=" * 60)

    np.random.seed(42)
    env = CliffWalking(height=4, width=12)

    print(f"\n开始训练 (500回合)...")
    Q, episode_returns = expected_sarsa(env, episodes=500, alpha=0.5, epsilon=0.1)

    early_avg = np.mean(episode_returns[:50])
    late_avg = np.mean(episode_returns[-50:])

    print(f"\n训练完成!")
    print(f"  前50回合平均回报: {early_avg:.2f}")
    print(f"  后50回合平均回报: {late_avg:.2f}")

    return {'avg_return': late_avg, 'improves': late_avg > -100}


if __name__ == '__main__':
    result = test()
    print(f"\n✅ 解答说明:")
    print(f"  1. 期望计算: E[Q(S',·)] = Σ π(a|S')Q(S',a)")
    print(f"  2. ε-greedy概率: π(a*) = 1-ε+ε/n, π(a≠a*) = ε/n")
    print(f"  3. 更新: Q(S,A) ← Q(S,A) + α[R+γE[Q]-Q(S,A)]")
    print(f"  4. 比SARSA稳定，比Q-learning安全")
