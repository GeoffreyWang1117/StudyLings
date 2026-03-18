"""
全同粒子与对称性 Identical Particles and Symmetry
难度 Difficulty: ★★★★

物理背景 Physical Background:
--------------------------
在量子力学中，全同粒子是严格不可区分的。交换两个粒子的位置，
物理状态不能有任何可观测的改变。这导致了波函数对称性的基本要求。

1. 全同性原理 Indistinguishability Principle:
   交换算符 P₁₂ 的本征值只能是 ±1
   - 玻色子: P₁₂ψ = +ψ (对称波函数)
   - 费米子: P₁₂ψ = -ψ (反对称波函数)

2. 自旋-统计定理 Spin-Statistics Theorem:
   - 整数自旋粒子 (s = 0, 1, 2, ...) → 玻色子
   - 半整数自旋粒子 (s = 1/2, 3/2, ...) → 费米子

3. 泡利不相容原理 Pauli Exclusion Principle:
   两个费米子不能占据相同的量子态。
   这是反对称性的直接结果: 若两粒子态相同，则 ψ = -ψ = 0

4. 交换相互作用 Exchange Interaction:
   由于波函数对称性，全同粒子间存在有效的"交换力"，
   即使没有真实的力也会表现出排斥或吸引行为。

学习目标 Learning Objectives:
--------------------------
1. 理解全同粒子的对称化和反对称化波函数
2. 掌握斯莱特行列式的构造方法
3. 理解交换积分和库仑积分
4. 掌握费米-狄拉克和玻色-爱因斯坦分布
5. 了解玻色-爱因斯坦凝聚
6. 理解泡利不相容原理的应用

关键公式 Key Formulas:
---------------------
- 对称化: ψ_S = (ψ_aψ_b + ψ_bψ_a)/√2
- 反对称化: ψ_A = (ψ_aψ_b - ψ_bψ_a)/√2
- 斯莱特行列式: Ψ = (1/√N!) det[ψᵢ(rⱼ)]
- 费米-狄拉克: f(E) = 1/(exp((E-μ)/kT) + 1)
- 玻色-爱因斯坦: n(E) = 1/(exp((E-μ)/kT) - 1)
- 费米能: E_F = (ℏ²/2m)(3π²n)^(2/3)

HINT: 费米子: ψ(1,2) = -ψ(2,1)（反对称）
HINT: 玻色子: ψ(1,2) = +ψ(2,1)（对称）
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import factorial
from itertools import permutations
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import hbar, m_e, e, k_B, a_0

# I AM NOT DONE

# =============================================================================
# 练习 10.1: 波函数对称性
# Exercise 10.1: Wavefunction Symmetry
#
# 物理背景 Physical Background:
# 两个全同粒子的波函数必须满足特定的交换对称性:
# - 玻色子: 交换两粒子，波函数不变
# - 费米子: 交换两粒子，波函数变号
#
# 对于两个粒子分别占据态a和b的情况:
# - 对称态: ψ_S = (ψ_a(1)ψ_b(2) + ψ_a(2)ψ_b(1))/√2
# - 反对称态: ψ_A = (ψ_a(1)ψ_b(2) - ψ_a(2)ψ_b(1))/√2
# =============================================================================
def symmetrize_wavefunction(psi_1, psi_2):
    """
    对称化波函数（玻色子）Symmetrized wavefunction (bosons)

    ψ_S(1,2) = (1/√2)[ψ_a(1)ψ_b(2) + ψ_a(2)ψ_b(1)]

    对于玻色子（如光子、π介子、⁴He原子），波函数必须对称。
    这意味着玻色子倾向于"聚集"在相同的量子态（玻色增强）。

    参数 Parameters:
        psi_1: 第一项 ψ_a(1)ψ_b(2)
        psi_2: 第二项 ψ_a(2)ψ_b(1)

    返回 Returns:
        对称化的波函数值
    """
    return (psi_1 + psi_2) / np.sqrt(2)


def antisymmetrize_wavefunction(psi_1, psi_2):
    """
    反对称化波函数（费米子）Antisymmetrized wavefunction (fermions)

    ψ_A(1,2) = (1/√2)[ψ_a(1)ψ_b(2) - ψ_a(2)ψ_b(1)]

    对于费米子（如电子、质子、中子），波函数必须反对称。
    当 a = b 时，ψ_A = 0，这就是泡利不相容原理。

    参数 Parameters:
        psi_1: 第一项 ψ_a(1)ψ_b(2)
        psi_2: 第二项 ψ_a(2)ψ_b(1)

    返回 Returns:
        反对称化的波函数值
    """
    return (psi_1 - psi_2) / np.sqrt(2)

def exchange_parity(psi_12, psi_21):
    """
    判断交换宇称 Determine exchange parity

    通过比较 ψ(1,2) 和 ψ(2,1) 判断粒子类型:
    - ψ(1,2) = +ψ(2,1): 玻色子 (返回 +1)
    - ψ(1,2) = -ψ(2,1): 费米子 (返回 -1)
    - 其他: 非对称态 (返回 0)

    参数 Parameters:
        psi_12: ψ(r₁, r₂) 的值
        psi_21: ψ(r₂, r₁) 的值

    返回 Returns:
        +1: 玻色子
        -1: 费米子
         0: 非本征态
    """
    if np.isclose(psi_12, psi_21, rtol=0.01):
        return 1
    elif np.isclose(psi_12, -psi_21, rtol=0.01):
        return -1
    else:
        return 0  # 非本征态


# =============================================================================
# 练习 10.2: 斯莱特行列式
# Exercise 10.2: Slater Determinant
#
# 物理背景 Physical Background:
# 对于N个费米子，反对称波函数可以用行列式形式简洁表示。
# 这就是斯莱特行列式，它自动满足:
# 1. 交换任意两个粒子，波函数变号（行列式性质）
# 2. 两个粒子占据相同态时，波函数为零（泡利原理）
#
# 斯莱特行列式是多电子原子和分子计算的基础。
# =============================================================================
def slater_determinant(orbitals):
    """
    构建斯莱特行列式 Construct Slater determinant

    Ψ = (1/√N!) |ψ₁(r₁) ψ₂(r₁) ... ψ_N(r₁)|
                |ψ₁(r₂) ψ₂(r₂) ... ψ_N(r₂)|
                |...                      |
                |ψ₁(r_N) ψ₂(r_N) ... ψ_N(r_N)|

    行列式的反对称性保证了费米子波函数的正确对称性。

    参数 Parameters:
        orbitals: N×N矩阵，orbitals[i,j] = ψ_j(r_i)
                  行索引i对应粒子位置，列索引j对应轨道

    返回 Returns:
        Ψ: 归一化的斯莱特行列式值
    """
    N = orbitals.shape[0]
    det = np.linalg.det(orbitals)
    return det / np.sqrt(factorial(N))


def two_electron_antisym(psi_a, psi_b, spin_a, spin_b):
    """
    两电子反对称波函数（空间×自旋）Two-electron antisymmetric wavefunction

    总波函数 = 空间部分 × 自旋部分，必须是反对称的。

    自旋组合:
    - 单态 (S=0): 自旋反对称 → 空间对称
    - 三重态 (S=1): 自旋对称 → 空间反对称

    参数 Parameters:
        psi_a, psi_b: 空间波函数值
        spin_a, spin_b: 自旋态 (相同或不同)

    返回 Returns:
        适当对称性的空间波函数部分
    """
    if spin_a == spin_b:
        # 自旋对称（三重态）→ 空间反对称
        spatial = antisymmetrize_wavefunction(psi_a, psi_b)
    else:
        # 自旋反对称（单态）→ 空间可以对称
        spatial = symmetrize_wavefunction(psi_a, psi_b)
    return spatial


# =============================================================================
# 练习 10.3: 交换相互作用
# Exercise 10.3: Exchange Interaction
#
# 物理背景 Physical Background:
# 由于波函数对称性，全同粒子间存在有效的"交换相互作用"。
#
# 库仑积分 J (Coulomb integral):
#   描述两个电子的经典库仑排斥能。
#
# 交换积分 K (Exchange integral):
#   没有经典对应，纯粹是量子效应。
#   来源于费米子波函数的反对称性。
#
# 对于两电子系统:
#   单态能量: E_singlet = E₀ + J + K
#   三重态能量: E_triplet = E₀ + J - K
#   能量分裂: ΔE = 2K
#
# 交换相互作用是理解原子磁性、化学键的基础。
# =============================================================================
def coulomb_integral(psi_a, psi_b, r1, r2, dr):
    """
    库仑积分 Coulomb integral

    J = ∬|ψ_a(r₁)|² e²/(4πε₀|r₁-r₂|) |ψ_b(r₂)|² d³r₁d³r₂

    物理意义: 两个电子电荷分布之间的经典库仑排斥能。

    这里使用简化的一维近似进行数值积分。

    参数 Parameters:
        psi_a, psi_b: 波函数数组
        r1, r2: 位置数组 (m)
        dr: 积分步长 (m)

    返回 Returns:
        J: 库仑积分值 (J)
    """
    from utils.constants import epsilon_0
    k_e = e**2 / (4 * np.pi * epsilon_0)

    J = 0
    for i, r1i in enumerate(r1):
        for j, r2j in enumerate(r2):
            if abs(r1i - r2j) > 1e-10:
                J += abs(psi_a[i])**2 * abs(psi_b[j])**2 * k_e / abs(r1i - r2j) * dr**2
    return J

def exchange_integral(psi_a, psi_b, r1, r2, dr):
    """
    交换积分 Exchange integral

    K = ∬ψ_a*(r₁)ψ_b*(r₂) e²/(4πε₀|r₁-r₂|) ψ_a(r₂)ψ_b(r₁) d³r₁d³r₂

    物理意义:
    没有经典对应，是纯量子效应。
    来源于费米子波函数的反对称性要求。
    决定了单态-三重态的能量分裂。

    参数 Parameters:
        psi_a, psi_b: 波函数数组
        r1, r2: 位置数组 (m)
        dr: 积分步长 (m)

    返回 Returns:
        K: 交换积分值 (J)
    """
    from utils.constants import epsilon_0
    k_e = e**2 / (4 * np.pi * epsilon_0)

    K = 0
    for i, r1i in enumerate(r1):
        for j, r2j in enumerate(r2):
            if abs(r1i - r2j) > 1e-10:
                K += np.conj(psi_a[i]) * np.conj(psi_b[j]) * \
                     psi_a[j] * psi_b[i] * k_e / abs(r1i - r2j) * dr**2
    return np.real(K)

def singlet_triplet_splitting(J, K):
    """
    单态-三重态能量分裂 Singlet-triplet splitting

    E_singlet = E₀ + J + K (自旋单态，S=0)
    E_triplet = E₀ + J - K (自旋三重态，S=1)
    ΔE = E_singlet - E_triplet = 2K

    若 K > 0: 三重态能量更低（如氦原子的正氦）
    若 K < 0: 单态能量更低

    参数 Parameters:
        J: 库仑积分 (此函数中未使用，保留接口完整性)
        K: 交换积分

    返回 Returns:
        ΔE = 2K: 能量分裂 (J)
    """
    return 2 * K


# =============================================================================
# 练习 10.4: 费米-狄拉克分布
# Exercise 10.4: Fermi-Dirac Distribution
#
# 物理背景 Physical Background:
# 费米-狄拉克分布描述了热平衡下费米子的能态占据概率。
# 由于泡利不相容原理，每个量子态最多只能有一个费米子。
#
# 关键特性:
# - T=0时: E < μ 的态完全填满，E > μ 的态完全空
# - T>0时: 费米面附近有热展宽，宽度 ~ kT
# - f(μ) = 1/2 对于所有温度
#
# 应用:
# - 金属中的电子分布
# - 半导体物理
# - 白矮星、中子星的简并压
# =============================================================================
def fermi_dirac(E, mu, T):
    """
    费米-狄拉克分布 Fermi-Dirac distribution

    f(E) = 1/(exp((E-μ)/(k_BT)) + 1)

    性质:
    - f(E) ∈ [0, 1]: 表示态的占据概率
    - f(μ) = 1/2: 费米面处的占据概率
    - T → 0: 变为阶跃函数

    参数 Parameters:
        E: 能量 (J)
        mu: 化学势/费米能 (J)
        T: 温度 (K)

    返回 Returns:
        f(E): 占据概率
    """
    if T < 1e-10:
        # T=0 极限: 阶跃函数
        return 1.0 if E < mu else 0.0
    x = (E - mu) / (k_B * T)
    # 避免数值溢出
    if x > 100:
        return 0
    elif x < -100:
        return 1
    return 1 / (np.exp(x) + 1)

def fermi_energy_3d(n, m=m_e):
    """
    三维自由电子气的费米能 Fermi energy in 3D

    E_F = (ℏ²/2m)(3π²n)^(2/3)

    费米能是T=0时最高被占据态的能量。
    对于金属，E_F 通常在几eV量级。

    参数 Parameters:
        n: 电子数密度 (1/m³)
        m: 电子质量 (kg)

    返回 Returns:
        E_F: 费米能 (J)
    """
    return (hbar**2 / (2 * m)) * (3 * np.pi**2 * n)**(2/3)


def electron_density_at_T0(E_F, m=m_e):
    """
    T=0时的电子密度（费米能的逆运算）Electron density at T=0

    n = (2mE_F/ℏ²)^(3/2) / (3π²)

    参数 Parameters:
        E_F: 费米能 (J)
        m: 电子质量 (kg)

    返回 Returns:
        n: 电子数密度 (1/m³)
    """
    return (2 * m * E_F / hbar**2)**(3/2) / (3 * np.pi**2)


# =============================================================================
# 练习 10.5: 玻色-爱因斯坦分布
# Exercise 10.5: Bose-Einstein Distribution
#
# 物理背景 Physical Background:
# 玻色-爱因斯坦分布描述热平衡下玻色子的能态占据。
# 与费米子不同，任意多个玻色子可以占据同一量子态。
#
# 关键特性:
# - n(E) 可以是任意正数（无上限）
# - μ ≤ 0 对于玻色子（否则分布函数会变负）
# - 当 T → T_c 时，μ → 0，发生玻色-爱因斯坦凝聚
#
# 应用:
# - 黑体辐射（光子，μ=0）
# - 声子比热
# - 超流氦和BEC
# =============================================================================
def bose_einstein(E, mu, T):
    """
    玻色-爱因斯坦分布 Bose-Einstein distribution

    n(E) = 1/(exp((E-μ)/(k_BT)) - 1)

    性质:
    - n(E) ≥ 0: 表示平均占据数
    - 需要 E > μ 以保证 n > 0
    - 对于光子和声子，μ = 0

    参数 Parameters:
        E: 能量 (J)
        mu: 化学势 (J), 对于玻色子 μ ≤ 0
        T: 温度 (K)

    返回 Returns:
        n(E): 平均占据数
    """
    if T < 1e-10:
        return np.inf if E <= mu else 0
    x = (E - mu) / (k_B * T)
    if x > 100:
        return 0
    elif x < 0.01:
        # 小x近似，避免除以接近零的数
        return k_B * T / (E - mu) if E > mu else np.inf
    return 1 / (np.exp(x) - 1)

def bec_critical_temperature(n, m):
    """
    玻色-爱因斯坦凝聚临界温度 BEC critical temperature

    T_c = (2πℏ²/m)(n/ζ(3/2))^(2/3) / k_B

    其中 ζ(3/2) ≈ 2.612 是黎曼zeta函数。

    当 T < T_c 时，宏观数量的玻色子凝聚到基态。
    典型的实验系统:
    - 液氦-4: T_c ≈ 2.17 K
    - 稀释碱金属气体: T_c ~ nK

    参数 Parameters:
        n: 玻色子数密度 (1/m³)
        m: 玻色子质量 (kg)

    返回 Returns:
        T_c: 临界温度 (K)
    """
    zeta_3_2 = 2.612  # ζ(3/2)
    T_c = (2 * np.pi * hbar**2 / m) * (n / zeta_3_2)**(2/3) / k_B
    return T_c


def condensate_fraction(T, T_c):
    """
    凝聚体分数 Condensate fraction

    N₀/N = 1 - (T/T_c)^(3/2)

    表示基态中粒子数占总粒子数的比例。
    - T = 0: N₀/N = 1 (全部凝聚)
    - T = T_c: N₀/N = 0 (凝聚消失)

    参数 Parameters:
        T: 温度 (K)
        T_c: 临界温度 (K)

    返回 Returns:
        N₀/N: 凝聚分数 (0到1之间)
    """
    if T >= T_c:
        return 0
    return 1 - (T / T_c)**(3/2)


# =============================================================================
# 练习 10.6: 泡利不相容原理
# Exercise 10.6: Pauli Exclusion Principle
#
# 物理背景 Physical Background:
# 泡利不相容原理是费米子反对称性的直接结果:
# 两个全同费米子不能占据完全相同的量子态。
#
# 重要后果:
# 1. 原子结构: 电子按能级依次填充，形成壳层结构
# 2. 元素周期表: 化学性质的周期性来自电子壳层的填充规律
# 3. 简并压: 即使在绝对零度，费米子也不能全部塌缩到基态
#    这阻止了白矮星和中子星的引力坍缩
# =============================================================================
def max_electrons_in_shell(n):
    """
    壳层n中最多电子数 Maximum electrons in shell n

    N_max = 2n²

    其中:
    - n²: 轨道简并度（l从0到n-1，每个l有2l+1个m值）
    - 2: 自旋简并度（ms = ±1/2）

    例如:
    - n=1: 2个电子 (1s²)
    - n=2: 8个电子 (2s² 2p⁶)
    - n=3: 18个电子 (3s² 3p⁶ 3d¹⁰)

    参数 Parameters:
        n: 主量子数

    返回 Returns:
        N_max: 最大电子数
    """
    return 2 * n**2


def electron_configuration(Z):
    """
    基态电子组态（简化）Ground state electron configuration

    按照能量从低到高依次填充轨道。
    轨道填充顺序（近似）: 1s, 2s, 2p, 3s, 3p, 4s, 3d, 4p, ...

    参数 Parameters:
        Z: 原子序数（核电荷数）

    返回 Returns:
        config: 字典，键为轨道名，值为电子数
    """
    # 轨道顺序（近似）
    orbitals = ['1s', '2s', '2p', '3s', '3p', '4s', '3d', '4p', '5s', '4d', '5p']
    max_electrons = [2, 2, 6, 2, 6, 2, 10, 6, 2, 10, 6]

    config = {}
    remaining = Z
    for orb, max_e in zip(orbitals, max_electrons):
        if remaining <= 0:
            break
        electrons = min(remaining, max_e)
        if electrons > 0:
            config[orb] = electrons
        remaining -= electrons

    return config

def degeneracy_pressure(n, m=m_e):
    """
    费米简并压 Fermi degeneracy pressure

    P = (2/5)(3π²)^(2/3) (ℏ²/m) n^(5/3)

    这是零温度下费米气体的压强，完全由量子效应产生。
    即使没有热运动，泡利不相容原理也阻止费米子全部塌缩到基态，
    形成一个具有动能的费米海，产生压强。

    应用:
    - 白矮星: 电子简并压对抗引力
    - 中子星: 中子简并压对抗引力
    - 金属中的电子压强

    参数 Parameters:
        n: 费米子数密度 (1/m³)
        m: 费米子质量 (kg)

    返回 Returns:
        P: 简并压 (Pa)
    """
    return (2/5) * (3 * np.pi**2)**(2/3) * (hbar**2 / m) * n**(5/3)


# =============================================================================
# 可视化
# =============================================================================
def plot_identical_particles():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 对称vs反对称波函数
    ax1 = axes[0, 0]
    x = np.linspace(-5, 5, 200)

    psi_a = np.exp(-0.5*(x-1)**2)
    psi_b = np.exp(-0.5*(x+1)**2)

    psi_sym = (psi_a + psi_b) / np.sqrt(2)
    psi_anti = (psi_a - psi_b) / np.sqrt(2)

    ax1.plot(x, psi_a, 'b--', alpha=0.5, label='ψ_a')
    ax1.plot(x, psi_b, 'r--', alpha=0.5, label='ψ_b')
    ax1.plot(x, psi_sym, 'g-', linewidth=2, label='对称')
    ax1.plot(x, psi_anti, 'm-', linewidth=2, label='反对称')
    ax1.set_xlabel('x')
    ax1.set_ylabel('ψ')
    ax1.set_title('波函数对称化')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 费米-狄拉克分布
    ax2 = axes[0, 1]
    E_F = 1  # 归一化
    E = np.linspace(0, 3*E_F, 200)

    for T_ratio in [0.01, 0.1, 0.5, 1]:
        T = T_ratio * E_F / k_B
        f = [fermi_dirac(Ei, E_F, T) for Ei in E]
        ax2.plot(E/E_F, f, label=f'T = {T_ratio}E_F/k_B', linewidth=2)

    ax2.axvline(x=1, color='k', linestyle='--', alpha=0.5)
    ax2.set_xlabel('E/E_F')
    ax2.set_ylabel('f(E)')
    ax2.set_title('费米-狄拉克分布')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 玻色-爱因斯坦分布
    ax3 = axes[0, 2]
    E = np.linspace(0.01, 5, 200)

    for T in [0.5, 1, 2]:
        # μ = 0 for photons
        n_BE = [bose_einstein(Ei, 0, T) for Ei in E]
        ax3.plot(E, n_BE, label=f'k_BT = {T}', linewidth=2)

    ax3.set_xlabel('E')
    ax3.set_ylabel('n(E)')
    ax3.set_title('玻色-爱因斯坦分布 (μ=0)')
    ax3.set_ylim(0, 10)
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 交换能vs距离
    ax4 = axes[1, 0]
    # 简化模型
    R = np.linspace(0.5, 5, 100)
    K_model = np.exp(-R) * (1 + R)  # 氢分子型

    ax4.plot(R, K_model, 'b-', linewidth=2)
    ax4.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    ax4.set_xlabel('原子间距 R (a_0)')
    ax4.set_ylabel('交换积分 K (arb.)')
    ax4.set_title('交换相互作用')
    ax4.grid(True, alpha=0.3)

    # 5. BEC凝聚分数
    ax5 = axes[1, 1]
    T_ratio = np.linspace(0, 1.5, 100)
    N0_N = [condensate_fraction(Ti, 1) for Ti in T_ratio]

    ax5.plot(T_ratio, N0_N, 'b-', linewidth=2)
    ax5.axvline(x=1, color='r', linestyle='--', label='T_c')
    ax5.set_xlabel('T/T_c')
    ax5.set_ylabel('N₀/N')
    ax5.set_title('BEC凝聚分数')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. 壳层填充
    ax6 = axes[1, 2]
    n_shells = [1, 2, 3, 4]
    electrons = [max_electrons_in_shell(n) for n in n_shells]
    cumulative = np.cumsum(electrons)

    ax6.bar(n_shells, electrons, alpha=0.7, label='每壳层电子数')
    ax6.plot(n_shells, cumulative, 'ro-', linewidth=2, label='累积电子数')
    ax6.set_xlabel('壳层 n')
    ax6.set_ylabel('电子数')
    ax6.set_title('壳层填充（泡利原理）')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('identical_particles.png', dpi=150)
    print("图像已保存为 identical_particles.png")
    plt.show()


def verify():
    all_passed = True

    # Check 10.1
    psi_1 = 1
    psi_2 = 0
    psi_sym = symmetrize_wavefunction(psi_1, psi_2)
    psi_anti = antisymmetrize_wavefunction(psi_1, psi_2)
    if not np.isclose(psi_sym, 1/np.sqrt(2), rtol=0.01):
        print("❌ 10.1 对称化错误")
        all_passed = False
    else:
        print(f"✓ 10.1 波函数对称性正确")

    # Check 10.2
    orbitals = np.array([[1, 0], [0, 1]])
    det = slater_determinant(orbitals)
    if not np.isclose(abs(det), 1/np.sqrt(2), rtol=0.01):
        print("❌ 10.2 斯莱特行列式错误")
        all_passed = False
    else:
        print(f"✓ 10.2 斯莱特行列式正确")

    # Check 10.3
    delta_E = singlet_triplet_splitting(1, 0.5)
    if delta_E != 1:
        print("❌ 10.3 单态-三重态分裂错误")
        all_passed = False
    else:
        print(f"✓ 10.3 交换相互作用正确")

    # Check 10.4
    f_half = fermi_dirac(1, 1, 1e10)
    if not np.isclose(f_half, 0.5, rtol=0.01):
        print("❌ 10.4 E=μ时f应为0.5")
        all_passed = False
    else:
        n = 1e28
        E_F = fermi_energy_3d(n)
        print(f"✓ 10.4 费米-狄拉克分布正确 (E_F = {E_F/e:.2f} eV)")

    # Check 10.5
    T_c = bec_critical_temperature(1e20, 87*1.67e-27)  # Rb-87
    if T_c <= 0:
        print("❌ 10.5 BEC临界温度应为正")
        all_passed = False
    else:
        print(f"✓ 10.5 玻色-爱因斯坦分布正确 (T_c ≈ {T_c*1e9:.1f} nK)")

    # Check 10.6
    max_2 = max_electrons_in_shell(2)
    if max_2 != 8:
        print("❌ 10.6 n=2壳层应容纳8个电子")
        all_passed = False
    else:
        config = electron_configuration(26)  # Fe
        print(f"✓ 10.6 泡利原理正确 (Fe配置: {config})")

    if all_passed:
        print("\n🎉 所有测试通过！")
        try:
            plot_identical_particles()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("全同粒子与对称性 Identical Particles and Symmetry")
    print("=" * 50)
    verify()
