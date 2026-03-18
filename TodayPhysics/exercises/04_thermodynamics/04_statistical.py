"""
统计物理 Statistical Physics
难度 Difficulty: ★★★★★

学习目标 Learning Objectives:
- 理解配分函数的物理意义及其作为热力学桥梁的角色
  Understand the physical meaning of partition function as a bridge to thermodynamics
- 掌握玻尔兹曼分布及其应用
  Master Boltzmann distribution and its applications
- 分析费米-狄拉克和玻色-爱因斯坦统计的区别
  Analyze differences between Fermi-Dirac and Bose-Einstein statistics
- 计算系统的各种热力学量
  Calculate various thermodynamic quantities of systems
- 理解量子谐振子和二能级系统的统计行为
  Understand statistical behavior of quantum harmonic oscillator and two-level systems

物理背景 Physical Background:
统计物理是连接微观力学和宏观热力学的理论框架。其核心思想是：
宏观可观测量是微观态的统计平均。

配分函数 Z 是统计物理中最重要的量，它包含了系统的全部热力学信息。
通过对 Z 求导，可以得到所有热力学量（能量、熵、自由能等）。

HINT: 配分函数: Z = Σᵢ exp(-Eᵢ/kT) = Σᵢ exp(-βEᵢ)，β = 1/(kT)
HINT: 玻尔兹曼概率: Pᵢ = exp(-Eᵢ/kT)/Z = gᵢ exp(-βEᵢ)/Z
HINT: 亥姆霍兹自由能: F = -kT ln(Z)
HINT: 平均能量: <E> = -∂(lnZ)/∂β = kT² ∂(lnZ)/∂T
HINT: 熵: S = k[lnZ + β<E>] = -∂F/∂T
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import k_B, h, hbar, m_e, eV

# I AM NOT DONE

# =============================================================================
# 练习 4.1: 配分函数
# Exercise 4.1: Partition Function
# =============================================================================
# 配分函数是统计力学的核心 Partition function is the heart of statistical mechanics
#
# 定义 Definition:
#   Z = Σᵢ exp(-Eᵢ/kT) = Σᵢ exp(-βEᵢ)
#   其中 β = 1/(kT) 是逆温度
#
# 如果能级有简并度 If energy levels have degeneracy:
#   Z = Σᵢ gᵢ exp(-Eᵢ/kT)
#   其中 gᵢ 是能级 Eᵢ 的简并度
#
# 配分函数的物理意义 Physical meaning:
#   Z 可以理解为系统"有效"可达态的数目
#   高温时更多态参与，Z 增大

def partition_function_discrete(energies, T):
    """
    离散能级的配分函数 Partition function for discrete energy levels

    公式 Formula: Z = Σᵢ exp(-Eᵢ/kT)

    参数 Parameters:
        energies: 能级列表 (J) - List of energy levels
        T: 温度 (K) - Temperature

    返回 Returns:
        Z: 配分函数（无量纲）- Partition function (dimensionless)

    注意 Note:
        能量的零点选取不影响热力学量的计算（只影响 Z 的绝对值）
    """
    # TODO: 计算配分函数（对所有能级求和）
    # TODO: Calculate partition function (sum over all energy levels)
    beta = 1 / (k_B * T)
    Z = np.sum(np.exp(-beta * np.array(energies)))
    return Z


def partition_function_with_degeneracy(energies, degeneracies, T):
    """
    考虑简并度的配分函数 Partition function with degeneracy

    公式 Formula: Z = Σᵢ gᵢ exp(-Eᵢ/kT)

    参数 Parameters:
        energies: 能级列表 (J) - List of energy levels
        degeneracies: 各能级的简并度列表 - List of degeneracies
        T: 温度 (K) - Temperature

    返回 Returns:
        Z: 配分函数 - Partition function

    示例 Example:
        氢原子 n=2 能级有 g=4 的简并度（2s + 三个 2p）
    """
    beta = 1 / (k_B * T)
    # TODO: 计算含简并度的配分函数
    # TODO: Calculate partition function including degeneracy
    Z = np.sum(np.array(degeneracies) * np.exp(-beta * np.array(energies)))
    return Z


def boltzmann_probability(E, T, Z):
    """
    玻尔兹曼概率分布 Boltzmann probability distribution

    公式 Formula: P(E) = exp(-E/kT) / Z

    参数 Parameters:
        E: 能量 (J) - Energy
        T: 温度 (K) - Temperature
        Z: 配分函数 - Partition function

    返回 Returns:
        P: 系统处于能量 E 的概率 - Probability of the system being at energy E

    物理意义 Physical meaning:
        高能态概率小（指数衰减），低能态概率大
        温度越高，高能态被占据的概率越大
    """
    beta = 1 / (k_B * T)
    # TODO: 计算玻尔兹曼概率
    # TODO: Calculate Boltzmann probability
    P = np.exp(-beta * E) / Z
    return P


# =============================================================================
# 练习 4.2: 热力学量从配分函数
# Exercise 4.2: Thermodynamic Quantities from Z
# =============================================================================
# 配分函数与热力学 Partition Function and Thermodynamics:
#
# 配分函数包含了系统的全部热力学信息，所有热力学量都可以从 Z 推导出来
#
# 关键公式 Key Formulas:
#   亥姆霍兹自由能: F = -kT ln(Z)
#   平均能量: <E> = -∂(lnZ)/∂β = kT² ∂(lnZ)/∂T
#   熵: S = k[ln(Z) + β<E>] = (E - F)/T = -∂F/∂T
#   热容: C_V = ∂<E>/∂T = <ΔE²>/(kT²)
#
# 涨落-耗散关系 Fluctuation-Dissipation:
#   热容与能量涨落相关: C_V = (<E²> - <E>²) / (kT²)
#   这是统计物理中普遍存在的涨落-响应联系

def free_energy_from_Z(Z, T):
    """
    从配分函数计算亥姆霍兹自由能 Helmholtz free energy from partition function

    公式 Formula: F = -kT ln(Z)

    参数 Parameters:
        Z: 配分函数（无量纲）- Partition function
        T: 温度 (K) - Temperature

    返回 Returns:
        F: 亥姆霍兹自由能 (J) - Helmholtz free energy

    物理意义 Physical Meaning:
        F 是恒温恒容条件下系统可做的最大功
        自发过程总使 F 减小
    """
    # TODO: 计算自由能
    # TODO: Calculate free energy
    F = -k_B * T * np.log(Z)
    return F


def average_energy_from_Z(energies, T, Z=None):
    """
    从配分函数计算平均能量 Average energy from partition function

    公式 Formula: <E> = Σᵢ Eᵢ Pᵢ = -∂(lnZ)/∂β

    参数 Parameters:
        energies: 能级列表 (J) - List of energy levels
        T: 温度 (K) - Temperature
        Z: 配分函数（可选，若不提供则自动计算）

    返回 Returns:
        E_avg: 平均能量 (J) - Average energy

    注意 Note:
        高温极限：<E> 趋向于所有能级的算术平均
        低温极限：<E> 趋向于基态能量
    """
    if Z is None:
        Z = partition_function_discrete(energies, T)
    beta = 1 / (k_B * T)
    # TODO: 计算平均能量（加权平均）
    # TODO: Calculate average energy (weighted average)
    probs = np.exp(-beta * np.array(energies)) / Z
    E_avg = np.sum(np.array(energies) * probs)
    return E_avg


def entropy_from_Z(Z, T, E_avg):
    """
    从配分函数计算熵 Entropy from partition function

    公式 Formula: S = (E - F)/T = k[ln(Z) + β<E>]

    参数 Parameters:
        Z: 配分函数 - Partition function
        T: 温度 (K) - Temperature
        E_avg: 平均能量 (J) - Average energy

    返回 Returns:
        S: 熵 (J/K) - Entropy

    物理意义 Physical Meaning:
        熵反映系统微观状态数：S = k ln(W)
        高温时更多态被占据，熵增大
    """
    F = free_energy_from_Z(Z, T)
    # TODO: 计算熵
    # TODO: Calculate entropy
    S = (E_avg - F) / T
    return S


def heat_capacity_from_energy_variance(energies, T, Z=None):
    """
    从能量涨落计算热容 Heat capacity from energy variance

    公式 Formula: C_V = (<E²> - <E>²) / (kT²) = <ΔE²> / (kT²)

    参数 Parameters:
        energies: 能级列表 (J) - List of energy levels
        T: 温度 (K) - Temperature
        Z: 配分函数（可选）

    返回 Returns:
        C_V: 定容热容 (J/K) - Heat capacity at constant volume

    物理意义 Physical Meaning:
        热容越大，能量涨落越大
        这是涨落-耗散定理的一个实例
    """
    if Z is None:
        Z = partition_function_discrete(energies, T)
    beta = 1 / (k_B * T)
    probs = np.exp(-beta * np.array(energies)) / Z

    E_avg = np.sum(np.array(energies) * probs)
    E2_avg = np.sum(np.array(energies)**2 * probs)
    variance = E2_avg - E_avg**2

    # TODO: 计算热容
    # TODO: Calculate heat capacity
    C_V = variance / (k_B * T**2)
    return C_V


# =============================================================================
# 练习 4.3: 谐振子配分函数
# Exercise 4.3: Harmonic Oscillator Partition Function
# =============================================================================
# 量子谐振子 Quantum Harmonic Oscillator:
#
# 能级 Energy Levels: Eₙ = ℏω(n + 1/2), n = 0, 1, 2, ...
#   - 零点能 Zero-point energy: E₀ = ℏω/2（量子效应）
#   - 能级等间距，间隔为 ℏω
#
# 配分函数（几何级数求和）Partition Function (geometric series):
#   Z = Σₙ exp(-βℏω(n + 1/2)) = exp(-βℏω/2) / (1 - exp(-βℏω))
#
# 爱因斯坦模型 Einstein Model:
#   固体热容的量子模型，将晶格振动视为独立的量子谐振子
#   低温时热容 ~ exp(-ℏω/kT) → 0（解释了热容的低温"冻结"）
#   高温时热容 → k（杜隆-珀替定律）

def quantum_harmonic_oscillator_Z(omega, T, n_max=100):
    """
    量子谐振子配分函数 Partition function of quantum harmonic oscillator

    公式 Formula: Z = exp(-βℏω/2) / (1 - exp(-βℏω))

    参数 Parameters:
        omega: 角频率 (rad/s) - Angular frequency
        T: 温度 (K) - Temperature
        n_max: （未使用，精确公式无需截断）

    返回 Returns:
        Z: 配分函数 - Partition function

    极限行为 Limiting Behavior:
        高温 (kT >> ℏω): Z ≈ kT/(ℏω)
        低温 (kT << ℏω): Z ≈ exp(-ℏω/2kT)
    """
    beta = 1 / (k_B * T)
    # TODO: 计算配分函数（精确公式，几何级数求和）
    # TODO: Calculate partition function (exact formula, geometric series)
    x = beta * hbar * omega
    Z = np.exp(-x/2) / (1 - np.exp(-x))
    return Z


def quantum_ho_average_energy(omega, T):
    """
    量子谐振子平均能量 Average energy of quantum harmonic oscillator

    公式 Formula: <E> = ℏω(1/2 + n̄)，其中 n̄ = 1/(exp(βℏω) - 1)

    参数 Parameters:
        omega: 角频率 (rad/s) - Angular frequency
        T: 温度 (K) - Temperature

    返回 Returns:
        E_avg: 平均能量 (J) - Average energy

    物理意义 Physical Meaning:
        n̄ 是平均量子数（玻色分布），表示平均激发的声子数
        零点能 ℏω/2 在任何温度下都存在
    """
    beta = 1 / (k_B * T)
    x = beta * hbar * omega
    # TODO: 计算平均能量
    # TODO: Calculate average energy
    n_avg = 1 / (np.exp(x) - 1)  # 平均量子数（玻色分布）
    E_avg = hbar * omega * (0.5 + n_avg)
    return E_avg


def quantum_ho_heat_capacity(omega, T):
    """
    量子谐振子热容（爱因斯坦模型）Heat capacity (Einstein model)

    公式 Formula: C = k × (ℏω/kT)² × exp(ℏω/kT) / (exp(ℏω/kT) - 1)²

    参数 Parameters:
        omega: 角频率 (rad/s) - Angular frequency
        T: 温度 (K) - Temperature

    返回 Returns:
        C: 热容 (J/K) - Heat capacity

    爱因斯坦温度 Einstein Temperature:
        T_E = ℏω/k，特征温度
        T >> T_E: C → k（经典极限）
        T << T_E: C ∝ exp(-T_E/T) → 0（量子"冻结"）
    """
    beta = 1 / (k_B * T)
    x = beta * hbar * omega
    # TODO: 计算热容
    # TODO: Calculate heat capacity
    C = k_B * x**2 * np.exp(x) / (np.exp(x) - 1)**2
    return C


# =============================================================================
# 练习 4.4: 费米-狄拉克统计
# Exercise 4.4: Fermi-Dirac Statistics
# =============================================================================
# 费米-狄拉克统计 Fermi-Dirac Statistics:
#
# 适用于费米子（自旋为半整数的粒子）：电子、质子、中子、夸克等
# 费米子遵守泡利不相容原理：每个量子态最多容纳一个粒子
#
# 费米-狄拉克分布 Fermi-Dirac Distribution:
#   f(E) = 1 / (exp((E-μ)/kT) + 1)
#   - μ: 化学势，T=0 时即为费米能 E_F
#   - 在 E = μ 处，f = 0.5
#   - T → 0: f 变成阶跃函数（E < E_F 时 f=1，E > E_F 时 f=0）
#
# 费米能 Fermi Energy:
#   E_F = (ℏ²/2m)(3π²n)^(2/3)
#   典型金属的 E_F ≈ 1-10 eV，对应费米温度 T_F ≈ 10⁴-10⁵ K

def fermi_dirac_distribution(E, mu, T):
    """
    费米-狄拉克分布 Fermi-Dirac distribution

    公式 Formula: f(E) = 1 / (exp((E-μ)/kT) + 1)

    参数 Parameters:
        E: 能量 (J) - Energy
        mu: 化学势 (J) - Chemical potential (Fermi energy at T=0)
        T: 温度 (K) - Temperature

    返回 Returns:
        f: 占据概率 (0 到 1 之间) - Occupation probability

    特点 Characteristics:
        - f(E=μ) = 0.5（在化学势处概率恰好为 1/2）
        - E << μ: f → 1（态被占据）
        - E >> μ: f → 0（态空置）
        - T → 0: 变成阶跃函数
    """
    if T == 0:
        return np.where(E < mu, 1.0, 0.0)
    # TODO: 计算费米-狄拉克分布
    # TODO: Calculate Fermi-Dirac distribution
    beta = 1 / (k_B * T)
    f = 1 / (np.exp(beta * (E - mu)) + 1)
    return f


def fermi_energy_3d(n):
    """
    三维自由电子气的费米能 Fermi energy of 3D free electron gas

    公式 Formula: E_F = (ℏ²/2m)(3π²n)^(2/3)

    参数 Parameters:
        n: 电子数密度 (m⁻³) - Electron number density

    返回 Returns:
        E_F: 费米能 (J) - Fermi energy

    典型值 Typical Values:
        铜: n ≈ 8.5×10²⁸ m⁻³, E_F ≈ 7.0 eV
        金: n ≈ 5.9×10²⁸ m⁻³, E_F ≈ 5.5 eV
    """
    # TODO: 计算费米能
    # TODO: Calculate Fermi energy
    E_F = (hbar**2 / (2 * m_e)) * (3 * np.pi**2 * n)**(2/3)
    return E_F


def density_of_states_3d(E, V, m=m_e):
    """
    三维自由电子气的态密度 Density of states for 3D free electron gas

    公式 Formula: g(E) = (V/2π²) × (2m/ℏ²)^(3/2) × √E

    参数 Parameters:
        E: 能量 (J) - Energy
        V: 体积 (m³) - Volume
        m: 粒子质量 (kg)，默认为电子质量

    返回 Returns:
        g: 态密度 (J⁻¹)，单位能量间隔内的量子态数

    物理意义 Physical Meaning:
        态密度 g(E) dE 表示能量在 [E, E+dE] 范围内的量子态数目
        g(E) ∝ √E 反映了三维动量空间的几何
    """
    if E < 0:
        return 0
    # TODO: 计算态密度
    # TODO: Calculate density of states
    prefactor = V / (2 * np.pi**2) * (2 * m / hbar**2)**(3/2)
    g = prefactor * np.sqrt(E)
    return g


def electron_number_integral(mu, T, V, E_max=10*eV, n_points=1000):
    """
    积分计算电子总数 Calculate total electron number by integration

    公式 Formula: N = ∫₀^∞ g(E) f(E) dE

    参数 Parameters:
        mu: 化学势 (J) - Chemical potential
        T: 温度 (K) - Temperature
        V: 体积 (m³) - Volume
        E_max: 积分上限 (J) - Upper limit of integration
        n_points: 积分点数 - Number of integration points

    返回 Returns:
        N: 电子总数 - Total number of electrons

    应用 Application:
        通过调节 μ 使计算的 N 等于实际电子数，可求出有限温度下的化学势
    """
    E = np.linspace(1e-10, E_max, n_points)
    g = np.array([density_of_states_3d(e, V) for e in E])
    f = fermi_dirac_distribution(E, mu, T)
    # TODO: 数值积分计算电子总数
    # TODO: Numerical integration for total electron number
    N = np.trapz(g * f, E)
    return N


# =============================================================================
# 练习 4.5: 玻色-爱因斯坦统计
# Exercise 4.5: Bose-Einstein Statistics
# =============================================================================
# 玻色-爱因斯坦统计 Bose-Einstein Statistics:
#
# 适用于玻色子（自旋为整数的粒子）：光子、声子、介子、原子（整数自旋）
# 玻色子不遵守泡利不相容原理：每个量子态可容纳任意多个粒子
#
# 玻色-爱因斯坦分布 Bose-Einstein Distribution:
#   n(E) = 1 / (exp((E-μ)/kT) - 1)
#   - μ ≤ 0（否则基态占据数会发散）
#   - 光子和声子: μ = 0（粒子数不守恒）
#
# 玻色-爱因斯坦凝聚 (BEC) Bose-Einstein Condensation:
#   当 T < T_c 时，宏观数量的粒子凝聚到基态
#   凝聚比例: N₀/N = 1 - (T/T_c)^(3/2)

def bose_einstein_distribution(E, mu, T):
    """
    玻色-爱因斯坦分布 Bose-Einstein distribution

    公式 Formula: n(E) = 1 / (exp((E-μ)/kT) - 1)

    参数 Parameters:
        E: 能量 (J) - Energy
        mu: 化学势 (J)，对于光子 μ = 0 - Chemical potential
        T: 温度 (K) - Temperature

    返回 Returns:
        n: 平均占据数（可大于1）- Average occupation number

    注意 Note:
        - 必须有 E > μ，否则占据数为负（非物理）
        - μ → 0⁻ 且 E → 0 时，n → ∞，这是 BEC 的前兆
    """
    if T == 0:
        raise ValueError("温度为零时玻色-爱因斯坦分布在基态发散")
    beta = 1 / (k_B * T)
    # TODO: 计算玻色-爱因斯坦分布
    # TODO: Calculate Bose-Einstein distribution
    n = 1 / (np.exp(beta * (E - mu)) - 1)
    return n


def planck_distribution(nu, T):
    """
    普朗克黑体辐射分布 Planck black body radiation distribution

    公式 Formula: u(ν) = (8πhν³/c³) / (exp(hν/kT) - 1)

    参数 Parameters:
        nu: 频率 (Hz) - Frequency
        T: 温度 (K) - Temperature

    返回 Returns:
        u: 能量密度 (J/m³/Hz) - Spectral energy density

    相关定律 Related Laws:
        - 维恩位移定律: λ_max T = 2.898 × 10⁻³ m·K
        - 斯特藩-玻尔兹曼定律: P = σT⁴ (σ = 5.67 × 10⁻⁸ W/m²·K⁴)
    """
    from utils.constants import c
    if T <= 0:
        return 0
    x = h * nu / (k_B * T)
    # TODO: 计算能量密度
    # TODO: Calculate energy density
    prefactor = 8 * np.pi * h * nu**3 / c**3
    u = prefactor / (np.exp(x) - 1)
    return u


def bec_critical_temperature(n, m):
    """
    玻色-爱因斯坦凝聚临界温度 BEC critical temperature

    公式 Formula: T_c = (2πℏ²/mk_B)(n/ζ(3/2))^(2/3)

    参数 Parameters:
        n: 粒子数密度 (m⁻³) - Particle number density
        m: 粒子质量 (kg) - Particle mass

    返回 Returns:
        T_c: 临界温度 (K) - Critical temperature

    典型值 Typical Values:
        ⁸⁷Rb 原子气体: n ≈ 10²⁰ m⁻³, T_c ≈ 100 nK
        液氦(⁴He): T_λ ≈ 2.17 K（与理论值有偏差，因相互作用）

    ζ(3/2) ≈ 2.612 是黎曼 zeta 函数
    """
    zeta_3_2 = 2.612375  # ζ(3/2)
    # TODO: 计算 BEC 临界温度
    # TODO: Calculate BEC critical temperature
    T_c = (2 * np.pi * hbar**2 / (m * k_B)) * (n / zeta_3_2)**(2/3)
    return T_c


def bec_condensate_fraction(T, T_c):
    """
    BEC 凝聚比例 BEC condensate fraction

    公式 Formula: N₀/N = 1 - (T/T_c)^(3/2), T < T_c

    参数 Parameters:
        T: 温度 (K) - Temperature
        T_c: 临界温度 (K) - Critical temperature

    返回 Returns:
        fraction: 凝聚到基态的粒子比例 - Fraction of particles in ground state

    物理意义 Physical Meaning:
        T < T_c 时，有宏观数量的粒子占据基态（零动量态）
        T → 0 时，几乎所有粒子都在基态
        T → T_c⁻ 时，凝聚比例 → 0
    """
    if T >= T_c:
        return 0
    # TODO: 计算凝聚比例
    # TODO: Calculate condensate fraction
    fraction = 1 - (T / T_c)**(3/2)
    return fraction


# =============================================================================
# 练习 4.6: 麦克斯韦-玻尔兹曼分布
# Exercise 4.6: Maxwell-Boltzmann Distribution
# =============================================================================
# 麦克斯韦-玻尔兹曼速率分布 Maxwell-Boltzmann Speed Distribution:
#
# 描述理想气体分子速率的统计分布（经典极限）
#
# 分布函数 Distribution Function:
#   f(v) = 4π(m/2πkT)^(3/2) × v² exp(-mv²/2kT)
#
# 三种特征速率 Three Characteristic Speeds:
#   1. 最概然速率 v_p = √(2kT/m)（分布峰值位置）
#   2. 平均速率 <v> = √(8kT/πm) ≈ 1.128 v_p
#   3. 均方根速率 v_rms = √(3kT/m) ≈ 1.225 v_p
#
# 关系: v_p < <v> < v_rms

def maxwell_boltzmann_speed(v, m, T):
    """
    麦克斯韦-玻尔兹曼速率分布 Maxwell-Boltzmann speed distribution

    公式 Formula: f(v) = 4π(m/2πkT)^(3/2) × v² × exp(-mv²/2kT)

    参数 Parameters:
        v: 速率 (m/s) - Speed
        m: 分子质量 (kg) - Molecular mass
        T: 温度 (K) - Temperature

    返回 Returns:
        f: 概率密度 (s/m) - Probability density

    归一化 Normalization:
        ∫₀^∞ f(v) dv = 1

    物理意义 Physical Meaning:
        f(v) dv 是分子速率在 [v, v+dv] 范围内的概率
    """
    # TODO: 计算麦克斯韦-玻尔兹曼速率分布
    # TODO: Calculate Maxwell-Boltzmann speed distribution
    prefactor = 4 * np.pi * (m / (2 * np.pi * k_B * T))**(3/2)
    f = prefactor * v**2 * np.exp(-m * v**2 / (2 * k_B * T))
    return f


def most_probable_speed(m, T):
    """
    最概然速率 Most probable speed

    公式 Formula: v_p = √(2kT/m)

    参数 Parameters:
        m: 分子质量 (kg) - Molecular mass
        T: 温度 (K) - Temperature

    返回 Returns:
        v_p: 最概然速率 (m/s) - Most probable speed

    物理意义 Physical Meaning:
        分布函数 f(v) 的峰值位置
        即最多分子所具有的速率
    """
    return np.sqrt(2 * k_B * T / m)


def mean_speed(m, T):
    """
    平均速率 Mean (average) speed

    公式 Formula: <v> = √(8kT/πm) ≈ 1.128 v_p

    参数 Parameters:
        m: 分子质量 (kg) - Molecular mass
        T: 温度 (K) - Temperature

    返回 Returns:
        v_mean: 平均速率 (m/s) - Mean speed

    物理意义 Physical Meaning:
        所有分子速率的算术平均值
        <v> = ∫₀^∞ v f(v) dv
    """
    return np.sqrt(8 * k_B * T / (np.pi * m))


def rms_speed(m, T):
    """
    均方根速率 Root-mean-square (RMS) speed

    公式 Formula: v_rms = √(3kT/m) = √<v²> ≈ 1.225 v_p

    参数 Parameters:
        m: 分子质量 (kg) - Molecular mass
        T: 温度 (K) - Temperature

    返回 Returns:
        v_rms: 均方根速率 (m/s) - RMS speed

    物理意义 Physical Meaning:
        与分子平均动能直接相关: <E_k> = (1/2)m<v²> = (1/2)m v_rms²
        v_rms = √<v²> = ∫₀^∞ v² f(v) dv
    """
    return np.sqrt(3 * k_B * T / m)


# =============================================================================
# 练习 4.7: 二能级系统
# Exercise 4.7: Two-Level System
# =============================================================================
# 二能级系统 Two-Level System:
#
# 最简单的量子统计模型，只有两个能级：E₀ = 0, E₁ = ε
# 例如：电子自旋在磁场中、原子的两个能级等
#
# 配分函数 Partition Function: Z = 1 + exp(-ε/kT)
#
# 平均能量: <E> = ε / (1 + exp(ε/kT))
#   - T → 0: <E> → 0（只有基态被占据）
#   - T → ∞: <E> → ε/2（两态等概率）
#
# 肖特基热容 Schottky Heat Capacity:
#   在低温和高温都趋于零，中间有峰值
#   峰值出现在 kT ≈ 0.42 ε 附近

def two_level_partition_function(epsilon, T):
    """
    二能级系统的配分函数 Partition function of two-level system

    公式 Formula: Z = 1 + exp(-ε/kT)

    参数 Parameters:
        epsilon: 激发态能量 (J) - Excited state energy
        T: 温度 (K) - Temperature

    返回 Returns:
        Z: 配分函数 - Partition function

    极限行为 Limiting Behavior:
        低温 (kT << ε): Z → 1（只有基态）
        高温 (kT >> ε): Z → 2（两态等概率）
    """
    beta = 1 / (k_B * T)
    # TODO: 计算二能级系统配分函数
    # TODO: Calculate two-level system partition function
    Z = 1 + np.exp(-beta * epsilon)
    return Z


def two_level_average_energy(epsilon, T):
    """
    二能级系统平均能量 Average energy of two-level system

    公式 Formula: <E> = ε / (1 + exp(ε/kT))

    参数 Parameters:
        epsilon: 激发态能量 (J) - Excited state energy
        T: 温度 (K) - Temperature

    返回 Returns:
        E_avg: 平均能量 (J) - Average energy

    物理意义 Physical Meaning:
        <E> = ε × P₁，其中 P₁ 是激发态的占据概率
    """
    beta = 1 / (k_B * T)
    # TODO: 计算平均能量
    # TODO: Calculate average energy
    E_avg = epsilon / (1 + np.exp(beta * epsilon))
    return E_avg


def two_level_heat_capacity(epsilon, T):
    """
    二能级系统热容（肖特基热容）Schottky heat capacity

    公式 Formula: C = k × (ε/kT)² × exp(ε/kT) / (1 + exp(ε/kT))²

    参数 Parameters:
        epsilon: 激发态能量 (J) - Excited state energy
        T: 温度 (K) - Temperature

    返回 Returns:
        C: 热容 (J/K) - Heat capacity

    特点 Characteristics:
        - 低温: C ∝ (ε/kT)² exp(-ε/kT) → 0
        - 高温: C ∝ (ε/kT)² → 0
        - 峰值在 kT ≈ 0.42ε，最大值约 0.44k

    应用 Applications:
        某些材料在低温下的热容异常（如顺磁盐）
    """
    beta = 1 / (k_B * T)
    x = beta * epsilon
    # TODO: 计算肖特基热容
    # TODO: Calculate Schottky heat capacity
    C = k_B * x**2 * np.exp(x) / (1 + np.exp(x))**2
    return C


def two_level_population_ratio(epsilon, T):
    """
    高能级与低能级的粒子数比 Population ratio of excited to ground state

    公式 Formula: N₁/N₀ = exp(-ε/kT)（玻尔兹曼因子）

    参数 Parameters:
        epsilon: 激发态能量 (J) - Excited state energy
        T: 温度 (K) - Temperature

    返回 Returns:
        ratio: N₁/N₀ 粒子数比 - Population ratio

    物理意义 Physical Meaning:
        这就是玻尔兹曼因子，描述热平衡时不同能级的相对占据数
        T → 0: ratio → 0（只有基态被占据）
        T → ∞: ratio → 1（两态等概率）
    """
    beta = 1 / (k_B * T)
    return np.exp(-beta * epsilon)


# =============================================================================
# 可视化 Visualization
# =============================================================================
# 本节绘制统计物理相关的图表:
# 1. 费米-狄拉克分布 - 展示温度对分布的影响
# 2. 麦克斯韦-玻尔兹曼速率分布 - 不同温度下的速率分布
# 3. 普朗克黑体辐射 - 不同温度下的光谱
# 4. 量子谐振子热容（爱因斯坦模型）- 量子效应导致的热容"冻结"
# 5. 二能级系统热容（肖特基热容）- 特征峰值
# 6. BEC 凝聚比例 - 低温下的宏观量子现象

def plot_statistical():
    """
    绘制统计物理相关图表 Plot statistical physics diagrams

    包含6个子图 Contains 6 subplots:
        1. 费米-狄拉克分布 Fermi-Dirac distribution
        2. 麦克斯韦-玻尔兹曼速率分布 Maxwell-Boltzmann speed distribution
        3. 普朗克黑体辐射 Planck black body radiation
        4. 爱因斯坦模型热容 Einstein model heat capacity
        5. 肖特基热容 Schottky heat capacity
        6. BEC凝聚比例 BEC condensate fraction
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    # 1. 费米-狄拉克分布（不同温度）
    ax1 = axes[0, 0]
    E_range = np.linspace(0, 2*eV, 200)
    mu = 1.0 * eV
    T_values = [300, 1000, 3000]

    for T in T_values:
        f_FD = fermi_dirac_distribution(E_range, mu, T)
        ax1.plot(E_range/eV, f_FD, label=f'FD, T={T}K', linewidth=1.5)

    ax1.axvline(x=mu/eV, color='k', linestyle='--', alpha=0.5, label='μ')
    ax1.set_xlabel('E (eV)')
    ax1.set_ylabel('f(E)')
    ax1.set_title('费米-狄拉克分布')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 麦克斯韦-玻尔兹曼速率分布
    ax2 = axes[0, 1]
    from utils.constants import m_p
    m_gas = 28 * m_p  # N2分子
    v_range = np.linspace(0, 2000, 200)

    for T in [100, 300, 600]:
        f_MB = maxwell_boltzmann_speed(v_range, m_gas, T)
        v_p = most_probable_speed(m_gas, T)
        ax2.plot(v_range, f_MB*1e3, label=f'T={T}K', linewidth=1.5)
        ax2.axvline(x=v_p, color='k', linestyle=':', alpha=0.3)

    ax2.set_xlabel('Speed (m/s)')
    ax2.set_ylabel('f(v) (×10⁻³)')
    ax2.set_title('麦克斯韦-玻尔兹曼分布 (N₂)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 普朗克黑体辐射
    ax3 = axes[0, 2]
    nu_range = np.linspace(1e12, 2e15, 500)

    for T in [3000, 4000, 5000, 6000]:
        u = [planck_distribution(nu, T) for nu in nu_range]
        ax3.plot(nu_range/1e14, np.array(u)*1e14, label=f'T={T}K', linewidth=1.5)

    ax3.set_xlabel('Frequency (×10¹⁴ Hz)')
    ax3.set_ylabel('u(ν) (×10⁻¹⁴)')
    ax3.set_title('普朗克黑体辐射')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 量子谐振子热容（爱因斯坦模型）
    ax4 = axes[1, 0]
    omega = 1e14  # rad/s
    T_range = np.linspace(10, 1000, 200)
    T_Einstein = hbar * omega / k_B  # 爱因斯坦温度

    C_quantum = [quantum_ho_heat_capacity(omega, T) / k_B for T in T_range]
    C_classical = [1.0] * len(T_range)  # 经典结果 k_B

    ax4.plot(T_range/T_Einstein, C_quantum, 'b-', label='Quantum', linewidth=2)
    ax4.plot(T_range/T_Einstein, C_classical, 'r--', label='Classical', linewidth=2)
    ax4.set_xlabel('T/T_E')
    ax4.set_ylabel('C/k_B')
    ax4.set_title('爱因斯坦模型热容')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 二能级系统热容（肖特基热容）
    ax5 = axes[1, 1]
    epsilon = 0.1 * eV
    T_range = np.linspace(100, 2000, 200)

    C_two = [two_level_heat_capacity(epsilon, T) / k_B for T in T_range]

    ax5.plot(k_B * T_range / epsilon, C_two, 'g-', linewidth=2)
    ax5.set_xlabel('kT/ε')
    ax5.set_ylabel('C/k_B')
    ax5.set_title('肖特基热容')
    ax5.grid(True, alpha=0.3)

    # 6. BEC凝聚比例
    ax6 = axes[1, 2]
    T_c = 100  # 假设临界温度
    T_range = np.linspace(1, 150, 200)

    fraction = [bec_condensate_fraction(T, T_c) for T in T_range]

    ax6.plot(T_range/T_c, fraction, 'b-', linewidth=2)
    ax6.axvline(x=1, color='r', linestyle='--', label='T_c')
    ax6.set_xlabel('T/T_c')
    ax6.set_ylabel('N₀/N')
    ax6.set_title('玻色-爱因斯坦凝聚')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('statistical_physics.png', dpi=150)
    print("图像已保存为 statistical_physics.png")
    plt.show()


def verify():
    """
    验证统计物理练习的正确性 Verify statistical physics exercises

    测试内容 Test Contents:
        - 4.1 配分函数计算
        - 4.2 玻尔兹曼概率归一化
        - 4.3 量子谐振子平均能量
        - 4.4 费米-狄拉克分布特性
        - 4.6 麦克斯韦-玻尔兹曼速率关系
        - 4.7 二能级系统配分函数
    """
    all_passed = True

    # 测试 4.1 - 配分函数 Partition function
    energies = [0, 1*eV, 2*eV]
    T = 1000
    Z = partition_function_discrete(energies, T)
    if Z <= 0:
        print("错误 4.1: 配分函数必须为正值")
        print("  提示: Z = Σ exp(-βEᵢ)，所有项都是正数")
        all_passed = False
    else:
        print(f"通过 4.1: 配分函数正确 (Z = {Z:.4f})")

    # 测试 4.2 - 概率归一化 Probability normalization
    probs = [boltzmann_probability(E, T, Z) for E in energies]
    if not np.isclose(sum(probs), 1, rtol=0.01):
        print("错误 4.2: 玻尔兹曼概率之和应为1（归一化）")
        print(f"  计算得到的概率和 = {sum(probs):.4f}")
        all_passed = False
    else:
        print(f"通过 4.2: 玻尔兹曼分布正确 (概率和 = {sum(probs):.4f})")

    # 测试 4.3 - 量子谐振子 Quantum harmonic oscillator
    omega = 1e14
    T = 500
    E_qho = quantum_ho_average_energy(omega, T)
    # 高温极限应接近 kT
    if T * k_B > hbar * omega:
        if not np.isclose(E_qho, k_B * T, rtol=0.3):
            print("错误 4.3: 量子谐振子高温极限应趋近 kT")
            print(f"  计算得到 <E> = {E_qho/eV:.4f} eV, kT = {k_B*T/eV:.4f} eV")
            all_passed = False
        else:
            print(f"通过 4.3: 量子谐振子正确 (<E> = {E_qho/eV:.4f} eV)")
    else:
        print(f"通过 4.3: 量子谐振子正确 (<E> = {E_qho/eV:.4f} eV)")

    # 测试 4.4 - 费米-狄拉克分布 Fermi-Dirac distribution
    mu = 1.0 * eV
    f_at_mu = fermi_dirac_distribution(mu, mu, T)
    if not np.isclose(f_at_mu, 0.5, rtol=0.01):
        print("错误 4.4: 费米-狄拉克分布在 E = μ 处应等于 0.5")
        print(f"  计算得到 f(μ) = {f_at_mu:.4f}")
        print("  提示: f(E) = 1/(exp((E-μ)/kT) + 1)，当 E = μ 时 f = 0.5")
        all_passed = False
    else:
        print("通过 4.4: 费米-狄拉克分布正确 (f(μ) = 0.5)")

    # 测试 4.6 - 麦克斯韦-玻尔兹曼分布 Maxwell-Boltzmann distribution
    from utils.constants import m_p
    m = 28 * m_p  # N2 分子
    T = 300
    v_p = most_probable_speed(m, T)
    v_mean = mean_speed(m, T)
    v_rms = rms_speed(m, T)
    # 应有 v_p < v_mean < v_rms
    if not (v_p < v_mean < v_rms):
        print("错误 4.6: 速率关系应满足 v_p < <v> < v_rms")
        print(f"  计算得到: v_p = {v_p:.0f}, <v> = {v_mean:.0f}, v_rms = {v_rms:.0f} m/s")
        all_passed = False
    else:
        print(f"通过 4.6: 麦克斯韦-玻尔兹曼正确 (v_p={v_p:.0f}, <v>={v_mean:.0f}, v_rms={v_rms:.0f} m/s)")

    # 测试 4.7 - 二能级系统 Two-level system
    epsilon = 0.1 * eV
    Z_2 = two_level_partition_function(epsilon, T)
    if Z_2 <= 1:
        print("错误 4.7: 二能级系统配分函数应大于1")
        print(f"  计算得到 Z = {Z_2:.4f}")
        print("  提示: Z = 1 + exp(-ε/kT) > 1")
        all_passed = False
    else:
        print(f"通过 4.7: 二能级系统正确 (Z = {Z_2:.4f})")

    if all_passed:
        print("\n所有测试通过！")
        try:
            plot_statistical()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("统计物理 Statistical Physics")
    print("=" * 50)
    verify()
