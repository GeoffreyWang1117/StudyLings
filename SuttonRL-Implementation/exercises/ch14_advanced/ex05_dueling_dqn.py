"""
练习: Dueling DQN

算法描述:
Dueling DQN通过分离值函数V(s)和优势函数A(s,a)的表示来改进DQN架构。
这种架构更容易学习哪些状态本身就有价值，而不管采取什么动作。

核心思想:
- 标准DQN: Q(s,a) 直接输出
- Dueling DQN: Q(s,a) = V(s) + [A(s,a) - mean_a A(s,a)]

架构:
输入s -> 共享层 -> 分支:
                   ├─ 值流: V(s)
                   └─ 优势流: A(s,a) 对所有动作
Q(s,a) = V(s) + A(s,a) - mean(A(s,:))

优势:
- 更好地识别状态价值
- 在动作影响小的状态下学习更快
- 对Q值的更新更高效

参考: Wang et al. (2016) "Dueling Network Architectures for Deep RL"
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
        costheta, sintheta = np.cos(theta), np.sin(theta)
        temp = (force + self.masspole * self.length * theta_dot**2 * sintheta) / (self.masscart + self.masspole)
        thetaacc = (self.gravity * sintheta - costheta * temp) / (self.length * (4.0 / 3.0 - self.masspole * costheta**2 / (self.masscart + self.masspole)))
        xacc = temp - self.masspole * self.length * thetaacc * costheta / (self.masscart + self.masspole)
        x, x_dot = x + self.tau * x_dot, x_dot + self.tau * xacc
        theta, theta_dot = theta + self.tau * theta_dot, theta_dot + self.tau * thetaacc
        self.state = np.array([x, x_dot, theta, theta_dot])
        self.steps += 1
        done = (x < -self.x_threshold or x > self.x_threshold or theta < -self.theta_threshold or theta > self.theta_threshold or self.steps >= 500)
        return self.state, (1.0 if not done else 0.0), done


class ReplayBuffer:
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)
    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))
    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        return (np.array([x[0] for x in batch]), np.array([x[1] for x in batch]), np.array([x[2] for x in batch]), np.array([x[3] for x in batch]), np.array([x[4] for x in batch]))
    def __len__(self):
        return len(self.buffer)


class DuelingQNetwork:
    """Dueling Q Network (线性近似)"""
    def __init__(self, state_dim, action_dim, alpha=0.001):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.alpha = alpha
        # TODO: 初始化值流和优势流参数
        self.value_weights = np.random.randn(state_dim, 1) * 0.01
        self.advantage_weights = np.random.randn(state_dim, action_dim) * 0.01
    
    def forward(self, state):
        """
        前向传播: Q(s,a) = V(s) + [A(s,a) - mean_a A(s,a)]
        """
        if state.ndim == 1:
            state = state.reshape(1, -1)
        # TODO: 计算V(s)和A(s,a)
        values = state @ self.value_weights  # [batch, 1]
        advantages = state @ self.advantage_weights  # [batch, actions]
        # TODO: 合并: Q = V + (A - mean(A))
        q_values = values + (advantages - np.mean(advantages, axis=1, keepdims=True))
        return q_values
    
    def update(self, states, actions, targets):
        # 简化更新（实际应分别更新两个流）
        q_values = self.forward(states)
        errors = targets - q_values[np.arange(len(actions)), actions]
        for i in range(len(states)):
            # 更新值流
            self.value_weights += self.alpha * errors[i] * states[i].reshape(-1, 1)
            # 更新优势流
            grad_adv = np.zeros((self.state_dim, self.action_dim))
            grad_adv[:, actions[i]] = states[i]
            self.advantage_weights += self.alpha * errors[i] * grad_adv
    
    def copy_from(self, other):
        self.value_weights = other.value_weights.copy()
        self.advantage_weights = other.advantage_weights.copy()


def dueling_dqn(env, episodes=500, gamma=0.99, epsilon_start=1.0, epsilon_end=0.01, epsilon_decay=0.995, batch_size=32, target_update=10):
    q_network = DuelingQNetwork(4, 2, alpha=0.001)
    target_network = DuelingQNetwork(4, 2)
    target_network.copy_from(q_network)
    replay_buffer = ReplayBuffer(10000)
    episode_returns = []
    epsilon = epsilon_start
    
    # TODO: 实现Dueling DQN主循环（与Double DQN类似）
    pass  # TODO
    
    return q_network, episode_returns


def test():
    print("=" * 60)
    print("测试 Dueling DQN - CartPole")
    print("=" * 60)
    np.random.seed(42)
    random.seed(42)
    env = CartPole()
    q_network, episode_returns = dueling_dqn(env, episodes=500)
    early_avg = np.mean(episode_returns[:50])
    late_avg = np.mean(episode_returns[-50:])
    print(f"\n前50回合: {early_avg:.2f}, 后50回合: {late_avg:.2f}")
    return {'converges': late_avg > early_avg, 'avg_return': late_avg}


if __name__ == '__main__':
    test()
    print(f"\n提示: Dueling架构分离V(s)和A(s,a)，学习更高效")
