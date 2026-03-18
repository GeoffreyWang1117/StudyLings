"""
练习 02: 量子叠加态
==================

目标：使用 Hadamard 门创建叠加态

知识点：
- Hadamard 门 (H) 是最重要的量子门之一
- H|0⟩ = (|0⟩ + |1⟩)/√2  （等概率叠加）
- H|1⟩ = (|0⟩ - |1⟩)/√2
- 叠加态意味着量子比特同时处于多个状态

任务：创建一个量子电路，将量子比特置于叠加态
"""

from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib
matplotlib.use('Agg')


def create_superposition():
    """
    创建一个处于叠加态的量子比特

    返回：
        QuantumCircuit: 包含叠加态的电路
    """
    # TODO: 创建一个量子电路
    qc = QuantumCircuit(1, 1)  # 1个量子比特，1个经典比特

    # TODO: 对量子比特应用 Hadamard 门
    # 提示：使用 qc.h(qubit_index)
    # 你的代码在这里

    # 添加测量以便我们能看到结果
    qc.measure(0, 0)

    return qc


def test_superposition():
    """测试叠加态"""
    qc = create_superposition()

    # 检查电路
    assert qc.num_qubits == 1, "应该有1个量子比特"

    # 运行电路
    simulator = Aer.get_backend('qasm_simulator')
    job = simulator.run(qc, shots=1000)
    result = job.result()
    counts = result.get_counts(qc)

    print("测量结果:", counts)
    print("\n电路图:")
    print(qc.draw(output='text'))

    # 检查结果：应该大约各占50%
    if '0' in counts and '1' in counts:
        ratio_0 = counts.get('0', 0) / 1000
        ratio_1 = counts.get('1', 0) / 1000

        # 允许一定的统计误差
        assert 0.4 < ratio_0 < 0.6, f"测量到 |0⟩ 的概率应该约为50%，实际为 {ratio_0*100:.1f}%"
        assert 0.4 < ratio_1 < 0.6, f"测量到 |1⟩ 的概率应该约为50%，实际为 {ratio_1*100:.1f}%"

        print("\n✓ 叠加态创建成功！")
        print(f"  |0⟩: {ratio_0*100:.1f}%")
        print(f"  |1⟩: {ratio_1*100:.1f}%")
        return True
    else:
        raise AssertionError("结果应该同时包含 0 和 1。你是否忘记应用 Hadamard 门？")


if __name__ == '__main__':
    try:
        test_superposition()
        print("\n🎉 恭喜！你已掌握量子叠加态！")
        print("这是量子计算区别于经典计算的关键特性之一。")
    except AssertionError as e:
        print(f"❌ 测试失败: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        exit(1)
