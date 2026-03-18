"""
解答: Double DQN
"""

import numpy as np
from collections import deque
import random


class CartPole:
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
        temp = (force + self.masspole * self.length * theta_dot**2 * sintheta) / (self.masscart + self.masspole)
        thetaacc = (self.gravity * sintheta - costheta * temp) / (self.length * (4.0 / 3.0 - self.masspole * costheta**2 / (self.masscart + self.masspole)))
        xacc = temp - self.masspole * self.length * thetaacc * costheta / (self.masscart + self.masspole)
        x = x + self.tau * x_dot
        x_dot = x_dot + self.tau * xacc
        theta = theta + self.tau * theta_dot
        theta_dot = theta_dot + self.tau * thetaacc
        self.state = np.array([x, x_dot, theta, theta_dot])
        self.steps += 1
        done = (x < -self.x_threshold or x > self.x_threshold or theta < -self.theta_threshold or theta > self.theta_threshold or self.steps >= 500)
        reward = 1.0 if not done else 0.0
        return self.state, reward, done


class ReplayBuffer:
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)
    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))
    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        return (np.array([x[0] for x in batch]), np.array([x[1] for x in batch]), 
                np.array([x[2] for x in batch]), np.array([x[3] for x in batch]), 
                np.array([x[4] for x in batch]))
    def __len__(self):
        return len(self.buffer)


class QNetwork:
    def __init__(self, state_dim, action_dim, alpha=0.001):
        self.state_dim, self.action_dim, self.alpha = state_dim, action_dim, alpha
        self.weights = np.random.randn(state_dim, action_dim) * 0.01
    def forward(self, state):
        if state.ndim == 1: state = state.reshape(1, -1)
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


def double_dqn(env, episodes=500, gamma=0.99, epsilon_start=1.0, epsilon_end=0.01, epsilon_decay=0.995, batch_size=32, target_update=10):
    q_network = QNetwork(4, 2, alpha=0.001)
    target_network = QNetwork(4, 2)
    target_network.copy_from(q_network)
    replay_buffer = ReplayBuffer(10000)
    episode_returns = []
    epsilon = epsilon_start
    
    for episode in range(episodes):
        state = env.reset()
        episode_return = 0
        while True:
            if np.random.random() < epsilon:
                action = np.random.randint(2)
            else:
                action = np.argmax(q_network.forward(state))
            next_state, reward, done = env.step(action)
            episode_return += reward
            replay_buffer.push(state, action, reward, next_state, done)
            
            if len(replay_buffer) >= batch_size:
                states, actions, rewards, next_states, dones = replay_buffer.sample(batch_size)
                # Double DQN核心
                online_q_values = q_network.forward(next_states)
                best_actions = np.argmax(online_q_values, axis=1)
                target_q_values = target_network.forward(next_states)
                selected_q = target_q_values[np.arange(batch_size), best_actions]
                targets = rewards + gamma * selected_q * (1 - dones)
                q_network.update(states, actions, targets)
            
            state = next_state
            if done: break
        
        episode_returns.append(episode_return)
        if episode % target_update == 0:
            target_network.copy_from(q_network)
        epsilon = max(epsilon_end, epsilon * epsilon_decay)
    
    return q_network, episode_returns


def test():
    print("=" * 60)
    print("测试 Double DQN [解答版本]")
    print("=" * 60)
    np.random.seed(42)
    random.seed(42)
    env = CartPole()
    q_network, episode_returns = double_dqn(env, episodes=500)
    early_avg = np.mean(episode_returns[:50])
    late_avg = np.mean(episode_returns[-50:])
    print(f"\n前50回合: {early_avg:.2f}, 后50回合: {late_avg:.2f}")
    print(f"\n✅ 核心改进: a*=argmax Q(s',a;θ), y=r+γQ(s',a*;θ⁻)")
    print(f"  在线网络选择动作，目标网络评估，减少过估计")
    return {'converges': late_avg > early_avg, 'avg_return': late_avg}


if __name__ == '__main__':
    test()
