"""
电路分析 Circuit Analysis
难度 Difficulty: ★★★

学习目标 Learning Objectives:
- 理解基尔霍夫定律的物理本质 (Understand Kirchhoff's laws)
- 分析RC、RL和RLC电路的暂态和稳态响应 (Analyze transient and steady-state response)
- 掌握交流电路的阻抗分析方法 (Master AC circuit impedance analysis)
- 理解共振、品质因子和滤波器设计 (Resonance, Q-factor, filters)

物理背景 Physical Background:
电路分析基于电荷守恒和能量守恒两个基本原理。
基尔霍夫定律是麦克斯韦方程在电路中的应用。

核心公式 Key Formulas:
- 基尔霍夫电流定律 KCL: ΣI = 0 (电荷守恒)
- 基尔霍夫电压定律 KVL: ΣV = 0 (能量守恒)
- RC时间常数: τ = RC [s]
- RL时间常数: τ = L/R [s]
- RLC共振频率: f₀ = 1/(2π√LC) [Hz]
- 品质因子: Q = ω₀L/R = 1/(ω₀RC)
- 复阻抗: Z_C = 1/(jωC), Z_L = jωL

交流电路 AC Circuits:
- 相量法将微分方程转化为代数方程
- 阻抗 Z = R + jX（实部为电阻，虚部为电抗）
- 功率因数: cos(φ)

单位说明 Units:
- 电阻: Ω (欧姆)
- 电容: F (法拉) = C/V = A·s/V
- 电感: H (亨利) = Wb/A = V·s/A
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])

# I AM NOT DONE

# =============================================================================
# 练习 5.1: RC电路
# Exercise 5.1: RC Circuit
# =============================================================================
# 物理背景 Physical Background:
# RC电路是电阻和电容串联的基本电路。
# 电容的"惰性"导致电压不能突变，产生指数型充放电过程。
# 时间常数 τ = RC 表征响应速度。

def rc_charging(V0, R, C, t):
    """
    RC电路充电过程
    RC circuit charging process

    参数 Parameters:
        V0: 电源电压 [V]
        R: 电阻 [Ω]
        C: 电容 [F]
        t: 时间 [s]

    返回 Returns:
        电容电压 V(t) [V]

    公式 Formula:
        V(t) = V₀(1 - e^(-t/τ)), τ = RC

    特征值:
        t = τ: V = 0.632 V₀
        t = 5τ: V ≈ 0.993 V₀（实际视为充满）
    """
    tau = R * C  # 时间常数 Time constant
    # TODO: 计算电压 (Calculate voltage)
    V = V0 * (1 - np.exp(-t / tau))
    return V

def rc_discharging(V0, R, C, t):
    """
    RC电路放电过程
    RC circuit discharging process

    公式 Formula:
        V(t) = V₀ e^(-t/τ)

    电容储能通过电阻消耗
    """
    tau = R * C
    V = V0 * np.exp(-t / tau)
    return V

def rc_time_constant(R, C):
    """
    时间常数 τ = RC [s]
    Time constant

    物理意义: τ越大，充放电越慢
    """
    return R * C


# =============================================================================
# 练习 5.2: RL电路
# Exercise 5.2: RL Circuit
# =============================================================================
# 物理背景 Physical Background:
# RL电路是电阻和电感串联的基本电路。
# 电感反抗电流变化，时间常数 τ = L/R。
# 与RC电路对偶：RC中电压不能突变，RL中电流不能突变。

def rl_current_rise(V0, R, L, t):
    """
    RL电路电流上升过程
    RL circuit current rise

    参数 Parameters:
        V0: 电源电压 [V]
        R: 电阻 [Ω]
        L: 电感 [H]
        t: 时间 [s]

    返回 Returns:
        电流 I(t) [A]

    公式 Formula:
        I(t) = (V₀/R)(1 - e^(-t/τ)), τ = L/R
    """
    tau = L / R  # 时间常数 Time constant
    # TODO: 计算电流 (Calculate current)
    I = (V0 / R) * (1 - np.exp(-t / tau))
    return I

def rl_current_decay(I0, R, L, t):
    """
    RL电路电流衰减过程
    RL circuit current decay

    公式 Formula:
        I(t) = I₀ e^(-t/τ)

    警告: 断开电感时可能产生很高的感应电压！
    """
    tau = L / R
    I = I0 * np.exp(-t / tau)
    return I


# =============================================================================
# 练习 5.3: RLC电路
# Exercise 5.3: RLC Circuit
# =============================================================================
# 物理背景 Physical Background:
# RLC电路是二阶系统，展示共振现象。
# 根据阻尼程度分为：过阻尼、临界阻尼、欠阻尼。
# 共振时阻抗最小（串联）或最大（并联），能量在L和C间振荡。

def rlc_resonance_frequency(L, C):
    """
    RLC电路共振频率
    RLC circuit resonance frequency

    返回 Returns:
        共振频率 f₀ [Hz]

    公式 Formula:
        ω₀ = 1/√(LC) [rad/s]
        f₀ = ω₀/(2π) = 1/(2π√LC) [Hz]

    共振时: X_L = X_C，总阻抗为纯电阻
    """
    omega_0 = 1 / np.sqrt(L * C)
    f_0 = omega_0 / (2 * np.pi)
    return f_0

def rlc_quality_factor(R, L, C):
    """
    品质因子 Q
    Quality factor

    公式 Formula:
        Q = ω₀L/R = 1/(ω₀RC) = (1/R)√(L/C)

    物理意义:
        Q 越大，共振峰越尖锐
        Q = f₀/Δf（相对带宽的倒数）
        Q 表示能量损耗率的倒数
    """
    omega_0 = 1 / np.sqrt(L * C)
    Q = omega_0 * L / R
    return Q

def rlc_damping(R, L, C):
    """
    判断RLC电路阻尼类型
    Determine RLC circuit damping type

    返回 Returns:
        'overdamped': 过阻尼（无振荡）
        'critically_damped': 临界阻尼（最快无振荡衰减）
        'underdamped': 欠阻尼（振荡衰减）

    判据: 比较 R² 与 4L/C
    """
    # TODO: 判断阻尼类型 (Determine damping type)
    discriminant = R**2 - 4*L/C
    if discriminant > 0:
        return 'overdamped'  # 过阻尼
    elif np.isclose(discriminant, 0, atol=1e-10):
        return 'critically_damped'  # 临界阻尼
    else:
        return 'underdamped'  # 欠阻尼

def rlc_underdamped_voltage(V0, R, L, C, t):
    """
    欠阻尼RLC电路电压响应
    Underdamped RLC circuit voltage response

    公式 Formula:
        V(t) = V₀ e^(-γt) cos(ω_d t)
        γ = R/(2L)（阻尼系数）
        ω_d = √(ω₀² - γ²)（阻尼振荡频率）
    """
    omega_0 = 1 / np.sqrt(L * C)
    gamma = R / (2 * L)  # 阻尼系数
    omega_d = np.sqrt(omega_0**2 - gamma**2)  # 阻尼振荡频率

    V = V0 * np.exp(-gamma * t) * np.cos(omega_d * t)
    return V


# =============================================================================
# 练习 5.4: 交流电路阻抗
# Exercise 5.4: AC Circuit Impedance
# =============================================================================
# 物理背景 Physical Background:
# 阻抗是交流电路中电压与电流的比值（复数）。
# 使用相量法可将微分方程转化为代数方程。
# Z = R + jX，R为电阻（耗能），X为电抗（储能）

def capacitor_impedance(C, omega):
    """
    电容的复阻抗
    Capacitor impedance

    公式 Formula:
        Z_C = 1/(jωC) = -j/(ωC)

    特点: 纯容性，电流超前电压90°
    频率越高，阻抗越小（高频通过）
    """
    return -1j / (omega * C)

def inductor_impedance(L, omega):
    """
    电感的复阻抗
    Inductor impedance

    公式 Formula:
        Z_L = jωL

    特点: 纯感性，电流滞后电压90°
    频率越高，阻抗越大（低频通过）
    """
    return 1j * omega * L

def series_impedance(R, L, C, omega):
    """
    串联RLC电路总阻抗
    Series RLC circuit impedance

    公式 Formula:
        Z = R + jωL + 1/(jωC) = R + j(ωL - 1/(ωC))

    共振时: ωL = 1/(ωC)，Z = R（纯电阻）
    """
    # TODO: 计算总阻抗 (Calculate total impedance)
    Z = R + inductor_impedance(L, omega) + capacitor_impedance(C, omega)
    return Z

def parallel_impedance(Z1, Z2):
    """
    并联阻抗
    Parallel impedance

    公式 Formula:
        1/Z = 1/Z₁ + 1/Z₂
        Z = Z₁Z₂/(Z₁ + Z₂)
    """
    return (Z1 * Z2) / (Z1 + Z2)


# =============================================================================
# 练习 5.5: 功率分析
# Exercise 5.5: Power Analysis
# =============================================================================
# 物理背景 Physical Background:
# 交流电路中，电压和电流可能存在相位差φ。
# 只有同相部分才消耗实际功率（有功功率）。
# 功率三角形: S² = P² + Q²

def ac_power(V_rms, I_rms, phi):
    """
    交流功率分析
    AC power analysis

    参数 Parameters:
        V_rms: 电压有效值 [V]
        I_rms: 电流有效值 [A]
        phi: 电压与电流相位差 [rad]

    返回 Returns:
        P: 有功功率 [W]（实际消耗的功率）
        Q: 无功功率 [VAR]（储能元件交换的功率）
        S: 视在功率 [VA]（电压电流乘积）

    功率三角形 Power Triangle:
        S² = P² + Q²
        P = S cos(φ)
        Q = S sin(φ)
    """
    P = V_rms * I_rms * np.cos(phi)  # 有功功率 Active power
    Q = V_rms * I_rms * np.sin(phi)  # 无功功率 Reactive power
    S = V_rms * I_rms               # 视在功率 Apparent power
    return P, Q, S

def power_factor(phi):
    """
    功率因数
    Power factor

    公式: PF = cos(φ) = P/S

    意义: 功率因数越高，电能利用效率越高
    工业要求: PF > 0.9（否则需要功率因数补偿）
    """
    return np.cos(phi)


# =============================================================================
# 练习 5.6: 滤波器
# Exercise 5.6: Filters
# =============================================================================
# 物理背景 Physical Background:
# 滤波器利用电容和电感的频率特性选择性地通过或阻止某些频率。
# RC低通滤波器：低频通过，高频衰减（电容对高频短路）
# RC高通滤波器：高频通过，低频衰减（电容对低频开路）
# 截止频率 f_c：增益下降到 1/√2（-3dB）的频率

def low_pass_filter_gain(R, C, omega):
    """
    RC低通滤波器增益
    RC low-pass filter gain

    参数 Parameters:
        R: 电阻 [Ω]
        C: 电容 [F]
        omega: 角频率 [rad/s]

    返回 Returns:
        增益幅值 |H(ω)|

    公式 Formula:
        H(ω) = 1/(1 + jωRC)
        |H(ω)| = 1/√(1 + (ωRC)²)

    特性 Characteristics:
        ω << ω_c: |H| → 1（全通）
        ω = ω_c: |H| = 1/√2 = 0.707（-3dB点）
        ω >> ω_c: |H| → 1/(ωRC)（-20dB/decade衰减）
    """
    H = 1 / (1 + 1j * omega * R * C)
    return np.abs(H)

def high_pass_filter_gain(R, C, omega):
    """
    RC高通滤波器增益
    RC high-pass filter gain

    参数 Parameters:
        R: 电阻 [Ω]
        C: 电容 [F]
        omega: 角频率 [rad/s]

    返回 Returns:
        增益幅值 |H(ω)|

    公式 Formula:
        H(ω) = jωRC/(1 + jωRC)
        |H(ω)| = ωRC/√(1 + (ωRC)²)

    特性 Characteristics:
        ω << ω_c: |H| → ωRC（+20dB/decade上升）
        ω = ω_c: |H| = 1/√2 = 0.707（-3dB点）
        ω >> ω_c: |H| → 1（全通）
    """
    H = 1j * omega * R * C / (1 + 1j * omega * R * C)
    return np.abs(H)

def cutoff_frequency(R, C):
    """
    截止频率
    Cutoff frequency

    返回 Returns:
        截止频率 f_c [Hz]

    公式 Formula:
        ω_c = 1/(RC) [rad/s]
        f_c = ω_c/(2π) = 1/(2πRC) [Hz]

    物理意义 Physical Meaning:
        截止频率是滤波器频率响应的特征点
        此处增益下降到最大值的 1/√2 ≈ 0.707（即-3dB）
    """
    return 1 / (2 * np.pi * R * C)


# =============================================================================
# 可视化
# =============================================================================
def plot_circuits():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 参数
    R = 1000  # 1 kΩ
    C = 1e-6  # 1 μF
    L = 0.1   # 100 mH
    V0 = 5    # 5 V

    # 1. RC充放电
    ax1 = axes[0, 0]
    tau = rc_time_constant(R, C)
    t = np.linspace(0, 5*tau, 500)

    V_charge = rc_charging(V0, R, C, t)
    V_discharge = rc_discharging(V0, R, C, t)

    ax1.plot(t*1000, V_charge, 'b-', label='充电', linewidth=2)
    ax1.plot(t*1000, V_discharge, 'r-', label='放电', linewidth=2)
    ax1.axvline(x=tau*1000, color='k', linestyle='--', alpha=0.5)
    ax1.axhline(y=V0*0.632, color='k', linestyle='--', alpha=0.5)
    ax1.set_xlabel('t (ms)')
    ax1.set_ylabel('V (V)')
    ax1.set_title(f'RC电路 (τ = {tau*1000:.2f} ms)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. RL电路
    ax2 = axes[0, 1]
    tau_rl = L / R
    t_rl = np.linspace(0, 5*tau_rl, 500)

    I_rise = rl_current_rise(V0, R, L, t_rl)
    I_decay = rl_current_decay(V0/R, R, L, t_rl)

    ax2.plot(t_rl*1000, I_rise*1000, 'b-', label='上升', linewidth=2)
    ax2.plot(t_rl*1000, I_decay*1000, 'r-', label='衰减', linewidth=2)
    ax2.set_xlabel('t (ms)')
    ax2.set_ylabel('I (mA)')
    ax2.set_title(f'RL电路 (τ = {tau_rl*1000:.4f} ms)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. RLC阻尼振荡
    ax3 = axes[0, 2]
    # 选择欠阻尼参数
    R_rlc = 100
    t_rlc = np.linspace(0, 0.01, 500)

    V_rlc = rlc_underdamped_voltage(V0, R_rlc, L, C, t_rlc)
    ax3.plot(t_rlc*1000, V_rlc, 'g-', linewidth=2)
    ax3.set_xlabel('t (ms)')
    ax3.set_ylabel('V (V)')
    f0 = rlc_resonance_frequency(L, C)
    Q = rlc_quality_factor(R_rlc, L, C)
    ax3.set_title(f'RLC欠阻尼 (f₀ = {f0:.0f} Hz, Q = {Q:.1f})')
    ax3.grid(True, alpha=0.3)

    # 4. 阻抗频率响应
    ax4 = axes[1, 0]
    f = np.logspace(1, 5, 500)
    omega = 2 * np.pi * f

    Z = [series_impedance(R, L, C, w) for w in omega]
    Z_mag = np.abs(Z)

    ax4.loglog(f, Z_mag, 'b-', linewidth=2)
    ax4.axvline(x=rlc_resonance_frequency(L, C), color='r', linestyle='--', label='共振')
    ax4.set_xlabel('f (Hz)')
    ax4.set_ylabel('|Z| (Ω)')
    ax4.set_title('RLC串联阻抗')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 低通/高通滤波器
    ax5 = axes[1, 1]
    f_c = cutoff_frequency(R, C)

    H_low = [low_pass_filter_gain(R, C, w) for w in omega]
    H_high = [high_pass_filter_gain(R, C, w) for w in omega]

    ax5.semilogx(f, 20*np.log10(H_low), 'b-', label='低通', linewidth=2)
    ax5.semilogx(f, 20*np.log10(H_high), 'r-', label='高通', linewidth=2)
    ax5.axvline(x=f_c, color='k', linestyle='--', alpha=0.5)
    ax5.axhline(y=-3, color='k', linestyle='--', alpha=0.5)
    ax5.set_xlabel('f (Hz)')
    ax5.set_ylabel('增益 (dB)')
    ax5.set_title(f'RC滤波器 (f_c = {f_c:.0f} Hz)')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    ax5.set_ylim(-40, 5)

    # 6. 功率三角形
    ax6 = axes[1, 2]
    phi_range = np.linspace(0, np.pi/2, 100)
    V_rms, I_rms = 220, 1

    P_vals = [ac_power(V_rms, I_rms, phi)[0] for phi in phi_range]
    Q_vals = [ac_power(V_rms, I_rms, phi)[1] for phi in phi_range]

    ax6.plot(np.degrees(phi_range), P_vals, 'b-', label='有功功率 P', linewidth=2)
    ax6.plot(np.degrees(phi_range), Q_vals, 'r-', label='无功功率 Q', linewidth=2)
    ax6.axhline(y=V_rms*I_rms, color='g', linestyle='--', label='视在功率 S')
    ax6.set_xlabel('相位角 φ (degrees)')
    ax6.set_ylabel('功率 (W/VAR/VA)')
    ax6.set_title('交流功率')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('circuits.png', dpi=150)
    print("图像已保存为 circuits.png")
    plt.show()


def verify():
    """
    验证所有电路分析练习
    Verify all circuit analysis exercises

    验证内容 Verification:
        5.1 RC电路充放电特性
        5.2 RL电路电流响应
        5.3 RLC电路共振频率和品质因子
        5.4 交流阻抗计算
        5.5 功率分析（功率三角形）
        5.6 滤波器频率响应
    """
    all_passed = True

    # 测试参数 Test parameters
    R = 1000   # 电阻 1 kΩ
    C = 1e-6   # 电容 1 μF
    L = 0.1    # 电感 100 mH
    V0 = 5     # 电压 5 V

    # 验证 5.1: RC电路
    # Check 5.1: RC circuit
    tau = rc_time_constant(R, C)
    V_tau = rc_charging(V0, R, C, tau)
    expected = V0 * (1 - np.exp(-1))  # t=τ时电压应为 0.632 V0
    if not np.isclose(V_tau, expected, rtol=0.01):
        print("❌ 5.1 RC充电错误")
        print("   提示: V(τ) = V₀(1 - e⁻¹) ≈ 0.632 V₀")
        all_passed = False
    else:
        print(f"✓ 5.1 RC电路正确 (τ = {tau*1000:.3f} ms)")

    # 验证 5.2: RL电路
    # Check 5.2: RL circuit
    tau_rl = L / R
    I_tau = rl_current_rise(V0, R, L, tau_rl)
    expected_I = (V0/R) * (1 - np.exp(-1))  # t=τ时电流应为 0.632 I_max
    if not np.isclose(I_tau, expected_I, rtol=0.01):
        print("❌ 5.2 RL电路错误")
        print("   提示: I(τ) = (V₀/R)(1 - e⁻¹) ≈ 0.632 × V₀/R")
        all_passed = False
    else:
        print("✓ 5.2 RL电路正确")

    # 验证 5.3: RLC共振
    # Check 5.3: RLC resonance
    f0 = rlc_resonance_frequency(L, C)
    expected_f0 = 1 / (2 * np.pi * np.sqrt(L * C))
    if not np.isclose(f0, expected_f0, rtol=0.01):
        print("❌ 5.3 RLC共振频率错误")
        print("   提示: f₀ = 1/(2π√LC)")
        all_passed = False
    else:
        print(f"✓ 5.3 RLC共振正确 (f₀ = {f0:.1f} Hz)")

    # 验证 5.4: 阻抗计算（共振时Z=R）
    # Check 5.4: Impedance (Z=R at resonance)
    omega_0 = 2 * np.pi * f0
    Z_res = series_impedance(R, L, C, omega_0)
    if not np.isclose(np.abs(Z_res), R, rtol=0.1):
        print("❌ 5.4 共振时阻抗应接近R")
        print("   提示: 共振时 X_L = X_C，阻抗为纯电阻")
        all_passed = False
    else:
        print("✓ 5.4 阻抗计算正确")

    # 验证 5.5: 功率三角形 P² + Q² = S²
    # Check 5.5: Power triangle
    P, Q, S = ac_power(220, 1, np.pi/4)
    if not np.isclose(P**2 + Q**2, S**2, rtol=0.01):
        print("❌ 5.5 功率关系错误")
        print("   提示: 功率三角形 S² = P² + Q²")
        all_passed = False
    else:
        print(f"✓ 5.5 功率分析正确 (P² + Q² = S²)")

    # 验证 5.6: 滤波器（截止频率处增益为 -3dB）
    # Check 5.6: Filter (-3dB at cutoff)
    f_c = cutoff_frequency(R, C)
    H_at_fc = low_pass_filter_gain(R, C, 2*np.pi*f_c)
    if not np.isclose(H_at_fc, 1/np.sqrt(2), rtol=0.01):
        print("❌ 5.6 截止频率处增益应为 -3dB")
        print("   提示: f = f_c 时 |H| = 1/√2 ≈ 0.707")
        all_passed = False
    else:
        print(f"✓ 5.6 滤波器正确 (f_c = {f_c:.1f} Hz)")

    if all_passed:
        print("\n🎉 所有测试通过！")
        try:
            plot_circuits()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("电路分析 Circuit Analysis")
    print("=" * 50)
    verify()
