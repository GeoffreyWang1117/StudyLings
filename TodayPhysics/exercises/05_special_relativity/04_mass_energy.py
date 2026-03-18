"""
质能等价 Mass-Energy Equivalence
难度 Difficulty: ★★★★

学习目标 Learning Objectives:
- 深入理解质能关系 E=mc² 的物理意义
  Deeply understand the physical meaning of E=mc²
- 掌握核反应中的质量亏损和结合能计算
  Master mass defect and binding energy in nuclear reactions
- 分析核裂变和核聚变的能量释放
  Analyze energy release in nuclear fission and fusion
- 理解粒子湮灭和质量测量
  Understand particle annihilation and mass measurement

物理背景 Physical Background:
爱因斯坦的质能等价原理 E=mc² 是物理学最著名的方程。
它表明质量和能量是同一物理量的两种表现形式，可以相互转换。

静止能量 E₀ = mc²:
- 1 kg 质量等价于约 9×10¹⁶ J 能量
- 电子静止能量: 0.511 MeV
- 质子静止能量: 938.3 MeV

结合能 Binding Energy:
- 原子核的质量小于组成它的核子质量之和
- 质量亏损: Δm = Z×m_H + N×m_n - M_nucleus
- 结合能: B = Δm × c²，表示将核子分开需要的能量
- Fe-56 的每核子结合能最大（约 8.8 MeV），是核稳定性的峰值

核反应能量:
- 裂变: 重核分裂成轻核，释放约 200 MeV/核（如 U-235）
- 聚变: 轻核结合成重核，释放约 17.6 MeV（D-T反应）
- 湮灭: 正反物质完全转化为能量，效率 100%

单位说明 Units:
- 质量: kg, u (原子质量单位), MeV/c²
- 能量: J, eV, keV, MeV, GeV
- 1 u = 1.66054×10⁻²⁷ kg = 931.5 MeV/c²
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import c, m_e, m_p, eV

# I AM NOT DONE

# 原子质量单位 Atomic mass unit
u = 1.66054e-27  # kg, 1 u ≈ 931.5 MeV/c²
MeV = 1e6 * eV   # 兆电子伏特

# =============================================================================
# 练习 4.1: 质能等价
# Exercise 4.1: Mass-Energy Equivalence
#
# 物理背景：E=mc² 是爱因斯坦最著名的方程。
# 它表明质量本身就是一种能量形式。
# 即使物体静止，它也具有巨大的内在能量。
#
# Physical background: E=mc² is Einstein's most famous equation.
# Mass itself is a form of energy. Even at rest, objects have immense energy.
# =============================================================================

def rest_mass_energy(m):
    """
    计算静止能量 Calculate rest energy

    公式 Formula: E₀ = mc²

    参数 Parameters:
        m: 静止质量 (kg)

    返回 Returns:
        E0: 静止能量 (J)

    例子：
    - 1 kg → 9×10¹⁶ J（相当于约 20 兆吨 TNT）
    - 电子 → 0.511 MeV
    - 质子 → 938.3 MeV
    """
    return m * c**2


def mass_from_energy(E):
    """
    从能量计算等效质量 Calculate equivalent mass from energy

    公式 Formula: m = E/c²

    参数 Parameters:
        E: 能量 (J)

    返回 Returns:
        m: 等效质量 (kg)

    应用：光子没有静止质量，但有能量，因此有等效质量 m = E/c² = hf/c²
    """
    return E / c**2


# =============================================================================
# 练习 4.2: 结合能
# Exercise 4.2: Binding Energy
#
# 物理背景：原子核的质量小于组成它的核子质量之和！
# 这个"消失"的质量转化为了结合能，是核子结合在一起释放的能量。
# 要把原子核拆成单独的核子，需要提供等量的能量。
#
# Physical background: Nuclear mass is less than the sum of its nucleons!
# This "missing" mass is converted to binding energy.
# =============================================================================

def binding_energy(Z, N, M_atom):
    """
    计算原子核结合能 Calculate nuclear binding energy

    公式 Formula: B = [Z×m_H + N×m_n - M_atom]c²

    参数 Parameters:
        Z: 质子数 (原子序数)
        N: 中子数
        M_atom: 原子质量 (kg)

    返回 Returns:
        B: 结合能 (J)

    物理意义：
    - 结合能 > 0 表示核是稳定的
    - 结合能越大，核越稳定
    - Fe-56 的每核子结合能最大（约 8.8 MeV）
    """
    m_H = 1.007825 * u  # 氢原子质量（包含电子）
    m_n = 1.008665 * u  # 中子质量

    # 质量亏损 = 自由核子质量之和 - 原子核质量
    mass_defect = Z * m_H + N * m_n - M_atom
    return mass_defect * c**2  # E = Δm × c²


def binding_energy_per_nucleon(B, A):
    """
    计算每核子结合能 Calculate binding energy per nucleon

    公式 Formula: B/A

    参数 Parameters:
        B: 总结合能 (J)
        A: 质量数 (A = Z + N)

    返回 Returns:
        B_per_A: 每核子结合能 (J)

    重要性：
    - B/A 是衡量核稳定性的关键指标
    - 最稳定的核（Fe, Ni附近）B/A ≈ 8.8 MeV
    - 轻核和重核的 B/A 都较小
    - 聚变和裂变都是向 Fe-56 靠近的过程
    """
    return B / A


# =============================================================================
# 练习 4.3: 核裂变
# Exercise 4.3: Nuclear Fission
#
# 物理背景：重核（如 U-235）吸收中子后分裂成两个较轻的核。
# 由于轻核的每核子结合能更大，分裂过程释放能量。
# 每次 U-235 裂变释放约 200 MeV 能量，是化学反应的数百万倍。
#
# Physical background: Heavy nuclei (like U-235) split into lighter nuclei.
# Since lighter nuclei have higher binding energy per nucleon, energy is released.
# =============================================================================

def fission_energy_u235():
    """
    U-235 裂变能量 U-235 fission energy

    每个 U-235 核裂变释放约 200 MeV 能量
    其中约 170 MeV 是碎片动能，30 MeV 是中子、γ射线等

    返回 Returns:
        energy: 每次裂变能量 (J)
    """
    return 200 * MeV


def fission_mass_to_energy(m_fuel):
    """
    计算裂变燃料释放的能量 Calculate energy from fission fuel

    参数 Parameters:
        m_fuel: 燃料质量 (kg)

    返回 Returns:
        energy: 释放能量 (J)

    效率约 0.1%：
    - 每次裂变质量亏损约 0.1% × 235u
    - 1 kg U-235 完全裂变释放约 8.2×10¹³ J
    - 相当于约 20,000 吨 TNT
    """
    efficiency = 0.001  # 约 0.1% 质量转化为能量
    return efficiency * m_fuel * c**2


def critical_mass_estimate(density, sigma_f, nu):
    """
    估算临界质量 Estimate critical mass

    临界质量是维持链式反应所需的最小质量。
    当中子产生率等于损失率时达到临界。

    参数 Parameters:
        density: 材料密度 (kg/m³)
        sigma_f: 裂变截面 (m²)
        nu: 每次裂变产生的中子数（U-235 约 2.5）

    返回 Returns:
        M_critical: 临界质量 (kg)

    简化模型：忽略了中子反射、泄漏等复杂因素
    实际 U-235 临界质量约 52 kg（球形，无反射层）
    """
    n = density / (235 * u)  # 核密度
    R_c = 1 / (sigma_f * n * (nu - 1))**(1/3)
    return (4/3) * np.pi * R_c**3 * density


# =============================================================================
# 练习 4.4: 核聚变
# Exercise 4.4: Nuclear Fusion
#
# 物理背景：轻核（氢、氦同位素）聚合成更重的核。
# 由于产物的每核子结合能更大，聚变释放能量。
# 太阳和恒星的能量来源就是核聚变。
# 人类正在研究受控核聚变作为未来的清洁能源。
#
# Physical background: Light nuclei fuse into heavier ones.
# The Sun and stars are powered by nuclear fusion.
# =============================================================================

def fusion_energy_dd():
    """
    D-D 聚变能量 Deuterium-Deuterium fusion energy

    两个氘核聚变有两个等概率的分支:
    D + D → He-3 + n + 3.27 MeV
    D + D → T + p + 4.03 MeV
    平均约 3.65 MeV

    返回 Returns:
        energy: 平均能量 (J)
    """
    return 3.65 * MeV


def fusion_energy_dt():
    """
    D-T 聚变能量 Deuterium-Tritium fusion energy

    反应式: D + T → He-4 + n + 17.6 MeV

    这是最容易实现的聚变反应，阈值温度最低（约 1 亿度）。
    ITER 和 NIF 都是基于 D-T 聚变。

    返回 Returns:
        energy: 聚变能量 (J)
    """
    return 17.6 * MeV


def stellar_fusion_rate(M_star, L_star):
    """
    计算恒星的氢聚变率 Calculate stellar hydrogen fusion rate

    太阳的氢燃烧（pp链）:
    4H → He-4 + 2e⁺ + 2ν + 26.7 MeV
    质量转化效率约 0.7%

    参数 Parameters:
        M_star: 恒星质量 (kg)，用于参考
        L_star: 恒星光度 (W)

    返回 Returns:
        dm_dt: 质量消耗率 (kg/s)

    太阳每秒燃烧约 6×10¹¹ kg 氢，
    转化为约 4.3×10⁹ kg 的能量（约 4×10²⁶ W）
    """
    efficiency = 0.007  # 0.7% 质量转化效率
    return L_star / (efficiency * c**2)


# =============================================================================
# 练习 4.5: 粒子湮灭
# Exercise 4.5: Particle Annihilation
#
# 物理背景：当物质与反物质相遇时，会完全湮灭并转化为能量。
# 这是质能转换效率 100% 的过程！
# 反物质是最高效的能量存储形式，但生产成本极高。
#
# Physical background: When matter meets antimatter, they annihilate
# completely, converting 100% of mass to energy.
# =============================================================================

def electron_positron_annihilation():
    """
    电子-正电子湮灭 Electron-positron annihilation

    反应式: e⁺ + e⁻ → 2γ

    释放能量 = 2 × m_e c² = 1.022 MeV
    产生两个 0.511 MeV 的伽马光子（方向相反以守恒动量）

    返回 Returns:
        energy: 湮灭能量 (J)

    这是正电子发射断层扫描（PET）的原理基础
    """
    return 2 * m_e * c**2


def proton_antiproton_annihilation():
    """
    质子-反质子湮灭 Proton-antiproton annihilation

    反应式: p + p̄ → 多个 π 介子 → 最终产物

    释放能量 ≈ 2 × m_p c² ≈ 1876 MeV
    实际产生多个 π 介子，然后衰变成轻子和光子

    返回 Returns:
        energy: 湮灭能量 (J)
    """
    return 2 * m_p * c**2


def antimatter_energy_density():
    """
    计算反物质的能量密度 Calculate antimatter energy density

    反物质是终极燃料，质能转换效率 100%
    能量密度 = ρc² (物质-反物质都贡献)

    比较:
    - 汽油: ~50 MJ/kg
    - 核裂变: ~80,000,000 MJ/kg (0.1%)
    - 核聚变: ~630,000,000 MJ/kg (0.7%)
    - 反物质: ~90,000,000,000,000 MJ/kg (100%)

    返回 Returns:
        energy_density: 能量密度 (J/m³)
    """
    rho = 1000  # kg/m³（假设液态密度）
    return rho * c**2  # 完全湮灭时的能量密度


# =============================================================================
# 练习 4.6: 质量测量
# Exercise 4.6: Mass Measurement
# =============================================================================
def mass_from_momentum_energy(p, E):
    """
    从动量和能量测量质量
    m = √(E² - (pc)²) / c²
    """
    m_squared_c4 = E**2 - (p * c)**2
    if m_squared_c4 < 0:
        return 0  # 光子或测量误差
    return np.sqrt(m_squared_c4) / c**2

def invariant_mass(E_total, p_total):
    """
    多粒子系统的不变质量
    M_inv = √(E_total² - (p_total c)²) / c²
    """
    return mass_from_momentum_energy(p_total, E_total)


# =============================================================================
# 可视化
# =============================================================================
def plot_mass_energy():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 结合能曲线
    ax1 = axes[0, 0]
    # 一些常见核素的结合能数据
    nuclei = [
        ('H-2', 2, 2.22),
        ('He-4', 4, 28.3),
        ('C-12', 12, 92.2),
        ('O-16', 16, 127.6),
        ('Fe-56', 56, 492.3),
        ('U-235', 235, 1783.9),
        ('U-238', 238, 1801.7)
    ]

    A = [n[1] for n in nuclei]
    B_per_A = [n[2]/n[1] for n in nuclei]

    ax1.plot(A, B_per_A, 'bo-', linewidth=2, markersize=8)
    for n in nuclei:
        ax1.annotate(n[0], (n[1], n[2]/n[1]), xytext=(5, 5),
                    textcoords='offset points', fontsize=9)

    ax1.set_xlabel('质量数 A')
    ax1.set_ylabel('B/A (MeV)')
    ax1.set_title('每核子结合能')
    ax1.grid(True, alpha=0.3)

    # 2. 质能转换
    ax2 = axes[0, 1]
    m = np.logspace(-30, 0, 100)  # kg
    E = [rest_mass_energy(mi) for mi in m]

    ax2.loglog(m, np.array(E)/1e15, 'b-', linewidth=2)
    ax2.axhline(y=4.2e17/1e15, color='r', linestyle='--', alpha=0.5, label='1吨TNT')
    ax2.axvline(x=m_e, color='g', linestyle=':', alpha=0.5, label='电子')
    ax2.axvline(x=m_p, color='orange', linestyle=':', alpha=0.5, label='质子')

    ax2.set_xlabel('质量 (kg)')
    ax2.set_ylabel('能量 (PJ)')
    ax2.set_title('质能等价 E = mc²')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 核反应能量比较
    ax3 = axes[0, 2]
    reactions = ['化学燃烧', 'D-D聚变', 'D-T聚变', 'U-235裂变', '湮灭']
    energies_per_mass = [
        50e6,  # 化学燃烧 ~50 MJ/kg
        3.4e14,  # D-D聚变
        3.4e14,  # D-T聚变
        8.2e13,  # U-235裂变
        9e16   # 湮灭 (c²)
    ]

    ax3.barh(reactions, np.log10(energies_per_mass), alpha=0.7)
    ax3.set_xlabel('log₁₀(能量/质量) [J/kg]')
    ax3.set_title('各种反应的能量密度')
    ax3.grid(True, alpha=0.3)

    # 4. 粒子质量谱
    ax4 = axes[1, 0]
    particles = ['电子', '质子', '中子', 'π⁺', 'K⁺', 'D', 'He-4']
    masses_mev = [0.511, 938.3, 939.6, 139.6, 493.7, 1875.6, 3727.4]

    ax4.barh(particles, masses_mev, alpha=0.7)
    ax4.set_xlabel('mc² (MeV)')
    ax4.set_title('粒子静止能量')
    ax4.grid(True, alpha=0.3)

    # 5. 恒星能量产生
    ax5 = axes[1, 1]
    # 太阳数据
    L_sun = 3.828e26  # W
    M_sun = 1.989e30  # kg

    t = np.linspace(0, 10, 100)  # Gyr
    M_burned = [stellar_fusion_rate(M_sun, L_sun) * ti * 3.156e16 for ti in t]  # kg

    ax5.plot(t, np.array(M_burned)/M_sun * 100, 'orange', linewidth=2)
    ax5.set_xlabel('时间 (Gyr)')
    ax5.set_ylabel('消耗质量 (%)')
    ax5.set_title('太阳氢燃烧')
    ax5.grid(True, alpha=0.3)

    # 6. 相对论质量
    ax6 = axes[1, 2]
    v = np.linspace(0, 0.999, 100) * c
    gamma = 1 / np.sqrt(1 - (v/c)**2)
    m_rel = gamma  # 相对于静质量

    ax6.semilogy(v/c, m_rel, 'b-', linewidth=2)
    ax6.set_xlabel('v/c')
    ax6.set_ylabel('γ = E/(m₀c²)')
    ax6.set_title('相对论总能量/静能量')
    ax6.grid(True, alpha=0.3)
    ax6.set_ylim(1, 100)

    plt.tight_layout()
    plt.savefig('mass_energy.png', dpi=150)
    print("图像已保存为 mass_energy.png")
    plt.show()


def verify():
    """
    验证所有练习的正确性 Verify all exercises

    检查内容 Checks:
    4.1 质能等价（电子静止能量）
    4.2 结合能计算（He-4）
    4.3 核裂变能量（U-235）
    4.4 核聚变能量（D-T）
    4.5 粒子湮灭能量（电子-正电子）
    4.6 质量测量（从能量和动量）
    """
    all_passed = True

    # 检查 4.1 - 质能等价
    E_electron = rest_mass_energy(m_e)
    expected = 0.511 * MeV
    if not np.isclose(E_electron, expected, rtol=0.01):
        print("错误 4.1 电子静止能量计算错误")
        all_passed = False
    else:
        print(f"通过 4.1 质能等价正确 (m_e c² = {E_electron/MeV:.3f} MeV)")

    # 检查 4.2 - He-4结合能
    M_He4 = 4.002603 * u
    B = binding_energy(2, 2, M_He4)
    expected_B = 28.3 * MeV
    if not np.isclose(B, expected_B, rtol=0.05):
        print(f"错误 4.2 He-4 结合能计算错误: {B/MeV:.1f} MeV")
        all_passed = False
    else:
        print(f"通过 4.2 结合能正确 (He-4: {B/MeV:.1f} MeV)")

    # 检查 4.3 - U-235裂变能
    E_fission = fission_energy_u235()
    if not np.isclose(E_fission, 200*MeV, rtol=0.01):
        print("错误 4.3 U-235 裂变能计算错误")
        all_passed = False
    else:
        print(f"通过 4.3 裂变能正确 (U-235: 约 200 MeV)")

    # 检查 4.4 - D-T聚变能
    E_dt = fusion_energy_dt()
    if not np.isclose(E_dt, 17.6*MeV, rtol=0.01):
        print("错误 4.4 D-T 聚变能计算错误")
        all_passed = False
    else:
        print(f"通过 4.4 聚变能正确 (D-T: 17.6 MeV)")

    # 检查 4.5 - 湮灭能量
    E_ann = electron_positron_annihilation()
    expected_ann = 1.022 * MeV
    if not np.isclose(E_ann, expected_ann, rtol=0.01):
        print("错误 4.5 电子-正电子湮灭能量计算错误")
        all_passed = False
    else:
        print(f"通过 4.5 湮灭能量正确 (e⁺e⁻: 1.022 MeV)")

    # 检查 4.6 - 质量测量
    E = 1000 * MeV
    p = 800 * MeV / c
    m = mass_from_momentum_energy(p, E)
    expected_m = np.sqrt(E**2 - (p*c)**2) / c**2
    if not np.isclose(m, expected_m, rtol=0.01):
        print("错误 4.6 从能量动量测量质量计算错误")
        all_passed = False
    else:
        print(f"通过 4.6 质量测量正确 (m² = (E²-(pc)²)/c⁴)")

    if all_passed:
        print("\n所有测试通过！正在生成可视化图像...")
        try:
            plot_mass_energy()
        except Exception as e:
            print(f"可视化生成失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("质能等价 Mass-Energy Equivalence")
    print("=" * 50)
    verify()
