"""
理想气体与热力学定律 Ideal Gas and Thermodynamics Laws
难度 Difficulty: ★★★

学习目标 Learning Objectives:
- 理解理想气体状态方程及其微观意义
  Understand the ideal gas law and its microscopic meaning
- 掌握热力学第一定律（能量守恒）
  Master the first law of thermodynamics (energy conservation)
- 计算等温、绝热过程中的功和热量
  Calculate work and heat in isothermal and adiabatic processes
- 理解卡诺循环与热机效率的极限
  Understand the Carnot cycle and the limit of heat engine efficiency
- 掌握麦克斯韦-玻尔兹曼速率分布
  Master the Maxwell-Boltzmann speed distribution

物理背景 Physical Background:
理想气体是热力学中最基本的模型，假设气体分子之间没有相互作用，
且分子本身不占体积。虽然是理想化模型，但在常温常压下能很好地
描述真实气体的行为。

热力学第一定律是能量守恒定律在热学中的表述：系统内能的变化
等于吸收的热量减去对外做的功。

HINT: 理想气体方程: PV = nRT，其中 R = 8.314 J/(mol·K)
HINT: 热力学第一定律: ΔU = Q - W（功为系统对外做的功）
HINT: 绝热过程: PV^γ = 常数，γ = Cp/Cv 是热容比
HINT: 卡诺效率: η = 1 - Tc/Th 是热机效率的理论上限
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import k_B, R, N_A

# I AM NOT DONE

# =============================================================================
# 练习 1.1: 理想气体状态方程
# Exercise 1.1: Ideal Gas Law
# =============================================================================
# 理想气体状态方程是描述理想气体宏观性质的基本方程
# The ideal gas law is the fundamental equation describing macroscopic properties
#
# 方程形式 Equation form:
#   PV = nRT
#
# 变量说明 Variable definitions:
#   P: 压强 Pressure (Pa = N/m² = kg/(m·s²))
#   V: 体积 Volume (m³)
#   n: 物质的量 Amount of substance (mol)
#   R: 气体常数 Gas constant = 8.314 J/(mol·K)
#   T: 绝对温度 Absolute temperature (K)
#
# 物理意义 Physical meaning:
#   压强与温度成正比，与体积成反比
#   1 mol 理想气体在标准状态 (0°C, 1 atm) 下的体积约为 22.4 L

def ideal_gas_pressure(n, V, T):
    """
    计算理想气体压强 Calculate ideal gas pressure

    公式 Formula: P = nRT/V

    参数 Parameters:
        n: 物质的量 (mol) - Amount of substance
        V: 体积 (m³) - Volume
        T: 绝对温度 (K) - Absolute temperature

    返回 Returns:
        P: 压强 (Pa) - Pressure
    """
    # TODO: 根据理想气体状态方程计算压强
    # TODO: Calculate pressure using the ideal gas law
    P = n * R * T / V  # 修改这里
    return P


def ideal_gas_volume(n, P, T):
    """
    计算理想气体体积 Calculate ideal gas volume

    公式 Formula: V = nRT/P

    参数 Parameters:
        n: 物质的量 (mol) - Amount of substance
        P: 压强 (Pa) - Pressure
        T: 绝对温度 (K) - Absolute temperature

    返回 Returns:
        V: 体积 (m³) - Volume
    """
    # TODO: 根据理想气体状态方程计算体积
    # TODO: Calculate volume using the ideal gas law
    V = n * R * T / P  # 修改这里
    return V


def ideal_gas_temperature(P, V, n):
    """
    计算理想气体温度 Calculate ideal gas temperature

    公式 Formula: T = PV/(nR)

    参数 Parameters:
        P: 压强 (Pa) - Pressure
        V: 体积 (m³) - Volume
        n: 物质的量 (mol) - Amount of substance

    返回 Returns:
        T: 绝对温度 (K) - Absolute temperature
    """
    # TODO: 根据理想气体状态方程计算温度
    # TODO: Calculate temperature using the ideal gas law
    T = P * V / (n * R)  # 修改这里
    return T


# 标准状态参数 Standard state parameters:
# 标准状态定义: 1 mol 气体在 1 atm (101325 Pa)、0°C (273.15 K) 条件下
n_std = 1.0  # mol - 物质的量
P_std = 101325  # Pa (1 atm) - 标准大气压
T_std = 273.15  # K (0°C) - 标准温度（冰点）
V_std = ideal_gas_volume(n_std, P_std, T_std)  # 约为 22.4 L


# =============================================================================
# 练习 1.2: 等温过程
# Exercise 1.2: Isothermal Process
# =============================================================================
# 等温过程 Isothermal process:
#   - 温度保持不变 Temperature remains constant: T = 常数 const
#   - 由玻意耳定律 Boyle's law: PV = 常数 const
#   - 理想气体等温过程中，内能不变 ΔU = 0
#   - 吸收的热量全部转化为对外做的功 Q = W
#
# 等温膨胀功 Work in isothermal expansion:
#   W = ∫P dV = ∫(nRT/V) dV = nRT ln(V₂/V₁)
#   - 膨胀时 V₂ > V₁，W > 0，气体对外做功
#   - 压缩时 V₂ < V₁，W < 0，外界对气体做功

def isothermal_work(n, T, V1, V2):
    """
    计算等温膨胀/压缩做的功 Calculate work in isothermal process

    公式 Formula: W = nRT ln(V₂/V₁) = nRT ln(P₁/P₂)

    参数 Parameters:
        n: 物质的量 (mol) - Amount of substance
        T: 温度 (K) - Temperature
        V1: 初始体积 (m³) - Initial volume
        V2: 末态体积 (m³) - Final volume

    返回 Returns:
        W: 功 (J) - Work done by the gas
        W > 0 表示气体对外做功（膨胀）
        W < 0 表示外界对气体做功（压缩）
    """
    # TODO: 使用等温过程功的公式计算
    # TODO: Calculate using the isothermal work formula
    W = n * R * T * np.log(V2 / V1)  # 修改这里
    return W


def isothermal_process(P1, V1, V2_range):
    """
    返回等温过程的 P-V 曲线 Return P-V curve for isothermal process

    公式 Formula: PV = P₁V₁ = 常数，所以 P₂ = P₁V₁/V₂

    参数 Parameters:
        P1: 初始压强 (Pa) - Initial pressure
        V1: 初始体积 (m³) - Initial volume
        V2_range: 体积数组 (m³) - Array of volumes

    返回 Returns:
        P2: 对应的压强数组 (Pa) - Corresponding pressures
    """
    # TODO: 根据玻意耳定律 PV = 常数 计算压强
    # TODO: Calculate pressure using Boyle's law PV = const
    P2 = P1 * V1 / V2_range  # 修改这里
    return P2


# =============================================================================
# 练习 1.3: 绝热过程
# Exercise 1.3: Adiabatic Process
# =============================================================================
# 绝热过程 Adiabatic process:
#   - 系统与外界没有热量交换 No heat exchange: Q = 0
#   - 由热力学第一定律: ΔU = -W（内能变化等于负功）
#   - 绝热方程 Adiabatic equation: PV^γ = 常数 const
#   - 另一形式: TV^(γ-1) = 常数 const
#
# 热容比（绝热指数）γ = Cp/Cv:
#   - 单原子气体 (He, Ar): γ = 5/3 ≈ 1.67（仅有平动自由度）
#   - 双原子气体 (N₂, O₂): γ = 7/5 = 1.4（平动+转动自由度）
#   - 多原子气体: γ 更小，因为有更多自由度
#
# 绝热过程的功 Work in adiabatic process:
#   W = ∫P dV = nCv(T₁ - T₂) = nR(T₁ - T₂)/(γ - 1)

# 热容比参数 Heat capacity ratio (adiabatic index):
gamma_mono = 5/3  # 单原子气体 Monatomic gas (He, Ne, Ar)
gamma_di = 7/5    # 双原子气体 Diatomic gas (N₂, O₂, H₂)

def adiabatic_process(P1, V1, V2_range, gamma):
    """
    返回绝热过程的 P-V 曲线 Return P-V curve for adiabatic process

    公式 Formula: P₁V₁^γ = P₂V₂^γ，所以 P₂ = P₁(V₁/V₂)^γ

    参数 Parameters:
        P1: 初始压强 (Pa) - Initial pressure
        V1: 初始体积 (m³) - Initial volume
        V2_range: 体积数组 (m³) - Array of volumes
        gamma: 热容比 γ = Cp/Cv - Heat capacity ratio

    返回 Returns:
        P2: 对应的压强数组 (Pa) - Corresponding pressures

    注意: 绝热线比等温线更陡峭（γ > 1）
    Note: Adiabatic curve is steeper than isothermal (γ > 1)
    """
    # TODO: 根据绝热方程 PV^γ = 常数 计算压强
    # TODO: Calculate pressure using adiabatic equation PV^γ = const
    P2 = P1 * (V1 / V2_range)**gamma  # 修改这里
    return P2


def adiabatic_temperature(T1, V1, V2, gamma):
    """
    计算绝热过程后的温度 Calculate temperature after adiabatic process

    公式 Formula: T₁V₁^(γ-1) = T₂V₂^(γ-1)，所以 T₂ = T₁(V₁/V₂)^(γ-1)

    参数 Parameters:
        T1: 初始温度 (K) - Initial temperature
        V1: 初始体积 (m³) - Initial volume
        V2: 末态体积 (m³) - Final volume
        gamma: 热容比 γ = Cp/Cv - Heat capacity ratio

    返回 Returns:
        T2: 末态温度 (K) - Final temperature

    物理意义 Physical meaning:
        绝热膨胀时温度降低（气体对外做功消耗内能）
        绝热压缩时温度升高（外界对气体做功增加内能）
    """
    # TODO: 根据绝热过程温度-体积关系计算末态温度
    # TODO: Calculate final temperature using T-V relation
    T2 = T1 * (V1 / V2)**(gamma - 1)  # 修改这里
    return T2


def adiabatic_work(n, T1, T2, gamma):
    """
    计算绝热过程做的功 Calculate work in adiabatic process

    公式 Formula:
        W = nCv(T₁ - T₂) = nR(T₁ - T₂)/(γ - 1)
        其中 Cv = R/(γ - 1) 是定容热容

    参数 Parameters:
        n: 物质的量 (mol) - Amount of substance
        T1: 初始温度 (K) - Initial temperature
        T2: 末态温度 (K) - Final temperature
        gamma: 热容比 γ = Cp/Cv - Heat capacity ratio

    返回 Returns:
        W: 功 (J) - Work done by the gas

    推导 Derivation:
        由 Q = 0 和 ΔU = Q - W 得 W = -ΔU = -nCvΔT = nCv(T₁ - T₂)
    """
    # TODO: 使用绝热过程功的公式计算
    # TODO: Calculate using the adiabatic work formula
    W = n * R * (T1 - T2) / (gamma - 1)  # 修改这里
    return W


# =============================================================================
# 练习 1.4: 热力学第一定律
# Exercise 1.4: First Law of Thermodynamics
# =============================================================================
# 热力学第一定律是能量守恒定律在热学中的表述
# The first law is the statement of energy conservation in thermodynamics
#
# 公式 Formula: ΔU = Q - W
#   ΔU: 内能变化 Change in internal energy (J)
#   Q: 系统吸收的热量 Heat absorbed by the system (J)
#   W: 系统对外做的功 Work done by the system (J)
#
# 符号约定 Sign convention:
#   Q > 0: 系统吸热  Q < 0: 系统放热
#   W > 0: 系统对外做功  W < 0: 外界对系统做功
#
# 理想气体的内能 Internal energy of ideal gas:
#   - 只与温度有关，与压强、体积无关
#   - U = nCvT（以绝对零度为参考点）
#   - ΔU = nCvΔT（内能变化）

def internal_energy_change(n, Cv, delta_T):
    """
    计算内能变化 Calculate change in internal energy

    公式 Formula: ΔU = nCvΔT

    参数 Parameters:
        n: 物质的量 (mol) - Amount of substance
        Cv: 定容摩尔热容 (J/(mol·K)) - Molar heat capacity at constant volume
        delta_T: 温度变化 (K) - Temperature change

    返回 Returns:
        delta_U: 内能变化 (J) - Change in internal energy

    物理意义 Physical meaning:
        理想气体的内能来源于分子的动能，只与温度有关
    """
    # TODO: 计算内能变化 ΔU = nCvΔT
    # TODO: Calculate internal energy change
    delta_U = n * Cv * delta_T  # 修改这里
    return delta_U


def heat_from_first_law(delta_U, W):
    """
    由热力学第一定律计算热量 Calculate heat from first law

    公式 Formula: Q = ΔU + W（由 ΔU = Q - W 变形得到）

    参数 Parameters:
        delta_U: 内能变化 (J) - Change in internal energy
        W: 系统对外做的功 (J) - Work done by the system

    返回 Returns:
        Q: 系统吸收的热量 (J) - Heat absorbed by the system
    """
    # TODO: 根据热力学第一定律计算热量
    # TODO: Calculate heat using the first law
    Q = delta_U + W  # 修改这里
    return Q


# 理想气体的热容 Heat capacities of ideal gas:
# 定容热容 Cv = R/(γ-1) - 恒定体积下加热所需热量
# 定压热容 Cp = γR/(γ-1) - 恒定压强下加热所需热量
# 迈耶关系 Mayer's relation: Cp - Cv = R
Cv_mono = R / (gamma_mono - 1)  # 单原子气体定容热容 ≈ 12.5 J/(mol·K)
Cp_mono = gamma_mono * R / (gamma_mono - 1)  # 单原子气体定压热容 ≈ 20.8 J/(mol·K)


# =============================================================================
# 练习 1.5: 卡诺循环
# Exercise 1.5: Carnot Cycle
# =============================================================================
# 卡诺循环是理想热机的理论模型，由四个可逆过程组成：
# The Carnot cycle is the theoretical model of an ideal heat engine
#
# 循环过程 Cycle processes:
#   1. 等温膨胀（高温热源 Th）：吸热 Qh，对外做功
#   2. 绝热膨胀：温度从 Th 降至 Tc，对外做功
#   3. 等温压缩（低温热源 Tc）：放热 Qc，外界做功
#   4. 绝热压缩：温度从 Tc 升至 Th，外界做功
#
# 卡诺效率 Carnot efficiency:
#   η = W/Qh = 1 - Tc/Th = 1 - Qc/Qh
#
# 重要性 Importance:
#   - 卡诺效率是工作在相同温度范围内所有热机效率的上限
#   - 只与两热源温度有关，与工作物质无关
#   - 实际热机效率总是低于卡诺效率（不可逆损失）

def carnot_efficiency(T_hot, T_cold):
    """
    计算卡诺循环效率 Calculate Carnot cycle efficiency

    公式 Formula: η = 1 - Tc/Th

    参数 Parameters:
        T_hot: 高温热源温度 (K) - Hot reservoir temperature
        T_cold: 低温热源温度 (K) - Cold reservoir temperature

    返回 Returns:
        efficiency: 效率（无量纲，0到1之间）- Efficiency (dimensionless, 0 to 1)

    注意 Note:
        温度必须使用绝对温标（开尔文）
        Temperatures must be in absolute scale (Kelvin)
    """
    # TODO: 计算卡诺效率 η = 1 - Tc/Th
    # TODO: Calculate Carnot efficiency
    efficiency = 1 - T_cold / T_hot  # 修改这里
    return efficiency


def carnot_work(Q_hot, T_hot, T_cold):
    """
    计算卡诺热机做的功 Calculate work done by Carnot engine

    公式 Formula: W = Qh × η = Qh × (1 - Tc/Th)

    参数 Parameters:
        Q_hot: 从高温热源吸收的热量 (J) - Heat absorbed from hot reservoir
        T_hot: 高温热源温度 (K) - Hot reservoir temperature
        T_cold: 低温热源温度 (K) - Cold reservoir temperature

    返回 Returns:
        W: 热机对外做的净功 (J) - Net work done by the engine

    能量守恒 Energy conservation:
        Qh = W + Qc（吸收的热量 = 做的功 + 放出的热量）
    """
    eta = carnot_efficiency(T_hot, T_cold)
    # TODO: 计算热机做的功 W = Qh × η
    # TODO: Calculate work done by the engine
    W = Q_hot * eta  # 修改这里
    return W


# 示例参数 Example parameters:
# 高温热源 500K（如蒸汽），低温热源 300K（如环境温度）
T_hot = 500  # K - 高温热源温度 Hot reservoir temperature
T_cold = 300  # K - 低温热源温度 Cold reservoir temperature
eta_carnot = carnot_efficiency(T_hot, T_cold)  # 理论最大效率 = 40%


# =============================================================================
# 练习 1.6: 麦克斯韦-玻尔兹曼分布
# Exercise 1.6: Maxwell-Boltzmann Distribution
# =============================================================================
# 麦克斯韦-玻尔兹曼分布描述热平衡状态下气体分子的速率分布
# Maxwell-Boltzmann distribution describes the speed distribution of gas molecules
# in thermal equilibrium
#
# 速率分布函数 Speed distribution function:
#   f(v) = 4π × (m/(2πkT))^(3/2) × v² × exp(-mv²/(2kT))
#
# 物理意义 Physical meaning:
#   - f(v)dv 表示速率在 v 到 v+dv 范围内的分子比例
#   - 分布曲线不对称：有长尾向高速延伸
#   - 温度升高时，分布变宽，峰值右移
#
# 三种特征速率 Three characteristic speeds:
#   v_p < <v> < v_rms
#   最概然速率 < 平均速率 < 方均根速率

def maxwell_boltzmann_speed(v, m, T):
    """
    麦克斯韦-玻尔兹曼速率分布 Maxwell-Boltzmann speed distribution

    公式 Formula:
        f(v) = 4π × (m/(2πkT))^(3/2) × v² × exp(-mv²/(2kT))

    参数 Parameters:
        v: 速率 (m/s) - Speed（可以是数组）
        m: 分子质量 (kg) - Molecular mass
        T: 温度 (K) - Temperature

    返回 Returns:
        f_v: 速率分布函数值 (s/m) - Speed distribution function

    归一化 Normalization:
        ∫₀^∞ f(v)dv = 1
    """
    factor = (m / (2 * np.pi * k_B * T))**1.5
    # TODO: 计算麦克斯韦-玻尔兹曼速率分布
    # TODO: Calculate Maxwell-Boltzmann speed distribution
    f_v = 4 * np.pi * factor * v**2 * np.exp(-m * v**2 / (2 * k_B * T))  # 修改这里
    return f_v


def most_probable_speed(m, T):
    """
    最概然速率 Most probable speed

    公式 Formula: v_p = sqrt(2kT/m)

    参数 Parameters:
        m: 分子质量 (kg) - Molecular mass
        T: 温度 (K) - Temperature

    返回 Returns:
        v_p: 最概然速率 (m/s) - Most probable speed

    物理意义 Physical meaning:
        速率分布函数的峰值对应的速率
        由 df/dv = 0 求得
    """
    # TODO: 计算最概然速率
    # TODO: Calculate most probable speed
    v_p = np.sqrt(2 * k_B * T / m)  # 修改这里
    return v_p


def mean_speed(m, T):
    """
    平均速率 Mean (average) speed

    公式 Formula: <v> = sqrt(8kT/(πm)) ≈ 1.128 × v_p

    参数 Parameters:
        m: 分子质量 (kg) - Molecular mass
        T: 温度 (K) - Temperature

    返回 Returns:
        v_mean: 平均速率 (m/s) - Mean speed

    物理意义 Physical meaning:
        <v> = ∫₀^∞ v × f(v)dv
        所有分子速率的算术平均值
    """
    # TODO: 计算平均速率
    # TODO: Calculate mean speed
    v_mean = np.sqrt(8 * k_B * T / (np.pi * m))  # 修改这里
    return v_mean


def rms_speed(m, T):
    """
    方均根速率 Root-mean-square (RMS) speed

    公式 Formula: v_rms = sqrt(3kT/m) ≈ 1.225 × v_p

    参数 Parameters:
        m: 分子质量 (kg) - Molecular mass
        T: 温度 (K) - Temperature

    返回 Returns:
        v_rms: 方均根速率 (m/s) - RMS speed

    物理意义 Physical meaning:
        v_rms = sqrt(<v²>) = sqrt(∫₀^∞ v² × f(v)dv)
        与分子平均动能直接相关: <E_k> = (1/2)m × v_rms² = (3/2)kT
    """
    # TODO: 计算方均根速率
    # TODO: Calculate RMS speed
    v_rms = np.sqrt(3 * k_B * T / m)  # 修改这里
    return v_rms


# 氮气分子质量 Molecular mass of N₂:
# M = 28 g/mol = 28×10⁻³ kg/mol
# m = M/N_A = 单个分子质量 (kg/molecule)
m_N2 = 28e-3 / N_A  # kg per molecule ≈ 4.65×10⁻²⁶ kg


# =============================================================================
# 可视化 Visualization
# =============================================================================
def plot_thermodynamics():
    """
    绘制热力学图 Plot thermodynamics diagrams

    包含以下四个子图 Contains four subplots:
    1. P-V 图：等温过程 vs 绝热过程
    2. 卡诺效率与温度比的关系
    3. 麦克斯韦-玻尔兹曼速率分布（不同温度）
    4. 三种特征速率随温度的变化
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # 1. P-V 图：等温 vs 绝热
    ax1 = axes[0, 0]
    V_range = np.linspace(0.5, 3, 100) * V_std
    P_iso = isothermal_process(P_std, V_std, V_range)
    P_adi = adiabatic_process(P_std, V_std, V_range, gamma_di)

    ax1.plot(V_range*1e3, P_iso/1e3, 'b-', label='Isothermal', linewidth=2)
    ax1.plot(V_range*1e3, P_adi/1e3, 'r-', label='Adiabatic (γ=1.4)', linewidth=2)
    ax1.set_xlabel('Volume (L)')
    ax1.set_ylabel('Pressure (kPa)')
    ax1.set_title('P-V 图 (等温 vs 绝热)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 卡诺效率 vs 温度比
    ax2 = axes[0, 1]
    T_ratio = np.linspace(0.1, 0.95, 100)
    eta = 1 - T_ratio
    ax2.plot(T_ratio, eta * 100, 'g-', linewidth=2)
    ax2.axhline(y=eta_carnot*100, color='r', linestyle='--',
                label=f'T_c/T_h = {T_cold/T_hot:.1f}, η = {eta_carnot*100:.1f}%')
    ax2.set_xlabel('T_cold / T_hot')
    ax2.set_ylabel('Efficiency (%)')
    ax2.set_title('卡诺效率 Carnot Efficiency')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 麦克斯韦-玻尔兹曼分布（不同温度）
    ax3 = axes[1, 0]
    v_range = np.linspace(0, 2000, 500)
    for T in [200, 300, 500, 1000]:
        f = maxwell_boltzmann_speed(v_range, m_N2, T)
        ax3.plot(v_range, f*1e3, label=f'T = {T} K')

    ax3.set_xlabel('Speed (m/s)')
    ax3.set_ylabel('f(v) (×10⁻³)')
    ax3.set_title('麦克斯韦-玻尔兹曼速率分布')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 特征速率 vs 温度
    ax4 = axes[1, 1]
    T_range = np.linspace(100, 1000, 100)
    v_p = most_probable_speed(m_N2, T_range)
    v_mean = mean_speed(m_N2, T_range)
    v_rms_arr = rms_speed(m_N2, T_range)

    ax4.plot(T_range, v_p, 'b-', label='Most probable v_p')
    ax4.plot(T_range, v_mean, 'g-', label='Mean <v>')
    ax4.plot(T_range, v_rms_arr, 'r-', label='RMS v_rms')
    ax4.set_xlabel('Temperature (K)')
    ax4.set_ylabel('Speed (m/s)')
    ax4.set_title('特征速率 Characteristic Speeds (N₂)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('thermodynamics.png', dpi=150)
    print("图像已保存为 thermodynamics.png")
    plt.show()


# =============================================================================
# 验证函数 Verification
# =============================================================================
def verify():
    """
    验证所有练习的正确性 Verify all exercises

    测试内容 Tests:
    1.1 理想气体状态方程
    1.2 等温过程
    1.3 绝热过程
    1.4 热力学第一定律
    1.5 卡诺效率
    1.6 麦克斯韦-玻尔兹曼分布
    """
    all_passed = True

    # 检查 1.1 - 理想气体状态方程 Ideal gas law
    expected_V = n_std * R * T_std / P_std  # ≈ 22.4 L
    if not np.isclose(V_std, expected_V, rtol=0.01):
        print(f"错误 1.1: 理想气体状态方程计算错误")
        print(f"  期望体积: {expected_V*1e3:.2f} L, 实际得到: {V_std*1e3:.2f} L")
        all_passed = False
    else:
        print(f"通过 1.1: 理想气体状态方程正确 (标准状态体积 V = {V_std*1e3:.2f} L)")

    # 检查 1.2 - 等温过程 Isothermal work
    W_iso = isothermal_work(1.0, 300, 1e-3, 2e-3)  # 从 1L 膨胀到 2L
    expected_W = 1.0 * R * 300 * np.log(2)
    if not np.isclose(W_iso, expected_W, rtol=0.01):
        print("错误 1.2: 等温过程功计算错误")
        print(f"  期望功: {expected_W:.1f} J, 实际得到: {W_iso:.1f} J")
        all_passed = False
    else:
        print(f"通过 1.2: 等温过程正确 (体积加倍时 W = {W_iso:.1f} J)")

    # 检查 1.3 - 绝热过程 Adiabatic process
    T2_adi = adiabatic_temperature(300, 1e-3, 2e-3, gamma_di)
    expected_T2 = 300 * (1/2)**(gamma_di - 1)
    if not np.isclose(T2_adi, expected_T2, rtol=0.01):
        print("错误 1.3: 绝热过程温度计算错误")
        print(f"  期望温度: {expected_T2:.1f} K, 实际得到: {T2_adi:.1f} K")
        all_passed = False
    else:
        print(f"通过 1.3: 绝热过程正确 (T: 300K -> {T2_adi:.1f}K，体积加倍后)")

    # 检查 1.4 - 热力学第一定律 First law
    delta_U = internal_energy_change(1.0, Cv_mono, 100)
    expected_dU = 1.0 * Cv_mono * 100
    if not np.isclose(delta_U, expected_dU, rtol=0.01):
        print("错误 1.4: 热力学第一定律计算错误")
        print(f"  期望内能变化: {expected_dU:.1f} J, 实际得到: {delta_U:.1f} J")
        all_passed = False
    else:
        print(f"通过 1.4: 热力学第一定律正确 (ΔT=100K 时 ΔU = {delta_U:.1f} J)")

    # 检查 1.5 - 卡诺效率 Carnot efficiency
    expected_eta = 1 - 300/500  # 0.4
    if not np.isclose(eta_carnot, expected_eta, rtol=0.01):
        print(f"错误 1.5: 卡诺效率计算错误")
        print(f"  期望效率: {expected_eta:.1%}, 实际得到: {eta_carnot:.1%}")
        all_passed = False
    else:
        print(f"通过 1.5: 卡诺效率正确 (Th=500K, Tc=300K 时 η = {eta_carnot:.1%})")

    # 检查 1.6 - 麦克斯韦-玻尔兹曼分布 Maxwell-Boltzmann
    v_p = most_probable_speed(m_N2, 300)
    expected_vp = np.sqrt(2 * k_B * 300 / m_N2)
    if not np.isclose(v_p, expected_vp, rtol=0.01):
        print("错误 1.6: 麦克斯韦-玻尔兹曼分布计算错误")
        print(f"  期望最概然速率: {expected_vp:.0f} m/s, 实际得到: {v_p:.0f} m/s")
        all_passed = False
    else:
        v_m = mean_speed(m_N2, 300)
        v_r = rms_speed(m_N2, 300)
        print(f"通过 1.6: 麦克斯韦-玻尔兹曼分布正确")
        print(f"     N₂ 在 300K 时: v_p={v_p:.0f}, <v>={v_m:.0f}, v_rms={v_r:.0f} m/s")

    if all_passed:
        print("\n所有测试通过！正在生成可视化...")
        try:
            plot_thermodynamics()
        except Exception as e:
            print(f"可视化生成失败: {e}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("理想气体与热力学定律 Thermodynamics")
    print("=" * 50)
    verify()
