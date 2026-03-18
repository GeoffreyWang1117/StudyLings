"""
练习 01: 量子比特基础
==================

目标：理解量子比特的概念并创建你的第一个量子电路

知识点：
- 量子比特（Qubit）是量子计算的基本单位
- 经典比特只能是 0 或 1，但量子比特可以处于叠加态
- 量子态用 |0⟩ 和 |1⟩ 表示（Dirac 记号）

任务：创建一个包含 1 个量子比特的量子电路
"""

from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib
matplotlib.use('Agg')  # 非GUI后端


def create_single_qubit_circuit():
    """
    创建一个单量子比特电路

    返回：
        QuantumCircuit: 包含1个量子比特的电路
    """
    # TODO: 创建一个包含 1 个量子比特的量子电路
    # 提示：使用 QuantumCircuit(n) 其中 n 是量子比特数量
    qc = None  # 替换这一行

    return qc


def test_circuit():
    """测试你的电路"""
    qc = create_single_qubit_circuit()

    # 检查电路是否正确创建
    assert qc is not None, "电路不能为 None"
    assert isinstance(qc, QuantumCircuit), "必须返回 QuantumCircuit 对象"
    assert qc.num_qubits == 1, f"电路应该有 1 个量子比特，但有 {qc.num_qubits} 个"

    print("✓ 电路创建成功！")
    print(f"  量子比特数量: {qc.num_qubits}")
    print("\n电路图:")
    print(qc.draw(output='text'))

    return True


if __name__ == '__main__':
    try:
        test_circuit()
        print("\n🎉 恭喜！你已完成第一个练习！")
        print("量子比特默认初始化为 |0⟩ 态。")
    except AssertionError as e:
        print(f"❌ 测试失败: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        exit(1)
