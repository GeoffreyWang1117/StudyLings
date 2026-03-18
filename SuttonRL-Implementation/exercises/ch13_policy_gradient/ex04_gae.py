"""
练习: GAE (Generalized Advantage Estimation)

算法描述:
GAE是一种计算advantage函数的技术，通过λ参数平衡偏差和方差。
是PPO、TRPO等现代policy gradient算法的标准配置。

核心思想:
- TD(λ)的思想应用到advantage estimation
- 使用指数加权平均多个n-step advantages
- λ参数控制偏差-方差权衡

数学推导:
1. n-step advantage:
   A^(n) = r_t + γr_{t+1} + ... + γ^{n-1}r_{t+n-1} + γ^n V(s_{t+n}) - V(s_t)

2. GAE advantage:
   A^GAE(γ,λ) = (1-λ)(A^(1) + λA^(2) + λ²A^(3) + ...)
                = Σ_{l=0}^∞ (γλ)^l δ_{t+l}

3. 其中 δ_t = r_t + γV(s_{t+1}) - V(s_t)  [TD error]

λ参数效果:
- λ=0: A = δ (TD(0), 高偏差低方差)
- λ=1: A = Σδ = G - V (MC, 低偏差高方差)
- λ∈(0,1): 平衡

优势:
- 显著减少方差（比MC）
- 保持较低偏差（比TD(0)）
- 现代policy gradient标配
- 简单高效

参考: Schulman et al. (2016) "High-Dimensional Continuous Control Using GAE"
PPO、TRPO论文中都使用GAE
"""

import numpy as np

class GAEAgent:
    """使用GAE的Actor-Critic智能体"""
    def __init__(self, state_dim, action_dim, gamma=0.99, lambda_=0.95,
                 actor_lr=0.0003, critic_lr=0.001):
        """
        初始化

        Args:
            state_dim: 状态维度
            action_dim: 动作维度
            gamma: 折扣因子
            lambda_: GAE的λ参数
            actor_lr: actor学习率
            critic_lr: critic学习率
        """
        self.gamma = gamma
        self.lambda_ = lambda_
        self.actor_lr = actor_lr
        self.critic_lr = critic_lr

        # Actor网络 (策略)
        self.actor_weights = np.random.randn(state_dim, action_dim) * 0.01
        # Critic网络 (价值函数)
        self.critic_weights = np.random.randn(state_dim) * 0.01

    def get_value(self, state):
        """估计状态价值 V(s)"""
        # TODO: 实现价值估计
        # 提示: V(s) = s^T w
        pass  # TODO

    def get_action_probs(self, state):
        """获取动作概率分布"""
        # TODO: 实现softmax策略
        # 提示1: logits = s^T θ
        # 提示2: probs = softmax(logits)
        pass  # TODO

    def select_action(self, state):
        """根据策略采样动作"""
        # TODO: 从策略分布采样
        # 提示: np.random.choice(actions, p=probs)
        pass  # TODO

    def compute_gae(self, rewards, values, next_values, dones):
        """
        计算GAE advantages

        Args:
            rewards: 奖励序列 [T]
            values: 状态价值序列 V(s_t) [T]
            next_values: 下一状态价值 V(s_{t+1}) [T]
            dones: 终止标志 [T]

        Returns:
            advantages: GAE advantages [T]
            returns: 目标回报 V_target [T]
        """
        # TODO: 实现GAE计算
        # 提示1: 计算TD errors: δ_t = r_t + γV(s_{t+1}) - V(s_t)
        # 提示2: 考虑done标志: 终止时 δ_t = r_t - V(s_t)
        # 提示3: 反向计算GAE: A_t = δ_t + γλA_{t+1}
        # 提示4: 从最后一步开始: A_T = δ_T
        # 提示5: 计算returns: returns = advantages + values

        advantages = np.zeros_like(rewards)
        # TODO: 初始化最后一个advantage

        # TODO: 反向遍历计算GAE
        # for t in reversed(range(len(rewards))):
        #     if dones[t]:
        #         delta = ...
        #         advantages[t] = delta
        #     else:
        #         delta = ...
        #         advantages[t] = delta + gamma * lambda_ * advantages[t+1]

        # TODO: 计算目标回报
        returns = None  # TODO

        return advantages, returns

    def update_critic(self, states, returns):
        """更新价值函数"""
        # TODO: 实现critic更新
        # 提示1: 对每个(state, return)
        # 提示2: 计算预测价值: v_pred = self.get_value(state)
        # 提示3: 计算误差: error = return - v_pred
        # 提示4: 梯度下降: w += α * error * state
        pass  # TODO

    def update_actor(self, states, actions, advantages):
        """使用GAE advantages更新策略"""
        # TODO: 实现actor更新
        # 提示1: 对每个(state, action, advantage)
        # 提示2: 计算策略梯度: ∇log π(a|s) * A
        # 提示3: one_hot编码动作
        # 提示4: 梯度: grad = state^T (one_hot - probs) * advantage
        # 提示5: 更新: θ += α * grad
        pass  # TODO

    def train_episode(self, env):
        """训练一个episode"""
        # TODO: 实现episode训练
        # 提示1: 收集轨迹
        states, actions, rewards, values, dones = [], [], [], [], []

        # 提示2: 交互收集数据
        # state = env.reset()
        # while not done:
        #     action = self.select_action(state)
        #     value = self.get_value(state)
        #     next_state, reward, done = env.step(action)
        #     记录数据
        #     state = next_state

        # 提示3: 计算GAE
        # advantages, returns = self.compute_gae(...)

        # 提示4: 更新网络
        # self.update_critic(states, returns)
        # self.update_actor(states, actions, advantages)

        pass  # TODO


def compare_lambda_values():
    """比较不同λ值对学习的影响"""
    # TODO: 实验比较λ∈{0, 0.5, 0.9, 0.95, 1.0}的效果
    # 提示1: λ=0 -> TD(0) advantage (高偏差低方差)
    # 提示2: λ=1 -> MC advantage (低偏差高方差)
    # 提示3: λ=0.95 -> 通常是最佳平衡
    pass  # TODO


def visualize_gae_computation():
    """可视化GAE计算过程"""
    print("\n=== GAE计算示例 ===")

    # 示例轨迹
    rewards = np.array([1.0, 0.0, 0.0, 1.0, 2.0])
    values = np.array([0.5, 0.6, 0.7, 0.8, 0.9])
    next_values = np.array([0.6, 0.7, 0.8, 0.9, 0.0])  # 最后一个是终止状态
    dones = np.array([False, False, False, False, True])

    gamma, lambda_ = 0.99, 0.95

    # TODO: 手动计算GAE展示过程
    # 提示1: 计算每步的TD error
    # 提示2: 展示GAE的递归计算
    # 提示3: 对比不同λ值的结果

    print("Rewards:", rewards)
    print("Values:", values)
    print("\n计算TD errors:")
    # TODO: 实现

    print("\n计算GAE advantages (λ=0.95):")
    # TODO: 实现

    print("\n对比: λ=0 (TD) vs λ=1 (MC) vs λ=0.95 (GAE)")
    # TODO: 实现


class SimpleCartPole:
    """简化的CartPole环境"""
    def __init__(self):
        self.state_dim = 4
        self.action_dim = 2
        self.max_steps = 200
        self.reset()

    def reset(self):
        self.state = np.random.randn(self.state_dim) * 0.1
        self.steps = 0
        return self.state

    def step(self, action):
        # 简化动力学
        self.state += (action * 2 - 1) * 0.1 + np.random.randn(self.state_dim) * 0.02
        self.steps += 1

        # 奖励: 保持平衡
        reward = 1.0 if abs(self.state[0]) < 2.0 else -1.0
        done = abs(self.state[0]) > 2.0 or self.steps >= self.max_steps

        return self.state, reward, done


if __name__ == "__main__":
    print("练习: GAE (Generalized Advantage Estimation)")
    print("核心: 使用λ参数平衡advantage estimation的偏差-方差")
    print("\n关键公式:")
    print("  δ_t = r_t + γV(s_{t+1}) - V(s_t)")
    print("  A^GAE = Σ_{l=0}^∞ (γλ)^l δ_{t+l}")
    print("  递归形式: A_t = δ_t + γλA_{t+1}")
    print("\nλ参数效果:")
    print("  λ=0: TD(0) advantage (高偏差, 低方差)")
    print("  λ=1: MC advantage (低偏差, 高方差)")
    print("  λ=0.95: 典型最佳值")

    print("\n" + "="*50)
    visualize_gae_computation()

    print("\n" + "="*50)
    print("测试GAE Agent...")
    env = SimpleCartPole()
    agent = GAEAgent(state_dim=4, action_dim=2, lambda_=0.95)

    for episode in range(10):
        total_reward = agent.train_episode(env)
        print(f"Episode {episode}, Total Reward: {total_reward:.2f}")

    print("\n应用: PPO、TRPO等现代策略梯度算法的核心组件")
