"""
波导与谐振腔 Waveguides and Cavities
难度 Difficulty: ★★★★

学习目标 Learning Objectives:
- 理解波导中电磁波的传播特性 (Understand EM wave propagation in waveguides)
- 掌握截止频率和模式分析 (Master cutoff frequency and mode analysis)
- 分析谐振腔的共振条件和品质因子 (Analyze cavity resonance and Q factor)
- 理解波导中的色散和损耗 (Understand dispersion and losses)

物理背景 Physical Background:
波导是限制电磁波在特定路径传播的结构。由于边界条件限制，
只有满足特定条件的模式才能传播。存在截止频率，低于此频率
的波无法传播。谐振腔是封闭的波导，只允许特定频率共振。

核心公式 Key Formulas:
- 矩形波导截止频率: f_c = (c/2)√((m/a)² + (n/b)²)
- 波导波长: λ_g = λ/√(1 - (λ/λ_c)²) > λ
- 相速度: v_p = c/√(1 - (f_c/f)²) > c
- 群速度: v_g = c√(1 - (f_c/f)²) < c
- 色散关系: v_p × v_g = c²
- TE波阻抗: Z_TE = η₀/√(1 - (f_c/f)²)
- TM波阻抗: Z_TM = η₀√(1 - (f_c/f)²)
- 品质因子: Q = ω₀U/P_loss = f₀/Δf

模式类型 Mode Types:
- TE模式（横电模）: E_z = 0，存在H_z
- TM模式（横磁模）: H_z = 0，存在E_z
- TEM模式: E_z = H_z = 0（单导体波导不支持）

单位说明 Units:
- 频率: Hz, GHz
- 波长: m, mm
- 衰减: Np/m (奈培/米) 或 dB/m
- 品质因子Q: 无量纲
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import c, epsilon_0, mu_0

# I AM NOT DONE

# =============================================================================
# 练习 9.1: 矩形波导基础
# Exercise 9.1: Rectangular Waveguide Basics
# =============================================================================
# 物理背景 Physical Background:
# 矩形波导是最常用的微波传输线。波在导体壁之间反射传播，
# 只有满足边界条件的特定模式能够传播。主模TE₁₀是最低截止频率的模式。

def cutoff_frequency_rectangular(a, b, m, n):
    """
    矩形波导截止频率
    Rectangular waveguide cutoff frequency

    参数 Parameters:
        a: 宽边尺寸 [m]（沿x方向）
        b: 窄边尺寸 [m]（沿y方向）
        m, n: 模式指数（非负整数）

    返回 Returns:
        截止频率 f_c [Hz]

    公式 Formula:
        f_c = (c/2)√((m/a)² + (n/b)²)

    常用模式:
        TE₁₀: f_c = c/(2a)（主模，最低截止频率）
        TE₂₀: f_c = c/a
        TE₀₁: f_c = c/(2b)
    """
    return (c / 2) * np.sqrt((m/a)**2 + (n/b)**2)


def cutoff_wavelength_rectangular(a, b, m, n):
    """
    截止波长
    Cutoff wavelength

    参数 Parameters:
        a, b: 波导尺寸 [m]
        m, n: 模式指数

    返回 Returns:
        截止波长 λ_c [m]

    公式 Formula:
        λ_c = 2/√((m/a)² + (n/b)²)

    说明: 波长大于λ_c的波无法传播
    """
    f_c = cutoff_frequency_rectangular(a, b, m, n)
    if f_c == 0:
        return np.inf
    return c / f_c


def guide_wavelength(wavelength, wavelength_c):
    """
    波导波长
    Guide wavelength

    参数 Parameters:
        wavelength: 自由空间波长 λ [m]
        wavelength_c: 截止波长 λ_c [m]

    返回 Returns:
        波导波长 λ_g [m]

    公式 Formula:
        λ_g = λ/√(1 - (λ/λ_c)²)

    特点:
        λ_g > λ（波导中波长总是大于自由空间波长）
        λ → λ_c 时，λ_g → ∞
    """
    if wavelength >= wavelength_c:
        return np.inf  # 截止，无法传播
    return wavelength / np.sqrt(1 - (wavelength/wavelength_c)**2)


def phase_velocity(f, f_c):
    """
    相速度
    Phase velocity

    参数 Parameters:
        f: 工作频率 [Hz]
        f_c: 截止频率 [Hz]

    返回 Returns:
        相速度 v_p [m/s]

    公式 Formula:
        v_p = c/√(1 - (f_c/f)²)

    特点: v_p > c（超光速，但不传递信息）
    """
    if f <= f_c:
        return np.inf
    return c / np.sqrt(1 - (f_c/f)**2)


def group_velocity(f, f_c):
    """
    群速度
    Group velocity

    参数 Parameters:
        f: 工作频率 [Hz]
        f_c: 截止频率 [Hz]

    返回 Returns:
        群速度 v_g [m/s]

    公式 Formula:
        v_g = c√(1 - (f_c/f)²)

    特点:
        v_g < c（能量传播速度小于光速）
        v_p × v_g = c²（色散关系）
    """
    if f <= f_c:
        return 0  # 截止时能量不传播
    return c * np.sqrt(1 - (f_c/f)**2)


# =============================================================================
# 练习 9.2: TE和TM模式
# Exercise 9.2: TE and TM Modes
# =============================================================================
# 物理背景 Physical Background:
# TE模式（横电模）：电场完全横向，E_z = 0，存在纵向磁场H_z
# TM模式（横磁模）：磁场完全横向，H_z = 0，存在纵向电场E_z
# TE₁₀是矩形波导的主模，具有最低的截止频率。

def te_mode_field_hz(x, y, a, b, m, n, H0=1):
    """
    TE_mn模式的H_z分量
    H_z component of TE_mn mode

    参数 Parameters:
        x, y: 波导内位置坐标 [m]
        a, b: 波导尺寸 [m]
        m, n: 模式指数
        H0: 振幅 [A/m]

    返回 Returns:
        H_z [A/m]

    公式 Formula:
        H_z = H₀ cos(mπx/a) cos(nπy/b)

    边界条件: 在导体壁上 ∂H_z/∂n = 0
    """
    return H0 * np.cos(m * np.pi * x / a) * np.cos(n * np.pi * y / b)


def tm_mode_field_ez(x, y, a, b, m, n, E0=1):
    """
    TM_mn模式的E_z分量
    E_z component of TM_mn mode

    参数 Parameters:
        x, y: 波导内位置坐标 [m]
        a, b: 波导尺寸 [m]
        m, n: 模式指数（必须m≥1且n≥1）
        E0: 振幅 [V/m]

    返回 Returns:
        E_z [V/m]

    公式 Formula:
        E_z = E₀ sin(mπx/a) sin(nπy/b)

    边界条件: 在导体壁上 E_z = 0
    注意: TM模式要求m≥1且n≥1，所以没有TM₁₀或TM₀₁
    """
    return E0 * np.sin(m * np.pi * x / a) * np.sin(n * np.pi * y / b)


def te10_dominant_mode_cutoff(a):
    """
    TE₁₀主模截止频率
    TE₁₀ dominant mode cutoff frequency

    参数 Parameters:
        a: 波导宽边尺寸 [m]

    返回 Returns:
        截止频率 f_c [Hz]

    公式 Formula:
        f_c = c/(2a)

    说明: TE₁₀是矩形波导最常用的模式
    工作频率通常选在 f_c < f < 2f_c（单模工作区）
    """
    return c / (2 * a)


def wave_impedance_te(f, f_c, eta_0=None):
    """
    TE模式的波阻抗
    Wave impedance for TE mode

    参数 Parameters:
        f: 工作频率 [Hz]
        f_c: 截止频率 [Hz]
        eta_0: 自由空间阻抗 [Ω]（默认377Ω）

    返回 Returns:
        波阻抗 Z_TE [Ω]

    公式 Formula:
        Z_TE = η₀/√(1 - (f_c/f)²)

    特点: Z_TE > η₀（TE模式波阻抗大于自由空间阻抗）
    """
    if eta_0 is None:
        eta_0 = np.sqrt(mu_0 / epsilon_0)  # ≈ 377 Ω
    if f <= f_c:
        return np.inf
    return eta_0 / np.sqrt(1 - (f_c/f)**2)


def wave_impedance_tm(f, f_c, eta_0=None):
    """
    TM模式的波阻抗
    Wave impedance for TM mode

    参数 Parameters:
        f: 工作频率 [Hz]
        f_c: 截止频率 [Hz]
        eta_0: 自由空间阻抗 [Ω]

    返回 Returns:
        波阻抗 Z_TM [Ω]

    公式 Formula:
        Z_TM = η₀√(1 - (f_c/f)²)

    特点: Z_TM < η₀（TM模式波阻抗小于自由空间阻抗）
    """
    if eta_0 is None:
        eta_0 = np.sqrt(mu_0 / epsilon_0)
    if f <= f_c:
        return 0
    return eta_0 * np.sqrt(1 - (f_c/f)**2)


# =============================================================================
# 练习 9.3: 圆形波导
# Exercise 9.3: Circular Waveguide
# =============================================================================
# 物理背景 Physical Background:
# 圆形波导的模式由贝塞尔函数描述。主模是TE₁₁模式。
# 圆形波导常用于旋转接头和高功率应用。
# 截止频率由贝塞尔函数的零点决定。

def cutoff_frequency_circular_te(a, m, n):
    """
    圆形波导TE_mn模式截止频率
    TE mode cutoff frequency for circular waveguide

    参数 Parameters:
        a: 波导半径 [m]
        m: 角向模式指数
        n: 径向模式指数（第n个零点）

    返回 Returns:
        截止频率 f_c [Hz]

    公式 Formula:
        f_c = c×p'_mn/(2πa)
        p'_mn: J_m'(x)=0的第n个根（贝塞尔函数导数的零点）

    常用值:
        TE₁₁: p'₁₁ = 1.841（主模，最低截止频率）
        TE₀₁: p'₀₁ = 3.832
        TE₂₁: p'₂₁ = 3.054
    """
    # J_m'(x) = 0 的根值
    p_prime_mn = {
        (0, 1): 3.832, (1, 1): 1.841, (2, 1): 3.054,
        (0, 2): 7.016, (1, 2): 5.331, (2, 2): 6.706,
        (0, 3): 10.174, (1, 3): 8.536
    }
    key = (m, n)
    if key not in p_prime_mn:
        return None
    return c * p_prime_mn[key] / (2 * np.pi * a)


def cutoff_frequency_circular_tm(a, m, n):
    """
    圆形波导TM_mn模式截止频率
    TM mode cutoff frequency for circular waveguide

    参数 Parameters:
        a: 波导半径 [m]
        m: 角向模式指数
        n: 径向模式指数

    返回 Returns:
        截止频率 f_c [Hz]

    公式 Formula:
        f_c = c×p_mn/(2πa)
        p_mn: J_m(x)=0的第n个根（贝塞尔函数的零点）

    常用值:
        TM₀₁: p₀₁ = 2.405
        TM₁₁: p₁₁ = 3.832
        TM₂₁: p₂₁ = 5.136
    """
    # J_m(x) = 0 的根值
    p_mn = {
        (0, 1): 2.405, (1, 1): 3.832, (2, 1): 5.136,
        (0, 2): 5.520, (1, 2): 7.016, (2, 2): 8.417,
        (0, 3): 8.654, (1, 3): 10.174
    }
    key = (m, n)
    if key not in p_mn:
        return None
    return c * p_mn[key] / (2 * np.pi * a)


def circular_te11_cutoff(a):
    """
    TE₁₁模式截止频率（圆形波导主模）
    TE₁₁ mode cutoff (dominant mode)

    参数 Parameters:
        a: 波导半径 [m]

    返回 Returns:
        截止频率 f_c [Hz]

    公式 Formula:
        f_c = c×1.841/(2πa)

    说明: TE₁₁是圆形波导截止频率最低的模式
    """
    return c * 1.841 / (2 * np.pi * a)


# =============================================================================
# 练习 9.4: 谐振腔
# Exercise 9.4: Resonant Cavities
# =============================================================================
# 物理背景 Physical Background:
# 谐振腔是封闭的波导，电磁能量在腔内来回反射形成驻波。
# 只有满足边界条件的特定频率能够共振。
# 品质因子Q描述能量储存与损耗的比值，越高越好。

def resonant_frequency_rectangular(a, b, d, m, n, p):
    """
    矩形谐振腔共振频率
    Resonant frequency of rectangular cavity

    参数 Parameters:
        a, b: 波导截面尺寸 [m]
        d: 腔长（沿z方向）[m]
        m, n, p: 三个方向的模式指数

    返回 Returns:
        共振频率 f_mnp [Hz]

    公式 Formula:
        f_mnp = (c/2)√((m/a)² + (n/b)² + (p/d)²)

    常用模式:
        TE₁₀₁: 最常用的谐振模式
    """
    return (c / 2) * np.sqrt((m/a)**2 + (n/b)**2 + (p/d)**2)


def resonant_frequency_cylindrical(a, d, m, n, p, mode='TE'):
    """
    圆柱形谐振腔共振频率
    Resonant frequency of cylindrical cavity

    参数 Parameters:
        a: 腔半径 [m]
        d: 腔长 [m]
        m, n: 横向模式指数
        p: 纵向模式指数
        mode: 'TE' 或 'TM'

    返回 Returns:
        共振频率 [Hz]

    公式 Formula:
        TE: f = (c/2π)√((p'_mn/a)² + (pπ/d)²)
        TM: f = (c/2π)√((p_mn/a)² + (pπ/d)²)
    """
    # 贝塞尔函数根值
    p_prime_mn = {(0, 1): 3.832, (1, 1): 1.841, (2, 1): 3.054}
    p_mn = {(0, 1): 2.405, (1, 1): 3.832, (2, 1): 5.136}

    key = (m, n)
    if mode == 'TE':
        if key not in p_prime_mn:
            return None
        x_val = p_prime_mn[key]
    else:
        if key not in p_mn:
            return None
        x_val = p_mn[key]

    return (c / (2 * np.pi)) * np.sqrt((x_val/a)**2 + (p * np.pi / d)**2)


def quality_factor(omega_0, stored_energy, power_loss):
    """
    品质因子
    Quality factor

    参数 Parameters:
        omega_0: 共振角频率 [rad/s]
        stored_energy: 储存能量 U [J]
        power_loss: 功率损耗 P_loss [W]

    返回 Returns:
        品质因子 Q（无量纲）

    公式 Formula:
        Q = ω₀U/P_loss

    物理意义:
        Q = 2π × (储能)/(每周期损耗)
        Q越高，谐振峰越尖锐，选择性越好
        典型值: 铜腔 Q ~ 10³-10⁴，超导腔 Q ~ 10⁹-10¹¹
    """
    if power_loss == 0:
        return np.inf
    return omega_0 * stored_energy / power_loss


def bandwidth_from_q(f_0, Q):
    """
    半功率带宽
    Half-power bandwidth from Q

    参数 Parameters:
        f_0: 共振频率 [Hz]
        Q: 品质因子

    返回 Returns:
        带宽 Δf [Hz]

    公式 Formula:
        Δf = f₀/Q

    说明: 带宽是响应下降到峰值一半时的频率范围
    """
    return f_0 / Q


# =============================================================================
# 练习 9.5: 波导损耗
# Exercise 9.5: Waveguide Losses
# =============================================================================
# 物理背景 Physical Background:
# 波导损耗主要来自导体壁的欧姆损耗。高频电流集中在导体表面
#（趋肤效应），有效电阻增大。损耗与表面电阻和电流分布有关。

def skin_depth(f, sigma, mu_r=1):
    """
    趋肤深度
    Skin depth

    参数 Parameters:
        f: 频率 [Hz]
        sigma: 电导率 [S/m]
        mu_r: 相对磁导率

    返回 Returns:
        趋肤深度 δ [m]

    公式 Formula:
        δ = √(2/(ωμσ))

    说明:
        电流密度在深度δ处衰减到表面的1/e
        铜在10GHz: δ ≈ 0.66 μm
    """
    omega = 2 * np.pi * f
    mu = mu_r * mu_0
    return np.sqrt(2 / (omega * mu * sigma))


def surface_resistance(f, sigma, mu_r=1):
    """
    表面电阻
    Surface resistance

    参数 Parameters:
        f: 频率 [Hz]
        sigma: 电导率 [S/m]
        mu_r: 相对磁导率

    返回 Returns:
        表面电阻 R_s [Ω]

    公式 Formula:
        R_s = √(ωμ/(2σ)) = 1/(σδ)

    说明: R_s与√f成正比，频率越高损耗越大
    """
    delta = skin_depth(f, sigma, mu_r)
    return 1 / (sigma * delta)


def attenuation_te10(a, b, f, sigma, mu_r=1):
    """
    TE₁₀模式衰减常数（导体损耗）
    Attenuation constant for TE₁₀ mode

    参数 Parameters:
        a, b: 波导尺寸 [m]
        f: 工作频率 [Hz]
        sigma: 导体电导率 [S/m]
        mu_r: 相对磁导率

    返回 Returns:
        衰减常数 α [Np/m]

    公式 Formula:
        α = (R_s/(bη)) × (1 + 2b(f_c/f)²/a) / √(1-(f_c/f)²)

    说明: 接近截止频率时衰减急剧增大
    """
    f_c = te10_dominant_mode_cutoff(a)
    if f <= f_c:
        return np.inf  # 截止

    Rs = surface_resistance(f, sigma, mu_r)
    eta = np.sqrt(mu_0 / epsilon_0)  # 自由空间阻抗

    factor = 1 + 2 * b * (f_c/f)**2 / a
    alpha = Rs / (b * eta) * factor / np.sqrt(1 - (f_c/f)**2)
    return alpha


def power_attenuation_db(alpha, length):
    """
    功率衰减（dB）
    Power attenuation in dB

    参数 Parameters:
        alpha: 衰减常数 [Np/m]
        length: 传输距离 [m]

    返回 Returns:
        衰减量 [dB]

    公式 Formula:
        P(z)/P(0) = exp(-2αz)
        衰减(dB) = 8.686 × α × z

    转换: 1 Np = 8.686 dB
    """
    return 8.686 * alpha * length


# =============================================================================
# 练习 9.6: 波导耦合
# Exercise 9.6: Waveguide Coupling
# =============================================================================
# 物理背景 Physical Background:
# 波导与其他传输线或元件的连接需要耦合结构。
# 常用耦合方式包括孔径耦合、探针耦合和环耦合。
# 良好的耦合需要阻抗匹配以减少反射。

def coupling_aperture_field(E_inc, aperture_area, wavelength):
    """
    孔径耦合（简化模型）
    Aperture coupling (simplified)

    参数 Parameters:
        E_inc: 入射电场强度 [V/m]
        aperture_area: 孔径面积 [m²]
        wavelength: 波长 [m]

    返回 Returns:
        耦合场强度（正比量）

    说明: 小孔近似，耦合功率正比于孔面积和k²
    """
    k = 2 * np.pi / wavelength
    return E_inc * aperture_area * k**2


def waveguide_to_coax_coupling(a, d_probe, f, f_c):
    """
    波导到同轴探针耦合
    Waveguide to coax probe coupling

    参数 Parameters:
        a: 波导宽边 [m]
        d_probe: 探针深度 [m]
        f: 工作频率 [Hz]
        f_c: 截止频率 [Hz]

    返回 Returns:
        耦合系数（归一化）

    说明:
        探针通常放在波导中心（E场最大处）
        探针深度影响耦合强度
    """
    if f <= f_c:
        return 0
    # 探针在波导中心，与E场耦合
    coupling = np.sin(np.pi * d_probe / (2 * a))
    return coupling * np.sqrt(1 - (f_c/f)**2)


def iris_coupling_coefficient(aperture_width, a, f, f_c):
    """
    窄缝（光阑）耦合系数
    Iris coupling coefficient

    参数 Parameters:
        aperture_width: 光阑开口宽度 [m]
        a: 波导宽边 [m]
        f: 工作频率 [Hz]
        f_c: 截止频率 [Hz]

    返回 Returns:
        耦合系数

    说明: 光阑常用于波导滤波器和耦合器
    """
    if f <= f_c:
        return 0
    return (aperture_width / a)**2


def matched_load_reflection(Z_load, Z_waveguide):
    """
    负载反射系数
    Load reflection coefficient

    参数 Parameters:
        Z_load: 负载阻抗 [Ω]
        Z_waveguide: 波导阻抗 [Ω]

    返回 Returns:
        反射系数 Γ（复数）

    公式 Formula:
        Γ = (Z_L - Z_wg)/(Z_L + Z_wg)

    匹配条件: Z_L = Z_wg 时 Γ = 0（无反射）
    """
    return (Z_load - Z_waveguide) / (Z_load + Z_waveguide)


# =============================================================================
# 可视化
# =============================================================================
def plot_waveguides():
    """绘制波导相关图"""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 波导参数 (WR-90, X波段)
    a = 22.86e-3  # m (宽边)
    b = 10.16e-3  # m (窄边)

    # 1. 色散关系
    ax1 = axes[0, 0]
    f_c = te10_dominant_mode_cutoff(a)
    f = np.linspace(1.01 * f_c, 3 * f_c, 100)

    v_p = [phase_velocity(fi, f_c) for fi in f]
    v_g = [group_velocity(fi, f_c) for fi in f]

    ax1.plot(f/1e9, np.array(v_p)/c, 'b-', label='相速度 v_p/c', linewidth=2)
    ax1.plot(f/1e9, np.array(v_g)/c, 'r-', label='群速度 v_g/c', linewidth=2)
    ax1.axhline(y=1, color='k', linestyle='--', alpha=0.5)
    ax1.axvline(x=f_c/1e9, color='g', linestyle=':', alpha=0.5, label='f_c')
    ax1.set_xlabel('频率 (GHz)')
    ax1.set_ylabel('v/c')
    ax1.set_title('波导色散关系')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 3)

    # 2. TE₁₀模式场分布
    ax2 = axes[0, 1]
    x = np.linspace(0, a, 50)
    y = np.linspace(0, b, 30)
    X, Y = np.meshgrid(x, y)

    # E_y 分布 (TE₁₀)
    E_y = np.sin(np.pi * X / a)

    im = ax2.contourf(X*1e3, Y*1e3, E_y, levels=20, cmap='RdBu')
    ax2.set_xlabel('x (mm)')
    ax2.set_ylabel('y (mm)')
    ax2.set_title('TE₁₀ 模式 E_y 分布')
    plt.colorbar(im, ax=ax2)

    # 3. 多模式截止频率
    ax3 = axes[0, 2]
    modes = []
    f_cutoffs = []

    for m in range(4):
        for n in range(3):
            if m == 0 and n == 0:
                continue
            f_c_mn = cutoff_frequency_rectangular(a, b, m, n)
            modes.append(f'TE/TM_{m}{n}')
            f_cutoffs.append(f_c_mn / 1e9)

    # 排序
    sorted_pairs = sorted(zip(f_cutoffs, modes))
    f_cutoffs, modes = zip(*sorted_pairs[:8])

    ax3.barh(range(len(modes)), f_cutoffs, alpha=0.7)
    ax3.set_yticks(range(len(modes)))
    ax3.set_yticklabels(modes)
    ax3.set_xlabel('截止频率 (GHz)')
    ax3.set_title('矩形波导模式')
    ax3.grid(True, alpha=0.3)

    # 4. 波导波长
    ax4 = axes[1, 0]
    wavelength = np.linspace(0.5, 0.99, 100) * (2*a)  # 小于截止波长
    wavelength_c = 2 * a

    lambda_g = [guide_wavelength(lam, wavelength_c) for lam in wavelength]

    ax4.plot(wavelength/wavelength_c, np.array(lambda_g)/wavelength_c, 'b-', linewidth=2)
    ax4.set_xlabel('λ/λ_c')
    ax4.set_ylabel('λ_g/λ_c')
    ax4.set_title('波导波长')
    ax4.grid(True, alpha=0.3)
    ax4.set_xlim(0.5, 1)
    ax4.set_ylim(0, 5)

    # 5. 衰减
    ax5 = axes[1, 1]
    sigma_cu = 5.8e7  # 铜电导率
    f_range = np.linspace(1.1 * f_c, 3 * f_c, 100)

    alpha = [attenuation_te10(a, b, fi, sigma_cu) for fi in f_range]

    ax5.semilogy(f_range/1e9, alpha, 'b-', linewidth=2)
    ax5.set_xlabel('频率 (GHz)')
    ax5.set_ylabel('衰减常数 (Np/m)')
    ax5.set_title('TE₁₀ 模式损耗')
    ax5.grid(True, alpha=0.3)

    # 6. 谐振腔Q因子
    ax6 = axes[1, 2]
    d_range = np.linspace(0.5, 3, 50) * a

    # 简化的Q计算 (实际需要更复杂的分析)
    Q_values = []
    for d in d_range:
        f_res = resonant_frequency_rectangular(a, b, d, 1, 0, 1)
        delta = skin_depth(f_res, sigma_cu)
        # 简化估算: Q ≈ 体积/(表面积×δ)
        volume = a * b * d
        surface = 2 * (a*b + b*d + a*d)
        Q_approx = volume / (surface * delta) * 2
        Q_values.append(Q_approx)

    ax6.plot(d_range/a, Q_values, 'g-', linewidth=2)
    ax6.set_xlabel('d/a')
    ax6.set_ylabel('Q')
    ax6.set_title('矩形腔 TE₁₀₁ 品质因子')
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('waveguides.png', dpi=150)
    print("图像已保存为 waveguides.png")
    plt.show()


# =============================================================================
# 验证函数
# =============================================================================
def verify():
    """
    验证所有波导与谐振腔练习
    Verify all waveguide and cavity exercises

    验证内容 Verification:
        9.1 矩形波导截止频率
        9.2 波导波长计算
        9.3 相速度和群速度关系
        9.4 圆形波导
        9.5 谐振腔共振频率
        9.6 趋肤深度和导体损耗
    """
    all_passed = True

    # WR-90 波导参数（X波段标准波导）
    a = 22.86e-3  # m (宽边)
    b = 10.16e-3  # m (窄边)

    # 验证 9.1: 截止频率
    # Check 9.1: Cutoff frequency
    f_c = cutoff_frequency_rectangular(a, b, 1, 0)
    expected_fc = c / (2 * a)
    if not np.isclose(f_c, expected_fc, rtol=0.01):
        print("❌ 9.1 截止频率错误")
        print("   提示: f_c(TE₁₀) = c/(2a)")
        all_passed = False
    else:
        print(f"✓ 9.1 截止频率正确 (f_c(TE₁₀) = {f_c/1e9:.2f} GHz)")

    # 验证 9.2: 波导波长
    # Check 9.2: Guide wavelength
    wavelength = c / (1.5 * f_c)  # 工作在1.5倍截止频率
    wavelength_c = c / f_c
    lambda_g = guide_wavelength(wavelength, wavelength_c)

    expected_lambda_g = wavelength / np.sqrt(1 - (wavelength/wavelength_c)**2)
    if not np.isclose(lambda_g, expected_lambda_g, rtol=0.01):
        print("❌ 9.2 波导波长错误")
        print("   提示: λ_g = λ/√(1 - (λ/λ_c)²)")
        all_passed = False
    else:
        print(f"✓ 9.2 波导波长正确 (λ_g = {lambda_g*1e3:.1f} mm)")

    # 验证 9.3: 相速度和群速度
    # Check 9.3: Phase and group velocity
    f = 1.5 * f_c
    v_p = phase_velocity(f, f_c)
    v_g = group_velocity(f, f_c)

    if v_p * v_g > c**2 * 1.01 or v_p * v_g < c**2 * 0.99:
        print("❌ 9.3 应满足色散关系 v_p × v_g = c²")
        all_passed = False
    else:
        print(f"✓ 9.3 相速度群速度关系正确 (v_p×v_g/c² = {v_p*v_g/c**2:.3f})")

    # 验证 9.4: 圆形波导
    # Check 9.4: Circular waveguide
    a_circ = 10e-3  # 10mm半径
    f_c_te11 = circular_te11_cutoff(a_circ)
    expected_fc_circ = c * 1.841 / (2 * np.pi * a_circ)

    if not np.isclose(f_c_te11, expected_fc_circ, rtol=0.01):
        print("❌ 9.4 圆波导截止频率错误")
        print("   提示: f_c(TE₁₁) = c×1.841/(2πa)")
        all_passed = False
    else:
        print(f"✓ 9.4 圆波导正确 (f_c(TE₁₁) = {f_c_te11/1e9:.2f} GHz)")

    # 验证 9.5: 谐振腔
    # Check 9.5: Resonant cavity
    d = 30e-3  # 腔长30mm
    f_res = resonant_frequency_rectangular(a, b, d, 1, 0, 1)

    if f_res <= 0:
        print("❌ 9.5 谐振频率应为正值")
        all_passed = False
    else:
        print(f"✓ 9.5 谐振腔正确 (f₁₀₁ = {f_res/1e9:.2f} GHz)")

    # 验证 9.6: 趋肤深度
    # Check 9.6: Skin depth
    sigma_cu = 5.8e7  # 铜的电导率 [S/m]
    f_test = 10e9     # 10 GHz
    delta = skin_depth(f_test, sigma_cu)
    expected_delta = np.sqrt(2 / (2*np.pi*f_test * mu_0 * sigma_cu))

    if not np.isclose(delta, expected_delta, rtol=0.01):
        print("❌ 9.6 趋肤深度错误")
        print("   提示: δ = √(2/(ωμσ))")
        all_passed = False
    else:
        print(f"✓ 9.6 趋肤深度正确 (δ = {delta*1e6:.2f} μm @ 10 GHz)")

    if all_passed:
        print("\n🎉 所有测试通过！正在生成可视化...")
        try:
            plot_waveguides()
        except Exception as ex:
            print(f"可视化生成失败: {ex}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("波导与谐振腔 Waveguides and Cavities")
    print("=" * 50)
    verify()
