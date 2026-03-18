"""
参考系拖曳效应 Frame Dragging
难度 Difficulty: ★★★★★

学习目标 Learning Objectives:
- 理解Lense-Thirring效应（参考系拖曳/引力磁效应）
- 掌握克尔度规（旋转黑洞）的基本性质
- 分析能层（ergosphere）和彭罗斯过程
- 了解Gravity Probe B实验对广义相对论的验证

物理背景 Physical Background:
当质量旋转时，它会"拖曳"周围的时空一起旋转，这被称为参考系拖曳效应
（frame dragging）或Lense-Thirring效应。这是广义相对论特有的预言，
类似于电磁学中的磁效应（因此也称为"引力磁效应"）。

克尔黑洞的独特性质 Unique Properties of Kerr Black Holes:
  - 两个视界：外视界r₊和内视界r₋
  - 能层（ergosphere）：一个可以提取旋转能量的区域
  - 彭罗斯过程：从旋转黑洞中提取能量的机制
  - 极端克尔黑洞：a = GM/c²时，两个视界合并

实验验证 Experimental Verification:
  - Gravity Probe B (2004-2005)：直接测量地球引起的参考系拖曳
  - LAGEOS卫星：测量Lense-Thirring进动
  - 脉冲星双星系统：间接验证

关键公式 Key Formulas:
  - 克尔自旋参数: a = J/(Mc)
  - 外视界: r₊ = GM/c² + √((GM/c²)² - a²)
  - 能层边界: r_e = GM/c² + √((GM/c²)² - a²cos²θ)
  - Lense-Thirring进动: Ω_LT ≈ 2GJ/(c²r³)

单位说明 Units:
  - 角动量 J: kg·m²/s
  - 自旋参数 a: m（长度量纲）
  - 进动角速度: rad/s
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import G, c, M_sun

# I AM NOT DONE

# =============================================================================
# 练习 6.1: Lense-Thirring效应
# Exercise 6.1: Lense-Thirring Effect
# =============================================================================
def frame_dragging_rate(J, r, M):
    """
    参考系拖曳角速度（远场近似）
    Ω_LT ≈ 2GJ/(c²r³)
    J: 角动量
    r: 距离
    M: 质量（用于无量纲化）
    """
    return 2 * G * J / (c**2 * r**3)

def lense_thirring_precession(J, a_orbit, e, M):
    """
    Lense-Thirring进动率（卫星轨道）
    Ω_LT = 2GJ/(c²a³(1-e²)^(3/2))
    a_orbit: 轨道半长轴
    e: 轨道偏心率
    """
    return 2 * G * J / (c**2 * a_orbit**3 * (1 - e**2)**(3/2))

def geodetic_precession(M, a_orbit, e):
    """
    测地进动（de Sitter进动）
    Ω_geo = 3(GM)^(3/2) / (c²a^(5/2)(1-e²))
    """
    return 3 * (G * M)**(3/2) / (c**2 * a_orbit**(5/2) * (1 - e**2))


# =============================================================================
# 练习 6.2: 克尔黑洞参数
# Exercise 6.2: Kerr Black Hole Parameters
# =============================================================================
def kerr_spin_parameter(J, M):
    """
    克尔自旋参数
    a = J/(Mc)
    |a| ≤ GM/c² 对应有视界的黑洞
    """
    return J / (M * c)

def dimensionless_spin(J, M):
    """
    无量纲自旋参数
    χ = a/(GM/c²) = Jc/(GM²)
    0 ≤ χ ≤ 1 对应克尔黑洞
    """
    return J * c / (G * M**2)

def angular_momentum_from_spin(chi, M):
    """
    从无量纲自旋计算角动量
    J = χGM²/c
    """
    return chi * G * M**2 / c


# =============================================================================
# 练习 6.3: 克尔视界
# Exercise 6.3: Kerr Horizons
# =============================================================================
def kerr_outer_horizon(M, a):
    """
    克尔黑洞外视界
    r₊ = GM/c² + √((GM/c²)² - a²)
    """
    r_g = G * M / c**2
    if np.abs(a) > r_g:
        return None  # 裸奇点
    return r_g + np.sqrt(r_g**2 - a**2)

def kerr_inner_horizon(M, a):
    """
    克尔黑洞内视界
    r₋ = GM/c² - √((GM/c²)² - a²)
    """
    r_g = G * M / c**2
    if np.abs(a) > r_g:
        return None
    return r_g - np.sqrt(r_g**2 - a**2)

def kerr_horizon_area(M, a):
    """
    克尔黑洞视界面积
    A = 8πGM/c²(GM/c² + √((GM/c²)² - a²))
    """
    r_plus = kerr_outer_horizon(M, a)
    if r_plus is None:
        return None
    r_g = G * M / c**2
    return 8 * np.pi * r_g * r_plus


# =============================================================================
# 练习 6.4: 能层
# Exercise 6.4: Ergosphere
# =============================================================================
def ergosphere_radius(M, a, theta):
    """
    能层外边界半径
    r_e = GM/c² + √((GM/c²)² - a²cos²θ)
    """
    r_g = G * M / c**2
    return r_g + np.sqrt(r_g**2 - a**2 * np.cos(theta)**2)

def static_limit(M, a, theta):
    """
    静态极限（能层外边界的另一种表述）
    """
    return ergosphere_radius(M, a, theta)

def ergosphere_volume(M, a):
    """
    能层体积（近似）
    V_ergo ≈ (4π/3)(r_e³ - r₊³) 在赤道处
    """
    r_e_eq = ergosphere_radius(M, a, np.pi/2)
    r_plus = kerr_outer_horizon(M, a)
    if r_plus is None:
        return None
    return (4 * np.pi / 3) * (r_e_eq**3 - r_plus**3)


# =============================================================================
# 练习 6.5: 彭罗斯过程
# Exercise 6.5: Penrose Process
# =============================================================================
def penrose_energy_extraction_max(M, a):
    """
    彭罗斯过程最大能量提取效率
    η_max = 1 - √(1 - χ²/4) 当 χ << 1
    对于极端克尔黑洞 χ=1: η ≈ 0.29
    """
    chi = a * c**2 / (G * M)  # 无量纲自旋
    if chi > 1:
        chi = 1
    return 1 - np.sqrt(0.5 * (1 + np.sqrt(1 - chi**2)))

def irreducible_mass(M, a):
    """
    不可约质量
    M_irr = √((M² + √(M⁴ - J²c⁻²))/ 2)
    """
    J = a * M * c
    return np.sqrt((M**2 + np.sqrt(M**4 - (J/c)**2)) / 2)

def extractable_energy(M, a):
    """
    可提取能量
    E_ext = (M - M_irr)c²
    """
    M_irr = irreducible_mass(M, a)
    return (M - M_irr) * c**2


# =============================================================================
# 练习 6.6: 旋转参考系中的物理
# Exercise 6.6: Physics in Rotating Frames
# =============================================================================
def zamo_angular_velocity(M, a, r, theta=np.pi/2):
    """
    零角动量观测者(ZAMO)角速度
    Ω_ZAMO = -g_tφ/g_φφ ≈ 2GJr/(c(r⁴ + a²r² + 2a²Mr))
    """
    J = a * M * c
    r_g = G * M / c**2
    # 简化的赤道面表达式
    numerator = 2 * r_g * a
    denominator = r**2 + a**2 + 2 * r_g * a**2 / r
    return numerator / (r * denominator) * c

def gravitomagnetic_field(J, r):
    """
    引力磁场（类比电磁学）
    B_g ~ GJ/(c²r³)
    """
    return G * J / (c**2 * r**3)

def gyroscope_precession_rate(J, r):
    """
    陀螺仪进动率
    Ω_gyro ≈ GJ/(c²r³)
    """
    return G * J / (c**2 * r**3)


# =============================================================================
# 可视化
# =============================================================================
def plot_frame_dragging():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 克尔黑洞截面（视界和能层）
    ax1 = axes[0, 0]
    M = 10 * M_sun

    for chi in [0, 0.5, 0.9, 0.99]:
        a = chi * G * M / c**2
        theta = np.linspace(0, 2*np.pi, 200)

        # 外视界
        r_plus = kerr_outer_horizon(M, a)
        if r_plus:
            r_g = G * M / c**2
            x_h = r_plus * np.sin(theta) / r_g
            z_h = r_plus * np.cos(theta) / r_g
            ax1.plot(x_h, z_h, '--', alpha=0.5)

        # 能层
        r_e = [ergosphere_radius(M, a, t) for t in theta]
        x_e = np.array(r_e) * np.sin(theta) / r_g
        z_e = np.array(r_e) * np.cos(theta) / r_g
        ax1.plot(x_e, z_e, label=f'χ={chi}')

    ax1.set_xlabel('x/(GM/c²)')
    ax1.set_ylabel('z/(GM/c²)')
    ax1.set_title('克尔黑洞截面')
    ax1.legend()
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.3)

    # 2. 拖曳角速度vs距离
    ax2 = axes[0, 1]
    M = 10 * M_sun
    chi = 0.9
    a = chi * G * M / c**2
    J = a * M * c

    r_g = G * M / c**2
    r = np.linspace(2, 20, 100) * r_g

    omega_drag = [frame_dragging_rate(J, ri, M) for ri in r]

    ax2.semilogy(r/r_g, omega_drag, 'b-', linewidth=2)
    ax2.set_xlabel('r/(GM/c²)')
    ax2.set_ylabel('Ω_drag (rad/s)')
    ax2.set_title('参考系拖曳角速度 (χ=0.9)')
    ax2.grid(True, alpha=0.3)

    # 3. 视界半径vs自旋
    ax3 = axes[0, 2]
    chi_range = np.linspace(0, 0.999, 100)

    r_plus_vals = []
    r_minus_vals = []

    for chi in chi_range:
        a = chi * G * M / c**2
        r_p = kerr_outer_horizon(M, a)
        r_m = kerr_inner_horizon(M, a)
        r_plus_vals.append(r_p / r_g if r_p else np.nan)
        r_minus_vals.append(r_m / r_g if r_m else np.nan)

    ax3.plot(chi_range, r_plus_vals, 'b-', label='r₊ (外视界)', linewidth=2)
    ax3.plot(chi_range, r_minus_vals, 'r-', label='r₋ (内视界)', linewidth=2)
    ax3.axhline(y=2, color='k', linestyle='--', alpha=0.5, label='史瓦西')
    ax3.set_xlabel('χ = a/(GM/c²)')
    ax3.set_ylabel('r/(GM/c²)')
    ax3.set_title('克尔视界半径')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 彭罗斯效率vs自旋
    ax4 = axes[1, 0]
    chi_range = np.linspace(0.01, 0.999, 100)

    eta = []
    for chi in chi_range:
        a = chi * G * M / c**2
        e = penrose_energy_extraction_max(M, a)
        eta.append(e * 100)  # 百分比

    ax4.plot(chi_range, eta, 'g-', linewidth=2)
    ax4.set_xlabel('χ')
    ax4.set_ylabel('最大效率 (%)')
    ax4.set_title('彭罗斯过程能量提取')
    ax4.grid(True, alpha=0.3)

    # 5. 不可约质量
    ax5 = axes[1, 1]

    M_irr_vals = []
    for chi in chi_range:
        a = chi * G * M / c**2
        M_irr = irreducible_mass(M, a)
        M_irr_vals.append(M_irr / M)

    ax5.plot(chi_range, M_irr_vals, 'purple', linewidth=2)
    ax5.axhline(y=1/np.sqrt(2), color='r', linestyle='--',
                alpha=0.5, label='极端克尔极限')
    ax5.set_xlabel('χ')
    ax5.set_ylabel('M_irr/M')
    ax5.set_title('不可约质量')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. Gravity Probe B验证
    ax6 = axes[1, 2]
    # 地球数据
    M_earth = 5.972e24  # kg
    J_earth = 7.08e33   # kg m²/s
    R_earth = 6.371e6   # m

    h_orbit = np.linspace(400, 2000, 100) * 1e3  # 轨道高度 (m)
    r_orbit = R_earth + h_orbit

    omega_lt = [lense_thirring_precession(J_earth, r, 0, M_earth)
                * 180/np.pi * 3600 * 1000 * 365.25 * 24 * 3600  # mas/yr
                for r in r_orbit]
    omega_geo = [geodetic_precession(M_earth, r, 0)
                 * 180/np.pi * 3600 * 1000 * 365.25 * 24 * 3600
                 for r in r_orbit]

    ax6.semilogy(h_orbit/1e3, omega_lt, 'b-', label='Lense-Thirring', linewidth=2)
    ax6.semilogy(h_orbit/1e3, omega_geo, 'r-', label='测地进动', linewidth=2)
    ax6.set_xlabel('轨道高度 (km)')
    ax6.set_ylabel('进动率 (mas/yr)')
    ax6.set_title('地球卫星进动')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('frame_dragging.png', dpi=150)
    print("图像已保存为 frame_dragging.png")
    plt.show()


def verify():
    """
    验证所有练习的正确性
    Verify all exercises for correctness
    """
    all_passed = True

    M = 10 * M_sun
    chi = 0.9  # 无量纲自旋参数
    a = chi * G * M / c**2  # 自旋参数
    J = a * M * c  # 角动量
    r_g = G * M / c**2  # 引力半径

    # 检查 6.1 - Lense-Thirring效应 Lense-Thirring effect
    omega_lt = frame_dragging_rate(J, 10 * r_g, M)
    if omega_lt <= 0:
        print("错误 6.1: Lense-Thirring进动率应为正值")
        all_passed = False
    else:
        print(f"正确 6.1: Lense-Thirring效应 (Omega_LT = {omega_lt:.2e} rad/s)")

    # 检查 6.2 - 克尔参数 Kerr parameters
    chi_calc = dimensionless_spin(J, M)
    if not np.isclose(chi_calc, chi, rtol=0.01):
        print("错误 6.2: 无量纲自旋参数计算不正确")
        all_passed = False
    else:
        print(f"正确 6.2: 克尔参数 (chi = {chi_calc:.2f})")

    # 检查 6.3 - 克尔视界 Kerr horizons
    r_plus = kerr_outer_horizon(M, a)
    r_minus = kerr_inner_horizon(M, a)
    if r_plus is None or r_minus is None:
        print("错误 6.3: 视界计算返回None，请检查公式")
        all_passed = False
    elif r_plus <= r_minus:
        print("错误 6.3: 外视界应大于内视界 (r+ > r-)")
        all_passed = False
    else:
        print(f"正确 6.3: 克尔视界 (r+ = {r_plus/r_g:.2f} r_g)")

    # 检查 6.4 - 能层 Ergosphere
    r_e_eq = ergosphere_radius(M, a, np.pi/2)  # 赤道
    r_e_pole = ergosphere_radius(M, a, 0)  # 极点
    if r_e_eq <= r_plus or not np.isclose(r_e_pole, r_plus, rtol=0.01):
        print("错误 6.4: 能层边界计算不正确（赤道处应大于视界，极点处应等于视界）")
        all_passed = False
    else:
        print(f"正确 6.4: 能层 (r_e(赤道) = {r_e_eq/r_g:.2f} r_g)")

    # 检查 6.5 - 彭罗斯过程 Penrose process
    eta = penrose_energy_extraction_max(M, a)
    if eta <= 0 or eta > 0.5:
        print("错误 6.5: 彭罗斯效率应在0到50%之间")
        all_passed = False
    else:
        print(f"正确 6.5: 彭罗斯过程 (eta_max = {eta*100:.1f}%)")

    # 检查 6.6 - 旋转参考系 Rotating frame
    omega_zamo = zamo_angular_velocity(M, a, 5 * r_g)
    if omega_zamo <= 0:
        print("错误 6.6: ZAMO角速度应为正值（同向旋转）")
        all_passed = False
    else:
        print(f"正确 6.6: 旋转参考系 (Omega_ZAMO = {omega_zamo:.2e} rad/s)")

    if all_passed:
        print("\n所有测试通过！")
        try:
            plot_frame_dragging()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("参考系拖曳效应 Frame Dragging")
    print("=" * 50)
    verify()
