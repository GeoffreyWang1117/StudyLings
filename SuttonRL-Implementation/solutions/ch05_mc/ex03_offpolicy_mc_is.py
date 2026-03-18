"""
解答: Off-policy MC with Importance Sampling
"""

import numpy as np
from collections import defaultdict


class BlackjackEnv:
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
        if usable_ace: player_sum += 10
        return (player_sum, self.dealer_showing, usable_ace)

    def step(self, action):
        if action == 1:
            self.player.append(self._draw_card())
            player_sum = sum(self.player)
            usable_ace = (1 in self.player and player_sum + 10 <= 21)
            if usable_ace: player_sum += 10
            if player_sum > 21:
                return self._get_state(), -1, True
            else:
                return self._get_state(), 0, False
        else:
            return self._dealer_play()

    def _dealer_play(self):
        dealer = [self.dealer_showing, self.dealer_hidden]
        while True:
            dealer_sum = sum(dealer)
            usable_ace = (1 in dealer and dealer_sum + 10 <= 21)
            if usable_ace: dealer_sum += 10
            if dealer_sum >= 17: break
            dealer.append(self._draw_card())

        player_sum = sum(self.player)
        usable_ace = (1 in self.player and player_sum + 10 <= 21)
        if usable_ace: player_sum += 10

        if dealer_sum > 21: reward = 1
        elif player_sum > dealer_sum: reward = 1
        elif player_sum < dealer_sum: reward = -1
        else: reward = 0

        return self._get_state(), reward, True


def offpolicy_mc_control(env, episodes=100000, gamma=1.0, epsilon=0.1):
    Q = defaultdict(lambda: np.zeros(env.action_space))
    C = defaultdict(lambda: np.zeros(env.action_space))
    
    for episode in range(episodes):
        # 生成回合（行为策略：ε-greedy）
        trajectory = []
        state = env.reset()
        done = False
        
        while not done:
            if np.random.random() < epsilon:
                action = np.random.randint(2)
            else:
                action = np.argmax(Q[state])
            next_state, reward, done = env.step(action)
            trajectory.append((state, action, reward))
            state = next_state
        
        # 加权重要性采样
        G = 0
        W = 1
        
        for t in reversed(range(len(trajectory))):
            state, action, reward = trajectory[t]
            G = gamma * G + reward
            C[state][action] += W
            Q[state][action] += (W / C[state][action]) * (G - Q[state][action])
            
            # 目标策略是贪心的
            if action != np.argmax(Q[state]):
                break  # 重要性采样截断
            
            # 更新权重 W *= π(a|s) / b(a|s)
            # π(a|s) = 1 (贪心), b(a|s) = 1-ε+ε/2 (ε-greedy的贪心动作)
            W *= 1.0 / (1 - epsilon + epsilon / 2)
    
    policy = defaultdict(int)
    for s in Q:
        policy[s] = np.argmax(Q[s])
    
    return Q, policy


def test():
    print("=" * 60)
    print("测试 Off-policy MC [解答版本]")
    print("=" * 60)
    
    np.random.seed(42)
    env = BlackjackEnv()
    Q, policy = offpolicy_mc_control(env, episodes=100000, gamma=1.0, epsilon=0.1)
    
    print(f"\n学习了 {len(policy)} 个状态的策略")
    print(f"\n✅ 核心: ρ = π(a|s) / b(a|s), 加权重要性采样")
    
    return {'learns': len(policy) > 0}


if __name__ == '__main__':
    test()
