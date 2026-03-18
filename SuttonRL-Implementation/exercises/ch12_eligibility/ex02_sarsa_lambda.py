"""
练习: SARSA(λ) - Eligibility Traces for SARSA

算法描述:
SARSA(λ)结合了n-step方法和eligibility traces，在TD(0)和MC之间平衡。

核心思想:
- Eligibility trace记录状态-动作对的访问历史
- λ参数控制credit assignment的衰减
- 同时更新所有有trace的状态-动作对

更新规则:
- δ = R + γQ(S',A') - Q(S,A)  [TD error]
- e(s,a) ← γλe(s,a) + 1(s=S, a=A)  [accumulating traces]
- Q(s,a) ← Q(s,a) + αδe(s,a)  [for all s,a]

λ参数:
- λ=0: SARSA (TD(0))
- λ=1: Monte Carlo
- λ∈(0,1): n-step的加权平均

优势:
- 更快的学习（比TD(0)）
- 更好的credit assignment
- 在线学习（比MC）

参考: Sutton & Barto (2018) Chapter 12 - Eligibility Traces
"""

import numpy as np
from collections import defaultdict

class SarsaLambda:
    """SARSA(λ)算法"""
    def __init__(self, n_actions, alpha=0.1, gamma=0.99, lambda_=0.9, epsilon=0.1):
        """
        初始化

        Args:
            n_actions: 动作数
            alpha: 学习率
            gamma: 折扣因子
            lambda_: trace衰减参数
            epsilon: ε-greedy探索率
        """
        self.n_actions = n_actions
        self.alpha = alpha
        self.gamma = gamma
        self.lambda_ = lambda_
        self.epsilon = epsilon

        # Q值表: Q(s,a)
        self.Q = defaultdict(lambda: np.zeros(n_actions))
        # Eligibility traces: e(s,a)
        self.traces = defaultdict(lambda: np.zeros(n_actions))

    def select_action(self, state):
        """ε-greedy策略选择动作"""
        # TODO: 实现ε-greedy
        # 提示1: 以ε概率随机探索
        # 提示2: 以1-ε概率选择最优动作
        pass  # TODO

    def reset_traces(self):
        """重置所有eligibility traces"""
        # TODO: 清空traces字典
        # 提示: 创建新的defaultdict
        pass  # TODO

    def update_traces(self, state, action, trace_type='accumulating'):
        """
        更新eligibility traces

        Args:
            state: 当前状态
            action: 当前动作
            trace_type: 'accumulating' or 'replacing'
        """
        # TODO: 实现trace更新
        # 提示1: 先衰减所有traces: e(s,a) *= γλ
        # 提示2: accumulating: e(S,A) += 1
        # 提示3: replacing: e(S,A) = 1
        # 提示4: 遍历所有状态-动作对
        pass  # TODO

    def update(self, state, action, reward, next_state, next_action, done):
        """
        SARSA(λ)更新

        Args:
            state: 当前状态
            action: 当前动作
            reward: 获得奖励
            next_state: 下一状态
            next_action: 下一动作
            done: 是否终止
        """
        # TODO: 实现SARSA(λ)更新
        # 提示1: 计算TD error
        if done:
            # 提示2: 终止状态: δ = R - Q(S,A)
            pass  # TODO
        else:
            # 提示3: 非终止: δ = R + γQ(S',A') - Q(S,A)
            pass  # TODO

        # 提示4: 更新当前状态-动作的trace
        # self.update_traces(state, action)

        # 提示5: 使用traces更新所有Q值
        # for s in self.Q.keys():
        #     for a in range(self.n_actions):
        #         Q(s,a) += α * δ * e(s,a)
        pass  # TODO

    def train_episode(self, env, trace_type='accumulating'):
        """
        训练一个episode

        Args:
            env: 环境
            trace_type: trace类型

        Returns:
            total_reward: episode总奖励
        """
        # TODO: 实现episode训练
        # 提示1: 重置traces和环境
        # 提示2: 选择初始动作
        # 提示3: 循环直到终止:
        #   - 执行动作
        #   - 选择下一动作
        #   - SARSA(λ)更新
        #   - 更新状态和动作
        # 提示4: 返回总奖励
        pass  # TODO


def compare_lambda_values(env, episodes=500, runs=10):
    """比较不同λ值的效果"""
    lambda_values = [0.0, 0.3, 0.6, 0.9, 1.0]
    results = {}

    # TODO: 实现比较实验
    # 提示1: 对每个λ值
    # 提示2:   运行多次实验
    # 提示3:   记录平均回报
    # 提示4: 绘制学习曲线
    pass  # TODO

    return results


def test_trace_decay():
    """测试trace衰减机制"""
    agent = SarsaLambda(n_actions=4, lambda_=0.9)

    # TODO: 测试trace衰减
    # 提示1: 设置初始trace值
    # 提示2: 更新多次观察衰减
    # 提示3: 验证: e_new = γλ * e_old
    pass  # TODO


# 简单环境用于测试
class SimpleGridWorld:
    """简单网格世界"""
    def __init__(self, size=5):
        self.size = size
        self.n_actions = 4  # 上下左右
        self.reset()

    def reset(self):
        self.state = 0  # 左上角
        self.goal = self.size * self.size - 1  # 右下角
        return self.state

    def step(self, action):
        row, col = self.state // self.size, self.state % self.size

        # 动作: 0=上, 1=下, 2=左, 3=右
        if action == 0 and row > 0:
            row -= 1
        elif action == 1 and row < self.size - 1:
            row += 1
        elif action == 2 and col > 0:
            col -= 1
        elif action == 3 and col < self.size - 1:
            col += 1

        self.state = row * self.size + col

        # 奖励和终止
        if self.state == self.goal:
            return self.state, 1.0, True
        else:
            return self.state, -0.01, False


if __name__ == "__main__":
    print("练习: SARSA(λ) - Eligibility Traces for SARSA")
    print("核心: 结合TD和MC，使用eligibility traces加速学习")
    print("\n关键公式:")
    print("  δ = R + γQ(S',A') - Q(S,A)")
    print("  e(s,a) ← γλe(s,a) + 1(s=S, a=A)")
    print("  Q(s,a) ← Q(s,a) + αδe(s,a)  ∀s,a")
    print("\nλ参数效果:")
    print("  λ=0: SARSA (one-step)")
    print("  λ=1: Monte Carlo")
    print("  λ∈(0,1): 平衡")

    # 测试
    env = SimpleGridWorld(size=5)
    agent = SarsaLambda(n_actions=4, lambda_=0.9)

    print("\n开始训练...")
    for episode in range(100):
        reward = agent.train_episode(env)
        if episode % 20 == 0:
            print(f"Episode {episode}, Reward: {reward:.2f}")
