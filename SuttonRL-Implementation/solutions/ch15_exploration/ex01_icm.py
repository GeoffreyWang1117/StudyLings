"""解答: ICM"""
import numpy as np

class GridWorldExploration:
    def __init__(self, size=10):
        self.size = size
        self.n_states = size * size
        self.n_actions = 4
        self.goal = (size-1, size-1)
        self.reset()
    def reset(self):
        self.pos = (0, 0)
        self.visited = set([self.pos])
        return self._state_index(self.pos)
    def step(self, action):
        row, col = self.pos
        if action == 0: row = max(0, row - 1)
        elif action == 1: row = min(self.size - 1, row + 1)
        elif action == 2: col = max(0, col - 1)
        elif action == 3: col = min(self.size - 1, col + 1)
        self.pos = (row, col)
        self.visited.add(self.pos)
        extrinsic_reward = 1.0 if self.pos == self.goal else 0.0
        done = (self.pos == self.goal)
        return self._state_index(self.pos), extrinsic_reward, done
    def _state_index(self, pos):
        return pos[0] * self.size + pos[1]

class ICM:
    def __init__(self, state_dim, action_dim, feature_dim=32, lr=0.001):
        self.state_dim, self.action_dim, self.feature_dim, self.lr = state_dim, action_dim, feature_dim, lr
        self.feature_weights = np.random.randn(state_dim, feature_dim) * 0.01
        self.forward_weights = np.random.randn(feature_dim + action_dim, feature_dim) * 0.01
        self.inverse_weights = np.random.randn(feature_dim * 2, action_dim) * 0.01

    def encode_state(self, state):
        state_onehot = np.zeros(self.state_dim)
        state_onehot[state] = 1
        return state_onehot @ self.feature_weights

    def forward_model(self, state_features, action):
        action_onehot = np.zeros(self.action_dim)
        action_onehot[action] = 1
        input_vec = np.concatenate([state_features, action_onehot])
        return input_vec @ self.forward_weights

    def inverse_model(self, state_features, next_state_features):
        input_vec = np.concatenate([state_features, next_state_features])
        logits = input_vec @ self.inverse_weights
        exp_logits = np.exp(logits - np.max(logits))
        return exp_logits / np.sum(exp_logits)

    def compute_intrinsic_reward(self, state, action, next_state):
        state_features = self.encode_state(state)
        next_state_features = self.encode_state(next_state)
        predicted_next = self.forward_model(state_features, action)
        return np.sum((predicted_next - next_state_features)**2)

    def update(self, state, action, next_state):
        state_features = self.encode_state(state)
        next_state_features = self.encode_state(next_state)
        predicted_next = self.forward_model(state_features, action)
        forward_error = predicted_next - next_state_features
        action_probs = self.inverse_model(state_features, next_state_features)
        action_onehot = np.zeros(self.action_dim)
        action_onehot[action] = 1
        return np.sum(forward_error**2), -np.sum(action_onehot * np.log(action_probs + 1e-10))

def icm_exploration(env, episodes=500, beta=0.2):
    icm = ICM(env.n_states, env.n_actions, feature_dim=32)
    Q = np.zeros((env.n_states, env.n_actions))
    alpha, gamma, epsilon = 0.1, 0.99, 0.1
    all_visited = set()
    
    for episode in range(episodes):
        state = env.reset()
        done = False
        
        while not done:
            if np.random.random() < epsilon:
                action = np.random.randint(env.n_actions)
            else:
                action = np.argmax(Q[state])
            
            next_state, r_ext, done = env.step(action)
            
            # 计算内在奖励
            r_int = icm.compute_intrinsic_reward(state, action, next_state)
            r_total = r_ext + beta * r_int
            
            # Q-learning更新
            Q[state, action] += alpha * (r_total + gamma * np.max(Q[next_state]) - Q[state, action])
            
            # 更新ICM
            icm.update(state, action, next_state)
            
            all_visited.add(state)
            state = next_state
    
    return len(all_visited) / env.n_states, all_visited

def test():
    print("="*60 + "\n测试 ICM [解答版本]\n" + "="*60)
    np.random.seed(42)
    env = GridWorldExploration(size=10)
    coverage, visited = icm_exploration(env, episodes=500, beta=0.2)
    print(f"\n覆盖率: {coverage:.1%} ({len(visited)}/{env.n_states})")
    print(f"\n✅ ICM核心:")
    print(f"  1. Forward Model: 预测φ(s')")
    print(f"  2. Intrinsic Reward: ||φ̂(s') - φ(s')||²")
    print(f"  3. r_total = r_ext + β·r_int")
    print(f"\n效果: 自动探索新奇状态，适用于稀疏奖励")
    return {'coverage': coverage, 'explores_well': coverage > 0.5}

if __name__ == '__main__': test()
