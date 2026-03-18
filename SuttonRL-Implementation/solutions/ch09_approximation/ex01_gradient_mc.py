"""
解答: 梯度蒙特卡洛

这是 ex01_gradient_mc.py 的完整实现解答
"""

import numpy as np


class RandomWalk1000:
    """1000状态随机游走"""

    def __init__(self):
        self.n_states = 1002
        self.start_state = 500

    def reset(self):
        self.state = self.start_state
        return self.state

    def step(self):
        step = np.random.randint(1, 101)
        direction = np.random.choice([-1, 1])
        self.state += direction * step

        if self.state <= 0:
            return 0, -1, True
        elif self.state >= 1001:
            return 1001, 1, True
        else:
            return self.state, 0, False


def state_aggregation_features(state, n_groups=10):
    """状态聚合特征"""
    features = np.zeros(n_groups)

    if state == 0 or state == 1001:
        return features  # 终止状态

    # 计算状态属于哪一组
    group = min(int((state - 1) / (1000 / n_groups)), n_groups - 1)
    features[group] = 1

    return features


def polynomial_features(state, degree=5):
    """多项式特征"""
    s = state / 1001.0  # 归一化到[0, 1]
    features = np.array([s**i for i in range(degree + 1)])
    return features


class LinearValueFunction:
    """线性值函数"""

    def __init__(self, feature_dim):
        self.w = np.zeros(feature_dim)

    def value(self, features):
        """v̂(s,w) = w^T x(s)"""
        return np.dot(self.w, features)

    def update(self, features, target, alpha):
        """梯度更新: w ← w + α[G - v̂]∇v̂"""
        prediction = self.value(features)
        error = target - prediction
        # 梯度 = features (线性情况)
        self.w += alpha * error * features


def generate_episode(env, feature_func):
    """生成一个回合"""
    episode = []
    state = env.reset()
    done = False

    while not done:
        features = feature_func(state)
        next_state, reward, done = env.step()
        episode.append((features, reward))
        state = next_state

    return episode


def gradient_mc(env, value_func, feature_func, episodes=5000, alpha=0.01, gamma=1.0):
    """梯度蒙特卡洛"""
    for episode_num in range(episodes):
        # 生成回合
        episode = generate_episode(env, feature_func)

        # 计算回报并更新
        G = 0
        for t in range(len(episode) - 1, -1, -1):
            features, reward = episode[t]

            # 累积回报
            G = gamma * G + reward

            # 梯度更新
            value_func.update(features, G, alpha)

    return value_func


def test():
    """测试函数"""
    print("=" * 60)
    print("测试梯度MC - 1000-state Random Walk [解答版本]")
    print("=" * 60)

    np.random.seed(42)

    env = RandomWalk1000()

    print(f"\n使用状态聚合特征:")

    feature_dim = 10
    value_func = LinearValueFunction(feature_dim)
    feature_func = lambda s: state_aggregation_features(s, n_groups=10)

    value_func = gradient_mc(env, value_func, feature_func, episodes=5000, alpha=0.01)

    print(f"\n学到的权重:")
    print(value_func.w)

    print(f"\n示例状态值:")
    for state in [100, 300, 500, 700, 900]:
        features = feature_func(state)
        v = value_func.value(features)
        print(f"  V({state:3d}) = {v:6.3f}")

    true_value_500 = 0
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

    print(f"\n✅ 解答说明:")
    print(f"  1. state_aggregation_features(): 将状态分组")
    print(f"  2. generate_episode(): 生成完整回合")
    print(f"  3. gradient_mc(): 从后往前计算G并更新w")
    print(f"  4. 梯度更新: w += α[G - v̂(s,w)]x(s)")
