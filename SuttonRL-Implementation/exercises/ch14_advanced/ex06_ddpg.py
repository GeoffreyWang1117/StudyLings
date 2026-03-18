"""
练习: DDPG (Deep Deterministic Policy Gradient)

算法描述:
DDPG是用于连续动作空间的Actor-Critic算法，结合了DQN的经验回放和
确定性策略梯度。是2025年连续控制的基础算法之一。

核心思想:
- 确定性策略: a = μ(s|θ)
- Critic: Q(s,a|w)
- 经验回放 + 目标网络
- Ornstein-Uhlenbeck噪声用于探索

更新规则:
- Critic: 最小化 (y - Q(s,a|w))^2, 其中 y = r + γQ(s',μ(s'|θ⁻)|w⁻)
- Actor: 最大化 Q(s,μ(s|θ)|w)

参考: Lillicrap et al. (2015) "Continuous control with deep RL"
"""

import numpy as np
from collections import deque
import random


class SimplePendulum:
    """简化的Pendulum环境"""
    def __init__(self):
        self.max_speed = 8.0
        self.max_torque = 2.0
        self.dt = 0.05
        self.g = 10.0
        self.m = 1.0
        self.l = 1.0
        self.reset()

    def reset(self):
        self.theta = np.random.uniform(-np.pi, np.pi)
        self.theta_dot = np.random.uniform(-1, 1)
        return self._get_state()

    def _get_state(self):
        return np.array([np.cos(self.theta), np.sin(self.theta), self.theta_dot])

    def step(self, action):
        action = np.clip(action, -self.max_torque, self.max_torque)[0]
        
        # 动力学
        theta_dot_dot = (-3 * self.g / (2 * self.l) * np.sin(self.theta) + 
                         3.0 / (self.m * self.l ** 2) * action)
        
        self.theta_dot += theta_dot_dot * self.dt
        self.theta_dot = np.clip(self.theta_dot, -self.max_speed, self.max_speed)
        self.theta += self.theta_dot * self.dt
        
        # 归一化角度
        self.theta = ((self.theta + np.pi) % (2 * np.pi)) - np.pi
        
        # 奖励：鼓励竖直向上（theta=0）
        reward = -(self.theta**2 + 0.1 * self.theta_dot**2 + 0.001 * action**2)
        
        return self._get_state(), reward, False


class ReplayBuffer:
    def __init__(self, capacity=100000):
        self.buffer = deque(maxlen=capacity)
    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))
    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        return (np.array([x[0] for x in batch]), np.array([x[1] for x in batch]).reshape(-1, 1),
                np.array([x[2] for x in batch]), np.array([x[3] for x in batch]), 
                np.array([x[4] for x in batch]))
    def __len__(self): return len(self.buffer)


class Actor:
    """确定性策略网络（线性）"""
    def __init__(self, state_dim, action_dim, action_bound, lr=0.0001):
        self.state_dim, self.action_dim, self.action_bound = state_dim, action_dim, action_bound
        self.lr = lr
        self.weights = np.random.randn(state_dim, action_dim) * 0.01
    
    def forward(self, state):
        if state.ndim == 1: state = state.reshape(1, -1)
        return self.action_bound * np.tanh(state @ self.weights)
    
    def update(self, states, critic_grad):
        # TODO: Actor使用critic提供的梯度更新
        # 简化版本
        for i in range(len(states)):
            action_grad = self.action_bound * (1 - np.tanh(states[i] @ self.weights)**2)
            self.weights += self.lr * np.outer(states[i], critic_grad[i] * action_grad)
    
    def copy_from(self, other):
        self.weights = other.weights.copy()


class Critic:
    """Q网络（线性）"""
    def __init__(self, state_dim, action_dim, lr=0.001):
        self.state_dim, self.action_dim, self.lr = state_dim, action_dim, lr
        self.weights_s = np.random.randn(state_dim, 1) * 0.01
        self.weights_a = np.random.randn(action_dim, 1) * 0.01
    
    def forward(self, states, actions):
        if states.ndim == 1: states = states.reshape(1, -1)
        if actions.ndim == 1: actions = actions.reshape(1, -1)
        return states @ self.weights_s + actions @ self.weights_a
    
    def update(self, states, actions, targets):
        q_values = self.forward(states, actions)
        errors = targets.reshape(-1, 1) - q_values
        for i in range(len(states)):
            self.weights_s += self.lr * errors[i] * states[i].reshape(-1, 1)
            self.weights_a += self.lr * errors[i] * actions[i].reshape(-1, 1)
    
    def copy_from(self, other):
        self.weights_s, self.weights_a = other.weights_s.copy(), other.weights_a.copy()


def ddpg(env, episodes=200, gamma=0.99, tau=0.001, batch_size=64):
    """DDPG算法"""
    state_dim, action_dim, action_bound = 3, 1, env.max_torque
    
    actor = Actor(state_dim, action_dim, action_bound, lr=0.0001)
    actor_target = Actor(state_dim, action_dim, action_bound)
    actor_target.copy_from(actor)
    
    critic = Critic(state_dim, action_dim, lr=0.001)
    critic_target = Critic(state_dim, action_dim)
    critic_target.copy_from(critic)
    
    replay_buffer = ReplayBuffer(100000)
    episode_returns = []
    
    # TODO: 实现DDPG主循环
    # 提示: 添加噪声探索，软更新目标网络
    pass  # TODO
    
    return actor, critic, episode_returns


def test():
    print("=" * 60)
    print("测试 DDPG - Pendulum")
    print("=" * 60)
    np.random.seed(42); random.seed(42)
    env = SimplePendulum()
    actor, critic, episode_returns = ddpg(env, episodes=200)
    print(f"\n前50回合: {np.mean(episode_returns[:50]):.2f}")
    print(f"后50回合: {np.mean(episode_returns[-50:]):.2f}")
    return {'converges': True}


if __name__ == '__main__':
    test()
    print("\n提示: DDPG用于连续动作空间，结合DQN技巧")
