"""
测地线方程 Geodesic Equations
难度 Difficulty: ★★★★★

学习目标 Learning Objectives:
- 理解测地线作为弯曲时空中"最直"路径的几何意义
- 掌握克里斯托费尔符号（联络系数）的物理含义和计算方法
- 分析自由落体粒子在引力场中的运动轨迹
- 理解有效势能方法在分析轨道运动中的应用
- 计算广义相对论的经典检验：光线偏折和近日点进动

物理背景 Physical Background:
在广义相对论中，自由落体粒子沿测地线运动。测地线是弯曲时空中两点间的
"最直"路径，类似于平面上的直线或球面上的大圆。测地线方程将时空几何
（通过克里斯托费尔符号）与粒子运动联系起来，体现了爱因斯坦的核心思想：
"物质告诉时空如何弯曲，时空告诉物质如何运动"。

关键概念 Key Concepts:
- 测地线：自由粒子在弯曲时空中的世界线
- 克里斯托费尔符号：描述坐标基矢如何随位置变化
- 有效势能：将轨道问题简化为一维问题的强大工具
- 光线偏折：爱因斯坦1919年日食验证的著名预言
- 近日点进动：水星轨道异常的广义相对论解释

关键公式 Key Formulas:
- 测地线方程: d²x^μ/dτ² + Γ^μ_νσ (dx^ν/dτ)(dx^σ/dτ) = 0
- 克里斯托费尔符号: Γ^λ_μν = (1/2)g^λρ(∂_μg_ρν + ∂_νg_ρμ - ∂_ρg_μν)
- 有效势能: V_eff = -GM/r + L²/(2r²) - GML²/(c²r³)
- 光线偏折角: δφ ≈ 4GM/(bc²)
- 近日点进动: Δφ = 6πGM/(c²a(1-e²))

单位说明 Units:
- 角动量 Angular momentum: kg·m²/s
- 进动角 Precession angle: 弧度 rad 或 角秒 arcsec
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import G, c, M_sun

# I AM NOT DONE

# =============================================================================
# 练习 1.1: 平坦时空中的测地线
# Exercise 1.1: Geodesics in Flat Spacetime
#
# 物理背景 Physical Background:
# 在没有引力的平坦时空（闵可夫斯基时空）中，测地线就是直线。
# 这对应于牛顿力学中的惯性运动：没有外力作用时，物体做匀速直线运动。
# 闵可夫斯基度规: ds² = -c²dt² + dx² + dy² + dz²
#
# 数学形式 Mathematical Form:
# 由于克里斯托费尔符号全为零，测地线方程简化为:
# d²x^μ/dτ² = 0
# 解为: x^μ(τ) = x₀^μ + u^μ τ，其中u^μ是四速度
# =============================================================================

def flat_spacetime_geodesic(x0, v0, tau_max, n_points=100):
    """
    计算平坦时空中的测地线（直线运动）
    Calculate geodesic in flat spacetime (straight line motion)

    闵可夫斯基时空度规 Minkowski metric: ds² = -c²dt² + dx² + dy² + dz²
    测地线解 Geodesic solution: x(τ) = x₀ + v₀×τ

    参数 Parameters:
        x0: 初始位置 Initial position (m)
        v0: 初始速度 Initial velocity (m/s)
        tau_max: 最大固有时间 Maximum proper time (s)
        n_points: 采样点数 Number of sample points

    返回 Returns:
        tau: 固有时间数组 Proper time array (s)
        x: 位置数组 Position array (m)
    """
    tau = np.linspace(0, tau_max, n_points)
    # TODO: 计算平坦时空中的测地线
    # 提示：在没有引力的情况下，这就是简单的匀速直线运动
    x = x0 + v0 * tau
    return tau, x


# =============================================================================
# 练习 1.2: 史瓦西度规的克里斯托费尔符号
# Exercise 1.2: Christoffel Symbols for Schwarzschild Metric
#
# 物理背景 Physical Background:
# 克里斯托费尔符号（也称为联络系数或Levi-Civita联络）描述了
# 坐标基矢如何随位置变化。它们是度规张量的一阶导数的组合，
# 包含了时空弯曲的全部信息。
#
# 物理意义 Physical Meaning:
# - Γ^r_tt: 描述静止粒子感受到的"引力加速度"
# - Γ^t_rt: 描述引力场对时间坐标的影响
# - 这些符号在测地线方程中起到"力"的作用
#
# 计算方法 Calculation Method:
# Γ^λ_μν = (1/2)g^λρ(∂_μg_ρν + ∂_νg_ρμ - ∂_ρg_μν)
# =============================================================================

def christoffel_schwarzschild_radial(r, r_s):
    """
    计算史瓦西度规的径向克里斯托费尔符号 Γ^r_tt
    Calculate radial Christoffel symbol for Schwarzschild metric

    公式 Formula: Γ^r_tt = (c²r_s/2r²)(1 - r_s/r)

    参数 Parameters:
        r: 径向坐标 Radial coordinate (m)
        r_s: 史瓦西半径 Schwarzschild radius (m)

    返回 Returns:
        Gamma_r_tt: 克里斯托费尔符号 Γ^r_tt (m/s²)

    物理意义 Physical Meaning:
        这个分量与静止粒子感受到的"引力加速度"相关
        在牛顿极限下，它趋近于 GM/r² = g
    """
    if r <= r_s:
        return np.inf  # 在视界内，坐标奇异
    # TODO: 计算 Γ^r_tt
    # 提示：这是导致径向"引力"的主要项
    Gamma_r_tt = (c**2 * r_s / (2 * r**2)) * (1 - r_s / r)
    return Gamma_r_tt


def christoffel_schwarzschild_time(r, r_s):
    """
    计算史瓦西度规的时间分量克里斯托费尔符号 Γ^t_rt
    Calculate time component Christoffel symbol for Schwarzschild metric

    公式 Formula: Γ^t_rt = r_s / (2r(r - r_s))

    参数 Parameters:
        r: 径向坐标 Radial coordinate (m)
        r_s: 史瓦西半径 Schwarzschild radius (m)

    返回 Returns:
        Gamma_t_rt: 克里斯托费尔符号 Γ^t_rt (1/m)

    物理意义 Physical Meaning:
        这个分量描述了径向运动如何影响时间坐标的演化
        它与引力红移和时间膨胀效应相关
    """
    if r <= r_s:
        return np.inf  # 在视界内，坐标奇异
    # TODO: 计算 Γ^t_rt
    # 提示：注意分母中的 (r - r_s) 项
    Gamma_t_rt = r_s / (2 * r * (r - r_s))
    return Gamma_t_rt


# =============================================================================
# 练习 1.3: 径向自由落体的测地线
# Exercise 1.3: Radial Free Fall Geodesic
#
# 物理背景 Physical Background:
# 这是广义相对论中最基本的问题之一：描述一个粒子沿径向自由落入
# 史瓦西黑洞的运动。测地线方程是一组耦合的常微分方程，需要数值求解。
#
# 方程结构 Equation Structure:
# 对于径向运动（θ和φ不变），测地线方程简化为：
# d²t/dτ² + 2Γ^t_rt (dr/dτ)(dt/dτ) = 0
# d²r/dτ² + Γ^r_tt (dt/dτ)² + Γ^r_rr (dr/dτ)² = 0
#
# 数值方法 Numerical Method:
# 将二阶ODE转化为一阶ODE组：
# state = [t, r, dt/dτ, dr/dτ]
# =============================================================================

def radial_geodesic_equations(state, tau, M):
    """
    径向测地线方程的微分形式（用于数值积分）
    Differential form of radial geodesic equations (for numerical integration)

    状态向量 State vector: [t, r, dt/dτ, dr/dτ]

    测地线方程 Geodesic equations:
    d²t/dτ² + 2Γ^t_rt (dr/dτ)(dt/dτ) = 0
    d²r/dτ² + Γ^r_tt (dt/dτ)² + Γ^r_rr (dr/dτ)² = 0

    参数 Parameters:
        state: 状态向量 [t, r, dt/dτ, dr/dτ]
        tau: 固有时间 Proper time (s)
        M: 黑洞质量 Black hole mass (kg)

    返回 Returns:
        导数向量 [dt/dτ, dr/dτ, d²t/dτ², d²r/dτ²]
    """
    t, r, dt_dtau, dr_dtau = state
    r_s = 2 * G * M / c**2

    if r <= r_s * 1.001:  # 接近视界时停止计算，避免数值奇异
        return [0, 0, 0, 0]

    # 计算克里斯托费尔符号
    # Christoffel symbols
    Gamma_t_rt = r_s / (2 * r * (r - r_s))          # 时间-径向混合项
    Gamma_r_tt = (c**2 * r_s / (2 * r**2)) * (1 - r_s / r)  # 径向"引力"项
    Gamma_r_rr = -r_s / (2 * r * (r - r_s))         # 纯径向项

    # TODO: 计算测地线方程的右端项
    # 提示：这些方程描述了粒子在弯曲时空中的"加速度"
    d2t_dtau2 = -2 * Gamma_t_rt * dr_dtau * dt_dtau
    d2r_dtau2 = -Gamma_r_tt * dt_dtau**2 - Gamma_r_rr * dr_dtau**2

    return [dt_dtau, dr_dtau, d2t_dtau2, d2r_dtau2]


def solve_radial_geodesic(r0, M, tau_max, n_points=1000):
    """
    求解径向自由落体的测地线
    初始条件: 静止释放于r₀
    """
    r_s = 2 * G * M / c**2

    # 初始条件: 静止释放
    # 对于静止观察者, dt/dτ = 1/√(1-r_s/r)
    dt_dtau_0 = 1 / np.sqrt(1 - r_s / r0)
    dr_dtau_0 = 0

    state0 = [0, r0, dt_dtau_0, dr_dtau_0]
    tau = np.linspace(0, tau_max, n_points)

    solution = odeint(radial_geodesic_equations, state0, tau, args=(M,))

    return tau, solution[:, 0], solution[:, 1]  # tau, t, r


# =============================================================================
# 练习 1.4: 有效势能
# Exercise 1.4: Effective Potential
#
# 物理背景 Physical Background:
# 有效势能方法是分析轨道运动的强大工具。通过引入有效势能，
# 可以将二维轨道问题简化为一维的"能量守恒"问题。
#
# 公式比较 Formula Comparison:
# 牛顿力学: V_eff = -GM/r + L²/(2r²)
# 广义相对论: V_eff = -GM/r + L²/(2r²) - GML²/(c²r³)
#
# 广义相对论修正项的影响 Effect of GR Correction:
# - 最后一项 -GML²/(c²r³) 是纯粹的广义相对论效应
# - 在小r处，这一项变得重要，导致轨道不闭合（进动）
# - 这一项解释了水星近日点的异常进动
# =============================================================================

def effective_potential(r, L, M):
    """
    计算测地线运动的有效势能（广义相对论）
    Calculate effective potential for geodesic motion (General Relativity)

    公式 Formula: V_eff = -GM/r + L²/(2r²) - GML²/(c²r³)

    参数 Parameters:
        r: 径向距离 Radial distance (m)
        L: 单位质量角动量 Specific angular momentum (m²/s)
        M: 中心天体质量 Central mass (kg)

    返回 Returns:
        V_eff: 有效势能 Effective potential (J/kg = m²/s²)

    注意 Note:
        最后一项 -GML²/(c²r³) 是广义相对论修正项，
        在牛顿力学中不存在，是导致近日点进动的原因
    """
    r_s = 2 * G * M / c**2

    # TODO: 计算有效势能
    # 提示：注意第三项是GR特有的修正项
    V_eff = -G * M / r + L**2 / (2 * r**2) - G * M * L**2 / (c**2 * r**3)
    return V_eff


def effective_potential_newtonian(r, L, M):
    """
    计算牛顿力学的有效势能（用于比较）
    Calculate Newtonian effective potential (for comparison)

    公式 Formula: V_eff_newton = -GM/r + L²/(2r²)

    参数 Parameters:
        r: 径向距离 Radial distance (m)
        L: 单位质量角动量 Specific angular momentum (m²/s)
        M: 中心天体质量 Central mass (kg)

    返回 Returns:
        V_eff: 牛顿有效势能 Newtonian effective potential (m²/s²)

    物理意义 Physical Meaning:
        第一项是引力势能，第二项是离心势能（角动量守恒的结果）
    """
    return -G * M / r + L**2 / (2 * r**2)


# =============================================================================
# 练习 1.5: 圆轨道条件
# Exercise 1.5: Circular Orbit Condition
# =============================================================================
def circular_orbit_radius(L, M):
    """
    稳定圆轨道半径（从dV_eff/dr = 0求解）
    对于史瓦西时空: r_c 需要满足 r² - L²r/(Mc²) + 3L²/c² = 0 (简化形式)

    返回稳定圆轨道的半径
    """
    r_s = 2 * G * M / c**2
    # 简化: 对于大角动量, 稳定轨道约在
    # r ≈ L²/(GMc²) (主要项)

    # TODO: 计算圆轨道半径
    # 使用有效势能极值条件
    r_approx = L**2 / (G * M * c**2) * (1 + np.sqrt(1 - 12 * (G * M)**2 / (L**2 * c**2)))
    return r_approx


def orbital_period_proper(r, M):
    """
    固有轨道周期 (相对于轨道上的观察者)
    T_proper = 2π√(r³/GM) × √(1 - 3r_s/(2r))
    """
    r_s = 2 * G * M / c**2

    # TODO: 计算固有周期
    T_kepler = 2 * np.pi * np.sqrt(r**3 / (G * M))
    correction = np.sqrt(1 - 3 * r_s / (2 * r))
    T_proper = T_kepler * correction
    return T_proper


# =============================================================================
# 练习 1.6: 光子的测地线
# Exercise 1.6: Photon Geodesics
#
# 物理背景 Physical Background:
# 光子沿零测地线（ds² = 0）运动。在引力场中，光线会发生偏折，
# 这是广义相对论的关键预言之一。1919年爱丁顿的日食观测验证了
# 这一预言，使爱因斯坦一举成名。
#
# 历史意义 Historical Significance:
# - 牛顿理论预言的偏折角: δφ_Newton = 2GM/(bc²) ≈ 0.87"
# - 广义相对论预言: δφ_GR = 4GM/(bc²) ≈ 1.75"
# - 1919年日食观测证实了GR的预言，震惊世界
#
# 应用 Applications:
# - 引力透镜效应
# - 爱因斯坦环
# - 宇宙学中的暗物质探测
# =============================================================================

def photon_deflection_angle(b, M):
    """
    计算光线在引力场中的偏折角
    Calculate light deflection angle in gravitational field

    公式 Formula: δφ ≈ 4GM/(bc²)（弱场近似）

    参数 Parameters:
        b: 冲击参数（光线最近距离）Impact parameter (m)
        M: 引力源质量 Gravitating mass (kg)

    返回 Returns:
        delta_phi: 偏折角 Deflection angle (弧度 rad)

    历史 History:
        对于掠过太阳边缘的光线 (b ≈ R_☉ ≈ 7×10⁸ m):
        δφ ≈ 1.75 角秒，1919年日食验证
    """
    # TODO: 计算偏折角
    # 提示：注意这是GR值，是牛顿预言的2倍
    delta_phi = 4 * G * M / (b * c**2)
    return delta_phi


def einstein_ring_radius(D_LS, D_L, D_S, M):
    """
    计算爱因斯坦环的角半径
    Calculate Einstein ring angular radius

    公式 Formula: θ_E = √(4GM × D_LS / (c² × D_L × D_S))

    参数 Parameters:
        D_LS: 透镜到光源的距离 Lens-source distance (m)
        D_L: 观察者到透镜的距离 Observer-lens distance (m)
        D_S: 观察者到光源的距离 Observer-source distance (m)
        M: 透镜质量 Lens mass (kg)

    返回 Returns:
        theta_E: 爱因斯坦环角半径 Einstein ring angular radius (弧度 rad)

    物理意义 Physical Meaning:
        当光源、透镜、观察者完美对齐时，背景光源会被放大成一个
        完美的圆环（爱因斯坦环）
    """
    # TODO: 计算爱因斯坦环半径
    # 提示：这是引力透镜效应的特征尺度
    theta_E = np.sqrt(4 * G * M * D_LS / (c**2 * D_L * D_S))
    return theta_E


# =============================================================================
# 练习 1.7: 进动效应
# Exercise 1.7: Precession Effect
#
# 物理背景 Physical Background:
# 在牛顿引力中，行星轨道是闭合的椭圆。但在广义相对论中，
# 由于有效势能中的额外项，轨道不再闭合，近日点会逐渐进动。
# 水星近日点进动的精确解释是广义相对论的首个定量验证。
#
# 历史意义 Historical Significance:
# - 19世纪天文学家发现水星近日点进动比牛顿预言多出约43角秒/世纪
# - 1915年爱因斯坦用广义相对论精确解释了这一异常
# - 这个计算让爱因斯坦"心悸了好几天"
#
# 公式 Formula: Δφ = 6πGM/(c²a(1-e²))
# 其中 a 是半长轴，e 是离心率
# =============================================================================

def perihelion_precession(a, e, M):
    """
    计算近日点进动角（每轨道）
    Calculate perihelion precession per orbit

    公式 Formula: Δφ = 6πGM/(c²a(1-e²))

    参数 Parameters:
        a: 轨道半长轴 Semi-major axis (m)
        e: 轨道离心率 Orbital eccentricity (无量纲 dimensionless)
        M: 中心天体质量 Central mass (kg)

    返回 Returns:
        delta_phi: 每轨道进动角 Precession per orbit (弧度 rad)

    物理意义 Physical Meaning:
        这个进动是纯粹的广义相对论效应，在牛顿引力中不存在
        离心率越大或半长轴越小，进动越明显
    """
    # TODO: 计算进动角
    # 提示：注意分母中的 (1-e²) 项
    delta_phi = 6 * np.pi * G * M / (c**2 * a * (1 - e**2))
    return delta_phi


def mercury_precession_per_century():
    """
    计算水星近日点进动（每世纪角秒）
    Calculate Mercury's perihelion precession per century

    水星轨道参数 Mercury's Orbital Parameters:
        a = 5.79 × 10¹⁰ m (半长轴)
        e = 0.2056 (离心率)
        T = 87.97 天 (轨道周期)

    返回 Returns:
        arcsec: 每世纪进动角秒 Precession in arcseconds per century

    历史 History:
        观测值：约43角秒/世纪
        GR预言：42.98角秒/世纪
        这个精确吻合是广义相对论的重要验证
    """
    # 水星轨道参数 Mercury orbital parameters
    a_mercury = 5.79e10  # 半长轴 Semi-major axis (m)
    e_mercury = 0.2056   # 离心率 Eccentricity
    T_mercury = 87.97 * 24 * 3600  # 轨道周期 Orbital period (s)

    # 每轨道进动 Precession per orbit
    delta_phi_orbit = perihelion_precession(a_mercury, e_mercury, M_sun)

    # 每世纪轨道数 Orbits per century
    century = 100 * 365.25 * 24 * 3600  # 一个世纪的秒数
    orbits_per_century = century / T_mercury  # 约415轨道/世纪

    # 每世纪进动（转换为角秒）Precession per century (in arcseconds)
    delta_phi_century = delta_phi_orbit * orbits_per_century
    arcsec = delta_phi_century * 180 / np.pi * 3600  # 弧度转角秒

    return arcsec


# =============================================================================
# 可视化
# =============================================================================
def plot_geodesics():
    """绘制测地线相关图"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    M = 10 * M_sun  # 10太阳质量黑洞
    r_s = 2 * G * M / c**2

    # 1. 有效势能
    ax1 = axes[0, 0]
    r_range = np.linspace(3 * r_s, 20 * r_s, 200)

    for L_factor in [3.5, 4.0, 4.5, 5.0]:
        L = L_factor * r_s * c  # 角动量
        V_eff = [effective_potential(r, L, M) for r in r_range]
        V_newton = [effective_potential_newtonian(r, L, M) for r in r_range]
        ax1.plot(r_range / r_s, np.array(V_eff) / c**2,
                label=f'GR (L={L_factor}r_s c)', linewidth=2)

    ax1.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    ax1.axvline(x=3, color='r', linestyle='--', alpha=0.5, label='ISCO (3r_s)')
    ax1.set_xlabel('r / r_s')
    ax1.set_ylabel('V_eff / c²')
    ax1.set_title('有效势能 Effective Potential')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(-0.1, 0.1)

    # 2. 径向自由落体
    ax2 = axes[0, 1]
    r0 = 10 * r_s
    tau_max = 5e-4  # 秒
    tau, t, r = solve_radial_geodesic(r0, M, tau_max)

    valid = r > r_s * 1.01
    ax2.plot(tau[valid] * 1e6, r[valid] / r_s, 'b-', linewidth=2, label='r(τ)')
    ax2.axhline(y=1, color='r', linestyle='--', label='Event Horizon')
    ax2.set_xlabel('Proper time τ (μs)')
    ax2.set_ylabel('r / r_s')
    ax2.set_title('径向自由落体 Radial Free Fall')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 光线偏折
    ax3 = axes[1, 0]
    b_range = np.linspace(2 * r_s, 20 * r_s, 100)
    deflection = [photon_deflection_angle(b, M) * 180 / np.pi * 3600 for b in b_range]

    ax3.plot(b_range / r_s, deflection, 'g-', linewidth=2)
    ax3.set_xlabel('Impact parameter b / r_s')
    ax3.set_ylabel('Deflection angle (arcsec)')
    ax3.set_title('光线偏折 Light Deflection')
    ax3.grid(True, alpha=0.3)
    ax3.set_yscale('log')

    # 4. 近日点进动
    ax4 = axes[1, 1]
    e_range = np.linspace(0.01, 0.9, 100)
    a = 5.79e10  # 水星半长轴
    precession = [perihelion_precession(a, e, M_sun) * 180 / np.pi * 3600 * 415
                  for e in e_range]  # 415轨道/世纪

    ax4.plot(e_range, precession, 'r-', linewidth=2)
    ax4.axvline(x=0.2056, color='b', linestyle='--', label='Mercury e=0.206')
    ax4.axhline(y=43, color='g', linestyle='--', alpha=0.5, label='Observed ~43"')
    ax4.set_xlabel('Eccentricity e')
    ax4.set_ylabel('Precession (arcsec/century)')
    ax4.set_title('近日点进动 Perihelion Precession')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('geodesics.png', dpi=150)
    print("图像已保存为 geodesics.png")
    plt.show()


# =============================================================================
# 验证函数 Verification Functions
# =============================================================================
def verify():
    """
    验证所有练习的正确性
    Verify all exercises for correctness
    """
    all_passed = True

    M = M_sun
    r_s = 2 * G * M / c**2

    # 检查 1.1 - 平坦时空测地线 Flat spacetime geodesic
    tau, x = flat_spacetime_geodesic(0, 1, 10)
    if not np.isclose(x[-1], 10, rtol=0.01):
        print("错误 1.1: 平坦时空测地线计算不正确，应为直线运动 x = x₀ + v₀×τ")
        all_passed = False
    else:
        print("正确 1.1: 平坦时空测地线 (直线运动)")

    # 检查 1.2 - 克里斯托费尔符号 Christoffel symbols
    Gamma_r_tt = christoffel_schwarzschild_radial(2 * r_s, r_s)
    if Gamma_r_tt <= 0:
        print("错误 1.2: 克里斯托费尔符号 Γ^r_tt 应为正值")
        all_passed = False
    else:
        print(f"正确 1.2: 克里斯托费尔符号计算")

    # 检查 1.3 - 径向测地线 Radial geodesic
    r0 = 10 * r_s
    tau, t, r = solve_radial_geodesic(r0, M, 1e-2)
    if r[-1] >= r0:
        print("错误 1.3: 径向测地线应描述向内下落的运动")
        all_passed = False
    else:
        print(f"正确 1.3: 径向测地线 (r: {r0/r_s:.1f}r_s -> {r[-1]/r_s:.1f}r_s)")

    # 检查 1.4 - 有效势能 Effective potential
    L = 4 * r_s * c
    V_at_6rs = effective_potential(6 * r_s, L, M)
    if V_at_6rs == 0:
        print("错误 1.4: 有效势能不应恰好为零，请检查公式")
        all_passed = False
    else:
        print(f"正确 1.4: 有效势能计算")

    # 检查 1.6 - 光线偏折 Photon deflection
    # 掠过太阳边缘: b ≈ R_sun ≈ 7×10⁸ m
    R_sun = 6.96e8
    delta_phi = photon_deflection_angle(R_sun, M_sun)
    expected_arcsec = 1.75  # 约1.75角秒（1919年日食验证）
    actual_arcsec = delta_phi * 180 / np.pi * 3600
    if not np.isclose(actual_arcsec, expected_arcsec, rtol=0.1):
        print(f"错误 1.6: 光线偏折角计算不正确，期望约1.75角秒，得到 {actual_arcsec:.2f}角秒")
        all_passed = False
    else:
        print(f"正确 1.6: 光线偏折 (太阳边缘: {actual_arcsec:.2f}角秒)")

    # 检查 1.7 - 水星进动 Mercury precession
    precession = mercury_precession_per_century()
    if not np.isclose(precession, 43, rtol=0.1):
        print(f"错误 1.7: 水星近日点进动计算不正确，期望约43角秒/世纪，得到 {precession:.1f}角秒/世纪")
        all_passed = False
    else:
        print(f"正确 1.7: 水星近日点进动 ({precession:.1f}角秒/世纪)")

    if all_passed:
        print("\n所有测试通过！正在生成可视化...")
        try:
            plot_geodesics()
        except Exception as e:
            print(f"可视化生成失败: {e}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("测地线方程 Geodesic Equations")
    print("=" * 50)
    verify()
