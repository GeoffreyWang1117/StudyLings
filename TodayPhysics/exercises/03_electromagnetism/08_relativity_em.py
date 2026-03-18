"""
相对论性电磁学 Relativistic Electromagnetism
难度 Difficulty: ★★★★★

学习目标 Learning Objectives:
- 理解电磁场的洛伦兹变换 (Understand Lorentz transformation of EM fields)
- 掌握电磁场张量及其不变量 (Master field tensor and invariants)
- 分析运动电荷的场分布 (Analyze field of moving charge)
- 理解四维势和规范变换 (Understand four-potential and gauge)

物理背景 Physical Background:
电磁场在不同惯性系中的表现不同。在一个参考系中是纯电场，
在另一个参考系中可能既有电场又有磁场。电磁场张量统一描述
电场和磁场，使麦克斯韦方程具有明显的洛伦兹协变形式。

核心公式 Key Formulas:
- 洛伦兹因子: γ = 1/√(1 - v²/c²)
- 电场变换: E'_∥ = E_∥, E'_⊥ = γ(E_⊥ + v × B)
- 磁场变换: B'_∥ = B_∥, B'_⊥ = γ(B_⊥ - v × E/c²)
- 电磁场张量: F^μν（4×4反对称张量）
- 第一不变量: I₁ = E² - c²B²（在所有惯性系中相同）
- 第二不变量: I₂ = E·B（在所有惯性系中相同）
- 四维电流: J^μ = (cρ, J)
- 四维势: A^μ = (φ/c, A)

重要结论 Key Results:
- 纯电场在另一参考系中可产生磁场
- 运动电荷的场在前进方向被"压缩"（聚束效应）
- E·B = 0 时，存在使E或B为零的参考系
- 麦克斯韦方程的洛伦兹协变形式: ∂_μF^μν = μ₀J^ν

单位说明 Units:
- 采用SI单位制
- 度规约定: (+,-,-,-) 或 (-,+,+,+)，本文件使用(+,-,-,-)
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import c, epsilon_0, mu_0, e, m_e

# I AM NOT DONE

# =============================================================================
# 练习 8.1: 洛伦兹因子
# Exercise 8.1: Lorentz Factor
# =============================================================================
# 物理背景 Physical Background:
# 洛伦兹因子γ是狭义相对论的核心量，描述时间膨胀和长度收缩。
# 当v << c时，γ ≈ 1；当v → c时，γ → ∞。

def lorentz_factor(v):
    """
    洛伦兹因子
    Lorentz factor

    参数 Parameters:
        v: 速度 [m/s]

    返回 Returns:
        γ（无量纲）

    公式 Formula:
        γ = 1/√(1 - v²/c²) = 1/√(1 - β²)

    常用值:
        v = 0.6c: γ = 1.25
        v = 0.8c: γ = 1.67
        v = 0.9c: γ = 2.29
        v = 0.99c: γ = 7.09
    """
    return 1 / np.sqrt(1 - (v/c)**2)


def velocity_from_gamma(gamma):
    """
    从洛伦兹因子求速度
    Velocity from Lorentz factor

    参数 Parameters:
        gamma: 洛伦兹因子（无量纲）

    返回 Returns:
        速度 v [m/s]

    公式 Formula:
        v = c√(1 - 1/γ²)
    """
    return c * np.sqrt(1 - 1/gamma**2)


# =============================================================================
# 练习 8.2: 电场的洛伦兹变换
# Exercise 8.2: Lorentz Transformation of Electric Field
# =============================================================================
# 物理背景 Physical Background:
# 电场在不同惯性系中的值不同。平行于相对运动方向的分量不变，
# 垂直分量发生变换，且与磁场耦合。这说明电场和磁场是同一物理
# 实体（电磁场）的不同表现。

def transform_E_parallel(E_para, v):
    """
    平行于速度方向的电场分量（不变）
    Parallel electric field component (invariant)

    参数 Parameters:
        E_para: 电场平行分量 [V/m]
        v: 相对速度 [m/s]（实际未使用）

    返回 Returns:
        E'_∥ [V/m]

    公式 Formula:
        E'_∥ = E_∥（平行分量不变）
    """
    return E_para


def transform_E_perpendicular(E_perp, B_perp, v):
    """
    垂直于速度方向的电场分量变换
    Perpendicular electric field transformation

    参数 Parameters:
        E_perp: 电场垂直分量 [V/m]
        B_perp: 磁场垂直分量 [T]
        v: 相对速度 [m/s]

    返回 Returns:
        E'_⊥ [V/m]

    公式 Formula:
        E'_⊥ = γ(E_⊥ + v × B)

    说明: 磁场对电场变换有贡献
    在纯磁场中运动，会"看到"电场
    """
    gamma = lorentz_factor(v)
    # v × B 对 E' 的贡献
    return gamma * (E_perp + v * B_perp)


def transform_electric_field(E, B, v_vec):
    """
    电场的完整洛伦兹变换
    Complete Lorentz transformation of electric field

    参数 Parameters:
        E: 电场矢量 [Ex, Ey, Ez] [V/m]
        B: 磁场矢量 [Bx, By, Bz] [T]
        v_vec: 速度矢量 [vx, vy, vz] [m/s]

    返回 Returns:
        E': 变换后的电场 [V/m]

    公式 Formula:
        E' = γ(E + v × B) - (γ-1)(E·v̂)v̂

    等价形式:
        E'_∥ = E_∥
        E'_⊥ = γ(E_⊥ + v × B)
    """
    v = np.linalg.norm(v_vec)
    if v < 1e-10:
        return np.array(E)

    gamma = lorentz_factor(v)
    v_hat = v_vec / v

    # v × B 项
    v_cross_B = np.cross(v_vec, B)

    # 平行分量 (E·v̂)v̂
    E_para = np.dot(E, v_hat) * v_hat

    E_prime = gamma * (np.array(E) + v_cross_B) - (gamma - 1) * E_para
    return E_prime


# =============================================================================
# 练习 8.3: 磁场的洛伦兹变换
# Exercise 8.3: Lorentz Transformation of Magnetic Field
# =============================================================================
# 物理背景 Physical Background:
# 磁场的变换与电场对称。在纯电场中运动，会"看到"磁场。
# 这解释了为什么运动电荷产生磁场——在电荷静止的参考系中只有电场。

def transform_B_parallel(B_para, v):
    """
    平行于速度方向的磁场分量（不变）
    Parallel magnetic field component (invariant)

    公式 Formula:
        B'_∥ = B_∥（平行分量不变）
    """
    return B_para


def transform_B_perpendicular(B_perp, E_perp, v):
    """
    垂直于速度方向的磁场分量变换
    Perpendicular magnetic field transformation

    参数 Parameters:
        B_perp: 磁场垂直分量 [T]
        E_perp: 电场垂直分量 [V/m]
        v: 相对速度 [m/s]

    返回 Returns:
        B'_⊥ [T]

    公式 Formula:
        B'_⊥ = γ(B_⊥ - v × E/c²)

    说明: 电场对磁场变换有贡献
    在纯电场中运动，会"看到"磁场
    """
    gamma = lorentz_factor(v)
    return gamma * (B_perp - v * E_perp / c**2)


def transform_magnetic_field(E, B, v_vec):
    """
    磁场的完整洛伦兹变换
    Complete Lorentz transformation of magnetic field

    参数 Parameters:
        E: 电场矢量 [V/m]
        B: 磁场矢量 [T]
        v_vec: 速度矢量 [m/s]

    返回 Returns:
        B': 变换后的磁场 [T]

    公式 Formula:
        B' = γ(B - v × E/c²) - (γ-1)(B·v̂)v̂

    等价形式:
        B'_∥ = B_∥
        B'_⊥ = γ(B_⊥ - v × E/c²)
    """
    v = np.linalg.norm(v_vec)
    if v < 1e-10:
        return np.array(B)

    gamma = lorentz_factor(v)
    v_hat = v_vec / v

    # v × E / c² 项
    v_cross_E = np.cross(v_vec, E) / c**2

    # 平行分量 (B·v̂)v̂
    B_para = np.dot(B, v_hat) * v_hat

    B_prime = gamma * (np.array(B) - v_cross_E) - (gamma - 1) * B_para
    return B_prime


# =============================================================================
# 练习 8.4: 电磁场张量
# Exercise 8.4: Electromagnetic Field Tensor
# =============================================================================
# 物理背景 Physical Background:
# 电磁场张量F^μν是一个4×4反对称张量，将电场和磁场统一描述。
# 使用张量形式，麦克斯韦方程可以写成明显的洛伦兹协变形式。
# 存在两个洛伦兹不变量，它们在所有惯性系中取值相同。

def field_tensor(E, B):
    """
    电磁场张量
    Electromagnetic field tensor F^μν

    参数 Parameters:
        E: 电场 [Ex, Ey, Ez] [V/m]
        B: 磁场 [Bx, By, Bz] [T]

    返回 Returns:
        F^μν: 4×4反对称张量

    矩阵形式（使用(+,-,-,-)度规）:
        F^μν = | 0    -Ex/c  -Ey/c  -Ez/c |
               | Ex/c   0     -Bz    By   |
               | Ey/c   Bz     0    -Bx   |
               | Ez/c  -By    Bx     0    |

    说明: 对角线为零，F^μν = -F^νμ
    """
    Ex, Ey, Ez = E
    Bx, By, Bz = B

    F = np.array([
        [0, -Ex/c, -Ey/c, -Ez/c],
        [Ex/c, 0, -Bz, By],
        [Ey/c, Bz, 0, -Bx],
        [Ez/c, -By, Bx, 0]
    ])
    return F


def dual_field_tensor(E, B):
    """
    对偶电磁场张量
    Dual field tensor G^μν

    参数 Parameters:
        E: 电场 [V/m]
        B: 磁场 [T]

    返回 Returns:
        G^μν: 对偶张量

    公式 Formula:
        G^μν = (1/2)ε^μνρσ F_ρσ

    矩阵形式:
        G^μν = | 0    -Bx   -By   -Bz  |
               | Bx    0    Ez/c -Ey/c |
               | By  -Ez/c   0    Ex/c |
               | Bz   Ey/c -Ex/c   0   |

    说明: 对偶变换相当于 E → cB, B → -E/c
    """
    Ex, Ey, Ez = E
    Bx, By, Bz = B

    G = np.array([
        [0, -Bx, -By, -Bz],
        [Bx, 0, Ez/c, -Ey/c],
        [By, -Ez/c, 0, Ex/c],
        [Bz, Ey/c, -Ex/c, 0]
    ])
    return G


def lorentz_invariant_1(E, B):
    """
    第一洛伦兹不变量
    First Lorentz invariant

    返回 Returns:
        I₁ = E² - c²B² [V²/m²]

    公式 Formula:
        I₁ = E² - c²B² = -(1/2)F_μν F^μν

    物理意义:
        I₁ > 0: 电场占主导（类电场）
        I₁ < 0: 磁场占主导（类磁场）
        I₁ = 0: 电磁波（E = cB）
    """
    return np.dot(E, E) - c**2 * np.dot(B, B)


def lorentz_invariant_2(E, B):
    """
    第二洛伦兹不变量
    Second Lorentz invariant

    返回 Returns:
        I₂ = E·B [V·T/m]

    公式 Formula:
        I₂ = E·B = -(c/4)F_μν G^μν

    物理意义:
        I₂ = 0: 存在使E或B为零的参考系
        I₂ ≠ 0: 任何参考系中E和B都不为零
        电磁波: I₂ = 0（E⊥B）
    """
    return np.dot(E, B)


# =============================================================================
# 练习 8.5: 运动电荷的场
# Exercise 8.5: Field of a Moving Charge
# =============================================================================
# 物理背景 Physical Background:
# 匀速运动电荷的场不是球对称的。场在垂直于运动方向上增强，
# 在运动方向上减弱（场被"压扁"）。高速粒子的场集中在
# 与运动方向垂直的"盘"状区域（相对论性聚束效应）。

def moving_charge_E_field(q, r_vec, v_vec):
    """
    匀速运动电荷的电场
    Electric field of uniformly moving charge

    参数 Parameters:
        q: 电荷量 [C]
        r_vec: 从电荷到场点的位矢 [m]
        v_vec: 电荷速度 [m/s]

    返回 Returns:
        电场矢量 E [V/m]

    公式 Formula（电荷在原点时）:
        E = (q/4πε₀) × (1-β²)r̂ / [r²(1-β²sin²θ)]^(3/2)

    特点:
        θ = 0 (沿运动方向): E ∝ 1/γ²（减弱）
        θ = π/2 (垂直方向): E ∝ γ（增强）

    这是李纳-维谢尔势的匀速运动特例
    """
    v = np.linalg.norm(v_vec)
    r = np.linalg.norm(r_vec)

    if r < 1e-20:
        return np.array([np.inf, np.inf, np.inf])

    gamma = lorentz_factor(v)
    beta = v / c

    # 计算v和r之间的夹角
    if v > 1e-10:
        cos_theta = np.dot(r_vec, v_vec) / (r * v)
        sin_theta_sq = 1 - cos_theta**2
    else:
        sin_theta_sq = 0

    # 场强度因子
    factor = (1 - beta**2) / (r**2 * (1 - beta**2 * sin_theta_sq)**(3/2))
    E_mag = q / (4 * np.pi * epsilon_0) * factor

    r_hat = r_vec / r
    return E_mag * r_hat


def moving_charge_B_field(q, r_vec, v_vec):
    """
    匀速运动电荷的磁场
    Magnetic field of uniformly moving charge

    参数 Parameters:
        q: 电荷量 [C]
        r_vec: 从电荷到场点的位矢 [m]
        v_vec: 电荷速度 [m/s]

    返回 Returns:
        磁场矢量 B [T]

    公式 Formula:
        B = (v × E) / c² = μ₀ε₀(v × E)

    说明: 磁场环绕运动方向，大小与速度成正比
    """
    E = moving_charge_E_field(q, r_vec, v_vec)
    return np.cross(v_vec, E) / c**2


def relativistic_beaming_angle(gamma):
    """
    相对论性聚束角
    Relativistic beaming angle

    参数 Parameters:
        gamma: 洛伦兹因子

    返回 Returns:
        聚束半角 θ_beam [rad]

    公式 Formula:
        θ_beam ≈ 1/γ

    物理意义:
        高速粒子的辐射/场集中在半角约1/γ的锥内
        同步辐射、切伦科夫辐射的特征
        γ = 10: θ ≈ 5.7°
        γ = 100: θ ≈ 0.57°
    """
    return 1 / gamma


# =============================================================================
# 练习 8.6: 四维电流和势
# Exercise 8.6: Four-Current and Four-Potential
# =============================================================================
# 物理背景 Physical Background:
# 四维形式将标量和矢量合并为协变量。
# 电荷守恒和连续性方程变成 ∂_μJ^μ = 0。
# 麦克斯韦方程变成 □A^μ = μ₀J^μ（洛伦兹规范下）。

def four_current(rho, J):
    """
    四维电流密度
    Four-current density

    参数 Parameters:
        rho: 电荷密度 [C/m³]
        J: 电流密度矢量 [Jx, Jy, Jz] [A/m²]

    返回 Returns:
        J^μ = (cρ, Jx, Jy, Jz)

    连续性方程（四维形式）:
        ∂_μJ^μ = 0
        等价于 ∂ρ/∂t + ∇·J = 0
    """
    return np.array([c * rho, J[0], J[1], J[2]])


def four_potential(phi, A):
    """
    四维势
    Four-potential

    参数 Parameters:
        phi: 标量电势 [V]
        A: 矢量磁势 [Ax, Ay, Az] [T·m]

    返回 Returns:
        A^μ = (φ/c, Ax, Ay, Az)

    电磁场与势的关系:
        F^μν = ∂^μA^ν - ∂^νA^μ
        即 E = -∇φ - ∂A/∂t, B = ∇×A
    """
    return np.array([phi/c, A[0], A[1], A[2]])


def lorentz_gauge_condition(phi, A, drho_dt, div_A):
    """
    洛伦兹规范条件
    Lorentz gauge condition

    参数 Parameters:
        phi: 标量势 [V]
        A: 矢量势 [T·m]
        drho_dt: ∂φ/∂t [V/s]（实际未使用）
        div_A: ∇·A [T]

    返回 Returns:
        是否满足洛伦兹规范（布尔值）

    洛伦兹规范:
        ∂_μA^μ = 0
        等价于 (1/c²)∂φ/∂t + ∇·A = 0

    优点: 方程解耦，明显的洛伦兹协变性
    """
    return np.abs(drho_dt/c**2 + div_A) < 1e-10


def transform_four_potential(phi, A, v):
    """
    四维势的洛伦兹变换
    Lorentz transformation of four-potential

    参数 Parameters:
        phi: 标量势 [V]
        A: 矢量势 [Ax, Ay, Az] [T·m]
        v: 沿x方向的相对速度 [m/s]

    返回 Returns:
        (phi', A'): 变换后的势

    公式 Formula（沿x方向boost）:
        φ' = γ(φ - vAx)
        A'x = γ(Ax - vφ/c²)
        A'y = Ay
        A'z = Az
    """
    gamma = lorentz_factor(v)

    phi_prime = gamma * (phi - v * A[0])
    Ax_prime = gamma * (A[0] - v * phi / c**2)
    Ay_prime = A[1]
    Az_prime = A[2]

    return phi_prime, np.array([Ax_prime, Ay_prime, Az_prime])


# =============================================================================
# 可视化
# =============================================================================
def plot_relativity_em():
    """绘制相对论电磁学相关图"""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 洛伦兹因子
    ax1 = axes[0, 0]
    v = np.linspace(0, 0.999, 100) * c
    gamma = [lorentz_factor(vi) for vi in v]

    ax1.semilogy(v/c, gamma, 'b-', linewidth=2)
    ax1.axhline(y=2, color='r', linestyle='--', alpha=0.5, label='γ = 2 (v = 0.866c)')
    ax1.axhline(y=10, color='g', linestyle='--', alpha=0.5, label='γ = 10 (v = 0.995c)')
    ax1.set_xlabel('v/c')
    ax1.set_ylabel('γ')
    ax1.set_title('洛伦兹因子')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 运动电荷的电场分布
    ax2 = axes[0, 1]
    theta = np.linspace(0, 2*np.pi, 100)

    for beta in [0, 0.5, 0.9, 0.99]:
        gamma_val = 1 / np.sqrt(1 - beta**2) if beta < 1 else 100
        # 电场强度的角分布 (归一化)
        sin_theta = np.sin(theta)
        E_factor = (1 - beta**2) / (1 - beta**2 * sin_theta**2)**(3/2)
        ax2.polar(theta, E_factor, label=f'β = {beta}', linewidth=2)

    ax2.set_title('运动电荷电场角分布')
    ax2.legend(loc='upper right')

    # 3. 电场变换
    ax3 = axes[0, 2]
    v_range = np.linspace(0, 0.99, 50) * c

    E0 = 1e6  # V/m
    B0 = 1e-3  # T

    E_trans = [transform_E_perpendicular(E0, B0, v) for v in v_range]
    E_trans_no_B = [lorentz_factor(v) * E0 for v in v_range]

    ax3.plot(v_range/c, np.array(E_trans)/E0, 'b-', linewidth=2, label='E\'_⊥ (with B)')
    ax3.plot(v_range/c, np.array(E_trans_no_B)/E0, 'r--', linewidth=2, label='E\'_⊥ (B=0)')
    ax3.set_xlabel('v/c')
    ax3.set_ylabel('E\'/E₀')
    ax3.set_title('电场洛伦兹变换')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 电磁场不变量
    ax4 = axes[1, 0]
    v_test = np.linspace(0, 0.9, 20) * c

    E = np.array([1e6, 0, 0])  # V/m
    B = np.array([0, 0, 1e-3])  # T

    I1_original = lorentz_invariant_1(E, B)
    I2_original = lorentz_invariant_2(E, B)

    I1_transformed = []
    I2_transformed = []

    for v in v_test:
        v_vec = np.array([v, 0, 0])
        E_prime = transform_electric_field(E, B, v_vec)
        B_prime = transform_magnetic_field(E, B, v_vec)
        I1_transformed.append(lorentz_invariant_1(E_prime, B_prime))
        I2_transformed.append(lorentz_invariant_2(E_prime, B_prime))

    ax4.plot(v_test/c, np.array(I1_transformed)/I1_original, 'bo-', label='I₁/I₁₀')
    ax4.axhline(y=1, color='r', linestyle='--', alpha=0.5)
    ax4.set_xlabel('v/c')
    ax4.set_ylabel('不变量比值')
    ax4.set_title('洛伦兹不变量验证')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim(0.9, 1.1)

    # 5. 相对论性聚束
    ax5 = axes[1, 1]
    gamma_range = np.linspace(1, 100, 100)
    theta_beam = [relativistic_beaming_angle(g) * 180 / np.pi for g in gamma_range]

    ax5.semilogy(gamma_range, theta_beam, 'b-', linewidth=2)
    ax5.set_xlabel('γ')
    ax5.set_ylabel('聚束角 (度)')
    ax5.set_title('相对论性聚束效应')
    ax5.grid(True, alpha=0.3)

    # 6. 电磁场张量可视化
    ax6 = axes[1, 2]
    E_test = np.array([1, 0.5, 0])
    B_test = np.array([0, 0, 0.5])

    F = field_tensor(E_test, B_test)

    im = ax6.imshow(F, cmap='RdBu', vmin=-1.5, vmax=1.5)
    ax6.set_xticks([0, 1, 2, 3])
    ax6.set_yticks([0, 1, 2, 3])
    ax6.set_xticklabels(['0', '1', '2', '3'])
    ax6.set_yticklabels(['0', '1', '2', '3'])
    ax6.set_xlabel('ν')
    ax6.set_ylabel('μ')
    ax6.set_title('电磁场张量 F^μν')
    plt.colorbar(im, ax=ax6)

    plt.tight_layout()
    plt.savefig('relativity_em.png', dpi=150)
    print("图像已保存为 relativity_em.png")
    plt.show()


# =============================================================================
# 验证函数
# =============================================================================
def verify():
    """
    验证所有相对论电磁学练习
    Verify all relativistic electromagnetism exercises

    验证内容 Verification:
        8.1 洛伦兹因子计算
        8.2 电场洛伦兹变换
        8.3 磁场洛伦兹变换
        8.4 洛伦兹不变量
        8.5 运动电荷的场
        8.6 四维电流和势
    """
    all_passed = True

    # 验证 8.1: 洛伦兹因子
    # Check 8.1: Lorentz factor
    gamma = lorentz_factor(0.6 * c)
    expected_gamma = 1.25  # 3/4/5 直角三角形
    if not np.isclose(gamma, expected_gamma, rtol=0.01):
        print("❌ 8.1 洛伦兹因子错误")
        print("   提示: γ = 1/√(1 - v²/c²)")
        all_passed = False
    else:
        print(f"✓ 8.1 洛伦兹因子正确 (γ(0.6c) = {gamma:.3f})")

    # 验证 8.2: 电场变换
    # Check 8.2: Electric field transformation
    E_para = 1e6   # 平行分量
    E_perp = 1e6   # 垂直分量
    B_perp = 0     # 无磁场
    v = 0.5 * c

    E_para_prime = transform_E_parallel(E_para, v)
    E_perp_prime = transform_E_perpendicular(E_perp, B_perp, v)

    if not np.isclose(E_para_prime, E_para):
        print("❌ 8.2 平行电场应不变")
        print("   提示: E'_∥ = E_∥")
        all_passed = False
    elif not np.isclose(E_perp_prime, lorentz_factor(v) * E_perp, rtol=0.01):
        print("❌ 8.2 垂直电场变换错误")
        print("   提示: E'_⊥ = γE_⊥（无磁场时）")
        all_passed = False
    else:
        print(f"✓ 8.2 电场变换正确")

    # 验证 8.3: 磁场变换
    # Check 8.3: Magnetic field transformation
    B_para = 1e-3  # 平行分量
    B_perp = 1e-3  # 垂直分量
    E_perp = 0     # 无电场

    B_para_prime = transform_B_parallel(B_para, v)
    B_perp_prime = transform_B_perpendicular(B_perp, E_perp, v)

    if not np.isclose(B_para_prime, B_para):
        print("❌ 8.3 平行磁场应不变")
        print("   提示: B'_∥ = B_∥")
        all_passed = False
    else:
        print(f"✓ 8.3 磁场变换正确")

    # 验证 8.4: 洛伦兹不变量
    # Check 8.4: Lorentz invariants
    E = np.array([1e6, 0, 0])  # 沿x的电场
    B = np.array([0, 0, 1e-3]) # 沿z的磁场

    I1_before = lorentz_invariant_1(E, B)
    I2_before = lorentz_invariant_2(E, B)

    v_vec = np.array([0.5*c, 0, 0])
    E_prime = transform_electric_field(E, B, v_vec)
    B_prime = transform_magnetic_field(E, B, v_vec)

    I1_after = lorentz_invariant_1(E_prime, B_prime)
    I2_after = lorentz_invariant_2(E_prime, B_prime)

    if not np.isclose(I1_before, I1_after, rtol=0.05):
        print(f"❌ 8.4 第一不变量I₁应保持不变")
        print(f"   变换前: {I1_before:.2e}, 变换后: {I1_after:.2e}")
        all_passed = False
    else:
        print(f"✓ 8.4 洛伦兹不变量正确（I₁和I₂在变换后保持不变）")

    # 验证 8.5: 运动电荷的场
    # Check 8.5: Field of moving charge
    q = e
    r_vec = np.array([1e-9, 0, 0])  # 1nm处
    v_vec = np.array([0, 0, 0])     # 静止电荷

    E_static = moving_charge_E_field(q, r_vec, v_vec)
    expected_E = q / (4 * np.pi * epsilon_0 * 1e-18)  # 库仑定律

    if not np.isclose(E_static[0], expected_E, rtol=0.01):
        print("❌ 8.5 静止电荷场应符合库仑定律")
        all_passed = False
    else:
        print(f"✓ 8.5 运动电荷场正确（静止时回归库仑定律）")

    # 验证 8.6: 四维电流
    # Check 8.6: Four-current
    rho = 1e-6  # C/m³
    J = np.array([1, 0, 0])  # A/m²

    J_mu = four_current(rho, J)
    if not np.isclose(J_mu[0], c * rho):
        print("❌ 8.6 四维电流错误")
        print("   提示: J⁰ = cρ")
        all_passed = False
    else:
        print(f"✓ 8.6 四维电流和势正确")

    if all_passed:
        print("\n🎉 所有测试通过！正在生成可视化...")
        try:
            plot_relativity_em()
        except Exception as ex:
            print(f"可视化生成失败: {ex}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("相对论性电磁学 Relativistic Electromagnetism")
    print("=" * 50)
    verify()
