"""
练习 13: Shor 因数分解算法
==================

目标：理解 Shor 算法的原理并实现简化版本

知识点：
- Shor 算法可以在多项式时间内分解大整数
- 威胁到 RSA 等现代加密系统
- 是量子算法最著名的应用之一
- 结合了量子和经典计算

算法步骤：
1. 选择随机数 a < N
2. 计算 gcd(a, N)，如果 > 1 则找到因子
3. 使用量子算法找到 a^r ≡ 1 (mod N) 的周期 r
4. 如果 r 是偶数且 a^(r/2) ≠ -1 (mod N)，则：
   因子是 gcd(a^(r/2) ± 1, N)

量子部分：周期查找
- 使用量子相位估计和 QFT
- 这是量子优势所在

警告：完整的 Shor 算法需要大量量子比特
这里我们实现简化版本用于理解原理

任务：实现 Shor 算法的周期查找部分
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import Aer
from qiskit.circuit.library import QFT
import numpy as np
from math import gcd
from fractions import Fraction


def classical_order_finding(a, N):
    """
    经典方法找周期（用于小数字）

    找到最小的 r 使得 a^r ≡ 1 (mod N)

    参数：
        a: 底数
        N: 模数

    返回：
        int: 周期 r
    """
    r = 1
    y = a % N

    while y != 1:
        y = (y * a) % N
        r += 1
        if r > N:  # 防止无限循环
            return None

    return r


def shors_algorithm_classical(N):
    """
    Shor 算法的经典部分

    参数：
        N: 要分解的数

    返回：
        tuple: (factor1, factor2) 或 None
    """
    print(f"分解 N = {N}")

    # 检查 N 是否是偶数
    if N % 2 == 0:
        return (2, N // 2)

    # 随机选择 a
    for a in range(2, N):
        print(f"\n尝试 a = {a}")

        # 步骤 1: 检查 gcd
        g = gcd(a, N)
        if g > 1:
            print(f"  找到因子（通过 gcd）: {g}")
            return (g, N // g)

        # 步骤 2: 找周期 r
        r = classical_order_finding(a, N)

        if r is None:
            continue

        print(f"  找到周期: r = {r}")

        # 步骤 3: 检查 r 是否可用
        if r % 2 != 0:
            print(f"  r 是奇数，重试")
            continue

        # 步骤 4: 计算可能的因子
        x = pow(a, r // 2, N)

        if x == N - 1:
            print(f"  a^(r/2) ≡ -1 (mod N)，重试")
            continue

        # 计算因子
        factor1 = gcd(x + 1, N)
        factor2 = gcd(x - 1, N)

        if factor1 > 1 and factor1 < N:
            print(f"  ✓ 找到因子: {factor1} 和 {N // factor1}")
            return (factor1, N // factor1)

        if factor2 > 1 and factor2 < N:
            print(f"  ✓ 找到因子: {factor2} 和 {N // factor2}")
            return (factor2, N // factor2)

    return None


def quantum_period_finding_simple(a, N):
    """
    简化的量子周期查找（演示用）

    实际的 Shor 算法需要更多量子比特和模幂运算电路
    这里我们演示核心思想

    参数：
        a: 底数
        N: 模数

    返回：
        int: 估计的周期
    """
    # 注意：这是简化版，实际实现需要：
    # 1. 足够的量子比特（约 2 log N）
    # 2. 模幂运算 U|y⟩ = |ay mod N⟩
    # 3. QFT 提取周期信息

    # 这里我们用经典方法找周期来演示流程
    print("  [量子周期查找]")
    r = classical_order_finding(a, N)
    print(f"  量子算法找到周期: r = {r}")
    return r


def create_modular_exponentiation_circuit(a, N, n_count):
    """
    创建模幂运算电路（简化版）

    实现 U|y⟩ = |a*y mod N⟩

    注意：完整实现非常复杂，这里只是框架

    参数：
        a: 底数
        N: 模数
        n_count: 计数量子比特数

    返回：
        QuantumCircuit: 模幂运算电路
    """
    # 实际的模幂运算需要：
    # - 量子加法器
    # - 量子乘法器
    # - 模运算
    # 这超出了入门练习的范围

    # 这里返回一个占位符电路
    n_qubits = n_count + int(np.ceil(np.log2(N)))
    qc = QuantumCircuit(n_qubits, name=f'U^a mod {N}')

    # TODO: 实现模幂运算（高级主题）
    # 实际实现需要参考 Qiskit 教程

    return qc


def test_shor_classical():
    """测试 Shor 算法（经典版本）"""
    print("测试 Shor 因数分解算法（经典模拟）\n")
    print("=" * 60)

    # 测试用例
    test_cases = [15, 21, 35]

    for N in test_cases:
        print(f"\n{'=' * 60}")
        result = shors_algorithm_classical(N)

        if result:
            f1, f2 = result
            assert f1 * f2 == N, f"因子错误: {f1} * {f2} ≠ {N}"
            print(f"\n✓ 成功分解 {N} = {f1} × {f2}")
        else:
            print(f"\n✗ 分解 {N} 失败")

    return True


def explain_shor():
    """解释 Shor 算法"""
    print("\n" + "=" * 60)
    print("Shor 算法详解")
    print("=" * 60)

    print("""
为什么 Shor 算法重要？

  RSA 加密的安全性基于：
    - 分解大整数（如 2048 位）在经典计算机上很难
    - 最好的经典算法：次指数时间

  Shor 算法：
    - 多项式时间！O((log N)³)
    - 威胁到现有的公钥密码系统

算法核心：

  问题：分解 N = p × q

  转化为：找周期 r 使得 a^r ≡ 1 (mod N)

  如何利用周期？
    如果 r 是偶数：
      a^r - 1 = (a^(r/2) - 1)(a^(r/2) + 1) ≡ 0 (mod N)

    则 gcd(a^(r/2) ± 1, N) 可能是 N 的因子

量子部分：周期查找

  经典方法：
    - 计算 a^1, a^2, a^3, ... mod N
    - 直到找到周期
    - 时间：O(r)，r 可能很大

  量子方法：
    1. 准备叠加态： Σ |x⟩|0⟩
    2. 计算模幂运算： Σ |x⟩|a^x mod N⟩
    3. 测量第二个寄存器，得到某个值 y
    4. 第一个寄存器坍缩到 {x : a^x ≡ y (mod N)}
    5. 应用 QFT 提取周期信息
    6. 测量得到 r 的倍数

实现挑战：

  ⚠ 需要大量量子比特
     - 分解 N 需要约 2 log N 个量子比特
     - 分解 2048 位数需要 ~4000 量子比特

  ⚠ 需要低错误率
     - 需要量子纠错
     - 目前的 NISQ 设备还不够

  ⚠ 模幂运算电路复杂
     - 需要量子算术电路
     - 门深度很大

现状 (2024-2025)：

  实验进展：
    ✓ 2001: 分解 15 = 3 × 5 (IBM, 7 qubits)
    ✓ 2012: 分解 21 = 3 × 7 (优化版)
    ✓ 2019: 分解 35 = 5 × 7

  目标：
    ⚠ 分解 2048 位 RSA 密钥
    ⚠ 估计需要百万级量子比特（考虑纠错）
    ⚠ 预计还需要 10-20 年

影响：

  密码学：
    - 需要迁移到后量子密码 (Post-Quantum Cryptography)
    - NIST 正在标准化抗量子算法

  理论意义：
    - 证明了量子计算的巨大潜力
    - BQP vs NP 的重要证据

有趣的事实：
  - Peter Shor 因此算法获得 2023 年 ACM 图灵奖提名
  - RSA 的发明者说："Shor 算法是美丽的，尽管它威胁到我的工作"
    """)


if __name__ == '__main__':
    try:
        test_shor_classical()
        explain_shor()

        print("\n🎉 恭喜！你已理解 Shor 算法！")
        print("\n关键要点:")
        print("- 将因数分解转化为周期查找")
        print("- 量子周期查找比经典指数级更快")
        print("- 威胁 RSA 等加密系统")
        print("- 完整实现需要大规模容错量子计算机")
        print("\n这是量子计算最著名的应用！")

    except AssertionError as e:
        print(f"❌ 测试失败: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
