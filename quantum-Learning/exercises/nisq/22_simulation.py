"""
练习 22: 量子模拟
==================

目标：使用量子计算机模拟量子系统

知识点：
- 量子模拟是量子计算的杀手级应用
- 模拟量子系统的时间演化
- Hamiltonian 模拟

应用：
- 凝聚态物理
- 高能物理
- 量子化学

任务：模拟简单的量子系统
"""

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp
import numpy as np


def simulate_ising_model(n_qubits, J, h, t):
    """
    模拟 Ising 模型
    
    H = -J Σ Z_i Z_{i+1} - h Σ X_i
    """
    print(f"模拟 {n_qubits}-qubit Ising 模型")
    print(f"参数: J={J}, h={h}, t={t}\n")
    
    qc = QuantumCircuit(n_qubits)
    
    # 初始态：|+⟩^⊗n
    qc.h(range(n_qubits))
    
    # Trotter 分解：exp(-iHt) ≈ (exp(-iH_1 dt) exp(-iH_2 dt))^n
    n_steps = 10
    dt = t / n_steps
    
    for _ in range(n_steps):
        # ZZ 项
        for i in range(n_qubits - 1):
            qc.cx(i, i+1)
            qc.rz(2 * J * dt, i+1)
            qc.cx(i, i+1)
        
        # X 项
        for i in range(n_qubits):
            qc.rx(2 * h * dt, i)
    
    print("电路图:")
    print(qc.draw(output='text', fold=-1))
    
    state = Statevector.from_instruction(qc)
    
    print(f"\n最终态的振幅（前4个）:")
    for i in range(min(4, len(state.data))):
        print(f"  |{i:0{n_qubits}b}⟩: {state.data[i]:.4f}")
    
    print("\n✓ 量子模拟完成！")
    print("量子计算机可以高效模拟量子系统！")


if __name__ == '__main__':
    simulate_ising_model(n_qubits=3, J=1.0, h=0.5, t=1.0)
