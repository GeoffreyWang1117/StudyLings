"""
宇宙学基础 Cosmology Fundamentals (Friedmann Equations)
难度 Difficulty: ★★★★★

学习目标 Learning Objectives:
- 理解Friedmann方程及其描述宇宙演化的核心地位
- 掌握宇宙膨胀的数学和物理描述：哈勃参数、标度因子
- 分析不同宇宙组分（物质、辐射、暗能量）的演化规律
- 计算宇宙年龄、各种宇宙学距离和减速参数
- 理解宇宙微波背景辐射(CMB)的物理意义

物理背景 Physical Background:
弗里德曼方程是应用爱因斯坦场方程于均匀各向同性宇宙（宇宙学原理）
得到的结果。这些方程控制着宇宙的整体演化，包括：
  - 宇宙的膨胀历史
  - 物质和辐射密度的演化
  - 宇宙的加速或减速膨胀

当前宇宙学标准模型（ΛCDM模型）的关键参数:
  - H₀ ≈ 70 km/s/Mpc (哈勃常数)
  - Ω_m ≈ 0.3 (物质密度参数，包括暗物质)
  - Ω_Λ ≈ 0.7 (暗能量密度参数)
  - Ω_r ≈ 9×10⁻⁵ (辐射密度参数)

关键公式 Key Formulas:
  - 第一弗里德曼方程: H² = (8πG/3)ρ - kc²/a² + Λc²/3
  - 第二弗里德曼方程: ä/a = -(4πG/3)(ρ + 3p/c²) + Λc²/3
  - 连续性方程: dρ/dt + 3H(ρ + p/c²) = 0
  - 密度演化: ρ_m ∝ a⁻³, ρ_r ∝ a⁻⁴, ρ_Λ = const

单位说明 Units:
  - 哈勃常数 H₀: km/s/Mpc 或 s⁻¹
  - 密度 ρ: kg/m³
  - 距离: Mpc (百万秒差距) = 3.086×10²² m
  - 时间: Gyr (十亿年) = 3.15×10¹⁶ s
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint, quad
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import G, c, hbar, k_B

# I AM NOT DONE

# =============================================================================
# 宇宙学常数 Cosmological Constants
# =============================================================================
# 哈勃常数 Hubble constant
H_0 = 70  # km/s/Mpc (观测值，有约±5的不确定性)
H_0_SI = H_0 * 1e3 / 3.086e22  # 转换为 SI 单位 (s⁻¹ = 1/s)

# 当前密度参数 Present-day density parameters (ΛCDM模型)
# 这些参数满足: Ω_m + Ω_r + Ω_Λ + Ω_k = 1
Omega_m0 = 0.3      # 物质（重子+暗物质）Matter (baryons + dark matter)
Omega_r0 = 9e-5     # 辐射（光子+中微子）Radiation (photons + neutrinos)
Omega_Lambda = 0.7  # 暗能量（宇宙学常数）Dark energy (cosmological constant)
Omega_k0 = 0        # 曲率（平坦宇宙）Curvature (flat universe)

# =============================================================================
# 练习 1.1: 哈勃参数
# Exercise 1.1: Hubble Parameter
#
# 物理背景 Physical Background:
# 哈勃参数 H(t) = ȧ/a 描述了宇宙膨胀的速率。它随时间（或等效地，
# 随标度因子）变化，反映了宇宙不同组分的主导地位如何随时间改变。
#
# 演化规律 Evolution:
# - 早期宇宙（辐射主导）: H ∝ a⁻²
# - 中期宇宙（物质主导）: H ∝ a⁻³/²
# - 晚期宇宙（暗能量主导）: H → 常数
# =============================================================================

def hubble_parameter(a, Omega_m=Omega_m0, Omega_r=Omega_r0,
                    Omega_L=Omega_Lambda, Omega_k=Omega_k0):
    """
    计算哈勃参数随标度因子的变化
    Calculate Hubble parameter as function of scale factor

    公式 Formula: H(a)² = H₀² [Ω_r/a⁴ + Ω_m/a³ + Ω_k/a² + Ω_Λ]

    参数 Parameters:
        a: 标度因子 Scale factor (今天 a=1)
        Omega_m: 物质密度参数 Matter density parameter
        Omega_r: 辐射密度参数 Radiation density parameter
        Omega_L: 暗能量密度参数 Dark energy density parameter
        Omega_k: 曲率参数 Curvature parameter

    返回 Returns:
        H: 哈勃参数 Hubble parameter (s⁻¹)

    物理意义 Physical Meaning:
        不同项的贡献随a的变化说明了宇宙组分如何主导不同时期
    """
    # TODO: 计算哈勃参数
    # 提示：每个组分以不同的幂次依赖于标度因子
    H_squared = H_0_SI**2 * (Omega_r / a**4 + Omega_m / a**3 +
                             Omega_k / a**2 + Omega_L)
    return np.sqrt(H_squared)


def hubble_time():
    """
    计算哈勃时间
    Calculate Hubble time

    公式 Formula: t_H = 1/H₀

    返回 Returns:
        t_H: 哈勃时间 Hubble time (s)

    物理意义 Physical Meaning:
        哈勃时间是宇宙年龄的特征尺度，约为14 Gyr
    """
    return 1 / H_0_SI


def hubble_distance():
    """
    计算哈勃距离
    Calculate Hubble distance

    公式 Formula: d_H = c/H₀

    返回 Returns:
        d_H: 哈勃距离 Hubble distance (m)

    物理意义 Physical Meaning:
        哈勃距离是可观测宇宙大小的特征尺度，约为4.4 Gpc
    """
    return c / H_0_SI


# =============================================================================
# 练习 1.2: 临界密度
# Exercise 1.2: Critical Density
#
# 物理背景 Physical Background:
# 临界密度是区分宇宙几何（开放、平坦、闭合）的关键密度值。
# 如果宇宙的总密度等于临界密度，宇宙是平坦的（欧几里得几何）。
#
# 密度演化 Density Evolution:
# 不同组分的密度随宇宙膨胀以不同方式稀释:
# - 物质: ρ_m ∝ a⁻³ (体积稀释)
# - 辐射: ρ_r ∝ a⁻⁴ (体积稀释 + 红移)
# - 暗能量: ρ_Λ = 常数 (不稀释，这正是"暗能量"的奇特之处)
# =============================================================================

def critical_density(H):
    """
    计算临界密度
    Calculate critical density

    公式 Formula: ρ_c = 3H²/(8πG)

    参数 Parameters:
        H: 哈勃参数 Hubble parameter (s⁻¹)

    返回 Returns:
        rho_c: 临界密度 Critical density (kg/m³)

    物理意义 Physical Meaning:
        今天的临界密度约为 ρ_c,0 ≈ 9.5×10⁻²⁷ kg/m³
        这大约相当于每立方米6个氢原子
    """
    # TODO: 计算临界密度
    # 提示：这是使宇宙平坦所需的总密度
    rho_c = 3 * H**2 / (8 * np.pi * G)
    return rho_c


def matter_density(a, rho_m0):
    """
    计算物质密度随标度因子的变化
    Calculate matter density evolution with scale factor

    公式 Formula: ρ_m(a) = ρ_m0 / a³

    参数 Parameters:
        a: 标度因子 Scale factor
        rho_m0: 今天的物质密度 Present matter density (kg/m³)

    返回 Returns:
        rho_m: 物质密度 Matter density (kg/m³)

    物理意义 Physical Meaning:
        a⁻³ 因子来自体积的增加（V ∝ a³）
    """
    return rho_m0 / a**3


def radiation_density(a, rho_r0):
    """
    计算辐射密度随标度因子的变化
    Calculate radiation density evolution with scale factor

    公式 Formula: ρ_r(a) = ρ_r0 / a⁴

    参数 Parameters:
        a: 标度因子 Scale factor
        rho_r0: 今天的辐射密度 Present radiation density (kg/m³)

    返回 Returns:
        rho_r: 辐射密度 Radiation density (kg/m³)

    物理意义 Physical Meaning:
        a⁻⁴ = a⁻³（体积稀释）× a⁻¹（波长红移导致能量降低）
    """
    return rho_r0 / a**4


def dark_energy_density(rho_Lambda):
    """
    计算暗能量密度（宇宙学常数模型）
    Calculate dark energy density (cosmological constant model)

    公式 Formula: ρ_Λ = 常数 (不随时间变化)

    参数 Parameters:
        rho_Lambda: 暗能量密度 Dark energy density (kg/m³)

    返回 Returns:
        rho_Lambda: 暗能量密度（不变）Dark energy density (unchanged)

    物理意义 Physical Meaning:
        暗能量密度不随宇宙膨胀而稀释，这是导致宇宙加速膨胀的原因
    """
    return rho_Lambda


# =============================================================================
# 练习 1.3: 宇宙年龄
# Exercise 1.3: Age of the Universe
# =============================================================================
def cosmic_time_integrand(a, Omega_m, Omega_r, Omega_L, Omega_k):
    """
    宇宙时间积分被积函数
    dt = da / (aH(a))
    """
    if a <= 0:
        return 0
    H = hubble_parameter(a, Omega_m, Omega_r, Omega_L, Omega_k)
    return 1 / (a * H)


def age_of_universe(Omega_m=Omega_m0, Omega_r=Omega_r0,
                   Omega_L=Omega_Lambda, Omega_k=Omega_k0):
    """
    计算宇宙年龄
    t₀ = ∫₀¹ da/(aH(a))
    """
    # TODO: 数值积分计算年龄
    result, _ = quad(cosmic_time_integrand, 1e-10, 1,
                     args=(Omega_m, Omega_r, Omega_L, Omega_k))
    return result


def lookback_time(z, Omega_m=Omega_m0, Omega_r=Omega_r0,
                  Omega_L=Omega_Lambda, Omega_k=Omega_k0):
    """
    回溯时间（从今天到红移z的时间）
    t_lookback = ∫_{a}^{1} da/(aH(a))
    其中 a = 1/(1+z)
    """
    a = 1 / (1 + z)
    result, _ = quad(cosmic_time_integrand, a, 1,
                     args=(Omega_m, Omega_r, Omega_L, Omega_k))
    return result


# =============================================================================
# 练习 1.4: 减速参数
# Exercise 1.4: Deceleration Parameter
# =============================================================================
def deceleration_parameter(a, Omega_m=Omega_m0, Omega_r=Omega_r0,
                           Omega_L=Omega_Lambda):
    """
    减速参数
    q = -a a''/(a')² = Ω_r/a⁴ + Ω_m/(2a³) - Ω_Λ
    (归一化到今天的值)

    q > 0: 减速膨胀
    q < 0: 加速膨胀
    """
    # TODO: 计算减速参数
    numerator = Omega_r / a**4 + Omega_m / (2 * a**3) - Omega_L
    denominator = Omega_r / a**4 + Omega_m / a**3 + Omega_L
    q = numerator / denominator
    return q


def acceleration_epoch_redshift():
    """
    宇宙开始加速膨胀的红移 (q=0时)
    对于 Ω_m = 0.3, Ω_Λ = 0.7:
    z_acc ≈ (2Ω_Λ/Ω_m)^(1/3) - 1
    """
    z_acc = (2 * Omega_Lambda / Omega_m0)**(1/3) - 1
    return z_acc


# =============================================================================
# 练习 1.5: 距离-红移关系
# Exercise 1.5: Distance-Redshift Relation
# =============================================================================
def comoving_distance(z, Omega_m=Omega_m0, Omega_r=Omega_r0,
                      Omega_L=Omega_Lambda, Omega_k=Omega_k0):
    """
    共动距离
    D_c = c ∫₀^z dz'/H(z')
    """
    def integrand(z_prime):
        a = 1 / (1 + z_prime)
        H = hubble_parameter(a, Omega_m, Omega_r, Omega_L, Omega_k)
        return c / H

    # TODO: 数值积分
    result, _ = quad(integrand, 0, z)
    return result


def luminosity_distance(z, Omega_m=Omega_m0, Omega_r=Omega_r0,
                        Omega_L=Omega_Lambda, Omega_k=Omega_k0):
    """
    光度距离 D_L = (1+z) D_c (平坦宇宙)
    """
    D_c = comoving_distance(z, Omega_m, Omega_r, Omega_L, Omega_k)
    return (1 + z) * D_c


def angular_diameter_distance(z, Omega_m=Omega_m0, Omega_r=Omega_r0,
                               Omega_L=Omega_Lambda, Omega_k=Omega_k0):
    """
    角直径距离 D_A = D_c/(1+z) (平坦宇宙)
    """
    D_c = comoving_distance(z, Omega_m, Omega_r, Omega_L, Omega_k)
    return D_c / (1 + z)


# =============================================================================
# 练习 1.6: 标度因子演化
# Exercise 1.6: Scale Factor Evolution
# =============================================================================
def scale_factor_ode(a, t, Omega_m, Omega_r, Omega_L):
    """
    标度因子演化的微分方程
    da/dt = a H(a)
    """
    if a <= 0:
        return 0
    H = hubble_parameter(a, Omega_m, Omega_r, Omega_L, 0)
    return a * H


def solve_scale_factor(t_range, Omega_m=Omega_m0, Omega_r=Omega_r0,
                       Omega_L=Omega_Lambda):
    """
    求解标度因子随时间的演化
    """
    a0 = 1e-6  # 初始标度因子
    solution = odeint(scale_factor_ode, a0, t_range, args=(Omega_m, Omega_r, Omega_L))
    return solution.flatten()


def matter_radiation_equality():
    """
    物质-辐射相等时期的标度因子
    a_eq = Ω_r / Ω_m
    """
    return Omega_r0 / Omega_m0


# =============================================================================
# 练习 1.7: 宇宙微波背景
# Exercise 1.7: Cosmic Microwave Background
# =============================================================================
def cmb_temperature(a, T_0=2.725):
    """
    CMB温度随标度因子变化
    T(a) = T₀ / a

    T₀ = 2.725 K (今天的CMB温度)
    """
    return T_0 / a


def cmb_redshift():
    """
    CMB最后散射面的红移
    z_cmb ≈ 1100
    """
    return 1100


def horizon_size_at_cmb():
    """
    CMB时期的粒子视界大小（共动）
    """
    z_cmb = cmb_redshift()
    a_cmb = 1 / (1 + z_cmb)

    def integrand(a):
        if a <= 0:
            return 0
        H = hubble_parameter(a, Omega_m0, Omega_r0, Omega_Lambda, 0)
        return c / (a**2 * H)

    result, _ = quad(integrand, 1e-10, a_cmb)
    return result


# =============================================================================
# 可视化
# =============================================================================
def plot_cosmology():
    """绘制宇宙学相关图"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # 1. 哈勃参数演化
    ax1 = axes[0, 0]
    z_range = np.linspace(0, 10, 200)
    a_range = 1 / (1 + z_range)
    H_values = [hubble_parameter(a) / H_0_SI for a in a_range]

    ax1.plot(z_range, H_values, 'b-', linewidth=2)
    ax1.set_xlabel('Redshift z')
    ax1.set_ylabel('H(z) / H_0')
    ax1.set_title('哈勃参数演化')
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')

    # 2. 密度参数演化
    ax2 = axes[0, 1]
    z_range2 = np.logspace(-1, 4, 200)
    a_range2 = 1 / (1 + z_range2)

    rho_c_today = critical_density(H_0_SI)
    rho_m0 = Omega_m0 * rho_c_today
    rho_r0 = Omega_r0 * rho_c_today
    rho_L = Omega_Lambda * rho_c_today

    Omega_m_z = [matter_density(a, rho_m0) / critical_density(hubble_parameter(a))
                 for a in a_range2]
    Omega_r_z = [radiation_density(a, rho_r0) / critical_density(hubble_parameter(a))
                 for a in a_range2]
    Omega_L_z = [dark_energy_density(rho_L) / critical_density(hubble_parameter(a))
                 for a in a_range2]

    ax2.semilogx(1 + z_range2, Omega_m_z, 'b-', label='Matter', linewidth=2)
    ax2.semilogx(1 + z_range2, Omega_r_z, 'r-', label='Radiation', linewidth=2)
    ax2.semilogx(1 + z_range2, Omega_L_z, 'g-', label='Dark Energy', linewidth=2)
    ax2.axvline(x=1 + matter_radiation_equality()**(-1), color='orange', linestyle='--',
                label='Matter-Radiation Eq.')
    ax2.set_xlabel('1 + z')
    ax2.set_ylabel('Omega_i(z)')
    ax2.set_title('密度参数演化')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 1.1)

    # 3. 距离-红移关系
    ax3 = axes[1, 0]
    z_dist = np.linspace(0.01, 3, 100)
    D_L = [luminosity_distance(z) / 3.086e22 for z in z_dist]  # 转换为 Mpc
    D_A = [angular_diameter_distance(z) / 3.086e22 for z in z_dist]

    ax3.plot(z_dist, D_L, 'b-', label='Luminosity distance D_L', linewidth=2)
    ax3.plot(z_dist, D_A, 'r-', label='Angular diameter distance D_A', linewidth=2)
    ax3.set_xlabel('Redshift z')
    ax3.set_ylabel('Distance (Mpc)')
    ax3.set_title('距离-红移关系')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 减速参数
    ax4 = axes[1, 1]
    z_q = np.linspace(0, 5, 200)
    a_q = 1 / (1 + z_q)
    q_values = [deceleration_parameter(a) for a in a_q]

    ax4.plot(z_q, q_values, 'g-', linewidth=2)
    ax4.axhline(y=0, color='k', linestyle='--')
    z_acc = acceleration_epoch_redshift()
    ax4.axvline(x=z_acc, color='r', linestyle='--',
                label=f'Acceleration starts (z={z_acc:.2f})')
    ax4.fill_between(z_q, q_values, 0, where=np.array(q_values) < 0,
                     alpha=0.3, color='green', label='Accelerating')
    ax4.set_xlabel('Redshift z')
    ax4.set_ylabel('Deceleration parameter q')
    ax4.set_title('减速参数演化')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('cosmology.png', dpi=150)
    print("图像已保存为 cosmology.png")
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

    # 检查 1.1 - 哈勃参数 Hubble parameter
    H_today = hubble_parameter(1)
    if not np.isclose(H_today, H_0_SI, rtol=0.01):
        print("错误 1.1: 今天的哈勃参数应等于 H₀，请检查公式")
        all_passed = False
    else:
        t_H = hubble_time() / (3600 * 24 * 365.25 * 1e9)  # 转换为Gyr
        print(f"正确 1.1: 哈勃参数 (H_0 = {H_0} km/s/Mpc, t_H = {t_H:.1f} Gyr)")

    # 检查 1.2 - 临界密度 Critical density
    rho_c = critical_density(H_0_SI)
    expected_rho_c = 3 * H_0_SI**2 / (8 * np.pi * G)
    if not np.isclose(rho_c, expected_rho_c, rtol=0.01):
        print("错误 1.2: 临界密度计算不正确，请检查公式 ρ_c = 3H²/(8πG)")
        all_passed = False
    else:
        print(f"正确 1.2: 临界密度 (ρ_c = {rho_c:.2e} kg/m³)")

    # 检查 1.3 - 宇宙年龄 Age of universe
    t_age = age_of_universe() / (3600 * 24 * 365.25 * 1e9)  # 转换为Gyr
    if t_age < 10 or t_age > 20:
        print(f"错误 1.3: 宇宙年龄应在10-20 Gyr之间，得到 {t_age:.1f} Gyr")
        all_passed = False
    else:
        print(f"正确 1.3: 宇宙年龄 (t₀ = {t_age:.1f} Gyr)")

    # 检查 1.4 - 减速参数 Deceleration parameter
    q_today = deceleration_parameter(1)
    if q_today >= 0:
        print("错误 1.4: 当前宇宙应在加速膨胀 (q < 0)")
        all_passed = False
    else:
        z_acc = acceleration_epoch_redshift()
        print(f"正确 1.4: 减速参数 (q₀ = {q_today:.2f}, 加速始于 z = {z_acc:.2f})")

    # 检查 1.5 - 距离-红移关系 Distance-redshift relation
    D_L_z1 = luminosity_distance(1) / 3.086e22  # 转换为 Mpc
    if D_L_z1 < 3000 or D_L_z1 > 10000:
        print(f"错误 1.5: 光度距离值不合理")
        all_passed = False
    else:
        print(f"正确 1.5: 距离-红移关系 (D_L(z=1) = {D_L_z1:.0f} Mpc)")

    # 检查 1.6 - 物质-辐射相等时期 Matter-radiation equality
    a_eq = matter_radiation_equality()
    z_eq = 1 / a_eq - 1
    if z_eq < 1000 or z_eq > 10000:
        print("错误 1.6: 物质-辐射相等的红移应在1000-10000之间")
        all_passed = False
    else:
        print(f"正确 1.6: 物质-辐射相等 (z_eq = {z_eq:.0f})")

    # 检查 1.7 - 宇宙微波背景 CMB
    T_cmb = cmb_temperature(1)
    if not np.isclose(T_cmb, 2.725, rtol=0.01):
        print("错误 1.7: 今天的CMB温度应为约2.725 K")
        all_passed = False
    else:
        z_cmb = cmb_redshift()
        T_at_cmb = cmb_temperature(1 / (1 + z_cmb))
        print(f"正确 1.7: CMB (T₀ = {T_cmb} K, T(z=1100) = {T_at_cmb:.0f} K)")

    if all_passed:
        print("\n所有测试通过！正在生成可视化...")
        try:
            plot_cosmology()
        except Exception as e:
            print(f"可视化生成失败: {e}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("宇宙学基础 Cosmology Fundamentals")
    print("=" * 50)
    verify()
