"""
练习: REINFORCE with Baseline

算法描述:
REINFORCE with Baseline是对基础REINFORCE的重要改进，通过引入基线函数来减少方差。
基线不会引入偏差，但能显著降低梯度估计的方差，加快学习速度。

核心思想:
- 基础REINFORCE使用: ∇J(θ) ∝ Σ_t ∇log π(A_t|S_t,θ) G_t
- 加入基线: ∇J(θ) ∝ Σ_t ∇log π(A_t|S_t,θ) (G_t - b(S_t))
- 最佳基线: b(S_t) = V(S_t) （状态值函数）
- 优势函数: A(s,a) = Q(s,a) - V(s) = G_t - V(S_t)

为什么有效:
- 减少方差: 去除状态值的基准水平
- 无偏估计: E[∇log π(a|s) · b(s)] = 0
- 保留符号: 好动作(A>0)增强，差动作(A<0)减弱

伪代码:
┌────────────────────────────────────────────────────┐
│ 初始化: 策略参数θ, 值函数参数w                     │
│                                                    │
│ 循环（对每个回合）:                                │
│   生成回合: S_0,A_0,R_1,...,S_T 遵循π(·|·,θ)       │
│                                                    │
│   对回合中的每一步 t:                              │
│     G ← Σ_{k=t+1}^T γ^{k-t-1} R_k                 │
│     δ ← G - V(S_t, w)  [TD误差/优势]               │
│                                                    │
│     w ← w + α_w δ ∇V(S_t, w)  [更新值函数]         │
│     θ ← θ + α_θ γ^t δ ∇log π(A_t|S_t,θ) [更新策略] │
└────────────────────────────────────────────────────┘

使用 CartPole 环境

要求:
- 实现REINFORCE with Baseline
- 维护独立的值函数
- 使用优势函数A = G - V(s)
- 观察相比基础REINFORCE的改进
- 收敛应更快更稳定

参考: Sutton & Barto 第13章, 第13.4节
      Williams (1992) "Simple Statistical Gradient-Following Algorithms"
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


class PolicyNetwork:
    """策略网络（线性softmax）"""
    
    def __init__(self, state_dim, action_dim, alpha=0.001):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.alpha = alpha
        self.theta = np.random.randn(state_dim, action_dim) * 0.01
    
    def get_action_probs(self, state):
        """计算动作概率"""
        logits = state @ self.theta
        exp_logits = np.exp(logits - np.max(logits))
        return exp_logits / np.sum(exp_logits)
    
    def sample_action(self, state):
        """采样动作"""
        probs = self.get_action_probs(state)
        return np.random.choice(self.action_dim, p=probs)
    
    def update(self, state, action, advantage):
        """
        策略梯度更新（with baseline）

        Args:
            state: 状态
            action: 动作
            advantage: 优势函数 A = G - V(s)
        """
        # TODO: 实现策略梯度更新
        # 提示1: probs = self.get_action_probs(state)
        # 提示2: 计算梯度 ∇log π(a|s)
        #   对softmax策略: ∇log π(a|s) = φ(s) - Σ π(a'|s)φ(s,a')
        #   简化: grad_log_pi = φ(s,a) - E[φ(s,·)]
        # 提示3: 创建one-hot向量
        #   one_hot = np.zeros(self.action_dim)
        #   one_hot[action] = 1
        # 提示4: 梯度 = state的外积与(one_hot - probs)
        #   grad = np.outer(state, one_hot - probs)
        # 提示5: 策略梯度更新: θ ← θ + α·advantage·grad
        #   self.theta += self.alpha * advantage * grad
        
        pass  # TODO: 删除这一行


class ValueNetwork:
    """值函数网络（线性）"""
    
    def __init__(self, state_dim, alpha=0.01):
        self.state_dim = state_dim
        self.alpha = alpha
        self.w = np.random.randn(state_dim) * 0.01
    
    def value(self, state):
        """计算状态值"""
        return np.dot(self.w, state)
    
    def update(self, state, td_error):
        """
        值函数更新

        Args:
            state: 状态
            td_error: TD误差 δ = G - V(s)
        """
        # TODO: 实现值函数更新
        # 提示1: 梯度下降最小化 (G - V(s))^2
        # 提示2: ∇V(s) = state （线性函数）
        # 提示3: w ← w + α·td_error·state
        
        pass  # TODO: 删除这一行


def reinforce_baseline(env, episodes=1000, gamma=0.99):
    """
    REINFORCE with Baseline算法

    Args:
        env: 环境
        episodes: 回合数
        gamma: 折扣因子

    Returns:
        policy: 训练好的策略
        value: 训练好的值函数
        episode_returns: 每回合总回报
    """
    state_dim = 4
    action_dim = 2
    
    policy = PolicyNetwork(state_dim, action_dim, alpha=0.001)
    value = ValueNetwork(state_dim, alpha=0.01)
    
    episode_returns = []
    
    # TODO: 实现REINFORCE with Baseline主循环
    # 提示1: for episode in range(episodes):
    # 提示2:   # 生成回合
    # 提示3:   states, actions, rewards = [], [], []
    # 提示4:   state = env.reset()
    # 提示5:   done = False
    # 提示6:
    # 提示7:   while not done:
    # 提示8:     action = policy.sample_action(state)
    # 提示9:     next_state, reward, done = env.step(action)
    # 提示10:
    # 提示11:    states.append(state)
    # 提示12:    actions.append(action)
    # 提示13:    rewards.append(reward)
    # 提示14:
    # 提示15:    state = next_state
    # 提示16:
    # 提示17:  episode_return = sum(rewards)
    # 提示18:  episode_returns.append(episode_return)
    # 提示19:
    # 提示20:  # 计算回报并更新
    # 提示21:  G = 0
    # 提示22:  for t in reversed(range(len(states))):
    # 提示23:    G = rewards[t] + gamma * G
    # 提示24:
    # 提示25:    # 计算优势函数
    # 提示26:    baseline = value.value(states[t])
    # 提示27:    advantage = G - baseline
    # 提示28:
    # 提示29:    # 更新值函数和策略
    # 提示30:    value.update(states[t], advantage)
    # 提示31:    policy.update(states[t], actions[t], advantage)
    
    pass  # TODO: 删除这一行
    
    return policy, value, episode_returns


def test():
    """测试函数"""
    print("=" * 60)
    print("测试 REINFORCE with Baseline - CartPole")
    print("=" * 60)
    
    np.random.seed(42)
    
    env = CartPole()
    
    print(f"\n开始训练 (1000回合)...")
    
    policy, value, episode_returns = reinforce_baseline(env, episodes=1000, gamma=0.99)
    
    # 分析结果
    early_avg = np.mean(episode_returns[:100])
    late_avg = np.mean(episode_returns[-100:])
    
    print(f"\n训练完成!")
    print(f"  前100回合平均回报: {early_avg:.2f}")
    print(f"  后100回合平均回报: {late_avg:.2f}")
    print(f"  改进: {late_avg - early_avg:.2f}")
    
    # 显示学习曲线
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
    print(f"  - Baseline减少方差但不引入偏差")
    print(f"  - 最佳baseline是状态值函数V(s)")
    print(f"  - 优势函数A(s,a) = G - V(s)指示动作优劣")
    print(f"  - 比基础REINFORCE收敛更快更稳定")
    print(f"\n理论:")
    print(f"  - E[∇log π(a|s) · b(s)] = 0 (baseline无偏)")
    print(f"  - Var[G - b] < Var[G] (减少方差)")
    print(f"  - 2025年所有策略梯度方法都使用baseline")
