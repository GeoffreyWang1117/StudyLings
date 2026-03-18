"""
相对论动力学 Relativistic Dynamics
难度 Difficulty: ★★★★

学习目标 Learning Objectives:
- 理解相对论性动量和能量的物理意义
  Understand the physical meaning of relativistic momentum and energy
- 掌握四维动量的概念和应用
  Master the concept and applications of four-momentum
- 分析粒子碰撞和阈能计算
  Analyze particle collisions and threshold energy calculations
- 理解相对论多普勒效应
  Understand relativistic Doppler effect

物理背景 Physical Background:
在高速运动下，经典力学的动量 p = mv 和动能 KE = ½mv² 不再适用。
相对论动力学引入洛伦兹因子 γ 来修正这些公式：
- 相对论动量: p = γmv
- 相对论动能: KE = (γ-1)mc²
- 总能量: E = γmc² = KE + mc²

四维动量是时空中的四矢量，在洛伦兹变换下保持其"长度"（不变量）。
四动量: p^μ = (E/c, px, py, pz)
不变量: p·p = (E/c)² - |p|² = (mc)²

关键公式 Key Formulas:
- 相对论动量 Relativistic momentum: p = γmv
- 总能量 Total energy: E = γmc²
- 能量-动量关系: E² = (pc)² + (mc²)²
- 阈能（固定靶）: E_th = [(Σm_f)² - m₁² - m₂²]c² / (2m₂)
- 纵向多普勒: f = f₀√((1+β)/(1-β)) (接近)

单位说明 Units:
- 能量: J, eV, keV, MeV, GeV
- 动量: kg·m/s 或 eV/c, MeV/c
- 质量: kg 或 eV/c², MeV/c²
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import c, m_e, m_p, eV

# I AM NOT DONE

# =============================================================================
# 练习 2.1: 洛伦兹因子
# Exercise 2.1: Lorentz Factor
#
# 物理背景：洛伦兹因子 γ 是所有相对论效应的核心。
# γ ≥ 1，当 v=0 时 γ=1，当 v→c 时 γ→∞。
# =============================================================================

def lorentz_factor(v):
    """
    计算洛伦兹因子 Calculate Lorentz factor

    公式 Formula: γ = 1/√(1 - v²/c²) = 1/√(1 - β²)

    参数 Parameters:
        v: 速度 velocity (m/s)

    返回 Returns:
        gamma: 洛伦兹因子 (无量纲 dimensionless)，γ ≥ 1
    """
    beta = v / c  # β = v/c，归一化速度
    # TODO: 计算洛伦兹因子
    gamma = 1 / np.sqrt(1 - beta**2)
    return gamma


def velocity_from_gamma(gamma):
    """
    从洛伦兹因子反推速度 Calculate velocity from Lorentz factor

    公式 Formula: β = √(1 - 1/γ²), v = βc

    参数 Parameters:
        gamma: 洛伦兹因子，必须 γ ≥ 1

    返回 Returns:
        v: 速度 velocity (m/s)
    """
    beta = np.sqrt(1 - 1/gamma**2)
    return beta * c


# =============================================================================
# 练习 2.2: 相对论动量
# Exercise 2.2: Relativistic Momentum
#
# 物理背景：相对论动量 p = γmv 比经典动量 mv 多一个 γ 因子。
# 当 v→c 时，p→∞，这解释了为什么有质量的物体无法达到光速。
# 牛顿第二定律的相对论形式: F = dp/dt = d(γmv)/dt
# =============================================================================

def relativistic_momentum(m, v):
    """
    计算相对论动量 Calculate relativistic momentum

    公式 Formula: p = γmv

    参数 Parameters:
        m: 静止质量 rest mass (kg)
        v: 速度 velocity (m/s)

    返回 Returns:
        p: 相对论动量 (kg·m/s)

    注意：当 v << c 时，γ ≈ 1，退化为经典动量 p ≈ mv
    """
    gamma = lorentz_factor(v)
    # TODO: 计算相对论动量
    p = gamma * m * v
    return p


def classical_momentum(m, v):
    """
    经典动量 Classical momentum

    公式 Formula: p = mv

    用于与相对论动量比较
    """
    return m * v


# =============================================================================
# 练习 2.3: 相对论能量
# Exercise 2.3: Relativistic Energy
#
# 物理背景：爱因斯坦的质能等价 E = mc² 是静止能量。
# 运动物体的总能量 E = γmc² 包含静止能量和动能。
# 总能量 = 静止能量 + 动能: E = mc² + KE
# =============================================================================

def rest_energy(m):
    """
    静止能量 Rest energy

    公式 Formula: E₀ = mc²

    这是物质固有的能量，即使静止也存在。
    电子静止能量约 0.511 MeV，质子约 938 MeV。
    """
    return m * c**2


def total_energy(m, v):
    """
    总能量 Total energy

    公式 Formula: E = γmc²

    参数 Parameters:
        m: 静止质量 rest mass (kg)
        v: 速度 velocity (m/s)

    返回 Returns:
        E: 总能量 (J)

    关系: E = E₀ + KE = mc² + (γ-1)mc²
    """
    gamma = lorentz_factor(v)
    return gamma * m * c**2


def kinetic_energy_relativistic(m, v):
    """
    相对论动能 Relativistic kinetic energy

    公式 Formula: K = (γ-1)mc²

    参数 Parameters:
        m: 静止质量 rest mass (kg)
        v: 速度 velocity (m/s)

    返回 Returns:
        K: 动能 kinetic energy (J)

    注意：当 v << c 时，γ-1 ≈ ½v²/c²，所以 K ≈ ½mv²（经典极限）
    """
    gamma = lorentz_factor(v)
    # TODO: 计算相对论动能
    K = (gamma - 1) * m * c**2
    return K


def energy_momentum_relation(E, p, m):
    """
    验证能量-动量关系 Verify energy-momentum relation

    公式 Formula: E² = (pc)² + (mc²)²

    这是洛伦兹不变量，在所有惯性参考系中成立。
    对于光子（m=0）：E = pc
    对于静止粒子（p=0）：E = mc²
    """
    E_squared = E**2
    expected = (p * c)**2 + (m * c**2)**2
    return np.isclose(E_squared, expected, rtol=1e-6)


# =============================================================================
# 练习 2.4: 四维动量
# Exercise 2.4: Four-Momentum
#
# 物理背景：四维动量是时空中的四矢量，将能量和动量统一在一起。
# p^μ = (E/c, px, py, pz) 在洛伦兹变换下像四矢量一样变换。
# 四动量的"模方"是洛伦兹不变量，等于 (mc)²。
#
# Physical background: Four-momentum is a four-vector that unifies energy
# and momentum. Its "magnitude squared" is a Lorentz invariant = (mc)².
# =============================================================================

def four_momentum(m, v):
    """
    四维动量 Four-momentum

    公式 Formula: p^μ = (E/c, px, py, pz)

    参数 Parameters:
        m: 静止质量 rest mass (kg)
        v: 速度 velocity (m/s)，假设沿 x 方向运动

    返回 Returns:
        p_mu: 四动量数组 [E/c, px, py, pz]

    四动量的分量:
    - p⁰ = E/c = γmc
    - p¹ = px = γmvx
    - p², p³ = 0 (假设沿x轴运动)
    """
    gamma = lorentz_factor(v)
    E = gamma * m * c**2  # 总能量
    p = gamma * m * v     # 三动量大小

    return np.array([E/c, p, 0, 0])


def four_momentum_invariant(p_mu):
    """
    四维动量不变量 Four-momentum invariant

    公式 Formula: p·p = (E/c)² - |p|² = (mc)²

    使用闵可夫斯基度规 η = diag(1, -1, -1, -1)
    内积定义: A·B = A⁰B⁰ - A¹B¹ - A²B² - A³B³

    参数 Parameters:
        p_mu: 四动量数组 [p⁰, p¹, p², p³]

    返回 Returns:
        invariant: 不变量 (mc)² (kg²·m²/s²)

    这个不变量在所有参考系中相同，用于粒子识别。
    """
    # TODO: 计算不变量
    # 使用度规 (+,-,-,-) 计算
    invariant = p_mu[0]**2 - p_mu[1]**2 - p_mu[2]**2 - p_mu[3]**2
    return invariant


def mass_from_four_momentum(p_mu):
    """
    从四动量计算静质量 Calculate rest mass from four-momentum

    公式: m = √(p·p) / c

    这是粒子物理中识别粒子的标准方法：
    测量能量和动量，计算不变质量。
    """
    inv = four_momentum_invariant(p_mu)
    return np.sqrt(inv) / c  # 返回 m（单位：kg）


# =============================================================================
# 练习 2.5: 粒子碰撞
# Exercise 2.5: Particle Collisions
#
# 物理背景：高能物理中粒子碰撞遵循能量和动量守恒。
# 阈能是产生新粒子所需的最小入射能量。
# 质心系能量 √s 是碰撞物理中的关键参数。
#
# Physical background: Particle collisions conserve energy and momentum.
# Threshold energy is the minimum energy to produce new particles.
# =============================================================================

def threshold_energy(m1, m2, m3, m4):
    """
    计算反应阈能（固定靶实验）
    Calculate threshold energy (fixed target experiment)

    反应: m1 + m2 → m3 + m4 (m2 静止)

    公式 Formula: E_th = [(m3+m4)² - (m1+m2)²]c² / (2m2)

    参数 Parameters:
        m1: 入射粒子质量 (kg)
        m2: 靶粒子质量 (kg)，静止
        m3, m4: 产物粒子质量 (kg)

    返回 Returns:
        E_th: 阈能，入射粒子的最小总能量 (J)

    物理解释：阈能是刚好能产生反应产物的最小能量，
    此时所有产物在质心系中静止。
    """
    # TODO: 计算阈能
    E_th = ((m3 + m4)**2 - (m1 + m2)**2) * c**4 / (2 * m2 * c**2)
    return E_th


def center_of_mass_energy(E1, p1, m2):
    """
    计算质心系能量（固定靶碰撞）
    Calculate center-of-mass energy (fixed target collision)

    公式 Formula: √s = √(2E₁m₂c² + m₁²c⁴ + m₂²c⁴)

    参数 Parameters:
        E1: 入射粒子能量 (J)
        p1: 入射粒子动量大小 (kg·m/s)
        m2: 靶粒子质量 (kg)，静止

    返回 Returns:
        sqrt_s: 质心系总能量 (J)

    √s 是对撞机物理中最重要的参数，决定了可产生粒子的质量上限。
    """
    m1_squared = (E1**2 - (p1*c)**2) / c**4  # 从能量动量关系求 m1²
    s = 2 * E1 * m2 * c**2 + m1_squared * c**4 + (m2 * c**2)**2
    return np.sqrt(s)


def compton_wavelength_shift(theta):
    """
    计算康普顿散射波长偏移 Compton scattering wavelength shift

    公式 Formula: Δλ = λ_C (1 - cos θ)

    其中 λ_C = h/(m_e c) ≈ 2.426 pm 是电子的康普顿波长

    参数 Parameters:
        theta: 散射角 (rad)

    返回 Returns:
        delta_lambda: 波长偏移 (m)

    物理意义：光子与电子碰撞后波长增加（能量减少），
    这是粒子性的直接证据。θ = π 时偏移最大（背散射）。
    """
    h = 2 * np.pi * 1.055e-34  # 普朗克常数 h = 2πℏ
    lambda_c = h / (m_e * c)   # 康普顿波长 ≈ 2.426×10⁻¹² m
    return lambda_c * (1 - np.cos(theta))


# =============================================================================
# 练习 2.6: 相对论性多普勒效应
# Exercise 2.6: Relativistic Doppler Effect
#
# 物理背景：相对论多普勒效应与经典多普勒效应不同，包含时间膨胀修正。
# 纵向效应：光源沿视线运动，频率蓝移（接近）或红移（远离）。
# 横向效应：光源垂直于视线运动，仅有时间膨胀导致的红移（经典无此效应）。
#
# Physical background: Relativistic Doppler effect includes time dilation.
# Longitudinal: source moves along line of sight (blueshift/redshift)
# Transverse: source moves perpendicular to line of sight (pure time dilation)
# =============================================================================

def relativistic_doppler_longitudinal(f0, v, approaching=True):
    """
    纵向相对论多普勒效应 Longitudinal relativistic Doppler effect

    公式 Formulas:
        接近 approaching: f = f₀ √((1+β)/(1-β)) (蓝移 blueshift)
        远离 receding:    f = f₀ √((1-β)/(1+β)) (红移 redshift)

    参数 Parameters:
        f0: 光源静止时发出的频率 (Hz)
        v: 相对速度 (m/s)
        approaching: True=接近（蓝移），False=远离（红移）

    返回 Returns:
        f: 观测到的频率 (Hz)

    应用：宇宙学红移测量星系退行速度，雷达测速
    """
    beta = v / c
    if approaching:
        f = f0 * np.sqrt((1 + beta) / (1 - beta))  # 蓝移，频率增加
    else:
        f = f0 * np.sqrt((1 - beta) / (1 + beta))  # 红移，频率减少
    return f


def relativistic_doppler_transverse(f0, v):
    """
    横向相对论多普勒效应 Transverse relativistic Doppler effect

    公式 Formula: f = f₀ / γ

    参数 Parameters:
        f0: 光源静止时发出的频率 (Hz)
        v: 相对速度 (m/s)

    返回 Returns:
        f: 观测到的频率 (Hz)

    物理解释：这是纯粹的时间膨胀效应。
    运动光源的时钟变慢，所以发出的光频率降低（红移）。
    经典多普勒效应没有横向效应，这是相对论独有的。
    """
    gamma = lorentz_factor(v)
    return f0 / gamma  # 总是红移（频率降低）


# =============================================================================
# 可视化
# =============================================================================
def plot_relativistic_dynamics():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 洛伦兹因子
    ax1 = axes[0, 0]
    v = np.linspace(0, 0.999, 500) * c
    gamma = [lorentz_factor(vi) for vi in v]

    ax1.semilogy(v/c, gamma, 'b-', linewidth=2)
    ax1.set_xlabel('v/c')
    ax1.set_ylabel('γ')
    ax1.set_title('洛伦兹因子')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(1, 100)

    # 2. 动量比较
    ax2 = axes[0, 1]
    p_rel = [relativistic_momentum(m_e, vi) for vi in v]
    p_class = [classical_momentum(m_e, vi) for vi in v]

    ax2.plot(v/c, np.array(p_rel)/(m_e*c), 'b-', label='相对论', linewidth=2)
    ax2.plot(v/c, np.array(p_class)/(m_e*c), 'r--', label='经典', linewidth=2)
    ax2.set_xlabel('v/c')
    ax2.set_ylabel('p/(m_e c)')
    ax2.set_title('动量比较')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 10)

    # 3. 动能比较
    ax3 = axes[0, 2]
    K_rel = [kinetic_energy_relativistic(m_e, vi) for vi in v]
    K_class = [0.5 * m_e * vi**2 for vi in v]
    E0 = rest_energy(m_e)

    ax3.plot(v/c, np.array(K_rel)/E0, 'b-', label='相对论', linewidth=2)
    ax3.plot(v/c, np.array(K_class)/E0, 'r--', label='经典', linewidth=2)
    ax3.set_xlabel('v/c')
    ax3.set_ylabel('K/(m_e c²)')
    ax3.set_title('动能比较')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim(0, 5)

    # 4. 能量-动量关系
    ax4 = axes[1, 0]
    p_range = np.linspace(0, 5, 100) * m_e * c
    E = np.sqrt((p_range * c)**2 + (m_e * c**2)**2)

    ax4.plot(p_range/(m_e*c), E/(m_e*c**2), 'b-', label='E(p)', linewidth=2)
    ax4.plot(p_range/(m_e*c), p_range*c/(m_e*c**2), 'r--', label='E = pc (光子)', linewidth=2)
    ax4.axhline(y=1, color='g', linestyle=':', label='m_e c²')
    ax4.set_xlabel('p/(m_e c)')
    ax4.set_ylabel('E/(m_e c²)')
    ax4.set_title('能量-动量关系')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 康普顿散射
    ax5 = axes[1, 1]
    theta = np.linspace(0, np.pi, 100)
    delta_lambda = [compton_wavelength_shift(t) * 1e12 for t in theta]  # pm

    ax5.plot(np.degrees(theta), delta_lambda, 'g-', linewidth=2)
    ax5.set_xlabel('散射角 θ (degrees)')
    ax5.set_ylabel('Δλ (pm)')
    ax5.set_title('康普顿散射波长偏移')
    ax5.grid(True, alpha=0.3)

    # 6. 相对论多普勒效应
    ax6 = axes[1, 2]
    v_doppler = np.linspace(0.01, 0.99, 100) * c

    f_approach = [relativistic_doppler_longitudinal(1, vi, True) for vi in v_doppler]
    f_recede = [relativistic_doppler_longitudinal(1, vi, False) for vi in v_doppler]
    f_trans = [relativistic_doppler_transverse(1, vi) for vi in v_doppler]

    ax6.semilogy(v_doppler/c, f_approach, 'b-', label='接近', linewidth=2)
    ax6.semilogy(v_doppler/c, f_recede, 'r-', label='远离', linewidth=2)
    ax6.semilogy(v_doppler/c, f_trans, 'g--', label='横向', linewidth=2)
    ax6.axhline(y=1, color='k', linestyle=':', alpha=0.5)
    ax6.set_xlabel('v/c')
    ax6.set_ylabel('f/f₀')
    ax6.set_title('相对论多普勒效应')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('relativistic_dynamics.png', dpi=150)
    print("图像已保存为 relativistic_dynamics.png")
    plt.show()


def verify():
    """
    验证所有练习的正确性 Verify all exercises

    检查内容 Checks:
    2.1 洛伦兹因子计算
    2.2 相对论动量
    2.3 静止能量
    2.4 四动量不变量
    2.5 阈能计算
    2.6 多普勒效应方向
    """
    all_passed = True

    # 检查 2.1 - 洛伦兹因子
    gamma = lorentz_factor(0.6 * c)
    expected_gamma = 1.25  # γ(0.6c) = 1/√(1-0.36) = 1.25
    if not np.isclose(gamma, expected_gamma, rtol=0.01):
        print("错误 2.1 洛伦兹因子计算错误")
        all_passed = False
    else:
        print(f"通过 2.1 洛伦兹因子正确 (v=0.6c 时 γ = {gamma:.3f})")

    # 检查 2.2 - 相对论动量
    p = relativistic_momentum(m_e, 0.9 * c)
    gamma_09 = lorentz_factor(0.9 * c)
    expected_p = gamma_09 * m_e * 0.9 * c
    if not np.isclose(p, expected_p, rtol=0.01):
        print("错误 2.2 相对论动量计算错误")
        all_passed = False
    else:
        print(f"通过 2.2 相对论动量正确 (p = γmv)")

    # 检查 2.3 - 静止能量
    E0 = rest_energy(m_e)
    expected_E0 = 0.511e6 * eV  # 电子静止能量约 0.511 MeV
    if not np.isclose(E0, expected_E0, rtol=0.01):
        print("错误 2.3 电子静止能量计算错误")
        all_passed = False
    else:
        print(f"通过 2.3 静止能量正确 (m_e c² = {E0/eV/1e6:.3f} MeV)")

    # 检查 2.4 - 四动量不变量
    p_mu = four_momentum(m_e, 0.8 * c)
    inv = four_momentum_invariant(p_mu)
    expected_inv = (m_e * c)**2  # 不变量应等于 (mc)²
    if not np.isclose(inv, expected_inv, rtol=0.01):
        print("错误 2.4 四动量不变量计算错误，应等于 (mc)²")
        all_passed = False
    else:
        print("通过 2.4 四动量不变量正确 (p·p = (mc)²)")

    # 检查 2.5 - 阈能
    # 反应: p + p → p + p + p + p̄ (产生质子-反质子对)
    E_th = threshold_energy(m_p, m_p, 3*m_p, m_p)
    if E_th <= 0:
        print("错误 2.5 阈能应为正值")
        all_passed = False
    else:
        print(f"通过 2.5 阈能计算正确 (E_th > 0)")

    # 检查 2.6 - 多普勒效应
    f_approach = relativistic_doppler_longitudinal(1, 0.5*c, True)
    f_recede = relativistic_doppler_longitudinal(1, 0.5*c, False)
    if not (f_approach > 1 and f_recede < 1):
        print("错误 2.6 多普勒效应方向错误：接近应蓝移，远离应红移")
        all_passed = False
    else:
        print(f"通过 2.6 多普勒效应正确 (接近蓝移 f={f_approach:.2f}, 远离红移 f={f_recede:.2f})")

    if all_passed:
        print("\n所有测试通过！正在生成可视化图像...")
        try:
            plot_relativistic_dynamics()
        except Exception as e:
            print(f"可视化生成失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("相对论动力学 Relativistic Dynamics")
    print("=" * 50)
    verify()
