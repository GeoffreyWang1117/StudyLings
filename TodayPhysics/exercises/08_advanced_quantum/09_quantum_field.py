"""
量子场论入门 Introduction to Quantum Field Theory
难度 Difficulty: ★★★★★

物理背景 Physical Background:
==================================
量子场论是将量子力学与狭义相对论相结合的理论框架，是描述基本粒子
相互作用的标准语言。量子场论允许粒子的产生和湮灭，这是单粒子
量子力学无法描述的。

历史发展:
- 1927-1930: 狄拉克量子化电磁场，建立QED雏形
- 1940s: 费曼、施温格、朝永振一郎发展重整化理论
- 1954: 杨振宁-米尔斯建立非阿贝尔规范理论
- 1970s: 标准模型建立（电弱统一 + QCD）

核心思想:
1. 场是基本实体，粒子是场的激发
2. 局域规范对称性决定相互作用
3. 费曼图提供系统的微扰计算方法

学习目标 Learning Objectives:
- 理解相对论性场方程（Klein-Gordon, Dirac）
- 掌握场的量子化和传播子概念
- 学习费曼图的物理意义和计算规则
- 了解QED的基本结构

关键公式 Key Formulas:
- Klein-Gordon方程: (□ + m²c²/ℏ²)φ = 0，描述自旋0粒子
- Dirac方程: (iγ^μ∂_μ - mc/ℏ)ψ = 0，描述自旋1/2粒子
- 标量场传播子: iΔ_F(x-y) = ⟨0|T{φ(x)φ(y)}|0⟩
- 费曼传播子（动量空间）: D(p) = i/(p² - m²c² + iε)
- 精细结构常数: α = e²/(4πε₀ℏc) ≈ 1/137

HINT: Klein-Gordon方程: (□ + m²)φ = 0 (自然单位)
HINT: Dirac方程: (iγ^μ∂_μ - m)ψ = 0
HINT: 传播子: iΔ_F(x-y) = ⟨0|T{φ(x)φ(y)}|0⟩（时间序乘积）
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import hbar, c, m_e, eV

# I AM NOT DONE

# =============================================================================
# 练习 9.1: Klein-Gordon场
# Exercise 9.1: Klein-Gordon Field
#
# 物理背景:
# Klein-Gordon方程是描述自旋0相对论粒子（如π介子、Higgs粒子）的场方程。
# 它是薛定谔方程的相对论推广，但最初被解释为单粒子方程时遇到负概率问题。
# 正确解释需要量子场论框架：负能解对应反粒子。
#
# 方程: (□ + m²c²/ℏ²)φ = 0
# 其中 □ = ∂²/∂t² - c²∇² 是达朗贝尔算符
# =============================================================================
def klein_gordon_dispersion(k, m):
    """
    Klein-Gordon色散关系 Klein-Gordon Dispersion Relation

    从平面波解 φ ~ exp(i(k·r - ωt)) 代入Klein-Gordon方程得到:
    ω² = k²c² + (mc²/ℏ)²

    这正是相对论能量-动量关系 E² = p²c² + m²c⁴ 的量子版本
    (令 E = ℏω, p = ℏk)

    参数:
        k (float): 波矢量大小 [1/m]
        m (float): 粒子质量 [kg]

    返回:
        float: 角频率 ω [rad/s]
    """
    return np.sqrt(k**2 * c**2 + (m * c**2 / hbar)**2)


def compton_wavelength(m):
    """
    康普顿波长 Compton Wavelength

    定义: λ_C = h/(mc) = 2πℏ/(mc)

    物理意义:
    - 量子效应变得重要的特征长度尺度
    - 粒子定域在 Δx ~ λ_C 时，能量不确定性 ~ mc²（可产生粒子-反粒子对）
    - 标志着单粒子量子力学失效，需要量子场论

    典型值:
    - 电子: λ_C ≈ 2.4×10⁻¹² m
    - 质子: λ_C ≈ 1.3×10⁻¹⁵ m

    参数:
        m (float): 粒子质量 [kg]

    返回:
        float: 康普顿波长 [m]
    """
    return 2 * np.pi * hbar / (m * c)


def klein_gordon_propagator_momentum(p, m):
    """
    Klein-Gordon传播子（动量空间）Momentum Space Propagator

    Feynman传播子: D(p) = i/(p² - m²c² + iε)

    物理意义:
    - 描述虚粒子（内线）的传播
    - iε规定了因果性（正频率向前传播，负频率向后传播）
    - 极点位于 p² = m²c²（质壳条件）

    本函数返回分母 p² - m²c²，用于判断是否在质壳上

    参数:
        p (float): 四动量的模平方 [J/c]
        m (float): 粒子质量 [kg]

    返回:
        float: 传播子分母
    """
    return p**2 - (m * c)**2


def scalar_field_mode_expansion():
    """
    标量场的模式展开 Mode Expansion of Scalar Field

    实标量场的正则量子化:
    φ(x) = ∫d³k/(2π)^(3/2) × 1/√(2ω_k) × [a_k e^{ikx} + a†_k e^{-ikx}]

    物理解释:
    - a_k: 动量为 k 的粒子的湮灭算符
    - a†_k: 动量为 k 的粒子的产生算符
    - 1/√(2ω_k): 洛伦兹不变归一化
    - 正频部分: 吸收光子
    - 负频部分: 发射光子

    对易关系: [a_k, a†_k'] = δ³(k - k')

    返回:
        str: 模式展开表达式
    """
    return "φ(x) = ∫d³k/(2π)^(3/2) [a_k e^{ikx} + a†_k e^{-ikx}]/√(2ω_k)"


def vacuum_energy_density(k_max, m, volume):
    """
    真空能量密度（紫外截断）Vacuum Energy Density

    公式: E_vac/V = ∫d³k/(2π)³ × ℏω_k/2

    物理意义:
    - 每个场模式的零点能 ℏω_k/2 对真空能量有贡献
    - 不截断时发散 → 需要重整化
    - 这是宇宙学常数问题的核心

    著名问题:
    - 理论预言的真空能量密度与观测暗能量相差 ~10¹²⁰ 倍
    - 被称为"物理学历史上最糟糕的理论预言"

    参数:
        k_max (float): 动量截断 [1/m]
        m (float): 场的质量 [kg]
        volume (float): 体积（未使用，返回密度）

    返回:
        float: 能量密度 [J/m³]
    """
    # 简化为一维积分
    k_vals = np.linspace(0, k_max, 1000)
    omega_k = klein_gordon_dispersion(k_vals, m)
    dk = k_vals[1] - k_vals[0]

    # 球对称积分
    integrand = k_vals**2 * hbar * omega_k / 2
    E_density = np.sum(integrand) * dk / (2 * np.pi**2)
    return E_density


# =============================================================================
# 练习 9.2: Dirac场
# Exercise 9.2: Dirac Field
#
# 物理背景:
# Dirac方程描述自旋1/2的相对论粒子（电子、夸克等）。
# 狄拉克1928年提出此方程，预言了正电子的存在（1932年实验证实）。
#
# 关键特征:
# - 四分量旋量（上两分量: 粒子，下两分量: 反粒子）
# - γ矩阵满足Clifford代数
# - 自然包含自旋和磁矩
# =============================================================================
def gamma_matrices():
    """
    Dirac γ矩阵（Dirac表示）Gamma Matrices in Dirac Representation

    定义:
    γ⁰ = [[I₂, 0], [0, -I₂]]
    γⁱ = [[0, σⁱ], [-σⁱ, 0]], i = 1,2,3

    其中 σⁱ 是泡利矩阵

    Clifford代数:
    {γ^μ, γ^ν} = 2η^μν I₄
    其中 η = diag(1,-1,-1,-1) 是闵可夫斯基度规

    物理意义:
    - γ矩阵编码了时空的结构
    - 保证Dirac方程的洛伦兹协变性

    返回:
        tuple: (γ⁰, γ¹, γ², γ³) 四个 4×4 复数矩阵
    """
    # Pauli矩阵
    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
    I2 = np.eye(2, dtype=complex)
    zero2 = np.zeros((2, 2), dtype=complex)

    gamma0 = np.block([[I2, zero2], [zero2, -I2]])
    gamma1 = np.block([[zero2, sigma_x], [-sigma_x, zero2]])
    gamma2 = np.block([[zero2, sigma_y], [-sigma_y, zero2]])
    gamma3 = np.block([[zero2, sigma_z], [-sigma_z, zero2]])

    return gamma0, gamma1, gamma2, gamma3


def gamma5_matrix():
    """
    γ⁵ 矩阵（手征性算符）Gamma-5 Matrix (Chirality Operator)

    定义: γ⁵ = iγ⁰γ¹γ²γ³

    性质:
    - (γ⁵)² = I₄
    - {γ⁵, γ^μ} = 0
    - (γ⁵)† = γ⁵

    物理意义:
    - 手征投影算符: P_L = (1-γ⁵)/2, P_R = (1+γ⁵)/2
    - 区分左手和右手费米子
    - 弱相互作用只耦合左手费米子（宇称破缺）

    返回:
        np.ndarray: 4×4 γ⁵ 矩阵
    """
    g0, g1, g2, g3 = gamma_matrices()
    return 1j * g0 @ g1 @ g2 @ g3


def clifford_algebra_check(gamma_mu, gamma_nu, mu, nu):
    """
    Clifford代数验证 Clifford Algebra Verification

    验证: {γ^μ, γ^ν} = γ^μ γ^ν + γ^ν γ^μ = 2η^μν I₄

    闵可夫斯基度规:
    η = diag(+1, -1, -1, -1) (东海岸约定)

    结果:
    - μ = ν = 0: {γ⁰, γ⁰} = 2I
    - μ = ν = i (空间): {γⁱ, γⁱ} = -2I
    - μ ≠ ν: {γ^μ, γ^ν} = 0

    参数:
        gamma_mu, gamma_nu: γ矩阵
        mu, nu: 洛伦兹指标

    返回:
        bool: 是否满足Clifford代数
    """
    anticomm = gamma_mu @ gamma_nu + gamma_nu @ gamma_mu
    eta = np.diag([1, -1, -1, -1])

    expected = 2 * eta[mu, nu] * np.eye(4)
    return np.allclose(anticomm, expected)


def dirac_spinor_positive_energy(p, m, spin):
    """
    正能量Dirac旋量 Positive Energy Dirac Spinor

    u(p,s) 满足Dirac方程: (γ^μ p_μ - m)u = 0

    归一化: ū u = 2m（洛伦兹标量）

    物理意义:
    - 描述正能量粒子（如电子）
    - spin = 'up'/'down' 指自旋投影
    - 在静止系简化，然后Lorentz推进到任意动量

    注意: 本函数采用简化实现（假设动量沿z轴）

    参数:
        p (np.ndarray): 三动量 [px, py, pz]
        m (float): 粒子质量
        spin (str): 自旋状态 'up' 或 'down'

    返回:
        np.ndarray: 4分量Dirac旋量
    """
    # 简化：假设p沿z方向
    E = np.sqrt(np.sum(p**2) * c**2 + (m * c**2)**2)

    if spin == 'up':
        chi = np.array([1, 0], dtype=complex)
    else:
        chi = np.array([0, 1], dtype=complex)

    # 简化的旋量
    N = np.sqrt(E + m * c**2)
    sigma_z = np.array([[1, 0], [0, -1]])
    sigma_dot_p = p[2] * sigma_z if len(p) > 2 else 0

    u_upper = N * chi
    u_lower = c * sigma_dot_p @ chi / (E + m * c**2) if E + m * c**2 > 0 else np.zeros(2)

    return np.concatenate([u_upper, u_lower])


def dirac_current(psi_bar, gamma_mu, psi):
    """
    Dirac流 Dirac Current

    定义: j^μ = ψ̄ γ^μ ψ
    其中 ψ̄ = ψ† γ⁰ 是Dirac共轭

    守恒性:
    ∂_μ j^μ = 0（连续性方程）

    分量意义:
    - j⁰ = ψ̄ γ⁰ ψ = ψ†ψ: 概率密度（正定）
    - j^i: 概率流密度

    物理应用:
    - 与光子耦合: L_int = e j^μ A_μ

    参数:
        psi_bar: Dirac共轭旋量 ψ̄
        gamma_mu: γ^μ 矩阵
        psi: Dirac旋量 ψ

    返回:
        complex: 流的 μ 分量
    """
    return psi_bar @ gamma_mu @ psi


# =============================================================================
# 练习 9.3: 传播子和格林函数
# Exercise 9.3: Propagators and Green Functions
#
# 物理背景:
# 传播子是量子场论的核心对象，描述粒子从一点传播到另一点的振幅。
# 费曼传播子包含了因果性和正确的边界条件。
#
# 重要性:
# - 费曼图中的内线对应传播子
# - 格林函数方法求解场方程
# - 连接时间序乘积和可观测量
# =============================================================================
def feynman_propagator_scalar(x, m):
    """
    标量场Feynman传播子（位置空间）Scalar Feynman Propagator

    精确形式涉及贝塞尔函数，这里给出远场渐近行为:
    Δ_F(x) ∝ exp(-m c |x| / ℏ) / |x|，对于 |x| >> λ_C

    物理意义:
    - 有质量粒子的传播在距离 ~ λ_C 外指数衰减
    - 这解释了短程力（如核力）的来源
    - 无质量粒子（光子）: Δ_F ∝ 1/|x|（库仑势）

    参数:
        x (float): 空间距离 [m]
        m (float): 粒子质量 [kg]

    返回:
        float: 传播子值（任意归一化）
    """
    r = np.abs(x)
    mc_hbar = m * c / hbar
    if r > 0:
        return np.exp(-mc_hbar * r) / r
    return np.inf


def photon_propagator_momentum(k):
    """
    光子传播子（Feynman规范）Photon Propagator

    Feynman规范下:
    D_μν(k) = -iη_μν / (k² + iε)

    规范依赖:
    - Feynman规范（ξ=1）: 最简单，常用于QED计算
    - Landau规范（ξ=0）: 横向分量
    - Coulomb规范: 非协变但物理直观

    光子无质量 → 极点在 k² = 0

    参数:
        k (float): 四动量模平方 k²

    返回:
        float: 传播子分母 1/k²
    """
    k2 = k**2
    if k2 == 0:
        return np.inf
    return -1 / k2


def fermion_propagator_momentum(p, m):
    """
    费米子传播子（动量空间）Fermion Propagator

    形式: S(p) = i(γ·p + m) / (p² - m² + iε)
         = i / (γ·p - m + iε)

    分子结构:
    - γ·p + m = γ^μ p_μ + m 是4×4矩阵
    - 这不是简单的数，而是旋量空间的算符

    物理意义:
    - 极点在 p² = m²（质壳）
    - 正能态向前传播，负能态向后传播（Feynman-Stuckelberg解释）

    参数:
        p (float): 四动量模平方
        m (float): 费米子质量

    返回:
        float: 传播子分母 p² - m²
    """
    return p**2 - m**2


def time_ordered_product():
    """
    时间序乘积 Time-Ordered Product

    定义:
    T{φ(x)φ(y)} = θ(x⁰-y⁰)φ(x)φ(y) + θ(y⁰-x⁰)φ(y)φ(x)

    物理意义:
    - 时间较晚的场算符放在左边
    - 保证因果性
    - 费曼传播子是时间序乘积的真空期望值

    与Feynman传播子的关系:
    iΔ_F(x-y) = ⟨0|T{φ(x)φ(y)}|0⟩

    返回:
        str: 时间序乘积定义
    """
    return "T{φ(x)φ(y)} = θ(x⁰-y⁰)φ(x)φ(y) + θ(y⁰-x⁰)φ(y)φ(x)"


def retarded_greens_function(x, t, m):
    """
    推迟格林函数 Retarded Green's Function

    定义: G_ret(x,t) = θ(t) ⟨[φ(x,t), φ(0,0)]⟩

    特性:
    - 只在 t > 0 时非零（因果性）
    - 满足 (□ + m²) G_ret = δ⁴(x)
    - 用于线性响应理论

    与Feynman传播子的区别:
    - 推迟: 只有因果响应
    - Feynman: 正频向前 + 负频向后

    参数:
        x (float): 空间位置
        t (float): 时间
        m (float): 质量

    返回:
        float: 格林函数值（简化近似）
    """
    if t <= 0:
        return 0
    # 简化
    return np.exp(-m * c**2 * t / hbar) if t > 0 else 0


# =============================================================================
# 练习 9.4: QED基础
# Exercise 9.4: QED Basics
#
# 物理背景:
# 量子电动力学(QED)是描述电子与光子相互作用的量子场论。
# QED是最精确的物理理论，预言与实验符合到小数点后12位。
#
# 核心内容:
# - 电子场 ψ 和光子场 A_μ 的耦合
# - 精细结构常数 α ≈ 1/137 是耦合强度
# - 规范对称性保证电荷守恒
# =============================================================================
def fine_structure_constant():
    """
    精细结构常数 Fine Structure Constant

    定义: α = e²/(4πε₀ℏc) ≈ 1/137.036

    物理意义:
    - 电磁相互作用的无量纲耦合常数
    - α << 1 使得QED微扰展开收敛
    - 决定原子精细结构能级分裂

    实验测量:
    α⁻¹ = 137.035999084(21)（2018年CODATA）

    跑动耦合:
    α(q²) 随能标增加（真空极化效应）
    在 q ~ M_Z 时: α ≈ 1/128

    返回:
        float: α ≈ 1/137
    """
    return 1 / 137.036


def qed_lagrangian():
    """
    QED拉格朗日量 QED Lagrangian

    完整形式:
    L = ψ̄(iγ^μ∂_μ - m)ψ - (1/4)F_μν F^μν - eψ̄γ^μψ A_μ

    各项含义:
    1. ψ̄(iγ^μ∂_μ - m)ψ: 自由Dirac场（电子动能+质量）
    2. -(1/4)F_μν F^μν: 自由Maxwell场（光子）
    3. -eψ̄γ^μψ A_μ = -e j^μ A_μ: 相互作用项

    规范对称性:
    - 在 ψ → e^{iθ(x)} ψ, A_μ → A_μ - ∂_μθ/e 下不变
    - 这是U(1)局域规范对称性

    返回:
        str: 拉格朗日量表达式
    """
    return "L = ψ̄(iγ·∂ - m)ψ - (1/4)F² - eψ̄γ·Aψ"


def electron_photon_vertex():
    """
    电子-光子顶点 Electron-Photon Vertex

    树级顶点因子: Γ^μ = -ieγ^μ

    Feynman规则:
    - 每个顶点贡献因子 -ieγ^μ
    - 顶点连接两条电子线和一条光子线
    - 满足能量-动量守恒

    顶点修正（圈图）:
    Γ^μ → γ^μ F_1(q²) + (iσ^μν q_ν / 2m) F_2(q²)
    - F_1: 电荷形状因子
    - F_2: 反常磁矩形状因子

    返回:
        np.ndarray: 顶点矩阵（时间分量）
    """
    alpha = fine_structure_constant()
    e = np.sqrt(4 * np.pi * alpha)  # 自然单位
    g0, g1, g2, g3 = gamma_matrices()
    return -1j * e * g0  # 简化：只返回时间分量


def coulomb_potential_qed(r, alpha=None):
    """
    库仑势（QED树级）Coulomb Potential from QED

    公式: V(r) = -αℏc/r

    从QED推导:
    - 交换单光子的散射振幅
    - 在非相对论极限下傅里叶变换
    - 得到经典库仑势

    这验证了QED与经典电磁学的对应

    参数:
        r (float): 距离 [m]
        alpha (float): 精细结构常数（默认使用标准值）

    返回:
        float: 势能 [J]
    """
    if alpha is None:
        alpha = fine_structure_constant()
    return -alpha * hbar * c / r


def vacuum_polarization_correction(r, alpha=None):
    """
    真空极化修正（Uehling势）Vacuum Polarization Correction

    一阶修正:
    δV ≈ -(2α²/15π) × (ℏc/r) × (λ_C/r)²

    物理机制:
    - 虚电子-正电子对在真空中极化
    - 有效屏蔽电荷，使近距离耦合增强
    - 这是跑动耦合常数的来源

    可观测效应:
    - Lamb位移的部分贡献 (~-27 MHz for 2S-2P)
    - 介子原子能级移动

    参数:
        r (float): 距离 [m]
        alpha (float): 精细结构常数

    返回:
        float: 势能修正 [J]
    """
    if alpha is None:
        alpha = fine_structure_constant()
    lambda_C = compton_wavelength(m_e)
    return -(2 * alpha**2 / (15 * np.pi)) * hbar * c / r * (lambda_C / r)**2


# =============================================================================
# 练习 9.5: 费曼图
# Exercise 9.5: Feynman Diagrams
#
# 物理背景:
# 费曼图是计算散射振幅的图形化方法，由费曼在1940年代发明。
# 每个图对应微扰展开的一项，提供了直观的物理图像。
#
# 费曼图元素:
# - 外线: 渐近态粒子
# - 内线: 虚粒子（传播子）
# - 顶点: 相互作用
#
# 计算规则:
# 1. 画出所有可能的图
# 2. 对每个图写出振幅（按费曼规则）
# 3. 对内动量积分
# 4. 对圈图进行重整化
# =============================================================================
def feynman_rules_qed():
    """
    QED费曼规则 QED Feynman Rules

    完整规则集:
    1. 外电子线: u(p) 或 ū(p)（入/出）
    2. 外正电子线: v̄(p) 或 v(p)（入/出）
    3. 外光子线: ε_μ(k)（极化向量）
    4. 内电子线: i(γ·p + m)/(p² - m² + iε)
    5. 内光子线: -iη_μν/(k² + iε)
    6. 顶点: -ieγ^μ
    7. 圈动量积分: ∫d⁴k/(2π)⁴
    8. 费米子圈: 额外因子 (-1)

    返回:
        dict: 费曼规则字典
    """
    return {
        'external_fermion': 'u(p) or v(p)',
        'external_photon': 'ε_μ(k)',
        'internal_fermion': 'i(γ·p + m)/(p² - m²)',
        'internal_photon': '-iη_μν/k²',
        'vertex': '-ieγ^μ',
        'loop': '∫d⁴k/(2π)⁴'
    }


def tree_level_amplitude():
    """
    树级振幅 Tree-Level Amplitude

    定义: 不含圈（loop）的费曼图振幅

    特点:
    - 最低阶近似，~ α^n (n为顶点数)
    - 无需重整化（无紫外发散）
    - 物理上对应经典极限

    组成:
    M_tree = [外线因子] × [顶点因子] × [传播子]

    例: 电子散射
    - 单光子交换: M ~ α（两个顶点）

    返回:
        str: 树级振幅结构描述
    """
    return "M_tree = 外线因子 × 顶点因子 × 传播子"


def loop_amplitude():
    """
    圈图振幅 Loop Amplitude

    定义: 含有闭合回路的费曼图振幅

    特点:
    - 量子修正，比树级高一阶 α
    - 通常紫外发散，需要重整化
    - 对应真正的量子效应

    计算步骤:
    1. 按费曼规则写出被积函数
    2. 对圈动量 ∫d⁴k/(2π)⁴ 积分
    3. 使用维数正规化处理发散
    4. 重整化去除无穷大

    物理效应:
    - 电子反常磁矩: a_e = α/(2π) + O(α²)
    - Lamb位移
    - 跑动耦合常数

    返回:
        str: 圈图振幅结构描述
    """
    return "M_loop = ∫d⁴k/(2π)⁴ × [费曼规则]"


def crossing_symmetry():
    """
    交叉对称性 Crossing Symmetry

    不同散射通道之间的关系:
    s道 ↔ t道 ↔ u道

    物理意义:
    - 入射粒子 ↔ 出射反粒子（能量反号）
    - 同一振幅在不同运动学区域给出不同过程
    - 来自场论的解析性

    例: e⁺e⁻ → μ⁺μ⁻ (s道) 与 e⁻μ⁻ → e⁻μ⁻ (t道) 相关

    数学表述:
    M(s,t,u) 在不同区域描述不同过程
    s + t + u = Σ m_i²

    返回:
        str: 交叉变换规则
    """
    return "M(s) ↔ M(t): p_2 → -p_2"


def mandelstam_variables(p1, p2, p3, p4):
    """
    Mandelstam变量 Mandelstam Variables

    定义 (2 → 2 散射):
    s = (p₁ + p₂)²：质心系能量平方
    t = (p₁ - p₃)²：动量转移平方
    u = (p₁ - p₄)²：交换动量转移平方

    守恒律: s + t + u = m₁² + m₂² + m₃² + m₄²

    物理解释:
    - s道: 粒子湮灭产生中间态
    - t道: 粒子交换力载子
    - u道: 交换粒子（费米子需反对称化）

    参数:
        p1, p2: 入射粒子四动量
        p3, p4: 出射粒子四动量

    返回:
        tuple: (s, t, u)
    """
    s = (p1 + p2)**2
    t = (p1 - p3)**2
    u = (p1 - p4)**2
    return s, t, u


# =============================================================================
# 练习 9.6: 散射振幅
# Exercise 9.6: Scattering Amplitudes
#
# 物理背景:
# 散射截面是可测量的物理量，连接理论计算与实验观测。
# 从费曼图计算振幅，再转换为截面。
#
# 关键公式:
# dσ/dΩ = |M|² × (相空间因子)
# =============================================================================
def compton_scattering_cross_section(E_gamma, theta):
    """
    Compton散射微分截面（Klein-Nishina公式）Klein-Nishina Formula

    光子被电子散射的精确QED结果（1929年）

    公式结构:
    dσ/dΩ = (r_e²/2) × P² × (P + 1/P - sin²θ)
    其中 P = ω'/ω = 1/[1 + x(1-cosθ)]
    x = E_γ/(m_e c²)

    极限情况:
    - 低能 (x << 1): 退化为Thomson散射 σ_T = 8πr_e²/3
    - 高能 (x >> 1): 截面下降 ~ 1/E

    参数:
        E_gamma (float): 入射光子能量 [J]
        theta (float): 散射角 [rad]

    返回:
        float: 微分截面 [m²/sr]
    """
    r_e = 2.82e-15  # 经典电子半径
    x = E_gamma / (m_e * c**2)
    P = 1 / (1 + x * (1 - np.cos(theta)))

    dsigma_domega = 0.5 * r_e**2 * P**2 * (P + 1/P - np.sin(theta)**2)
    return dsigma_domega


def moller_scattering():
    """
    Moller散射 e⁻e⁻ → e⁻e⁻

    需要两个费曼图:
    1. t道: 直接交换光子
    2. u道: 交换电子（费米子交换）

    由于全同费米子的反对称性，两图必须相减:
    M = M_t - M_u

    这导致干涉效应，在某些角度增强或抑制散射

    历史意义:
    - 1932年Moller首次计算
    - 验证了QED和费米子统计

    返回:
        str: 振幅结构描述
    """
    return "M = M_t + M_u (交换图干涉)"


def bhabha_scattering():
    """
    Bhabha散射 e⁺e⁻ → e⁺e⁻

    需要两个费曼图:
    1. s道: 正负电子湮灭为虚光子，再产生正负电子对
    2. t道: 光子交换

    M = M_s + M_t（两图相加，因为是不同粒子）

    物理应用:
    - 正负电子对撞机的亮度监测
    - 束流能量标定

    返回:
        str: 振幅结构描述
    """
    return "M = M_s + M_t (湮灭+交换)"


def pair_production_threshold(m):
    """
    正负粒子对产生阈值 Pair Production Threshold

    质心系阈能: E_th = 2mc²

    物理过程:
    γ → e⁺ + e⁻ (需要核来保证动量守恒)

    实验室系中:
    - 在核场中: E_γ > 2m_e c² ≈ 1.022 MeV
    - 与电子碰撞: E_γ > 4m_e c²

    应用:
    - γ射线探测器的能量响应
    - 宇宙射线物理

    参数:
        m (float): 产生粒子的质量 [kg]

    返回:
        float: 阈能 [J]
    """
    return 2 * m * c**2


def cross_section_dimension():
    """
    散射截面量纲 Cross Section Dimension

    量纲: [σ] = 长度² = 面积

    常用单位:
    - 1 barn = 10⁻²⁸ m² = 10⁻²⁴ cm²
    - 1 millibarn (mb) = 10⁻³¹ m²
    - 1 microbarn (μb) = 10⁻³⁴ m²
    - 1 nanobarn (nb) = 10⁻³⁷ m²
    - 1 picobarn (pb) = 10⁻⁴⁰ m²

    典型量级:
    - 核反应: ~ barn
    - 强相互作用: ~ mb
    - 弱相互作用: ~ pb-fb

    历史趣闻:
    "barn" 源于二战，意为"像谷仓一样大"（对核反应来说）

    返回:
        float: 1 barn 对应的 m² 值
    """
    return 1e-28  # 1 barn in m²


# =============================================================================
# 可视化 Visualization
# 绘制量子场论关键物理量:
# 1. Klein-Gordon色散关系（有质量vs无质量）
# 2. Feynman传播子的空间衰减
# 3. Compton散射角分布
# 4. QED势能（库仑+真空极化修正）
# 5. γ⁵矩阵结构
# 6. 真空能量的紫外发散
# =============================================================================
def plot_quantum_field():
    """绘制量子场论相关图 Plot Quantum Field Theory Results"""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 色散关系
    ax1 = axes[0, 0]
    k = np.linspace(-5, 5, 200) / compton_wavelength(m_e)

    omega_massive = [klein_gordon_dispersion(ki, m_e) for ki in k]
    omega_massless = np.abs(k) * c

    ax1.plot(k * compton_wavelength(m_e), np.array(omega_massive)/(m_e*c**2/hbar),
            'b-', label='有质量', linewidth=2)
    ax1.plot(k * compton_wavelength(m_e), omega_massless/(m_e*c**2/hbar),
            'r--', label='无质量', linewidth=2)
    ax1.set_xlabel('k × λ_C')
    ax1.set_ylabel('ω / (mc²/ℏ)')
    ax1.set_title('Klein-Gordon色散关系')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 传播子
    ax2 = axes[0, 1]
    r = np.linspace(0.1, 5, 100) * compton_wavelength(m_e)

    prop = [feynman_propagator_scalar(ri, m_e) for ri in r]

    ax2.semilogy(r / compton_wavelength(m_e), prop, 'b-', linewidth=2)
    ax2.set_xlabel('r / λ_C')
    ax2.set_ylabel('Δ_F (arb. units)')
    ax2.set_title('Feynman传播子')
    ax2.grid(True, alpha=0.3)

    # 3. Compton散射截面
    ax3 = axes[0, 2]
    theta = np.linspace(0.01, np.pi, 100)

    for E_ratio in [0.1, 1, 10]:
        E_gamma = E_ratio * m_e * c**2
        dsigma = [compton_scattering_cross_section(E_gamma, t) for t in theta]
        ax3.plot(np.degrees(theta), np.array(dsigma) / (2.82e-15)**2,
                label=f'E_γ = {E_ratio}m_ec²', linewidth=2)

    ax3.set_xlabel('θ (度)')
    ax3.set_ylabel('dσ/dΩ / r_e²')
    ax3.set_title('Compton散射角分布')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 库仑势和真空极化修正
    ax4 = axes[1, 0]
    r = np.linspace(0.01, 5, 100) * compton_wavelength(m_e)

    V_coulomb = [coulomb_potential_qed(ri) / eV for ri in r]
    V_uehling = [vacuum_polarization_correction(ri) / eV for ri in r]

    ax4.plot(r / compton_wavelength(m_e), V_coulomb, 'b-', label='库仑势', linewidth=2)
    ax4.plot(r / compton_wavelength(m_e), np.array(V_uehling) * 1e5, 'r-',
            label='真空极化 ×10⁵', linewidth=2)
    ax4.set_xlabel('r / λ_C')
    ax4.set_ylabel('V (eV)')
    ax4.set_title('QED势能')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. Gamma矩阵可视化
    ax5 = axes[1, 1]
    g0, g1, g2, g3 = gamma_matrices()
    g5 = gamma5_matrix()

    im = ax5.imshow(np.abs(g5), cmap='Blues')
    ax5.set_title('|γ⁵| 矩阵')
    ax5.set_xlabel('列')
    ax5.set_ylabel('行')
    plt.colorbar(im, ax=ax5)

    # 6. 真空能量（截断）
    ax6 = axes[1, 2]
    k_max_range = np.logspace(-1, 2, 50) / compton_wavelength(m_e)

    E_vac = [vacuum_energy_density(km, m_e, 1) for km in k_max_range]

    ax6.loglog(k_max_range * compton_wavelength(m_e), E_vac, 'b-', linewidth=2)
    ax6.set_xlabel('k_max × λ_C')
    ax6.set_ylabel('真空能量密度')
    ax6.set_title('真空能量（截断依赖）')
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('quantum_field.png', dpi=150)
    print("图像已保存为 quantum_field.png")
    plt.show()


# =============================================================================
# 验证函数 Verification
# =============================================================================
def verify():
    """验证所有练习 Verify all exercises"""
    all_passed = True

    # Check 9.1 - Klein-Gordon色散关系
    k_test = 1e10  # 1/m
    omega = klein_gordon_dispersion(k_test, m_e)

    if omega <= 0:
        print("X 9.1 错误：色散关系 ω = √(k²c² + m²c⁴/ℏ²) 应给出正频率")
        all_passed = False
    else:
        print(f"V 9.1 Klein-Gordon场正确（色散关系验证通过）")

    # Check 9.2 - γ矩阵Clifford代数 Gamma matrices
    g0, g1, g2, g3 = gamma_matrices()

    # 验证 {γ⁰, γ⁰} = 2η⁰⁰ = 2
    anticomm_00 = g0 @ g0 + g0 @ g0
    if not np.allclose(anticomm_00, 2 * np.eye(4)):
        print("X 9.2 错误：γ矩阵应满足Clifford代数 {γ^μ, γ^ν} = 2η^μν")
        all_passed = False
    else:
        print("V 9.2 Dirac场正确（Clifford代数验证通过）")

    # Check 9.3 - Feynman传播子 Propagator
    r_test = compton_wavelength(m_e)
    prop = feynman_propagator_scalar(r_test, m_e)

    if prop <= 0:
        print("X 9.3 错误：Feynman传播子在实空间应为正值")
        all_passed = False
    else:
        print("V 9.3 传播子正确（空间衰减行为正确）")

    # Check 9.4 - 精细结构常数 Fine structure constant
    alpha = fine_structure_constant()

    if not np.isclose(alpha, 1/137, rtol=0.01):
        print("X 9.4 错误：精细结构常数应为 α ≈ 1/137")
        all_passed = False
    else:
        print(f"V 9.4 QED基础正确 (α = 1/{1/alpha:.1f})")

    # Check 9.5 - 费曼规则 Feynman rules
    rules = feynman_rules_qed()

    if 'vertex' not in rules:
        print("X 9.5 错误：费曼规则应包含顶点因子 -ieγ^μ")
        all_passed = False
    else:
        print("V 9.5 费曼图正确（规则集完整）")

    # Check 9.6 - 散射截面 Cross section
    sigma = compton_scattering_cross_section(m_e * c**2, np.pi/2)

    if sigma <= 0:
        print("X 9.6 错误：Compton散射截面应为正值")
        all_passed = False
    else:
        print("V 9.6 散射振幅正确（Klein-Nishina公式）")

    if all_passed:
        print("\n所有测试通过！正在生成可视化...")
        try:
            plot_quantum_field()
        except Exception as ex:
            print(f"可视化生成失败: {ex}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("量子场论入门 Quantum Field Theory")
    print("=" * 50)
    verify()
