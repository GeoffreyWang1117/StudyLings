"""
练习: Dyna-Q+

算法描述:
Dyna-Q+是Dyna-Q的改进版，通过奖励bonus鼓励探索长时间未访问的状态-动作对。

改进:
- Exploration bonus: r+ = r + κ√τ (τ是未访问时间)
- 适应环境变化
- 鼓励重访旧状态检查变化

参考: Sutton & Barto 第8章
"""

print("练习: Dyna-Q+ - 添加探索bonus")
print("核心: r_bonus = r + κ·√(time_since_visit)")
