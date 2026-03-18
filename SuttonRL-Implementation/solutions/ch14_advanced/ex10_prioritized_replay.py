"""解答: Prioritized Experience Replay (PER)"""
import numpy as np

class SumTree:
    def __init__(self, capacity):
        self.capacity = capacity
        self.tree = np.zeros(2 * capacity - 1)
        self.data = np.zeros(capacity, dtype=object)
        self.write = 0
        self.n_entries = 0

    def _propagate(self, idx, change):
        parent = (idx - 1) // 2
        self.tree[parent] += change
        if parent != 0:
            self._propagate(parent, change)

    def _retrieve(self, idx, s):
        left = 2 * idx + 1
        right = left + 1
        if left >= len(self.tree):
            return idx
        if s <= self.tree[left]:
            return self._retrieve(left, s)
        else:
            return self._retrieve(right, s - self.tree[left])

    def total(self):
        return self.tree[0]

    def add(self, priority, data):
        idx = self.write + self.capacity - 1
        self.data[self.write] = data
        self.update(idx, priority)
        self.write = (self.write + 1) % self.capacity
        self.n_entries = min(self.n_entries + 1, self.capacity)

    def update(self, idx, priority):
        change = priority - self.tree[idx]
        self.tree[idx] = priority
        self._propagate(idx, change)

    def get(self, s):
        idx = self._retrieve(0, s)
        data_idx = idx - self.capacity + 1
        return idx, self.tree[idx], self.data[data_idx]


class PrioritizedReplayBuffer:
    def __init__(self, capacity, alpha=0.6, beta_start=0.4, beta_frames=100000):
        self.tree = SumTree(capacity)
        self.capacity = capacity
        self.alpha = alpha
        self.beta_start = beta_start
        self.beta_frames = beta_frames
        self.frame = 1
        self.epsilon = 0.01

    def _get_priority(self, td_error):
        return (abs(td_error) + self.epsilon) ** self.alpha

    def add(self, state, action, reward, next_state, done, td_error):
        priority = self._get_priority(td_error)
        data = (state, action, reward, next_state, done)
        self.tree.add(priority, data)

    def sample(self, batch_size):
        batch, indices, weights = [], [], []
        segment = self.tree.total() / batch_size

        # β退火
        beta = min(1.0, self.beta_start + self.frame * (1.0 - self.beta_start) / self.beta_frames)
        self.frame += 1

        min_prob = np.min(self.tree.tree[-self.tree.capacity:]) / self.tree.total()
        max_weight = (self.tree.n_entries * min_prob) ** (-beta)

        for i in range(batch_size):
            s = np.random.uniform(segment * i, segment * (i + 1))
            idx, priority, data = self.tree.get(s)

            # IS权重
            sampling_prob = priority / self.tree.total()
            weight = (self.tree.n_entries * sampling_prob) ** (-beta)
            weight /= max_weight

            batch.append(data)
            indices.append(idx)
            weights.append(weight)

        return batch, indices, np.array(weights)

    def update_priorities(self, indices, td_errors):
        for idx, td_error in zip(indices, td_errors):
            priority = self._get_priority(td_error)
            self.tree.update(idx, priority)


class DQNWithPER:
    def __init__(self, state_dim, action_dim, buffer_size=10000):
        self.state_dim, self.action_dim = state_dim, action_dim
        self.gamma, self.epsilon, self.lr = 0.99, 0.1, 0.001
        self.q_weights = np.random.randn(state_dim, action_dim) * 0.01
        self.target_weights = self.q_weights.copy()
        self.buffer = PrioritizedReplayBuffer(buffer_size)

    def get_q_values(self, state, use_target=False):
        weights = self.target_weights if use_target else self.q_weights
        return state @ weights

    def select_action(self, state):
        if np.random.random() < self.epsilon:
            return np.random.randint(self.action_dim)
        return np.argmax(self.get_q_values(state))

    def train_step(self, batch_size=32):
        if self.buffer.tree.n_entries < batch_size:
            return

        batch, indices, weights = self.buffer.sample(batch_size)
        td_errors = []

        for i, (state, action, reward, next_state, done) in enumerate(batch):
            q_current = self.get_q_values(state)[action]
            q_next = 0 if done else np.max(self.get_q_values(next_state, use_target=True))
            td_target = reward + self.gamma * q_next
            td_error = td_target - q_current
            td_errors.append(td_error)

            # 使用IS权重加权更新
            grad = weights[i] * td_error * state
            self.q_weights[:, action] += self.lr * grad

        # 更新优先级
        self.buffer.update_priorities(indices, td_errors)

    def update_target_network(self):
        self.target_weights = self.q_weights.copy()


print("✅ PER核心:")
print("  1. 优先级: p_i = (|δ_i| + ε)^α")
print("  2. SumTree: O(log N)采样和更新")
print("  3. Importance Sampling: w_i = (N·P(i))^(-β)")
print("  4. β从0.4退火到1，修正偏差")
print("\n效果:")
print("  - 提高样本效率 (学习更快)")
print("  - 关注重要经验 (TD error大)")
print("  - Rainbow DQN核心组件")
print("\n2025年地位: DQN系列算法的标准配置")
