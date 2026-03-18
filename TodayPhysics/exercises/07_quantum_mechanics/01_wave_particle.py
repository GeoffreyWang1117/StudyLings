"""
波粒二象性与薛定谔方程 Wave-Particle Duality and Schrödinger Equation
难度 Difficulty: ★★★★

物理背景 Physical Background:
--------------------------
量子力学是描述微观世界的基本理论。1924年德布罗意提出物质波假说，
认为所有物质都具有波动性，其波长 λ = h/p（h为普朗克常数，p为动量）。
1926年薛定谔建立了描述量子系统演化的波动方程：
    含时方程: iℏ∂ψ/∂t = Ĥψ （描述量子态随时间的演化）
    定态方程: Ĥψ = Eψ （求解能量本征值和本征态）

学习目标 Learning Objectives:
--------------------------
1. 理解德布罗意波长的物理意义，掌握波长与动量/能量的关系
2. 理解波函数的概率诠释，掌握归一化条件 ∫|ψ|²dx = 1
3. 掌握一维无限深势阱的解析解（能级公式和波函数）
4. 理解量子谐振子的能级量子化和零点能概念
5. 学习有限差分法数值求解薛定谔方程
6. 掌握期望值和不确定度的计算方法

关键公式 Key Formulas:
--------------------
- 德布罗意波长: λ = h/p = h/√(2mE)
- 无限深势阱能级: E_n = n²π²ℏ²/(2mL²)，n = 1,2,3,...
- 谐振子能级: E_n = (n + 1/2)ℏω，n = 0,1,2,...（注意零点能 E_0 = ℏω/2）
- 期望值: <A> = ∫ψ*Âψ dx
- 不确定度: ΔA = √(<A²> - <A>²)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import h, hbar, m_e, eV, c

# I AM NOT DONE

# =============================================================================
# 练习 1.1: 德布罗意波长
# Exercise 1.1: de Broglie Wavelength
# -----------------------------------------------------------------------------
# 物理背景：德布罗意假说（1924年）指出所有物质都具有波动性
# 波长与动量的关系：λ = h/p，其中 h 是普朗克常数
# 这一假说后来被电子衍射实验所证实（戴维森-革末实验）
# 典型尺度：100 eV电子的波长约为 0.12 nm，与原子尺度相当
# =============================================================================
def de_broglie_wavelength(p):
    """
    计算德布罗意波长 Calculate de Broglie wavelength

    公式: λ = h/p

    参数 Parameters:
        p: 动量 momentum (kg·m/s)

    返回 Returns:
        wavelength: 德布罗意波长 (m)

    物理意义：波长越短，粒子性越明显；波长越长，波动性越明显
    """
    # TODO: 根据德布罗意公式计算波长
    # 提示：使用普朗克常数 h 和动量 p
    wavelength = h / p  # 修改这里
    return wavelength


def electron_wavelength_from_energy(KE):
    """
    从动能计算电子的德布罗意波长 Calculate electron wavelength from kinetic energy

    推导过程（非相对论近似）:
        动能: KE = p²/(2m) → p = √(2m·KE)
        波长: λ = h/p = h/√(2m·KE)

    参数 Parameters:
        KE: 动能 kinetic energy (J)

    返回 Returns:
        wavelength: 德布罗意波长 (m)

    注意：当 KE > 0.1 MeV 时需要考虑相对论修正
    """
    # 从动能计算动量（非相对论近似）
    p = np.sqrt(2 * m_e * KE)
    # TODO: 调用 de_broglie_wavelength 函数计算并返回波长
    return de_broglie_wavelength(p)  # 修改这里


# 例子: 100 eV 电子的波长（电子显微镜中常用的加速电压量级）
# 预期结果：约 0.123 nm，这正是为什么电子显微镜能观察到原子级别的结构
KE_electron = 100 * eV
lambda_electron = electron_wavelength_from_energy(KE_electron)


# =============================================================================
# 练习 1.2: 波函数归一化
# Exercise 1.2: Wave Function Normalization
# -----------------------------------------------------------------------------
# 物理背景：波函数的概率诠释（玻恩诠释，1926年）
# |ψ(x)|² dx 表示粒子在 [x, x+dx] 区间内被发现的概率
# 归一化条件保证总概率为1：∫|ψ|²dx = 1
# 这是量子力学最基本的公设之一
# =============================================================================
def normalize_wavefunction(psi, x):
    """
    归一化波函数使得 ∫|ψ|²dx = 1

    参数 Parameters:
        psi: 波函数数组 wavefunction array (复数或实数)
        x: 位置数组 position array (m)

    返回 Returns:
        psi_normalized: 归一化后的波函数

    数值方法：使用矩形积分法计算 ∫|ψ|²dx
    """
    dx = x[1] - x[0]  # 空间步长
    # TODO: 计算归一化常数 N = √(∫|ψ|²dx)，然后返回 ψ/N
    # 提示：归一化后的波函数满足 ∫|ψ_norm|²dx = 1
    norm = np.sqrt(np.sum(np.abs(psi)**2) * dx)
    psi_normalized = psi / norm  # 修改这里
    return psi_normalized


def probability_density(psi):
    """
    计算概率密度 Calculate probability density

    公式: ρ(x) = |ψ(x)|² = ψ*(x)·ψ(x)

    对于复数波函数，|ψ|² = ψ*ψ（ψ*是复共轭）
    概率密度的物理意义：ρ(x)dx 是粒子在 x 附近 dx 范围内被探测到的概率
    """
    return np.abs(psi)**2


# =============================================================================
# 练习 1.3: 无限深势阱（一维盒子）
# Exercise 1.3: Infinite Square Well (Particle in a Box)
# -----------------------------------------------------------------------------
# 物理背景：这是量子力学中最简单的束缚态问题
# 粒子被限制在宽度为 L 的一维区域内，势阱内 V=0，阱外 V=∞
#
# 边界条件：ψ(0) = ψ(L) = 0（波函数在势阱边界连续）
# 这导致能量量子化，只有特定的能量值是允许的
#
# 重要物理结论：
# 1. 能量量子化：E_n ∝ n²，高能级间距越来越大
# 2. 零点能：基态能量 E_1 > 0（不确定性原理的体现）
# 3. 波函数节点：第n态有 (n-1) 个节点
# =============================================================================
# 势能: V(x) = 0 for 0 < x < L, V(x) = ∞ otherwise
# 能级: E_n = n²π²ℏ²/(2mL²), n = 1, 2, 3, ...
# 波函数: ψ_n(x) = √(2/L) * sin(nπx/L)

def infinite_well_energy(n, L, m=m_e):
    """
    计算无限深势阱第n能级的能量 Calculate energy levels of infinite square well

    公式: E_n = n²π²ℏ²/(2mL²)

    参数 Parameters:
        n: 主量子数 (n = 1, 2, 3, ...)，n=1对应基态
        L: 势阱宽度 well width (m)
        m: 粒子质量 particle mass (kg)，默认为电子质量

    返回 Returns:
        E_n: 第n能级的能量 (J)

    物理意义：能量与n²成正比，与L²成反比
    尺度估计：1nm势阱中电子的基态能量约为 0.38 eV
    """
    # TODO: 根据公式 E_n = n²π²ℏ²/(2mL²) 计算能量
    E_n = (n**2 * np.pi**2 * hbar**2) / (2 * m * L**2)  # 修改这里
    return E_n


def infinite_well_wavefunction(x, n, L):
    """
    计算无限深势阱第n态的波函数 Calculate wavefunction of infinite well

    公式: ψ_n(x) = √(2/L) · sin(nπx/L)，对于 0 < x < L
          ψ_n(x) = 0，对于 x ≤ 0 或 x ≥ L

    参数 Parameters:
        x: 位置数组 position array (m)
        n: 主量子数 (n = 1, 2, 3, ...)
        L: 势阱宽度 (m)

    返回 Returns:
        psi: 波函数数组

    归一化验证：∫₀ᴸ |ψ_n|² dx = (2/L)∫₀ᴸ sin²(nπx/L) dx = 1
    """
    # TODO: 计算归一化波函数，注意阱外波函数为0
    psi = np.sqrt(2/L) * np.sin(n * np.pi * x / L)  # 修改这里
    # 势阱外波函数为0（满足边界条件）
    psi = np.where((x > 0) & (x < L), psi, 0)
    return psi


# 势阱参数设置
L = 1e-9  # 势阱宽度 1 nm（典型的量子点尺度）
x_well = np.linspace(-0.1*L, 1.1*L, 500)  # 位置数组（含阱外区域以便观察边界条件）


# =============================================================================
# 练习 1.4: 量子谐振子
# Exercise 1.4: Quantum Harmonic Oscillator
# -----------------------------------------------------------------------------
# 物理背景：谐振子是物理学中最重要的模型之一
# 任何势能在极小值附近都可以近似为谐振子势（泰勒展开取二次项）
# 应用：分子振动、晶格振动（声子）、电磁场量子化（光子）
#
# 势能: V(x) = (1/2)mω²x²（抛物线形势阱）
# 量子力学求解得到离散能级：E_n = (n + 1/2)ℏω
#
# 重要特点：
# 1. 能级等间距：ΔE = ℏω（与经典振子频率相同）
# 2. 零点能：E_0 = ℏω/2 ≠ 0（不确定性原理的直接结果）
# 3. 波函数含高斯包络：exp(-ξ²/2)，体现粒子主要分布在势阱底部
# =============================================================================
# 势能: V(x) = (1/2)mω²x²
# 能级: E_n = (n + 1/2)ℏω, n = 0, 1, 2, ...

def harmonic_oscillator_energy(n, omega, hbar=hbar):
    """
    计算量子谐振子第n能级的能量 Calculate harmonic oscillator energy level

    公式: E_n = (n + 1/2)ℏω

    参数 Parameters:
        n: 量子数 (n = 0, 1, 2, ...)，n=0对应基态
        omega: 角频率 angular frequency (rad/s)
        hbar: 约化普朗克常数 (J·s)

    返回 Returns:
        E_n: 第n能级的能量 (J)

    物理意义：n=0时 E_0 = ℏω/2 是零点能，体现量子涨落
    """
    # TODO: 根据公式 E_n = (n + 1/2)ℏω 计算能量
    E_n = (n + 0.5) * hbar * omega  # 修改这里
    return E_n


def hermite_polynomial(n, x):
    """
    厄米多项式 Hermite Polynomial H_n(x)

    递推关系: H_{n+1}(x) = 2x·H_n(x) - 2n·H_{n-1}(x)
    初始条件: H_0(x) = 1, H_1(x) = 2x

    前几个多项式:
        H_0 = 1
        H_1 = 2x
        H_2 = 4x² - 2
        H_3 = 8x³ - 12x

    厄米多项式是谐振子波函数的核心组成部分
    """
    if n == 0:
        return np.ones_like(x)
    elif n == 1:
        return 2 * x
    else:
        H_prev2 = np.ones_like(x)
        H_prev1 = 2 * x
        for i in range(2, n + 1):
            H_curr = 2 * x * H_prev1 - 2 * (i - 1) * H_prev2
            H_prev2 = H_prev1
            H_prev1 = H_curr
        return H_curr


def harmonic_oscillator_wavefunction(x, n, m, omega):
    """
    计算量子谐振子第n态波函数 Calculate harmonic oscillator wavefunction

    公式: ψ_n(x) = (mω/πℏ)^(1/4) · (1/√(2ⁿn!)) · H_n(ξ) · exp(-ξ²/2)
    其中无量纲坐标: ξ = √(mω/ℏ) · x

    参数 Parameters:
        x: 位置数组 (m)
        n: 量子数 (n = 0, 1, 2, ...)
        m: 粒子质量 (kg)
        omega: 角频率 (rad/s)

    返回 Returns:
        psi: 波函数数组

    波函数特点：
    - 高斯包络 exp(-ξ²/2) 保证波函数在无穷远处趋于0
    - H_n(ξ) 决定节点数，第n态有n个节点
    - 基态 n=0 是纯高斯函数，无节点
    """
    # 无量纲坐标变换
    xi = np.sqrt(m * omega / hbar) * x

    # 归一化常数：保证 ∫|ψ|²dx = 1
    norm = (m * omega / (np.pi * hbar))**0.25 / np.sqrt(2**n * np.math.factorial(n))

    # TODO: 计算波函数 ψ = 归一化常数 × H_n(ξ) × exp(-ξ²/2)
    psi = norm * hermite_polynomial(n, xi) * np.exp(-xi**2 / 2)  # 修改这里
    return psi


# =============================================================================
# 练习 1.5: 数值求解薛定谔方程（有限差分法）
# Exercise 1.5: Numerical Solution of Schrödinger Equation
# -----------------------------------------------------------------------------
# 物理背景：对于复杂势场，薛定谔方程通常没有解析解
# 需要使用数值方法求解，常用方法包括：
# 1. 有限差分法（本练习使用）
# 2. 变分法
# 3. 打靶法
#
# 有限差分法原理：
# 将连续空间离散化，用差分近似微分
# d²ψ/dx² ≈ (ψᵢ₊₁ - 2ψᵢ + ψᵢ₋₁)/dx²
# 这将微分方程转化为矩阵本征值问题：Hψ = Eψ
# =============================================================================
def build_hamiltonian_matrix(x, V, m=m_e):
    """
    构建哈密顿量矩阵 Build Hamiltonian matrix using finite difference method

    哈密顿算符: Ĥ = -ℏ²/(2m) · d²/dx² + V(x)

    有限差分近似（三点公式）:
        d²ψ/dx² ≈ (ψᵢ₊₁ - 2ψᵢ + ψᵢ₋₁)/dx²

    矩阵形式：H 是三对角矩阵
        对角元: H[i,i] = 2·(-ℏ²/(2m·dx²)) + V[i]
        非对角元: H[i,i±1] = -ℏ²/(2m·dx²)

    参数 Parameters:
        x: 位置数组 (m)
        V: 势能数组 (J)
        m: 粒子质量 (kg)

    返回 Returns:
        H: 哈密顿量矩阵 (N×N)
    """
    N = len(x)
    dx = x[1] - x[0]  # 空间步长

    # 动能项系数: T = -ℏ²/(2m·dx²)
    kinetic_coeff = -hbar**2 / (2 * m * dx**2)

    # 构建三对角矩阵
    H = np.zeros((N, N))

    for i in range(N):
        H[i, i] = -2 * kinetic_coeff + V[i]  # 对角元：动能 + 势能
        if i > 0:
            H[i, i-1] = kinetic_coeff  # 下对角元
        if i < N-1:
            H[i, i+1] = kinetic_coeff  # 上对角元

    return H


def solve_schrodinger(x, V, n_states=5, m=m_e):
    """
    数值求解定态薛定谔方程 Numerically solve time-independent Schrödinger equation

    方程: Ĥψ = Eψ（本征值问题）

    参数 Parameters:
        x: 位置数组 (m)
        V: 势能数组 (J)
        n_states: 需要求解的能级数目
        m: 粒子质量 (kg)

    返回 Returns:
        energies: 能量本征值数组 (J)，从小到大排列
        wavefunctions: 波函数矩阵，第i列对应第i个本征态

    注意：使用 scipy.linalg.eigh 求解厄米矩阵本征值问题
    """
    H = build_hamiltonian_matrix(x, V, m)

    # TODO: 使用 scipy.linalg.eigh 求解本征值问题
    # eigh 专门用于厄米矩阵（实对称矩阵），返回实本征值
    energies, wavefunctions = linalg.eigh(H)  # 修改这里

    # 只取前 n_states 个最低能级
    energies = energies[:n_states]
    wavefunctions = wavefunctions[:, :n_states]

    # 对每个本征态进行归一化
    dx = x[1] - x[0]
    for i in range(n_states):
        norm = np.sqrt(np.sum(np.abs(wavefunctions[:, i])**2) * dx)
        wavefunctions[:, i] /= norm

    return energies, wavefunctions


# -------------------------
# 数值求解无限深势阱测试
# -------------------------
N_points = 200  # 离散化点数（越多精度越高，但计算量增大）
x_num = np.linspace(0, L, N_points)
V_well = np.zeros(N_points)  # 阱内势能为0
# 设置边界条件：用极大势垒模拟无限深势阱的边界
V_well[0] = 1e10 * eV   # 左边界势垒
V_well[-1] = 1e10 * eV  # 右边界势垒

# 求解前5个能级
E_numerical, psi_numerical = solve_schrodinger(x_num, V_well, n_states=5)


# =============================================================================
# 练习 1.6: 期望值计算
# Exercise 1.6: Expectation Values
# -----------------------------------------------------------------------------
# 物理背景：量子力学中，可观测量的测量结果是概率性的
# 期望值 <A> 表示多次测量的平均值
#
# 期望值公式: <A> = ∫ψ*(x) Â ψ(x) dx
# 对于位置算符: <x> = ∫ψ*(x) x ψ(x) dx
#
# 不确定度定义: ΔA = √(<A²> - <A>²)
# 海森堡不确定性原理: Δx·Δp ≥ ℏ/2
# =============================================================================
def expectation_position(psi, x):
    """
    计算位置期望值 Calculate position expectation value

    公式: <x> = ∫ψ*(x)·x·ψ(x) dx = ∫x|ψ(x)|² dx

    参数 Parameters:
        psi: 波函数数组（应已归一化）
        x: 位置数组 (m)

    返回 Returns:
        <x>: 位置期望值 (m)

    物理意义：<x>是粒子位置的平均值，但单次测量不一定得到这个值
    """
    dx = x[1] - x[0]
    # TODO: 计算位置期望值 <x> = ∫ψ*·x·ψ dx
    x_exp = np.sum(np.conj(psi) * x * psi) * dx  # 修改这里
    return np.real(x_exp)  # 取实部（期望值应为实数）


def expectation_position_squared(psi, x):
    """
    计算位置平方的期望值 Calculate <x²>

    公式: <x²> = ∫ψ*(x)·x²·ψ(x) dx

    用于计算位置不确定度：Δx = √(<x²> - <x>²)
    """
    dx = x[1] - x[0]
    x2_exp = np.sum(np.conj(psi) * x**2 * psi) * dx
    return np.real(x2_exp)


def position_uncertainty(psi, x):
    """
    计算位置不确定度 Calculate position uncertainty

    公式: Δx = √(<x²> - <x>²) = √(方差)

    参数 Parameters:
        psi: 波函数数组
        x: 位置数组 (m)

    返回 Returns:
        Δx: 位置不确定度 (m)

    物理意义：
    - Δx 描述粒子位置的"展宽"或"不确定程度"
    - 对于无限深势阱基态: Δx ≈ 0.18L
    - 海森堡不确定性原理: Δx·Δp ≥ ℏ/2
    """
    x_exp = expectation_position(psi, x)
    x2_exp = expectation_position_squared(psi, x)
    # TODO: 根据公式 Δx = √(<x²> - <x>²) 计算不确定度
    delta_x = np.sqrt(x2_exp - x_exp**2)  # 修改这里
    return delta_x


# =============================================================================
# 可视化
# =============================================================================
def plot_quantum():
    """绘制量子力学结果"""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    # 1. 德布罗意波长 vs 能量
    ax1 = axes[0, 0]
    energies_ev = np.logspace(0, 4, 100)  # 1 eV to 10000 eV
    wavelengths = [electron_wavelength_from_energy(E * eV) * 1e12 for E in energies_ev]  # pm
    ax1.loglog(energies_ev, wavelengths)
    ax1.set_xlabel('Energy (eV)')
    ax1.set_ylabel('Wavelength (pm)')
    ax1.set_title('德布罗意波长 de Broglie Wavelength')
    ax1.grid(True, alpha=0.3)

    # 2. 无限深势阱波函数
    ax2 = axes[0, 1]
    x_plot = np.linspace(0, L, 200)
    for n in [1, 2, 3, 4]:
        psi = infinite_well_wavefunction(x_plot, n, L)
        E = infinite_well_energy(n, L) / eV
        ax2.plot(x_plot/1e-9, psi/1e4.5 + n, label=f'n={n}, E={E:.1f} eV')
    ax2.set_xlabel('x (nm)')
    ax2.set_ylabel('ψ (shifted)')
    ax2.set_title('无限深势阱波函数 Infinite Well')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 无限深势阱概率密度
    ax3 = axes[0, 2]
    for n in [1, 2, 3]:
        psi = infinite_well_wavefunction(x_plot, n, L)
        prob = probability_density(psi)
        ax3.plot(x_plot/1e-9, prob/1e9, label=f'n={n}')
    ax3.set_xlabel('x (nm)')
    ax3.set_ylabel('|ψ|² (nm⁻¹)')
    ax3.set_title('概率密度 Probability Density')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 数值解 vs 解析解比较
    ax4 = axes[1, 0]
    for i in range(3):
        # 数值解
        ax4.plot(x_num/1e-9, psi_numerical[:, i]**2 / 1e9, '-', label=f'Numerical n={i+1}')
        # 解析解
        psi_exact = infinite_well_wavefunction(x_num, i+1, L)
        ax4.plot(x_num/1e-9, psi_exact**2 / 1e9, '--', alpha=0.7)
    ax4.set_xlabel('x (nm)')
    ax4.set_ylabel('|ψ|² (nm⁻¹)')
    ax4.set_title('数值解 vs 解析解')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 能级比较
    ax5 = axes[1, 1]
    n_levels = 5
    E_exact = [infinite_well_energy(n, L) / eV for n in range(1, n_levels+1)]
    E_num = E_numerical / eV

    x_pos = np.arange(n_levels)
    width = 0.35
    ax5.bar(x_pos - width/2, E_exact, width, label='Analytical')
    ax5.bar(x_pos + width/2, E_num, width, label='Numerical')
    ax5.set_xlabel('n')
    ax5.set_ylabel('Energy (eV)')
    ax5.set_title('能级对比 Energy Levels')
    ax5.set_xticks(x_pos)
    ax5.set_xticklabels([str(i+1) for i in x_pos])
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. 谐振子波函数
    ax6 = axes[1, 2]
    omega = 1e15  # rad/s
    x_ho = np.linspace(-3e-9, 3e-9, 500)
    for n in [0, 1, 2, 3]:
        psi_ho = harmonic_oscillator_wavefunction(x_ho, n, m_e, omega)
        E_ho = harmonic_oscillator_energy(n, omega) / eV
        # 偏移显示
        ax6.plot(x_ho/1e-9, psi_ho/1e4.5 + n, label=f'n={n}')
    ax6.set_xlabel('x (nm)')
    ax6.set_ylabel('ψ (shifted)')
    ax6.set_title('谐振子波函数 Harmonic Oscillator')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('quantum_mechanics.png', dpi=150)
    print("图像已保存为 quantum_mechanics.png")
    plt.show()


# =============================================================================
# 验证函数
# Verification Function
# =============================================================================
def verify():
    """验证所有练习的正确性 Verify all exercises"""
    all_passed = True

    # 检查 1.1 - 德布罗意波长
    # Check 1.1 - de Broglie wavelength
    # 100 eV 电子的波长约为 0.123 nm
    expected_lambda = h / np.sqrt(2 * m_e * 100 * eV)
    if not np.isclose(lambda_electron, expected_lambda, rtol=0.01):
        print(f"错误 1.1: 德布罗意波长计算错误")
        print(f"  期望值: {expected_lambda*1e9:.4f} nm")
        print(f"  计算值: {lambda_electron*1e9:.4f} nm")
        all_passed = False
    else:
        print(f"通过 1.1: 德布罗意波长正确 (100eV电子: lambda = {lambda_electron*1e9:.4f} nm)")

    # 检查 1.2 - 波函数归一化
    # Check 1.2 - Normalization
    x_test = np.linspace(0, L, 1000)
    psi_test = np.sin(np.pi * x_test / L)
    psi_norm = normalize_wavefunction(psi_test, x_test)
    dx = x_test[1] - x_test[0]
    integral = np.sum(np.abs(psi_norm)**2) * dx
    if not np.isclose(integral, 1.0, rtol=0.01):
        print(f"错误 1.2: 波函数归一化失败")
        print(f"  积分值 |psi|^2 dx = {integral:.4f}，应为 1.0")
        all_passed = False
    else:
        print("通过 1.2: 波函数归一化正确")

    # 检查 1.3 - 无限深势阱能级
    # Check 1.3 - Infinite well energy
    E1_exact = np.pi**2 * hbar**2 / (2 * m_e * L**2)
    E1_calc = infinite_well_energy(1, L)
    if not np.isclose(E1_calc, E1_exact, rtol=0.01):
        print(f"错误 1.3: 无限深势阱能级公式错误")
        print(f"  期望 E_1 = {E1_exact/eV:.3f} eV")
        print(f"  计算 E_1 = {E1_calc/eV:.3f} eV")
        all_passed = False
    else:
        print(f"通过 1.3: 无限深势阱能级正确 (E_1 = {E1_calc/eV:.3f} eV)")

    # 检查 1.4 - 谐振子能级
    # Check 1.4 - Harmonic oscillator energy
    omega_test = 1e15
    E0_ho = harmonic_oscillator_energy(0, omega_test)
    expected_E0 = 0.5 * hbar * omega_test
    if not np.isclose(E0_ho, expected_E0, rtol=0.01):
        print("错误 1.4: 谐振子基态能量公式错误")
        print(f"  期望 E_0 = {expected_E0/eV:.3f} eV")
        print(f"  计算 E_0 = {E0_ho/eV:.3f} eV")
        all_passed = False
    else:
        print(f"通过 1.4: 谐振子能级正确 (E_0 = {E0_ho/eV:.3f} eV)")

    # 检查 1.5 - 数值求解薛定谔方程
    # Check 1.5 - Numerical solution
    # 比较数值解与解析解的前三个能级
    for i in range(3):
        E_exact = infinite_well_energy(i+1, L)
        E_num = E_numerical[i]
        rel_error = abs(E_num - E_exact) / E_exact
        if rel_error > 0.05:  # 允许5%误差
            print(f"错误 1.5: 数值解能级 n={i+1} 误差过大")
            print(f"  相对误差: {rel_error*100:.1f}%，超过允许的 5%")
            all_passed = False
            break
    else:
        print("通过 1.5: 数值求解薛定谔方程正确 (相对误差 < 5%)")

    # 检查 1.6 - 期望值计算
    # Check 1.6 - Expectation values
    psi_ground = infinite_well_wavefunction(x_num, 1, L)
    x_exp = expectation_position(psi_ground, x_num)
    expected_x_exp = L / 2  # 基态粒子平均位于势阱中心
    if not np.isclose(x_exp, expected_x_exp, rtol=0.05):
        print(f"错误 1.6: 位置期望值计算错误")
        print(f"  期望 <x> = {expected_x_exp*1e9:.3f} nm（势阱中心）")
        print(f"  计算 <x> = {x_exp*1e9:.3f} nm")
        all_passed = False
    else:
        delta_x = position_uncertainty(psi_ground, x_num)
        print(f"通过 1.6: 期望值计算正确 (<x> = {x_exp*1e9:.3f} nm, Delta_x = {delta_x*1e9:.3f} nm)")

    if all_passed:
        print("\n所有测试通过！正在生成可视化...")
        try:
            plot_quantum()
        except Exception as e:
            print(f"可视化生成失败: {e}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("波粒二象性与薛定谔方程 Quantum Mechanics")
    print("=" * 50)
    verify()
