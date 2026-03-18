"""
电偶极子和磁偶极子 Electric and Magnetic Dipoles
难度 Difficulty: ★★★

学习目标 Learning Objectives:
- 理解电偶极子和磁偶极子的场分布 (Understand dipole field distributions)
- 掌握偶极子在外场中的行为 (Master dipole behavior in external fields)
- 分析偶极子间的相互作用 (Analyze dipole-dipole interactions)
- 了解感应偶极子和极化 (Understand induced dipoles and polarization)

物理背景 Physical Background:
偶极子是电磁学中的重要概念。电偶极子由一对等量异号电荷组成，
磁偶极子可以是电流环或基本粒子的固有磁矩。
偶极子场是多极展开的第一项，在远场近似中占主导。

核心公式 Key Formulas:
- 电偶极矩: p = qd [C·m]（从负电荷指向正电荷）
- 磁偶极矩: m = IA [A·m²]（电流环）
- 电偶极势: φ = p·cos(θ)/(4πε₀r²)
- 电偶极场: E_r = 2p·cos(θ)/(4πε₀r³), E_θ = p·sin(θ)/(4πε₀r³)
- 磁偶极场: B_r = μ₀·2m·cos(θ)/(4πr³), B_θ = μ₀·m·sin(θ)/(4πr³)
- 偶极子力矩: τ = p × E, τ = m × B
- 偶极子势能: U = -p·E, U = -m·B
- 玻尔磁子: μ_B = eℏ/(2m_e) ≈ 9.274×10⁻²⁴ J/T

分子物理应用 Molecular Physics:
- 极性分子具有永久电偶极矩（如水分子 p ≈ 6.2×10⁻³⁰ C·m）
- 非极性分子在电场中产生感应偶极矩
- 偶极子相互作用是分子间力的重要来源

单位说明 Units:
- 电偶极矩: C·m 或 D (德拜, 1D ≈ 3.336×10⁻³⁰ C·m)
- 磁偶极矩: A·m² 或 J/T
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import epsilon_0, mu_0, c, e, m_e, hbar

# I AM NOT DONE

# =============================================================================
# 练习 7.1: 电偶极矩
# Exercise 7.1: Electric Dipole Moment
# =============================================================================
# 物理背景 Physical Background:
# 电偶极子由距离为d的正负电荷±q组成。
# 偶极矩p是一个矢量，方向从负电荷指向正电荷。
# 在远场(r >> d)，偶极子场比点电荷场衰减更快(1/r³ vs 1/r²)。

def electric_dipole_moment(q, d):
    """
    电偶极矩
    Electric dipole moment

    参数 Parameters:
        q: 电荷量 [C]
        d: 电荷间距 [m]

    返回 Returns:
        偶极矩大小 p [C·m]

    公式 Formula:
        p = q × d

    说明: 偶极矩方向从负电荷指向正电荷
    """
    return q * d


def dipole_potential(p, r, theta):
    """
    电偶极子的电势（远场近似）
    Electric dipole potential (far field)

    参数 Parameters:
        p: 偶极矩大小 [C·m]
        r: 到偶极子中心的距离 [m]
        theta: 与偶极轴的夹角 [rad]

    返回 Returns:
        电势 φ [V]

    公式 Formula:
        φ = p·cos(θ)/(4πε₀r²)

    特点:
        θ = 0 (沿偶极方向): φ > 0
        θ = π/2 (垂直于偶极): φ = 0
        θ = π (反方向): φ < 0
    """
    # TODO: 计算电势 (Calculate potential)
    phi = (1 / (4 * np.pi * epsilon_0)) * p * np.cos(theta) / r**2
    return phi


def dipole_electric_field_r(p, r, theta):
    """
    电偶极子电场的径向分量
    Radial component of dipole electric field

    参数 Parameters:
        p: 偶极矩大小 [C·m]
        r: 距离 [m]
        theta: 与偶极轴夹角 [rad]

    返回 Returns:
        E_r [V/m]

    公式 Formula:
        E_r = (2p·cos(θ))/(4πε₀r³)

    说明: 沿径向，指向或背离偶极子
    """
    # TODO: 计算E_r
    E_r = (1 / (4 * np.pi * epsilon_0)) * 2 * p * np.cos(theta) / r**3
    return E_r


def dipole_electric_field_theta(p, r, theta):
    """
    电偶极子电场的角向分量
    Angular component of dipole electric field

    参数 Parameters:
        p: 偶极矩大小 [C·m]
        r: 距离 [m]
        theta: 与偶极轴夹角 [rad]

    返回 Returns:
        E_θ [V/m]

    公式 Formula:
        E_θ = (p·sin(θ))/(4πε₀r³)

    说明: 沿θ增大方向
    """
    # TODO: 计算E_theta
    E_theta = (1 / (4 * np.pi * epsilon_0)) * p * np.sin(theta) / r**3
    return E_theta


# =============================================================================
# 练习 7.2: 电偶极子在外场中
# Exercise 7.2: Electric Dipole in External Field
# =============================================================================
# 物理背景 Physical Background:
# 在均匀电场中，偶极子受力矩但不受净力。
# 力矩使偶极子趋向于与电场对齐（最低能量状态）。
# 在非均匀电场中，偶极子会被吸引到场强更大的区域。

def dipole_torque(p, E, theta):
    """
    电偶极子在均匀电场中的力矩
    Torque on electric dipole in uniform field

    参数 Parameters:
        p: 偶极矩大小 [C·m]
        E: 电场强度 [V/m]
        theta: 偶极矩与电场夹角 [rad]

    返回 Returns:
        力矩大小 τ [N·m]

    公式 Formula:
        τ = p × E = pE·sin(θ)

    说明: 力矩使偶极子转向与电场平行
    """
    return p * E * np.sin(theta)


def dipole_potential_energy(p, E, theta):
    """
    电偶极子在电场中的势能
    Potential energy of electric dipole in field

    参数 Parameters:
        p: 偶极矩大小 [C·m]
        E: 电场强度 [V/m]
        theta: 偶极矩与电场夹角 [rad]

    返回 Returns:
        势能 U [J]

    公式 Formula:
        U = -p·E = -pE·cos(θ)

    能量分析:
        θ = 0: U = -pE（最低，稳定平衡）
        θ = π/2: U = 0
        θ = π: U = +pE（最高，不稳定平衡）
    """
    # TODO: 计算势能 (Calculate potential energy)
    U = -p * E * np.cos(theta)
    return U


def dipole_force_nonuniform(p, dE_dz):
    """
    电偶极子在非均匀电场中的力
    Force on dipole in non-uniform field

    参数 Parameters:
        p: 偶极矩大小 [C·m]
        dE_dz: 电场沿z方向的梯度 [V/m²]

    返回 Returns:
        力 F [N]

    公式 Formula:
        F = (p·∇)E
        对于沿z方向的偶极子: F = p·(dE/dz)

    应用: 介电泳、电场梯度操纵分子
    """
    return p * dE_dz


# =============================================================================
# 练习 7.3: 磁偶极矩
# Exercise 7.3: Magnetic Dipole Moment
# =============================================================================
# 物理背景 Physical Background:
# 磁偶极子可以来自：
# 1. 电流环：m = IA，方向由右手定则确定
# 2. 粒子自旋：电子、质子等具有固有磁矩
# 玻尔磁子是原子磁矩的基本单位。

def magnetic_dipole_moment_loop(I, A):
    """
    电流环的磁偶极矩
    Magnetic dipole moment of current loop

    参数 Parameters:
        I: 电流 [A]
        A: 环的面积 [m²]

    返回 Returns:
        磁偶极矩 m [A·m²]

    公式 Formula:
        m = I × A

    方向: 由右手定则确定，四指沿电流方向，拇指指向m方向
    """
    return I * A


def magnetic_dipole_moment_spin(g, S):
    """
    自旋磁矩
    Spin magnetic moment

    参数 Parameters:
        g: 朗德g因子（电子约为2.002）
        S: 自旋角动量 [J·s]

    返回 Returns:
        磁矩 m [J/T]

    公式 Formula:
        m = g × (e/2m_e) × S

    说明: 电子自旋磁矩约为1个玻尔磁子
    """
    return g * (e / (2 * m_e)) * S


def bohr_magneton():
    """
    玻尔磁子
    Bohr magneton

    返回 Returns:
        μ_B [J/T] 或 [A·m²]

    公式 Formula:
        μ_B = eℏ/(2m_e) ≈ 9.274×10⁻²⁴ J/T

    意义: 原子磁矩的自然单位
    电子轨道磁矩为 μ_B 的整数倍
    """
    return e * hbar / (2 * m_e)


# =============================================================================
# 练习 7.4: 磁偶极子的场
# Exercise 7.4: Magnetic Dipole Field
# =============================================================================
# 物理背景 Physical Background:
# 磁偶极子的场与电偶极子场具有相同的角分布。
# 在远场，磁场强度与距离的三次方成反比。
# 地球磁场可近似为一个大磁偶极子产生的场。

def magnetic_dipole_field_r(m, r, theta):
    """
    磁偶极子磁场的径向分量（远场）
    Radial component of magnetic dipole field

    参数 Parameters:
        m: 磁偶极矩 [A·m²]
        r: 距离 [m]
        theta: 与磁矩方向的夹角 [rad]

    返回 Returns:
        B_r [T]

    公式 Formula:
        B_r = (μ₀/4π) × 2m·cos(θ)/r³
    """
    # TODO: 计算B_r
    B_r = (mu_0 / (4 * np.pi)) * 2 * m * np.cos(theta) / r**3
    return B_r


def magnetic_dipole_field_theta(m, r, theta):
    """
    磁偶极子磁场的角向分量
    Angular component of magnetic dipole field

    参数 Parameters:
        m: 磁偶极矩 [A·m²]
        r: 距离 [m]
        theta: 与磁矩方向的夹角 [rad]

    返回 Returns:
        B_θ [T]

    公式 Formula:
        B_θ = (μ₀/4π) × m·sin(θ)/r³
    """
    # TODO: 计算B_theta
    B_theta = (mu_0 / (4 * np.pi)) * m * np.sin(theta) / r**3
    return B_theta


def magnetic_dipole_field_z_axis(m, z):
    """
    磁偶极子沿轴上的场 (θ=0)
    Magnetic dipole field on axis

    参数 Parameters:
        m: 磁偶极矩 [A·m²]
        z: 轴上距离 [m]

    返回 Returns:
        B_z [T]

    公式 Formula:
        B_z = (μ₀/4π) × 2m/z³ = (μ₀/2π) × m/z³

    应用: 测量磁偶极矩的实验设计
    """
    return (mu_0 / (2 * np.pi)) * m / z**3


# =============================================================================
# 练习 7.5: 磁偶极子在外场中
# Exercise 7.5: Magnetic Dipole in External Field
# =============================================================================
# 物理背景 Physical Background:
# 磁偶极子在磁场中的行为与电偶极子在电场中类似。
# 力矩使磁矩趋向于与磁场平行（能量最低）。
# 如果磁矩与角动量耦合，会产生进动现象（拉莫尔进动）。

def magnetic_torque(m, B, theta):
    """
    磁偶极子在磁场中的力矩
    Torque on magnetic dipole in field

    参数 Parameters:
        m: 磁偶极矩 [A·m²]
        B: 磁场强度 [T]
        theta: 磁矩与磁场夹角 [rad]

    返回 Returns:
        力矩大小 τ [N·m]

    公式 Formula:
        τ = m × B = mB·sin(θ)
    """
    return m * B * np.sin(theta)


def magnetic_potential_energy(m, B, theta):
    """
    磁偶极子在磁场中的势能
    Potential energy of magnetic dipole in field

    参数 Parameters:
        m: 磁偶极矩 [A·m²]
        B: 磁场强度 [T]
        theta: 磁矩与磁场夹角 [rad]

    返回 Returns:
        势能 U [J]

    公式 Formula:
        U = -m·B = -mB·cos(θ)

    塞曼效应: 原子在磁场中能级分裂 ΔE = μ_B·B
    """
    return -m * B * np.cos(theta)


def larmor_frequency(B, g=2):
    """
    拉莫尔进动频率
    Larmor precession frequency

    参数 Parameters:
        B: 磁场强度 [T]
        g: 朗德g因子（电子约为2）

    返回 Returns:
        角频率 ω_L [rad/s]

    公式 Formula:
        ω_L = g × e × B / (2m_e)

    物理意义: 磁矩绕磁场方向进动的角频率
    电子在1T磁场中: ω_L ≈ 1.76×10¹¹ rad/s

    应用: 核磁共振(NMR)、电子自旋共振(ESR)
    """
    return g * e * B / (2 * m_e)


# =============================================================================
# 练习 7.6: 偶极子-偶极子相互作用
# Exercise 7.6: Dipole-Dipole Interaction
# =============================================================================
# 物理背景 Physical Background:
# 偶极子-偶极子相互作用能与距离的三次方成反比。
# 相互作用强烈依赖于取向：头尾排列吸引，并排排列排斥。
# 这种相互作用是液晶、铁电体等材料性质的基础。

def electric_dipole_interaction_energy(p1, p2, r, theta1, theta2, phi):
    """
    两个电偶极子之间的相互作用能
    Interaction energy between two electric dipoles

    参数 Parameters:
        p1, p2: 两个偶极矩大小 [C·m]
        r: 偶极子间距离 [m]
        theta1, theta2: 各偶极子与连线的夹角 [rad]
        phi: 两偶极子绕连线的相对方位角 [rad]

    返回 Returns:
        相互作用能 U [J]

    公式 Formula:
        U = (p₁p₂)/(4πε₀r³) × [2cos(θ₁)cos(θ₂) - sin(θ₁)sin(θ₂)cos(φ)]

    特殊情况:
        头尾相连(θ₁=θ₂=0): U = -2p₁p₂/(4πε₀r³) < 0（吸引）
        并排(θ₁=θ₂=π/2, φ=0): U = -p₁p₂/(4πε₀r³) < 0（吸引）
        反并排(θ₁=θ₂=π/2, φ=π): U = +p₁p₂/(4πε₀r³) > 0（排斥）
    """
    prefactor = 1 / (4 * np.pi * epsilon_0 * r**3)
    angular = (2 * np.cos(theta1) * np.cos(theta2) -
               np.sin(theta1) * np.sin(theta2) * np.cos(phi))

    # TODO: 计算相互作用能 (Calculate interaction energy)
    U = prefactor * p1 * p2 * angular
    return U


def magnetic_dipole_interaction_energy(m1, m2, r, config='parallel'):
    """
    两个磁偶极子的相互作用能
    Interaction energy between two magnetic dipoles

    参数 Parameters:
        m1, m2: 两个磁偶极矩 [A·m²]
        r: 偶极子间距离 [m]
        config: 配置 'parallel'(头尾)或'perpendicular'(并排)

    返回 Returns:
        相互作用能 U [J]

    配置说明:
        parallel: 两磁矩平行且沿连线（头尾相连）
        perpendicular: 两磁矩平行但垂直于连线（并排）
    """
    prefactor = mu_0 / (4 * np.pi * r**3)

    if config == 'parallel':
        # 头尾相连配置: 吸引
        U = -2 * prefactor * m1 * m2
    elif config == 'perpendicular':
        # 并排配置: 排斥
        U = prefactor * m1 * m2
    else:
        U = 0

    return U


# =============================================================================
# 练习 7.7: 感应偶极子
# Exercise 7.7: Induced Dipoles
# =============================================================================
# 物理背景 Physical Background:
# 非极性原子/分子在电场中会被极化，产生感应偶极矩。
# 极化率α描述了感应偶极矩与电场的关系。
# 感应偶极子间的相互作用导致范德瓦尔斯力。

def polarizability_hydrogen():
    """
    氢原子的极化率（近似）
    Polarizability of hydrogen atom (approximate)

    返回 Returns:
        极化率 α [C²·m²/J]

    公式 Formula:
        α ≈ 4πε₀a₀³

    其中 a₀ 是玻尔半径
    数值: α ≈ 6.67×10⁻⁴¹ C²·m²/J
    """
    from utils.constants import a_0
    return 4 * np.pi * epsilon_0 * a_0**3


def induced_dipole_moment(alpha, E):
    """
    感应偶极矩
    Induced dipole moment

    参数 Parameters:
        alpha: 极化率 [C²·m²/J]
        E: 电场强度 [V/m]

    返回 Returns:
        感应偶极矩 p_ind [C·m]

    公式 Formula:
        p_ind = α × E

    说明: 线性响应，适用于弱电场
    """
    return alpha * E


def van_der_waals_energy(alpha1, alpha2, r, I1, I2):
    """
    范德瓦尔斯相互作用能（London色散力）
    van der Waals interaction energy (London dispersion)

    参数 Parameters:
        alpha1, alpha2: 两原子的极化率 [C²·m²/J]
        r: 原子间距 [m]
        I1, I2: 两原子的电离能 [J]

    返回 Returns:
        相互作用能 U [J]

    公式 Formula:
        U = -C₆/r⁶
        C₆ ≈ (3/2) × α₁α₂I₁I₂/(I₁+I₂)

    物理机制: 量子涨落产生瞬时偶极矩，诱导邻近原子极化
    特点: 普遍存在，与r⁶成反比
    """
    C6 = (3/2) * alpha1 * alpha2 * I1 * I2 / (I1 + I2)
    return -C6 / r**6


def debye_interaction(p_perm, alpha, r):
    """
    Debye相互作用（永久偶极子与感应偶极子）
    Debye interaction (permanent-induced dipole)

    参数 Parameters:
        p_perm: 永久偶极矩 [C·m]
        alpha: 非极性分子的极化率 [C²·m²/J]
        r: 分子间距 [m]

    返回 Returns:
        相互作用能 U [J]（热平均后）

    公式 Formula:
        U = -p²α/(4πε₀)²/r⁶

    物理机制: 极性分子的电场诱导非极性分子极化
    特点: 与r⁶成反比，总是吸引的
    """
    return -p_perm**2 * alpha / (4 * np.pi * epsilon_0)**2 / r**6


# =============================================================================
# 可视化
# =============================================================================
def plot_dipoles():
    """绘制偶极子相关图"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # 1. 电偶极子场线
    ax1 = axes[0, 0]
    p = 1e-30  # C·m (典型分子偶极矩量级)

    # 创建网格
    x = np.linspace(-2, 2, 50) * 1e-9
    z = np.linspace(-2, 2, 50) * 1e-9
    X, Z = np.meshgrid(x, z)

    # 计算场
    r = np.sqrt(X**2 + Z**2)
    r[r < 0.1e-9] = 0.1e-9  # 避免奇点
    theta = np.arctan2(np.abs(X), Z)

    E_r = dipole_electric_field_r(p, r, theta)
    E_theta = dipole_electric_field_theta(p, r, theta)

    # 转换到笛卡尔坐标
    E_x = E_r * np.sin(theta) + E_theta * np.cos(theta) * np.sign(X)
    E_z = E_r * np.cos(theta) - E_theta * np.sin(theta)

    # 归一化用于流线图
    E_mag = np.sqrt(E_x**2 + E_z**2)
    E_x_norm = E_x / E_mag
    E_z_norm = E_z / E_mag

    ax1.streamplot(X * 1e9, Z * 1e9, E_x_norm, E_z_norm, density=1.5, color='b')
    ax1.scatter([0], [0], s=100, c='r', marker='o', label='Dipole')
    ax1.set_xlabel('x (nm)')
    ax1.set_ylabel('z (nm)')
    ax1.set_title('电偶极子场线')
    ax1.set_aspect('equal')
    ax1.legend()

    # 2. 偶极子势能 vs 角度
    ax2 = axes[0, 1]
    theta_range = np.linspace(0, 2 * np.pi, 100)

    # 电偶极子
    p_val = 1e-30
    E_field = 1e6  # V/m
    U_electric = [dipole_potential_energy(p_val, E_field, theta) / e
                  for theta in theta_range]

    # 磁偶极子
    mu_B_val = bohr_magneton()
    B_field = 1  # T
    U_magnetic = [magnetic_potential_energy(mu_B_val, B_field, theta) / e * 1e3
                  for theta in theta_range]  # meV

    ax2.plot(theta_range * 180 / np.pi, U_electric, 'b-', linewidth=2,
            label='Electric (eV)')
    ax2.plot(theta_range * 180 / np.pi, U_magnetic, 'r-', linewidth=2,
            label='Magnetic (meV)')
    ax2.set_xlabel('Angle (degrees)')
    ax2.set_ylabel('Potential Energy')
    ax2.set_title('偶极子在外场中的势能')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 偶极子-偶极子相互作用
    ax3 = axes[1, 0]
    r_range = np.linspace(0.3, 3, 100) * 1e-9
    p1 = p2 = 1e-30  # C·m

    # 平行配置
    U_parallel = [electric_dipole_interaction_energy(p1, p2, r, 0, 0, 0) / e * 1e3
                  for r in r_range]
    # 反平行配置
    U_anti = [electric_dipole_interaction_energy(p1, p2, r, np.pi, 0, 0) / e * 1e3
              for r in r_range]
    # 垂直配置
    U_perp = [electric_dipole_interaction_energy(p1, p2, r, np.pi/2, np.pi/2, 0) / e * 1e3
              for r in r_range]

    ax3.plot(r_range * 1e9, U_parallel, 'b-', linewidth=2, label='Parallel (head-tail)')
    ax3.plot(r_range * 1e9, U_anti, 'r-', linewidth=2, label='Anti-parallel')
    ax3.plot(r_range * 1e9, U_perp, 'g-', linewidth=2, label='Perpendicular')
    ax3.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    ax3.set_xlabel('Distance (nm)')
    ax3.set_ylabel('Interaction Energy (meV)')
    ax3.set_title('偶极子-偶极子相互作用')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim(-10, 10)

    # 4. 范德瓦尔斯势
    ax4 = axes[1, 1]
    from utils.constants import a_0
    alpha = polarizability_hydrogen()
    I_H = 13.6 * e  # 氢电离能

    r_vdw = np.linspace(3, 15, 100) * a_0
    U_vdw = [van_der_waals_energy(alpha, alpha, r, I_H, I_H) / e * 1e3
             for r in r_vdw]

    ax4.plot(r_vdw / a_0, U_vdw, 'b-', linewidth=2)
    ax4.set_xlabel('Distance (a_0)')
    ax4.set_ylabel('van der Waals Energy (meV)')
    ax4.set_title('范德瓦尔斯相互作用 (H-H)')
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('dipoles.png', dpi=150)
    print("图像已保存为 dipoles.png")
    plt.show()


# =============================================================================
# 验证函数
# =============================================================================
def verify():
    """
    验证所有偶极子练习
    Verify all dipole exercises

    验证内容 Verification:
        7.1 电偶极矩计算
        7.2 偶极子势能
        7.3 玻尔磁子
        7.4 磁偶极场
        7.5 拉莫尔进动频率
        7.6 偶极子-偶极子相互作用
        7.7 原子极化率
    """
    all_passed = True

    # 验证 7.1: 电偶极矩
    # Check 7.1: Electric dipole moment
    q = e
    d = 1e-10  # 1埃 (1 Angstrom)
    p = electric_dipole_moment(q, d)
    if not np.isclose(p, e * 1e-10):
        print("❌ 7.1 电偶极矩计算错误")
        print("   提示: p = q × d")
        all_passed = False
    else:
        print(f"✓ 7.1 电偶极矩正确 (p = {p:.2e} C·m)")

    # 验证 7.2: 偶极子在电场中的势能
    # Check 7.2: Dipole potential energy in field
    E_field = 1e6  # V/m
    U_0 = dipole_potential_energy(p, E_field, 0)      # θ = 0
    U_pi = dipole_potential_energy(p, E_field, np.pi)  # θ = π
    if U_0 >= U_pi:
        print("❌ 7.2 势能应在θ=0时最小（稳定平衡）")
        print("   提示: U = -pE·cos(θ)")
        all_passed = False
    else:
        print(f"✓ 7.2 偶极子势能正确 (最低: U(0) = {U_0/e:.6f} eV)")

    # 验证 7.3: 玻尔磁子
    # Check 7.3: Bohr magneton
    mu_B = bohr_magneton()
    expected_mu_B = 9.274e-24  # J/T
    if not np.isclose(mu_B, expected_mu_B, rtol=0.01):
        print("❌ 7.3 玻尔磁子错误")
        print("   提示: μ_B = eℏ/(2m_e) ≈ 9.274×10⁻²⁴ J/T")
        all_passed = False
    else:
        print(f"✓ 7.3 磁偶极矩正确 (μ_B = {mu_B:.3e} J/T)")

    # 验证 7.4: 磁偶极场
    # Check 7.4: Magnetic dipole field
    m = mu_B
    r = 1e-9  # 1 nm
    B_axis = magnetic_dipole_field_z_axis(m, r)
    if B_axis <= 0:
        print("❌ 7.4 磁场计算错误（场强应为正）")
        print("   提示: B_z = (μ₀/2π) × m/z³")
        all_passed = False
    else:
        print(f"✓ 7.4 磁偶极场正确 (轴上1nm处: B = {B_axis:.2e} T)")

    # 验证 7.5: 拉莫尔进动频率
    # Check 7.5: Larmor precession frequency
    B = 1  # Tesla
    omega_L = larmor_frequency(B)
    expected_omega = 1.76e11  # rad/s (约)
    if not np.isclose(omega_L, expected_omega, rtol=0.1):
        print("❌ 7.5 拉莫尔频率错误")
        print("   提示: ω_L = g·e·B/(2m_e)，电子在1T磁场中约1.76×10¹¹ rad/s")
        all_passed = False
    else:
        print(f"✓ 7.5 拉莫尔频率正确 (ω_L = {omega_L:.2e} rad/s)")

    # 验证 7.6: 偶极子-偶极子相互作用
    # Check 7.6: Dipole-dipole interaction
    p1 = p2 = 1e-30  # C·m
    r = 1e-9
    U_dd = electric_dipole_interaction_energy(p1, p2, r, 0, 0, 0)
    if U_dd >= 0:
        print("❌ 7.6 头尾排列的偶极子应相互吸引（U < 0）")
        all_passed = False
    else:
        print(f"✓ 7.6 偶极子相互作用正确（头尾吸引）")

    # 验证 7.7: 原子极化率
    # Check 7.7: Atomic polarizability
    alpha = polarizability_hydrogen()
    from utils.constants import a_0
    alpha_expected = 4 * np.pi * epsilon_0 * a_0**3
    if not np.isclose(alpha, alpha_expected, rtol=0.01):
        print("❌ 7.7 极化率错误")
        print("   提示: α ≈ 4πε₀a₀³")
        all_passed = False
    else:
        print(f"✓ 7.7 极化率正确 (α_H = {alpha:.2e} C²·m²/J)")

    if all_passed:
        print("\n🎉 所有测试通过！正在生成可视化...")
        try:
            plot_dipoles()
        except Exception as e:
            print(f"可视化生成失败: {e}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("电偶极子和磁偶极子 Electric and Magnetic Dipoles")
    print("=" * 50)
    verify()
