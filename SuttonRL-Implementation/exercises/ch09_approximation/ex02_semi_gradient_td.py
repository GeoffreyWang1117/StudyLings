"""
练习: 半梯度TD (Semi-gradient TD(0))

算法描述:
半梯度TD结合了TD学习和函数近似。称为"半梯度"是因为只对当前估计求梯度，
而不对目标（包含下一状态的值）求梯度。

核心思想:
- TD目标: R + γv̂(S', w)
- 梯度更新: w ← w + α[R + γv̂(S', w) - v̂(S, w)]∇v̂(S, w)
- 比MC更低方差，更快学习

伪代码:
┌────────────────────────────────────────────────────┐
│ 输入: 策略 π, 可微分函数 v̂(·, w)                  │
│ 初始化: 权重 w 任意值                              │
│                                                    │
│ 循环（对每个回合）:                                │
│   初始化 S                                         │
│   对回合中的每一步:                                │
│     A ~ π(·|S)                                     │
│     执行 A, 观察 R, S'                             │
│     w ← w + α[R + γv̂(S',w) - v̂(S,w)]∇v̂(S,w)      │
│     S ← S'                                         │
│   直到 S 是终止状态                                │
└────────────────────────────────────────────────────┘

使用 1000-state Random Walk

要求:
- 实现半梯度TD(0)
- 使用线性函数近似
- 比较与梯度MC的学习速度
- 观察在线学习的效果

参考: Sutton & Barto 第9章, 第9.3节
"""

import numpy as np


class RandomWalk1000:
    """1000状态随机游走（同 ex01）"""

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
    group = min(int((state - 1) / (1000 / n_groups)), n_groups - 1)
    features[group] = 1
    return features


class LinearValueFunction:
    """线性值函数（同 ex01）"""

    def __init__(self, feature_dim):
        self.w = np.zeros(feature_dim)

    def value(self, features):
        return np.dot(self.w, features)

    def update(self, features, target, alpha):
        prediction = self.value(features)
        error = target - prediction
        self.w += alpha * error * features


def semi_gradient_td0(env, value_func, feature_func, episodes=5000, alpha=0.01, gamma=1.0):
    """
    半梯度TD(0)算法

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
    # TODO: 实现半梯度TD(0)
    # 提示1: for episode in range(episodes):
    # 提示2:   state = env.reset()
    # 提示3:   features = feature_func(state)
    # 提示4:   done = False
    # 提示5:
    # 提示6:   while not done:
    # 提示7:     next_state, reward, done = env.step()
    # 提示8:     next_features = feature_func(next_state)
    # 提示9:
    # 提示10:    # 计算TD目标
    # 提示11:    if done:
    # 提示12:      td_target = reward  # 终止状态值为0
    # 提示13:    else:
    # 提示14:      td_target = reward + gamma * value_func.value(next_features)
    # 提示15:
    # 提示16:    # 半梯度更新
    # 提示17:    value_func.update(features, td_target, alpha)
    # 提示18:
    # 提示19:    state = next_state
    # 提示20:    features = next_features

    pass  # TODO: 删除这一行

    return value_func


def test():
    """测试函数"""
    print("=" * 60)
    print("测试半梯度TD(0) - 1000-state Random Walk")
    print("=" * 60)

    np.random.seed(42)

    env = RandomWalk1000()

    print(f"\n使用状态聚合特征 (10组):")
    print("=" * 60)

    feature_dim = 10
    value_func = LinearValueFunction(feature_dim)
    feature_func = lambda s: state_aggregation_features(s, n_groups=10)

    print(f"\n开始训练 (5000回合)...")

    value_func = semi_gradient_td0(env, value_func, feature_func, episodes=5000, alpha=0.01)

    print(f"\n学到的权重:")
    print(value_func.w)

    # 评估状态值
    print(f"\n示例状态值:")
    for state in [100, 300, 500, 700, 900]:
        features = feature_func(state)
        v = value_func.value(features)
        true_v = 2 * state / 1001 - 1
        print(f"  V({state:3d}) = {v:6.3f}  (真实 ≈ {true_v:6.3f})")

    # 验证
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

    print(f"\n提示:")
    print(f"  - 半梯度TD比MC学习更快")
    print(f"  - 在线学习，每步都更新")
    print(f"  - 称为'半梯度'因为不对目标求梯度")
    print(f"  - 实践中非常有效")
