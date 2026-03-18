"""
黑洞物理 Black Hole Physics
难度 Difficulty: ★★★★★

学习目标 Learning Objectives:
- 理解事件视界、奇点和时空因果结构
- 掌握黑洞热力学四定律和霍金辐射
- 分析克尔（旋转）黑洞的独特性质
- 理解引力波探测的基本原理
- 了解潮汐瓦解事件的物理机制

物理背景 Physical Background:
黑洞是广义相对论最令人惊奇的预言之一。它们不仅是引力最极端的表现，
还与量子力学、热力学和信息论有着深刻的联系。

黑洞类型 Types of Black Holes:
  - 史瓦西黑洞：无自旋、无电荷（最简单情况）
  - 克尔黑洞：有自旋、无电荷（天体物理最常见）
  - 雷斯纳-诺德斯特朗黑洞：无自旋、有电荷
  - 克尔-纽曼黑洞：有自旋、有电荷（最一般情况）

黑洞热力学 Black Hole Thermodynamics:
霍金在1974年发现黑洞并非完全"黑"，它们会辐射热辐射（霍金辐射）。
这一发现将引力、量子力学和热力学联系在一起，是理论物理最重要的
成就之一。

关键公式 Key Formulas:
  - 史瓦西半径: r_s = 2GM/c²
  - 霍金温度: T_H = ℏc³/(8πGMk_B)
  - 贝肯斯坦-霍金熵: S = k_B c³ A/(4Gℏ)
  - 霍金辐射功率: P = ℏc⁶/(15360πG²M²)
  - 蒸发时间: t_evap = 5120πG²M³/(ℏc⁴)

单位说明 Units:
  - 温度 Temperature: K (开尔文)
  - 熵 Entropy: J/K
  - 功率 Power: W (瓦特)
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import G, c, hbar, k_B, M_sun

# I AM NOT DONE

# =============================================================================
# 练习 4.1: 史瓦西黑洞
# Exercise 4.1: Schwarzschild Black Hole
#
# 物理背景 Physical Background:
# 史瓦西黑洞是最简单的黑洞解：球对称、静态、不带电荷、不旋转。
# 它由唯一的参数——质量M——完全描述。
#
# 关键特征 Key Features:
# - 事件视界 (r = r_s): 一旦进入就无法返回的边界
# - 奇点 (r = 0): 时空曲率发散，物理定律失效
# - 视界面积只增不减（经典情况）
# =============================================================================

def schwarzschild_radius(M):
    """
    计算史瓦西半径（事件视界半径）
    Calculate Schwarzschild radius (event horizon radius)

    公式 Formula: r_s = 2GM/c²

    参数 Parameters:
        M: 黑洞质量 Black hole mass (kg)

    返回 Returns:
        r_s: 史瓦西半径 Schwarzschild radius (m)
    """
    return 2 * G * M / c**2


def event_horizon_area(M):
    """
    计算事件视界面积
    Calculate event horizon area

    公式 Formula: A = 4πr_s² = 16πG²M²/c⁴

    参数 Parameters:
        M: 黑洞质量 Black hole mass (kg)

    返回 Returns:
        A: 视界面积 Horizon area (m²)

    物理意义 Physical Meaning:
        视界面积在经典过程中只能增加，不能减少（面积定理）
        这与热力学第二定律（熵增）有深刻联系
    """
    r_s = schwarzschild_radius(M)
    return 4 * np.pi * r_s**2


def escape_velocity(M, r):
    """
    计算逃逸速度
    Calculate escape velocity

    公式 Formula: v_esc = √(2GM/r)

    参数 Parameters:
        M: 中心质量 Central mass (kg)
        r: 距离 Distance (m)

    返回 Returns:
        v_esc: 逃逸速度 Escape velocity (m/s)

    物理意义 Physical Meaning:
        在视界处 (r = r_s)，逃逸速度恰好等于光速 c
        这正是黑洞"黑"的原因——连光都无法逃逸
    """
    return np.sqrt(2 * G * M / r)


# =============================================================================
# 练习 4.2: 黑洞热力学
# Exercise 4.2: Black Hole Thermodynamics
#
# 物理背景 Physical Background:
# 1974年，霍金惊人地发现黑洞会发出热辐射（霍金辐射）。这一发现
# 将量子力学、广义相对论和热力学统一起来，是理论物理最重要的进展之一。
#
# 黑洞热力学四定律（类比经典热力学）:
# - 第零定律：视界表面引力κ处处相等（类比温度均匀）
# - 第一定律：dM = κdA/(8πG) + ΩdJ + ΦdQ（能量守恒）
# - 第二定律：视界面积不减少 δA ≥ 0（熵增）
# - 第三定律：无法通过有限步骤使 κ → 0（无法达到绝对零度）
# =============================================================================

def hawking_temperature(M):
    """
    计算霍金温度
    Calculate Hawking temperature

    公式 Formula: T_H = ℏc³/(8πGMk_B)

    参数 Parameters:
        M: 黑洞质量 Black hole mass (kg)

    返回 Returns:
        T: 霍金温度 Hawking temperature (K)

    物理意义 Physical Meaning:
        霍金温度与质量成反比：小黑洞更热！
        太阳质量黑洞: T ≈ 6×10⁻⁸ K（远低于CMB温度2.7K）
        原初黑洞 M ≈ 10¹² kg: T ≈ 10¹¹ K（极热，可能正在蒸发）
    """
    return hbar * c**3 / (8 * np.pi * G * M * k_B)


def bekenstein_hawking_entropy(M):
    """
    计算贝肯斯坦-霍金熵
    Calculate Bekenstein-Hawking entropy

    公式 Formula: S = k_B c³ A/(4Gℏ)

    参数 Parameters:
        M: 黑洞质量 Black hole mass (kg)

    返回 Returns:
        S: 黑洞熵 Black hole entropy (J/K)

    物理意义 Physical Meaning:
        黑洞熵与视界面积成正比（而非体积！）
        这暗示了"全息原理"：信息存储在边界上
        太阳质量黑洞的熵约为 10⁷⁷ k_B，远大于太阳本身
    """
    A = event_horizon_area(M)
    return k_B * c**3 * A / (4 * G * hbar)


def hawking_luminosity(M):
    """
    计算霍金辐射功率
    Calculate Hawking radiation luminosity

    公式 Formula: P = ℏc⁶/(15360πG²M²)

    参数 Parameters:
        M: 黑洞质量 Black hole mass (kg)

    返回 Returns:
        P: 辐射功率 Luminosity (W)

    物理意义 Physical Meaning:
        功率与M²成反比：小黑洞辐射得更快
        太阳质量黑洞: P ≈ 10⁻²⁹ W（完全可忽略）
        原初黑洞 M ≈ 10¹² kg: P ≈ 10¹¹ W（显著辐射）
    """
    return hbar * c**6 / (15360 * np.pi * G**2 * M**2)


# =============================================================================
# 练习 4.3: 黑洞蒸发
# Exercise 4.3: Black Hole Evaporation
#
# 物理背景 Physical Background:
# 由于霍金辐射，黑洞会逐渐失去质量并最终"蒸发"消失。
# 这个过程对于恒星级和超大质量黑洞来说极其缓慢，但对于小黑洞
# （如原初黑洞）可能是可观测的。
#
# 蒸发过程的特点 Characteristics:
# - 蒸发时间 t_evap ∝ M³: 大黑洞寿命极长
# - 蒸发速度 dM/dt ∝ -1/M²: 越小越快
# - 最后阶段是爆发性的"黑洞爆炸"
# =============================================================================

def evaporation_time(M):
    """
    计算黑洞完全蒸发所需时间
    Calculate time for complete black hole evaporation

    公式 Formula: t_evap = 5120πG²M³/(ℏc⁴)

    参数 Parameters:
        M: 黑洞初始质量 Initial black hole mass (kg)

    返回 Returns:
        t: 蒸发时间 Evaporation time (s)

    物理意义 Physical Meaning:
        太阳质量黑洞: t_evap ≈ 10⁶⁷ 年（远超宇宙年龄10¹⁰年）
        恰好在宇宙年龄内蒸发完的原初黑洞: M ≈ 5×10¹¹ kg
    """
    return 5120 * np.pi * G**2 * M**3 / (hbar * c**4)


def mass_vs_time(M0, t):
    """
    计算黑洞质量随时间的变化
    Calculate black hole mass evolution with time

    公式 Formula: M(t) = (M₀³ - 3K×t)^(1/3)，其中 K = ℏc⁴/(5120πG²)

    参数 Parameters:
        M0: 初始质量 Initial mass (kg)
        t: 时间 Time (s)

    返回 Returns:
        M: 当前质量 Current mass (kg)

    物理意义 Physical Meaning:
        质量减少速度随着黑洞变小而加快
        最终时刻 M → 0，功率 P → ∞（"黑洞爆炸"）
    """
    k = hbar * c**4 / (5120 * np.pi * G**2)
    M_cubed = M0**3 - 3 * k * t
    if M_cubed <= 0:
        return 0  # 黑洞已完全蒸发
    return M_cubed**(1/3)


# =============================================================================
# 练习 4.4: 克尔黑洞
# Exercise 4.4: Kerr Black Hole
# =============================================================================
def kerr_outer_horizon(M, a):
    """
    克尔黑洞外视界
    r_+ = GM/c² + √((GM/c²)² - a²)
    a = J/(Mc): 约化角动量
    """
    r_g = G * M / c**2
    if a > r_g:
        return None  # 裸奇点
    return r_g + np.sqrt(r_g**2 - a**2)

def kerr_ergosphere(M, a, theta):
    """
    克尔黑洞能层半径
    r_e = GM/c² + √((GM/c²)² - a²cos²θ)
    """
    r_g = G * M / c**2
    return r_g + np.sqrt(r_g**2 - a**2 * np.cos(theta)**2)

def frame_dragging_angular_velocity(M, a, r):
    """
    参考系拖曳角速度（简化）
    Ω = 2GMa/(c²r³)
    """
    return 2 * G * M * a / (c**2 * r**3)


# =============================================================================
# 练习 4.5: 引力波
# Exercise 4.5: Gravitational Waves
# =============================================================================
def gravitational_wave_frequency(M_chirp, t_coalescence):
    """
    引力波频率演化（啁啾质量近似）
    f ≈ (5/(256t))^(3/8) × (c³/(πGM_chirp))^(5/8)
    """
    if t_coalescence <= 0:
        return np.inf
    term1 = (5 / (256 * t_coalescence))**(3/8)
    term2 = (c**3 / (np.pi * G * M_chirp))**(5/8)
    return term1 * term2

def chirp_mass(m1, m2):
    """
    啁啾质量 M_c = (m1×m2)^(3/5) / (m1+m2)^(1/5)
    """
    return (m1 * m2)**(3/5) / (m1 + m2)**(1/5)

def gravitational_wave_strain(M_chirp, r, f):
    """
    引力波应变幅度（简化）
    h ≈ (4/r) × (GM_c/c²)^(5/3) × (πf/c)^(2/3)
    """
    return (4/r) * (G * M_chirp / c**2)**(5/3) * (np.pi * f / c)**(2/3)


# =============================================================================
# 练习 4.6: 潮汐瓦解
# Exercise 4.6: Tidal Disruption
# =============================================================================
def tidal_radius(M_bh, M_star, R_star):
    """
    潮汐瓦解半径
    r_t ≈ R_star × (M_bh/M_star)^(1/3)
    """
    return R_star * (M_bh / M_star)**(1/3)

def spaghettification_distance(M, delta_r):
    """
    "意面化"发生的距离（潮汐力等于人体承受极限）
    简化: r ≈ (2GM×delta_r/a_max)^(1/3)
    a_max ≈ 10g
    """
    a_max = 10 * 9.81  # 人体极限加速度
    return (2 * G * M * delta_r / a_max)**(1/3)


# =============================================================================
# 可视化
# =============================================================================
def plot_black_holes():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 史瓦西半径vs质量
    ax1 = axes[0, 0]
    M = np.logspace(-10, 10, 100) * M_sun
    r_s = [schwarzschild_radius(m) / 1000 for m in M]  # km

    ax1.loglog(M/M_sun, r_s, 'b-', linewidth=2)
    ax1.axhline(y=3, color='r', linestyle='--', alpha=0.5, label='3 km (1 M☉)')
    ax1.set_xlabel('M/M☉')
    ax1.set_ylabel('r_s (km)')
    ax1.set_title('史瓦西半径')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 霍金温度
    ax2 = axes[0, 1]
    T_H = [hawking_temperature(m) for m in M]

    ax2.loglog(M/M_sun, T_H, 'r-', linewidth=2)
    ax2.axhline(y=2.7, color='g', linestyle='--', alpha=0.5, label='CMB (2.7K)')
    ax2.set_xlabel('M/M☉')
    ax2.set_ylabel('T_H (K)')
    ax2.set_title('霍金温度')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 蒸发时间
    ax3 = axes[0, 2]
    M_small = np.logspace(-20, -5, 100) * M_sun
    t_evap = [evaporation_time(m) / (365.25*24*3600) for m in M_small]  # 年

    ax3.loglog(M_small/M_sun, t_evap, 'g-', linewidth=2)
    ax3.axhline(y=13.8e9, color='orange', linestyle='--', alpha=0.5, label='宇宙年龄')
    ax3.set_xlabel('M/M☉')
    ax3.set_ylabel('蒸发时间 (年)')
    ax3.set_title('黑洞蒸发')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 克尔黑洞视界
    ax4 = axes[1, 0]
    M_kerr = 10 * M_sun
    r_g = G * M_kerr / c**2

    a_range = np.linspace(0, 0.99*r_g, 100)
    r_plus = [kerr_outer_horizon(M_kerr, a) for a in a_range]

    theta = np.linspace(0, np.pi, 100)
    for a_frac in [0, 0.5, 0.9]:
        a = a_frac * r_g
        r_ergo = [kerr_ergosphere(M_kerr, a, t) for t in theta]
        label = f'a/r_g = {a_frac}'
        ax4.polar(theta, np.array(r_ergo)/r_g, label=label, linewidth=2)

    ax4.set_title('克尔黑洞能层')
    ax4.legend(loc='upper right')

    # 5. 引力波频率
    ax5 = axes[1, 1]
    M_c = chirp_mass(30*M_sun, 30*M_sun)
    t_coal = np.logspace(-2, 3, 100)  # 秒
    f_gw = [gravitational_wave_frequency(M_c, t) for t in t_coal]

    ax5.loglog(t_coal, f_gw, 'purple', linewidth=2)
    ax5.axhline(y=100, color='r', linestyle='--', alpha=0.5, label='LIGO敏感区')
    ax5.set_xlabel('距并合时间 (s)')
    ax5.set_ylabel('f (Hz)')
    ax5.set_title('引力波频率啁啾')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. 潮汐瓦解
    ax6 = axes[1, 2]
    M_bh = np.logspace(5, 9, 100) * M_sun
    R_sun_val = 6.96e8
    r_t = [tidal_radius(m, M_sun, R_sun_val) for m in M_bh]
    r_s_bh = [schwarzschild_radius(m) for m in M_bh]

    ax6.loglog(M_bh/M_sun, np.array(r_t)/1e9, 'b-', label='潮汐半径', linewidth=2)
    ax6.loglog(M_bh/M_sun, np.array(r_s_bh)/1e9, 'r-', label='视界半径', linewidth=2)
    ax6.set_xlabel('M_BH/M☉')
    ax6.set_ylabel('半径 (10⁹ m)')
    ax6.set_title('潮汐瓦解 vs 视界')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('black_holes.png', dpi=150)
    print("图像已保存为 black_holes.png")
    plt.show()


def verify():
    """
    验证所有练习的正确性
    Verify all exercises for correctness
    """
    all_passed = True

    # 检查 4.1 - 史瓦西半径 Schwarzschild radius
    r_s = schwarzschild_radius(M_sun)
    expected_rs = 2953  # m（约3公里）
    if not np.isclose(r_s, expected_rs, rtol=0.01):
        print("错误 4.1: 史瓦西半径计算不正确，请检查公式 r_s = 2GM/c²")
        all_passed = False
    else:
        print(f"正确 4.1: 史瓦西半径 (r_s(M_sun) = {r_s:.0f} m)")

    # 检查 4.2 - 霍金温度 Hawking temperature
    T = hawking_temperature(M_sun)
    expected_T = 6.17e-8  # K（极低温度）
    if not np.isclose(T, expected_T, rtol=0.1):
        print(f"错误 4.2: 霍金温度计算不正确，请检查公式 T = ℏc³/(8πGMk_B)")
        all_passed = False
    else:
        print(f"正确 4.2: 霍金温度 (T(M_sun) = {T:.2e} K)")

    # 检查 4.3 - 蒸发时间 Evaporation time
    t_evap = evaporation_time(M_sun)
    if t_evap < 1e60:
        print("错误 4.3: 太阳质量黑洞蒸发时间应远大于宇宙年龄")
        all_passed = False
    else:
        print(f"正确 4.3: 蒸发时间 (t >> 宇宙年龄)")

    # 检查 4.4 - 克尔黑洞 Kerr black hole
    r_plus = kerr_outer_horizon(M_sun, 0)
    if not np.isclose(r_plus, schwarzschild_radius(M_sun)/2, rtol=0.01):
        print("错误 4.4: 当 a=0 时，克尔黑洞应退化为史瓦西黑洞")
        all_passed = False
    else:
        print("正确 4.4: 克尔黑洞视界计算")

    # 检查 4.5 - 啁啾质量 Chirp mass
    M_c = chirp_mass(30*M_sun, 30*M_sun)
    expected_Mc = 30 * M_sun * 2**(-1/5)
    if not np.isclose(M_c, expected_Mc, rtol=0.01):
        print("错误 4.5: 啁啾质量计算不正确，请检查公式")
        all_passed = False
    else:
        print(f"正确 4.5: 引力波参数 (M_c = {M_c/M_sun:.1f} M_sun)")

    # 检查 4.6 - 潮汐瓦解 Tidal disruption
    r_t = tidal_radius(1e6*M_sun, M_sun, 6.96e8)
    r_s_smbh = schwarzschild_radius(1e6*M_sun)
    if r_t < r_s_smbh:
        print("错误 4.6: 对于10⁶ M_sun黑洞，恒星应在视界外被瓦解")
        all_passed = False
    else:
        print(f"正确 4.6: 潮汐瓦解 (r_t > r_s)")

    if all_passed:
        print("\n所有测试通过！")
        try:
            plot_black_holes()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("黑洞物理 Black Hole Physics")
    print("=" * 50)
    verify()
