"""
练习 05: 贝尔态（Bell States）
==================

目标：创建量子纠缠态

知识点：
- 量子纠缠是量子力学最神奇的现象之一
- 贝尔态是最简单的纠缠态，由两个量子比特组成
- 四个贝尔态：
  |Φ+⟩ = (|00⟩ + |11⟩)/√2
  |Φ-⟩ = (|00⟩ - |11⟩)/√2
  |Ψ+⟩ = (|01⟩ + |10⟩)/√2
  |Ψ-⟩ = (|01⟩ - |10⟩)/√2

- 纠缠态的特点：测量一个量子比特会立即影响另一个

任务：创建贝尔态并验证纠缠特性
"""

from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
import numpy as np


def create_bell_state():
    """
    创建 |Φ+⟩ = (|00⟩ + |11⟩)/√2 贝尔态

    步骤：
    1. 对第一个量子比特应用 H 门
    2. 使用 CNOT 门连接两个量子比特

    返回：
        QuantumCircuit: 创建贝尔态的电路
    """
    qc = QuantumCircuit(2)

    # TODO: 对第一个量子比特(索引0)应用 Hadamard 门

    # TODO: 应用 CNOT 门，控制量子比特是0，目标量子比特是1
    # 提示：qc.cx(control, target)

    return qc


def create_all_bell_states():
    """
    创建所有四个贝尔态

    返回：
        dict: 包含所有贝尔态电路的字典
    """
    bell_states = {}

    # |Φ+⟩ = (|00⟩ + |11⟩)/√2
    qc_phi_plus = QuantumCircuit(2)
    # TODO: H 门 + CNOT 门


    bell_states['Φ+'] = qc_phi_plus

    # |Φ-⟩ = (|00⟩ - |11⟩)/√2
    qc_phi_minus = QuantumCircuit(2)
    # TODO: 提示：在 |Φ+⟩ 基础上对第一个量子比特加 Z 门


    bell_states['Φ-'] = qc_phi_minus

    # |Ψ+⟩ = (|01⟩ + |10⟩)/√2
    qc_psi_plus = QuantumCircuit(2)
    # TODO: 提示：在 |Φ+⟩ 基础上对第二个量子比特加 X 门


    bell_states['Ψ+'] = qc_psi_plus

    # |Ψ-⟩ = (|01⟩ - |10⟩)/√2
    qc_psi_minus = QuantumCircuit(2)
    # TODO: 组合使用 X 和 Z 门


    bell_states['Ψ-'] = qc_psi_minus

    return bell_states


def test_bell_state():
    """测试贝尔态"""

    print("测试 1: 创建 |Φ+⟩ 贝尔态")
    qc = create_bell_state()
    print(qc.draw(output='text'))

    # 获取状态向量
    state = Statevector.from_instruction(qc)
    print(f"状态向量: {state.data}")

    # 期望的贝尔态: (|00⟩ + |11⟩)/√2 = [1/√2, 0, 0, 1/√2]
    expected = np.array([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)])

    assert np.allclose(state.data, expected), f"状态应该是 |Φ+⟩，但得到 {state.data}"
    print("✓ 贝尔态创建成功！\n")

    # 测试测量相关性
    print("测试 2: 验证测量相关性")
    qc_measure = qc.copy()
    qc_measure.measure_all()

    simulator = Aer.get_backend('qasm_simulator')
    job = simulator.run(qc_measure, shots=1000)
    counts = job.result().get_counts()

    print(f"测量结果: {counts}")

    # 贝尔态应该只测量到 00 和 11，不会出现 01 或 10
    assert '01' not in counts or counts.get('01', 0) < 10, "不应该测量到 |01⟩"
    assert '10' not in counts or counts.get('10', 0) < 10, "不应该测量到 |10⟩"

    total = counts.get('00', 0) + counts.get('11', 0)
    assert total > 980, "应该几乎总是测量到 00 或 11"

    print("✓ 测量相关性验证通过！")
    print("  这证明了两个量子比特是纠缠的：")
    print("  测量第一个比特为0时，第二个必然是0")
    print("  测量第一个比特为1时，第二个必然是1\n")

    return True


def test_all_bell_states():
    """测试所有贝尔态"""
    print("测试 3: 创建所有四个贝尔态")

    bell_states = create_all_bell_states()

    expected_states = {
        'Φ+': np.array([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)]),
        'Φ-': np.array([1/np.sqrt(2), 0, 0, -1/np.sqrt(2)]),
        'Ψ+': np.array([0, 1/np.sqrt(2), 1/np.sqrt(2), 0]),
        'Ψ-': np.array([0, 1/np.sqrt(2), -1/np.sqrt(2), 0]),
    }

    for name, qc in bell_states.items():
        if qc is not None and qc.num_qubits > 0:
            print(f"\n|{name}⟩:")
            print(qc.draw(output='text'))
            state = Statevector.from_instruction(qc)
            print(f"状态: {state.data}")

            # 检查是否是正确的贝尔态（允许全局相位）
            fidelity = np.abs(np.dot(np.conj(state.data), expected_states[name]))
            if fidelity > 0.99:
                print(f"✓ 正确！")
            else:
                print(f"⚠ 请完成 |{name}⟩ 的创建")

    return True


if __name__ == '__main__':
    try:
        test_bell_state()
        test_all_bell_states()

        print("\n🎉 恭喜！你已掌握量子纠缠！")
        print("\n关键要点:")
        print("- 纠缠态无法被分解为单个量子比特的张量积")
        print("- 测量一个量子比特会瞬间影响另一个（无论距离多远）")
        print("- 贝尔态是最大纠缠态")
        print("- Einstein 称之为'鬼魅般的超距作用'")

    except AssertionError as e:
        print(f"❌ 测试失败: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
