"""
练习 08: Deutsch 算法
==================

目标：实现第一个展示量子优势的算法

知识点：
- Deutsch 算法是第一个证明量子计算机可以比经典计算机更快的算法
- 问题：判断一个布尔函数 f:{0,1}→{0,1} 是常数还是平衡的
  * 常数函数：f(0)=f(1)
  * 平衡函数：f(0)≠f(1)
- 经典：需要2次查询
- 量子：只需1次查询！

算法步骤：
1. 准备 |01⟩ 态
2. 对两个量子比特应用 H 门
3. 应用 Oracle Uf
4. 对第一个量子比特应用 H 门
5. 测量第一个量子比特：0=常数，1=平衡

任务：实现 Deutsch 算法
"""

from qiskit import QuantumCircuit
from qiskit_aer import Aer
import numpy as np


def deutsch_oracle(function_type):
    """
    创建 Deutsch 算法的 Oracle

    参数：
        function_type: 'constant_0', 'constant_1', 'balanced_x', 'balanced_xnot'

    返回：
        QuantumCircuit: Oracle 电路
    """
    oracle = QuantumCircuit(2, name='Oracle')

    if function_type == 'constant_0':
        # f(x) = 0 对所有 x
        # 不需要任何操作
        pass

    elif function_type == 'constant_1':
        # f(x) = 1 对所有 x
        # TODO: 翻转目标量子比特（索引1）


    elif function_type == 'balanced_x':
        # f(x) = x (恒等函数)
        # TODO: CNOT 门，控制=0，目标=1


    elif function_type == 'balanced_xnot':
        # f(x) = NOT x
        # TODO: X 门在控制位，然后 CNOT，然后 X 门在控制位



    return oracle


def deutsch_algorithm(oracle):
    """
    实现 Deutsch 算法

    参数：
        oracle: Oracle 电路

    返回：
        QuantumCircuit: 完整的 Deutsch 算法电路
    """
    qc = QuantumCircuit(2, 1)

    # 步骤1: 准备 |01⟩
    # TODO: 对第二个量子比特应用 X 门


    # 步骤2: 应用 H 门到两个量子比特
    # TODO: qc.h(0) 和 qc.h(1)



    qc.barrier()

    # 步骤3: 应用 Oracle
    qc.compose(oracle, inplace=True)

    qc.barrier()

    # 步骤4: 对第一个量子比特应用 H 门
    # TODO: qc.h(0)


    # 步骤5: 测量第一个量子比特
    qc.measure(0, 0)

    return qc


def test_deutsch():
    """测试 Deutsch 算法"""
    print("测试 Deutsch 算法\n")
    print("=" * 60)

    test_cases = {
        'constant_0': '常数',
        'constant_1': '常数',
        'balanced_x': '平衡',
        'balanced_xnot': '平衡'
    }

    simulator = Aer.get_backend('qasm_simulator')

    for func_type, expected in test_cases.items():
        print(f"\n函数类型: {func_type}")

        oracle = deutsch_oracle(func_type)
        qc = deutsch_algorithm(oracle)

        # 显示电路（仅第一次）
        if func_type == 'constant_0':
            print("\n电路结构:")
            print(qc.draw(output='text'))

        # 运行电路
        job = simulator.run(qc, shots=100)
        counts = job.result().get_counts()

        print(f"测量结果: {counts}")

        # 检查结果
        if expected == '常数':
            assert '0' in counts, f"{func_type} 应该测量到 0（常数）"
            assert counts.get('0', 0) > 95, f"{func_type} 应该几乎总是得到 0"
            print(f"✓ 正确识别为常数函数")
        else:  # 平衡
            assert '1' in counts, f"{func_type} 应该测量到 1（平衡）"
            assert counts.get('1', 0) > 95, f"{func_type} 应该几乎总是得到 1"
            print(f"✓ 正确识别为平衡函数")

    return True


def explain_deutsch():
    """解释 Deutsch 算法"""
    print("\n" + "=" * 60)
    print("Deutsch 算法工作原理")
    print("=" * 60)

    print("""
为什么只需要一次查询？

经典情况：
- 必须计算 f(0) 和 f(1) 才能判断
- 需要2次查询

量子情况：
- 利用量子叠加和相位
- 初始态：|+⟩|-⟩ = (|0⟩+|1⟩)/√2 ⊗ (|0⟩-|1⟩)/√2
- Oracle 作用后，函数信息编码在全局相位中
- 第二次 H 门提取这个相位信息
- 只需1次查询！

这虽然是个简单问题，但证明了量子优势的存在！

数学：
- 常数函数：H|±⟩ = |0⟩
- 平衡函数：H|∓⟩ = |1⟩

历史意义：
- 1985年由 David Deutsch 提出
- 第一个量子算法
- 启发了后续的 Deutsch-Jozsa、Grover、Shor 等算法
    """)


if __name__ == '__main__':
    try:
        test_deutsch()
        explain_deutsch()

        print("\n🎉 恭喜！你已掌握 Deutsch 算法！")
        print("\n关键要点:")
        print("- 第一个量子优势算法")
        print("- 利用量子叠加和干涉")
        print("- 只需1次查询 vs 经典的2次")
        print("- 量子计算的里程碑")

    except AssertionError as e:
        print(f"❌ 测试失败: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
