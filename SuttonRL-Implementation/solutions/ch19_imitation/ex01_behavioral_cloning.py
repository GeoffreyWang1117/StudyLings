"""解答: Behavioral Cloning"""
import numpy as np

class BehavioralCloning:
    def __init__(self, state_dim, action_dim, learning_rate=0.001):
        self.state_dim, self.action_dim, self.lr = state_dim, action_dim, learning_rate
        self.weights = np.random.randn(state_dim, action_dim) * 0.01
        self.bias = np.zeros(action_dim)

    def get_action_probs(self, state):
        logits = state @ self.weights + self.bias
        exp_logits = np.exp(logits - np.max(logits))
        return exp_logits / np.sum(exp_logits)

    def predict_action(self, state, deterministic=False):
        probs = self.get_action_probs(state)
        if deterministic:
            return np.argmax(probs)
        return np.random.choice(len(probs), p=probs)

    def train_on_batch(self, states, actions):
        batch_size = len(states)
        total_loss = 0

        for state, action in zip(states, actions):
            probs = self.get_action_probs(state)
            # 交叉熵损失
            loss = -np.log(probs[action] + 1e-8)
            total_loss += loss

            # 梯度: ∇L = state^T (probs - one_hot)
            one_hot = np.zeros(self.action_dim)
            one_hot[action] = 1
            grad_weights = np.outer(state, probs - one_hot)
            grad_bias = probs - one_hot

            # 更新参数
            self.weights -= self.lr * grad_weights
            self.bias -= self.lr * grad_bias

        return total_loss / batch_size

    def train(self, expert_data, epochs=100, batch_size=32):
        history = []
        for epoch in range(epochs):
            np.random.shuffle(expert_data)
            epoch_loss = 0
            n_batches = len(expert_data) // batch_size

            for i in range(n_batches):
                batch = expert_data[i*batch_size:(i+1)*batch_size]
                states = np.array([s for s, a in batch])
                actions = np.array([a for s, a in batch])
                loss = self.train_on_batch(states, actions)
                epoch_loss += loss

            avg_loss = epoch_loss / n_batches if n_batches > 0 else 0
            history.append(avg_loss)
            if epoch % 10 == 0:
                print(f"Epoch {epoch}, Loss: {avg_loss:.4f}")

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


def collect_expert_data(env, expert_policy, n_episodes=100):
    expert_data = []
    for _ in range(n_episodes):
        state = env.reset()
        done = False
        while not done:
            action = expert_policy(state)
            expert_data.append((state.copy(), action))
            state, _, done = env.step(action)
    return expert_data


class SimpleNavigationEnv:
    def __init__(self):
        self.state_dim, self.action_dim = 4, 4
        self.reset()

    def reset(self):
        self.pos, self.goal = np.random.rand(2) * 10, np.random.rand(2) * 10
        return self._get_state()

    def _get_state(self):
        return np.concatenate([self.pos, self.goal])

    def step(self, action):
        move = {0: [0, 1], 1: [0, -1], 2: [-1, 0], 3: [1, 0]}
        self.pos += move[action]
        self.pos = np.clip(self.pos, 0, 10)
        dist = np.linalg.norm(self.pos - self.goal)
        return self._get_state(), -dist, dist < 0.5


def expert_policy(state):
    pos, goal = state[:2], state[2:]
    diff = goal - pos
    return (2 if diff[0] < 0 else 3) if abs(diff[0]) > abs(diff[1]) else (1 if diff[1] < 0 else 0)


print("✅ Behavioral Cloning核心:")
print("  1. 监督学习目标: L(θ) = E[-log π_θ(a|s)]")
print("  2. 从专家演示学习: D = {(s,a)}")
print("  3. 简单快速，不需要奖励函数")
print("\n局限:")
print("  - Covariate shift: 训练分布 ≠ 测试分布")
print("  - 误差累积: O(T²)")
print("  - 无法超越专家")
print("\nRLHF应用: SFT阶段 (Supervised Fine-Tuning)")
print("  ChatGPT: 在人类标注对话上做BC -> 初始化策略 -> PPO优化")
print("2025年地位: RLHF第一步，LLM对齐的基础")
