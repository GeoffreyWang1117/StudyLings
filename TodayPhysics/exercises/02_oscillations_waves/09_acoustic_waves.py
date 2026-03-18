"""
声学与声波 Acoustics and Sound Waves
难度 Difficulty: ★★★

学习目标 Learning Objectives:
- 理解声波在不同介质中的传播原理
  Understand sound wave propagation in different media
- 掌握声压、声强和分贝标度的关系
  Master relationships between sound pressure, intensity, and decibels
- 分析管道中的声学共振和驻波
  Analyze acoustic resonance and standing waves in pipes
- 了解多普勒效应和各类声学应用
  Understand Doppler effect and acoustic applications

物理背景 Physical Background:
声波是通过介质传播的机械纵波，需要介质支持（不能在真空中传播）。

声速：
- 理想气体：v = √(γP/ρ) = √(γRT/M)
  γ: 绝热指数，R: 气体常数，T: 温度，M: 摩尔质量
- 空气（20°C）：约 343 m/s
- 水：约 1500 m/s
- 钢：约 5000 m/s

声压与声强：
- 声压 p：压强对平衡值的偏离 (Pa)
- 声强 I：单位面积的声功率 I = p²/(ρv) (W/m²)
- 声压级：L_p = 20 log₁₀(p/p₀) dB，p₀ = 20 μPa（听阈）
- 声强级：L_I = 10 log₁₀(I/I₀) dB，I₀ = 10⁻¹² W/m²

人耳特性：
- 听阈（0 dB）：20 μPa 或 10⁻¹² W/m²
- 痛阈（约120 dB）
- 安全长期暴露限值：约 85 dB

声波衰减：
- 几何扩散：I ∝ 1/r²（点源）
- 大气吸收：I ∝ e^(-αr)，α 与频率相关

HINT: 声速: v = √(B/ρ) 或 √(γP/ρ)
HINT: 声强: I = p²/(ρv)
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import k_B

# I AM NOT DONE

# 标准大气条件
P_atm = 101325  # Pa
rho_air = 1.225  # kg/m³
gamma_air = 1.4

# =============================================================================
# 练习 9.1: 声波基础
# Exercise 9.1: Sound Wave Basics
# =============================================================================
def sound_speed_ideal_gas(gamma, P, rho):
    """
    理想气体中的声速
    v = √(γP/ρ)
    """
    return np.sqrt(gamma * P / rho)

def sound_speed_temperature(T, M=0.029, gamma=1.4):
    """
    声速与温度的关系
    v = √(γRT/M)
    M: 摩尔质量 (空气约29 g/mol)
    """
    R = 8.314  # J/(mol·K)
    return np.sqrt(gamma * R * T / M)

def sound_wavelength(v, f):
    """
    声波波长
    λ = v/f
    """
    return v / f

def sound_intensity(P_rms, rho, v):
    """
    声强
    I = P²/(ρv)
    P_rms: 声压均方根
    """
    return P_rms**2 / (rho * v)


# =============================================================================
# 练习 9.2: 声压级
# Exercise 9.2: Sound Pressure Level
# =============================================================================
def sound_pressure_level(P_rms, P_ref=2e-5):
    """
    声压级 (SPL)
    L_p = 20 log₁₀(P/P_ref) dB
    P_ref = 20 μPa (听阈)
    """
    return 20 * np.log10(P_rms / P_ref)

def sound_intensity_level(I, I_ref=1e-12):
    """
    声强级
    L_I = 10 log₁₀(I/I_ref) dB
    I_ref = 10⁻¹² W/m²
    """
    return 10 * np.log10(I / I_ref)

def decibel_to_pressure(L_p, P_ref=2e-5):
    """
    从分贝转换为声压
    P = P_ref × 10^(L_p/20)
    """
    return P_ref * 10**(L_p / 20)

def combine_sound_levels(L_list):
    """
    组合多个声源的声压级
    L_total = 10 log₁₀(Σ 10^(Lᵢ/10))
    """
    return 10 * np.log10(np.sum(10**(np.array(L_list)/10)))


# =============================================================================
# 练习 9.3: 管道声学
# Exercise 9.3: Pipe Acoustics
# =============================================================================
def open_pipe_frequencies(L, v, n=1):
    """
    开管共振频率
    f_n = nv/(2L), n = 1, 2, 3, ...
    """
    return n * v / (2 * L)

def closed_pipe_frequencies(L, v, n=1):
    """
    闭管共振频率（一端封闭）
    f_n = nv/(4L), n = 1, 3, 5, ... (只有奇数谐波)
    """
    return n * v / (4 * L)

def helmholtz_resonator_frequency(v, A, V, L_neck):
    """
    亥姆霍兹共振器频率
    f = (v/2π)√(A/(V×L_eff))
    A: 颈口面积
    V: 腔体体积
    L_neck: 颈部长度
    """
    L_eff = L_neck + 0.6 * np.sqrt(A / np.pi)  # 端口修正
    return (v / (2 * np.pi)) * np.sqrt(A / (V * L_eff))

def organ_pipe_frequency(L, v, open_ended=True):
    """
    管风琴管频率
    """
    if open_ended:
        return open_pipe_frequencies(L, v, 1)
    return closed_pipe_frequencies(L, v, 1)


# =============================================================================
# 练习 9.4: 多普勒效应
# Exercise 9.4: Doppler Effect
# =============================================================================
def doppler_frequency(f0, v_sound, v_source=0, v_observer=0):
    """
    多普勒效应频率变化
    f = f₀ × (v + v_observer)/(v - v_source)
    正方向: 源向观察者运动
    """
    return f0 * (v_sound + v_observer) / (v_sound - v_source)

def doppler_shift_approaching(f0, v_rel, v_sound):
    """
    接近时的频移
    Δf/f₀ ≈ v_rel/v (低速近似)
    """
    return f0 * v_rel / v_sound

def sonic_boom_angle(v_source, v_sound):
    """
    音锥半角（马赫锥）
    sin(θ) = v_sound/v_source = 1/M
    """
    M = v_source / v_sound
    if M <= 1:
        return np.pi / 2  # 未超音速
    return np.arcsin(1 / M)

def mach_number(v_source, v_sound):
    """
    马赫数
    M = v_source/v_sound
    """
    return v_source / v_sound


# =============================================================================
# 练习 9.5: 声波衰减
# Exercise 9.5: Sound Attenuation
# =============================================================================
def geometric_spreading(I0, r):
    """
    几何扩散衰减（点源）
    I = I₀ × (r₀/r)²
    假设 r₀ = 1 m
    """
    return I0 / r**2

def atmospheric_absorption(I0, alpha, r):
    """
    大气吸收
    I = I₀ exp(-2αr)
    α: 吸收系数 [1/m]
    """
    return I0 * np.exp(-2 * alpha * r)

def absorption_coefficient_frequency(f, humidity=50, T=293):
    """
    吸收系数与频率的关系（简化）
    α ∝ f² (低频) 或 f (高频)
    """
    # 简化模型
    f_kHz = f / 1000
    return 1e-4 * f_kHz**1.5  # Np/m

def sound_transmission_loss(rho1, v1, rho2, v2):
    """
    声透射损耗
    TL = 10 log₁₀(1/τ)
    τ = 4Z₁Z₂/(Z₁+Z₂)²
    """
    Z1, Z2 = rho1 * v1, rho2 * v2
    tau = 4 * Z1 * Z2 / (Z1 + Z2)**2
    return -10 * np.log10(tau)


# =============================================================================
# 练习 9.6: 声学应用
# Exercise 9.6: Acoustic Applications
# =============================================================================
def ultrasound_imaging_depth(f, alpha_tissue=0.5):
    """
    超声成像最大深度
    d_max ≈ 1/(2αf) (往返路径)
    α: 组织吸收系数 [dB/(cm·MHz)]
    """
    # 转换单位：假设需要回波信号衰减<40dB
    max_attenuation_db = 40
    f_MHz = f / 1e6
    return max_attenuation_db / (2 * alpha_tissue * f_MHz) / 100  # m

def sonar_range_equation(P_t, G, sigma, wavelength, S_min):
    """
    主动声呐距离方程（简化）
    R_max = ((P_t × G² × λ² × σ)/(64π³ × S_min))^(1/4)
    """
    numerator = P_t * G**2 * wavelength**2 * sigma
    denominator = 64 * np.pi**3 * S_min
    return (numerator / denominator)**(1/4)

def acoustic_levitation_force(P, rho, v, R):
    """
    声悬浮力（简化）
    F ∝ P²R²/(ρv²)
    """
    return P**2 * R**2 / (rho * v**2)

def noise_reduction_barrier(H, d_s, d_r, wavelength):
    """
    声屏障降噪（简化Maekawa公式）
    ΔL ≈ 10 log₁₀(3 + 20N)
    N: 菲涅尔数 = 2δ/λ
    δ: 路径差
    """
    # 路径差
    delta = np.sqrt(H**2 + d_s**2) + np.sqrt(H**2 + d_r**2) - (d_s + d_r)
    N = 2 * delta / wavelength
    if N < 0:
        return 0
    return 10 * np.log10(3 + 20 * N)


# =============================================================================
# 可视化
# =============================================================================
def plot_acoustics():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 声速与温度
    ax1 = axes[0, 0]
    T = np.linspace(200, 400, 100)

    v = [sound_speed_temperature(t) for t in T]

    ax1.plot(T - 273, v, 'b-', linewidth=2)
    ax1.set_xlabel('温度 (°C)')
    ax1.set_ylabel('声速 (m/s)')
    ax1.set_title('空气中的声速')
    ax1.grid(True, alpha=0.3)

    # 2. 声压级与声压
    ax2 = axes[0, 1]
    L_p = np.linspace(0, 140, 100)

    P = [decibel_to_pressure(l) for l in L_p]

    ax2.semilogy(L_p, P, 'b-', linewidth=2)
    ax2.axvline(x=85, color='r', linestyle='--', alpha=0.5, label='安全上限')
    ax2.axvline(x=120, color='orange', linestyle='--', alpha=0.5, label='疼痛阈值')
    ax2.set_xlabel('声压级 (dB)')
    ax2.set_ylabel('声压 (Pa)')
    ax2.set_title('声压与声压级')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 管道驻波
    ax3 = axes[0, 2]
    x = np.linspace(0, 1, 200)
    L = 1  # m

    for n in [1, 2, 3]:
        # 开管驻波模式
        mode = np.sin(n * np.pi * x / L)
        ax3.plot(x, mode + 2*n, label=f'n = {n}', linewidth=2)

    ax3.set_xlabel('x/L')
    ax3.set_ylabel('位移（偏移显示）')
    ax3.set_title('开管驻波模式')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 多普勒效应
    ax4 = axes[1, 0]
    v_source = np.linspace(-100, 100, 200)
    f0 = 1000  # Hz
    v_sound = 343

    f = [doppler_frequency(f0, v_sound, vs) for vs in v_source]

    ax4.plot(v_source, f, 'b-', linewidth=2)
    ax4.axhline(y=f0, color='r', linestyle='--', alpha=0.5, label='f₀')
    ax4.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    ax4.set_xlabel('声源速度 (m/s, 正=接近)')
    ax4.set_ylabel('观测频率 (Hz)')
    ax4.set_title('多普勒效应')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 声波衰减
    ax5 = axes[1, 1]
    r = np.linspace(1, 100, 100)
    I0 = 1

    I_geo = [geometric_spreading(I0, ri) for ri in r]
    alpha = 0.01  # 1/m
    I_abs = [atmospheric_absorption(I0, alpha, ri) for ri in r]
    I_total = [geometric_spreading(I0, ri) * np.exp(-2*alpha*ri) for ri in r]

    ax5.semilogy(r, I_geo, 'b-', label='几何扩散', linewidth=2)
    ax5.semilogy(r, I_abs, 'r-', label='吸收', linewidth=2)
    ax5.semilogy(r, I_total, 'g--', label='总衰减', linewidth=2)
    ax5.set_xlabel('距离 (m)')
    ax5.set_ylabel('相对强度')
    ax5.set_title('声波衰减')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. 马赫锥
    ax6 = axes[1, 2]
    M = np.linspace(1.01, 5, 100)

    theta = [np.degrees(sonic_boom_angle(m * 343, 343)) for m in M]

    ax6.plot(M, theta, 'b-', linewidth=2)
    ax6.set_xlabel('马赫数')
    ax6.set_ylabel('马赫锥半角 (度)')
    ax6.set_title('超音速马赫锥')
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('acoustics.png', dpi=150)
    print("图像已保存为 acoustics.png")
    plt.show()


def verify():
    """
    验证所有练习的正确性
    Verify all exercises
    """
    all_passed = True

    # 检查 9.1 - 声速 Check sound speed
    v = sound_speed_temperature(293)  # 20°C = 293K
    if not np.isclose(v, 343, rtol=0.02):
        print(f"错误 9.1: 20°C 空气中声速应约 343 m/s，计算得到 {v:.0f} m/s")
        all_passed = False
    else:
        print(f"通过 9.1: 声波基础正确 (20°C空气中声速 v = {v:.0f} m/s)")

    # 检查 9.2 - 声压级 Check sound pressure level
    L_p = sound_pressure_level(2e-5)  # 参考声压（听阈）
    if not np.isclose(L_p, 0, atol=0.1):
        print("错误 9.2: 参考声压 20 μPa 对应的声压级应为 0 dB")
        all_passed = False
    else:
        print(f"通过 9.2: 声压级正确 (听阈声压 20 μPa → L_p = {L_p:.0f} dB)")

    # 检查 9.3 - 管道共振 Check pipe resonance
    L = 0.5  # 管长 0.5 m
    v = 343  # 声速 343 m/s
    f1 = open_pipe_frequencies(L, v, 1)  # 开管基频
    expected = 343  # Hz，即 v/(2L) = 343/(2×0.5) = 343 Hz
    if not np.isclose(f1, expected, rtol=0.01):
        print("错误 9.3: 开管基频计算错误，f₁ = v/(2L)")
        all_passed = False
    else:
        print(f"通过 9.3: 管道声学正确 (L=0.5m 开管基频 f₁ = {f1:.0f} Hz)")

    # 检查 9.4 - 多普勒效应 Check Doppler effect
    f0 = 1000  # 声源频率 1000 Hz
    f_approach = doppler_frequency(f0, 343, v_source=34.3)  # 声源以 0.1 马赫靠近
    if f_approach <= f0:
        print("错误 9.4: 声源靠近时观测频率应升高")
        all_passed = False
    else:
        print(f"通过 9.4: 多普勒效应正确 (靠近时 f = {f_approach:.0f} Hz > {f0} Hz)")

    # 检查 9.5 - 几何扩散 Check geometric spreading
    I = geometric_spreading(1, 10)  # 距离10m处的相对强度
    if not np.isclose(I, 0.01, rtol=0.01):
        print("错误 9.5: 几何扩散衰减错误，I ∝ 1/r² → 10m处为1/100")
        all_passed = False
    else:
        print("通过 9.5: 声波衰减正确（10m处强度衰减为1/100）")

    # 检查 9.6 - 超声成像 Check ultrasound imaging
    depth = ultrasound_imaging_depth(5e6)  # 5 MHz 超声
    if depth <= 0 or depth > 0.5:
        print("错误 9.6: 5MHz超声成像深度应在合理范围（几厘米到十几厘米）")
        all_passed = False
    else:
        print(f"通过 9.6: 声学应用正确 (5MHz超声成像深度约 {depth*100:.0f} cm)")

    if all_passed:
        print("\n全部测试通过！正在生成可视化图像...")
        print("All tests passed! Generating visualization...")
        try:
            plot_acoustics()
        except Exception as e:
            print(f"可视化失败 Visualization failed: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("声学与声波 Acoustics and Sound Waves")
    print("=" * 50)
    verify()
