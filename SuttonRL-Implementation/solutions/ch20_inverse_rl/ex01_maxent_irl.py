"""解答: MaxEnt IRL"""
import numpy as np

class MaxEntIRL:
    def __init__(self, state_dim, action_dim, n_features, lr=0.01):
        self.theta = np.random.randn(n_features) * 0.01
        self.lr = lr

    def extract_features(self, state, action):
        return np.concatenate([state, [action]])

    def compute_reward(self, state, action):
        features = self.extract_features(state, action)
        return np.dot(self.theta, features)

    def compute_expert_feature_expectation(self, expert_trajectories):
        feature_sum = None
        count = 0
        for traj in expert_trajectories:
            for state, action in traj:
                features = self.extract_features(state, action)
                if feature_sum is None:
                    feature_sum = features
                else:
                    feature_sum += features
                count += 1
        return feature_sum / count if count > 0 else feature_sum

    def train(self, expert_data, env, n_iterations=100):
        expert_feature_exp = self.compute_expert_feature_expectation(expert_data)
        for iteration in range(n_iterations):
            # 简化: 假设有策略π_R，计算其特征期望
            # 实际需要用RL训练π_R
            learner_feature_exp = expert_feature_exp  # 简化
            grad = expert_feature_exp - learner_feature_exp
            self.theta += self.lr * grad
            if iteration % 10 == 0:
                print(f"Iteration {iteration}, θ: {self.theta}")


print("✅ MaxEnt IRL核心:")
print("  1. 假设: 专家遵循最大熵策略")
print("  2. 目标: 特征匹配 E_expert[φ] = E_π[φ]")
print("  3. 奖励: R(s,a) = θ^T φ(s,a)")
print("  4. 更新: θ += α(E_expert[φ] - E_π[φ])")
print("\nRLHF应用:")
print("  - 奖励建模的理论基础")
print("  - 从人类偏好推断奖励")
print("  - Bradley-Terry模型 (偏好对比)")
print("2025年地位: RLHF理论支撑，理解奖励学习的基础")
