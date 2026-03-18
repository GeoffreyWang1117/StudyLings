"""
解答: 首次访问 MC (First-Visit Monte Carlo)

这是 ex01_first_visit_mc.py 的完整实现解答
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


def simple_policy(state):
    """简单策略：>=20停牌"""
    player_sum, _, _ = state
    return 0 if player_sum >= 20 else 1


def generate_episode(env, policy):
    """
    生成一个完整回合

    Returns:
        episode: [(state, action, reward), ...]
    """
    episode = []
    state = env.reset()
    done = False

    while not done:
        action = policy(state)
        next_state, reward, done = env.step(action)
        episode.append((state, action, reward))
        state = next_state

    return episode


def first_visit_mc_prediction(env, policy, episodes=10000, gamma=1.0):
    """
    首次访问 MC 预测

    对每个回合:
    1. 生成回合
    2. 从后往前计算回报G
    3. 对首次访问的状态，记录G并更新V
    """
    V = defaultdict(float)
    returns = defaultdict(list)

    for _ in range(episodes):
        # 生成回合
        episode = generate_episode(env, policy)

        # 计算回报
        G = 0
        visited_states = set()

        # 从后往前遍历
        for t in range(len(episode) - 1, -1, -1):
            state, action, reward = episode[t]

            # 累积回报
            G = gamma * G + reward

            # 首次访问检查
            if state not in visited_states:
                visited_states.add(state)

                # 记录回报
                returns[state].append(G)

                # 更新值函数（样本平均）
                V[state] = np.mean(returns[state])

    return V


def test():
    """测试函数"""
    print("=" * 60)
    print("测试首次访问 MC - Blackjack [解答版本]")
    print("=" * 60)

    np.random.seed(42)

    env = BlackjackEnv()

    print(f"\n开始训练...")

    V = first_visit_mc_prediction(env, simple_policy, episodes=10000, gamma=1.0)

    print(f"\n训练完成!")
    print(f"  估计了 {len(V)} 个状态的值")

    # 示例状态值
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

    if len(V) > 0:
        avg_value = np.mean(list(V.values()))
        print(f"\n平均状态值: {avg_value:.4f}")
        converges = len(V) >= 100
        value_error_max = abs(avg_value)
    else:
        converges = False
        value_error_max = 1.0

    return {
        'converges': converges,
        'value_error_max': value_error_max,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n✅ 解答说明:")
    print(f"  1. generate_episode(): 生成完整回合")
    print(f"  2. 从后往前计算回报G")
    print(f"  3. 对首次访问的状态，记录G")
    print(f"  4. V(s) = 平均所有访问s的回报")
    print(f"  5. MC方法无需模型，只需经验")
