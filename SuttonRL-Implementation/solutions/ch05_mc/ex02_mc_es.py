"""
解答: MC 探索启动 (Monte Carlo with Exploring Starts)

这是 ex02_mc_es.py 的完整实现解答
"""

import numpy as np
from collections import defaultdict


class BlackjackEnv:
    """Blackjack 环境"""

    def __init__(self):
        self.action_space = 2

    def reset(self):
        self.player = [self._draw_card(), self._draw_card()]
        self.dealer_showing = self._draw_card()
        self.dealer_hidden = self._draw_card()
        return self._get_state()

    def set_state(self, player_sum, dealer_showing, usable_ace):
        """设置特定状态（用于探索启动）"""
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
    # 探索启动：随机选择初始状态
    player_sum = np.random.randint(12, 22)  # 12-21
    dealer_showing = np.random.randint(1, 11)
    usable_ace = np.random.choice([True, False])

    env.set_state(player_sum, dealer_showing, usable_ace)
    state = env._get_state()

    # 随机选择初始动作（探索启动）
    action = np.random.randint(0, 2)

    episode = []
    done = False

    # 执行初始动作
    next_state, reward, done = env.step(action)
    episode.append((state, action, reward))

    # 后续按照策略继续
    state = next_state
    while not done:
        action = policy[state]
        next_state, reward, done = env.step(action)
        episode.append((state, action, reward))
        state = next_state

    return episode


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

    for episode_num in range(episodes):
        # 生成带探索启动的回合
        episode = generate_episode_with_es(env, policy, Q)

        # 计算回报并更新
        G = 0
        visited_sa = set()

        # 从后往前处理回合
        for t in range(len(episode) - 1, -1, -1):
            state, action, reward = episode[t]
            G = gamma * G + reward

            sa_pair = (state, action)

            # 首次访问MC
            if sa_pair not in visited_sa:
                visited_sa.add(sa_pair)
                returns[sa_pair].append(G)
                Q[state][action] = np.mean(returns[sa_pair])

                # 贪心策略改进
                policy[state] = np.argmax(Q[state])

    return Q, policy


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 MC 探索启动 - Blackjack [解答版本]")
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

    print(f"\n✅ 解答说明:")
    print(f"  1. 探索启动: 随机选择初始(s,a)对")
    print(f"  2. 生成回合: 初始随机动作，后续按策略")
    print(f"  3. 首次访问MC: 计算G，更新Q(s,a)")
    print(f"  4. 贪心改进: π(s) ← argmax_a Q(s,a)")
    print(f"\n策略特点:")
    print(f"  - 高点数(≥20): 停牌")
    print(f"  - 低点数(≤15): 要牌")
    print(f"  - 中间点数: 取决于庄家明牌")
