"""解答: DPO (Direct Preference Optimization)"""
import numpy as np

class DPO:
    def __init__(self, state_dim, action_dim, beta=0.1, lr=0.0003):
        self.beta, self.lr = beta, lr
        self.policy_weights = np.random.randn(state_dim, action_dim) * 0.01
        self.ref_weights = self.policy_weights.copy()

    def get_action_probs(self, state, use_ref=False):
        weights = self.ref_weights if use_ref else self.policy_weights
        logits = state @ weights
        exp_logits = np.exp(logits - np.max(logits))
        return exp_logits / np.sum(exp_logits)

    def compute_log_ratio(self, state, action):
        pi = self.get_action_probs(state, use_ref=False)
        pi_ref = self.get_action_probs(state, use_ref=True)
        return np.log(pi[action] + 1e-8) - np.log(pi_ref[action] + 1e-8)

    def compute_dpo_loss(self, state, action_w, action_l):
        log_ratio_w = self.compute_log_ratio(state, action_w)
        log_ratio_l = self.compute_log_ratio(state, action_l)
        logits = self.beta * (log_ratio_w - log_ratio_l)
        # loss = -log σ(logits)
        return -np.log(1 / (1 + np.exp(-logits)) + 1e-8)

    def train_step(self, state, action_w, action_l):
        loss = self.compute_dpo_loss(state, action_w, action_l)

        # 简化的梯度更新
        log_ratio_w = self.compute_log_ratio(state, action_w)
        log_ratio_l = self.compute_log_ratio(state, action_l)
        logits = self.beta * (log_ratio_w - log_ratio_l)

        # σ(-logits) = 1 / (1 + exp(logits))
        grad_coef = 1 / (1 + np.exp(logits))

        # 更新策略 (简化)
        pi_w = self.get_action_probs(state)
        pi_l = self.get_action_probs(state)

        one_hot_w = np.zeros(len(pi_w))
        one_hot_w[action_w] = 1
        one_hot_l = np.zeros(len(pi_l))
        one_hot_l[action_l] = 1

        grad_w = np.outer(state, one_hot_w - pi_w)
        grad_l = np.outer(state, one_hot_l - pi_l)

        self.policy_weights += self.lr * self.beta * grad_coef * (grad_w - grad_l)

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


print("✅ DPO核心:")
print("  1. 直接优化: Preference -> Policy (跳过RM和RL)")
print("  2. 损失: -log σ(β·[log π/π_ref]_w - β·[log π/π_ref]_l)")
print("  3. 数学等价: DPO = RLHF的闭式解")
print("  4. 优势: 简单、稳定、高效")
print("\nRLHF vs DPO:")
print("  RLHF: SFT -> RM -> RL (三阶段)")
print("  DPO: SFT -> Direct Opt (一阶段)")
print("\n2025年地位: 快速流行，与RLHF互补")
print("应用: Llama 2, Mistral, Zephyr, many open-source LLMs")
print("论文: Rafailov et al. (2023), NeurIPS 2023")
