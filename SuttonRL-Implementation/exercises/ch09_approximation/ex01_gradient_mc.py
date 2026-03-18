"""
练习: 梯度蒙特卡洛 (Gradient Monte Carlo with Function Approximation)

算法描述:
当状态空间很大时，无法用表格表示值函数。函数近似使用参数化函数 v̂(s, w)
来近似真实值函数。梯度MC使用梯度下降最小化均方误差。

核心思想:
- 参数化值函数: v̂(s, w) = w^T x(s)  (线性情况)
- 目标: 最小化 J(w) = E[(v_π(S) - v̂(S, w))^2]
- 梯度下降: w ← w + α[G_t - v̂(S_t, w)]∇v̂(S_t, w)

对于线性函数近似:
    v̂(s, w) = w^T x(s)
    ∇v̂(s, w) = x(s)

伪代码:
┌────────────────────────────────────────────────────┐
│ 输入: 策略 π, 可微分函数 v̂(·, w)                  │
│ 初始化: 权重 w 任意值                              │
│                                                    │
│ 循环（对每个回合）:                                │
│   生成回合: S_0, A_0, R_1, ..., S_T                │
│   对回合中的每一步 t = 0, ..., T-1:                │
│     G_t ← Σ_{k=t+1}^T γ^{k-t-1} R_k               │
│     w ← w + α[G_t - v̂(S_t, w)]∇v̂(S_t, w)          │
└────────────────────────────────────────────────────┘

使用 1000-state Random Walk:
- 状态: 0, 1, ..., 1001 (1-1000是非终止)
- 起始: 状态500
- 动作: 左右随机游走 (步长1-100随机)
- 奖励: 到达0获得-1，到达1001获得+1
- 特征: 状态聚合或多项式基函数

要求:
- 实现线性函数近似
- 实现梯度MC算法
- 使用特征表示（如状态聚合）
- 比较不同特征的效果

参考: Sutton & Barto 第9章, 第9.3节
"""

import numpy as np


class RandomWalk1000:
    """1000状态随机游走"""

    def __init__(self):
        self.n_states = 1002  # 0 和 1001 是终止状态
        self.start_state = 500

    def reset(self):
        """重置环境"""
        self.state = self.start_state
        return self.state

    def step(self):
        """
        随机游走一步

        Returns:
            next_state, reward, done
        """
        # 随机选择方向和步长
        step = np.random.randint(1, 101)  # 1-100
        direction = np.random.choice([-1, 1])

        self.state += direction * step

        # 检查终止
        if self.state <= 0:
            return 0, -1, True
        elif self.state >= 1001:
            return 1001, 1, True
        else:
            return self.state, 0, False


def state_aggregation_features(state, n_groups=10):
    """
    状态聚合特征

    将1000个状态分成 n_groups 组，每组用一个特征表示

    Args:
        state: 状态 (0-1001)
        n_groups: 分组数量

    Returns:
        features: 特征向量 (one-hot)
    """
    # TODO: 实现状态聚合特征
    # 提示1: 创建 n_groups 维的特征向量
    # 提示2: features = np.zeros(n_groups)
    # 提示3: 计算状态属于哪一组: group = min(int(state / (1002 / n_groups)), n_groups - 1)
    # 提示4: 设置对应特征为1: features[group] = 1
    # 提示5: return features

    pass  # TODO: 删除这一行，实现特征函数


def polynomial_features(state, degree=5):
    """
    多项式基函数特征

    Args:
        state: 状态
        degree: 多项式阶数

    Returns:
        features: [1, s, s^2, ..., s^degree]
    """
    # TODO: 实现多项式特征
    # 提示1: 归一化状态到 [0, 1]: s = state / 1001.0
    # 提示2: 创建特征: features = np.array([s**i for i in range(degree + 1)])
    # 提示3: return features

    pass  # TODO: 删除这一行，实现多项式特征


class LinearValueFunction:
    """线性值函数近似"""

    def __init__(self, feature_dim):
        """
        初始化

        Args:
            feature_dim: 特征维度
        """
        self.w = np.zeros(feature_dim)

    def value(self, features):
        """
        计算状态值 v̂(s, w) = w^T x(s)

        Args:
            features: 特征向量

        Returns:
            值估计
        """
        # TODO: 实现值计算
        # 提示: return np.dot(self.w, features)

        pass  # TODO: 删除这一行

    def update(self, features, target, alpha):
        """
        梯度更新: w ← w + α[G - v̂(s, w)]∇v̂(s, w)

        对于线性函数，∇v̂(s, w) = x(s)

        Args:
            features: 特征向量 x(s)
            target: 目标值 G
            alpha: 学习率
        """
        # TODO: 实现梯度更新
        # 提示1: 计算预测值: prediction = self.value(features)
        # 提示2: 计算误差: error = target - prediction
        # 提示3: 梯度: gradient = features  (线性情况下)
        # 提示4: 更新权重: self.w += alpha * error * gradient

        pass  # TODO: 删除这一行


def generate_episode(env, feature_func):
    """
    生成一个回合

    Args:
        env: 环境
        feature_func: 特征函数

    Returns:
        episode: [(features, reward), ...]
    """
    # TODO: 实现回合生成
    # 提示1: episode = []
    # 提示2: state = env.reset()
    # 提示3: done = False
    # 提示4: while not done:
    # 提示5:   features = feature_func(state)
    # 提示6:   next_state, reward, done = env.step()
    # 提示7:   episode.append((features, reward))
    # 提示8:   state = next_state
    # 提示9: return episode

    pass  # TODO: 删除这一行


def gradient_mc(env, value_func, feature_func, episodes=5000, alpha=0.01, gamma=1.0):
    """
    梯度蒙特卡洛算法

    Args:
        env: 环境
        value_func: 值函数对象
        feature_func: 特征函数
        episodes: 回合数
        alpha: 学习率
        gamma: 折扣因子

    Returns:
        value_func: 训练后的值函数
    """
    # TODO: 实现梯度MC
    # 提示1: for episode_num in range(episodes):
    # 提示2:   episode = generate_episode(env, feature_func)
    # 提示3:   G = 0
    # 提示4:   # 从后往前计算回报
    # 提示5:   for t in range(len(episode) - 1, -1, -1):
    # 提示6:     features, reward = episode[t]
    # 提示7:     G = gamma * G + reward
    # 提示8:     # 梯度更新
    # 提示9:     value_func.update(features, G, alpha)

    pass  # TODO: 删除这一行

    return value_func


def test():
    """测试函数"""
    print("=" * 60)
    print("测试梯度MC - 1000-state Random Walk")
    print("=" * 60)

    np.random.seed(42)

    env = RandomWalk1000()

    # 测试状态聚合特征
    print(f"\n使用状态聚合特征 (10组):")
    print("=" * 60)

    feature_dim = 10
    value_func = LinearValueFunction(feature_dim)
    feature_func = lambda s: state_aggregation_features(s, n_groups=10)

    value_func = gradient_mc(env, value_func, feature_func, episodes=5000, alpha=0.01)

    # 打印学到的值函数
    print(f"\n学到的权重:")
    print(value_func.w)

    # 评估一些状态
    print(f"\n示例状态值:")
    for state in [100, 300, 500, 700, 900]:
        features = feature_func(state)
        v = value_func.value(features)
        print(f"  V({state:3d}) = {v:6.3f}")

    # 真实值应该近似线性: V(s) ≈ 2s/1001 - 1
    true_value_500 = 2 * 500 / 1001 - 1
    estimated_value_500 = value_func.value(feature_func(500))
    error = abs(estimated_value_500 - true_value_500)

    print(f"\n状态500:")
    print(f"  真实值 ≈ {true_value_500:.3f}")
    print(f"  估计值 = {estimated_value_500:.3f}")
    print(f"  误差 = {error:.3f}")

    return {
        'converges': error < 0.3,
        'value_error': error,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n提示:")
    print(f"  - 函数近似用于大状态空间")
    print(f"  - 线性函数: v̂(s,w) = w^T x(s)")
    print(f"  - 特征工程很重要")
    print(f"  - 状态聚合是最简单的特征表示")
