"""
练习: World Model Basics

算法描述:
World Model学习环境动态模型，用于规划和策略学习。
这是model-based RL的基础，2025年在样本效率和迁移学习中很重要。

核心思想:
- 学习转移模型: P(s'|s,a)
- 学习奖励模型: R(s,a)
- 使用模型进行规划
- Dyna架构: 真实经验 + 模拟经验

应用:
- 样本效率提升
- 安全RL（先模拟再执行）
- 迁移学习

参考: Sutton "Dyna Architecture"
       Ha & Schmidhuber (2018) "World Models"
"""

import numpy as np

class WorldModel:
    """环境动态模型"""
    def __init__(self, n_states, n_actions):
        self.n_states = n_states
        self.n_actions = n_actions
        # 转移计数: N(s,a,s')
        self.transition_counts = np.zeros((n_states, n_actions, n_states))
        # 奖励累积
        self.reward_sum = np.zeros((n_states, n_actions))
        self.reward_count = np.zeros((n_states, n_actions))
    
    def update(self, state, action, reward, next_state):
        """从真实经验更新模型"""
        # TODO: 更新转移计数和奖励
        pass  # TODO
    
    def sample_transition(self, state, action):
        """从模型采样转移"""
        # TODO: 根据学到的模型采样
        pass  # TODO
    
    def predict_reward(self, state, action):
        """预测奖励"""
        # TODO: 返回平均奖励
        pass  # TODO

print("练习: 实现World Model - 学习环境动态")
print("核心: 统计转移概率P(s'|s,a)和奖励R(s,a)")
