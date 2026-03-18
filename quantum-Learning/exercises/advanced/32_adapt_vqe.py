"""
练习 32: ADAPT-VQE (Adaptive VQE)
==================

目标：实现自适应变分量子本征求解器

知识点：
- ADAPT-VQE 动态构建 ansatz
- 避免贫瘠高原问题
- 只添加必要的门

算法特点：
- 从简单 ansatz 开始
- 迭代添加最有用的算符
- 自适应电路深度

前沿进展（2019-2024）：
- Grimsley et al. (2019) 首次提出
- 2023-2024: 改进的算符池设计
- 应用于量子化学、凝聚态物理

任务：实现 ADAPT-VQE 的核心思想
"""

from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector
import numpy as np
from scipy.optimize import minimize


def create_operator_pool():
    """
    创建算符池

    对于2量子比特系统，使用简单的池

    返回：
        list: Pauli 算符列表
    """
    # TODO: 创建算符池
    # 对于量子化学，通常使用 fermionic 激发算符
    # 这里使用简化的 Pauli 算符池

    pool = [
        SparsePauliOp.from_list([('XX', 1.0)]),
        SparsePauliOp.from_list([('YY', 1.0)]),
        SparsePauliOp.from_list([('ZZ', 1.0)]),
        SparsePauliOp.from_list([('XI', 1.0)]),
        SparsePauliOp.from_list([('YI', 1.0)]),
        SparsePauliOp.from_list([('ZI', 1.0)]),
        SparsePauliOp.from_list([('IX', 1.0)]),
        SparsePauliOp.from_list([('IY', 1.0)]),
        SparsePauliOp.from_list([('IZ', 1.0)]),
    ]

    return pool


def compute_gradient(state, hamiltonian, operator):
    """
    计算梯度

    ∂E/∂θ|_{θ=0} = ⟨ψ|[H, A]|ψ⟩

    参数：
        state: 当前态
        hamiltonian: 哈密顿量
        operator: 算符 A

    返回：
        float: 梯度
    """
    # TODO: 计算对易子 [H, A]
    # 梯度 = ⟨ψ|[H, A]|ψ⟩

    # [H, A] = HA - AH
    HA = hamiltonian.dot(operator)
    AH = operator.dot(hamiltonian)
    commutator = HA - AH

    # ⟨ψ|[H,A]|ψ⟩
    gradient = state.expectation_value(commutator).real

    return abs(gradient)


def apply_operator_to_circuit(qc, operator, param):
    """
    将参数化算符添加到电路

    exp(-i θ A) ≈ 实现

    参数：
        qc: 量子电路
        operator: Pauli 算符
        param: 参数
    """
    # TODO: 实现 exp(-i θ A)
    # 对于 Pauli 算符，使用 Pauli 旋转

    pauli_str = str(operator.paulis[0])

    if pauli_str == 'XX':
        qc.rxx(2 * param, 0, 1)
    elif pauli_str == 'YY':
        qc.ryy(2 * param, 0, 1)
    elif pauli_str == 'ZZ':
        qc.rzz(2 * param, 0, 1)
    elif pauli_str == 'XI':
        qc.rx(2 * param, 0)
    elif pauli_str == 'YI':
        qc.ry(2 * param, 0)
    elif pauli_str == 'ZI':
        qc.rz(2 * param, 0)
    elif pauli_str == 'IX':
        qc.rx(2 * param, 1)
    elif pauli_str == 'IY':
        qc.ry(2 * param, 1)
    elif pauli_str == 'IZ':
        qc.rz(2 * param, 1)


def adapt_vqe(hamiltonian, initial_state=None, max_iterations=5):
    """
    ADAPT-VQE 算法

    参数：
        hamiltonian: 目标哈密顿量
        initial_state: 初始态（默认 |00⟩）
        max_iterations: 最大迭代次数

    返回：
        dict: 结果
    """
    print("ADAPT-VQE: 自适应变分量子本征求解器\n")
    print("=" * 60)

    n_qubits = hamiltonian.num_qubits

    # 初始化
    if initial_state is None:
        qc = QuantumCircuit(n_qubits)
        current_state = Statevector.from_instruction(qc)
    else:
        current_state = initial_state

    # 算符池
    operator_pool = create_operator_pool()

    # 选择的算符和参数
    selected_operators = []
    parameters = []

    # 精确解（用于比较）
    exact_energy = min(np.linalg.eigvalsh(hamiltonian.to_matrix()))
    print(f"精确基态能量: {exact_energy:.6f}\n")

    # ADAPT 迭代
    for iteration in range(max_iterations):
        print(f"迭代 {iteration + 1}:")

        # 计算当前能量
        current_energy = current_state.expectation_value(hamiltonian).real
        print(f"  当前能量: {current_energy:.6f}")
        print(f"  误差: {abs(current_energy - exact_energy):.6f}")

        # TODO: 计算所有算符的梯度
        gradients = []
        for op in operator_pool:
            grad = compute_gradient(current_state, hamiltonian, op)
            gradients.append(grad)

        # 选择最大梯度的算符
        max_grad_idx = np.argmax(gradients)
        max_gradient = gradients[max_grad_idx]

        print(f"  最大梯度: {max_gradient:.6f}")

        # 收敛检查
        if max_gradient < 1e-3:
            print("  → 收敛！")
            break

        selected_op = operator_pool[max_grad_idx]
        print(f"  选择算符: {selected_op.paulis[0]}")

        # TODO: 添加算符并优化参数
        selected_operators.append(selected_op)
        parameters.append(0.0)  # 初始参数

        # 优化所有参数
        def energy_function(params):
            # 构建电路
            qc = QuantumCircuit(n_qubits)
            for i, (op, param) in enumerate(zip(selected_operators, params)):
                apply_operator_to_circuit(qc, op, param)

            # 计算能量
            state = Statevector.from_instruction(qc)
            energy = state.expectation_value(hamiltonian).real
            return energy

        # 优化
        result = minimize(energy_function, parameters, method='COBYLA',
                         options={'maxiter': 100})

        parameters = result.x.tolist()

        # 更新当前态
        qc = QuantumCircuit(n_qubits)
        for op, param in zip(selected_operators, parameters):
            apply_operator_to_circuit(qc, op, param)
        current_state = Statevector.from_instruction(qc)

        print(f"  优化后能量: {result.fun:.6f}\n")

    final_energy = current_state.expectation_value(hamiltonian).real

    print("=" * 60)
    print(f"最终能量: {final_energy:.6f}")
    print(f"精确能量: {exact_energy:.6f}")
    print(f"误差: {abs(final_energy - exact_energy):.6f}")
    print(f"电路深度: {len(selected_operators)} 个算符")

    return {
        'energy': final_energy,
        'exact_energy': exact_energy,
        'operators': selected_operators,
        'parameters': parameters,
        'circuit_depth': len(selected_operators)
    }


def test_adapt_vqe():
    """测试 ADAPT-VQE"""
    print("测试 ADAPT-VQE 算法\n")

    # 使用简单的哈密顿量
    H = SparsePauliOp.from_list([
        ('II', -1.0),
        ('ZZ', -0.5),
        ('XX', 0.5),
    ])

    result = adapt_vqe(H, max_iterations=5)

    # 验证
    assert abs(result['energy'] - result['exact_energy']) < 0.1, \
        "ADAPT-VQE 能量误差过大"

    print("\n✓ ADAPT-VQE 测试通过！")

    return True


def explain_adapt_vqe():
    """解释 ADAPT-VQE"""
    print("\n" + "=" * 60)
    print("ADAPT-VQE 详解")
    print("=" * 60)

    print("""
ADAPT-VQE vs VQE：

  传统 VQE：
    - 固定 ansatz 结构
    - 可能过度参数化（贫瘠高原）
    - 或欠参数化（表达能力不足）

  ADAPT-VQE：
    ✓ 动态构建 ansatz
    ✓ 只添加需要的算符
    ✓ 避免贫瘠高原
    ✓ 电路深度自适应

算法流程：

  1. 初始化：|ψ⟩ = |ψ_0⟩（通常是 HF 态）

  2. 循环：
     a. 计算梯度：∂E/∂θ_i|_{θ=0} = ⟨ψ|[H, A_i]|ψ⟩
     b. 选择最大梯度的算符 A_max
     c. 添加 exp(-i θ A_max) 到电路
     d. 优化所有参数

  3. 收敛：当 max|gradient| < ε

算符池设计：

  量子化学：
    - 单激发：a†_i a_j
    - 双激发：a†_i a†_j a_k a_l
    - UCCSD 算符

  凝聚态物理：
    - Pauli 算符组合
    - 特定对称性

  一般问题：
    - Pauli 字符串
    - Lie 代数生成元

优势：

  ✓ 紧凑的电路
     - 只添加必要的门
     - 减少噪声影响

  ✓ 避免贫瘠高原
     - 梯度始终有意义
     - 易于优化

  ✓ 系统化
     - 有理论保证
     - 收敛性质好

前沿进展（2023-2024）：

  🔬 改进的算符池
     - 基于问题对称性
     - 预筛选策略

  🔬 ADAPT-QAOA
     - 组合优化问题
     - 动态混合器

  🔬 硬件高效 ADAPT
     - 考虑硬件拓扑
     - 减少 SWAP 门

  🔬 快速梯度评估
     - 经典 shadow
     - 减少测量开销

应用：

  量子化学：
    - 分子基态能量
    - 激发态（ADAPT-VQD）

  凝聚态：
    - 强关联系统
    - 相变研究

  优化：
    - QUBO 问题
    - MaxCut 等

挑战：

  ⚠ 算符池选择
     - 池太大：计算开销
     - 池太小：表达能力不足

  ⚠ 梯度计算
     - 需要多次测量
     - 噪声影响

  ⚠ 收敛速度
     - 可能需要多次迭代
     - 参数优化仍然困难

2024-2025 研究方向：

  - 与量子纠错结合
  - 更智能的算符选择
  - 并行 ADAPT（选择多个算符）
  - 与机器学习结合

结论：

  ADAPT-VQE 代表了变分量子算法的
  新范式：自适应和问题导向！
    """)

    print("\n✓ ADAPT-VQE 是 VQE 的智能进化版本")


if __name__ == '__main__':
    try:
        test_adapt_vqe()
        explain_adapt_vqe()

        print("\n🎉 恭喜！你已掌握 ADAPT-VQE！")
        print("\n关键要点:")
        print("- 动态构建 ansatz")
        print("- 避免贫瘠高原")
        print("- 2019-2024 重要进展")
        print("- 量子化学的实用工具")

    except AssertionError as e:
        print(f"❌ 测试失败: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
