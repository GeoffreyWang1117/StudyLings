"""
练习: 首次访问 MC 预测 (First-Visit Monte Carlo Prediction)

算法描述:
蒙特卡洛方法通过对完整回合的平均回报来估计状态值函数。
首次访问 MC 只在状态第一次出现时记录回报。

核心思想:
- v_π(s) ≈ 平均所有从状态 s 开始的回报
- 只需要经验（回合样本），不需要环境模型
- 必须等待回合结束才能更新

伪代码:
┌────────────────────────────────────────────────────┐
│ 输入: 策略 π                                       │
│ 初始化:                                            │
│   V(s) = 任意值，对所有 s ∈ S                      │
│   Returns(s) = 空列表，对所有 s ∈ S                │
│                                                    │
│ 循环（对每个回合）:                                │
│   生成一个回合：S_0, A_0, R_1, S_1, ..., S_T       │
│   G ← 0                                            │
│   对回合中的每一步 t = T-1, T-2, ..., 0:           │
│     G ← γG + R_{t+1}                               │
│     如果 S_t 不在 S_0, S_1, ..., S_{t-1} 中出现:   │
│       将 G 追加到 Returns(S_t)                     │
│       V(S_t) ← average(Returns(S_t))               │
└────────────────────────────────────────────────────┘

使用 Blackjack 环境:
- 玩家目标: 获得点数和接近21但不超过21
- 状态: (玩家点数, 庄家明牌, 是否有可用A)
- 动作: 0=停牌(stick), 1=要牌(hit)
- 奖励: +1(赢), 0(平), -1(输)

要求:
- 实现首次访问 MC 预测
- 使用固定策略评估
- 运行足够多回合直到收敛

参考: Sutton & Barto 第5章, 第5.1节
"""

import numpy as np
from collections import defaultdict


class BlackjackEnv:
    """简化的21点环境"""

    def __init__(self):
        self.action_space = 2  # 0=stick, 1=hit

    def reset(self):
        """开始新回合"""
        # 玩家初始两张牌
        self.player = [self._draw_card(), self._draw_card()]
        # 庄家明牌
        self.dealer_showing = self._draw_card()
        # 庄家暗牌
        self.dealer_hidden = self._draw_card()

        return self._get_state()

    def _draw_card(self):
        """抽牌：1-10，J/Q/K算10"""
        card = min(np.random.randint(1, 14), 10)
        return card

    def _get_state(self):
        """
        获取状态
        Returns: (player_sum, dealer_showing, usable_ace)
        """
        player_sum = sum(self.player)
        usable_ace = (1 in self.player and player_sum + 10 <= 21)

        if usable_ace:
            player_sum += 10

        return (player_sum, self.dealer_showing, usable_ace)

    def step(self, action):
        """
        执行动作

        Args:
            action: 0=stick(停牌), 1=hit(要牌)

        Returns:
            state, reward, done
        """
        if action == 1:  # hit
            self.player.append(self._draw_card())
            player_sum = sum(self.player)
            usable_ace = (1 in self.player and player_sum + 10 <= 21)

            if usable_ace:
                player_sum += 10

            if player_sum > 21:
                return self._get_state(), -1, True  # 爆牌，输
            else:
                return self._get_state(), 0, False

        else:  # stick
            # 玩家停牌，庄家开始抽牌
            return self._dealer_play()

    def _dealer_play(self):
        """庄家按固定策略抽牌"""
        dealer = [self.dealer_showing, self.dealer_hidden]

        while True:
            dealer_sum = sum(dealer)
            usable_ace = (1 in dealer and dealer_sum + 10 <= 21)

            if usable_ace:
                dealer_sum += 10

            if dealer_sum >= 17:
                break
            dealer.append(self._draw_card())

        # 计算玩家点数
        player_sum = sum(self.player)
        usable_ace = (1 in self.player and player_sum + 10 <= 21)
        if usable_ace:
            player_sum += 10

        # 比较
        if dealer_sum > 21:
            reward = 1  # 庄家爆牌，玩家赢
        elif player_sum > dealer_sum:
            reward = 1
        elif player_sum < dealer_sum:
            reward = -1
        else:
            reward = 0

        return self._get_state(), reward, True


def simple_policy(state):
    """
    简单策略：玩家点数 >= 20 则停牌，否则要牌

    Args:
        state: (player_sum, dealer_showing, usable_ace)

    Returns:
        action: 0 or 1
    """
    player_sum, _, _ = state
    return 0 if player_sum >= 20 else 1


def generate_episode(env, policy):
    """
    生成一个完整回合

    Args:
        env: 环境
        policy: 策略函数

    Returns:
        episode: [(state, action, reward), ...]
    """
    # TODO: 实现回合生成
    # 提示1: episode = []
    # 提示2: state = env.reset()
    # 提示3: done = False
    # 提示4: while not done:
    # 提示5:   action = policy(state)
    # 提示6:   next_state, reward, done = env.step(action)
    # 提示7:   episode.append((state, action, reward))
    # 提示8:   state = next_state
    # 提示9: return episode

    pass  # TODO: 删除这一行，实现回合生成


def first_visit_mc_prediction(env, policy, episodes=10000, gamma=1.0):
    """
    首次访问 MC 预测

    Args:
        env: 环境
        policy: 策略函数
        episodes: 回合数
        gamma: 折扣因子

    Returns:
        V: 状态值函数（字典）
    """
    # 初始化
    V = defaultdict(float)
    returns = defaultdict(list)

    # TODO: 实现首次访问 MC 算法
    # 提示1: for _ in range(episodes):
    # 提示2:   episode = generate_episode(env, policy)
    # 提示3:   G = 0
    # 提示4:   visited_states = set()
    # 提示5:   # 从后往前遍历回合
    # 提示6:   for t in range(len(episode) - 1, -1, -1):
    # 提示7:     state, action, reward = episode[t]
    # 提示8:     G = gamma * G + reward
    # 提示9:     # 首次访问检查
    # 提示10:    if state not in visited_states:
    # 提示11:      visited_states.add(state)
    # 提示12:      returns[state].append(G)
    # 提示13:      V[state] = np.mean(returns[state])

    pass  # TODO: 删除这一行，实现 MC 预测

    return V


def test():
    """测试函数"""
    print("=" * 60)
    print("测试首次访问 MC - Blackjack")
    print("=" * 60)

    np.random.seed(42)

    env = BlackjackEnv()

    print(f"\n环境: Blackjack (21点)")
    print(f"策略: 玩家点数 >= 20 停牌，否则要牌")
    print(f"回合数: 10000")
    print(f"折扣因子 γ: 1.0")
    print(f"\n开始训练...")

    V = first_visit_mc_prediction(env, simple_policy, episodes=10000, gamma=1.0)

    print(f"\n训练完成!")
    print(f"  估计了 {len(V)} 个状态的值")

    # 显示一些示例状态值
    print(f"\n示例状态值:")
    print("=" * 60)
    sample_states = [
        (20, 10, False),
        (20, 10, True),
        (18, 10, False),
        (12, 2, False),
    ]

    for state in sample_states:
        if state in V:
            print(f"  状态 {state}: V = {V[state]:6.3f}")

    # 验证：点数20应该有较高的值（接近胜率）
    # 检查收敛性
    if len(V) > 0:
        avg_value = np.mean(list(V.values()))
        print(f"\n平均状态值: {avg_value:.4f}")

        converges = len(V) >= 100  # 至少访问了100个状态
        value_error_max = abs(avg_value)  # 简化的误差度量
    else:
        converges = False
        value_error_max = 1.0

    return {
        'converges': converges,
        'value_error_max': value_error_max,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n提示:")
    print(f"  - MC 方法需要完整回合，适合分节式任务")
    print(f"  - 首次访问 vs 每次访问的区别在于状态重复访问的处理")
    print(f"  - 不需要环境模型，只需要经验")
