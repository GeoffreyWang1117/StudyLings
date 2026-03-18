"""
解答: Actor-Critic with Baseline

这是 ex01_actor_critic_baseline.py 的完整实现解答
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


class ActorNetwork:
    """Actor网络（策略）"""

    def __init__(self, state_dim, action_dim, alpha=0.001):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.alpha = alpha
        self.theta = np.random.randn(state_dim, action_dim) * 0.01

    def get_action_probs(self, state):
        """计算动作概率"""
        logits = state @ self.theta
        exp_logits = np.exp(logits - np.max(logits))
        probs = exp_logits / np.sum(exp_logits)
        return probs

    def sample_action(self, state):
        """采样动作"""
        probs = self.get_action_probs(state)
        return np.random.choice(self.action_dim, p=probs)

    def update(self, state, action, advantage):
        """更新策略参数"""
        probs = self.get_action_probs(state)

        # 计算梯度
        one_hot = np.zeros(self.action_dim)
        one_hot[action] = 1
        gradient = np.outer(state, one_hot - probs)

        # 策略梯度更新
        self.theta += self.alpha * advantage * gradient


class CriticNetwork:
    """Critic网络（值函数）"""

    def __init__(self, state_dim, alpha=0.01):
        self.state_dim = state_dim
        self.alpha = alpha
        self.w = np.random.randn(state_dim) * 0.01

    def value(self, state):
        """计算状态值"""
        return np.dot(self.w, state)

    def update(self, state, td_error):
        """更新值函数参数"""
        self.w += self.alpha * td_error * state


def actor_critic(env, episodes=1000, gamma=0.99, actor_alpha=0.001, critic_alpha=0.01):
    """Actor-Critic算法"""
    state_dim = 4
    action_dim = 2

    actor = ActorNetwork(state_dim, action_dim, alpha=actor_alpha)
    critic = CriticNetwork(state_dim, alpha=critic_alpha)

    episode_returns = []

    for episode in range(episodes):
        state = env.reset()
        episode_return = 0
        I = 1  # 折扣累积

        while True:
            # Actor选择动作
            action = actor.sample_action(state)
            next_state, reward, done = env.step(action)
            episode_return += reward

            # 计算TD误差（优势）
            if done:
                td_error = reward - critic.value(state)
            else:
                td_error = reward + gamma * critic.value(next_state) - critic.value(state)

            # 更新Critic
            critic.update(state, td_error)

            # 更新Actor（使用优势）
            actor.update(state, action, I * td_error)

            I *= gamma
            state = next_state

            if done:
                break

        episode_returns.append(episode_return)

    return actor, critic, episode_returns


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 Actor-Critic with Baseline - CartPole [解答版本]")
    print("=" * 60)

    np.random.seed(42)

    env = CartPole()

    print(f"\n开始训练...")

    actor, critic, episode_returns = actor_critic(
        env, episodes=1000, gamma=0.99, actor_alpha=0.001, critic_alpha=0.01
    )

    early_avg = np.mean(episode_returns[:100])
    late_avg = np.mean(episode_returns[-100:])

    print(f"\n训练完成!")
    print(f"  前100回合平均回报: {early_avg:.2f}")
    print(f"  后100回合平均回报: {late_avg:.2f}")
    print(f"  改进: {late_avg - early_avg:.2f}")

    # 学习曲线
    print(f"\n学习曲线 (每100回合):")
    for i in range(0, len(episode_returns), 100):
        avg = np.mean(episode_returns[i:i+100])
        bar_len = int(avg / 10)
        print(f"  回合 {i:4d}-{i+100:4d}: {'█' * bar_len} {avg:.1f}")

    return {
        'converges': late_avg > early_avg,
        'avg_return': late_avg,
    }


if __name__ == '__main__':
    result = test()

    print(f"\n✅ 解答说明:")
    print(f"  1. Actor选择动作: π(a|s,θ)")
    print(f"  2. Critic评估: v̂(s,w)")
    print(f"  3. TD误差作为优势: δ = R + γv̂(s') - v̂(s)")
    print(f"  4. 同时更新: θ += αδ∇ln π, w += αδ∇v̂")
