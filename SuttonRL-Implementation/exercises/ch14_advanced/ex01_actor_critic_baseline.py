"""
练习: Actor-Critic with Baseline (带基线的Actor-Critic)

算法描述:
Actor-Critic是策略梯度方法的重要改进。Actor负责选择动作（策略网络），
Critic负责评估状态值（值函数网络）。使用TD误差作为优势估计可以减少方差。

核心思想:
- Actor: 策略网络 π(a|s, θ)
- Critic: 状态值函数 v̂(s, w)
- 优势估计: A(s,a) ≈ δ = R + γv̂(s', w) - v̂(s, w)
- 策略更新: θ ← θ + α_θ δ ∇ln π(a|s, θ)
- 值函数更新: w ← w + α_w δ ∇v̂(s, w)

伪代码:
┌────────────────────────────────────────────────────┐
│ 输入: 可微分策略 π(a|s,θ), 可微分值函数 v̂(s,w)   │
│ 参数: 步长 α_θ, α_w                                │
│ 初始化: θ, w 任意值                                │
│                                                    │
│ 循环（对每个回合）:                                │
│   初始化 S (起始状态)                              │
│   I ← 1                                            │
│                                                    │
│   循环（对回合中的每一步）:                        │
│     A ~ π(·|S, θ)                                  │
│     执行 A, 观察 S', R                             │
│                                                    │
│     δ ← R + γv̂(S', w) - v̂(S, w)  (如果S'终止，则γ=0)│
│     w ← w + α_w δ ∇v̂(S, w)                        │
│     θ ← θ + α_θ I δ ∇ln π(A|S, θ)                  │
│     I ← γI                                         │
│     S ← S'                                         │
│   直到 S 是终止状态                                │
└────────────────────────────────────────────────────┘

使用 CartPole 环境

要求:
- 实现Actor网络（策略）
- 实现Critic网络（值函数）
- 使用TD误差作为优势
- 同时更新两个网络
- 观察比纯REINFORCE的改进

参考: Sutton & Barto 第13章, 第13.5节
"""

import numpy as np


class CartPole:
    """CartPole环境（简化版）"""

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


class ActorNetwork:
    """Actor网络（策略）- 线性softmax"""

    def __init__(self, state_dim, action_dim, alpha=0.001):
        """
        初始化Actor

        Args:
            state_dim: 状态维度
            action_dim: 动作维度
            alpha: 学习率
        """
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.alpha = alpha
        self.theta = np.random.randn(state_dim, action_dim) * 0.01

    def get_action_probs(self, state):
        """计算动作概率分布"""
        # TODO: 实现softmax策略
        # 提示1: logits = state @ self.theta
        # 提示2: 为数值稳定性，减去最大值
        # 提示3: exp_logits = np.exp(logits - np.max(logits))
        # 提示4: probs = exp_logits / np.sum(exp_logits)
        # 提示5: return probs

        pass  # TODO: 删除这一行

    def sample_action(self, state):
        """采样动作"""
        # TODO: 实现动作采样
        # 提示: probs = self.get_action_probs(state)
        #      return np.random.choice(self.action_dim, p=probs)

        pass  # TODO: 删除这一行

    def update(self, state, action, advantage):
        """
        更新策略参数

        θ ← θ + α * advantage * ∇ln π(a|s, θ)

        Args:
            state: 状态
            action: 动作
            advantage: 优势值（TD误差）
        """
        # TODO: 实现策略梯度更新
        # 提示1: probs = self.get_action_probs(state)
        # 提示2: 计算梯度 ∇ln π(a|s, θ)
        #        对于softmax策略: ∇ln π(a|s) = x(s) ⊗ (e_a - π(s))
        #        其中 e_a 是one-hot向量
        # 提示3: one_hot = np.zeros(self.action_dim)
        #        one_hot[action] = 1
        # 提示4: gradient = np.outer(state, one_hot - probs)
        # 提示5: self.theta += self.alpha * advantage * gradient

        pass  # TODO: 删除这一行


class CriticNetwork:
    """Critic网络（值函数）- 线性"""

    def __init__(self, state_dim, alpha=0.01):
        """
        初始化Critic

        Args:
            state_dim: 状态维度
            alpha: 学习率
        """
        self.state_dim = state_dim
        self.alpha = alpha
        self.w = np.random.randn(state_dim) * 0.01

    def value(self, state):
        """
        计算状态值 v̂(s, w) = w^T s

        Args:
            state: 状态

        Returns:
            状态值估计
        """
        # TODO: 实现值计算
        # 提示: return np.dot(self.w, state)

        pass  # TODO: 删除这一行

    def update(self, state, td_error):
        """
        更新值函数参数

        w ← w + α * td_error * ∇v̂(s, w)

        对于线性函数: ∇v̂(s, w) = s

        Args:
            state: 状态
            td_error: TD误差
        """
        # TODO: 实现值函数更新
        # 提示1: 梯度就是状态本身（线性情况）
        # 提示2: self.w += self.alpha * td_error * state

        pass  # TODO: 删除这一行


def actor_critic(env, episodes=1000, gamma=0.99, actor_alpha=0.001, critic_alpha=0.01):
    """
    Actor-Critic with Baseline算法

    Args:
        env: 环境
        episodes: 回合数
        gamma: 折扣因子
        actor_alpha: Actor学习率
        critic_alpha: Critic学习率

    Returns:
        actor: 训练好的Actor
        critic: 训练好的Critic
        episode_returns: 每回合总回报
    """
    state_dim = 4
    action_dim = 2

    actor = ActorNetwork(state_dim, action_dim, alpha=actor_alpha)
    critic = CriticNetwork(state_dim, alpha=critic_alpha)

    episode_returns = []

    # TODO: 实现Actor-Critic主循环
    # 提示1: for episode in range(episodes):
    # 提示2:   state = env.reset()
    # 提示3:   episode_return = 0
    # 提示4:   I = 1  # 折扣累积
    # 提示5:
    # 提示6:   while True:
    # 提示7:     # Actor选择动作
    # 提示8:     action = actor.sample_action(state)
    # 提示9:     next_state, reward, done = env.step(action)
    # 提示10:    episode_return += reward
    # 提示11:
    # 提示12:    # 计算TD误差（优势）
    # 提示13:    if done:
    # 提示14:      td_error = reward - critic.value(state)
    # 提示15:    else:
    # 提示16:      td_error = reward + gamma * critic.value(next_state) - critic.value(state)
    # 提示17:
    # 提示18:    # 更新Critic
    # 提示19:    critic.update(state, td_error)
    # 提示20:
    # 提示21:    # 更新Actor（使用优势）
    # 提示22:    actor.update(state, action, I * td_error)
    # 提示23:
    # 提示24:    I *= gamma
    # 提示25:    state = next_state
    # 提示26:
    # 提示27:    if done:
    # 提示28:      break
    # 提示29:
    # 提示30:  episode_returns.append(episode_return)

    pass  # TODO: 删除这一行

    return actor, critic, episode_returns


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 Actor-Critic with Baseline - CartPole")
    print("=" * 60)

    np.random.seed(42)

    env = CartPole()

    print(f"\n开始训练...")
    print(f"  回合数: 1000")
    print(f"  Actor学习率: 0.001")
    print(f"  Critic学习率: 0.01")

    actor, critic, episode_returns = actor_critic(
        env, episodes=1000, gamma=0.99, actor_alpha=0.001, critic_alpha=0.01
    )

    # 分析结果
    early_avg = np.mean(episode_returns[:100])
    late_avg = np.mean(episode_returns[-100:])

    print(f"\n训练完成!")
    print(f"  前100回合平均回报: {early_avg:.2f}")
    print(f"  后100回合平均回报: {late_avg:.2f}")
    print(f"  改进: {late_avg - early_avg:.2f}")

    # 简单可视化
    print(f"\n学习曲线 (每100回合):")
    for i in range(0, len(episode_returns), 100):
        avg = np.mean(episode_returns[i:i+100])
        bar_len = int(avg / 10)
        print(f"  回合 {i:4d}-{i+100:4d}: {'█' * bar_len} {avg:.1f}")

    converges = late_avg > early_avg

    return {
        'converges': converges,
        'avg_return': late_avg,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n提示:")
    print(f"  - Actor-Critic比REINFORCE方差更小")
    print(f"  - TD误差作为优势估计")
    print(f"  - Critic提供基线，减少方差")
    print(f"  - 两个网络同时训练")
