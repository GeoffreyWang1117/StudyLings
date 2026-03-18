"""
练习 15: 相位翻转码
==================

目标：纠正相位翻转错误

知识点：
- 相位翻转错误：Z 错误，|+⟩ → |-⟩
- 在 X 基（Hadamard 基）中工作
- 结构类似比特翻转码，但在不同的基中

编码：
- |+⟩_L → |+++⟩
- |-⟩_L → |---⟩

原理：
- 在 Z 基中的比特翻转 = 在 X 基中的相位翻转
- 通过基变换将相位翻转转化为比特翻转

任务：实现相位翻转码
"""

from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.quantum_info import Statevector
import numpy as np


def encode_phase_flip(qc, data_qubit):
    """
    编码到相位翻转码

    |+⟩ → |+++⟩
    |-⟩ → |---⟩

    参数：
        qc: 量子电路
        data_qubit: 数据量子比特索引
    """
    # TODO: 实现编码
    # 策略：
    # 1. 转换到 X 基（应用 H 门）
    # 2. 进行"比特翻转编码"（CNOT）
    # 3. 转换回 Z 基（应用 H 门）

    # 步骤 1: H 门变换到 X 基


    # 步骤 2: CNOT 编码



    # 步骤 3: H 门变换回 Z 基




def detect_phase_flip(qc):
    """
    检测相位翻转错误

    在 X 基中测量 syndrome

    参数：
        qc: 量子电路
    """
    # TODO: 检测相位错误
    # 策略：转换到 X 基，检测"比特翻转"

    # 转换到 X 基



    # 测量 syndrome（比较量子比特）
    # 使用辅助量子比特进行奇偶检查

    # 这里简化：我们只演示原理


def create_phase_flip_circuit():
    """
    创建相位翻转码演示电路

    返回：
        QuantumCircuit: 相位翻转码电路
    """
    qc = QuantumCircuit(3, name='Phase_Flip_Code')

    # 准备初始态 |+⟩
    qc.h(0)

    qc.barrier(label='初始态 |+⟩')

    # TODO: 编码
    encode_phase_flip(qc, 0)

    qc.barrier(label='编码完成')

    # 引入相位翻转错误（Z 门）
    qc.z(1)

    qc.barrier(label='相位错误')

    # 解码前转换到 X 基检测
    qc.h([0, 1, 2])

    return qc


def test_phase_flip_code():
    """测试相位翻转码"""
    print("测试相位翻转码\n")
    print("=" * 60)

    qc = create_phase_flip_circuit()

    print("电路图:")
    print(qc.draw(output='text'))

    # 获取状态向量
    state = Statevector.from_instruction(qc)

    print(f"\n状态向量:")
    for i, amp in enumerate(state.data):
        if abs(amp) > 0.01:
            print(f"  |{i:03b}⟩: {amp.real:+.4f} {amp.imag:+.4f}j")

    print("\n✓ 相位翻转码电路创建成功")

    return True


def demonstrate_phase_vs_bit_flip():
    """演示相位翻转和比特翻转的关系"""
    print("\n" + "=" * 60)
    print("相位翻转 vs 比特翻转")
    print("=" * 60)

    print("""
基变换的威力：

  Z 基（计算基）：
    - 比特翻转：X 错误
    - |0⟩ →X→ |1⟩

  X 基（Hadamard 基）：
    - 相位翻转：Z 错误
    - |+⟩ →Z→ |-⟩

  关键观察：
    H Z H = X

  即：在 X 基中，Z 错误看起来像 X 错误！

相位翻转码的策略：

  1. 变换到 X 基（应用 H）
  2. 使用比特翻转码的技术
  3. 变换回 Z 基

  编码：
    |+⟩ →(H)→ |0⟩ →(编码)→ |000⟩ →(H⊗3)→ |+++⟩

  在 |+++⟩ 上的 Z 错误：
    Z|+⟩ = |-⟩

    所以 Z 错误在第 i 个量子比特上会产生 |++- ...⟩

  检测：
    变换到 X 基，检测"比特翻转"

示例：

  无错误：
    |+++⟩ →(H⊗3)→ |000⟩

  q[1] 上有 Z 错误：
    |+\u2212+⟩ →(H⊗3)→ |010⟩

  syndrome 检测到差异！
    """)

    # 演示代码
    print("\n实际演示：")

    qc1 = QuantumCircuit(3)
    qc1.h([0, 1, 2])  # |+++⟩
    print("\n无错误： |+++⟩")
    state1 = Statevector.from_instruction(qc1)
    qc1.h([0, 1, 2])  # 变回 Z 基
    state1_z = Statevector.from_instruction(qc1)
    print(f"Z 基中: {state1_z.data}")

    qc2 = QuantumCircuit(3)
    qc2.h([0, 1, 2])  # |+++⟩
    qc2.z(1)          # Z 错误在 q[1]
    print("\nZ 错误在 q[1]： |+\u2212+⟩")
    state2 = Statevector.from_instruction(qc2)
    qc2.h([0, 1, 2])  # 变回 Z 基
    state2_z = Statevector.from_instruction(qc2)
    print(f"Z 基中: {state2_z.data}")

    print("\n差异清晰可见！")


def explain_phase_flip_code():
    """解释相位翻转码"""
    print("\n" + "=" * 60)
    print("相位翻转码原理")
    print("=" * 60)

    print("""
为什么需要相位翻转码？

  实际量子系统的错误：
    - 比特翻转错误（X 错误）：振幅阻尼
    - 相位翻转错误（Z 错误）：相位阻尼
    - 两者都可能发生！

相位错误的物理来源：

  1. 环境耦合
     - 量子比特与环境的相互作用
     - 导致相位信息丢失

  2. 控制错误
     - 门操作的不完美实现
     - 过度/不足旋转

编码方案：

  |ψ⟩ = α|+⟩ + β|-⟩

  编码后：
    α|+++⟩ + β|---⟩

  单个 Z 错误：
    α|+\u2212+⟩ + β|-+-⟩

  仍然可以通过多数投票纠正！

完整性：

  比特翻转码 + 相位翻转码 = ?

  还不够！需要同时纠正两种错误。

  解决方案：
    - Shor 9-qubit 码
    - Steane 7-qubit 码
    - CSS 码族

练习思考：

  Q: 为什么不能简单地组合两个码？
  A: 需要同时保护 X 和 Z 错误，需要特殊设计

  Q: 3 个量子比特够用吗？
  A: 不够！纠正任意错误至少需要 5 个量子比特
     （量子 Hamming 界）
    """)


if __name__ == '__main__':
    try:
        test_phase_flip_code()
        demonstrate_phase_vs_bit_flip()
        explain_phase_flip_code()

        print("\n🎉 恭喜！你已掌握相位翻转码！")
        print("\n关键要点:")
        print("- 相位错误 = X基中的比特翻转")
        print("- 基变换是强大的工具")
        print("- 需要同时保护 X 和 Z 错误")
        print("- 通往更高级纠错码的道路")

    except AssertionError as e:
        print(f"❌ 测试失败: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
