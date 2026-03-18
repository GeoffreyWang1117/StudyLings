"""
解答: n步TD预测

这是 ex01_n_step_td.py 的完整实现解答
"""

import numpy as np


class RandomWalk:
    """随机游走环境"""

    def __init__(self, n_states=7):
        self.n_states = n_states
        self.start_state = n_states // 2

    def reset(self):
        self.state = self.start_state
        return self.state

    def step(self, action):
        if action == 0:  # 左
            self.state -= 1
        else:  # 右
            self.state += 1

        if self.state == 0:
            return self.state, 0, True
        elif self.state == self.n_states - 1:
            return self.state, 1, True
        else:
            return self.state, 0, False


def random_policy():
    """随机策略"""
    return np.random.randint(0, 2)


def n_step_td_prediction(env, n=1, episodes=100, alpha=0.1, gamma=1.0):
    """n步TD预测"""
    # 初始化值函数
    V = np.zeros(env.n_states)

    for episode in range(episodes):
        # 存储状态和奖励序列
        states = [env.reset()]
        rewards = [0]  # R_0不存在，占位

        T = float('inf')
        t = 0

        while True:
            if t < T:
                # 采取动作
                action = random_policy()
                next_state, reward, done = env.step(action)

                states.append(next_state)
                rewards.append(reward)

                if done:
                    T = t + 1

            # 更新时间步 τ
            tau = t - n + 1

            if tau >= 0:
                # 计算n步回报G
                G = 0.0
                for i in range(tau + 1, min(tau + n, T) + 1):
                    G += (gamma ** (i - tau - 1)) * rewards[i]

                # 如果未到终止，加上自举项
                if tau + n < T:
                    G += (gamma ** n) * V[states[tau + n]]

                # 更新值函数
                V[states[tau]] += alpha * (G - V[states[tau]])

            if tau == T - 1:
                break

            t += 1

    return V


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 n步TD预测 - Random Walk [解答版本]")
    print("=" * 60)

    np.random.seed(42)

    env = RandomWalk(n_states=7)
    true_V = np.array([0, 1/6, 2/6, 3/6, 4/6, 5/6, 0])

    print(f"\n真实值函数: {true_V}")
    print(f"\n测试不同的n值...")

    n_values = [1, 2, 4, 8]
    errors = {}

    for n in n_values:
        print(f"\nn = {n}:")
        V = n_step_td_prediction(env, n=n, episodes=100, alpha=0.1, gamma=1.0)

        error = np.sqrt(np.mean((V - true_V) ** 2))
        errors[n] = error

        print(f"  学习值: {V}")
        print(f"  RMSE: {error:.4f}")

    best_n = min(errors, key=errors.get)
    print(f"\n最佳 n: {best_n}, RMSE: {errors[best_n]:.4f}")

    return {
        'converges': errors[best_n] < 0.3,
        'value_error_max': errors[best_n],
    }


if __name__ == '__main__':
    result = test()

    print(f"\n✅ 解答说明:")
    print(f"  1. 存储最近n步的状态和奖励")
    print(f"  2. 计算n步回报: G = ΣR + γ^n V(S_{t+n})")
    print(f"  3. τ = t - n + 1 是要更新的时间步")
    print(f"  4. 延迟n步更新，平衡偏差和方差")
