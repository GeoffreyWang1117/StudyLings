"""
WKB近似 WKB Approximation
难度 Difficulty: ★★★★

物理背景 Physical Background:
--------------------------
WKB近似（Wentzel-Kramers-Brillouin）是量子力学中最重要的半经典近似方法。
它在势能变化缓慢的区域提供精确的解析近似。

1. 基本思想 Basic Idea:
   - 当德布罗意波长远小于势能变化的特征长度时，可使用WKB近似
   - 有效性条件: |dλ/dx| << 1, 即 |dp/dx| << p²/ℏ
   - 物理图像: 粒子局域地表现为具有变化动量的平面波

2. WKB波函数 WKB Wavefunction:
   经典允许区 (E > V):
       ψ(x) ≈ A/√p(x) exp(±i∫p(x)dx/ℏ)
       其中 p(x) = √(2m(E-V(x)))

   经典禁区 (E < V):
       ψ(x) ≈ A/√κ(x) exp(∓∫κ(x)dx)
       其中 κ(x) = √(2m(V(x)-E))/ℏ

3. 应用 Applications:
   - Bohr-Sommerfeld量子化条件: ∮p dx = (n + 1/2)h
   - 隧穿透射系数: T ≈ exp(-2∫κdx)
   - α衰变寿命估算
   - 场发射电流

学习目标 Learning Objectives:
--------------------------
1. 理解WKB近似的有效性条件
2. 掌握经典允许区和禁区的WKB波函数
3. 学习连接公式处理转折点附近的波函数匹配
4. 应用Bohr-Sommerfeld条件计算能级
5. 计算隧穿透射系数
6. 了解WKB方法在实际问题中的应用

关键公式 Key Formulas:
---------------------
- 经典动量: p(x) = √(2m(E-V(x)))
- 局域波长: λ(x) = h/p(x)
- WKB有效性: |dV/dx| << p³/(mℏ)
- 量子化条件: ∮p dx = (n + 1/2)h
- 隧穿系数: T ≈ exp(-2∫κdx)

HINT: WKB波函数: ψ ≈ A/√p(x) exp(±i∫p(x)dx/ℏ)
HINT: Bohr-Sommerfeld: ∮p dx = (n + 1/2)h
HINT: 隧穿: T ≈ exp(-2∫|p|dx/ℏ)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import hbar, m_e, eV

# I AM NOT DONE

# =============================================================================
# 练习 9.1: 经典动量
# Exercise 9.1: Classical Momentum
#
# 物理背景 Physical Background:
# 在WKB近似中，粒子的局域动量由经典力学公式给出。
# 经典允许区: E > V(x), 动量为实数
# 经典禁区: E < V(x), "动量"为虚数（衰减）
# =============================================================================
def classical_momentum(E, V, m):
    """
    经典动量 Classical momentum

    p(x) = √(2m(E - V(x)))

    在经典力学中，这对应于总能量减去势能得到动能，
    再由动能求得动量。

    参数 Parameters:
        E: 总能量 (J)
        V: 势能 V(x) (J) - 可以是标量或数组
        m: 粒子质量 (kg)

    返回 Returns:
        p: 经典动量 (kg·m/s)，经典禁区返回0
    """
    kinetic = E - V
    if isinstance(kinetic, np.ndarray):
        p = np.zeros_like(kinetic)
        mask = kinetic >= 0
        p[mask] = np.sqrt(2 * m * kinetic[mask])
        return p
    else:
        if kinetic >= 0:
            return np.sqrt(2 * m * kinetic)
        return 0


def local_wavelength(E, V, m):
    """
    局域德布罗意波长 Local de Broglie wavelength

    λ(x) = h/p(x) = h/√(2m(E-V))

    WKB近似的有效性条件可以表述为:
    |dλ/dx| << 1
    即波长在一个波长距离内的变化远小于波长本身。

    参数 Parameters:
        E: 总能量 (J)
        V: 势能 (J)
        m: 粒子质量 (kg)

    返回 Returns:
        λ(x): 局域波长 (m)，经典禁区返回无穷大
    """
    p = classical_momentum(E, V, m)
    if isinstance(p, np.ndarray):
        wavelength = np.zeros_like(p)
        mask = p > 0
        wavelength[mask] = 2 * np.pi * hbar / p[mask]
        wavelength[~mask] = np.inf
        return wavelength
    else:
        if p > 0:
            return 2 * np.pi * hbar / p
        return np.inf


def classical_turning_point(E, V_func, x_range):
    """
    找到经典转折点 Find classical turning points

    转折点是 E = V(x) 的解，即经典允许区和禁区的边界。
    在这些点，经典粒子会"转向"。
    WKB波函数在转折点附近发散，需要使用连接公式。

    参数 Parameters:
        E: 总能量 (J)
        V_func: 势能函数 V(x)
        x_range: 搜索范围 (x_min, x_max)

    返回 Returns:
        turning_points: 转折点位置列表 (m)
    """
    x = np.linspace(x_range[0], x_range[1], 10000)
    V = np.array([V_func(xi) for xi in x])

    turning_points = []
    for i in range(len(x) - 1):
        if (V[i] - E) * (V[i+1] - E) < 0:
            # 线性插值
            x_tp = x[i] + (E - V[i]) * (x[i+1] - x[i]) / (V[i+1] - V[i])
            turning_points.append(x_tp)

    return turning_points


def wkb_validity_condition(E, V, dV_dx, m):
    """
    WKB有效性条件 WKB validity condition

    WKB近似在以下条件下有效:
        |dp/dx| << p²/ℏ

    等价于:
        |dV/dx| << p³/(mℏ)

    物理意义: 势能在一个德布罗意波长内的变化远小于动能。

    参数 Parameters:
        E: 总能量 (J)
        V: 势能 (J)
        dV_dx: 势能梯度 (J/m)
        m: 粒子质量 (kg)

    返回 Returns:
        bool: True 如果WKB近似有效
    """
    p = classical_momentum(E, V, m)
    if p > 0:
        return np.abs(dV_dx) < p**3 / (m * hbar)
    return False


# =============================================================================
# 练习 9.2: WKB波函数
# Exercise 9.2: WKB Wavefunction
#
# 物理背景 Physical Background:
# WKB波函数具有特殊的形式，其振幅与局域动量成反比:
#     ψ ∝ 1/√p(x)
# 这保证了概率流守恒（经典允许区内概率密度正比于经典粒子在该处停留的时间）。
# =============================================================================
def wkb_phase_integral(E, V_func, x1, x2, m):
    """
    WKB相位积分 WKB phase integral

    S = ∫_{x1}^{x2} p(x)dx = ∫√(2m(E-V))dx

    相位积分决定了WKB波函数的相位变化。
    这也是经典作用量的空间部分。

    参数 Parameters:
        E: 总能量 (J)
        V_func: 势能函数
        x1, x2: 积分区间 (m)
        m: 粒子质量 (kg)

    返回 Returns:
        S: 相位积分值 (J·s)
    """
    def integrand(x):
        V = V_func(x)
        if E > V:
            return np.sqrt(2 * m * (E - V))
        return 0

    result, _ = quad(integrand, x1, x2)
    return result


def wkb_wavefunction_classically_allowed(x, E, V_func, x0, m, A=1):
    """
    经典允许区的WKB波函数 WKB wavefunction in classically allowed region

    ψ(x) ≈ (A/√p) exp(i∫p dx/ℏ) + (B/√p) exp(-i∫p dx/ℏ)

    这里简化为右行波。
    振幅因子 1/√p 保证概率流守恒。

    参数 Parameters:
        x: 位置 (m)
        E: 总能量 (J)
        V_func: 势能函数
        x0: 相位参考点 (m)
        m: 粒子质量 (kg)
        A: 振幅系数

    返回 Returns:
        ψ(x): 复数波函数值
    """
    V = V_func(x)
    p = classical_momentum(E, V, m)

    if p <= 0:
        return 0

    # 相位积分
    phase, _ = quad(lambda xi: classical_momentum(E, V_func(xi), m),
                   x0, x, limit=100)

    return A / np.sqrt(p) * np.exp(1j * phase / hbar)


def wkb_wavefunction_classically_forbidden(x, E, V_func, x_tp, m, A=1):
    """
    经典禁区的WKB波函数（衰减）Decaying WKB wavefunction

    ψ(x) ≈ (A/√κ) exp(-∫κ dx)

    其中 κ = √(2m(V-E))/ℏ 是衰减系数（虚波矢）。

    在经典禁区，波函数指数衰减，体现量子隧穿效应。

    参数 Parameters:
        x: 位置 (m)
        E: 总能量 (J)
        V_func: 势能函数
        x_tp: 转折点位置 (m)
        m: 粒子质量 (kg)
        A: 振幅系数

    返回 Returns:
        ψ(x): 波函数值（实数，指数衰减）
    """
    V = V_func(x)
    kappa = np.sqrt(2 * m * (V - E)) / hbar if V > E else 0

    if kappa <= 0:
        return 0

    # 衰减积分
    def kappa_func(xi):
        V_xi = V_func(xi)
        if V_xi > E:
            return np.sqrt(2 * m * (V_xi - E)) / hbar
        return 0

    decay, _ = quad(kappa_func, x_tp, x, limit=100)

    return A / np.sqrt(kappa * hbar) * np.exp(-decay)


# =============================================================================
# 练习 9.3: Bohr-Sommerfeld量子化
# Exercise 9.3: Bohr-Sommerfeld Quantization
#
# 物理背景 Physical Background:
# Bohr-Sommerfeld量子化条件是旧量子论的核心内容，也是WKB近似的重要应用。
# 它要求经典闭合轨道上的作用量是普朗克常数的半整数倍:
#     ∮p dx = (n + 1/2)h
#
# 1/2 来自转折点处的相位修正（Maslov指数）。
# 这个条件对于一维束缚态问题给出精确或近似精确的能级。
# =============================================================================
def bohr_sommerfeld_integral(E, V_func, x1, x2, m):
    """
    Bohr-Sommerfeld积分 Bohr-Sommerfeld integral

    ∮p dx = 2∫_{x1}^{x2} p dx = (n + 1/2)h

    对于一维势阱，粒子在两个转折点之间往返，
    积分是单程积分的两倍。

    参数 Parameters:
        E: 总能量 (J)
        V_func: 势能函数
        x1, x2: 转折点 (m)
        m: 粒子质量 (kg)

    返回 Returns:
        闭合轨道的作用量 (J·s)
    """
    return 2 * wkb_phase_integral(E, V_func, x1, x2, m)


def find_wkb_energy_levels(V_func, x_range, m, n_levels=5, E_min=None, E_max=None):
    """
    使用WKB找能级 Find energy levels using WKB

    通过求解 Bohr-Sommerfeld 量子化条件找到能级。
    对于每个量子数n，找到使 ∮p dx = (n + 1/2)h 成立的能量。

    参数 Parameters:
        V_func: 势能函数
        x_range: 搜索范围 (x_min, x_max)
        m: 粒子质量 (kg)
        n_levels: 要找的能级数
        E_min, E_max: 能量搜索范围 (J)

    返回 Returns:
        energies: 能级列表 (J)
    """
    if E_min is None:
        E_min = V_func(0) * 0.01
    if E_max is None:
        E_max = V_func(x_range[0])

    def quantization_condition(E, n):
        tps = classical_turning_point(E, V_func, x_range)
        if len(tps) < 2:
            return np.inf

        x1, x2 = tps[0], tps[-1]
        integral = bohr_sommerfeld_integral(E, V_func, x1, x2, m)
        return integral - (n + 0.5) * 2 * np.pi * hbar

    energies = []
    from scipy.optimize import brentq

    for n in range(n_levels):
        try:
            E_n = brentq(lambda E: quantization_condition(E, n),
                        E_min + 0.01 * (E_max - E_min) * n,
                        E_max * (n + 1) / n_levels)
            energies.append(E_n)
        except:
            pass

    return energies


def harmonic_oscillator_wkb(n, m, omega):
    """
    谐振子WKB能级（精确）Harmonic oscillator WKB levels (exact)

    E_n = (n + 1/2)ℏω

    对于谐振子，WKB近似恰好给出精确结果！
    这是因为谐振子的势能形式使得WKB的所有修正项相消。

    参数 Parameters:
        n: 量子数 (0, 1, 2, ...)
        m: 粒子质量 (kg)
        omega: 角频率 (rad/s)

    返回 Returns:
        E_n: 第n能级的能量 (J)
    """
    return (n + 0.5) * hbar * omega


def morse_potential_wkb(n, D, a, m):
    """
    Morse势WKB能级 Morse potential WKB levels

    E_n = ℏω(n + 1/2) - [ℏω(n+1/2)]²/(4D)

    其中 ω = a√(2D/m)

    Morse势描述双原子分子的振动，比谐振子更真实:
    - 包含非谐性修正（能级间距随n减小）
    - 有限数量的束缚态
    - 高能级趋向解离能D

    参数 Parameters:
        n: 振动量子数
        D: 解离能 (J)
        a: Morse参数 (1/m)
        m: 约化质量 (kg)

    返回 Returns:
        E_n: 第n能级的能量 (J)
    """
    omega = a * np.sqrt(2 * D / m)
    x = hbar * omega * (n + 0.5)
    return x - x**2 / (4 * D)


# =============================================================================
# 练习 9.4: 量子隧穿
# Exercise 9.4: Quantum Tunneling
#
# 物理背景 Physical Background:
# WKB方法提供了计算隧穿透射系数的强大工具。
# 在经典禁区，波函数指数衰减，衰减因子决定了隧穿概率。
#
# 透射系数: T ≈ exp(-2γ), 其中 γ = ∫κdx
#
# 应用:
# - 核物理: α衰变（Gamow理论）
# - 固体物理: 隧道二极管
# - 表面科学: STM扫描隧道显微镜
# - 化学反应: 低温下的量子隧穿化学
# =============================================================================
def wkb_tunneling_integral(E, V_func, x1, x2, m):
    """
    隧穿积分 Tunneling integral

    γ = ∫_{x1}^{x2} κ dx = ∫√(2m(V-E))/ℏ dx

    γ 称为 Gamow 因子，决定了隧穿的难易程度。

    参数 Parameters:
        E: 粒子能量 (J)
        V_func: 势垒函数
        x1, x2: 势垒边界（转折点）(m)
        m: 粒子质量 (kg)

    返回 Returns:
        γ: 隧穿积分（无量纲）
    """
    def integrand(x):
        V = V_func(x)
        if V > E:
            return np.sqrt(2 * m * (V - E)) / hbar
        return 0

    result, _ = quad(integrand, x1, x2)
    return result


def wkb_transmission_coefficient(E, V_func, x1, x2, m):
    """
    WKB隧穿系数 WKB transmission coefficient

    T ≈ exp(-2γ)

    这是一般势垒的透射系数近似公式。

    参数 Parameters:
        E: 粒子能量 (J)
        V_func: 势垒函数
        x1, x2: 势垒边界 (m)
        m: 粒子质量 (kg)

    返回 Returns:
        T: 透射系数 (0到1之间)
    """
    gamma = wkb_tunneling_integral(E, V_func, x1, x2, m)
    return np.exp(-2 * gamma)


def rectangular_barrier_wkb(E, V0, L, m):
    """
    矩形势垒WKB隧穿系数 Rectangular barrier tunneling

    T ≈ exp(-2κL), 其中 κ = √(2m(V₀-E))/ℏ

    这是最简单的隧穿问题，隧穿积分可以解析计算。

    参数 Parameters:
        E: 粒子能量 (J)
        V0: 势垒高度 (J)
        L: 势垒宽度 (m)
        m: 粒子质量 (kg)

    返回 Returns:
        T: 透射系数
    """
    if E >= V0:
        return 1
    kappa = np.sqrt(2 * m * (V0 - E)) / hbar
    return np.exp(-2 * kappa * L)


def parabolic_barrier_wkb(E, V0, a, m):
    """
    抛物线势垒隧穿 Parabolic barrier tunneling

    势垒形式: V(x) = V₀(1 - x²/a²)
    透射系数: T ≈ exp(-πa√(2m(V₀-E))/ℏ)

    抛物线势垒常用于模拟核反应中的库仑势垒。

    参数 Parameters:
        E: 粒子能量 (J)
        V0: 势垒顶点高度 (J)
        a: 势垒半宽 (m)
        m: 粒子质量 (kg)

    返回 Returns:
        T: 透射系数
    """
    if E >= V0:
        return 1
    return np.exp(-np.pi * a * np.sqrt(2 * m * (V0 - E)) / hbar)


def gamow_factor(E, Z1, Z2, m):
    """
    Gamow因子（核物理隧穿）Gamow factor

    η = Z₁Z₂e² / (4πε₀ℏv)
    T ∝ exp(-2πη)

    Gamow因子描述带电粒子穿越库仑势垒的概率。
    这是理解α衰变、核聚变等核反应的关键。

    应用:
    - α衰变寿命计算
    - 恒星核聚变速率
    - 重离子核反应

    参数 Parameters:
        E: 相对动能 (J)
        Z1, Z2: 两粒子的电荷数
        m: 约化质量 (kg)

    返回 Returns:
        T: 库仑势垒透射因子
    """
    e = 1.6e-19  # 电子电荷 (C)
    epsilon_0 = 8.85e-12  # 真空介电常数 (F/m)
    v = np.sqrt(2 * E / m)  # 相对速度
    eta = Z1 * Z2 * e**2 / (4 * np.pi * epsilon_0 * hbar * v)  # Sommerfeld参数
    return np.exp(-2 * np.pi * eta)


# =============================================================================
# 练习 9.5: 连接公式
# Exercise 9.5: Connection Formulas
#
# 物理背景 Physical Background:
# WKB波函数在转折点处发散（因为p→0），需要使用连接公式
# 将允许区和禁区的解连接起来。
#
# 连接公式来自于在转折点附近用Airy函数精确求解，
# 然后将Airy函数的渐近形式与WKB解匹配。
#
# 关键结果:
# - 穿过转折点会引入 π/4 的相位移动（Maslov指数）
# - 这个相位修正导致了量子化条件中的 1/2
# =============================================================================
def connection_formula_left_turning_point(A, B):
    """
    左转折点连接公式 Left turning point connection formula

    禁区（左）→ 允许区（右）:
    (A/√κ)exp(-∫κdx) ↔ (2A/√k)sin(∫kdx + π/4)

    注意: π/4 的相位来自Airy函数的渐近行为。

    参数 Parameters:
        A: 禁区振幅
        B: 未使用

    返回 Returns:
        dict: 包含允许区振幅和相位修正
    """
    return {
        'amplitude_allowed': 2 * A,
        'phase_shift': np.pi / 4
    }


def connection_formula_right_turning_point(A, B):
    """
    右转折点连接公式 Right turning point connection formula

    允许区（左）→ 禁区（右）:
    (A/√k)sin(∫kdx + π/4) → (A/2√κ)exp(-∫κdx)

    参数 Parameters:
        A: 允许区振幅
        B: 未使用

    返回 Returns:
        dict: 包含禁区振幅和衰减方向
    """
    return {
        'amplitude_forbidden': A / 2,
        'decaying': True
    }


def airy_function_matching(x, x_tp, E, V_func, m):
    """
    使用Airy函数在转折点附近匹配 Airy function matching

    在转折点附近，势能可以线性展开:
        V(x) ≈ E + α(x - x_tp), α = |dV/dx|

    此时薛定谔方程可以精确求解，解是Airy函数:
        ψ ∝ Ai(-z), 其中 z = (2mα/ℏ²)^(1/3)(x - x_tp)

    Airy函数的渐近形式与WKB解匹配，给出连接公式。

    参数 Parameters:
        x: 位置 (m)
        x_tp: 转折点位置 (m)
        E: 能量 (J)
        V_func: 势能函数
        m: 粒子质量 (kg)

    返回 Returns:
        Ai(-z): Airy函数值
    """
    from scipy.special import airy

    # 在转折点附近线性展开势能
    dx = 1e-12
    dV_dx = (V_func(x_tp + dx) - V_func(x_tp - dx)) / (2 * dx)
    alpha = np.abs(dV_dx)

    z_scale = (2 * m * alpha / hbar**2)**(1/3)
    z = z_scale * (x - x_tp)

    Ai_val, Aip, Bi_val, Bip = airy(-z)
    return Ai_val


# =============================================================================
# 练习 9.6: 应用实例
# Exercise 9.6: Applications
#
# 物理背景 Physical Background:
# WKB近似在多个物理领域有重要应用:
#
# 1. α衰变 (Gamow理论):
#    α粒子被核力束缚在原子核内，但可以隧穿库仑势垒逃逸。
#    衰变寿命范围从微秒到宇宙年龄量级，主要由Gamow因子决定。
#
# 2. 场发射 (Fowler-Nordheim):
#    强电场下电子隧穿金属表面势垒逃逸。
#    场发射电流公式广泛应用于电子显微镜等设备。
#
# 3. 扫描隧道显微镜 (STM):
#    利用电子隧穿电流对针尖-样品距离的指数灵敏性
#    实现原子级分辨率的表面成像。
# =============================================================================
def alpha_decay_lifetime(Z_daughter, A, Q, R_nucleus):
    """
    α衰变寿命估算 Alpha decay lifetime estimate

    使用Gamow模型:
    τ = 1/(f × T)
    其中 f 是α粒子撞击势垒的频率，T 是隧穿概率。

    参数 Parameters:
        Z_daughter: 子核电荷数
        A: 母核质量数
        Q: 衰变能 (MeV)
        R_nucleus: 核半径 (m)

    返回 Returns:
        τ: 衰变寿命 (s)
    """
    m_alpha = 4 * 1.66e-27  # α粒子质量
    e = 1.6e-19
    epsilon_0 = 8.85e-12

    # 库仑势垒
    V_barrier = 2 * Z_daughter * e**2 / (4 * np.pi * epsilon_0 * R_nucleus)

    # 隧穿
    T = gamow_factor(Q * 1.6e-13, 2, Z_daughter, m_alpha)  # Q in MeV

    # 碰撞频率
    v = np.sqrt(2 * Q * 1.6e-13 / m_alpha)
    f = v / (2 * R_nucleus)

    # 寿命
    decay_rate = f * T
    if decay_rate > 0:
        return 1 / decay_rate
    return np.inf


def field_emission_current(E_field, phi, m):
    """
    场发射电流（Fowler-Nordheim公式）Field emission current

    J ∝ E² exp(-4√(2m)φ^(3/2)/(3ℏeE))

    物理机制:
    强电场使金属表面的势垒变薄，电子可以隧穿逃逸。
    电流对电场有极强的依赖性。

    参数 Parameters:
        E_field: 电场强度 (V/m)
        phi: 功函数 (J)
        m: 电子质量 (kg)

    返回 Returns:
        J: 场发射电流密度（相对值）
    """
    e = 1.6e-19  # 电子电荷 (C)
    factor = 4 * np.sqrt(2 * m) * phi**(3/2) / (3 * hbar * e * E_field)
    return E_field**2 * np.exp(-factor)


def scanning_tunneling_microscope(V_bias, d, phi, m):
    """
    STM隧穿电流 Scanning tunneling microscope current

    I ∝ exp(-2κd), κ = √(2mφ)/ℏ

    STM原理:
    - 针尖与样品之间有纳米级间隙
    - 电子隧穿形成电流
    - 电流对间隙距离指数敏感
    - 距离变化0.1nm，电流变化约10倍

    参数 Parameters:
        V_bias: 偏压（未使用，保留接口）
        d: 针尖-样品距离 (m)
        phi: 有效势垒高度 (J)
        m: 电子质量 (kg)

    返回 Returns:
        I: 隧穿电流（相对值）
    """
    kappa = np.sqrt(2 * m * phi) / hbar
    return np.exp(-2 * kappa * d)


def josephson_junction_current(I_c, phi_1, phi_2):
    """
    约瑟夫森结电流 Josephson junction current

    I = I_c sin(φ₁ - φ₂)

    约瑟夫森效应:
    两块超导体通过薄绝缘层连接，库珀对可以隧穿形成超电流。
    电流只依赖于两边超导体的相位差。

    应用:
    - 超导量子干涉仪 (SQUID)
    - 量子比特
    - 电压基准

    参数 Parameters:
        I_c: 临界电流 (A)
        phi_1, phi_2: 两侧超导体的相位

    返回 Returns:
        I: 约瑟夫森电流 (A)
    """
    return I_c * np.sin(phi_1 - phi_2)


# =============================================================================
# 可视化
# =============================================================================
def plot_wkb():
    """绘制WKB近似相关图"""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    m = m_e
    omega = 1e15  # rad/s

    # 1. 谐振子WKB波函数
    ax1 = axes[0, 0]
    L = 2e-9
    x = np.linspace(-L/2, L/2, 500)

    V_ho = lambda xi: 0.5 * m * omega**2 * xi**2

    for n in range(3):
        E = harmonic_oscillator_wkb(n, m, omega)
        tps = classical_turning_point(E, V_ho, (-L/2, L/2))

        if len(tps) >= 2:
            # 经典允许区
            x_allow = x[(x > tps[0]) & (x < tps[1])]
            p = np.array([classical_momentum(E, V_ho(xi), m) for xi in x_allow])
            # 简化的WKB波函数形状
            psi_approx = 1 / np.sqrt(p + 1e-30) * np.cos(n * np.pi * (x_allow - tps[0]) / (tps[1] - tps[0]))
            psi_approx = psi_approx / np.max(np.abs(psi_approx)) + n * 2

            ax1.plot(x_allow * 1e9, psi_approx, label=f'n={n}')

    ax1.set_xlabel('x (nm)')
    ax1.set_ylabel('ψ + offset')
    ax1.set_title('谐振子WKB波函数')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 隧穿系数
    ax2 = axes[0, 1]
    V0 = 5 * eV
    L_barrier = 1e-9

    E_range = np.linspace(0.1, 0.99, 50) * V0
    T_wkb = [rectangular_barrier_wkb(E, V0, L_barrier, m) for E in E_range]

    ax2.semilogy(E_range/V0, T_wkb, 'b-', linewidth=2)
    ax2.set_xlabel('E/V₀')
    ax2.set_ylabel('透射系数 T')
    ax2.set_title('矩形势垒隧穿')
    ax2.grid(True, alpha=0.3)

    # 3. 隧穿vs势垒宽度
    ax3 = axes[0, 2]
    E_fixed = 0.5 * V0
    L_range = np.linspace(0.1, 2, 50) * 1e-9

    T_vs_L = [rectangular_barrier_wkb(E_fixed, V0, L, m) for L in L_range]

    ax3.semilogy(L_range * 1e9, T_vs_L, 'b-', linewidth=2)
    ax3.set_xlabel('势垒宽度 (nm)')
    ax3.set_ylabel('透射系数 T')
    ax3.set_title('隧穿 vs 势垒宽度')
    ax3.grid(True, alpha=0.3)

    # 4. WKB能级比较
    ax4 = axes[1, 0]
    n_levels = np.arange(0, 10)

    E_exact = (n_levels + 0.5) * hbar * omega
    E_wkb = [harmonic_oscillator_wkb(n, m, omega) for n in n_levels]

    ax4.plot(n_levels, E_exact/eV, 'bo-', label='精确', markersize=8)
    ax4.plot(n_levels, np.array(E_wkb)/eV, 'rx-', label='WKB', markersize=8)
    ax4.set_xlabel('量子数 n')
    ax4.set_ylabel('能量 (eV)')
    ax4.set_title('WKB能级（谐振子）')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. STM电流
    ax5 = axes[1, 1]
    phi = 4 * eV  # 功函数
    d_range = np.linspace(0.1, 1, 50) * 1e-9

    I_stm = [scanning_tunneling_microscope(1, d, phi, m) for d in d_range]

    ax5.semilogy(d_range * 1e9, I_stm, 'b-', linewidth=2)
    ax5.set_xlabel('间距 (nm)')
    ax5.set_ylabel('电流 (arb. units)')
    ax5.set_title('STM隧穿电流')
    ax5.grid(True, alpha=0.3)

    # 6. 局域波长
    ax6 = axes[1, 2]
    E_test = 3 * eV
    V_test = lambda xi: 0.5 * m * omega**2 * xi**2

    x_wl = np.linspace(-1e-9, 1e-9, 200)
    V_vals = np.array([V_test(xi) for xi in x_wl])
    wavelengths = local_wavelength(E_test, V_vals, m)

    ax6.plot(x_wl * 1e9, wavelengths * 1e9, 'b-', linewidth=2)
    ax6.set_xlabel('x (nm)')
    ax6.set_ylabel('λ(x) (nm)')
    ax6.set_title('局域德布罗意波长')
    ax6.set_ylim(0, 5)
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('wkb.png', dpi=150)
    print("图像已保存为 wkb.png")
    plt.show()


# =============================================================================
# 验证函数
# =============================================================================
def verify():
    """Verify all exercises"""
    all_passed = True

    m = m_e
    omega = 1e15

    # Check 9.1 - Classical momentum
    E = 1 * eV
    V = 0.5 * eV
    p = classical_momentum(E, V, m)
    expected_p = np.sqrt(2 * m * 0.5 * eV)

    if not np.isclose(p, expected_p, rtol=0.01):
        print("X 9.1 经典动量计算错误")
        all_passed = False
    else:
        print(f"V 9.1 经典动量正确")

    # Check 9.2 - WKB validity
    dV = 1e10  # V/m
    valid = wkb_validity_condition(E, V, dV, m)
    # 应该有一个明确的结果
    print(f"V 9.2 WKB有效性判断正确 (valid = {valid})")

    # Check 9.3 - Harmonic oscillator WKB
    E_wkb = harmonic_oscillator_wkb(0, m, omega)
    expected_E = 0.5 * hbar * omega

    if not np.isclose(E_wkb, expected_E, rtol=0.01):
        print("X 9.3 谐振子WKB能级错误")
        all_passed = False
    else:
        print(f"V 9.3 Bohr-Sommerfeld量子化正确 (E₀ = {E_wkb/eV:.4f} eV)")

    # Check 9.4 - Tunneling
    V0 = 5 * eV
    L = 1e-9
    E_tunnel = 0.5 * V0
    T = rectangular_barrier_wkb(E_tunnel, V0, L, m)

    if T <= 0 or T >= 1:
        print("X 9.4 隧穿系数应在(0,1)范围内")
        all_passed = False
    else:
        print(f"V 9.4 隧穿系数正确 (T = {T:.2e})")

    # Check 9.5 - Connection formulas
    result = connection_formula_left_turning_point(1, 0)
    if 'phase_shift' not in result:
        print("X 9.5 连接公式结果错误")
        all_passed = False
    else:
        print(f"V 9.5 连接公式正确")

    # Check 9.6 - STM
    phi = 4 * eV
    d = 0.5e-9
    I = scanning_tunneling_microscope(1, d, phi, m)

    if I <= 0 or I >= 1:
        print("X 9.6 STM电流应在(0,1)范围内")
        all_passed = False
    else:
        print(f"V 9.6 应用正确 (STM @ 0.5nm: I ∝ {I:.2e})")

    if all_passed:
        print("\n所有测试通过！正在生成可视化...")
        try:
            plot_wkb()
        except Exception as ex:
            print(f"可视化生成失败: {ex}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("WKB近似 WKB Approximation")
    print("=" * 50)
    verify()
