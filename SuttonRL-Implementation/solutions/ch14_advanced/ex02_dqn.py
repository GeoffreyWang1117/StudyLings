"""
解答: DQN (Deep Q-Network)

这是 ex02_dqn.py 的完整实现解答
"""

import numpy as np
from collections import deque
import random


class CartPole:
    """CartPole环境"""

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

        done = (
            x < -self.x_threshold
            or x > self.x_threshold
            or theta < -self.theta_threshold
            or theta > self.theta_threshold
            or self.steps >= 500
        )

        reward = 1.0 if not done else 0.0

        return self.state, reward, done


class ReplayBuffer:
    """经验回放缓冲区"""

    def __init__(self, capacity=10000):
        """
        初始化

        Args:
            capacity: 缓冲区容量
        """
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        """
        存储转移

        Args:
            state: 当前状态
            action: 动作
            reward: 奖励
            next_state: 下一状态
            done: 是否终止
        """
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        """
        随机采样批次

        Args:
            batch_size: 批次大小

        Returns:
            states, actions, rewards, next_states, dones
        """
        batch = random.sample(self.buffer, batch_size)

        # 分离各个元素
        states = np.array([x[0] for x in batch])
        actions = np.array([x[1] for x in batch])
        rewards = np.array([x[2] for x in batch])
        next_states = np.array([x[3] for x in batch])
        dones = np.array([x[4] for x in batch])

        return states, actions, rewards, next_states, dones

    def __len__(self):
        """返回缓冲区大小"""
        return len(self.buffer)


class QNetwork:
    """Q网络（简化为线性）"""

    def __init__(self, state_dim, action_dim, alpha=0.001):
        """
        初始化

        Args:
            state_dim: 状态维度
            action_dim: 动作维度
            alpha: 学习率
        """
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.alpha = alpha
        self.weights = np.random.randn(state_dim, action_dim) * 0.01

    def forward(self, state):
        """
        前向传播计算Q值

        Q(s, a) = W^T s  (线性近似)

        Args:
            state: 状态或状态批次

        Returns:
            q_values: 所有动作的Q值
        """
        # 处理单个状态或批次
        if state.ndim == 1:
            state = state.reshape(1, -1)

        return state @ self.weights

    def update(self, states, actions, targets):
        """
        更新Q网络参数

        最小化: L = (target - Q(s, a))²

        Args:
            states: 状态批次
            actions: 动作批次
            targets: TD目标批次
        """
        # 计算当前Q值
        q_values = self.forward(states)  # [batch_size, action_dim]

        # 提取选择动作的Q值
        q_selected = q_values[np.arange(len(actions)), actions]

        # 计算误差
        errors = targets - q_selected

        # 计算梯度并更新（简化的梯度下降）
        for i in range(len(states)):
            grad = np.outer(states[i], np.zeros(self.action_dim))
            grad[:, actions[i]] = states[i]
            self.weights += self.alpha * errors[i] * grad

    def copy_from(self, other):
        """
        从另一个网络复制参数

        Args:
            other: 源网络
        """
        self.weights = other.weights.copy()


def dqn(env, episodes=500, gamma=0.99, epsilon_start=1.0, epsilon_end=0.01,
        epsilon_decay=0.995, batch_size=32, target_update=10):
    """
    DQN算法

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

    # 初始化网络和缓冲区
    q_network = QNetwork(state_dim, action_dim, alpha=0.001)
    target_network = QNetwork(state_dim, action_dim)
    target_network.copy_from(q_network)

    replay_buffer = ReplayBuffer(capacity=10000)

    episode_returns = []
    epsilon = epsilon_start

    for episode in range(episodes):
        state = env.reset()
        episode_return = 0

        while True:
            # ε-greedy动作选择
            if np.random.random() < epsilon:
                action = np.random.randint(action_dim)
            else:
                q_values = q_network.forward(state)
                action = np.argmax(q_values)

            next_state, reward, done = env.step(action)
            episode_return += reward

            # 存储经验
            replay_buffer.push(state, action, reward, next_state, done)

            # 训练（如果有足够经验）
            if len(replay_buffer) >= batch_size:
                states, actions, rewards, next_states, dones = replay_buffer.sample(batch_size)

                # 计算TD目标（使用目标网络）
                next_q_values = target_network.forward(next_states)
                max_next_q = np.max(next_q_values, axis=1)
                targets = rewards + gamma * max_next_q * (1 - dones)

                # 更新Q网络
                q_network.update(states, actions, targets)

            state = next_state

            if done:
                break

        episode_returns.append(episode_return)

        # 更新目标网络
        if episode % target_update == 0:
            target_network.copy_from(q_network)

        # 衰减epsilon
        epsilon = max(epsilon_end, epsilon * epsilon_decay)

    return q_network, episode_returns


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 DQN - CartPole [解答版本]")
    print("=" * 60)

    np.random.seed(42)
    random.seed(42)

    env = CartPole()

    print(f"\n开始训练...")
    print(f"  回合数: 500")
    print(f"  批次大小: 32")
    print(f"  目标网络更新: 每10回合")

    q_network, episode_returns = dqn(env, episodes=500, batch_size=32, target_update=10)

    # 分析结果
    early_avg = np.mean(episode_returns[:50])
    late_avg = np.mean(episode_returns[-50:])

    print(f"\n训练完成!")
    print(f"  前50回合平均回报: {early_avg:.2f}")
    print(f"  后50回合平均回报: {late_avg:.2f}")
    print(f"  改进: {late_avg - early_avg:.2f}")

    # 学习曲线
    print(f"\n学习曲线 (每50回合):")
    for i in range(0, len(episode_returns), 50):
        avg = np.mean(episode_returns[i:i+50])
        bar_len = int(avg / 10)
        print(f"  回合 {i:3d}-{i+50:3d}: {'█' * bar_len} {avg:.1f}")

    converges = late_avg > early_avg

    return {
        'converges': converges,
        'avg_return': late_avg,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n✅ 解答说明:")
    print(f"  1. Q网络: Q(s,a;θ) = W^T s (线性近似)")
    print(f"  2. 经验回放: 存储(s,a,r,s')，随机采样批次")
    print(f"  3. 目标网络: θ⁻固定，稳定TD目标")
    print(f"  4. ε衰减: 从探索到利用")
    print(f"\nDQN的关键创新:")
    print(f"  - Experience Replay打破数据相关性")
    print(f"  - Target Network稳定训练")
    print(f"  - 这两个技巧对深度RL至关重要")
