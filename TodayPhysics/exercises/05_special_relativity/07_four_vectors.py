"""
四矢量与张量 Four-Vectors and Tensors
难度 Difficulty: ★★★★

学习目标 Learning Objectives:
- 理解四矢量的定义和洛伦兹变换性质
  Understand four-vector definitions and Lorentz transformation properties
- 掌握闵可夫斯基度规和内积计算
  Master Minkowski metric and inner product calculations
- 分析能量-动量四矢量及其不变量
  Analyze energy-momentum four-vector and its invariants
- 应用四矢量方法解决相对论问题
  Apply four-vector methods to solve relativistic problems

物理背景 Physical Background:
四矢量是狭义相对论的数学基础。在四维时空中，物理量被组织成四矢量，
在洛伦兹变换下保持协变性（变换规律简单一致）。

闵可夫斯基度规 Minkowski Metric:
η_μν = diag(1, -1, -1, -1) 或 diag(-1, 1, 1, 1)（符号约定不同）
本文件使用 (+,-,-,-) 约定。

四矢量内积:
A·B = η_μν A^μ B^ν = A⁰B⁰ - A¹B¹ - A²B² - A³B³
内积是洛伦兹标量（不变量）。

常见四矢量:
- 四位置: x^μ = (ct, x, y, z)
- 四速度: u^μ = γ(c, v_x, v_y, v_z)，满足 u·u = c²
- 四动量: p^μ = (E/c, p_x, p_y, p_z)，满足 p·p = (mc)²
- 四力: f^μ = dp^μ/dτ

关键公式 Key Formulas:
- 度规: η = diag(1, -1, -1, -1)
- 四矢量内积: A·B = A⁰B⁰ - A¹B¹ - A²B² - A³B³
- 四速度归一化: u·u = c²
- 四动量不变量: p·p = (mc)²
- 洛伦兹变换矩阵: x'^μ = Λ^μ_ν x^ν

单位说明 Units:
- 四位置: (m, m, m, m) 或 (s, m, m, m)（取决于 x⁰ = ct 或 t）
- 四动量: (kg·m/s, kg·m/s, kg·m/s, kg·m/s) 或自然单位
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import c, m_e, m_p, eV, MeV, GeV

# I AM NOT DONE

# 闵可夫斯基度规 (符号约定: +---)
eta = np.diag([1, -1, -1, -1])

# =============================================================================
# 练习 7.1: 四矢量基础
# Exercise 7.1: Four-Vector Basics
#
# 物理背景：四矢量是狭义相对论的核心数学工具
#
# 四矢量内积：
# 使用闵可夫斯基度规 η = diag(1, -1, -1, -1)
# A·B = η_μν A^μ B^ν = A⁰B⁰ - A¹B¹ - A²B² - A³B³
#
# 重要性质：四矢量内积是洛伦兹不变量！
# 在所有惯性系中，A·B 的值相同
#
# 四矢量分类：
# - 类时 (timelike): A·A > 0，可以是有质量粒子的四动量
# - 类空 (spacelike): A·A < 0，连接类空分离的事件
# - 类光 (lightlike/null): A·A = 0，光子的四动量
#
# Physical background: Four-vectors and Minkowski inner product
# =============================================================================
def four_vector_inner_product(A, B):
    """
    四矢量内积（使用闵可夫斯基度规）Four-vector inner product

    公式 Formula: A·B = η_μν A^μ B^ν = A⁰B⁰ - A¹B¹ - A²B² - A³B³

    参数 Parameters:
        A, B: 四维数组 [A⁰, A¹, A², A³]

    返回 Returns:
        标量: A·B（洛伦兹不变量）

    注意：
    - 使用 (+,-,-,-) 度规约定
    - 结果可正、可负、可为零
    - 在所有惯性系中值相同
    """
    A = np.array(A)
    B = np.array(B)
    return A[0]*B[0] - A[1]*B[1] - A[2]*B[2] - A[3]*B[3]

def four_vector_magnitude_squared(A):
    """
    四矢量的模方 Squared magnitude of four-vector

    公式 Formula: A² = A·A = (A⁰)² - (A¹)² - (A²)² - (A³)²

    返回 Returns:
        A² (可正、负或零)

    物理意义：
    - 对于四动量: p² = (E/c)² - p² = (mc)²
    - 对于时空间隔: ds² = c²dt² - dx² - dy² - dz²
    """
    return four_vector_inner_product(A, A)

def is_timelike(A):
    """
    判断四矢量是否类时 Check if timelike

    判据 Criterion: A·A > 0

    物理意义：
    - 有质量粒子的四动量是类时的
    - 类时间隔表示可以用亚光速信号连接的事件对
    - 类时区域在光锥内部
    """
    return four_vector_magnitude_squared(A) > 0

def is_spacelike(A):
    """
    判断四矢量是否类空 Check if spacelike

    判据 Criterion: A·A < 0

    物理意义：
    - 类空间隔表示不能用任何信号连接的事件对
    - 类空区域在光锥外部
    - 存在参考系使得两事件同时发生
    """
    return four_vector_magnitude_squared(A) < 0

def is_lightlike(A):
    """
    判断四矢量是否类光（光锥上）Check if lightlike/null

    判据 Criterion: A·A = 0

    物理意义：
    - 光子的四动量是类光的
    - 光锥本身：ds² = 0
    - 只有光信号能连接的事件对
    """
    return np.isclose(four_vector_magnitude_squared(A), 0, atol=1e-10)


# =============================================================================
# 练习 7.2: 四位置和固有时
# Exercise 7.2: Four-Position and Proper Time
#
# 物理背景：四位置是时空中事件的坐标
#
# 四位置定义：
# x^μ = (ct, x, y, z) 或 (x⁰, x¹, x², x³)
# 注意第零分量是 ct 而非 t，这使所有分量有相同量纲
#
# 时空间隔：
# ds² = c²dt² - dx² - dy² - dz² = η_μν dx^μ dx^ν
# 这是闵可夫斯基时空中的"距离"
#
# 固有时与时空间隔的关系：
# - 类时间隔 (ds² > 0): dτ = ds/c，代表时钟测量的时间
# - 类空间隔 (ds² < 0): 不能定义固有时
# - 类光间隔 (ds² = 0): 光子的世界线，固有时为零
#
# Physical background: Four-position and spacetime intervals
# =============================================================================
def four_position(t, x, y, z):
    """
    四位置矢量 Four-position vector

    公式 Formula: x^μ = (ct, x, y, z)

    参数 Parameters:
        t: 时间坐标 (s)
        x, y, z: 空间坐标 (m)

    返回 Returns:
        四维数组 [ct, x, y, z] (m, m, m, m)

    说明：使用 ct 作为第零分量使所有分量量纲统一
    """
    return np.array([c * t, x, y, z])

def spacetime_interval(x1, x2):
    """
    时空间隔 Spacetime interval

    公式 Formula: Δs² = c²Δt² - Δx² - Δy² - Δz²

    参数 Parameters:
        x1, x2: 两个四位置矢量

    返回 Returns:
        Δs²: 时空间隔的平方 (m²)

    分类：
    - Δs² > 0: 类时间隔，两事件可以因果联系
    - Δs² < 0: 类空间隔，两事件不能因果联系
    - Δs² = 0: 类光间隔，只有光能连接
    """
    dx = np.array(x2) - np.array(x1)
    return four_vector_magnitude_squared(dx)

def proper_time_interval(x1, x2):
    """
    固有时间隔 Proper time interval

    公式 Formula: Δτ = √(Δs²)/c（类时间隔时有效）

    参数 Parameters:
        x1, x2: 两个四位置矢量

    返回 Returns:
        Δτ: 固有时间隔 (s)，类空或类光时返回 0

    物理意义：
    - 固有时是沿世界线运动的时钟测量的时间
    - 它是洛伦兹不变量，所有观测者同意其值
    - 惯性运动（直线世界线）的固有时最长
    """
    ds_squared = spacetime_interval(x1, x2)
    if ds_squared <= 0:
        return 0  # 类空或类光间隔无固有时
    return np.sqrt(ds_squared) / c


# =============================================================================
# 练习 7.3: 四速度
# Exercise 7.3: Four-Velocity
#
# 物理背景：四速度是粒子在时空中的"速度"
#
# 四速度定义：
# u^μ = dx^μ/dτ = γ(c, vx, vy, vz)
# 其中 τ 是固有时，v 是三速度
#
# 关键性质：
# 四速度的模方是常数！
# u·u = γ²(c² - v²) = γ²c²(1 - β²) = c²
#
# 这是洛伦兹变换保持的约束条件
# 无论粒子如何运动，u·u = c² 恒成立
#
# 与三速度的区别：
# - 三速度 v 可以从 0 到 c
# - 四速度的模恒为 c
# - 四速度各分量可以任意大（γ → ∞ 时）
#
# Physical background: Four-velocity and its normalization
# =============================================================================
def gamma_factor(v):
    """
    洛伦兹因子 Lorentz factor

    公式 Formula: γ = 1/√(1 - v²/c²) = 1/√(1 - β²)

    参数 Parameters:
        v: 三速度大小 (m/s)

    返回 Returns:
        γ: 洛伦兹因子（≥ 1）

    性质：
    - v = 0: γ = 1
    - v → c: γ → ∞
    - γ 出现在几乎所有相对论公式中
    """
    beta = v / c
    return 1 / np.sqrt(1 - beta**2)

def four_velocity(vx, vy, vz):
    """
    四速度 Four-velocity

    公式 Formula: u^μ = γ(c, vx, vy, vz)

    参数 Parameters:
        vx, vy, vz: 三速度分量 (m/s)

    返回 Returns:
        四维数组 [γc, γvx, γvy, γvz] (m/s)

    归一化条件：u·u = c²（恒成立）

    静止粒子 (v=0): u^μ = (c, 0, 0, 0)
    高速粒子 (v→c): u⁰ → ∞，但 u·u = c² 不变
    """
    v = np.sqrt(vx**2 + vy**2 + vz**2)
    gamma = gamma_factor(v)
    return np.array([gamma * c, gamma * vx, gamma * vy, gamma * vz])

def four_velocity_magnitude_squared(u):
    """
    四速度的模方 Squared magnitude of four-velocity

    公式 Formula: u·u = (u⁰)² - (u¹)² - (u²)² - (u³)²

    返回 Returns:
        u·u（应该恒等于 c²）

    验证：这个函数可以用来验证四速度计算是否正确
    如果 |u·u - c²| > ε，说明计算有误
    """
    return four_vector_magnitude_squared(u)


# =============================================================================
# 练习 7.4: 四动量
# Exercise 7.4: Four-Momentum
#
# 物理背景：四动量是粒子的核心属性
#
# 四动量定义：
# p^μ = mu^μ = (E/c, px, py, pz)
# 其中 E = γmc² 是总能量，p = γmv 是相对论动量
#
# 质壳条件 Mass-shell condition:
# p·p = (E/c)² - |p|² = (mc)²
# 这是能量-动量关系 E² = (pc)² + (mc²)² 的四矢量形式
#
# 光子的四动量:
# 光子质量为零，p·p = 0，但 E = pc ≠ 0
# p^μ = (E/c, E/c × n̂)，其中 n̂ 是传播方向单位矢量
#
# 守恒律：
# 在碰撞或衰变中，总四动量守恒：Σp^μ_initial = Σp^μ_final
# 这同时包含了能量守恒和动量守恒
#
# Physical background: Four-momentum and mass-shell condition
# =============================================================================
def four_momentum(m, vx, vy, vz):
    """
    四动量 Four-momentum

    公式 Formula: p^μ = mu^μ = (E/c, px, py, pz)

    参数 Parameters:
        m: 静止质量 (kg)
        vx, vy, vz: 三速度分量 (m/s)

    返回 Returns:
        四维数组 [E/c, px, py, pz] (kg·m/s)

    质壳条件：p·p = (mc)²（有质量粒子）
    无质量粒子：p·p = 0

    注意：第零分量是 E/c 而非 E，保持量纲一致
    """
    u = four_velocity(vx, vy, vz)
    return m * u

def energy_from_four_momentum(p):
    """
    从四动量提取能量 Extract energy from four-momentum

    公式 Formula: E = c × p⁰

    参数 Parameters:
        p: 四动量数组 [E/c, px, py, pz]

    返回 Returns:
        E: 总能量 (J)

    这是提取四动量第零分量并恢复正确单位
    """
    return c * p[0]

def momentum_from_four_momentum(p):
    """
    从四动量提取三动量 Extract three-momentum from four-momentum

    公式 Formula: p_3D = (p¹, p², p³)

    参数 Parameters:
        p: 四动量数组 [E/c, px, py, pz]

    返回 Returns:
        三维数组 [px, py, pz] (kg·m/s)

    这是提取四动量的空间分量
    """
    return p[1:4]

def invariant_mass(p):
    """
    不变质量 Invariant mass

    公式 Formula: m = √(p·p)/c = √((E/c)² - |p|²)/c

    参数 Parameters:
        p: 四动量数组

    返回 Returns:
        m: 不变质量 (kg)

    物理意义：
    - 单粒子：返回静止质量
    - 多粒子系统：返回系统的不变质量（质心系总质量）
    - 洛伦兹不变量，所有参考系中值相同
    """
    p_squared = four_vector_magnitude_squared(p)
    return np.sqrt(p_squared) / c


# =============================================================================
# 练习 7.5: 洛伦兹变换矩阵
# Exercise 7.5: Lorentz Transformation Matrix
#
# 物理背景：洛伦兹变换是狭义相对论的数学核心
#
# 洛伦兹推进 (Boost):
# 从一个惯性系变换到相对运动的另一个惯性系
# x'^μ = Λ^μ_ν x^ν（矩阵乘法）
#
# 沿 x 方向的推进矩阵:
# Λ = | γ    -βγ   0   0 |
#     |-βγ    γ    0   0 |
#     | 0     0    1   0 |
#     | 0     0    0   1 |
#
# 重要性质：
# 1. Λ(v)·Λ(-v) = I（逆变换）
# 2. det(Λ) = 1（保持定向）
# 3. Λᵀ η Λ = η（保持度规）
#
# 一般方向的推进更复杂，涉及旋转和推进的组合
#
# Physical background: Lorentz transformation matrices
# =============================================================================
def lorentz_boost_x(v):
    """
    沿 x 方向的洛伦兹推进矩阵 Lorentz boost matrix along x

    公式 Formula:
    Λ = | γ    -βγ   0   0 |
        |-βγ    γ    0   0 |
        | 0     0    1   0 |
        | 0     0    0   1 |

    参数 Parameters:
        v: 新参考系相对原参考系沿 x 方向的速度 (m/s)

    返回 Returns:
        4×4 洛伦兹变换矩阵

    应用：x'^μ = Λ^μ_ν x^ν
    逆变换：Λ(-v) 或 Λ⁻¹
    """
    beta = v / c
    gamma = gamma_factor(v)

    Lambda = np.array([
        [gamma, -beta*gamma, 0, 0],
        [-beta*gamma, gamma, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    return Lambda

def lorentz_boost_general(v_vec):
    """
    一般方向的洛伦兹推进 General Lorentz boost

    参数 Parameters:
        v_vec: 三维速度矢量 [vx, vy, vz] (m/s)

    返回 Returns:
        4×4 洛伦兹变换矩阵

    公式（分量形式）:
    Λ⁰₀ = γ
    Λ⁰ᵢ = Λⁱ₀ = -βγnᵢ
    Λⁱⱼ = δⁱⱼ + (γ-1)nᵢnⱼ

    其中 nᵢ 是速度方向的单位矢量分量

    注意：这比沿坐标轴的推进复杂，空间分量混合变换
    """
    v = np.linalg.norm(v_vec)
    if v < 1e-10:
        return np.eye(4)  # 无运动，返回单位矩阵

    n = v_vec / v  # 速度方向单位矢量
    beta = v / c
    gamma = gamma_factor(v)

    Lambda = np.eye(4)
    Lambda[0, 0] = gamma
    Lambda[0, 1:4] = -beta * gamma * n
    Lambda[1:4, 0] = -beta * gamma * n

    # 空间-空间分量
    for i in range(3):
        for j in range(3):
            Lambda[i+1, j+1] = (gamma - 1) * n[i] * n[j]
            if i == j:
                Lambda[i+1, j+1] += 1

    return Lambda

def transform_four_vector(A, Lambda):
    """
    对四矢量应用洛伦兹变换 Apply Lorentz transformation

    公式 Formula: A'^μ = Λ^μ_ν A^ν

    参数 Parameters:
        A: 原四矢量（四维数组）
        Lambda: 4×4 洛伦兹变换矩阵

    返回 Returns:
        A': 变换后的四矢量

    应用示例：
    - 变换四位置（时空坐标变换）
    - 变换四动量（能量动量变换）
    - 变换电磁场（场变换）
    """
    return Lambda @ np.array(A)


# =============================================================================
# 练习 7.6: 能量-动量守恒
# Exercise 7.6: Energy-Momentum Conservation
#
# 物理背景：四动量守恒统一了能量守恒和动量守恒
#
# 四动量守恒：
# Σp^μ_initial = Σp^μ_final
# 这一个方程同时表达：
# - μ=0: 能量守恒 ΣE_i = ΣE_f
# - μ=1,2,3: 三动量守恒 Σp_i = Σp_f
#
# 质心系能量 √s:
# s = (Σp)² = (Σp)·(Σp) 是洛伦兹不变量
# √s = E_cm 是质心系总能量
# 这是粒子物理实验的关键参数
#
# 阈能计算：
# 利用 √s_min = Σm_products × c² 和四动量守恒
# 可以计算产生新粒子所需的最小束流能量
#
# Physical background: Four-momentum conservation in reactions
# =============================================================================
def total_four_momentum(particles):
    """
    计算粒子系统的总四动量 Total four-momentum of a system

    公式 Formula: P^μ_total = Σ p^μ_i

    参数 Parameters:
        particles: 四动量列表 [[E₁/c, p1x, p1y, p1z], ...]

    返回 Returns:
        P_total: 总四动量（四维数组）

    物理意义：
    - 封闭系统的总四动量守恒
    - P_total·P_total = s 是洛伦兹不变量
    - √s 是质心系总能量
    """
    p_total = np.zeros(4)
    for p in particles:
        p_total += np.array(p)
    return p_total

def center_of_mass_energy(p_total):
    """
    质心系能量 Center of mass energy

    公式 Formula: E_cm = c√(P_total · P_total) = √s

    参数 Parameters:
        p_total: 总四动量数组

    返回 Returns:
        E_cm: 质心系总能量 (J)

    物理意义：
    - 在质心系中，总动量为零
    - 所有能量都是"可用能量"
    - √s 是粒子物理实验的核心参数
    - LHC: √s = 13-14 TeV
    """
    s = four_vector_magnitude_squared(p_total)
    return c * np.sqrt(s)

def threshold_energy(m_products, m_target, m_beam):
    """
    粒子反应阈能 Threshold energy for particle production

    反应 Reaction: beam + target → products

    公式 Formula:
    E_th = [(Σm_f)² - m_beam² - m_target²]c⁴ / (2m_target c²)

    参数 Parameters:
        m_products: 产物质量列表 [m₁, m₂, ...] (kg)
        m_target: 靶粒子质量（静止）(kg)
        m_beam: 束流粒子质量 (kg)

    返回 Returns:
        E_th: 阈值能量（束流粒子总能量）(J)

    推导：
    1. 在阈值处，产物在质心系中都静止
    2. √s_min = Σm_products × c²
    3. 固定靶: s = 2m_target E_beam + (m_beam c²)² + (m_target c²)²
    4. 联立求解得 E_th

    示例：反质子产生 p + p → 4p，E_th = 7m_p c² ≈ 6.6 GeV
    """
    sum_m_products = sum(m_products)
    E_th = ((sum_m_products**2 - m_beam**2 - m_target**2) * c**4) / (2 * m_target * c**2)
    return E_th


# =============================================================================
# 可视化
# =============================================================================
def plot_four_vectors():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 四矢量类型（光锥图）
    ax1 = axes[0, 0]
    t = np.linspace(-2, 2, 100)
    x = np.linspace(-2, 2, 100)
    T, X = np.meshgrid(t, x)

    # 光锥: ct = ±x
    ax1.plot([-2, 0, 2], [-2, 0, 2], 'r-', linewidth=2, label='光锥')
    ax1.plot([-2, 0, 2], [2, 0, -2], 'r-', linewidth=2)
    ax1.fill_between(t, t, 2, alpha=0.2, color='blue', label='类时（未来）')
    ax1.fill_between(t, -2, t, where=(t > -t), alpha=0.2, color='green', label='类空')
    ax1.set_xlabel('x/c')
    ax1.set_ylabel('ct')
    ax1.set_title('闵可夫斯基时空')
    ax1.set_xlim(-2, 2)
    ax1.set_ylim(-2, 2)
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)
    ax1.set_aspect('equal')

    # 2. 四速度vs三速度
    ax2 = axes[0, 1]
    v = np.linspace(0, 0.99*c, 100)
    gamma = [gamma_factor(vi) for vi in v]
    u0 = [g * c for g in gamma]

    ax2.plot(v/c, u0, 'b-', linewidth=2, label='u⁰ = γc')
    ax2.plot(v/c, np.array(gamma) * v, 'r-', linewidth=2, label='u¹ = γv')
    ax2.set_xlabel('v/c')
    ax2.set_ylabel('四速度分量')
    ax2.set_title('四速度')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 相对论动量
    ax3 = axes[0, 2]
    m = m_e
    E = [gamma_factor(vi) * m * c**2 / MeV for vi in v]
    p_mag = [gamma_factor(vi) * m * vi * c / MeV for vi in v]

    ax3.plot(v/c, E, 'b-', linewidth=2, label='E (MeV)')
    ax3.plot(v/c, p_mag, 'r-', linewidth=2, label='pc (MeV)')
    ax3.set_xlabel('v/c')
    ax3.set_ylabel('能量/动量 (MeV)')
    ax3.set_title('相对论能量-动量')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 洛伦兹变换
    ax4 = axes[1, 0]
    # 变换一系列事件
    events_t = np.linspace(-1, 1, 20)
    events_x = np.zeros(20)

    v_boost = 0.5 * c
    Lambda = lorentz_boost_x(v_boost)

    t_prime = []
    x_prime = []
    for t_ev, x_ev in zip(events_t, events_x):
        event = four_position(t_ev, x_ev, 0, 0)
        event_prime = transform_four_vector(event, Lambda)
        t_prime.append(event_prime[0] / c)
        x_prime.append(event_prime[1])

    ax4.scatter(events_x, events_t, c='blue', s=50, label='原始')
    ax4.scatter(x_prime, t_prime, c='red', s=50, label='变换后 (v=0.5c)')
    ax4.set_xlabel('x')
    ax4.set_ylabel('t')
    ax4.set_title('洛伦兹变换效果')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 不变质量
    ax5 = axes[1, 1]
    # 双粒子系统
    E_beam = np.linspace(1, 10, 100) * m_p * c**2
    m_inv = []

    for E in E_beam:
        # 束粒子四动量
        p_beam_mag = np.sqrt(E**2 - (m_p * c**2)**2) / c
        p_beam = np.array([E/c, p_beam_mag, 0, 0])
        # 靶粒子静止
        p_target = np.array([m_p * c, 0, 0, 0])

        p_total = p_beam + p_target
        m_cm = invariant_mass(p_total)
        m_inv.append(m_cm / m_p)

    ax5.plot(E_beam / (m_p * c**2), m_inv, 'b-', linewidth=2)
    ax5.set_xlabel('E_beam / m_p c²')
    ax5.set_ylabel('不变质量 / m_p')
    ax5.set_title('双粒子系统不变质量')
    ax5.grid(True, alpha=0.3)

    # 6. 四动量守恒示意
    ax6 = axes[1, 2]
    # 康普顿散射
    angles = np.linspace(0, np.pi, 100)

    # 入射光子能量
    E_gamma = 0.511 * MeV  # 等于电子静止质量能

    E_scattered = []
    for theta in angles:
        # 康普顿公式
        E_s = E_gamma / (1 + (E_gamma / (m_e * c**2)) * (1 - np.cos(theta)))
        E_scattered.append(E_s / MeV)

    ax6.plot(np.degrees(angles), E_scattered, 'b-', linewidth=2)
    ax6.set_xlabel('散射角 (度)')
    ax6.set_ylabel('散射光子能量 (MeV)')
    ax6.set_title('康普顿散射（四动量守恒）')
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('four_vectors.png', dpi=150)
    print("图像已保存为 four_vectors.png")
    plt.show()


def verify():
    """
    验证所有练习的正确性 Verify all exercises

    检查内容 Checks:
    7.1 四矢量内积 (使用闵可夫斯基度规)
    7.2 时空间隔
    7.3 四速度归一化 (u·u = c²)
    7.4 四动量与不变质量
    7.5 洛伦兹变换矩阵的逆
    7.6 质心系能量计算
    """
    all_passed = True

    # 检查 7.1 - 四矢量内积
    A = [2, 1, 0, 0]
    B = [1, 1, 0, 0]
    inner = four_vector_inner_product(A, B)
    expected = 2*1 - 1*1 - 0 - 0  # 使用度规 (+,-,-,-)
    if not np.isclose(inner, expected, rtol=0.01):
        print("错误 7.1 四矢量内积计算错误")
        all_passed = False
    else:
        print(f"通过 7.1 四矢量内积正确 (A·B = {inner})")

    # 检查 7.2 - 时空间隔
    x1 = four_position(0, 0, 0, 0)
    x2 = four_position(1, c*0.5, 0, 0)
    ds2 = spacetime_interval(x1, x2)
    expected_ds2 = (c*1)**2 - (c*0.5)**2
    if not np.isclose(ds2, expected_ds2, rtol=0.01):
        print("错误 7.2 时空间隔计算错误")
        all_passed = False
    else:
        print(f"通过 7.2 时空间隔正确 (ds² > 0，类时间隔)")

    # 检查 7.3 - 四速度归一化
    u = four_velocity(0, 0, 0)  # 静止粒子
    u_squared = four_velocity_magnitude_squared(u)
    if not np.isclose(u_squared, c**2, rtol=0.01):
        print("错误 7.3 四速度模方应等于 c²")
        all_passed = False
    else:
        print(f"通过 7.3 四速度归一化正确 (u·u = c²)")

    # 检查 7.4 - 四动量与不变质量
    p = four_momentum(m_e, 0, 0, 0)
    m_inv = invariant_mass(p)
    if not np.isclose(m_inv, m_e, rtol=0.01):
        print("错误 7.4 静止粒子的不变质量应等于其静止质量")
        all_passed = False
    else:
        print(f"通过 7.4 四动量正确 (静止电子不变质量 = m_e)")

    # 检查 7.5 - 洛伦兹变换矩阵
    Lambda = lorentz_boost_x(0.6 * c)
    Lambda_inv = lorentz_boost_x(-0.6 * c)
    identity_check = Lambda @ Lambda_inv
    if not np.allclose(identity_check, np.eye(4), rtol=0.01):
        print("错误 7.5 洛伦兹变换与其逆的乘积应为单位矩阵")
        all_passed = False
    else:
        print(f"通过 7.5 洛伦兹变换矩阵正确 (Λ(v)·Λ(-v) = I)")

    # 检查 7.6 - 质心系能量
    p_photon = np.array([MeV/c, MeV/c, 0, 0])  # 1 MeV 光子
    p_electron = np.array([m_e*c, 0, 0, 0])     # 静止电子
    p_total = total_four_momentum([p_photon, p_electron])
    E_cm = center_of_mass_energy(p_total)
    if E_cm <= m_e * c**2:
        print("错误 7.6 质心能量应大于电子静止能量")
        all_passed = False
    else:
        print(f"通过 7.6 质心能量正确 (E_cm = {E_cm/MeV:.3f} MeV)")

    if all_passed:
        print("\n所有测试通过！正在生成可视化图像...")
        try:
            plot_four_vectors()
        except Exception as e:
            print(f"可视化生成失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("四矢量与张量 Four-Vectors and Tensors")
    print("=" * 50)
    verify()
