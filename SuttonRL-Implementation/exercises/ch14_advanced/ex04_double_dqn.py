"""
练习: Double DQN

算法描述:
Double DQN将Double Q-Learning的思想应用于DQN，通过解耦动作选择和评估
来减少DQN的过估计问题。这是DQN最重要的改进之一。

问题背景:
标准DQN使用: y = r + γ max_a' Q(s',a'; θ⁻)
这会导致过估计，因为用同一个网络选择和评估动作

Double DQN的解决方案:
- 用在线网络θ选择动作: a* = argmax_a Q(s',a; θ)
- 用目标网络θ⁻评估动作: y = r + γ Q(s', a*; θ⁻)

核心改进:
标准DQN: y = r + γ max_a Q(s',a; θ⁻)
Double DQN: y = r + γ Q(s', argmax_a Q(s',a; θ); θ⁻)

伪代码:
┌────────────────────────────────────────────────────┐
│ 初始化: Q网络θ, 目标网络θ⁻=θ, 经验池D              │
│                                                    │
│ 对每个回合:                                        │
│   对回合中的每一步:                                │
│     ε-greedy选择动作a                              │
│     存储(s,a,r,s')到D                              │
│                                                    │
│     从D采样批次                                    │
│     对批次中的每个(s,a,r,s',done):                 │
│       if done:                                     │
│         y = r                                      │
│       else:                                        │
│         a* = argmax_a' Q(s',a'; θ)  [在线网络选择] │
│         y = r + γQ(s',a*; θ⁻)       [目标网络评估] │
│                                                    │
│       损失: L = (y - Q(s,a; θ))²                   │
│       更新θ                                        │
│                                                    │
│     每C步: θ⁻ ← θ                                  │
└────────────────────────────────────────────────────┘

使用 CartPole 环境

要求:
- 实现Double DQN
- 对比标准DQN
- 观察减少过估计的效果
- 性能应优于标准DQN

参考: van Hasselt et al. (2015) "Deep Reinforcement Learning with Double Q-learning"
"""

import numpy as np
from collections import deque
import random


class CartPole:
    """CartPole环境（同ex02）"""
    
    def __init__(self):
        self.gravity = 9.8
        self.masscart = 1.0
        self.masspole = 0.1
        self.length = 0.5
        self.force_mag = 10.0
        self.tau = 0.02
        self.theta_threshold = 12 * np.pi / 180
        self.x_threshold = 2.4
        self.reset()

    def reset(self):
        self.state = np.random.uniform(-0.05, 0.05, 4)
        self.steps = 0
        return self.state

    def step(self, action):
        x, x_dot, theta, theta_dot = self.state
        force = self.force_mag if action == 1 else -self.force_mag
        
        costheta = np.cos(theta)
        sintheta = np.sin(theta)
        
        temp = (force + self.masspole * self.length * theta_dot**2 * sintheta) / (
            self.masscart + self.masspole
        )
        thetaacc = (self.gravity * sintheta - costheta * temp) / (
            self.length * (4.0 / 3.0 - self.masspole * costheta**2 / (self.masscart + self.masspole))
        )
        xacc = temp - self.masspole * self.length * thetaacc * costheta / (self.masscart + self.masspole)
        
        x = x + self.tau * x_dot
        x_dot = x_dot + self.tau * xacc
        theta = theta + self.tau * theta_dot
        theta_dot = theta_dot + self.tau * thetaacc
        
        self.state = np.array([x, x_dot, theta, theta_dot])
        self.steps += 1
        
        done = (x < -self.x_threshold or x > self.x_threshold or 
                theta < -self.theta_threshold or theta > self.theta_threshold or
                self.steps >= 500)
        
        reward = 1.0 if not done else 0.0
        return self.state, reward, done


class ReplayBuffer:
    """经验回放（同ex02）"""
    
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)
    
    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))
    
    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states = np.array([x[0] for x in batch])
        actions = np.array([x[1] for x in batch])
        rewards = np.array([x[2] for x in batch])
        next_states = np.array([x[3] for x in batch])
        dones = np.array([x[4] for x in batch])
        return states, actions, rewards, next_states, dones
    
    def __len__(self):
        return len(self.buffer)


class QNetwork:
    """Q网络（线性近似）"""
    
    def __init__(self, state_dim, action_dim, alpha=0.001):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.alpha = alpha
        self.weights = np.random.randn(state_dim, action_dim) * 0.01
    
    def forward(self, state):
        if state.ndim == 1:
            state = state.reshape(1, -1)
        return state @ self.weights
    
    def update(self, states, actions, targets):
        q_values = self.forward(states)
        q_selected = q_values[np.arange(len(actions)), actions]
        errors = targets - q_selected
        
        for i in range(len(states)):
            grad = np.outer(states[i], np.zeros(self.action_dim))
            grad[:, actions[i]] = states[i]
            self.weights += self.alpha * errors[i] * grad
    
    def copy_from(self, other):
        self.weights = other.weights.copy()


def double_dqn(env, episodes=500, gamma=0.99, epsilon_start=1.0, epsilon_end=0.01,
               epsilon_decay=0.995, batch_size=32, target_update=10):
    """
    Double DQN算法

    Args:
        env: 环境
        episodes: 回合数
        gamma: 折扣因子
        epsilon_start: 初始探索率
        epsilon_end: 最终探索率
        epsilon_decay: 探索率衰减
        batch_size: 批次大小
        target_update: 目标网络更新频率

    Returns:
        q_network: 训练好的Q网络
        episode_returns: 每回合总回报
    """
    state_dim = 4
    action_dim = 2
    
    q_network = QNetwork(state_dim, action_dim, alpha=0.001)
    target_network = QNetwork(state_dim, action_dim)
    target_network.copy_from(q_network)
    
    replay_buffer = ReplayBuffer(capacity=10000)
    episode_returns = []
    epsilon = epsilon_start
    
    # TODO: 实现Double DQN主循环
    # 提示1: for episode in range(episodes):
    # 提示2:   state = env.reset()
    # 提示3:   episode_return = 0
    # 提示4:
    # 提示5:   while True:
    # 提示6:     # ε-greedy
    # 提示7:     if np.random.random() < epsilon:
    # 提示8:       action = np.random.randint(action_dim)
    # 提示9:     else:
    # 提示10:      q_values = q_network.forward(state)
    # 提示11:      action = np.argmax(q_values)
    # 提示12:
    # 提示13:    next_state, reward, done = env.step(action)
    # 提示14:    episode_return += reward
    # 提示15:    replay_buffer.push(state, action, reward, next_state, done)
    # 提示16:
    # 提示17:    if len(replay_buffer) >= batch_size:
    # 提示18:      states, actions, rewards, next_states, dones = replay_buffer.sample(batch_size)
    # 提示19:
    # 提示20:      # Double DQN: 用在线网络选择，目标网络评估
    # 提示21:      online_q_values = q_network.forward(next_states)
    # 提示22:      best_actions = np.argmax(online_q_values, axis=1)  # 在线网络选择
    # 提示23:
    # 提示24:      target_q_values = target_network.forward(next_states)
    # 提示25:      selected_q = target_q_values[np.arange(batch_size), best_actions]  # 目标网络评估
    # 提示26:
    # 提示27:      targets = rewards + gamma * selected_q * (1 - dones)
    # 提示28:      q_network.update(states, actions, targets)
    # 提示29:
    # 提示30:    state = next_state
    # 提示31:    if done:
    # 提示32:      break
    # 提示33:
    # 提示34:  episode_returns.append(episode_return)
    # 提示35:
    # 提示36:  if episode % target_update == 0:
    # 提示37:    target_network.copy_from(q_network)
    # 提示38:
    # 提示39:  epsilon = max(epsilon_end, epsilon * epsilon_decay)
    
    pass  # TODO: 删除这一行
    
    return q_network, episode_returns


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 Double DQN - CartPole")
    print("=" * 60)
    
    np.random.seed(42)
    random.seed(42)
    
    env = CartPole()
    
    print(f"\n开始训练...")
    q_network, episode_returns = double_dqn(env, episodes=500)
    
    early_avg = np.mean(episode_returns[:50])
    late_avg = np.mean(episode_returns[-50:])
    
    print(f"\n训练完成!")
    print(f"  前50回合平均: {early_avg:.2f}")
    print(f"  后50回合平均: {late_avg:.2f}")
    
    return {'converges': late_avg > early_avg, 'avg_return': late_avg}


if __name__ == '__main__':
    result = test()
    
    print(f"\n提示:")
    print(f"  - Double DQN减少Q值过估计")
    print(f"  - 在线网络选择，目标网络评估")
    print(f"  - 比标准DQN更稳定")
    print(f"  - 2025年几乎所有DQN实现都用此方法")
