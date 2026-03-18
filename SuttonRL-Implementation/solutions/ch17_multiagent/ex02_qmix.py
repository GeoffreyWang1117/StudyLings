"""解答: QMIX核心思想"""
print("✅ QMIX核心:")
print("  1. 个体Q值: Q_i(τ_i, a_i) 每个智能体")
print("  2. Mixing Network: Q_tot = f(Q_1,...,Q_n; s)")
print("  3. 单调性: 使用非负权重保证∂Q_tot/∂Q_i ≥ 0")
print("  4. CTDE: Centralized Training, Decentralized Execution")
print("\n效果: argmax_a Q_tot = [argmax_a1 Q_1, ..., argmax_an Q_n]")
print("2025年地位: 多智能体协作的SOTA方法之一")
