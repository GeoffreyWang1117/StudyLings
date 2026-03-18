"""
解答: PPO (Proximal Policy Optimization)

这是 ex03_ppo.py 的完整实现解答
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
        advantages = np.zeros_like(rewards)
        gae = 0

        # 从后往前计算GAE
        for t in reversed(range(len(rewards))):
            delta = rewards[t] + gamma * next_values[t] * (1 - dones[t]) - values[t]
            gae = delta + gamma * lam * (1 - dones[t]) * gae
            advantages[t] = gae

        return advantages

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
        # 标准化优势
        advantages = (advantages - np.mean(advantages)) / (np.std(advantages) + 1e-8)

        for epoch in range(epochs):
            # 打乱数据
            indices = np.random.permutation(len(states))

            for start in range(0, len(states), batch_size):
                end = min(start + batch_size, len(states))
                batch_idx = indices[start:end]

                batch_states = states[batch_idx]
                batch_actions = actions[batch_idx]
                batch_old_probs = old_probs[batch_idx]
                batch_advantages = advantages[batch_idx]
                batch_returns = returns[batch_idx]

                # 计算当前策略概率
                current_probs = np.array([self.get_action_probs(s)[a]
                                        for s, a in zip(batch_states, batch_actions)])

                # 计算比率
                ratio = current_probs / (batch_old_probs + 1e-10)

                # PPO裁剪目标
                surr1 = ratio * batch_advantages
                surr2 = np.clip(ratio, 1 - self.clip_epsilon, 1 + self.clip_epsilon) * batch_advantages
                policy_loss = -np.mean(np.minimum(surr1, surr2))

                # 更新策略（简化的梯度上升）
                for i in range(len(batch_states)):
                    probs = self.get_action_probs(batch_states[i])
                    one_hot = np.zeros(self.action_dim)
                    one_hot[batch_actions[i]] = 1
                    grad = np.outer(batch_states[i], one_hot - probs)

                    # 根据裁剪后的优势更新
                    if surr1[i] < surr2[i]:
                        self.policy_theta += self.policy_lr * batch_advantages[i] * grad

                # 更新值函数
                for i in range(len(batch_states)):
                    value = self.get_value(batch_states[i])
                    value_loss = (batch_returns[i] - value) ** 2
                    grad = (batch_returns[i] - value) * batch_states[i]
                    self.value_w += self.value_lr * grad


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
    """
    PPO主函数

    Args:
        env: 环境
        iterations: 迭代次数
        gamma: 折扣因子

    Returns:
        agent: 训练好的智能体
        episode_returns: 每次迭代的平均回报
    """
    agent = PPOAgent(state_dim=4, action_dim=2)

    episode_returns = []

    for iteration in range(iterations):
        # 收集轨迹
        states, actions, rewards, values, dones, old_probs = collect_trajectories(env, agent, max_steps=2048)

        # 计算下一状态值
        next_values = np.zeros_like(values)
        for i in range(len(states) - 1):
            if not dones[i]:
                next_values[i] = values[i + 1]

        # 计算优势估计（GAE）
        advantages = agent.compute_gae(rewards, values, next_values, dones, gamma=gamma, lam=0.95)

        # 计算回报
        returns = advantages + values

        # 更新策略和值函数
        agent.update(states, actions, old_probs, advantages, returns, epochs=10, batch_size=64)

        # 记录平均回报
        avg_return = np.mean(rewards)
        episode_returns.append(avg_return)

    return agent, episode_returns


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 PPO - CartPole [解答版本]")
    print("=" * 60)

    np.random.seed(42)

    env = CartPole()

    print(f"\n开始训练...")
    print(f"  迭代次数: 100")
    print(f"  裁剪参数 ε: 0.2")

    agent, episode_returns = ppo(env, iterations=100)

    # 分析结果
    early_avg = np.mean(episode_returns[:10])
    late_avg = np.mean(episode_returns[-10:])

    print(f"\n训练完成!")
    print(f"  前10次平均回报: {early_avg:.3f}")
    print(f"  后10次平均回报: {late_avg:.3f}")
    print(f"  改进: {late_avg - early_avg:.3f}")

    # 学习曲线
    print(f"\n学习曲线 (每10次):")
    for i in range(0, len(episode_returns), 10):
        avg = np.mean(episode_returns[i:i+10])
        bar_len = int(avg * 50)
        print(f"  迭代 {i:2d}-{i+10:2d}: {'█' * bar_len} {avg:.3f}")

    converges = late_avg > early_avg

    return {
        'converges': converges,
        'avg_return': late_avg,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n✅ 解答说明:")
    print(f"  1. 收集轨迹: 用当前策略采样")
    print(f"  2. GAE计算: Â = Σ(γλ)^l δ_t")
    print(f"  3. 裁剪目标: L = min(r·Â, clip(r)·Â)")
    print(f"  4. 多轮更新: 重复使用数据，提高样本效率")
    print(f"\nPPO的优势:")
    print(f"  - 训练稳定: 裁剪防止策略变化过大")
    print(f"  - 样本效率: 多轮更新重复利用数据")
    print(f"  - 易于实现: 简单有效")
    print(f"  - 应用广泛: RLHF、机器人控制等")
