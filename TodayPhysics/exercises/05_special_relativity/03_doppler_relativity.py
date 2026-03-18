"""
相对论多普勒效应 Relativistic Doppler Effect
难度 Difficulty: ★★★★

学习目标 Learning Objectives:
- 理解相对论多普勒效应的推导和物理本质
  Understand the derivation and physics of relativistic Doppler effect
- 掌握纵向和横向多普勒效应的区别
  Master longitudinal vs transverse Doppler effects
- 分析宇宙学红移与退行速度的关系
  Analyze cosmological redshift and recession velocity
- 应用于光谱分析和雷达/激光测速
  Apply to spectral analysis and radar/lidar speed measurement

物理背景 Physical Background:
相对论多普勒效应与经典多普勒效应有本质区别：
1. 相对论效应包含时间膨胀修正（运动时钟变慢）
2. 存在纯粹的横向多普勒效应（经典理论中不存在）
3. 频率变化取决于相对速度，而非分别对源和观测者的速度

纵向效应 Longitudinal Effect:
- 接近时蓝移: f = f₀√((1+β)/(1-β))，频率增加
- 远离时红移: f = f₀√((1-β)/(1+β))，频率减少

横向效应 Transverse Effect:
- f = f₀/γ，总是红移
- 这是纯粹的时间膨胀效应，经典多普勒没有

宇宙学红移 Cosmological Redshift:
- 红移参数: z = (λ_obs - λ_emit)/λ_emit = λ_obs/λ_emit - 1
- 对于退行源: z = √((1+β)/(1-β)) - 1
- 哈勃定律: v = H₀ × d（退行速度正比于距离）

应用 Applications:
- 天文学：测量恒星和星系的径向速度
- 宇宙学：测量宇宙膨胀速度
- 交通测速：雷达测速枪
- 医学：多普勒超声

单位说明 Units:
- 频率: Hz
- 波长: m 或 nm（可见光常用 nm）
- 红移: 无量纲
- 哈勃常数: km/s/Mpc (约 70 km/s/Mpc)
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import c, h

# I AM NOT DONE

# =============================================================================
# 练习 3.1: 洛伦兹因子与速度参数
# Exercise 3.1: Lorentz Factor and Velocity Parameter
#
# 物理背景：β 和 γ 是相对论中最常用的两个参数。
# β = v/c 是归一化速度，取值范围 0 ≤ β < 1
# γ = 1/√(1-β²) 是洛伦兹因子，取值范围 γ ≥ 1
# =============================================================================

def lorentz_factor(v):
    """
    计算洛伦兹因子 Calculate Lorentz factor

    公式 Formula: γ = 1/√(1 - v²/c²) = 1/√(1 - β²)

    参数 Parameters:
        v: 速度 velocity (m/s)，必须 |v| < c

    返回 Returns:
        gamma: 洛伦兹因子 (无量纲)，γ ≥ 1

    常用值:
    - v = 0.5c → γ ≈ 1.15
    - v = 0.9c → γ ≈ 2.29
    - v = 0.99c → γ ≈ 7.09
    """
    beta = v / c
    if np.any(np.abs(beta) >= 1):
        raise ValueError("速度必须小于光速 Velocity must be less than c")
    # TODO: 计算洛伦兹因子
    gamma = 1 / np.sqrt(1 - beta**2)
    return gamma


def velocity_parameter(v):
    """
    计算速度参数 Calculate velocity parameter

    公式 Formula: β = v/c

    参数 Parameters:
        v: 速度 velocity (m/s)

    返回 Returns:
        beta: 速度参数 (无量纲)，0 ≤ β < 1

    β 是在相对论公式中频繁出现的无量纲参数。
    """
    return v / c


# =============================================================================
# 练习 3.2: 纵向相对论多普勒效应
# Exercise 3.2: Longitudinal Relativistic Doppler Effect
#
# 物理背景：当光源沿视线方向运动时，观测到的频率发生变化。
# 接近时蓝移（频率增加，波长减少），远离时红移（频率减少，波长增加）。
#
# 相对论公式与经典公式的区别：
# - 经典: f = f₀(1 ± v/c)（声波多普勒）
# - 相对论: f = f₀√((1±β)/(1∓β))，包含时间膨胀修正
#
# Physical background: Longitudinal Doppler effect occurs when source
# moves along the line of sight. Approaching causes blueshift, receding redshift.
# =============================================================================

def relativistic_doppler_frequency(f0, v, approaching=True):
    """
    计算纵向相对论多普勒效应（频率）
    Longitudinal relativistic Doppler effect (frequency)

    公式 Formulas:
        接近 (blueshift): f = f₀ √((1+β)/(1-β))
        远离 (redshift):  f = f₀ √((1-β)/(1+β))

    参数 Parameters:
        f0: 光源固有频率 (Hz)，在光源静止参考系中测量
        v: 相对速度 (m/s)
        approaching: True=接近（蓝移），False=远离（红移）

    返回 Returns:
        f: 观测者测量的频率 (Hz)

    物理解释：
    - 接近时 f > f₀（蓝移），光看起来更蓝
    - 远离时 f < f₀（红移），光看起来更红
    """
    beta = v / c
    # TODO: 计算观测频率
    if approaching:
        f = f0 * np.sqrt((1 + beta) / (1 - beta))  # 蓝移
    else:
        f = f0 * np.sqrt((1 - beta) / (1 + beta))  # 红移
    return f


def relativistic_doppler_wavelength(lambda0, v, approaching=True):
    """
    计算纵向相对论多普勒效应（波长）
    Longitudinal relativistic Doppler effect (wavelength)

    公式 Formulas:
        接近 (blueshift): λ = λ₀ √((1-β)/(1+β))，波长变短
        远离 (redshift):  λ = λ₀ √((1+β)/(1-β))，波长变长

    参数 Parameters:
        lambda0: 光源固有波长 (m)
        v: 相对速度 (m/s)
        approaching: True=接近（蓝移），False=远离（红移）

    返回 Returns:
        wavelength: 观测者测量的波长 (m)

    注意：波长和频率的变化方向相反（λf = c）
    """
    beta = v / c
    # TODO: 计算观测波长
    if approaching:
        wavelength = lambda0 * np.sqrt((1 - beta) / (1 + beta))  # 蓝移
    else:
        wavelength = lambda0 * np.sqrt((1 + beta) / (1 - beta))  # 红移
    return wavelength


def classical_doppler_comparison(f0, v, approaching=True):
    """
    经典与相对论多普勒效应比较
    Compare classical vs relativistic Doppler effect

    经典公式 Classical: f = f₀(1 ± v/c)（适用于声波）

    参数 Parameters:
        f0: 源频率 (Hz)
        v: 相对速度 (m/s)
        approaching: True=接近，False=远离

    返回 Returns:
        (f_classical, f_relativistic): 经典和相对论预测的频率

    当 v << c 时，两者近似相等。
    当 v 接近 c 时，差异显著。
    """
    beta = v / c
    if approaching:
        f_classical = f0 * (1 + beta)  # 经典公式
        f_relativistic = relativistic_doppler_frequency(f0, v, True)
    else:
        f_classical = f0 * (1 - beta)
        f_relativistic = relativistic_doppler_frequency(f0, v, False)

    return f_classical, f_relativistic


# =============================================================================
# 练习 3.3: 横向相对论多普勒效应
# Exercise 3.3: Transverse Relativistic Doppler Effect
#
# 物理背景：横向多普勒效应是相对论独有的效应！
# 当光源垂直于视线运动时，经典理论预测没有多普勒频移。
# 但相对论预测有红移，这是纯粹的时间膨胀效应。
#
# 这个效应在1938年由Ives和Stilwell首次实验验证。
#
# Physical background: Transverse Doppler effect is unique to relativity!
# Classical theory predicts no frequency shift for perpendicular motion.
# Relativistic theory predicts redshift due to time dilation.
# =============================================================================

def transverse_doppler_frequency(f0, v):
    """
    计算横向多普勒效应（频率）
    Transverse Doppler effect (frequency)

    公式 Formula: f = f₀ / γ

    参数 Parameters:
        f0: 光源固有频率 (Hz)
        v: 光源速度 (m/s)，垂直于视线方向

    返回 Returns:
        f: 观测频率 (Hz)，总是小于 f₀（红移）

    物理解释：
    - 这是纯粹的时间膨胀效应
    - 运动时钟变慢，所以发出的光频率降低
    - 经典多普勒效应没有横向分量
    - 这是验证狭义相对论的重要实验之一
    """
    gamma = lorentz_factor(v)
    # TODO: 计算频率
    f = f0 / gamma
    return f


def transverse_doppler_wavelength(lambda0, v):
    """
    计算横向多普勒效应（波长）
    Transverse Doppler effect (wavelength)

    公式 Formula: λ = γλ₀

    参数 Parameters:
        lambda0: 光源固有波长 (m)
        v: 光源速度 (m/s)

    返回 Returns:
        wavelength: 观测波长 (m)，总是大于 λ₀（红移）
    """
    gamma = lorentz_factor(v)
    return gamma * lambda0


def general_doppler_angle(f0, v, theta):
    """
    任意角度的相对论多普勒效应
    General relativistic Doppler effect at arbitrary angle

    公式 Formula: f = f₀ / (γ(1 - β cos θ))

    参数 Parameters:
        f0: 光源固有频率 (Hz)
        v: 光源速度 (m/s)
        theta: 光源运动方向与观测方向的夹角 (rad)
               θ = 0: 光源向观测者运动（接近）
               θ = π: 光源远离观测者（远离）
               θ = π/2: 横向运动

    返回 Returns:
        f: 观测频率 (Hz)

    特例验证:
    - θ = 0: f = f₀√((1+β)/(1-β))（纵向接近）
    - θ = π: f = f₀√((1-β)/(1+β))（纵向远离）
    - θ = π/2: f = f₀/γ（横向）
    """
    beta = v / c
    gamma = lorentz_factor(v)
    # TODO: 计算频率
    f = f0 / (gamma * (1 - beta * np.cos(theta)))
    return f


# =============================================================================
# 练习 3.4: 红移参数
# Exercise 3.4: Redshift Parameter
#
# 物理背景：红移参数 z 是天文学中描述多普勒效应的标准量。
# z > 0 表示红移（源远离），z < 0 表示蓝移（源接近）。
# 宇宙中几乎所有星系都有正红移，说明宇宙在膨胀。
#
# Physical background: Redshift parameter z is the standard measure in astronomy.
# z > 0 means redshift (source receding), z < 0 means blueshift (approaching).
# Almost all galaxies show positive z, indicating cosmic expansion.
# =============================================================================

def redshift_from_wavelength(lambda_obs, lambda_emit):
    """
    从观测波长计算红移参数
    Calculate redshift from observed wavelength

    公式 Formula: z = (λ_obs - λ_emit) / λ_emit = λ_obs/λ_emit - 1

    参数 Parameters:
        lambda_obs: 观测波长 (m)
        lambda_emit: 发射波长（固有波长）(m)

    返回 Returns:
        z: 红移参数 (无量纲)

    解释：z = 0 表示无红移，z = 1 表示波长加倍
    """
    # TODO: 计算红移
    z = (lambda_obs - lambda_emit) / lambda_emit
    return z


def redshift_from_frequency(f_obs, f_emit):
    """
    从观测频率计算红移参数
    Calculate redshift from observed frequency

    公式 Formula: z = (f_emit - f_obs) / f_obs = f_emit/f_obs - 1

    参数 Parameters:
        f_obs: 观测频率 (Hz)
        f_emit: 发射频率（固有频率）(Hz)

    返回 Returns:
        z: 红移参数 (无量纲)

    注意：频率公式与波长公式等价（λf = c）
    """
    z = (f_emit - f_obs) / f_obs
    return z


def velocity_from_redshift_relativistic(z):
    """
    从红移计算相对论速度（退行速度）
    Calculate relativistic velocity from redshift

    推导 Derivation:
        1 + z = √((1+β)/(1-β))
        (1+z)² = (1+β)/(1-β)
        β = ((1+z)² - 1) / ((1+z)² + 1)

    参数 Parameters:
        z: 红移参数 (无量纲)

    返回 Returns:
        v: 退行速度 (m/s)

    例如：z = 1 → β ≈ 0.6，z = 2 → β ≈ 0.8
    """
    # TODO: 计算速度
    z_factor = (1 + z)**2
    beta = (z_factor - 1) / (z_factor + 1)
    v = beta * c
    return v


def velocity_from_redshift_classical(z):
    """
    经典近似的红移-速度关系
    Classical approximation for redshift-velocity relation

    公式 Formula: v ≈ zc （仅当 z << 1 时有效）

    参数 Parameters:
        z: 红移参数 (无量纲)

    返回 Returns:
        v: 近似退行速度 (m/s)

    适用范围：z < 0.1 时误差小于 5%
    注意：当 z > 1 时，此公式给出 v > c，物理上无意义
    """
    return z * c


def redshift_from_velocity(v):
    """
    从退行速度计算红移
    Calculate redshift from recession velocity

    公式 Formula: z = √((1+β)/(1-β)) - 1

    参数 Parameters:
        v: 退行速度 (m/s)

    返回 Returns:
        z: 红移参数 (无量纲)

    当 v → c 时，z → ∞
    """
    beta = v / c
    # TODO: 计算红移
    z = np.sqrt((1 + beta) / (1 - beta)) - 1
    return z


# =============================================================================
# 练习 3.5: 宇宙学红移
# Exercise 3.5: Cosmological Redshift
#
# 物理背景：宇宙学红移与普通多普勒红移有本质区别！
# 宇宙学红移是由于宇宙膨胀导致的空间本身的拉伸，而非源的运动。
# 尺度因子 a(t) 描述宇宙的膨胀，a 增大表示宇宙在膨胀。
# 光在传播过程中波长随空间一起被拉伸。
#
# Physical background: Cosmological redshift differs from Doppler redshift!
# It's due to the expansion of space itself, not source motion.
# The scale factor a(t) describes cosmic expansion.
#
# 哈勃定律 Hubble's Law: v = H₀ × d
# 遥远星系的退行速度正比于其距离
# =============================================================================

def cosmological_redshift_scale_factor(z):
    """
    从宇宙学红移计算发射时的尺度因子
    Calculate scale factor at emission from cosmological redshift

    公式 Formula: 1 + z = a₀/a_emit = 1/a_emit (设当前 a₀ = 1)

    参数 Parameters:
        z: 宇宙学红移 (无量纲)

    返回 Returns:
        a_emit: 光发射时的宇宙尺度因子 (无量纲)

    物理意义：
    - z = 1 时，a_emit = 0.5，宇宙当时只有现在的一半大
    - z = 2 时，a_emit = 1/3，宇宙只有现在的三分之一
    - 宇宙微波背景辐射 z ≈ 1089，a_emit ≈ 0.0009
    """
    # TODO: 计算尺度因子
    a_emit = 1 / (1 + z)
    return a_emit


def lookback_time_estimate(z, H0=70):
    """
    估算回望时间（简化模型）
    Estimate lookback time (simplified model)

    简化公式 Simplified: t_lb ≈ z / H₀ (仅对小 z 有效)

    参数 Parameters:
        z: 红移 (无量纲)
        H0: 哈勃常数 (km/s/Mpc)，当前值约 70 km/s/Mpc

    返回 Returns:
        t_lb: 回望时间 (Gyr)，即光传播了多长时间

    注意：精确计算需要宇宙学模型（包含物质、暗能量等）
    """
    # 单位转换: H0 从 km/s/Mpc 转为 1/Gyr
    H0_per_sec = H0 * 1000 / (3.086e22)  # 转换为 1/s
    H0_per_Gyr = H0_per_sec * 3.156e16   # 转换为 1/Gyr

    # TODO: 计算回望时间
    t_lb = z / H0_per_Gyr  # Gyr
    return t_lb


def hubble_recession_velocity(d, H0=70):
    """
    计算哈勃退行速度
    Calculate Hubble recession velocity

    公式 Formula: v = H₀ × d （哈勃定律）

    参数 Parameters:
        d: 距离 (Mpc)，1 Mpc ≈ 3.26 百万光年
        H0: 哈勃常数 (km/s/Mpc)

    返回 Returns:
        v: 退行速度 (km/s)

    例如：d = 100 Mpc → v = 7000 km/s
    注意：当 v > c 时，这表示空间膨胀速度，不是真正的物体运动
    """
    return H0 * d


def hubble_distance(z, H0=70):
    """
    从红移估算距离（非相对论近似）
    Estimate distance from redshift (non-relativistic)

    公式 Formula: d = v/H₀ = zc/H₀

    参数 Parameters:
        z: 红移 (无量纲)
        H0: 哈勃常数 (km/s/Mpc)

    返回 Returns:
        d: 距离 (Mpc)

    注意：此公式仅对 z < 0.1 准确，大红移需要宇宙学模型
    """
    # TODO: 计算距离
    v = velocity_from_redshift_classical(z) / 1000  # 转换为 km/s
    d = v / H0  # Mpc
    return d


# =============================================================================
# 练习 3.6: 光谱线分析
# Exercise 3.6: Spectral Line Analysis
#
# 物理背景：天文光谱学通过识别谱线来确定天体的化学成分和运动状态。
# 每种元素有特定的谱线波长（如氢的巴尔末系）。
# 通过观测波长与静止波长的比较，可以计算红移和退行速度。
#
# Physical background: Astronomical spectroscopy identifies elements and
# measures motion through spectral lines. Each element has characteristic
# wavelengths. Comparing observed vs rest wavelengths gives redshift.
# =============================================================================

# 常见谱线波长 Common spectral line wavelengths (nm)
H_ALPHA = 656.28     # Hα（氢巴尔末α线），红色
H_BETA = 486.13      # Hβ（氢巴尔末β线），蓝绿色
LYMAN_ALPHA = 121.57 # Lyα（氢莱曼α线），远紫外
CA_K = 393.37        # Ca II K线（钙），紫外


def identify_redshifted_line(lambda_obs, rest_wavelengths):
    """
    识别红移后的谱线 Identify redshifted spectral line

    参数 Parameters:
        lambda_obs: 观测波长 (nm)
        rest_wavelengths: 静止波长字典 {'线名': 波长}

    返回 Returns:
        (best_line, best_z): 最可能的谱线名称和对应的红移

    方法：对每条已知谱线计算假设红移，选择最合理的匹配。
    实际应用中需要多条谱线一致确认。
    """
    best_line = None
    best_z = None
    min_diff = float('inf')

    for name, lambda_rest in rest_wavelengths.items():
        z = redshift_from_wavelength(lambda_obs, lambda_rest)
        if z > 0:  # 只考虑红移（大多数天体在远离）
            diff = abs(z)
            if diff < min_diff:
                min_diff = diff
                best_line = name
                best_z = z

    return best_line, best_z


def wavelength_at_redshift(lambda_rest, z):
    """
    计算红移后的波长 Calculate wavelength at given redshift

    公式 Formula: λ_obs = λ_rest × (1 + z)

    参数 Parameters:
        lambda_rest: 静止波长 (任意单位，通常 nm)
        z: 红移参数 (无量纲)

    返回 Returns:
        lambda_obs: 观测波长 (与输入相同单位)

    例如：Hα (656.28 nm) 在 z=1 时变为 1312.56 nm（近红外）
    """
    return lambda_rest * (1 + z)


def spectrum_shift(wavelengths, z):
    """
    将整个光谱红移 Shift entire spectrum by redshift

    参数 Parameters:
        wavelengths: 波长数组 (任意单位)
        z: 红移参数 (无量纲)

    返回 Returns:
        shifted_wavelengths: 红移后的波长数组

    用于模拟不同红移下天体的光谱
    """
    return np.array(wavelengths) * (1 + z)


# =============================================================================
# 练习 3.7: 雷达和激光测速
# Exercise 3.7: Radar and Laser Speed Measurement
#
# 物理背景：雷达测速利用多普勒效应测量目标速度。
# 电磁波发射到目标，反射回来。由于目标运动，往返各有一次多普勒频移。
# 因此总频移是单程的两倍。
#
# 应用：交通测速雷达、飞机雷达、气象雷达、激光测距测速
#
# Physical background: Radar speed measurement uses Doppler effect.
# Signal reflects off target, experiencing Doppler shift twice (round trip).
# =============================================================================

def radar_doppler_shift(f0, v, round_trip=True):
    """
    计算雷达多普勒频移 Calculate radar Doppler shift

    参数 Parameters:
        f0: 发射频率 (Hz)
        v: 目标速度 (m/s)，正值表示接近
        round_trip: 是否往返（True=雷达，False=单程）

    返回 Returns:
        delta_f: 频率偏移 (Hz)

    近似公式（v << c）：
    - 单程: Δf ≈ f₀v/c
    - 往返: Δf ≈ 2f₀v/c

    例如：10 GHz 雷达，目标速度 30 m/s
    Δf ≈ 2×10×10⁹×30/(3×10⁸) = 2000 Hz = 2 kHz
    """
    if round_trip:
        # 相对论精确公式（往返）
        # 信号去程：接近目标（蓝移），返程：目标接近源（再次蓝移）
        f_return = relativistic_doppler_frequency(
            relativistic_doppler_frequency(f0, v, approaching=True),
            v, approaching=True
        )
        return f_return - f0
    else:
        return relativistic_doppler_frequency(f0, v, approaching=True) - f0


def speed_from_radar_shift(f0, delta_f, round_trip=True):
    """
    从雷达频移计算速度 Calculate speed from radar frequency shift

    近似公式 Approximate formula:
    - 往返: v ≈ (Δf × c) / (2f₀)
    - 单程: v ≈ (Δf × c) / f₀

    参数 Parameters:
        f0: 发射频率 (Hz)
        delta_f: 测量到的频移 (Hz)
        round_trip: 是否往返测量

    返回 Returns:
        v: 目标速度 (m/s)

    注意：此公式是非相对论近似，对于日常速度足够精确
    """
    if round_trip:
        # TODO: 计算速度
        v = delta_f * c / (2 * f0)
    else:
        v = delta_f * c / f0
    return v


def lidar_velocity_resolution(wavelength, delta_f):
    """
    计算激光雷达速度分辨率 Calculate LIDAR velocity resolution

    公式 Formula: Δv = (λ × Δf) / 2

    参数 Parameters:
        wavelength: 激光波长 (m)
        delta_f: 频率分辨率 (Hz)

    返回 Returns:
        delta_v: 速度分辨率 (m/s)

    激光雷达（LIDAR）使用激光而非微波，波长更短，精度更高。
    常用于自动驾驶、测绘、大气探测等。
    """
    return wavelength * delta_f / 2


# =============================================================================
# 可视化
# =============================================================================
def plot_relativistic_doppler():
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    # 1. 纵向多普勒效应
    ax1 = axes[0, 0]
    beta_range = np.linspace(0.01, 0.99, 100)
    v_range = beta_range * c

    f_approach = [relativistic_doppler_frequency(1, v, True) for v in v_range]
    f_recede = [relativistic_doppler_frequency(1, v, False) for v in v_range]

    ax1.semilogy(beta_range, f_approach, 'b-', label='Approaching', linewidth=2)
    ax1.semilogy(beta_range, f_recede, 'r-', label='Receding', linewidth=2)
    ax1.axhline(y=1, color='k', linestyle='--', alpha=0.5)
    ax1.set_xlabel('v/c')
    ax1.set_ylabel('f/f₀')
    ax1.set_title('纵向相对论多普勒效应')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 经典vs相对论比较
    ax2 = axes[0, 1]
    for v in v_range:
        f_c, f_r = classical_doppler_comparison(1, v, True)

    f_classical = [1 + beta for beta in beta_range]
    f_rel = [relativistic_doppler_frequency(1, v, True) for v in v_range]

    ax2.plot(beta_range, f_classical, 'r--', label='Classical', linewidth=2)
    ax2.plot(beta_range, f_rel, 'b-', label='Relativistic', linewidth=2)
    ax2.set_xlabel('v/c')
    ax2.set_ylabel('f/f₀ (approaching)')
    ax2.set_title('经典vs相对论多普勒')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 横向多普勒效应
    ax3 = axes[0, 2]
    f_trans = [transverse_doppler_frequency(1, v) for v in v_range]

    ax3.plot(beta_range, f_trans, 'g-', linewidth=2)
    ax3.axhline(y=1, color='k', linestyle='--', alpha=0.5)
    ax3.set_xlabel('v/c')
    ax3.set_ylabel('f/f₀')
    ax3.set_title('横向多普勒效应（时间膨胀）')
    ax3.grid(True, alpha=0.3)

    # 4. 角度依赖
    ax4 = axes[1, 0]
    theta_range = np.linspace(0, np.pi, 100)
    for beta in [0.3, 0.5, 0.7, 0.9]:
        f_theta = [general_doppler_angle(1, beta*c, theta) for theta in theta_range]
        ax4.plot(np.degrees(theta_range), f_theta, label=f'β = {beta}', linewidth=1.5)

    ax4.axhline(y=1, color='k', linestyle='--', alpha=0.5)
    ax4.set_xlabel('Angle θ (degrees)')
    ax4.set_ylabel('f/f₀')
    ax4.set_title('角度依赖的多普勒效应')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 红移-速度关系
    ax5 = axes[1, 1]
    z_range = np.linspace(0, 5, 100)

    v_rel = [velocity_from_redshift_relativistic(z)/c for z in z_range]
    v_class = [velocity_from_redshift_classical(z)/c for z in z_range]

    ax5.plot(z_range, v_rel, 'b-', label='Relativistic', linewidth=2)
    ax5.plot(z_range, v_class, 'r--', label='Classical (v=zc)', linewidth=2)
    ax5.axhline(y=1, color='k', linestyle=':', alpha=0.5, label='c')
    ax5.set_xlabel('Redshift z')
    ax5.set_ylabel('v/c')
    ax5.set_title('红移-速度关系')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. 谱线红移
    ax6 = axes[1, 2]
    z_values = [0, 0.5, 1.0, 2.0]
    colors = ['blue', 'green', 'orange', 'red']

    for z, color in zip(z_values, colors):
        # Hα线
        lambda_shifted = wavelength_at_redshift(H_ALPHA, z)
        ax6.axvline(x=lambda_shifted, color=color, linewidth=2,
                   label=f'z = {z}, λ = {lambda_shifted:.0f} nm')

    ax6.set_xlabel('Wavelength (nm)')
    ax6.set_ylabel('Intensity (a.u.)')
    ax6.set_title('Hα线红移')
    ax6.legend()
    ax6.set_xlim(600, 2000)
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('relativistic_doppler.png', dpi=150)
    print("图像已保存为 relativistic_doppler.png")
    plt.show()


def verify():
    """
    验证所有练习的正确性 Verify all exercises

    检查内容 Checks:
    3.2 纵向多普勒效应
    3.3 横向多普勒效应和角度依赖
    3.4 红移-速度转换自洽性
    3.5 宇宙学红移与尺度因子
    3.6 谱线红移计算
    3.7 雷达测速
    """
    all_passed = True

    # 检查 3.2 - 纵向多普勒
    v = 0.6 * c
    f_approach = relativistic_doppler_frequency(1, v, True)
    beta = 0.6
    expected = np.sqrt((1 + beta) / (1 - beta))
    if not np.isclose(f_approach, expected, rtol=0.01):
        print("错误 3.2 纵向多普勒效应计算错误")
        all_passed = False
    else:
        print(f"通过 3.2 纵向多普勒正确 (v=0.6c 时 f/f₀ = {f_approach:.3f})")

    # 检查 3.3 - 横向多普勒
    f_trans = transverse_doppler_frequency(1, v)
    gamma = lorentz_factor(v)
    expected_trans = 1 / gamma
    if not np.isclose(f_trans, expected_trans, rtol=0.01):
        print("错误 3.3 横向多普勒效应计算错误")
        all_passed = False
    else:
        print(f"通过 3.3 横向多普勒正确 (v=0.6c 时 f/f₀ = {f_trans:.3f})")

    # 检查角度依赖
    f_0 = general_doppler_angle(1, v, 0)  # θ=0 应等于接近（蓝移）
    if not np.isclose(f_0, f_approach, rtol=0.01):
        print("错误 3.3 角度依赖计算错误")
        all_passed = False
    else:
        print("通过 3.3 角度依赖正确 (θ=0 等于纵向接近)")

    # 检查 3.4 - 红移参数
    z = 1.0
    v_from_z = velocity_from_redshift_relativistic(z)
    z_back = redshift_from_velocity(v_from_z)
    if not np.isclose(z_back, z, rtol=0.01):
        print("错误 3.4 红移-速度转换不自洽")
        all_passed = False
    else:
        print(f"通过 3.4 红移参数正确 (z=1 对应 v/c = {v_from_z/c:.3f})")

    # 检查 3.5 - 宇宙学红移
    z_cosmo = 2.0
    a = cosmological_redshift_scale_factor(z_cosmo)
    if not np.isclose(a, 1/3, rtol=0.01):
        print("错误 3.5 宇宙学红移与尺度因子关系错误")
        all_passed = False
    else:
        print(f"通过 3.5 宇宙学红移正确 (z=2 时 a = {a:.3f})")

    # 检查 3.6 - 谱线红移
    lambda_obs = wavelength_at_redshift(H_ALPHA, 1.0)
    expected_lambda = H_ALPHA * 2  # z=1 时波长加倍
    if not np.isclose(lambda_obs, expected_lambda, rtol=0.01):
        print("错误 3.6 谱线红移计算错误")
        all_passed = False
    else:
        print(f"通过 3.6 谱线红移正确 (Hα 在 z=1 时: {lambda_obs:.1f} nm)")

    # 检查 3.7 - 雷达测速
    f0 = 10e9  # 10 GHz
    v_target = 30  # m/s
    delta_f = radar_doppler_shift(f0, v_target, round_trip=True)
    v_measured = speed_from_radar_shift(f0, delta_f, round_trip=True)
    if not np.isclose(v_measured, v_target, rtol=0.05):
        print("错误 3.7 雷达测速计算错误")
        all_passed = False
    else:
        print(f"通过 3.7 雷达测速正确 (30 m/s 目标频移 Δf = {delta_f/1e3:.1f} kHz)")

    if all_passed:
        print("\n所有测试通过！正在生成可视化图像...")
        try:
            plot_relativistic_doppler()
        except Exception as e:
            print(f"可视化生成失败: {e}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("相对论多普勒效应 Relativistic Doppler Effect")
    print("=" * 50)
    verify()
