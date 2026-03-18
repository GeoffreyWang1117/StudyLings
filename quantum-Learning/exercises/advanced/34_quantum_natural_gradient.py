"""
练习 34: 量子自然梯度
==================

目标：使用量子自然梯度优化变分电路

知识点：
- 自然梯度优化
- Quantum Fisher Information
- 量子几何张量

前沿进展（2019-2024）：
- Stokes et al. (2020): 量子自然梯度理论
- 2023-2024: 高效实现和应用
- 解决贫瘠高原问题

应用：
- VQE、QAOA 的优化
- 量子机器学习训练
- 避免局部最小值

任务：理解和实现量子自然梯度
"""

from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import Statevector
import numpy as np


def quantum_fisher_information_matrix(ansatz, params_values, params):
    """
    计算量子 Fisher 信息矩阵 (QFIM)

    F_ij = Re⟨∂_i ψ|∂_j ψ⟩ - Re⟨∂_i ψ|ψ⟩⟨ψ|∂_j ψ⟩

    参数：
        ansatz: 参数化电路
        params_values: 参数值
        params: 参数向量

    返回：
        numpy.ndarray: Fisher 信息矩阵
    """
    n_params = len(params)
    F = np.zeros((n_params, n_params))

    # TODO: 计算 Fisher 矩阵
    # 使用参数移位规则计算导数

    epsilon = np.pi / 2  # 参数移位量

    for i in range(n_params):
        for j in range(i, n_params):
            # 计算 F_ij
            # 使用 4 点公式

            # |ψ(θ + ε_i + ε_j)⟩
            params_pp = params_values.copy()
            params_pp[i] += epsilon
            params_pp[j] += epsilon
            param_dict = {params[k]: params_pp[k] for k in range(n_params)}
            psi_pp = Statevector.from_instruction(ansatz.assign_parameters(param_dict))

            # |ψ(θ + ε_i - ε_j)⟩
            params_pm = params_values.copy()
            params_pm[i] += epsilon
            params_pm[j] -= epsilon
            param_dict = {params[k]: params_pm[k] for k in range(n_params)}
            psi_pm = Statevector.from_instruction(ansatz.assign_parameters(param_dict))

            # |ψ(θ - ε_i + ε_j)⟩
            params_mp = params_values.copy()
            params_mp[i] -= epsilon
            params_mp[j] += epsilon
            param_dict = {params[k]: params_mp[k] for k in range(n_params)}
            psi_mp = Statevector.from_instruction(ansatz.assign_parameters(param_dict))

            # |ψ(θ - ε_i - ε_j)⟩
            params_mm = params_values.copy()
            params_mm[i] -= epsilon
            params_mm[j] -= epsilon
            param_dict = {params[k]: params_mm[k] for k in range(n_params)}
            psi_mm = Statevector.from_instruction(ansatz.assign_parameters(param_dict))

            # 计算 F_ij（简化公式）
            overlap_pp_mm = np.abs(np.dot(np.conj(psi_pp.data), psi_mm.data))**2
            overlap_pm_mp = np.abs(np.dot(np.conj(psi_pm.data), psi_mp.data))**2

            F[i, j] = (overlap_pp_mm - overlap_pm_mp) / 8
            F[j, i] = F[i, j]  # 对称

    return F


def compute_gradient(ansatz, params_values, params, hamiltonian):
    """
    计算普通梯度 ∂E/∂θ

    参数：
        ansatz: 参数化电路
        params_values: 参数值
        params: 参数向量
        hamiltonian: 哈密顿量

    返回：
        numpy.ndarray: 梯度向量
    """
    n_params = len(params)
    gradient = np.zeros(n_params)

    epsilon = np.pi / 2

    for i in range(n_params):
        # 参数移位规则
        # ∂E/∂θ_i = (E(θ + ε) - E(θ - ε)) / (2 sin ε)

        # E(θ + ε)
        params_plus = params_values.copy()
        params_plus[i] += epsilon
        param_dict = {params[k]: params_plus[k] for k in range(n_params)}
        psi_plus = Statevector.from_instruction(ansatz.assign_parameters(param_dict))
        E_plus = psi_plus.expectation_value(hamiltonian).real

        # E(θ - ε)
        params_minus = params_values.copy()
        params_minus[i] -= epsilon
        param_dict = {params[k]: params_minus[k] for k in range(n_params)}
        psi_minus = Statevector.from_instruction(ansatz.assign_parameters(param_dict))
        E_minus = psi_minus.expectation_value(hamiltonian).real

        gradient[i] = (E_plus - E_minus) / (2 * np.sin(epsilon))

    return gradient


def quantum_natural_gradient_step(gradient, fisher_matrix, learning_rate=0.01):
    """
    量子自然梯度更新步骤

    Δθ = -η F^{-1} g

    参数：
        gradient: 普通梯度
        fisher_matrix: Fisher 信息矩阵
        learning_rate: 学习率

    返回：
        numpy.ndarray: 参数更新
    """
    # TODO: 计算自然梯度
    # 需要求 Fisher 矩阵的逆

    # 添加正则化以避免奇异
    regularization = 1e-5
    F_reg = fisher_matrix + regularization * np.eye(len(gradient))

    # 自然梯度 = F^{-1} g
    natural_gradient = np.linalg.solve(F_reg, gradient)

    # 参数更新
    update = -learning_rate * natural_gradient

    return update


def compare_optimizers():
    """
    比较普通梯度下降和自然梯度下降
    """
    print("比较优化器：普通梯度 vs 量子自然梯度\n")
    print("=" * 60)

    # 创建简单的优化问题
    from qiskit.quantum_info import SparsePauliOp

    n_qubits = 2
    params = ParameterVector('θ', 4)

    # 简单 ansatz
    ansatz = QuantumCircuit(n_qubits)
    ansatz.ry(params[0], 0)
    ansatz.ry(params[1], 1)
    ansatz.cx(0, 1)
    ansatz.ry(params[2], 0)
    ansatz.ry(params[3], 1)

    # 目标哈密顿量
    H = SparsePauliOp.from_list([
        ('ZZ', 1.0),
        ('XX', 0.5),
    ])

    # 初始参数
    params_vanilla = np.random.rand(4) * 2 * np.pi
    params_natural = params_vanilla.copy()

    # 优化步数
    n_steps = 10

    print("步骤 | 普通梯度能量 | 自然梯度能量")
    print("-" * 60)

    energies_vanilla = []
    energies_natural = []

    for step in range(n_steps):
        # 普通梯度下降
        grad_vanilla = compute_gradient(ansatz, params_vanilla, params, H)
        params_vanilla -= 0.1 * grad_vanilla

        param_dict = {params[i]: params_vanilla[i] for i in range(4)}
        psi_vanilla = Statevector.from_instruction(ansatz.assign_parameters(param_dict))
        E_vanilla = psi_vanilla.expectation_value(H).real
        energies_vanilla.append(E_vanilla)

        # 量子自然梯度
        grad_natural = compute_gradient(ansatz, params_natural, params, H)
        fisher = quantum_fisher_information_matrix(ansatz, params_natural, params)
        update_natural = quantum_natural_gradient_step(grad_natural, fisher, learning_rate=0.1)
        params_natural += update_natural

        param_dict = {params[i]: params_natural[i] for i in range(4)}
        psi_natural = Statevector.from_instruction(ansatz.assign_parameters(param_dict))
        E_natural = psi_natural.expectation_value(H).real
        energies_natural.append(E_natural)

        print(f"{step:4d} | {E_vanilla:14.6f} | {E_natural:16.6f}")

    # 精确解
    exact_energy = min(np.linalg.eigvalsh(H.to_matrix()))
    print(f"\n精确基态能量: {exact_energy:.6f}")

    print(f"\n普通梯度最终误差: {abs(energies_vanilla[-1] - exact_energy):.6f}")
    print(f"自然梯度最终误差: {abs(energies_natural[-1] - exact_energy):.6f}")

    print("\n✓ 量子自然梯度通常收敛更快！")


def explain_quantum_natural_gradient():
    """解释量子自然梯度"""
    print("\n" + "=" * 60)
    print("量子自然梯度详解")
    print("=" * 60)

    print("""
为什么需要自然梯度？

  普通梯度下降的问题：
    - 参数空间不是欧几里得的
    - 不同参数方向的"距离"不同
    - 可能走很多弯路

  自然梯度的优势：
    ✓ 考虑参数空间的几何
    ✓ 沿着最陡方向（在流形上）
    ✓ 收敛更快
    ✓ 避免贫瘠高原

数学基础：

  参数空间是一个流形，配备度规张量 g_ij

  在量子态流形上：
    g_ij = Re⟨∂_i ψ|∂_j ψ⟩ - Re⟨∂_i ψ|ψ⟩⟨ψ|∂_j ψ⟩
        = Quantum Fisher Information Matrix (QFIM)

  自然梯度：
    ∇̃f = g^{-1} ∇f

  更新规则：
    θ_{t+1} = θ_t - η g^{-1} ∇E

量子 Fisher 信息：

  定义：
    F_ij = 4 Re⟨∂_i ψ|∂_j ψ⟩ - 4 Re⟨∂_i ψ|ψ⟩⟨ψ|∂_j ψ⟩

  物理意义：
    - 衡量参数变化对态的影响
    - 量子统计距离的度量
    - 与量子 Cramér-Rao 界相关

  计算方法：
    1. 参数移位规则（Parameter-Shift Rule）
    2. 线性组合技术
    3. 直接测量（需要辅助量子比特）

实现技巧：

  1. 正则化：
     F + λI（避免奇异性）

  2. Block-diagonal 近似：
     减少计算量

  3. 随机估计：
     只估计对角或部分元素

  4. 自适应学习率：
     结合 Adam 等优化器

应用（2023-2024）：

  VQE 优化：
    - 加速收敛
    - 避免局部最小值
    - IBM Qiskit Nature 实现

  QAOA：
    - 参数优化
    - 提高近似比

  量子机器学习：
    - QNN 训练
    - 避免贫瘠高原

  量子控制：
    - 优化控制脉冲
    - 提高门保真度

前沿研究（2024-2025）：

  🔬 高效 QFIM 测量
     - 经典 shadow 技术
     - 张量网络方法

  🔬 自适应自然梯度
     - 动态调整正则化
     - 二阶信息利用

  🔬 分布式量子自然梯度
     - 多个量子设备协同
     - 联邦学习

  🔬 与误差缓解结合
     - 噪声鲁棒的 Fisher 矩阵

性能分析：

  时间复杂度：
    - 梯度计算：O(p) 次电路运行
    - QFIM 计算：O(p²) 次电路运行
    - 矩阵求逆：O(p³) 经典计算

    p = 参数数量

  空间复杂度：
    - 存储 QFIM：O(p²)

  加速效果：
    - 通常减少 50-90% 的迭代次数
    - 对病态问题尤其有效

挑战：

  ⚠ 计算开销大
  ⚠ 需要精确的梯度估计
  ⚠ QFIM 可能病态
  ⚠ 噪声影响

结论：

  量子自然梯度是变分量子算法优化的
  强大工具，尤其在 NISQ 时代！
    """)

    print("\n✓ 量子自然梯度：从参数空间的几何角度优化")


if __name__ == '__main__':
    try:
        compare_optimizers()
        explain_quantum_natural_gradient()

        print("\n🎉 恭喜！你已掌握量子自然梯度！")
        print("\n关键要点:")
        print("- 考虑参数空间几何")
        print("- Fisher 信息矩阵")
        print("- 2020-2024 重要进展")
        print("- 变分算法优化的关键技术")

    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
