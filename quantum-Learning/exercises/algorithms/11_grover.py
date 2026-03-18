"""
练习 11: Grover 搜索算法
==================

目标：实现量子搜索算法

知识点：
- Grover 算法在无序数据库中搜索
- 经典：O(N) - 必须逐个检查
- 量子：O(√N) - 二次加速
- 对于 N=10^6，经典需要 ~10^6 次，量子只需 ~10^3 次

算法组件：
1. Oracle：标记目标项
2. Diffusion Operator（扩散算子）：振幅放大
3. 迭代次数：约 π/4 * √N 次

应用：
- 数据库搜索
- 优化问题
- 密码分析
- SAT 求解

任务：实现 Grover 搜索算法
"""

from qiskit import QuantumCircuit
from qiskit_aer import Aer
import numpy as np
import math


def create_grover_oracle(n, target):
    """
    创建 Grover Oracle（标记目标）

    参数：
        n: 量子比特数
        target: 目标状态（整数），例如 target=3 表示 |011⟩

    返回：
        QuantumCircuit: Oracle 电路
    """
    oracle = QuantumCircuit(n, name='Oracle')

    # 将目标转换为二进制
    target_bits = format(target, f'0{n}b')

    # TODO: 实现 Oracle
    # 策略：使用 X 门和多控制 Z 门
    # 1. 对于目标中为 '0' 的位，应用 X 门
    # 2. 应用多控制 Z 门
    # 3. 撤销步骤 1 的 X 门

    # 步骤 1: X 门翻转 '0' 位
    for i, bit in enumerate(reversed(target_bits)):
        if bit == '0':
            oracle.x(i)

    # 步骤 2: 多控制 Z 门（标记目标）
    # 使用 Qiskit 的 mcz 或者等效实现
    if n == 2:
        oracle.cz(0, 1)
    elif n >= 2:
        # 对于 n >= 2，使用 h + mcx + h 来实现 mcz
        oracle.h(n-1)
        oracle.mcx(list(range(n-1)), n-1)
        oracle.h(n-1)

    # 步骤 3: 撤销 X 门
    for i, bit in enumerate(reversed(target_bits)):
        if bit == '0':
            oracle.x(i)

    return oracle


def create_diffusion_operator(n):
    """
    创建扩散算子（Grover Diffusion Operator）
    也称为"关于平均值的反射"

    数学：D = 2|s⟩⟨s| - I，其中 |s⟩ = H^⊗n|0⟩^⊗n

    参数：
        n: 量子比特数

    返回：
        QuantumCircuit: 扩散算子电路
    """
    diffusion = QuantumCircuit(n, name='Diffusion')

    # TODO: 实现扩散算子
    # 步骤 1: 应用 H 门到所有量子比特

    # 步骤 2: 应用 X 门到所有量子比特

    # 步骤 3: 多控制 Z 门

    # 步骤 4: 撤销 X 门

    # 步骤 5: 撤销 H 门

    return diffusion


def grover_algorithm(n, target):
    """
    实现 Grover 搜索算法

    参数：
        n: 量子比特数
        target: 要搜索的目标（整数）

    返回：
        QuantumCircuit: Grover 算法电路
    """
    qc = QuantumCircuit(n, n)

    # 计算最优迭代次数
    N = 2**n
    iterations = int(np.pi / 4 * np.sqrt(N))

    print(f"搜索空间大小: {N}")
    print(f"Grover 迭代次数: {iterations}")

    # 步骤 1: 初始化为均匀叠加态
    # TODO: 对所有量子比特应用 H 门

    # 步骤 2: Grover 迭代
    oracle = create_grover_oracle(n, target)
    diffusion = create_diffusion_operator(n)

    for _ in range(iterations):
        qc.compose(oracle, inplace=True)
        qc.compose(diffusion, inplace=True)

    # 步骤 3: 测量
    qc.measure(range(n), range(n))

    return qc


def test_grover():
    """测试 Grover 算法"""
    print("测试 Grover 搜索算法\n")
    print("=" * 60)

    test_cases = [
        (2, 3),   # 4个元素中找3
        (3, 5),   # 8个元素中找5
        (4, 9),   # 16个元素中找9
    ]

    simulator = Aer.get_backend('qasm_simulator')

    for n, target in test_cases:
        print(f"\nn={n}, 目标={target} (二进制: {format(target, f'0{n}b')})")

        qc = grover_algorithm(n, target)

        # 显示电路（仅一次）
        if n == 2:
            print("\n电路结构:")
            print(qc.draw(output='text'))

        # 运行
        job = simulator.run(qc, shots=1000)
        counts = job.result().get_counts()

        # 显示结果
        print(f"\n测量结果（前5个）:")
        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        for state, count in sorted_counts[:5]:
            print(f"  {state}: {count} ({count/10:.1f}%)")

        # 验证
        target_bits = format(target, f'0{n}b')[::-1]  # Qiskit 顺序
        if target_bits in counts:
            success_rate = counts[target_bits] / 1000
            print(f"\n✓ 找到目标 {target_bits}，成功率: {success_rate*100:.1f}%")
            assert success_rate > 0.5, f"成功率应该 > 50%，实际: {success_rate*100:.1f}%"
        else:
            raise AssertionError(f"未找到目标 {target_bits}")

    return True


def analyze_complexity():
    """分析 Grover 算法的复杂度"""
    print("\n" + "=" * 60)
    print("Grover 算法复杂度分析")
    print("=" * 60)

    print("\n{:>10} | {:>15} | {:>15} | {:>10}".format(
        'N', '经典查询', 'Grover迭代', '加速比'))
    print("-" * 60)

    for n in [4, 8, 16, 20, 24]:
        N = 2**n
        classical = N / 2  # 平均
        quantum = int(np.pi / 4 * np.sqrt(N))
        speedup = classical / quantum

        print("{:10d} | {:15.0f} | {:15d} | {:10.2f}x".format(
            N, classical, quantum, speedup))

    print("""
关键洞察：
- 经典：O(N) - 线性
- 量子：O(√N) - 平方根
- 二次加速（不是指数，但依然显著！）

实际意义：
- 对于大数据库搜索，显著减少查询次数
- 应用于密码分析（如 AES 密钥搜索）
- 是少数几个对实际问题有用的量子算法之一

限制：
- 需要量子 RAM（QRAM）来存储数据
- 二次加速不如 Shor 的指数加速
- 但应用范围更广
    """)


if __name__ == '__main__':
    try:
        test_grover()
        analyze_complexity()

        print("\n🎉 恭喜！你已掌握 Grover 搜索算法！")
        print("\n关键要点:")
        print("- 无序搜索的二次加速")
        print("- Oracle + Diffusion 的优雅组合")
        print("- 振幅放大的经典例子")
        print("- 少数几个有实际应用价值的量子算法")
        print("\n历史：")
        print("1996年由 Lov Grover 发明，是量子算法的里程碑")

    except AssertionError as e:
        print(f"❌ 测试失败: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
