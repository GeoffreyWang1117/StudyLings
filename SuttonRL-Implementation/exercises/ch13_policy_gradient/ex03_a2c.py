"""
练习: A2C (Advantage Actor-Critic)

算法描述:
A2C是同步版本的Advantage Actor-Critic，是2025年最常用的Actor-Critic实现之一。
它结合了策略梯度和值函数估计，使用TD learning更新值函数，提供更低方差的优势估计。

核心思想:
- Actor: 策略网络π(a|s,θ)
- Critic: 值函数V(s,w)
- TD优势: A(s,a) = r + γV(s') - V(s)
- 在线更新：每步都更新，不需要等回合结束

与REINFORCE with Baseline的区别:
- REINFORCE: 使用完整回报G，回合结束后更新
- A2C: 使用TD目标r+γV(s')，每步更新

与A3C的区别:
- A3C (Asynchronous): 多个worker异步更新
- A2C (Synchronous): 单个或批量同步更新，更稳定

伪代码:
┌────────────────────────────────────────────────────┐
│ 初始化: 策略参数θ, 值函数参数w                     │
│                                                    │
│ 循环（对每个回合）:                                │
│   初始化 S                                         │
│   I ← 1  [折扣累积]                                │
│                                                    │
│   循环（对回合中的每一步）:                        │
│     A ~ π(·|S, θ)                                  │
│     执行 A，观察 R, S'                             │
│                                                    │
│     if S' 是终止:                                  │
│       δ ← R - V(S, w)                              │
│     else:                                          │
│       δ ← R + γV(S', w) - V(S, w)  [TD误差]        │
│                                                    │
│     w ← w + α_w δ ∇V(S, w)  [Critic更新]           │
│     θ ← θ + α_θ I δ ∇log π(A|S, θ)  [Actor更新]    │
│                                                    │
│     I ← γI                                         │
│     S ← S'                                         │
│   直到 S 是终止状态                                │
└────────────────────────────────────────────────────┘

使用 CartPole 环境

要求:
- 实现A2C算法
- 使用TD误差作为优势
- 每步更新（在线学习）
- 观察相比REINFORCE的改进
- 收敛应更快

参考: Mnih et al. (2016) "Asynchronous Methods for Deep Reinforcement Learning"
      Wu et al. (2017) "Scalable trust-region method for deep reinforcement learning"
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
        
        done = (x < -self.x_threshold or x > self.x_threshold or 
                theta < -self.theta_threshold or theta > self.theta_threshold or
                self.steps >= 500)
        
        reward = 1.0 if not done else 0.0
        return self.state, reward, done


class A2CAgent:
    """A2C智能体"""
    
    def __init__(self, state_dim, action_dim, policy_lr=0.001, value_lr=0.01):
        """
        初始化

        Args:
            state_dim: 状态维度
            action_dim: 动作维度
            policy_lr: 策略学习率
            value_lr: 值函数学习率
        """
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.policy_lr = policy_lr
        self.value_lr = value_lr
        
        # Actor参数
        self.policy_theta = np.random.randn(state_dim, action_dim) * 0.01
        
        # Critic参数
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
    
    def update(self, state, action, td_error):
        """
        A2C更新

        Args:
            state: 状态
            action: 动作
            td_error: TD误差 δ = r + γV(s') - V(s)
        """
        # TODO: 实现Critic更新
        # 提示1: 值函数梯度: ∇V(s) = state
        # 提示2: Critic更新: w ← w + α_w·δ·∇V(s)
        #   self.value_w += self.value_lr * td_error * state
        
        # TODO: 实现Actor更新
        # 提示3: 策略梯度: ∇log π(a|s)
        # 提示4: probs = self.get_action_probs(state)
        # 提示5: one_hot = np.zeros(self.action_dim)
        #   one_hot[action] = 1
        # 提示6: grad = np.outer(state, one_hot - probs)
        # 提示7: Actor更新: θ ← θ + α_θ·δ·grad
        #   self.policy_theta += self.policy_lr * td_error * grad
        
        pass  # TODO: 删除这一行


def a2c(env, episodes=1000, gamma=0.99):
    """
    A2C算法

    Args:
        env: 环境
        episodes: 回合数
        gamma: 折扣因子

    Returns:
        agent: 训练好的A2C智能体
        episode_returns: 每回合总回报
    """
    state_dim = 4
    action_dim = 2
    
    agent = A2CAgent(state_dim, action_dim, policy_lr=0.001, value_lr=0.01)
    episode_returns = []
    
    # TODO: 实现A2C主循环
    # 提示1: for episode in range(episodes):
    # 提示2:   state = env.reset()
    # 提示3:   episode_return = 0
    # 提示4:   I = 1  # 折扣累积
    # 提示5:   done = False
    # 提示6:
    # 提示7:   while not done:
    # 提示8:     action = agent.sample_action(state)
    # 提示9:     next_state, reward, done = env.step(action)
    # 提示10:    episode_return += reward
    # 提示11:
    # 提示12:    # 计算TD误差
    # 提示13:    if done:
    # 提示14:      td_error = reward - agent.get_value(state)
    # 提示15:    else:
    # 提示16:      td_error = reward + gamma * agent.get_value(next_state) - agent.get_value(state)
    # 提示17:
    # 提示18:    # A2C更新（带折扣累积）
    # 提示19:    agent.update(state, action, I * td_error)
    # 提示20:
    # 提示21:    I *= gamma
    # 提示22:    state = next_state
    # 提示23:
    # 提示24:  episode_returns.append(episode_return)
    
    pass  # TODO: 删除这一行
    
    return agent, episode_returns


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 A2C - CartPole")
    print("=" * 60)
    
    np.random.seed(42)
    
    env = CartPole()
    
    print(f"\n开始训练 (1000回合)...")
    
    agent, episode_returns = a2c(env, episodes=1000, gamma=0.99)
    
    # 分析结果
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
    
    print(f"\n提示:")
    print(f"  - A2C使用TD误差作为优势估计")
    print(f"  - 每步更新，不需要等回合结束")
    print(f"  - Actor学习策略，Critic评估值函数")
    print(f"  - 比REINFORCE方差更小，学习更快")
    print(f"\n2025年应用:")
    print(f"  - 许多RL库的默认Actor-Critic实现")
    print(f"  - 可扩展到并行训练（批量同步）")
    print(f"  - 是PPO、SAC等高级算法的基础")
