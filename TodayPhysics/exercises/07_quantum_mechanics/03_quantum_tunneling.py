"""
量子隧穿 Quantum Tunneling
难度 Difficulty: ★★★★

物理背景 Physical Background:
--------------------------
量子隧穿是量子力学最惊人的预言之一。经典力学中，粒子遇到比自身能量高的
势垒时会被完全反射。但在量子力学中，由于波函数的连续性，粒子有一定概率
穿透势垒出现在另一侧，这就是量子隧穿效应。

隧穿效应的物理本质：
- 波函数在势垒内部指数衰减：psi ~ exp(-kappa*x)
- 衰减长度 1/kappa = hbar/sqrt(2m(V-E))
- 若势垒不是无限宽，波函数在另一侧仍有有限振幅

重要应用：
1. 扫描隧穿显微镜(STM)：利用隧穿电流测量表面原子结构
2. 隧穿二极管：量子隧穿器件
3. 核物理中的alpha衰变：alpha粒子隧穿出原子核
4. 恒星核聚变：质子隧穿克服库仑势垒

学习目标 Learning Objectives:
--------------------------
1. 理解量子隧穿的物理机制和数学描述
2. 掌握透射系数的计算（WKB近似和精确解）
3. 了解隧穿电流的距离依赖性
4. 认识隧穿效应在STM、核衰变等中的应用

关键公式 Key Formulas:
--------------------
- 衰减常数: kappa = sqrt(2m(V-E))/hbar
- WKB透射系数: T ≈ exp(-2*kappa*L)（薄势垒近似）
- 精确透射系数: T = 1/(1 + V^2*sinh^2(kappa*L)/(4E(V-E)))
- STM电流: I ∝ V*exp(-2*kappa*z)（z为针尖-样品距离）
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import hbar, m_e, eV

# I AM NOT DONE

# =============================================================================
# 练习 3.1: 矩形势垒
# Exercise 3.1: Rectangular Potential Barrier
# -----------------------------------------------------------------------------
# 物理背景：矩形势垒是最简单的隧穿模型
#
#         V(x)
#          ^
#       V₀ |   ╔═══════╗
#          |   ║       ║
#       E  |---║-------║---  (入射粒子能量)
#          |   ║       ║
#          └───╨───────╨────> x
#              0       L
#
# 三个区域的薛定谔方程解：
# 区域I  (x<0):  psi = A*exp(ikx) + B*exp(-ikx)（入射+反射）
# 区域II (0<x<L): psi = C*exp(-kappa*x) + D*exp(kappa*x)（指数衰减）
# 区域III (x>L): psi = F*exp(ikx)（透射）
# =============================================================================
def decay_constant(m, V, E):
    """
    计算势垒内的衰减常数 Calculate decay constant inside barrier

    公式: kappa = sqrt(2m(V-E)) / hbar

    参数 Parameters:
        m: 粒子质量 (kg)
        V: 势垒高度 (J)
        E: 粒子能量 (J)

    返回 Returns:
        kappa: 衰减常数 (m^-1)

    物理意义：
    - kappa 描述波函数在势垒内的衰减速度
    - 衰减长度 1/kappa = hbar/sqrt(2m(V-E))
    - 若 E >= V，粒子能经典地通过势垒，返回0
    """
    if E >= V:
        return 0  # 经典允许区，无指数衰减
    # TODO: 根据公式计算衰减常数
    kappa = np.sqrt(2 * m * (V - E)) / hbar
    return kappa


def transmission_coefficient_approx(m, V, E, L):
    """
    计算透射系数（WKB近似）Calculate transmission coefficient (WKB approximation)

    公式: T ≈ exp(-2*kappa*L)

    参数 Parameters:
        m: 粒子质量 (kg)
        V: 势垒高度 (J)
        E: 粒子能量 (J)
        L: 势垒宽度 (m)

    返回 Returns:
        T: 透射系数（0到1之间的概率）

    WKB近似条件：势垒足够高且宽（kappa*L >> 1）
    此时主要由指数因子决定，忽略前因子和干涉效应
    """
    kappa = decay_constant(m, V, E)
    if kappa == 0:
        return 1.0  # 经典允许区，完全透射
    # TODO: 根据WKB公式计算透射系数
    T = np.exp(-2 * kappa * L)
    return T


# =============================================================================
# 练习 3.2: 精确透射系数
# Exercise 3.2: Exact Transmission Coefficient
# -----------------------------------------------------------------------------
# 物理背景：通过匹配三个区域边界条件可得精确解
#
# 边界条件（psi 和 dpsi/dx 连续）：
# 在 x=0: A+B = C+D, ik(A-B) = -kappa(C-D)
# 在 x=L: 类似的连续性条件
#
# 精确公式考虑了多次反射的干涉效应
# WKB近似忽略了这些干涉，只保留主要的指数衰减因子
# =============================================================================
def transmission_coefficient_exact(m, V, E, L):
    """
    计算矩形势垒的精确透射系数 Calculate exact transmission coefficient

    公式（E < V时）: T = 1 / (1 + V^2*sinh^2(kappa*L)/(4E(V-E)))

    公式（E > V时）: T = 4k^2*k'^2 / (k^2 + k'^2)^2
    其中 k = sqrt(2mE)/hbar, k' = sqrt(2m(E-V))/hbar

    参数 Parameters:
        m: 粒子质量 (kg)
        V: 势垒高度 (J)
        E: 粒子能量 (J)
        L: 势垒宽度 (m)

    返回 Returns:
        T: 精确透射系数

    与WKB近似的比较：
    - 当 kappa*L >> 1 时，sinh(kappa*L) ≈ exp(kappa*L)/2
    - 此时精确公式简化为 T ≈ exp(-2*kappa*L)，与WKB一致
    - 对于薄势垒或能量接近势垒顶的情况，需要用精确公式
    """
    if E >= V:
        # 经典允许区，粒子能量超过势垒高度
        k = np.sqrt(2 * m * E) / hbar
        k_prime = np.sqrt(2 * m * (E - V)) / hbar
        # 此时也有部分反射（波数突变导致阻抗失配）
        return 4 * k**2 * k_prime**2 / ((k**2 + k_prime**2)**2)

    kappa = decay_constant(m, V, E)
    sinh_term = np.sinh(kappa * L)

    # TODO: 根据精确公式计算透射系数
    T = 1 / (1 + V**2 * sinh_term**2 / (4 * E * (V - E)))
    return T


# =============================================================================
# 练习 3.3: 隧穿电流
# Exercise 3.3: Tunneling Current
# -----------------------------------------------------------------------------
# 物理背景：金属-绝缘体-金属隧穿结中的电流
#
# Simmons模型（1963年）描述隧穿电流与势垒参数的关系
# 在低偏压近似下：J ∝ V × exp(-alpha*L*sqrt(phi))
#
# 其中：
# - V: 外加偏压
# - L: 隧穿势垒宽度（通常是绝缘层厚度）
# - phi: 平均势垒高度（与材料功函数相关）
# - alpha ≈ 1.025 A^-1 eV^-1/2 是与电子质量相关的常数
#
# 应用：隧穿结、分子电子学、STM等
# =============================================================================
def tunneling_current_density(V_bias, L, phi, T_temp=300):
    """
    计算简化的隧穿电流密度 Calculate tunneling current density (simplified)

    公式: J ∝ V × exp(-alpha*L*sqrt(phi))

    参数 Parameters:
        V_bias: 外加偏压 (V)
        L: 势垒宽度 (A，埃)
        phi: 势垒高度 (eV)
        T_temp: 温度 (K)，此简化模型中未使用

    返回 Returns:
        J: 电流密度（任意单位）

    物理意义：
    - 电流随势垒宽度L指数下降
    - 电流随势垒高度phi增加而减小
    - 此公式适用于低偏压情况
    """
    alpha = 1.025  # 单位: A^-1 eV^-1/2 （A表示埃）
    # TODO: 根据简化Simmons公式计算电流密度
    J = V_bias * np.exp(-alpha * L * np.sqrt(phi))
    return J


# =============================================================================
# 练习 3.4: Alpha衰变
# Exercise 3.4: Alpha Decay
# -----------------------------------------------------------------------------
# 物理背景：放射性核素的alpha衰变是量子隧穿的经典应用
#
# Gamow理论（1928年）：
# 1. alpha粒子在原子核内以一定动能E_alpha运动
# 2. 需要克服库仑势垒才能逃逸
# 3. 库仑势垒高度远大于alpha动能，经典物理无法解释衰变
# 4. 量子隧穿使得alpha粒子有小概率穿透势垒
#
# 这是量子力学首次成功解释核物理现象
# Gamow因子解释了半衰期从微秒到数十亿年的巨大差异
# =============================================================================
def alpha_decay_half_life(Z, E_alpha, r_nucleus):
    """
    估算alpha衰变半衰期 Estimate alpha decay half-life (Gamow model)

    Gamow因子: G ≈ exp(-2*pi*eta)
    其中 eta = Z_alpha*Z_daughter*e²/(4*pi*epsilon_0*hbar*v)

    参数 Parameters:
        Z: 母核原子序数
        E_alpha: alpha粒子动能 (J)
        r_nucleus: 核半径 (m)，此简化版未直接使用

    返回 Returns:
        相对半衰期指标（-log(G)的值）

    物理意义：
    - 半衰期与Gamow因子呈指数关系
    - 能量越高，半衰期越短
    - 核电荷越大，半衰期越长
    - 这解释了Geiger-Nuttall定律
    """
    from utils.constants import e, epsilon_0

    Z_alpha = 2  # alpha粒子电荷数
    Z_daughter = Z - 2  # 子核电荷数
    m_alpha = 4 * 1.66e-27  # alpha粒子质量（约4个原子质量单位）
    v = np.sqrt(2 * E_alpha / m_alpha)  # alpha粒子速度

    # Sommerfeld参数 eta
    eta = Z_alpha * Z_daughter * e**2 / (4 * np.pi * epsilon_0 * hbar * v)
    # Gamow穿透因子
    G = np.exp(-2 * np.pi * eta)

    # 半衰期正比于 1/G，返回 -log(G) 作为相对指标
    return -np.log(G)


# =============================================================================
# 练习 3.5: 扫描隧穿显微镜
# Exercise 3.5: Scanning Tunneling Microscope (STM)
# -----------------------------------------------------------------------------
# 物理背景：STM是利用量子隧穿效应的纳米尺度成像技术
#
# 工作原理：
# 1. 导电针尖接近样品表面（距离约1nm）
# 2. 加偏压后，电子通过真空隧穿到针尖/样品
# 3. 隧穿电流对距离极其敏感：I ∝ exp(-2*kappa*z)
# 4. 通过扫描和反馈控制可以得到原子级别的表面图像
#
# STM由Binnig和Rohrer发明（1981年），获1986年诺贝尔物理学奖
#
# 典型参数：
# - 功函数 phi ≈ 4-5 eV（金属的典型值）
# - 针尖-样品距离 z ≈ 0.5-1 nm
# - 电流 I ≈ 0.1-10 nA
# =============================================================================
def stm_current(z, V_bias, phi=4.5):
    """
    计算STM隧穿电流 Calculate STM tunneling current

    公式: I ∝ V × exp(-2*kappa*z)
    其中 kappa = sqrt(2m*phi)/hbar

    参数 Parameters:
        z: 针尖-样品距离 (m)
        V_bias: 偏压 (V)
        phi: 有效势垒高度（功函数）(eV)，默认4.5 eV

    返回 Returns:
        I: 隧穿电流（任意单位）

    灵敏度：z每增加0.1nm，电流约减少一个数量级！
    这使得STM具有亚埃级别的垂直分辨率
    """
    # 计算衰减常数
    kappa = np.sqrt(2 * m_e * phi * eV) / hbar
    # TODO: 计算隧穿电流
    I = V_bias * np.exp(-2 * kappa * z)
    return I


def stm_resolution(phi=4.5):
    """
    估算STM的垂直分辨率 Estimate STM vertical resolution

    定义：使电流变化10倍所需的高度变化
    Delta_z = ln(10)/(2*kappa)

    参数 Parameters:
        phi: 有效势垒高度 (eV)

    返回 Returns:
        Delta_z: 垂直分辨率 (m)

    典型值：对于 phi=4.5 eV，Delta_z ≈ 0.1 nm = 1 A
    这意味着STM可以分辨单原子台阶
    """
    kappa = np.sqrt(2 * m_e * phi * eV) / hbar
    # 电流变化10倍对应的高度变化
    delta_z = np.log(10) / (2 * kappa)
    return delta_z


# =============================================================================
# 练习 3.6: 共振隧穿
# Exercise 3.6: Resonant Tunneling
# -----------------------------------------------------------------------------
# 物理背景：双势垒结构中的共振隧穿效应
#
#         V(x)
#          ^
#       V₀ |   ╔═══╗     ╔═══╗
#          |   ║   ║     ║   ║
#          |   ║   ╚═════╝   ║
#          └───╨─────────────╨────> x
#              L     d     L
#
# 共振隧穿原理：
# 1. 两个势垒之间形成量子阱
# 2. 量子阱中存在准束缚态，能量为 E_n
# 3. 当入射粒子能量 E ≈ E_n 时，发生共振
# 4. 共振时透射系数可达1，即完美透射！
#
# 应用：共振隧穿二极管(RTD)、量子级联激光器
# =============================================================================
def double_barrier_transmission(E, V, L, d, m=m_e):
    """
    计算双势垒结构的透射系数 Calculate transmission for double barrier

    参数 Parameters:
        E: 入射粒子能量 (J)
        V: 势垒高度 (J)
        L: 单个势垒宽度 (m)
        d: 两势垒之间的阱宽 (m)
        m: 粒子质量 (kg)

    返回 Returns:
        T: 透射系数

    共振条件：当 E 等于阱中准束缚态能量 E_n 时，T → 1
    非共振时：T ≈ T_single²（两个独立势垒的乘积）

    物理解释：共振时相当于粒子在阱中驻留很长时间，
    多次尝试隧穿最终以接近1的概率穿透
    """
    # 用无限深势阱近似计算阱中准束缚态能级
    E_n = (np.arange(1, 10)**2 * np.pi**2 * hbar**2) / (2 * m * d**2)

    # 判断是否接近共振能量
    for En in E_n:
        if abs(E - En) < 0.01 * eV:  # 共振宽度（简化处理）
            return 1.0  # 共振隧穿，透射系数趋近1

    # 非共振时，透射系数约等于两个势垒透射系数的乘积
    T_single = transmission_coefficient_approx(m, V, E, L)
    return T_single**2


# =============================================================================
# 可视化
# =============================================================================
def plot_tunneling():
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. 波函数穿透势垒
    ax1 = axes[0, 0]
    V0 = 1 * eV
    E = 0.5 * eV
    L = 1e-9

    x1 = np.linspace(-2e-9, 0, 100)
    x2 = np.linspace(0, L, 100)
    x3 = np.linspace(L, 3e-9, 100)

    k = np.sqrt(2 * m_e * E) / hbar
    kappa = decay_constant(m_e, V0, E)
    T = transmission_coefficient_exact(m_e, V0, E, L)

    psi1 = np.exp(1j * k * x1) + np.sqrt(1-T) * np.exp(-1j * k * x1)
    psi2 = np.exp(-kappa * x2)
    psi3 = np.sqrt(T) * np.exp(1j * k * x3)

    ax1.plot(x1*1e9, np.abs(psi1)**2, 'b-', linewidth=2)
    ax1.plot(x2*1e9, np.abs(psi2)**2, 'r-', linewidth=2)
    ax1.plot(x3*1e9, np.abs(psi3)**2, 'g-', linewidth=2)
    ax1.fill_between([0, L*1e9], 0, 1, alpha=0.3, color='gray')
    ax1.set_xlabel('x (nm)')
    ax1.set_ylabel('|ψ|²')
    ax1.set_title('量子隧穿 Quantum Tunneling')
    ax1.grid(True, alpha=0.3)

    # 2. 透射系数vs能量
    ax2 = axes[0, 1]
    E_range = np.linspace(0.01, 1.5, 200) * eV
    T_approx = [transmission_coefficient_approx(m_e, V0, E, L) for E in E_range]
    T_exact = [transmission_coefficient_exact(m_e, V0, E, L) for E in E_range]

    ax2.semilogy(E_range/eV, T_approx, 'b--', label='WKB approx', linewidth=2)
    ax2.semilogy(E_range/eV, T_exact, 'r-', label='Exact', linewidth=2)
    ax2.axvline(x=1, color='k', linestyle='--', alpha=0.5)
    ax2.set_xlabel('E/V₀')
    ax2.set_ylabel('Transmission T')
    ax2.set_title('透射系数')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. STM电流
    ax3 = axes[1, 0]
    z = np.linspace(0.3e-9, 2e-9, 100)
    I = stm_current(z, 0.1)
    ax3.semilogy(z*1e9, I/I[0], 'b-', linewidth=2)
    ax3.set_xlabel('Tip-sample distance (nm)')
    ax3.set_ylabel('I/I₀')
    ax3.set_title('STM隧穿电流')
    ax3.grid(True, alpha=0.3)

    # 4. 透射系数vs势垒宽度
    ax4 = axes[1, 1]
    L_range = np.linspace(0.1, 3, 100) * 1e-9
    for E_ratio in [0.3, 0.5, 0.7, 0.9]:
        E = E_ratio * V0
        T_L = [transmission_coefficient_approx(m_e, V0, E, L) for L in L_range]
        ax4.semilogy(L_range*1e9, T_L, label=f'E/V₀ = {E_ratio}', linewidth=2)

    ax4.set_xlabel('Barrier width (nm)')
    ax4.set_ylabel('Transmission T')
    ax4.set_title('透射系数vs势垒宽度')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('quantum_tunneling.png', dpi=150)
    print("图像已保存为 quantum_tunneling.png")
    plt.show()


def verify():
    """验证所有练习的正确性 Verify all exercises"""
    all_passed = True

    # 测试参数
    V0 = 1 * eV    # 势垒高度 1 eV
    E = 0.5 * eV   # 粒子能量 0.5 eV
    L = 1e-9       # 势垒宽度 1 nm

    # 检查 3.1 - 衰减常数
    kappa = decay_constant(m_e, V0, E)
    expected_kappa = np.sqrt(2 * m_e * (V0 - E)) / hbar
    if not np.isclose(kappa, expected_kappa, rtol=0.01):
        print("错误 3.1: 衰减常数计算错误")
        print(f"  期望 kappa = {expected_kappa*1e-9:.2f} nm^-1")
        print(f"  计算 kappa = {kappa*1e-9:.2f} nm^-1")
        all_passed = False
    else:
        print(f"通过 3.1: 衰减常数正确 (kappa = {kappa*1e-9:.2f} nm^-1)")

    # 检查 3.2 - 透射系数
    T = transmission_coefficient_exact(m_e, V0, E, L)
    if T <= 0 or T >= 1:
        print("错误 3.2: 透射系数应在 (0, 1) 范围内")
        print(f"  计算得到 T = {T}")
        all_passed = False
    else:
        print(f"通过 3.2: 透射系数正确 (T = {T:.4f})")

    # 检查 3.3 - 隧穿电流
    J = tunneling_current_density(1.0, 10, 4.5)
    if J <= 0:
        print("错误 3.3: 隧穿电流应为正值")
        all_passed = False
    else:
        print("通过 3.3: 隧穿电流计算正确")

    # 检查 3.5 - STM分辨率
    resolution = stm_resolution()
    if resolution <= 0 or resolution > 1e-9:
        print("错误 3.5: STM垂直分辨率计算错误")
        print(f"  分辨率应在埃量级，计算得到 {resolution*1e10:.2f} A")
        all_passed = False
    else:
        print(f"通过 3.5: STM正确 (垂直分辨率约 {resolution*1e10:.2f} A)")

    if all_passed:
        print("\n所有测试通过！正在生成可视化...")
        try:
            plot_tunneling()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("量子隧穿 Quantum Tunneling")
    print("=" * 50)
    verify()
