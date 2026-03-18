"""
练习: GAIL (Generative Adversarial Imitation Learning)

算法描述:
GAIL使用对抗训练进行模仿学习，不需要显式的奖励函数。
核心思想来自GAN，用判别器区分专家和学习者的行为。

核心思想:
- 判别器D: 区分专家轨迹vs学习者轨迹
- 生成器(策略)π: 尽量让D无法区分
- 最小化: H(π) + E_π[-log D(s,a)]

数学公式:
1. 判别器目标:
   max_D E_expert[log D(s,a)] + E_π[log(1-D(s,a))]

2. 策略目标:
   min_π -H(π) + E_π[-log D(s,a)]
   其中H(π)是熵正则化

3. 等价于最小化专家和学习者分布的JS散度

优势:
- 不需要显式奖励函数
- 可以从未标注轨迹学习
- 理论上等价于IRL + RL

在RLHF中的意义:
- 奖励建模的另一种视角
- 对抗训练思想（虽然RLHF不直接用GAIL）
- 理解"从偏好学习"的理论基础

参考: Ho & Ermon (2016) "Generative Adversarial Imitation Learning"
"""

import numpy as np

class Discriminator:
    """判别器: 区分专家vs学习者"""
    def __init__(self, state_dim, action_dim, lr=0.001):
        # TODO: 初始化判别器网络
        # 提示: 输入(s,a)，输出概率[0,1]
        pass

    def predict(self, state, action):
        """预测是否来自专家"""
        # TODO: 实现预测
        # 提示: D(s,a) = sigmoid(concat(s,a) @ weights)
        pass

    def train_step(self, expert_batch, learner_batch):
        """训练判别器"""
        # TODO: 实现训练
        # 提示1: expert标签=1, learner标签=0
        # 提示2: 二分类交叉熵损失
        # 提示3: 更新判别器参数
        pass


class GAILAgent:
    """GAIL智能体"""
    def __init__(self, state_dim, action_dim):
        self.discriminator = Discriminator(state_dim, action_dim)
        # TODO: 初始化策略网络
        # 提示: 使用任何policy gradient方法(如TRPO、PPO)
        pass

    def get_reward(self, state, action):
        """从判别器获取隐式奖励"""
        # TODO: 实现奖励计算
        # 提示: r = -log(1 - D(s,a))
        # 这个奖励鼓励策略生成"像专家"的行为
        pass

    def train(self, env, expert_data, n_iterations=100):
        """GAIL训练循环"""
        # TODO: 实现训练循环
        # 提示1: 每次迭代:
        #   1) 用当前策略收集轨迹
        #   2) 训练判别器区分expert vs learner
        #   3) 用判别器奖励训练策略
        pass


print("练习: GAIL - 对抗式模仿学习")
print("核心: 用GAN思想进行模仿学习")
print("判别器: 区分专家vs学习者")
print("策略: 骗过判别器")
print("\n应用: 不需要奖励函数的模仿学习")
