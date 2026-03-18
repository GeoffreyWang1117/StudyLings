"""
引力波物理 Gravitational Wave Physics
难度 Difficulty: ★★★★★

学习目标 Learning Objectives:
- 理解引力波作为时空涟漪的物理本质
- 掌握引力波的产生机制：四极辐射公式
- 了解引力波探测原理和LIGO/Virgo实验
- 分析双星并合（旋近-并合-铃振）的引力波信号
- 计算啁啾质量和引力波应变

物理背景 Physical Background:
引力波是爱因斯坦在1916年预言的时空涟漪，2015年LIGO首次直接探测到，
这是物理学历史上最重要的发现之一。引力波以光速传播，有两种偏振态
（+和×），携带着关于剧烈天体物理事件的独特信息。

引力波源 Gravitational Wave Sources:
  - 紧密双星系统（如双黑洞、双中子星、黑洞-中子星）
  - 核心坍缩超新星
  - 旋转非对称中子星（脉冲星）
  - 宇宙学背景（原初引力波）

里程碑事件 Milestone Events:
  - GW150914：首次直接探测（双黑洞，约30+30 M_sun）
  - GW170817：首次双中子星并合（多信使天文学的开端）

关键公式 Key Formulas:
  - 引力波应变: h ≈ (4G/c⁴)(M_c/r)(πfM_c G/c³)^(2/3)
  - 啁啾质量: M_c = (m₁m₂)^(3/5)/(m₁+m₂)^(1/5)
  - 频率演化: df/dt = (96/5)π^(8/3)(GM_c/c³)^(5/3) f^(11/3)
  - 四极辐射功率: L_GW = (G/5c⁵)<Q̈_ij Q̈^ij>

单位说明 Units:
  - 应变 Strain: 无量纲 (典型值 ~10⁻²¹)
  - 频率 Frequency: Hz
  - 啁啾质量 Chirp mass: kg 或 M_sun
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import G, c, hbar, M_sun, pc

# I AM NOT DONE

# =============================================================================
# 练习 5.1: 引力波基础
# Exercise 5.1: Gravitational Wave Basics
#
# 物理背景 Physical Background:
# 引力波是时空本身的振动，以光速传播。与电磁波不同，引力波是
# 自旋为2的辐射，具有两个偏振态（+和×），它们使空间在垂直于
# 传播方向的平面上产生"潮汐"形变。
#
# 探测原理 Detection Principle:
# LIGO等探测器使用激光干涉仪测量引力波引起的微小臂长变化。
# 典型应变 h ~ 10⁻²¹，意味着4公里臂长变化仅约10⁻¹⁸米！
# =============================================================================

def gravitational_wave_speed():
    """
    引力波传播速度
    Gravitational wave propagation speed

    返回 Returns:
        c: 光速 Speed of light (m/s)

    物理意义 Physical Meaning:
        在广义相对论中，引力波严格以光速传播
        GW170817事件验证了 |v_GW - c|/c < 10⁻¹⁵
    """
    return c


def gravitational_wave_polarizations():
    """
    引力波偏振态
    Gravitational wave polarizations

    返回 Returns:
        偏振态列表 List of polarizations

    物理意义 Physical Meaning:
        + 偏振：沿45°对角线拉伸/压缩
        × 偏振：沿坐标轴拉伸/压缩
        两种偏振相差45°（而非电磁波的90°）
    """
    return ['plus (+)', 'cross (x)']


def strain_plus(h0, omega, t, phi=0):
    """
    计算 + 偏振应变
    Calculate plus polarization strain

    公式 Formula: h_+ = h₀ cos(ωt + φ)

    参数 Parameters:
        h0: 应变幅度 Strain amplitude (无量纲 dimensionless)
        omega: 角频率 Angular frequency (rad/s)
        t: 时间 Time (s)
        phi: 初相位 Initial phase (rad)

    返回 Returns:
        h_plus: + 偏振应变 Plus strain
    """
    return h0 * np.cos(omega * t + phi)


def strain_cross(h0, omega, t, phi=0):
    """
    计算 × 偏振应变
    Calculate cross polarization strain

    公式 Formula: h_× = h₀ sin(ωt + φ)

    参数 Parameters:
        h0: 应变幅度 Strain amplitude
        omega: 角频率 Angular frequency (rad/s)
        t: 时间 Time (s)
        phi: 初相位 Initial phase (rad)

    返回 Returns:
        h_cross: × 偏振应变 Cross strain
    """
    return h0 * np.sin(omega * t + phi)


def arm_length_change(L, h):
    """
    计算干涉仪臂长变化
    Calculate interferometer arm length change

    公式 Formula: ΔL = h × L / 2

    参数 Parameters:
        L: 臂长 Arm length (m)，LIGO为4 km
        h: 应变 Strain (无量纲 dimensionless)

    返回 Returns:
        delta_L: 臂长变化 Arm length change (m)

    物理意义 Physical Meaning:
        h = 10⁻²¹, L = 4 km 时，ΔL ≈ 2×10⁻¹⁸ m
        这比质子直径小1000倍！
    """
    return h * L / 2


def gw_energy_flux(h, f):
    """
    计算引力波能量通量
    Calculate gravitational wave energy flux

    公式 Formula: F = (πc³/4G) × f² × h²

    参数 Parameters:
        h: 应变幅度 Strain amplitude
        f: 频率 Frequency (Hz)

    返回 Returns:
        F: 能量通量 Energy flux (W/m²)
    """
    return np.pi * c**3 / (4 * G) * f**2 * h**2


# =============================================================================
# 练习 5.2: 四极辐射公式
# Exercise 5.2: Quadrupole Radiation Formula
# =============================================================================
def quadrupole_moment_tensor(masses, positions):
    """
    质量四极矩张量
    Q_ij = Σ m(3 x_i x_j - r² δ_ij)
    """
    Q = np.zeros((3, 3))

    for m, r in zip(masses, positions):
        r2 = np.dot(r, r)
        for i in range(3):
            for j in range(3):
                Q[i, j] += m * (3 * r[i] * r[j] - r2 * (1 if i == j else 0))

    return Q


def gw_luminosity_quadrupole(Q_ddot):
    """
    四极辐射功率
    L_GW = (G/5c⁵) × <Q̈_ij Q̈_ij>
    Q_ddot: 四极矩的二阶时间导数
    """
    # 计算迹外部分的平方
    trace_free_sq = np.sum(Q_ddot**2) - (np.trace(Q_ddot)**2) / 3
    return G / (5 * c**5) * trace_free_sq


def gw_strain_quadrupole(Q_ddot, r):
    """
    四极辐射产生的应变（简化）
    h ≈ (2G/c⁴r) × Q̈
    """
    return 2 * G / (c**4 * r) * np.max(np.abs(Q_ddot))


def characteristic_strain(h, f, T):
    """
    特征应变
    h_c = h × √(f × T)
    T: 观测时间或信号持续时间
    """
    return h * np.sqrt(f * T)


# =============================================================================
# 练习 5.3: 双星系统
# Exercise 5.3: Binary Systems
# =============================================================================
def chirp_mass(m1, m2):
    """
    啁啾质量
    M_c = (m1 × m2)^(3/5) / (m1 + m2)^(1/5)
    """
    return (m1 * m2)**(3/5) / (m1 + m2)**(1/5)


def total_mass(m1, m2):
    """总质量"""
    return m1 + m2


def reduced_mass(m1, m2):
    """约化质量"""
    return m1 * m2 / (m1 + m2)


def orbital_frequency(m1, m2, a):
    """
    轨道频率（开普勒）
    f_orb = (1/2π)√(G(m1+m2)/a³)
    """
    return np.sqrt(G * (m1 + m2) / a**3) / (2 * np.pi)


def gw_frequency(f_orbital):
    """
    引力波频率是轨道频率的两倍
    f_GW = 2 × f_orb
    """
    return 2 * f_orbital


def orbital_separation(m1, m2, f_gw):
    """
    从引力波频率计算轨道间距
    a = [(G(m1+m2))/(π f_GW)²]^(1/3)
    """
    f_orb = f_gw / 2
    return (G * (m1 + m2) / (2 * np.pi * f_orb)**2)**(1/3)


# =============================================================================
# 练习 5.4: 并合波形
# Exercise 5.4: Inspiral Waveform
# =============================================================================
def frequency_evolution(f, M_chirp):
    """
    频率演化率
    df/dt = (96/5) π^(8/3) (G M_c/c³)^(5/3) f^(11/3)
    """
    return (96/5) * np.pi**(8/3) * (G * M_chirp / c**3)**(5/3) * f**(11/3)


def time_to_coalescence(f, M_chirp):
    """
    并合时间
    t_c = (5/256) (G M_c/c³)^(-5/3) (πf)^(-8/3)
    """
    return (5/256) * (G * M_chirp / c**3)**(-5/3) * (np.pi * f)**(-8/3)


def strain_amplitude(M_chirp, r, f):
    """
    引力波应变幅度
    h = (4/r) (G M_c/c²)^(5/3) (π f/c)^(2/3)
    """
    return (4/r) * (G * M_chirp / c**2)**(5/3) * (np.pi * f / c)**(2/3)


def inspiral_waveform(t, M_chirp, r, t_coal, phi_0=0):
    """
    旋近阶段波形（简化的Newton级近似）
    """
    tau = t_coal - t
    tau = np.maximum(tau, 1e-10)  # 避免除零

    # 频率演化
    f = (5 / (256 * tau))**(3/8) * (G * M_chirp / c**3)**(-5/8) / np.pi

    # 相位
    phi = phi_0 - 2 * (tau / (5 * G * M_chirp / c**3))**(5/8)

    # 幅度
    h = strain_amplitude(M_chirp, r, f)

    return h * np.cos(2 * np.pi * f * t + phi)


def isco_frequency(M_total):
    """
    最内稳定圆轨道（ISCO）频率
    f_ISCO = c³/(6^(3/2) π G M)
    """
    return c**3 / (6**(3/2) * np.pi * G * M_total)


# =============================================================================
# 练习 5.5: 引力波探测器
# Exercise 5.5: Gravitational Wave Detectors
# =============================================================================
def ligo_arm_length():
    """LIGO臂长"""
    return 4e3  # 4 km


def ligo_design_sensitivity():
    """
    LIGO设计灵敏度
    约 10^-23 Hz^(-1/2) @ 100 Hz
    """
    return 1e-23  # strain/√Hz


def shot_noise_limit(power, wavelength, L):
    """
    散粒噪声极限
    h_shot ∝ √(ℏω/P) / L
    """
    omega = 2 * np.pi * c / wavelength
    return np.sqrt(hbar * omega / power) / L


def seismic_noise_estimate(f, f0=10):
    """
    地震噪声估计（低频）
    h_seismic ∝ f^(-4) for f < f0
    """
    return 1e-18 * (f0/f)**4


def thermal_noise_estimate(f, f0=100):
    """
    热噪声估计
    """
    return 1e-23 * (f0/f)**0.5


def detector_horizon(h_sensitivity, M_chirp, f_peak):
    """
    探测视界距离
    D_horizon = h / h_sensitivity
    """
    h = strain_amplitude(M_chirp, 1, f_peak)  # 1 Mpc处的应变
    return h / h_sensitivity * (1e6 * pc)  # 返回以米为单位


# =============================================================================
# 练习 5.6: 引力波天文学
# Exercise 5.6: Gravitational Wave Astronomy
# =============================================================================
def luminosity_distance_from_strain(h_obs, M_chirp, f):
    """
    从观测应变推断光度距离
    """
    h_1mpc = strain_amplitude(M_chirp, 1e6 * pc, f)
    return h_1mpc / h_obs * (1e6 * pc)


def chirp_mass_from_waveform(f, df_dt):
    """
    从波形推断啁啾质量
    M_c = (c³/G) × (5/(96 π^(8/3)))^(3/5) × f^(-11/5) × (df/dt)^(3/5)
    """
    return (c**3 / G) * (5 / (96 * np.pi**(8/3)))**(3/5) * \
           f**(-11/5) * df_dt**(3/5)


def energy_radiated_inspiral(m1, m2, f_start, f_end):
    """
    旋近阶段辐射的能量（简化）
    E ≈ η M c² (v/c)² / 2
    v/c ∝ f^(2/3)
    """
    M = m1 + m2
    eta = reduced_mass(m1, m2) / M

    v_start = (np.pi * G * M * f_start / c**3)**(1/3) * c
    v_end = (np.pi * G * M * f_end / c**3)**(1/3) * c

    E_start = eta * M * c**2 * (v_start/c)**2 / 2
    E_end = eta * M * c**2 * (v_end/c)**2 / 2

    return E_end - E_start


def gw170817_parameters():
    """
    GW170817（首个中子星并合）参数
    """
    return {
        'chirp_mass': 1.188 * M_sun,
        'total_mass': 2.74 * M_sun,
        'distance': 40 * 1e6 * pc,  # 40 Mpc
        'peak_strain': 1.1e-22
    }


# =============================================================================
# 可视化
# =============================================================================
def plot_gravitational_waves():
    """绘制引力波相关图"""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 偏振模式
    ax1 = axes[0, 0]
    t = np.linspace(0, 4*np.pi, 200)
    h0 = 1
    omega = 1

    h_plus = strain_plus(h0, omega, t)
    h_cross = strain_cross(h0, omega, t)

    ax1.plot(t, h_plus, 'b-', label='h_+', linewidth=2)
    ax1.plot(t, h_cross, 'r-', label='h_×', linewidth=2)
    ax1.set_xlabel('ωt')
    ax1.set_ylabel('h/h₀')
    ax1.set_title('引力波偏振')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 啁啾波形
    ax2 = axes[0, 1]
    m1 = m2 = 30 * M_sun
    M_c = chirp_mass(m1, m2)
    r = 400 * 1e6 * pc  # 400 Mpc

    t_coal = 1  # 秒
    t_wave = np.linspace(0, 0.99*t_coal, 1000)

    h_wave = inspiral_waveform(t_wave, M_c, r, t_coal)

    ax2.plot((t_wave - t_coal) * 1000, h_wave * 1e21, 'b-', linewidth=0.5)
    ax2.set_xlabel('t - t_coal (ms)')
    ax2.set_ylabel('h × 10²¹')
    ax2.set_title('啁啾波形 (30+30 M☉)')
    ax2.grid(True, alpha=0.3)

    # 3. 频率演化
    ax3 = axes[0, 2]
    f_range = np.logspace(0, 3, 100)  # 1 - 1000 Hz

    for m_total in [10, 30, 100]:
        M_c_temp = chirp_mass(m_total/2 * M_sun, m_total/2 * M_sun)
        t_coal = [time_to_coalescence(f, M_c_temp) for f in f_range]
        ax3.loglog(f_range, t_coal, label=f'{m_total} M☉', linewidth=2)

    ax3.set_xlabel('f (Hz)')
    ax3.set_ylabel('并合时间 (s)')
    ax3.set_title('并合时间 vs 频率')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim(1e-3, 1e10)

    # 4. 探测器灵敏度曲线（示意）
    ax4 = axes[1, 0]
    f_det = np.logspace(0, 4, 200)

    # 简化的噪声曲线
    h_noise = np.zeros_like(f_det)
    for i, f in enumerate(f_det):
        seismic = seismic_noise_estimate(f)
        thermal = thermal_noise_estimate(f)
        shot = 1e-23 * (f/100)**0.5
        h_noise[i] = np.sqrt(seismic**2 + thermal**2 + shot**2)

    ax4.loglog(f_det, h_noise, 'b-', linewidth=2)
    ax4.axhline(y=1e-23, color='r', linestyle='--', alpha=0.5, label='设计目标')
    ax4.set_xlabel('f (Hz)')
    ax4.set_ylabel('应变噪声 (1/√Hz)')
    ax4.set_title('探测器灵敏度曲线（示意）')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim(1e-24, 1e-16)

    # 5. 应变 vs 距离
    ax5 = axes[1, 1]
    d_range = np.logspace(1, 4, 100) * 1e6 * pc  # 10 - 10000 Mpc

    f_100 = 100  # Hz
    for m_total in [10, 30, 100]:
        M_c_temp = chirp_mass(m_total/2 * M_sun, m_total/2 * M_sun)
        h_strain = [strain_amplitude(M_c_temp, d, f_100) for d in d_range]
        ax5.loglog(d_range/(1e6*pc), h_strain, label=f'{m_total} M☉', linewidth=2)

    ax5.axhline(y=1e-23, color='k', linestyle='--', alpha=0.5, label='灵敏度')
    ax5.set_xlabel('距离 (Mpc)')
    ax5.set_ylabel('h @ 100 Hz')
    ax5.set_title('应变 vs 距离')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. 轨道衰减
    ax6 = axes[1, 2]
    m1 = m2 = 1.4 * M_sun  # 中子星
    M_c = chirp_mass(m1, m2)

    # 从不同频率开始
    a_range = np.logspace(5, 8, 100)  # 10^5 to 10^8 m

    f_gw = [gw_frequency(orbital_frequency(m1, m2, a)) for a in a_range]
    t_merge = [time_to_coalescence(f, M_c) / (365.25*24*3600) for f in f_gw]  # 年

    ax6.loglog(a_range/1e3, t_merge, 'b-', linewidth=2)
    ax6.set_xlabel('轨道半径 (km)')
    ax6.set_ylabel('并合时间 (年)')
    ax6.set_title('双中子星轨道衰减')
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('gravitational_waves.png', dpi=150)
    print("图像已保存为 gravitational_waves.png")
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

    # 检查 5.1 - 引力波速度 GW speed
    v_gw = gravitational_wave_speed()
    if v_gw != c:
        print("错误 5.1: 引力波速度应精确等于光速")
        all_passed = False
    else:
        print(f"正确 5.1: 引力波速度 (c = {c:.3e} m/s)")

    # 检查 5.2 - 四极辐射 Quadrupole formula
    Q = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]]) * 1e40
    L = gw_luminosity_quadrupole(Q)
    if L <= 0:
        print("错误 5.2: 四极辐射功率应为正值")
        all_passed = False
    else:
        print(f"正确 5.2: 四极辐射公式")

    # 检查 5.3 - 啁啾质量 Chirp mass
    m1 = m2 = 30 * M_sun
    M_c = chirp_mass(m1, m2)
    expected_Mc = (m1 * m2)**(3/5) / (m1 + m2)**(1/5)

    if not np.isclose(M_c, expected_Mc, rtol=0.01):
        print("错误 5.3: 啁啾质量计算不正确，请检查公式 M_c = (m₁m₂)^(3/5)/(m₁+m₂)^(1/5)")
        all_passed = False
    else:
        print(f"正确 5.3: 啁啾质量 (M_c = {M_c/M_sun:.1f} M_sun)")

    # 检查 5.4 - 频率演化 Frequency evolution
    f = 100  # Hz
    df_dt = frequency_evolution(f, M_c)

    if df_dt <= 0:
        print("错误 5.4: 旋近阶段频率应该单调增加")
        all_passed = False
    else:
        print(f"正确 5.4: 频率演化 (df/dt @ 100Hz = {df_dt:.1f} Hz/s)")

    # 检查 5.5 - 探测器 Detector
    h_sens = ligo_design_sensitivity()
    D_horizon = detector_horizon(h_sens, M_c, 100)

    if D_horizon <= 0:
        print("错误 5.5: 探测器视界距离应为正值")
        all_passed = False
    else:
        print(f"正确 5.5: 探测器参数 (视界距离 ~ {D_horizon/pc/1e9:.0f} Gpc)")

    # 检查 5.6 - GW170817事件 GW170817
    params = gw170817_parameters()
    if params['chirp_mass'] / M_sun < 1 or params['chirp_mass'] / M_sun > 2:
        print("错误 5.6: GW170817的啁啾质量应约为1.2 M_sun")
        all_passed = False
    else:
        print(f"正确 5.6: 引力波天文学 (GW170817: M_c = {params['chirp_mass']/M_sun:.3f} M_sun)")

    if all_passed:
        print("\n所有测试通过！正在生成可视化...")
        try:
            plot_gravitational_waves()
        except Exception as ex:
            print(f"可视化生成失败: {ex}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("引力波物理 Gravitational Wave Physics")
    print("=" * 50)
    verify()
