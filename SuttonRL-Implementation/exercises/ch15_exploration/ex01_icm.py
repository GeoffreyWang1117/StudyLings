"""
练习: ICM (Intrinsic Curiosity Module)

算法描述:
ICM通过预测环境动态来生成内在奖励，鼓励智能体探索新奇状态。
这是2025年稀疏奖励环境中最常用的探索方法之一。

核心思想:
- Forward Model: 预测 φ(s_{t+1}) = f(φ(s_t), a_t)
- Inverse Model: 预测动作 â = g(φ(s_t), φ(s_{t+1}))
- 内在奖励: r_i = ||φ(s_{t+1}) - f(φ(s_t), a_t)||²
- 总奖励: r_total = r_e + β·r_i

优势:
- 自动探索新奇状态
- 对环境动态建模
- 适用于稀疏奖励

应用:
- 视频游戏（如Montezuma's Revenge）
- 机器人探索
- 好奇心驱动学习

参考: Pathak et al. (2017) "Curiosity-driven Exploration by Self-supervised Prediction"
"""

import numpy as np


class GridWorldExploration:
    """需要探索的网格世界"""
    def __init__(self, size=10):
        self.size = size
        self.n_states = size * size
        self.n_actions = 4  # 上下左右
        self.goal = (size-1, size-1)
        self.reset()

    def reset(self):
        self.pos = (0, 0)
        self.visited = set([self.pos])
        return self._state_index(self.pos)

    def step(self, action):
        row, col = self.pos
        if action == 0: row = max(0, row - 1)
        elif action == 1: row = min(self.size - 1, row + 1)
        elif action == 2: col = max(0, col - 1)
        elif action == 3: col = min(self.size - 1, col + 1)
        
        self.pos = (row, col)
        self.visited.add(self.pos)
        
        # 外在奖励：到达目标
        extrinsic_reward = 1.0 if self.pos == self.goal else 0.0
        done = (self.pos == self.goal)
        
        return self._state_index(self.pos), extrinsic_reward, done

    def _state_index(self, pos):
        return pos[0] * self.size + pos[1]


class ICM:
    """Intrinsic Curiosity Module"""
    def __init__(self, state_dim, action_dim, feature_dim=32, lr=0.001):
        """
        初始化
        
        Args:
            state_dim: 状态维度
            action_dim: 动作维度
            feature_dim: 特征维度
            lr: 学习率
        """
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.feature_dim = feature_dim
        self.lr = lr
        
        # 特征提取器（简化为线性）
        self.feature_weights = np.random.randn(state_dim, feature_dim) * 0.01
        
        # Forward Model: φ(s'), a -> φ(s_{t+1})预测
        self.forward_weights = np.random.randn(feature_dim + action_dim, feature_dim) * 0.01
        
        # Inverse Model: φ(s), φ(s') -> a预测
        self.inverse_weights = np.random.randn(feature_dim * 2, action_dim) * 0.01

    def encode_state(self, state):
        """提取状态特征"""
        # TODO: 实现特征提取
        # 提示1: 将状态编码为one-hot
        # 提示2: state_onehot = np.zeros(self.state_dim)
        # 提示3: state_onehot[state] = 1
        # 提示4: features = state_onehot @ self.feature_weights
        # 提示5: return features
        pass  # TODO

    def forward_model(self, state_features, action):
        """Forward Model: 预测下一状态特征"""
        # TODO: 实现forward model
        # 提示1: 创建动作one-hot
        # 提示2: action_onehot = np.zeros(self.action_dim)
        # 提示3: action_onehot[action] = 1
        # 提示4: 拼接特征和动作
        # 提示5: input_vec = np.concatenate([state_features, action_onehot])
        # 提示6: predicted_next = input_vec @ self.forward_weights
        # 提示7: return predicted_next
        pass  # TODO

    def inverse_model(self, state_features, next_state_features):
        """Inverse Model: 预测动作"""
        # TODO: 实现inverse model
        # 提示1: 拼接当前和下一状态特征
        # 提示2: input_vec = np.concatenate([state_features, next_state_features])
        # 提示3: logits = input_vec @ self.inverse_weights
        # 提示4: 使用softmax
        # 提示5: exp_logits = np.exp(logits - np.max(logits))
        # 提示6: probs = exp_logits / np.sum(exp_logits)
        # 提示7: return probs
        pass  # TODO

    def compute_intrinsic_reward(self, state, action, next_state):
        """
        计算内在奖励
        
        Args:
            state: 当前状态
            action: 动作
            next_state: 下一状态
            
        Returns:
            intrinsic_reward: 内在奖励（预测误差）
        """
        # TODO: 计算内在奖励
        # 提示1: 提取特征
        # 提示2: state_features = self.encode_state(state)
        # 提示3: next_state_features = self.encode_state(next_state)
        # 提示4: 前向预测
        # 提示5: predicted_next = self.forward_model(state_features, action)
        # 提示6: 计算预测误差作为内在奖励
        # 提示7: intrinsic_reward = np.sum((predicted_next - next_state_features)**2)
        # 提示8: return intrinsic_reward
        pass  # TODO

    def update(self, state, action, next_state):
        """更新ICM模型"""
        # 简化版本更新
        state_features = self.encode_state(state)
        next_state_features = self.encode_state(next_state)
        
        # Forward model loss
        predicted_next = self.forward_model(state_features, action)
        forward_error = predicted_next - next_state_features
        
        # Inverse model loss
        action_probs = self.inverse_model(state_features, next_state_features)
        
        # 简化的梯度更新（实际应该用反向传播）
        # 这里只是示意性更新
        action_onehot = np.zeros(self.action_dim)
        action_onehot[action] = 1
        inverse_error = action_onehot - action_probs
        
        return np.sum(forward_error**2), -np.sum(action_onehot * np.log(action_probs + 1e-10))


def icm_exploration(env, episodes=500, beta=0.2):
    """
    使用ICM的探索
    
    Args:
        env: 环境
        episodes: 回合数
        beta: 内在奖励权重
        
    Returns:
        exploration_coverage: 探索覆盖率
    """
    state_dim = env.n_states
    action_dim = env.n_actions
    
    icm = ICM(state_dim, action_dim, feature_dim=32)
    
    # 简单的Q-learning + ICM
    Q = np.zeros((state_dim, action_dim))
    alpha = 0.1
    gamma = 0.99
    epsilon = 0.1
    
    all_visited = set()
    
    # TODO: 实现ICM探索主循环
    # 提示: 使用 r_total = r_extrinsic + beta * r_intrinsic
    pass  # TODO
    
    coverage = len(all_visited) / env.n_states
    return coverage, all_visited


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 ICM - GridWorld Exploration")
    print("=" * 60)
    
    np.random.seed(42)
    env = GridWorldExploration(size=10)
    
    print(f"\n环境: {env.size}x{env.size} GridWorld")
    print(f"总状态数: {env.n_states}")
    print(f"\n开始探索 (500回合)...")
    
    coverage, visited = icm_exploration(env, episodes=500, beta=0.2)
    
    print(f"\n探索结果:")
    print(f"  访问状态数: {len(visited)}/{env.n_states}")
    print(f"  覆盖率: {coverage:.1%}")
    
    return {
        'coverage': coverage,
        'explores_well': coverage > 0.5,
    }


if __name__ == '__main__':
    result = test()
    
    print(f"\n提示:")
    print(f"  - ICM通过预测误差生成内在奖励")
    print(f"  - 鼓励探索新奇、难预测的状态")
    print(f"  - Forward Model预测下一状态特征")
    print(f"  - Inverse Model预测动作（辅助训练）")
    print(f"\n2025年应用:")
    print(f"  - 稀疏奖励游戏（Montezuma's Revenge）")
    print(f"  - 机器人探索未知环境")
    print(f"  - 好奇心驱动的强化学习")
