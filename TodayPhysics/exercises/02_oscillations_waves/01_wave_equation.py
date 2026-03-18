"""
波动方程与波的叠加 Wave Equation and Superposition
难度 Difficulty: ★★★

学习目标 Learning Objectives:
- 理解波动方程的数学形式及其物理意义
  Understand the mathematical form and physical meaning of wave equation
- 掌握行波和驻波的概念与区别
  Master the concepts of traveling waves and standing waves
- 模拟波的叠加与干涉现象
  Simulate wave superposition and interference phenomena
- 理解拍频和波包的形成机制
  Understand the formation of beats and wave packets

物理背景 Physical Background:
波动是振动在介质中的传播。一维波动方程描述了波动现象的基本规律：
∂²y/∂t² = v² * ∂²y/∂x²
其中 v 是波速，由介质性质决定。

波动的基本参数：
- 振幅 A: 最大位移，单位 m
- 波长 λ: 相邻同相点间距，单位 m
- 频率 f: 每秒振动次数，单位 Hz
- 周期 T = 1/f: 完成一次振动的时间，单位 s
- 波数 k = 2π/λ: 空间角频率，单位 rad/m
- 角频率 ω = 2πf: 时间角频率，单位 rad/s
- 波速 v = λf = ω/k: 波形传播速度，单位 m/s

HINT: 一维波动方程: ∂²y/∂t² = v² * ∂²y/∂x²
HINT: 行波解: y = A*sin(kx - ωt) 其中 v = ω/k
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])

# I AM NOT DONE

# =============================================================================
# 练习 1.1: 行波的基本参数
# Exercise 1.1: Basic Parameters of Traveling Wave
# =============================================================================
"""
物理背景：
正弦行波是最基本的波动形式，其数学表达式为 y = A*sin(kx - ωt)
- 正号 (+kx) 表示沿 x 负方向传播
- 负号 (-ωt) 表示波形随时间向正方向移动

各参数的物理意义：
- 波数 k: 单位长度内的波动相位变化，k = 2π/λ [rad/m]
- 角频率 ω: 单位时间内的相位变化，ω = 2πf [rad/s]
- 波速 v: 等相位点的传播速度，v = λf = ω/k [m/s]
- 周期 T: 波完成一次完整振动的时间，T = 1/f [s]

Physical Background:
A sinusoidal traveling wave has the form y = A*sin(kx - ωt)
The wave speed v = λf = ω/k represents the phase velocity.
"""
# 给定参数 Given parameters
A = 0.1  # 振幅 Amplitude (m)
wavelength = 2.0  # 波长 Wavelength λ (m)
f = 5.0  # 频率 Frequency (Hz)

# TODO: 根据上述公式计算波的基本参数
# TODO: Calculate basic wave parameters using the formulas above
k = None  # 波数 Wave number (rad/m)，公式：k = 2π/λ
omega = None  # 角频率 Angular frequency (rad/s)，公式：ω = 2πf
v_wave = None  # 波速 Wave velocity (m/s)，公式：v = λf 或 v = ω/k
T_period = None  # 周期 Period (s)，公式：T = 1/f


# =============================================================================
# 练习 1.2: 行波函数
# Exercise 1.2: Traveling Wave Function
# =============================================================================
"""
物理背景：
行波（Traveling Wave）是一种波形在空间中传播的波动形式。
波动方程 y = A*sin(kx - ωt) 中：
- 当 t 增加时，需要 x 也增加才能保持相位不变
- 因此这是一列向 +x 方向传播的波
- 若改为 y = A*sin(kx + ωt)，则向 -x 方向传播

任意时刻 t，波形是 x 的正弦函数
任意位置 x，振动是 t 的简谐运动
"""
def traveling_wave(x, t, A, k, omega, direction=1):
    """
    计算行波在位置 x 和时间 t 的位移
    Calculate displacement of traveling wave at position x and time t

    参数 Parameters:
    - x: 位置坐标 Position (m)
    - t: 时间 Time (s)
    - A: 振幅 Amplitude (m)
    - k: 波数 Wave number (rad/m)
    - omega: 角频率 Angular frequency (rad/s)
    - direction: 传播方向 Propagation direction
                 +1 表示向右（+x）传播 rightward
                 -1 表示向左（-x）传播 leftward

    返回 Returns:
    - y: 位移 Displacement (m)

    公式 Formula: y = A * sin(kx - direction*ω*t)
    """
    # TODO: 返回波的位移，使用正弦函数计算
    # TODO: Return wave displacement using sine function
    return A * np.sin(k * x - direction * omega * t)  # 修改这里


# 创建空间和时间网格
x = np.linspace(0, 10, 500)
t_values = np.linspace(0, 1, 100)


# =============================================================================
# 练习 1.3: 驻波
# Exercise 1.3: Standing Wave
# =============================================================================
"""
物理背景：
驻波（Standing Wave）是两列振幅相同、频率相同、传播方向相反的行波叠加形成的。
特点：
- 波节（Node）：振幅始终为零的点，位置满足 sin(kx) = 0，即 x = nλ/2
- 波腹（Antinode）：振幅最大的点，位置满足 |sin(kx)| = 1，即 x = (2n+1)λ/4
- 驻波不传播能量，能量在波节和波腹之间来回转换

数学推导：
y = y_right + y_left
  = A*sin(kx - ωt) + A*sin(kx + ωt)
  = 2A*sin(kx)*cos(ωt)  （利用和差化积公式）

空间因子 sin(kx) 决定各点的振幅分布
时间因子 cos(ωt) 决定所有点同相振动
"""
def standing_wave(x, t, A, k, omega):
    """
    计算驻波在位置 x 和时间 t 的位移
    Calculate displacement of standing wave at position x and time t

    参数 Parameters:
    - x: 位置坐标 Position (m)
    - t: 时间 Time (s)
    - A: 单列行波的振幅 Amplitude of single wave (m)
    - k: 波数 Wave number (rad/m)
    - omega: 角频率 Angular frequency (rad/s)

    返回 Returns:
    - y: 位移 Displacement (m)，最大值为 2A

    公式 Formula: y = 2A * sin(kx) * cos(ωt)
    """
    # TODO: 返回驻波的位移，注意振幅是 2A
    # TODO: Return standing wave displacement, note amplitude is 2A
    return 2 * A * np.sin(k * x) * np.cos(omega * t)  # 修改这里


# =============================================================================
# 练习 1.4: 双波干涉
# Exercise 1.4: Two-Wave Interference
# =============================================================================
"""
物理背景：
波的干涉（Interference）是两列或多列波相遇时，振幅相加形成新波形的现象。
这是波动特有的性质，遵循叠加原理。

干涉类型取决于相位差 φ：
- 相长干涉（Constructive）：φ = 0, 2π, 4π... 合振幅 = 2A
- 相消干涉（Destructive）：φ = π, 3π, 5π... 合振幅 = 0
- 部分干涉：其他相位差，合振幅在 0 到 2A 之间

合成波振幅公式（利用三角恒等式）：
y = y1 + y2 = 2A*cos(φ/2)*sin(kx - ωt + φ/2)
合振幅 = 2A*|cos(φ/2)|
"""
def two_wave_interference(x, t, A, k, omega, phi):
    """
    计算两波干涉结果
    Calculate the result of two-wave interference

    参数 Parameters:
    - x: 位置坐标 Position (m)
    - t: 时间 Time (s)
    - A: 单列波振幅 Amplitude of each wave (m)
    - k: 波数 Wave number (rad/m)
    - omega: 角频率 Angular frequency (rad/s)
    - phi: 两波之间的相位差 Phase difference (rad)

    返回 Returns:
    - y: 合成波位移 Resultant displacement (m)
    """
    y1 = A * np.sin(k * x - omega * t)  # 第一列波 First wave
    y2 = A * np.sin(k * x - omega * t + phi)  # 第二列波（有相位差）Second wave
    # TODO: 返回两波叠加结果（叠加原理）
    # TODO: Return superposition of two waves (superposition principle)
    return y1 + y2  # 修改这里


# 典型相位差情况 Typical phase differences
phi_constructive = 0  # 相长干涉 Constructive interference: φ=0 → 振幅加倍
phi_destructive = np.pi  # 相消干涉 Destructive interference: φ=π → 振幅为零
phi_partial = np.pi / 2  # 部分干涉 Partial interference: φ=π/2 → 振幅为√2 A


# =============================================================================
# 练习 1.5: 拍频现象
# Exercise 1.5: Beat Frequency
# =============================================================================
"""
物理背景：
拍频（Beat）是两列频率接近的波叠加时产生的振幅周期性变化现象。
这在音乐中常用于调音——当两个音叉频率接近时，会听到"嗡嗡"的拍音。

数学分析：
y = y1 + y2 = A*cos(ω1*t) + A*cos(ω2*t)
利用和差化积公式：
y = 2A*cos((ω1-ω2)/2 * t) * cos((ω1+ω2)/2 * t)
     ↑                        ↑
   包络（慢变化）           载波（快变化）

拍频 f_beat = |f1 - f2|
包络振动的频率是拍频的一半，但因为有正负两个峰，
人耳听到的拍音频率等于 |f1 - f2|

应用：调音时使拍频趋近于零即达到同频
"""
# 示例：两个接近 A4 音高的频率
f1 = 440  # Hz (标准 A4 音 Standard A4 pitch)
f2 = 442  # Hz (略高 Slightly higher)
omega1 = 2 * np.pi * f1  # 角频率 ω1 (rad/s)
omega2 = 2 * np.pi * f2  # 角频率 ω2 (rad/s)

# TODO: 计算拍频，公式：f_beat = |f1 - f2|
# TODO: Calculate beat frequency using formula: f_beat = |f1 - f2|
f_beat = None  # 单位 Hz，修改这里


def beat_signal(t, A, omega1, omega2):
    """
    计算拍频信号
    Calculate beat signal

    参数 Parameters:
    - t: 时间 Time (s)
    - A: 单列波振幅 Amplitude of each wave
    - omega1: 第一列波角频率 Angular frequency of wave 1 (rad/s)
    - omega2: 第二列波角频率 Angular frequency of wave 2 (rad/s)

    返回 Returns:
    - y: 合成信号 Resultant signal
    """
    # TODO: 返回两列余弦波的叠加
    # TODO: Return superposition of two cosine waves
    return A * np.cos(omega1 * t) + A * np.cos(omega2 * t)  # 修改这里


# =============================================================================
# 练习 1.6: 波包与群速度
# Exercise 1.6: Wave Packet and Group Velocity
# =============================================================================
"""
物理背景：
波包（Wave Packet）是由多个不同频率的波叠加形成的局域化波动。
在量子力学中，波包用于描述粒子的波动性。

高斯波包是最常见的波包形式：
y = A * exp(-(x-x0)²/(2σ²)) * cos(k0*x - ω0*t)
    ↑                          ↑
  包络（高斯函数）           载波（正弦波）

两种速度：
- 相速度 v_p = ω/k：单一频率波的传播速度（载波速度）
- 群速度 v_g = dω/dk：波包包络的传播速度（能量传播速度）

色散（Dispersion）：当 v_g ≠ v_p 时，波包会在传播中展宽
- 无色散介质：v_g = v_p（如真空中的光）
- 正常色散：v_g < v_p（如玻璃中的可见光）
- 反常色散：v_g > v_p

海森堡不确定性原理：Δx·Δk ≥ 1/2
波包越窄（Δx 小），包含的波数范围越宽（Δk 大）
"""
def gaussian_wave_packet(x, t, A, sigma, k0, omega0, v_g):
    """
    计算高斯波包
    Calculate Gaussian wave packet

    参数 Parameters:
    - x: 位置坐标 Position (m)
    - t: 时间 Time (s)
    - A: 振幅 Amplitude (m)
    - sigma: 波包空间宽度（标准差）Spatial width of packet (m)
    - k0: 中心波数 Central wave number (rad/m)
    - omega0: 中心角频率 Central angular frequency (rad/s)
    - v_g: 群速度 Group velocity (m/s)

    返回 Returns:
    - y: 波包位移 Wave packet displacement (m)
    """
    # 波包中心位置随群速度移动 Packet center moves with group velocity
    x0 = v_g * t
    # 高斯包络 Gaussian envelope
    envelope = np.exp(-(x - x0)**2 / (2 * sigma**2))
    # 载波（正弦调制）Carrier wave
    carrier = np.cos(k0 * x - omega0 * t)
    # TODO: 返回波包 = 包络 × 载波
    # TODO: Return wave packet = envelope × carrier
    return A * envelope * carrier  # 修改这里


# 波包参数 Wave packet parameters
sigma = 1.0  # 波包空间宽度 Packet width (m)
k0 = 2 * np.pi  # 中心波数 Central wave number (rad/m)，对应波长 λ=1m
omega0 = 2 * np.pi * 2  # 中心角频率 Central angular frequency (rad/s)，对应频率 f=2Hz
v_phase = omega0 / k0  # 相速度 Phase velocity (m/s)
v_group = v_phase  # 群速度 Group velocity，无色散介质中 v_g = v_p


# =============================================================================
# 可视化
# =============================================================================
def plot_waves():
    """绘制各种波形"""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    # 确保参数已计算
    if k is None or omega is None:
        print("请先完成参数计算")
        return

    # 1. 行波快照
    ax1 = axes[0, 0]
    for t in [0, T_period/4, T_period/2]:
        y = traveling_wave(x, t, A, k, omega)
        ax1.plot(x, y, label=f't = {t:.3f}s')
    ax1.set_xlabel('x (m)')
    ax1.set_ylabel('y (m)')
    ax1.set_title('行波 Traveling Wave')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 驻波
    ax2 = axes[0, 1]
    for t in [0, T_period/8, T_period/4]:
        y = standing_wave(x, t, A, k, omega)
        ax2.plot(x, y, label=f't = {t:.3f}s')
    ax2.set_xlabel('x (m)')
    ax2.set_ylabel('y (m)')
    ax2.set_title('驻波 Standing Wave')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 干涉 - 相长
    ax3 = axes[0, 2]
    t_snap = 0
    y_sum = two_wave_interference(x, t_snap, A, k, omega, phi_constructive)
    ax3.plot(x, A * np.sin(k * x), 'b--', alpha=0.5, label='Wave 1')
    ax3.plot(x, A * np.sin(k * x + phi_constructive), 'r--', alpha=0.5, label='Wave 2')
    ax3.plot(x, y_sum, 'g-', linewidth=2, label='Sum')
    ax3.set_xlabel('x (m)')
    ax3.set_ylabel('y (m)')
    ax3.set_title('相长干涉 Constructive (φ=0)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 干涉 - 相消
    ax4 = axes[1, 0]
    y_sum = two_wave_interference(x, t_snap, A, k, omega, phi_destructive)
    ax4.plot(x, A * np.sin(k * x), 'b--', alpha=0.5, label='Wave 1')
    ax4.plot(x, A * np.sin(k * x + phi_destructive), 'r--', alpha=0.5, label='Wave 2')
    ax4.plot(x, y_sum, 'g-', linewidth=2, label='Sum')
    ax4.set_xlabel('x (m)')
    ax4.set_ylabel('y (m)')
    ax4.set_title('相消干涉 Destructive (φ=π)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 拍频
    ax5 = axes[1, 1]
    t_beat = np.linspace(0, 1, 5000)
    y_beat = beat_signal(t_beat, 1.0, omega1, omega2)
    ax5.plot(t_beat, y_beat, 'b-', linewidth=0.5)
    # 包络线
    envelope_beat = 2 * np.cos((omega1 - omega2) / 2 * t_beat)
    ax5.plot(t_beat, envelope_beat, 'r--', label='Envelope')
    ax5.plot(t_beat, -envelope_beat, 'r--')
    ax5.set_xlabel('t (s)')
    ax5.set_ylabel('y')
    ax5.set_title(f'拍频 Beat Frequency (f_beat = {f_beat} Hz)' if f_beat else 'Beat')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    ax5.set_xlim(0, 0.5)

    # 6. 波包
    ax6 = axes[1, 2]
    x_packet = np.linspace(-5, 15, 500)
    for t in [0, 1, 2]:
        y = gaussian_wave_packet(x_packet, t, A, sigma, k0, omega0, v_group)
        ax6.plot(x_packet, y, label=f't = {t}s')
    ax6.set_xlabel('x (m)')
    ax6.set_ylabel('y (m)')
    ax6.set_title('高斯波包 Gaussian Wave Packet')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('wave_equation.png', dpi=150)
    print("图像已保存为 wave_equation.png")
    plt.show()


# =============================================================================
# 验证函数 Verification
# =============================================================================
def verify():
    """
    验证所有练习的正确性
    Verify all exercises
    """
    all_passed = True

    # 检查 1.1 - 波动参数 Check wave parameters
    expected_k = 2 * np.pi / wavelength
    expected_omega = 2 * np.pi * f
    expected_v = wavelength * f
    expected_T = 1 / f

    if k is None or omega is None or v_wave is None or T_period is None:
        print("错误 1.1: 波参数未完成，请计算 k, omega, v_wave, T_period")
        all_passed = False
    elif not np.isclose(k, expected_k, rtol=0.01):
        print(f"错误 1.1: 波数计算错误，期望值 {expected_k:.2f} rad/m，你的答案 {k}")
        all_passed = False
    elif not np.isclose(omega, expected_omega, rtol=0.01):
        print(f"错误 1.1: 角频率计算错误，期望值 {expected_omega:.2f} rad/s，你的答案 {omega}")
        all_passed = False
    elif not np.isclose(v_wave, expected_v, rtol=0.01):
        print(f"错误 1.1: 波速计算错误，期望值 {expected_v:.2f} m/s，你的答案 {v_wave}")
        all_passed = False
    else:
        print(f"通过 1.1: 波参数正确 (k={k:.2f} rad/m, ω={omega:.2f} rad/s, v={v_wave:.2f} m/s, T={T_period:.3f} s)")

    # 检查 1.2 - 行波函数 Check traveling wave function
    if k is not None and omega is not None:
        y_test = traveling_wave(0.5, 0.1, A, expected_k, expected_omega)
        y_expected = A * np.sin(expected_k * 0.5 - expected_omega * 0.1)
        if not np.isclose(y_test, y_expected, rtol=0.01):
            print("错误 1.2: 行波函数实现错误，请检查公式 y = A*sin(kx - ωt)")
            all_passed = False
        else:
            print("通过 1.2: 行波函数正确")

    # 检查 1.3 - 驻波函数 Check standing wave function
    if k is not None and omega is not None:
        y_stand = standing_wave(0.5, 0.1, A, expected_k, expected_omega)
        y_expected = 2 * A * np.sin(expected_k * 0.5) * np.cos(expected_omega * 0.1)
        if not np.isclose(y_stand, y_expected, rtol=0.01):
            print("错误 1.3: 驻波函数实现错误，请检查公式 y = 2A*sin(kx)*cos(ωt)")
            all_passed = False
        else:
            print("通过 1.3: 驻波函数正确")

    # 检查 1.4 - 波的干涉 Check wave interference
    if k is not None and omega is not None:
        # 相长干涉：振幅加倍 Constructive: should double amplitude
        y_con = two_wave_interference(0.25, 0, A, expected_k, expected_omega, 0)
        y_single = A * np.sin(expected_k * 0.25)
        if not np.isclose(y_con, 2 * y_single, rtol=0.05):
            print("错误 1.4: 相长干涉实现错误，相位差为0时振幅应加倍")
            all_passed = False
        else:
            # 相消干涉：完全抵消 Destructive: should cancel
            y_des = two_wave_interference(0.25, 0, A, expected_k, expected_omega, np.pi)
            if not np.isclose(y_des, 0, atol=0.01):
                print("错误 1.4: 相消干涉实现错误，相位差为π时振幅应为零")
                all_passed = False
            else:
                print("通过 1.4: 波的干涉正确")

    # 检查 1.5 - 拍频 Check beat frequency
    expected_f_beat = abs(f1 - f2)
    if f_beat is None:
        print("错误 1.5: 拍频未计算，请使用公式 f_beat = |f1 - f2|")
        all_passed = False
    elif not np.isclose(f_beat, expected_f_beat):
        print(f"错误 1.5: 拍频计算错误，期望值 {expected_f_beat} Hz，你的答案 {f_beat} Hz")
        all_passed = False
    else:
        print(f"通过 1.5: 拍频正确 (f_beat = {f_beat} Hz)")

    # 检查 1.6 - 波包 Check wave packet
    x_test = np.linspace(-2, 2, 100)
    y_packet = gaussian_wave_packet(x_test, 0, A, sigma, k0, omega0, v_group)
    # 检查波包形状：中心振幅大于边缘 Check localized shape
    center_idx = len(x_test) // 2
    if np.abs(y_packet[center_idx]) < np.abs(y_packet[0]):
        print("错误 1.6: 波包形状错误，高斯波包应在中心处振幅最大")
        all_passed = False
    else:
        print("通过 1.6: 波包函数正确")

    if all_passed:
        print("\n全部测试通过！正在生成可视化图像...")
        print("All tests passed! Generating visualization...")
        try:
            plot_waves()
        except Exception as e:
            print(f"可视化生成失败 Visualization failed: {e}")

    return all_passed


if __name__ == "__main__":
    print("=" * 60)
    print("波动方程与波的叠加 Wave Equation and Superposition")
    print("=" * 60)
    verify()
