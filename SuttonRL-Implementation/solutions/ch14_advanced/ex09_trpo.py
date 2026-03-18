"""解答: TRPO核心思想"""
print("TRPO核心:")
print("1. 约束: KL(π_old || π_new) ≤ δ")
print("2. 求解: 共轭梯度法")
print("3. 保证: 单调改进")
print("\nPPO vs TRPO:")
print("- PPO: 裁剪目标，简单高效")
print("- TRPO: KL约束，理论保证更强")
print("\n2025年: PPO更常用，TRPO作为理论基础")
