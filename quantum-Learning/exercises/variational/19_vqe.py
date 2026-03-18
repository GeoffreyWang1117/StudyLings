"""
练习 19: VQE (Variational Quantum Eigensolver)
==================

目标：实现变分量子本征求解器

知识点：
- VQE 是 NISQ 时代最重要的算法之一
- 用于找到哈密顿量 H 的最小本征值（基态能量）
- 混合量子-经典算法：
  * 量子：准备试探态并测量期望值
  * 经典：优化参数

应用：
- 量子化学（分子基态能量）
- 材料科学
- 优化问题
- 凝聚态物理

VQE 流程：
1. 准备参数化量子电路 |ψ(θ)⟩
2. 测量 ⟨ψ(θ)|H|ψ(θ)⟩
3. 经典优化器更新 θ
4. 重复直到收敛

任务：实现 VQE 算法
"""

from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.quantum_info import SparsePauliOp
import numpy as np
from scipy.optimize import minimize


def create_ansatz(parameters):
    """
    创建参数化量子电路（Ansatz）

    使用 Hardware-Efficient Ansatz：
    - 单量子比特旋转门（RY, RZ）
    - CNOT 纠缠门

    参数：
        parameters: 参数数组

    返回：
        QuantumCircuit: 参数化电路
    """
    n_qubits = 2
    qc = QuantumCircuit(n_qubits)

    # TODO: 实现参数化电路
    # 示例结构：
    # Layer 1: RY gates
    # Layer 2: Entangling CNOTs
    # Layer 3: RY gates again

    # 提示：
    # qc.ry(parameters[0], 0)
    # qc.ry(parameters[1], 1)
    # qc.cx(0, 1)
    # qc.ry(parameters[2], 0)
    # qc.ry(parameters[3], 1)

    return qc


def measure_expectation(qc, observable):
    """
    测量期望值 ⟨ψ|O|ψ⟩

    参数：
        qc: 量子电路（准备好的态）
        observable: SparsePauliOp 可观测量

    返回：
        float: 期望值
    """
    # 使用 Qiskit 的 Estimator 或 Statevector
    from qiskit.quantum_info import Statevector

    # 获取状态向量
    state = Statevector.from_instruction(qc)

    # 计算期望值
    expectation = state.expectation_value(observable).real

    return expectation


def vqe_objective(parameters, hamiltonian):
    """
    VQE 目标函数

    参数：
        parameters: 电路参数
        hamiltonian: 哈密顿量

    返回：
        float: 能量期望值
    """
    # TODO: 创建 ansatz
    qc = create_ansatz(parameters)

    # TODO: 测量期望值
    energy = measure_expectation(qc, hamiltonian)

    return energy


def run_vqe(hamiltonian, initial_params=None):
    """
    运行 VQE 算法

    参数：
        hamiltonian: 要求解的哈密顿量
        initial_params: 初始参数（可选）

    返回：
        dict: 包含最优能量和参数的结果
    """
    # 参数数量
    n_params = 4

    # 初始参数
    if initial_params is None:
        initial_params = np.random.rand(n_params) * 2 * np.pi

    print("VQE 优化开始...")
    print(f"初始参数: {initial_params}")

    # TODO: 使用经典优化器
    # 提示：使用 scipy.optimize.minimize
    result = minimize(
        vqe_objective,
        initial_params,
        args=(hamiltonian,),
        method='COBYLA',
        options={'maxiter': 100}
    )

    print(f"\n优化完成！")
    print(f"迭代次数: {result.nfev}")
    print(f"最优能量: {result.fun:.6f}")
    print(f"最优参数: {result.x}")

    return {
        'energy': result.fun,
        'parameters': result.x,
        'iterations': result.nfev
    }


def test_vqe_h2():
    """测试 VQE：氢分子 H2"""
    print("测试 VQE：氢分子 (H2) 问题\n")
    print("=" * 60)

    # 简化的 H2 哈密顿量（2 量子比特）
    # 这是 H2 分子在 STO-3G 基组下的简化版本
    hamiltonian = SparsePauliOp.from_list([
        ('II', -1.0523),
        ('IZ', 0.3979),
        ('ZI', -0.3979),
        ('ZZ', -0.0112),
        ('XX', 0.1809),
    ])

    print("哈密顿量:")
    print(hamiltonian)
    print()

    # 精确解（用于比较）
    from qiskit.quantum_info import Statevector
    exact_energy = min(np.linalg.eigvalsh(hamiltonian.to_matrix()))
    print(f"精确基态能量: {exact_energy:.6f}\n")

    # 运行 VQE
    result = run_vqe(hamiltonian)

    # 验证结果
    error = abs(result['energy'] - exact_energy)
    print(f"\n误差: {error:.6f}")

    # 允许一定的数值误差
    assert error < 0.01, f"VQE 能量误差过大: {error}"

    print("✓ VQE 成功找到基态能量！")

    return True


def test_vqe_simple():
    """测试 VQE：简单哈密顿量"""
    print("\n" + "=" * 60)
    print("测试 VQE：简单哈密顿量 H = Z")
    print("=" * 60)

    # 简单哈密顿量：H = Z（本征值：+1, -1）
    hamiltonian = SparsePauliOp.from_list([('Z', 1.0)])

    print("\n哈密顿量: H = Z")
    print("期望基态能量: -1.0\n")

    # 运行 VQE
    result = run_vqe(hamiltonian, initial_params=np.array([np.pi, 0]))

    # 验证
    assert abs(result['energy'] - (-1.0)) < 0.1, "应该找到能量 -1"

    print("✓ VQE 正确！")

    return True


def explain_vqe():
    """解释 VQE 算法"""
    print("\n" + "=" * 60)
    print("VQE 工作原理")
    print("=" * 60)

    print("""
变分原理：
  对于任何试探态 |ψ⟩：
  E₀ ≤ ⟨ψ|H|ψ⟩
  其中 E₀ 是基态能量

VQE 策略：
  1. 参数化试探态：|ψ(θ)⟩
  2. 测量能量：E(θ) = ⟨ψ(θ)|H|ψ(θ)⟩
  3. 优化参数：min_θ E(θ)
  4. 收敛到基态

为什么适合 NISQ 设备？
  ✓ 电路深度浅（减少噪声影响）
  ✓ 利用经典优化器（容错）
  ✓ 可以逐步改进（变分特性）
  ✗ 需要多次测量（采样开销）

应用实例：
  - 2017: IBM 用 VQE 计算 H2 分子能量
  - 2020: Google 用 VQE 模拟化学反应
  - 2023: 药物发现、材料设计等

前沿进展：
  - 2024-2025: VQE 与纠错结合
  - 更高效的 ansatz 设计
  - 量子机器学习中的应用
    """)


if __name__ == '__main__':
    try:
        test_vqe_simple()
        test_vqe_h2()
        explain_vqe()

        print("\n🎉 恭喜！你已掌握 VQE 算法！")
        print("\n关键要点:")
        print("- NISQ 时代最重要的算法")
        print("- 量子-经典混合算法")
        print("- 应用于量子化学和优化")
        print("- 变分原理保证能量下界")
        print("\n这是通往实用量子计算的重要一步！")

    except AssertionError as e:
        print(f"❌ 测试失败: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
