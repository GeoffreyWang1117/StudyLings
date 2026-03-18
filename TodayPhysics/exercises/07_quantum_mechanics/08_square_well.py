"""
无限和有限方势阱 Infinite and Finite Square Wells
难度 Difficulty: ★★★

物理背景 Physical Background:
--------------------------
方势阱是量子力学中最基础的模型之一，用于描述粒子在有限空间内的束缚态。

1. 无限深方势阱 Infinite Square Well:
   - 势能: V=0 (0<x<L), V=∞ (其他)
   - 粒子被完全限制在阱内
   - 能级量子化: E_n = n²π²ℏ²/(2mL²), n=1,2,3,...
   - 波函数: ψ_n(x) = √(2/L)sin(nπx/L)
   - 基态能量非零（零点能）

2. 有限深方势阱 Finite Square Well:
   - 势能: V=0 (|x|<L/2), V=V₀ (|x|>L/2)
   - 波函数可穿透到势垒区域（指数衰减）
   - 束缚态数量有限，由无量纲参数 z₀=L√(2mV₀)/(2ℏ) 决定
   - 能级需求解超越方程

3. 量子隧穿效应 Quantum Tunneling:
   - 粒子有一定概率出现在经典禁区
   - 穿透深度: δ = ℏ/√(2m(V₀-E))

学习目标 Learning Objectives:
--------------------------
1. 理解能级量子化的物理根源（驻波条件）
2. 掌握有限势阱的超越方程求解方法
3. 分析波函数的穿透效应
4. 理解双势阱中的隧穿分裂
5. 了解周期势阱与能带理论的联系
6. 掌握量子点的能级结构

关键公式 Key Formulas:
---------------------
- 无限势阱能级: E_n = n²π²ℏ²/(2mL²)
- 有限势阱参数: z₀ = L√(2mV₀)/(2ℏ)
- 束缚态数量: N = floor(2z₀/π) + 1
- 穿透深度: δ = 1/κ = ℏ/√(2m(V₀-E))
- 隧穿分裂: ΔE ≈ ℏω exp(-2κd)
- 量子点能级: E = (π²ℏ²/2m)(n_x²/L_x² + n_y²/L_y² + n_z²/L_z²)

HINT: 无限势阱: E_n = n²π²ℏ²/(2mL²), ψ_n = √(2/L)sin(nπx/L)
HINT: 有限势阱: 超越方程确定能级
HINT: 穿透深度: κ = √(2m(V₀-E))/ℏ
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import hbar, m_e, eV

# I AM NOT DONE

# =============================================================================
# 练习 8.1: 无限深方势阱
# Exercise 8.1: Infinite Square Well
#
# 物理背景 Physical Background:
# 无限深方势阱是最简单的量子束缚态模型。粒子被完全限制在宽度为L的区域内，
# 波函数必须在边界处为零（边界条件）。这导致只有特定波长的驻波能够存在，
# 从而产生能级量子化。
#
# 能级公式: E_n = n²π²ℏ²/(2mL²), n=1,2,3,...
# 波函数: ψ_n(x) = √(2/L) sin(nπx/L)
#
# 特点:
# - 基态能量非零（零点能），体现不确定性原理
# - 能级间距随n增大而增大
# - 波函数有(n-1)个节点
# =============================================================================
def infinite_well_energy(n, L, m):
    """
    无限深方势阱能级 Infinite well energy levels

    E_n = n²π²ℏ²/(2mL²)

    参数 Parameters:
        n: 量子数 quantum number (n = 1, 2, 3, ...)
        L: 势阱宽度 well width (m)
        m: 粒子质量 particle mass (kg)

    返回 Returns:
        E_n: 第n能级的能量 (J)
    """
    return n**2 * np.pi**2 * hbar**2 / (2 * m * L**2)


def infinite_well_wavefunction(x, n, L):
    """
    无限深方势阱波函数 Infinite well wavefunction (0 < x < L)

    ψ_n(x) = √(2/L) sin(nπx/L)

    波函数性质:
    - 在边界处为零: ψ(0) = ψ(L) = 0
    - 已归一化: ∫|ψ|²dx = 1
    - 有(n-1)个节点

    参数 Parameters:
        x: 位置 position (m)
        n: 量子数 quantum number
        L: 势阱宽度 well width (m)

    返回 Returns:
        ψ_n(x): 波函数值
    """
    return np.sqrt(2/L) * np.sin(n * np.pi * x / L)


def infinite_well_momentum(n, L):
    """
    动量的可能测量值 Possible momentum values

    p = ±nπℏ/L

    注意: 势阱中的粒子动量不是确定的，测量会得到 +p 或 -p

    参数 Parameters:
        n: 量子数 quantum number
        L: 势阱宽度 well width (m)

    返回 Returns:
        |p|: 动量的绝对值 (kg·m/s)
    """
    return n * np.pi * hbar / L


def energy_level_spacing(n, L, m):
    """
    相邻能级间距 Energy level spacing

    ΔE = E_{n+1} - E_n = (2n+1)π²ℏ²/(2mL²)

    特点: 间距随量子数n线性增加

    参数 Parameters:
        n: 量子数 quantum number
        L: 势阱宽度 well width (m)
        m: 粒子质量 particle mass (kg)

    返回 Returns:
        ΔE: 能级间距 (J)
    """
    return (2*n + 1) * np.pi**2 * hbar**2 / (2 * m * L**2)


def transition_wavelength(n_upper, n_lower, L, m):
    """
    跃迁波长 Transition wavelength

    光子能量等于能级差: E_photon = ΔE = E_upper - E_lower
    波长: λ = hc/ΔE

    参数 Parameters:
        n_upper: 上能级量子数
        n_lower: 下能级量子数
        L: 势阱宽度 (m)
        m: 粒子质量 (kg)

    返回 Returns:
        λ: 跃迁波长 (m)
    """
    c = 3e8  # 光速 (m/s)
    h = 2 * np.pi * hbar  # 普朗克常数 (J·s)
    dE = infinite_well_energy(n_upper, L, m) - infinite_well_energy(n_lower, L, m)
    return h * c / dE


# =============================================================================
# 练习 8.2: 有限深方势阱 - 对称情况
# Exercise 8.2: Finite Square Well - Symmetric Case
#
# 物理背景 Physical Background:
# 有限深方势阱更接近实际物理系统。势能在阱内为零，阱外为有限值V₀。
# 与无限势阱不同，波函数可以穿透到阱外（指数衰减），体现量子隧穿效应。
#
# 求解方法:
# 1. 定义无量纲参数 z = kL/2, z₀ = L√(2mV₀)/(2ℏ)
# 2. 偶宇称态满足: z tan(z) = √(z₀² - z²)
# 3. 奇宇称态满足: -z cot(z) = √(z₀² - z²)
# 4. 束缚态数量: N = floor(2z₀/π) + 1
# =============================================================================
def finite_well_z0(V0, L, m):
    """
    无量纲参数 z₀ Dimensionless parameter z₀

    z₀ = L√(2mV₀)/(2ℏ)

    物理意义: z₀ 决定了势阱能容纳多少个束缚态
    - z₀ < π/2: 只有1个束缚态（基态）
    - π/2 < z₀ < π: 有2个束缚态
    - 一般: N = floor(2z₀/π) + 1

    参数 Parameters:
        V0: 势阱深度 well depth (J)
        L: 势阱宽度 well width (m)
        m: 粒子质量 particle mass (kg)

    返回 Returns:
        z₀: 无量纲参数
    """
    return L * np.sqrt(2 * m * V0) / (2 * hbar)


def number_of_bound_states(V0, L, m):
    """
    束缚态数量 Number of bound states

    N = floor(z₀/(π/2)) + 1 = floor(2z₀/π) + 1

    注意: 无论势阱多浅，至少有一个束缚态（一维情况）

    参数 Parameters:
        V0: 势阱深度 (J)
        L: 势阱宽度 (m)
        m: 粒子质量 (kg)

    返回 Returns:
        N: 束缚态数量
    """
    z0 = finite_well_z0(V0, L, m)
    return int(z0 / (np.pi/2)) + 1


def even_state_equation(z, z0):
    """
    偶宇称态超越方程 Even parity state transcendental equation

    z tan(z) = √(z₀² - z²)

    偶宇称态的波函数形如 ψ(x) ∝ cos(kx)，关于原点对称。
    求解此方程可得到偶宇称态的能级。

    参数 Parameters:
        z: 无量纲变量 z = kL/2
        z0: 势阱参数

    返回 Returns:
        f(z) = z tan(z) - √(z₀² - z²), 方程的根使 f(z) = 0
    """
    if z >= z0:
        return np.inf
    return z * np.tan(z) - np.sqrt(z0**2 - z**2)


def odd_state_equation(z, z0):
    """
    奇宇称态超越方程 Odd parity state transcendental equation

    -z cot(z) = √(z₀² - z²)

    奇宇称态的波函数形如 ψ(x) ∝ sin(kx)，关于原点反对称。
    求解此方程可得到奇宇称态的能级。

    参数 Parameters:
        z: 无量纲变量 z = kL/2
        z0: 势阱参数

    返回 Returns:
        f(z) = -z cot(z) - √(z₀² - z²), 方程的根使 f(z) = 0
    """
    if z >= z0:
        return np.inf
    tan_z = np.tan(z)
    if np.abs(tan_z) < 1e-10:
        return np.inf
    return -z / tan_z - np.sqrt(z0**2 - z**2)


def solve_finite_well_energies(V0, L, m, n_states=None):
    """
    求解有限势阱的能级 Solve finite well energy levels

    使用 Brent 方法数值求解超越方程

    算法说明:
    1. 偶态在区间 (nπ, (n+0.5)π) 内求解
    2. 奇态在区间 ((n+0.5)π, (n+1)π) 内求解
    3. 使用二分法找根

    参数 Parameters:
        V0: 势阱深度 (J)
        L: 势阱宽度 (m)
        m: 粒子质量 (kg)
        n_states: 要求解的态数量（默认为所有束缚态）

    返回 Returns:
        energies: 能级列表，从低到高排序 (J)
    """
    z0 = finite_well_z0(V0, L, m)

    if n_states is None:
        n_states = number_of_bound_states(V0, L, m)

    energies = []

    # 偶态: 在 (0, π/2), (π, 3π/2), ... 区间
    # 奇态: 在 (π/2, π), (3π/2, 2π), ... 区间

    for n in range(n_states):
        if n % 2 == 0:  # 偶态
            interval_num = n // 2
            z_min = interval_num * np.pi + 1e-10
            z_max = min((interval_num + 0.5) * np.pi - 1e-10, z0 - 1e-10)

            if z_max > z_min:
                try:
                    z = brentq(even_state_equation, z_min, z_max, args=(z0,))
                    E = z**2 * 2 * hbar**2 / (m * L**2)
                    energies.append(E)
                except:
                    pass
        else:  # 奇态
            interval_num = (n - 1) // 2
            z_min = (interval_num + 0.5) * np.pi + 1e-10
            z_max = min((interval_num + 1) * np.pi - 1e-10, z0 - 1e-10)

            if z_max > z_min:
                try:
                    z = brentq(odd_state_equation, z_min, z_max, args=(z0,))
                    E = z**2 * 2 * hbar**2 / (m * L**2)
                    energies.append(E)
                except:
                    pass

    return sorted(energies)


# =============================================================================
# 练习 8.3: 有限势阱波函数
# Exercise 8.3: Finite Well Wavefunctions
#
# 物理背景 Physical Background:
# 有限势阱的波函数在阱内是振荡函数（正弦或余弦），
# 在阱外是指数衰减函数。波函数及其导数在边界处必须连续。
#
# 穿透效应:
# - 粒子有非零概率出现在经典禁区（势垒区域）
# - 穿透深度 δ = 1/κ = ℏ/√(2m(V₀-E)) 描述波函数衰减的特征长度
# - 当 E → V₀ 时，穿透深度趋于无穷大
# =============================================================================
def penetration_depth(V0, E, m):
    """
    穿透深度（衰减长度）Penetration depth

    δ = κ⁻¹ = ℏ/√(2m(V₀-E))

    物理意义: 波函数在势垒中衰减到 1/e 的特征长度

    参数 Parameters:
        V0: 势垒高度 barrier height (J)
        E: 粒子能量 particle energy (J)
        m: 粒子质量 particle mass (kg)

    返回 Returns:
        δ: 穿透深度 (m)
    """
    if E >= V0:
        return np.inf
    kappa = np.sqrt(2 * m * (V0 - E)) / hbar
    return 1 / kappa


def finite_well_wavefunction(x, E, V0, L, m, parity='even'):
    """
    有限势阱波函数 Finite well wavefunction

    阱内 (|x| < L/2):
        偶宇称: ψ ∝ cos(kx), k = √(2mE)/ℏ
        奇宇称: ψ ∝ sin(kx)

    阱外 (|x| > L/2):
        ψ ∝ exp(-κ|x|), κ = √(2m(V₀-E))/ℏ

    参数 Parameters:
        x: 位置数组 (m)
        E: 能量 (J)
        V0: 势阱深度 (J)
        L: 势阱宽度 (m)
        m: 粒子质量 (kg)
        parity: 'even' 或 'odd'

    返回 Returns:
        ψ(x): 归一化波函数
    """
    k = np.sqrt(2 * m * E) / hbar
    kappa = np.sqrt(2 * m * (V0 - E)) / hbar

    psi = np.zeros_like(x)

    # 内部 |x| < L/2
    inside = np.abs(x) <= L/2
    if parity == 'even':
        psi[inside] = np.cos(k * x[inside])
    else:
        psi[inside] = np.sin(k * x[inside])

    # 外部 |x| > L/2
    outside_right = x > L/2
    outside_left = x < -L/2

    # 匹配边界条件
    if parity == 'even':
        A = np.cos(k * L/2) * np.exp(kappa * L/2)
    else:
        A = np.sin(k * L/2) * np.exp(kappa * L/2)

    psi[outside_right] = A * np.exp(-kappa * x[outside_right])
    psi[outside_left] = (1 if parity == 'even' else -1) * A * np.exp(kappa * x[outside_left])

    # 归一化
    dx = x[1] - x[0]
    norm = np.sqrt(np.trapezoid(psi**2, x))
    if norm > 0:
        psi = psi / norm

    return psi


def probability_outside_well(psi, x, L):
    """
    粒子在势阱外的概率 Probability outside the well

    P_outside = ∫_{|x|>L/2} |ψ(x)|² dx

    这体现了量子隧穿效应：粒子有一定概率出现在经典禁区。

    参数 Parameters:
        psi: 波函数数组
        x: 位置数组 (m)
        L: 势阱宽度 (m)

    返回 Returns:
        P: 阱外概率 (0到1之间)
    """
    dx = x[1] - x[0]
    outside_mask = np.abs(x) > L/2
    prob_outside = np.trapezoid(psi[outside_mask]**2, x[outside_mask])
    return prob_outside


# =============================================================================
# 练习 8.4: 对称双势阱
# Exercise 8.4: Symmetric Double Well
#
# 物理背景 Physical Background:
# 双势阱模型描述了许多重要的物理现象:
# - 氨分子 NH₃ 的伞式振动
# - 化学反应中的势垒穿越
# - 固体中的双稳态缺陷
#
# 关键现象:
# 1. 隧穿分裂: 原本简并的两个阱内态分裂为成键态和反键态
# 2. 能级分裂: ΔE ≈ ℏω exp(-2κd), d为势垒宽度
# 3. 隧穿振荡: 粒子在两阱之间周期性振荡，周期 T = h/ΔE
# =============================================================================
def double_well_potential(x, V0, a, b):
    """
    对称双势阱势能 Symmetric double well potential

    势能结构:
    - V = 0: 两个势阱区域
    - V = V₀: 中间势垒区域
    - V = V₀: 外部区域

    参数 Parameters:
        x: 位置 (m)
        V0: 势垒高度 (J)
        a: 阱半宽 (m)
        b: 总半宽 (m)

    返回 Returns:
        V(x): 势能 (J)
    """
    x = np.asarray(x)
    V = np.zeros_like(x)

    # 势垒区域
    barrier_mask = (np.abs(x) > a) & (np.abs(x) < b)
    V[barrier_mask] = V0

    # 外部区域
    outside_mask = np.abs(x) >= b
    V[outside_mask] = V0

    return V


def tunnel_splitting(E0, V0, d, m):
    """
    隧穿导致的能级分裂（WKB近似）Tunnel splitting (WKB approximation)

    ΔE ≈ ℏω exp(-2∫κdx) ≈ (ℏω/π) exp(-2κd)

    物理图像:
    - 当势垒足够薄时，粒子可以隧穿到另一个阱
    - 原本简并的两个态发生分裂
    - 分裂大小随势垒宽度指数衰减

    参数 Parameters:
        E0: 单阱基态能量 (J)
        V0: 势垒高度 (J)
        d: 势垒宽度 (m)
        m: 粒子质量 (kg)

    返回 Returns:
        ΔE: 能级分裂 (J)
    """
    if E0 >= V0:
        return 0

    kappa = np.sqrt(2 * m * (V0 - E0)) / hbar
    # 简化：假设ω ≈ √(E0/m) / L
    omega_approx = np.sqrt(E0 / m) * 1e10

    return (hbar * omega_approx / np.pi) * np.exp(-2 * kappa * d)


def bonding_antibonding_states():
    """
    成键态和反键态 Bonding and antibonding states

    成键态 Bonding state:
        ψ_+ = (ψ_L + ψ_R)/√2 (对称)
        E_+ = E_0 - ΔE/2 (能量较低)

    反键态 Antibonding state:
        ψ_- = (ψ_L - ψ_R)/√2 (反对称)
        E_- = E_0 + ΔE/2 (能量较高)

    返回 Returns:
        描述成键态和反键态的字符串
    """
    return "bonding (symmetric, lower energy)", "antibonding (antisymmetric, higher energy)"


# =============================================================================
# 练习 8.5: 周期势阱
# Exercise 8.5: Periodic Potential Wells
#
# 物理背景 Physical Background:
# Kronig-Penney模型是理解固体能带理论的基础模型。
# 周期性排列的势阱模拟了晶格中原子势的周期性。
#
# 关键概念:
# 1. 布洛赫定理: ψ(x+a) = exp(iKa)ψ(x), K为布洛赫波矢
# 2. 能带结构: 允许的能量形成连续的能带，禁止的能量形成带隙
# 3. 布里渊区: K ∈ [-π/a, π/a]
#
# 这是理解半导体、绝缘体、金属导电性差异的基础。
# =============================================================================
def kronig_penney_condition(k, K, a, b, V0, m, E):
    """
    Kronig-Penney模型色散关系 Kronig-Penney dispersion relation

    cos(K(a+b)) = cos(ka)cosh(κb) + (κ²-k²)/(2kκ)sin(ka)sinh(κb)

    其中:
        k = √(2mE)/ℏ: 阱内波矢
        κ = √(2m(V₀-E))/ℏ: 势垒内衰减常数
        K: 布洛赫波矢
        a: 阱宽
        b: 势垒宽

    只有当方程有解时，能量E才是允许的。

    参数 Parameters:
        k: 阱内波矢 (1/m)
        K: 布洛赫波矢 (1/m)
        a: 阱宽 (m)
        b: 势垒宽 (m)
        V0: 势垒高度 (J)
        m: 粒子质量 (kg)
        E: 能量 (J)

    返回 Returns:
        条件值，为零时E为允许能量
    """
    if E >= V0:
        k_well = np.sqrt(2 * m * E) / hbar
        k_barrier = np.sqrt(2 * m * (E - V0)) / hbar
        return (np.cos(K * (a + b)) -
                np.cos(k_well * a) * np.cos(k_barrier * b) +
                (k_well**2 + k_barrier**2) / (2 * k_well * k_barrier) *
                np.sin(k_well * a) * np.sin(k_barrier * b))
    else:
        k_well = np.sqrt(2 * m * E) / hbar
        kappa = np.sqrt(2 * m * (V0 - E)) / hbar

        return (np.cos(K * (a + b)) -
                np.cos(k_well * a) * np.cosh(kappa * b) -
                (kappa**2 - k_well**2) / (2 * k_well * kappa) *
                np.sin(k_well * a) * np.sinh(kappa * b))


def energy_bands(V0, a, b, m, n_bands=3, n_points=100):
    """
    计算能带结构 Calculate energy band structure

    通过在第一布里渊区内扫描K值，找到满足色散关系的能量。

    参数 Parameters:
        V0: 势垒高度 (J)
        a: 阱宽 (m)
        b: 势垒宽 (m)
        m: 粒子质量 (kg)
        n_bands: 计算的能带数
        n_points: K空间的采样点数

    返回 Returns:
        K_range: 布洛赫波矢数组
        bands: 各能带的能量
    """
    K_range = np.linspace(-np.pi/(a+b), np.pi/(a+b), n_points)

    bands = []
    for band_idx in range(n_bands):
        E_band = []
        # 简化：扫描能量找满足条件的点
        E_scan = np.linspace(0.01 * V0, 2 * V0, 1000)

        for K in K_range:
            for E in E_scan:
                k_well = np.sqrt(2 * m * E) / hbar if E > 0 else 0
                cond = kronig_penney_condition(k_well, K, a, b, V0, m, E)
                if np.abs(cond) < 0.1:
                    E_band.append(E)
                    break

        bands.append(E_band)

    return K_range, bands


def band_gap(E_top_lower, E_bottom_upper):
    """
    带隙 Band gap

    E_gap = E_bottom(upper band) - E_top(lower band)

    带隙决定材料的电学性质:
    - E_gap = 0: 金属（导体）
    - E_gap ~ 1-3 eV: 半导体
    - E_gap > 3 eV: 绝缘体

    参数 Parameters:
        E_top_lower: 下能带顶部能量 (J)
        E_bottom_upper: 上能带底部能量 (J)

    返回 Returns:
        E_gap: 带隙宽度 (J)
    """
    return E_bottom_upper - E_top_lower


# =============================================================================
# 练习 8.6: 量子点
# Exercise 8.6: Quantum Dots
#
# 物理背景 Physical Background:
# 量子点是三维纳米结构，粒子在所有三个方向都被限制。
# 由于量子限制效应，量子点具有离散的能级，类似于"人造原子"。
#
# 应用:
# - 量子点激光器
# - 量子点显示器 (QLED)
# - 量子计算中的量子比特
# - 生物标记和成像
#
# 尺寸效应:
# - 能级间距 ∝ 1/L²
# - 通过改变量子点尺寸可调节发光波长
# =============================================================================
def quantum_dot_energy_3d(nx, ny, nz, Lx, Ly, Lz, m):
    """
    三维量子点（无限势阱）能级 3D quantum dot energy levels

    E = (π²ℏ²/2m)(n_x²/L_x² + n_y²/L_y² + n_z²/L_z²)

    量子数: n_x, n_y, n_z = 1, 2, 3, ...

    对于立方量子点 (Lx=Ly=Lz=L):
        基态 (1,1,1): E = 3π²ℏ²/(2mL²)

    参数 Parameters:
        nx, ny, nz: 三个方向的量子数
        Lx, Ly, Lz: 三个方向的尺寸 (m)
        m: 粒子质量 (kg)

    返回 Returns:
        E: 能量 (J)
    """
    return (np.pi**2 * hbar**2 / (2 * m)) * \
           (nx**2/Lx**2 + ny**2/Ly**2 + nz**2/Lz**2)


def degeneracy_cubic_dot(n_total, L, m):
    """
    立方量子点的能级简并度 Degeneracy in cubic quantum dot

    对于立方量子点，能量只依赖于 n_x² + n_y² + n_z²。
    不同的 (n_x, n_y, n_z) 组合可能给出相同的能量，造成简并。

    例如: (2,1,1), (1,2,1), (1,1,2) 三个态是简并的。

    参数 Parameters:
        n_total: 参考量子数
        L: 量子点边长 (m)
        m: 粒子质量 (kg)

    返回 Returns:
        简并度（具有相同能量的态数）
    """
    E_target = quantum_dot_energy_3d(n_total, 1, 1, L, L, L, m)

    count = 0
    for nx in range(1, n_total + 1):
        for ny in range(1, n_total + 1):
            for nz in range(1, n_total + 1):
                E = quantum_dot_energy_3d(nx, ny, nz, L, L, L, m)
                if np.isclose(E, E_target, rtol=0.01):
                    count += 1
    return count


def quantum_dot_emission_wavelength(L, m):
    """
    量子点发射波长（基态到第一激发态）Quantum dot emission wavelength

    λ = hc/ΔE, 其中 ΔE = E₂ - E₁

    量子点尺寸越小，能级间距越大，发射波长越短（蓝移）。

    参数 Parameters:
        L: 量子点边长 (m)
        m: 粒子（电子）质量 (kg)

    返回 Returns:
        λ: 发射波长 (m)
    """
    c = 3e8  # 光速 (m/s)
    E1 = quantum_dot_energy_3d(1, 1, 1, L, L, L, m)
    E2 = quantum_dot_energy_3d(2, 1, 1, L, L, L, m)
    dE = E2 - E1
    return 2 * np.pi * hbar * c / dE


def confinement_energy(L, m):
    """
    量子限制能量（相对于体材料）Quantum confinement energy

    E_conf = π²ℏ²/(2mL²)

    这是由于量子限制导致的能量增加（相对于体材料的能带边缘）。
    量子点越小，限制能量越大。

    参数 Parameters:
        L: 量子点尺寸 (m)
        m: 有效质量 (kg)

    返回 Returns:
        E_conf: 限制能量 (J)
    """
    return np.pi**2 * hbar**2 / (2 * m * L**2)


# =============================================================================
# 可视化
# =============================================================================
def plot_square_wells():
    """绘制方势阱相关图"""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    m = m_e
    L = 1e-9  # 1 nm

    # 1. 无限势阱
    ax1 = axes[0, 0]
    x = np.linspace(0, L, 200)

    for n in range(1, 5):
        psi = infinite_well_wavefunction(x, n, L)
        E = infinite_well_energy(n, L, m)
        ax1.plot(x*1e9, psi*1e-4.5 + n**2, label=f'n={n}')

    ax1.set_xlabel('x (nm)')
    ax1.set_ylabel('能级 + ψ')
    ax1.set_title('无限深方势阱')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 有限势阱能级
    ax2 = axes[0, 1]
    V0 = 10 * eV

    energies = solve_finite_well_energies(V0, L, m)

    x_plot = [0, 1]
    for i, E in enumerate(energies):
        ax2.hlines(E/eV, 0, 1, colors='b', linewidth=2)
        ax2.text(1.05, E/eV, f'n={i+1}: {E/eV:.2f} eV', va='center')

    ax2.hlines(V0/eV, 0, 1, colors='r', linestyles='--', label='V₀')
    ax2.set_xlim(-0.5, 2)
    ax2.set_ylabel('能量 (eV)')
    ax2.set_title(f'有限势阱能级 (V₀={V0/eV}eV)')
    ax2.set_xticks([])
    ax2.legend()

    # 3. 有限势阱波函数
    ax3 = axes[0, 2]
    x_fw = np.linspace(-2*L, 2*L, 500)
    V0_fw = 5 * eV

    E_levels = solve_finite_well_energies(V0_fw, L, m)

    for i, E in enumerate(E_levels[:3]):
        parity = 'even' if i % 2 == 0 else 'odd'
        psi = finite_well_wavefunction(x_fw, E, V0_fw, L, m, parity)
        ax3.plot(x_fw*1e9, psi*1e-4.5 + i*2, label=f'n={i+1}')

    # 势阱边界
    ax3.axvline(x=-L/2*1e9, color='k', linestyle='--', alpha=0.5)
    ax3.axvline(x=L/2*1e9, color='k', linestyle='--', alpha=0.5)

    ax3.set_xlabel('x (nm)')
    ax3.set_ylabel('ψ + offset')
    ax3.set_title('有限势阱波函数')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 穿透深度
    ax4 = axes[1, 0]
    E_range = np.linspace(0.1, 0.9, 100) * V0

    depths = [penetration_depth(V0, E, m) for E in E_range]

    ax4.semilogy(E_range/V0, np.array(depths)*1e9, 'b-', linewidth=2)
    ax4.set_xlabel('E/V₀')
    ax4.set_ylabel('穿透深度 (nm)')
    ax4.set_title('穿透深度')
    ax4.grid(True, alpha=0.3)

    # 5. 束缚态数量
    ax5 = axes[1, 1]
    V0_range = np.linspace(0.1, 20, 100) * eV

    n_states = [number_of_bound_states(V, L, m) for V in V0_range]

    ax5.plot(V0_range/eV, n_states, 'b-', linewidth=2)
    ax5.set_xlabel('V₀ (eV)')
    ax5.set_ylabel('束缚态数量')
    ax5.set_title('束缚态数量 vs 势阱深度')
    ax5.grid(True, alpha=0.3)

    # 6. 量子点能级
    ax6 = axes[1, 2]
    L_dot = np.linspace(1, 10, 100) * 1e-9

    E_111 = [quantum_dot_energy_3d(1, 1, 1, l, l, l, m) for l in L_dot]
    E_211 = [quantum_dot_energy_3d(2, 1, 1, l, l, l, m) for l in L_dot]
    E_221 = [quantum_dot_energy_3d(2, 2, 1, l, l, l, m) for l in L_dot]

    ax6.semilogy(L_dot*1e9, np.array(E_111)/eV, 'b-', label='(1,1,1)', linewidth=2)
    ax6.semilogy(L_dot*1e9, np.array(E_211)/eV, 'r-', label='(2,1,1)', linewidth=2)
    ax6.semilogy(L_dot*1e9, np.array(E_221)/eV, 'g-', label='(2,2,1)', linewidth=2)
    ax6.set_xlabel('L (nm)')
    ax6.set_ylabel('能量 (eV)')
    ax6.set_title('量子点能级')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('square_well.png', dpi=150)
    print("图像已保存为 square_well.png")
    plt.show()


# =============================================================================
# 验证函数
# =============================================================================
def verify():
    """Verify all exercises"""
    all_passed = True

    m = m_e
    L = 1e-9

    # Check 8.1 - Infinite well
    E1 = infinite_well_energy(1, L, m)
    expected_E1 = np.pi**2 * hbar**2 / (2 * m * L**2)

    if not np.isclose(E1, expected_E1, rtol=0.01):
        print("X 8.1 无限势阱基态能量错误")
        all_passed = False
    else:
        print(f"V 8.1 无限势阱正确 (E₁ = {E1/eV:.3f} eV)")

    # Check 8.2 - Finite well z0
    V0 = 10 * eV
    z0 = finite_well_z0(V0, L, m)

    if z0 <= 0:
        print("X 8.2 z₀应为正")
        all_passed = False
    else:
        print(f"V 8.2 有限势阱参数正确 (z₀ = {z0:.2f})")

    # Check 8.3 - Bound state count
    n_bound = number_of_bound_states(V0, L, m)

    if n_bound < 1:
        print("X 8.3 至少应有一个束缚态")
        all_passed = False
    else:
        print(f"V 8.3 束缚态数量正确 (N = {n_bound})")

    # Check 8.4 - Penetration depth
    E_test = 0.5 * V0
    delta = penetration_depth(V0, E_test, m)

    if delta <= 0:
        print("X 8.4 穿透深度应为正")
        all_passed = False
    else:
        print(f"V 8.4 穿透深度正确 (δ = {delta*1e9:.3f} nm)")

    # Check 8.5 - Finite well energies
    energies = solve_finite_well_energies(V0, L, m)

    if len(energies) == 0:
        print("X 8.5 应能找到能级")
        all_passed = False
    else:
        print(f"V 8.5 有限势阱能级正确 (找到 {len(energies)} 个能级)")

    # Check 8.6 - 3D quantum dot
    E_111 = quantum_dot_energy_3d(1, 1, 1, L, L, L, m)
    expected = 3 * np.pi**2 * hbar**2 / (2 * m * L**2)

    if not np.isclose(E_111, expected, rtol=0.01):
        print("X 8.6 量子点基态能量错误")
        all_passed = False
    else:
        print(f"V 8.6 量子点正确 (E_111 = {E_111/eV:.3f} eV)")

    if all_passed:
        print("\n所有测试通过！正在生成可视化...")
        try:
            plot_square_wells()
        except Exception as ex:
            print(f"可视化生成失败: {ex}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("无限和有限方势阱 Square Wells")
    print("=" * 50)
    verify()
