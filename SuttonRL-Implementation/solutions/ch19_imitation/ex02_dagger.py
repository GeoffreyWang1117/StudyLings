"""解答: DAgger"""
import numpy as np

class DAgger:
    def __init__(self, state_dim, action_dim, learning_rate=0.001):
        self.state_dim, self.action_dim, self.lr = state_dim, action_dim, learning_rate
        self.weights = np.random.randn(state_dim, action_dim) * 0.01
        self.bias = np.zeros(action_dim)
        self.aggregated_data = []

    def get_action_probs(self, state):
        logits = state @ self.weights + self.bias
        exp_logits = np.exp(logits - np.max(logits))
        return exp_logits / np.sum(exp_logits)

    def predict_action(self, state, deterministic=False):
        probs = self.get_action_probs(state)
        return np.argmax(probs) if deterministic else np.random.choice(len(probs), p=probs)

    def train_on_data(self, data, epochs=10, batch_size=32):
        for epoch in range(epochs):
            np.random.shuffle(data)
            for i in range(0, len(data), batch_size):
                batch = data[i:i+batch_size]
                for state, action in batch:
                    probs = self.get_action_probs(state)
                    one_hot = np.zeros(self.action_dim)
                    one_hot[action] = 1
                    self.weights -= self.lr * np.outer(state, probs - one_hot)
                    self.bias -= self.lr * (probs - one_hot)

    def collect_trajectory(self, env, deterministic=False):
        trajectory = []
        state = env.reset()
        done = False
        while not done:
            action = self.predict_action(state, deterministic)
            next_state, reward, done = env.step(action)
            trajectory.append((state.copy(), action, reward))
            state = next_state
        return trajectory

    def get_expert_labels(self, states, expert_policy):
        return [expert_policy(state) for state in states]

    def dagger_iteration(self, env, expert_policy, n_trajectories=10):
        new_states = []
        for _ in range(n_trajectories):
            trajectory = self.collect_trajectory(env)
            states = [s for s, a, r in trajectory]
            new_states.extend(states)

        expert_actions = self.get_expert_labels(new_states, expert_policy)

        for state, action in zip(new_states, expert_actions):
            self.aggregated_data.append((state, action))

        self.train_on_data(self.aggregated_data, epochs=5)
        return len(new_states)

    def train_with_dagger(self, env, expert_policy, initial_data, n_iterations=10, trajectories_per_iter=10):
        self.aggregated_data = initial_data.copy()
        self.train_on_data(self.aggregated_data, epochs=10)
        history = []

        for iteration in range(n_iterations):
            perf = self.evaluate(env, n_episodes=5)
            history.append(perf)
            print(f"Iteration {iteration}, Performance: {perf:.2f}, Data size: {len(self.aggregated_data)}")
            self.dagger_iteration(env, expert_policy, trajectories_per_iter)

        return history

    def evaluate(self, env, n_episodes=10):
        total_rewards = []
        for _ in range(n_episodes):
            state = env.reset()
            episode_reward = 0
            done = False
            while not done:
                action = self.predict_action(state, deterministic=True)
                state, reward, done = env.step(action)
                episode_reward += reward
            total_rewards.append(episode_reward)
        return np.mean(total_rewards)


class GridWorld:
    def __init__(self, size=10):
        self.size, self.state_dim, self.action_dim = size, 2, 4
        self.reset()

    def reset(self):
        self.pos, self.goal = np.array([0, 0]), np.array([self.size-1, self.size-1])
        return self.pos.copy()

    def step(self, action):
        move = {0: [0, 1], 1: [0, -1], 2: [-1, 0], 3: [1, 0]}
        self.pos += move[action]
        self.pos = np.clip(self.pos, 0, self.size-1)
        dist = np.linalg.norm(self.pos - self.goal)
        return self.pos.copy(), -dist, dist < 1.0


def expert_policy(state, goal=np.array([9, 9])):
    diff = goal - state
    return (3 if diff[0] > 0 else 2) if abs(diff[0]) > abs(diff[1]) else (0 if diff[1] > 0 else 1)


print("✅ DAgger核心:")
print("  1. 迭代收集: 在π的分布上收集数据")
print("  2. 专家标注: 对新状态请专家标注")
print("  3. 数据聚合: D ← D ∪ D_new")
print("  4. 重新训练: π ← BC(D)")
print("\n优势:")
print("  - 解决covariate shift")
print("  - 误差界: O(Tε) vs BC的O(T²ε)")
print("  - 理论保证更好")
print("\nRLHF联系:")
print("  - 迭代数据收集的理论基础")
print("  - SFT -> RL -> 新数据 -> 再训练")
print("2025年地位: 模仿学习经典算法，RLHF迭代训练的理论支撑")
