"""
练习: QMIX

算法描述:
QMIX通过mixing network学习联合Q值，同时保持去中心化执行。
这是2025年多智能体RL最流行的方法之一。

核心思想:
- 每个智能体: Q_i(τ_i, a_i)
- Mixing network: Q_tot = f(Q_1, Q_2, ..., Q_n)
- 单调性约束: ∂Q_tot/∂Q_i ≥ 0
- 中心化训练，去中心化执行 (CTDE)

优势:
- 学习协调策略
- 保证个体最优=团队最优
- 可扩展

应用:
- 多机器人协作
- 游戏AI（星际争霸）
- 无人机编队

参考: Rashid et al. (2018) "QMIX: Monotonic Value Function Factorisation"
"""

print("练习: QMIX - 单调值函数分解")
print("核心: Q_tot = MixingNet(Q_1, ..., Q_n)")
print("约束: ∂Q_tot/∂Q_i ≥ 0 (单调性)")
