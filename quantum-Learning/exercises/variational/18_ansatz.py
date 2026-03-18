"""
练习 18: 参数化量子电路（Ansatz）
==================

目标：设计和实现参数化量子电路

知识点：
- Ansatz 是变分量子算法的核心
- 参数化电路允许通过调整参数来优化
- 不同的 ansatz 适用于不同的问题

Ansatz 类型：
1. Hardware-Efficient Ansatz：适配硬件拓扑
2. Problem-Inspired Ansatz：基于问题结构
3. UCCSD Ansatz：用于量子化学

任务：实现多种 ansatz 设计
"""

from qiskit import QuantumCircuit, Parameter
from qiskit.circuit import ParameterVector
import numpy as np


def create_hardware_efficient_ansatz(n_qubits, depth=1):
    """
    创建 Hardware-Efficient Ansatz

    特点：
    - 利用硬件的天然连接
    - 旋转层 + 纠缠层交替

    参数：
        n_qubits: 量子比特数
        depth: 电路深度（重复层数）

    返回：
        QuantumCircuit: 参数化电路
    """
    # TODO: 创建参数
    # params = ParameterVector('θ', length=n_qubits * depth * 2)

    qc = QuantumCircuit(n_qubits)

    # TODO: 实现 ansatz
    # for d in range(depth):
    #     # 旋转层
    #     for i in range(n_qubits):
    #         qc.ry(params[...], i)
    #         qc.rz(params[...], i)
    #
    #     # 纠缠层
    #     for i in range(n_qubits - 1):
    #         qc.cx(i, i+1)

    return qc


def create_alternating_layered_ansatz(n_qubits, depth=2):
    """
    创建交替分层 Ansatz

    结构：RY - CZ - RY - CZ - ...

    参数：
        n_qubits: 量子比特数
        depth: 深度

    返回：
        QuantumCircuit
    """
    params = ParameterVector('θ', length=n_qubits * depth)
    qc = QuantumCircuit(n_qubits)

    param_idx = 0
    for d in range(depth):
        # RY 层
        for i in range(n_qubits):
            qc.ry(params[param_idx], i)
            param_idx += 1

        # CZ 纠缠层
        if d < depth - 1:  # 最后一层不需要纠缠
            for i in range(n_qubits - 1):
                qc.cz(i, i + 1)

    return qc


def count_parameters(qc):
    """
    计算电路中的参数数量

    参数：
        qc: 量子电路

    返回：
        int: 参数数量
    """
    return len(qc.parameters)


def test_ansatz():
    """测试不同的 ansatz"""
    print("测试参数化量子电路（Ansatz）\n")
    print("=" * 60)

    n_qubits = 3

    # 测试 1: Hardware-Efficient Ansatz
    print(f"测试 1: Hardware-Efficient Ansatz ({n_qubits} qubits)")
    he_ansatz = create_hardware_efficient_ansatz(n_qubits, depth=2)

    print(f"参数数量: {count_parameters(he_ansatz)}")
    print("\n电路结构:")
    print(he_ansatz.draw(output='text'))

    # 测试 2: Alternating Layered Ansatz
    print(f"\n{'='*60}")
    print(f"测试 2: Alternating Layered Ansatz ({n_qubits} qubits)")
    al_ansatz = create_alternating_layered_ansatz(n_qubits, depth=2)

    print(f"参数数量: {count_parameters(al_ansatz)}")
    print("\n电路结构:")
    print(al_ansatz.draw(output='text'))

    print("\n✓ Ansatz 创建成功！")

    return True


def explain_ansatz():
    """解释 Ansatz 设计"""
    print("\n" + "=" * 60)
    print("Ansatz 设计原则")
    print("=" * 60)

    print("""
什么是 Ansatz？

  变分量子算法的流程：
    1. 准备参数化量子态：|ψ(θ)⟩
    2. 测量目标函数：f(θ) = ⟨ψ(θ)|H|ψ(θ)⟩
    3. 经典优化：θ ← argmin f(θ)
    4. 重复直到收敛

  Ansatz = |ψ(θ)⟩ 的电路表示

设计考虑：

  1. 表达能力（Expressibility）
     - 能否表达目标态？
     - 参数空间是否足够大？

  2. 纠缠能力（Entangling Capability）
     - 能产生足够的纠缠吗？
     - 对于强关联系统尤其重要

  3. 硬件效率（Hardware Efficiency）
     - 门数量合理吗？
     - 电路深度可控吗？
     - 适配硬件连接拓扑吗？

  4. 可训练性（Trainability）
     - 存在贫瘠高原（Barren Plateau）吗？
     - 梯度会消失吗？

Ansatz 类型：

  Hardware-Efficient Ansatz：
    ✓ 适配硬件
    ✓ 浅电路深度
    ✗ 可能缺乏物理意义
    ✗ 可能遇到贫瘠高原

  Problem-Inspired Ansatz：
    ✓ 编码问题结构
    ✓ 更快收敛
    ✗ 需要领域知识
    ✗ 可能更深

  UCCSD（量子化学）：
    ✓ 基于耦合簇理论
    ✓ 有物理意义
    ✗ 电路非常深
    ✗ 参数很多

贫瘠高原问题：

  现象：
    - 在大规模参数化电路中
    - 梯度随量子比特数指数衰减
    - 优化变得不可行

  解决方案：
    - 分层训练
    - 问题特定的 ansatz
    - 初始化策略

前沿研究（2024-2025）：

  🔬 自适应 Ansatz
     - ADAPT-VQE：动态增长 ansatz
     - 只添加需要的门

  🔬 对称性保护
     - 利用物理对称性
     - 减少参数空间

  🔬 量子自然梯度
     - 更好的优化策略
     - 避免贫瘠高原

  🔬 可微分量子电路
     - 端到端量子机器学习
     - 与经典神经网络混合

最佳实践：

  1. 从简单开始，逐渐增加复杂度
  2. 使用先验知识（如对称性）
  3. 监控梯度大小
  4. 尝试多个初始化
  5. 可视化优化景观
    """)


if __name__ == '__main__':
    try:
        test_ansatz()
        explain_ansatz()

        print("\n🎉 恭喜！你已掌握 Ansatz 设计！")
        print("\n关键要点:")
        print("- Ansatz 是变分算法的核心")
        print("- 需要平衡表达能力和可训练性")
        print("- 不同问题需要不同设计")
        print("- 贫瘠高原是重要挑战")

    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
