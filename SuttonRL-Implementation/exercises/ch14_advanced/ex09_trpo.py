"""
练习: TRPO (Trust Region Policy Optimization)

算法描述:
TRPO通过限制策略更新的KL散度来保证单调改进，是PPO的前身。

核心思想:
- 约束优化: max E[r] s.t. KL(π_old || π_new) ≤ δ
- 使用共轭梯度求解
- 理论保证单调改进

参考: Schulman et al. (2015) "Trust Region Policy Optimization"
"""

print("练习: 理解TRPO的信任域优化")
print("核心: KL约束 + 共轭梯度")
print("注: PPO是TRPO的简化版，更易实现")
