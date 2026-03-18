"""
洛伦兹变换与狭义相对论 Lorentz Transformation and Special Relativity
难度 Difficulty: ★★★★

学习目标 Learning Objectives:
- 理解洛伦兹变换的数学形式和物理意义
  Understand the mathematical form and physical meaning of Lorentz transformation
- 掌握时间膨胀和长度收缩效应的计算
  Master the calculation of time dilation and length contraction effects
- 计算相对论性动量和能量，理解质能等价
  Calculate relativistic momentum and energy, understand mass-energy equivalence
- 应用速度叠加公式处理高速运动问题
  Apply velocity addition formula to high-speed motion problems

物理背景 Physical Background:
狭义相对论由爱因斯坦于1905年提出，基于两个基本假设：
1. 相对性原理：物理定律在所有惯性参考系中形式相同
2. 光速不变原理：真空中光速在所有惯性系中相同，c ≈ 3×10⁸ m/s

洛伦兹变换取代了伽利略变换，正确描述了高速运动下的时空关系。
当速度远小于光速时（v << c），洛伦兹变换退化为伽利略变换。

关键公式 Key Formulas:
- 洛伦兹因子 Lorentz factor: γ = 1/√(1 - v²/c²) = 1/√(1 - β²), β = v/c
- 时间膨胀 Time dilation: Δt = γΔt₀ （运动时钟走得慢）
- 长度收缩 Length contraction: L = L₀/γ （运动方向长度缩短）
- 质能关系 Mass-energy: E = γmc², E₀ = mc²（静止能量）
- 动量 Momentum: p = γmv
- 能量-动量关系: E² = (pc)² + (mc²)²

单位说明 Units:
- 速度 velocity: m/s
- 时间 time: s
- 长度 length: m
- 能量 energy: J 或 eV
- 动量 momentum: kg·m/s 或 eV/c
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import c, m_e, m_p, eV, MeV

# I AM NOT DONE

# =============================================================================
# 练习 1.1: 洛伦兹因子
# Exercise 1.1: Lorentz Factor
#
# 物理背景：洛伦兹因子 γ 是狭义相对论中最核心的量，它出现在所有相对论效应中。
# 当 v→0 时，γ→1（经典极限）；当 v→c 时，γ→∞（相对论极限）。
# Physical background: The Lorentz factor γ is the most fundamental quantity
# in special relativity. As v→0, γ→1 (classical limit); as v→c, γ→∞.
# =============================================================================
def lorentz_factor(v):
    """
    计算洛伦兹因子 Calculate Lorentz factor

    公式 Formula: γ = 1/√(1 - v²/c²) = 1/√(1 - β²)

    参数 Parameters:
        v: 速度 velocity (m/s)，必须满足 |v| < c

    返回 Returns:
        gamma: 洛伦兹因子 Lorentz factor (无量纲 dimensionless)

    物理意义：γ 表示相对论效应的强度
    - γ = 1: 无相对论效应（v = 0）
    - γ = 1.15: v ≈ 0.5c
    - γ = 2.29: v ≈ 0.9c
    - γ = 7.09: v ≈ 0.99c
    """
    beta = v / c  # 归一化速度 normalized velocity
    if np.any(np.abs(beta) >= 1):
        raise ValueError("速度必须小于光速 Velocity must be less than speed of light")
    # TODO: 计算洛伦兹因子
    # 提示：使用公式 γ = 1/√(1 - β²)
    gamma = 1 / np.sqrt(1 - beta**2)  # 修改这里
    return gamma


# 测试不同速度的洛伦兹因子
# Test Lorentz factor at different velocities
v_test = 0.9 * c  # 0.9c，接近光速 approaching speed of light
gamma_test = lorentz_factor(v_test)


# =============================================================================
# 练习 1.2: 时间膨胀
# Exercise 1.2: Time Dilation
#
# 物理背景：运动的时钟走得慢！这是相对论最著名的效应之一。
# 固有时 Δt₀ 是在与物体共动的参考系中测量的时间（时钟与物体静止）。
# 坐标时 Δt 是在"静止"参考系中测量的时间，Δt > Δt₀。
#
# Physical background: Moving clocks run slow! This is one of the most famous
# effects of relativity. Proper time Δt₀ is measured in the rest frame of the
# object. Coordinate time Δt is measured in the "stationary" frame, Δt > Δt₀.
#
# 实验验证：μ子衰变实验、原子钟飞行实验、GPS卫星校正
# =============================================================================

def time_dilation(proper_time, v):
    """
    计算时间膨胀 Calculate time dilation

    公式 Formula: Δt = γΔt₀ = Δt₀/√(1 - v²/c²)

    参数 Parameters:
        proper_time: 固有时 Δt₀ (s)，在物体静止参考系中测量的时间
        v: 相对速度 (m/s)，物体相对于观测者的速度

    返回 Returns:
        dilated_time: 膨胀后的时间 Δt (s)，在观测者参考系中测量的时间

    物理解释：
    - 运动的时钟走得慢，γ 越大，时间膨胀越显著
    - 当 v = 0.8c 时，γ ≈ 1.67，即运动时钟每走1秒，静止时钟走1.67秒
    """
    gamma = lorentz_factor(v)
    # TODO: 计算膨胀后的时间
    # 提示：膨胀后的时间 = γ × 固有时
    dilated_time = gamma * proper_time  # 修改这里
    return dilated_time


# 例子: 飞船以 0.8c 飞行，飞船上的时钟过了 1 年
# Example: A spaceship travels at 0.8c, ship's clock shows 1 year passed
v_ship = 0.8 * c
proper_time = 1.0 * 365.25 * 24 * 3600  # 1 year in seconds (飞船时间)
dilated_time = time_dilation(proper_time, v_ship)
years_on_earth = dilated_time / (365.25 * 24 * 3600)  # 地球上过了多少年


# =============================================================================
# 练习 1.3: 长度收缩
# Exercise 1.3: Length Contraction
#
# 物理背景：运动的物体在运动方向上变短！
# 固有长度 L₀ 是在物体静止参考系中测量的长度。
# 收缩只发生在运动方向，垂直方向的长度不变。
#
# Physical background: Moving objects are shorter in the direction of motion!
# Proper length L₀ is measured in the object's rest frame.
# Contraction only occurs along the direction of motion.
#
# 注意：长度收缩是真实的物理效应，不是视觉错觉
# =============================================================================

def length_contraction(proper_length, v):
    """
    计算长度收缩 Calculate length contraction

    公式 Formula: L = L₀/γ = L₀√(1 - v²/c²)

    参数 Parameters:
        proper_length: 固有长度 L₀ (m)，物体静止时的长度
        v: 相对速度 (m/s)，物体相对于观测者的速度

    返回 Returns:
        contracted_length: 收缩后的长度 L (m)，在观测者参考系中测量的长度

    物理解释：
    - 运动物体在运动方向上收缩，收缩因子为 1/γ
    - 当 v = 0.9c 时，γ ≈ 2.29，长度收缩为原来的 43.6%
    - 收缩只影响运动方向，垂直方向保持不变
    """
    gamma = lorentz_factor(v)
    # TODO: 计算收缩后的长度
    # 提示：收缩后的长度 = 固有长度 / γ
    contracted_length = proper_length / gamma  # 修改这里
    return contracted_length


# 例子: 一艘 100m 长的飞船以 0.9c 飞过
# Example: A 100m long spaceship flies past at 0.9c
L0 = 100.0  # m（飞船的固有长度，飞船上测量）
L_contracted = length_contraction(L0, 0.9 * c)  # 地球上观测到的长度


# =============================================================================
# 练习 1.4: 洛伦兹变换
# Exercise 1.4: Lorentz Transformation
#
# 物理背景：洛伦兹变换描述了不同惯性参考系之间时空坐标的关系。
# 设 S' 系相对于 S 系以速度 v 沿 x 轴正方向运动，且 t=t'=0 时两原点重合。
#
# Physical background: Lorentz transformation describes the relationship
# between spacetime coordinates in different inertial frames.
#
# 洛伦兹变换取代了伽利略变换 x' = x - vt, t' = t
# 关键区别：时间也会变换，空间和时间相互关联
# =============================================================================

def lorentz_transform(x, t, v):
    """
    洛伦兹变换: 从S系到S'系 Lorentz transformation: from S to S'

    公式 Formulas:
        x' = γ(x - vt)
        t' = γ(t - vx/c²)

    参数 Parameters:
        x: S系中的位置坐标 (m)
        t: S系中的时间坐标 (s)
        v: S'相对于S的速度 (m/s)，沿x轴正方向

    返回 Returns:
        (x', t'): S'系中的坐标和时间 (m, s)

    注意：y 和 z 坐标在洛伦兹变换下保持不变（y' = y, z' = z）
    """
    gamma = lorentz_factor(v)
    # TODO: 计算变换后的坐标
    # 提示：注意时间变换中有 vx/c² 项，这反映了同时性的相对性
    x_prime = gamma * (x - v * t)
    t_prime = gamma * (t - v * x / c**2)
    return x_prime, t_prime


def inverse_lorentz_transform(x_prime, t_prime, v):
    """
    逆洛伦兹变换: 从S'系到S系 Inverse Lorentz transformation: from S' to S

    公式 Formulas:
        x = γ(x' + vt')
        t = γ(t' + vx'/c²)

    参数 Parameters:
        x_prime: S'系中的位置坐标 (m)
        t_prime: S'系中的时间坐标 (s)
        v: S'相对于S的速度 (m/s)

    返回 Returns:
        (x, t): S系中的坐标和时间 (m, s)

    注意：逆变换只需将 v 替换为 -v（从S'看，S以-v运动）
    """
    gamma = lorentz_factor(v)
    # TODO: 计算逆变换
    # 提示：逆变换的公式中 v 变为 +v（符号相反）
    x = gamma * (x_prime + v * t_prime)
    t = gamma * (t_prime + v * x_prime / c**2)
    return x, t


# =============================================================================
# 练习 1.5: 速度叠加公式
# Exercise 1.5: Velocity Addition
#
# 物理背景：在相对论中，速度不能简单相加！
# 经典力学中 u = u' + v，但这会导致速度超过光速。
# 相对论速度叠加公式保证合成速度永远不会超过光速。
#
# Physical background: In relativity, velocities cannot simply be added!
# The relativistic formula ensures the combined speed never exceeds c.
#
# 特例：如果 u' = c 或 v = c，则 u = c（光速不变原理）
# =============================================================================

def relativistic_velocity_addition(u_prime, v):
    """
    相对论速度叠加 Relativistic velocity addition

    公式 Formula: u = (u' + v) / (1 + u'v/c²)

    参数 Parameters:
        u_prime: 物体在S'系中的速度 (m/s)
        v: S'相对于S的速度 (m/s)

    返回 Returns:
        u: 物体在S系中的速度 (m/s)

    重要性质：
    - 当 u', v << c 时，退化为经典公式 u ≈ u' + v
    - 无论 u' 和 v 多大，只要小于 c，则 u < c
    - 如果 u' = c，则 u = c（光速不变）
    """
    # TODO: 计算合成速度
    # 提示：分母中的修正项 u'v/c² 防止速度超过光速
    u = (u_prime + v) / (1 + u_prime * v / c**2)  # 修改这里
    return u


# 测试: 两艘飞船各以 0.9c 相向飞行，它们的相对速度
# Test: Two spaceships each traveling at 0.9c towards each other
v1 = 0.9 * c  # 第一艘飞船相对于地球的速度
v2 = 0.9 * c  # 第二艘飞船相对于第一艘飞船的速度
relative_v = relativistic_velocity_addition(v2, v1)
# 经典力学预期: 1.8c（超光速！）
# 相对论结果: ≈ 0.9945c（仍小于光速）


# =============================================================================
# 练习 1.6: 相对论能量和动量
# Exercise 1.6: Relativistic Energy and Momentum
#
# 物理背景：爱因斯坦最著名的方程 E = mc² 实际上是静止能量。
# 完整的质能关系是 E = γmc²，包含了动能和静止能量。
# 相对论动量 p = γmv 在高速时显著大于经典动量 mv。
#
# Physical background: Einstein's famous E = mc² is actually rest energy.
# The complete relation is E = γmc², including kinetic and rest energy.
#
# 核心关系：E² = (pc)² + (mc²)² （能量-动量关系，洛伦兹不变量）
# =============================================================================

def relativistic_momentum(m, v):
    """
    相对论动量 Relativistic momentum

    公式 Formula: p = γmv

    参数 Parameters:
        m: 静止质量 rest mass (kg)
        v: 速度 velocity (m/s)

    返回 Returns:
        p: 相对论动量 (kg·m/s)

    注意：当 v→c 时，p→∞，这就是为什么有质量的物体无法达到光速
    """
    gamma = lorentz_factor(v)
    # TODO: 计算动量
    # 提示：相对论动量比经典动量多一个 γ 因子
    p = gamma * m * v  # 修改这里
    return p


def relativistic_energy(m, v):
    """
    相对论总能量 Relativistic total energy

    公式 Formula: E = γmc²

    参数 Parameters:
        m: 静止质量 rest mass (kg)
        v: 速度 velocity (m/s)

    返回 Returns:
        E: 总能量 total energy (J)

    总能量 = 静止能量 + 动能: E = mc² + KE
    """
    gamma = lorentz_factor(v)
    # TODO: 计算总能量
    E = gamma * m * c**2  # 修改这里
    return E


def kinetic_energy(m, v):
    """
    相对论动能 Relativistic kinetic energy

    公式 Formula: KE = (γ-1)mc²

    参数 Parameters:
        m: 静止质量 rest mass (kg)
        v: 速度 velocity (m/s)

    返回 Returns:
        KE: 动能 kinetic energy (J)

    注意：当 v << c 时，KE ≈ ½mv²（退化为经典动能）
    证明：γ - 1 ≈ ½v²/c² 当 v << c
    """
    gamma = lorentz_factor(v)
    # TODO: 计算动能
    # 提示：动能 = 总能量 - 静止能量
    KE = (gamma - 1) * m * c**2  # 修改这里
    return KE


def rest_energy(m):
    """
    静止能量 Rest energy

    公式 Formula: E₀ = mc²

    这就是爱因斯坦著名的质能等价公式！
    1 kg 的质量等价于约 9×10¹⁶ J 的能量。
    """
    return m * c**2


def verify_energy_momentum_relation(m, v):
    """
    验证能量-动量关系 Verify energy-momentum relation

    公式 Formula: E² = (pc)² + (mc²)²

    这是洛伦兹不变量，在所有参考系中成立。
    对于光子（m=0）：E = pc
    对于静止粒子（p=0）：E = mc²
    """
    E = relativistic_energy(m, v)
    p = relativistic_momentum(m, v)
    E0 = rest_energy(m)

    # TODO: 计算并比较
    # 从能量-动量关系计算能量
    E_from_relation = np.sqrt((p * c)**2 + E0**2)
    return np.isclose(E, E_from_relation)


# =============================================================================
# 练习 1.7: 时空图（闵可夫斯基图）
# Exercise 1.7: Spacetime Diagram (Minkowski Diagram)
#
# 物理背景：时空图是可视化相对论效应的重要工具。
# 横轴表示空间坐标 x，纵轴表示时间 t（或 ct）。
# 光锥：所有光线的世界线，斜率为 ±1（当使用 ct 作为纵轴时）。
# 世界线：粒子在时空中的轨迹，斜率的倒数表示速度。
#
# Physical background: Spacetime diagrams visualize relativistic effects.
# Light cone: worldlines of all light rays, slope = ±1 (when using ct as axis)
# =============================================================================

def plot_spacetime_diagram():
    """绘制时空图 Plot spacetime diagram"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # 左图: 世界线和光锥
    ax1 = axes[0]

    # 光锥
    t = np.linspace(0, 5, 100)
    ax1.plot(c*t/1e8, t, 'y-', label='Light cone', linewidth=2)
    ax1.plot(-c*t/1e8, t, 'y-', linewidth=2)
    ax1.fill_between(c*t/1e8, t, -c*t/1e8, alpha=0.1, color='yellow')

    # 静止物体世界线
    ax1.plot([0, 0], [0, 5], 'b-', linewidth=2, label='At rest')

    # 匀速运动物体 (v = 0.5c)
    v1 = 0.5 * c
    ax1.plot(v1*t/1e8, t, 'r-', linewidth=2, label='v = 0.5c')

    # 加速物体
    a = 0.1 * c  # 加速度
    x_acc = 0.5 * a * t**2 / 1e8
    ax1.plot(x_acc, t, 'g-', linewidth=2, label='Accelerating')

    ax1.set_xlabel('x (×10⁸ m)')
    ax1.set_ylabel('t (s)')
    ax1.set_title('时空图 Spacetime Diagram')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(-5, 5)

    # 右图: 洛伦兹变换后的坐标系
    ax2 = axes[1]

    # 原始坐标系
    ax2.axhline(y=0, color='blue', linestyle='-', label="S: t=0")
    ax2.axvline(x=0, color='blue', linestyle='-', label="S: x=0")

    # 变换后的坐标系 (v = 0.6c)
    v = 0.6 * c
    beta = v / c

    # t'=0 线: t = βx/c (在x-ct图中: ct = βx)
    x_range = np.linspace(-4, 4, 100)
    ax2.plot(x_range, beta * x_range, 'r-', linewidth=2, label="S': t'=0")

    # x'=0 线: x = vt (在x-ct图中: x = βct)
    ct_range = np.linspace(-4, 4, 100)
    ax2.plot(beta * ct_range, ct_range, 'r--', linewidth=2, label="S': x'=0")

    # 光锥
    ax2.plot(x_range, x_range, 'y-', linewidth=1.5, alpha=0.7)
    ax2.plot(x_range, -x_range, 'y-', linewidth=1.5, alpha=0.7)

    ax2.set_xlabel('x/c (s)')
    ax2.set_ylabel('t (s)')
    ax2.set_title("洛伦兹变换坐标系 (v=0.6c)")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(-4, 4)
    ax2.set_ylim(-4, 4)
    ax2.set_aspect('equal')

    plt.tight_layout()
    plt.savefig('special_relativity.png', dpi=150)
    print("图像已保存为 special_relativity.png")
    plt.show()


# =============================================================================
# 可视化：相对论效应图示
# Visualization: Relativistic Effects
# =============================================================================

def plot_relativistic_effects():
    """
    绘制相对论效应 Plot relativistic effects

    图1: 洛伦兹因子 γ vs 速度
    图2: 时间膨胀 Δt/Δt₀ vs 速度
    图3: 长度收缩 L/L₀ vs 速度
    图4: 相对论动能 vs 经典动能
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    v_range = np.linspace(0, 0.99*c, 100)
    beta_range = v_range / c

    # 1. 洛伦兹因子
    ax1 = axes[0, 0]
    gamma_range = 1 / np.sqrt(1 - beta_range**2)
    ax1.plot(beta_range, gamma_range, 'b-', linewidth=2)
    ax1.set_xlabel('v/c')
    ax1.set_ylabel('γ')
    ax1.set_title('洛伦兹因子 Lorentz Factor')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 10)

    # 2. 时间膨胀
    ax2 = axes[0, 1]
    ax2.plot(beta_range, gamma_range, 'r-', linewidth=2)
    ax2.set_xlabel('v/c')
    ax2.set_ylabel('Δt/Δt₀ = γ')
    ax2.set_title('时间膨胀 Time Dilation')
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 10)

    # 3. 长度收缩
    ax3 = axes[1, 0]
    ax3.plot(beta_range, 1/gamma_range, 'g-', linewidth=2)
    ax3.set_xlabel('v/c')
    ax3.set_ylabel('L/L₀ = 1/γ')
    ax3.set_title('长度收缩 Length Contraction')
    ax3.grid(True, alpha=0.3)

    # 4. 动能对比
    ax4 = axes[1, 1]
    # 相对论动能
    KE_rel = (gamma_range - 1) * m_e * c**2 / MeV
    # 经典动能
    KE_class = 0.5 * m_e * v_range**2 / MeV
    ax4.plot(beta_range, KE_rel, 'b-', linewidth=2, label='Relativistic')
    ax4.plot(beta_range, KE_class, 'r--', linewidth=2, label='Classical')
    ax4.set_xlabel('v/c')
    ax4.set_ylabel('KE (MeV)')
    ax4.set_title('动能对比 Kinetic Energy Comparison')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim(0, 5)

    plt.tight_layout()
    plt.savefig('relativistic_effects.png', dpi=150)
    print("图像已保存为 relativistic_effects.png")
    plt.show()


# =============================================================================
# 验证函数
# Verification Function
# =============================================================================
def verify():
    """
    验证所有练习的正确性 Verify all exercises

    检查内容：
    1.1 洛伦兹因子计算
    1.2 时间膨胀效应
    1.3 长度收缩效应
    1.4 洛伦兹变换的自洽性
    1.5 速度叠加公式（结果不超光速）
    1.6 能量-动量关系
    """
    all_passed = True

    # 检查 1.1 - 洛伦兹因子
    # Check 1.1 - Lorentz factor
    expected_gamma = 1 / np.sqrt(1 - 0.9**2)  # γ ≈ 2.294
    if not np.isclose(gamma_test, expected_gamma, rtol=0.01):
        print(f"错误 1.1 洛伦兹因子计算错误: 期望 {expected_gamma:.3f}, 得到 {gamma_test:.3f}")
        all_passed = False
    else:
        print(f"通过 1.1 洛伦兹因子正确 (v=0.9c 时 γ = {gamma_test:.3f})")

    # 检查 1.2 - 时间膨胀
    # Check 1.2 - Time dilation
    expected_years = 1.0 / np.sqrt(1 - 0.8**2)  # ≈ 1.667 years
    if not np.isclose(years_on_earth, expected_years, rtol=0.01):
        print(f"错误 1.2 时间膨胀计算错误: 期望 {expected_years:.3f} 年, 得到 {years_on_earth:.3f} 年")
        all_passed = False
    else:
        print(f"通过 1.2 时间膨胀正确 (飞船上1年 = 地球上{years_on_earth:.3f}年)")

    # 检查 1.3 - 长度收缩
    # Check 1.3 - Length contraction
    gamma_09 = 1 / np.sqrt(1 - 0.9**2)
    expected_L = L0 / gamma_09
    if not np.isclose(L_contracted, expected_L, rtol=0.01):
        print(f"错误 1.3 长度收缩计算错误: 期望 {expected_L:.2f} m, 得到 {L_contracted:.2f} m")
        all_passed = False
    else:
        print(f"通过 1.3 长度收缩正确 (100m 在 0.9c 时收缩为 {L_contracted:.2f}m)")

    # 检查 1.4 - 洛伦兹变换
    # Check 1.4 - Lorentz transform
    x_test, t_test = 1e8, 1.0  # x = 10^8 m, t = 1 s
    v_test = 0.5 * c
    x_p, t_p = lorentz_transform(x_test, t_test, v_test)
    x_back, t_back = inverse_lorentz_transform(x_p, t_p, v_test)
    if not (np.isclose(x_back, x_test, rtol=0.01) and np.isclose(t_back, t_test, rtol=0.01)):
        print("错误 1.4 洛伦兹变换与逆变换不自洽")
        all_passed = False
    else:
        print("通过 1.4 洛伦兹变换正确（正变换-逆变换自洽）")

    # 检查 1.5 - 速度叠加
    # Check 1.5 - Velocity addition
    if relative_v >= c:
        print(f"错误 1.5 速度叠加结果超过光速: {relative_v/c:.4f}c >= c")
        all_passed = False
    else:
        expected_v = (0.9 + 0.9) / (1 + 0.9*0.9) * c  # ≈ 0.9945c
        if not np.isclose(relative_v, expected_v, rtol=0.01):
            print(f"错误 1.5 速度叠加计算错误: 期望 {expected_v/c:.4f}c, 得到 {relative_v/c:.4f}c")
            all_passed = False
        else:
            print(f"通过 1.5 速度叠加正确 (0.9c + 0.9c = {relative_v/c:.4f}c < c)")

    # 检查 1.6 - 能量-动量关系
    # Check 1.6 - Energy-momentum relation
    if not verify_energy_momentum_relation(m_e, 0.8*c):
        print("错误 1.6 能量-动量关系 E² = (pc)² + (mc²)² 验证失败")
        all_passed = False
    else:
        E = relativistic_energy(m_e, 0.8*c)
        KE = kinetic_energy(m_e, 0.8*c)
        print(f"通过 1.6 能量-动量关系正确 (E² = (pc)² + (mc²)²)")
        print(f"     电子在 v=0.8c 时: 总能量 E = {E/MeV:.3f} MeV, 动能 KE = {KE/MeV:.3f} MeV")

    if all_passed:
        print("\n所有测试通过！正在生成可视化图像...")
        print("All tests passed! Generating visualizations...")
        try:
            plot_relativistic_effects()
            plot_spacetime_diagram()
        except Exception as e:
            print(f"可视化生成失败 Visualization failed: {e}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("洛伦兹变换与狭义相对论 Special Relativity")
    print("=" * 50)
    verify()
