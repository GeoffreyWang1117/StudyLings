"""
练习 16: Shor 9-qubit 码
==================

目标：理解同时纠正比特翻转和相位翻转错误的码

知识点：
- Shor 码使用 9 个量子比特编码 1 个逻辑量子比特
- 可以同时纠正一个 X 错误或一个 Z 错误
- 结合了比特翻转码和相位翻转码的思想

编码结构：
- 外层：相位翻转码（3 个逻辑量子比特）
- 内层：每个逻辑量子比特用比特翻转码保护（3 个物理量子比特）

任务：理解 Shor 码的结构
"""

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np


def encode_shor_code(qc):
    """
    编码到 Shor 9-qubit 码

    |0⟩_L → (|000⟩ + |111⟩)(|000⟩ + |111⟩)(|000⟩ + |111⟩) / 2√2
    |1⟩_L → (|000⟩ - |111⟩)(|000⟩ - |111⟩)(|000⟩ - |111⟩) / 2√2

    参数：
        qc: 9量子比特电路
    """
    # TODO: 实现 Shor 编码
    # 步骤 1: 相位翻转编码（外层）
    # qc.cx(0, 3)
    # qc.cx(0, 6)

    # 步骤 2: 对每组 3 个量子比特进行比特翻转编码（内层）
    # 第一组
    # qc.h(0); qc.cx(0, 1); qc.cx(0, 2); qc.h([0, 1, 2])
    # 第二组
    # qc.h(3); qc.cx(3, 4); qc.cx(3, 5); qc.h([3, 4, 5])
    # 第三组
    # qc.h(6); qc.cx(6, 7); qc.cx(6, 8); qc.h([6, 7, 8])

    pass


def test_shor_code():
    """测试 Shor 码"""
    print("测试 Shor 9-qubit 码\n")
    print("=" * 60)

    qc = QuantumCircuit(9)

    # 准备 |+⟩ 态
    qc.h(0)

    print("初始态: |+⟩ = (|0⟩ + |1⟩)/√2\n")

    # 编码
    encode_shor_code(qc)

    print("电路图:")
    print(qc.draw(output='text'))

    # 获取状态
    state = Statevector.from_instruction(qc)

    print(f"\n编码后的状态复杂度: {len(state.data)} 维")
    print("（9 个量子比特 = 2^9 = 512 维希尔伯特空间）")

    print("\n✓ Shor 码是第一个通用量子纠错码")

    return True


def explain_shor_code():
    """解释 Shor 码"""
    print("\n" + "=" * 60)
    print("Shor 码详解")
    print("=" * 60)

    print("""
Shor 码的创新：

  问题：
    - 比特翻转码：只纠正 X 错误
    - 相位翻转码：只纠正 Z 错误
    - 需要：同时纠正两种错误

  Shor 的方案（级联码）：

    1. 用相位翻转码保护（需要 3 个"逻辑"量子比特）
    2. 用比特翻转码保护每个"逻辑"量子比特（每个需要 3 个物理量子比特）
    3. 总共：3 × 3 = 9 个物理量子比特

  编码示例：

    |0⟩_L → (|000⟩ + |111⟩) ⊗ (|000⟩ + |111⟩) ⊗ (|000⟩ + |111⟩) / 2√2

  这个态同时受到：
    - X 保护：任何一组内的比特翻转可被检测
    - Z 保护：任何一组间的相位翻转可被检测

性能：

  ✓ 可以纠正任意单量子比特错误
  ✓ X, Y, Z 错误都可以纠正
    （Y = iXZ，可以分解）

  代价：
    - 9 个物理量子比特 → 1 个逻辑量子比特
    - 编码率：1/9 ≈ 11%

改进：

  - Steane 7-qubit 码：7:1（更高效）
  - 完美 5-qubit 码：5:1（最优）
  - CSS 码：通用构造方法

历史意义：

  1995 年，Peter Shor 证明：
    ✓ 量子纠错是可能的
    ✓ 容错量子计算是可行的
    ✓ 开启了量子纠错理论的研究

  这个发现拯救了量子计算领域！
    """)


if __name__ == '__main__':
    try:
        test_shor_code()
        explain_shor_code()

        print("\n🎉 恭喜！你已理解 Shor 码！")
        print("\n关键要点:")
        print("- 级联编码：外层 + 内层")
        print("- 同时纠正 X 和 Z 错误")
        print("- 第一个通用量子纠错码")
        print("- 量子纠错的里程碑")

    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
