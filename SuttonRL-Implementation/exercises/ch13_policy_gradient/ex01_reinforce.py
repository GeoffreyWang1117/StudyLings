"""
练习: REINFORCE 算法 (Monte Carlo Policy Gradient)

算法描述:
REINFORCE 是最基本的策略梯度算法。它直接优化参数化策略，
而不是通过值函数间接优化。

核心思想:
- 参数化策略 π(a|s, θ)
- 目标：最大化期望回报 J(θ) = E[G_t]
- 策略梯度定理：∇J(θ) ∝ E[G_t ∇ln π(A_t|S_t, θ)]

更新规则:
    θ ← θ + α G_t ∇ln π(A_t|S_t, θ)

伪代码:
┌────────────────────────────────────────────────────┐
│ 输入: 可微分策略 π(a|s,θ)                          │
│ 参数: 步长 α > 0                                   │
│ 初始化: 策略参数 θ                                 │
│                                                    │
│ 循环(对每个回合):                                  │
│   生成回合 S_0,A_0,R_1,...,S_T ~ π(·|·,θ)          │
│   对回合中的每一步 t = 0, 1, ..., T-1:             │
│     G ← Σ_{k=t+1}^T γ^{k-t-1} R_k                 │
│     θ ← θ + α γ^t G ∇ln π(A_t|S_t, θ)              │
└────────────────────────────────────────────────────┘

使用 CartPole 环境（简化版）:
- 状态: 小车位置、速度、杆角度、角速度
- 动作: 左推(0)、右推(1)
- 奖励: 每步+1（杆保持直立）
- 终止: 杆倾斜太大或小车离中心太远

要求:
- 实现 REINFORCE 算法
- 使用 softmax 策略
- 观察学习曲线

参考: Sutton & Barto 第13章, 第13.3节
"""

import numpy as np


class SimpleCartPole:
    """简化的 CartPole 环境"""

    def __init__(self):
        self.gravity = 9.8
        self.masscart = 1.0
        self.masspole = 0.1
        self.length = 0.5
        self.force_mag = 10.0
        self.tau = 0.02  # 时间步长

        # 阈值
        self.theta_threshold = 12 * np.pi / 180
        self.x_threshold = 2.4

        self.reset()

    def reset(self):
        """重置环境"""
        self.state = np.random.uniform(-0.05, 0.05, 4)
        self.steps = 0
        return self.state

    def step(self, action):
        """
        执行动作

        Args:
            action: 0=左, 1=右

        Returns:
            next_state, reward, done
        """
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

        # 更新状态
        x = x + self.tau * x_dot
        x_dot = x_dot + self.tau * xacc
        theta = theta + self.tau * theta_dot
        theta_dot = theta_dot + self.tau * thetaacc

        self.state = np.array([x, x_dot, theta, theta_dot])
        self.steps += 1

        # 检查终止
        done = (
            x < -self.x_threshold
            or x > self.x_threshold
            or theta < -self.theta_threshold
            or theta > self.theta_threshold
            or self.steps >= 200
        )

        reward = 1.0 if not done else 0.0

        return self.state, reward, done


class PolicyNetwork:
    """简单的策略网络（线性 softmax）"""

    def __init__(self, state_dim, action_dim):
        """
        初始化

        Args:
            state_dim: 状态维度
            action_dim: 动作维度
        """
        self.state_dim = state_dim
        self.action_dim = action_dim

        # 初始化参数（小随机值）
        self.theta = np.random.randn(state_dim, action_dim) * 0.01

    def get_action_probs(self, state):
        """
        计算动作概率

        Args:
            state: 状态向量

        Returns:
            动作概率分布
        """
        # TODO: 实现 softmax 策略
        # 提示1: 计算 logits = state @ self.theta
        # 提示2: 使用 softmax: exp(logits) / sum(exp(logits))
        # 提示3: 为数值稳定性，减去最大值

        pass  # TODO: 删除这一行，实现 softmax

    def sample_action(self, state):
        """
        采样动作

        Args:
            state: 状态

        Returns:
            action: 采样的动作
        """
        # TODO: 根据概率分布采样动作
        # 提示: probs = self.get_action_probs(state)
        #      action = np.random.choice(self.action_dim, p=probs)

        pass  # TODO: 删除这一行，实现动作采样

    def compute_gradient(self, state, action):
        """
        计算策略梯度 ∇ln π(a|s, θ)

        Args:
            state: 状态
            action: 动作

        Returns:
            gradient: 梯度（与 theta 同形状）
        """
        # TODO: 计算 ∇ln π(a|s, θ)
        # 提示1: probs = self.get_action_probs(state)
        # 提示2: ∇ln π(a|s) = x * (𝟙(a) - π(a|s))
        #       其中 x 是状态，𝟙(a) 是 one-hot
        # 提示3: gradient = np.outer(state, one_hot - probs)

        pass  # TODO: 删除这一行，实现梯度计算


def reinforce(env, episodes=500, alpha=0.01, gamma=0.99):
    """
    REINFORCE 算法

    Args:
        env: 环境
        episodes: 回合数
        alpha: 学习率
        gamma: 折扣因子

    Returns:
        policy: 学习到的策略
        episode_returns: 每回合的总回报
    """
    state_dim = 4  # CartPole 状态维度
    action_dim = 2  # 动作数量

    policy = PolicyNetwork(state_dim, action_dim)
    episode_returns = []

    # TODO: 实现 REINFORCE 主循环
    # 提示1: for episode in range(episodes):
    # 提示2:   # 生成回合
    # 提示3:   state = env.reset()
    # 提示4:   states, actions, rewards = [], [], []
    # 提示5:   done = False
    # 提示6:   while not done:
    # 提示7:     action = policy.sample_action(state)
    # 提示8:     next_state, reward, done = env.step(action)
    # 提示9:     states.append(state)
    # 提示10:    actions.append(action)
    # 提示11:    rewards.append(reward)
    # 提示12:    state = next_state
    # 提示13:
    # 提示14:  # 计算回报并更新
    # 提示15:  G = 0
    # 提示16:  for t in range(len(states) - 1, -1, -1):
    # 提示17:    G = gamma * G + rewards[t]
    # 提示18:    gradient = policy.compute_gradient(states[t], actions[t])
    # 提示19:    policy.theta += alpha * (gamma ** t) * G * gradient
    # 提示20:
    # 提示21:  episode_returns.append(sum(rewards))

    pass  # TODO: 删除这一行，实现 REINFORCE

    return policy, episode_returns


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 REINFORCE - CartPole")
    print("=" * 60)

    np.random.seed(42)

    env = SimpleCartPole()

    print(f"\n环境: CartPole")
    print(f"算法: REINFORCE")
    print(f"回合数: 500")
    print(f"学习率 α: 0.01")
    print(f"\n开始训练...")

    policy, episode_returns = reinforce(env, episodes=500, alpha=0.01, gamma=0.99)

    print(f"\n训练完成!")

    # 分析结果
    early_avg = np.mean(episode_returns[:50])
    late_avg = np.mean(episode_returns[-50:])

    print(f"  前50回合平均回报: {early_avg:.2f}")
    print(f"  后50回合平均回报: {late_avg:.2f}")
    print(f"  改进: {late_avg - early_avg:.2f}")

    # 简单可视化
    print(f"\n学习曲线 (每50回合):")
    for i in range(0, len(episode_returns), 50):
        avg = np.mean(episode_returns[i:i+50])
        bar_len = int(avg / 5)
        print(f"  回合 {i:3d}-{i+50:3d}: {'█' * bar_len} {avg:.1f}")

    # 验证
    converges = late_avg > early_avg  # 应该有改进
    avg_return = late_avg

    return {
        'converges': converges,
        'avg_return': avg_return,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n提示:")
    print(f"  - REINFORCE 是 Monte Carlo 方法，高方差")
    print(f"  - 学习率需要仔细调整")
    print(f"  - 策略梯度直接优化策略，适合连续动作")
