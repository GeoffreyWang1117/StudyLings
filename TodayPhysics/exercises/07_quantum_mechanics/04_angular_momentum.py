"""
角动量算符 Angular Momentum Operators
难度 Difficulty: ★★★★

物理背景 Physical Background:
--------------------------
角动量是量子力学中的核心概念，与系统的旋转对称性密切相关。
在经典力学中，角动量 L = r × p 是一个矢量。
在量子力学中，角动量成为算符，其分量满足特定的对易关系。

量子角动量的关键特性：
1. 角动量分量不能同时确定（不对易）
2. 只有 L² 和 L_z 可以同时测量（相容观测量）
3. 角动量量子化：l = 0, 1, 2, ...（整数）或 1/2, 3/2, ...（半整数）
4. 磁量子数：m = -l, -l+1, ..., l-1, l

学习目标 Learning Objectives:
--------------------------
1. 掌握角动量算符的矩阵表示（L_x, L_y, L_z, L_+, L_-）
2. 理解对易关系 [L_x, L_y] = i*hbar*L_z（及循环置换）
3. 验证 L² 的本征值为 hbar²l(l+1)
4. 理解升降算符的作用和不确定性关系
5. 熟悉球谐函数作为角动量本征态
6. 了解角动量耦合（两个角动量的合成）

关键公式 Key Formulas:
--------------------
- 对易关系: [L_x, L_y] = i*hbar*L_z, [L_y, L_z] = i*hbar*L_x, [L_z, L_x] = i*hbar*L_y
- L² 本征值: L²|l,m> = hbar²*l(l+1)|l,m>
- L_z 本征值: L_z|l,m> = hbar*m|l,m>
- 升降算符: L_±|l,m> = hbar*sqrt(l(l+1)-m(m±1))|l,m±1>
- 不确定性关系: Delta_L_x * Delta_L_y >= (hbar/2)|<L_z>|
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import sph_harm
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import hbar

# I AM NOT DONE

# =============================================================================
# 练习 1.1: 角动量算符的矩阵表示
# Exercise 1.1: Matrix Representation of Angular Momentum
# -----------------------------------------------------------------------------
# 物理背景：在有限维希尔伯特空间中，算符可以用矩阵表示
# 对于给定的 l，基底为 |l,m>，m = -l, -l+1, ..., l-1, l
# 共有 (2l+1) 个基矢，因此矩阵维度为 (2l+1) × (2l+1)
#
# 矩阵元计算：
# <l,m'|L_z|l,m> = hbar*m * delta_{m',m}（对角矩阵）
# <l,m'|L_+|l,m> = hbar*sqrt(l(l+1)-m(m+1)) * delta_{m',m+1}
# <l,m'|L_-|l,m> = hbar*sqrt(l(l+1)-m(m-1)) * delta_{m',m-1}
# =============================================================================
def Lz_matrix(l):
    """
    构建 L_z 算符的矩阵表示 Build matrix representation of L_z

    本征值方程: L_z|l,m> = hbar*m|l,m>

    参数 Parameters:
        l: 角量子数（整数或半整数）

    返回 Returns:
        Lz: (2l+1)×(2l+1) 对角矩阵

    矩阵结构：对角矩阵，对角元为 hbar*m，m从-l到+l
    例如 l=1 时：Lz = hbar * diag(-1, 0, 1)
    """
    dim = 2 * l + 1
    Lz = np.zeros((dim, dim), dtype=complex)

    # TODO: 构建 L_z 矩阵（对角矩阵）
    for i, m in enumerate(range(-l, l + 1)):
        Lz[i, i] = hbar * m

    return Lz


def Lplus_matrix(l):
    """
    构建升算符 L_+ = L_x + i*L_y 的矩阵表示

    作用规则: L_+|l,m> = hbar * sqrt(l(l+1) - m(m+1)) |l,m+1>

    物理意义：升算符将磁量子数 m 增加 1
    当 m = l 时，L_+|l,l> = 0（已是最高态）

    矩阵结构：上对角矩阵（次对角线上方）
    """
    dim = 2 * l + 1
    Lplus = np.zeros((dim, dim), dtype=complex)

    # TODO: 构建升算符矩阵
    # 注意：L_+|l,m> 得到 |l,m+1>，所以矩阵元在上对角位置
    for i, m in enumerate(range(-l, l + 1)):
        if m < l:  # m+1 必须 <= l
            coeff = hbar * np.sqrt(l * (l + 1) - m * (m + 1))
            Lplus[i + 1, i] = coeff  # |m+1><m| 位置

    return Lplus


def Lminus_matrix(l):
    """
    构建降算符 L_- = L_x - i*L_y 的矩阵表示

    作用规则: L_-|l,m> = hbar * sqrt(l(l+1) - m(m-1)) |l,m-1>

    物理意义：降算符将磁量子数 m 减少 1
    当 m = -l 时，L_-|l,-l> = 0（已是最低态）

    矩阵结构：下对角矩阵（次对角线下方）
    注意：L_- = (L_+)^dagger（厄米共轭）
    """
    dim = 2 * l + 1
    Lminus = np.zeros((dim, dim), dtype=complex)

    # TODO: 构建降算符矩阵
    for i, m in enumerate(range(-l, l + 1)):
        if m > -l:  # m-1 必须 >= -l
            coeff = hbar * np.sqrt(l * (l + 1) - m * (m - 1))
            Lminus[i - 1, i] = coeff  # |m-1><m| 位置

    return Lminus


def Lx_matrix(l):
    """
    构建 L_x 算符的矩阵表示

    公式: L_x = (L_+ + L_-) / 2

    这是从升降算符定义反推出来的
    L_x 是厄米算符，矩阵为实对称矩阵
    """
    Lplus = Lplus_matrix(l)
    Lminus = Lminus_matrix(l)
    return (Lplus + Lminus) / 2


def Ly_matrix(l):
    """
    构建 L_y 算符的矩阵表示

    公式: L_y = (L_+ - L_-) / (2i)

    L_y 是厄米算符，矩阵元为纯虚数
    """
    Lplus = Lplus_matrix(l)
    Lminus = Lminus_matrix(l)
    return (Lplus - Lminus) / (2j)


# =============================================================================
# 练习 1.2: 角动量平方算符
# Exercise 1.2: L-squared Operator
# -----------------------------------------------------------------------------
# 物理背景：L² 测量角动量的总大小（不涉及方向）
# L² 和任意 L_i 对易，因此可以同时测量
# 选择 L² 和 L_z 作为完备对易观测量集（CSCO）
#
# 重要恒等式：L² = L_+L_- + L_z² - hbar*L_z = L_-L_+ + L_z² + hbar*L_z
# =============================================================================
def L2_matrix(l):
    """
    构建角动量平方算符 L² 的矩阵表示

    公式: L² = L_x² + L_y² + L_z²

    本征值: L²|l,m> = hbar²*l(l+1)|l,m>

    注意：L² 对所有 m 给出相同的本征值 hbar²*l(l+1)
    因此 L² 在 |l,m> 基底下是单位矩阵乘以 hbar²*l(l+1)

    参数 Parameters:
        l: 角量子数

    返回 Returns:
        L2: (2l+1)×(2l+1) 矩阵（实际上正比于单位矩阵）
    """
    Lx = Lx_matrix(l)
    Ly = Ly_matrix(l)
    Lz = Lz_matrix(l)

    # TODO: 计算 L² = L_x² + L_y² + L_z²
    L2 = Lx @ Lx + Ly @ Ly + Lz @ Lz
    return L2


def verify_L2_eigenvalue(l):
    """
    验证 L² 的本征值为 hbar²*l(l+1)

    对于给定的 l，所有 (2l+1) 个本征值应该相同
    这体现了 L² 和 L_z 可以同时对角化

    返回 Returns:
        True 如果所有本征值都等于 hbar²*l(l+1)
    """
    L2 = L2_matrix(l)
    eigenvalues = np.linalg.eigvalsh(L2)  # 厄米矩阵本征值
    expected = hbar**2 * l * (l + 1)
    return np.allclose(eigenvalues, expected)


# =============================================================================
# 练习 1.3: 对易关系
# Exercise 1.3: Commutation Relations
# -----------------------------------------------------------------------------
# 物理背景：对易关系是量子力学的核心
#
# 角动量对易关系（称为 so(3) 李代数）：
# [L_x, L_y] = i*hbar*L_z
# [L_y, L_z] = i*hbar*L_x
# [L_z, L_x] = i*hbar*L_y
# 简记为: [L_i, L_j] = i*hbar*epsilon_{ijk}*L_k
#
# 物理意义：
# - 不对易意味着不能同时精确测量
# - [A, B] != 0 导致不确定性关系 Delta_A * Delta_B >= |<[A,B]>|/2
#
# 特别地：[L², L_i] = 0，所以 L² 和任一分量可同时测量
# =============================================================================
def commutator(A, B):
    """
    计算两个算符的对易子 Calculate commutator of two operators

    定义: [A, B] = AB - BA

    性质：
    - [A, B] = -[B, A]（反对称）
    - [A, BC] = [A,B]C + B[A,C]（莱布尼茨律）
    - [A, B]^dagger = -[A^dagger, B^dagger]
    """
    return A @ B - B @ A


def verify_commutation_Lx_Ly(l):
    """
    验证对易关系 [L_x, L_y] = i*hbar*L_z

    这是角动量对易关系中最重要的一个
    其他关系可通过循环置换得到

    返回 Returns:
        True 如果对易关系成立（在数值精度内）
    """
    Lx = Lx_matrix(l)
    Ly = Ly_matrix(l)
    Lz = Lz_matrix(l)

    # TODO: 计算对易子 [L_x, L_y] 并与 i*hbar*L_z 比较
    comm = commutator(Lx, Ly)
    expected = 1j * hbar * Lz
    return np.allclose(comm, expected)


def verify_commutation_L2_Lz(l):
    """
    验证 [L², L_z] = 0

    物理意义：L² 和 L_z 对易，因此它们是相容观测量
    可以找到同时是 L² 和 L_z 本征态的量子态
    这就是 |l, m> 态

    返回 Returns:
        True 如果对易子为零矩阵
    """
    L2 = L2_matrix(l)
    Lz = Lz_matrix(l)

    comm = commutator(L2, Lz)
    return np.allclose(comm, 0)


# =============================================================================
# 练习 1.4: 不确定性关系
# Exercise 1.4: Uncertainty Relations
# -----------------------------------------------------------------------------
# 物理背景：海森堡不确定性原理的一般形式
#
# 对于任意两个可观测量 A 和 B：
# Delta_A * Delta_B >= (1/2)|<[A, B]>|
#
# 对于角动量分量：
# Delta_L_x * Delta_L_y >= (hbar/2)|<L_z>|
#
# 特别地，对于 |l, m=0> 态：<L_z> = 0，不确定性关系变成 >= 0（平凡）
# 对于 |l, m=l> 态：<L_z> = hbar*l，不确定性关系非平凡
# =============================================================================
def expectation_value(A, state):
    """
    计算算符 A 在量子态 |state> 中的期望值

    公式: <A> = <state|A|state> = state^dagger * A * state

    参数 Parameters:
        A: 算符矩阵
        state: 量子态向量（列向量）

    返回 Returns:
        <A>: 期望值（实数，对于厄米算符）
    """
    return np.real(np.conj(state) @ A @ state)


def uncertainty(A, state):
    """
    计算算符 A 在量子态 |state> 中的不确定度

    公式: Delta_A = sqrt(<A²> - <A>²) = sqrt(方差)

    参数 Parameters:
        A: 算符矩阵
        state: 量子态向量

    返回 Returns:
        Delta_A: 不确定度（标准差）

    物理意义：测量结果的统计涨落
    """
    exp_A = expectation_value(A, state)
    exp_A2 = expectation_value(A @ A, state)
    return np.sqrt(exp_A2 - exp_A**2)


def verify_uncertainty_relation(l, m):
    """
    验证角动量的不确定性关系

    待验证: Delta_L_x * Delta_L_y >= (hbar/2)|<L_z>|

    参数 Parameters:
        l: 角量子数
        m: 磁量子数

    返回 Returns:
        True 如果不确定性关系成立

    对于 |l, m> 态，<L_z> = hbar*m
    当 m != 0 时，不确定性关系给出非平凡下界
    """
    Lx = Lx_matrix(l)
    Ly = Ly_matrix(l)
    Lz = Lz_matrix(l)

    # 构建 |l, m> 态向量
    dim = 2 * l + 1
    state = np.zeros(dim, dtype=complex)
    state[m + l] = 1  # |l, m> 对应数组索引 m+l

    # 计算不确定度
    delta_Lx = uncertainty(Lx, state)
    delta_Ly = uncertainty(Ly, state)
    exp_Lz = expectation_value(Lz, state)

    # 验证不等式
    lhs = delta_Lx * delta_Ly
    rhs = (hbar / 2) * abs(exp_Lz)

    return lhs >= rhs - 1e-10  # 允许数值误差


# =============================================================================
# 练习 1.5: 球谐函数
# Exercise 1.5: Spherical Harmonics
# -----------------------------------------------------------------------------
# 物理背景：球谐函数是球坐标中角度部分的本征函数
#
# Y_l^m(theta, phi) 是 L² 和 L_z 的共同本征函数：
# L² Y_l^m = hbar²*l(l+1) Y_l^m
# L_z Y_l^m = hbar*m Y_l^m
#
# 球谐函数的结构：
# Y_l^m(theta, phi) = N_{lm} * P_l^m(cos(theta)) * exp(i*m*phi)
# 其中 P_l^m 是缔合勒让德函数，N_{lm} 是归一化常数
#
# 正交归一性：
# integral Y_l^m* Y_l'^m' sin(theta) d(theta) d(phi) = delta_{ll'} delta_{mm'}
# =============================================================================
def spherical_harmonic(l, m, theta, phi):
    """
    计算球谐函数 Y_l^m(theta, phi)

    参数 Parameters:
        l: 角量子数（非负整数）
        m: 磁量子数（-l <= m <= l）
        theta: 极角（0 到 pi）
        phi: 方位角（0 到 2*pi）

    返回 Returns:
        Y_l^m: 球谐函数值（复数）

    注意：scipy.special.sph_harm 的参数顺序是 (m, l, phi, theta)
    与物理学惯例 (l, m, theta, phi) 不同
    """
    # scipy的sph_harm参数顺序是 (m, l, phi, theta)
    return sph_harm(m, l, phi, theta)


def probability_density_angular(l, m, theta, phi):
    """
    计算角向概率密度 |Y_l^m(theta, phi)|²

    物理意义：电子在 (theta, phi) 方向被发现的相对概率
    不同的 (l, m) 对应不同的角分布形状
    例如：s轨道(l=0)球对称，p轨道(l=1)有方向性
    """
    Y = spherical_harmonic(l, m, theta, phi)
    return np.abs(Y)**2


def verify_orthonormality(l1, m1, l2, m2, n_theta=50, n_phi=100):
    """
    验证球谐函数的正交归一性

    公式: integral Y_{l1}^{m1}* Y_{l2}^{m2} sin(theta) d(theta) d(phi)
          = delta_{l1,l2} * delta_{m1,m2}

    参数 Parameters:
        l1, m1: 第一个球谐函数的量子数
        l2, m2: 第二个球谐函数的量子数
        n_theta, n_phi: 数值积分的网格点数

    返回 Returns:
        True 如果正交归一性在数值误差范围内成立

    注意：sin(theta) 因子是球面面元 dOmega = sin(theta) d(theta) d(phi) 的一部分
    """
    theta = np.linspace(0, np.pi, n_theta)
    phi = np.linspace(0, 2 * np.pi, n_phi)
    dtheta = theta[1] - theta[0]
    dphi = phi[1] - phi[0]

    THETA, PHI = np.meshgrid(theta, phi, indexing='ij')

    Y1 = spherical_harmonic(l1, m1, THETA, PHI)
    Y2 = spherical_harmonic(l2, m2, THETA, PHI)

    # 被积函数：Y1* × Y2 × sin(theta)
    integrand = np.conj(Y1) * Y2 * np.sin(THETA)
    integral = np.sum(integrand) * dtheta * dphi

    expected = 1 if (l1 == l2 and m1 == m2) else 0
    return np.isclose(np.abs(integral), expected, atol=0.1)


# =============================================================================
# 练习 1.6: 轨道角动量和磁量子数
# Exercise 1.6: Orbital Angular Momentum and Magnetic Quantum Number
# -----------------------------------------------------------------------------
# 物理背景：角动量量子化是量子力学的核心特征
#
# 关键结论：
# 1. 角动量大小：|L| = hbar*sqrt(l(l+1))，不是 hbar*l！
# 2. z分量只能取离散值：L_z = hbar*m，m = -l,...,+l
# 3. 角动量不能完全沿z轴对齐（|L| > |L_z|_max = hbar*l）
#
# 与磁矩的关系：
# 运动电荷产生磁矩：mu = (q/2m)*L = -(e/2m_e)*L（电子）
# 这就是为什么 m 称为"磁"量子数——它决定磁矩在磁场中的能量
# =============================================================================
def angular_momentum_magnitude(l):
    """
    计算角动量大小 Calculate angular momentum magnitude

    公式: |L| = hbar * sqrt(l(l+1))

    参数 Parameters:
        l: 角量子数（非负整数）

    返回 Returns:
        |L|: 角动量大小 (J·s)

    注意：|L| > hbar*l，角动量不能完全沿任何方向对齐
    这是量子力学的固有特性，与不确定性原理相关
    """
    return hbar * np.sqrt(l * (l + 1))


def z_component_values(l):
    """
    返回 L_z 的所有可能测量值

    取值范围: L_z = hbar*m，其中 m = -l, -l+1, ..., l-1, l

    参数 Parameters:
        l: 角量子数

    返回 Returns:
        列表，包含 (2l+1) 个可能的 L_z 值

    例如 l=1 时：L_z 可取 -hbar, 0, +hbar（共3个值）
    """
    return [hbar * m for m in range(-l, l + 1)]


def magnetic_moment(l, m, g_l=1):
    """
    计算轨道磁矩的z分量 Calculate z-component of orbital magnetic moment

    公式: mu_z = -g_l * mu_B * m

    参数 Parameters:
        l: 角量子数（此处用于物理解释，公式中实际使用 m）
        m: 磁量子数
        g_l: 轨道g因子（对于纯轨道运动 g_l = 1）

    返回 Returns:
        mu_z: 磁矩z分量 (J/T = A·m²)

    其中 mu_B = e*hbar/(2m_e) ≈ 9.27×10^-24 J/T 是玻尔磁子
    负号来自电子带负电
    """
    from utils.constants import e, m_e
    mu_B = e * hbar / (2 * m_e)  # 玻尔磁子
    return -g_l * mu_B * m


# =============================================================================
# 练习 1.7: 角动量耦合
# Exercise 1.7: Angular Momentum Coupling
# -----------------------------------------------------------------------------
# 物理背景：两个角动量如何合成为总角动量
#
# 应用场景：
# 1. 轨道-自旋耦合（L-S耦合）：J = L + S
# 2. 两电子耦合：L_total = L_1 + L_2
# 3. 核自旋与电子角动量耦合
#
# 耦合规则（三角关系）：
# 若 l1 和 l2 耦合成 L，则 L 的可能值为：
# L = |l1-l2|, |l1-l2|+1, ..., l1+l2-1, l1+l2
# 共 (l1+l2) - |l1-l2| + 1 个可能值
#
# 态数守恒：耦合前后的总态数相等
# (2l1+1)(2l2+1) = sum_L (2L+1)
# =============================================================================
def coupled_angular_momentum_range(l1, l2):
    """
    计算两个角动量耦合后的可能总角动量值

    公式: L = |l1-l2|, |l1-l2|+1, ..., l1+l2

    参数 Parameters:
        l1, l2: 两个角量子数

    返回 Returns:
        列表，包含所有可能的总角量子数 L

    例如：l1=1, l2=2 → L = 1, 2, 3（共3个可能值）
    物理解释：两个矢量相加，结果的大小在 |l1-l2| 到 l1+l2 之间
    """
    L_min = abs(l1 - l2)
    L_max = l1 + l2
    return list(range(L_min, L_max + 1))


def total_states_count(l1, l2):
    """
    计算两个角动量系统的总态数

    公式: N = (2l1+1) × (2l2+1)

    参数 Parameters:
        l1, l2: 两个角量子数

    返回 Returns:
        总态数

    这等于非耦合基 |l1,m1;l2,m2> 的数目
    也等于耦合基 |L,M> 的数目：sum_{L=|l1-l2|}^{l1+l2} (2L+1)
    态数守恒体现了希尔伯特空间维度不变
    """
    return (2 * l1 + 1) * (2 * l2 + 1)


def clebsch_gordan_selection(l1, m1, l2, m2, L, M):
    """
    检查 Clebsch-Gordan 系数的选择定则

    Clebsch-Gordan 系数 <l1,m1;l2,m2|L,M> 非零的条件：
    1. M = m1 + m2（磁量子数守恒）
    2. |l1-l2| <= L <= l1+l2（三角关系）
    3. |M| <= L（磁量子数范围）

    参数 Parameters:
        l1, m1: 第一个角动量的量子数
        l2, m2: 第二个角动量的量子数
        L, M: 总角动量的量子数

    返回 Returns:
        True 如果 CG 系数可能非零
    """
    if M != m1 + m2:
        return False  # 磁量子数守恒
    if L < abs(l1 - l2) or L > l1 + l2:
        return False  # 三角不等式
    if abs(M) > L:
        return False  # M 范围限制
    return True


# =============================================================================
# 可视化
# =============================================================================
def plot_angular_momentum():
    """绘制角动量相关图"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # 1. 球谐函数 |Y_l^m|²
    ax1 = axes[0, 0]
    theta = np.linspace(0, np.pi, 100)
    phi = 0  # 固定phi

    for l in range(4):
        for m in range(0, l + 1):
            Y2 = probability_density_angular(l, m, theta, phi)
            ax1.plot(theta * 180 / np.pi, Y2, label=f'l={l}, m={m}')

    ax1.set_xlabel('theta (degrees)')
    ax1.set_ylabel('|Y_l^m|^2')
    ax1.set_title('球谐函数概率密度 (phi=0)')
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)

    # 2. 角动量大小 vs l
    ax2 = axes[0, 1]
    l_range = np.arange(0, 10)
    L_magnitude = [angular_momentum_magnitude(l) / hbar for l in l_range]
    L_classical = l_range  # 经典极限

    ax2.plot(l_range, L_magnitude, 'bo-', label='QM: sqrt(l(l+1))', linewidth=2)
    ax2.plot(l_range, L_classical, 'r--', label='Classical: l', linewidth=2)
    ax2.set_xlabel('l')
    ax2.set_ylabel('|L| / hbar')
    ax2.set_title('角动量大小')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. L_z 的可能取值
    ax3 = axes[1, 0]
    for l in range(1, 5):
        Lz_values = z_component_values(l)
        ax3.scatter([l] * len(Lz_values), np.array(Lz_values) / hbar,
                   s=100, label=f'l={l}')

    ax3.set_xlabel('l')
    ax3.set_ylabel('L_z / hbar')
    ax3.set_title('L_z 量子化')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 3D 球谐函数可视化 (l=2, m=0)
    ax4 = axes[1, 1]
    ax4 = fig.add_subplot(2, 2, 4, projection='3d')

    l, m = 2, 0
    theta_3d = np.linspace(0, np.pi, 50)
    phi_3d = np.linspace(0, 2 * np.pi, 50)
    THETA, PHI = np.meshgrid(theta_3d, phi_3d)

    R = np.abs(spherical_harmonic(l, m, THETA, PHI))

    X = R * np.sin(THETA) * np.cos(PHI)
    Y = R * np.sin(THETA) * np.sin(PHI)
    Z = R * np.cos(THETA)

    ax4.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
    ax4.set_xlabel('X')
    ax4.set_ylabel('Y')
    ax4.set_zlabel('Z')
    ax4.set_title(f'|Y_{l}^{m}| 3D visualization')

    plt.tight_layout()
    plt.savefig('angular_momentum.png', dpi=150)
    print("图像已保存为 angular_momentum.png")
    plt.show()


# =============================================================================
# 验证函数
# Verification Function
# =============================================================================
def verify():
    """验证所有练习的正确性 Verify all exercises"""
    all_passed = True

    # 检查 1.1 - 角动量矩阵表示
    Lz = Lz_matrix(1)
    expected_diag = [-hbar, 0, hbar]
    if not np.allclose(np.diag(Lz), expected_diag):
        print("错误 1.1: L_z 矩阵构建错误")
        print("  l=1 时对角元应为 [-hbar, 0, hbar]")
        all_passed = False
    else:
        print("通过 1.1: 角动量矩阵表示正确")

    # 检查 1.2 - L² 本征值
    for l in [1, 2, 3]:
        if not verify_L2_eigenvalue(l):
            print(f"错误 1.2: L^2 本征值错误 (l={l})")
            print(f"  期望: hbar^2 * {l}*({l}+1) = hbar^2 * {l*(l+1)}")
            all_passed = False
            break
    else:
        print("通过 1.2: L^2 本征值正确（对 l=1,2,3 验证通过）")

    # 检查 1.3 - 对易关系
    if not verify_commutation_Lx_Ly(1):
        print("错误 1.3: 对易关系 [L_x, L_y] = i*hbar*L_z 验证失败")
        all_passed = False
    elif not verify_commutation_L2_Lz(2):
        print("错误 1.3: 对易关系 [L^2, L_z] = 0 验证失败")
        all_passed = False
    else:
        print("通过 1.3: 对易关系正确")

    # 检查 1.4 - 不确定性关系
    if not verify_uncertainty_relation(2, 1):
        print("错误 1.4: 不确定性关系 Delta_Lx * Delta_Ly >= (hbar/2)|<Lz>| 验证失败")
        all_passed = False
    else:
        print("通过 1.4: 不确定性关系正确")

    # 检查 1.5 - 球谐函数正交归一性
    if not verify_orthonormality(1, 0, 1, 0):
        print("错误 1.5: 球谐函数归一化条件 integral |Y|^2 = 1 不成立")
        all_passed = False
    elif not verify_orthonormality(1, 0, 2, 0):
        print("错误 1.5: 球谐函数正交性条件不成立（不同 l 应正交）")
        all_passed = False
    else:
        print("通过 1.5: 球谐函数正交归一性正确")

    # 检查 1.6 - 角动量大小
    L_l2 = angular_momentum_magnitude(2)
    expected_L = hbar * np.sqrt(6)
    if not np.isclose(L_l2, expected_L):
        print("错误 1.6: 角动量大小计算错误")
        print(f"  l=2 时 |L| 应为 sqrt(6)*hbar")
        all_passed = False
    else:
        print(f"通过 1.6: 角动量大小正确 (l=2: |L| = sqrt(6)*hbar)")

    # 检查 1.7 - 角动量耦合
    L_range = coupled_angular_momentum_range(1, 2)
    if L_range != [1, 2, 3]:
        print("错误 1.7: 角动量耦合计算错误")
        print("  l1=1, l2=2 耦合后 L 应取 1, 2, 3")
        all_passed = False
    else:
        n_states = total_states_count(1, 2)
        print(f"通过 1.7: 角动量耦合正确 (l1=1, l2=2: L={L_range}, 总态数={n_states})")

    if all_passed:
        print("\n所有测试通过！正在生成可视化...")
        try:
            plot_angular_momentum()
        except Exception as e:
            print(f"可视化生成失败: {e}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("角动量算符 Angular Momentum Operators")
    print("=" * 50)
    verify()
