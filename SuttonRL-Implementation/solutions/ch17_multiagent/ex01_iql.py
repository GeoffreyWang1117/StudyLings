"""解答: IQL"""
import numpy as np
from collections import defaultdict

class MultiAgentEnv:
    def __init__(self, n_agents=2, grid_size=5):
        self.n_agents, self.grid_size, self.n_actions = n_agents, grid_size, 5
        self.reset()
    def reset(self):
        self.agent_positions = [np.random.randint(0, self.grid_size, 2) for _ in range(self.n_agents)]
        self.resource_pos = np.random.randint(0, self.grid_size, 2)
        return self._get_states()
    def _get_states(self):
        return [tuple(np.concatenate([pos, self.resource_pos])) for pos in self.agent_positions]
    def step(self, actions):
        rewards = [0.0] * self.n_agents
        for i, action in enumerate(actions):
            if action == 0: self.agent_positions[i][0] = max(0, self.agent_positions[i][0] - 1)
            elif action == 1: self.agent_positions[i][0] = min(self.grid_size-1, self.agent_positions[i][0] + 1)
            elif action == 2: self.agent_positions[i][1] = max(0, self.agent_positions[i][1] - 1)
            elif action == 3: self.agent_positions[i][1] = min(self.grid_size-1, self.agent_positions[i][1] + 1)
        for i in range(self.n_agents):
            if np.array_equal(self.agent_positions[i], self.resource_pos):
                rewards[i] = 1.0
        for i in range(self.n_agents):
            for j in range(i+1, self.n_agents):
                if np.array_equal(self.agent_positions[i], self.agent_positions[j]):
                    rewards[i] -= 0.5; rewards[j] -= 0.5
        done = any(r > 0 for r in rewards)
        return self._get_states(), rewards, done

def independent_q_learning(env, episodes=1000, alpha=0.1, gamma=0.99, epsilon=0.1):
    Q_tables = [defaultdict(lambda: np.zeros(env.n_actions)) for _ in range(env.n_agents)]
    
    for episode in range(episodes):
        states = env.reset()
        done = False
        
        while not done:
            # 每个智能体独立选择动作
            actions = []
            for i in range(env.n_agents):
                if np.random.random() < epsilon:
                    action = np.random.randint(env.n_actions)
                else:
                    action = np.argmax(Q_tables[i][states[i]])
                actions.append(action)
            
            next_states, rewards, done = env.step(actions)
            
            # 每个智能体独立更新
            for i in range(env.n_agents):
                Q_tables[i][states[i]][actions[i]] += alpha * (
                    rewards[i] + gamma * np.max(Q_tables[i][next_states[i]]) - Q_tables[i][states[i]][actions[i]]
                )
            
            states = next_states
    
    return Q_tables

print("✅ IQL核心:")
print("  1. 每个智能体i维护Q_i(s,a_i)")
print("  2. 独立学习，将他人视为环境")
print("  3. 去中心化执行")
print("\n优势: 简单可扩展  局限: 非平稳性")
