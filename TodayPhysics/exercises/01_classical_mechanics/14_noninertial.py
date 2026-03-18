"""
非惯性参考系 Non-Inertial Reference Frames
难度 Difficulty: ★★★★

================================================================================
学习目标 Learning Objectives
================================================================================
- 理解惯性力（伪力）的物理本质
  Understand the physical nature of inertial forces (pseudo-forces)
- 掌握科里奥利力和离心力的计算
  Master the calculation of Coriolis and centrifugal forces
- 分析旋转参考系中的运动现象
  Analyze motion phenomena in rotating reference frames
- 应用于地球表面运动问题（傅科摆、自由落体偏转）
  Apply to problems on Earth's surface (Foucault pendulum, free fall deflection)

================================================================================
物理背景 Physical Background
================================================================================
非惯性参考系是相对于惯性系有加速度的参考系。
在非惯性系中，需要引入惯性力才能使用牛顿定律。

1. 惯性力（伪力）Inertial Forces:
   不是真实的相互作用力，而是参考系加速的表现
   惯性系观察者不会看到这些力

2. 离心力 Centrifugal Force:
   F_cf = mω²r（指向转轴向外）
   - 在旋转参考系中，物体似乎受到向外的力
   - 洗衣机脱水、离心机、人造重力

3. 科里奥利力 Coriolis Force:
   F_cor = -2m(ω × v)
   - 只在物体相对旋转系运动时出现
   - 垂直于速度方向（在北半球使运动偏右）
   - 影响大气环流、洋流、远程射击

4. 地球上的效应 Effects on Earth:
   - 有效重力: g_eff = g₀ - ω²R cos²φ（纬度φ处）
   - 傅科摆: 摆动平面以 ω sin φ 的角速度旋转
   - 自由落体向东偏转

5. 傅科摆 Foucault Pendulum:
   证明地球自转的经典实验
   旋转周期 T = 24小时/|sin φ|
   - 极地: T = 24小时
   - 赤道: T = ∞（不旋转）

6. 潮汐力 Tidal Forces:
   由引力梯度产生，使物体形变
   a_tidal ≈ 2GMr/R³

HINT: 离心力: F_cf = mω²r（向外）
HINT: 科里奥利力: F_cor = -2m(ω×v)（北半球向右偏）
HINT: 傅科摆周期: T = 24h/|sinφ|
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import G

# I AM NOT DONE

# 地球参数
omega_earth = 7.27e-5  # rad/s
R_earth = 6.371e6  # m
g = 9.81  # m/s²

# =============================================================================
# 练习 14.1: 离心力
# Exercise 14.1: Centrifugal Force
# =============================================================================
# 离心力是旋转参考系中最基本的惯性力
# 它解释了为什么旋转物体上的物品"被甩出去"

def centrifugal_force(m, omega, r):
    """
    离心力 Centrifugal Force
    F_cf = mω²r（沿径向向外）

    物理意义：
    - 在旋转参考系中，物体似乎受到向外的力
    - 实际上是惯性的表现（物体趋于直线运动）

    应用实例：
    - 离心机: 分离不同密度物质
    - 洗衣机脱水: 水被"甩"出
    - 空间站人造重力: ω²r = g

    参数 Parameters:
        m: 质量 [kg]
        omega: 角速度 [rad/s]
        r: 到转轴的距离 [m]
    返回 Returns:
        离心力大小 [N]
    """
    # TODO: 计算离心力（向外）
    return m * omega**2 * r

def effective_gravity(latitude, omega=omega_earth, R=R_earth, g0=g):
    """
    考虑地球自转的有效重力加速度 Effective Gravity

    g_eff = g₀ - ω²R cos²(φ)

    地球自转产生的离心力减小了有效重力:
    - 赤道: 离心力最大，g_eff ≈ 9.78 m/s²
    - 极地: 离心力为零，g_eff ≈ 9.83 m/s²
    - 差异约0.5%

    参数 Parameters:
        latitude: 纬度（度）
        omega: 地球自转角速度 [rad/s]
        R: 地球半径 [m]
        g0: 重力加速度（不考虑自转）[m/s²]
    返回 Returns:
        有效重力加速度 [m/s²]
    """
    phi = np.radians(latitude)
    r = R * np.cos(phi)  # 到转轴的垂直距离
    g_eff = g0 - omega**2 * r * np.cos(phi)
    return g_eff


# =============================================================================
# 练习 14.2: 科里奥利力
# Exercise 14.2: Coriolis Force
# =============================================================================
# 科里奥利力只在物体相对旋转系运动时出现
# 它垂直于速度方向，不做功但改变运动方向

def coriolis_force(m, omega_vec, v_vec):
    """
    科里奥利力 Coriolis Force
    F_cor = -2m(ω × v)

    特点：
    - 垂直于速度和转轴（叉积方向）
    - 不做功（垂直于运动方向）
    - 北半球使运动偏右，南半球偏左

    重要应用：
    - 大气环流: 信风、西风带
    - 台风旋转方向（北半球逆时针）
    - 洋流分布
    - 远程炮弹轨迹修正

    参数 Parameters:
        m: 质量 [kg]
        omega_vec: 角速度矢量 [rad/s]
        v_vec: 速度矢量 [m/s]
    返回 Returns:
        科里奥利力矢量 [N]
    """
    # TODO: 计算科里奥利力（叉积）
    return -2 * m * np.cross(omega_vec, v_vec)

def coriolis_deflection(v, t, latitude, omega=omega_earth):
    """
    科里奥利偏转 Coriolis Deflection

    水平运动物体在科里奥利力作用下的偏转
    偏转量: Δx ≈ (1/2)f·v·t²
    其中 f = 2ω sin(φ) 是科里奥利参数

    参数 Parameters:
        v: 速度大小 [m/s]
        t: 运动时间 [s]
        latitude: 纬度（度）
        omega: 地球自转角速度 [rad/s]
    返回 Returns:
        侧向偏转量 [m]
    """
    phi = np.radians(latitude)
    f = 2 * omega * np.sin(phi)  # 科里奥利参数
    return 0.5 * f * v * t**2


# =============================================================================
# 练习 14.3: 傅科摆
# Exercise 14.3: Foucault Pendulum
# =============================================================================
# 傅科摆是1851年莱昂·傅科设计的实验
# 是地球自转的直接证明，不依赖天文观测

def foucault_period(latitude, omega=omega_earth):
    """
    傅科摆周期 Foucault Pendulum Period
    T = 24小时/|sin(φ)|

    物理原理：
    - 摆动平面在惯性空间中保持不变
    - 但地球在其下方旋转
    - 在地面观察者看来，摆动平面在旋转

    不同纬度的周期：
    - 极地(φ=90°): T = 24小时
    - 中纬度: T = 24/sin(φ)小时
    - 赤道(φ=0°): T = ∞（不旋转）

    参数 Parameters:
        latitude: 纬度（度）
        omega: 地球自转角速度 [rad/s]
    返回 Returns:
        傅科摆完整旋转周期 [s]
    """
    phi = np.radians(latitude)
    if np.abs(np.sin(phi)) < 1e-10:
        return np.inf  # 赤道处不旋转
    T_sidereal = 2 * np.pi / omega  # 恒星日（约23小时56分）
    return T_sidereal / np.abs(np.sin(phi))

def foucault_rotation_rate(latitude, omega=omega_earth):
    """
    傅科摆平面旋转角速度 Foucault Pendulum Rotation Rate
    Ω = ω sin(φ)

    北半球顺时针旋转（从上往下看）
    南半球逆时针旋转
    """
    phi = np.radians(latitude)
    return omega * np.sin(phi)


# =============================================================================
# 练习 14.4: 旋转参考系运动方程
# Exercise 14.4: Equations of Motion in Rotating Frame
# =============================================================================
def rotating_frame_eom(state, t, omega, m=1):
    """
    旋转参考系中的运动方程（2D，绕z轴旋转）
    包含离心力和科里奥利力
    """
    x, y, vx, vy = state

    # 离心加速度 (向外)
    a_cf_x = omega**2 * x
    a_cf_y = omega**2 * y

    # 科里奥利加速度 (ω沿z轴)
    a_cor_x = 2 * omega * vy
    a_cor_y = -2 * omega * vx

    ax = a_cf_x + a_cor_x
    ay = a_cf_y + a_cor_y

    return [vx, vy, ax, ay]

def rotating_frame_trajectory(x0, y0, vx0, vy0, omega, t_span):
    """计算旋转参考系中的轨迹"""
    state0 = [x0, y0, vx0, vy0]
    t = np.linspace(t_span[0], t_span[1], 1000)
    sol = odeint(rotating_frame_eom, state0, t, args=(omega,))
    return t, sol


# =============================================================================
# 练习 14.5: 自由落体偏转
# Exercise 14.5: Free Fall Deflection
# =============================================================================
def eastward_deflection(h, latitude, omega=omega_earth):
    """
    自由落体的向东偏转
    Δx ≈ (1/3)ω cos(φ)√(8h³/g)
    """
    phi = np.radians(latitude)
    delta_x = (1/3) * omega * np.cos(phi) * np.sqrt(8 * h**3 / g)
    return delta_x

def free_fall_time(h):
    """自由落体时间"""
    return np.sqrt(2 * h / g)


# =============================================================================
# 练习 14.6: 潮汐力
# Exercise 14.6: Tidal Forces
# =============================================================================
# 潮汐力是引力梯度造成的差异力
# 它使物体趋于沿连心线方向拉伸、垂直方向压缩

def tidal_acceleration(r, R, M):
    """
    潮汐加速度 Tidal Acceleration
    a_tidal ≈ 2GMr/R³

    物理原理：
    - 近端点受到的引力比质心处更强
    - 远端点受到的引力比质心处更弱
    - 差异造成相对质心的加速度

    应用：
    - 海洋潮汐（月球和太阳）
    - 洛希极限（行星环的形成）
    - 意大利面化效应（黑洞附近）

    参数 Parameters:
        r: 距离质心的位移（可正可负）[m]
        R: 到引力源的距离 [m]
        M: 引力源质量 [kg]
    返回 Returns:
        潮汐加速度 [m/s²]
    """
    return 2 * G * M * r / R**3

def tidal_bulge_height(R_body, R_orbit, M_tide, M_body):
    """
    潮汐隆起高度 Tidal Bulge Height

    h ≈ (3/2)(M_tide/M_body)(R_body/R_orbit)³ × R_body

    地球上的潮汐隆起:
    - 月球造成: 约0.5米
    - 太阳造成: 约0.25米
    - 两者叠加: 大潮（朔望）和小潮（弦月）
    """
    return 1.5 * (M_tide / M_body) * (R_body / R_orbit)**3 * R_body


# =============================================================================
# 可视化
# =============================================================================
def plot_noninertial():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 有效重力vs纬度
    ax1 = axes[0, 0]
    lat = np.linspace(0, 90, 100)
    g_eff = [effective_gravity(l) for l in lat]

    ax1.plot(lat, g_eff, 'b-', linewidth=2)
    ax1.set_xlabel('纬度 (°)')
    ax1.set_ylabel('g_eff (m/s²)')
    ax1.set_title('有效重力加速度')
    ax1.grid(True, alpha=0.3)

    # 2. 傅科摆周期vs纬度
    ax2 = axes[0, 1]
    lat_foucault = np.linspace(10, 90, 100)
    T_foucault = [foucault_period(l) / 3600 for l in lat_foucault]  # 小时

    ax2.plot(lat_foucault, T_foucault, 'r-', linewidth=2)
    ax2.set_xlabel('纬度 (°)')
    ax2.set_ylabel('周期 (小时)')
    ax2.set_title('傅科摆周期')
    ax2.set_ylim(0, 100)
    ax2.grid(True, alpha=0.3)

    # 3. 旋转参考系轨迹
    ax3 = axes[0, 2]
    omega = 0.5
    t, sol = rotating_frame_trajectory(1, 0, 0, 0.5, omega, [0, 20])

    ax3.plot(sol[:, 0], sol[:, 1], 'g-', linewidth=1.5)
    ax3.scatter([1], [0], c='red', s=50, zorder=5)
    ax3.set_xlabel('x')
    ax3.set_ylabel('y')
    ax3.set_title('旋转参考系中的轨迹')
    ax3.axis('equal')
    ax3.grid(True, alpha=0.3)

    # 4. 自由落体偏转
    ax4 = axes[1, 0]
    h = np.linspace(1, 1000, 100)

    for lat in [0, 30, 45, 60]:
        delta_x = [eastward_deflection(hi, lat) * 100 for hi in h]  # cm
        ax4.plot(h, delta_x, label=f'{lat}°', linewidth=2)

    ax4.set_xlabel('落体高度 (m)')
    ax4.set_ylabel('向东偏转 (cm)')
    ax4.set_title('自由落体偏转')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 科里奥利力方向
    ax5 = axes[1, 1]
    # 北半球，向北运动
    theta = np.linspace(0, 2*np.pi, 100)
    v_x = np.cos(theta)
    v_y = np.sin(theta)

    # 科里奥利力方向（北半球向右偏）
    f_x = v_y  # 比例
    f_y = -v_x

    ax5.quiver([0]*8, [0]*8, v_x[::12], v_y[::12], color='blue', scale=5, label='速度')
    ax5.quiver(v_x[::12], v_y[::12], f_x[::12], f_y[::12], color='red', scale=5, label='科里奥利力')
    ax5.set_xlim(-1.5, 1.5)
    ax5.set_ylim(-1.5, 1.5)
    ax5.set_xlabel('x')
    ax5.set_ylabel('y')
    ax5.set_title('科里奥利力方向（北半球）')
    ax5.legend()
    ax5.axis('equal')
    ax5.grid(True, alpha=0.3)

    # 6. 潮汐力
    ax6 = axes[1, 2]
    # 地月系统
    R_moon = 3.844e8  # m
    M_moon = 7.35e22  # kg
    r = np.linspace(-R_earth, R_earth, 100)

    a_tidal = [tidal_acceleration(ri, R_moon, M_moon) * 1e7 for ri in r]  # ×10^7 m/s²

    ax6.plot(r/R_earth, a_tidal, 'purple', linewidth=2)
    ax6.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    ax6.set_xlabel('r/R_地球')
    ax6.set_ylabel('a_潮汐 (×10⁻⁷ m/s²)')
    ax6.set_title('月球潮汐加速度')
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('noninertial.png', dpi=150)
    print("图像已保存为 noninertial.png")
    plt.show()


def verify():
    all_passed = True

    # Check 14.1
    F_cf = centrifugal_force(1, 1, 1)
    if not np.isclose(F_cf, 1, rtol=0.01):
        print("❌ 14.1 离心力错误")
        all_passed = False
    else:
        print("✓ 14.1 离心力正确")

    # Check 14.2
    omega_vec = np.array([0, 0, 1])
    v_vec = np.array([1, 0, 0])
    F_cor = coriolis_force(1, omega_vec, v_vec)
    expected = np.array([0, 2, 0])
    if not np.allclose(F_cor, expected, rtol=0.01):
        print("❌ 14.2 科里奥利力错误")
        all_passed = False
    else:
        print("✓ 14.2 科里奥利力正确")

    # Check 14.3
    T_pole = foucault_period(90)
    T_sidereal = 2 * np.pi / omega_earth
    if not np.isclose(T_pole, T_sidereal, rtol=0.01):
        print("❌ 14.3 极地傅科摆周期应等于恒星日")
        all_passed = False
    else:
        print(f"✓ 14.3 傅科摆正确 (极地周期 = {T_pole/3600:.1f}小时)")

    # Check 14.4
    t, sol = rotating_frame_trajectory(1, 0, 0, 0, 1, [0, 1])
    if len(sol) == 0:
        print("❌ 14.4 运动方程求解错误")
        all_passed = False
    else:
        print("✓ 14.4 旋转参考系方程正确")

    # Check 14.5
    delta_x = eastward_deflection(100, 45)
    if delta_x <= 0:
        print("❌ 14.5 自由落体偏转应向东")
        all_passed = False
    else:
        print(f"✓ 14.5 自由落体偏转正确 (100m落体偏转 {delta_x*100:.2f} cm)")

    # Check 14.6
    a_tidal = tidal_acceleration(1, 1, 1)
    if a_tidal != 2 * G:
        print("❌ 14.6 潮汐加速度错误")
        all_passed = False
    else:
        print("✓ 14.6 潮汐力正确")

    if all_passed:
        print("\n🎉 所有测试通过！")
        try:
            plot_noninertial()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("非惯性参考系 Non-Inertial Reference Frames")
    print("=" * 50)
    verify()
