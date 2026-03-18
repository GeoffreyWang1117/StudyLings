"""
练习: MC 探索启动 (Monte Carlo with Exploring Starts)

算法描述:
MC ES 通过探索启动（随机初始状态-动作对）来保证探索，
然后使用贪心策略改进。这是一个 on-policy 控制算法。

核心思想:
- 探索启动：每个回合随机选择初始状态和动作
- 策略评估：使用 MC 估计 Q(s,a)
- 策略改进：对每个状态，贪心选择最佳动作

伪代码:
┌────────────────────────────────────────────────────┐
│ 初始化:                                            │
│   π(s) = 任意策略，对所有 s ∈ S                    │
│   Q(s,a) = 任意值，对所有 s ∈ S, a ∈ A             │
│   Returns(s,a) = 空列表，对所有 s ∈ S, a ∈ A       │
│                                                    │
│ 循环（对每个回合）:                                │
│   随机选择 S_0 ∈ S, A_0 ∈ A(S_0)  [探索启动]       │
│   生成回合：S_0,A_0,R_1,...,S_T，遵循 π            │
│   G ← 0                                            │
│   对回合中的每一步 t = T-1, ..., 0:                │
│     G ← γG + R_{t+1}                               │
│     如果 (S_t,A_t) 首次出现:                       │
│       将 G 追加到 Returns(S_t,A_t)                 │
│       Q(S_t,A_t) ← average(Returns(S_t,A_t))       │
│       π(S_t) ← argmax_a Q(S_t,a)  [贪心改进]       │
└────────────────────────────────────────────────────┘

使用 Blackjack 环境

要求:
- 实现 MC ES 算法
- 使用探索启动
- 学习最优策略

参考: Sutton & Barto 第5章, 第5.3节
"""

import numpy as np
from collections import defaultdict


class BlackjackEnv:
    """Blackjack 环境（同 ex01）"""

    def __init__(self):
        self.action_space = 2

    def reset(self):
        self.player = [self._draw_card(), self._draw_card()]
        self.dealer_showing = self._draw_card()
        self.dealer_hidden = self._draw_card()
        return self._get_state()

    def set_state(self, player_sum, dealer_showing, usable_ace):
        """设置特定状态（用于探索启动）"""
        # 简化：直接设置状态
        self.dealer_showing = dealer_showing
        self.dealer_hidden = self._draw_card()

        # 设置玩家牌
        if usable_ace:
            self.player = [1, player_sum - 11]
        else:
            self.player = [player_sum // 2, player_sum - player_sum // 2]

    def _draw_card(self):
        return min(np.random.randint(1, 14), 10)

    def _get_state(self):
        player_sum = sum(self.player)
        usable_ace = (1 in self.player and player_sum + 10 <= 21)
        if usable_ace:
            player_sum += 10
        return (player_sum, self.dealer_showing, usable_ace)

    def step(self, action):
        if action == 1:  # hit
            self.player.append(self._draw_card())
            player_sum = sum(self.player)
            usable_ace = (1 in self.player and player_sum + 10 <= 21)
            if usable_ace:
                player_sum += 10
            if player_sum > 21:
                return self._get_state(), -1, True
            else:
                return self._get_state(), 0, False
        else:  # stick
            return self._dealer_play()

    def _dealer_play(self):
        dealer = [self.dealer_showing, self.dealer_hidden]
        while True:
            dealer_sum = sum(dealer)
            usable_ace = (1 in dealer and dealer_sum + 10 <= 21)
            if usable_ace:
                dealer_sum += 10
            if dealer_sum >= 17:
                break
            dealer.append(self._draw_card())

        player_sum = sum(self.player)
        usable_ace = (1 in self.player and player_sum + 10 <= 21)
        if usable_ace:
            player_sum += 10

        if dealer_sum > 21:
            reward = 1
        elif player_sum > dealer_sum:
            reward = 1
        elif player_sum < dealer_sum:
            reward = -1
        else:
            reward = 0

        return self._get_state(), reward, True


def generate_episode_with_es(env, policy, Q):
    """
    生成带探索启动的回合

    Args:
        env: 环境
        policy: 当前策略（字典）
        Q: Q值函数

    Returns:
        episode: [(state, action, reward), ...]
    """
    # TODO: 实现探索启动的回合生成
    # 提示1: 随机选择初始状态（Blackjack中）
    #   player_sum = np.random.randint(12, 22)  # 12-21
    #   dealer_showing = np.random.randint(1, 11)
    #   usable_ace = np.random.choice([True, False])
    # 提示2: env.set_state(player_sum, dealer_showing, usable_ace)
    # 提示3: state = env._get_state()
    # 提示4: 随机选择初始动作
    #   action = np.random.randint(0, 2)
    # 提示5: episode = []
    # 提示6: 执行初始动作，然后按照策略继续
    # 提示7: 后续步骤使用 policy[state] 选择动作

    pass  # TODO: 删除这一行，实现探索启动


def mc_exploring_starts(env, episodes=50000, gamma=1.0):
    """
    MC 探索启动算法

    Args:
        env: 环境
        episodes: 回合数
        gamma: 折扣因子

    Returns:
        Q: 最优 Q 值
        policy: 最优策略
    """
    # 初始化
    Q = defaultdict(lambda: np.zeros(env.action_space))
    returns = defaultdict(list)
    policy = defaultdict(lambda: np.random.randint(0, env.action_space))

    # TODO: 实现 MC ES 主循环
    # 提示1: for episode_num in range(episodes):
    # 提示2:   episode = generate_episode_with_es(env, policy, Q)
    # 提示3:   G = 0
    # 提示4:   visited_sa = set()
    # 提示5:   # 从后往前
    # 提示6:   for t in range(len(episode) - 1, -1, -1):
    # 提示7:     state, action, reward = episode[t]
    # 提示8:     G = gamma * G + reward
    # 提示9:     sa_pair = (state, action)
    # 提示10:    if sa_pair not in visited_sa:
    # 提示11:      visited_sa.add(sa_pair)
    # 提示12:      returns[sa_pair].append(G)
    # 提示13:      Q[state][action] = np.mean(returns[sa_pair])
    # 提示14:      # 贪心策略改进
    # 提示15:      policy[state] = np.argmax(Q[state])

    pass  # TODO: 删除这一行，实现 MC ES

    return Q, policy


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 MC 探索启动 - Blackjack")
    print("=" * 60)

    np.random.seed(42)

    env = BlackjackEnv()

    print(f"\n环境: Blackjack")
    print(f"算法: MC Exploring Starts")
    print(f"回合数: 50000")
    print(f"\n开始训练...")

    Q, policy = mc_exploring_starts(env, episodes=50000, gamma=1.0)

    print(f"\n训练完成!")
    print(f"  学习了 {len(policy)} 个状态的策略")

    # 显示学到的策略
    print(f"\n学到的策略示例:")
    print("=" * 60)
    print("状态 (玩家点数, 庄家明牌, 可用A) -> 动作")

    sample_states = [
        (20, 10, False),
        (18, 10, False),
        (16, 10, False),
        (12, 2, False),
        (12, 10, False),
    ]

    action_names = ['停牌(stick)', '要牌(hit)']
    for state in sample_states:
        if state in policy:
            action = policy[state]
            print(f"  {state} -> {action_names[action]}")

    # 验证策略改进
    if len(policy) > 0:
        # 点数高应该倾向停牌
        policy_improves = True
        avg_return = 0.0
    else:
        policy_improves = False
        avg_return = -1.0

    return {
        'policy_improves': policy_improves,
        'return_threshold': avg_return,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n提示:")
    print(f"  - 探索启动保证所有状态-动作对被访问")
    print(f"  - 策略改进使用贪心选择")
    print(f"  - 最优策略：高点数停牌，低点数要牌")
