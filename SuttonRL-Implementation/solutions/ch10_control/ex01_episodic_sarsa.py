"""
解答: 分节式半梯度SARSA

这是 ex01_episodic_sarsa.py 的完整实现解答
"""

import numpy as np


class MountainCar:
    """山地车环境（同练习）"""

    def __init__(self):
        self.min_position = -1.2
        self.max_position = 0.6
        self.max_speed = 0.07
        self.goal_position = 0.5
        self.n_actions = 3
        self.reset()

    def reset(self):
        self.position = -0.5
        self.velocity = 0.0
        return self._get_state()

    def _get_state(self):
        return np.array([self.position, self.velocity])

    def step(self, action):
        force = (action - 1) * 0.001
        self.velocity += force + np.cos(3 * self.position) * (-0.0025)
        self.velocity = np.clip(self.velocity, -self.max_speed, self.max_speed)
        self.position += self.velocity
        self.position = np.clip(self.position, self.min_position, self.max_position)

        if self.position == self.min_position and self.velocity < 0:
            self.velocity = 0

        done = self.position >= self.goal_position
        reward = 0.0 if done else -1.0

        return self._get_state(), reward, done


def tile_coding_features(state, action, n_tiles_per_dim=8):
    """Tile Coding特征"""
    # 简化的tile coding
    pos_idx = int((state[0] + 1.2) / 1.8 * n_tiles_per_dim)
    vel_idx = int((state[1] + 0.07) / 0.14 * n_tiles_per_dim)

    pos_idx = np.clip(pos_idx, 0, n_tiles_per_dim - 1)
    vel_idx = np.clip(vel_idx, 0, n_tiles_per_dim - 1)

    feature_dim = n_tiles_per_dim * n_tiles_per_dim * 3
    features = np.zeros(feature_dim)

    idx = action * (n_tiles_per_dim * n_tiles_per_dim) + pos_idx * n_tiles_per_dim + vel_idx
    features[idx] = 1

    return features


class LinearActionValueFunction:
    """线性动作值函数"""

    def __init__(self, feature_dim):
        self.w = np.zeros(feature_dim)

    def value(self, features):
        """q̂(s,a,w) = w^T x(s,a)"""
        return np.dot(self.w, features)

    def update(self, features, target, alpha):
        """梯度更新"""
        prediction = self.value(features)
        error = target - prediction
        self.w += alpha * error * features


def epsilon_greedy(q_func, state, epsilon, n_actions, feature_func):
    """ε-greedy策略"""
    if np.random.random() < epsilon:
        return np.random.randint(n_actions)
    else:
        q_values = []
        for a in range(n_actions):
            features = feature_func(state, a)
            q_values.append(q_func.value(features))
        return np.argmax(q_values)


def semi_gradient_sarsa(env, episodes=500, alpha=0.01, gamma=1.0, epsilon=0.1):
    """半梯度SARSA"""
    feature_dim = 8 * 8 * 3
    q_func = LinearActionValueFunction(feature_dim)
    feature_func = lambda s, a: tile_coding_features(s, a, n_tiles_per_dim=8)

    episode_lengths = []

    for episode in range(episodes):
        state = env.reset()
        action = epsilon_greedy(q_func, state, epsilon, env.n_actions, feature_func)
        steps = 0

        while True:
            steps += 1
            next_state, reward, done = env.step(action)

            features = feature_func(state, action)

            if done:
                # 终止状态更新
                td_target = reward
                q_func.update(features, td_target, alpha)
                break

            # 选择下一个动作
            next_action = epsilon_greedy(q_func, next_state, epsilon, env.n_actions, feature_func)
            next_features = feature_func(next_state, next_action)

            # SARSA更新
            td_target = reward + gamma * q_func.value(next_features)
            q_func.update(features, td_target, alpha)

            state = next_state
            action = next_action

        episode_lengths.append(steps)

    return q_func, episode_lengths


def test():
    """测试函数"""
    print("=" * 60)
    print("测试半梯度SARSA - Mountain Car [解答版本]")
    print("=" * 60)

    np.random.seed(42)

    env = MountainCar()

    print(f"\n开始训练...")

    q_func, episode_lengths = semi_gradient_sarsa(env, episodes=500, alpha=0.01, epsilon=0.1)

    early_avg = np.mean(episode_lengths[:50])
    late_avg = np.mean(episode_lengths[-50:])

    print(f"\n训练完成!")
    print(f"  前50回合平均步数: {early_avg:.1f}")
    print(f"  后50回合平均步数: {late_avg:.1f}")
    print(f"  改进: {early_avg - late_avg:.1f} 步")

    converges = late_avg < early_avg

    return {
        'converges': converges,
        'episode_length': late_avg,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n✅ 解答说明:")
    print(f"  1. tile_coding_features(): 离散化连续状态")
    print(f"  2. epsilon_greedy(): 基于q̂选择动作")
    print(f"  3. SARSA更新: w += α[R + γq̂(S',A') - q̂(S,A)]x(S,A)")
    print(f"  4. 函数近似使连续控制成为可能")
