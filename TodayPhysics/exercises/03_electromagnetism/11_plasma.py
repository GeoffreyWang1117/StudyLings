"""
等离子体物理基础 Plasma Physics Basics
难度 Difficulty: ★★★★

学习目标 Learning Objectives:
- 理解等离子体的基本性质和参数 (Understand plasma properties and parameters)
- 掌握德拜屏蔽和等离子体振荡 (Master Debye shielding and plasma oscillations)
- 分析电磁波在等离子体中的传播 (Analyze EM wave propagation in plasma)
- 理解带电粒子在磁场中的运动 (Understand charged particle motion in B field)

物理背景 Physical Background:
等离子体是物质的第四态，由离子和电子组成的电离气体。
宇宙中99%以上的可见物质是等离子体（恒星、星际介质等）。
地球上的等离子体应用包括聚变能源、半导体加工、照明等。

核心公式 Key Formulas:
- 德拜长度: λ_D = √(ε₀k_BT_e/(n_e e²))
- 等离子体频率: ω_p = √(n_e e²/(ε₀m_e))
- 回旋频率: ω_c = |q|B/m
- 拉莫尔半径: r_L = mv_⊥/(|q|B)
- 等离子体折射率: n² = 1 - (ω_p/ω)²
- 朗缪尔波色散: ω² = ω_p² + 3k²v_th²

等离子体判据 Plasma Criteria:
- 准中性: L >> λ_D（系统尺寸远大于德拜长度）
- 集体行为: N_D >> 1（德拜球内粒子数远大于1）
- 弱碰撞: ω_p τ >> 1（等离子体周期内碰撞很少）

单位说明 Units:
- 密度: m⁻³（有时用cm⁻³）
- 温度: K 或 eV（1 eV ≈ 11600 K）
- 频率: Hz 或 rad/s
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import epsilon_0, k_B, e, m_e, m_p, c

# I AM NOT DONE

# =============================================================================
# 练习 11.1: 德拜长度
# Exercise 11.1: Debye Length
# =============================================================================
# 物理背景 Physical Background:
# 德拜长度是等离子体最重要的特征尺度。
# 在德拜长度范围内，单个带电粒子的电场会被周围粒子屏蔽。
# 德拜长度之外，等离子体表现为准中性。

def debye_length(n_e, T_e):
    """
    德拜长度 - 等离子体屏蔽特征尺度
    Debye length - characteristic shielding scale

    参数 Parameters:
        n_e: 电子密度 [m⁻³]
        T_e: 电子温度 [K]

    返回 Returns:
        德拜长度 λ_D [m]

    公式 Formula:
        λ_D = √(ε₀k_BT_e/(n_e e²))

    典型值:
        聚变等离子体(n=10²⁰, T=10⁸K): λ_D ~ 10⁻⁴ m
        电离层(n=10¹², T=1000K): λ_D ~ 10⁻² m
    """
    # TODO: 计算德拜长度 (Calculate Debye length)
    lambda_D = np.sqrt(epsilon_0 * k_B * T_e / (n_e * e**2))
    return lambda_D

def debye_number(n_e, T_e):
    """
    德拜球内粒子数
    Number of particles in Debye sphere

    参数 Parameters:
        n_e: 电子密度 [m⁻³]
        T_e: 电子温度 [K]

    返回 Returns:
        德拜数 N_D（无量纲）

    公式 Formula:
        N_D = (4/3)π n_e λ_D³

    物理意义:
        N_D >> 1: 弱耦合等离子体，集体效应主导
        N_D ~ 1: 强耦合等离子体，粒子相关性重要
    """
    lambda_D = debye_length(n_e, T_e)
    N_D = (4/3) * np.pi * n_e * lambda_D**3
    return N_D


# =============================================================================
# 练习 11.2: 等离子体频率
# Exercise 11.2: Plasma Frequency
# =============================================================================
# 物理背景 Physical Background:
# 等离子体频率是电子（或离子）在恢复力下振荡的自然频率。
# 当电子被扰动偏离平衡位置时，产生净电荷，电场将电子拉回。
# 等离子体频率是等离子体中波动传播的下限。

def plasma_frequency_electron(n_e):
    """
    电子等离子体频率
    Electron plasma frequency

    参数 Parameters:
        n_e: 电子密度 [m⁻³]

    返回 Returns:
        电子等离子体角频率 ω_pe [rad/s]

    公式 Formula:
        ω_pe = √(n_e e²/(ε₀m_e))

    简化公式:
        f_pe [Hz] ≈ 9√n_e [m⁻³]

    意义: 频率低于ω_pe的电磁波不能在等离子体中传播
    """
    # TODO: 计算电子等离子体频率 (Calculate electron plasma frequency)
    omega_pe = np.sqrt(n_e * e**2 / (epsilon_0 * m_e))
    return omega_pe

def plasma_frequency_ion(n_i, m_i=m_p):
    """
    离子等离子体频率
    Ion plasma frequency

    参数 Parameters:
        n_i: 离子密度 [m⁻³]
        m_i: 离子质量 [kg]（默认为质子质量）

    返回 Returns:
        离子等离子体角频率 ω_pi [rad/s]

    公式 Formula:
        ω_pi = √(n_i e²/(ε₀m_i))

    说明: 由于m_i >> m_e，ω_pi << ω_pe
    """
    omega_pi = np.sqrt(n_i * e**2 / (epsilon_0 * m_i))
    return omega_pi

def plasma_parameter(n_e, T_e):
    """
    等离子体参数（库仑对数相关）
    Plasma parameter

    返回 Returns:
        Λ = N_D（德拜数）

    判据:
        Λ >> 1: 弱耦合等离子体（理想等离子体）
        Λ ~ 1: 强耦合等离子体
    """
    return debye_number(n_e, T_e)


# =============================================================================
# 练习 11.3: 电磁波在等离子体中传播
# Exercise 11.3: EM Wave Propagation in Plasma
# =============================================================================
# 物理背景 Physical Background:
# 等离子体对电磁波是色散介质。自由电子对电场响应产生极化电流，
# 改变了有效介电常数。低于等离子体频率的波被反射。
# 这解释了为什么无线电波能被电离层反射。

def refractive_index_plasma(omega, n_e):
    """
    等离子体折射率
    Plasma refractive index

    参数 Parameters:
        omega: 电磁波角频率 [rad/s]
        n_e: 电子密度 [m⁻³]

    返回 Returns:
        折射率 n（无量纲）

    公式 Formula:
        n² = 1 - (ω_p/ω)²
        ω < ω_p: n² < 0（截止，波衰减）
        ω > ω_p: n < 1（相速度超光速）

    应用: 电离层无线电传播、等离子体诊断
    """
    omega_p = plasma_frequency_electron(n_e)
    n_squared = 1 - (omega_p / omega)**2
    if n_squared < 0:
        return 0  # 截止区
    return np.sqrt(n_squared)

def cutoff_frequency(n_e):
    """
    截止频率
    Cutoff frequency

    参数 Parameters:
        n_e: 电子密度 [m⁻³]

    返回 Returns:
        截止角频率 ω_c [rad/s]

    说明: 截止频率等于等离子体频率
    低于此频率的电磁波不能在等离子体中传播
    """
    return plasma_frequency_electron(n_e)

def group_velocity_plasma(omega, n_e):
    """
    等离子体中的群速度
    Group velocity in plasma

    参数 Parameters:
        omega: 电磁波角频率 [rad/s]
        n_e: 电子密度 [m⁻³]

    返回 Returns:
        群速度 v_g [m/s]

    公式 Formula:
        v_g = c√(1 - (ω_p/ω)²)

    特点: v_g < c，能量传播速度小于光速
    与波导中的色散特性相似
    """
    omega_p = plasma_frequency_electron(n_e)
    if omega <= omega_p:
        return 0  # 截止
    return c * np.sqrt(1 - (omega_p / omega)**2)


# =============================================================================
# 练习 11.4: 回旋运动
# Exercise 11.4: Cyclotron Motion
# =============================================================================
# 物理背景 Physical Background:
# 带电粒子在磁场中受洛伦兹力作用做圆周运动（回旋运动）。
# 回旋频率只与电荷质量比和磁场有关，与速度无关。
# 这是回旋加速器、磁约束聚变等技术的基础。

def cyclotron_frequency(q, m, B):
    """
    回旋频率（角频率）
    Cyclotron frequency

    参数 Parameters:
        q: 电荷 [C]
        m: 质量 [kg]
        B: 磁场强度 [T]

    返回 Returns:
        回旋角频率 ω_c [rad/s]

    公式 Formula:
        ω_c = |q|B/m

    典型值:
        电子在1T磁场: ω_c ≈ 1.76×10¹¹ rad/s
        质子在1T磁场: ω_c ≈ 9.58×10⁷ rad/s
    """
    # TODO: 计算回旋频率 (Calculate cyclotron frequency)
    omega_c = np.abs(q) * B / m
    return omega_c

def larmor_radius(v_perp, q, m, B):
    """
    拉莫尔半径（回旋半径）
    Larmor radius

    参数 Parameters:
        v_perp: 垂直于磁场的速度分量 [m/s]
        q: 电荷 [C]
        m: 质量 [kg]
        B: 磁场强度 [T]

    返回 Returns:
        拉莫尔半径 r_L [m]

    公式 Formula:
        r_L = mv_⊥/(|q|B)

    说明: 速度越大或磁场越弱，回旋半径越大
    """
    r_L = m * v_perp / (np.abs(q) * B)
    return r_L

def cyclotron_motion(t, v0, B, q=e, m=m_e):
    """
    回旋运动轨迹
    Cyclotron motion trajectory

    参数 Parameters:
        t: 时间 [s]
        v0: 垂直速度 [m/s]
        B: 磁场强度 [T]（沿z方向）
        q: 电荷 [C]
        m: 质量 [kg]

    返回 Returns:
        (x, y): 轨迹坐标 [m]

    说明: 假设B沿z方向，初始时刻粒子在原点
    """
    omega_c = cyclotron_frequency(q, m, B)
    r_L = larmor_radius(v0, q, m, B)

    x = r_L * np.sin(omega_c * t)
    y = r_L * (1 - np.cos(omega_c * t))
    return x, y


# =============================================================================
# 练习 11.5: 磁镜效应
# Exercise 11.5: Magnetic Mirror Effect
# =============================================================================
# 物理背景 Physical Background:
# 当粒子沿磁力线运动进入磁场增强区域时，由于磁矩守恒，
# 垂直速度增大，平行速度减小，直到被反射。
# 这是范艾伦辐射带和磁约束聚变中的重要效应。

def magnetic_moment(m, v_perp, B):
    """
    磁矩（绝热不变量）
    Magnetic moment (adiabatic invariant)

    参数 Parameters:
        m: 质量 [kg]
        v_perp: 垂直速度 [m/s]
        B: 磁场强度 [T]

    返回 Returns:
        磁矩 μ [J/T]

    公式 Formula:
        μ = mv_⊥²/(2B)

    物理意义: 在缓变磁场中μ是绝热不变量
    """
    return m * v_perp**2 / (2 * B)

def mirror_ratio(B_max, B_min):
    """
    磁镜比
    Mirror ratio

    参数 Parameters:
        B_max: 最大磁场 [T]
        B_min: 最小磁场 [T]

    返回 Returns:
        磁镜比 R（无量纲）

    公式 Formula:
        R = B_max/B_min

    说明: R越大，约束能力越强
    """
    return B_max / B_min

def loss_cone_angle(B_max, B_min):
    """
    损失锥角度
    Loss cone angle

    参数 Parameters:
        B_max: 磁镜处磁场 [T]
        B_min: 中心磁场 [T]

    返回 Returns:
        损失锥半角 θ_loss [rad]

    公式 Formula:
        sin²(θ_loss) = B_min/B_max = 1/R

    物理意义:
        俯仰角小于θ_loss的粒子会逃逸
        俯仰角大于θ_loss的粒子被反射约束
    """
    R = mirror_ratio(B_max, B_min)
    theta_loss = np.arcsin(1 / np.sqrt(R))
    return theta_loss


# =============================================================================
# 练习 11.6: 朗缪尔波
# Exercise 11.6: Langmuir Waves
# =============================================================================
# 物理背景 Physical Background:
# 朗缪尔波是等离子体中的纵向电子振荡，也称为等离子体波。
# 这是等离子体最基本的集体激发模式。
# 离子声波是涉及离子运动的低频纵波。

def langmuir_dispersion(k, n_e, T_e):
    """
    朗缪尔波色散关系
    Langmuir wave dispersion relation

    参数 Parameters:
        k: 波数 [m⁻¹]
        n_e: 电子密度 [m⁻³]
        T_e: 电子温度 [K]

    返回 Returns:
        角频率 ω [rad/s]

    公式 Formula:
        ω² = ω_p² + 3k²v_th²
        v_th = √(k_BT_e/m_e)

    说明:
        k → 0: ω → ω_p（等离子体振荡）
        热修正项(3k²v_th²)来自电子压力
    """
    omega_p = plasma_frequency_electron(n_e)
    v_th = np.sqrt(k_B * T_e / m_e)  # 热速度
    omega_squared = omega_p**2 + 3 * k**2 * v_th**2
    return np.sqrt(omega_squared)

def ion_acoustic_speed(T_e, T_i, m_i=m_p):
    """
    离子声波速度
    Ion acoustic speed

    参数 Parameters:
        T_e: 电子温度 [K]
        T_i: 离子温度 [K]
        m_i: 离子质量 [kg]

    返回 Returns:
        离子声速 c_s [m/s]

    公式 Formula:
        c_s = √(k_B(T_e + 3T_i)/m_i)

    说明: 当T_e >> T_i时，c_s ≈ √(k_BT_e/m_i)
    类似于气体声速，但压力来自电子
    """
    c_s = np.sqrt(k_B * (T_e + 3 * T_i) / m_i)
    return c_s

def ion_acoustic_dispersion(k, n_e, T_e, T_i, m_i=m_p):
    """
    离子声波色散关系
    Ion acoustic wave dispersion

    参数 Parameters:
        k: 波数 [m⁻¹]
        n_e: 电子密度 [m⁻³]
        T_e: 电子温度 [K]
        T_i: 离子温度 [K]
        m_i: 离子质量 [kg]

    返回 Returns:
        角频率 ω [rad/s]

    公式 Formula（简化）:
        ω = k × c_s

    说明: 离子声波是等离子体中的低频纵波
    """
    c_s = ion_acoustic_speed(T_e, T_i, m_i)
    return k * c_s


# =============================================================================
# 可视化
# =============================================================================
def plot_plasma():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 德拜长度vs密度和温度
    ax1 = axes[0, 0]
    n_e = np.logspace(15, 22, 100)  # m⁻³

    for T in [1e4, 1e6, 1e8]:
        lambda_D = [debye_length(n, T) for n in n_e]
        ax1.loglog(n_e, lambda_D, label=f'T={T:.0e} K', linewidth=2)

    ax1.set_xlabel('电子密度 n_e (m⁻³)')
    ax1.set_ylabel('德拜长度 λ_D (m)')
    ax1.set_title('德拜长度')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 等离子体频率
    ax2 = axes[0, 1]
    omega_p = [plasma_frequency_electron(n) for n in n_e]
    f_p = [w / (2 * np.pi) for w in omega_p]

    ax2.loglog(n_e, f_p, 'b-', linewidth=2)
    ax2.set_xlabel('电子密度 n_e (m⁻³)')
    ax2.set_ylabel('等离子体频率 f_p (Hz)')
    ax2.set_title('电子等离子体频率')
    ax2.grid(True, alpha=0.3)

    # 3. 折射率vs频率
    ax3 = axes[0, 2]
    n_e_fixed = 1e18  # m⁻³
    omega_p = plasma_frequency_electron(n_e_fixed)
    omega = np.linspace(0.5 * omega_p, 5 * omega_p, 200)

    n_refract = [refractive_index_plasma(w, n_e_fixed) for w in omega]
    ax3.plot(omega / omega_p, n_refract, 'b-', linewidth=2)
    ax3.axvline(x=1, color='r', linestyle='--', label='ω = ω_p')
    ax3.set_xlabel('ω / ω_p')
    ax3.set_ylabel('折射率 n')
    ax3.set_title('等离子体折射率')
    ax3.set_ylim(0, 1.2)
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 回旋运动
    ax4 = axes[1, 0]
    B = 1  # T
    v0 = 1e6  # m/s
    t = np.linspace(0, 5e-10, 1000)

    x, y = cyclotron_motion(t, v0, B)
    ax4.plot(x * 1e6, y * 1e6, 'b-', linewidth=1.5)
    ax4.set_xlabel('x (μm)')
    ax4.set_ylabel('y (μm)')
    ax4.set_title('电子回旋运动 (B=1T)')
    ax4.axis('equal')
    ax4.grid(True, alpha=0.3)

    # 5. 朗缪尔波色散
    ax5 = axes[1, 1]
    n_e_wave = 1e18
    T_e = 1e6
    k = np.linspace(0, 1e7, 200)

    omega_L = [langmuir_dispersion(kv, n_e_wave, T_e) for kv in k]
    omega_p_ref = plasma_frequency_electron(n_e_wave)

    ax5.plot(k * 1e-6, np.array(omega_L) / omega_p_ref, 'b-', linewidth=2)
    ax5.axhline(y=1, color='r', linestyle='--', label='ω_p')
    ax5.set_xlabel('k (×10⁶ m⁻¹)')
    ax5.set_ylabel('ω / ω_p')
    ax5.set_title('朗缪尔波色散关系')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. 损失锥
    ax6 = axes[1, 2]
    theta = np.linspace(0, np.pi/2, 100)

    for R in [2, 5, 10]:
        B_min, B_max = 1, R
        theta_loss = loss_cone_angle(B_max, B_min)
        theta_pass = np.linspace(theta_loss, np.pi/2 - theta_loss, 50)

        ax6.fill_between(np.degrees(theta_pass), 0, 1, alpha=0.3, label=f'R={R}')
        ax6.axvline(x=np.degrees(theta_loss), linestyle='--')

    ax6.set_xlabel('俯仰角 θ (度)')
    ax6.set_ylabel('被约束')
    ax6.set_title('磁镜损失锥')
    ax6.set_xlim(0, 90)
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('plasma.png', dpi=150)
    print("图像已保存为 plasma.png")
    plt.show()


def verify():
    """
    验证所有等离子体物理练习
    Verify all plasma physics exercises

    验证内容 Verification:
        11.1 德拜长度计算
        11.2 等离子体频率
        11.3 折射率和波传播
        11.4 回旋频率
        11.5 磁镜损失锥
        11.6 朗缪尔波色散
    """
    all_passed = True

    # 测试参数
    n_e = 1e18  # 电子密度 m⁻³
    T_e = 1e6   # 电子温度 K（约100 eV）

    # 验证 11.1: 德拜长度
    # Check 11.1: Debye length
    lambda_D = debye_length(n_e, T_e)
    expected_lambda = np.sqrt(epsilon_0 * k_B * T_e / (n_e * e**2))
    if not np.isclose(lambda_D, expected_lambda, rtol=0.01):
        print("❌ 11.1 德拜长度计算错误")
        print("   提示: λ_D = √(ε₀k_BT_e/(n_ee²))")
        all_passed = False
    else:
        print(f"✓ 11.1 德拜长度正确 (λ_D = {lambda_D:.2e} m)")

    # 验证 11.2: 等离子体频率
    # Check 11.2: Plasma frequency
    omega_p = plasma_frequency_electron(n_e)
    f_p = omega_p / (2 * np.pi)
    if omega_p <= 0:
        print("❌ 11.2 等离子体频率应为正")
        all_passed = False
    else:
        print(f"✓ 11.2 等离子体频率正确 (f_p = {f_p:.2e} Hz)")

    # 验证 11.3: 等离子体折射率
    # Check 11.3: Plasma refractive index
    n = refractive_index_plasma(2 * omega_p, n_e)
    expected_n = np.sqrt(1 - 0.25)  # n² = 1 - (1/2)² = 0.75
    if not np.isclose(n, expected_n, rtol=0.01):
        print("❌ 11.3 等离子体折射率错误")
        print("   提示: n² = 1 - (ω_p/ω)²")
        all_passed = False
    else:
        print(f"✓ 11.3 折射率正确 (n(2ω_p) = {n:.3f})")

    # 验证 11.4: 回旋频率
    # Check 11.4: Cyclotron frequency
    B = 1  # T
    omega_c = cyclotron_frequency(e, m_e, B)
    expected_omega_c = e * B / m_e
    if not np.isclose(omega_c, expected_omega_c, rtol=0.01):
        print("❌ 11.4 回旋频率错误")
        print("   提示: ω_c = |q|B/m")
        all_passed = False
    else:
        print(f"✓ 11.4 回旋频率正确 (ω_c = {omega_c:.2e} rad/s)")

    # 验证 11.5: 损失锥
    # Check 11.5: Loss cone
    theta_loss = loss_cone_angle(4, 1)  # 磁镜比 R = 4
    expected_theta = np.arcsin(0.5)     # sin(θ) = 1/√R = 1/2
    if not np.isclose(theta_loss, expected_theta, rtol=0.01):
        print("❌ 11.5 损失锥角度错误")
        print("   提示: sin²(θ) = 1/R")
        all_passed = False
    else:
        print(f"✓ 11.5 损失锥正确 (θ_loss = {np.degrees(theta_loss):.1f}°)")

    # 验证 11.6: 朗缪尔波
    # Check 11.6: Langmuir wave
    omega_L = langmuir_dispersion(0, n_e, T_e)
    if not np.isclose(omega_L, omega_p, rtol=0.01):
        print("❌ 11.6 朗缪尔波k=0时ω应等于ω_p")
        print("   提示: ω² = ω_p² + 3k²v_th²，k=0时ω=ω_p")
        all_passed = False
    else:
        print(f"✓ 11.6 朗缪尔波正确 (ω(k=0) = ω_p)")

    if all_passed:
        print("\n🎉 所有测试通过！")
        try:
            plot_plasma()
        except Exception as ex:
            print(f"可视化失败: {ex}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("等离子体物理基础 Plasma Physics Basics")
    print("=" * 50)
    verify()
