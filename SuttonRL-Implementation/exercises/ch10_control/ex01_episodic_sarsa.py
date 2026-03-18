"""
练习: 分节式半梯度SARSA (Episodic Semi-gradient SARSA)

算法描述:
半梯度SARSA将SARSA算法扩展到函数近似。使用参数化的动作值函数 q̂(s,a,w)
代替表格Q(s,a)，使其能处理大规模甚至连续状态空间。

核心思想:
- 参数化: q̂(s, a, w) = w^T x(s, a)  (线性情况)
- SARSA更新: w ← w + α[R + γq̂(S',A',w) - q̂(S,A,w)]∇q̂(S,A,w)
- 对于线性函数: ∇q̂(s,a,w) = x(s,a)

伪代码:
┌────────────────────────────────────────────────────┐
│ 输入: 可微分函数 q̂(·,·,w)                         │
│ 参数: 步长 α > 0, 小常数 ε > 0                     │
│ 初始化: 权重 w 任意值                              │
│                                                    │
│ 循环（对每个回合）:                                │
│   S ← 初始状态                                     │
│   A ~ ε-greedy(q̂(S,·,w))                           │
│                                                    │
│   循环（对回合中的每一步）:                        │
│     执行 A, 观察 R, S'                             │
│     if S' 是终止:                                  │
│       w ← w + α[R - q̂(S,A,w)]∇q̂(S,A,w)            │
│       跳出循环                                     │
│     A' ~ ε-greedy(q̂(S',·,w))                       │
│     w ← w + α[R+γq̂(S',A',w)-q̂(S,A,w)]∇q̂(S,A,w)   │
│     S ← S', A ← A'                                 │
└────────────────────────────────────────────────────┘

使用 Mountain Car 环境（简化版）:
- 状态: (位置, 速度) - 连续
- 动作: 左推(-1), 不动(0), 右推(+1)
- 目标: 到达右侧山顶
- 奖励: 每步-1（鼓励快速到达）

要求:
- 实现线性函数近似的动作值函数
- 实现半梯度SARSA
- 使用Tile Coding或RBF特征
- 解决连续状态空间问题

参考: Sutton & Barto 第10章, 第10.1节
"""

import numpy as np


class MountainCar:
    """山地车环境（简化版）"""

    def __init__(self):
        self.min_position = -1.2
        self.max_position = 0.6
        self.max_speed = 0.07
        self.goal_position = 0.5
        self.n_actions = 3  # 左、不动、右

        self.reset()

    def reset(self):
        """重置环境"""
        self.position = -0.5
        self.velocity = 0.0
        return self._get_state()

    def _get_state(self):
        """获取状态"""
        return np.array([self.position, self.velocity])

    def step(self, action):
        """
        执行动作

        Args:
            action: 0=左, 1=不动, 2=右

        Returns:
            state, reward, done
        """
        # 动作映射
        force = (action - 1) * 0.001  # -0.001, 0, 0.001

        # 更新速度
        self.velocity += force + np.cos(3 * self.position) * (-0.0025)
        self.velocity = np.clip(self.velocity, -self.max_speed, self.max_speed)

        # 更新位置
        self.position += self.velocity
        self.position = np.clip(self.position, self.min_position, self.max_position)

        # 左边界时速度归零
        if self.position == self.min_position and self.velocity < 0:
            self.velocity = 0

        # 检查终止
        done = self.position >= self.goal_position

        reward = -1.0
        if done:
            reward = 0.0

        return self._get_state(), reward, done


def tile_coding_features(state, action, n_tilings=8, n_tiles_per_dim=8):
    """
    Tile Coding 特征表示

    Args:
        state: [position, velocity]
        action: 动作 (0, 1, 2)
        n_tilings: tiling数量
        n_tiles_per_dim: 每个维度的tile数

    Returns:
        features: 稀疏特征向量
    """
    # TODO: 实现简化的Tile Coding
    # 提示1: 为简化，使用粗网格编码
    # 提示2: position范围 [-1.2, 0.6], velocity范围 [-0.07, 0.07]
    # 提示3: 将状态离散化到网格
    # 提示4: pos_idx = int((state[0] + 1.2) / 1.8 * n_tiles_per_dim)
    # 提示5: vel_idx = int((state[1] + 0.07) / 0.14 * n_tiles_per_dim)
    # 提示6: pos_idx = np.clip(pos_idx, 0, n_tiles_per_dim - 1)
    # 提示7: vel_idx = np.clip(vel_idx, 0, n_tiles_per_dim - 1)
    # 提示8: 创建特征向量（每个动作独立的特征）
    # 提示9: feature_dim = n_tiles_per_dim * n_tiles_per_dim * 3  # 3个动作
    # 提示10: features = np.zeros(feature_dim)
    # 提示11: idx = action * (n_tiles_per_dim * n_tiles_per_dim) + pos_idx * n_tiles_per_dim + vel_idx
    # 提示12: features[idx] = 1
    # 提示13: return features

    pass  # TODO: 删除这一行


class LinearActionValueFunction:
    """线性动作值函数"""

    def __init__(self, feature_dim):
        """
        初始化

        Args:
            feature_dim: 特征维度
        """
        self.w = np.zeros(feature_dim)

    def value(self, features):
        """
        计算 q̂(s, a, w) = w^T x(s, a)

        Args:
            features: 特征向量

        Returns:
            q值估计
        """
        # TODO: 实现q值计算
        # 提示: return np.dot(self.w, features)

        pass  # TODO: 删除这一行

    def update(self, features, target, alpha):
        """
        半梯度更新: w ← w + α[target - q̂]∇q̂

        Args:
            features: 特征向量 x(s, a)
            target: TD目标
            alpha: 学习率
        """
        # TODO: 实现梯度更新
        # 提示1: prediction = self.value(features)
        # 提示2: error = target - prediction
        # 提示3: self.w += alpha * error * features

        pass  # TODO: 删除这一行


def epsilon_greedy(q_func, state, epsilon, n_actions, feature_func):
    """
    ε-greedy策略

    Args:
        q_func: 动作值函数
        state: 当前状态
        epsilon: 探索概率
        n_actions: 动作数量
        feature_func: 特征函数

    Returns:
        action: 选择的动作
    """
    # TODO: 实现ε-greedy
    # 提示1: if np.random.random() < epsilon:
    # 提示2:   return np.random.randint(n_actions)
    # 提示3: else:
    # 提示4:   # 计算所有动作的q值
    # 提示5:   q_values = []
    # 提示6:   for a in range(n_actions):
    # 提示7:     features = feature_func(state, a)
    # 提示8:     q_values.append(q_func.value(features))
    # 提示9:   return np.argmax(q_values)

    pass  # TODO: 删除这一行


def semi_gradient_sarsa(env, episodes=500, alpha=0.01, gamma=1.0, epsilon=0.1):
    """
    分节式半梯度SARSA

    Args:
        env: 环境
        episodes: 回合数
        alpha: 学习率
        gamma: 折扣因子
        epsilon: 探索概率

    Returns:
        q_func: 学到的动作值函数
        episode_lengths: 每回合的步数
    """
    # 初始化
    feature_dim = 8 * 8 * 3  # tile coding特征维度
    q_func = LinearActionValueFunction(feature_dim)
    feature_func = lambda s, a: tile_coding_features(s, a, n_tiles_per_dim=8)

    episode_lengths = []

    # TODO: 实现半梯度SARSA主循环
    # 提示1: for episode in range(episodes):
    # 提示2:   state = env.reset()
    # 提示3:   action = epsilon_greedy(q_func, state, epsilon, env.n_actions, feature_func)
    # 提示4:   steps = 0
    # 提示5:
    # 提示6:   while True:
    # 提示7:     steps += 1
    # 提示8:     next_state, reward, done = env.step(action)
    # 提示9:
    # 提示10:    features = feature_func(state, action)
    # 提示11:
    # 提示12:    if done:
    # 提示13:      # 终止状态更新
    # 提示14:      td_target = reward
    # 提示15:      q_func.update(features, td_target, alpha)
    # 提示16:      break
    # 提示17:
    # 提示18:    # 选择下一个动作
    # 提示19:    next_action = epsilon_greedy(q_func, next_state, epsilon, env.n_actions, feature_func)
    # 提示20:    next_features = feature_func(next_state, next_action)
    # 提示21:
    # 提示22:    # SARSA更新
    # 提示23:    td_target = reward + gamma * q_func.value(next_features)
    # 提示24:    q_func.update(features, td_target, alpha)
    # 提示25:
    # 提示26:    state = next_state
    # 提示27:    action = next_action
    # 提示28:
    # 提示29:  episode_lengths.append(steps)

    pass  # TODO: 删除这一行

    return q_func, episode_lengths


def test():
    """测试函数"""
    print("=" * 60)
    print("测试半梯度SARSA - Mountain Car")
    print("=" * 60)

    np.random.seed(42)

    env = MountainCar()

    print(f"\n开始训练...")
    print(f"  回合数: 500")
    print(f"  学习率: 0.01")
    print(f"  探索率: 0.1")

    q_func, episode_lengths = semi_gradient_sarsa(env, episodes=500, alpha=0.01, epsilon=0.1)

    # 分析结果
    early_avg = np.mean(episode_lengths[:50])
    late_avg = np.mean(episode_lengths[-50:])

    print(f"\n训练完成!")
    print(f"  前50回合平均步数: {early_avg:.1f}")
    print(f"  后50回合平均步数: {late_avg:.1f}")
    print(f"  改进: {early_avg - late_avg:.1f} 步")

    # 验证学习
    converges = late_avg < early_avg

    return {
        'converges': converges,
        'episode_length': late_avg,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n提示:")
    print(f"  - 函数近似使SARSA能处理连续状态")
    print(f"  - Tile Coding是有效的特征表示")
    print(f"  - 半梯度方法实践中很稳定")
    print(f"  - Mountain Car是经典的连续控制问题")
