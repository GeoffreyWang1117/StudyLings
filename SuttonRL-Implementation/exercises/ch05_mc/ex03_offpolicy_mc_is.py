"""
练习: Off-policy MC with Importance Sampling

算法描述:
Off-policy蒙特卡洛使用重要性采样来从行为策略b生成的数据中学习目标策略π。
这允许我们使用探索性策略收集数据，同时学习确定性最优策略。

核心思想:
- 行为策略b: 用于生成数据（如ε-greedy）
- 目标策略π: 我们想要学习的策略（如贪心）
- 重要性采样比率: ρ = π(A|S) / b(A|S)
- 加权回报: G' = ρ·G

两种方法:
1. 普通重要性采样: V(s) = Σρ_i·G_i / n
2. 加权重要性采样: V(s) = Σρ_i·G_i / Σρ_i

伪代码:
┌────────────────────────────────────────────────────┐
│ 初始化: Q(s,a), C(s,a) = 0, π(s) = 贪心(Q)         │
│                                                    │
│ 循环（对每个回合）:                                │
│   b = 任意软策略（覆盖π）                          │
│   生成回合: S_0,A_0,R_1,...,S_T 遵循b              │
│   G ← 0                                            │
│   W ← 1  [累积重要性采样权重]                      │
│                                                    │
│   对t = T-1, T-2, ..., 0:                          │
│     G ← γG + R_{t+1}                               │
│     C(S_t,A_t) ← C(S_t,A_t) + W                    │
│     Q(S_t,A_t) ← Q(S_t,A_t) + W/C(S_t,A_t)[G-Q(S_t,A_t)]│
│     π(S_t) ← argmax_a Q(S_t,a)                     │
│                                                    │
│     if A_t ≠ π(S_t): 跳出循环  [重要性采样截断]    │
│     W ← W · 1/b(A_t|S_t)  [更新权重]               │
└────────────────────────────────────────────────────┘

要求:
- 实现加权重要性采样
- 使用ε-greedy作为行为策略
- 使用贪心作为目标策略
- 观察off-policy学习效果

参考: Sutton & Barto 第5章, 第5.6节
"""

import numpy as np
from collections import defaultdict


class BlackjackEnv:
    """Blackjack环境"""
    def __init__(self):
        self.action_space = 2

    def reset(self):
        self.player = [self._draw_card(), self._draw_card()]
        self.dealer_showing = self._draw_card()
        self.dealer_hidden = self._draw_card()
        return self._get_state()

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


def behavior_policy(Q, state, epsilon=0.1):
    """行为策略: ε-greedy"""
    if np.random.random() < epsilon:
        return np.random.randint(2)
    else:
        return np.argmax(Q[state])


def target_policy(Q, state):
    """目标策略: 贪心"""
    return np.argmax(Q[state])


def offpolicy_mc_control(env, episodes=100000, gamma=1.0, epsilon=0.1):
    """
    Off-policy MC Control with Weighted Importance Sampling

    Args:
        env: 环境
        episodes: 回合数
        gamma: 折扣因子
        epsilon: 行为策略探索率

    Returns:
        Q: 学到的动作值函数
        policy: 目标策略
    """
    Q = defaultdict(lambda: np.zeros(env.action_space))
    C = defaultdict(lambda: np.zeros(env.action_space))
    
    # TODO: 实现Off-policy MC主循环
    # 提示: 参考伪代码，重点是重要性采样权重W的计算
    
    pass  # TODO: 删除这一行
    
    policy = defaultdict(int)
    for s in Q:
        policy[s] = np.argmax(Q[s])
    
    return Q, policy


def test():
    print("=" * 60)
    print("测试 Off-policy MC - Blackjack")
    print("=" * 60)
    
    np.random.seed(42)
    env = BlackjackEnv()
    
    print(f"\n开始训练 (100000回合)...")
    Q, policy = offpolicy_mc_control(env, episodes=100000, gamma=1.0, epsilon=0.1)
    
    print(f"\n学习了 {len(policy)} 个状态的策略")
    
    print(f"\n示例策略:")
    action_names = ['停牌', '要牌']
    for state in [(20, 10, False), (18, 10, False), (12, 2, False)]:
        if state in policy:
            print(f"  {state} -> {action_names[policy[state]]}")
    
    return {'learns': len(policy) > 0}


if __name__ == '__main__':
    test()
    print(f"\n提示: Off-policy允许从探索数据中学习最优策略")
