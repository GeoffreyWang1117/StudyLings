"""
解答: 策略迭代
"""

import numpy as np


class GridWorld:
    def __init__(self, size=4):
        self.size = size
        self.n_states = size * size
        self.n_actions = 4
        self.terminal_states = [0, self.n_states - 1]

    def is_terminal(self, state):
        return state in self.terminal_states

    def step(self, state, action):
        if self.is_terminal(state):
            return state, 0
        row, col = state // self.size, state % self.size
        if action == 0: row = max(row - 1, 0)
        elif action == 1: row = min(row + 1, self.size - 1)
        elif action == 2: col = max(col - 1, 0)
        elif action == 3: col = min(col + 1, self.size - 1)
        return row * self.size + col, -1


def policy_evaluation(env, policy, V, gamma=1.0, theta=0.01):
    while True:
        delta = 0
        for s in range(env.n_states):
            if env.is_terminal(s):
                continue
            v = V[s]
            action = policy[s]
            next_state, reward = env.step(s, action)
            V[s] = reward + gamma * V[next_state]
            delta = max(delta, abs(v - V[s]))
        if delta < theta:
            break
    return V


def policy_improvement(env, V, gamma=1.0):
    policy = np.zeros(env.n_states, dtype=int)
    policy_stable = True
    
    for s in range(env.n_states):
        if env.is_terminal(s):
            continue
        old_action = policy[s]
        action_values = []
        for a in range(env.n_actions):
            next_state, reward = env.step(s, a)
            action_values.append(reward + gamma * V[next_state])
        policy[s] = np.argmax(action_values)
        if old_action != policy[s]:
            policy_stable = False
    
    return policy, policy_stable


def policy_iteration(env, gamma=1.0, theta=0.01):
    V = np.zeros(env.n_states)
    policy = np.random.randint(0, env.n_actions, env.n_states)
    iterations = 0
    
    while True:
        iterations += 1
        V = policy_evaluation(env, policy, V, gamma, theta)
        policy, policy_stable = policy_improvement(env, V, gamma)
        if policy_stable:
            break
    
    return V, policy, iterations


def test():
    print("=" * 60)
    print("测试策略迭代 [解答版本]")
    print("=" * 60)
    
    np.random.seed(42)
    env = GridWorld(size=4)
    V, policy, iterations = policy_iteration(env, gamma=1.0, theta=0.01)
    
    print(f"\n收敛! 迭代次数: {iterations}")
    print(f"\n✅ 核心步骤:")
    print(f"  1. 策略评估: V^π(s) = r + γV^π(s')")
    print(f"  2. 策略改进: π(s) = argmax_a Σp(s',r|s,a)[r+γV(s')]")
    print(f"  3. 重复直到策略稳定")
    print(f"\n特点: 比值迭代收敛更快，但每轮成本更高")
    
    return {'iterations': iterations, 'converges': iterations < 20}


if __name__ == '__main__':
    test()
