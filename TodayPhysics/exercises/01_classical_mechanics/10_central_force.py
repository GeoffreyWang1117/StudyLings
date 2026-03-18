"""
中心力与有效势能 Central Force and Effective Potential
难度 Difficulty: ★★★★

================================================================================
学习目标 Learning Objectives
================================================================================
- 理解中心力场的守恒量（能量和角动量）
  Understand conserved quantities in central force fields (energy and angular momentum)
- 掌握有效势能方法简化二维问题为一维问题
  Master the effective potential method to reduce 2D problems to 1D
- 分析开普勒问题和轨道分类
  Analyze Kepler problem and orbit classification
- 计算轨道参数（半长轴、偏心率、近日点/远日点）
  Calculate orbital parameters (semi-major axis, eccentricity, perihelion/aphelion)

================================================================================
物理背景 Physical Background
================================================================================
中心力场是指力始终指向（或背离）某一固定点的力场。

1. 角动量守恒 Conservation of Angular Momentum:
   L = mr²φ̇ = 常数
   - 中心力对原点的力矩为零，故角动量守恒
   - 运动限制在固定平面内

2. 有效势能 Effective Potential:
   V_eff(r) = V(r) + L²/(2mr²)
   - 第一项: 真实势能（如引力势能 V = -GMm/r）
   - 第二项: 离心势能，来自角动量约束
   - 将二维问题化简为一维径向运动

3. 轨道分类（引力场）Orbit Classification:
   - E < 0: 束缚轨道（椭圆或圆）
   - E = 0: 临界逃逸（抛物线）
   - E > 0: 非束缚轨道（双曲线）

4. 开普勒轨道参数 Kepler Orbital Parameters:
   - 半长轴: a = -GMm/(2E)（对于束缚轨道）
   - 偏心率: e = √(1 + 2EL²/(G²M²m³))
   - 极坐标方程: r = p/(1 + e·cos(φ))，其中 p = L²/(GMm²)

5. 霍曼转移轨道 Hohmann Transfer:
   - 在两个圆轨道之间最节能的转移方式
   - 转移轨道是一个椭圆，与两个圆轨道相切

HINT: 中心力场角动量守恒: L = mr²φ̇ = 常数
HINT: 有效势能: V_eff = V(r) + L²/(2mr²)
HINT: 轨道能量决定轨道类型: E < 0 束缚态, E ≥ 0 散射态
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import G, M_sun, AU

# I AM NOT DONE

# =============================================================================
# 练习 10.1: 有效势能
# Exercise 10.1: Effective Potential
# =============================================================================
# 有效势能将二维中心力问题化简为一维径向运动问题
# 物理意义：离心势能代表维持角动量守恒所需的"势垒"
# 单位：V_eff [J], r [m], L [kg·m²/s], m [kg], M [kg]

def gravitational_potential(r, M, m):
    """
    引力势能 Gravitational Potential Energy
    V = -GMm/r

    参数 Parameters:
        r: 到引力中心的距离 [m]
        M: 中心天体质量 [kg]
        m: 轨道物体质量 [kg]
    返回 Returns:
        引力势能 [J]（负值表示束缚态）
    """
    return -G * M * m / r

def effective_potential(r, L, m, M):
    """
    有效势能 Effective Potential
    V_eff = V(r) + L²/(2mr²)
         = -GMm/r + L²/(2mr²)

    包含两部分：
    1. 引力势能 -GMm/r（吸引，随r增大趋于0）
    2. 离心势能 L²/(2mr²)（排斥，随r减小急剧增大）

    参数 Parameters:
        r: 径向距离 [m]
        L: 角动量 [kg·m²/s]
        m: 轨道物体质量 [kg]
        M: 中心天体质量 [kg]
    返回 Returns:
        有效势能 [J]
    """
    V = gravitational_potential(r, M, m)
    # TODO: 计算有效势能（加入离心势能项）
    V_eff = V + L**2 / (2 * m * r**2)
    return V_eff

def centrifugal_potential(r, L, m):
    """
    离心势能 Centrifugal Potential
    V_c = L²/(2mr²)

    来源于角动量守恒的约束效应
    当粒子试图靠近中心时，必须加速旋转以保持L不变
    这种效应等效于一个向外的排斥势
    """
    return L**2 / (2 * m * r**2)


# =============================================================================
# 练习 10.2: 轨道能量
# Exercise 10.2: Orbital Energy
# =============================================================================
# 轨道总能量决定了轨道的类型（束缚或散射）
# 能量守恒：E = (1/2)mṙ² + V_eff(r) = 常数

def orbital_energy(r, v_r, L, m, M):
    """
    轨道总能量 Total Orbital Energy
    E = (1/2)mṙ² + V_eff(r)
      = (1/2)mṙ² + (1/2)m(L/mr)² - GMm/r
      = 径向动能 + 离心势能 + 引力势能

    参数 Parameters:
        r: 径向距离 [m]
        v_r: 径向速度 ṙ [m/s]
        L: 角动量 [kg·m²/s]
        m: 轨道物体质量 [kg]
        M: 中心天体质量 [kg]
    返回 Returns:
        总能量 [J]
    """
    V_eff = effective_potential(r, L, m, M)
    # TODO: 计算总能量（径向动能 + 有效势能）
    E = 0.5 * m * v_r**2 + V_eff
    return E

def classify_orbit(E, m, M, L):
    """
    根据能量分类轨道 Classify Orbit by Energy

    轨道类型取决于总能量与有效势能最小值的关系：
    - E < 0: 束缚轨道（椭圆或圆形）- 粒子被束缚在有限区域
    - E = 0: 临界逃逸（抛物线）- 恰好能逃离到无穷远
    - E > 0: 散射轨道（双曲线）- 粒子来自无穷远又散射到无穷远

    返回 Returns:
        轨道类型字符串: "ellipse", "parabola", 或 "hyperbola"
    """
    if E < 0:
        return "ellipse"
    elif np.isclose(E, 0, atol=1e-10):
        return "parabola"
    else:
        return "hyperbola"


# =============================================================================
# 练习 10.3: 轨道参数
# Exercise 10.3: Orbital Parameters
# =============================================================================
# 开普勒轨道的几何参数完全由能量E和角动量L决定
# 这些参数描述了椭圆轨道的大小和形状

def semi_major_axis(E, m, M):
    """
    半长轴 Semi-major Axis
    a = -GMm/(2E)（仅对 E < 0 的椭圆轨道有意义）

    物理意义：椭圆的"平均半径"，决定轨道周期
    开普勒第三定律: T² ∝ a³

    参数 Parameters:
        E: 总能量 [J]（必须为负值才有有限半长轴）
        m: 轨道物体质量 [kg]
        M: 中心天体质量 [kg]
    返回 Returns:
        半长轴 [m]（若 E ≥ 0 返回无穷大）
    """
    if E >= 0:
        return np.inf
    # TODO: 计算半长轴
    a = -G * M * m / (2 * E)
    return a

def eccentricity(E, L, m, M):
    """
    偏心率 Eccentricity
    e = √(1 + 2EL²/(G²M²m³))

    几何意义：描述轨道的"扁平程度"
    - e = 0: 圆形轨道
    - 0 < e < 1: 椭圆轨道
    - e = 1: 抛物线轨道
    - e > 1: 双曲线轨道

    参数 Parameters:
        E: 总能量 [J]
        L: 角动量 [kg·m²/s]
        m: 轨道物体质量 [kg]
        M: 中心天体质量 [kg]
    返回 Returns:
        偏心率（无量纲）
    """
    # TODO: 计算偏心率
    e = np.sqrt(1 + 2 * E * L**2 / (G**2 * M**2 * m**3))
    return e

def perihelion_aphelion(a, e):
    """
    近日点和远日点距离 Perihelion and Aphelion Distances
    r_p = a(1-e)  近日点（最近点）
    r_a = a(1+e)  远日点（最远点）

    注意：仅对椭圆轨道 (e < 1) 有意义
    对于双曲线轨道，r_a < 0 无物理意义

    返回 Returns:
        (r_p, r_a): 近日点和远日点距离 [m]
    """
    r_p = a * (1 - e)
    r_a = a * (1 + e)
    return r_p, r_a


# =============================================================================
# 练习 10.4: 轨道方程
# Exercise 10.4: Orbital Equation
# =============================================================================
# 开普勒轨道的极坐标方程，描述了轨道的几何形状
# 这是圆锥曲线的焦点极坐标形式

def orbit_equation(phi, L, m, M, e):
    """
    极坐标下的轨道方程 Orbital Equation in Polar Coordinates
    r(φ) = p / (1 + e·cos(φ))

    其中 p = L²/(GMm²) 是半正焦弦（半通径）

    这是圆锥曲线的统一形式：
    - e = 0: 圆（r = p = 常数）
    - e < 1: 椭圆（φ = 0 为近日点）
    - e = 1: 抛物线
    - e > 1: 双曲线

    参数 Parameters:
        phi: 真近点角（从近日点测量）[rad]
        L: 角动量 [kg·m²/s]
        m: 轨道物体质量 [kg]
        M: 中心天体质量 [kg]
        e: 偏心率（无量纲）
    返回 Returns:
        轨道半径 r [m]
    """
    p = L**2 / (G * M * m**2)  # 半正焦弦 semi-latus rectum
    # TODO: 计算轨道半径（圆锥曲线极坐标方程）
    r = p / (1 + e * np.cos(phi))
    return r


# =============================================================================
# 练习 10.5: 圆轨道
# Exercise 10.5: Circular Orbit
# =============================================================================
# 圆轨道是椭圆轨道的特例（e = 0）
# 满足向心力 = 引力的条件: mv²/r = GMm/r²

def circular_orbit_velocity(r, M):
    """
    圆轨道速度 Circular Orbit Velocity
    v = √(GM/r)

    推导：向心加速度 = 引力加速度
    v²/r = GM/r² → v = √(GM/r)

    物理意义：在半径r处维持圆轨道所需的速度
    这也是该高度的第一宇宙速度

    参数 Parameters:
        r: 轨道半径 [m]
        M: 中心天体质量 [kg]
    返回 Returns:
        轨道速度 [m/s]
    """
    return np.sqrt(G * M / r)

def circular_orbit_angular_momentum(m, r, M):
    """
    圆轨道角动量 Circular Orbit Angular Momentum
    L = m·r·v = m√(GMr)

    圆轨道上角动量守恒，且等于 m×r×圆轨道速度
    """
    v = circular_orbit_velocity(r, M)
    return m * r * v

def circular_orbit_energy(m, r, M):
    """
    圆轨道能量 Circular Orbit Energy
    E = -GMm/(2r) = (1/2)V

    圆轨道能量恰好等于势能的一半（位力定理）
    动能 T = GMm/(2r) = -V/2
    总能量 E = T + V = V/2 = -GMm/(2r)
    """
    return -G * M * m / (2 * r)


# =============================================================================
# 练习 10.6: 转移轨道
# Exercise 10.6: Transfer Orbit (Hohmann Transfer)
# =============================================================================
# 霍曼转移是在两个共面圆轨道之间转移的最节能方式
# 转移轨道是一个椭圆，其近日点在内轨道，远日点在外轨道

def hohmann_transfer_delta_v(r1, r2, M):
    """
    霍曼转移轨道的速度增量 Hohmann Transfer Delta-V
    从半径 r1 的圆轨道转移到半径 r2 的圆轨道

    转移过程（假设 r1 < r2）：
    1. 在 r1 处加速进入转移椭圆（Δv₁）
    2. 沿转移椭圆运行半圈
    3. 在 r2 处加速进入目标圆轨道（Δv₂）

    转移椭圆的半长轴: a_transfer = (r1 + r2)/2
    利用能量守恒: v² = GM(2/r - 1/a)（vis-viva方程）

    参数 Parameters:
        r1: 初始圆轨道半径 [m]
        r2: 目标圆轨道半径 [m]
        M: 中心天体质量 [kg]
    返回 Returns:
        (delta_v1, delta_v2, total_delta_v): 两次速度增量和总增量 [m/s]
    """
    v1 = circular_orbit_velocity(r1, M)  # 初始圆轨道速度
    v2 = circular_orbit_velocity(r2, M)  # 目标圆轨道速度

    # 转移轨道参数
    a_transfer = (r1 + r2) / 2  # 转移椭圆半长轴
    # vis-viva方程计算转移轨道在两端点的速度
    v_transfer_1 = np.sqrt(G * M * (2/r1 - 1/a_transfer))
    v_transfer_2 = np.sqrt(G * M * (2/r2 - 1/a_transfer))

    # TODO: 计算两次速度增量
    delta_v1 = v_transfer_1 - v1  # 在近地点的速度增量
    delta_v2 = v2 - v_transfer_2  # 在远地点的速度增量
    total_delta_v = abs(delta_v1) + abs(delta_v2)

    return delta_v1, delta_v2, total_delta_v


# =============================================================================
# 可视化
# =============================================================================
def plot_effective_potential():
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 有效势能曲线
    ax1 = axes[0]
    m = 1.0  # 单位质量
    M = M_sun
    L_values = [1e15, 2e15, 3e15]  # 不同角动量

    r = np.linspace(0.1 * AU, 5 * AU, 500)

    for L in L_values:
        V_eff = effective_potential(r, L, m, M)
        ax1.plot(r/AU, V_eff/1e9, label=f'L = {L:.0e}')

    ax1.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    ax1.set_xlabel('r (AU)')
    ax1.set_ylabel('V_eff (×10⁹ J)')
    ax1.set_title('有效势能 Effective Potential')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(-5, 5)

    # 轨道形状
    ax2 = axes[1]
    phi = np.linspace(0, 2*np.pi, 500)

    for e in [0, 0.3, 0.6, 0.9]:
        L = circular_orbit_angular_momentum(m, AU, M)
        r = orbit_equation(phi, L, m, M, e)
        x = r * np.cos(phi)
        y = r * np.sin(phi)
        ax2.plot(x/AU, y/AU, label=f'e = {e}')

    ax2.plot(0, 0, 'yo', markersize=10)
    ax2.set_xlabel('x (AU)')
    ax2.set_ylabel('y (AU)')
    ax2.set_title('不同偏心率的轨道 Orbits')
    ax2.set_aspect('equal')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('central_force.png', dpi=150)
    print("图像已保存为 central_force.png")
    plt.show()


def verify():
    all_passed = True
    m = 1.0
    M = M_sun

    # Check 10.1
    L = circular_orbit_angular_momentum(m, AU, M)
    V_eff = effective_potential(AU, L, m, M)
    E_circ = circular_orbit_energy(m, AU, M)
    if not np.isclose(V_eff, E_circ, rtol=0.01):
        print("❌ 10.1 有效势能错误")
        all_passed = False
    else:
        print("✓ 10.1 有效势能正确")

    # Check 10.3
    E = circular_orbit_energy(m, AU, M)
    a = semi_major_axis(E, m, M)
    if not np.isclose(a, AU, rtol=0.01):
        print("❌ 10.3 半长轴计算错误")
        all_passed = False
    else:
        print(f"✓ 10.3 轨道参数正确 (a = {a/AU:.2f} AU)")

    # Check 10.5
    v_circ = circular_orbit_velocity(AU, M)
    expected_v = np.sqrt(G * M / AU)
    if not np.isclose(v_circ, expected_v, rtol=0.01):
        print("❌ 10.5 圆轨道速度错误")
        all_passed = False
    else:
        print(f"✓ 10.5 圆轨道正确 (v = {v_circ/1e3:.2f} km/s)")

    # Check 10.6
    dv1, dv2, total = hohmann_transfer_delta_v(AU, 1.524*AU, M)  # 地球到火星
    if total <= 0:
        print("❌ 10.6 霍曼转移错误")
        all_passed = False
    else:
        print(f"✓ 10.6 霍曼转移正确 (Δv_total = {total/1e3:.2f} km/s)")

    if all_passed:
        print("\n🎉 所有测试通过！")
        try:
            plot_effective_potential()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("中心力与有效势能 Central Force")
    print("=" * 50)
    verify()
