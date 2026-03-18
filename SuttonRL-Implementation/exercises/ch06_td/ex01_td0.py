"""
练习: TD(0) 预测 (Temporal-Difference Learning)

算法描述:
TD(0)是最基础的时序差分学习算法，用于策略评估（预测问题）。
它结合了蒙特卡洛的采样和动态规划的自举（bootstrapping）。

核心思想:
- 使用当前估计 V(S') 来估计回报
- TD目标: R + γV(S')
- TD误差: δ = R + γV(S') - V(S)
- 增量更新: V(S) ← V(S) + α·δ

与MC和DP的关系:
- MC: V(S) ← V(S) + α[G - V(S)]  (需要完整回合)
- DP: V(s) = Σπ(a|s)Σp(s',r|s,a)[r + γV(s')]  (需要模型)
- TD: V(S) ← V(S) + α[R + γV(S') - V(S)]  (在线学习，无需模型)

伪代码:
┌────────────────────────────────────────────────────┐
│ 输入: 策略 π                                       │
│ 初始化: V(s) 任意值，V(terminal) = 0               │
│                                                    │
│ 循环（对每个回合）:                                │
│   初始化 S                                         │
│   循环（对回合中的每一步）:                        │
│     A ← π(S)                                       │
│     执行 A，观察 R, S'                             │
│     V(S) ← V(S) + α[R + γV(S') - V(S)]             │
│     S ← S'                                         │
│   直到 S 是终止状态                                │
└────────────────────────────────────────────────────┘

使用 Random Walk 环境

要求:
- 实现TD(0)预测算法
- 观察在线学习的特性
- 比较与MC的收敛速度
- 状态值误差应小于 0.3

参考: Sutton & Barto 第6章, 第6.1节
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
    # 也可以随机初始化：V = np.random.rand(env.n_states) * 0.5

    # TODO: 实现TD(0)主循环
    # 提示1: for episode in range(episodes):
    # 提示2:   state = env.reset()
    # 提示3:   done = False
    # 提示4:
    # 提示5:   while not done:
    # 提示6:     next_state, reward, done = env.step()
    # 提示7:
    # 提示8:     # 计算TD目标
    # 提示9:     if done:
    # 提示10:      td_target = reward
    # 提示11:    else:
    # 提示12:      td_target = reward + gamma * V[next_state]
    # 提示13:
    # 提示14:    # TD更新
    # 提示15:    td_error = td_target - V[state]
    # 提示16:    V[state] = V[state] + alpha * td_error
    # 提示17:
    # 提示18:    state = next_state

    pass  # TODO: 删除这一行

    return V


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 TD(0) 预测 - Random Walk")
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

    print(f"\n提示:")
    print(f"  - TD(0)是最基础的TD算法")
    print(f"  - 结合了MC的采样和DP的自举")
    print(f"  - 可以在线学习，不需要等回合结束")
    print(f"  - 比MC方差更小，比DP更灵活")
    print(f"\n调参建议:")
    print(f"  - 学习率α: 0.05-0.2 (太大不稳定，太小收敛慢)")
    print(f"  - 可以尝试不同的初始化观察影响")
