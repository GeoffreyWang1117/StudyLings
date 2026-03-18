"""
解答: Double Q-Learning
"""

import numpy as np


class MaxBiasEnv:
    def __init__(self, n_actions_B=10):
        self.n_actions_B = n_actions_B
        self.n_states = 3
        self.state_A, self.state_B, self.terminal = 0, 1, 2

    def reset(self):
        self.state = self.state_A
        return self.state

    def step(self, action):
        if self.state == self.state_A:
            if action == 0:
                return self.terminal, 0, True
            else:
                self.state = self.state_B
                return self.state, 0, False
        elif self.state == self.state_B:
            reward = np.random.normal(-0.1, 1.0)
            return self.terminal, reward, True
        else:
            return self.terminal, 0, True


def double_q_learning(env, episodes=300, alpha=0.1, gamma=1.0, epsilon=0.1):
    max_actions = max(2, env.n_actions_B)
    Q1 = np.zeros((env.n_states, max_actions))
    Q2 = np.zeros((env.n_states, max_actions))
    left_actions = []

    for episode in range(episodes):
        state = env.reset()
        done = False

        while not done:
            if state == env.state_A:
                n_actions = 2
            elif state == env.state_B:
                n_actions = env.n_actions_B
            else:
                break

            # ε-greedy based on Q1+Q2
            if np.random.random() < epsilon:
                action = np.random.randint(n_actions)
            else:
                Q_sum = Q1[state, :n_actions] + Q2[state, :n_actions]
                action = np.argmax(Q_sum)

            if state == env.state_A:
                left_actions.append(1 if action == 0 else 0)

            next_state, reward, done = env.step(action)

            # Randomly update Q1 or Q2
            if np.random.random() < 0.5:
                if not done:
                    best_action = np.argmax(Q1[next_state])
                    td_target = reward + gamma * Q2[next_state, best_action]
                else:
                    td_target = reward
                Q1[state, action] += alpha * (td_target - Q1[state, action])
            else:
                if not done:
                    best_action = np.argmax(Q2[next_state])
                    td_target = reward + gamma * Q1[next_state, best_action]
                else:
                    td_target = reward
                Q2[state, action] += alpha * (td_target - Q2[state, action])

            state = next_state

    left_action_pct = np.mean(left_actions) if left_actions else 0
    return Q1, Q2, left_action_pct


def test():
    print("=" * 60)
    print("测试 Double Q-Learning [解答版本]")
    print("=" * 60)

    np.random.seed(42)
    env = MaxBiasEnv(n_actions_B=10)
    
    Q1, Q2, left_pct = double_q_learning(env, episodes=300, alpha=0.1, epsilon=0.1)
    
    print(f"\n在状态A选择左的比例: {left_pct:.1%}")
    print(f"\n✅ 解答说明:")
    print(f"  1. 维护Q1和Q2两个独立Q函数")
    print(f"  2. 用Q1选择: A*=argmax Q1(s,a)")
    print(f"  3. 用Q2评估: Q2(s,A*)")
    print(f"  4. 反之亦然，随机选择")
    print(f"\n效果: 减少Q-learning的最大化偏差，学到正确策略")
    
    return {'left_action_pct': left_pct, 'learns_correct': left_pct > 0.5}


if __name__ == '__main__':
    test()
