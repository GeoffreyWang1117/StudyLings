"""
练习: DQN (Deep Q-Network)

算法描述:
DQN是第一个成功将深度学习应用于RL的算法。它使用神经网络近似Q函数，
并引入了经验回放和目标网络两个关键技巧来稳定训练。

核心思想:
- Q网络: Q(s, a; θ) 近似最优动作值函数
- 经验回放: 存储经验(s,a,r,s')，随机采样批次训练
- 目标网络: 使用固定的旧参数 θ⁻ 计算TD目标
- ε-贪心探索: 逐渐减小ε

关键创新:
1. Experience Replay: 打破数据相关性
2. Target Network: 稳定训练目标
3. 端到端学习: 直接从像素到动作

伪代码:
┌────────────────────────────────────────────────────┐
│ 初始化: Q网络参数 θ, 目标网络参数 θ⁻ = θ           │
│        经验回放缓冲区 D                             │
│                                                    │
│ 对每个回合:                                        │
│   初始化 S                                         │
│                                                    │
│   对回合中的每一步:                                │
│     以概率 ε 选择随机动作 A                        │
│     否则 A = argmax_a Q(S, a; θ)                   │
│                                                    │
│     执行 A, 观察 R, S'                             │
│     存储转移 (S, A, R, S') 到 D                    │
│                                                    │
│     从 D 随机采样批次 {(s,a,r,s')}                 │
│     对批次中的每个样本:                            │
│       if s' 是终止:                                │
│         y = r                                      │
│       else:                                        │
│         y = r + γ max_a' Q(s', a'; θ⁻)            │
│                                                    │
│       损失: L = (y - Q(s, a; θ))²                  │
│       梯度下降更新 θ                               │
│                                                    │
│     每 C 步: θ⁻ ← θ (更新目标网络)                 │
│     S ← S'                                         │
└────────────────────────────────────────────────────┘

使用 CartPole 环境

要求:
- 实现Q网络（简化为线性）
- 实现经验回放缓冲区
- 实现目标网络
- 实现DQN训练循环
- 观察训练稳定性

参考: Mnih et al. (2015) "Human-level control through deep reinforcement learning"
"""

import numpy as np
from collections import deque
import random


class CartPole:
    """CartPole环境（同上）"""

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
        # TODO: 实现经验存储
        # 提示: self.buffer.append((state, action, reward, next_state, done))

        pass  # TODO: 删除这一行

    def sample(self, batch_size):
        """
        随机采样批次

        Args:
            batch_size: 批次大小

        Returns:
            states, actions, rewards, next_states, dones
        """
        # TODO: 实现批次采样
        # 提示1: batch = random.sample(self.buffer, batch_size)
        # 提示2: 分离各个元素
        #   states = np.array([x[0] for x in batch])
        #   actions = np.array([x[1] for x in batch])
        #   rewards = np.array([x[2] for x in batch])
        #   next_states = np.array([x[3] for x in batch])
        #   dones = np.array([x[4] for x in batch])
        # 提示3: return states, actions, rewards, next_states, dones

        pass  # TODO: 删除这一行

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
        # TODO: 实现前向传播
        # 提示1: 如果是单个状态: return state @ self.weights
        # 提示2: 如果是批次: return states @ self.weights
        # 提示3: 检查维度: if state.ndim == 1: state = state.reshape(1, -1)

        pass  # TODO: 删除这一行

    def update(self, states, actions, targets):
        """
        更新Q网络参数

        最小化: L = (target - Q(s, a))²

        Args:
            states: 状态批次
            actions: 动作批次
            targets: TD目标批次
        """
        # TODO: 实现参数更新
        # 提示1: 计算当前Q值
        #   q_values = self.forward(states)  # [batch_size, action_dim]
        # 提示2: 提取选择动作的Q值
        #   q_selected = q_values[np.arange(len(actions)), actions]
        # 提示3: 计算误差
        #   errors = targets - q_selected
        # 提示4: 计算梯度并更新（简化的梯度下降）
        #   for i in range(len(states)):
        #     grad = np.outer(states[i], np.zeros(self.action_dim))
        #     grad[:, actions[i]] = states[i]
        #     self.weights += self.alpha * errors[i] * grad

        pass  # TODO: 删除这一行

    def copy_from(self, other):
        """
        从另一个网络复制参数

        Args:
            other: 源网络
        """
        # TODO: 实现参数复制
        # 提示: self.weights = other.weights.copy()

        pass  # TODO: 删除这一行


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

    # TODO: 实现DQN主循环
    # 提示1: for episode in range(episodes):
    # 提示2:   state = env.reset()
    # 提示3:   episode_return = 0
    # 提示4:
    # 提示5:   while True:
    # 提示6:     # ε-greedy动作选择
    # 提示7:     if np.random.random() < epsilon:
    # 提示8:       action = np.random.randint(action_dim)
    # 提示9:     else:
    # 提示10:      q_values = q_network.forward(state)
    # 提示11:      action = np.argmax(q_values)
    # 提示12:
    # 提示13:    next_state, reward, done = env.step(action)
    # 提示14:    episode_return += reward
    # 提示15:
    # 提示16:    # 存储经验
    # 提示17:    replay_buffer.push(state, action, reward, next_state, done)
    # 提示18:
    # 提示19:    # 训练（如果有足够经验）
    # 提示20:    if len(replay_buffer) >= batch_size:
    # 提示21:      states, actions, rewards, next_states, dones = replay_buffer.sample(batch_size)
    # 提示22:
    # 提示23:      # 计算TD目标（使用目标网络）
    # 提示24:      next_q_values = target_network.forward(next_states)
    # 提示25:      max_next_q = np.max(next_q_values, axis=1)
    # 提示26:      targets = rewards + gamma * max_next_q * (1 - dones)
    # 提示27:
    # 提示28:      # 更新Q网络
    # 提示29:      q_network.update(states, actions, targets)
    # 提示30:
    # 提示31:    state = next_state
    # 提示32:
    # 提示33:    if done:
    # 提示34:      break
    # 提示35:
    # 提示36:  episode_returns.append(episode_return)
    # 提示37:
    # 提示38:  # 更新目标网络
    # 提示39:  if episode % target_update == 0:
    # 提示40:    target_network.copy_from(q_network)
    # 提示41:
    # 提示42:  # 衰减epsilon
    # 提示43:  epsilon = max(epsilon_end, epsilon * epsilon_decay)

    pass  # TODO: 删除这一行

    return q_network, episode_returns


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 DQN - CartPole")
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

    print(f"\n提示:")
    print(f"  - DQN引入经验回放和目标网络")
    print(f"  - 经验回放打破数据相关性")
    print(f"  - 目标网络稳定训练")
    print(f"  - ε逐渐衰减平衡探索与利用")
