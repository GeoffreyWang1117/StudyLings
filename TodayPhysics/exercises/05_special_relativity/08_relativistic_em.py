"""
相对论电动力学 Relativistic Electrodynamics
难度 Difficulty: ★★★★★

学习目标 Learning Objectives:
- 理解电磁场张量的构造和物理意义
  Understand the electromagnetic field tensor construction and meaning
- 掌握电磁场在不同参考系中的洛伦兹变换
  Master Lorentz transformation of electromagnetic fields
- 分析相对论协变形式的麦克斯韦方程
  Analyze Maxwell's equations in covariant form
- 计算运动电荷的电磁场
  Calculate electromagnetic fields of moving charges

物理背景 Physical Background:
麦克斯韦方程在洛伦兹变换下是协变的，这是狭义相对论的核心预言之一。
电场和磁场不是独立的，而是同一个物理量（电磁场张量）在不同参考系中的分量。

电磁场张量 F^μν:
将电场 E 和磁场 B 统一在一个反对称张量中：
F^μν = | 0    -Ex/c  -Ey/c  -Ez/c |
       | Ex/c   0     -Bz    By   |
       | Ey/c  Bz      0    -Bx   |
       | Ez/c -By     Bx     0    |

电磁场的洛伦兹变换:
- 沿速度方向的分量不变: E∥' = E∥, B∥' = B∥
- 垂直方向混合变换: E⊥' = γ(E⊥ + v×B), B⊥' = γ(B⊥ - v×E/c²)

洛伦兹不变量:
- I₁ = E² - c²B² (在所有参考系中相同)
- I₂ = E·B (在所有参考系中相同)

关键公式 Key Formulas:
- 电磁场张量: F^μν = ∂^μA^ν - ∂^νA^μ
- 协变洛伦兹力: f^μ = qF^μν u_ν
- 协变麦克斯韦方程: ∂_μF^μν = μ₀j^ν
- Bianchi恒等式: ∂_λF_μν + ∂_μF_νλ + ∂_νF_λμ = 0
- Larmor辐射功率: P = q²a²/(6πε₀c³)

单位说明 Units:
- 电场: V/m = N/C
- 磁场: T = Wb/m² = kg/(A·s²)
- 四势: A^μ = (φ/c, Ax, Ay, Az)
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import c, epsilon_0, mu_0, e, m_e

# I AM NOT DONE

# =============================================================================
# 练习 8.1: 电磁场张量
# Exercise 8.1: Electromagnetic Field Tensor
#
# 物理背景：电磁场张量将电场和磁场统一在一个数学对象中
#
# 为什么需要电磁场张量？
# 在三维表述中，电场 E 和磁场 B 是独立的矢量。
# 但洛伦兹变换会将它们混合 - 一个参考系的纯电场
# 在另一个参考系中变成电场和磁场的混合。
# 电磁场张量 F^μν 使变换规律简单统一。
#
# 电磁场张量的结构：
# F^μν 是反对称张量（F^μν = -F^νμ）
# 6 个独立分量恰好对应 E 的 3 个分量 + B 的 3 个分量
#
# 对偶张量 *F^μν:
# 通过 E ↔ cB 对换（或 Levi-Civita 符号缩并）得到
# 在麦克斯韦方程的协变形式中出现
#
# Physical background: Unifying E and B in the field tensor
# =============================================================================
def electromagnetic_field_tensor(E, B):
    """
    构建电磁场张量 F^μν Electromagnetic field tensor

    公式 Formula:
    F^μν = | 0    -Ex/c  -Ey/c  -Ez/c |
           | Ex/c   0     -Bz    By   |
           | Ey/c  Bz      0    -Bx   |
           | Ez/c -By     Bx     0    |

    参数 Parameters:
        E: 电场三分量 [Ex, Ey, Ez] (V/m)
        B: 磁场三分量 [Bx, By, Bz] (T)

    返回 Returns:
        F: 4×4 电磁场张量（反对称）

    性质：
    - F^μν = -F^νμ（反对称）
    - F^0i = -Ei/c，F^ij = -ε^ijk B_k
    - 在洛伦兹变换下: F'^μν = Λ^μ_α Λ^ν_β F^αβ
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
    对偶电磁场张量 *F^μν Dual field tensor

    公式 Formula: *F^μν = (1/2)ε^μνρσ F_ρσ
    等效于 E ↔ cB 对换

    *F^μν = | 0    -Bx   -By   -Bz   |
            | Bx    0    Ez/c -Ey/c |
            | By  -Ez/c   0    Ex/c |
            | Bz   Ey/c -Ex/c  0    |

    参数 Parameters:
        E: 电场三分量 (V/m)
        B: 磁场三分量 (T)

    返回 Returns:
        *F: 4×4 对偶场张量

    应用：
    - 协变麦克斯韦方程: ∂_μ*F^μν = 0（无磁单极子，法拉第定律）
    - 场不变量: F_μν *F^μν ∝ E·B
    """
    Ex, Ey, Ez = E
    Bx, By, Bz = B

    F_dual = np.array([
        [0, -Bx, -By, -Bz],
        [Bx, 0, Ez/c, -Ey/c],
        [By, -Ez/c, 0, Ex/c],
        [Bz, Ey/c, -Ex/c, 0]
    ])
    return F_dual


# =============================================================================
# 练习 8.2: 场的洛伦兹变换
# Exercise 8.2: Lorentz Transformation of Fields
#
# 物理背景：电场和磁场在参考系变换下混合
#
# 一个著名的例子：
# 静止电荷只产生电场。但在运动参考系中看，
# 这个电荷在运动，形成电流，因此产生磁场。
# E 和 B 不是独立的，而是同一物理量的不同分量。
#
# 变换规律（沿 x 方向推进）:
# - 平行分量不变: E∥' = E∥, B∥' = B∥
# - 垂直分量混合变换:
#   E⊥' = γ(E⊥ + v×B)
#   B⊥' = γ(B⊥ - v×E/c²)
#
# 洛伦兹不变量：
# - I₁ = E² - c²B² = E'² - c²B'²
# - I₂ = E·B = E'·B'
# 这两个量在所有参考系中相同！
#
# Physical background: Mixing of E and B under Lorentz transformation
# =============================================================================
def transform_fields(E, B, v):
    """
    电磁场的洛伦兹变换 Lorentz transformation of EM fields

    公式 Formula（沿 x 方向推进）:
    E∥' = E∥,  B∥' = B∥（平行分量不变）
    E⊥' = γ(E⊥ + v×B),  B⊥' = γ(B⊥ - v×E/c²)

    参数 Parameters:
        E: 原参考系电场 [Ex, Ey, Ez] (V/m)
        B: 原参考系磁场 [Bx, By, Bz] (T)
        v: 新参考系相对原参考系沿 x 方向的速度 (m/s)

    返回 Returns:
        (E', B'): 新参考系中的电场和磁场

    重要示例：
    - 纯电场变换后出现磁场
    - 纯磁场变换后出现电场
    - 这体现了电磁场的统一性
    """
    Ex, Ey, Ez = E
    Bx, By, Bz = B

    gamma = 1 / np.sqrt(1 - (v/c)**2)

    # 沿 x 方向（推进方向）的分量不变
    Ex_prime = Ex
    Bx_prime = Bx

    # 垂直于推进方向的分量混合变换
    Ey_prime = gamma * (Ey - v * Bz)
    Ez_prime = gamma * (Ez + v * By)

    By_prime = gamma * (By + v * Ez / c**2)
    Bz_prime = gamma * (Bz - v * Ey / c**2)

    E_prime = np.array([Ex_prime, Ey_prime, Ez_prime])
    B_prime = np.array([Bx_prime, By_prime, Bz_prime])

    return E_prime, B_prime

def field_invariants(E, B):
    """
    电磁场的洛伦兹不变量 Lorentz invariants of EM fields

    公式 Formula:
    I₁ = E² - c²B²（第一不变量）
    I₂ = E·B（第二不变量）

    参数 Parameters:
        E: 电场矢量 (V/m)
        B: 磁场矢量 (T)

    返回 Returns:
        (I1, I2): 两个洛伦兹不变量

    物理意义：
    - I₁ > 0: 电场主导，存在参考系使 B = 0
    - I₁ < 0: 磁场主导，存在参考系使 E = 0
    - I₁ = 0: 电磁波（E ⊥ B，|E| = c|B|）
    - I₂ = 0: 可以找到参考系使 E ⊥ B
    - I₂ ≠ 0: E 和 B 在所有参考系中都不垂直
    """
    I1 = np.dot(E, E) - c**2 * np.dot(B, B)
    I2 = np.dot(E, B)
    return I1, I2


# =============================================================================
# 练习 8.3: 四势
# Exercise 8.3: Four-Potential
#
# 物理背景：四势是电磁场的"源"
#
# 三维表述中：
# E = -∇φ - ∂A/∂t（电场来自标量势和矢量势）
# B = ∇×A（磁场来自矢量势）
#
# 四维表述：
# 四势 A^μ = (φ/c, Ax, Ay, Az) 是四矢量
# 场张量: F^μν = ∂^μA^ν - ∂^νA^μ
#
# 规范自由度：
# A^μ → A^μ + ∂^μχ 不改变物理场
# 洛伦兹规范: ∂_μA^μ = 0（协变条件）
# 库仑规范: ∇·A = 0（非协变）
#
# Lienard-Wiechert 势：
# 运动点电荷的精确势，考虑推迟时间效应
#
# Physical background: Four-potential and gauge freedom
# =============================================================================
def four_potential(phi, A):
    """
    四势 Four-potential

    公式 Formula: A^μ = (φ/c, Ax, Ay, Az)

    参数 Parameters:
        phi: 标量势（电势）(V)
        A: 矢量势 [Ax, Ay, Az] (Wb/m = V·s/m)

    返回 Returns:
        A^μ: 四势数组

    关系：
    - E = -∇φ - ∂A/∂t
    - B = ∇×A
    - F^μν = ∂^μA^ν - ∂^νA^μ
    """
    return np.array([phi/c, A[0], A[1], A[2]])

def lorentz_gauge_condition(A_mu, derivatives):
    """
    洛伦兹规范条件 Lorentz gauge condition

    公式 Formula: ∂_μA^μ = 0
    展开形式: (1/c²)∂φ/∂t + ∇·A = 0

    参数 Parameters:
        A_mu: 四势（未使用，为接口一致性）
        derivatives: 四势各分量的导数 [∂A⁰/∂(ct), ∂A¹/∂x, ∂A²/∂y, ∂A³/∂z]

    返回 Returns:
        ∂_μA^μ 的值（应该为零满足规范条件）

    物理意义：
    - 洛伦兹规范是协变条件（在所有参考系中形式相同）
    - 在此规范下，A^μ 满足波动方程: □A^μ = μ₀j^μ
    - 简化了电磁场的求解
    """
    # 使用闵可夫斯基度规的缩并: ∂_μA^μ = ∂₀A⁰ - ∂₁A¹ - ∂₂A² - ∂₃A³
    return derivatives[0] - derivatives[1] - derivatives[2] - derivatives[3]

def coulomb_four_potential(q, r, v=np.zeros(3)):
    """
    点电荷的四势 Four-potential of a point charge

    公式 Formula:
    静止: φ = kq/r, A = 0
    运动（简化）: φ = γkq/r, A = vφ/c²

    参数 Parameters:
        q: 电荷量 (C)
        r: 到电荷的距离 (m)
        v: 电荷速度 (m/s)，默认静止

    返回 Returns:
        A^μ: 四势数组

    说明：
    - 精确的运动电荷势是 Lienard-Wiechert 势
    - 需要考虑推迟时间（光信号传播延迟）
    - 这里给出的是简化近似
    """
    k = 1 / (4 * np.pi * epsilon_0)
    if np.linalg.norm(v) < 1e-10:
        # 静止电荷：标准库仑势
        phi = k * q / r
        A = np.zeros(3)
    else:
        # 运动电荷（简化处理，忽略推迟效应）
        gamma = 1 / np.sqrt(1 - np.dot(v, v)/c**2)
        phi = gamma * k * q / r
        A = v * phi / c**2

    return four_potential(phi, A)


# =============================================================================
# 练习 8.4: 协变洛伦兹力
# Exercise 8.4: Covariant Lorentz Force
#
# 物理背景：洛伦兹力的四矢量形式
#
# 三维洛伦兹力：
# F = q(E + v×B)
# 电场做功，磁场不做功
#
# 协变形式：
# dp^μ/dτ = qF^μν u_ν = f^μ
# 其中 f^μ 是四力
#
# 四力的分量：
# f⁰ = γqE·v/c（功率除以 c）
# fⁱ = γq(E + v×B)ⁱ（三力乘 γ）
#
# 协变形式的优点：
# - 简洁统一（一个方程代替四个）
# - 变换性质清晰
# - 易于推广到弯曲时空
#
# Physical background: Covariant Lorentz force equation
# =============================================================================
def lorentz_force_four_vector(q, F_tensor, u):
    """
    协变形式的洛伦兹力 Covariant Lorentz force

    公式 Formula: f^μ = dp^μ/dτ = qF^μν u_ν

    参数 Parameters:
        q: 电荷量 (C)
        F_tensor: 4×4 电磁场张量 F^μν
        u: 四速度 u^μ = γ(c, vx, vy, vz)

    返回 Returns:
        f^μ: 四力数组

    计算步骤：
    1. 降指标: u_ν = η_νμ u^μ
    2. 矩阵乘法: f^μ = q F^μν u_ν

    物理意义：
    - f⁰ = γP/c（P 是功率）
    - f^i = γF^i（F 是三维力）
    """
    # 下降指标: u_ν = η_νμ u^μ
    eta = np.diag([1, -1, -1, -1])
    u_lower = eta @ u

    f = q * F_tensor @ u_lower
    return f

def extract_three_force(f_mu, gamma):
    """
    从四力提取三力 Extract three-force from four-force

    公式 Formula: F = f^i/γ（i = 1, 2, 3）

    参数 Parameters:
        f_mu: 四力数组 [f⁰, f¹, f², f³]
        gamma: 洛伦兹因子

    返回 Returns:
        F: 三维力向量 [Fx, Fy, Fz] (N)

    关系：f^i = γF^i
    因为 f^μ = dp^μ/dτ = γdp^μ/dt
    """
    return f_mu[1:4] / gamma

def power_from_four_force(f_mu, c_val=c):
    """
    从四力提取功率 Extract power from four-force

    公式 Formula: P = cf⁰

    参数 Parameters:
        f_mu: 四力数组
        c_val: 光速（默认使用全局常数）

    返回 Returns:
        P: 功率 (W)

    推导：
    f⁰ = dp⁰/dτ = γd(E/c)/dt = γP/c
    但由于 f⁰ 的定义，直接有 P = cf⁰
    """
    return c_val * f_mu[0]


# =============================================================================
# 练习 8.5: 运动电荷的场
# Exercise 8.5: Fields of a Moving Charge
#
# 物理背景：运动电荷的电磁场分布
#
# 静止电荷的场是球对称的库仑场。
# 运动电荷的场不再球对称——沿运动方向"压缩"。
#
# 场的角分布：
# 电场在垂直于速度方向最强，沿速度方向最弱
# 比值: E⊥/E∥ = γ²（高速时差异巨大）
#
# 物理图像：
# 在电荷静止系中场是球对称的。
# 变换到实验室系时，洛伦兹收缩使等势面变成椭球。
# 电场线被压扁成"薄饼"形状。
#
# 磁场：
# 运动电荷产生磁场 B = v×E/c²
# 这是运动电荷形成"电流"的结果
#
# Physical background: Relativistic compression of field lines
# =============================================================================
def moving_charge_fields(q, r_vec, v_vec):
    """
    匀速运动电荷的电磁场 EM fields of uniformly moving charge

    参数 Parameters:
        q: 电荷量 (C)
        r_vec: 场点相对于电荷的位置矢量 (m)
        v_vec: 电荷速度矢量 (m/s)

    返回 Returns:
        (E, B): 电场 (V/m) 和磁场 (T)

    公式特点：
    - 电场沿径向，但大小依赖于角度
    - 垂直方向电场增强因子 γ
    - 平行方向电场减弱因子 1/γ²
    - B = v×E/c²

    注意：这是"瞬时"场，没有考虑辐射效应
    加速电荷会辐射，需要 Lienard-Wiechert 势的完整处理
    """
    v = np.linalg.norm(v_vec)
    if v < 1e-10:
        # 静止电荷：标准库仑场
        r = np.linalg.norm(r_vec)
        k = 1 / (4 * np.pi * epsilon_0)
        E = k * q * r_vec / r**3
        B = np.zeros(3)
        return E, B

    gamma = 1 / np.sqrt(1 - v**2/c**2)
    r = np.linalg.norm(r_vec)
    r_hat = r_vec / r

    # 分解为平行和垂直分量
    v_hat = v_vec / v
    r_parallel = np.dot(r_vec, v_hat)
    r_perp_vec = r_vec - r_parallel * v_hat

    # 有效距离（考虑相对论压缩）
    # R_eff² = r²(1 - β²sin²θ) = r_∥² + γ²r_⊥²
    sin_theta_squared = np.dot(r_perp_vec, r_perp_vec) / r**2
    R_eff = r * np.sqrt(1 - (v/c)**2 * sin_theta_squared)

    # 电场（压缩后的库仑场）
    k = 1 / (4 * np.pi * epsilon_0)
    E = k * q * r_vec / (gamma**2 * R_eff**3)

    # 磁场：运动电荷产生的磁场
    B = np.cross(v_vec, E) / c**2

    return E, B


# =============================================================================
# 练习 8.6: 辐射场
# Exercise 8.6: Radiation Fields
#
# 物理背景：加速电荷辐射电磁波
#
# Larmor 公式（非相对论）:
# P = q²a²/(6πε₀c³)
# 辐射功率正比于加速度平方
#
# 相对论修正：
# P = (q²γ⁴/(6πε₀c³))(a⊥² + γ²a∥²)
# 其中 a∥ 和 a⊥ 是平行和垂直于速度的加速度分量
#
# 关键特点：
# 1. 垂直加速度更有效辐射（因子 γ⁴）
# 2. 平行加速度辐射更强（额外因子 γ²）
# 3. 高速粒子的辐射功率可以非常大
#
# 同步辐射：
# 带电粒子在磁场中做圆周运动时的辐射
# 特征频率: ω ~ γ³ω_c（ω_c 是回旋频率）
# 辐射集中在前进方向的 1/γ 锥角内
#
# Physical background: Radiation from accelerated charges
# =============================================================================
def larmor_power(q, a):
    """
    非相对论性 Larmor 辐射功率 Non-relativistic Larmor power

    公式 Formula: P = q²a²/(6πε₀c³)

    参数 Parameters:
        q: 电荷量 (C)
        a: 加速度大小 (m/s²)

    返回 Returns:
        P: 辐射功率 (W)

    数量级估计：
    - 电子以 10¹⁵ m/s² 加速: P ~ 10⁻²⁷ W（极小）
    - 但在同步加速器中 γ 很大时辐射显著

    应用：
    - 射电天文学（脉冲星辐射）
    - 加速器物理（束流能量损失）
    """
    return q**2 * a**2 / (6 * np.pi * epsilon_0 * c**3)

def relativistic_larmor_power(q, gamma, a_parallel, a_perp):
    """
    相对论性 Larmor 公式 Relativistic Larmor formula

    公式 Formula: P = (q²γ⁴/(6πε₀c³))(a⊥² + γ²a∥²)

    参数 Parameters:
        q: 电荷量 (C)
        gamma: 洛伦兹因子
        a_parallel: 平行于速度的加速度分量 (m/s²)
        a_perp: 垂直于速度的加速度分量 (m/s²)

    返回 Returns:
        P: 辐射功率 (W)

    物理要点：
    - γ⁴ 因子使高能粒子辐射极强
    - 平行加速度有额外 γ² 增强
    - 同步辐射（磁场中圆周运动）只有 a⊥，功率 ∝ γ⁴

    应用：
    - 同步辐射光源（X射线源）
    - 天体物理喷流辐射
    """
    return q**2 * gamma**4 / (6 * np.pi * epsilon_0 * c**3) * (a_perp**2 + gamma**2 * a_parallel**2)

def synchrotron_characteristic_frequency(gamma, omega_c):
    """
    同步辐射特征频率 Synchrotron characteristic frequency

    公式 Formula: ω_char ≈ γ³ω_c

    参数 Parameters:
        gamma: 洛伦兹因子
        omega_c: 回旋频率 ω_c = eB/m (rad/s)

    返回 Returns:
        ω_char: 特征角频率 (rad/s)

    物理解释：
    - 非相对论回旋辐射频率 = ω_c
    - 相对论效应使辐射脉冲变窄（时间膨胀）
    - 傅里叶变换使频谱展宽到 γ³ω_c
    - LHC 中 γ ~ 7000，频率提升到 X 射线波段

    同步辐射光源的应用：
    - 蛋白质晶体学
    - 材料科学
    - 医学成像
    """
    return gamma**3 * omega_c


# =============================================================================
# 可视化
# =============================================================================
def plot_relativistic_em():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 电磁场张量分量
    ax1 = axes[0, 0]
    E = [1, 0, 0]
    B = [0, 1, 0]
    F = electromagnetic_field_tensor(E, B)

    im = ax1.imshow(F, cmap='RdBu', aspect='equal')
    ax1.set_xticks(range(4))
    ax1.set_yticks(range(4))
    ax1.set_xticklabels(['0', '1', '2', '3'])
    ax1.set_yticklabels(['0', '1', '2', '3'])
    ax1.set_title(r'电磁场张量 $F^{\mu\nu}$')
    plt.colorbar(im, ax=ax1)

    # 2. 场变换
    ax2 = axes[0, 1]
    v_vals = np.linspace(0, 0.9*c, 50)
    E_orig = [0, 1, 0]  # y方向电场
    B_orig = [0, 0, 0]

    Ey_prime = []
    Bz_prime = []
    for v in v_vals:
        E_p, B_p = transform_fields(E_orig, B_orig, v)
        Ey_prime.append(E_p[1])
        Bz_prime.append(B_p[2] * c)  # 乘c便于比较

    ax2.plot(v_vals/c, Ey_prime, 'b-', linewidth=2, label="E'_y")
    ax2.plot(v_vals/c, Bz_prime, 'r-', linewidth=2, label="cB'_z")
    ax2.set_xlabel('v/c')
    ax2.set_ylabel('场强')
    ax2.set_title('纯电场的变换')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 场不变量
    ax3 = axes[0, 2]
    E_orig = [1, 0, 0]
    B_orig = [0, 0.5/c, 0]
    I1_orig, I2_orig = field_invariants(E_orig, B_orig)

    I1_vals = []
    I2_vals = []
    for v in v_vals:
        E_p, B_p = transform_fields(E_orig, B_orig, v)
        I1, I2 = field_invariants(E_p, B_p)
        I1_vals.append(I1)
        I2_vals.append(I2)

    ax3.plot(v_vals/c, I1_vals, 'b-', linewidth=2, label='I₁ = E²-c²B²')
    ax3.axhline(y=I1_orig, color='b', linestyle='--', alpha=0.5)
    ax3.plot(v_vals/c, I2_vals, 'r-', linewidth=2, label='I₂ = E·B')
    ax3.axhline(y=I2_orig, color='r', linestyle='--', alpha=0.5)
    ax3.set_xlabel('v/c')
    ax3.set_ylabel('不变量')
    ax3.set_title('洛伦兹不变量')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 运动电荷的场（电场线压缩）
    ax4 = axes[1, 0]
    q = e
    v_charge = 0.9 * c

    x = np.linspace(-2, 2, 20)
    y = np.linspace(-2, 2, 20)
    X, Y = np.meshgrid(x, y)

    Ex = np.zeros_like(X)
    Ey = np.zeros_like(Y)

    for i in range(len(x)):
        for j in range(len(y)):
            r_vec = np.array([X[j, i], Y[j, i], 0])
            if np.linalg.norm(r_vec) > 0.1:
                E, B = moving_charge_fields(q, r_vec, np.array([v_charge, 0, 0]))
                Ex[j, i] = E[0]
                Ey[j, i] = E[1]

    # 归一化
    E_mag = np.sqrt(Ex**2 + Ey**2)
    E_mag[E_mag == 0] = 1
    ax4.streamplot(X, Y, Ex/E_mag, Ey/E_mag, density=1.5, color=np.log10(E_mag+1), cmap='hot')
    ax4.scatter([0], [0], c='blue', s=100, zorder=5)
    ax4.set_xlabel('x')
    ax4.set_ylabel('y')
    ax4.set_title('运动电荷的电场 (v=0.9c)')
    ax4.set_aspect('equal')

    # 5. Larmor辐射功率
    ax5 = axes[1, 1]
    a = 1e15  # m/s²
    gamma_vals = np.linspace(1, 100, 100)

    P_nonrel = larmor_power(e, a)
    P_rel = [relativistic_larmor_power(e, g, 0, a) for g in gamma_vals]

    ax5.semilogy(gamma_vals, P_rel, 'b-', linewidth=2, label='相对论')
    ax5.axhline(y=P_nonrel, color='r', linestyle='--', label='非相对论')
    ax5.set_xlabel('γ')
    ax5.set_ylabel('辐射功率 P (W)')
    ax5.set_title('Larmor辐射功率')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. 同步辐射频谱
    ax6 = axes[1, 2]
    B_field = 1  # T
    omega_c = e * B_field / m_e

    gamma_sync = np.linspace(1, 1000, 100)
    omega_char = [synchrotron_characteristic_frequency(g, omega_c) / (2*np.pi) for g in gamma_sync]

    ax6.loglog(gamma_sync, omega_char, 'b-', linewidth=2)
    ax6.set_xlabel('γ')
    ax6.set_ylabel('特征频率 (Hz)')
    ax6.set_title('同步辐射特征频率')
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('relativistic_em.png', dpi=150)
    print("图像已保存为 relativistic_em.png")
    plt.show()


def verify():
    """
    验证所有练习的正确性 Verify all exercises

    检查内容 Checks:
    8.1 电磁场张量构建
    8.2 场变换保持洛伦兹不变量
    8.3 四势构建
    8.4 协变洛伦兹力
    8.5 运动电荷场计算
    8.6 Larmor辐射功率
    """
    all_passed = True

    # 检查 8.1 - 电磁场张量
    E = [1, 0, 0]
    B = [0, 0, 1]
    F = electromagnetic_field_tensor(E, B)
    if F[1, 0] != E[0]/c or F[1, 2] != -B[2]:
        print("错误 8.1 电磁场张量构建不正确，检查 F^μν 的分量定义")
        all_passed = False
    else:
        print(f"通过 8.1 电磁场张量正确")

    # 检查 8.2 - 场变换保持不变量
    E_orig = [0, 1, 0]
    B_orig = [0, 0, 0]
    E_p, B_p = transform_fields(E_orig, B_orig, 0.5*c)
    I1_orig, I2_orig = field_invariants(E_orig, B_orig)
    I1_new, I2_new = field_invariants(E_p, B_p)
    if not np.isclose(I1_orig, I1_new, rtol=0.01):
        print("错误 8.2 场变换后不变量 I₁ = E² - c²B² 不守恒")
        all_passed = False
    else:
        print(f"通过 8.2 场变换正确（洛伦兹不变量守恒）")

    # 检查 8.3 - 四势
    phi = 1
    A = [0, 0, 0]
    A_mu = four_potential(phi, A)
    if not np.isclose(A_mu[0], phi/c, rtol=0.01):
        print("错误 8.3 四势第零分量应为 φ/c")
        all_passed = False
    else:
        print(f"通过 8.3 四势正确")

    # 检查 8.4 - 协变洛伦兹力
    E = [1, 0, 0]
    B = [0, 0, 0]
    F_tensor = electromagnetic_field_tensor(E, B)
    u = np.array([c, 0, 0, 0])  # 静止粒子的四速度
    f = lorentz_force_four_vector(1, F_tensor, u)
    if not np.isclose(f[1], E[0], rtol=0.01):
        print("错误 8.4 协变洛伦兹力计算不正确，静止电荷应受纯电场力")
        all_passed = False
    else:
        print(f"通过 8.4 协变洛伦兹力正确")

    # 检查 8.5 - 运动电荷场
    E, B = moving_charge_fields(e, np.array([1e-10, 0, 0]), np.zeros(3))
    if E[0] <= 0:
        print("错误 8.5 正电荷在正 x 方向产生的电场应为正")
        all_passed = False
    else:
        print(f"通过 8.5 运动电荷场正确")

    # 检查 8.6 - Larmor辐射
    P = larmor_power(e, 1e15)
    if P <= 0:
        print("错误 8.6 Larmor辐射功率应为正值")
        all_passed = False
    else:
        print(f"通过 8.6 Larmor辐射正确 (P = {P:.2e} W)")

    if all_passed:
        print("\n所有测试通过！正在生成可视化图像...")
        try:
            plot_relativistic_em()
        except Exception as e:
            print(f"可视化生成失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("相对论电动力学 Relativistic Electrodynamics")
    print("=" * 50)
    verify()
