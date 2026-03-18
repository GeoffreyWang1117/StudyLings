"""
练习: TD(λ) 预测

算法描述:
TD(λ) 使用资格迹（eligibility traces）来高效实现 n步方法的效果。
资格迹记录了每个状态对当前学习的"资格程度"。

核心思想:
- λ=0: TD(0)
- λ=1: Monte Carlo
- 0<λ<1: 介于两者之间

资格迹更新:
    z_t(s) = γλz_{t-1}(s) + 𝟙(S_t = s)

值函数更新:
    δ_t = R_{t+1} + γV(S_{t+1}) - V(S_t)
    V(s) ← V(s) + αδ_t z_t(s)  对所有 s

伪代码 (在线 λ-回报算法):
┌────────────────────────────────────────────────────┐
│ 输入: 策略 π, λ ∈ [0,1]                            │
│ 初始化: V(s) 任意值，对所有 s ∈ S+                 │
│                                                    │
│ 对每个回合:                                        │
│   初始化 S                                         │
│   z(s) ← 0, 对所有 s ∈ S                           │
│                                                    │
│   对回合中的每一步:                                │
│     A ~ π(·|S)                                     │
│     执行 A, 观察 R, S'                             │
│     δ ← R + γV(S') - V(S)                          │
│     z(S) ← z(S) + 1  (累积迹)                      │
│     # 或 z(S) ← 1   (替代迹)                       │
│                                                    │
│     对所有 s ∈ S:                                  │
│       V(s) ← V(s) + αδz(s)                         │
│       z(s) ← γλz(s)                                │
│                                                    │
│     S ← S'                                         │
│   直到 S 是终止状态                                │
└────────────────────────────────────────────────────┘

使用 Random Walk 环境

要求:
- 实现 TD(λ) 算法
- 使用累积迹或替代迹
- 比较不同 λ 值的性能

参考: Sutton & Barto 第12章, 第12.1-12.2节
"""

import numpy as np


class RandomWalk:
    """Random Walk 环境（同 ex01）"""

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
    """
    TD(λ) 预测算法

    Args:
        env: 环境
        lambda_param: λ 参数 (0-1)
        episodes: 回合数
        alpha: 学习率
        gamma: 折扣因子
        use_replacing: 是否使用替代迹（否则使用累积迹）

    Returns:
        V: 学习到的值函数
    """
    # 初始化
    V = np.zeros(env.n_states)

    # TODO: 实现 TD(λ) 算法
    # 提示1: for episode in range(episodes):
    # 提示2:   state = env.reset()
    # 提示3:   # 初始化资格迹
    # 提示4:   z = np.zeros(env.n_states)
    # 提示5:   done = False
    # 提示6:
    # 提示7:   while not done:
    # 提示8:     # 选择动作
    # 提示9:     action = random_policy()
    # 提示10:    next_state, reward, done = env.step(action)
    # 提示11:
    # 提示12:    # 计算 TD 误差
    # 提示13:    delta = reward + gamma * V[next_state] - V[state]
    # 提示14:
    # 提示15:    # 更新资格迹
    # 提示16:    if use_replacing:
    # 提示17:      z[state] = 1  # 替代迹
    # 提示18:    else:
    # 提示19:      z[state] += 1  # 累积迹
    # 提示20:
    # 提示21:    # 更新所有状态的值函数
    # 提示22:    V += alpha * delta * z
    # 提示23:
    # 提示24:    # 衰减资格迹
    # 提示25:    z *= gamma * lambda_param
    # 提示26:
    # 提示27:    state = next_state

    pass  # TODO: 删除这一行，实现 TD(λ)

    return V


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 TD(λ) - Random Walk")
    print("=" * 60)

    np.random.seed(42)

    env = RandomWalk(n_states=7)
    true_V = np.array([0, 1/6, 2/6, 3/6, 4/6, 5/6, 0])

    print(f"\n环境: Random Walk")
    print(f"真实值: {true_V}")
    print(f"\n测试不同的 λ 值...")

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
    print(f"\n最佳 λ: {best_lambda}, RMSE: {errors[best_lambda]:.4f}")

    # 测试替代迹
    print(f"\n使用替代迹 (λ=0.5):")
    V_replacing = td_lambda(env, lambda_param=0.5, episodes=100, alpha=0.1, use_replacing=True)
    error_replacing = np.sqrt(np.mean((V_replacing - true_V) ** 2))
    print(f"  RMSE: {error_replacing:.4f}")

    converges = errors[best_lambda] < 0.3

    return {
        'converges': converges,
        'value_error_max': errors[best_lambda],
    }


if __name__ == '__main__':
    result = test()

    print(f"\n提示:")
    print(f"  - λ=0 等价于 TD(0)")
    print(f"  - λ=1 等价于 MC（但是在线更新）")
    print(f"  - 资格迹实现了高效的信用分配")
    print(f"  - 累积迹 vs 替代迹：替代迹防止过度累积")
