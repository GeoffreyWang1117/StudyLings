"""
二次量子化基础 Second Quantization Basics
难度 Difficulty: ★★★★★

物理背景 Physical Background:
==================================
二次量子化是量子场论的基础，提供了处理全同粒子系统的自然框架。
与一次量子化（将经典力学量子化）不同，二次量子化将粒子数本身量子化。

历史意义:
- 1927年: 狄拉克首次提出二次量子化处理电磁场
- 1928年: 约当-维格纳将其推广到费米子
- 二次量子化是量子场论、凝聚态物理、量子光学的基础

核心概念:
1. 产生算符 a†: 在量子态中增加一个粒子
2. 湮灭算符 a: 在量子态中减少一个粒子
3. 粒子数算符 N = a†a: 测量粒子数
4. Fock空间: 不同粒子数态的直和空间

学习目标 Learning Objectives:
- 理解产生湮灭算符的定义和性质
- 掌握玻色子对易关系和费米子反对易关系
- 分析全同粒子的量子统计（玻色-爱因斯坦/费米-狄拉克分布）
- 理解相干态的物理意义（量子光学基础）

关键公式 Key Formulas:
- 玻色子对易关系: [a, a†] = 1, [a, a] = [a†, a†] = 0
- 费米子反对易关系: {c, c†} = 1, {c, c} = {c†, c†} = 0
- 粒子数表象: |n⟩ = (a†)^n/√(n!) |0⟩
- 湮灭作用: a|n⟩ = √n |n-1⟩
- 产生作用: a†|n⟩ = √(n+1) |n+1⟩
- 相干态: |α⟩ = exp(-|α|²/2) Σ (α^n/√n!) |n⟩
- 玻色-爱因斯坦分布: n_BE = 1/(exp((ε-μ)/k_B T) - 1)
- 费米-狄拉克分布: n_FD = 1/(exp((ε-μ)/k_B T) + 1)

HINT: 玻色子: [a, a†] = 1 (对易关系)
HINT: 费米子: {c, c†} = 1 (反对易关系)
HINT: 粒子数表象: |n⟩ = (a†)^n/√(n!) |0⟩
HINT: 泡利不相容原理: (c†)² = 0 (费米子不能占据同一量子态)
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import hbar, k_B, eV

# I AM NOT DONE

# =============================================================================
# 练习 8.1: 玻色子算符
# Exercise 8.1: Boson Operators
#
# 物理背景:
# 玻色子（如光子、声子、介子）服从玻色-爱因斯坦统计，不受泡利不相容原理限制。
# 玻色子算符满足对易关系，是量子光学和凝聚态物理的基础。
#
# 对易关系的物理意义:
# - [a, a†] = 1 保证了能量本征值的等间距性质
# - 这正是谐振子能级 E_n = ℏω(n+1/2) 的根源
# =============================================================================
def boson_commutator():
    """
    玻色子对易关系 Boson Commutation Relations

    对易子定义: [A, B] = AB - BA

    物理意义:
    - [a, a†] = 1: 产生和湮灭算符不对易，这导致零点能的存在
    - [a, a] = 0: 两次湮灭的顺序无关
    - [a†, a†] = 0: 两次产生的顺序无关

    返回:
        dict: 对易关系结果
    """
    return {
        '[a, a†]': 1,
        '[a, a]': 0,
        '[a†, a†]': 0
    }


def boson_number_operator_matrix(n_max):
    """
    粒子数算符矩阵 N = a†a Number Operator Matrix

    物理意义:
    - N|n⟩ = n|n⟩，本征值为非负整数
    - 在Fock空间基底 {|0⟩, |1⟩, ..., |n_max⟩} 下为对角矩阵

    参数:
        n_max (int): 最大粒子数（截断）

    返回:
        np.ndarray: (n_max+1) x (n_max+1) 对角矩阵
    """
    N = np.diag(np.arange(n_max + 1))
    return N


def boson_annihilation_matrix(n_max):
    """
    玻色子湮灭算符矩阵 a Annihilation Operator Matrix

    作用规则: a|n⟩ = √n |n-1⟩
    - 减少一个粒子
    - a|0⟩ = 0（真空态被湮灭为零）

    矩阵元: ⟨m|a|n⟩ = √n δ_{m,n-1}
    矩阵结构: 次对角矩阵（上三角）

    参数:
        n_max (int): 最大粒子数（截断）

    返回:
        np.ndarray: (n_max+1) x (n_max+1) 矩阵
    """
    a = np.zeros((n_max + 1, n_max + 1))
    for n in range(1, n_max + 1):
        a[n-1, n] = np.sqrt(n)
    return a


def boson_creation_matrix(n_max):
    """
    玻色子产生算符矩阵 a† Creation Operator Matrix

    作用规则: a†|n⟩ = √(n+1) |n+1⟩
    - 增加一个粒子
    - 可无限叠加（玻色子凝聚的基础）

    矩阵元: ⟨m|a†|n⟩ = √(n+1) δ_{m,n+1}
    注意: a† = (a)^T（厄米共轭）

    参数:
        n_max (int): 最大粒子数（截断）

    返回:
        np.ndarray: (n_max+1) x (n_max+1) 矩阵
    """
    return boson_annihilation_matrix(n_max).T


def coherent_state(alpha, n_max):
    """
    相干态 |α⟩ Coherent State

    定义: |α⟩ = exp(-|α|²/2) Σ_n (α^n/√n!) |n⟩

    物理意义:
    - 湮灭算符的本征态: a|α⟩ = α|α⟩
    - 最接近经典电磁场的量子态
    - 激光输出的良好近似
    - 具有最小不确定性（ΔxΔp = ℏ/2）

    性质:
    - 粒子数服从泊松分布: P(n) = |⟨n|α⟩|² = e^{-|α|²} |α|^{2n}/n!
    - 平均粒子数: ⟨n⟩ = |α|²
    - 方差: Δn = |α|（等于标准差）

    参数:
        alpha (complex): 相干态参数（复振幅）
        n_max (int): 粒子数截断

    返回:
        np.ndarray: 粒子数基底下的展开系数
    """
    coeffs = np.zeros(n_max + 1, dtype=complex)

    prefactor = np.exp(-np.abs(alpha)**2 / 2)

    for n in range(n_max + 1):
        coeffs[n] = prefactor * alpha**n / np.sqrt(float(np.math.factorial(n)))

    return coeffs


def coherent_state_properties(alpha):
    """
    相干态的统计性质 Properties of Coherent States

    核心性质:
    - 平均粒子数: ⟨n⟩ = |α|²
    - 粒子数方差: Var(n) = |α|²
    - 标准差: Δn = |α|
    - 相对涨落: Δn/⟨n⟩ = 1/|α| → 0（经典极限）

    物理意义:
    - 大|α|时量子涨落相对减小，趋于经典行为
    - Mandel Q参数 = 0（泊松统计）

    参数:
        alpha (complex): 相干态参数

    返回:
        dict: 包含 mean_n, variance, std_n
    """
    n_mean = np.abs(alpha)**2
    n_variance = np.abs(alpha)**2
    return {
        'mean_n': n_mean,
        'variance': n_variance,
        'std_n': np.sqrt(n_variance)
    }


# =============================================================================
# 练习 8.2: 费米子算符
# Exercise 8.2: Fermion Operators
#
# 物理背景:
# 费米子（如电子、质子、中子、夸克）服从费米-狄拉克统计和泡利不相容原理。
# 反对易关系 {c, c†} = 1 自动实现了泡利不相容原理: (c†)² = 0。
#
# 应用领域:
# - 固体物理中的电子
# - 核物理中的核子
# - 量子化学中的分子轨道
# =============================================================================
def fermion_anticommutator():
    """
    费米子反对易关系 Fermion Anticommutation Relations

    反对易子定义: {A, B} = AB + BA

    关键关系:
    - {c, c†} = 1: 保证归一化
    - {c, c} = 0 → c² = 0: 同一态湮灭两次为零
    - {c†, c†} = 0 → (c†)² = 0: 不能创建两个相同费米子（泡利原理）

    物理意义:
    每个单粒子态只能被0或1个费米子占据（占据数 n ∈ {0, 1}）

    返回:
        dict: 反对易关系结果
    """
    return {
        '{c, c†}': 1,
        '{c, c}': 0,
        '{c†, c†}': 0
    }


def fermion_annihilation_matrix():
    """
    单模费米子湮灭算符矩阵 Single-Mode Fermion Annihilation Matrix

    作用规则:
    - c|1⟩ = |0⟩（从占据态移除粒子）
    - c|0⟩ = 0（空态无法再湮灭）

    矩阵形式（在{|0⟩, |1⟩}基底下）:
    c = |0><1| = [[0, 1], [0, 0]]

    注意: 费米子只有两个态（占据/未占据），所以是2x2矩阵

    返回:
        np.ndarray: 2x2 复数矩阵
    """
    c = np.array([
        [0, 1],
        [0, 0]
    ], dtype=complex)
    return c


def fermion_creation_matrix():
    """
    费米子产生算符矩阵 c† Fermion Creation Matrix

    作用规则:
    - c†|0⟩ = |1⟩（在空态中创建粒子）
    - c†|1⟩ = 0（泡利不相容: 不能再添加粒子）

    矩阵形式: c† = |1><0| = [[0, 0], [1, 0]]

    返回:
        np.ndarray: 2x2 复数矩阵
    """
    return fermion_annihilation_matrix().T


def fermion_number_matrix():
    """
    费米子数算符 n = c†c Fermion Number Operator

    本征值: n|0⟩ = 0|0⟩, n|1⟩ = 1|1⟩
    矩阵形式: n = [[0, 0], [0, 1]] = diag(0, 1)

    性质: n² = n（投影算符）

    返回:
        np.ndarray: 2x2 对角矩阵
    """
    c = fermion_annihilation_matrix()
    c_dag = fermion_creation_matrix()
    return c_dag @ c


def pauli_exclusion_check(c_dag):
    """
    验证泡利不相容原理 Pauli Exclusion Principle Verification

    核心: (c†)² = 0

    物理意义:
    - 不能在同一量子态创建两个费米子
    - 这是反对易关系 {c†, c†} = 0 的直接结果
    - 解释了原子的电子壳层结构

    参数:
        c_dag (np.ndarray): 费米子产生算符矩阵

    返回:
        bool: 若 (c†)² = 0 则返回 True
    """
    return np.allclose(c_dag @ c_dag, 0)


# =============================================================================
# 练习 8.3: 多模系统
# Exercise 8.3: Multi-Mode Systems
#
# 物理背景:
# 实际系统通常包含多个量子态（模式），如多模光场、晶格振动等。
# 多模系统的Fock空间是各单模Fock空间的张量积。
#
# 关键概念:
# - 不同模式的算符对易（玻色子）或反对易（费米子）
# - Jordan-Wigner变换: 连接自旋链和费米子链
# - 交换对称性决定了玻色子/费米子的统计性质
# =============================================================================
def two_mode_boson_state(n1, n2, n_max):
    """
    双模玻色子态 |n1, n2⟩ Two-Mode Boson State

    态向量构造:
    |n1, n2⟩ = |n1⟩ ⊗ |n2⟩
    在乘积基 {|0,0⟩, |0,1⟩, ..., |n_max, n_max⟩} 下的分量

    参数:
        n1 (int): 第一模式的粒子数
        n2 (int): 第二模式的粒子数
        n_max (int): 每个模式的最大粒子数

    返回:
        np.ndarray: 态向量（长度为 (n_max+1)²）
    """
    dim = (n_max + 1)**2
    state = np.zeros(dim, dtype=complex)
    index = n1 * (n_max + 1) + n2
    if index < dim:
        state[index] = 1
    return state


def two_mode_fermion_state(occ1, occ2):
    """
    双模费米子态 Two-Mode Fermion State

    Fock空间基底:
    |00⟩, |01⟩, |10⟩, |11⟩（共4个态）
    每个模式只能占据0或1个粒子

    注意: 多费米子态需要考虑反对称化

    参数:
        occ1 (int): 第一模式占据数 (0 或 1)
        occ2 (int): 第二模式占据数 (0 或 1)

    返回:
        np.ndarray: 4维态向量
    """
    state = np.zeros(4, dtype=complex)
    index = occ1 * 2 + occ2
    state[index] = 1
    return state


def jordan_wigner_transformation(j, N_sites):
    """
    Jordan-Wigner变换 Jordan-Wigner Transformation

    将一维自旋链映射到无相互作用费米子:
    c_j = (∏_{k<j} σ_z^k) σ_-^j

    物理意义:
    - 建立自旋1/2系统与费米子系统的精确映射
    - 自旋链的XY模型可映射为自由费米子
    - 弦算符 ∏ σ_z 保证了费米子的反对易性

    应用:
    - 一维可解模型（如XY模型、Ising模型）
    - 拓扑相变研究
    - 量子计算中的费米子模拟

    参数:
        j (int): 格点指标
        N_sites (int): 总格点数

    返回:
        str: 变换表达式
    """
    # 简化：返回字符串描述
    return f"c_{j} = (prod_k<{j} sigma_z^k) sigma_-^{j}"


def exchange_symmetry_boson(psi_12, psi_21):
    """
    玻色子交换对称性 Boson Exchange Symmetry

    玻色子波函数在粒子交换下对称:
    ψ(r₁, r₂) = ψ(r₂, r₁)

    物理后果:
    - 玻色子可以占据相同量子态
    - 玻色-爱因斯坦凝聚的基础
    - 例: 光子、⁴He原子

    参数:
        psi_12: 粒子1在前的波函数
        psi_21: 粒子2在前的波函数

    返回:
        bool: 是否满足对称性
    """
    return np.allclose(psi_12, psi_21)


def exchange_symmetry_fermion(psi_12, psi_21):
    """
    费米子交换反对称性 Fermion Exchange Antisymmetry

    费米子波函数在粒子交换下反对称:
    ψ(r₁, r₂) = -ψ(r₂, r₁)

    物理后果:
    - 当 r₁ = r₂ 时，ψ = 0（泡利不相容）
    - Slater行列式的数学基础
    - 例: 电子、质子、中子

    参数:
        psi_12: 粒子1在前的波函数
        psi_21: 粒子2在前的波函数

    返回:
        bool: 是否满足反对称性
    """
    return np.allclose(psi_12, -psi_21)


# =============================================================================
# 练习 8.4: 谐振子的二次量子化
# Exercise 8.4: Second Quantization of Harmonic Oscillator
#
# 物理背景:
# 谐振子是二次量子化最自然的应用。产生湮灭算符最初就是为谐振子定义的。
#
# 核心公式:
# - x = √(ℏ/2mω) (a + a†)
# - p = i√(mωℏ/2) (a† - a)
# - H = ℏω(a†a + 1/2) = ℏω(N + 1/2)
#
# 物理意义:
# - 能级等间距: E_n = ℏω(n + 1/2)
# - 零点能 E_0 = ℏω/2 来自量子涨落
# - 光场量子化的原型
# =============================================================================
def position_operator(n_max, m, omega):
    """
    位置算符的二次量子化形式 Position Operator in Second Quantization

    公式: x = √(ℏ/2mω) (a + a†)

    物理意义:
    - x是厄米算符（可观测量）
    - 矩阵元 ⟨n|x|m⟩ ≠ 0 仅当 m = n±1
    - 这导致选择定则 Δn = ±1

    参数:
        n_max (int): 粒子数截断
        m (float): 粒子质量 [kg]
        omega (float): 角频率 [rad/s]

    返回:
        np.ndarray: 位置算符矩阵
    """
    a = boson_annihilation_matrix(n_max)
    a_dag = boson_creation_matrix(n_max)
    x_scale = np.sqrt(hbar / (2 * m * omega))
    return x_scale * (a + a_dag)


def momentum_operator(n_max, m, omega):
    """
    动量算符的二次量子化形式 Momentum Operator in Second Quantization

    公式: p = i√(mωℏ/2) (a† - a)

    验证:
    - [x, p] = iℏ（正则对易关系）
    - p也是厄米算符

    参数:
        n_max (int): 粒子数截断
        m (float): 粒子质量 [kg]
        omega (float): 角频率 [rad/s]

    返回:
        np.ndarray: 动量算符矩阵
    """
    a = boson_annihilation_matrix(n_max)
    a_dag = boson_creation_matrix(n_max)
    p_scale = 1j * np.sqrt(m * omega * hbar / 2)
    return p_scale * (a_dag - a)


def hamiltonian_harmonic_oscillator(n_max, omega):
    """
    谐振子哈密顿量 Harmonic Oscillator Hamiltonian

    公式: H = ℏω(a†a + 1/2) = ℏω(N + 1/2)

    能级结构:
    - E_n = ℏω(n + 1/2), n = 0, 1, 2, ...
    - 等间距: ΔE = ℏω
    - 基态能 E_0 = ℏω/2（零点能）

    物理应用:
    - 分子振动光谱
    - 晶格声子
    - 电磁场量子化

    参数:
        n_max (int): 粒子数截断
        omega (float): 角频率 [rad/s]

    返回:
        np.ndarray: 哈密顿量矩阵（对角）
    """
    N = boson_number_operator_matrix(n_max)
    return hbar * omega * (N + 0.5 * np.eye(n_max + 1))


def uncertainty_product(n, m, omega):
    """
    位置-动量不确定性乘积 Uncertainty Product

    公式: ΔxΔp = ℏ(n + 1/2)

    注意:
    - 基态 n=0: ΔxΔp = ℏ/2（最小不确定性态）
    - 激发态 n>0: 不确定性增加
    - 相干态也是最小不确定性态

    参数:
        n (int): 量子数
        m (float): 质量（未使用，保留接口一致性）
        omega (float): 角频率（未使用）

    返回:
        float: 不确定性乘积 [J·s]
    """
    return hbar * (n + 0.5)


def zero_point_energy(omega):
    """
    零点能 Zero-Point Energy

    公式: E_0 = ℏω/2

    物理意义:
    - 量子系统即使在基态也有能量涨落
    - 来源于不确定性原理
    - 可观测效应: Casimir效应、Lamb位移

    宇宙学问题:
    - 真空能量密度与暗能量密度相差~120个数量级
    - 这是现代物理学最大的未解之谜之一

    参数:
        omega (float): 角频率 [rad/s]

    返回:
        float: 零点能 [J]
    """
    return hbar * omega / 2


# =============================================================================
# 练习 8.5: 玻色和费米统计
# Exercise 8.5: Bose and Fermi Statistics
#
# 物理背景:
# 全同粒子的量子统计由其交换对称性决定。
# - 玻色子: 整数自旋，对称波函数 → 玻色-爱因斯坦统计
# - 费米子: 半整数自旋，反对称波函数 → 费米-狄拉克统计
#
# 经典极限:
# 当 exp((ε-μ)/k_B T) >> 1 时，两种分布都趋于 Maxwell-Boltzmann 分布
#
# 关键物理现象:
# - 玻色-爱因斯坦凝聚 (BEC): T < T_c 时宏观粒子数占据基态
# - 费米简并: T → 0 时电子填满至费米能级
# =============================================================================
def bose_einstein_distribution(epsilon, mu, T):
    """
    玻色-爱因斯坦分布 Bose-Einstein Distribution

    公式: n_BE = 1/(exp((ε-μ)/(k_B T)) - 1)

    适用条件:
    - ε > μ（否则分布发散，需要BEC处理）
    - T > 0

    物理意义:
    - 描述无相互作用玻色子在热平衡时的平均占据数
    - 低能态的占据增强（玻色增强）
    - 光子的情况: μ = 0（普朗克分布）

    参数:
        epsilon (float): 单粒子能量 [J]
        mu (float): 化学势 [J]
        T (float): 温度 [K]

    返回:
        float: 平均占据数
    """
    x = (epsilon - mu) / (k_B * T)
    if x > 700:
        return 0
    return 1 / (np.exp(x) - 1)


def fermi_dirac_distribution(epsilon, mu, T):
    """
    费米-狄拉克分布 Fermi-Dirac Distribution

    公式: n_FD = 1/(exp((ε-μ)/(k_B T)) + 1)

    特殊极限:
    - T → 0: 阶跃函数 n = θ(μ - ε)
    - T → ∞: n → 1/2（高温极限）

    物理意义:
    - 0 ≤ n_FD ≤ 1（泡利原理的体现）
    - μ(T=0) = E_F（费米能）
    - 金属电子论、半导体物理的基础

    参数:
        epsilon (float): 单粒子能量 [J]
        mu (float): 化学势 [J]（T=0时为费米能）
        T (float): 温度 [K]

    返回:
        float: 平均占据数 (0到1之间)
    """
    x = (epsilon - mu) / (k_B * T)
    if x > 700:
        return 0
    if x < -700:
        return 1
    return 1 / (np.exp(x) + 1)


def maxwell_boltzmann_distribution(epsilon, mu, T):
    """
    麦克斯韦-玻尔兹曼分布 Maxwell-Boltzmann Distribution

    公式: n_MB = exp(-(ε-μ)/(k_B T))

    物理意义:
    - 经典统计力学的分布
    - 忽略量子效应时的近似
    - 高温低密度极限下有效

    适用条件:
    - exp((ε-μ)/(k_B T)) >> 1
    - 即 n << 1（稀薄气体）

    参数:
        epsilon (float): 单粒子能量 [J]
        mu (float): 化学势 [J]
        T (float): 温度 [K]

    返回:
        float: 平均占据数
    """
    x = (epsilon - mu) / (k_B * T)
    if x > 700:
        return 0
    return np.exp(-x)


def chemical_potential_fermion_T0(E_F):
    """
    T=0时费米子的化学势 Chemical Potential at T=0

    公式: μ(T=0) = E_F

    费米能的物理意义:
    - 基态时最高被占据能级
    - 对于金属: E_F ~ 几eV
    - 决定了低温物理性质

    温度修正（低温）:
    μ(T) ≈ E_F[1 - (π²/12)(k_B T/E_F)²]

    参数:
        E_F (float): 费米能 [J]

    返回:
        float: 化学势 [J]
    """
    return E_F


def specific_heat_electron_gas(T, E_F, N):
    """
    电子气比热（低温）Electron Gas Specific Heat

    公式: C_V = (π²/3) × N k_B² T / E_F

    物理解释:
    - 只有费米面附近 ~k_B T 能量范围内的电子能被激发
    - 有效电子数 ~ N(k_B T/E_F)
    - 每个电子贡献 ~k_B → C_V ∝ T

    与经典结果对比:
    - 经典: C_V = (3/2)Nk_B（常数）
    - 量子: C_V ∝ T（线性）
    - 实验验证了量子理论的正确性

    参数:
        T (float): 温度 [K]
        E_F (float): 费米能 [J]
        N (int): 电子数

    返回:
        float: 比热容 [J/K]
    """
    return (np.pi**2 / 3) * N * k_B**2 * T / E_F


# =============================================================================
# 练习 8.6: 场算符
# Exercise 8.6: Field Operators
#
# 物理背景:
# 场算符将二次量子化推广到连续空间，是量子场论的基础。
#
# 场算符的构造:
# - 选择完备单粒子基 {φ_k(x)}
# - 场湮灭算符: ψ(x) = Σ_k φ_k(x) a_k
# - 场产生算符: ψ†(x) = Σ_k φ_k*(x) a_k†
#
# 物理意义:
# - ψ†(x) 在位置 x 创建一个粒子
# - ψ(x) 在位置 x 湮灭一个粒子
# - 粒子数密度: n(x) = ψ†(x)ψ(x)
# =============================================================================
def field_operator_expansion():
    """
    场算符的模式展开 Mode Expansion of Field Operators

    展开形式:
    ψ(x) = Σ_k φ_k(x) a_k （湮灭场）
    ψ†(x) = Σ_k φ_k*(x) a_k† （产生场）

    物理意义:
    - φ_k(x): 单粒子波函数（模式函数）
    - a_k: 模式 k 的湮灭算符
    - 将离散模式和连续空间联系起来

    返回:
        str: 场算符展开表达式
    """
    return "ψ(x) = Σ_k φ_k(x) a_k"


def field_commutator_boson():
    """
    玻色场的对易关系 Boson Field Commutator

    关键关系:
    [ψ(x), ψ†(x')] = δ(x-x')
    [ψ(x), ψ(x')] = 0
    [ψ†(x), ψ†(x')] = 0

    物理意义:
    - 不同位置的场算符是独立的
    - δ函数保证了正则对易关系
    - 这是局域场论的基础

    返回:
        str: 对易关系表达式
    """
    return "[ψ(x), ψ†(x')] = δ(x-x')"


def field_anticommutator_fermion():
    """
    费米场的反对易关系 Fermion Field Anticommutator

    关键关系:
    {ψ(x), ψ†(x')} = δ(x-x')
    {ψ(x), ψ(x')} = 0
    {ψ†(x), ψ†(x')} = 0

    物理意义:
    - 费米子的局域反对易性
    - x = x' 时 {ψ, ψ†} = 1（归一化）
    - 同一位置不能有两个费米子

    返回:
        str: 反对易关系表达式
    """
    return "{ψ(x), ψ†(x')} = δ(x-x')"


def particle_density_operator(psi_dag, psi):
    """
    粒子数密度算符 Particle Density Operator

    定义: n(x) = ψ†(x)ψ(x)

    物理意义:
    - ⟨n(x)⟩ 给出位置 x 的粒子密度
    - 总粒子数: N = ∫n(x)dx

    注意:
    - 正规序（玻色子）或反正规序（费米子）避免无穷大

    参数:
        psi_dag: ψ†(x) 的值
        psi: ψ(x) 的值

    返回:
        粒子密度值
    """
    return psi_dag * psi


def current_density_operator():
    """
    流密度算符 Current Density Operator

    定义: j(x) = (ℏ/2mi)[ψ†∇ψ - (∇ψ†)ψ]

    物理意义:
    - 描述粒子流
    - 满足连续性方程: ∂n/∂t + ∇·j = 0

    量子力学形式:
    - 与单粒子概率流公式相同
    - 但现在是算符形式

    返回:
        str: 流密度算符表达式
    """
    return "j = (ℏ/2mi)[ψ†∇ψ - (∇ψ†)ψ]"


# =============================================================================
# 可视化 Visualization
# 绘制二次量子化的关键物理量:
# 1. 相干态的粒子数分布（泊松分布）
# 2. 玻色/费米/经典分布函数比较
# 3. 费米-狄拉克分布的温度依赖
# 4. 谐振子能级结构
# 5. 位置算符矩阵元
# 6. 不确定性乘积随量子数变化
# =============================================================================
def plot_second_quantization():
    """绘制二次量子化相关图 Plot Second Quantization Results"""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 相干态的粒子数分布
    ax1 = axes[0, 0]
    n_max = 20
    n_vals = np.arange(n_max + 1)

    for alpha_val in [1, 2, 4]:
        coeffs = coherent_state(alpha_val, n_max)
        prob = np.abs(coeffs)**2
        ax1.plot(n_vals, prob, 'o-', label=f'|α|={alpha_val}', markersize=4)

    ax1.set_xlabel('n')
    ax1.set_ylabel('P(n)')
    ax1.set_title('相干态粒子数分布')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 玻色子和费米子分布
    ax2 = axes[0, 1]
    T = 300  # K
    mu = 0

    epsilon = np.linspace(-0.5, 1, 200) * eV

    n_BE = []
    n_FD = []
    n_MB = []

    for e in epsilon:
        if e > mu:
            n_BE.append(bose_einstein_distribution(e, mu, T))
        else:
            n_BE.append(np.nan)
        n_FD.append(fermi_dirac_distribution(e, mu, T))
        n_MB.append(maxwell_boltzmann_distribution(e, mu, T))

    ax2.plot(epsilon/eV, n_BE, 'b-', label='Bose-Einstein', linewidth=2)
    ax2.plot(epsilon/eV, n_FD, 'r-', label='Fermi-Dirac', linewidth=2)
    ax2.plot(epsilon/eV, n_MB, 'g--', label='Maxwell-Boltzmann', linewidth=2)
    ax2.axvline(x=0, color='k', linestyle=':', alpha=0.5)
    ax2.set_xlabel('(ε - μ) (eV)')
    ax2.set_ylabel('⟨n⟩')
    ax2.set_title(f'量子统计分布 (T = {T} K)')
    ax2.legend()
    ax2.set_xlim(-0.5, 1)
    ax2.set_ylim(0, 3)
    ax2.grid(True, alpha=0.3)

    # 3. 费米-狄拉克分布的温度依赖
    ax3 = axes[0, 2]
    mu_FD = 5 * eV  # 费米能
    epsilon_FD = np.linspace(3, 7, 200) * eV

    for T_val in [100, 300, 1000, 3000]:
        n_FD_T = [fermi_dirac_distribution(e, mu_FD, T_val) for e in epsilon_FD]
        ax3.plot(epsilon_FD/eV, n_FD_T, label=f'T={T_val}K', linewidth=2)

    ax3.axvline(x=5, color='k', linestyle='--', alpha=0.5, label='μ')
    ax3.set_xlabel('ε (eV)')
    ax3.set_ylabel('f(ε)')
    ax3.set_title('费米-狄拉克分布')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 谐振子能级
    ax4 = axes[1, 0]
    n_max = 5
    omega = 1e15

    H = hamiltonian_harmonic_oscillator(n_max, omega)
    eigenvalues = np.diag(H)

    ax4.barh(range(n_max + 1), eigenvalues/eV, alpha=0.7)
    ax4.set_ylabel('n')
    ax4.set_xlabel('E (eV)')
    ax4.set_title('谐振子能级')
    ax4.grid(True, alpha=0.3)

    # 5. 位置算符矩阵元
    ax5 = axes[1, 1]
    m = 9.1e-31
    x_op = position_operator(n_max, m, omega)

    im = ax5.imshow(np.abs(x_op) * 1e9, cmap='Blues')
    ax5.set_xlabel('m')
    ax5.set_ylabel('n')
    ax5.set_title('|⟨n|x|m⟩| (nm)')
    plt.colorbar(im, ax=ax5)

    # 6. 不确定性
    ax6 = axes[1, 2]
    n_range = np.arange(0, 20)

    uncertainty = [uncertainty_product(n, m, omega) / hbar for n in n_range]

    ax6.plot(n_range, uncertainty, 'bo-', linewidth=2, markersize=6)
    ax6.axhline(y=0.5, color='r', linestyle='--', alpha=0.5, label='最小值 ℏ/2')
    ax6.set_xlabel('n')
    ax6.set_ylabel('ΔxΔp/ℏ')
    ax6.set_title('不确定性乘积')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('second_quantization.png', dpi=150)
    print("图像已保存为 second_quantization.png")
    plt.show()


# =============================================================================
# 验证函数 Verification
# =============================================================================
def verify():
    """验证所有练习 Verify all exercises"""
    all_passed = True

    # Check 8.1 - 玻色子对易关系 Boson commutator
    comm = boson_commutator()
    if comm['[a, a†]'] != 1:
        print("X 8.1 错误：玻色子对易关系应满足 [a, a†] = 1")
        all_passed = False
    else:
        print("V 8.1 玻色子算符正确 ([a, a†] = 1)")

    # Check 8.2 - 费米子反对易关系 Fermion anticommutator
    anticomm = fermion_anticommutator()
    if anticomm['{c, c†}'] != 1:
        print("X 8.2 错误：费米子反对易关系应满足 {c, c†} = 1")
        all_passed = False
    else:
        print("V 8.2 费米子算符正确 ({c, c†} = 1)")

    # Check 8.3 - 产生湮灭算符矩阵 Creation/annihilation matrices
    n_max = 5
    a = boson_annihilation_matrix(n_max)
    a_dag = boson_creation_matrix(n_max)

    # 验证 [a, a†] = 1（在有限截断内）
    commutator = a @ a_dag - a_dag @ a
    if not np.allclose(commutator, np.eye(n_max + 1)):
        print("X 8.3 错误：矩阵形式的对易关系 [a, a†] 应等于单位矩阵")
        all_passed = False
    else:
        print("V 8.3 多模系统正确（矩阵对易关系验证通过）")

    # Check 8.4 - 相干态 Coherent state
    alpha = 2
    coeffs = coherent_state(alpha, 20)
    props = coherent_state_properties(alpha)

    # 计算平均粒子数 ⟨n⟩ = Σ n |c_n|²
    n_mean_calc = sum(n * np.abs(coeffs[n])**2 for n in range(len(coeffs)))

    if not np.isclose(n_mean_calc, props['mean_n'], rtol=0.05):
        print("X 8.4 错误：相干态平均粒子数应为 |α|²")
        all_passed = False
    else:
        print(f"V 8.4 谐振子二次量子化正确 (⟨n⟩ = {n_mean_calc:.2f} ≈ |α|² = {props['mean_n']:.2f})")

    # Check 8.5 - 量子统计分布 Statistics
    T = 300  # 室温
    mu = 0   # 化学势
    epsilon = 0.1 * eV  # 能量

    n_be = bose_einstein_distribution(epsilon, mu, T)
    n_fd = fermi_dirac_distribution(epsilon, mu, T)

    if n_be < 0 or n_fd < 0 or n_fd > 1:
        print("X 8.5 错误：玻色分布应 ≥ 0，费米分布应在 [0,1] 范围内")
        all_passed = False
    else:
        print(f"V 8.5 量子统计正确 (n_BE = {n_be:.3f}, n_FD = {n_fd:.3f})")

    # Check 8.6 - 场算符 Field operators
    comm_str = field_commutator_boson()
    if "δ" not in comm_str:
        print("X 8.6 错误：场算符对易关系应包含δ函数")
        all_passed = False
    else:
        print("V 8.6 场算符正确 ([ψ(x), ψ†(x')] = δ(x-x'))")

    if all_passed:
        print("\n所有测试通过！正在生成可视化...")
        try:
            plot_second_quantization()
        except Exception as ex:
            print(f"可视化生成失败: {ex}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("二次量子化基础 Second Quantization")
    print("=" * 50)
    verify()
