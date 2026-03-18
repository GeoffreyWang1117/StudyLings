"""解答: SARSA(λ)"""
import numpy as np
from collections import defaultdict

class SarsaLambda:
    def __init__(self, n_actions, alpha=0.1, gamma=0.99, lambda_=0.9, epsilon=0.1):
        self.n_actions, self.alpha, self.gamma, self.lambda_, self.epsilon = n_actions, alpha, gamma, lambda_, epsilon
        self.Q = defaultdict(lambda: np.zeros(n_actions))
        self.traces = defaultdict(lambda: np.zeros(n_actions))

    def select_action(self, state):
        if np.random.random() < self.epsilon:
            return np.random.randint(self.n_actions)
        return np.argmax(self.Q[state])

    def reset_traces(self):
        self.traces = defaultdict(lambda: np.zeros(self.n_actions))

    def update_traces(self, state, action, trace_type='accumulating'):
        # 衰减所有traces
        for s in list(self.traces.keys()):
            self.traces[s] *= self.gamma * self.lambda_
            # 清除接近零的traces
            if np.max(np.abs(self.traces[s])) < 1e-6:
                del self.traces[s]

        # 更新当前state-action的trace
        if trace_type == 'accumulating':
            self.traces[state][action] += 1
        else:  # replacing
            self.traces[state][action] = 1

    def update(self, state, action, reward, next_state, next_action, done):
        # TD error
        if done:
            td_error = reward - self.Q[state][action]
        else:
            td_error = reward + self.gamma * self.Q[next_state][next_action] - self.Q[state][action]

        # 更新当前state-action的trace
        self.update_traces(state, action)

        # 使用traces更新所有Q值
        for s in list(self.traces.keys()):
            for a in range(self.n_actions):
                if self.traces[s][a] > 0:
                    self.Q[s][a] += self.alpha * td_error * self.traces[s][a]

    def train_episode(self, env, trace_type='accumulating'):
        self.reset_traces()
        state = env.reset()
        action = self.select_action(state)
        total_reward = 0

        done = False
        while not done:
            next_state, reward, done = env.step(action)
            next_action = self.select_action(next_state) if not done else 0

            self.update(state, action, reward, next_state, next_action, done)

            state, action = next_state, next_action
            total_reward += reward

        return total_reward


class SimpleGridWorld:
    def __init__(self, size=5):
        self.size, self.n_actions = size, 4
        self.reset()

    def reset(self):
        self.state, self.goal = 0, self.size * self.size - 1
        return self.state

    def step(self, action):
        row, col = self.state // self.size, self.state % self.size
        if action == 0 and row > 0: row -= 1
        elif action == 1 and row < self.size - 1: row += 1
        elif action == 2 and col > 0: col -= 1
        elif action == 3 and col < self.size - 1: col += 1
        self.state = row * self.size + col
        return self.state, (1.0 if self.state == self.goal else -0.01), (self.state == self.goal)


print("✅ SARSA(λ)核心:")
print("  1. Eligibility traces: e(s,a) = γλe(s,a) + 1")
print("  2. TD error: δ = R + γQ(S',A') - Q(S,A)")
print("  3. 更新所有Q值: Q(s,a) += αδe(s,a)")
print("  4. λ控制credit assignment范围")
print("\n效果: 比SARSA更快的学习，比MC更稳定")
print("应用: 连续控制任务，需要快速credit assignment的场景")
print("2025年地位: 经典算法，理解traces机制的基础")
