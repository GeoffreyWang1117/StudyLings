"""
练习: 半梯度Off-Policy方法 (Semi-gradient Off-policy TD)

算法描述:
Off-policy方法在函数近似下变得更加复杂。需要使用重要性采样比率
来修正行为策略和目标策略之间的差异。

核心思想:
- 行为策略 b(a|s): 生成数据的策略
- 目标策略 π(a|s): 我们想学习的策略
- 重要性采样比率: ρ = π(A|S) / b(A|S)
- 更新: w ← w + α ρ [R + γq̂(S',A',w) - q̂(S,A,w)]∇q̂(S,A,w)

警告：致命三元组
函数近似 + Off-policy + Bootstrapping 可能导致发散！

伪代码:
┌────────────────────────────────────────────────────┐
│ 输入: 目标策略 π, 行为策略 b                       │
│ 初始化: 权重 w 任意值                              │
│                                                    │
│ 循环（对每个回合）:                                │
│   初始化 S                                         │
│   A ~ b(·|S)                                       │
│                                                    │
│   循环（对回合中的每一步）:                        │
│     执行 A, 观察 R, S'                             │
│     A' ~ b(·|S')                                   │
│                                                    │
│     ρ ← π(A|S) / b(A|S)                            │
│                                                    │
│     if S' 是终止:                                  │
│       w ← w + α ρ [R - q̂(S,A,w)]∇q̂(S,A,w)         │
│       跳出循环                                     │
│                                                    │
│     w ← w + α ρ [R+γq̂(S',π(S'),w)-q̂(S,A,w)]∇q̂(S,A,w)│
│     S ← S', A ← A'                                 │
└────────────────────────────────────────────────────┘

使用简化的Random Walk环境

要求:
- 实现重要性采样比率计算
- 实现半梯度off-policy TD
- 观察发散问题（如果发生）
- 比较on-policy和off-policy的稳定性

参考: Sutton & Barto 第11章, 第11.2节
"""

import numpy as np


class RandomWalk:
    """Random Walk 环境"""

    def __init__(self, n_states=19):
        """
        初始化

        Args:
            n_states: 非终止状态数量
        """
        self.n_states = n_states + 2  # 包括两个终止状态
        self.start_state = n_states // 2 + 1
        self.n_actions = 2  # 左、右

    def reset(self):
        self.state = self.start_state
        return self.state

    def step(self, action):
        """
        执行动作

        Args:
            action: 0=左, 1=右

        Returns:
            next_state, reward, done
        """
        if action == 0:  # 左
            self.state -= 1
        else:  # 右
            self.state += 1

        if self.state == 0:
            return 0, -1, True
        elif self.state == self.n_states - 1:
            return self.n_states - 1, 1, True
        else:
            return self.state, 0, False


def tabular_features(state, action, n_states, n_actions):
    """
    表格特征（用于验证算法）

    Args:
        state: 状态
        action: 动作
        n_states: 状态数
        n_actions: 动作数

    Returns:
        features: one-hot特征
    """
    # TODO: 实现表格特征
    # 提示1: feature_dim = n_states * n_actions
    # 提示2: features = np.zeros(feature_dim)
    # 提示3: idx = state * n_actions + action
    # 提示4: features[idx] = 1
    # 提示5: return features

    pass  # TODO: 删除这一行


class LinearActionValueFunction:
    """线性动作值函数"""

    def __init__(self, feature_dim):
        self.w = np.zeros(feature_dim)

    def value(self, features):
        return np.dot(self.w, features)

    def update(self, features, target, alpha, rho=1.0):
        """
        Off-policy更新: w ← w + α ρ [target - q̂]∇q̂

        Args:
            features: 特征
            target: TD目标
            alpha: 学习率
            rho: 重要性采样比率
        """
        # TODO: 实现off-policy更新
        # 提示1: prediction = self.value(features)
        # 提示2: error = target - prediction
        # 提示3: self.w += alpha * rho * error * features

        pass  # TODO: 删除这一行


def greedy_policy(q_func, state, n_actions, feature_func):
    """
    贪心策略（目标策略）

    Args:
        q_func: 动作值函数
        state: 状态
        n_actions: 动作数
        feature_func: 特征函数

    Returns:
        action: 贪心动作
    """
    # TODO: 实现贪心策略
    # 提示1: q_values = []
    # 提示2: for a in range(n_actions):
    # 提示3:   features = feature_func(state, a)
    # 提示4:   q_values.append(q_func.value(features))
    # 提示5: return np.argmax(q_values)

    pass  # TODO: 删除这一行


def epsilon_greedy_policy(q_func, state, epsilon, n_actions, feature_func):
    """ε-greedy策略（行为策略）"""
    if np.random.random() < epsilon:
        return np.random.randint(n_actions)
    else:
        return greedy_policy(q_func, state, n_actions, feature_func)


def importance_sampling_ratio(target_action, behavior_action, epsilon, n_actions):
    """
    计算重要性采样比率

    ρ = π(a|s) / b(a|s)

    Args:
        target_action: 目标策略选择的动作（贪心）
        behavior_action: 行为策略选择的动作
        epsilon: 行为策略的探索率
        n_actions: 动作数

    Returns:
        rho: 重要性采样比率
    """
    # TODO: 实现重要性采样比率
    # 提示1: 目标策略是贪心的: π(a|s) = 1 if a == target_action else 0
    # 提示2: 行为策略是ε-greedy:
    #   b(a|s) = 1 - ε + ε/n  if a == greedy_action
    #   b(a|s) = ε/n          otherwise
    # 提示3: if behavior_action != target_action:
    #          return 0  # π(behavior_action) = 0
    # 提示4: else:
    #          # b(target_action) = 1 - ε + ε/n_actions
    #          b_prob = 1 - epsilon + epsilon / n_actions
    #          return 1.0 / b_prob

    pass  # TODO: 删除这一行


def semi_gradient_off_policy_td(env, episodes=1000, alpha=0.01, gamma=1.0, epsilon=0.1):
    """
    半梯度Off-policy TD

    Args:
        env: 环境
        episodes: 回合数
        alpha: 学习率
        gamma: 折扣因子
        epsilon: 行为策略探索率

    Returns:
        q_func: 学到的动作值函数
        diverged: 是否发散
    """
    n_states = env.n_states
    n_actions = env.n_actions

    # 初始化
    feature_dim = n_states * n_actions
    q_func = LinearActionValueFunction(feature_dim)
    feature_func = lambda s, a: tabular_features(s, a, n_states, n_actions)

    diverged = False

    # TODO: 实现半梯度off-policy TD主循环
    # 提示1: for episode in range(episodes):
    # 提示2:   state = env.reset()
    # 提示3:   # 行为策略选择动作
    # 提示4:   action = epsilon_greedy_policy(q_func, state, epsilon, n_actions, feature_func)
    # 提示5:
    # 提示6:   while True:
    # 提示7:     next_state, reward, done = env.step(action)
    # 提示8:     features = feature_func(state, action)
    # 提示9:
    # 提示10:    # 计算目标策略的动作
    # 提示11:    target_action = greedy_policy(q_func, state, n_actions, feature_func)
    # 提示12:
    # 提示13:    # 计算重要性采样比率
    # 提示14:    rho = importance_sampling_ratio(target_action, action, epsilon, n_actions)
    # 提示15:
    # 提示16:    if done:
    # 提示17:      td_target = reward
    # 提示18:      q_func.update(features, td_target, alpha, rho)
    # 提示19:      break
    # 提示20:
    # 提示21:    # 选择下一个动作（行为策略）
    # 提示22:    next_action = epsilon_greedy_policy(q_func, next_state, epsilon, n_actions, feature_func)
    # 提示23:
    # 提示24:    # 计算TD目标（使用目标策略）
    # 提示25:    next_target_action = greedy_policy(q_func, next_state, n_actions, feature_func)
    # 提示26:    next_features = feature_func(next_state, next_target_action)
    # 提示27:    td_target = reward + gamma * q_func.value(next_features)
    # 提示28:
    # 提示29:    # Off-policy更新
    # 提示30:    q_func.update(features, td_target, alpha, rho)
    # 提示31:
    # 提示32:    # 检查发散
    # 提示33:    if np.max(np.abs(q_func.w)) > 1000:
    # 提示34:      diverged = True
    # 提示35:      break
    # 提示36:
    # 提示37:    state = next_state
    # 提示38:    action = next_action
    # 提示39:
    # 提示40:  if diverged:
    # 提示41:    break

    pass  # TODO: 删除这一行

    return q_func, diverged


def test():
    """测试函数"""
    print("=" * 60)
    print("测试半梯度Off-policy TD - Random Walk")
    print("=" * 60)

    np.random.seed(42)

    env = RandomWalk(n_states=19)

    print(f"\n开始训练...")
    print(f"  目标策略: 贪心")
    print(f"  行为策略: ε-greedy (ε=0.1)")

    q_func, diverged = semi_gradient_off_policy_td(env, episodes=1000, alpha=0.01, epsilon=0.1)

    if diverged:
        print(f"\n⚠️  检测到发散！")
        print(f"  这演示了'致命三元组'问题")
    else:
        print(f"\n✅ 训练完成，未发散")

    print(f"\n权重统计:")
    print(f"  最大值: {np.max(q_func.w):.2f}")
    print(f"  最小值: {np.min(q_func.w):.2f}")
    print(f"  平均值: {np.mean(q_func.w):.2f}")

    return {
        'converges': not diverged,
        'stable': not diverged,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n提示:")
    print(f"  - Off-policy + 函数近似 + Bootstrapping = 可能发散")
    print(f"  - 重要性采样修正策略差异")
    print(f"  - 需要更小的学习率来保持稳定")
    print(f"  - 致命三元组是RL中的重要挑战")
