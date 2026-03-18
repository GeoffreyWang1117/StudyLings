"""
电磁感应 Electromagnetic Induction
难度 Difficulty: ★★★

学习目标 Learning Objectives:
- 理解法拉第电磁感应定律的物理本质 (Understand Faraday's law)
- 掌握楞次定律判断感应电流方向 (Master Lenz's law)
- 分析自感和互感现象 (Analyze self and mutual inductance)
- 理解RL电路的暂态过程 (Understand RL circuit transients)

物理背景 Physical Background:
电磁感应是法拉第1831年发现的现象：变化的磁场产生电场（感应电动势）。
这是麦克斯韦方程组的核心内容之一，也是发电机和变压器的工作原理。

核心公式 Key Formulas:
- 磁通量 Magnetic flux: Φ = B·A = BA cos(θ) [Wb]
- 法拉第定律 Faraday's Law: ε = -dΦ/dt [V]
- 动生电动势 Motional EMF: ε = BLv [V]
- 螺线管自感 Solenoid inductance: L = μ₀N²A/l [H]
- 电感储能 Inductor energy: U = (1/2)LI² [J]
- RL时间常数: τ = L/R [s]

楞次定律 Lenz's Law:
感应电流的方向总是阻碍引起感应的磁通量变化。
负号的物理意义：能量守恒！

单位说明 Units:
- 磁通量: Wb (韦伯) = V·s
- 电感: H (亨利) = V·s/A = Wb/A
- 电动势: V (伏特)
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import mu_0

# I AM NOT DONE

# =============================================================================
# 练习 3.1: 磁通量
# Exercise 3.1: Magnetic Flux
# =============================================================================
# 物理背景 Physical Background:
# 磁通量描述穿过某一面积的磁场"总量"。
# 它是理解电磁感应的基础概念。
#
# 直观理解: 想象磁场线穿过一个面，磁通量就是穿过的磁场线数目

def magnetic_flux(B, A, theta=0):
    """
    计算磁通量
    Calculate magnetic flux

    参数 Parameters:
        B: 磁场强度 [T]
        A: 面积 [m²]
        theta: 磁场方向与面法向夹角 [rad]

    返回 Returns:
        磁通量 Φ [Wb] (韦伯)

    公式 Formula:
        Φ = B·A = BA cos(θ)
        当 θ = 0 时（B垂直穿过面），磁通量最大
        当 θ = 90° 时（B平行于面），磁通量为零
    """
    # TODO: 计算磁通量 (Calculate magnetic flux)
    Phi = B * A * np.cos(theta)
    return Phi

def flux_through_loop(B, R, theta=0):
    """
    圆形线圈的磁通量
    Magnetic flux through a circular loop
    """
    A = np.pi * R**2
    return magnetic_flux(B, A, theta)


# =============================================================================
# 练习 3.2: 法拉第定律
# Exercise 3.2: Faraday's Law
# =============================================================================
# 物理背景 Physical Background:
# 法拉第电磁感应定律：变化的磁通量产生感应电动势。
# 这是电磁学的核心定律之一，也是发电机的工作原理。
#
# 楞次定律 Lenz's Law:
# 负号表示感应电动势总是反抗引起它的磁通量变化。
# 这是能量守恒的体现！

def induced_emf(dPhi_dt):
    """
    法拉第电磁感应定律
    Faraday's law of electromagnetic induction

    参数 Parameters:
        dPhi_dt: 磁通量变化率 [Wb/s]

    返回 Returns:
        感应电动势 ε [V]

    公式 Formula:
        ε = -dΦ/dt

    负号意义（楞次定律）:
        - dΦ/dt > 0（磁通增加）→ ε < 0（反向电动势）
        - dΦ/dt < 0（磁通减少）→ ε > 0（正向电动势）
        感应电流产生的磁场总是阻碍原磁通的变化
    """
    # TODO: 计算感应电动势 (Calculate induced EMF)
    emf = -dPhi_dt
    return emf

def motional_emf(B, L, v):
    """
    动生电动势
    Motional EMF

    当导体在磁场中运动时，导体中的自由电子受洛伦兹力作用而移动，
    在导体两端形成电势差。

    参数 Parameters:
        B: 磁场强度 [T]
        L: 导体长度（垂直于v和B）[m]
        v: 导体速度（垂直于B）[m/s]

    公式 Formula:
        ε = BLv

    应用: 发电机、电磁刹车
    """
    return B * L * v


# =============================================================================
# 练习 3.3: 自感
# Exercise 3.3: Self-Inductance
# =============================================================================
# 物理背景 Physical Background:
# 自感描述线圈自身电流变化引起的感应电动势。
# 电感器是储能元件，能量储存在磁场中。
#
# 直观理解: 电感"惯性"——反抗电流的变化

def inductance_solenoid(N, A, l):
    """
    螺线管自感
    Self-inductance of a solenoid

    参数 Parameters:
        N: 匝数 (无量纲)
        A: 截面积 [m²]
        l: 长度 [m]

    返回 Returns:
        自感 L [H] (亨利)

    公式 Formula:
        L = μ₀N²A/l

    推导:
        磁场 B = μ₀nI = μ₀NI/l
        磁通 Φ = BA = μ₀NIA/l
        总磁通链 NΦ = μ₀N²IA/l
        自感 L = NΦ/I = μ₀N²A/l
    """
    # TODO: 计算自感 (Calculate self-inductance)
    L = mu_0 * N**2 * A / l
    return L

def self_induced_emf(L, dI_dt):
    """
    自感电动势
    Self-induced EMF

    公式 Formula:
        ε = -L(dI/dt)

    物理意义: 电流增加时产生反向电动势阻止增加
    """
    return -L * dI_dt

def magnetic_energy_inductor(L, I):
    """
    电感器储存的磁场能量
    Magnetic energy stored in inductor

    公式 Formula:
        U = (1/2)LI² [J]

    类比: 类似于电容器储能 U = (1/2)CV²
    """
    return 0.5 * L * I**2


# =============================================================================
# 练习 3.4: 互感
# Exercise 3.4: Mutual Inductance
# =============================================================================
# 物理背景 Physical Background:
# 互感描述一个线圈电流变化在另一个线圈中产生的感应电动势。
# 这是变压器的工作原理。
#
# 互易定理: M₁₂ = M₂₁ = M

def mutual_inductance_coaxial(N1, N2, A, l):
    """
    同轴螺线管的互感
    Mutual inductance of coaxial solenoids

    参数 Parameters:
        N1: 初级线圈匝数
        N2: 次级线圈匝数
        A: 公共截面积 [m²]
        l: 长度 [m]

    返回 Returns:
        互感 M [H]

    公式 Formula:
        M = μ₀N₁N₂A/l

    应用: 变压器、无线充电
    """
    # TODO: 计算互感 (Calculate mutual inductance)
    M = mu_0 * N1 * N2 * A / l
    return M

def mutual_induced_emf(M, dI_dt):
    """
    互感电动势
    Mutually induced EMF

    线圈1的电流变化在线圈2中产生的电动势:
    ε₂ = -M(dI₁/dt)
    """
    return -M * dI_dt


# =============================================================================
# 练习 3.5: RL电路
# Exercise 3.5: RL Circuit
# =============================================================================
# 物理背景 Physical Background:
# RL电路是电感和电阻串联的电路。
# 电感的"惯性"使电流不能突变，导致暂态过程。
#
# 时间常数 τ = L/R 表示电流达到稳态值约63.2%所需时间
# 5τ后电流达到稳态值的99.3%

def rl_time_constant(L, R):
    """
    RL电路时间常数
    RL circuit time constant

    公式 Formula:
        τ = L/R [s]

    物理意义: τ越大，电流变化越慢（电感越大或电阻越小）
    """
    return L / R

def rl_current_growth(V, R, L, t):
    """
    RL电路接通后电流增长（充电过程）
    Current growth in RL circuit after switch-on

    参数 Parameters:
        V: 电源电压 [V]
        R: 电阻 [Ω]
        L: 电感 [H]
        t: 时间 [s]

    返回 Returns:
        电流 I(t) [A]

    公式 Formula:
        I(t) = (V/R)(1 - e^(-t/τ))

    特征值:
        t = 0: I = 0 (电流不能突变)
        t = τ: I = 0.632 × V/R
        t → ∞: I = V/R (稳态电流)
    """
    tau = rl_time_constant(L, R)
    # TODO: 计算电流 (Calculate current)
    I = (V / R) * (1 - np.exp(-t / tau))
    return I

def rl_current_decay(I0, R, L, t):
    """
    RL电路断开后电流衰减（放电过程）
    Current decay in RL circuit after switch-off

    公式 Formula:
        I(t) = I₀ e^(-t/τ)

    注意: 电感中储存的能量通过电阻消耗
    """
    tau = rl_time_constant(L, R)
    return I0 * np.exp(-t / tau)


# =============================================================================
# 练习 3.6: 发电机
# Exercise 3.6: AC Generator
# =============================================================================
# 物理背景 Physical Background:
# 发电机将机械能转换为电能。
# 线圈在磁场中旋转，磁通量周期性变化，产生交流电动势。
#
# 工作原理: Φ = BA cos(ωt) → ε = -dΦ/dt = BAω sin(ωt)

def generator_emf(N, B, A, omega, t):
    """
    交流发电机瞬时电动势
    Instantaneous EMF of an AC generator

    参数 Parameters:
        N: 线圈匝数
        B: 磁场强度 [T]
        A: 线圈面积 [m²]
        omega: 角频率 [rad/s]
        t: 时间 [s]

    返回 Returns:
        瞬时电动势 ε(t) [V]

    公式 Formula:
        ε(t) = NBAω sin(ωt) = ε₀ sin(ωt)

    推导:
        磁通 Φ = NBAcos(ωt)
        感应电动势 ε = -dΦ/dt = NBAω sin(ωt)
    """
    # TODO: 计算电动势 (Calculate EMF)
    emf = N * B * A * omega * np.sin(omega * t)
    return emf

def generator_peak_emf(N, B, A, omega):
    """
    峰值电动势
    Peak EMF of generator

    公式: ε₀ = NBAω

    有效值: ε_rms = ε₀/√2
    """
    return N * B * A * omega


# =============================================================================
# 练习 3.7: 涡流
# Exercise 3.7: Eddy Currents
# =============================================================================
# 物理背景 Physical Background:
# 当导体处于变化的磁场中时，在导体内部感应出环形电流，称为涡流。
# 涡流会产生热量（涡流损耗），在变压器和电机中需要尽量减小。
#
# 应用:
# - 电磁炉（利用涡流加热）
# - 涡流制动
# - 金属探测器

def eddy_current_power(B, omega, sigma, t, V):
    """
    涡流功率损耗估算（简化模型）
    Estimate of eddy current power loss (simplified model)

    参数 Parameters:
        B: 磁场幅值 [T]
        omega: 角频率 [rad/s]
        sigma: 电导率 [S/m]
        t: 材料厚度 [m]
        V: 体积 [m³]

    返回 Returns:
        功率损耗 P [W]

    公式 Formula (近似):
        P ∝ σω²B²t²V

    减小涡流损耗的方法:
        1. 使用叠片铁芯（减小t）
        2. 使用高电阻率材料（减小σ）
    """
    return sigma * omega**2 * B**2 * t**2 * V


# =============================================================================
# 可视化
# =============================================================================
def plot_induction():
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. RL电路电流增长
    ax1 = axes[0, 0]
    V, R, L = 10, 100, 1  # V, Ω, H
    tau = rl_time_constant(L, R)
    t = np.linspace(0, 5*tau, 200)
    I = rl_current_growth(V, R, L, t)
    ax1.plot(t*1000, I*1000, 'b-', linewidth=2)
    ax1.axhline(y=V/R*1000, color='r', linestyle='--', label='I_max')
    ax1.axvline(x=tau*1000, color='g', linestyle='--', label='τ')
    ax1.set_xlabel('t (ms)')
    ax1.set_ylabel('I (mA)')
    ax1.set_title('RL电路电流增长')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. RL电路电流衰减
    ax2 = axes[0, 1]
    I0 = V / R
    I_decay = rl_current_decay(I0, R, L, t)
    ax2.plot(t*1000, I_decay*1000, 'r-', linewidth=2)
    ax2.set_xlabel('t (ms)')
    ax2.set_ylabel('I (mA)')
    ax2.set_title('RL电路电流衰减')
    ax2.grid(True, alpha=0.3)

    # 3. 发电机输出
    ax3 = axes[1, 0]
    N, B, A, omega = 100, 0.5, 0.01, 100*np.pi  # 50Hz
    t_gen = np.linspace(0, 0.04, 500)  # 2个周期
    emf = generator_emf(N, B, A, omega, t_gen)
    ax3.plot(t_gen*1000, emf, 'b-', linewidth=2)
    ax3.set_xlabel('t (ms)')
    ax3.set_ylabel('EMF (V)')
    ax3.set_title(f'交流发电机输出 (f=50Hz)')
    ax3.grid(True, alpha=0.3)

    # 4. 电感储能
    ax4 = axes[1, 1]
    I_range = np.linspace(0, 1, 100)
    for L_val in [0.1, 0.5, 1.0]:
        U = magnetic_energy_inductor(L_val, I_range)
        ax4.plot(I_range, U, label=f'L = {L_val} H')
    ax4.set_xlabel('I (A)')
    ax4.set_ylabel('U (J)')
    ax4.set_title('电感储能')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('electromagnetic_induction.png', dpi=150)
    print("图像已保存为 electromagnetic_induction.png")
    plt.show()


def verify():
    """
    验证所有练习的正确性
    Verify correctness of all exercises
    """
    all_passed = True

    # 检查 3.1 - 磁通量 (Check magnetic flux)
    Phi = magnetic_flux(0.5, 0.01, 0)
    if not np.isclose(Phi, 0.005, rtol=0.01):
        print("❌ 3.1 磁通量计算错误")
        print("   提示: Φ = BA cos(θ)，当θ=0时 Φ = BA")
        all_passed = False
    else:
        print(f"✓ 3.1 磁通量正确 (Φ = {Phi*1000:.1f} mWb)")

    # 检查 3.2 - 法拉第定律 (Check Faraday's law)
    emf = induced_emf(0.1)
    if not np.isclose(emf, -0.1, rtol=0.01):
        print("❌ 3.2 感应电动势计算错误")
        print("   提示: ε = -dΦ/dt，注意负号（楞次定律）")
        all_passed = False
    else:
        print(f"✓ 3.2 法拉第定律正确（含楞次定律负号）")

    # 检查 3.3 - 自感 (Check self-inductance)
    L = inductance_solenoid(1000, 1e-4, 0.1)
    expected = mu_0 * 1e6 * 1e-4 / 0.1
    if not np.isclose(L, expected, rtol=0.01):
        print("❌ 3.3 螺线管自感计算错误")
        print("   提示: L = μ₀N²A/l")
        all_passed = False
    else:
        print(f"✓ 3.3 自感正确 (L = {L*1000:.2f} mH)")

    # 检查 3.5 - RL电路时间常数 (Check RL time constant)
    tau = rl_time_constant(1, 100)
    if not np.isclose(tau, 0.01, rtol=0.01):
        print("❌ 3.5 RL电路时间常数计算错误")
        print("   提示: τ = L/R")
        all_passed = False
    else:
        print(f"✓ 3.5 RL电路正确 (τ = {tau*1000:.1f} ms)")

    # 检查 3.6 - 发电机 (Check generator)
    emf_peak = generator_peak_emf(100, 0.5, 0.01, 100*np.pi)
    if emf_peak <= 0:
        print("❌ 3.6 发电机峰值电动势计算错误")
        print("   提示: ε₀ = NBAω")
        all_passed = False
    else:
        print(f"✓ 3.6 发电机正确 (ε₀ = {emf_peak:.1f} V)")

    if all_passed:
        print("\n🎉 所有测试通过！")
        try:
            plot_induction()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("电磁感应 Electromagnetic Induction")
    print("=" * 50)
    verify()
