"""
解答: TD(λ)

这是 ex01_td_lambda.py 的完整实现解答
"""

import numpy as np


class RandomWalk:
    """Random Walk环境"""

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


def td_lambda(env, lambda_param=0.5, episodes=100, alpha=0.1, gamma=1.0, use_replacing=False):
    """TD(λ)算法"""
    # 初始化值函数
    V = np.zeros(env.n_states)

    for episode in range(episodes):
        state = env.reset()

        # 初始化资格迹
        z = np.zeros(env.n_states)

        done = False

        while not done:
            # 选择动作
            action = random_policy()
            next_state, reward, done = env.step(action)

            # 计算TD误差
            delta = reward + gamma * V[next_state] - V[state]

            # 更新资格迹
            if use_replacing:
                z[state] = 1  # 替代迹
            else:
                z[state] += 1  # 累积迹

            # 更新所有状态的值函数
            V += alpha * delta * z

            # 衰减资格迹
            z *= gamma * lambda_param

            state = next_state

    return V


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 TD(λ) - Random Walk [解答版本]")
    print("=" * 60)

    np.random.seed(42)

    env = RandomWalk(n_states=7)
    true_V = np.array([0, 1/6, 2/6, 3/6, 4/6, 5/6, 0])

    print(f"\n真实值: {true_V}")
    print(f"\n测试不同的λ值...")

    lambda_values = [0.0, 0.3, 0.5, 0.8, 1.0]
    errors = {}

    for lam in lambda_values:
        print(f"\nλ = {lam}:")
        V = td_lambda(env, lambda_param=lam, episodes=100, alpha=0.1)

        error = np.sqrt(np.mean((V - true_V) ** 2))
        errors[lam] = error

        print(f"  学习值: {np.round(V, 3)}")
        print(f"  RMSE: {error:.4f}")

    best_lambda = min(errors, key=errors.get)
    print(f"\n最佳λ: {best_lambda}, RMSE: {errors[best_lambda]:.4f}")

    # 测试替代迹
    print(f"\n使用替代迹 (λ=0.5):")
    V_replacing = td_lambda(env, lambda_param=0.5, episodes=100, alpha=0.1, use_replacing=True)
    error_replacing = np.sqrt(np.mean((V_replacing - true_V) ** 2))
    print(f"  RMSE: {error_replacing:.4f}")

    return {
        'converges': errors[best_lambda] < 0.3,
        'value_error_max': errors[best_lambda],
    }


if __name__ == '__main__':
    result = test()

    print(f"\n✅ 解答说明:")
    print(f"  1. 初始化资格迹 z=0")
    print(f"  2. δ = R + γV(S') - V(S)")
    print(f"  3. z(S) += 1 (累积) 或 z(S) = 1 (替代)")
    print(f"  4. V += αδz (所有状态)")
    print(f"  5. z *= γλ (衰减)")
