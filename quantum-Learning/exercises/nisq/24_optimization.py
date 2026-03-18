"""
练习 24: 量子优化应用
==================

目标：使用量子算法解决实际优化问题

知识点：
- 投资组合优化
- 车辆路径问题
- 资源分配

示例：投资组合优化
- 最大化回报
- 最小化风险
- 满足预算约束

任务：使用 QAOA 解决投资组合优化
"""

import numpy as np


def portfolio_optimization_demo():
    """
    投资组合优化演示
    """
    print("量子优化：投资组合问题\n")
    print("=" * 60)
    
    print("""
问题设定：
  - 4 种资产可选
  - 每种资产有期望回报和风险
  - 预算限制：最多选择 2 种资产
  - 目标：最大化回报，最小化风险

资产信息：
  资产 A: 回报 12%, 风险 5%
  资产 B: 回报 10%, 风险 3%
  资产 C: 回报 8%,  风险 2%
  资产 D: 回报 15%, 风险 8%

量子方法：
  1. 编码为 QUBO 问题
  2. 使用 QAOA 求解
  3. 得到最优资产组合

实际应用：
  - 金融机构使用量子算法优化大规模投资组合
  - JPMorgan, Goldman Sachs 等都在研究
  - 对于大规模问题，量子可能提供优势
    """)
    
    # 模拟结果
    returns = np.array([0.12, 0.10, 0.08, 0.15])
    risks = np.array([0.05, 0.03, 0.02, 0.08])
    
    print("\n经典暴力搜索：")
    best_combo = None
    best_score = -float('inf')
    
    for i in range(16):  # 2^4 种组合
        bits = [(i >> j) & 1 for j in range(4)]
        if sum(bits) == 2:  # 预算约束
            ret = sum(b * r for b, r in zip(bits, returns))
            risk = sum(b * r for b, r in zip(bits, risks))
            score = ret - 0.5 * risk  # 风险调整回报
            
            if score > best_score:
                best_score = score
                best_combo = bits
    
    assets = ['A', 'B', 'C', 'D']
    selected = [assets[i] for i, b in enumerate(best_combo) if b]
    
    print(f"最优组合: {', '.join(selected)}")
    print(f"期望回报: {sum(b*r for b,r in zip(best_combo, returns)):.2%}")
    print(f"风险: {sum(b*r for b,r in zip(best_combo, risks)):.2%}")
    
    print("\n✓ 优化完成！")
    print("\n量子优化的实际应用：")
    print("- 金融：投资组合、风险管理")
    print("- 物流：车辆路径、调度")
    print("- 能源：电网优化")
    print("- 制造：供应链优化")


if __name__ == '__main__':
    portfolio_optimization_demo()
