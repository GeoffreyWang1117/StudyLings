"""
练习: SAC (Soft Actor-Critic)

算法描述:
SAC是基于最大熵强化学习的off-policy算法，在2025年是连续控制的SOTA方法之一。

核心思想:
- 最大化期望回报 + 熵: J = E[Σ r_t + α H(π(·|s_t))]
- 自动调节温度参数α
- 随机策略（vs DDPG的确定性策略）

优势:
- 样本效率高
- 训练稳定
- 鼓励探索

参考: Haarnoja et al. (2018) "Soft Actor-Critic"
"""

print("练习: 实现SAC")
print("核心: 最大熵目标 + 自动温度调节")
print("提示: 策略输出分布，Critic使用期望Q值")
