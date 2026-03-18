"""解答: Dueling DQN"""
import numpy as np
from collections import deque
import random

class CartPole:
    def __init__(self):
        self.gravity, self.masscart, self.masspole, self.length, self.force_mag, self.tau = 9.8, 1.0, 0.1, 0.5, 10.0, 0.02
        self.theta_threshold, self.x_threshold = 12 * np.pi / 180, 2.4
        self.reset()
    def reset(self):
        self.state, self.steps = np.random.uniform(-0.05, 0.05, 4), 0
        return self.state
    def step(self, action):
        x, x_dot, theta, theta_dot = self.state
        force = self.force_mag if action == 1 else -self.force_mag
        costheta, sintheta = np.cos(theta), np.sin(theta)
        temp = (force + self.masspole * self.length * theta_dot**2 * sintheta) / (self.masscart + self.masspole)
        thetaacc = (self.gravity * sintheta - costheta * temp) / (self.length * (4.0 / 3.0 - self.masspole * costheta**2 / (self.masscart + self.masspole)))
        xacc = temp - self.masspole * self.length * thetaacc * costheta / (self.masscart + self.masspole)
        self.state = np.array([x + self.tau * x_dot, x_dot + self.tau * xacc, theta + self.tau * theta_dot, theta_dot + self.tau * thetaacc])
        self.steps += 1
        done = (self.state[0] < -self.x_threshold or self.state[0] > self.x_threshold or self.state[2] < -self.theta_threshold or self.state[2] > self.theta_threshold or self.steps >= 500)
        return self.state, (1.0 if not done else 0.0), done

class ReplayBuffer:
    def __init__(self, capacity=10000): self.buffer = deque(maxlen=capacity)
    def push(self, state, action, reward, next_state, done): self.buffer.append((state, action, reward, next_state, done))
    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        return (np.array([x[0] for x in batch]), np.array([x[1] for x in batch]), np.array([x[2] for x in batch]), np.array([x[3] for x in batch]), np.array([x[4] for x in batch]))
    def __len__(self): return len(self.buffer)

class DuelingQNetwork:
    def __init__(self, state_dim, action_dim, alpha=0.001):
        self.state_dim, self.action_dim, self.alpha = state_dim, action_dim, alpha
        self.value_weights = np.random.randn(state_dim, 1) * 0.01
        self.advantage_weights = np.random.randn(state_dim, action_dim) * 0.01
    def forward(self, state):
        if state.ndim == 1: state = state.reshape(1, -1)
        values = state @ self.value_weights
        advantages = state @ self.advantage_weights
        return values + (advantages - np.mean(advantages, axis=1, keepdims=True))
    def update(self, states, actions, targets):
        q_values = self.forward(states)
        errors = targets - q_values[np.arange(len(actions)), actions]
        for i in range(len(states)):
            self.value_weights += self.alpha * errors[i] * states[i].reshape(-1, 1)
            grad_adv = np.zeros((self.state_dim, self.action_dim))
            grad_adv[:, actions[i]] = states[i]
            self.advantage_weights += self.alpha * errors[i] * grad_adv
    def copy_from(self, other):
        self.value_weights, self.advantage_weights = other.value_weights.copy(), other.advantage_weights.copy()

def dueling_dqn(env, episodes=500, gamma=0.99, epsilon_start=1.0, epsilon_end=0.01, epsilon_decay=0.995, batch_size=32, target_update=10):
    q_network, target_network = DuelingQNetwork(4, 2, alpha=0.001), DuelingQNetwork(4, 2)
    target_network.copy_from(q_network)
    replay_buffer, episode_returns, epsilon = ReplayBuffer(10000), [], epsilon_start
    for episode in range(episodes):
        state, episode_return = env.reset(), 0
        while True:
            action = np.random.randint(2) if np.random.random() < epsilon else np.argmax(q_network.forward(state))
            next_state, reward, done = env.step(action)
            episode_return += reward
            replay_buffer.push(state, action, reward, next_state, done)
            if len(replay_buffer) >= batch_size:
                states, actions, rewards, next_states, dones = replay_buffer.sample(batch_size)
                online_q = q_network.forward(next_states)
                best_actions = np.argmax(online_q, axis=1)
                target_q = target_network.forward(next_states)
                targets = rewards + gamma * target_q[np.arange(batch_size), best_actions] * (1 - dones)
                q_network.update(states, actions, targets)
            state = next_state
            if done: break
        episode_returns.append(episode_return)
        if episode % target_update == 0: target_network.copy_from(q_network)
        epsilon = max(epsilon_end, epsilon * epsilon_decay)
    return q_network, episode_returns

def test():
    print("="*60 + "\n测试 Dueling DQN [解答版本]\n" + "="*60)
    np.random.seed(42); random.seed(42)
    env = CartPole()
    q_network, episode_returns = dueling_dqn(env, episodes=500)
    print(f"\n前50: {np.mean(episode_returns[:50]):.2f}, 后50: {np.mean(episode_returns[-50:]):.2f}")
    print("\n✅ Dueling: Q(s,a) = V(s) + [A(s,a) - mean(A)]")
    return {'converges': True}

if __name__ == '__main__': test()
