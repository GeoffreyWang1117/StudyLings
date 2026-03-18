"""
练习 14: 比特翻转码
==================

目标：实现最简单的量子纠错码

知识点：
- 量子纠错是实现可靠量子计算的关键
- 比特翻转码保护量子态免受比特翻转错误（X 错误）
- 使用 3 个物理量子比特编码 1 个逻辑量子比特
- 编码：|0⟩_L → |000⟩, |1⟩_L → |111⟩

原理：
- 通过冗余实现纠错
- 多数投票：如果一个比特翻转，另外两个仍然正确
- Syndrome 测量检测错误位置而不破坏量子态

任务：实现 3-qubit 比特翻转码
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector, state_fidelity
import numpy as np


def encode_bit_flip(qc, data_qubit):
    """
    编码逻辑量子比特到比特翻转码

    |ψ⟩ = α|0⟩ + β|1⟩ → α|000⟩ + β|111⟩

    参数：
        qc: 量子电路
        data_qubit: 数据量子比特索引（假设后续是编码量子比特）
    """
    # TODO: 实现编码
    # 使用 CNOT 门将数据复制到其他两个量子比特
    # qc.cx(data_qubit, data_qubit + 1)
    # qc.cx(data_qubit, data_qubit + 2)

    pass


def measure_syndrome_bit_flip(qc, data_qubits, ancilla_qubits, classical_bits):
    """
    测量 syndrome（错误综合征）

    不测量数据量子比特本身，而是测量奇偶性

    参数：
        qc: 量子电路
        data_qubits: 数据量子比特索引列表 [q0, q1, q2]
        ancilla_qubits: 辅助量子比特索引列表 [a0, a1]
        classical_bits: 经典比特索引列表 [c0, c1]
    """
    # Syndrome 1: 比较 q0 和 q1
    # TODO: CNOT(q0, a0)
    # TODO: CNOT(q1, a0)
    # TODO: measure(a0, c0)



    qc.barrier()

    # Syndrome 2: 比较 q1 和 q2
    # TODO: CNOT(q1, a1)
    # TODO: CNOT(q2, a1)
    # TODO: measure(a1, c1)




def correct_bit_flip_error(qc, data_qubits, classical_bits):
    """
    根据 syndrome 纠正错误

    Syndrome 解读：
    - 00: 无错误
    - 01: q0 有错误
    - 10: q2 有错误
    - 11: q1 有错误

    参数：
        qc: 量子电路
        data_qubits: 数据量子比特索引
        classical_bits: syndrome 测量结果
    """
    # TODO: 根据 syndrome 应用 X 门纠正
    # 使用 c_if 条件执行

    # if syndrome == 01 (二进制), apply X to q0
    # if syndrome == 11, apply X to q1
    # if syndrome == 10, apply X to q2

    # 提示：在 Qiskit 中使用经典控制比较复杂
    # 简化版本：我们在后处理中处理


def create_bit_flip_code_circuit():
    """
    创建完整的比特翻转码电路（编码 + 错误 + 检测 + 纠正）

    返回：
        QuantumCircuit: 比特翻转码电路
    """
    # 3 个数据量子比特 + 2 个辅助量子比特
    data = QuantumRegister(3, 'data')
    ancilla = QuantumRegister(2, 'ancilla')
    syndrome = ClassicalRegister(2, 'syndrome')
    qc = QuantumCircuit(data, ancilla, syndrome)

    # 准备初始态（例如 |+⟩ = (|0⟩ + |1⟩)/√2）
    qc.h(data[0])

    qc.barrier(label='初始态')

    # TODO: 编码
    encode_bit_flip(qc, 0)

    qc.barrier(label='编码完成')

    # 引入错误（在 q[1] 上）
    qc.x(data[1])

    qc.barrier(label='错误注入')

    # TODO: Syndrome 测量
    measure_syndrome_bit_flip(qc, [0, 1, 2], [3, 4], [0, 1])

    qc.barrier(label='Syndrome测量')

    return qc


def test_bit_flip_code():
    """测试比特翻转码"""
    print("测试 3-qubit 比特翻转码\n")
    print("=" * 60)

    # 创建电路
    qc = create_bit_flip_code_circuit()

    print("电路图:")
    print(qc.draw(output='text'))

    # 运行电路
    simulator = Aer.get_backend('qasm_simulator')
    job = simulator.run(qc, shots=100)
    counts = job.result().get_counts()

    print(f"\nSyndrome 测量结果: {counts}")

    # 分析 syndrome
    print("\nSyndrome 分析:")
    for syndrome_str, count in sorted(counts.items()):
        syndrome_int = int(syndrome_str, 2)
        if syndrome_int == 0:
            error_location = "无错误"
        elif syndrome_int == 1:
            error_location = "q[0] 有错误"
        elif syndrome_int == 2:
            error_location = "q[2] 有错误"
        elif syndrome_int == 3:
            error_location = "q[1] 有错误"

        print(f"  Syndrome {syndrome_str}: {error_location} (出现 {count} 次)")

    # 验证：我们在 q[1] 注入了错误，应该检测到 syndrome = 11
    expected_syndrome = '11'
    assert expected_syndrome in counts, f"应该检测到 syndrome {expected_syndrome}"
    assert counts[expected_syndrome] > 90, f"检测率应该很高"

    print("\n✓ 比特翻转码成功检测到错误！")

    return True


def demonstrate_error_correction():
    """演示完整的纠错过程"""
    print("\n" + "=" * 60)
    print("完整纠错演示")
    print("=" * 60)

    # 不使用 syndrome 测量，直接演示编码和纠错
    qc = QuantumCircuit(3)

    # 准备 |+⟩ 态
    qc.h(0)

    print("\n步骤 1: 初始态 |+⟩")
    state_initial = Statevector.from_instruction(qc)

    # 编码
    qc.cx(0, 1)
    qc.cx(0, 2)

    print("步骤 2: 编码为 |+++⟩ (逻辑 |+⟩)")
    state_encoded = Statevector.from_instruction(qc)

    # 引入错误
    qc.x(1)

    print("步骤 3: 在 q[1] 引入比特翻转错误")
    state_error = Statevector.from_instruction(qc)

    # 纠错（简化：直接应用 X 到 q[1]）
    qc.x(1)

    print("步骤 4: 纠正错误")
    state_corrected = Statevector.from_instruction(qc)

    # 解码
    qc.cx(0, 2)
    qc.cx(0, 1)

    print("步骤 5: 解码")
    state_final = Statevector.from_instruction(qc)

    # 计算保真度
    # 只看第一个量子比特（逻辑量子比特）
    fidelity = abs(state_initial.data[0] * np.conj(state_final.data[0]) +
                   state_initial.data[1] * np.conj(state_final.data[1]))

    print(f"\n初始态和最终态的保真度: {fidelity:.6f}")
    print("✓ 量子态成功恢复！")


def explain_bit_flip_code():
    """解释比特翻转码"""
    print("\n" + "=" * 60)
    print("比特翻转码原理")
    print("=" * 60)

    print("""
量子纠错的挑战：

  经典纠错：
    - 复制数据：0 → 000
    - 多数投票纠错

  量子纠错的困难：
    ✗ 不可克隆定理：不能复制未知量子态
    ✗ 测量会破坏叠加态
    ✗ 错误是连续的（不只是 0/1）

比特翻转码的解决方案：

  编码（不是克隆！）：
    |0⟩_L → |000⟩
    |1⟩_L → |111⟩
    α|0⟩ + β|1⟩ → α|000⟩ + β|111⟩

  关键：保持了叠加！

  Syndrome 测量：
    - 不测量量子比特的值
    - 只测量奇偶性（比较量子比特）
    - 不破坏叠加态

  纠正：
    - 根据 syndrome 应用 X 门
    - 恢复原始态

Syndrome 表：
  ┌──────────┬─────────────┬──────────┐
  │ Syndrome │ 错误位置    │ 纠正操作 │
  ├──────────┼─────────────┼──────────┤
  │ 00       │ 无错误      │ 无       │
  │ 01       │ q[0] 翻转   │ X(q[0])  │
  │ 10       │ q[2] 翻转   │ X(q[2])  │
  │ 11       │ q[1] 翻转   │ X(q[1])  │
  └──────────┴─────────────┴──────────┘

限制：
  ⚠ 只能纠正单个比特翻转错误
  ✗ 不能纠正相位翻转错误（Z 错误）
  ✗ 两个或更多错误会失败

下一步：
  - 相位翻转码（纠正 Z 错误）
  - Shor 码（同时纠正 X 和 Z 错误）
  - 更高效的码（如表面码、LDPC）

历史意义：
  - 证明了量子纠错是可能的
  - 开启了容错量子计算的研究
  - 1995-1996 年的重大突破
    """)


if __name__ == '__main__':
    try:
        test_bit_flip_code()
        demonstrate_error_correction()
        explain_bit_flip_code()

        print("\n🎉 恭喜！你已掌握量子纠错的基础！")
        print("\n关键要点:")
        print("- 量子纠错不违反不可克隆定理")
        print("- Syndrome 测量不破坏量子态")
        print("- 冗余编码 + 奇偶检查 = 纠错")
        print("- 这是容错量子计算的基础")

    except AssertionError as e:
        print(f"❌ 测试失败: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
