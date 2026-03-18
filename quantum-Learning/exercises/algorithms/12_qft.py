"""
练习 12: 量子傅立叶变换 (QFT)
==================

目标：实现量子傅立叶变换

知识点：
- QFT 是许多量子算法的核心组件
- 是经典离散傅立叶变换 (DFT) 的量子版本
- Shor 算法、相位估计等都依赖 QFT
- 复杂度：经典 FFT 是 O(N log N)，QFT 是 O((log N)²)

QFT 定义：
  |j⟩ → (1/√N) Σ_{k=0}^{N-1} e^{2πijk/N} |k⟩

应用：
- Shor 因数分解算法
- 量子相位估计
- 周期查找

任务：实现量子傅立叶变换
"""

from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
import numpy as np
import math


def qft_rotations(circuit, n):
    """
    对 n 个量子比特应用 QFT 旋转

    参数：
        circuit: 量子电路
        n: 量子比特索引（从 n-1 到 0 递归）
    """
    if n == 0:
        return circuit

    n -= 1

    # TODO: 应用 Hadamard 门到量子比特 n
    # circuit.h(n)

    # TODO: 应用受控旋转门
    # 对于 j 从 0 到 n-1:
    #   应用 CP(π/2^(n-j)) 门，控制=j，目标=n
    # 提示：circuit.cp(angle, control, target)

    for qubit in range(n):
        # 计算旋转角度
        angle = np.pi / (2 ** (n - qubit))
        # TODO: 应用受控相位门
        # circuit.cp(angle, qubit, n)
        pass

    # 递归调用
    qft_rotations(circuit, n)


def swap_registers(circuit, n):
    """
    反转量子比特顺序（Qiskit 的约定）

    参数：
        circuit: 量子电路
        n: 量子比特数量
    """
    # TODO: 交换量子比特顺序
    # 提示：for i in range(n//2): circuit.swap(i, n-i-1)

    for i in range(n // 2):
        # TODO: 交换 i 和 n-i-1
        # circuit.swap(i, n - i - 1)
        pass


def create_qft(n):
    """
    创建 n 量子比特的 QFT 电路

    参数：
        n: 量子比特数量

    返回：
        QuantumCircuit: QFT 电路
    """
    qc = QuantumCircuit(n, name='QFT')

    # TODO: 应用 QFT 旋转
    # qft_rotations(qc, n)

    # TODO: 交换量子比特
    # swap_registers(qc, n)

    return qc


def create_inverse_qft(n):
    """
    创建逆 QFT 电路

    参数：
        n: 量子比特数量

    返回：
        QuantumCircuit: 逆 QFT 电路
    """
    qft = create_qft(n)
    # 逆 QFT 就是 QFT 的逆电路
    inverse_qft = qft.inverse()
    inverse_qft.name = 'QFT†'
    return inverse_qft


def test_qft():
    """测试 QFT"""
    print("测试量子傅立叶变换\n")
    print("=" * 60)

    # 测试 1: 3 量子比特 QFT
    print("测试 1: 3-qubit QFT")
    n = 3
    qc = QuantumCircuit(n)

    # 准备初始态 |1⟩
    qc.x(0)

    # 应用 QFT
    qft = create_qft(n)
    qc.compose(qft, inplace=True)

    print("\n电路图:")
    print(qc.draw(output='text'))

    # 获取状态向量
    state = Statevector.from_instruction(qc)
    print(f"\nQFT|1⟩ 的状态向量:")
    for i, amp in enumerate(state.data):
        if abs(amp) > 0.01:
            print(f"  |{i:03b}⟩: {amp:.4f}")

    print("✓ QFT 执行成功")

    # 测试 2: QFT 和逆 QFT
    print("\n" + "=" * 60)
    print("测试 2: QFT 和逆 QFT 应该相互抵消")

    qc2 = QuantumCircuit(n)
    qc2.x(0)  # |1⟩
    qc2.h(1)  # 部分叠加

    initial_state = Statevector.from_instruction(qc2)

    # 应用 QFT 然后逆 QFT
    qft = create_qft(n)
    qft_inv = create_inverse_qft(n)

    qc2.compose(qft, inplace=True)
    qc2.compose(qft_inv, inplace=True)

    final_state = Statevector.from_instruction(qc2)

    # 计算保真度
    fidelity = abs(np.dot(np.conj(initial_state.data), final_state.data))
    print(f"初始态和最终态的保真度: {fidelity:.6f}")

    assert fidelity > 0.999, f"QFT 和逆 QFT 应该抵消，保真度: {fidelity}"

    print("✓ QFT 和逆 QFT 正确抵消")

    return True


def explain_qft():
    """解释 QFT"""
    print("\n" + "=" * 60)
    print("量子傅立叶变换原理")
    print("=" * 60)

    print("""
QFT 的作用：
  将计算基态映射到傅立叶基态

  |j⟩ → (1/√N) Σ_{k=0}^{N-1} e^{2πijk/N} |k⟩

电路结构：
  1. 对每个量子比特：
     a. 应用 Hadamard 门
     b. 应用一系列受控相位旋转
  2. 反转量子比特顺序

示例 (n=3):
  - H 门 + CP(π/2), CP(π/4) 在 qubit 2
  - H 门 + CP(π/2) 在 qubit 1
  - H 门在 qubit 0
  - SWAP 门交换顺序

为什么 QFT 重要？

  1. Shor 算法的核心
     - 用于找到函数的周期
     - 将周期信息编码在相位中

  2. 量子相位估计
     - 估计酉算子的本征值
     - 许多算法的基础

  3. 指数级加速
     - 经典 FFT: O(N log N)
     - QFT: O((log N)²) 门操作
     - 注意：测量会破坏叠加，不能直接提取所有傅立叶系数

数学细节：
  对于 n 量子比特，N = 2^n

  QFT|j⟩ = (1/√N) Σ_{k=0}^{N-1} ω^{jk} |k⟩

  其中 ω = e^{2πi/N} 是 N 次单位根

  可以写成张量积形式：
  QFT|j⟩ = ⊗_{k=1}^n (|0⟩ + e^{2πi j/2^k}|1⟩) / √2

历史：
  - 量子傅立叶变换由 Don Coppersmith 提出
  - 是 Shor 算法 (1994) 的关键组件
  - 开启了量子算法的新纪元
    """)


if __name__ == '__main__':
    try:
        test_qft()
        explain_qft()

        print("\n🎉 恭喜！你已掌握量子傅立叶变换！")
        print("\n关键要点:")
        print("- QFT 是经典 DFT 的量子版本")
        print("- 使用 Hadamard 门和受控相位门")
        print("- Shor 算法等的核心组件")
        print("- 展示了量子计算的指数级优势")

    except AssertionError as e:
        print(f"❌ 测试失败: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
