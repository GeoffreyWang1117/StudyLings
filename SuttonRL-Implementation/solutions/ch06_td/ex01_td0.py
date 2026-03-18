"""
解答: TD(0) 预测 (Temporal-Difference Learning)

这是 ex01_td0.py 的完整实现解答
"""

import numpy as np


class RandomWalk:
    """Random Walk环境（7状态版本）"""

    def __init__(self, n_states=5):
        """
        初始化

        Args:
            n_states: 非终止状态数量（默认5）
        """
        # 状态: 0(左终止), 1-5(非终止), 6(右终止)
        self.n_states = n_states + 2
        self.start_state = (n_states + 1) // 2  # 中间状态

    def reset(self):
        """重置环境"""
        self.state = self.start_state
        return self.state

    def step(self):
        """
        执行一步（随机左右移动）

        Returns:
            next_state, reward, done
        """
        # 随机向左或向右
        direction = np.random.choice([-1, 1])
        self.state += direction

        # 检查终止
        if self.state == 0:
            return 0, 0, True  # 左终止，奖励0
        elif self.state == self.n_states - 1:
            return self.n_states - 1, 1, True  # 右终止，奖励1
        else:
            return self.state, 0, False  # 继续，奖励0


def td0_prediction(env, episodes=100, alpha=0.1, gamma=1.0):
    """
    TD(0) 预测算法

    Args:
        env: 环境
        episodes: 回合数
        alpha: 学习率
        gamma: 折扣因子

    Returns:
        V: 学到的状态值函数
    """
    # 初始化状态值（除终止状态外）
    V = np.zeros(env.n_states)

    for episode in range(episodes):
        state = env.reset()
        done = False

        while not done:
            next_state, reward, done = env.step()

            # 计算TD目标
            if done:
                td_target = reward
            else:
                td_target = reward + gamma * V[next_state]

            # TD更新: V(S) ← V(S) + α[R + γV(S') - V(S)]
            td_error = td_target - V[state]
            V[state] = V[state] + alpha * td_error

            state = next_state

    return V


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 TD(0) 预测 - Random Walk [解答版本]")
    print("=" * 60)

    np.random.seed(42)

    env = RandomWalk(n_states=5)

    print(f"\n环境: Random Walk (5个非终止状态)")
    print(f"  状态: [0(终止), 1, 2, 3, 4, 5, 6(终止)]")
    print(f"  真实值: V ≈ [0, 1/6, 2/6, 3/6, 4/6, 5/6, 1]")

    print(f"\n开始训练 (100回合)...")

    V = td0_prediction(env, episodes=100, alpha=0.1, gamma=1.0)

    print(f"\n学到的状态值:")
    print("状态\t真实值\t估计值\t误差")
    print("-" * 40)

    true_values = np.array([0, 1/6, 2/6, 3/6, 4/6, 5/6, 1])
    total_error = 0

    for s in range(env.n_states):
        true_v = true_values[s]
        estimated_v = V[s]
        error = abs(true_v - estimated_v)
        total_error += error
        print(f"{s}\t{true_v:.3f}\t{estimated_v:.3f}\t{error:.3f}")

    avg_error = total_error / env.n_states

    print(f"\n平均绝对误差: {avg_error:.4f}")

    return {
        'avg_error': avg_error,
        'converges': avg_error < 0.3,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n✅ 解答说明:")
    print(f"  1. 初始化: V(s) = 0")
    print(f"  2. 每步更新: V(S) ← V(S) + α[R + γV(S') - V(S)]")
    print(f"  3. TD目标: R + γV(S')")
    print(f"  4. TD误差: δ = R + γV(S') - V(S)")
    print(f"\nTD(0)的特点:")
    print(f"  - 在线学习：每步更新，无需等回合结束")
    print(f"  - 自举：使用估计值更新估计值")
    print(f"  - 无需模型：直接从经验学习")
    print(f"  - 低方差：比MC方差小")
    print(f"\n与其他算法对比:")
    print(f"  - vs MC: 更快，方差更小，有偏（初期）")
    print(f"  - vs DP: 无需模型，可在线学习")
    print(f"  - TD(0)是RL最核心的算法之一")
