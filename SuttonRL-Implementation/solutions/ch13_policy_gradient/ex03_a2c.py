"""
解答: A2C (Advantage Actor-Critic)
"""

import numpy as np


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


class A2CAgent:
    def __init__(self, state_dim, action_dim, policy_lr=0.001, value_lr=0.01):
        self.state_dim, self.action_dim = state_dim, action_dim
        self.policy_lr, self.value_lr = policy_lr, value_lr
        self.policy_theta = np.random.randn(state_dim, action_dim) * 0.01
        self.value_w = np.random.randn(state_dim) * 0.01
    
    def get_action_probs(self, state):
        logits = state @ self.policy_theta
        exp_logits = np.exp(logits - np.max(logits))
        return exp_logits / np.sum(exp_logits)
    
    def sample_action(self, state):
        return np.random.choice(self.action_dim, p=self.get_action_probs(state))
    
    def get_value(self, state):
        return np.dot(self.value_w, state)
    
    def update(self, state, action, td_error):
        # Critic更新
        self.value_w += self.value_lr * td_error * state
        
        # Actor更新
        probs = self.get_action_probs(state)
        one_hot = np.zeros(self.action_dim)
        one_hot[action] = 1
        grad = np.outer(state, one_hot - probs)
        self.policy_theta += self.policy_lr * td_error * grad


def a2c(env, episodes=1000, gamma=0.99):
    agent = A2CAgent(4, 2, policy_lr=0.001, value_lr=0.01)
    episode_returns = []
    
    for episode in range(episodes):
        state = env.reset()
        episode_return = 0
        I = 1
        done = False
        
        while not done:
            action = agent.sample_action(state)
            next_state, reward, done = env.step(action)
            episode_return += reward
            
            # 计算TD误差
            if done:
                td_error = reward - agent.get_value(state)
            else:
                td_error = reward + gamma * agent.get_value(next_state) - agent.get_value(state)
            
            # A2C更新
            agent.update(state, action, I * td_error)
            
            I *= gamma
            state = next_state
        
        episode_returns.append(episode_return)
    
    return agent, episode_returns


def test():
    print("=" * 60)
    print("测试 A2C [解答版本]")
    print("=" * 60)
    
    np.random.seed(42)
    env = CartPole()
    agent, episode_returns = a2c(env, episodes=1000, gamma=0.99)
    
    early_avg = np.mean(episode_returns[:100])
    late_avg = np.mean(episode_returns[-100:])
    
    print(f"\n前100回合: {early_avg:.2f}, 后100回合: {late_avg:.2f}")
    print(f"\n✅ A2C核心:")
    print(f"  1. TD优势: δ = r + γV(s') - V(s)")
    print(f"  2. Critic: w += α·δ·∇V")
    print(f"  3. Actor: θ += α·δ·∇log π")
    print(f"  4. 在线更新，每步都学习")
    print(f"\n与REINFORCE对比:")
    print(f"  - REINFORCE: 使用G（高方差），回合结束更新")
    print(f"  - A2C: 使用TD误差（低方差），每步更新")
    print(f"\n2025年地位: Actor-Critic方法的标准实现")
    
    return {'converges': late_avg > early_avg, 'avg_return': late_avg}


if __name__ == '__main__':
    test()
