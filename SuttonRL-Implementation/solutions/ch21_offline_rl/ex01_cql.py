"""解答: CQL (Conservative Q-Learning)"""
import numpy as np

class CQL:
    def __init__(self, state_dim, action_dim, alpha=1.0, lr=0.001):
        self.state_dim, self.action_dim, self.alpha, self.lr = state_dim, action_dim, alpha, lr
        self.q_weights = np.random.randn(state_dim, action_dim) * 0.01
        self.target_weights = self.q_weights.copy()

    def get_q_values(self, state, use_target=False):
        weights = self.target_weights if use_target else self.q_weights
        return state @ weights

    def compute_cql_loss(self, states, actions, rewards, next_states, dones):
        batch_size = len(states)
        cql_loss, bellman_loss = 0, 0

        for i in range(batch_size):
            state, action, reward, next_state, done = states[i], actions[i], rewards[i], next_states[i], dones[i]

            q_values = self.get_q_values(state)
            q_current = q_values[action]

            # Bellman target
            if done:
                q_target = reward
            else:
                q_next = np.max(self.get_q_values(next_state, use_target=True))
                q_target = reward + 0.99 * q_next

            bellman_loss += (q_current - q_target) ** 2

            # CQL正则化: log-sum-exp - Q(s,a_data)
            max_q = np.max(q_values)
            lse = max_q + np.log(np.sum(np.exp(q_values - max_q)))
            cql_loss += lse - q_current

        return cql_loss / batch_size, bellman_loss / batch_size

    def train_step(self, batch, gamma=0.99):
        states, actions, rewards, next_states, dones = batch
        cql_loss, bellman_loss = self.compute_cql_loss(states, actions, rewards, next_states, dones)

        total_loss = self.alpha * cql_loss + bellman_loss

        # 简化梯度更新
        for i, (state, action) in enumerate(zip(states, actions)):
            q_values = self.get_q_values(state)
            grad = np.zeros_like(q_values)
            # CQL梯度 (简化)
            grad += np.exp(q_values - np.max(q_values))
            grad[action] -= 1
            # Bellman梯度
            q_target = rewards[i]
            if not dones[i]:
                q_target += gamma * np.max(self.get_q_values(next_states[i], use_target=True))
            grad[action] += 2 * (q_values[action] - q_target)

            self.q_weights[:, action] -= self.lr * self.alpha * state * grad[action]

        return total_loss

    def train(self, offline_data, n_steps=1000, batch_size=32):
        for step in range(n_steps):
            batch_indices = np.random.choice(len(offline_data), batch_size)
            batch = [offline_data[i] for i in batch_indices]
            states = np.array([b[0] for b in batch])
            actions = np.array([b[1] for b in batch])
            rewards = np.array([b[2] for b in batch])
            next_states = np.array([b[3] for b in batch])
            dones = np.array([b[4] for b in batch])

            loss = self.train_step((states, actions, rewards, next_states, dones))

            if step % 100 == 0:
                print(f"Step {step}, Loss: {loss:.4f}")

            if step % 50 == 0:
                self.target_weights = self.q_weights.copy()


print("✅ CQL核心:")
print("  1. 保守性: 惩罚OOD动作的Q值")
print("  2. CQL loss: LSE_a Q(s,a) - Q(s,a_data)")
print("  3. 总目标: α·CQL_loss + Bellman_loss")
print("  4. 效果: Q(s,a_seen) > Q(s,a_unseen)")
print("\nRLHF应用:")
print("  - RLHF是离线RL (固定数据)")
print("  - KL penalty ≈ CQL的保守性")
print("  - 避免过度偏离SFT策略")
print("2025年地位: 离线RL的SOTA，RLHF的理论基础")
