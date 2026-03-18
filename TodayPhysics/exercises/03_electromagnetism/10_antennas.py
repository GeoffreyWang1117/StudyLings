"""
天线辐射模式 Antenna Radiation Patterns
难度 Difficulty: ★★★★

学习目标 Learning Objectives:
- 理解天线的辐射原理和方向图 (Understand antenna radiation and patterns)
- 掌握方向性、增益和有效面积的概念 (Master directivity, gain, and effective aperture)
- 分析偶极子、阵列和口径天线 (Analyze dipoles, arrays, and aperture antennas)
- 理解弗里斯传输公式 (Understand Friis transmission equation)

物理背景 Physical Background:
天线是将导波转换为自由空间辐射（或反之）的器件。
加速电荷产生电磁辐射，天线通过控制电流分布来控制辐射方向。
方向性D描述天线将功率集中到特定方向的能力。

核心公式 Key Formulas:
- 赫兹偶极子辐射功率: P = η₀(πI₀dl/λ)²/3
- 赫兹偶极子方向性: D = 1.5 (1.76 dBi)
- 半波偶极子方向性: D = 1.64 (2.15 dBi)
- 半波偶极子辐射电阻: R_r ≈ 73.1 Ω
- 天线增益: G = ηD（η为效率）
- 有效面积: A_e = λ²G/(4π)
- 弗里斯公式: Pr/Pt = GtGr(λ/4πR)²
- 抛物面增益: G = η(πD/λ)²

天线参数 Antenna Parameters:
- 方向性D: 最大辐射强度与平均值之比
- 增益G: 考虑损耗后的方向性
- 波束宽度: 主瓣半功率点之间的角度
- 旁瓣电平: 旁瓣与主瓣之比

单位说明 Units:
- 增益: 无量纲或dBi（相对于各向同性）
- 阻抗: Ω
- 功率: W或dBm
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import c, epsilon_0, mu_0

# I AM NOT DONE

# 自由空间阻抗 Free space impedance
eta_0 = np.sqrt(mu_0 / epsilon_0)  # ≈ 377 Ω

# =============================================================================
# 练习 10.1: 赫兹偶极子
# Exercise 10.1: Hertzian Dipole
# =============================================================================
# 物理背景 Physical Background:
# 赫兹偶极子是最基本的天线模型，长度远小于波长(dl << λ)。
# 它是所有天线分析的基础，方向图呈"甜甜圈"形状。
# 辐射最强在垂直于偶极子的平面上。

def hertzian_dipole_radiation_pattern(theta):
    """
    赫兹偶极子辐射方向图（场强）
    Hertzian dipole radiation pattern

    参数 Parameters:
        theta: 与偶极子轴的夹角 [rad]

    返回 Returns:
        归一化场强 F(θ)

    公式 Formula:
        F(θ) = sin(θ)

    特点: θ=90°时最大，θ=0°和180°时为零
    """
    return np.sin(theta)


def hertzian_dipole_power_pattern(theta):
    """
    功率方向图（归一化）
    Normalized power pattern

    公式 Formula:
        P(θ) = F²(θ) = sin²(θ)
    """
    return np.sin(theta)**2


def hertzian_dipole_radiated_power(I0, dl, f):
    """
    赫兹偶极子辐射功率
    Radiated power of Hertzian dipole

    参数 Parameters:
        I0: 电流幅值 [A]
        dl: 偶极子长度 [m]
        f: 频率 [Hz]

    返回 Returns:
        辐射功率 P [W]

    公式 Formula:
        P = η₀(πI₀dl/λ)²/3

    说明: 短偶极子辐射效率较低
    """
    wavelength = c / f
    k = 2 * np.pi / wavelength
    return eta_0 * (np.pi * I0 * dl / wavelength)**2 / 3


def hertzian_dipole_radiation_resistance(dl, wavelength):
    """
    赫兹偶极子辐射电阻
    Radiation resistance of Hertzian dipole

    参数 Parameters:
        dl: 偶极子长度 [m]
        wavelength: 波长 [m]

    返回 Returns:
        辐射电阻 R_r [Ω]

    公式 Formula:
        R_r = (2π/3) × η₀ × (dl/λ)²

    说明: 电小天线辐射电阻很低，匹配困难
    例如: dl=λ/50 时 R_r ≈ 0.5Ω
    """
    return (2 * np.pi / 3) * eta_0 * (dl / wavelength)**2


def hertzian_dipole_directivity():
    """
    赫兹偶极子方向性
    Directivity of Hertzian dipole

    返回 Returns:
        方向性 D（无量纲）

    数值 Value:
        D = 1.5 = 1.76 dBi

    说明: 所有短偶极子方向性相同，与长度无关
    """
    return 1.5


# =============================================================================
# 练习 10.2: 半波偶极子
# Exercise 10.2: Half-Wave Dipole
# =============================================================================
# 物理背景 Physical Background:
# 半波偶极子是最常用的基准天线，长度为λ/2。
# 电流分布近似正弦，中心馈电处电流最大。
# 输入阻抗接近50-75Ω，便于与传输线匹配。

def half_wave_dipole_pattern(theta):
    """
    半波偶极子辐射方向图
    Half-wave dipole radiation pattern

    参数 Parameters:
        theta: 与偶极子轴的夹角 [rad]

    返回 Returns:
        归一化场强 F(θ)

    公式 Formula:
        F(θ) = cos(π/2 × cos(θ)) / sin(θ)

    特点: 比赫兹偶极子稍窄，主瓣更集中
    """
    # 避免在θ=0和π处的奇点
    theta = np.asarray(theta)
    result = np.zeros_like(theta, dtype=float)

    mask = (np.abs(np.sin(theta)) > 1e-10)
    result[mask] = np.abs(np.cos(np.pi/2 * np.cos(theta[mask])) / np.sin(theta[mask]))

    return result


def half_wave_dipole_radiation_resistance():
    """
    半波偶极子辐射电阻
    Radiation resistance of half-wave dipole

    返回 Returns:
        辐射电阻 R_r [Ω]

    数值 Value:
        R_r ≈ 73.1 Ω

    说明: 这是半波偶极子被广泛使用的原因之一
    便于与50Ω或75Ω同轴电缆匹配
    """
    return 73.1


def half_wave_dipole_input_impedance():
    """
    半波偶极子输入阻抗
    Input impedance of half-wave dipole

    返回 Returns:
        输入阻抗 Z_in [Ω]（复数）

    数值 Value:
        Z_in ≈ 73.1 + j42.5 Ω

    说明: 虚部表示天线略呈感性
    可通过调整长度使虚部为零
    """
    return complex(73.1, 42.5)


def half_wave_dipole_directivity():
    """
    半波偶极子方向性
    Directivity of half-wave dipole

    返回 Returns:
        方向性 D（无量纲）

    数值 Value:
        D ≈ 1.64 = 2.15 dBi

    比较: 比赫兹偶极子(1.5)略高
    """
    return 1.64


def half_wave_dipole_length(f):
    """
    半波偶极子物理长度
    Physical length of half-wave dipole

    参数 Parameters:
        f: 工作频率 [Hz]

    返回 Returns:
        物理长度 L [m]

    公式 Formula:
        L = λ/2 = c/(2f)

    实际应用中通常取 0.95×(λ/2) 以考虑端部效应
    """
    return c / (2 * f)


# =============================================================================
# 练习 10.3: 天线阵列
# Exercise 10.3: Antenna Arrays
# =============================================================================
# 物理背景 Physical Background:
# 天线阵列通过多个天线单元的相干叠加来增强方向性。
# 阵列因子描述了单元布局对方向图的影响。
# 可通过调节各单元的馈电相位实现波束扫描。

def array_factor_uniform(N, d, wavelength, theta, theta_0=0):
    """
    均匀线阵的阵因子
    Array factor of uniform linear array

    参数 Parameters:
        N: 阵元数量
        d: 阵元间距 [m]
        wavelength: 波长 [m]
        theta: 观察角 [rad]
        theta_0: 主波束指向 [rad]

    返回 Returns:
        阵因子 AF（无量纲）

    公式 Formula:
        AF = sin(Nψ/2) / sin(ψ/2)
        ψ = kd(cos(θ) - cos(θ₀))

    特点:
        主瓣方向: θ = θ₀
        主瓣峰值: AF_max = N
        零点: ψ = 2mπ/N (m≠0,N,2N,...)
    """
    k = 2 * np.pi / wavelength
    psi = k * d * (np.cos(theta) - np.cos(theta_0))

    # 避免除零
    eps = 1e-10
    numerator = np.sin(N * psi / 2)
    denominator = np.sin(psi / 2)

    result = np.where(np.abs(denominator) > eps,
                      numerator / denominator,
                      N)  # 在ψ=0处极限值为N
    return np.abs(result)


def array_beam_width(N, d, wavelength):
    """
    均匀阵列的主瓣宽度（近似）
    Approximate beamwidth of uniform array

    参数 Parameters:
        N: 阵元数量
        d: 阵元间距 [m]
        wavelength: 波长 [m]

    返回 Returns:
        半功率波束宽度 HPBW [rad]

    公式 Formula:
        HPBW ≈ 0.886λ/(Nd)（宽边阵列）

    说明: 阵列越大，波束越窄
    """
    return 0.886 * wavelength / (N * d)


def grating_lobe_condition(d, wavelength):
    """
    栅瓣出现条件
    Grating lobe condition

    参数 Parameters:
        d: 阵元间距 [m]
        wavelength: 波长 [m]

    返回 Returns:
        是否会出现栅瓣（布尔值）

    判据 Criterion:
        d > λ 时会出现栅瓣

    说明: 栅瓣是与主瓣幅度相同的副瓣，应避免
    通常选择 d ≤ λ/2 以消除栅瓣
    """
    return d > wavelength


def array_directivity(N, d, wavelength, element_directivity=1.5):
    """
    阵列方向性（简化估算）
    Estimated array directivity

    参数 Parameters:
        N: 阵元数量
        d: 阵元间距 [m]
        wavelength: 波长 [m]
        element_directivity: 单元方向性

    返回 Returns:
        阵列方向性 D（无量纲）

    近似公式:
        D_array ≈ N × D_element（d = λ/2时）

    说明: 理想情况下方向性与阵元数成正比
    """
    # 更精确的估算考虑间距
    if d <= wavelength / 2:
        return N * element_directivity
    else:
        # 考虑栅瓣的影响，方向性降低
        return N * element_directivity * (wavelength / (2 * d))


# =============================================================================
# 练习 10.4: 增益和有效面积
# Exercise 10.4: Gain and Effective Aperture
# =============================================================================
# 物理背景 Physical Background:
# 增益是考虑损耗后的方向性，是天线最重要的参数之一。
# 有效面积将天线与辐射等效为"收集面积"的概念。
# 弗里斯公式是无线链路分析的基础。

def antenna_gain(directivity, efficiency=1.0):
    """
    天线增益
    Antenna gain

    参数 Parameters:
        directivity: 方向性 D
        efficiency: 天线效率 η（0到1）

    返回 Returns:
        增益 G（无量纲）

    公式 Formula:
        G = η × D

    说明: 效率包括欧姆损耗、失配损耗等
    """
    return efficiency * directivity


def gain_dbi(gain_linear):
    """
    增益转换为dBi
    Convert gain to dBi

    参数 Parameters:
        gain_linear: 线性增益（无量纲）

    返回 Returns:
        增益 [dBi]

    公式 Formula:
        G_dBi = 10 log₁₀(G)

    常用值:
        G=1: 0 dBi（各向同性）
        G=1.5: 1.76 dBi（赫兹偶极子）
        G=1.64: 2.15 dBi（半波偶极子）
    """
    return 10 * np.log10(gain_linear)


def effective_aperture(gain, wavelength):
    """
    有效面积（有效孔径）
    Effective aperture

    参数 Parameters:
        gain: 天线增益（无量纲）
        wavelength: 波长 [m]

    返回 Returns:
        有效面积 A_e [m²]

    公式 Formula:
        A_e = λ²G/(4π)

    物理意义: 天线"捕获"入射功率的等效面积
    各向同性天线: A_e = λ²/(4π)
    """
    return wavelength**2 * gain / (4 * np.pi)


def friis_transmission(Pt, Gt, Gr, wavelength, R):
    """
    弗里斯传输公式
    Friis transmission equation

    参数 Parameters:
        Pt: 发射功率 [W]
        Gt: 发射天线增益（无量纲）
        Gr: 接收天线增益（无量纲）
        wavelength: 波长 [m]
        R: 发射与接收天线间距离 [m]

    返回 Returns:
        接收功率 Pr [W]

    公式 Formula:
        Pr = Pt × Gt × Gr × (λ/(4πR))²

    假设: 自由空间传播，极化匹配，阻抗匹配
    """
    return Pt * Gt * Gr * (wavelength / (4 * np.pi * R))**2


def free_space_path_loss_db(f, R):
    """
    自由空间路径损耗
    Free space path loss

    参数 Parameters:
        f: 频率 [Hz]
        R: 距离 [m]

    返回 Returns:
        路径损耗 FSPL [dB]

    公式 Formula:
        FSPL = 20log₁₀(4πR/λ) = 20log₁₀(4πRf/c)

    简化公式（常用）:
        FSPL(dB) = 32.44 + 20log₁₀(f_MHz) + 20log₁₀(R_km)
    """
    wavelength = c / f
    return 20 * np.log10(4 * np.pi * R / wavelength)


# =============================================================================
# 练习 10.5: 喇叭天线
# Exercise 10.5: Horn Antennas
# =============================================================================
# 物理背景 Physical Background:
# 喇叭天线是波导的渐变展开，常用作高增益天线或测量基准。
# 口径场近似均匀分布，方向图是sinc函数形式。
# 效率约50%，常用于反射面天线的馈源。

def horn_antenna_gain(A, wavelength, efficiency=0.5):
    """
    喇叭天线增益
    Horn antenna gain

    参数 Parameters:
        A: 口径面积 [m²]
        wavelength: 波长 [m]
        efficiency: 口径效率（典型0.5-0.6）

    返回 Returns:
        增益 G（无量纲）

    公式 Formula:
        G = η × 4πA/λ²

    说明: 口径效率包括相位误差和照射不均匀的影响
    """
    return efficiency * 4 * np.pi * A / wavelength**2


def horn_antenna_3db_beamwidth(D, wavelength, plane='E'):
    """
    喇叭天线3dB波束宽度
    3dB beamwidth of horn antenna

    参数 Parameters:
        D: 口径尺寸 [m]
        wavelength: 波长 [m]
        plane: 'E'面或'H'面

    返回 Returns:
        波束宽度 [度]

    近似公式:
        E面: θ_3dB ≈ 51λ/D 度
        H面: θ_3dB ≈ 70λ/D 度

    说明: H面波束较宽是因为电场分布呈余弦形状
    """
    if plane == 'E':
        return 51 * wavelength / D
    else:
        return 70 * wavelength / D


def pyramidal_horn_gain(a, b, wavelength):
    """
    角锥喇叭天线增益
    Pyramidal horn antenna gain

    参数 Parameters:
        a: 口径宽度（H面方向）[m]
        b: 口径高度（E面方向）[m]
        wavelength: 波长 [m]

    返回 Returns:
        增益 G（无量纲）

    公式 Formula:
        G ≈ 0.5 × 4π × a × b / λ²

    应用: 微波测量标准天线
    """
    return 0.5 * 4 * np.pi * a * b / wavelength**2


def horn_radiation_pattern(theta, D, wavelength):
    """
    喇叭天线方向图（简化）
    Simplified horn antenna pattern

    参数 Parameters:
        theta: 离轴角 [rad]
        D: 口径尺寸 [m]
        wavelength: 波长 [m]

    返回 Returns:
        归一化场强

    近似:
        对于均匀口径场分布，方向图为sinc函数
        F(θ) = sin(u)/u, u = πDsin(θ)/λ
    """
    k = 2 * np.pi / wavelength
    u = k * D * np.sin(theta) / 2

    result = np.where(np.abs(u) > 1e-10,
                      np.sin(u) / u,
                      1.0)
    return np.abs(result)


# =============================================================================
# 练习 10.6: 抛物面天线
# Exercise 10.6: Parabolic Dish Antennas
# =============================================================================
# 物理背景 Physical Background:
# 抛物面天线利用几何光学原理将平行光聚焦到焦点。
# 是实现高增益的最常用方法，广泛用于卫星通信和射电天文。
# 增益与(D/λ)²成正比，口径越大、频率越高，增益越高。

def parabolic_dish_gain(D, wavelength, efficiency=0.55):
    """
    抛物面天线增益
    Parabolic dish antenna gain

    参数 Parameters:
        D: 口径直径 [m]
        wavelength: 波长 [m]
        efficiency: 口径效率（典型0.5-0.7）

    返回 Returns:
        增益 G（无量纲）

    公式 Formula:
        G = η × (πD/λ)²

    例如: D=1m, f=10GHz(λ=3cm), η=0.55
          G ≈ 6000 ≈ 37.8 dBi
    """
    return efficiency * (np.pi * D / wavelength)**2


def parabolic_dish_beamwidth(D, wavelength):
    """
    抛物面天线3dB波束宽度
    3dB beamwidth of parabolic dish

    参数 Parameters:
        D: 口径直径 [m]
        wavelength: 波长 [m]

    返回 Returns:
        波束宽度 [度]

    公式 Formula:
        θ_3dB ≈ 70λ/D 度

    说明: 天线越大波束越窄，指向精度要求越高
    """
    return 70 * wavelength / D


def parabolic_dish_first_null(D, wavelength):
    """
    第一零点角度
    First null angle

    参数 Parameters:
        D: 口径直径 [m]
        wavelength: 波长 [m]

    返回 Returns:
        第一零点角度 [rad]

    公式 Formula:
        θ_null ≈ 1.22λ/D

    说明: 瑞利判据：两点源可分辨的最小角距离
    """
    return 1.22 * wavelength / D


def cassegrain_antenna_gain(D, d_sub, wavelength, efficiency=0.6):
    """
    卡塞格伦天线增益
    Cassegrain antenna gain

    参数 Parameters:
        D: 主反射面直径 [m]
        d_sub: 副反射面直径 [m]
        wavelength: 波长 [m]
        efficiency: 口径效率

    返回 Returns:
        增益 G（无量纲）

    公式 Formula:
        G = η × (πD/λ)² × (1 - (d_sub/D)²)

    说明: 副反射面遮挡会降低增益和增加旁瓣
    """
    blockage = (d_sub / D)**2  # 遮挡因子
    return efficiency * (np.pi * D / wavelength)**2 * (1 - blockage)


def airy_pattern(theta, D, wavelength):
    """
    圆形口径的艾里图样
    Airy pattern for circular aperture

    参数 Parameters:
        theta: 离轴角 [rad]
        D: 口径直径 [m]
        wavelength: 波长 [m]

    返回 Returns:
        功率方向图（归一化）

    精确公式:
        F(θ) = [2J₁(πDsinθ/λ)/(πDsinθ/λ)]²

    这里使用sinc²近似:
        F(θ) ≈ sinc²(πDsinθ/λ)
    """
    u = np.pi * D * np.sin(theta) / wavelength
    result = np.where(np.abs(u) > 1e-10,
                      (np.sin(u) / u)**2,
                      1.0)
    return result


# =============================================================================
# 可视化
# =============================================================================
def plot_antennas():
    """绘制天线相关图"""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 偶极子方向图比较
    ax1 = axes[0, 0]
    theta = np.linspace(0, np.pi, 200)

    # 极坐标转换
    hertz = hertzian_dipole_power_pattern(theta)
    half_wave = half_wave_dipole_pattern(theta)**2
    half_wave = half_wave / np.max(half_wave)  # 归一化

    ax1.plot(theta * 180/np.pi, hertz, 'b-', label='赫兹偶极子', linewidth=2)
    ax1.plot(theta * 180/np.pi, half_wave, 'r-', label='半波偶极子', linewidth=2)
    ax1.set_xlabel('θ (度)')
    ax1.set_ylabel('归一化功率')
    ax1.set_title('偶极子方向图')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 极坐标方向图
    ax2 = axes[0, 1]
    ax2 = plt.subplot(2, 3, 2, projection='polar')
    theta_polar = np.linspace(0, 2*np.pi, 400)

    # 对称展开
    pattern_hertz = np.sin(theta_polar)**2

    ax2.plot(theta_polar, pattern_hertz, 'b-', linewidth=2)
    ax2.set_title('赫兹偶极子 (极坐标)')

    # 3. 阵列因子
    ax3 = axes[0, 2]
    wavelength = 0.03  # 10 GHz
    d = wavelength / 2

    theta_array = np.linspace(0, np.pi, 500)
    for N in [2, 4, 8, 16]:
        AF = array_factor_uniform(N, d, wavelength, theta_array)
        AF_norm = AF / np.max(AF)
        ax3.plot(theta_array * 180/np.pi, 20*np.log10(AF_norm + 1e-10),
                label=f'N={N}', linewidth=1.5)

    ax3.set_xlabel('θ (度)')
    ax3.set_ylabel('阵因子 (dB)')
    ax3.set_title('均匀线阵')
    ax3.set_ylim(-40, 5)
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 增益vs口径
    ax4 = axes[1, 0]
    D_range = np.linspace(0.5, 10, 100)  # 以波长为单位

    G_dish = [parabolic_dish_gain(d, 1, 0.55) for d in D_range]

    ax4.semilogy(D_range, G_dish, 'b-', linewidth=2)
    ax4.set_xlabel('D/λ')
    ax4.set_ylabel('增益')
    ax4.set_title('抛物面天线增益')
    ax4.grid(True, alpha=0.3)

    # 5. 弗里斯公式
    ax5 = axes[1, 1]
    R = np.logspace(1, 6, 100)  # 10m to 1000km
    wavelength = 0.03  # 10 GHz

    Pt = 1  # 1W
    Gt = Gr = 10  # 10 dBi each

    Pr = [friis_transmission(Pt, Gt, Gr, wavelength, r) for r in R]

    ax5.loglog(R/1000, Pr, 'b-', linewidth=2)
    ax5.set_xlabel('距离 (km)')
    ax5.set_ylabel('接收功率 (W)')
    ax5.set_title('弗里斯传输 (Pt=1W, G=10dBi)')
    ax5.grid(True, alpha=0.3)

    # 6. 抛物面艾里图样
    ax6 = axes[1, 2]
    theta_dish = np.linspace(-10, 10, 500) * np.pi/180  # ±10度

    for D_lambda in [10, 20, 50]:
        pattern = airy_pattern(theta_dish, D_lambda, 1)
        ax6.plot(theta_dish * 180/np.pi, 10*np.log10(pattern + 1e-10),
                label=f'D={D_lambda}λ', linewidth=1.5)

    ax6.set_xlabel('θ (度)')
    ax6.set_ylabel('方向图 (dB)')
    ax6.set_title('抛物面天线方向图')
    ax6.set_ylim(-40, 5)
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('antennas.png', dpi=150)
    print("图像已保存为 antennas.png")
    plt.show()


# =============================================================================
# 验证函数
# =============================================================================
def verify():
    """
    验证所有天线练习
    Verify all antenna exercises

    验证内容 Verification:
        10.1 赫兹偶极子方向性
        10.2 半波偶极子参数
        10.3 天线阵列阵因子
        10.4 有效面积计算
        10.5 喇叭天线增益
        10.6 抛物面天线增益和波束宽度
    """
    all_passed = True

    # 验证 10.1: 赫兹偶极子
    # Check 10.1: Hertzian dipole
    D_hertz = hertzian_dipole_directivity()
    if not np.isclose(D_hertz, 1.5, rtol=0.01):
        print("❌ 10.1 赫兹偶极子方向性错误")
        print("   提示: D = 1.5 = 1.76 dBi")
        all_passed = False
    else:
        print(f"✓ 10.1 赫兹偶极子正确 (D = {D_hertz:.2f} = {gain_dbi(D_hertz):.2f} dBi)")

    # 验证 10.2: 半波偶极子
    # Check 10.2: Half-wave dipole
    D_half = half_wave_dipole_directivity()
    R_r = half_wave_dipole_radiation_resistance()

    if not np.isclose(D_half, 1.64, rtol=0.01):
        print("❌ 10.2 半波偶极子方向性错误")
        print("   提示: D ≈ 1.64 = 2.15 dBi")
        all_passed = False
    elif not np.isclose(R_r, 73.1, rtol=0.01):
        print("❌ 10.2 辐射电阻错误")
        print("   提示: R_r ≈ 73.1 Ω")
        all_passed = False
    else:
        print(f"✓ 10.2 半波偶极子正确 (D = {D_half:.2f}, R_r = {R_r:.1f} Ω)")

    # 验证 10.3: 天线阵列
    # Check 10.3: Antenna array
    N = 8
    d = 0.5  # λ/2
    wavelength = 1

    # 主瓣方向(θ=90°)阵因子应为N
    AF_max = array_factor_uniform(N, d, wavelength, np.pi/2)
    if not np.isclose(AF_max, N, rtol=0.01):
        print("❌ 10.3 阵因子最大值应为N")
        print("   提示: 宽边阵列主瓣方向 AF = N")
        all_passed = False
    else:
        print(f"✓ 10.3 天线阵列正确 (AF_max = {AF_max:.0f})")

    # 验证 10.4: 有效面积
    # Check 10.4: Effective aperture
    G = 10  # 10 dBi
    wavelength = 0.03  # 10 GHz
    A_e = effective_aperture(G, wavelength)
    expected_Ae = wavelength**2 * G / (4 * np.pi)

    if not np.isclose(A_e, expected_Ae, rtol=0.01):
        print("❌ 10.4 有效面积错误")
        print("   提示: A_e = λ²G/(4π)")
        all_passed = False
    else:
        print(f"✓ 10.4 有效面积正确 (A_e = {A_e*1e4:.2f} cm²)")

    # 验证 10.5: 喇叭天线
    # Check 10.5: Horn antenna
    a = 0.1   # 10cm口径
    b = 0.08
    wavelength = 0.03  # 10 GHz
    G_horn = pyramidal_horn_gain(a, b, wavelength)

    if G_horn <= 0:
        print("❌ 10.5 喇叭天线增益应为正")
        all_passed = False
    else:
        print(f"✓ 10.5 喇叭天线正确 (G = {gain_dbi(G_horn):.1f} dBi)")

    # 验证 10.6: 抛物面天线
    # Check 10.6: Parabolic dish
    D = 1  # 1m口径
    wavelength = 0.03  # 10 GHz
    G_dish = parabolic_dish_gain(D, wavelength)
    theta_3db = parabolic_dish_beamwidth(D, wavelength)

    if G_dish <= 0:
        print("❌ 10.6 抛物面增益应为正")
        all_passed = False
    else:
        print(f"✓ 10.6 抛物面天线正确 (G = {gain_dbi(G_dish):.1f} dBi, θ_3dB = {theta_3db:.1f}°)")

    if all_passed:
        print("\n🎉 所有测试通过！正在生成可视化...")
        try:
            plot_antennas()
        except Exception as ex:
            print(f"可视化生成失败: {ex}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("天线辐射模式 Antenna Radiation Patterns")
    print("=" * 50)
    verify()
