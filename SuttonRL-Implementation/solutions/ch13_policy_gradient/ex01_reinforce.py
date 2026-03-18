"""
解答: REINFORCE算法

这是 ex01_reinforce.py 的完整实现解答
"""

import numpy as np


class SimpleCartPole:
    """简化的CartPole环境"""

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
            or self.steps >= 200
        )

        reward = 1.0 if not done else 0.0

        return self.state, reward, done


class PolicyNetwork:
    """策略网络（线性softmax）"""

    def __init__(self, state_dim, action_dim):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.theta = np.random.randn(state_dim, action_dim) * 0.01

    def get_action_probs(self, state):
        """计算动作概率"""
        logits = state @ self.theta
        # 数值稳定性
        exp_logits = np.exp(logits - np.max(logits))
        probs = exp_logits / np.sum(exp_logits)
        return probs

    def sample_action(self, state):
        """采样动作"""
        probs = self.get_action_probs(state)
        action = np.random.choice(self.action_dim, p=probs)
        return action

    def compute_gradient(self, state, action):
        """计算策略梯度 ∇ln π(a|s, θ)"""
        probs = self.get_action_probs(state)

        # one-hot编码
        one_hot = np.zeros(self.action_dim)
        one_hot[action] = 1

        # 对于softmax策略: ∇ln π(a|s) = x(s) ⊗ (e_a - π(s))
        gradient = np.outer(state, one_hot - probs)

        return gradient


def reinforce(env, episodes=500, alpha=0.01, gamma=0.99):
    """REINFORCE算法"""
    state_dim = 4
    action_dim = 2

    policy = PolicyNetwork(state_dim, action_dim)
    episode_returns = []

    for episode in range(episodes):
        # 生成回合
        state = env.reset()
        states, actions, rewards = [], [], []
        done = False

        while not done:
            action = policy.sample_action(state)
            next_state, reward, done = env.step(action)

            states.append(state)
            actions.append(action)
            rewards.append(reward)

            state = next_state

        # 计算回报并更新
        G = 0
        for t in range(len(states) - 1, -1, -1):
            G = gamma * G + rewards[t]

            # REINFORCE更新
            gradient = policy.compute_gradient(states[t], actions[t])
            policy.theta += alpha * (gamma ** t) * G * gradient

        episode_returns.append(sum(rewards))

    return policy, episode_returns


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 REINFORCE - CartPole [解答版本]")
    print("=" * 60)

    np.random.seed(42)

    env = SimpleCartPole()

    print(f"\n开始训练...")

    policy, episode_returns = reinforce(env, episodes=500, alpha=0.01, gamma=0.99)

    print(f"\n训练完成!")

    early_avg = np.mean(episode_returns[:50])
    late_avg = np.mean(episode_returns[-50:])

    print(f"  前50回合平均回报: {early_avg:.2f}")
    print(f"  后50回合平均回报: {late_avg:.2f}")
    print(f"  改进: {late_avg - early_avg:.2f}")

    # 学习曲线
    print(f"\n学习曲线 (每50回合):")
    for i in range(0, len(episode_returns), 50):
        avg = np.mean(episode_returns[i:i+50])
        bar_len = int(avg / 5)
        print(f"  回合 {i:3d}-{i+50:3d}: {'█' * bar_len} {avg:.1f}")

    return {
        'converges': late_avg > early_avg,
        'avg_return': late_avg,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n✅ 解答说明:")
    print(f"  1. get_action_probs(): softmax(θ^T s)")
    print(f"  2. sample_action(): 按概率采样")
    print(f"  3. compute_gradient(): ∇ln π = x ⊗ (e_a - π)")
    print(f"  4. θ += α G_t ∇ln π(A_t|S_t, θ)")
