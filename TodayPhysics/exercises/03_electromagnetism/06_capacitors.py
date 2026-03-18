"""
电容器 Capacitors
难度 Difficulty: ★★★

学习目标 Learning Objectives:
- 理解电容的定义和物理意义 (Understand capacitance definition and meaning)
- 掌握各种几何形状电容器的计算 (Master capacitor calculations for various geometries)
- 分析电容器的能量存储机制 (Analyze energy storage in capacitors)
- 计算电容器的串并联组合 (Calculate series and parallel combinations)
- 理解介电质对电容的影响 (Understand dielectric effects on capacitance)

物理背景 Physical Background:
电容器是储存电荷和电能的基本元件。当导体带电时，
其电势与所带电荷成正比，比例系数的倒数就是电容。
电容只与导体的几何形状和介电质有关，与电荷量无关。

核心公式 Key Formulas:
- 电容定义: C = Q/V [F]
- 平行板电容: C = ε₀εᵣA/d
- 球形电容: C = 4πε₀εᵣab/(b-a)
- 圆柱形电容: C = 2πε₀εᵣL/ln(b/a)
- 电容储能: U = (1/2)CV² = (1/2)QV = Q²/(2C)
- 电场能量密度: u = (1/2)ε₀εᵣE² [J/m³]
- 串联: 1/C_eq = Σ(1/Cᵢ)
- 并联: C_eq = ΣCᵢ

介电质效应 Dielectric Effects:
- 介电质极化削弱电场
- 电容增大为真空的 εᵣ 倍
- 极化强度: P = ε₀(εᵣ - 1)E

单位说明 Units:
- 电容: F (法拉) = C/V = A·s/V
- 常用: μF (10⁻⁶F), nF (10⁻⁹F), pF (10⁻¹²F)
- 能量: J (焦耳)
- 能量密度: J/m³
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import epsilon_0

# I AM NOT DONE

# =============================================================================
# 练习 6.1: 电容的基本定义
# Exercise 6.1: Basic Definition of Capacitance
# =============================================================================
# 物理背景 Physical Background:
# 电容是描述导体储存电荷能力的物理量。
# 电容值由导体几何形状和介电质决定，与Q和V无关。
# C = Q/V：给定电压下能储存的电荷量越多，电容越大。

def capacitance_from_charge(Q, V):
    """
    电容的定义
    Definition of capacitance

    参数 Parameters:
        Q: 电荷量 [C]
        V: 电压 [V]

    返回 Returns:
        电容 C [F]

    公式 Formula:
        C = Q/V

    说明: 电容是比例系数，不依赖于Q或V
    """
    # TODO: 计算电容 (Calculate capacitance)
    C = Q / V
    return C


def charge_on_capacitor(C, V):
    """
    电容器上的电荷
    Charge on capacitor

    公式 Formula:
        Q = CV

    应用: 已知电容和电压求电荷量
    """
    return C * V


def voltage_on_capacitor(Q, C):
    """
    电容器上的电压
    Voltage on capacitor

    公式 Formula:
        V = Q/C

    应用: 已知电荷和电容求电压
    """
    return Q / C


# =============================================================================
# 练习 6.2: 平行板电容器
# Exercise 6.2: Parallel Plate Capacitor
# =============================================================================
# 物理背景 Physical Background:
# 平行板电容器是最简单、最常用的电容器结构。
# 两平行导体极板之间形成匀强电场，边缘效应忽略不计。
# 电容与极板面积成正比，与间距成反比。

def parallel_plate_capacitance(A, d, epsilon_r=1.0):
    """
    平行板电容器的电容
    Parallel plate capacitor capacitance

    参数 Parameters:
        A: 极板面积 [m²]
        d: 极板间距 [m]
        epsilon_r: 相对介电常数（无量纲）

    返回 Returns:
        电容 C [F]

    公式 Formula:
        C = ε₀εᵣA/d

    设计原则:
        增大电容：增大A、减小d、使用高εᵣ介电质
        注意: d太小会导致击穿
    """
    # TODO: 计算电容 (Calculate capacitance)
    C = epsilon_0 * epsilon_r * A / d
    return C


def electric_field_parallel_plate(V, d):
    """
    平行板电容器中的匀强电场
    Uniform electric field in parallel plate capacitor

    参数 Parameters:
        V: 两极板间电压 [V]
        d: 极板间距 [m]

    返回 Returns:
        电场强度 E [V/m]

    公式 Formula:
        E = V/d

    说明: 场强均匀，方向从正极板指向负极板
    """
    # TODO: 计算电场强度 (Calculate electric field)
    E = V / d
    return E


def surface_charge_density(Q, A):
    """
    极板表面电荷密度
    Surface charge density

    公式 Formula:
        σ = Q/A [C/m²]

    说明: 正极板 +σ，负极板 -σ
    """
    return Q / A


def field_from_surface_charge(sigma, epsilon_r=1.0):
    """
    从表面电荷密度计算电场
    Electric field from surface charge density

    公式 Formula:
        E = σ/(ε₀εᵣ) [V/m]

    推导: 由高斯定律得出
    """
    return sigma / (epsilon_0 * epsilon_r)


# =============================================================================
# 练习 6.3: 电容器的能量
# Exercise 6.3: Energy Stored in Capacitor
# =============================================================================
# 物理背景 Physical Background:
# 电容器储存的能量以电场能的形式存在于两极板之间。
# 三个等价的能量公式可根据已知量选用。
# 能量与电压的平方成正比，这是为什么高压电容器危险的原因。

def capacitor_energy_CV(C, V):
    """
    电容器储存的能量（用C和V表示）
    Energy stored in capacitor (in terms of C and V)

    参数 Parameters:
        C: 电容 [F]
        V: 电压 [V]

    返回 Returns:
        能量 U [J]

    公式 Formula:
        U = (1/2)CV²

    应用: 已知电容和电压时使用
    注意: 能量与V²成正比，高压电容器能量很大！
    """
    # TODO: 计算能量 (Calculate energy)
    U = 0.5 * C * V**2
    return U


def capacitor_energy_QV(Q, V):
    """
    电容器储存的能量（用Q和V表示）
    Energy stored in capacitor (in terms of Q and V)

    公式 Formula:
        U = (1/2)QV [J]

    推导: U = (1/2)CV² = (1/2)(Q/V)V² = (1/2)QV
    """
    return 0.5 * Q * V


def capacitor_energy_QC(Q, C):
    """
    电容器储存的能量（用Q和C表示）
    Energy stored in capacitor (in terms of Q and C)

    公式 Formula:
        U = Q²/(2C) [J]

    推导: U = (1/2)CV² = (1/2)C(Q/C)² = Q²/(2C)
    应用: 分析恒Q过程（如断开电源后改变电容）
    """
    return Q**2 / (2 * C)


def energy_density_electric_field(E, epsilon_r=1.0):
    """
    电场的能量密度
    Energy density of electric field

    参数 Parameters:
        E: 电场强度 [V/m]
        epsilon_r: 相对介电常数

    返回 Returns:
        能量密度 u [J/m³]

    公式 Formula:
        u = (1/2)ε₀εᵣE²

    物理意义: 电场本身储存能量，单位体积内的能量
    """
    # TODO: 计算能量密度 (Calculate energy density)
    u = 0.5 * epsilon_0 * epsilon_r * E**2
    return u


def total_energy_from_field(E, volume, epsilon_r=1.0):
    """
    从电场能量密度计算总能量
    Total energy from field energy density

    公式 Formula:
        U = u × V = (1/2)ε₀εᵣE² × V [J]

    说明: 对于匀强电场，直接乘以体积
    对于非匀强电场，需要对u积分
    """
    u = energy_density_electric_field(E, epsilon_r)
    return u * volume


# =============================================================================
# 练习 6.4: 电容器的串并联
# Exercise 6.4: Series and Parallel Capacitors
# =============================================================================
# 物理背景 Physical Background:
# 串联: 各电容器电荷相同（电荷守恒），电压分配
#       等效电容小于任一电容（总间距增大）
# 并联: 各电容器电压相同，电荷分配
#       等效电容为各电容之和（总面积增大）
# 注意: 电容的串并联公式与电阻相反！

def capacitors_in_series(C_list):
    """
    电容器串联
    Capacitors in series

    参数 Parameters:
        C_list: 电容值列表 [F]

    返回 Returns:
        等效电容 C_eq [F]

    公式 Formula:
        1/C_eq = 1/C₁ + 1/C₂ + ...

    特点: C_eq < min(Cᵢ)，串联后电容减小
    """
    # TODO: 计算等效电容 (Calculate equivalent capacitance)
    C_inv_sum = sum(1/C for C in C_list)
    C_eq = 1 / C_inv_sum
    return C_eq


def capacitors_in_parallel(C_list):
    """
    电容器并联
    Capacitors in parallel

    参数 Parameters:
        C_list: 电容值列表 [F]

    返回 Returns:
        等效电容 C_eq [F]

    公式 Formula:
        C_eq = C₁ + C₂ + ...

    特点: C_eq > max(Cᵢ)，并联后电容增大
    """
    # TODO: 计算等效电容 (Calculate equivalent capacitance)
    C_eq = sum(C_list)
    return C_eq


def voltage_divider_capacitors(V_total, C1, C2):
    """
    串联电容器的电压分配
    Voltage division in series capacitors

    参数 Parameters:
        V_total: 总电压 [V]
        C1, C2: 两个电容 [F]

    返回 Returns:
        V1, V2: 各电容上的电压 [V]

    原理 Principle:
        Q相同（电荷守恒）
        V = Q/C，电容小的分压多
        V₁/V₂ = C₂/C₁（反比关系）
    """
    C_eq = capacitors_in_series([C1, C2])
    Q = C_eq * V_total  # 串联电荷相同
    # TODO: 计算各电容器上的电压 (Calculate voltage on each capacitor)
    V1 = Q / C1
    V2 = Q / C2
    return V1, V2


def charge_distribution_parallel(V, C_list):
    """
    并联电容器的电荷分配
    Charge distribution in parallel capacitors

    参数 Parameters:
        V: 公共电压 [V]
        C_list: 电容值列表 [F]

    返回 Returns:
        Q_list: 各电容上的电荷 [C]

    原理 Principle:
        V相同（并联）
        Q = CV，电容大的存储电荷多
    """
    # TODO: 计算各电容器上的电荷 (Calculate charge on each capacitor)
    Q_list = [C * V for C in C_list]
    return Q_list


# =============================================================================
# 练习 6.5: 介电质
# Exercise 6.5: Dielectrics
# =============================================================================
# 物理背景 Physical Background:
# 介电质是绝缘体材料，插入电容器后会发生极化。
# 极化产生的束缚电荷部分抵消自由电荷的电场。
# 结果：相同电压下可储存更多电荷，电容增大。
# 常见介电质: 空气(εᵣ≈1), 纸(εᵣ≈3), 玻璃(εᵣ≈5), 陶瓷(εᵣ≈1000)

def capacitance_with_dielectric(C0, epsilon_r):
    """
    插入介电质后的电容变化
    Capacitance with dielectric

    参数 Parameters:
        C0: 真空（空气）中的电容 [F]
        epsilon_r: 相对介电常数（无量纲）

    返回 Returns:
        新电容 C [F]

    公式 Formula:
        C = εᵣC₀

    说明: 电容增大为原来的εᵣ倍
    """
    return epsilon_r * C0


def dielectric_constant(C, C0):
    """
    从电容变化求介电常数
    Determine dielectric constant from capacitance change

    公式 Formula:
        εᵣ = C/C₀

    应用: 实验测量介电常数
    """
    return C / C0


def field_in_dielectric(E0, epsilon_r):
    """
    介电质中的电场（电荷恒定时）
    Electric field in dielectric (constant charge)

    公式 Formula:
        E = E₀/εᵣ

    说明: 极化电荷部分抵消自由电荷的场
    如果电压恒定，电场不变，电荷增加
    """
    return E0 / epsilon_r


def polarization_field(E, epsilon_r):
    """
    极化强度
    Polarization

    参数 Parameters:
        E: 介电质中的电场 [V/m]
        epsilon_r: 相对介电常数

    返回 Returns:
        极化强度 P [C/m²]

    公式 Formula:
        P = ε₀(εᵣ - 1)E = ε₀χₑE

    说明: χₑ = εᵣ - 1 称为电极化率
    P表示单位体积内的电偶极矩
    """
    # TODO: 计算极化强度 (Calculate polarization)
    P = epsilon_0 * (epsilon_r - 1) * E
    return P


def dielectric_energy_density(E, epsilon_r):
    """
    介电质中的能量密度
    Energy density in dielectric

    公式 Formula:
        u = (1/2)ε₀εᵣE² = (1/2)DE [J/m³]

    其中 D = ε₀εᵣE 是电位移
    """
    return energy_density_electric_field(E, epsilon_r)


# =============================================================================
# 练习 6.6: 球形电容器
# Exercise 6.6: Spherical Capacitor
# =============================================================================
# 物理背景 Physical Background:
# 球形电容器由同心的内外导体球壳组成。
# 利用高斯定律求电场，再积分求电势差，最后算电容。
# 当外球半径趋于无穷大时，得到孤立球导体的电容。

def spherical_capacitor(a, b, epsilon_r=1.0):
    """
    球形电容器的电容
    Spherical capacitor capacitance

    参数 Parameters:
        a: 内球半径 [m]
        b: 外球半径 [m]
        epsilon_r: 相对介电常数

    返回 Returns:
        电容 C [F]

    公式 Formula:
        C = 4πε₀εᵣab/(b-a)

    推导:
        E(r) = Q/(4πε₀εᵣr²)
        V = ∫E·dr = Q(b-a)/(4πε₀εᵣab)
        C = Q/V
    """
    # TODO: 计算电容 (Calculate capacitance)
    C = 4 * np.pi * epsilon_0 * epsilon_r * a * b / (b - a)
    return C


def isolated_sphere_capacitance(a, epsilon_r=1.0):
    """
    孤立球导体的电容
    Isolated sphere capacitance

    参数 Parameters:
        a: 球半径 [m]
        epsilon_r: 相对介电常数

    返回 Returns:
        电容 C [F]

    公式 Formula:
        C = 4πε₀εᵣa (当 b → ∞)

    例如: 地球半径约6400km，电容约710μF
    """
    return 4 * np.pi * epsilon_0 * epsilon_r * a


def electric_field_spherical(Q, r, a, b, epsilon_r=1.0):
    """
    球形电容器中的电场（a < r < b）
    Electric field in spherical capacitor

    参数 Parameters:
        Q: 内球电荷 [C]
        r: 场点到球心距离 [m]
        a, b: 内外球半径 [m]
        epsilon_r: 相对介电常数

    返回 Returns:
        电场强度 E [V/m]

    公式 Formula:
        E = Q/(4πε₀εᵣr²)，a < r < b
        E = 0，r < a 或 r > b

    特点: 场强与 1/r² 成反比
    """
    if r < a or r > b:
        return 0  # 导体内部和外部电场为零
    # TODO: 计算电场 (Calculate electric field)
    E = Q / (4 * np.pi * epsilon_0 * epsilon_r * r**2)
    return E


# =============================================================================
# 练习 6.7: 圆柱形电容器
# Exercise 6.7: Cylindrical Capacitor
# =============================================================================
# 物理背景 Physical Background:
# 圆柱形（同轴）电容器由内外同轴圆柱导体组成。
# 同轴电缆就是典型的圆柱形电容器结构。
# 利用高斯定律：选取与轴同轴的圆柱面作高斯面。

def cylindrical_capacitor(a, b, L, epsilon_r=1.0):
    """
    圆柱形电容器的电容
    Cylindrical capacitor capacitance

    参数 Parameters:
        a: 内圆柱半径 [m]
        b: 外圆柱半径 [m]
        L: 圆柱长度 [m]
        epsilon_r: 相对介电常数

    返回 Returns:
        电容 C [F]

    公式 Formula:
        C = 2πε₀εᵣL/ln(b/a)

    推导:
        E(r) = λ/(2πε₀εᵣr)
        V = ∫E·dr = λ·ln(b/a)/(2πε₀εᵣ)
        C = Q/V = 2πε₀εᵣL/ln(b/a)
    """
    # TODO: 计算电容 (Calculate capacitance)
    C = 2 * np.pi * epsilon_0 * epsilon_r * L / np.log(b / a)
    return C


def electric_field_cylindrical(Q, r, a, b, L, epsilon_r=1.0):
    """
    圆柱形电容器中的电场（a < r < b）
    Electric field in cylindrical capacitor

    参数 Parameters:
        Q: 内圆柱总电荷 [C]
        r: 场点到轴线距离 [m]
        a, b: 内外圆柱半径 [m]
        L: 圆柱长度 [m]
        epsilon_r: 相对介电常数

    返回 Returns:
        电场强度 E [V/m]

    公式 Formula:
        E = Q/(2πε₀εᵣrL) = λ/(2πε₀εᵣr)
        其中 λ = Q/L 是线电荷密度

    特点: 场强与 1/r 成反比（区别于球形的1/r²）
    """
    if r < a or r > b:
        return 0  # 导体内部和外部电场为零
    # 线电荷密度 Line charge density
    lambda_l = Q / L
    # TODO: 计算电场 (Calculate electric field)
    E = lambda_l / (2 * np.pi * epsilon_0 * epsilon_r * r)
    return E


def coaxial_cable_capacitance_per_meter(a, b, epsilon_r=1.0):
    """
    同轴电缆的单位长度电容
    Coaxial cable capacitance per unit length

    参数 Parameters:
        a: 内导体半径 [m]
        b: 外导体内半径 [m]
        epsilon_r: 绝缘层相对介电常数

    返回 Returns:
        单位长度电容 C/L [F/m]

    公式 Formula:
        C/L = 2πε₀εᵣ/ln(b/a)

    应用: 同轴电缆的特性阻抗设计
    典型值: 约 50-100 pF/m
    """
    return 2 * np.pi * epsilon_0 * epsilon_r / np.log(b / a)


# =============================================================================
# 可视化
# =============================================================================
def plot_capacitors():
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    # 1. 平行板电容器电场
    ax1 = axes[0, 0]
    d_values = np.linspace(1e-3, 10e-3, 100)
    A = 0.01  # 0.01 m² = 100 cm²
    C_values = [parallel_plate_capacitance(A, d) * 1e12 for d in d_values]  # pF

    ax1.plot(d_values * 1e3, C_values, 'b-', linewidth=2)
    ax1.set_xlabel('Plate separation d (mm)')
    ax1.set_ylabel('Capacitance (pF)')
    ax1.set_title('平行板电容器 C vs d')
    ax1.grid(True, alpha=0.3)

    # 2. 介电常数的影响
    ax2 = axes[0, 1]
    epsilon_r_values = np.linspace(1, 10, 100)
    C0 = parallel_plate_capacitance(0.01, 1e-3)  # 基准电容
    C_dielectric = [capacitance_with_dielectric(C0, er) * 1e12 for er in epsilon_r_values]

    ax2.plot(epsilon_r_values, C_dielectric, 'r-', linewidth=2)
    ax2.set_xlabel('Relative permittivity (εᵣ)')
    ax2.set_ylabel('Capacitance (pF)')
    ax2.set_title('介电质对电容的影响')
    ax2.grid(True, alpha=0.3)

    # 3. 电容器能量
    ax3 = axes[0, 2]
    V_values = np.linspace(0, 100, 100)
    C_fixed = 10e-6  # 10 μF
    U_values = [capacitor_energy_CV(C_fixed, V) * 1e3 for V in V_values]  # mJ

    ax3.plot(V_values, U_values, 'g-', linewidth=2)
    ax3.set_xlabel('Voltage (V)')
    ax3.set_ylabel('Energy (mJ)')
    ax3.set_title('电容器储能 (C=10μF)')
    ax3.grid(True, alpha=0.3)

    # 4. 串并联比较
    ax4 = axes[1, 0]
    C1, C2 = 10e-6, 20e-6  # 10 μF, 20 μF
    C_series = capacitors_in_series([C1, C2])
    C_parallel = capacitors_in_parallel([C1, C2])

    labels = ['C₁', 'C₂', 'Series', 'Parallel']
    values = [C1*1e6, C2*1e6, C_series*1e6, C_parallel*1e6]
    colors = ['blue', 'blue', 'red', 'green']
    ax4.bar(labels, values, color=colors, alpha=0.7)
    ax4.set_ylabel('Capacitance (μF)')
    ax4.set_title('串并联电容比较')
    ax4.grid(True, alpha=0.3, axis='y')

    # 5. 球形电容器电场分布
    ax5 = axes[1, 1]
    a, b = 0.05, 0.1  # 内外半径
    Q = 1e-9  # 1 nC
    r_values = np.linspace(a, b, 100)
    E_values = [electric_field_spherical(Q, r, a, b) for r in r_values]

    ax5.plot(r_values * 100, E_values, 'b-', linewidth=2)
    ax5.set_xlabel('Radius r (cm)')
    ax5.set_ylabel('Electric field E (V/m)')
    ax5.set_title('球形电容器电场分布')
    ax5.grid(True, alpha=0.3)

    # 6. 圆柱形电容器
    ax6 = axes[1, 2]
    a, b, L = 0.001, 0.005, 1.0  # 1mm, 5mm, 1m
    r_cyl = np.linspace(a, b, 100)
    E_cyl = [electric_field_cylindrical(Q, r, a, b, L) for r in r_cyl]

    ax6.plot(r_cyl * 1000, E_cyl, 'r-', linewidth=2)
    ax6.set_xlabel('Radius r (mm)')
    ax6.set_ylabel('Electric field E (V/m)')
    ax6.set_title('圆柱形电容器电场分布')
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('capacitors.png', dpi=150)
    print("图像已保存为 capacitors.png")
    plt.show()


def verify():
    """
    验证所有电容器练习
    Verify all capacitor exercises

    验证内容 Verification:
        6.1 电容的基本定义 C=Q/V
        6.2 平行板电容器 C=ε₀A/d
        6.3 电容器储能 U=(1/2)CV²
        6.4 电容器串并联
        6.5 介电质效应
        6.6 球形电容器
        6.7 圆柱形电容器
    """
    all_passed = True

    # 验证 6.1: 电容基本定义
    # Check 6.1: Basic capacitance definition
    Q, V = 1e-6, 100  # 1 μC, 100 V
    C = capacitance_from_charge(Q, V)
    if not np.isclose(C, 1e-8, rtol=0.01):
        print("❌ 6.1 电容定义错误")
        print("   提示: C = Q/V")
        all_passed = False
    else:
        print(f"✓ 6.1 电容定义正确 (C = {C*1e9:.1f} nF)")

    # 验证 6.2: 平行板电容器
    # Check 6.2: Parallel plate capacitor
    A, d = 0.01, 1e-3  # 100 cm², 1 mm
    C_plate = parallel_plate_capacitance(A, d)
    expected_C = epsilon_0 * A / d
    if not np.isclose(C_plate, expected_C, rtol=0.01):
        print("❌ 6.2 平行板电容错误")
        print("   提示: C = ε₀A/d")
        all_passed = False
    else:
        print(f"✓ 6.2 平行板电容正确 (C = {C_plate*1e12:.1f} pF)")

    # 验证 6.3: 电容器能量
    # Check 6.3: Capacitor energy
    C_test, V_test = 10e-6, 50  # 10 μF, 50 V
    U = capacitor_energy_CV(C_test, V_test)
    expected_U = 0.5 * C_test * V_test**2
    if not np.isclose(U, expected_U, rtol=0.01):
        print("❌ 6.3 电容器能量错误")
        print("   提示: U = (1/2)CV²")
        all_passed = False
    else:
        print(f"✓ 6.3 电容器能量正确 (U = {U*1e3:.2f} mJ)")

    # 验证 6.4: 串并联
    # Check 6.4: Series and parallel
    C1, C2 = 10e-6, 20e-6
    C_series = capacitors_in_series([C1, C2])
    C_parallel = capacitors_in_parallel([C1, C2])

    expected_series = (C1 * C2) / (C1 + C2)
    expected_parallel = C1 + C2

    if not (np.isclose(C_series, expected_series, rtol=0.01) and
            np.isclose(C_parallel, expected_parallel, rtol=0.01)):
        print("❌ 6.4 串并联计算错误")
        print("   提示: 串联 1/C=Σ(1/Cᵢ), 并联 C=ΣCᵢ")
        all_passed = False
    else:
        print(f"✓ 6.4 串并联正确 (Cs={C_series*1e6:.2f}μF, Cp={C_parallel*1e6:.0f}μF)")

    # 验证 6.5: 介电质
    # Check 6.5: Dielectric
    C0 = 100e-12  # 100 pF
    epsilon_r = 4.0
    C_dielectric = capacitance_with_dielectric(C0, epsilon_r)
    if not np.isclose(C_dielectric, 4 * C0, rtol=0.01):
        print("❌ 6.5 介电质影响错误")
        print("   提示: C = εᵣC₀")
        all_passed = False
    else:
        print(f"✓ 6.5 介电质影响正确 (C = {C_dielectric*1e12:.0f} pF)")

    # 验证 6.6: 球形电容器
    # Check 6.6: Spherical capacitor
    a, b = 0.05, 0.1  # 5 cm, 10 cm
    C_sphere = spherical_capacitor(a, b)
    expected_sphere = 4 * np.pi * epsilon_0 * a * b / (b - a)
    if not np.isclose(C_sphere, expected_sphere, rtol=0.01):
        print("❌ 6.6 球形电容器错误")
        print("   提示: C = 4πε₀ab/(b-a)")
        all_passed = False
    else:
        print(f"✓ 6.6 球形电容器正确 (C = {C_sphere*1e12:.2f} pF)")

    # 验证 6.7: 圆柱形电容器
    # Check 6.7: Cylindrical capacitor
    a, b, L = 0.001, 0.005, 1.0
    C_cyl = cylindrical_capacitor(a, b, L)
    expected_cyl = 2 * np.pi * epsilon_0 * L / np.log(b/a)
    if not np.isclose(C_cyl, expected_cyl, rtol=0.01):
        print("❌ 6.7 圆柱形电容器错误")
        print("   提示: C = 2πε₀L/ln(b/a)")
        all_passed = False
    else:
        print(f"✓ 6.7 圆柱形电容器正确 (C = {C_cyl*1e12:.2f} pF)")

    if all_passed:
        print("\n🎉 所有测试通过！")
        try:
            plot_capacitors()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("电容器 Capacitors")
    print("=" * 50)
    verify()
