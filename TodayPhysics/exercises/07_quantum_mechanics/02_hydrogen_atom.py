"""
氢原子与原子物理 Hydrogen Atom and Atomic Physics
难度 Difficulty: ★★★★

物理背景 Physical Background:
--------------------------
氢原子是量子力学中唯一可以精确解析求解的原子体系。
1913年玻尔提出量子化轨道模型，成功解释了氢原子光谱。
1926年薛定谔用波动方程得到了氢原子的完整解析解。

氢原子的核心结果：
1. 能级公式: E_n = -13.6/n² eV（只依赖主量子数n）
2. 波函数由三个量子数描述: n(主), l(角动量), m(磁)
3. 玻尔半径 a_0 = 0.529 A 是原子尺度的基本单位

学习目标 Learning Objectives:
--------------------------
1. 掌握氢原子能级公式和里德伯公式
2. 理解玻尔模型的基本假设和局限性
3. 熟悉氢原子波函数的径向部分和角度部分
4. 理解量子数(n, l, m)的物理意义和取值规则
5. 计算径向概率密度，理解最概然半径与平均半径的区别
6. 了解原子光谱系列（Lyman、Balmer、Paschen等）

关键公式 Key Formulas:
--------------------
- 能级: E_n = -13.6 Z²/n² eV = -R_y Z²/n²（R_y = 13.6 eV 为里德伯能量）
- 里德伯公式: 1/lambda = R_inf Z² (1/n_1² - 1/n_2²)
- 玻尔半径: a_0 = 4pi epsilon_0 hbar²/(m_e e²) = 0.529 A
- 轨道角动量: L = sqrt(l(l+1)) hbar
- 磁量子数范围: m = -l, -l+1, ..., l-1, l（共 2l+1 个取值）
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import factorial, laguerre, sph_harm
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import hbar, m_e, e, a_0, R_inf, eV

# I AM NOT DONE

# =============================================================================
# 练习 2.1: 氢原子能级
# Exercise 2.1: Hydrogen Energy Levels
# -----------------------------------------------------------------------------
# 物理背景：氢原子能级由主量子数 n 完全确定
# 这是库仑势问题的特殊性质（称为"意外简并"或库仑简并）
#
# 能级公式推导：
# 从薛定谔方程求解得 E_n = -m_e e⁴/(8ε₀²h²n²) = -13.6/n² eV
# 负号表示束缚态，n→∞时能量趋于0（电离态）
#
# 物理意义：
# - n=1: 基态，E_1 = -13.6 eV（氢原子电离能）
# - n=2: 第一激发态，E_2 = -3.4 eV
# - n→∞: 连续谱，E = 0（电离阈值）
# =============================================================================
def hydrogen_energy(n, Z=1):
    """
    计算类氢原子能级 Calculate hydrogen-like atom energy level

    公式: E_n = -13.6 × Z²/n² eV

    参数 Parameters:
        n: 主量子数 (n = 1, 2, 3, ...)
        Z: 核电荷数（氢原子 Z=1，He⁺ Z=2，Li²⁺ Z=3）

    返回 Returns:
        E_n: 能级能量 (J)

    注意：返回值为焦耳，负值表示束缚态
    """
    # TODO: 根据公式计算能级，注意单位转换
    E_n = -13.6 * Z**2 / n**2 * eV  # eV转换为焦耳
    return E_n


def energy_difference(n1, n2, Z=1):
    """
    计算两能级之间的能量差 Calculate energy difference between two levels

    参数 Parameters:
        n1, n2: 两个能级的主量子数
        Z: 核电荷数

    返回 Returns:
        Delta E: 能量差的绝对值 (J)

    应用：光子吸收/发射时的能量等于能级差
    hnu = |E_n2 - E_n1|
    """
    E1 = hydrogen_energy(n1, Z)
    E2 = hydrogen_energy(n2, Z)
    return abs(E2 - E1)


# =============================================================================
# 练习 2.2: 光谱线波长
# Exercise 2.2: Spectral Line Wavelength
# -----------------------------------------------------------------------------
# 物理背景：里德伯公式是氢原子光谱的经验公式，后被玻尔理论解释
#
# 光谱系列（按下能级分类）：
# - Lyman系 (n_1=1): 紫外区，121.5 nm（Ly-alpha）起
# - Balmer系 (n_1=2): 可见光区，656.3 nm（H-alpha，红色）起
# - Paschen系 (n_1=3): 近红外区，1875 nm起
# - Brackett系 (n_1=4): 红外区
# - Pfund系 (n_1=5): 远红外区
#
# 里德伯常数 R_inf = m_e e⁴/(8ε₀²h³c) ≈ 1.097×10⁷ m⁻¹
# =============================================================================
def rydberg_wavelength(n1, n2, Z=1):
    """
    用里德伯公式计算光谱线波长 Calculate spectral line wavelength

    公式: 1/lambda = R_inf × Z² × (1/n_1² - 1/n_2²)

    参数 Parameters:
        n1: 下能级主量子数（电子跃迁的终态）
        n2: 上能级主量子数（电子跃迁的初态），n2 > n1
        Z: 核电荷数

    返回 Returns:
        lambda: 光谱线波长 (m)

    注意：n2 > n1 对应发射光谱（电子从高能级跃迁到低能级）
    """
    # TODO: 根据里德伯公式计算波长
    # 注意：要求 n2 > n1，否则波长为负
    inv_lambda = R_inf * Z**2 * (1/n1**2 - 1/n2**2)
    return 1 / inv_lambda


def spectral_series_name(n_lower):
    """
    返回光谱系列名称 Return spectral series name

    各系列发现者：
    - Lyman (1906): 紫外系列
    - Balmer (1885): 可见光系列（最早发现）
    - Paschen (1908): 红外系列
    - Brackett (1922): 远红外系列
    - Pfund (1924): 更远红外系列
    """
    names = {1: "Lyman", 2: "Balmer", 3: "Paschen", 4: "Brackett", 5: "Pfund"}
    return names.get(n_lower, f"n={n_lower}")


# =============================================================================
# 练习 2.3: 玻尔模型
# Exercise 2.3: Bohr Model
# -----------------------------------------------------------------------------
# 物理背景：玻尔模型（1913年）是量子力学的先驱
#
# 玻尔的三个假设：
# 1. 定态假设：电子在特定轨道上运动，不辐射能量
# 2. 跃迁假设：电子在不同轨道间跃迁时吸收/发射光子
# 3. 量子化条件：角动量 L = n*hbar（n = 1,2,3,...）
#
# 从这些假设可以推导出：
# - 轨道半径: r_n = n² a_0 / Z
# - 轨道速度: v_n = alpha × c × Z/n（alpha为精细结构常数）
# - 能量: E_n = -13.6 Z²/n² eV
#
# 局限性：玻尔模型无法解释多电子原子、精细结构等
# =============================================================================
def bohr_radius(n, Z=1):
    """
    计算玻尔轨道半径 Calculate Bohr orbit radius

    公式: r_n = n² × a_0 / Z

    参数 Parameters:
        n: 主量子数 (n = 1, 2, 3, ...)
        Z: 核电荷数

    返回 Returns:
        r_n: 轨道半径 (m)

    物理意义：
    - n=1, Z=1: r_1 = a_0 = 0.529 A（玻尔半径，原子尺度的基本单位）
    - 轨道半径与 n² 成正比，高激发态原子尺寸很大
    """
    # TODO: 根据公式计算轨道半径
    r_n = n**2 * a_0 / Z
    return r_n


def bohr_velocity(n, Z=1):
    """
    计算玻尔轨道速度 Calculate Bohr orbit velocity

    公式: v_n = alpha × c × Z/n

    其中 alpha = e²/(4pi epsilon_0 hbar c) ≈ 1/137 是精细结构常数

    参数 Parameters:
        n: 主量子数
        Z: 核电荷数

    返回 Returns:
        v_n: 轨道速度 (m/s)

    物理意义：
    - n=1, Z=1: v_1 ≈ c/137 ≈ 2.2×10⁶ m/s（电子速度约为光速的0.7%）
    - 对于重元素（大Z），内层电子速度接近光速，需要相对论修正
    """
    alpha = 1 / 137  # 精细结构常数
    from utils.constants import c
    return alpha * c * Z / n


def bohr_angular_momentum(n):
    """
    计算玻尔轨道角动量 Calculate Bohr orbital angular momentum

    公式: L = n × hbar

    参数 Parameters:
        n: 主量子数 (n = 1, 2, 3, ...)

    返回 Returns:
        L: 角动量 (J·s = kg·m²/s)

    注意：这是玻尔模型的量子化条件
    真正的量子力学给出 L = sqrt(l(l+1))hbar，其中 l = 0,1,...,n-1
    玻尔模型的 L = nhbar 只是近似
    """
    return n * hbar


# =============================================================================
# 练习 2.4: 径向波函数
# Exercise 2.4: Radial Wave Functions
# -----------------------------------------------------------------------------
# 物理背景：氢原子波函数可分离为径向部分和角度部分
# psi_{nlm}(r,theta,phi) = R_{nl}(r) × Y_l^m(theta, phi)
#
# 径向波函数的一般形式：
# R_{nl}(r) = N × rho^l × L_{n-l-1}^{2l+1}(rho) × exp(-rho/2)
# 其中 rho = 2Zr/(na_0)，L是缔合拉盖尔多项式
#
# 径向波函数特点：
# - R_{nl} 有 (n-l-1) 个节点（不含原点和无穷远）
# - l=0 (s轨道): R(0) ≠ 0
# - l>0 (p,d...轨道): R(0) = 0
# =============================================================================
def radial_wave_function_1s(r, Z=1):
    """
    1s轨道(n=1, l=0)径向波函数 Radial wavefunction for 1s orbital

    公式: R_10(r) = 2(Z/a_0)^(3/2) × exp(-Zr/a_0)

    参数 Parameters:
        r: 径向距离数组 (m)
        Z: 核电荷数

    返回 Returns:
        R: 径向波函数值

    特点：
    - 1s轨道无节点（除无穷远外）
    - R(0) ≠ 0，电子有限概率在原子核处
    - 指数衰减，特征衰减长度为 a_0/Z
    """
    # TODO: 计算1s径向波函数
    coef = 2 * (Z / a_0)**1.5  # 归一化系数
    R = coef * np.exp(-Z * r / a_0)
    return R


def radial_wave_function_2s(r, Z=1):
    """
    2s轨道(n=2, l=0)径向波函数 Radial wavefunction for 2s orbital

    公式: R_20(r) = (Z/(2a_0))^(3/2) × (2-rho) × exp(-rho/2) / sqrt(2)
    其中 rho = 2Zr/a_0

    特点：
    - 2s轨道有1个径向节点（在 r = 2a_0/Z 处）
    - R(0) ≠ 0（s轨道的特征）
    - 因子 (2-rho) 产生节点
    """
    rho = 2 * Z * r / a_0  # 无量纲径向坐标
    coef = (Z / (2*a_0))**1.5
    R = coef * (2 - rho) * np.exp(-rho/2) / np.sqrt(2)
    return R


def radial_wave_function_2p(r, Z=1):
    """
    2p轨道(n=2, l=1)径向波函数 Radial wavefunction for 2p orbital

    公式: R_21(r) = (Z/(2a_0))^(3/2) × rho × exp(-rho/2) / (2sqrt(6))
    其中 rho = 2Zr/a_0

    特点：
    - 2p轨道无径向节点（n-l-1 = 0）
    - R(0) = 0（p轨道的特征，l=1）
    - 因子 rho 使波函数在原点为0
    """
    rho = 2 * Z * r / a_0
    coef = (Z / (2*a_0))**1.5
    R = coef * rho * np.exp(-rho/2) / (2 * np.sqrt(6))
    return R


# =============================================================================
# 练习 2.5: 概率分布
# Exercise 2.5: Probability Distribution
# -----------------------------------------------------------------------------
# 物理背景：电子在空间中的概率分布
#
# 概率密度的两种表示：
# 1. 三维概率密度: |psi|² = |R|² |Y|²
# 2. 径向概率密度: P(r) = r² |R(r)|² × 4pi（对角度积分后）
#
# P(r)dr 表示电子在球壳 [r, r+dr] 内被发现的概率
# 注意因子 r²：体现球壳的体积效应（4pi r² dr）
#
# 最概然半径 vs 平均半径：
# - 最概然半径: dP/dr = 0 的解，即 P(r) 最大的位置
# - 平均半径: <r> = integral r × P(r) dr
# 两者通常不相等！
# =============================================================================
def radial_probability_density(R, r):
    """
    计算径向概率密度 Calculate radial probability density

    公式: P(r) = r² × |R(r)|²

    参数 Parameters:
        R: 径向波函数值
        r: 径向距离 (m)

    返回 Returns:
        P: 径向概率密度

    物理意义：P(r)dr 是电子在 [r, r+dr] 球壳内的概率
    归一化条件: integral_0^inf P(r) dr = 1
    """
    # TODO: 计算径向概率密度
    # 注意 r² 因子来源于球壳体积元
    P = r**2 * np.abs(R)**2
    return P


def most_probable_radius_1s(Z=1):
    """
    计算1s轨道的最概然半径 Calculate most probable radius for 1s

    对于1s轨道: r_mp = a_0/Z

    推导：对 P(r) = r² × |R_1s|² 求导，令 dP/dr = 0
    得到 r_mp = a_0/Z

    物理意义：这是电子最可能被发现的位置
    注意：最概然半径 ≠ 玻尔半径（但对1s恰好相等）
    """
    return a_0 / Z


def expectation_radius_1s(Z=1):
    """
    计算1s轨道的平均半径 Calculate expectation value of radius for 1s

    公式: <r>_1s = 1.5 × a_0/Z

    推导: <r> = integral r × P(r) dr = integral r³ |R_1s|² dr

    注意：平均半径 > 最概然半径
    这是因为波函数有长尾（指数衰减而非截断）
    """
    return 1.5 * a_0 / Z


# =============================================================================
# 练习 2.6: 量子数
# Exercise 2.6: Quantum Numbers
# -----------------------------------------------------------------------------
# 物理背景：氢原子波函数由三个量子数完全确定
#
# 三个量子数：
# 1. 主量子数 n = 1, 2, 3, ... （决定能量和轨道大小）
# 2. 角量子数 l = 0, 1, ..., n-1 （决定轨道形状）
#    命名：l=0(s), l=1(p), l=2(d), l=3(f)
# 3. 磁量子数 m = -l, -l+1, ..., l-1, l （决定空间取向）
#
# 自旋量子数（电子内禀性质）：
# m_s = +1/2 或 -1/2（自旋向上或向下）
#
# 泡利不相容原理：同一原子中不能有两个电子具有完全相同的量子数
# =============================================================================
def orbital_angular_momentum(l):
    """
    计算轨道角动量大小 Calculate orbital angular momentum magnitude

    公式: L = sqrt(l(l+1)) × hbar

    参数 Parameters:
        l: 角量子数 (l = 0, 1, 2, ...)

    返回 Returns:
        L: 角动量大小 (J·s)

    物理意义：
    - l=0: L=0（s轨道无角动量）
    - l=1: L=sqrt(2)hbar（p轨道）
    - l=2: L=sqrt(6)hbar（d轨道）
    """
    return np.sqrt(l * (l + 1)) * hbar


def magnetic_quantum_number_range(l):
    """
    返回磁量子数的所有可能取值 Return all possible magnetic quantum numbers

    规则: m_l = -l, -l+1, ..., -1, 0, 1, ..., l-1, l

    共有 (2l+1) 个取值，对应角动量在z方向的投影 L_z = m_l × hbar

    物理意义：磁量子数决定轨道在外磁场中的取向
    这就是为什么在磁场中能级会分裂（塞曼效应）
    """
    return list(range(-l, l + 1))


def orbital_degeneracy(n):
    """
    计算氢原子能级的简并度 Calculate degeneracy of hydrogen energy level

    公式: g(n) = n²（不考虑自旋）或 2n²（考虑自旋）

    参数 Parameters:
        n: 主量子数

    返回 Returns:
        简并度（不含自旋）

    推导：对于给定n，l可取 0,1,...,n-1
    每个l对应 2l+1 个m值
    总数 = sum_{l=0}^{n-1} (2l+1) = n²
    """
    return n**2


def electron_configuration(Z):
    """
    生成原子的电子排布 Generate electron configuration

    参数 Parameters:
        Z: 原子序数（核电荷数 = 电子数）

    返回 Returns:
        电子排布字符串，如 "1s^2 2s^2 2p^2"（碳原子）

    排布规则（构造原理）：
    1. 能量最低原理：电子优先填充能量低的轨道
    2. 泡利不相容原理：每个轨道最多2个电子（自旋相反）
    3. 洪特规则：同能级轨道先单占再配对

    注意：轨道能量顺序 1s < 2s < 2p < 3s < 3p < 4s < 3d < 4p
    （3d能量高于4s，这是多电子原子的特点）
    """
    # 按能量顺序排列的轨道
    orbitals = ['1s', '2s', '2p', '3s', '3p', '4s', '3d', '4p']
    # 每个轨道的最大电子数
    max_electrons = [2, 2, 6, 2, 6, 2, 10, 6]

    config = []
    remaining = Z  # 剩余待填充电子数
    for orb, max_e in zip(orbitals, max_electrons):
        if remaining <= 0:
            break
        n_e = min(remaining, max_e)
        config.append(f"{orb}^{n_e}")
        remaining -= n_e

    return ' '.join(config)


# =============================================================================
# 可视化
# =============================================================================
def plot_hydrogen():
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. 能级图
    ax1 = axes[0, 0]
    for n in range(1, 6):
        E = hydrogen_energy(n) / eV
        ax1.hlines(E, 0, 1, colors='b', linewidth=2)
        ax1.text(1.1, E, f'n={n}', va='center')

    # 跃迁线（Balmer系）
    for n_up in [3, 4, 5]:
        E_up = hydrogen_energy(n_up) / eV
        E_down = hydrogen_energy(2) / eV
        ax1.annotate('', xy=(0.5, E_down), xytext=(0.5, E_up),
                    arrowprops=dict(arrowstyle='->', color='red', alpha=0.5))

    ax1.set_xlim(-0.5, 2)
    ax1.set_ylim(-15, 0)
    ax1.set_ylabel('Energy (eV)')
    ax1.set_title('氢原子能级图')
    ax1.set_xticks([])
    ax1.grid(True, alpha=0.3, axis='y')

    # 2. 径向波函数
    ax2 = axes[0, 1]
    r = np.linspace(0, 15*a_0, 500)
    R_1s = radial_wave_function_1s(r)
    R_2s = radial_wave_function_2s(r)
    R_2p = radial_wave_function_2p(r)

    ax2.plot(r/a_0, R_1s * a_0**1.5, 'b-', label='1s', linewidth=2)
    ax2.plot(r/a_0, R_2s * a_0**1.5, 'r-', label='2s', linewidth=2)
    ax2.plot(r/a_0, R_2p * a_0**1.5, 'g-', label='2p', linewidth=2)
    ax2.set_xlabel('r/a₀')
    ax2.set_ylabel('R(r) × a₀^(3/2)')
    ax2.set_title('径向波函数')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 径向概率密度
    ax3 = axes[1, 0]
    P_1s = radial_probability_density(R_1s, r)
    P_2s = radial_probability_density(R_2s, r)
    P_2p = radial_probability_density(R_2p, r)

    ax3.plot(r/a_0, P_1s * a_0, 'b-', label='1s', linewidth=2)
    ax3.plot(r/a_0, P_2s * a_0, 'r-', label='2s', linewidth=2)
    ax3.plot(r/a_0, P_2p * a_0, 'g-', label='2p', linewidth=2)
    ax3.axvline(x=1, color='b', linestyle='--', alpha=0.5)  # 1s最概然
    ax3.set_xlabel('r/a₀')
    ax3.set_ylabel('P(r) × a₀')
    ax3.set_title('径向概率密度')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 光谱系列
    ax4 = axes[1, 1]
    series = {
        'Lyman': (1, 'b'),
        'Balmer': (2, 'g'),
        'Paschen': (3, 'r')
    }

    for name, (n_lower, color) in series.items():
        for n_upper in range(n_lower + 1, n_lower + 6):
            wavelength = rydberg_wavelength(n_lower, n_upper)
            ax4.vlines(wavelength*1e9, 0, 1, colors=color, linewidth=2)

    ax4.set_xlabel('Wavelength (nm)')
    ax4.set_title('氢原子光谱系列')
    ax4.set_xlim(0, 2000)
    ax4.legend(['Lyman', 'Balmer', 'Paschen'])
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('hydrogen_atom.png', dpi=150)
    print("图像已保存为 hydrogen_atom.png")
    plt.show()


def verify():
    """验证所有练习的正确性 Verify all exercises"""
    all_passed = True

    # 检查 2.1 - 氢原子能级
    E1 = hydrogen_energy(1)
    if not np.isclose(E1 / eV, -13.6, rtol=0.01):
        print("错误 2.1: 基态能量计算错误")
        print(f"  期望: E_1 = -13.6 eV")
        print(f"  计算: E_1 = {E1/eV:.2f} eV")
        all_passed = False
    else:
        print(f"通过 2.1: 氢原子能级正确 (E_1 = {E1/eV:.2f} eV)")

    # 检查 2.2 - 里德伯公式（Balmer H-alpha: n=3到n=2）
    lambda_Ha = rydberg_wavelength(2, 3)
    if not np.isclose(lambda_Ha * 1e9, 656, rtol=0.01):
        print("错误 2.2: H-alpha波长计算错误")
        print(f"  期望: lambda = 656 nm")
        print(f"  计算: lambda = {lambda_Ha*1e9:.1f} nm")
        all_passed = False
    else:
        print(f"通过 2.2: Balmer H-alpha = {lambda_Ha*1e9:.1f} nm")

    # 检查 2.3 - 玻尔半径
    r1 = bohr_radius(1)
    if not np.isclose(r1, a_0, rtol=0.01):
        print("错误 2.3: 玻尔半径计算错误")
        print(f"  期望: r_1 = a_0 = {a_0*1e10:.3f} A")
        print(f"  计算: r_1 = {r1*1e10:.3f} A")
        all_passed = False
    else:
        print(f"通过 2.3: 玻尔半径正确 (a_0 = {a_0*1e10:.3f} A)")

    # 检查 2.4 - 径向波函数
    r_test = np.array([a_0])
    R_test = radial_wave_function_1s(r_test)
    if len(R_test) != 1 or R_test[0] <= 0:
        print("错误 2.4: 径向波函数计算错误")
        print("  R_1s(a_0) 应为正值")
        all_passed = False
    else:
        print("通过 2.4: 径向波函数计算正确")

    # 检查 2.5 - 最概然半径
    r_mp = most_probable_radius_1s()
    if not np.isclose(r_mp, a_0, rtol=0.01):
        print("错误 2.5: 最概然半径计算错误")
        print(f"  1s轨道的最概然半径应等于 a_0")
        all_passed = False
    else:
        print(f"通过 2.5: 最概然半径正确 (r_mp = a_0)")

    # 检查 2.6 - 轨道角动量
    L_1 = orbital_angular_momentum(1)
    expected_L = np.sqrt(2) * hbar
    if not np.isclose(L_1, expected_L, rtol=0.01):
        print("错误 2.6: 轨道角动量计算错误")
        print(f"  l=1 时 L 应等于 sqrt(2)*hbar")
        all_passed = False
    else:
        print(f"通过 2.6: 角动量正确 (L(l=1) = sqrt(2)*hbar)")
        print(f"   碳原子(Z=6)电子排布: {electron_configuration(6)}")

    if all_passed:
        print("\n所有测试通过！正在生成可视化...")
        try:
            plot_hydrogen()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("氢原子与原子物理 Hydrogen Atom")
    print("=" * 50)
    verify()
