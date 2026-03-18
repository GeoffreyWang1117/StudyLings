"""
练习: SARSA (On-Policy TD Control)

算法描述:
SARSA 是一种 on-policy TD 控制算法。
名字来源于更新序列: (S_t, A_t, R_{t+1}, S_{t+1}, A_{t+1})

更新规则:
    Q(S_t, A_t) ← Q(S_t, A_t) + α[R_{t+1} + γQ(S_{t+1}, A_{t+1}) - Q(S_t, A_t)]

关键特点:
- On-policy: 使用当前策略生成数据并改进该策略
- 使用下一个状态-动作对 (S', A') 来更新
- A' 由当前策略选择（如 ε-greedy）

伪代码:
┌────────────────────────────────────────────────────┐
│ 初始化: Q(s,a) 任意值，Q(terminal,·) = 0           │
│                                                    │
│ 对每个回合:                                        │
│   初始化 S                                         │
│   选择 A ~ ε-greedy(Q(S,·))                        │
│                                                    │
│   对回合中的每一步:                                │
│     执行 A, 观察 R, S'                             │
│     选择 A' ~ ε-greedy(Q(S',·))                    │
│     Q(S,A) ← Q(S,A) + α[R + γQ(S',A') - Q(S,A)]   │
│     S ← S'; A ← A'                                 │
│   直到 S 是终止状态                                │
└────────────────────────────────────────────────────┘

本练习使用 Cliff Walking 环境:
- 4x12 网格世界
- 起点: 左下角 (3, 0)
- 终点: 右下角 (3, 11)
- 悬崖: 底部一行 (3, 1-10)
- 掉入悬崖: 奖励 -100, 回到起点
- 正常移动: 奖励 -1
- 到达终点: 回合结束

要求:
- 实现 SARSA 算法
- 使用 ε-greedy 策略
- 运行足够多回合直到收敛

参考: Sutton & Barto 第6章, 第6.4节, 示例6.6
"""

import numpy as np


class CliffWalking:
    """悬崖行走环境"""

    def __init__(self):
        self.height = 4
        self.width = 12
        self.n_actions = 4  # 上、下、左、右

        # 起点和终点
        self.start = (3, 0)
        self.goal = (3, 11)

        # 悬崖位置
        self.cliff = [(3, i) for i in range(1, 11)]

        self.reset()

    def reset(self):
        """重置环境"""
        self.state = self.start
        return self.state

    def step(self, action):
        """
        执行动作

        Args:
            action: 0=上, 1=下, 2=左, 3=右

        Returns:
            next_state: 下一状态
            reward: 奖励
            done: 是否结束
        """
        row, col = self.state

        # 执行动作
        if action == 0:  # 上
            row = max(0, row - 1)
        elif action == 1:  # 下
            row = min(self.height - 1, row + 1)
        elif action == 2:  # 左
            col = max(0, col - 1)
        elif action == 3:  # 右
            col = min(self.width - 1, col + 1)

        next_state = (row, col)

        # 检查悬崖
        if next_state in self.cliff:
            reward = -100
            next_state = self.start  # 回到起点
            done = False
        elif next_state == self.goal:
            reward = -1
            done = True
        else:
            reward = -1
            done = False

        self.state = next_state
        return next_state, reward, done


def epsilon_greedy(Q, state, epsilon, n_actions):
    """
    ε-greedy 策略

    Args:
        Q: Q值表
        state: 当前状态
        epsilon: 探索概率
        n_actions: 动作数量

    Returns:
        选择的动作
    """
    # TODO: 实现 ε-greedy 动作选择
    # 提示1: 以概率 ε 随机选择
    # 提示2: 否则选择 Q(s,a) 最大的动作
    # 提示3: 状态是元组 (row, col)，使用 Q[state] 访问

    pass  # TODO: 删除这一行，实现动作选择


def sarsa(env, episodes=500, alpha=0.1, gamma=1.0, epsilon=0.1):
    """
    SARSA 算法

    Args:
        env: 环境
        episodes: 回合数
        alpha: 学习率
        gamma: 折扣因子
        epsilon: 探索概率

    Returns:
        Q: 学习到的 Q 值
        episode_returns: 每个回合的总回报
    """
    # 初始化 Q 表（使用字典）
    Q = {}

    def get_q(state, action):
        """获取 Q 值，未见过的状态-动作对返回 0"""
        return Q.get((state, action), 0.0)

    def set_q(state, action, value):
        """设置 Q 值"""
        Q[(state, action)] = value

    episode_returns = []

    # TODO: 实现 SARSA 主循环
    # 提示1: for episode in range(episodes):
    # 提示2:   初始化状态: state = env.reset()
    # 提示3:   选择动作: action = epsilon_greedy(...)
    # 提示4:   episode_return = 0
    # 提示5:   while True:
    # 提示6:     执行动作: next_state, reward, done = env.step(action)
    # 提示7:     选择下一个动作: next_action = epsilon_greedy(...)
    # 提示8:     更新 Q 值:
    #            q_current = get_q(state, action)
    #            q_next = get_q(next_state, next_action)
    #            td_target = reward + gamma * q_next
    #            td_error = td_target - q_current
    #            set_q(state, action, q_current + alpha * td_error)
    # 提示9:     episode_return += reward
    # 提示10:    state = next_state
    # 提示11:    action = next_action
    # 提示12:    if done: break
    # 提示13:  episode_returns.append(episode_return)

    pass  # TODO: 删除这一行，实现 SARSA

    return Q, episode_returns


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 SARSA - Cliff Walking")
    print("=" * 60)

    np.random.seed(42)

    env = CliffWalking()

    print(f"\n环境: Cliff Walking {env.height}x{env.width}")
    print(f"起点: {env.start}")
    print(f"终点: {env.goal}")
    print(f"悬崖: 底部一行")
    print(f"\n超参数:")
    print(f"  回合数: 500")
    print(f"  学习率 α: 0.1")
    print(f"  折扣因子 γ: 1.0")
    print(f"  探索概率 ε: 0.1")
    print(f"\n开始训练...")

    Q, episode_returns = sarsa(env, episodes=500, alpha=0.1, gamma=1.0, epsilon=0.1)

    # 分析结果
    avg_return_last_100 = np.mean(episode_returns[-100:])
    print(f"\n" + "=" * 60)
    print(f"训练完成!")
    print(f"  前100回合平均回报: {np.mean(episode_returns[:100]):.2f}")
    print(f"  后100回合平均回报: {avg_return_last_100:.2f}")
    print(f"  最佳回合回报: {np.max(episode_returns):.2f}")
    print(f"=" * 60)

    # 可视化学到的策略
    print(f"\n学到的策略 (贪心):")
    print("=" * 50)
    action_symbols = ['↑', '↓', '←', '→']
    for row in range(env.height):
        for col in range(env.width):
            state = (row, col)
            if state == env.goal:
                print(" G", end=" ")
            elif state in env.cliff:
                print(" C", end=" ")
            elif state == env.start:
                print(" S", end=" ")
            else:
                # 找到最佳动作
                q_values = [Q.get((state, a), 0.0) for a in range(env.n_actions)]
                best_action = np.argmax(q_values)
                print(f" {action_symbols[best_action]}", end=" ")
        print()
    print("=" * 50)
    print("S=起点, G=终点, C=悬崖")

    # SARSA 是 on-policy，会学习安全路径（远离悬崖）
    converges = avg_return_last_100 > -100
    avg_return_min = avg_return_last_100

    return {
        'converges': converges,
        'avg_return_min': avg_return_min,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n提示:")
    print(f"  - SARSA 是 on-policy，会学习安全路径")
    print(f"  - 由于使用 ε-greedy，会偶尔探索，所以学习远离悬崖的路径")
    print(f"  - 对比 Q-Learning (off-policy) 会学习贴着悬崖走的最优路径")
