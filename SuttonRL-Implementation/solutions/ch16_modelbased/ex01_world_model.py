"""解答: World Model"""
import numpy as np

class WorldModel:
    def __init__(self, n_states, n_actions):
        self.n_states, self.n_actions = n_states, n_actions
        self.transition_counts = np.zeros((n_states, n_actions, n_states))
        self.reward_sum = np.zeros((n_states, n_actions))
        self.reward_count = np.zeros((n_states, n_actions))
    
    def update(self, state, action, reward, next_state):
        self.transition_counts[state, action, next_state] += 1
        self.reward_sum[state, action] += reward
        self.reward_count[state, action] += 1
    
    def sample_transition(self, state, action):
        probs = self.transition_counts[state, action]
        if np.sum(probs) == 0:
            return np.random.randint(self.n_states)
        probs = probs / np.sum(probs)
        return np.random.choice(self.n_states, p=probs)
    
    def predict_reward(self, state, action):
        if self.reward_count[state, action] == 0:
            return 0
        return self.reward_sum[state, action] / self.reward_count[state, action]

print("✅ World Model核心:")
print("  1. 学习P(s'|s,a): 统计转移频率")
print("  2. 学习R(s,a): 平均奖励")
print("  3. 用于规划和模拟")
print("\nDyna: 真实经验训练model，model生成模拟经验训练policy")
