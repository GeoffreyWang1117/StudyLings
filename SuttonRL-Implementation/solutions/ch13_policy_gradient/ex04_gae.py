"""解答: GAE (Generalized Advantage Estimation)"""
import numpy as np

class GAEAgent:
    def __init__(self, state_dim, action_dim, gamma=0.99, lambda_=0.95, actor_lr=0.0003, critic_lr=0.001):
        self.gamma, self.lambda_, self.actor_lr, self.critic_lr = gamma, lambda_, actor_lr, critic_lr
        self.actor_weights = np.random.randn(state_dim, action_dim) * 0.01
        self.critic_weights = np.random.randn(state_dim) * 0.01

    def get_value(self, state):
        return np.dot(state, self.critic_weights)

    def get_action_probs(self, state):
        logits = np.dot(state, self.actor_weights)
        exp_logits = np.exp(logits - np.max(logits))
        return exp_logits / np.sum(exp_logits)

    def select_action(self, state):
        probs = self.get_action_probs(state)
        return np.random.choice(len(probs), p=probs)

    def compute_gae(self, rewards, values, next_values, dones):
        """核心: GAE计算"""
        advantages = np.zeros_like(rewards, dtype=np.float32)
        last_gae = 0

        # 反向计算GAE
        for t in reversed(range(len(rewards))):
            if dones[t]:
                # 终止状态: δ = r - V(s)
                delta = rewards[t] - values[t]
                advantages[t] = delta
                last_gae = 0  # 重置GAE
            else:
                # 非终止: δ = r + γV(s') - V(s)
                delta = rewards[t] + self.gamma * next_values[t] - values[t]
                # GAE递归: A_t = δ_t + γλA_{t+1}
                advantages[t] = delta + self.gamma * self.lambda_ * last_gae
                last_gae = advantages[t]

        # 目标回报: R = A + V
        returns = advantages + values
        return advantages, returns

    def update_critic(self, states, returns):
        for state, target in zip(states, returns):
            v_pred = self.get_value(state)
            error = target - v_pred
            self.critic_weights += self.critic_lr * error * state

    def update_actor(self, states, actions, advantages):
        # 标准化advantages减少方差
        advantages = (advantages - np.mean(advantages)) / (np.std(advantages) + 1e-8)

        for state, action, advantage in zip(states, actions, advantages):
            probs = self.get_action_probs(state)
            one_hot = np.zeros(len(probs))
            one_hot[action] = 1
            grad = np.outer(state, one_hot - probs)
            self.actor_weights += self.actor_lr * advantage * grad

    def train_episode(self, env):
        states, actions, rewards, values, dones = [], [], [], [], []
        state = env.reset()
        total_reward = 0
        done = False

        while not done:
            action = self.select_action(state)
            value = self.get_value(state)
            next_state, reward, done = env.step(action)

            states.append(state)
            actions.append(action)
            rewards.append(reward)
            values.append(value)
            dones.append(done)

            state = next_state
            total_reward += reward

        # 计算next_values
        next_values = np.array([self.get_value(states[i+1]) if i < len(states)-1 else 0.0
                                for i in range(len(states))])

        # 计算GAE
        advantages, returns = self.compute_gae(
            np.array(rewards), np.array(values), next_values, np.array(dones)
        )

        # 更新网络
        self.update_critic(states, returns)
        self.update_actor(states, actions, advantages)

        return total_reward


class SimpleCartPole:
    def __init__(self):
        self.state_dim, self.action_dim, self.max_steps = 4, 2, 200
        self.reset()

    def reset(self):
        self.state, self.steps = np.random.randn(self.state_dim) * 0.1, 0
        return self.state

    def step(self, action):
        self.state += (action * 2 - 1) * 0.1 + np.random.randn(self.state_dim) * 0.02
        self.steps += 1
        reward = 1.0 if abs(self.state[0]) < 2.0 else -1.0
        done = abs(self.state[0]) > 2.0 or self.steps >= self.max_steps
        return self.state, reward, done


print("✅ GAE核心:")
print("  1. TD error: δ_t = r_t + γV(s_{t+1}) - V(s_t)")
print("  2. GAE递归: A_t = δ_t + γλA_{t+1}")
print("  3. λ参数平衡偏差-方差")
print("  4. 反向计算所有advantages")
print("\n优势:")
print("  - 显著减少方差 (vs MC)")
print("  - 保持低偏差 (vs TD)")
print("  - PPO/TRPO标配")
print("\n2025年地位: 现代policy gradient算法的必备组件")
print("应用: 所有基于actor-critic的算法 (PPO, TRPO, A3C等)")
