"""
练习 17: Syndrome 测量
==================

目标：深入理解 syndrome 测量的原理和技术

知识点：
- Syndrome 是错误的"指纹"
- 测量 syndrome 而不是直接测量量子态
- 使用稳定子（Stabilizer）的概念

稳定子理论：
- 稳定子码是最重要的量子纠错码类别
- Pauli 算子张量积的群论描述
- Syndrome = 稳定子测量的结果

任务：实现和理解 syndrome 测量
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import Aer
import numpy as np


def measure_stabilizer_xx(qc, q0, q1, ancilla, c_bit):
    """
    测量 XX 稳定子

    测量两个量子比特的 XX 奇偶性

    参数：
        qc: 量子电路
        q0, q1: 数据量子比特
        ancilla: 辅助量子比特
        c_bit: 经典比特
    """
    # TODO: 实现 XX 稳定子测量
    # 1. H on ancilla (准备 |+⟩)
    # 2. CNOT from ancilla to q0
    # 3. CNOT from ancilla to q1
    # 4. H on ancilla
    # 5. Measure ancilla

    pass


def measure_stabilizer_zz(qc, q0, q1, ancilla, c_bit):
    """
    测量 ZZ 稳定子

    测量两个量子比特的 ZZ 奇偶性

    参数：
        qc: 量子电路
        q0, q1: 数据量子比特
        ancilla: 辅助量子比特
        c_bit: 经典比特
    """
    # TODO: 实现 ZZ 稳定子测量
    # 1. CNOT from q0 to ancilla
    # 2. CNOT from q1 to ancilla
    # 3. Measure ancilla

    pass


def create_syndrome_measurement_demo():
    """
    创建 syndrome 测量演示电路

    返回：
        QuantumCircuit
    """
    data = QuantumRegister(2, 'data')
    ancilla = QuantumRegister(1, 'ancilla')
    syndrome = ClassicalRegister(1, 'syndrome')

    qc = QuantumCircuit(data, ancilla, syndrome)

    # 准备纠缠态
    qc.h(data[0])
    qc.cx(data[0], data[1])

    qc.barrier()

    # 引入错误
    qc.x(data[1])

    qc.barrier()

    # TODO: 测量 ZZ 稳定子
    measure_stabilizer_zz(qc, 0, 1, 2, 0)

    return qc


def test_syndrome_measurement():
    """测试 syndrome 测量"""
    print("测试 Syndrome 测量\n")
    print("=" * 60)

    qc = create_syndrome_measurement_demo()

    print("电路图:")
    print(qc.draw(output='text'))

    simulator = Aer.get_backend('qasm_simulator')
    job = simulator.run(qc, shots=100)
    counts = job.result().get_counts()

    print(f"\nSyndrome 结果: {counts}")

    print("\n✓ Syndrome 测量演示完成")

    return True


def explain_syndrome():
    """解释 syndrome 和稳定子"""
    print("\n" + "=" * 60)
    print("Syndrome 测量与稳定子理论")
    print("=" * 60)

    print("""
什么是 Syndrome？

  经典纠错：
    - 数据：101
    - 奇偶校验：1 ⊕ 0 ⊕ 1 = 0
    - Syndrome = 校验结果

  量子纠错：
    - 不能直接测量量子态
    - 测量某些"奇偶性"（稳定子）
    - Syndrome = 稳定子测量结果

稳定子（Stabilizer）：

  定义：
    S 是一个算子，如果 S|ψ⟩ = |ψ⟩，
    则 S 是态 |ψ⟩ 的稳定子

  例子：
    - ZZ 稳定子：ZZ|00⟩ = |00⟩, ZZ|11⟩ = |11⟩
    - XX 稳定子：XX|++⟩ = |++⟩, XX|--⟩ = |--⟩

  关键性质：
    - 稳定子测量不破坏被保护的子空间
    - 但能检测错误（错误会翻转稳定子的本征值）

Syndrome 测量的原理：

  1. 准备辅助量子比特
  2. 与数据量子比特进行纠缠操作
  3. 测量辅助量子比特
  4. 数据量子比特不被直接测量！

示例：测量 ZZ

  电路：
    q0 ───●───
          │
    q1 ───●───
          │
    anc ──┤M├─

  如果测量得 0：ZZ本征值 = +1（无错误或偶数错误）
  如果测量得 1：ZZ本征值 = -1（奇数错误）

稳定子码的优势：

  ✓ 统一框架：描述大多数重要的纠错码
  ✓ 高效 syndrome 提取
  ✓ 容易容错实现

常见稳定子码：

  - Shor 码
  - Steane 码
  - 表面码（最实用）
  - CSS 码族

历史：

  - Gottesman 1996：稳定子形式化
  - Calderbank-Shor-Steane 1996：CSS 码
  - 为现代量子纠错奠定基础

数学细节：

  Pauli 群：
    P_n = {±1, ±i}^⊗n × {I, X, Y, Z}^⊗n

  稳定子群 S ⊂ P_n：
    - 阿贝尔群
    - 不包含 -I
    - 定义码空间：C = {|ψ⟩ : S|ψ⟩ = |ψ⟩ for all S ∈ S}

  Syndrome：
    测量每个稳定子生成元的本征值
    """)


if __name__ == '__main__':
    try:
        test_syndrome_measurement()
        explain_syndrome()

        print("\n🎉 恭喜！你已掌握 Syndrome 测量！")
        print("\n关键要点:")
        print("- Syndrome = 错误的指纹")
        print("- 稳定子理论提供统一框架")
        print("- 不破坏量子态的巧妙测量")
        print("- 现代量子纠错的基础")

    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
