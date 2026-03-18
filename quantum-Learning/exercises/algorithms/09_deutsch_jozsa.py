"""
练习 09: Deutsch-Jozsa 算法
==================

目标：实现 Deutsch 算法的多量子比特推广

知识点：
- Deutsch-Jozsa 算法是 Deutsch 算法的推广
- 问题：判断 f:{0,1}^n → {0,1} 是常数还是平衡的
  * 常数：所有输入返回相同值（全0或全1）
  * 平衡：恰好一半输入返回0，一半返回1
- 经典最坏情况：需要 2^(n-1) + 1 次查询
- 量子：只需 1 次查询！

量子优势：
- n=3: 经典最坏5次 vs 量子1次
- n=10: 经典最坏513次 vs 量子1次
- 指数级加速！

任务：实现 Deutsch-Jozsa 算法
"""

from qiskit import QuantumCircuit
from qiskit_aer import Aer
import numpy as np


def create_constant_oracle(n, output=0):
    """
    创建常数 Oracle

    参数：
        n: 输入量子比特数
        output: 0 或 1

    返回：
        QuantumCircuit: Oracle
    """
    oracle = QuantumCircuit(n + 1, name=f'Const_{output}')

    if output == 1:
        # f(x) = 1 对所有 x
        oracle.x(n)  # 翻转辅助量子比特

    return oracle


def create_balanced_oracle(n):
    """
    创建平衡 Oracle
    实现：f(x) = x0 (取第一个比特)

    参数：
        n: 输入量子比特数

    返回：
        QuantumCircuit: Oracle
    """
    oracle = QuantumCircuit(n + 1, name='Balanced')

    # TODO: 创建平衡 Oracle
    # 提示：CNOT from 第0个量子比特 to 第n个量子比特（辅助位）

    return oracle


def deutsch_jozsa(n, oracle):
    """
    实现 Deutsch-Jozsa 算法

    参数：
        n: 输入量子比特数
        oracle: Oracle 电路

    返回：
        QuantumCircuit: 完整算法电路
    """
    qc = QuantumCircuit(n + 1, n)

    # 步骤1: 准备辅助量子比特为 |1⟩
    # TODO: 对第n个量子比特应用 X 门

    # 步骤2: 对所有量子比特应用 H 门
    # TODO: 使用循环或 qc.h(range(n+1))

    qc.barrier()

    # 步骤3: 应用 Oracle
    qc.compose(oracle, inplace=True)

    qc.barrier()

    # 步骤4: 对输入量子比特应用 H 门
    # TODO: 对前 n 个量子比特应用 H 门

    # 步骤5: 测量前 n 个量子比特
    qc.measure(range(n), range(n))

    return qc


def test_deutsch_jozsa():
    """测试 Deutsch-Jozsa 算法"""
    print("测试 Deutsch-Jozsa 算法\n")
    print("=" * 60)

    test_cases = [
        (3, 'constant_0'),
        (3, 'constant_1'),
        (3, 'balanced'),
        (4, 'balanced'),
        (5, 'balanced'),
    ]

    simulator = Aer.get_backend('qasm_simulator')

    for n, oracle_type in test_cases:
        print(f"\nn={n}, Oracle类型: {oracle_type}")

        # 创建 Oracle
        if oracle_type == 'constant_0':
            oracle = create_constant_oracle(n, 0)
            expected = 'constant'
        elif oracle_type == 'constant_1':
            oracle = create_constant_oracle(n, 1)
            expected = 'constant'
        else:
            oracle = create_balanced_oracle(n)
            expected = 'balanced'

        # 创建算法电路
        qc = deutsch_jozsa(n, oracle)

        # 显示电路（仅一次）
        if n == 3 and oracle_type == 'constant_0':
            print("\n电路结构:")
            print(qc.draw(output='text'))

        # 运行
        job = simulator.run(qc, shots=100)
        counts = job.result().get_counts()

        print(f"测量结果: {counts}")

        # 检查结果
        all_zero = '0' * n
        if expected == 'constant':
            assert all_zero in counts, "常数函数应该测量到全0"
            assert counts.get(all_zero, 0) > 95, "应该几乎总是全0"
            print(f"✓ 正确识别为常数函数")
        else:
            # 平衡函数应该测量到非全0的结果
            assert all_zero not in counts or counts.get(all_zero, 0) < 5, \
                "平衡函数不应该测量到全0"
            print(f"✓ 正确识别为平衡函数")

    return True


def compare_complexity():
    """比较经典和量子复杂度"""
    print("\n" + "=" * 60)
    print("复杂度比较：经典 vs 量子")
    print("=" * 60)

    print("\n{:>5} | {:>15} | {:>10}".format('n', '经典(最坏)', '量子'))
    print("-" * 40)

    for n in [1, 2, 3, 5, 10, 20]:
        classical = 2**(n-1) + 1
        quantum = 1
        print("{:5d} | {:15d} | {:10d}".format(n, classical, quantum))

    print("""
结论：
- 经典复杂度：O(2^n) - 指数级
- 量子复杂度：O(1) - 常数！
- 这是量子计算最早的指数级加速示例

注意：
虽然有指数加速，但这是一个人工构造的问题。
Deutsch-Jozsa 主要是理论意义，证明量子优势的存在。
    """)


if __name__ == '__main__':
    try:
        test_deutsch_jozsa()
        compare_complexity()

        print("\n🎉 恭喜！你已掌握 Deutsch-Jozsa 算法！")
        print("\n关键要点:")
        print("- Deutsch 算法的多量子比特推广")
        print("- 展示了指数级量子加速")
        print("- 量子并行性的经典例子")
        print("- 启发了更多量子算法的发展")

    except AssertionError as e:
        print(f"❌ 测试失败: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
