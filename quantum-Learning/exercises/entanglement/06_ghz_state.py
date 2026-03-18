"""
练习 06: GHZ 态（多量子比特纠缠）
==================

目标：创建多量子比特纠缠态

知识点：
- GHZ 态是 Greenberger-Horne-Zeilinger 态的缩写
- 是贝尔态在多量子比特的推广
- 3量子比特 GHZ 态: |GHZ⟩ = (|000⟩ + |111⟩)/√2
- n量子比特 GHZ 态: |GHZ_n⟩ = (|0...0⟩ + |1...1⟩)/√2
- GHZ 态展示了多方量子纠缠的非经典特性

应用：
- 量子通信协议
- 量子密钥分发
- 测试量子力学基础（Bell不等式的推广）

任务：创建和验证 GHZ 态
"""

from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
import numpy as np


def create_ghz_3():
    """
    创建3量子比特 GHZ 态
    |GHZ⟩ = (|000⟩ + |111⟩)/√2

    步骤：
    1. 对第一个量子比特应用 H 门
    2. 对第一个和第二个量子比特应用 CNOT
    3. 对第二个和第三个量子比特应用 CNOT

    返回：
        QuantumCircuit: GHZ态电路
    """
    qc = QuantumCircuit(3)

    # TODO: 实现 GHZ 态
    # 提示：H(0), CNOT(0,1), CNOT(1,2)

    return qc


def create_ghz_n(n):
    """
    创建 n 量子比特 GHZ 态

    参数：
        n: 量子比特数量

    返回：
        QuantumCircuit: n量子比特GHZ态电路
    """
    qc = QuantumCircuit(n)

    # TODO: 推广到 n 量子比特
    # 提示：
    # 1. H 门作用在第0个量子比特
    # 2. CNOT 链：0->1->2->...->n-1

    return qc


def test_ghz_3():
    """测试3量子比特GHZ态"""
    print("测试 1: 创建3量子比特 GHZ 态")

    qc = create_ghz_3()
    print(qc.draw(output='text'))

    # 验证状态向量
    state = Statevector.from_instruction(qc)
    print(f"\n状态向量: {state.data}")

    # 期望: |000⟩ 和 |111⟩ 的叠加
    # 基底顺序: |000⟩, |001⟩, |010⟩, |011⟩, |100⟩, |101⟩, |110⟩, |111⟩
    expected = np.zeros(8, dtype=complex)
    expected[0] = 1/np.sqrt(2)  # |000⟩
    expected[7] = 1/np.sqrt(2)  # |111⟩

    assert np.allclose(state.data, expected), f"应该是 GHZ 态，但得到 {state.data}"
    print("✓ GHZ 态创建成功！\n")

    return True


def test_ghz_measurement():
    """测试GHZ态的测量特性"""
    print("测试 2: GHZ 态的测量相关性")

    qc = create_ghz_3()
    qc.measure_all()

    simulator = Aer.get_backend('qasm_simulator')
    job = simulator.run(qc, shots=1000)
    counts = job.result().get_counts()

    print(f"测量结果: {counts}")

    # GHZ态应该只测量到 000 和 111
    valid_outcomes = counts.get('000', 0) + counts.get('111', 0)
    assert valid_outcomes > 980, "应该几乎总是测量到 000 或 111"

    # 不应该出现混合结果（如 001, 010, 100 等）
    for outcome in ['001', '010', '011', '100', '101', '110']:
        assert counts.get(outcome, 0) < 20, f"不应该频繁测量到 {outcome}"

    print("✓ 测量相关性验证通过！")
    print("  三个量子比特完全关联：")
    print("  要么全是0，要么全是1\n")

    return True


def test_ghz_n():
    """测试n量子比特GHZ态"""
    print("测试 3: 创建不同大小的 GHZ 态")

    for n in [2, 4, 5]:
        qc = create_ghz_n(n)

        if qc is not None and qc.num_qubits == n:
            print(f"\n{n}-qubit GHZ 态:")
            print(qc.draw(output='text'))

            state = Statevector.from_instruction(qc)

            # 检查只有 |0...0⟩ 和 |1...1⟩ 有振幅
            expected_amplitude = 1/np.sqrt(2)

            # |0...0⟩ 是第0个基态
            assert np.isclose(abs(state.data[0]), expected_amplitude), \
                f"{n}-qubit: |0...0⟩ 振幅应为 1/√2"

            # |1...1⟩ 是最后一个基态
            assert np.isclose(abs(state.data[-1]), expected_amplitude), \
                f"{n}-qubit: |1...1⟩ 振幅应为 1/√2"

            # 其他态的振幅应接近0
            for i in range(1, len(state.data) - 1):
                assert np.isclose(abs(state.data[i]), 0, atol=1e-10), \
                    f"{n}-qubit: 中间态 {i} 振幅应为 0"

            print(f"✓ {n}-qubit GHZ 态正确！")

    return True


if __name__ == '__main__':
    try:
        test_ghz_3()
        test_ghz_measurement()
        test_ghz_n()

        print("\n🎉 恭喜！你已掌握多量子比特纠缠！")
        print("\n关键要点:")
        print("- GHZ 态是多方纠缠态")
        print("- 所有量子比特都是关联的")
        print("- 测量任何一个量子比特都会影响所有其他量子比特")
        print("- GHZ 态用于测试量子非局域性")
        print("\n有趣的事实:")
        print("GHZ 态违反了经典直觉，展示了量子力学的'怪异性'")

    except AssertionError as e:
        print(f"❌ 测试失败: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
