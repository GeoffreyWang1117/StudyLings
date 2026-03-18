"""
练习 31: VQLS (Variational Quantum Linear Solver)
==================

目标：使用变分方法求解线性方程组

知识点：
- VQLS 是 HHL 算法的 NISQ 友好版本
- 不需要相位估计（降低电路深度）
- 使用变分优化最小化成本函数

问题：求解 Ax = b

方法：
- 准备参数化态 |ψ(θ)⟩ ≈ |x⟩
- 最小化 ||A|ψ⟩ - |b⟩||²

前沿进展（2023-2024）：
- 改进的优化策略
- 与误差缓解结合
- 实际应用：金融建模、流体力学

任务：实现 VQLS 求解简单线性系统
"""

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import ParameterVector
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector, Operator
import numpy as np
from scipy.optimize import minimize


def create_vqls_ansatz(n_qubits, depth=2):
    """
    创建 VQLS 的 ansatz

    参数：
        n_qubits: 量子比特数
        depth: 电路深度

    返回：
        QuantumCircuit, ParameterVector
    """
    params = ParameterVector('θ', n_qubits * depth * 2)
    qc = QuantumCircuit(n_qubits)

    # TODO: 实现参数化电路
    # 提示：使用 RY 和 RZ 旋转 + CNOT 纠缠

    param_idx = 0
    for d in range(depth):
        # 旋转层
        for i in range(n_qubits):
            qc.ry(params[param_idx], i)
            param_idx += 1
            qc.rz(params[param_idx], i)
            param_idx += 1

        # 纠缠层
        if d < depth - 1:
            for i in range(n_qubits - 1):
                qc.cx(i, i + 1)

    return qc, params


def vqls_cost_function(params_values, A, b, ansatz, param_vector):
    """
    VQLS 成本函数

    最小化 ||A|ψ⟩ - |b⟩||² = ⟨ψ|A†A|ψ⟩ - 2Re⟨ψ|A†|b⟩ + ⟨b|b⟩

    参数：
        params_values: 参数值
        A: 矩阵（作为 Operator）
        b: 向量（作为 Statevector）
        ansatz: 参数化电路
        param_vector: 参数向量

    返回：
        float: 成本值
    """
    # 绑定参数
    param_dict = {param_vector[i]: params_values[i] for i in range(len(params_values))}
    bound_circuit = ansatz.assign_parameters(param_dict)

    # 获取 |ψ(θ)⟩
    psi = Statevector.from_instruction(bound_circuit)

    # 计算 ||A|ψ⟩ - |b⟩||²
    A_psi = psi.evolve(A)
    diff = A_psi.data - b.data
    cost = np.real(np.dot(np.conj(diff), diff))

    return cost


def solve_vqls(A_matrix, b_vector, n_qubits=2, depth=2, max_iter=100):
    """
    使用 VQLS 求解 Ax = b

    参数：
        A_matrix: 系数矩阵（numpy array）
        b_vector: 右端向量（numpy array）
        n_qubits: 量子比特数
        depth: ansatz 深度
        max_iter: 最大迭代次数

    返回：
        dict: 结果
    """
    print("VQLS: 变分量子线性求解器\n")
    print("=" * 60)

    # 转换为量子对象
    A = Operator(A_matrix)
    b_norm = np.linalg.norm(b_vector)
    b_normalized = b_vector / b_norm
    b = Statevector(b_normalized)

    print(f"矩阵 A:")
    print(A_matrix)
    print(f"\n向量 b: {b_vector}")

    # 经典解（用于比较）
    x_classical = np.linalg.solve(A_matrix, b_vector)
    print(f"\n经典解: {x_classical}")

    # 创建 ansatz
    ansatz, params = create_vqls_ansatz(n_qubits, depth)

    print(f"\nAnsatz 参数数量: {len(params)}")
    print("\n优化中...")

    # 初始化参数
    initial_params = np.random.rand(len(params)) * 2 * np.pi

    # TODO: 优化
    result = minimize(
        vqls_cost_function,
        initial_params,
        args=(A, b, ansatz, params),
        method='COBYLA',
        options={'maxiter': max_iter}
    )

    print(f"\n优化完成！")
    print(f"最终成本: {result.fun:.6f}")

    # 获取解
    param_dict = {params[i]: result.x[i] for i in range(len(params))}
    bound_circuit = ansatz.assign_parameters(param_dict)
    solution_state = Statevector.from_instruction(bound_circuit)

    # 提取振幅作为解
    x_quantum = solution_state.data.real * b_norm

    print(f"量子解: {x_quantum}")
    print(f"误差: {np.linalg.norm(x_quantum[:len(x_classical)] - x_classical):.6f}")

    return {
        'quantum_solution': x_quantum,
        'classical_solution': x_classical,
        'cost': result.fun,
        'params': result.x
    }


def test_vqls():
    """测试 VQLS"""
    print("测试 VQLS 算法\n")

    # 简单 2x2 系统
    A = np.array([
        [1.5, 0.5],
        [0.5, 1.5]
    ])

    b = np.array([1.0, 0.0])

    result = solve_vqls(A, b, n_qubits=2, depth=2, max_iter=50)

    # 验证
    x = result['quantum_solution'][:2]
    residual = np.linalg.norm(A @ x - b)

    print(f"\n验证: ||Ax - b|| = {residual:.6f}")

    assert residual < 0.5, "VQLS 解的误差过大"

    print("\n✓ VQLS 测试通过！")

    return True


def explain_vqls():
    """解释 VQLS"""
    print("\n" + "=" * 60)
    print("VQLS 详解")
    print("=" * 60)

    print("""
VQLS vs HHL：

  HHL（Harrow-Hassidim-Lloyd）：
    ✓ 指数加速（理论上）
    ✗ 需要相位估计（深电路）
    ✗ 需要容错量子计算机
    ✗ 输出是量子态，不能直接读取

  VQLS：
    ✓ 浅电路（NISQ 友好）
    ✓ 不需要相位估计
    ✓ 可以提取特定信息
    ✗ 需要经典优化（迭代次数多）
    ✗ 没有理论加速保证

算法原理：

  目标：找到 |x⟩ 使得 A|x⟩ = |b⟩

  方法：最小化
    C(θ) = ||A|ψ(θ)⟩ - |b⟩||²

  展开：
    C(θ) = ⟨ψ|A†A|ψ⟩ - 2Re⟨ψ|A†|b⟩ + ⟨b|b⟩

  每一项都可以高效测量！

测量策略：

  1. ⟨ψ|A†A|ψ⟩
     - Hadamard test
     - 或 SWAP test 变体

  2. ⟨ψ|A†|b⟩
     - 需要准备 |b⟩
     - 使用振幅编码

前沿进展（2023-2024）：

  🔬 改进的成本函数
     - 使用 Hadamard overlap test
     - 减少测量开销

  🔬 与误差缓解结合
     - Zero-noise extrapolation
     - Probabilistic error cancellation

  🔬 实际应用
     - 金融：投资组合优化
     - 工程：流体力学模拟
     - 机器学习：内核方法

应用示例：

  金融建模：
    - 解 Ax = b，其中 A 是协方差矩阵
    - 用于风险分析

  偏微分方程：
    - 离散化后的线性系统
    - 物理模拟

优势与限制：

  优势：
    ✓ NISQ 时代可实现
    ✓ 电路深度浅
    ✓ 理论框架成熟

  限制：
    ⚠ 优化可能困难（局部最小值）
    ⚠ 需要多次测量
    ⚠ 条件数影响性能
    ⚠ 准备 |b⟩ 可能昂贵

研究方向（2025+）：

  - 更好的 ansatz 设计
  - 预条件技术
  - 量子自然梯度
  - 与经典求解器的混合方法

结论：

  VQLS 是 NISQ 时代最有前景的
  线性系统求解方法之一！
    """)

    print("\n✓ VQLS 是 HHL 的 NISQ 友好替代方案")


if __name__ == '__main__':
    try:
        test_vqls()
        explain_vqls()

        print("\n🎉 恭喜！你已掌握 VQLS！")
        print("\n关键要点:")
        print("- NISQ 友好的线性求解器")
        print("- 变分优化替代相位估计")
        print("- 2023-2024 年研究热点")
        print("- 有实际应用前景")

    except AssertionError as e:
        print(f"❌ 测试失败: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
