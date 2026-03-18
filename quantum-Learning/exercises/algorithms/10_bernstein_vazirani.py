"""
练习 10: Bernstein-Vazirani 算法
==================

目标：找到隐藏的二进制字符串

知识点：
- 问题：给定 Oracle 计算 f(x) = s·x (mod 2)，找到隐藏字符串 s
  其中 s·x 是内积：s₀x₀ ⊕ s₁x₁ ⊕ ... ⊕ sₙ₋₁xₙ₋₁
- 经典：需要 n 次查询
- 量子：只需 1 次查询！

应用：
- 密码学
- 函数性质检测
- 量子学习理论

任务：实现 Bernstein-Vazirani 算法
"""

from qiskit import QuantumCircuit
from qiskit_aer import Aer
import numpy as np


def create_bv_oracle(secret_string):
    """
    创建 Bernstein-Vazirani Oracle

    Oracle 实现 f(x) = s·x (mod 2)

    参数：
        secret_string: 隐藏字符串，例如 '101'

    返回：
        QuantumCircuit: BV Oracle
    """
    n = len(secret_string)
    oracle = QuantumCircuit(n + 1, name='BV_Oracle')

    # TODO: 为 secret_string 中每个为 '1' 的位置应用 CNOT
    # 例如，secret_string='101':
    #   - 位置0是'1'，应用 CNOT(0, n)
    #   - 位置1是'0'，不操作
    #   - 位置2是'1'，应用 CNOT(2, n)

    for i, bit in enumerate(secret_string):
        if bit == '1':
            # TODO: 应用 CNOT，控制量子比特是 i，目标是 n
            pass

    return oracle


def bernstein_vazirani(n, oracle):
    """
    实现 Bernstein-Vazirani 算法

    参数：
        n: 隐藏字符串的长度
        oracle: BV Oracle

    返回：
        QuantumCircuit: 完整算法电路
    """
    qc = QuantumCircuit(n + 1, n)

    # TODO: 实现 BV 算法（与 Deutsch-Jozsa 非常相似！）
    # 步骤1: 准备辅助量子比特为 |1⟩

    # 步骤2: 对所有量子比特应用 H 门

    # 步骤3: 应用 Oracle

    # 步骤4: 对输入量子比特应用 H 门

    # 步骤5: 测量输入量子比特

    return qc


def test_bernstein_vazirani():
    """测试 Bernstein-Vazirani 算法"""
    print("测试 Bernstein-Vazirani 算法\n")
    print("=" * 60)

    test_cases = [
        '1',
        '10',
        '101',
        '1010',
        '11111',
        '10101010',
    ]

    simulator = Aer.get_backend('qasm_simulator')

    for secret in test_cases:
        print(f"\n隐藏字符串: {secret}")

        n = len(secret)
        oracle = create_bv_oracle(secret)
        qc = bernstein_vazirani(n, oracle)

        # 显示电路（仅一次）
        if secret == '101':
            print("\n电路结构:")
            print(qc.draw(output='text'))

        # 运行
        job = simulator.run(qc, shots=100)
        counts = job.result().get_counts()

        print(f"测量结果: {counts}")

        # 检查结果
        # 应该测量到隐藏字符串（注意 Qiskit 的比特顺序是反的）
        expected = secret[::-1]  # 反转字符串

        assert expected in counts, f"应该测量到 {expected}"
        assert counts.get(expected, 0) > 95, f"应该几乎总是得到 {expected}"
        print(f"✓ 成功找到隐藏字符串！")

    return True


def demonstrate_algorithm():
    """演示算法工作原理"""
    print("\n" + "=" * 60)
    print("Bernstein-Vazirani 算法原理")
    print("=" * 60)

    print("""
问题设定：
- 有一个黑箱函数 f(x) = s·x (mod 2)
- s 是长度为 n 的隐藏二进制字符串
- 目标：找到 s

经典方法：
- 查询 f(1000...0) 得到 s₀
- 查询 f(0100...0) 得到 s₁
- ...
- 需要 n 次查询

量子方法：
- 准备叠加态 |+⟩^⊗n
- 应用 Oracle（将 s 编码在相位中）
- 应用 H 门提取相位信息
- 测量直接得到 s
- 只需 1 次查询！

数学原理：
H^⊗n Uf H^⊗n |0⟩^⊗n |−⟩ = |s⟩ |−⟩

其中：
- Uf 是 Oracle
- |−⟩ = (|0⟩ - |1⟩)/√2 是辅助量子比特

这个算法完美展示了量子并行性！
    """)


if __name__ == '__main__':
    try:
        test_bernstein_vazirani()
        demonstrate_algorithm()

        print("\n🎉 恭喜！你已掌握 Bernstein-Vazirani 算法！")
        print("\n关键要点:")
        print("- 找隐藏字符串：n 次 → 1 次")
        print("- 量子并行性的优美示例")
        print("- Oracle 将信息编码在相位中")
        print("- Hadamard 门提取相位信息")

    except AssertionError as e:
        print(f"❌ 测试失败: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
