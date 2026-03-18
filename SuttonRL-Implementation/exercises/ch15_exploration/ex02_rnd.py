"""
练习: RND (Random Network Distillation)

算法描述:
RND通过预测随机网络的输出来生成探索奖励。相比ICM更简单但同样有效。

核心思想:
- Random Target Network: f(s) 随机初始化，固定不变
- Predictor Network: f̂(s) 训练预测f(s)
- 内在奖励: r_i = ||f̂(s) - f(s)||²
- 新状态难预测 -> 高奖励 -> 鼓励探索

优势:
- 比ICM更简单（不需要inverse model）
- 不受环境随机性影响
- 训练稳定

参考: Burda et al. (2018) "Exploration by Random Network Distillation"
"""

import numpy as np

class RND:
    def __init__(self, state_dim, feature_dim=32, lr=0.001):
        self.state_dim, self.feature_dim, self.lr = state_dim, feature_dim, lr
        # Target network (固定)
        self.target_weights = np.random.randn(state_dim, feature_dim) * 0.01
        # Predictor network (训练)
        self.predictor_weights = np.random.randn(state_dim, feature_dim) * 0.01
    
    def target_forward(self, state):
        """Random target network (固定)"""
        # TODO: 实现目标网络前向传播
        pass  # TODO
    
    def predictor_forward(self, state):
        """Predictor network (训练)"""
        # TODO: 实现预测网络前向传播
        pass  # TODO
    
    def compute_intrinsic_reward(self, state):
        """计算内在奖励（预测误差）"""
        # TODO: 实现内在奖励计算
        pass  # TODO
    
    def update(self, state):
        """更新predictor network"""
        # TODO: 更新预测网络
        pass  # TODO

print("练习: 实现RND探索")
print("提示: Target固定，Predictor学习预测，新状态难预测=高奖励")
