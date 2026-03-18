"""
气体动理论 Kinetic Theory of Gases
难度 Difficulty: ★★★

学习目标 Learning Objectives:
- 理解麦克斯韦速度分布及其物理意义
  Understand Maxwell velocity distribution and its physical meaning
- 掌握输运现象（粘度、热导率、扩散）的微观机制
  Master microscopic mechanisms of transport phenomena (viscosity, thermal conductivity, diffusion)
- 分析宏观热力学量（压强、温度）与微观分子运动的关系
  Analyze relations between macroscopic quantities (P, T) and microscopic molecular motion
- 计算平均自由程和碰撞频率
  Calculate mean free path and collision frequency
- 理解气体分子的能量分布和能均分定理
  Understand energy distribution of gas molecules and equipartition theorem

物理背景 Physical Background:
气体动理论从分子运动的角度解释气体的宏观性质。它假设气体由大量
不断运动的分子组成，通过统计平均得到宏观可观测量。

麦克斯韦速率分布是平衡态气体分子速率的概率分布，是统计力学最早
的成果之一。它成功预言了三种特征速率（最概然、平均、方均根）的
比值关系。

HINT: Maxwell速率分布: f(v) = 4π(m/2πk_BT)^(3/2) v² exp(-mv²/2k_BT)
HINT: 特征速率比: v_p : <v> : v_rms = 1 : 1.128 : 1.225
HINT: 平均自由程: λ = 1/(sqrt(2) n π d²)，d是分子直径
HINT: 压强的微观解释: P = (1/3) n m <v²> = n k_B T
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import k_B, N_A, R, m_p

# I AM NOT DONE

# 一些常用分子质量 Common molecular masses
# 使用质子质量 m_p 作为基本单位（原子质量单位的近似）
m_H2 = 2 * m_p   # 氢气分子
m_N2 = 28 * m_p  # 氮气分子
m_O2 = 32 * m_p  # 氧气分子
m_Ar = 40 * m_p  # 氩原子

# =============================================================================
# 练习 6.1: Maxwell速度分布
# Exercise 6.1: Maxwell Velocity Distribution
# =============================================================================
# 麦克斯韦速率分布是热平衡气体分子速率的概率分布
# Maxwell speed distribution describes the probability distribution of molecular speeds
#
# 推导思路 Derivation:
#   1. 三维速度分布: f(v_x, v_y, v_z) = f(v_x) × f(v_y) × f(v_z)（各向同性）
#   2. 每个分量服从高斯分布（根据玻尔兹曼因子）
#   3. 速率分布需要对速度空间进行球壳积分: f(v) = 4πv² × f(|v|)
#
# 三种特征速率 Three Characteristic Speeds:
#   - 最概然速率 v_p: 分布函数的峰值位置
#   - 平均速率 <v>: 所有分子速率的算术平均
#   - 均方根速率 v_rms: 与平均动能直接相关

def maxwell_speed_distribution(v, T, m):
    """
    麦克斯韦速率分布函数 Maxwell speed distribution function

    公式 Formula: f(v) = 4π(m/2πk_BT)^(3/2) × v² × exp(-mv²/2k_BT)

    参数 Parameters:
        v: 速率 (m/s) - Speed
        T: 温度 (K) - Temperature
        m: 分子质量 (kg) - Molecular mass

    返回 Returns:
        f(v): 概率密度 (s/m)，f(v)dv 是速率在 [v, v+dv] 的概率

    归一化 Normalization:
        ∫₀^∞ f(v) dv = 1
    """
    prefactor = 4 * np.pi * (m / (2 * np.pi * k_B * T))**(3/2)
    return prefactor * v**2 * np.exp(-m * v**2 / (2 * k_B * T))


def maxwell_velocity_1d(v, T, m):
    """
    一维麦克斯韦速度分布 1D Maxwell velocity distribution

    公式 Formula: f(v_x) = √(m/2πk_BT) × exp(-mv_x²/2k_BT)

    参数 Parameters:
        v: 速度分量 v_x (m/s)（可为正或负）- Velocity component
        T: 温度 (K) - Temperature
        m: 分子质量 (kg) - Molecular mass

    返回 Returns:
        f(v_x): 速度分量的概率密度

    注意 Note:
        这是高斯分布，中心在 v_x = 0
        标准差 σ = √(k_BT/m)
    """
    prefactor = np.sqrt(m / (2 * np.pi * k_B * T))
    return prefactor * np.exp(-m * v**2 / (2 * k_B * T))


def most_probable_speed(T, m):
    """
    最概然速率 Most probable speed

    公式 Formula: v_p = √(2k_BT/m)

    参数 Parameters:
        T: 温度 (K) - Temperature
        m: 分子质量 (kg) - Molecular mass

    返回 Returns:
        v_p: 最概然速率 (m/s)

    物理意义 Physical Meaning:
        速率分布函数 f(v) 的峰值位置
        即最多分子所具有的速率
    """
    return np.sqrt(2 * k_B * T / m)


def mean_speed(T, m):
    """
    平均速率 Mean (average) speed

    公式 Formula: <v> = √(8k_BT/πm) ≈ 1.128 × v_p

    参数 Parameters:
        T: 温度 (K) - Temperature
        m: 分子质量 (kg) - Molecular mass

    返回 Returns:
        v_mean: 平均速率 (m/s)

    应用 Applications:
        计算碰撞频率、输运系数等
    """
    return np.sqrt(8 * k_B * T / (np.pi * m))


def rms_speed(T, m):
    """
    均方根速率 Root-mean-square (RMS) speed

    公式 Formula: v_rms = √(3k_BT/m) = √<v²> ≈ 1.225 × v_p

    参数 Parameters:
        T: 温度 (K) - Temperature
        m: 分子质量 (kg) - Molecular mass

    返回 Returns:
        v_rms: 均方根速率 (m/s)

    物理意义 Physical Meaning:
        与平均动能直接相关: <E_k> = (1/2)m × v_rms² = (3/2)k_BT
    """
    return np.sqrt(3 * k_B * T / m)


def speed_ratios():
    """
    三种特征速率的比值 Ratios of three characteristic speeds

    公式 Formula: v_p : <v> : v_rms = 1 : √(4/π) : √(3/2) ≈ 1 : 1.128 : 1.225

    返回 Returns:
        (1, √(4/π), √(3/2)): 三个比值

    记忆技巧 Memorization:
        v_p < <v> < v_rms（从左到右依次增大）
    """
    return 1, np.sqrt(4/np.pi), np.sqrt(3/2)


# =============================================================================
# 练习 6.2: 能量分布
# Exercise 6.2: Energy Distribution
# =============================================================================
# 能量分布与能均分定理 Energy Distribution and Equipartition Theorem:
#
# 麦克斯韦-玻尔兹曼能量分布 Maxwell-Boltzmann Energy Distribution:
#   g(E) ∝ √E × exp(-E/k_BT)
#   - 低能时 g(E) ∝ √E（态密度因素）
#   - 高能时 g(E) ∝ exp(-E/k_BT)（玻尔兹曼因子）
#
# 能量均分定理 Equipartition Theorem:
#   每个平方项（动能或势能）平均贡献 (1/2)k_BT 的能量
#   - 单原子分子（3个平动自由度）: <E> = (3/2)k_BT
#   - 双原子分子（3平动 + 2转动）: <E> = (5/2)k_BT
#   - 非线性多原子分子（3平动 + 3转动）: <E> = 3k_BT

def maxwell_boltzmann_energy(E, T):
    """
    麦克斯韦-玻尔兹曼能量分布函数 Maxwell-Boltzmann energy distribution

    公式 Formula: g(E) = 2π(1/πk_BT)^(3/2) × √E × exp(-E/k_BT)

    参数 Parameters:
        E: 动能 (J) - Kinetic energy
        T: 温度 (K) - Temperature

    返回 Returns:
        g(E): 能量概率密度 (J⁻¹)

    物理意义 Physical Meaning:
        g(E) dE 是分子能量在 [E, E+dE] 范围内的概率
    """
    prefactor = 2 * np.pi * (1 / (np.pi * k_B * T))**(3/2)
    return prefactor * np.sqrt(E) * np.exp(-E / (k_B * T))


def mean_energy(T):
    """
    单原子分子的平均动能 Mean kinetic energy of monatomic molecule

    公式 Formula: <E> = (3/2)k_BT

    参数 Parameters:
        T: 温度 (K) - Temperature

    返回 Returns:
        E_mean: 平均动能 (J)

    物理意义 Physical Meaning:
        3个平动自由度，每个贡献 (1/2)k_BT
    """
    return 1.5 * k_B * T


def mean_energy_per_degree(T):
    """
    每个自由度的平均能量 Mean energy per degree of freedom

    公式 Formula: <E>₁ = (1/2)k_BT

    参数 Parameters:
        T: 温度 (K) - Temperature

    返回 Returns:
        E_per_dof: 每自由度能量 (J)

    应用 Application:
        这是能量均分定理的核心结果
    """
    return 0.5 * k_B * T


def energy_fluctuation(T):
    """
    能量涨落（方差）Energy fluctuation (variance)

    公式 Formula: <(ΔE)²> = <E²> - <E>² = (3/2)(k_BT)²

    参数 Parameters:
        T: 温度 (K) - Temperature

    返回 Returns:
        variance: 能量涨落 (J²)

    物理意义 Physical Meaning:
        热涨落反映了微观无序性
        相对涨落 √<ΔE²>/<E> = √(2/3) ≈ 0.82
    """
    return 1.5 * (k_B * T)**2


def equipartition_energy(f, T):
    """
    能量均分定理 Equipartition theorem

    公式 Formula: <E> = (f/2) × k_BT

    参数 Parameters:
        f: 自由度数 - Number of degrees of freedom
        T: 温度 (K) - Temperature

    返回 Returns:
        E_total: 总平均能量 (J)

    典型值 Typical Values:
        f = 3: 单原子分子（Ar, He）
        f = 5: 双原子分子室温（N₂, O₂，振动冻结）
        f = 6: 非线性分子（H₂O, CO₂）
    """
    return f * k_B * T / 2


# =============================================================================
# 练习 6.3: 压强和碰撞
# Exercise 6.3: Pressure and Collisions
# =============================================================================
# 压强的微观解释 Microscopic Interpretation of Pressure:
#
# 气体分子撞击容器壁产生压强：
#   P = (1/3) n m <v²> = n k_BT
#
# 单位面积的碰撞率 Wall Collision Rate:
#   Φ = n<v>/4（只有朝向壁面的分子才能碰撞）
#
# 逸散（Effusion）: 气体通过小孔流出
#   格雷厄姆定律：轻分子逸散更快

def pressure_kinetic(n, T, m):
    """
    理想气体压强（动理论推导）Ideal gas pressure from kinetic theory

    公式 Formula: P = n k_BT = (1/3) n m <v²>

    参数 Parameters:
        n: 分子数密度 (m⁻³) - Number density
        T: 温度 (K) - Temperature
        m: 分子质量 (kg) - Molecular mass

    返回 Returns:
        P: 压强 (Pa)

    物理意义 Physical Meaning:
        压强 = 分子对壁的平均动量传递率 / 面积
    """
    return n * k_B * T


def wall_collision_rate(n, T, m):
    """
    单位面积墙壁的碰撞率 Wall collision rate per unit area

    公式 Formula: Φ = n<v>/4

    参数 Parameters:
        n: 分子数密度 (m⁻³) - Number density
        T: 温度 (K) - Temperature
        m: 分子质量 (kg) - Molecular mass

    返回 Returns:
        Phi: 碰撞率 (m⁻²s⁻¹)，每秒每平方米的碰撞次数

    推导 Derivation:
        只有 v_x > 0 的分子才能撞击 x 方向的壁面
        考虑半球立体角积分得到因子 1/4
    """
    v_mean = mean_speed(T, m)
    return n * v_mean / 4


def momentum_transfer_rate(n, T, m):
    """
    单位面积墙壁的动量传递率（等于压强）
    Momentum transfer rate per unit area (equals pressure)

    公式 Formula: P = 2m × Φ × <v_x>_{v_x>0}

    参数 Parameters:
        n: 分子数密度 (m⁻³)
        T: 温度 (K)
        m: 分子质量 (kg)

    返回 Returns:
        P: 压强 (Pa)

    物理意义 Physical Meaning:
        每个分子碰撞壁面后动量变化 2m v_x（弹性碰撞）
    """
    Phi = wall_collision_rate(n, T, m)
    v_mean_x_positive = np.sqrt(k_B * T / (2 * np.pi * m))  # v_x > 0 的平均值
    return 2 * m * Phi * v_mean_x_positive


def effusion_rate(P, T, m, A):
    """
    气体逸散率（小孔流出）Effusion rate through a small hole

    公式 Formula: dN/dt = PA / √(2πmk_BT)

    参数 Parameters:
        P: 压强 (Pa) - Pressure
        T: 温度 (K) - Temperature
        m: 分子质量 (kg) - Molecular mass
        A: 小孔面积 (m²) - Hole area

    返回 Returns:
        rate: 逸散率（分子数/秒）

    条件 Condition:
        小孔直径 << 平均自由程（克努森逸散）
    """
    return P * A / np.sqrt(2 * np.pi * m * k_B * T)


def graham_law_ratio(m1, m2):
    """
    格雷厄姆逸散定律 Graham's law of effusion

    公式 Formula: rate₁/rate₂ = √(m₂/m₁)

    参数 Parameters:
        m1: 气体1的分子质量 (kg)
        m2: 气体2的分子质量 (kg)

    返回 Returns:
        ratio: 逸散速率比

    应用 Applications:
        - 同位素分离（如铀浓缩的气体扩散法）
        - 气体分子量测定
    """
    return np.sqrt(m2 / m1)


# =============================================================================
# 练习 6.4: 平均自由程
# Exercise 6.4: Mean Free Path
# =============================================================================
# 平均自由程 Mean Free Path:
#
# 分子在两次碰撞之间平均行进的距离
# λ = 1/(√2 n π d²)，其中 √2 来自相对速度
#
# 典型数值 Typical Values:
#   - 常温常压空气: λ ≈ 70 nm
#   - 低压真空 (1 Pa): λ ≈ 7 mm
#   - 超高真空 (10⁻⁶ Pa): λ ≈ 70 km
#
# Knudsen数 Knudsen Number:
#   Kn = λ/L（平均自由程与特征尺度之比）
#   Kn << 1: 连续介质流动
#   Kn >> 1: 自由分子流（稀薄气体）

def mean_free_path(n, d):
    """
    平均自由程 Mean free path

    公式 Formula: λ = 1/(√2 × n × π × d²)

    参数 Parameters:
        n: 分子数密度 (m⁻³) - Number density
        d: 分子有效直径 (m) - Effective molecular diameter

    返回 Returns:
        lambda: 平均自由程 (m)

    典型分子直径 Typical Molecular Diameters:
        N₂: 3.7×10⁻¹⁰ m
        O₂: 3.6×10⁻¹⁰ m
        Ar: 3.4×10⁻¹⁰ m
    """
    return 1 / (np.sqrt(2) * n * np.pi * d**2)


def mean_free_path_from_PT(P, T, d):
    """
    从压强和温度计算平均自由程 Mean free path from P and T

    公式 Formula: λ = k_BT/(√2 × P × π × d²)

    参数 Parameters:
        P: 压强 (Pa) - Pressure
        T: 温度 (K) - Temperature
        d: 分子有效直径 (m)

    返回 Returns:
        lambda: 平均自由程 (m)

    注意 Note:
        λ ∝ T/P，高温低压时平均自由程增大
    """
    n = P / (k_B * T)  # 理想气体状态方程
    return mean_free_path(n, d)


def collision_frequency(n, T, m, d):
    """
    碰撞频率 Collision frequency

    公式 Formula: z = √2 × n × π × d² × <v>

    参数 Parameters:
        n: 分子数密度 (m⁻³)
        T: 温度 (K)
        m: 分子质量 (kg)
        d: 分子有效直径 (m)

    返回 Returns:
        z: 碰撞频率 (s⁻¹)，单个分子每秒的平均碰撞次数

    典型值 Typical Value:
        常温常压: z ≈ 10⁹ s⁻¹
    """
    v_mean = mean_speed(T, m)
    return np.sqrt(2) * n * np.pi * d**2 * v_mean


def mean_free_time(n, T, m, d):
    """
    平均自由时间 Mean free time

    公式 Formula: τ = λ/<v> = 1/z

    参数 Parameters:
        n: 分子数密度 (m⁻³)
        T: 温度 (K)
        m: 分子质量 (kg)
        d: 分子有效直径 (m)

    返回 Returns:
        tau: 平均自由时间 (s)，两次碰撞之间的平均时间

    典型值 Typical Value:
        常温常压: τ ≈ 10⁻⁹ s
    """
    z = collision_frequency(n, T, m, d)
    return 1 / z


def knudsen_number(lambda_mfp, L):
    """
    克努森数 Knudsen number

    公式 Formula: Kn = λ/L

    参数 Parameters:
        lambda_mfp: 平均自由程 (m)
        L: 系统特征尺度 (m)

    返回 Returns:
        Kn: 克努森数（无量纲）

    流动分类 Flow Regimes:
        Kn < 0.01: 连续流（纳维-斯托克斯方程适用）
        0.01 < Kn < 0.1: 滑移流
        0.1 < Kn < 10: 过渡流
        Kn > 10: 自由分子流
    """
    return lambda_mfp / L


# =============================================================================
# 练习 6.5: 输运系数
# Exercise 6.5: Transport Coefficients
# =============================================================================
# 输运现象 Transport Phenomena:
#
# 当系统存在宏观不均匀性时，会产生输运过程：
#   1. 粘度（动量输运）: 速度梯度 → 剪切应力
#   2. 热导率（能量输运）: 温度梯度 → 热流
#   3. 扩散系数（质量输运）: 浓度梯度 → 质量流
#
# 动理论给出这些输运系数的微观表达式，都正比于 λ<v>
#
# 重要结论 Important Results:
#   - 粘度不依赖于压强（在一定范围内）
#   - 粘度正比于 √T

def viscosity_kinetic(m, T, d):
    """
    粘度（动理论结果）Viscosity from kinetic theory

    公式 Formula: η = (5/16) × √(m k_BT/π) / (π d²)

    参数 Parameters:
        m: 分子质量 (kg)
        T: 温度 (K)
        d: 分子有效直径 (m)

    返回 Returns:
        eta: 动力粘度 (Pa·s)

    特点 Characteristics:
        - η ∝ √T（温度升高，粘度增大，与液体相反）
        - η 与压强无关（在一定范围内）
    """
    prefactor = 5 / 16
    return prefactor * np.sqrt(m * k_B * T / np.pi) / (np.pi * d**2)


def thermal_conductivity_kinetic(m, T, d, cv):
    """
    热导率（动理论结果）Thermal conductivity from kinetic theory

    公式 Formula: κ = (25/32) × √(k_BT/πm) × cv / (π d²)

    参数 Parameters:
        m: 分子质量 (kg)
        T: 温度 (K)
        d: 分子有效直径 (m)
        cv: 单分子热容 (J/K)

    返回 Returns:
        kappa: 热导率 (W/m·K)

    物理意义 Physical Meaning:
        热导率 = 热扩散系数 × 密度 × 比热容
    """
    prefactor = 25 / 32
    return prefactor * np.sqrt(k_B * T / (np.pi * m)) * cv / (np.pi * d**2)


def diffusion_coefficient(T, m, n, d):
    """
    自扩散系数 Self-diffusion coefficient

    公式 Formula: D = (3/16) × √(k_BT/πm) / (n d²)

    参数 Parameters:
        T: 温度 (K)
        m: 分子质量 (kg)
        n: 分子数密度 (m⁻³)
        d: 分子有效直径 (m)

    返回 Returns:
        D: 扩散系数 (m²/s)

    注意 Note:
        D ∝ 1/P（压强增大，扩散减慢）
        D ∝ T^(3/2)
    """
    prefactor = 3 / 16
    return prefactor * np.sqrt(k_B * T / (np.pi * m)) / (n * d**2)


def prandtl_number(eta, kappa, cp):
    """
    普朗特数 Prandtl number

    公式 Formula: Pr = η × cp / κ

    参数 Parameters:
        eta: 动力粘度 (Pa·s)
        kappa: 热导率 (W/m·K)
        cp: 定压比热容 (J/kg·K)

    返回 Returns:
        Pr: 普朗特数（无量纲）

    物理意义 Physical Meaning:
        Pr = ν/α（动量扩散系数/热扩散系数）
        描述速度边界层与热边界层的相对厚度
        空气 Pr ≈ 0.7
    """
    return eta * cp / kappa


def schmidt_number(eta, rho, D):
    """
    施密特数 Schmidt number

    公式 Formula: Sc = η / (ρ × D) = ν / D

    参数 Parameters:
        eta: 动力粘度 (Pa·s)
        rho: 密度 (kg/m³)
        D: 扩散系数 (m²/s)

    返回 Returns:
        Sc: 施密特数（无量纲）

    物理意义 Physical Meaning:
        Sc = ν/D（动量扩散系数/质量扩散系数）
        描述速度边界层与浓度边界层的相对厚度
    """
    return eta / (rho * D)


def sutherland_formula(T, T0, eta0, S):
    """
    萨瑟兰粘度公式 Sutherland's viscosity formula

    公式 Formula: η = η₀ × (T/T₀)^(3/2) × (T₀ + S)/(T + S)

    参数 Parameters:
        T: 目标温度 (K)
        T0: 参考温度 (K)
        eta0: 参考温度下的粘度 (Pa·s)
        S: 萨瑟兰常数 (K)

    返回 Returns:
        eta: 温度 T 下的粘度 (Pa·s)

    典型萨瑟兰常数 Typical S values:
        空气: S = 110.4 K
        N₂: S = 111 K
        O₂: S = 127 K
    """
    return eta0 * (T/T0)**1.5 * (T0 + S) / (T + S)


# =============================================================================
# 练习 6.6: 分子速度实验
# Exercise 6.6: Molecular Speed Experiments
# =============================================================================
# 实验验证麦克斯韦分布 Experimental Verification of Maxwell Distribution:
#
# 1. 斯特恩实验（Stern Experiment, 1920）
#    使用旋转转盘选择特定速度的分子
#
# 2. 飞行时间法（Time-of-Flight, TOF）
#    测量分子飞过已知距离的时间
#
# 3. 多普勒展宽（Doppler Broadening）
#    热运动导致的光谱线展宽

def stern_gerlach_velocity_selector(v, omega, r1, r2, n_slots):
    """
    斯特恩速度选择器 Stern velocity selector

    工作原理 Working Principle:
        两个有狭缝的转盘同轴旋转，只有特定速度的分子能通过

    公式 Formula: v = ω(r₂ - r₁)/θ

    参数 Parameters:
        v: 速度（未使用）
        omega: 转盘角速度 (rad/s)
        r1, r2: 两转盘的半径 (m)
        n_slots: 狭缝数目

    返回 Returns:
        v_selected: 被选择的速度 (m/s)
    """
    theta = 2 * np.pi / n_slots  # 狭缝角间距
    return omega * (r2 - r1) / theta


def time_of_flight_velocity(L, t):
    """
    飞行时间法测速度 Time-of-flight velocity measurement

    公式 Formula: v = L/t

    参数 Parameters:
        L: 飞行距离 (m)
        t: 飞行时间 (s)

    返回 Returns:
        v: 分子速度 (m/s)

    应用 Applications:
        分子束实验、质谱仪等
    """
    return L / t


def doppler_broadening(f0, T, m):
    """
    多普勒展宽 Doppler broadening

    公式 Formula: Δf/f₀ = √(8k_BT ln2 / mc²)（半高全宽）

    参数 Parameters:
        f0: 中心频率 (Hz)
        T: 温度 (K)
        m: 原子/分子质量 (kg)

    返回 Returns:
        Δf/f₀: 相对线宽（无量纲）

    物理意义 Physical Meaning:
        由于热运动，不同速度的原子发出不同频率的光
        导致光谱线展宽，是麦克斯韦分布的直接证据
    """
    c = 3e8  # 光速
    return np.sqrt(8 * k_B * T * np.log(2) / (m * c**2))


def most_probable_velocity_fraction(v1, v2, T, m):
    """
    速率在 [v1, v2] 之间的分子比例 Fraction of molecules with speed in [v1, v2]

    公式 Formula: fraction = ∫[v1,v2] f(v) dv

    参数 Parameters:
        v1, v2: 速率范围的下限和上限 (m/s)
        T: 温度 (K)
        m: 分子质量 (kg)

    返回 Returns:
        fraction: 分子比例（0 到 1 之间）
    """
    from scipy.integrate import quad

    def integrand(v):
        return maxwell_speed_distribution(v, T, m)

    fraction, _ = quad(integrand, v1, v2)
    return fraction


def escape_velocity_fraction(v_esc, T, m):
    """
    速率大于逃逸速度的分子比例 Fraction with speed > escape velocity

    公式 Formula: fraction = ∫[v_esc,∞] f(v) dv

    参数 Parameters:
        v_esc: 逃逸速度 (m/s)
        T: 温度 (K)
        m: 分子质量 (kg)

    返回 Returns:
        fraction: 能逃逸的分子比例

    应用 Application:
        解释行星大气逃逸（如为何月球几乎没有大气）
        地球逃逸速度 ≈ 11.2 km/s
    """
    from scipy.integrate import quad

    def integrand(v):
        return maxwell_speed_distribution(v, T, m)

    # 积分到足够大的速度（50倍均方根速率）
    fraction, _ = quad(integrand, v_esc, 50 * rms_speed(T, m))
    return fraction


# =============================================================================
# 可视化 Visualization
# =============================================================================
# 本节绘制气体动理论相关的图表:
# 1. 不同气体的麦克斯韦速率分布 - 轻分子分布更宽
# 2. N₂ 的三种特征速率标记 - v_p < <v> < v_rms
# 3. 温度对分布的影响 - 高温时分布变宽，峰值右移
# 4. 能量分布 - 低能时 ∝ √E，高能时指数衰减
# 5. 平均自由程与压强的关系 - 对数坐标
# 6. 粘度的温度依赖 - 动理论与萨瑟兰公式比较

def plot_kinetic_theory():
    """
    绘制气体动理论相关图表 Plot kinetic theory diagrams

    包含6个子图 Contains 6 subplots:
        1. 不同气体的速率分布
        2. 特征速率标记
        3. 温度对分布的影响
        4. 能量分布
        5. 平均自由程 vs 压强
        6. 粘度的温度依赖
    """
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    T = 300  # K

    # 1. Maxwell速率分布
    ax1 = axes[0, 0]
    v = np.linspace(0, 2000, 500)

    for gas, m, name in [(m_H2, 'H₂'), (m_N2, 'N₂'), (m_O2, 'O₂'), (m_Ar, 'Ar')]:
        f = maxwell_speed_distribution(v, T, gas)
        ax1.plot(v, f * 1e3, label=name, linewidth=2)

    ax1.set_xlabel('v (m/s)')
    ax1.set_ylabel('f(v) × 10³')
    ax1.set_title(f'Maxwell速率分布 (T = {T} K)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 特征速率标记
    ax2 = axes[0, 1]
    m = m_N2
    f = maxwell_speed_distribution(v, T, m)

    v_p = most_probable_speed(T, m)
    v_mean = mean_speed(T, m)
    v_rms_val = rms_speed(T, m)

    ax2.plot(v, f * 1e3, 'b-', linewidth=2)
    ax2.axvline(x=v_p, color='r', linestyle='--', label=f'v_p = {v_p:.0f} m/s')
    ax2.axvline(x=v_mean, color='g', linestyle='--', label=f'<v> = {v_mean:.0f} m/s')
    ax2.axvline(x=v_rms_val, color='orange', linestyle='--', label=f'v_rms = {v_rms_val:.0f} m/s')
    ax2.set_xlabel('v (m/s)')
    ax2.set_ylabel('f(v) × 10³')
    ax2.set_title('N₂ 特征速率')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 温度对分布的影响
    ax3 = axes[0, 2]
    m = m_N2

    for T_val in [100, 300, 600, 1000]:
        f = maxwell_speed_distribution(v, T_val, m)
        ax3.plot(v, f * 1e3, label=f'T = {T_val} K', linewidth=2)

    ax3.set_xlabel('v (m/s)')
    ax3.set_ylabel('f(v) × 10³')
    ax3.set_title('温度对分布的影响 (N₂)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 能量分布
    ax4 = axes[1, 0]
    E = np.linspace(0, 0.3, 200) * 1.6e-19  # eV to J

    for T_val in [300, 600, 1000]:
        g = maxwell_boltzmann_energy(E, T_val)
        ax4.plot(E / 1.6e-19 * 1000, g * 1.6e-19 / 1000, label=f'T = {T_val} K', linewidth=2)

    ax4.set_xlabel('E (meV)')
    ax4.set_ylabel('g(E)')
    ax4.set_title('能量分布')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 平均自由程
    ax5 = axes[1, 1]
    P = np.logspace(0, 5, 100)  # Pa
    d = 3.7e-10  # N₂直径

    lambda_mfp = [mean_free_path_from_PT(p, T, d) for p in P]

    ax5.loglog(P, lambda_mfp, 'b-', linewidth=2)
    ax5.axhline(y=1e-3, color='r', linestyle='--', alpha=0.5, label='1 mm')
    ax5.axhline(y=1e-6, color='g', linestyle='--', alpha=0.5, label='1 μm')
    ax5.set_xlabel('P (Pa)')
    ax5.set_ylabel('λ (m)')
    ax5.set_title('平均自由程 vs 压强')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. 粘度温度依赖
    ax6 = axes[1, 2]
    T_range = np.linspace(200, 1000, 100)
    d = 3.7e-10

    eta = [viscosity_kinetic(m_N2, T_val, d) for T_val in T_range]

    # Sutherland公式 (N₂: S = 111 K, η₀ = 1.75e-5 at 300K)
    eta_sutherland = [sutherland_formula(T_val, 300, 1.75e-5, 111) for T_val in T_range]

    ax6.plot(T_range, np.array(eta) * 1e6, 'b-', label='动理论', linewidth=2)
    ax6.plot(T_range, np.array(eta_sutherland) * 1e6, 'r--', label='Sutherland', linewidth=2)
    ax6.set_xlabel('T (K)')
    ax6.set_ylabel('η (μPa·s)')
    ax6.set_title('粘度温度依赖')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('kinetic_theory.png', dpi=150)
    print("图像已保存为 kinetic_theory.png")
    plt.show()


# =============================================================================
# 验证函数 Verification
# =============================================================================
def verify():
    """
    验证气体动理论练习的正确性 Verify kinetic theory exercises

    测试内容 Test Contents:
        - 6.1 麦克斯韦分布归一化
        - 6.2 特征速率比值
        - 6.3 平均能量
        - 6.4 平均自由程数量级
        - 6.5 粘度计算
        - 6.6 壁面碰撞率
    """
    all_passed = True

    T = 300  # 室温
    m = m_N2  # 氮气分子

    # 测试 6.1 - 麦克斯韦分布归一化 Maxwell distribution normalization
    v = np.linspace(0, 5000, 10000)
    f = maxwell_speed_distribution(v, T, m)
    dv = v[1] - v[0]
    integral = np.sum(f) * dv

    if not np.isclose(integral, 1, rtol=0.01):
        print(f"错误 6.1: 麦克斯韦分布应归一化为 1")
        print(f"  计算得到的积分值 = {integral:.4f}")
        all_passed = False
    else:
        print(f"通过 6.1: 麦克斯韦分布正确（积分 = {integral:.4f}）")

    # 测试 6.2 - 速率比值 Speed ratios
    v_p = most_probable_speed(T, m)
    v_mean = mean_speed(T, m)
    v_rms_val = rms_speed(T, m)

    ratio_mean = v_mean / v_p
    ratio_rms = v_rms_val / v_p

    if not np.isclose(ratio_mean, np.sqrt(4/np.pi), rtol=0.01):
        print("错误 6.2: 速率比值不正确")
        print(f"  期望 <v>/v_p = √(4/π) ≈ 1.128, 计算得到 {ratio_mean:.4f}")
        all_passed = False
    else:
        print(f"通过 6.2: 特征速率正确 (v_p={v_p:.0f}, <v>={v_mean:.0f}, v_rms={v_rms_val:.0f} m/s)")

    # 测试 6.3 - 平均能量 Mean energy
    E_mean = mean_energy(T)
    expected = 1.5 * k_B * T

    if not np.isclose(E_mean, expected, rtol=0.01):
        print("错误 6.3: 平均能量应为 (3/2)k_BT")
        all_passed = False
    else:
        print(f"通过 6.3: 能量分布正确 (<E> = {E_mean/1.6e-19*1000:.1f} meV)")

    # 测试 6.4 - 平均自由程 Mean free path
    P = 1e5  # 1 atm
    d = 3.7e-10  # N₂ 分子直径
    lambda_mfp = mean_free_path_from_PT(P, T, d)
    expected_order = 1e-7  # ~100 nm at 1 atm

    if lambda_mfp < expected_order / 10 or lambda_mfp > expected_order * 10:
        print("错误 6.4: 平均自由程数量级不正确")
        print(f"  常温常压下应约为 100 nm，计算得到 {lambda_mfp*1e9:.1f} nm")
        all_passed = False
    else:
        print(f"通过 6.4: 平均自由程正确 (λ = {lambda_mfp*1e9:.1f} nm at 1 atm)")

    # 测试 6.5 - 粘度 Viscosity
    eta = viscosity_kinetic(m_N2, T, d)
    expected_eta = 1.7e-5  # N₂ at 300K ~ 17 μPa·s

    if not np.isclose(eta, expected_eta, rtol=0.3):
        print(f"错误 6.5: 粘度计算偏差较大")
        print(f"  期望约 17 μPa·s，计算得到 {eta*1e6:.1f} μPa·s")
        all_passed = False
    else:
        print(f"通过 6.5: 输运系数正确 (η = {eta*1e6:.1f} μPa·s)")

    # 测试 6.6 - 壁面碰撞率 Wall collision rate
    n = P / (k_B * T)
    Phi = wall_collision_rate(n, T, m)

    if Phi <= 0:
        print("错误 6.6: 碰撞率应为正值")
        all_passed = False
    else:
        print(f"通过 6.6: 碰撞率正确 (Φ = {Phi:.2e} m⁻²s⁻¹)")

    if all_passed:
        print("\n所有测试通过！")
        try:
            plot_kinetic_theory()
        except Exception as ex:
            print(f"可视化失败: {ex}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("气体动理论 Kinetic Theory of Gases")
    print("=" * 50)
    verify()
