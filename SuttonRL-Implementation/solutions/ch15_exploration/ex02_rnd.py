"""解答: RND"""
import numpy as np

class RND:
    def __init__(self, state_dim, feature_dim=32, lr=0.001):
        self.state_dim, self.feature_dim, self.lr = state_dim, feature_dim, lr
        self.target_weights = np.random.randn(state_dim, feature_dim) * 0.01
        self.predictor_weights = np.random.randn(state_dim, feature_dim) * 0.01
    
    def target_forward(self, state):
        state_onehot = np.zeros(self.state_dim)
        state_onehot[state] = 1
        return state_onehot @ self.target_weights
    
    def predictor_forward(self, state):
        state_onehot = np.zeros(self.state_dim)
        state_onehot[state] = 1
        return state_onehot @ self.predictor_weights
    
    def compute_intrinsic_reward(self, state):
        target_output = self.target_forward(state)
        predictor_output = self.predictor_forward(state)
        return np.sum((predictor_output - target_output)**2)
    
    def update(self, state):
        target_output = self.target_forward(state)
        predictor_output = self.predictor_forward(state)
        error = predictor_output - target_output
        state_onehot = np.zeros(self.state_dim)
        state_onehot[state] = 1
        self.predictor_weights -= self.lr * np.outer(state_onehot, error)
        return np.sum(error**2)

print("✅ RND核心:")
print("  1. Target Network f(s): 随机初始化，固定")
print("  2. Predictor f̂(s): 训练预测f(s)")
print("  3. r_int = ||f̂(s) - f(s)||²")
print("\n优势: 比ICM简单，不受环境噪声影响")
print("2025年地位: OpenAI在Montezuma's Revenge上的突破")
