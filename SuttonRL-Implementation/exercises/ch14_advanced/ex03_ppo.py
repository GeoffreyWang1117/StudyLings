"""
练习: PPO (Proximal Policy Optimization)

算法描述:
PPO是当前最流行的策略梯度算法之一。它通过限制策略更新的幅度来保持训练稳定性。
PPO使用"裁剪"的替代目标函数，防止策略更新过大。

核心思想:
- 重要性采样比率: r_t(θ) = π_θ(a|s) / π_θ_old(a|s)
- 裁剪目标: L^CLIP = E[min(r_t·A_t, clip(r_t, 1-ε, 1+ε)·A_t)]
- 防止策略变化过大
- 使用旧策略收集的数据进行多轮更新

关键优势:
1. 训练稳定
2. 样本效率高
3. 易于实现和调试
4. 适用于连续和离散动作空间

伪代码 (PPO-Clip):
┌────────────────────────────────────────────────────┐
│ 初始化: 策略参数 θ, 值函数参数 φ                   │
│                                                    │
│ 循环:                                              │
│   用当前策略 π_θ 收集 T 步轨迹                     │
│   计算优势估计 Â_t                                 │
│                                                    │
│   优化替代目标 (K个epoch):                         │
│     for epoch in 1..K:                             │
│       for 每个mini-batch:                          │
│         r_t(θ) = π_θ(a_t|s_t) / π_θ_old(a_t|s_t)  │
│         L^CLIP = E[min(r_t·Â_t, clip(r_t)·Â_t)]   │
│         更新 θ 最大化 L^CLIP                       │
│         更新 φ 最小化值函数误差                    │
│                                                    │
│   θ_old ← θ                                        │
└────────────────────────────────────────────────────┘

使用 CartPole 环境

要求:
- 实现策略网络和值函数网络
- 实现轨迹收集
- 实现优势估计（GAE）
- 实现PPO裁剪目标
- 多轮更新策略

参考: Schulman et al. (2017) "Proximal Policy Optimization Algorithms"
"""

import numpy as np


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


class PPOAgent:
    """PPO智能体"""

    def __init__(self, state_dim, action_dim, policy_lr=0.0003, value_lr=0.001, clip_epsilon=0.2):
        """
        初始化

        Args:
            state_dim: 状态维度
            action_dim: 动作维度
            policy_lr: 策略学习率
            value_lr: 值函数学习率
            clip_epsilon: PPO裁剪参数
        """
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.policy_lr = policy_lr
        self.value_lr = value_lr
        self.clip_epsilon = clip_epsilon

        # 策略网络参数
        self.policy_theta = np.random.randn(state_dim, action_dim) * 0.01

        # 值函数参数
        self.value_w = np.random.randn(state_dim) * 0.01

    def get_action_probs(self, state):
        """获取动作概率"""
        logits = state @ self.policy_theta
        exp_logits = np.exp(logits - np.max(logits))
        return exp_logits / np.sum(exp_logits)

    def sample_action(self, state):
        """采样动作"""
        probs = self.get_action_probs(state)
        return np.random.choice(self.action_dim, p=probs)

    def get_value(self, state):
        """获取状态值"""
        return np.dot(self.value_w, state)

    def compute_gae(self, rewards, values, next_values, dones, gamma=0.99, lam=0.95):
        """
        计算广义优势估计 (GAE)

        GAE(γ,λ) = Σ(γλ)^l δ_{t+l}
        其中 δ_t = r_t + γV(s_{t+1}) - V(s_t)

        Args:
            rewards: 奖励列表
            values: 状态值列表
            next_values: 下一状态值列表
            dones: 终止标记列表
            gamma: 折扣因子
            lam: GAE参数

        Returns:
            advantages: 优势估计
        """
        # TODO: 实现GAE
        # 提示1: advantages = np.zeros_like(rewards)
        # 提示2: gae = 0
        # 提示3: 从后往前计算
        # 提示4: for t in reversed(range(len(rewards))):
        # 提示5:   delta = rewards[t] + gamma * next_values[t] * (1 - dones[t]) - values[t]
        # 提示6:   gae = delta + gamma * lam * (1 - dones[t]) * gae
        # 提示7:   advantages[t] = gae
        # 提示8: return advantages

        pass  # TODO: 删除这一行

    def update(self, states, actions, old_probs, advantages, returns, epochs=10, batch_size=64):
        """
        PPO更新

        Args:
            states: 状态批次
            actions: 动作批次
            old_probs: 旧策略概率
            advantages: 优势估计
            returns: 回报
            epochs: 更新轮数
            batch_size: mini-batch大小
        """
        # TODO: 实现PPO更新
        # 提示1: for epoch in range(epochs):
        # 提示2:   # 打乱数据
        # 提示3:   indices = np.random.permutation(len(states))
        # 提示4:
        # 提示5:   for start in range(0, len(states), batch_size):
        # 提示6:     end = start + batch_size
        # 提示7:     batch_idx = indices[start:end]
        # 提示8:
        # 提示9:     batch_states = states[batch_idx]
        # 提示10:    batch_actions = actions[batch_idx]
        # 提示11:    batch_old_probs = old_probs[batch_idx]
        # 提示12:    batch_advantages = advantages[batch_idx]
        # 提示13:    batch_returns = returns[batch_idx]
        # 提示14:
        # 提示15:    # 计算当前策略概率
        # 提示16:    current_probs = np.array([self.get_action_probs(s)[a]
        # 提示17:                              for s, a in zip(batch_states, batch_actions)])
        # 提示18:
        # 提示19:    # 计算比率
        # 提示20:    ratio = current_probs / (batch_old_probs + 1e-10)
        # 提示21:
        # 提示22:    # PPO裁剪目标
        # 提示23:    surr1 = ratio * batch_advantages
        # 提示24:    surr2 = np.clip(ratio, 1 - self.clip_epsilon, 1 + self.clip_epsilon) * batch_advantages
        # 提示25:    policy_loss = -np.mean(np.minimum(surr1, surr2))
        # 提示26:
        # 提示27:    # 更新策略（简化的梯度）
        # 提示28:    for i in range(len(batch_states)):
        # 提示29:      probs = self.get_action_probs(batch_states[i])
        # 提示30:      one_hot = np.zeros(self.action_dim)
        # 提示31:      one_hot[batch_actions[i]] = 1
        # 提示32:      grad = np.outer(batch_states[i], one_hot - probs)
        # 提示33:      # 根据裁剪后的优势更新
        # 提示34:      if surr1[i] < surr2[i]:
        # 提示35:        self.policy_theta += self.policy_lr * batch_advantages[i] * grad
        # 提示36:
        # 提示37:    # 更新值函数
        # 提示38:    for i in range(len(batch_states)):
        # 提示39:      value = self.get_value(batch_states[i])
        # 提示40:      value_loss = (batch_returns[i] - value) ** 2
        # 提示41:      grad = (batch_returns[i] - value) * batch_states[i]
        # 提示42:      self.value_w += self.value_lr * grad

        pass  # TODO: 删除这一行


def collect_trajectories(env, agent, max_steps=2048):
    """收集轨迹"""
    states, actions, rewards, values, dones = [], [], [], [], []
    old_probs = []

    state = env.reset()
    for _ in range(max_steps):
        action = agent.sample_action(state)
        prob = agent.get_action_probs(state)[action]
        value = agent.get_value(state)

        next_state, reward, done = env.step(action)

        states.append(state)
        actions.append(action)
        rewards.append(reward)
        values.append(value)
        old_probs.append(prob)
        dones.append(done)

        state = next_state if not done else env.reset()

    return (np.array(states), np.array(actions), np.array(rewards),
            np.array(values), np.array(dones), np.array(old_probs))


def ppo(env, iterations=100, gamma=0.99):
    """PPO主函数"""
    agent = PPOAgent(state_dim=4, action_dim=2)

    episode_returns = []

    # TODO: 实现PPO主循环
    # 提示: 收集轨迹 -> 计算优势 -> 更新策略

    pass  # TODO: 删除这一行

    return agent, episode_returns


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 PPO - CartPole")
    print("=" * 60)

    np.random.seed(42)

    env = CartPole()

    print(f"\n开始训练...")

    agent, episode_returns = ppo(env, iterations=100)

    print(f"\n训练完成!")

    return {
        'converges': True,
        'avg_return': 0.0,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n提示:")
    print(f"  - PPO是最流行的策略梯度算法")
    print(f"  - 裁剪目标防止策略更新过大")
    print(f"  - GAE提供更好的优势估计")
    print(f"  - 多轮更新提高样本效率")
