"""
练习 04: 基本量子门
==================

目标：掌握单量子比特的基本量子门

知识点：
- X 门（泡利-X）：量子 NOT 门，|0⟩ ↔ |1⟩
- Y 门（泡利-Y）：绕 Y 轴旋转 π
- Z 门（泡利-Z）：相位翻转，|1⟩ → -|1⟩
- H 门（Hadamard）：创建叠加态
- S 门：相位门，π/2 相位
- T 门：π/4 相位门

矩阵表示：
X = [[0, 1],   Y = [[0, -i],  Z = [[1,  0],   H = 1/√2 * [[1,  1],
     [1, 0]]        [i,  0]]        [0, -1]]               [1, -1]]

任务：使用不同的量子门来操控量子比特
"""

from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
import numpy as np


def apply_x_gate():
    """
    应用 X 门将 |0⟩ 翻转为 |1⟩

    返回：
        QuantumCircuit: 应用了 X 门的电路
    """
    qc = QuantumCircuit(1)

    # TODO: 应用 X 门
    # 提示：qc.x(0)

    return qc


def apply_z_gate():
    """
    应用 Z 门到叠加态
    Z(H|0⟩) = Z((|0⟩ + |1⟩)/√2) = (|0⟩ - |1⟩)/√2

    返回：
        QuantumCircuit: 应用了 H 和 Z 门的电路
    """
    qc = QuantumCircuit(1)

    # TODO: 先应用 H 门创建叠加态

    # TODO: 再应用 Z 门改变相位
    # 提示：qc.z(0)

    return qc


def create_minus_state():
    """
    创建 |- ⟩ = (|0⟩ - |1⟩)/√2 态
    方法1: H 然后 Z
    方法2: X 然后 H

    返回：
        QuantumCircuit: 创建 |- ⟩ 态的电路
    """
    qc = QuantumCircuit(1)

    # TODO: 使用量子门创建 |- ⟩ 态
    # 提示：可以用 X 门然后 H 门

    return qc


def rotation_sequence():
    """
    应用一系列旋转门
    探索：XYZ = ?

    返回：
        QuantumCircuit: 应用了 X, Y, Z 序列的电路
    """
    qc = QuantumCircuit(1)

    # TODO: 依次应用 X, Y, Z 门
    # qc.x(0)
    # qc.y(0)
    # qc.z(0)

    return qc


def test_gates():
    """测试所有门操作"""

    # 测试1: X 门
    print("测试 1: X 门 (量子 NOT)")
    qc_x = apply_x_gate()
    print(qc_x.draw(output='text'))

    state_x = Statevector.from_instruction(qc_x)
    expected = Statevector([0, 1])  # |1⟩

    assert np.allclose(state_x.data, expected.data), "X 门应将 |0⟩ 变为 |1⟩"
    print(f"状态: {state_x.data}")
    print("✓ 通过\n")

    # 测试2: Z 门
    print("测试 2: Z 门 (相位翻转)")
    qc_z = apply_z_gate()
    print(qc_z.draw(output='text'))

    state_z = Statevector.from_instruction(qc_z)
    # HZ|0⟩ = H(Z(H|0⟩)) = (|0⟩ - |1⟩)/√2 的某个全局相位
    print(f"状态: {state_z.data}")
    print("✓ 通过\n")

    # 测试3: |- ⟩ 态
    print("测试 3: 创建 |- ⟩ 态")
    qc_minus = create_minus_state()
    print(qc_minus.draw(output='text'))

    state_minus = Statevector.from_instruction(qc_minus)
    expected_minus = Statevector([1/np.sqrt(2), -1/np.sqrt(2)])  # (|0⟩ - |1⟩)/√2

    # 检查是否相等（忽略全局相位）
    fidelity = np.abs(np.dot(np.conj(state_minus.data), expected_minus.data))
    assert np.isclose(fidelity, 1.0), f"状态应该是 |- ⟩，保真度: {fidelity}"
    print(f"状态: {state_minus.data}")
    print("✓ 通过\n")

    # 测试4: 门序列
    print("测试 4: XYZ 序列")
    qc_seq = rotation_sequence()
    print(qc_seq.draw(output='text'))

    state_seq = Statevector.from_instruction(qc_seq)
    print(f"最终状态: {state_seq.data}")
    print("✓ 通过\n")

    return True


if __name__ == '__main__':
    try:
        test_gates()
        print("🎉 恭喜！你已掌握基本量子门！")
        print("\n关键要点:")
        print("- X, Y, Z 是泡利门，它们是厄米的且平方为单位矩阵")
        print("- H 门创建叠加态，它是自己的逆")
        print("- 量子门是可逆的（酉矩阵）")
        print("- 门的组合可以创建复杂的量子态")
    except AssertionError as e:
        print(f"❌ 测试失败: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
