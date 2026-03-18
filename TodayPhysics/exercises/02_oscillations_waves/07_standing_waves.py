"""
驻波与共振 Standing Waves and Resonance
难度 Difficulty: ★★★

学习目标 Learning Objectives:
- 理解驻波的形成条件和特征
  Understand formation conditions and characteristics of standing waves
- 掌握弦和管的各阶振动模式
  Master vibration modes of strings and pipes
- 分析受迫振动的共振现象
  Analyze resonance phenomenon in forced oscillations
- 了解乐器物理学的基础
  Understand basics of musical instrument physics

物理背景 Physical Background:
驻波是两列振幅、频率相同、传播方向相反的行波叠加形成的特殊波动。

驻波特征：
- 节点（Node）：振幅始终为零的位置
- 波腹（Antinode）：振幅最大的位置
- 节点与波腹交替分布，间距为 λ/4
- 所有点同相振动（同时达到最大、同时为零）
- 驻波不传播能量

边界条件：
- 固定端：必为节点（y = 0）
- 自由端：必为波腹（dy/dx = 0）

共振频率（弦）：
f_n = nv/(2L) = (n/2L)√(T/μ), n = 1, 2, 3, ...
其中 T 是张力，μ 是线密度

共振频率（管）：
- 开管：f_n = nv/(2L), n = 1, 2, 3, ...（所有谐波）
- 闭管：f_n = nv/(4L), n = 1, 3, 5, ...（只有奇次谐波）

受迫振动共振：
当驱动频率接近固有频率时，振幅剧增
品质因子 Q = ω₀/γ 表征共振的尖锐程度

HINT: 驻波: y(x,t) = 2A sin(kx) cos(ωt)
HINT: 弦的基频: f₁ = v/(2L) = (1/2L)√(T/μ)
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])

# I AM NOT DONE

# =============================================================================
# 练习 7.1: 弦的振动
# Exercise 7.1: String Vibration
# =============================================================================
def string_wave_speed(T, mu):
    """
    弦波速度 v = √(T/μ)
    T: 张力
    μ: 线密度
    """
    return np.sqrt(T / mu)

def string_harmonic_frequency(n, L, v):
    """
    弦的第n次谐波频率 f_n = nv/(2L)
    """
    return n * v / (2 * L)

def string_harmonic_wavelength(n, L):
    """
    弦的第n次谐波波长 λ_n = 2L/n
    """
    return 2 * L / n


# =============================================================================
# 练习 7.2: 管的振动
# Exercise 7.2: Pipe Vibration
# =============================================================================
def open_pipe_frequencies(L, v, n_max=5):
    """
    开管的谐波频率 f_n = nv/(2L), n = 1,2,3,...
    """
    return [n * v / (2 * L) for n in range(1, n_max + 1)]

def closed_pipe_frequencies(L, v, n_max=5):
    """
    闭管的谐波频率 f_n = nv/(4L), n = 1,3,5,...（只有奇次谐波）
    """
    return [(2*n - 1) * v / (4 * L) for n in range(1, n_max + 1)]


# =============================================================================
# 练习 7.3: 驻波模式
# Exercise 7.3: Standing Wave Patterns
# =============================================================================
def standing_wave(x, t, A, k, omega):
    """
    驻波 y(x,t) = 2A sin(kx) cos(ωt)
    """
    return 2 * A * np.sin(k * x) * np.cos(omega * t)

def node_positions(L, n):
    """
    第n次谐波的节点位置（固定边界）
    """
    wavelength = 2 * L / n
    nodes = [i * wavelength / 2 for i in range(n + 1)]
    return nodes

def antinode_positions(L, n):
    """
    第n次谐波的波腹位置
    """
    wavelength = 2 * L / n
    antinodes = [(i + 0.5) * wavelength / 2 for i in range(n)]
    return [a for a in antinodes if a < L]


# =============================================================================
# 练习 7.4: 共振
# Exercise 7.4: Resonance
# =============================================================================
def resonance_amplitude(A0, omega, omega_0, gamma):
    """
    受迫振动共振幅度
    A = A₀ / √((ω₀² - ω²)² + (γω)²)
    """
    denom = np.sqrt((omega_0**2 - omega**2)**2 + (gamma * omega)**2)
    return A0 / denom

def resonance_frequency(omega_0, gamma):
    """
    共振频率（有阻尼）
    ω_res = √(ω₀² - γ²/2)
    """
    if gamma**2 / 2 > omega_0**2:
        return 0  # 过阻尼
    return np.sqrt(omega_0**2 - gamma**2 / 2)

def quality_factor(omega_0, gamma):
    """
    品质因子 Q = ω₀/γ
    """
    return omega_0 / gamma


# =============================================================================
# 练习 7.5: 拍频
# Exercise 7.5: Beat Frequency
# =============================================================================
def beat_frequency(f1, f2):
    """
    拍频 f_beat = |f₁ - f₂|
    """
    return abs(f1 - f2)

def beat_wave(A, f1, f2, t):
    """
    拍的波形 y = 2A cos(2π(f₁-f₂)t/2) cos(2π(f₁+f₂)t/2)
    """
    f_beat = (f1 - f2) / 2
    f_avg = (f1 + f2) / 2
    return 2 * A * np.cos(2 * np.pi * f_beat * t) * np.cos(2 * np.pi * f_avg * t)


# =============================================================================
# 练习 7.6: 乐器物理
# Exercise 7.6: Musical Instrument Physics
# =============================================================================
def guitar_string_frequency(L, T, mu, fret=0):
    """
    吉他弦频率
    fret: 品位号（每品频率提高半音）
    """
    L_eff = L / (2**(fret/12))  # 有效弦长
    v = string_wave_speed(T, mu)
    return string_harmonic_frequency(1, L_eff, v)

def organ_pipe_length(f, v, pipe_type='open'):
    """
    给定频率的管长
    """
    if pipe_type == 'open':
        return v / (2 * f)
    else:  # closed
        return v / (4 * f)


# =============================================================================
# 可视化
# =============================================================================
def plot_standing_waves():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    L = 1.0  # 弦长
    v = 100  # 波速

    # 1. 驻波模式
    ax1 = axes[0, 0]
    x = np.linspace(0, L, 500)

    for n in range(1, 5):
        f = string_harmonic_frequency(n, L, v)
        k = n * np.pi / L
        y = standing_wave(x, 0, 1, k, 0)  # t=0时
        ax1.plot(x, y + 2*n, label=f'n={n}', linewidth=2)

    ax1.set_xlabel('x (m)')
    ax1.set_ylabel('位移 (偏移显示)')
    ax1.set_title('弦的驻波模式')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 时间演化
    ax2 = axes[0, 1]
    n = 2
    k = n * np.pi / L
    omega = 2 * np.pi * string_harmonic_frequency(n, L, v)
    T = 2 * np.pi / omega

    for i, t_frac in enumerate([0, 0.25, 0.5, 0.75]):
        t = t_frac * T
        y = standing_wave(x, t, 1, k, omega)
        ax2.plot(x, y, label=f't = {t_frac}T', linewidth=2, alpha=0.7)

    ax2.set_xlabel('x (m)')
    ax2.set_ylabel('位移')
    ax2.set_title(f'驻波时间演化 (n={n})')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 共振曲线
    ax3 = axes[0, 2]
    omega_0 = 10
    omega = np.linspace(0.1, 20, 500)

    for Q in [2, 5, 10, 20]:
        gamma = omega_0 / Q
        A = [resonance_amplitude(1, w, omega_0, gamma) for w in omega]
        ax3.plot(omega/omega_0, A, label=f'Q={Q}', linewidth=2)

    ax3.set_xlabel('ω/ω₀')
    ax3.set_ylabel('幅度')
    ax3.set_title('共振曲线')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim(0, 15)

    # 4. 拍
    ax4 = axes[1, 0]
    f1, f2 = 440, 445  # Hz
    t = np.linspace(0, 0.5, 5000)
    y = beat_wave(1, f1, f2, t)

    ax4.plot(t*1000, y, 'b-', linewidth=0.5)
    ax4.set_xlabel('t (ms)')
    ax4.set_ylabel('幅度')
    ax4.set_title(f'拍 (f₁={f1}Hz, f₂={f2}Hz, f_beat={beat_frequency(f1,f2)}Hz)')
    ax4.grid(True, alpha=0.3)

    # 5. 开管vs闭管
    ax5 = axes[1, 1]
    L_pipe = 0.5
    v_sound = 343

    f_open = open_pipe_frequencies(L_pipe, v_sound, 6)
    f_closed = closed_pipe_frequencies(L_pipe, v_sound, 6)

    ax5.bar(np.arange(1, 7) - 0.15, f_open, 0.3, label='开管', alpha=0.7)
    ax5.bar(np.arange(1, 7) + 0.15, f_closed, 0.3, label='闭管', alpha=0.7)
    ax5.set_xlabel('谐波序号')
    ax5.set_ylabel('频率 (Hz)')
    ax5.set_title('开管 vs 闭管谐波')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. 吉他品位
    ax6 = axes[1, 2]
    L_guitar = 0.65  # 吉他有效弦长
    T = 70  # 张力 N
    mu = 0.001  # 线密度 kg/m

    frets = range(13)
    frequencies = [guitar_string_frequency(L_guitar, T, mu, f) for f in frets]

    ax6.bar(frets, frequencies, alpha=0.7)
    ax6.set_xlabel('品位')
    ax6.set_ylabel('频率 (Hz)')
    ax6.set_title('吉他品位频率')
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('standing_waves.png', dpi=150)
    print("图像已保存为 standing_waves.png")
    plt.show()


def verify():
    """
    验证所有练习的正确性
    Verify all exercises
    """
    all_passed = True

    # 检查 7.1 - 弦波速度 Check string wave speed
    v = string_wave_speed(100, 0.01)  # 张力 T=100N, 线密度 μ=0.01 kg/m
    expected_v = 100  # m/s
    if not np.isclose(v, expected_v, rtol=0.01):
        print("错误 7.1: 弦波速度计算错误，请检查公式 v = √(T/μ)")
        all_passed = False
    else:
        print(f"通过 7.1: 弦波速度正确 (T=100N, μ=0.01kg/m → v = {v} m/s)")

    # 检查 7.2 - 管振动 Check pipe vibrations
    f_open = open_pipe_frequencies(1, 343, 3)  # 1m长开管
    f_closed = closed_pipe_frequencies(1, 343, 3)  # 1m长闭管
    if f_open[0] != 2 * f_closed[0]:
        print("错误 7.2: 同长度开管基频应是闭管基频的2倍")
        all_passed = False
    else:
        print("通过 7.2: 管振动正确（开管/闭管基频关系正确）")

    # 检查 7.3 - 驻波节点 Check standing wave nodes
    nodes = node_positions(1, 3)  # 第3次谐波的节点
    if len(nodes) != 4:  # n次谐波有 n+1 个节点
        print("错误 7.3: 节点数目错误，第n次谐波应有n+1个节点")
        all_passed = False
    else:
        print("通过 7.3: 驻波模式正确（节点数正确）")

    # 检查 7.4 - 共振 Check resonance
    omega_res = resonance_frequency(10, 1)  # ω₀=10, γ=1
    if omega_res >= 10:
        print("错误 7.4: 有阻尼共振频率应小于无阻尼固有频率")
        all_passed = False
    else:
        print(f"通过 7.4: 共振正确 (有阻尼共振频率 ω_res = {omega_res:.2f} rad/s)")

    # 检查 7.5 - 拍频 Check beat frequency
    f_beat = beat_frequency(440, 445)  # A4(440Hz)与445Hz
    if f_beat != 5:
        print("错误 7.5: 拍频计算错误，应为 |f₁ - f₂| = 5 Hz")
        all_passed = False
    else:
        print(f"通过 7.5: 拍频正确 (440Hz 与 445Hz 拍频 = {f_beat} Hz)")

    # 检查 7.6 - 乐器物理 Check musical instrument physics
    f12 = guitar_string_frequency(0.65, 70, 0.001, 12)  # 第12品
    f0 = guitar_string_frequency(0.65, 70, 0.001, 0)   # 空弦
    if not np.isclose(f12, 2*f0, rtol=0.01):
        print("错误 7.6: 第12品应产生八度音（频率加倍）")
        all_passed = False
    else:
        print(f"通过 7.6: 乐器物理正确 (第12品 = 2 × 空弦频率，即八度音程)")

    if all_passed:
        print("\n全部测试通过！正在生成可视化图像...")
        print("All tests passed! Generating visualization...")
        try:
            plot_standing_waves()
        except Exception as e:
            print(f"可视化失败 Visualization failed: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("驻波与共振 Standing Waves and Resonance")
    print("=" * 50)
    verify()
