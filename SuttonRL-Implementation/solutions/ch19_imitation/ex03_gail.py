"""解答: GAIL (Generative Adversarial Imitation Learning)"""
import numpy as np

class Discriminator:
    def __init__(self, state_dim, action_dim, lr=0.001):
        input_dim = state_dim + action_dim
        self.weights = np.random.randn(input_dim, 1) * 0.01
        self.lr = lr

    def predict(self, state, action):
        x = np.concatenate([state, [action] if np.isscalar(action) else action])
        return 1 / (1 + np.exp(-np.dot(x, self.weights)))

    def train_step(self, expert_batch, learner_batch):
        loss = 0
        # Expert: 标签=1
        for s, a in expert_batch:
            x = np.concatenate([s, [a] if np.isscalar(a) else a])
            pred = self.predict(s, a)
            loss -= np.log(pred + 1e-8)
            grad = -(1 - pred) * x.reshape(-1, 1)
            self.weights -= self.lr * grad

        # Learner: 标签=0
        for s, a in learner_batch:
            x = np.concatenate([s, [a] if np.isscalar(a) else a])
            pred = self.predict(s, a)
            loss -= np.log(1 - pred + 1e-8)
            grad = pred * x.reshape(-1, 1)
            self.weights -= self.lr * grad

        return loss / (len(expert_batch) + len(learner_batch))


class GAILAgent:
    def __init__(self, state_dim, action_dim):
        self.state_dim, self.action_dim = state_dim, action_dim
        self.discriminator = Discriminator(state_dim, action_dim)
        self.policy_weights = np.random.randn(state_dim, action_dim) * 0.01
        self.lr = 0.001

    def get_action_probs(self, state):
        logits = state @ self.policy_weights
        exp_logits = np.exp(logits - np.max(logits))
        return exp_logits / np.sum(exp_logits)

    def select_action(self, state):
        probs = self.get_action_probs(state)
        return np.random.choice(len(probs), p=probs)

    def get_reward(self, state, action):
        d = self.discriminator.predict(state, action)[0]
        return -np.log(1 - d + 1e-8)  # 鼓励像专家

    def collect_trajectory(self, env):
        trajectory = []
        state = env.reset()
        done = False
        while not done:
            action = self.select_action(state)
            next_state, _, done = env.step(action)
            trajectory.append((state.copy(), action))
            state = next_state
        return trajectory

    def train(self, env, expert_data, n_iterations=100):
        for iteration in range(n_iterations):
            # 收集学习者轨迹
            learner_data = []
            for _ in range(10):
                traj = self.collect_trajectory(env)
                learner_data.extend(traj)

            # 训练判别器
            expert_batch = expert_data[:len(learner_data)]
            self.discriminator.train_step(expert_batch, learner_data)

            # 用判别器奖励训练策略 (简化的policy gradient)
            for state, action in learner_data:
                reward = self.get_reward(state, action)
                probs = self.get_action_probs(state)
                one_hot = np.zeros(self.action_dim)
                one_hot[action] = 1
                grad = np.outer(state, one_hot - probs)
                self.policy_weights += self.lr * reward * grad

            if iteration % 10 == 0:
                print(f"Iteration {iteration}")


print("✅ GAIL核心:")
print("  1. 判别器D: 区分专家vs学习者")
print("  2. 策略π: 生成像专家的行为")
print("  3. 对抗训练: min-max game")
print("  4. 隐式奖励: r = -log(1-D(s,a))")
print("\n优势:")
print("  - 不需要显式奖励函数")
print("  - 从未标注轨迹学习")
print("  - 理论上等价于IRL+RL")
print("\nRLHF联系:")
print("  - 对抗训练思想")
print("  - 从偏好/行为学习的理论基础")
print("2025年地位: 高级模仿学习方法，影响了RLHF的发展")
