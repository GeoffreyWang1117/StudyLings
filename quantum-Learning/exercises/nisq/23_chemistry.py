"""
练习 23: 量子化学应用
==================

目标：使用 VQE 计算分子能量

知识点：
- 量子化学是量子计算的重要应用
- 计算分子基态能量
- 药物发现、材料设计

示例分子：H2（氢分子）

任务：使用 VQE 计算 H2 基态能量
"""

from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector
from scipy.optimize import minimize
import numpy as np


def h2_hamiltonian():
    """
    H2 分子哈密顿量（简化版，STO-3G 基组）
    """
    # 这是简化的 H2 哈密顿量
    return SparsePauliOp.from_list([
        ('II', -1.0523),
        ('IZ', 0.3979),
        ('ZI', -0.3979),
        ('ZZ', -0.0112),
        ('XX', 0.1809),
    ])


def chemistry_ansatz(params):
    """
    化学启发的 ansatz
    """
    qc = QuantumCircuit(2)
    qc.ry(params[0], 0)
    qc.ry(params[1], 1)
    qc.cx(0, 1)
    qc.ry(params[2], 0)
    qc.ry(params[3], 1)
    return qc


def compute_energy(params):
    """
    计算能量期望值
    """
    qc = chemistry_ansatz(params)
    state = Statevector.from_instruction(qc)
    H = h2_hamiltonian()
    energy = state.expectation_value(H).real
    return energy


def run_chemistry_vqe():
    """
    运行 VQE 计算 H2 能量
    """
    print("量子化学：计算 H2 分子基态能量\n")
    print("=" * 60)
    
    # 精确解
    H = h2_hamiltonian()
    exact_energy = min(np.linalg.eigvalsh(H.to_matrix()))
    print(f"精确基态能量: {exact_energy:.6f} Hartree\n")
    
    # VQE 优化
    print("运行 VQE...")
    initial_params = np.random.rand(4) * 2 * np.pi
    
    result = minimize(compute_energy, initial_params, method='COBYLA', 
                     options={'maxiter': 100})
    
    print(f"VQE 能量: {result.fun:.6f} Hartree")
    print(f"误差: {abs(result.fun - exact_energy):.6f} Hartree")
    
    print("\n✓ 量子化学计算完成！")
    print("\n这是量子计算最有前景的应用之一：")
    print("- 药物发现")
    print("- 新材料设计")
    print("- 催化剂优化")


if __name__ == '__main__':
    run_chemistry_vqe()
