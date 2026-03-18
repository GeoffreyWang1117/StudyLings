"""
轨道力学 Orbital Mechanics
难度 Difficulty: ★★★★

================================================================================
学习目标 Learning Objectives
================================================================================
- 理解万有引力定律和开普勒三大定律
  Understand Newton's law of gravitation and Kepler's three laws
- 使用数值方法模拟行星轨道运动
  Simulate planetary orbital motion using numerical methods
- 分析轨道能量和角动量守恒
  Analyze conservation of orbital energy and angular momentum
- 计算逃逸速度和轨道转移
  Calculate escape velocity and orbital transfers

================================================================================
物理背景 Physical Background
================================================================================
1. 万有引力定律 Newton's Law of Gravitation:
   F = -GMm/r² * r_hat
   其中 G = 6.674×10⁻¹¹ N·m²/kg² 是万有引力常数
   负号表示引力是吸引力，指向引力源

2. 开普勒三大定律 Kepler's Three Laws:
   第一定律（椭圆轨道）: 行星绕太阳运动的轨道是椭圆，太阳在椭圆的一个焦点上
   第二定律（面积定律）: 行星与太阳的连线在相等时间内扫过相等的面积（角动量守恒）
   第三定律（周期定律）: T² = (4π²/GM) * a³，周期的平方与半长轴的立方成正比

3. 轨道类型 Orbit Types:
   - 圆轨道 Circular: e = 0
   - 椭圆轨道 Elliptical: 0 < e < 1（束缚轨道）
   - 抛物线轨道 Parabolic: e = 1（刚好逃逸）
   - 双曲线轨道 Hyperbolic: e > 1（逃逸轨道）

4. 重要公式 Key Formulas:
   - 圆轨道速度: v = sqrt(GM/r)
   - 逃逸速度: v_escape = sqrt(2GM/r) = sqrt(2) * v_circular
   - 轨道能量: E = -GMm/(2a)（对于椭圆轨道）
   - 角动量: L = m * r * v_perp（垂直于径向的速度分量）

HINT: 万有引力: F = -GMm/r² * r_hat（指向引力源的单位向量）
HINT: 开普勒第三定律: T² = (4π²/GM) * a³
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.physics_helpers import integrate_ode, magnitude
from utils.constants import G, M_sun, AU

# I AM NOT DONE

# =============================================================================
# 练习 6.1: 开普勒定律验证
# Exercise 6.1: Kepler's Laws Verification
# =============================================================================
# 物理背景 Physical Background:
# 开普勒第三定律是牛顿万有引力定律的直接推论。它建立了轨道周期与轨道大小的定量关系。
# 这个定律不仅适用于行星，也适用于任何绕中心天体运动的物体（如卫星、月球等）。
#
# 推导过程 Derivation:
# 对于圆轨道：向心力 = 万有引力
# mv²/r = GMm/r² → v = sqrt(GM/r)
# 周期 T = 2πr/v = 2πr/sqrt(GM/r) = 2π*sqrt(r³/GM)
# 对于椭圆轨道，r 替换为半长轴 a
#
# 题目 Problem:
# 地球绕太阳运动的参数 Earth's orbital parameters:
# 半长轴 a = 1 AU = 1.496×10¹¹ m
# 轨道周期 T = 1 年 = 3.156×10⁷ s
#
# 使用开普勒第三定律计算周期，验证与实际周期的一致性
# Calculate period using Kepler's Third Law and verify consistency
#
# 公式 Formula: T = 2π * sqrt(a³/(GM))
# 单位 Unit: 秒 (s)

a_earth = 1.0 * AU  # 地球轨道半长轴 Earth's semi-major axis
T_earth = 365.25 * 24 * 3600  # 地球实际轨道周期（秒）actual orbital period

# TODO: 使用开普勒第三定律计算周期，并与实际周期比较
# 提示：T = 2 * np.pi * np.sqrt(a_earth**3 / (G * M_sun))
T_calculated = None  # 修改这里 (单位：s)


# =============================================================================
# 练习 6.2: 轨道模拟 - 圆轨道
# Exercise 6.2: Orbital Simulation - Circular Orbit
# =============================================================================
# 物理背景 Physical Background:
# 轨道模拟需要数值求解牛顿运动方程。在引力场中，加速度由万有引力定律给出。
#
# 运动方程 Equations of Motion:
# 状态向量: y = [x, y, vx, vy]（位置和速度）
# dx/dt = vx, dy/dt = vy（速度）
# dvx/dt = ax, dvy/dt = ay（加速度）
#
# 引力加速度 Gravitational Acceleration:
# a = F/m = -GM/r² * r_hat = -GM/r³ * r_vec
# 分量形式: ax = -GM*x/r³, ay = -GM*y/r³
#
# 圆轨道条件 Circular Orbit Condition:
# 初始速度垂直于位置向量，大小为 v = sqrt(GM/r)

def gravitational_acceleration(x, y, M=M_sun):
    """
    计算万有引力产生的加速度
    Calculate gravitational acceleration

    参数 Parameters:
        x, y: 位置坐标（相对于中心天体）
        M: 中心天体质量

    返回 Returns:
        (ax, ay): 加速度分量

    物理公式 Physics:
        a = -GM/r³ * r = (-GM*x/r³, -GM*y/r³)
        负号表示加速度指向中心天体（吸引力）
    """
    r = np.sqrt(x**2 + y**2)  # 到中心天体的距离
    # 加速度分量（指向中心天体）
    ax = -G * M * x / r**3
    ay = -G * M * y / r**3
    return ax, ay


def orbital_derivatives(state, t, M=M_sun):
    """
    轨道运动的导数函数（供ODE求解器使用）
    Derivative function for orbital motion

    参数 Parameters:
        state: 状态向量 [x, y, vx, vy]
        t: 时间
        M: 中心天体质量

    返回 Returns:
        导数数组 [vx, vy, ax, ay]
    """
    x, y, vx, vy = state
    ax, ay = gravitational_acceleration(x, y, M)
    return np.array([vx, vy, ax, ay])


def simulate_orbit(r0, v0, M=M_sun, t_end=None, dt=3600):
    """
    模拟轨道运动
    r0: 初始位置 [x, y]
    v0: 初始速度 [vx, vy]
    """
    if t_end is None:
        t_end = 365.25 * 24 * 3600  # 1 year

    state0 = np.array([r0[0], r0[1], v0[0], v0[1]])

    def dydt(y, t):
        return orbital_derivatives(y, t, M)

    t, states = integrate_ode(dydt, state0, (0, t_end), dt, method='rk4')
    return t, states[:, 0], states[:, 1], states[:, 2], states[:, 3]


# 圆轨道初始条件
# 圆轨道速度: v = sqrt(GM/r)
r0_circular = [AU, 0]  # 初始位置
v_circular = np.sqrt(G * M_sun / AU)  # 圆轨道速度
v0_circular = [0, v_circular]  # 初始速度（垂直于位置向量）

# 运行模拟
t_circ, x_circ, y_circ, vx_circ, vy_circ = simulate_orbit(r0_circular, v0_circular)


# =============================================================================
# 练习 6.3: 椭圆轨道
# Exercise 6.3: Elliptical Orbit
# =============================================================================
# 通过改变初始速度来产生椭圆轨道
# 初速度小于圆轨道速度 -> 内落椭圆
# 初速度大于圆轨道速度 -> 外扩椭圆

# TODO: 设置一个椭圆轨道的初始速度（尝试1.2倍圆轨道速度）
v0_ellipse = [0, 1.2 * v_circular]  # 修改这里（可以尝试不同值）
t_ellip, x_ellip, y_ellip, vx_ellip, vy_ellip = simulate_orbit(
    r0_circular, v0_ellipse, t_end=2*365.25*24*3600
)


# =============================================================================
# 练习 6.4: 角动量守恒
# Exercise 6.4: Conservation of Angular Momentum
# =============================================================================
# 物理背景 Physical Background:
# 角动量是转动的"惯性"，在中心力场中守恒。这是开普勒第二定律的数学表达。
# 角动量守恒意味着行星在近日点速度快，远日点速度慢（等面积定律）。
#
# 公式 Formula:
# 角动量 L = r × p = m(r × v)
# 在二维中（r和v都在xy平面内）: L = m(x*vy - y*vx)，方向沿z轴
# 比角动量（单位质量的角动量）: L/m = x*vy - y*vx
#
# 守恒条件: 力矩为零 τ = r × F = 0
# 中心力 F 与 r 平行，所以叉积为零，角动量守恒

def calculate_angular_momentum(x, y, vx, vy):
    """
    计算比角动量（单位质量的角动量）
    Calculate specific angular momentum (angular momentum per unit mass)

    参数 Parameters:
        x, y: 位置坐标
        vx, vy: 速度分量

    返回 Returns:
        L/m = x*vy - y*vx（二维叉积的z分量）

    注意: 正值表示逆时针运动，负值表示顺时针运动
    """
    # L/m = r × v 的z分量 = x*vy - y*vx
    L = x * vy - y * vx
    return L


# 计算角动量随时间变化
L_circ = calculate_angular_momentum(x_circ, y_circ, vx_circ, vy_circ)
L_ellip = calculate_angular_momentum(x_ellip, y_ellip, vx_ellip, vy_ellip)


# =============================================================================
# 练习 6.5: 轨道能量
# Exercise 6.5: Orbital Energy
# =============================================================================
# 物理背景 Physical Background:
# 轨道总能量是动能和势能之和，在无其他力作用时守恒。
# 能量决定了轨道的类型和大小。
#
# 公式 Formulas:
# - 动能: KE = (1/2)mv²
# - 势能: PE = -GMm/r（取无穷远处为零势能点）
# - 总能量: E = KE + PE = (1/2)mv² - GMm/r
# - 比能量（单位质量）: E/m = (1/2)v² - GM/r
#
# 能量与轨道类型 Energy and Orbit Type:
# - E < 0: 束缚轨道（椭圆），E = -GM/(2a)
# - E = 0: 抛物线轨道（刚好逃逸）
# - E > 0: 双曲线轨道（逃逸）

def calculate_orbital_energy(x, y, vx, vy, M=M_sun):
    """
    计算比轨道能量（单位质量的轨道能量）
    Calculate specific orbital energy

    参数 Parameters:
        x, y: 位置坐标
        vx, vy: 速度分量
        M: 中心天体质量

    返回 Returns:
        E/m = (1/2)v² - GM/r

    能量符号意义:
        E < 0: 束缚轨道（椭圆或圆）
        E = 0: 抛物线轨道
        E > 0: 双曲线轨道
    """
    r = np.sqrt(x**2 + y**2)
    v_sq = vx**2 + vy**2
    # 比能量 = 动能/m - 势能/m
    E = 0.5 * v_sq - G * M / r
    return E


# 计算能量
E_circ = calculate_orbital_energy(x_circ, y_circ, vx_circ, vy_circ)
E_ellip = calculate_orbital_energy(x_ellip, y_ellip, vx_ellip, vy_ellip)


# =============================================================================
# 练习 6.6: 逃逸速度
# Exercise 6.6: Escape Velocity
# =============================================================================
# 物理背景 Physical Background:
# 逃逸速度是物体摆脱引力束缚所需的最小速度。
# 当物体的总能量恰好为零时，它将沿抛物线轨道运动到无穷远。
#
# 推导 Derivation:
# 逃逸条件: 总能量 E = 0
# (1/2)mv² - GMm/r = 0
# v_escape = sqrt(2GM/r)
#
# 重要关系 Important Relation:
# v_escape = sqrt(2) * v_circular
# 即：逃逸速度是同一位置圆轨道速度的 sqrt(2) ≈ 1.414 倍
#
# 应用 Applications:
# - 发射宇宙飞船
# - 判断陨石能否逃逸行星
# - 研究星系和恒星的形成
#
# 单位 Unit: m/s

# TODO: 计算地球轨道处（1 AU处）相对于太阳的逃逸速度
# 提示：v_escape = np.sqrt(2 * G * M_sun / AU)
v_escape = None  # 修改这里 (单位：m/s)

# TODO: 计算逃逸速度与圆轨道速度的比值
# 提示：v_escape / v_circular = sqrt(2)
ratio = None  # 修改这里 (应该等于 sqrt(2) ≈ 1.414)


# =============================================================================
# 可视化
# =============================================================================
def plot_orbits():
    """绘制轨道图"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # 1. 轨道形状
    ax1 = axes[0, 0]
    ax1.plot(x_circ/AU, y_circ/AU, 'b-', label='Circular', alpha=0.8)
    ax1.plot(x_ellip/AU, y_ellip/AU, 'r-', label='Elliptical', alpha=0.8)
    ax1.plot(0, 0, 'yo', markersize=15, label='Sun')
    ax1.set_xlabel('x (AU)')
    ax1.set_ylabel('y (AU)')
    ax1.set_title('轨道形状 Orbital Shapes')
    ax1.set_aspect('equal')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 角动量守恒
    ax2 = axes[0, 1]
    t_years = t_circ / (365.25 * 24 * 3600)
    ax2.plot(t_years, L_circ/1e15, 'b-', label='Circular')
    t_ellip_years = np.linspace(0, 2, len(L_ellip))
    ax2.plot(t_ellip_years, L_ellip/1e15, 'r-', label='Elliptical')
    ax2.set_xlabel('Time (years)')
    ax2.set_ylabel('L/m (×10¹⁵ m²/s)')
    ax2.set_title('角动量守恒 Angular Momentum Conservation')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 能量守恒
    ax3 = axes[1, 0]
    ax3.plot(t_years, E_circ/1e8, 'b-', label='Circular')
    ax3.plot(t_ellip_years, E_ellip/1e8, 'r-', label='Elliptical')
    ax3.set_xlabel('Time (years)')
    ax3.set_ylabel('E/m (×10⁸ J/kg)')
    ax3.set_title('轨道能量 Orbital Energy')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 速度大小
    ax4 = axes[1, 1]
    v_circ_mag = np.sqrt(vx_circ**2 + vy_circ**2) / 1000
    v_ellip_mag = np.sqrt(vx_ellip**2 + vy_ellip**2) / 1000
    ax4.plot(t_years, v_circ_mag, 'b-', label='Circular')
    ax4.plot(t_ellip_years, v_ellip_mag, 'r-', label='Elliptical')
    ax4.axhline(y=v_circular/1000, color='b', linestyle='--', alpha=0.5, label='v_circular')
    if v_escape is not None:
        ax4.axhline(y=v_escape/1000, color='g', linestyle='--', alpha=0.5, label='v_escape')
    ax4.set_xlabel('Time (years)')
    ax4.set_ylabel('Speed (km/s)')
    ax4.set_title('轨道速度 Orbital Speed')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('orbital_mechanics.png', dpi=150)
    print("图像已保存为 orbital_mechanics.png")
    plt.show()


# =============================================================================
# 验证函数
# =============================================================================
def verify():
    """Verify all exercises"""
    all_passed = True

    # Check 6.1 - Kepler's Third Law
    expected_T = 2 * np.pi * np.sqrt(a_earth**3 / (G * M_sun))
    if T_calculated is None:
        print("❌ 6.1 开普勒第三定律未完成")
        all_passed = False
    elif not np.isclose(T_calculated, expected_T, rtol=0.01):
        print(f"❌ 6.1 周期计算错误: 期望 {expected_T/86400:.1f} 天, 得到 {T_calculated/86400:.1f} 天")
        all_passed = False
    else:
        error = abs(T_calculated - T_earth) / T_earth * 100
        print(f"✓ 6.1 开普勒第三定律验证正确 (计算周期: {T_calculated/86400:.1f} 天, 误差: {error:.2f}%)")

    # Check 6.2 - Circular orbit
    if len(x_circ) > 100:
        # Check orbit is roughly circular
        r_values = np.sqrt(x_circ**2 + y_circ**2)
        r_variation = (np.max(r_values) - np.min(r_values)) / np.mean(r_values)
        if r_variation > 0.05:  # 5% tolerance
            print(f"❌ 6.2 圆轨道偏心率过大: {r_variation*100:.1f}%")
            all_passed = False
        else:
            print(f"✓ 6.2 圆轨道模拟正确 (半径变化: {r_variation*100:.2f}%)")
    else:
        print("❌ 6.2 轨道模拟数据不足")
        all_passed = False

    # Check 6.3 - Elliptical orbit
    if len(x_ellip) > 100:
        r_ellip = np.sqrt(x_ellip**2 + y_ellip**2)
        eccentricity = (np.max(r_ellip) - np.min(r_ellip)) / (np.max(r_ellip) + np.min(r_ellip))
        if eccentricity < 0.01:
            print("❌ 6.3 椭圆轨道偏心率过小")
            all_passed = False
        else:
            print(f"✓ 6.3 椭圆轨道正确 (偏心率约: {eccentricity:.3f})")
    else:
        print("❌ 6.3 椭圆轨道数据不足")
        all_passed = False

    # Check 6.4 - Angular momentum conservation
    L_variation = (np.max(L_circ) - np.min(L_circ)) / np.mean(L_circ)
    if L_variation > 0.01:
        print(f"❌ 6.4 角动量不守恒: 变化 {L_variation*100:.2f}%")
        all_passed = False
    else:
        print(f"✓ 6.4 角动量守恒验证正确 (变化 < 1%)")

    # Check 6.5 - Energy conservation
    E_variation = (np.max(E_circ) - np.min(E_circ)) / abs(np.mean(E_circ))
    if E_variation > 0.01:
        print(f"❌ 6.5 能量不守恒: 变化 {E_variation*100:.2f}%")
        all_passed = False
    else:
        print(f"✓ 6.5 轨道能量守恒正确 (变化 < 1%)")

    # Check 6.6 - Escape velocity
    expected_v_escape = np.sqrt(2 * G * M_sun / AU)
    expected_ratio = np.sqrt(2)
    if v_escape is None or ratio is None:
        print("❌ 6.6 逃逸速度未完成")
        all_passed = False
    elif not np.isclose(v_escape, expected_v_escape, rtol=0.01):
        print(f"❌ 6.6 逃逸速度错误: 期望 {expected_v_escape/1000:.2f} km/s, 得到 {v_escape/1000:.2f} km/s")
        all_passed = False
    elif not np.isclose(ratio, expected_ratio, rtol=0.01):
        print(f"❌ 6.6 速度比值错误: 期望 √2 ≈ {expected_ratio:.4f}, 得到 {ratio:.4f}")
        all_passed = False
    else:
        print(f"✓ 6.6 逃逸速度正确 (v_escape = {v_escape/1000:.2f} km/s, ratio = √2)")

    if all_passed:
        print("\n🎉 所有测试通过！正在生成可视化...")
        try:
            plot_orbits()
        except Exception as e:
            print(f"可视化生成失败: {e}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("轨道力学 Orbital Mechanics")
    print("=" * 50)
    verify()
