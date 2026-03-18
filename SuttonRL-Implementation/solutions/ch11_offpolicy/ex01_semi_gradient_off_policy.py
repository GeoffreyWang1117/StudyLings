"""
解答: 半梯度Off-Policy方法 (Semi-gradient Off-policy TD)

这是 ex01_semi_gradient_off_policy.py 的完整实现解答
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
    feature_dim = n_states * n_actions
    features = np.zeros(feature_dim)
    idx = state * n_actions + action
    features[idx] = 1
    return features


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
        prediction = self.value(features)
        error = target - prediction
        self.w += alpha * rho * error * features


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
    q_values = []
    for a in range(n_actions):
        features = feature_func(state, a)
        q_values.append(q_func.value(features))
    return np.argmax(q_values)


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
    # 目标策略是贪心的: π(a|s) = 1 if a == target_action else 0
    # 行为策略是ε-greedy:
    #   b(a|s) = 1 - ε + ε/n  if a == greedy_action
    #   b(a|s) = ε/n          otherwise

    if behavior_action != target_action:
        # π(behavior_action) = 0
        return 0.0
    else:
        # π(target_action) = 1
        # b(target_action) = 1 - ε + ε/n_actions
        b_prob = 1 - epsilon + epsilon / n_actions
        return 1.0 / b_prob


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

    for episode in range(episodes):
        state = env.reset()
        # 行为策略选择动作
        action = epsilon_greedy_policy(q_func, state, epsilon, n_actions, feature_func)

        while True:
            next_state, reward, done = env.step(action)
            features = feature_func(state, action)

            # 计算目标策略的动作
            target_action = greedy_policy(q_func, state, n_actions, feature_func)

            # 计算重要性采样比率
            rho = importance_sampling_ratio(target_action, action, epsilon, n_actions)

            if done:
                td_target = reward
                q_func.update(features, td_target, alpha, rho)
                break

            # 选择下一个动作（行为策略）
            next_action = epsilon_greedy_policy(q_func, next_state, epsilon, n_actions, feature_func)

            # 计算TD目标（使用目标策略）
            next_target_action = greedy_policy(q_func, next_state, n_actions, feature_func)
            next_features = feature_func(next_state, next_target_action)
            td_target = reward + gamma * q_func.value(next_features)

            # Off-policy更新
            q_func.update(features, td_target, alpha, rho)

            # 检查发散
            if np.max(np.abs(q_func.w)) > 1000:
                diverged = True
                break

            state = next_state
            action = next_action

        if diverged:
            break

    return q_func, diverged


def test():
    """测试函数"""
    print("=" * 60)
    print("测试半梯度Off-policy TD - Random Walk [解答版本]")
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

    print(f"\n✅ 解答说明:")
    print(f"  1. 行为策略: ε-greedy选择动作")
    print(f"  2. 目标策略: 贪心策略")
    print(f"  3. 重要性采样比率: ρ = π(a|s) / b(a|s)")
    print(f"  4. Off-policy更新: w ← w + αρδ∇q̂")
    print(f"\n致命三元组:")
    print(f"  - 函数近似 + Off-policy + Bootstrapping")
    print(f"  - 可能导致发散!")
    print(f"  - 需要小心设置学习率")
    print(f"  - 这是RL理论中的重要挑战")
