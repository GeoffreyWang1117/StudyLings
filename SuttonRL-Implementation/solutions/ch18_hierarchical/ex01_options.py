"""解答: Options Framework"""
import numpy as np

class Option:
    def __init__(self, name, initiation_set, policy, termination):
        self.name, self.initiation_set, self.policy, self.termination = name, initiation_set, policy, termination
    def can_initiate(self, state):
        return state in self.initiation_set
    def select_action(self, state):
        return self.policy(state)
    def should_terminate(self, state):
        return np.random.random() < self.termination(state)

class OptionsQLearning:
    def __init__(self, n_states, options):
        self.n_states, self.options = n_states, options
        self.Q = np.zeros((n_states, len(options)))
        self.alpha = 0.1
    
    def select_option(self, state, epsilon=0.1):
        available = [i for i, opt in enumerate(self.options) if opt.can_initiate(state)]
        if not available:
            return None
        if np.random.random() < epsilon:
            return np.random.choice(available)
        return available[np.argmax(self.Q[state, available])]
    
    def execute_option(self, env, state, option):
        total_reward, steps = 0, 0
        while not option.should_terminate(state):
            action = option.select_action(state)
            next_state, reward, done = env.step(action)
            total_reward += reward
            steps += 1
            state = next_state
            if done:
                break
        return total_reward, state, steps
    
    def update(self, state, option_idx, reward, next_state, steps, gamma=0.99):
        # SMDP Q-learning: Q(s,o) += α[r + γ^k max Q(s',·) - Q(s,o)]
        self.Q[state, option_idx] += self.alpha * (
            reward + (gamma ** steps) * np.max(self.Q[next_state]) - self.Q[state, option_idx]
        )

print("✅ Options核心:")
print("  1. Option o = (I, π, β)")
print("  2. Semi-MDP: 在option层面决策")
print("  3. 时间抽象: 一个option多步执行")
print("\n效果: 学习可复用技能，加速学习")
print("应用: 机器人技能库，层次化任务")
