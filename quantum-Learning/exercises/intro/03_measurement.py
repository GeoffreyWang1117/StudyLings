"""
练习 03: 量子测量
==================

目标：理解量子测量及其对量子态的影响

知识点：
- 测量会使量子态"坍缩"到某个确定的经典态
- 测量是概率性的：|ψ⟩ = α|0⟩ + β|1⟩，测量到 |0⟩ 的概率是 |α|²
- 测量后，量子态变为测量结果对应的态
- 测量是不可逆的操作

任务：创建不同的量子态并测量它们
"""

from qiskit import QuantumCircuit
from qiskit_aer import Aer
import numpy as np


def create_and_measure_zero():
    """
    创建 |0⟩ 态并测量

    返回：
        QuantumCircuit: 准备好测量的电路
    """
    qc = QuantumCircuit(1, 1)

    # TODO: 添加测量
    # 提示：使用 qc.measure(qubit_index, classical_bit_index)
    # 你的代码在这里

    return qc


def create_and_measure_one():
    """
    创建 |1⟩ 态并测量

    返回：
        QuantumCircuit: 准备好测量的电路
    """
    qc = QuantumCircuit(1, 1)

    # TODO: 使用 X 门将 |0⟩ 翻转为 |1⟩
    # 提示：qc.x(qubit_index)

    # TODO: 添加测量

    return qc


def create_and_measure_superposition():
    """
    创建叠加态并测量多次

    返回：
        QuantumCircuit: 准备好测量的电路
    """
    qc = QuantumCircuit(1, 1)

    # TODO: 创建叠加态（使用 H 门）

    # TODO: 添加测量

    return qc


def test_measurements():
    """测试所有测量"""
    simulator = Aer.get_backend('qasm_simulator')

    # 测试1: 测量 |0⟩
    print("测试 1: 测量 |0⟩ 态")
    qc0 = create_and_measure_zero()
    print(qc0.draw(output='text'))

    job0 = simulator.run(qc0, shots=100)
    counts0 = job0.result().get_counts()
    print(f"结果: {counts0}")

    assert '0' in counts0, "测量 |0⟩ 态应该得到 0"
    assert counts0.get('0', 0) > 95, "测量 |0⟩ 态应该几乎总是得到 0"
    print("✓ 通过\n")

    # 测试2: 测量 |1⟩
    print("测试 2: 测量 |1⟩ 态")
    qc1 = create_and_measure_one()
    print(qc1.draw(output='text'))

    job1 = simulator.run(qc1, shots=100)
    counts1 = job1.result().get_counts()
    print(f"结果: {counts1}")

    assert '1' in counts1, "测量 |1⟩ 态应该得到 1"
    assert counts1.get('1', 0) > 95, "测量 |1⟩ 态应该几乎总是得到 1"
    print("✓ 通过\n")

    # 测试3: 测量叠加态
    print("测试 3: 测量叠加态")
    qc_sup = create_and_measure_superposition()
    print(qc_sup.draw(output='text'))

    job_sup = simulator.run(qc_sup, shots=1000)
    counts_sup = job_sup.result().get_counts()
    print(f"结果: {counts_sup}")

    assert '0' in counts_sup and '1' in counts_sup, "叠加态应该产生 0 和 1"

    ratio_0 = counts_sup.get('0', 0) / 1000
    assert 0.4 < ratio_0 < 0.6, f"均匀叠加态测量到 0 的概率应约为50%"
    print("✓ 通过\n")

    return True


if __name__ == '__main__':
    try:
        test_measurements()
        print("🎉 恭喜！你已理解量子测量！")
        print("\n关键要点:")
        print("- 测量确定态 (|0⟩ 或 |1⟩) 总是得到确定结果")
        print("- 测量叠加态得到概率性结果")
        print("- 每次测量都会使量子态坍缩")
    except AssertionError as e:
        print(f"❌ 测试失败: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        exit(1)
