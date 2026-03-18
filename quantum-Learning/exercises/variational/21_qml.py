"""
练习 21: 量子机器学习基础
==================

目标：理解量子机器学习的基本概念

知识点：
- 量子神经网络（QNN）
- 量子分类器
- 量子特征图
- 混合量子-经典学习

应用：
- 分类问题
- 回归问题
- 生成模型

任务：实现简单的量子分类器
"""

from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
import numpy as np
from scipy.optimize import minimize


def feature_map(qc, x):
    """
    数据编码（特征图）
    
    将经典数据 x 编码到量子态
    """
    for i, val in enumerate(x):
        qc.ry(val, i)


def variational_circuit(qc, params):
    """
    变分层（可训练部分）
    """
    n = qc.num_qubits
    for i in range(n):
        qc.ry(params[i], i)
        qc.rz(params[i + n], i)
    
    for i in range(n-1):
        qc.cx(i, i+1)


def quantum_classifier(x, params):
    """
    量子分类器
    """
    n_qubits = len(x)
    qc = QuantumCircuit(n_qubits)
    
    feature_map(qc, x)
    variational_circuit(qc, params)
    
    # 测量第一个量子比特的期望值
    state = Statevector.from_instruction(qc)
    # 简化：返回 <Z_0>
    expectation = abs(state.data[0])**2 - abs(state.data[1])**2
    
    return expectation


def train_quantum_classifier():
    """训练量子分类器"""
    print("量子机器学习：训练分类器\n")
    print("=" * 60)
    
    # 简单的 XOR 问题数据
    X_train = np.array([[0, 0], [0, 1], [1, 0], [1, 1]]) * np.pi/2
    y_train = np.array([0, 1, 1, 0])  # XOR
    
    # 初始化参数
    n_params = 4  # 2 qubits * 2 params each
    params = np.random.rand(n_params) * 2 * np.pi
    
    print("训练数据（XOR问题）:")
    for x, y in zip(X_train, y_train):
        print(f"  输入: {x}, 标签: {y}")
    
    def loss(params):
        total_loss = 0
        for x, y in zip(X_train, y_train):
            pred = quantum_classifier(x, params)
            # 将期望值映射到 [0,1]
            pred = (pred + 1) / 2
            # 二元交叉熵
            total_loss += (y - pred)**2
        return total_loss / len(X_train)
    
    print("\n开始训练...")
    initial_loss = loss(params)
    print(f"初始损失: {initial_loss:.4f}")
    
    # 优化
    result = minimize(loss, params, method='COBYLA', options={'maxiter': 50})
    
    final_loss = result.fun
    print(f"最终损失: {final_loss:.4f}")
    
    print("\n✓ 量子分类器训练完成！")
    print("\n量子机器学习结合了量子计算和机器学习")
    print("是 2024-2025 年的研究热点！")

if __name__ == '__main__':
    train_quantum_classifier()
