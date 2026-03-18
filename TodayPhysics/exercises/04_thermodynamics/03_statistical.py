"""
统计力学基础 Statistical Mechanics
难度 Difficulty: ★★★★

学习目标 Learning Objectives:
- 理解微观态和宏观态的概念及其联系
  Understand microstates, macrostates and their connection
- 掌握玻尔兹曼分布及其物理意义
  Master Boltzmann distribution and its physical meaning
- 应用配分函数计算热力学量
  Apply partition function to calculate thermodynamic quantities
- 理解量子统计（费米-狄拉克和玻色-爱因斯坦分布）
  Understand quantum statistics (Fermi-Dirac and Bose-Einstein distributions)
- 分析简单系统（二能级系统、谐振子）的统计性质
  Analyze statistical properties of simple systems

物理背景 Physical Background:
统计力学是连接微观粒子运动和宏观热力学性质的桥梁。它假设系统的
各个微观态以一定的概率出现，并通过对所有微观态的统计平均得到
宏观可观测量。

核心思想是"等概率原理"：对于孤立系统，所有可达的微观态出现的
概率相等。对于与热库接触的系统，出现在能量 E 的微观态的概率
正比于玻尔兹曼因子 exp(-E/kT)。

HINT: 玻尔兹曼分布: P(E) ∝ exp(-E/kT)，高能态概率小
HINT: 配分函数: Z = Σᵢ exp(-Eᵢ/kT)，是计算热力学量的核心
HINT: 平均能量: <E> = -∂(lnZ)/∂β，其中 β = 1/(kT)
HINT: 亥姆霍兹自由能: F = -kT ln(Z)
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import k_B, hbar, eV

# I AM NOT DONE

# =============================================================================
# 练习 3.1: 玻尔兹曼分布
# Exercise 3.1: Boltzmann Distribution
# =============================================================================
# 玻尔兹曼分布描述热平衡时系统处于各能态的概率
# Boltzmann distribution describes probability of each energy state at equilibrium
#
# 核心公式 Core formula:
#   P(Eᵢ) = exp(-Eᵢ/kT) / Z
#   其中 Z = Σᵢ exp(-Eᵢ/kT) 是配分函数（归一化因子）
#
# 物理意义 Physical meaning:
#   - 能量越高，概率越小（指数衰减）
#   - 温度越高，高能态概率越大（热激发）
#   - kT 是热能的典型尺度，决定激发程度

def boltzmann_probability(E, T):
    """
    玻尔兹曼因子 Boltzmann factor

    公式 Formula: exp(-E/kT)

    参数 Parameters:
        E: 能量 (J) - Energy
        T: 温度 (K) - Temperature

    返回 Returns:
        玻尔兹曼因子（未归一化概率）

    注意 Note:
        这是未归一化的概率，需要除以配分函数 Z 得到真实概率
    """
    # TODO: 计算玻尔兹曼因子
    # TODO: Calculate Boltzmann factor
    return np.exp(-E / (k_B * T))

def maxwell_speed_distribution(v, T, m):
    """
    麦克斯韦速率分布 Maxwell speed distribution

    公式 Formula: f(v) = 4π(m/2πkT)^(3/2) v² exp(-mv²/2kT)

    参数 Parameters:
        v: 速率 (m/s) - Speed
        T: 温度 (K) - Temperature
        m: 分子质量 (kg) - Molecular mass

    返回 Returns:
        f(v): 速率分布函数 (s/m)

    推导 Derivation:
        从三维速度空间的玻尔兹曼分布积分得到
        f(v) = 4πv² × g(v_x)g(v_y)g(v_z)
    """
    coef = 4 * np.pi * (m / (2 * np.pi * k_B * T))**1.5
    f = coef * v**2 * np.exp(-m * v**2 / (2 * k_B * T))
    return f

def most_probable_speed(T, m):
    """
    最概然速率 Most probable speed

    公式 Formula: v_p = sqrt(2kT/m)

    物理意义: f(v) 达到最大值时的速率
    """
    return np.sqrt(2 * k_B * T / m)

def mean_speed(T, m):
    """
    平均速率 Mean speed

    公式 Formula: <v> = sqrt(8kT/πm) ≈ 1.128 v_p

    物理意义: <v> = ∫v·f(v)dv
    """
    return np.sqrt(8 * k_B * T / (np.pi * m))

def rms_speed(T, m):
    """
    方均根速率 Root-mean-square speed

    公式 Formula: v_rms = sqrt(3kT/m) ≈ 1.225 v_p

    物理意义: v_rms = sqrt(<v²>)，与平均动能直接相关
    """
    return np.sqrt(3 * k_B * T / m)


# =============================================================================
# 练习 3.2: 配分函数
# Exercise 3.2: Partition Function
# =============================================================================
# 配分函数是统计力学中最核心的概念
# Partition function is the most central concept in statistical mechanics
#
# 定义 Definition:
#   Z = Σᵢ exp(-Eᵢ/kT) = Σᵢ exp(-βEᵢ)，其中 β = 1/(kT)
#
# 重要性 Importance:
#   所有热力学量都可以从配分函数导出：
#   - 平均能量: <E> = -∂(lnZ)/∂β = kT² ∂(lnZ)/∂T
#   - 亥姆霍兹自由能: F = -kT ln(Z)
#   - 熵: S = k(lnZ + β<E>) = -∂F/∂T
#   - 热容: C = ∂<E>/∂T

def partition_function(energies, T):
    """
    计算配分函数 Calculate partition function

    公式 Formula: Z = Σᵢ exp(-Eᵢ/kT)

    参数 Parameters:
        energies: 能级列表 (J) - List of energy levels
        T: 温度 (K) - Temperature

    返回 Returns:
        Z: 配分函数（无量纲）- Partition function (dimensionless)

    物理意义 Physical meaning:
        Z 衡量系统有多少"有效"的可达态
        温度越高，更多高能态参与，Z 越大
    """
    # TODO: 计算配分函数（对所有态的玻尔兹曼因子求和）
    # TODO: Calculate partition function (sum of Boltzmann factors)
    Z = np.sum(np.exp(-np.array(energies) / (k_B * T)))
    return Z

def partition_function_harmonic(omega, T, n_max=100):
    """
    量子谐振子配分函数 Partition function of quantum harmonic oscillator

    能级 Energy levels: E_n = (n + 1/2)hbar*omega，n = 0, 1, 2, ...

    解析公式 Analytical formula:
        Z = exp(-hbar*omega/2kT) / (1 - exp(-hbar*omega/kT))
        = 1 / (2sinh(hbar*omega/2kT))

    参数 Parameters:
        omega: 角频率 (rad/s) - Angular frequency
        T: 温度 (K) - Temperature
        n_max: 数值计算时的最大量子数（此处未使用）

    返回 Returns:
        Z: 配分函数 - Partition function

    注意 Note:
        这是等比级数求和的结果，基态能量 hbar*omega/2 已包含
    """
    x = hbar * omega / (k_B * T)  # 无量纲温度参数
    Z = np.exp(-x/2) / (1 - np.exp(-x))
    return Z

def mean_energy_from_partition(Z, T, dZ_dT):
    """
    从配分函数计算平均能量 Calculate mean energy from partition function

    公式 Formula: <E> = kT² (∂lnZ/∂T) = kT² (1/Z)(∂Z/∂T)

    参数 Parameters:
        Z: 配分函数 - Partition function
        T: 温度 (K) - Temperature
        dZ_dT: 配分函数对温度的导数 - Derivative of Z with respect to T

    返回 Returns:
        <E>: 平均能量 (J) - Mean energy

    另一形式 Alternative form:
        <E> = -∂(lnZ)/∂β，其中 β = 1/(kT)
    """
    return k_B * T**2 * dZ_dT / Z


# =============================================================================
# 练习 3.3: 量子统计
# Exercise 3.3: Quantum Statistics
# =============================================================================
# 量子统计考虑了粒子的全同性和泡利不相容原理
# Quantum statistics accounts for particle indistinguishability and Pauli exclusion
#
# 两类量子粒子 Two types of quantum particles:
#   - 费米子（半整数自旋）：电子、质子、中子等，服从泡利不相容原理
#   - 玻色子（整数自旋）：光子、声子等，可以占据相同量子态
#
# 经典极限 Classical limit:
#   当 (E-μ)/kT >> 1 时，两种分布都趋近于玻尔兹曼分布

def fermi_dirac_distribution(E, mu, T):
    """
    费米-狄拉克分布 Fermi-Dirac distribution

    公式 Formula: f(E) = 1 / (exp((E-μ)/kT) + 1)

    参数 Parameters:
        E: 能量 (J) - Energy
        mu: 化学势/费米能 (J) - Chemical potential / Fermi energy
        T: 温度 (K) - Temperature

    返回 Returns:
        f(E): 平均占据数（0到1之间）- Mean occupation number

    物理意义 Physical meaning:
        - f(E) 表示能量为 E 的态的平均占据概率
        - T=0 时，E<μ 的态全满(f=1)，E>μ 的态全空(f=0)
        - E=μ 时，f = 0.5（无论温度多少）
    """
    x = (E - mu) / (k_B * T)
    # 避免数值溢出 Avoid numerical overflow
    x = np.clip(x, -500, 500)
    return 1 / (np.exp(x) + 1)

def bose_einstein_distribution(E, mu, T):
    """
    玻色-爱因斯坦分布 Bose-Einstein distribution

    公式 Formula: n(E) = 1 / (exp((E-μ)/kT) - 1)

    参数 Parameters:
        E: 能量 (J) - Energy（必须 E > μ）
        mu: 化学势 (J) - Chemical potential
        T: 温度 (K) - Temperature

    返回 Returns:
        n(E): 平均占据数（可以大于1）- Mean occupation number

    注意 Note:
        - 必须 E > μ，否则分母为负
        - 当 E → μ 时，n → ∞（玻色-爱因斯坦凝聚的信号）
        - 对于光子和声子，μ = 0
    """
    x = (E - mu) / (k_B * T)
    x = np.clip(x, 1e-10, 500)  # 确保 x > 0
    return 1 / (np.exp(x) - 1)

def planck_distribution(omega, T):
    """
    普朗克分布（光子气体）Planck distribution for photons

    公式 Formula: n(omega) = 1 / (exp(hbar*omega/kT) - 1)

    参数 Parameters:
        omega: 光子角频率 (rad/s) - Angular frequency
        T: 温度 (K) - Temperature

    返回 Returns:
        n(omega): 该频率模式的平均光子数 - Mean number of photons

    应用 Applications:
        - 黑体辐射
        - 激光物理
        - 宇宙微波背景辐射

    注意: 光子的化学势 μ = 0（光子数不守恒）
    """
    x = hbar * omega / (k_B * T)
    x = np.clip(x, 1e-10, 500)
    return 1 / (np.exp(x) - 1)


# =============================================================================
# 练习 3.4: 热力学量
# Exercise 3.4: Thermodynamic Quantities
# =============================================================================
# 从配分函数可以推导出所有平衡态热力学量
# All equilibrium thermodynamic quantities can be derived from partition function
#
# 主要公式 Main formulas:
#   F = -kT ln(Z)          亥姆霍兹自由能
#   S = -∂F/∂T = k(lnZ + β<E>)  熵
#   <E> = -∂(lnZ)/∂β        平均能量
#   C = ∂<E>/∂T            热容

def helmholtz_free_energy(T, Z):
    """
    亥姆霍兹自由能 Helmholtz free energy from partition function

    公式 Formula: F = -kT ln(Z)

    参数 Parameters:
        T: 温度 (K) - Temperature
        Z: 配分函数 - Partition function

    返回 Returns:
        F: 亥姆霍兹自由能 (J) - Helmholtz free energy

    物理意义 Physical meaning:
        F 是恒温恒容条件下可提取的最大功
        系统自发向 F 减小的方向演化
    """
    return -k_B * T * np.log(Z)

def entropy_from_partition(T, Z, E_mean):
    """
    从配分函数计算熵 Calculate entropy from partition function

    公式 Formula: S = (E - F)/T = k ln(Z) + <E>/T

    参数 Parameters:
        T: 温度 (K) - Temperature
        Z: 配分函数 - Partition function
        E_mean: 平均能量 (J) - Mean energy

    返回 Returns:
        S: 熵 (J/K) - Entropy

    推导 Derivation:
        由 F = <E> - TS 得 S = (<E> - F)/T
        代入 F = -kT ln(Z) 即得结果
    """
    return k_B * np.log(Z) + E_mean / T

def heat_capacity_harmonic(omega, T):
    """
    量子谐振子热容 Heat capacity of quantum harmonic oscillator

    公式 Formula: C = k (hbar*omega/kT)² exp(hbar*omega/kT) / (exp(hbar*omega/kT) - 1)²

    参数 Parameters:
        omega: 角频率 (rad/s) - Angular frequency
        T: 温度 (K) - Temperature

    返回 Returns:
        C: 热容 (J/K) - Heat capacity

    极限行为 Limiting behavior:
        - 高温 (kT >> hbar*omega): C → k（经典极限，能均分定理）
        - 低温 (kT << hbar*omega): C → 0（量子冻结）
    """
    x = hbar * omega / (k_B * T)  # 无量纲参数 θ/T，θ 是特征温度
    if x > 500:
        return 0  # 极低温时热容为零
    C = k_B * x**2 * np.exp(x) / (np.exp(x) - 1)**2
    return C


# =============================================================================
# 练习 3.5: 二能级系统
# Exercise 3.5: Two-Level System
# =============================================================================
# 二能级系统是统计力学中最简单的模型
# Two-level system is the simplest model in statistical mechanics
#
# 能级 Energy levels: E₀ = 0（基态），E₁ = ε（激发态）
#
# 这个模型的应用 Applications:
#   - 顺磁盐中的自旋（磁场中 E = ±μB）
#   - 分子振动的冻结
#   - 核磁共振

def two_level_partition(epsilon, T):
    """
    二能级系统配分函数 Partition function of two-level system

    能级 Energy levels: E₀ = 0, E₁ = ε
    公式 Formula: Z = 1 + exp(-ε/kT)

    参数 Parameters:
        epsilon: 能级间隔 (J) - Energy gap
        T: 温度 (K) - Temperature

    返回 Returns:
        Z: 配分函数 - Partition function

    极限 Limits:
        T → 0: Z → 1（只有基态）
        T → ∞: Z → 2（两态等概率）
    """
    return 1 + np.exp(-epsilon / (k_B * T))

def two_level_mean_energy(epsilon, T):
    """
    二能级系统平均能量 Mean energy of two-level system

    公式 Formula:
        <E> = ε × exp(-ε/kT) / (1 + exp(-ε/kT))
            = ε / (1 + exp(ε/kT))

    参数 Parameters:
        epsilon: 能级间隔 (J) - Energy gap
        T: 温度 (K) - Temperature

    返回 Returns:
        <E>: 平均能量 (J) - Mean energy

    极限 Limits:
        T → 0: <E> → 0（系统处于基态）
        T → ∞: <E> → ε/2（两态等概率占据）
    """
    return epsilon / (1 + np.exp(epsilon / (k_B * T)))

def two_level_heat_capacity(epsilon, T):
    """
    二能级系统热容（肖特基比热）Heat capacity of two-level system (Schottky anomaly)

    公式 Formula: C = k (ε/kT)² exp(ε/kT) / (1 + exp(ε/kT))²

    参数 Parameters:
        epsilon: 能级间隔 (J) - Energy gap
        T: 温度 (K) - Temperature

    返回 Returns:
        C: 热容 (J/K) - Heat capacity

    特点 Features:
        - 在 kT ~ ε 时有一个峰值（肖特基峰）
        - 高温和低温极限都趋于零
        - 这与谐振子热容的单调行为不同
    """
    x = epsilon / (k_B * T)
    if x > 500:
        return 0
    C = k_B * x**2 * np.exp(x) / (1 + np.exp(x))**2
    return C


# =============================================================================
# 练习 3.6: 理想气体状态方程
# Exercise 3.6: Ideal Gas from Statistics
# =============================================================================
# 从统计力学推导理想气体状态方程
# Deriving ideal gas law from statistical mechanics
#
# 关键概念 Key concept: 热德布罗意波长
#   λ = h/√(2πmkT)
#   当粒子间距 >> λ 时，量子效应可忽略，气体表现为经典
#
# 经典理想气体配分函数 Classical ideal gas partition function:
#   Z = Z₁^N / N!
#   其中 Z₁ = V/λ³ 是单粒子配分函数
#   N! 来自全同粒子的不可分辨性（吉布斯因子）

def ideal_gas_partition(V, T, m, N):
    """
    单原子理想气体配分函数（经典极限）
    Partition function of classical monatomic ideal gas

    公式 Formula: Z = (V/λ³)^N / N!
    使用斯特林近似: ln(N!) ≈ N ln(N) - N

    参数 Parameters:
        V: 体积 (m³) - Volume
        T: 温度 (K) - Temperature
        m: 单个原子质量 (kg) - Mass of single atom
        N: 原子数 - Number of atoms

    返回 Returns:
        Z: 配分函数 - Partition function

    推导 Derivation:
        ln(Z) = N ln(V/λ³) - ln(N!)
              ≈ N ln(V/λ³) - N ln(N) + N
              = N [ln(V/λ³) - ln(N) + 1]
    """
    h = 2 * np.pi * hbar  # 普朗克常数
    lambda_th = h / np.sqrt(2 * np.pi * m * k_B * T)  # 热德布罗意波长
    # ln(Z) = N ln(V/λ³) - N ln(N) + N (斯特林近似)
    ln_Z = N * (np.log(V / lambda_th**3) - np.log(N) + 1)
    return np.exp(ln_Z) if ln_Z < 700 else np.inf

def thermal_de_broglie_wavelength(T, m):
    """
    热德布罗意波长 Thermal de Broglie wavelength

    公式 Formula: λ = h/√(2πmkT)

    参数 Parameters:
        T: 温度 (K) - Temperature
        m: 粒子质量 (kg) - Particle mass

    返回 Returns:
        lambda_th: 热德布罗意波长 (m)

    物理意义 Physical meaning:
        - 描述粒子的量子特性尺度
        - 当 n λ³ << 1（n 是粒子数密度）时，量子效应可忽略
        - 当 n λ³ ~ 1 时，需要考虑量子统计

    典型值 Typical values at 300K:
        - 电子: λ ~ 4 nm
        - 氢原子: λ ~ 0.1 nm
        - 氮分子: λ ~ 0.02 nm
    """
    h = 2 * np.pi * hbar
    return h / np.sqrt(2 * np.pi * m * k_B * T)


# =============================================================================
# 可视化 Visualization
# =============================================================================
def plot_statistical():
    """
    绘制统计力学相关图表 Plot statistical mechanics diagrams

    包含六个子图 Contains six subplots:
    1. 麦克斯韦速率分布（不同温度）
    2. 费米-狄拉克分布（不同温度）
    3. 普朗克分布（黑体辐射光子数）
    4. 二能级系统热容（肖特基比热）
    5. 量子谐振子热容
    6. 热德布罗意波长（不同粒子）
    """
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 麦克斯韦速度分布
    ax1 = axes[0, 0]
    m_N2 = 28 * 1.66e-27  # N2分子质量
    v = np.linspace(0, 1500, 500)

    for T in [200, 300, 500]:
        f = maxwell_speed_distribution(v, T, m_N2)
        v_p = most_probable_speed(T, m_N2)
        ax1.plot(v, f*1000, label=f'T = {T} K', linewidth=2)

    ax1.set_xlabel('速度 v (m/s)')
    ax1.set_ylabel('f(v) × 1000')
    ax1.set_title('麦克斯韦速度分布')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 费米-狄拉克与玻色-爱因斯坦
    ax2 = axes[0, 1]
    E = np.linspace(0, 0.5, 500) * eV
    mu = 0.2 * eV

    for T_K in [300, 1000, 3000]:
        f_FD = fermi_dirac_distribution(E, mu, T_K)
        ax2.plot(E/eV, f_FD, label=f'T = {T_K} K', linewidth=2)

    ax2.axvline(x=mu/eV, color='k', linestyle='--', alpha=0.5)
    ax2.set_xlabel('E (eV)')
    ax2.set_ylabel('f(E)')
    ax2.set_title('费米-狄拉克分布')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 普朗克分布
    ax3 = axes[0, 2]
    omega = np.linspace(1e12, 1e15, 500)

    for T in [3000, 5000, 6000]:
        n = planck_distribution(omega, T)
        ax3.semilogy(omega/1e14, n, label=f'T = {T} K', linewidth=2)

    ax3.set_xlabel('ω (×10¹⁴ rad/s)')
    ax3.set_ylabel('n(ω)')
    ax3.set_title('普朗克分布')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 二能级热容
    ax4 = axes[1, 0]
    epsilon = 0.1 * eV
    T_range = np.linspace(100, 3000, 500)

    C = [two_level_heat_capacity(epsilon, T) / k_B for T in T_range]
    ax4.plot(k_B * T_range / epsilon, C, 'b-', linewidth=2)
    ax4.set_xlabel('kT/ε')
    ax4.set_ylabel('C/k_B')
    ax4.set_title('Schottky比热')
    ax4.grid(True, alpha=0.3)

    # 5. 谐振子热容
    ax5 = axes[1, 1]
    omega = 1e14  # rad/s

    C_ho = [heat_capacity_harmonic(omega, T) / k_B for T in T_range]
    ax5.plot(k_B * T_range / (hbar * omega), C_ho, 'r-', linewidth=2)
    ax5.axhline(y=1, color='k', linestyle='--', alpha=0.5, label='经典极限')
    ax5.set_xlabel('kT/ℏω')
    ax5.set_ylabel('C/k_B')
    ax5.set_title('量子谐振子热容')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. 热德布罗意波长
    ax6 = axes[1, 2]
    T_wave = np.linspace(10, 1000, 500)

    for name, m in [('电子', 9.11e-31), ('氢原子', 1.67e-27), ('氮分子', 28*1.66e-27)]:
        lambda_th = [thermal_de_broglie_wavelength(T, m) * 1e9 for T in T_wave]
        ax6.semilogy(T_wave, lambda_th, label=name, linewidth=2)

    ax6.set_xlabel('T (K)')
    ax6.set_ylabel('λ_th (nm)')
    ax6.set_title('热德布罗意波长')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('statistical.png', dpi=150)
    print("图像已保存为 statistical.png")
    plt.show()


def verify():
    """
    验证所有练习的正确性 Verify all exercises

    测试内容 Tests:
    3.1 麦克斯韦速率分布
    3.2 配分函数
    3.3 量子统计（费米-狄拉克分布）
    3.4 量子谐振子热容
    3.5 二能级系统
    3.6 热德布罗意波长
    """
    all_passed = True

    # 检查 3.1 - 麦克斯韦速率分布
    v_p = most_probable_speed(300, 28*1.66e-27)
    v_mean = mean_speed(300, 28*1.66e-27)
    if not v_p < v_mean:
        print("错误 3.1: 速度关系应满足 v_p < <v> < v_rms")
        all_passed = False
    else:
        print(f"通过 3.1: 麦克斯韦分布正确 (N₂在300K时 v_p = {v_p:.0f} m/s)")

    # 检查 3.2 - 配分函数
    T = 300
    energies = [0, 0.1*eV, 0.2*eV]
    Z = partition_function(energies, T)
    if Z <= 0:
        print("错误 3.2: 配分函数必须为正值")
        all_passed = False
    else:
        print(f"通过 3.2: 配分函数正确 (三能级系统 Z = {Z:.4f})")

    # 检查 3.3 - 费米-狄拉克分布
    f_FD = fermi_dirac_distribution(0.2*eV, 0.2*eV, 300)
    if not np.isclose(f_FD, 0.5, atol=0.01):
        print("错误 3.3: 费米分布在 E=μ 处应为 0.5")
        print(f"  实际得到: f(μ) = {f_FD:.3f}")
        all_passed = False
    else:
        print(f"通过 3.3: 量子统计正确 (f(E=μ) = {f_FD:.3f})")

    # 检查 3.4 - 量子谐振子热容
    omega = 1e14  # rad/s
    C = heat_capacity_harmonic(omega, 10000)  # 高温
    if not np.isclose(C / k_B, 1, rtol=0.1):
        print("错误 3.4: 高温极限热容应趋近于 k_B（经典能均分定理）")
        print(f"  实际得到: C/k_B = {C/k_B:.3f}")
        all_passed = False
    else:
        print(f"通过 3.4: 热容正确（高温经典极限 C/k_B ≈ {C/k_B:.3f}）")

    # 检查 3.5 - 二能级系统
    Z2 = two_level_partition(0.1*eV, 300)
    E2 = two_level_mean_energy(0.1*eV, 300)
    if E2 < 0 or E2 > 0.1*eV:
        print("错误 3.5: 二能级平均能量应在 [0, ε] 范围内")
        all_passed = False
    else:
        print(f"通过 3.5: 二能级系统正确 (<E> = {E2/eV*1000:.1f} meV)")

    # 检查 3.6 - 热德布罗意波长
    lambda_th = thermal_de_broglie_wavelength(300, 9.11e-31)  # 电子
    if lambda_th <= 0 or lambda_th > 1e-6:
        print("错误 3.6: 热德布罗意波长计算错误")
        all_passed = False
    else:
        print(f"通过 3.6: 热德布罗意波长正确 (电子在300K时 λ = {lambda_th*1e9:.2f} nm)")

    if all_passed:
        print("\n所有测试通过！")
        try:
            plot_statistical()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("统计力学基础 Statistical Mechanics")
    print("=" * 50)
    verify()
