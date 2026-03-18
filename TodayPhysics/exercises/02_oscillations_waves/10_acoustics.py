"""
声学与声波 Acoustics and Sound
难度 Difficulty: ★★★

学习目标 Learning Objectives:
- 理解声波在不同介质中的物理特性
  Understand physical properties of sound waves in different media
- 掌握声压、声强和分贝的换算关系
  Master conversions between sound pressure, intensity, and decibels
- 分析管中驻波和共振现象
  Analyze standing waves and resonance in pipes
- 了解声波衰减机制和混响
  Understand sound attenuation mechanisms and reverberation

物理背景 Physical Background:
声学是研究声波产生、传播和接收的学科，涉及物理、工程和生理学。

声速与介质：
- 气体：v = √(γRT/M)，与温度的平方根成正比
- 液体：v = √(B/ρ)，B 是体积模量
- 固体：v = √(E/ρ)（纵波），E 是杨氏模量

声学测量：
- 声压 p (Pa)：压强偏离平衡值
- 声强 I (W/m²)：单位面积声功率
- 声压级 L_p = 20 log₁₀(p/p₀) dB
- 声强级 L_I = 10 log₁₀(I/I₀) dB

分贝叠加：
两个声源的总声级不是简单相加
L_total = 10 log₁₀(10^(L1/10) + 10^(L2/10)) dB
例：两个相同的 60 dB 声源叠加 → 63 dB

室内声学：
- 混响时间 T₆₀：声级衰减 60 dB 的时间
- Sabine 公式：T₆₀ = 0.161 V/A
  V: 房间体积 (m³)，A: 等效吸声面积 (m²)

HINT: 声速: v = √(B/ρ)（流体中）
HINT: 声强: I = p²/(ρv)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import jv as bessel_j
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import k_B, R

# I AM NOT DONE

# 空气参数（20°C，1atm）
rho_air = 1.2  # kg/m³
v_sound_air = 343  # m/s
gamma_air = 1.4  # 绝热指数

# =============================================================================
# 练习 10.1: 声速
# Exercise 10.1: Speed of Sound
# =============================================================================
def speed_of_sound_gas(gamma, T, M):
    """
    理想气体中的声速
    v = √(γRT/M)

    gamma: 绝热指数
    T: 温度 (K)
    M: 摩尔质量 (kg/mol)
    """
    # TODO: 计算声速
    return np.sqrt(gamma * R * T / M)

def speed_of_sound_solid(E, rho):
    """
    固体中的纵波声速
    v = √(E/ρ)

    E: 杨氏模量
    rho: 密度
    """
    return np.sqrt(E / rho)

def speed_of_sound_liquid(B, rho):
    """
    液体中的声速
    v = √(B/ρ)

    B: 体积模量
    """
    return np.sqrt(B / rho)


# =============================================================================
# 练习 10.2: 声压和声强
# Exercise 10.2: Sound Pressure and Intensity
# =============================================================================
def sound_intensity(p_rms, rho=rho_air, v=v_sound_air):
    """
    声强
    I = p²/(ρv)

    p_rms: 声压有效值 (Pa)
    """
    # TODO: 计算声强
    return p_rms**2 / (rho * v)

def sound_pressure_from_intensity(I, rho=rho_air, v=v_sound_air):
    """
    从声强计算声压
    p = √(Iρv)
    """
    return np.sqrt(I * rho * v)

def particle_velocity(p, rho=rho_air, v=v_sound_air):
    """
    质点振动速度
    u = p/(ρv)
    """
    return p / (rho * v)


# =============================================================================
# 练习 10.3: 分贝和响度
# Exercise 10.3: Decibels and Loudness
# =============================================================================
def intensity_to_dB(I, I_0=1e-12):
    """
    声强级（分贝）
    L_I = 10 log₁₀(I/I₀)

    I_0: 参考声强（听阈）
    """
    return 10 * np.log10(I / I_0)

def dB_to_intensity(L_I, I_0=1e-12):
    """
    从分贝转换为声强
    """
    return I_0 * 10**(L_I / 10)

def pressure_to_dB(p, p_0=2e-5):
    """
    声压级（分贝）
    L_p = 20 log₁₀(p/p₀)
    """
    return 20 * np.log10(p / p_0)

def combine_sound_levels(L1, L2):
    """
    叠加两个声级
    """
    I1 = dB_to_intensity(L1)
    I2 = dB_to_intensity(L2)
    return intensity_to_dB(I1 + I2)


# =============================================================================
# 练习 10.4: 管中驻波
# Exercise 10.4: Standing Waves in Pipes
# =============================================================================
def open_pipe_frequencies(L, v=v_sound_air):
    """
    开管共振频率
    f_n = nv/(2L), n = 1, 2, 3, ...
    """
    return lambda n: n * v / (2 * L)

def closed_pipe_frequencies(L, v=v_sound_air):
    """
    闭管共振频率
    f_n = (2n-1)v/(4L), n = 1, 2, 3, ...
    只有奇次谐波
    """
    return lambda n: (2*n - 1) * v / (4 * L)

def pipe_resonance_wavelengths(L, pipe_type='open'):
    """
    计算前几个共振波长
    """
    wavelengths = []
    for n in range(1, 6):
        if pipe_type == 'open':
            wavelengths.append(2 * L / n)
        else:  # closed
            wavelengths.append(4 * L / (2*n - 1))
    return wavelengths


# =============================================================================
# 练习 10.5: 多普勒效应
# Exercise 10.5: Doppler Effect
# =============================================================================
def doppler_frequency(f_0, v_source, v_observer, v_sound=v_sound_air):
    """
    多普勒频移
    f = f₀ × (v + v_observer)/(v - v_source)

    v_source > 0: 靠近观察者
    v_observer > 0: 靠近声源
    """
    # TODO: 计算多普勒频移
    return f_0 * (v_sound + v_observer) / (v_sound - v_source)

def mach_number(v, v_sound=v_sound_air):
    """
    马赫数
    M = v/v_sound
    """
    return v / v_sound

def mach_cone_angle(M):
    """
    马赫锥半角
    sin(θ) = 1/M
    """
    if M <= 1:
        return np.pi / 2  # 未形成锥
    return np.arcsin(1 / M)


# =============================================================================
# 练习 10.6: 声波衰减
# Exercise 10.6: Sound Attenuation
# =============================================================================
def spherical_spreading(I_0, r):
    """
    球面扩散衰减
    I(r) = I₀ × (r₀/r)²
    假设 r₀ = 1m
    """
    return I_0 / r**2

def absorption_attenuation(I_0, alpha, x):
    """
    吸收衰减
    I(x) = I₀ exp(-αx)

    alpha: 吸收系数 [1/m]
    """
    return I_0 * np.exp(-alpha * x)

def atmospheric_absorption(f, humidity=50, T=293):
    """
    大气吸收系数（简化模型）
    高频衰减更强
    """
    # 简化：α ∝ f²
    alpha_0 = 1e-10  # 参考值
    return alpha_0 * f**2 * (1 + 0.01 * humidity)

def reverberation_time(V, A):
    """
    混响时间（Sabine公式）
    T_60 = 0.161 V/A

    V: 房间体积 (m³)
    A: 总吸收面积 (m²)
    """
    return 0.161 * V / A


# =============================================================================
# 可视化
# =============================================================================
def plot_acoustics():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 声速vs温度
    ax1 = axes[0, 0]
    T = np.linspace(250, 350, 100)
    M_air = 0.029  # kg/mol

    v_air = [speed_of_sound_gas(gamma_air, Ti, M_air) for Ti in T]

    ax1.plot(T - 273.15, v_air, 'b-', linewidth=2)
    ax1.set_xlabel('温度 (°C)')
    ax1.set_ylabel('声速 (m/s)')
    ax1.set_title('空气中的声速')
    ax1.grid(True, alpha=0.3)

    # 2. 声级量表
    ax2 = axes[0, 1]
    sources = ['听阈', '耳语', '正常交谈', '吸尘器', '摇滚音乐会', '喷气发动机']
    levels = [0, 30, 60, 70, 110, 140]

    colors = ['green' if L < 70 else 'orange' if L < 100 else 'red' for L in levels]
    ax2.barh(sources, levels, color=colors)
    ax2.axvline(x=85, color='red', linestyle='--', label='听力损伤阈值')
    ax2.set_xlabel('声级 (dB)')
    ax2.set_title('常见声音的声级')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 管中驻波
    ax3 = axes[0, 2]
    L = 1  # m
    x = np.linspace(0, L, 200)

    # 开管前三个模式
    for n in range(1, 4):
        k = n * np.pi / L
        y = np.sin(k * x) * 0.3 + n
        ax3.plot(x, y, linewidth=2, label=f'n={n}')

    ax3.set_xlabel('位置 x (m)')
    ax3.set_ylabel('模式')
    ax3.set_title('开管驻波模式')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 多普勒效应
    ax4 = axes[1, 0]
    v_source = np.linspace(-100, 100, 100)
    f_0 = 1000

    f_observed = [doppler_frequency(f_0, vs, 0) for vs in v_source]

    ax4.plot(v_source, f_observed, 'b-', linewidth=2)
    ax4.axhline(y=f_0, color='r', linestyle='--', label='f₀')
    ax4.axvline(x=0, color='k', linestyle=':', alpha=0.5)
    ax4.set_xlabel('声源速度 (m/s)')
    ax4.set_ylabel('观测频率 (Hz)')
    ax4.set_title('多普勒效应')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 距离衰减
    ax5 = axes[1, 1]
    r = np.linspace(1, 100, 100)
    I_0 = 1

    I_spread = spherical_spreading(I_0, r)
    I_with_abs = [spherical_spreading(I_0, ri) * np.exp(-0.01 * ri) for ri in r]

    ax5.semilogy(r, I_spread, 'b-', linewidth=2, label='仅扩散')
    ax5.semilogy(r, I_with_abs, 'r-', linewidth=2, label='扩散+吸收')
    ax5.set_xlabel('距离 (m)')
    ax5.set_ylabel('相对声强')
    ax5.set_title('声波衰减')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. 马赫锥
    ax6 = axes[1, 2]

    # 声源轨迹
    t = np.linspace(-2, 2, 100)
    M = 1.5
    x_source = M * v_sound_air * t

    ax6.plot(x_source, np.zeros_like(t), 'b-', linewidth=3, label='超音速物体')

    # 马赫锥
    theta = mach_cone_angle(M)
    for ti in np.linspace(-1, 1, 5):
        x0 = M * v_sound_air * ti
        cone_length = 500
        ax6.plot([x0, x0 - cone_length * np.cos(theta)],
                [0, cone_length * np.sin(theta)], 'r-', alpha=0.5)
        ax6.plot([x0, x0 - cone_length * np.cos(theta)],
                [0, -cone_length * np.sin(theta)], 'r-', alpha=0.5)

    ax6.set_xlim(-600, 600)
    ax6.set_ylim(-400, 400)
    ax6.set_xlabel('x (m)')
    ax6.set_ylabel('y (m)')
    ax6.set_title(f'马赫锥 (M={M})')
    ax6.set_aspect('equal')
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

    # 检查 10.1 - 声速 Check sound speed
    M_air = 0.029  # 空气摩尔质量 kg/mol
    v = speed_of_sound_gas(gamma_air, 293, M_air)  # 20°C = 293K
    if not np.isclose(v, v_sound_air, rtol=0.05):
        print("错误 10.1: 空气声速计算错误，请检查公式 v = √(γRT/M)")
        all_passed = False
    else:
        print(f"通过 10.1: 声速正确 (20°C空气中声速: {v:.1f} m/s)")

    # 检查 10.2 - 声强 Check sound intensity
    p = 1  # 声压 1 Pa
    I = sound_intensity(p)
    expected_I = p**2 / (rho_air * v_sound_air)
    if not np.isclose(I, expected_I, rtol=0.01):
        print("错误 10.2: 声强计算错误，请检查公式 I = p²/(ρv)")
        all_passed = False
    else:
        print(f"通过 10.2: 声压声强关系正确 (1Pa → {I:.2e} W/m²)")

    # 检查 10.3 - 分贝 Check decibels
    L = intensity_to_dB(1e-12)  # 参考声强
    if not np.isclose(L, 0, atol=0.1):
        print("错误 10.3: 参考声强 10⁻¹² W/m² 应对应 0 dB")
        all_passed = False
    else:
        L_60 = intensity_to_dB(1e-6)  # 1 μW/m²
        print(f"通过 10.3: 分贝计算正确 (10⁻⁶ W/m² = {L_60:.0f} dB)")

    # 检查 10.4 - 管驻波 Check pipe standing waves
    L = 0.5  # 管长 0.5 m
    f_open = open_pipe_frequencies(L)  # 返回函数
    f_closed = closed_pipe_frequencies(L)
    if not np.isclose(f_open(1), v_sound_air / (2*L), rtol=0.01):
        print("错误 10.4: 开管基频错误，f₁ = v/(2L)")
        all_passed = False
    else:
        print(f"通过 10.4: 管驻波正确 (L=0.5m 开管基频 = {f_open(1):.1f} Hz)")

    # 检查 10.5 - 多普勒效应 Check Doppler effect
    f_0 = 1000  # 声源频率
    f_approach = doppler_frequency(f_0, 34.3, 0)  # 以 0.1 马赫靠近
    if f_approach <= f_0:
        print("错误 10.5: 声源靠近时观测频率应升高")
        all_passed = False
    else:
        print(f"通过 10.5: 多普勒效应正确 (靠近时: {f_0}Hz → {f_approach:.0f}Hz)")

    # 检查 10.6 - 混响时间 Check reverberation time
    T_60 = reverberation_time(1000, 100)  # V=1000m³, A=100m²
    expected_T = 0.161 * 1000 / 100  # Sabine 公式
    if not np.isclose(T_60, expected_T, rtol=0.01):
        print("错误 10.6: 混响时间计算错误，请检查 Sabine 公式 T₆₀ = 0.161V/A")
        all_passed = False
    else:
        print(f"通过 10.6: 混响时间正确 (V=1000m³, A=100m² → T₆₀ = {T_60:.2f} s)")

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
    print("声学与声波 Acoustics and Sound")
    print("=" * 50)
    verify()
