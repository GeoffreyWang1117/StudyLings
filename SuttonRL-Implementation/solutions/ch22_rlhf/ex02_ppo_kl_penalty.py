"""解答: PPO with KL Penalty"""
import numpy as np

class PPO_KL:
    def __init__(self, state_dim, action_dim, beta=0.1, lr=0.0003):
        self.beta, self.lr = beta, lr
        self.policy_weights = np.random.randn(state_dim, action_dim) * 0.01
        self.sft_weights = self.policy_weights.copy()
        self.value_weights = np.random.randn(state_dim) * 0.01

    def get_action_probs(self, state, use_sft=False):
        weights = self.sft_weights if use_sft else self.policy_weights
        logits = state @ weights
        exp_logits = np.exp(logits - np.max(logits))
        return exp_logits / np.sum(exp_logits)

    def compute_kl_divergence(self, state):
        pi = self.get_action_probs(state, use_sft=False)
        pi_sft = self.get_action_probs(state, use_sft=True)
        # KL(π||π_SFT) = Σ π log(π/π_SFT)
        kl = np.sum(pi * np.log((pi + 1e-8) / (pi_sft + 1e-8)))
        return kl

    def compute_reward_with_kl(self, state, action, reward_model):
        r_rm = reward_model.compute_reward(state, action)
        kl = self.compute_kl_divergence(state)
        return r_rm - self.beta * kl

    def train_step(self, batch, reward_model):
        # 简化的PPO更新
        for state, action, old_prob in batch:
            # 计算带KL的奖励
            reward = self.compute_reward_with_kl(state, action, reward_model)

            # 计算ratio
            new_probs = self.get_action_probs(state)
            ratio = new_probs[action] / (old_prob + 1e-8)

            # PPO clip
            advantage = reward  # 简化: 用reward作为advantage
            clip_ratio = np.clip(ratio, 0.8, 1.2)
            loss = -min(ratio * advantage, clip_ratio * advantage)

            # 更新策略 (简化)
            one_hot = np.zeros(len(new_probs))
            one_hot[action] = 1
            grad = np.outer(state, one_hot - new_probs)
            self.policy_weights += self.lr * advantage * grad

        return loss


print("✅ PPO with KL核心:")
print("  1. 目标: max E[r(x,y) - β·KL(π||π_SFT)]")
print("  2. KL penalty: 防止过度偏离SFT")
print("  3. PPO: 稳定的策略优化")
print("  4. β: 控制探索vs保守")
print("\nRLHF完整流程:")
print("  SFT -> RM -> PPO+KL -> Aligned LLM")
print("\n2025年地位: ChatGPT/Claude/GPT-4的核心训练方法")
print("应用: 所有对齐的LLM (InstructGPT, ChatGPT, Claude等)")
