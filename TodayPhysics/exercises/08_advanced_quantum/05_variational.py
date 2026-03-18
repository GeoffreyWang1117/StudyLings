"""
变分法 Variational Method
难度 Difficulty: ★★★★

学习目标 Learning Objectives:
- 理解变分原理的物理意义和数学基础
- 掌握试探波函数的构造技巧
- 应用变分法求解基态能量（精确或近似）
- 了解线性变分法和Rayleigh-Ritz方法

物理背景 Physical Background:
1. 变分原理: 任意试探波函数的能量期望值都是基态能量的上界
   E[ψ] = ⟨ψ|H|ψ⟩/⟨ψ|ψ⟩ ≥ E₀
2. 这是量子力学最强大的近似方法之一
3. 试探波函数的选择体现物理直觉，参数通过优化确定

关键公式 Key Formulas:
- 能量泛函: E[ψ] = ⟨ψ|H|ψ⟩/⟨ψ|ψ⟩
- 变分条件: δE[ψ] = 0 或 ∂E/∂α = 0（对所有参数α）
- 线性变分: |ψ⟩ = Σᵢcᵢ|φᵢ⟩ → 广义本征值问题 Hc = ESc
- Rayleigh商: R[ψ] = ⟨ψ|H|ψ⟩/⟨ψ|ψ⟩

应用实例:
- 谐振子: 高斯试探函数给出精确解
- 氢原子: 指数试探函数给出精确基态
- 氦原子: 有效核电荷法给出约98%精度
- 分子: 构成量子化学的基础
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar, minimize
from scipy.integrate import quad
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import hbar, m_e, e, epsilon_0, a_0

# I AM NOT DONE

# =============================================================================
# 练习 1.1: 能量泛函 Energy Functional
#
# 物理背景:
# 能量泛函是变分法的核心，将波函数映射到能量值
# 对于哈密顿量 H = T + V（动能+势能）:
#   E[ψ] = ⟨ψ|H|ψ⟩/⟨ψ|ψ⟩ = (⟨T⟩ + ⟨V⟩)/⟨ψ|ψ⟩
#
# 变分原理保证: E[ψ] ≥ E₀（基态能量）
# 等号成立当且仅当 ψ = ψ₀（基态波函数）
# =============================================================================
def energy_functional(psi_func, V_func, x_range, n_points=1000):
    """
    计算能量泛函 Energy functional: E[ψ] = ⟨ψ|H|ψ⟩/⟨ψ|ψ⟩

    参数 Parameters:
        psi_func: 试探波函数 ψ(x)
        V_func: 势能函数 V(x)
        x_range: [x_min, x_max] 积分区间
        n_points: 数值积分点数

    返回 Returns:
        E: 能量期望值，单位 J

    哈密顿量: H = -ℏ²/(2m) d²/dx² + V(x)
    使用分部积分将动能转换为 ⟨dψ/dx|dψ/dx⟩ 形式
    """
    x = np.linspace(x_range[0], x_range[1], n_points)
    dx = x[1] - x[0]

    psi = psi_func(x)
    V = V_func(x)

    # 归一化积分 ⟨ψ|ψ⟩
    norm = np.sum(np.abs(psi)**2) * dx

    # 动能项: ⟨T⟩ = -(ℏ²/2m)⟨ψ|d²/dx²|ψ⟩
    # 分部积分后: = (ℏ²/2m)∫|dψ/dx|² dx（假设边界为零）
    dpsi_dx = np.gradient(psi, dx)
    kinetic = hbar**2 / (2 * m_e) * np.sum(np.abs(dpsi_dx)**2) * dx

    # 势能项: ⟨V⟩ = ∫|ψ|² V(x) dx
    potential = np.sum(np.abs(psi)**2 * V) * dx

    # TODO: 计算能量泛函 E = (⟨T⟩ + ⟨V⟩)/⟨ψ|ψ⟩
    E = (kinetic + potential) / norm
    return E


def normalize_wavefunction(psi_func, x_range, n_points=1000):
    """
    归一化波函数 Normalize wavefunction

    使归一化后的波函数满足 ∫|ψ|² dx = 1
    """
    x = np.linspace(x_range[0], x_range[1], n_points)
    dx = x[1] - x[0]
    psi = psi_func(x)
    norm = np.sqrt(np.sum(np.abs(psi)**2) * dx)
    return lambda x: psi_func(x) / norm


# =============================================================================
# 练习 1.2: 谐振子基态变分 Harmonic Oscillator Variational
#
# 物理背景:
# 谐振子是变分法的完美例子——高斯试探函数恰好给出精确解
#
# 试探波函数: ψ(x) = exp(-αx²)
# 势能: V(x) = mω²x²/2
#
# 解析计算:
# ⟨T⟩ = ℏ²α/2m, ⟨V⟩ = mω²/8α
# E(α) = ℏ²α/2m + mω²/8α
# 最优条件 dE/dα = 0 → α_opt = mω/2ℏ → E₀ = ℏω/2
# =============================================================================
def harmonic_oscillator_trial(x, alpha):
    """
    谐振子高斯试探波函数 Gaussian trial wavefunction

    ψ(x) = exp(-αx²)（未归一化）

    参数 Parameters:
        x: 位置坐标数组
        alpha: 变分参数，单位 m⁻²

    物理意义: α 控制波函数的宽度，α越大波函数越窄
    """
    return np.exp(-alpha * x**2)


def harmonic_oscillator_energy(alpha, omega):
    """
    计算谐振子试探波函数的能量 Harmonic oscillator variational energy

    参数 Parameters:
        alpha: 变分参数，单位 m⁻²
        omega: 谐振子角频率，单位 rad/s

    返回 Returns:
        E: 能量，单位 J

    解析公式: E(α) = ℏ²α/(2m) + mω²/(8α)
    - 第一项是动能，随α增大（波函数变窄，动量不确定性增大）
    - 第二项是势能，随α减小（波函数变宽，更多概率在高势能区）
    """
    # TODO: 计算动能和势能期望值
    kinetic = hbar**2 * alpha / (2 * m_e)       # ⟨T⟩ = ℏ²α/2m
    potential = m_e * omega**2 / (8 * alpha)    # ⟨V⟩ = mω²/8α
    return kinetic + potential


def optimal_alpha_harmonic(omega):
    """
    求解谐振子最优变分参数 Optimal variational parameter

    由 dE/dα = 0 解得:
    ℏ²/2m - mω²/8α² = 0
    α_opt = mω/(2ℏ)

    这正是精确基态波函数的参数！
    """
    return m_e * omega / (2 * hbar)


def variational_energy_harmonic(omega):
    """
    谐振子变分基态能量 Variational ground state energy

    将α_opt代入E(α)得到:
    E₀ = ℏω/2

    这是精确的基态能量！说明高斯函数形式正确
    """
    alpha_opt = optimal_alpha_harmonic(omega)
    return harmonic_oscillator_energy(alpha_opt, omega)


# =============================================================================
# 练习 1.3: 氢原子基态变分 Hydrogen Atom Variational
#
# 物理背景:
# 氢原子是变分法的另一个精确可解例子
#
# 试探波函数: ψ(r) = exp(-ζr)
# ζ（zeta）是有效核电荷参数（以1/a₀为单位）
#
# 势能: V(r) = -e²/(4πε₀r)
#
# 解析结果（原子单位）:
# ⟨T⟩ = ζ²/2, ⟨V⟩ = -ζ
# E(ζ) = (ζ²/2 - ζ) E_H
# 最优条件: ζ_opt = 1 → E₀ = -E_H/2 = -13.6 eV
# =============================================================================
def hydrogen_trial_radial(r, zeta):
    """
    氢原子试探波函数（径向部分）Hydrogen trial wavefunction

    ψ(r) = exp(-ζr)（未归一化）

    参数 Parameters:
        r: 径向坐标
        zeta: 有效核电荷参数，单位 a₀⁻¹

    物理意义: ζ 控制电子云的"收缩程度"
    ζ > 1: 电子更靠近核（屏蔽效应小）
    ζ < 1: 电子更远离核（屏蔽效应大）
    """
    return np.exp(-zeta * r)


def hydrogen_energy_variational(zeta):
    """
    计算氢原子变分能量 Hydrogen variational energy

    参数 Parameters:
        zeta: 有效核电荷参数

    返回 Returns:
        E: 能量，单位 J

    公式（原子单位）: E(ζ) = (ζ²/2 - ζ) E_H
    其中 E_H = e²/(4πε₀a₀) ≈ 27.2 eV（哈特里能量）

    物理解释:
    - ζ²/2: 动能项（ζ增大，波函数收缩，动能增加）
    - -ζ: 势能项（ζ增大，更靠近核，势能更负）
    """
    E_H = e**2 / (4 * np.pi * epsilon_0 * a_0)  # 1 Hartree

    # TODO: 计算变分能量
    # 动能期望值: ⟨T⟩ = ζ²/2 × E_H
    # 势能期望值: ⟨V⟩ = -ζ × E_H
    E = (zeta**2 / 2 - zeta) * E_H
    return E


def optimal_zeta_hydrogen():
    """
    求解氢原子最优变分参数 Optimal zeta for hydrogen

    由 dE/dζ = 0 解得: ζ - 1 = 0
    ζ_opt = 1（以a₀⁻¹为单位）

    这说明试探函数的形式是正确的！
    """
    result = minimize_scalar(hydrogen_energy_variational, bounds=(0.1, 3))
    return result.x


def hydrogen_ground_state_energy():
    """
    氢原子基态能量精确值 Exact hydrogen ground state energy

    E₀ = -E_H/2 = -13.6 eV = -1 Rydberg
    """
    return -13.6 * e


# =============================================================================
# 练习 1.4: 氦原子变分 Helium Atom Variational
#
# 物理背景:
# 氦原子是最简单的多电子原子，无法精确求解
# 变分法给出很好的近似（约98%精度）
#
# 简单试探波函数: ψ(r₁,r₂) = exp(-ζ(r₁+r₂))
# 物理意义: 两个电子独立地处于"有效核电荷"ζ的氢型轨道
#
# 能量组成（原子单位）:
# - 动能: 2 × ζ²/2 = ζ²
# - 电子-核: 2 × (-Zζ) = -4ζ（Z=2）
# - 电子-电子排斥: 5ζ/8（通过积分计算）
# =============================================================================
def helium_energy_simple(zeta):
    """
    计算氦原子简单变分能量 Helium variational energy

    试探波函数: ψ(r₁,r₂) = exp(-ζ(r₁+r₂))
    忽略电子关联，假设两电子独立

    参数 Parameters:
        zeta: 有效核电荷参数

    返回 Returns:
        E: 总能量，单位 J

    公式（原子单位）: E(ζ) = ζ² - 2Zζ + 5ζ/8
    其中 Z=2 是氦核电荷

    物理解释:
    - ζ < Z: 电子间排斥"屏蔽"了核电荷
    - 最优 ζ_opt = Z - 5/16 = 27/16 ≈ 1.69
    """
    E_H = e**2 / (4 * np.pi * epsilon_0 * a_0)  # 1 Hartree
    Z = 2

    # 动能项: 两个电子各贡献 ζ²/2
    kinetic = zeta**2

    # 电子-核相互作用: 两个电子各贡献 -Zζ
    electron_nuclear = -2 * Z * zeta

    # 电子-电子排斥: ⟨1/r₁₂⟩ = 5ζ/8（通过6维积分得到）
    electron_electron = 5 * zeta / 8

    # TODO: 计算总能量
    E = (kinetic + electron_nuclear + electron_electron) * E_H
    return E


def optimal_zeta_helium():
    """
    求解氦原子最优变分参数 Optimal zeta for helium

    由 dE/dζ = 0 解得:
    2ζ - 4 + 5/8 = 0
    ζ_opt = 2 - 5/16 = 27/16 ≈ 1.6875

    物理意义: 有效核电荷小于实际核电荷（屏蔽效应）
    """
    result = minimize_scalar(helium_energy_simple, bounds=(1, 3))
    return result.x


def helium_ground_state_experimental():
    """
    氦原子基态能量实验值 Experimental helium ground state

    E₀ = -79.0 eV（两个电子的总电离能）
    = -24.6 eV（第一电离能）- 54.4 eV（第二电离能）

    简单变分结果约 -77.5 eV，误差约2%
    """
    return -79.0 * e


# =============================================================================
# 练习 1.5: 线性变分法 Linear Variational Method
#
# 物理背景:
# 线性变分法将试探波函数写成基函数的线性组合
# |ψ⟩ = Σᵢ cᵢ|φᵢ⟩
#
# 变分条件 ∂E/∂cᵢ = 0 导出广义本征值问题:
# Hc = ESc
# 其中 H_ij = ⟨φᵢ|H|φⱼ⟩, S_ij = ⟨φᵢ|φⱼ⟩
#
# 优点:
# - 线性问题，有系统的求解方法
# - 增加基函数可系统改进结果
# - 是量子化学和固体物理的基础
# =============================================================================
def linear_variational_matrix(H_matrix, S_matrix):
    """
    求解线性变分问题 Solve linear variational problem

    参数 Parameters:
        H_matrix: 哈密顿量矩阵 H_ij = ⟨φᵢ|H|φⱼ⟩
        S_matrix: 重叠矩阵 S_ij = ⟨φᵢ|φⱼ⟩

    返回 Returns:
        eigenvalues: 能量本征值（从小到大排序）
        eigenvectors: 对应的系数向量

    求解广义本征值问题: Hc = ESc
    最小本征值是基态能量上界
    """
    from scipy.linalg import eigh

    # TODO: 求解广义本征值问题
    eigenvalues, eigenvectors = eigh(H_matrix, S_matrix)
    return eigenvalues, eigenvectors


def build_hamiltonian_matrix(basis_funcs, H_operator, x_range, n_points=1000):
    """
    构建哈密顿量矩阵 Build Hamiltonian matrix

    参数 Parameters:
        basis_funcs: 基函数列表 [φ₁, φ₂, ...]
        H_operator: 哈密顿量算符函数
        x_range: 积分区间
        n_points: 积分点数

    返回 Returns:
        H: 哈密顿量矩阵（厄米矩阵）

    矩阵元: H_ij = ⟨φᵢ|H|φⱼ⟩ = ∫φᵢ*(x) Hφⱼ(x) dx
    """
    n_basis = len(basis_funcs)
    H = np.zeros((n_basis, n_basis))

    x = np.linspace(x_range[0], x_range[1], n_points)
    dx = x[1] - x[0]

    for i in range(n_basis):
        for j in range(n_basis):
            phi_i = basis_funcs[i](x)
            H_phi_j = H_operator(basis_funcs[j], x, dx)
            H[i, j] = np.sum(np.conj(phi_i) * H_phi_j) * dx

    return H


def build_overlap_matrix(basis_funcs, x_range, n_points=1000):
    """
    构建重叠矩阵 Build overlap matrix

    参数 Parameters:
        basis_funcs: 基函数列表
        x_range: 积分区间
        n_points: 积分点数

    返回 Returns:
        S: 重叠矩阵

    矩阵元: S_ij = ⟨φᵢ|φⱼ⟩ = ∫φᵢ*(x) φⱼ(x) dx
    若基正交，则 S = I（单位矩阵）
    """
    n_basis = len(basis_funcs)
    S = np.zeros((n_basis, n_basis))

    x = np.linspace(x_range[0], x_range[1], n_points)
    dx = x[1] - x[0]

    for i in range(n_basis):
        for j in range(n_basis):
            phi_i = basis_funcs[i](x)
            phi_j = basis_funcs[j](x)
            S[i, j] = np.sum(np.conj(phi_i) * phi_j) * dx

    return S


# =============================================================================
# 练习 1.6: 双井势变分 Double Well Potential Variational
#
# 物理背景:
# 双势阱是量子隧穿的经典模型
# 势能: V(x) = V₀((x/a)² - 1)² 有两个极小值在 x = ±a
#
# 试探波函数:
# 对称态（基态）: ψ_s = φ_L + φ_R
# 反对称态（第一激发态）: ψ_a = φ_L - φ_R
# 其中 φ_L,R 是定域在左/右井的高斯函数
#
# 能级分裂: ΔE = E_a - E_s ∝ exp(-S/ℏ)
# S是势垒下的作用量（隧穿抑制因子）
# =============================================================================
def double_well_potential(x, V0, a):
    """
    双势阱势能 Double well potential

    V(x) = V₀((x/a)² - 1)²

    参数 Parameters:
        x: 位置坐标
        V0: 势垒高度
        a: 势阱位置参数

    势阱位于 x = ±a，势垒在 x = 0，高度为 V₀
    """
    return V0 * ((x / a)**2 - 1)**2


def double_well_trial(x, alpha, c):
    """
    双势阱试探波函数 Double well trial wavefunction

    ψ(x) = exp(-α(x-a)²) + c·exp(-α(x+a)²)

    参数 Parameters:
        x: 位置坐标
        alpha: 高斯宽度参数
        c: 对称性参数
           c = +1: 对称态（基态）
           c = -1: 反对称态（第一激发态）

    物理意义: 两个定域高斯函数的叠加
    """
    return np.exp(-alpha * (x - 1)**2) + c * np.exp(-alpha * (x + 1)**2)


def double_well_energy_variational(params, V0, a, x_range, c=1):
    """
    计算双势阱变分能量 Double well variational energy

    参数 Parameters:
        params: [alpha] 变分参数列表
        V0: 势垒高度
        a: 势阱位置
        x_range: 积分区间
        c: 对称性 (+1对称，-1反对称)

    返回 Returns:
        E: 能量期望值

    通过最小化此函数确定最优α
    """
    alpha = params[0]

    def psi(x):
        return double_well_trial(x, alpha, c)

    def V(x):
        return double_well_potential(x, V0, a)

    return energy_functional(psi, V, x_range)


# =============================================================================
# 练习 1.7: Rayleigh-Ritz 原理 Rayleigh-Ritz Principle
#
# 物理背景:
# Rayleigh-Ritz原理是变分法的数学基础
#
# Rayleigh商: R[ψ] = ⟨ψ|H|ψ⟩/⟨ψ|ψ⟩
# 定理: R[ψ] ≥ E₀，等号成立当且仅当 ψ = ψ₀
#
# 推广:
# - 若ψ与ψ₀正交，则 R[ψ] ≥ E₁（第一激发态能量）
# - 这是计算激发态能量的基础
# =============================================================================
def rayleigh_quotient(psi, H_psi, x, dx):
    """
    计算Rayleigh商 Rayleigh quotient

    参数 Parameters:
        psi: 波函数数组
        H_psi: H作用于ψ的结果
        x: 坐标数组
        dx: 积分步长

    返回 Returns:
        R: Rayleigh商 = ⟨ψ|H|ψ⟩/⟨ψ|ψ⟩

    这是能量泛函的另一种表达方式
    """
    numerator = np.sum(np.conj(psi) * H_psi) * dx
    denominator = np.sum(np.abs(psi)**2) * dx
    return np.real(numerator / denominator)


def verify_variational_bound(E_var, E_exact):
    """
    验证变分原理上界 Verify variational upper bound

    变分原理保证: E_var ≥ E_exact
    任何试探波函数给出的能量都不低于真实基态能量
    """
    return E_var >= E_exact - 1e-10  # 允许数值误差


def relative_error(E_var, E_exact):
    """
    计算变分能量的相对误差 Relative error

    误差 = |E_var - E_exact| / |E_exact|

    典型精度:
    - 好的试探函数: 误差 < 1%
    - 简单氦原子变分: 约 2%
    - 高精度计算: < 0.01%
    """
    return abs((E_var - E_exact) / E_exact)


def improve_trial_function(psi_func, H_operator, x_range, n_iterations=5):
    """
    通过迭代改进试探波函数 Improve trial function iteratively

    概念演示: 实际实现需要更复杂的算法如:
    - 虚时间传播
    - 扩散Monte Carlo
    - 自洽场方法

    这里仅返回原始函数
    """
    # 这里只返回原始函数，实际实现需要更复杂的算法
    return psi_func


# =============================================================================
# 可视化 Visualization
# 绘制变分能量曲线、最优参数等图像
# =============================================================================
def plot_variational():
    """绘制变分法相关图像"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # 1. 谐振子能量 vs 变分参数
    ax1 = axes[0, 0]
    omega = 1e15  # rad/s
    alpha_range = np.linspace(0.1, 5, 100) * m_e * omega / (2 * hbar)
    E_values = [harmonic_oscillator_energy(alpha, omega) for alpha in alpha_range]
    E_exact = 0.5 * hbar * omega

    alpha_opt = optimal_alpha_harmonic(omega)
    E_opt = harmonic_oscillator_energy(alpha_opt, omega)

    ax1.plot(alpha_range / (m_e * omega / (2 * hbar)),
             np.array(E_values) / (hbar * omega), 'b-', linewidth=2)
    ax1.axhline(y=0.5, color='r', linestyle='--', label='Exact E_0')
    ax1.scatter([1], [E_opt / (hbar * omega)], s=100, c='g', marker='o',
               label='Optimum', zorder=5)
    ax1.set_xlabel('alpha / alpha_opt')
    ax1.set_ylabel('E / (hbar*omega)')
    ax1.set_title('谐振子变分能量')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 2)

    # 2. 氢原子能量 vs 变分参数
    ax2 = axes[0, 1]
    zeta_range = np.linspace(0.3, 2, 100)
    E_H_values = [hydrogen_energy_variational(zeta) / e for zeta in zeta_range]

    zeta_opt = optimal_zeta_hydrogen()
    E_H_opt = hydrogen_energy_variational(zeta_opt) / e

    ax2.plot(zeta_range, E_H_values, 'b-', linewidth=2)
    ax2.axhline(y=-13.6, color='r', linestyle='--', label='Exact E_0')
    ax2.scatter([zeta_opt], [E_H_opt], s=100, c='g', marker='o',
               label='Optimum', zorder=5)
    ax2.set_xlabel('zeta (1/a_0)')
    ax2.set_ylabel('E (eV)')
    ax2.set_title('氢原子变分能量')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 氦原子能量 vs 变分参数
    ax3 = axes[1, 0]
    zeta_He_range = np.linspace(1, 2.5, 100)
    E_He_values = [helium_energy_simple(zeta) / e for zeta in zeta_He_range]

    zeta_He_opt = optimal_zeta_helium()
    E_He_opt = helium_energy_simple(zeta_He_opt) / e

    ax3.plot(zeta_He_range, E_He_values, 'b-', linewidth=2)
    ax3.axhline(y=-79.0, color='r', linestyle='--', label='Experimental')
    ax3.scatter([zeta_He_opt], [E_He_opt], s=100, c='g', marker='o',
               label=f'Optimum (zeta={zeta_He_opt:.2f})', zorder=5)
    ax3.set_xlabel('zeta')
    ax3.set_ylabel('E (eV)')
    ax3.set_title('氦原子变分能量 (简单变分)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 双势阱波函数
    ax4 = axes[1, 1]
    V0 = 1 * e
    a = 1 * a_0
    x = np.linspace(-3 * a, 3 * a, 200)

    V = double_well_potential(x, V0, a)
    ax4.plot(x / a_0, V / e, 'k-', linewidth=2, label='V(x)')

    # 试探波函数（任意alpha）
    alpha = 1 / a_0**2
    psi_sym = double_well_trial(x, alpha, 1)
    psi_antisym = double_well_trial(x, alpha, -1)

    # 归一化并缩放显示
    psi_sym /= np.max(np.abs(psi_sym))
    psi_antisym /= np.max(np.abs(psi_antisym))

    ax4.plot(x / a_0, psi_sym * 0.5 + 0.2, 'b-', linewidth=2, label='Symmetric')
    ax4.plot(x / a_0, psi_antisym * 0.5 + 0.6, 'r-', linewidth=2, label='Antisymmetric')
    ax4.set_xlabel('x / a_0')
    ax4.set_ylabel('V (eV), psi (arb.)')
    ax4.set_title('双势阱和试探波函数')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('variational.png', dpi=150)
    print("图像已保存为 variational.png")
    plt.show()


# =============================================================================
# 验证函数 Verification
# =============================================================================
def verify():
    """验证所有练习的正确性 Verify all exercises"""
    all_passed = True

    # 检查 1.2: 谐振子变分
    omega = 1e15
    E_var = variational_energy_harmonic(omega)
    E_exact = 0.5 * hbar * omega
    if not np.isclose(E_var, E_exact, rtol=0.001):
        print(f"错误 1.2: 谐振子变分能量与精确值不符 ({E_var/E_exact:.4f} × E_exact)")
        all_passed = False
    else:
        print(f"通过 1.2: 谐振子变分正确 (E = E_exact = ℏω/2)")

    # 检查 1.3: 氢原子变分
    zeta_opt = optimal_zeta_hydrogen()
    E_H_var = hydrogen_energy_variational(zeta_opt)
    E_H_exact = -13.6 * e
    if not np.isclose(zeta_opt, 1, rtol=0.01):
        print(f"错误 1.3: 氢原子最优参数应为1，得到 ζ={zeta_opt:.3f}")
        all_passed = False
    elif not np.isclose(E_H_var, E_H_exact, rtol=0.01):
        print(f"错误 1.3: 氢原子变分能量不正确")
        all_passed = False
    else:
        print(f"通过 1.3: 氢原子变分正确 (ζ_opt={zeta_opt:.2f}, E={E_H_var/e:.2f} eV)")

    # 检查 1.4: 氦原子变分
    zeta_He = optimal_zeta_helium()
    E_He_var = helium_energy_simple(zeta_He)
    E_He_exp = helium_ground_state_experimental()

    if not verify_variational_bound(E_He_var, E_He_exp):
        print("错误 1.4: 氦原子变分能量低于实验值，违反变分原理")
        all_passed = False
    else:
        error = relative_error(E_He_var, E_He_exp)
        print(f"通过 1.4: 氦原子变分正确 (E_var={E_He_var/e:.1f} eV，相对误差={error*100:.1f}%)")

    # 检查 1.5: 线性变分
    H_test = np.array([[1, 0.1], [0.1, 2]])
    S_test = np.eye(2)
    eigenvalues, _ = linear_variational_matrix(H_test, S_test)
    E_0 = eigenvalues[0]
    if E_0 > 1:  # 应小于最小对角元
        print("错误 1.5: 线性变分基态能量应小于最小对角元")
        all_passed = False
    else:
        print(f"通过 1.5: 线性变分正确 (E₀ = {E_0:.4f})")

    # 检查 1.6: 双势阱变分
    V0 = 0.1 * e
    a = 1 * a_0
    x_range = [-5 * a, 5 * a]
    result = minimize(double_well_energy_variational, [1/a_0**2],
                     args=(V0, a, x_range), method='Nelder-Mead')
    if not result.success:
        print("错误 1.6: 双势阱参数优化失败")
        all_passed = False
    else:
        E_dw = result.fun
        print(f"通过 1.6: 双势阱变分正确 (E₀ ≈ {E_dw/e:.4f} eV)")

    # 检查 1.7: 变分上界
    if not verify_variational_bound(E_var, E_exact):
        print("错误 1.7: 变分原理验证失败，E_var 应 ≥ E_exact")
        all_passed = False
    else:
        print("通过 1.7: 变分上界正确 (E_var ≥ E_exact)")

    if all_passed:
        print("\n所有测试通过！")
        try:
            plot_variational()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("变分法 Variational Method")
    print("=" * 50)
    verify()
