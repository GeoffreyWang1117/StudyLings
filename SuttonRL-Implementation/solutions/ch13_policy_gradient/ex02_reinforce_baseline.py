"""
解答: REINFORCE with Baseline
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
        costheta = np.cos(theta)
        sintheta = np.sin(theta)
        temp = (force + self.masspole * self.length * theta_dot**2 * sintheta) / (self.masscart + self.masspole)
        thetaacc = (self.gravity * sintheta - costheta * temp) / (self.length * (4.0 / 3.0 - self.masspole * costheta**2 / (self.masscart + self.masspole)))
        xacc = temp - self.masspole * self.length * thetaacc * costheta / (self.masscart + self.masspole)
        x = x + self.tau * x_dot
        x_dot = x_dot + self.tau * xacc
        theta = theta + self.tau * theta_dot
        theta_dot = theta_dot + self.tau * thetaacc
        self.state = np.array([x, x_dot, theta, theta_dot])
        self.steps += 1
        done = (x < -self.x_threshold or x > self.x_threshold or theta < -self.theta_threshold or theta > self.theta_threshold or self.steps >= 500)
        reward = 1.0 if not done else 0.0
        return self.state, reward, done


class PolicyNetwork:
    def __init__(self, state_dim, action_dim, alpha=0.001):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.alpha = alpha
        self.theta = np.random.randn(state_dim, action_dim) * 0.01
    
    def get_action_probs(self, state):
        logits = state @ self.theta
        exp_logits = np.exp(logits - np.max(logits))
        return exp_logits / np.sum(exp_logits)
    
    def sample_action(self, state):
        probs = self.get_action_probs(state)
        return np.random.choice(self.action_dim, p=probs)
    
    def update(self, state, action, advantage):
        probs = self.get_action_probs(state)
        one_hot = np.zeros(self.action_dim)
        one_hot[action] = 1
        grad = np.outer(state, one_hot - probs)
        self.theta += self.alpha * advantage * grad


class ValueNetwork:
    def __init__(self, state_dim, alpha=0.01):
        self.state_dim = state_dim
        self.alpha = alpha
        self.w = np.random.randn(state_dim) * 0.01
    
    def value(self, state):
        return np.dot(self.w, state)
    
    def update(self, state, td_error):
        self.w += self.alpha * td_error * state


def reinforce_baseline(env, episodes=1000, gamma=0.99):
    policy = PolicyNetwork(4, 2, alpha=0.001)
    value = ValueNetwork(4, alpha=0.01)
    episode_returns = []
    
    for episode in range(episodes):
        states, actions, rewards = [], [], []
        state = env.reset()
        done = False
        
        while not done:
            action = policy.sample_action(state)
            next_state, reward, done = env.step(action)
            states.append(state)
            actions.append(action)
            rewards.append(reward)
            state = next_state
        
        episode_return = sum(rewards)
        episode_returns.append(episode_return)
        
        # 从后往前计算回报并更新
        G = 0
        for t in reversed(range(len(states))):
            G = rewards[t] + gamma * G
            baseline = value.value(states[t])
            advantage = G - baseline
            value.update(states[t], advantage)
            policy.update(states[t], actions[t], advantage)
    
    return policy, value, episode_returns


def test():
    print("=" * 60)
    print("测试 REINFORCE with Baseline [解答版本]")
    print("=" * 60)
    
    np.random.seed(42)
    env = CartPole()
    
    print(f"\n开始训练 (1000回合)...")
    policy, value, episode_returns = reinforce_baseline(env, episodes=1000, gamma=0.99)
    
    early_avg = np.mean(episode_returns[:100])
    late_avg = np.mean(episode_returns[-100:])
    
    print(f"\n前100回合: {early_avg:.2f}, 后100回合: {late_avg:.2f}")
    print(f"\n✅ 核心改进:")
    print(f"  1. 优势函数: A(s,a) = G - V(s)")
    print(f"  2. 策略更新: θ += α·A·∇log π")
    print(f"  3. 值函数更新: w += α·A·∇V")
    print(f"  4. 显著减少方差，加快收敛")
    
    return {'converges': late_avg > early_avg, 'avg_return': late_avg}


if __name__ == '__main__':
    test()
