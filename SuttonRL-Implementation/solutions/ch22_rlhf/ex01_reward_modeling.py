"""解答: Reward Modeling"""
import numpy as np

class RewardModel:
    def __init__(self, state_dim, action_dim, lr=0.001):
        self.state_dim, self.action_dim, self.lr = state_dim, action_dim, lr
        self.weights = np.random.randn(state_dim + action_dim) * 0.01

    def compute_reward(self, state, action):
        features = np.concatenate([state, action])
        return np.dot(self.weights, features)

    def predict_preference(self, state, action_w, action_l):
        r_w = self.compute_reward(state, action_w)
        r_l = self.compute_reward(state, action_l)
        return 1 / (1 + np.exp(-(r_w - r_l)))  # sigmoid(r_w - r_l)

    def train_step(self, state, action_w, action_l):
        r_w = self.compute_reward(state, action_w)
        r_l = self.compute_reward(state, action_l)

        # Loss: -log σ(r_w - r_l)
        prob = 1 / (1 + np.exp(-(r_w - r_l)))
        loss = -np.log(prob + 1e-8)

        # 梯度: σ(r_l - r_w) * (feature_w - feature_l)
        grad_coef = 1 / (1 + np.exp(-(r_l - r_w)))  # σ(r_l - r_w)
        feature_w = np.concatenate([state, action_w])
        feature_l = np.concatenate([state, action_l])
        grad = grad_coef * (feature_w - feature_l)

        # 更新
        self.weights += self.lr * grad

        return loss

    def train(self, preference_data, epochs=100, batch_size=32):
        history = []
        for epoch in range(epochs):
            np.random.shuffle(preference_data)
            epoch_loss = 0
            for i in range(0, len(preference_data), batch_size):
                batch = preference_data[i:i+batch_size]
                batch_loss = 0
                for state, action_w, action_l in batch:
                    loss = self.train_step(state, action_w, action_l)
                    batch_loss += loss
                epoch_loss += batch_loss / len(batch)

            avg_loss = epoch_loss / (len(preference_data) // batch_size + 1)
            history.append(avg_loss)
            if epoch % 10 == 0:
                print(f"Epoch {epoch}, Loss: {avg_loss:.4f}")

        return history

    def evaluate(self, test_data):
        correct = 0
        for state, action_w, action_l in test_data:
            prob = self.predict_preference(state, action_w, action_l)
            if prob > 0.5:
                correct += 1
        return correct / len(test_data)


print("✅ Reward Modeling核心:")
print("  1. Bradley-Terry: P(y_w>y_l) = σ(r_w - r_l)")
print("  2. 训练目标: max log σ(r_w - r_l)")
print("  3. 输入: 偏好对比 (x, y_w, y_l)")
print("  4. 输出: 奖励函数 r(x,y)")
print("\nRLHF三阶段:")
print("  1. SFT: 监督微调 (BC)")
print("  2. RM: 奖励建模 (本算法)")
print("  3. RL: PPO with KL penalty")
print("\n2025年地位: 所有对齐LLM的核心技术")
print("应用: ChatGPT, Claude, GPT-4, Gemini, Llama 2/3等")
