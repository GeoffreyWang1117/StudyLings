"""
史瓦西度规与黑洞物理 Schwarzschild Metric and Black Hole Physics
难度 Difficulty: ★★★★★

学习目标 Learning Objectives:
- 理解史瓦西度规的物理意义及其作为爱因斯坦场方程球对称真空解的重要性
- 计算引力红移和时间延迟，理解强引力场中的时空弯曲效应
- 了解事件视界、光子球和最内稳定圆轨道(ISCO)等黑洞关键特征
- 掌握潮汐力和自由落体的相对论性描述

物理背景 Physical Background:
史瓦西度规是Karl Schwarzschild于1916年发现的爱因斯坦场方程的第一个精确解。
它描述了球对称、静态、真空时空的几何结构，是理解黑洞物理的基础。
史瓦西黑洞具有以下关键特征：
  - 事件视界 (r = r_s): 信息无法逃逸的边界
  - 光子球 (r = 1.5 r_s): 光子可以绕黑洞做圆周运动的半径
  - 最内稳定圆轨道 ISCO (r = 3 r_s): 物质轨道稳定的最小半径

关键公式 Key Formulas:
  - 史瓦西半径 Schwarzschild radius: r_s = 2GM/c²
  - 史瓦西度规 Schwarzschild metric:
    ds² = -(1-r_s/r)c²dt² + (1-r_s/r)⁻¹dr² + r²(dθ² + sin²θ dφ²)
  - 引力红移 Gravitational redshift: z = 1/√(1-r_s/r) - 1
  - 时间膨胀 Time dilation: dτ/dt = √(1-r_s/r)

单位说明 Units:
  - 质量 Mass: kg (千克)
  - 长度 Length: m (米)
  - 时间 Time: s (秒)
  - 速度 Velocity: m/s
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import G, c, M_sun

# I AM NOT DONE

# =============================================================================
# 练习 1.1: 史瓦西半径
# Exercise 1.1: Schwarzschild Radius
#
# 物理背景 Physical Background:
# 史瓦西半径是定义黑洞事件视界的关键尺度。当一个物体的半径小于其
# 史瓦西半径时，它就会坍缩成黑洞。这个半径也被称为"引力半径"。
#
# 公式推导 Formula Derivation:
# 从牛顿引力逃逸速度 v_esc = √(2GM/r) = c 可以得到经典估算，
# 而精确结果来自广义相对论中度规的奇点分析。
#
# 典型值 Typical Values:
# - 太阳: r_s ≈ 2.95 km
# - 地球: r_s ≈ 8.87 mm
# - 质子: r_s ≈ 2.48 × 10^-54 m
# =============================================================================
def schwarzschild_radius(M):
    """
    计算史瓦西半径 Calculate Schwarzschild radius

    公式 Formula: r_s = 2GM/c²

    参数 Parameters:
        M: 质量 Mass (kg)

    返回 Returns:
        r_s: 史瓦西半径 Schwarzschild radius (m)
    """
    # TODO: 计算史瓦西半径
    # 提示：使用万有引力常数G和光速c
    r_s = 2 * G * M / c**2  # 修改这里
    return r_s


# 计算不同天体的史瓦西半径
r_s_sun = schwarzschild_radius(M_sun)
r_s_earth = schwarzschild_radius(5.972e24)  # 地球


# =============================================================================
# 练习 1.2: 引力红移
# Exercise 1.2: Gravitational Redshift
#
# 物理背景 Physical Background:
# 引力红移是广义相对论的重要预言之一。当光从强引力场区域传播到弱引力场
# 区域时，会损失能量，表现为波长变长（红移）。这是1960年Pound-Rebka
# 实验验证的效应。
#
# 物理解释 Physical Interpretation:
# - 光子"爬出"引力势阱时需要消耗能量
# - 能量降低导致频率降低：E = hν
# - 从黑洞视界附近发出的光会被无限红移
#
# 公式说明 Formula Explanation:
# 在引力场中，光的频率会发生红移
# ν_obs/ν_emit = √((1 - r_s/r_emit) / (1 - r_s/r_obs))
# 当观察者在无穷远处 (r_obs → ∞) 时: ν_∞/ν_emit = √(1 - r_s/r_emit)
# =============================================================================

def gravitational_redshift(r_emit, r_s):
    """
    计算从半径 r_emit 处发出的光在无穷远处的红移
    Calculate gravitational redshift for light emitted at radius r_emit

    公式 Formula: z = (λ_obs - λ_emit)/λ_emit = 1/√(1 - r_s/r_emit) - 1

    参数 Parameters:
        r_emit: 光源所在半径 Emission radius (m)
        r_s: 史瓦西半径 Schwarzschild radius (m)

    返回 Returns:
        z: 红移参数 Redshift parameter (无量纲 dimensionless)

    注意 Note:
        当 r_emit → r_s 时，z → ∞ (无限红移)
    """
    if r_emit <= r_s:
        return np.inf  # 在视界内或视界上，红移无限大
    # TODO: 计算红移
    # 提示：使用公式 z = 1/√(1 - r_s/r_emit) - 1
    z = 1 / np.sqrt(1 - r_s / r_emit) - 1  # 修改这里
    return z


def frequency_ratio(r_emit, r_s):
    """
    计算频率比（观测频率与发射频率之比）
    Calculate frequency ratio between observed and emitted light

    公式 Formula: ν_∞/ν_emit = √(1 - r_s/r_emit)

    参数 Parameters:
        r_emit: 光源所在半径 Emission radius (m)
        r_s: 史瓦西半径 Schwarzschild radius (m)

    返回 Returns:
        ratio: 频率比 Frequency ratio (无量纲 dimensionless, 0 < ratio ≤ 1)
    """
    if r_emit <= r_s:
        return 0  # 在视界处，频率比为零（无限红移）
    # TODO: 计算频率比
    # 提示：频率比与红移的关系为 ratio = 1/(1+z)
    ratio = np.sqrt(1 - r_s / r_emit)  # 修改这里
    return ratio


# =============================================================================
# 练习 1.3: 引力时间延迟
# Exercise 1.3: Gravitational Time Dilation
#
# 物理背景 Physical Background:
# 引力时间膨胀是广义相对论的核心预言：在强引力场中，时间流逝比在弱引力场
# 中更慢。这一效应对GPS卫星系统至关重要，需要进行相对论修正才能保证定位
# 精度。
#
# 物理意义 Physical Meaning:
# - 固有时间(τ)：随物体运动的观察者测量的时间
# - 坐标时间(t)：远处静止观察者测量的时间
# - 在黑洞视界处，时间膨胀因子为零，意味着从远处看，
#   物体永远不会穿过视界
#
# 关键公式 Key Formula:
# dτ = √(1 - r_s/r) × dt
# 越靠近黑洞，时间流逝越慢
# =============================================================================

def proper_time(coordinate_time, r, r_s):
    """
    计算固有时间（相对于坐标时间）
    Calculate proper time relative to coordinate time

    公式 Formula: τ = √(1 - r_s/r) × t

    参数 Parameters:
        coordinate_time: 坐标时间 Coordinate time (s)
        r: 观察者所在半径 Observer radius (m)
        r_s: 史瓦西半径 Schwarzschild radius (m)

    返回 Returns:
        tau: 固有时间 Proper time (s)

    物理意义 Physical Meaning:
        固有时间总是小于坐标时间，表示引力场中时钟走得更慢
    """
    if r <= r_s:
        return 0  # 在视界处或内部，时间膨胀极端
    # TODO: 计算固有时间
    # 提示：使用时间膨胀因子乘以坐标时间
    tau = np.sqrt(1 - r_s / r) * coordinate_time  # 修改这里
    return tau


def time_dilation_factor(r, r_s):
    """
    计算时间膨胀因子
    Calculate time dilation factor

    公式 Formula: dτ/dt = √(1 - r_s/r)

    参数 Parameters:
        r: 观察者所在半径 Observer radius (m)
        r_s: 史瓦西半径 Schwarzschild radius (m)

    返回 Returns:
        factor: 时间膨胀因子 Time dilation factor (无量纲 dimensionless, 0 ≤ factor ≤ 1)

    物理意义 Physical Meaning:
        - factor = 1: 无引力场（平坦时空）
        - factor → 0: 接近视界（极端时间膨胀）
    """
    if r <= r_s:
        return 0  # 在视界处，时间膨胀因子为零
    # TODO: 计算时间膨胀因子
    # 提示：这就是度规 g_tt 分量的平方根
    factor = np.sqrt(1 - r_s / r)  # 修改这里
    return factor


# =============================================================================
# 练习 1.4: 光子球半径
# Exercise 1.4: Photon Sphere
#
# 物理背景 Physical Background:
# 光子球是一个特殊的球面，在这个半径上光子可以沿圆形轨道绕黑洞运行。
# 这是黑洞"阴影"边界的一个重要特征，与事件视界望远镜(EHT)拍摄的
# 黑洞图像直接相关。
#
# 物理特性 Physical Properties:
# - 光子球轨道是不稳定的：任何微小扰动都会导致光子要么落入黑洞，
#   要么逃逸到无穷远
# - 这是形成黑洞"光环"的原因
# - 光子球半径是史瓦西半径的1.5倍
#
# 公式 Formula: r_photon = (3/2) × r_s = 3GM/c²
# =============================================================================

def photon_sphere_radius(M):
    """
    计算光子球半径
    Calculate photon sphere radius

    公式 Formula: r_ph = 3GM/c² = 1.5 × r_s

    参数 Parameters:
        M: 黑洞质量 Black hole mass (kg)

    返回 Returns:
        r_ph: 光子球半径 Photon sphere radius (m)

    物理意义 Physical Meaning:
        在此半径处，光子可以沿圆形轨道运动（但不稳定）
    """
    # TODO: 计算光子球半径
    # 提示：光子球半径 = 1.5 × 史瓦西半径
    r_ph = 3 * G * M / c**2  # 修改这里
    return r_ph


# =============================================================================
# 练习 1.5: 最内稳定圆轨道 (ISCO)
# Exercise 1.5: Innermost Stable Circular Orbit
#
# 物理背景 Physical Background:
# ISCO是物质可以稳定绑定黑洞做圆周运动的最小半径。在ISCO以内，
# 任何圆轨道都是不稳定的，物质会螺旋落入黑洞。
#
# 天文学意义 Astrophysical Significance:
# - 吸积盘的内边界通常位于ISCO附近
# - ISCO处的辐射效率决定了吸积过程的能量释放
# - X射线双星和活动星系核的观测与ISCO密切相关
#
# 对于史瓦西黑洞（无自旋）:
# r_ISCO = 3 × r_s = 6GM/c²
# 对于克尔黑洞（有自旋），ISCO可以更小（顺向旋转）或更大（逆向旋转）
# =============================================================================

def isco_radius(M):
    """
    计算最内稳定圆轨道半径（史瓦西黑洞）
    Calculate innermost stable circular orbit radius (Schwarzschild black hole)

    公式 Formula: r_ISCO = 6GM/c² = 3 × r_s

    参数 Parameters:
        M: 黑洞质量 Black hole mass (kg)

    返回 Returns:
        r_isco: ISCO半径 ISCO radius (m)

    物理意义 Physical Meaning:
        在此半径以内，没有稳定的圆形轨道存在
    """
    # TODO: 计算 ISCO 半径
    # 提示：ISCO半径 = 3 × 史瓦西半径 = 6GM/c²
    r_isco = 6 * G * M / c**2  # 修改这里
    return r_isco


def orbital_velocity_at_isco(M):
    """
    计算 ISCO 处的轨道速度
    Calculate orbital velocity at ISCO

    公式 Formula: v = c/√6 ≈ 0.408c

    参数 Parameters:
        M: 黑洞质量 Black hole mass (kg) [实际上此公式与质量无关]

    返回 Returns:
        v: 轨道速度 Orbital velocity (m/s)

    注意 Note:
        这是相对论速度，约为光速的40.8%
        这也是为什么ISCO处的吸积盘温度极高的原因
    """
    # TODO: 计算速度
    # 提示：ISCO处的速度是一个普适值，与黑洞质量无关
    v = c / np.sqrt(6)  # 修改这里
    return v


# =============================================================================
# 练习 1.6: 潮汐力
# Exercise 1.6: Tidal Forces
#
# 物理背景 Physical Background:
# 潮汐力源于引力场的不均匀性。在黑洞附近，潮汐力可以变得极其强大，
# 足以将物体撕裂成细长的条状——这一过程被形象地称为"面条化"
# (spaghettification)。
#
# 物理解释 Physical Interpretation:
# - 物体的不同部位受到的引力不同
# - 径向潮汐力会拉伸物体
# - 切向潮汐力会压缩物体
#
# 黑洞质量的影响 Effect of Black Hole Mass:
# - 恒星级黑洞 (~10 M☉): 在视界外就会面条化
# - 超大质量黑洞 (~10⁹ M☉): 可以完整穿过视界后才面条化
#
# 公式 Formula: a_tidal ≈ 2GM×Δr/r³
# =============================================================================

def tidal_acceleration(M, r, delta_r):
    """
    计算潮汐加速度（牛顿近似）
    Calculate tidal acceleration (Newtonian approximation)

    公式 Formula: a_tidal = 2GM×Δr/r³

    参数 Parameters:
        M: 黑洞质量 Black hole mass (kg)
        r: 距黑洞中心的距离 Distance from black hole center (m)
        delta_r: 物体的径向尺寸 Radial extent of object (m)

    返回 Returns:
        a: 潮汐加速度 Tidal acceleration (m/s²)

    物理意义 Physical Meaning:
        这是物体两端受到的引力加速度之差
        当此值超过物体的结构强度时，物体会被撕裂
    """
    # TODO: 计算潮汐加速度
    # 提示：潮汐力与 1/r³ 成正比（比引力本身衰减得更快）
    a = 2 * G * M * delta_r / r**3  # 修改这里
    return a


def spaghettification_radius(M, human_height=1.8, max_g=10):
    """
    计算"面条化"半径：潮汐力超过人体承受极限的半径
    Calculate spaghettification radius where tidal forces become lethal

    当潮汐加速度 > max_g × g 时发生面条化
    Spaghettification occurs when tidal acceleration > max_g × g

    参数 Parameters:
        M: 黑洞质量 Black hole mass (kg)
        human_height: 人体身高 Human height (m), 默认 1.8m
        max_g: 人体可承受的最大加速度 Maximum survivable acceleration (g), 默认 10g

    返回 Returns:
        r: 面条化开始的半径 Spaghettification radius (m)

    注意 Note:
        对于超大质量黑洞，此半径可能小于史瓦西半径，
        意味着可以完整穿过事件视界
    """
    g = 9.8  # 标准重力加速度 Standard gravitational acceleration (m/s²)
    # 从 a = 2GM×Δr/r³ = max_g × g 解出 r
    # r³ = 2GM×Δr/(max_g×g)
    r = (2 * G * M * human_height / (max_g * g))**(1/3)
    return r


# =============================================================================
# 练习 1.7: 径向自由落体
# Exercise 1.7: Radial Free Fall
#
# 物理背景 Physical Background:
# 一个从静止释放的物体会沿径向自由落入黑洞。令人惊讶的是，
# 从下落者的角度（固有时间），穿过事件视界并到达奇点只需要有限的时间。
# 但从远处观察者的角度（坐标时间），物体永远不会到达视界。
#
# 关键概念 Key Concepts:
# - 固有时间（τ）：下落者自己测量的时间，是有限的
# - 坐标时间（t）：远处观察者测量的时间，趋于无穷大
# - 这种差异体现了广义相对论中时间的相对性
#
# 公式 Formula（从远处静止释放的近似）:
# τ ≈ (π/2) × r_start^(3/2) / √(2GM)
# =============================================================================

def free_fall_time(r_start, M):
    """
    计算从静止自由落体到事件视界的固有时间（近似）
    Calculate proper time for radial free fall from rest to event horizon

    公式 Formula: τ ≈ (π/2) × r_start^(3/2) / √(2GM)
    （从很远处落下时的近似公式）

    参数 Parameters:
        r_start: 初始释放位置 Initial release position (m)
        M: 黑洞质量 Black hole mass (kg)

    返回 Returns:
        tau: 下落者测量的固有时间 Proper time for faller (s)

    物理意义 Physical Meaning:
        这是下落者手表上显示的时间
        与远处观察者看到的无限长时间形成鲜明对比
    """
    r_s = schwarzschild_radius(M)
    # TODO: 计算落体时间
    # 提示：使用开普勒型公式的相对论推广
    tau = (np.pi / 2) * r_start**(3/2) / np.sqrt(2 * G * M)  # 修改这里
    return tau


# =============================================================================
# 可视化
# =============================================================================
def plot_black_hole():
    """绘制黑洞物理图"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # 使用10倍太阳质量的黑洞作为例子
    M_bh = 10 * M_sun
    r_s = schwarzschild_radius(M_bh)
    r_ph = photon_sphere_radius(M_bh)
    r_isco = isco_radius(M_bh)

    # 1. 时间膨胀因子
    ax1 = axes[0, 0]
    r_range = np.linspace(1.01 * r_s, 10 * r_s, 200)
    dilation = [time_dilation_factor(r, r_s) for r in r_range]

    ax1.plot(r_range / r_s, dilation, 'b-', linewidth=2)
    ax1.axvline(x=1, color='r', linestyle='--', label='Event Horizon')
    ax1.axvline(x=1.5, color='g', linestyle='--', label='Photon Sphere')
    ax1.axvline(x=3, color='orange', linestyle='--', label='ISCO')
    ax1.set_xlabel('r / r_s')
    ax1.set_ylabel('dτ/dt')
    ax1.set_title('引力时间膨胀 Gravitational Time Dilation')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 引力红移
    ax2 = axes[0, 1]
    z_values = [gravitational_redshift(r, r_s) for r in r_range]

    ax2.semilogy(r_range / r_s, z_values, 'r-', linewidth=2)
    ax2.axvline(x=1, color='r', linestyle='--', alpha=0.5)
    ax2.axvline(x=1.5, color='g', linestyle='--', alpha=0.5)
    ax2.set_xlabel('r / r_s')
    ax2.set_ylabel('Redshift z')
    ax2.set_title('引力红移 Gravitational Redshift')
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0.01, 100)

    # 3. 黑洞结构示意图
    ax3 = axes[1, 0]
    theta = np.linspace(0, 2*np.pi, 100)

    # 绘制各个重要半径
    for r, color, label in [(r_s, 'black', 'Event Horizon (r_s)'),
                            (r_ph, 'blue', 'Photon Sphere (1.5 r_s)'),
                            (r_isco, 'green', 'ISCO (3 r_s)')]:
        x = r * np.cos(theta) / r_s
        y = r * np.sin(theta) / r_s
        ax3.plot(x, y, color=color, label=label, linewidth=2)

    # 填充黑洞内部
    x_bh = r_s * np.cos(theta) / r_s
    y_bh = r_s * np.sin(theta) / r_s
    ax3.fill(x_bh, y_bh, color='black', alpha=0.8)

    ax3.set_xlabel('x / r_s')
    ax3.set_ylabel('y / r_s')
    ax3.set_title(f'黑洞结构 Black Hole Structure (M = 10 M_☉)')
    ax3.set_aspect('equal')
    ax3.legend(loc='upper right')
    ax3.set_xlim(-4, 4)
    ax3.set_ylim(-4, 4)
    ax3.grid(True, alpha=0.3)

    # 4. 不同质量黑洞的史瓦西半径
    ax4 = axes[1, 1]
    masses = np.logspace(0, 10, 100)  # 1 to 10^10 太阳质量
    radii = [schwarzschild_radius(m * M_sun) for m in masses]

    ax4.loglog(masses, radii, 'b-', linewidth=2)
    # 标记特殊点
    ax4.axhline(y=schwarzschild_radius(M_sun), color='orange', linestyle='--',
                label=f'Sun: r_s = {schwarzschild_radius(M_sun)/1e3:.2f} km')
    ax4.axhline(y=schwarzschild_radius(4e6 * M_sun), color='purple', linestyle='--',
                label=f'Sgr A* (~4×10⁶ M_☉)')

    ax4.set_xlabel('Mass (M_☉)')
    ax4.set_ylabel('Schwarzschild Radius (m)')
    ax4.set_title('史瓦西半径 vs 质量')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('general_relativity.png', dpi=150)
    print("图像已保存为 general_relativity.png")
    plt.show()


# =============================================================================
# 验证函数 Verification Functions
# =============================================================================
def verify():
    """
    验证所有练习的正确性
    Verify all exercises for correctness
    """
    all_passed = True

    # 检查 1.1 - 史瓦西半径 Schwarzschild radius
    expected_rs_sun = 2 * G * M_sun / c**2  # ≈ 2.95 km
    if not np.isclose(r_s_sun, expected_rs_sun, rtol=0.01):
        print(f"错误 1.1: 史瓦西半径计算不正确，请检查公式 r_s = 2GM/c²")
        all_passed = False
    else:
        print(f"正确 1.1: 史瓦西半径 (太阳: r_s = {r_s_sun/1e3:.3f} km)")

    # 检查 1.2 - 引力红移 Gravitational redshift
    # 在 r = 2*r_s 处, z 应该等于 √2 - 1 ≈ 0.414
    z_test = gravitational_redshift(2 * r_s_sun, r_s_sun)
    expected_z = 1 / np.sqrt(1 - 0.5) - 1
    if not np.isclose(z_test, expected_z, rtol=0.01):
        print(f"错误 1.2: 引力红移计算不正确，请检查公式 z = 1/√(1-r_s/r) - 1")
        all_passed = False
    else:
        print(f"正确 1.2: 引力红移 (r=2r_s处: z = {z_test:.3f})")

    # 检查 1.3 - 时间膨胀 Time dilation
    tau_test = proper_time(1.0, 2*r_s_sun, r_s_sun)
    expected_tau = np.sqrt(0.5) * 1.0
    if not np.isclose(tau_test, expected_tau, rtol=0.01):
        print(f"错误 1.3: 时间膨胀计算不正确，请检查公式 dτ = √(1-r_s/r)×dt")
        all_passed = False
    else:
        print(f"正确 1.3: 时间膨胀 (r=2r_s处: dτ/dt = {np.sqrt(0.5):.3f})")

    # 检查 1.4 - 光子球 Photon sphere
    r_ph = photon_sphere_radius(M_sun)
    expected_rph = 3 * G * M_sun / c**2
    if not np.isclose(r_ph, expected_rph, rtol=0.01):
        print(f"错误 1.4: 光子球半径计算不正确，请检查公式 r_ph = 3GM/c²")
        all_passed = False
    else:
        print(f"正确 1.4: 光子球半径 (r_ph = 1.5r_s = {r_ph/1e3:.3f} km)")

    # 检查 1.5 - ISCO
    r_isco = isco_radius(M_sun)
    expected_isco = 6 * G * M_sun / c**2
    if not np.isclose(r_isco, expected_isco, rtol=0.01):
        print(f"错误 1.5: ISCO半径计算不正确，请检查公式 r_ISCO = 6GM/c²")
        all_passed = False
    else:
        v_isco = orbital_velocity_at_isco(M_sun)
        print(f"正确 1.5: ISCO (r_ISCO = 3r_s = {r_isco/1e3:.2f} km, v = {v_isco/c:.3f}c)")

    # 检查 1.6 - 潮汐力 Tidal forces
    a_tidal = tidal_acceleration(M_sun, 2*r_s_sun, 1.0)
    expected_a = 2 * G * M_sun * 1.0 / (2*r_s_sun)**3
    if not np.isclose(a_tidal, expected_a, rtol=0.01):
        print(f"错误 1.6: 潮汐加速度计算不正确，请检查公式 a = 2GM×Δr/r³")
        all_passed = False
    else:
        print(f"正确 1.6: 潮汐力计算")

    # 检查 1.7 - 自由落体时间 Free fall time
    tau_fall = free_fall_time(10 * r_s_sun, M_sun)
    if tau_fall <= 0:
        print(f"错误 1.7: 自由落体时间应为正值，请检查公式")
        all_passed = False
    else:
        print(f"正确 1.7: 自由落体时间 (从10r_s落到r_s: τ ≈ {tau_fall*1e6:.1f} μs)")

    if all_passed:
        print("\n所有测试通过！正在生成可视化...")
        try:
            plot_black_hole()
        except Exception as e:
            print(f"可视化生成失败: {e}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("史瓦西度规与黑洞物理 General Relativity")
    print("=" * 50)
    verify()
