"""
相对论性粒子碰撞 Relativistic Particle Collisions
难度 Difficulty: ★★★★★

学习目标 Learning Objectives:
- 深入理解相对论性能量动量守恒
  Master relativistic energy-momentum conservation
- 掌握不变质量的计算和物理意义
  Understand invariant mass calculation and its physical meaning
- 分析高能碰撞物理和阈值能量
  Analyze high-energy collision physics and threshold energies
- 理解对撞机与固定靶实验的区别
  Understand collider vs fixed-target experiments

物理背景 Physical Background:
高能物理实验通过粒子碰撞研究物质的基本结构。
相对论碰撞遵循四动量守恒：总四动量在碰撞前后不变。

不变质量 Invariant Mass:
粒子系统的不变质量是洛伦兹不变量：
M²c⁴ = (ΣE)² - (Σp·c)²
它等于质心系中系统的总能量除以 c²。

对撞机 vs 固定靶:
- 固定靶: 束流粒子轰击静止靶，√s ∝ √E_beam
- 对撞机: 两束粒子对撞，√s = 2E_beam
- LHC 的 7 TeV 束流相当于 100,000 TeV 固定靶！

阈值能量:
产生新粒子需要的最小能量，由动量守恒和能量守恒共同决定。

关键公式 Key Formulas:
- 能量-动量关系: E² = (pc)² + (mc²)²
- 不变质量: M²c⁴ = (E₁+E₂)² - |p₁+p₂|²c²
- 质心系能量: √s = √(M²c⁴)
- 阈能（固定靶）: E_th = [(Σm_f)² - m_b² - m_t²]c² / (2m_t)

单位说明 Units:
- 能量: eV, keV, MeV, GeV, TeV
- 动量: eV/c, MeV/c, GeV/c
- 质量: eV/c², MeV/c², GeV/c²
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import c, m_e, m_p, eV, MeV, GeV

# I AM NOT DONE

# =============================================================================
# 练习 6.1: 相对论能量动量
# Exercise 6.1: Relativistic Energy-Momentum
#
# 物理背景：相对论力学中，能量和动量的关系与牛顿力学不同
#
# 能量-动量关系（质壳条件 mass-shell condition）:
# E² = (pc)² + (mc²)²
# 这是相对论的基本关系，连接能量、动量和静止质量
#
# 关键公式：
# - 总能量: E = γmc²
# - 动量: p = γmv
# - 动能: T = E - mc² = (γ - 1)mc²
# - 速度: v = pc²/E
#
# 极限情况：
# - 静止 (v=0): E = mc², p = 0
# - 高度相对论 (γ >> 1): E ≈ pc
# - 光子 (m=0): E = pc，永远以光速运动
#
# Physical background: Energy-momentum relations in special relativity
# =============================================================================
def lorentz_factor(v):
    """
    洛伦兹因子 Lorentz factor

    公式 Formula: γ = 1/√(1 - v²/c²)

    这是相对论中最基本的量，出现在所有变换中
    """
    return 1 / np.sqrt(1 - (v/c)**2)


def relativistic_energy(m, v):
    """
    相对论总能量 Relativistic total energy

    公式 Formula: E = γmc²

    参数 Parameters:
        m: 静止质量 (kg)
        v: 速度 (m/s)

    返回 Returns:
        E: 总能量 (J)

    物理意义：
    - 总能量 = 静止能量 + 动能
    - E = mc² + T
    - 即使 v=0，粒子也有能量 mc²（静止能量）
    """
    gamma = lorentz_factor(v)
    return gamma * m * c**2


def relativistic_momentum(m, v):
    """
    相对论动量 Relativistic momentum

    公式 Formula: p = γmv

    参数 Parameters:
        m: 静止质量 (kg)
        v: 速度 (m/s)

    返回 Returns:
        p: 动量 (kg·m/s)

    与牛顿力学的区别：
    - 牛顿: p = mv
    - 相对论: p = γmv
    - 当 v → c 时，p → ∞（无法加速到光速）
    """
    gamma = lorentz_factor(v)
    return gamma * m * v


def kinetic_energy(m, v):
    """
    相对论动能 Relativistic kinetic energy

    公式 Formula: T = (γ - 1)mc²

    参数 Parameters:
        m: 静止质量 (kg)
        v: 速度 (m/s)

    返回 Returns:
        T: 动能 (J)

    低速极限 (v << c):
    γ ≈ 1 + v²/(2c²)
    T ≈ ½mv²（回归牛顿结果）

    高速极限 (v → c):
    T ≈ γmc² → ∞
    """
    gamma = lorentz_factor(v)
    return (gamma - 1) * m * c**2


def energy_from_momentum(p, m):
    """
    从动量计算能量 Energy from momentum

    公式 Formula: E = √((pc)² + (mc²)²)

    参数 Parameters:
        p: 动量 (kg·m/s)
        m: 静止质量 (kg)

    返回 Returns:
        E: 总能量 (J)

    这是能量-动量关系 E² = (pc)² + (mc²)² 的直接应用
    对于光子 (m=0): E = pc
    """
    return np.sqrt((p * c)**2 + (m * c**2)**2)


def momentum_from_energy(E, m):
    """
    从能量计算动量 Momentum from energy

    公式 Formula: p = √(E² - (mc²)²) / c

    参数 Parameters:
        E: 总能量 (J)
        m: 静止质量 (kg)

    返回 Returns:
        p: 动量 (kg·m/s)

    注意：E 必须 ≥ mc²，否则动量为虚数（物理上不允许）
    """
    E_rest = m * c**2
    if E < E_rest:
        return 0
    return np.sqrt(E**2 - E_rest**2) / c


def velocity_from_momentum(p, m):
    """
    从动量计算速度 Velocity from momentum

    公式 Formula: v = pc²/E

    参数 Parameters:
        p: 动量 (kg·m/s)
        m: 静止质量 (kg)

    返回 Returns:
        v: 速度 (m/s)

    推导：从 p = γmv 和 E = γmc² 得 v = pc²/E
    当 m → 0 时，v → c（光子总是以光速运动）
    """
    E = energy_from_momentum(p, m)
    if E == 0:
        return 0
    return p * c**2 / E


# =============================================================================
# 练习 6.2: 不变质量
# Exercise 6.2: Invariant Mass
#
# 物理背景：不变质量是粒子物理中最重要的概念之一
#
# 不变质量定义：
# M²c⁴ = E² - (pc)² = (ΣE)² - |Σp|²c²（多粒子系统）
#
# 关键性质：
# 1. 洛伦兹不变量 - 所有参考系中值相同
# 2. 质心系能量 = Mc²
# 3. 用于识别共振态（如希格斯粒子、Z玻色子等）
#
# 双粒子系统：
# M²c⁴ = (E₁+E₂)² - |p₁+p₂|²c²
# 如果粒子反向运动（θ=π）：总动量小，不变质量大
# 如果粒子同向运动（θ=0）：总动量大，不变质量小
#
# 实验应用：
# - 粒子衰变重建母粒子质量
# - 寻找新粒子（不变质量谱中的峰）
#
# Physical background: Invariant mass - the Lorentz invariant quantity
# =============================================================================
def invariant_mass_two_particles(E1, E2, p1, p2, theta):
    """
    两粒子系统的不变质量 Invariant mass of two particles

    公式 Formula: M²c⁴ = (E₁ + E₂)² - |p₁ + p₂|²c²

    参数 Parameters:
        E1, E2: 两粒子能量 (J)
        p1, p2: 两粒子动量大小 (kg·m/s)
        theta: 两动量之间的夹角 (rad)

    返回 Returns:
        M: 不变质量 (kg)

    物理意义：
    - 不变质量是洛伦兹不变量
    - 它等于质心系中系统的总质量
    - θ = π（对头碰撞）时不变质量最大
    - θ = 0（同向运动）时不变质量最小
    """
    E_total = E1 + E2

    # 处理标量或向量输入
    p1_mag = np.linalg.norm(p1) if hasattr(p1, '__len__') else p1
    p2_mag = np.linalg.norm(p2) if hasattr(p2, '__len__') else p2

    # 余弦定理: |p₁ + p₂|² = |p₁|² + |p₂|² + 2|p₁||p₂|cos(θ)
    p_total_sq = p1_mag**2 + p2_mag**2 + 2 * p1_mag * p2_mag * np.cos(theta)

    M_sq_c4 = E_total**2 - p_total_sq * c**2

    if M_sq_c4 < 0:
        return 0  # 类空情况，物理上对应虚拟粒子
    return np.sqrt(M_sq_c4) / c**2


def invariant_mass_decay_products(E_list, p_vectors):
    """
    多粒子系统的不变质量 Invariant mass from decay products

    公式 Formula: M²c⁴ = (ΣE)² - |Σp|²c²

    参数 Parameters:
        E_list: 各粒子能量列表 (J)
        p_vectors: 各粒子三动量向量列表 [(px, py, pz), ...]

    返回 Returns:
        M: 系统不变质量 (kg)

    应用示例：
    - 希格斯粒子 H → γγ：从两光子重建 H 质量
    - Z玻色子 Z → e⁺e⁻：从电子对重建 Z 质量
    - J/ψ → μ⁺μ⁻：从μ子对重建 J/ψ 质量
    """
    E_total = sum(E_list)

    # 三动量向量求和
    p_total = np.zeros(3)
    for p in p_vectors:
        p_total += np.array(p)

    p_mag_sq = np.dot(p_total, p_total)
    M_sq_c4 = E_total**2 - p_mag_sq * c**2

    if M_sq_c4 < 0:
        return 0
    return np.sqrt(M_sq_c4) / c**2


def mandelstam_s(E1, E2, p1, p2, theta):
    """
    Mandelstam变量 s

    公式 Formula: s = (p₁ + p₂)² = (E₁ + E₂)² - |p₁ + p₂|²c²

    参数 Parameters:
        E1, E2: 两粒子能量 (J)
        p1, p2: 两粒子动量 (kg·m/s)
        theta: 动量夹角 (rad)

    返回 Returns:
        s: Mandelstam s 变量 (J²)

    物理意义：
    - s = (质心系总能量)²
    - √s 称为"质心能量"
    - 对撞机物理中，√s 是最重要的参数
    - LHC 的 √s = 13-14 TeV

    Mandelstam 变量还有 t 和 u，满足 s + t + u = Σm²c⁴
    """
    M_inv = invariant_mass_two_particles(E1, E2, p1, p2, theta)
    return (M_inv * c**2)**2


# =============================================================================
# 练习 6.3: 质心系
# Exercise 6.3: Center of Mass Frame
#
# 物理背景：质心系是粒子物理分析中最重要的参考系
#
# 质心系定义：
# 在质心系中，系统总动量为零：Σp*ᵢ = 0
# 所有能量都可用于产生新粒子
#
# 固定靶 vs 对撞机：
# 固定靶实验：束流粒子轰击静止靶
# - √s = √(2m_target × E_beam × c² + m²c⁴)
# - 高能极限：√s ≈ √(2m_target c² E_beam)
# - 能量利用效率低（大部分动能保持为系统运动）
#
# 对撞机实验：两束粒子对撞
# - √s = 2E_beam（等能量对撞）
# - 能量全部可用于产生新粒子
# - LHC: 7 TeV + 7 TeV → √s = 14 TeV
# - 如用固定靶达到相同 √s 需要 ~100,000 TeV 束流！
#
# Physical background: Center of mass frame analysis
# =============================================================================
def cm_velocity(E1, E2, p1, p2):
    """
    质心系速度（一维情况）CM frame velocity

    公式 Formula: v_cm = (p₁ + p₂)c² / (E₁ + E₂)

    参数 Parameters:
        E1, E2: 两粒子能量 (J)
        p1, p2: 两粒子动量（带符号，同向为正）(kg·m/s)

    返回 Returns:
        v_cm: 质心系相对实验室系的速度 (m/s)

    推导：从四动量变换，要求变换后总动量为零
    """
    return (p1 + p2) * c**2 / (E1 + E2)


def cm_energy(m1, m2, E_lab, p_lab):
    """
    质心系总能量（固定靶碰撞）CM energy for fixed target

    公式 Formula: √s = √(2m₂c²E_lab + (m₁c²)² + (m₂c²)²)

    参数 Parameters:
        m1: 束流粒子质量 (kg)
        m2: 靶粒子质量（静止）(kg)
        E_lab: 束流粒子在实验室系中的能量 (J)
        p_lab: （未使用，为接口一致性保留）

    返回 Returns:
        √s: 质心系总能量 (J)

    高能极限 (E_lab >> m₁c², m₂c²):
    √s ≈ √(2m₂c²E_lab)
    能量标度为 √E_lab 而非 E_lab！
    """
    s = 2 * m2 * c**2 * E_lab + (m1 * c**2)**2 + (m2 * c**2)**2
    return np.sqrt(s)


def available_energy_fixed_target(E_beam, m_beam, m_target):
    """
    固定靶碰撞的可用能量 Available energy in fixed target

    公式 Formula: E_avail = √s - (m₁ + m₂)c²

    参数 Parameters:
        E_beam: 束流能量 (J)
        m_beam: 束流粒子质量 (kg)
        m_target: 靶粒子质量 (kg)

    返回 Returns:
        E_avail: 可用于产生新粒子的能量 (J)

    物理意义：扣除产物最小静止质量后的剩余能量
    这才是真正可以用来产生新粒子的能量
    """
    sqrt_s = cm_energy(m_beam, m_target, E_beam, 0)
    return sqrt_s - (m_beam + m_target) * c**2


def collider_vs_fixed_target(E_beam):
    """
    对撞机 vs 固定靶的能量优势 Collider vs fixed target comparison

    公式 Formula:
    - 对撞机: √s = 2E_beam
    - 固定靶: √s ≈ √(2m_p c² E_beam)

    参数 Parameters:
        E_beam: 单束束流能量 (J)

    返回 Returns:
        (√s_collider, √s_fixed): 两种情况的质心能量 (J)

    数值示例（假设质子束流）:
    E_beam = 7 TeV (LHC):
    - 对撞机: √s = 14 TeV
    - 固定靶: √s ≈ 115 GeV
    - 对撞机优势: 因子 ~120

    这解释了为什么现代高能物理都用对撞机
    """
    # 假设质子-质子碰撞
    sqrt_s_collider = 2 * E_beam
    sqrt_s_fixed = np.sqrt(2 * m_p * c**2 * E_beam)
    return sqrt_s_collider, sqrt_s_fixed


# =============================================================================
# 练习 6.4: 阈值能量
# Exercise 6.4: Threshold Energies
#
# 物理背景：产生新粒子需要达到阈值能量
#
# 阈值条件：
# 在阈值处，所有产物在质心系中静止（动能为零）
# 因此 √s_min = Σm_products × c²
#
# 固定靶阈能公式：
# E_th = [(Σm_f)² - m_beam² - m_target²]c² / (2m_target)
#
# 经典例子：
# 1. 反质子产生 p + p → p + p + p + p̄
#    产物质量 = 4m_p，束流和靶都是质子
#    E_th = 7m_p c² ≈ 6.6 GeV
#
# 2. π⁰介子产生 p + p → p + p + π⁰
#    E_th ≈ 280 MeV（动能）
#
# 3. 希格斯玻色子产生
#    m_H = 125 GeV/c²，需要更复杂的产生机制
#
# Physical background: Threshold energies for particle production
# =============================================================================
def threshold_energy_fixed_target(m_products, m_beam, m_target):
    """
    固定靶反应的阈值能量 Threshold energy for fixed target

    公式 Formula: E_th = [(Σm_f)² - m_beam² - m_target²]c² / (2m_target)

    参数 Parameters:
        m_products: 产物质量列表 [m₁, m₂, ...] (kg)
        m_beam: 束流粒子质量 (kg)
        m_target: 靶粒子质量 (kg)

    返回 Returns:
        E_th: 阈值能量（束流粒子总能量）(J)

    推导：
    1. 阈值处产物在质心系中都静止
    2. √s_min = Σm_f × c²
    3. 固定靶: s = 2m_target × E_beam + m_beam² c⁴ + m_target² c⁴
    4. 联立求解得上述公式
    """
    sum_m_products = sum(m_products)
    E_th = ((sum_m_products**2 - m_beam**2 - m_target**2) * c**2 /
            (2 * m_target))
    return E_th


def pair_production_threshold():
    """
    电子对产生阈值 Pair production threshold

    反应 Reaction: γ + 核 → e⁺ + e⁻ + 核

    公式 Formula: E_th ≈ 2m_e c² = 1.022 MeV

    返回 Returns:
        E_th: 阈值光子能量 (J)

    说明：
    - 光子本身无法直接变成电子对（动量不守恒）
    - 需要原子核提供反冲，吸收多余动量
    - 在核库仑场中，阈值约为 2m_e c² = 1.022 MeV
    - 这是伽马射线探测器的基本原理
    """
    return 2 * m_e * c**2


def antiproton_production_threshold():
    """
    反质子产生阈值 Antiproton production threshold

    反应 Reaction: p + p → p + p + p + p̄

    公式 Formula: E_th = 7m_p c² ≈ 6.57 GeV

    返回 Returns:
        E_th: 阈值能量 (J)

    推导：
    - 产物质量 Σm_f = 4m_p
    - s_min = (4m_p c²)² = 16 m_p² c⁴
    - 固定靶: s = 2m_p E_th + 2(m_p c²)²
    - 联立: E_th = (16 - 2)m_p c²/2 = 7m_p c²

    历史意义：1955年在 Bevatron 加速器发现反质子
    正是根据这个阈值设计的束流能量
    """
    # 详细推导见docstring
    return 7 * m_p * c**2


def pion_production_threshold():
    """
    π⁰介子产生阈值 Pion production threshold

    反应 Reaction: p + p → p + p + π⁰

    返回 Returns:
        E_th: 阈值能量 (J)

    数值：
    - m_π⁰ = 135 MeV/c²
    - E_th ≈ 280 MeV (动能) + 2×938 MeV (静止能量)
    - 总能量约 2.16 GeV

    意义：π介子是最轻的强子，产生阈值最低
    宇宙射线与大气作用的主要产物
    """
    m_pi0 = 135 * MeV / c**2  # π⁰质量约 135 MeV/c²
    m_products = [m_p, m_p, m_pi0]
    return threshold_energy_fixed_target(m_products, m_p, m_p)


# =============================================================================
# 练习 6.5: 衰变运动学
# Exercise 6.5: Decay Kinematics
#
# 物理背景：粒子衰变是高能物理的核心课题
#
# 二体衰变 Two-body decay:
# 母粒子 A → 子粒子 B + C
# 在母粒子静止系中，两子粒子背靠背飞出
# 动量大小由能量-动量守恒唯一确定
#
# 关键公式（母粒子静止系）:
# - 动量: p* = c√[(M² - (m₁+m₂)²)(M² - (m₁-m₂)²)] / (2M)
# - 能量: E₁ = (M² + m₁² - m₂²)c² / (2M)
#
# 如果母粒子在运动：
# 需要用洛伦兹变换将结果变换到实验室系
# 这会导致产物角分布和能量分布的变化
#
# 实验应用：
# - K介子、B介子、D介子衰变
# - 希格斯粒子 H → γγ, ZZ, WW 等
# - 顶夸克 t → Wb
#
# Physical background: Two-body decay kinematics
# =============================================================================
def two_body_decay_momentum(M, m1, m2):
    """
    二体衰变的产物动量（母粒子静止系）Decay momentum in rest frame

    公式 Formula: p* = c√[(M² - (m₁+m₂)²)(M² - (m₁-m₂)²)] / (2M)

    参数 Parameters:
        M: 母粒子质量 (kg)
        m1, m2: 子粒子质量 (kg)

    返回 Returns:
        p*: 子粒子动量大小（两者相等）(kg·m/s)

    物理约束：
    - M ≥ m₁ + m₂（能量守恒）
    - 若 M = m₁ + m₂，则 p* = 0（阈值衰变）
    - 若 m₁ = m₂，公式简化为 p* = c√(M² - 4m²)/(2)
    """
    sum_m = m1 + m2
    diff_m = np.abs(m1 - m2)

    if M < sum_m:
        return 0  # 能量不足，无法衰变

    term1 = M**2 - sum_m**2
    term2 = M**2 - diff_m**2

    return c * np.sqrt(term1 * term2) / (2 * M)


def two_body_decay_energies(M, m1, m2):
    """
    二体衰变产物的能量（母粒子静止系）Decay energies in rest frame

    公式 Formula:
    E₁ = (M² + m₁² - m₂²)c² / (2M)
    E₂ = (M² + m₂² - m₁²)c² / (2M)

    参数 Parameters:
        M: 母粒子质量 (kg)
        m1, m2: 子粒子质量 (kg)

    返回 Returns:
        (E1, E2): 两子粒子能量 (J)

    验证：E₁ + E₂ = Mc²（能量守恒）
    若 m₁ = m₂，则 E₁ = E₂ = Mc²/2
    """
    E1 = (M**2 + m1**2 - m2**2) * c**2 / (2 * M)
    E2 = (M**2 + m2**2 - m1**2) * c**2 / (2 * M)
    return E1, E2


def boost_energy(E_cm, p_cm, v_boost, theta_cm):
    """
    从质心系洛伦兹变换到实验室系（能量）Boost energy to lab frame

    公式 Formula: E_lab = γ(E_cm + v·p_cm·cos(θ))

    参数 Parameters:
        E_cm: 质心系中粒子能量 (J)
        p_cm: 质心系中粒子动量大小 (kg·m/s)
        v_boost: 质心系相对实验室系的速度 (m/s)
        theta_cm: 粒子动量与 boost 方向的夹角（质心系中）(rad)

    返回 Returns:
        E_lab: 实验室系中的能量 (J)

    应用：将衰变产物从母粒子静止系变换到实验室系
    θ = 0: 正向飞出，能量最高
    θ = π: 反向飞出，能量最低
    """
    gamma = lorentz_factor(v_boost)
    return gamma * (E_cm + v_boost * p_cm * np.cos(theta_cm))


def boost_momentum_parallel(E_cm, p_cm, v_boost, theta_cm):
    """
    动量平行分量的洛伦兹变换 Boost parallel momentum component

    公式 Formula: p∥_lab = γ(p_cm·cos(θ) + v·E_cm/c²)

    参数 Parameters:
        E_cm: 质心系能量 (J)
        p_cm: 质心系动量大小 (kg·m/s)
        v_boost: boost 速度 (m/s)
        theta_cm: 动量与 boost 方向夹角 (rad)

    返回 Returns:
        p∥_lab: 实验室系中的平行动量分量 (kg·m/s)

    注意：垂直分量不变: p⊥_lab = p_cm·sin(θ)
    这导致"前向聚焦"效应：高速母粒子的衰变产物集中在前方
    """
    gamma = lorentz_factor(v_boost)
    p_para_cm = p_cm * np.cos(theta_cm)
    return gamma * (p_para_cm + v_boost * E_cm / c**2)


# =============================================================================
# 练习 6.6: Compton散射
# Exercise 6.6: Compton Scattering
#
# 物理背景：Compton散射是光子与电子的非弹性散射
#
# 历史意义：1923年 Compton 实验证明了光的粒子性
# X射线散射后波长变长，只能用光子碰撞解释
#
# Compton公式：
# Δλ = λ_C (1 - cos(θ))
# 其中 λ_C = h/(m_e c) = 2.426 pm 是 Compton 波长
#
# 能量公式：
# E' = E / (1 + (E/m_e c²)(1 - cos(θ)))
#
# 极限情况：
# - θ = 0: 前向散射，E' = E（无能量损失）
# - θ = π: 背向散射，E' 最小，电子获能最大
# - 若 E >> m_e c²，背散射 E' → m_e c²/2 ≈ 0.255 MeV
#
# 应用：
# - X射线和伽马射线探测器
# - 医学成像（CT扫描）
# - 天体物理（逆Compton散射产生高能光子）
#
# Physical background: Compton scattering - photon-electron collision
# =============================================================================
def compton_wavelength_shift(theta):
    """
    Compton波长偏移 Compton wavelength shift

    公式 Formula: Δλ = λ_C (1 - cos(θ))

    参数 Parameters:
        theta: 散射角 (rad)

    返回 Returns:
        Δλ: 波长增加量 (m)

    常数：λ_C = h/(m_e c) = 2.426×10⁻¹² m = 2.426 pm（Compton波长）

    物理意义：
    - Δλ 只取决于散射角，与入射波长无关
    - θ = π 时 Δλ_max = 2λ_C = 4.85 pm
    - 这是量子力学效应的直接证据
    """
    lambda_C = 2.426e-12  # m，电子 Compton 波长
    return lambda_C * (1 - np.cos(theta))


def compton_scattered_energy(E_gamma, theta):
    """
    Compton散射后光子能量 Scattered photon energy

    公式 Formula: E' = E / (1 + (E/m_e c²)(1 - cos(θ)))

    参数 Parameters:
        E_gamma: 入射光子能量 (J)
        theta: 散射角 (rad)

    返回 Returns:
        E': 散射光子能量 (J)

    特殊情况：
    - θ = 0: E' = E（前向，无散射）
    - θ = π/2: E' = E/(1 + E/m_e c²)
    - θ = π: E' = E/(1 + 2E/m_e c²)（背散射，能量损失最大）

    高能极限 (E >> m_e c²):
    背散射时 E' → m_e c²/2 ≈ 0.255 MeV（与入射能量无关！）
    """
    E_e = m_e * c**2
    return E_gamma / (1 + (E_gamma / E_e) * (1 - np.cos(theta)))


def compton_electron_energy(E_gamma, theta):
    """
    Compton散射反冲电子能量 Recoil electron energy

    公式 Formula: T_e = E_γ - E'_γ

    参数 Parameters:
        E_gamma: 入射光子能量 (J)
        theta: 光子散射角 (rad)

    返回 Returns:
        T_e: 反冲电子动能 (J)

    能量守恒：E_γ = E'_γ + T_e + m_e c²（电子静止能量）
    但这里 T_e 定义为动能，所以 T_e = E_γ - E'_γ

    背散射时电子获得最大能量：
    T_e,max = E_γ × 2E_γ/(m_e c² + 2E_γ)
    这是"Compton边"，在探测器能谱中是重要特征
    """
    E_gamma_prime = compton_scattered_energy(E_gamma, theta)
    return E_gamma - E_gamma_prime


def klein_nishina_cross_section_ratio(E_gamma, theta):
    """
    Klein-Nishina截面比值 Klein-Nishina cross section ratio

    公式 Formula: dσ/dΩ ∝ P²(P + 1/P - sin²θ)/2
    其中 P = E'/E 是散射光子与入射光子的能量比

    参数 Parameters:
        E_gamma: 入射光子能量 (J)
        theta: 散射角 (rad)

    返回 Returns:
        相对于 Thomson 截面的比值因子

    物理意义：
    - Klein-Nishina 公式是 Compton 散射的量子电动力学结果
    - 低能极限 (E << m_e c²): 回归 Thomson 散射
    - 高能时: 前向散射增强，后向散射抑制
    - 总截面随能量增加而减小（相对论效应）
    """
    x = E_gamma / (m_e * c**2)
    P = compton_scattered_energy(E_gamma, theta) / E_gamma

    return 0.5 * P**2 * (P + 1/P - np.sin(theta)**2)


# =============================================================================
# 可视化
# =============================================================================
def plot_relativistic_collisions():
    """绘制相对论碰撞相关图"""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 能量-动量关系
    ax1 = axes[0, 0]
    p = np.linspace(0, 5, 100) * m_e * c  # 以 m_e c 为单位

    E_electron = [energy_from_momentum(pi, m_e) for pi in p]
    E_photon = p * c  # 光子

    ax1.plot(p/(m_e*c), np.array(E_electron)/(m_e*c**2), 'b-',
            label='电子', linewidth=2)
    ax1.plot(p/(m_e*c), np.array(E_photon)/(m_e*c**2), 'r--',
            label='光子', linewidth=2)
    ax1.set_xlabel('p/(m_e c)')
    ax1.set_ylabel('E/(m_e c²)')
    ax1.set_title('能量-动量关系')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 固定靶 vs 对撞机
    ax2 = axes[0, 1]
    E_beam = np.logspace(0, 4, 100) * GeV

    sqrt_s_collider = 2 * E_beam
    sqrt_s_fixed = [cm_energy(m_p, m_p, E, 0) for E in E_beam]

    ax2.loglog(E_beam/GeV, np.array(sqrt_s_collider)/GeV, 'b-',
              label='对撞机', linewidth=2)
    ax2.loglog(E_beam/GeV, np.array(sqrt_s_fixed)/GeV, 'r-',
              label='固定靶', linewidth=2)
    ax2.set_xlabel('E_beam (GeV)')
    ax2.set_ylabel('√s (GeV)')
    ax2.set_title('质心系能量比较')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 双光子不变质量
    ax3 = axes[0, 2]
    theta = np.linspace(0, np.pi, 100)

    E1 = E2 = 100 * MeV
    p1 = p2 = E1 / c  # 光子

    M_inv = [invariant_mass_two_particles(E1, E2, p1, p2, t) for t in theta]

    ax3.plot(theta * 180/np.pi, np.array(M_inv)*c**2/MeV, 'b-', linewidth=2)
    ax3.set_xlabel('夹角 (度)')
    ax3.set_ylabel('M_inv (MeV/c²)')
    ax3.set_title('双光子不变质量')
    ax3.grid(True, alpha=0.3)

    # 4. Compton散射
    ax4 = axes[1, 0]
    theta_comp = np.linspace(0, np.pi, 100)

    for E_gamma_keV in [10, 100, 500, 1000]:
        E_gamma = E_gamma_keV * 1e3 * eV
        E_scattered = [compton_scattered_energy(E_gamma, t) for t in theta_comp]
        ax4.plot(theta_comp * 180/np.pi, np.array(E_scattered)/(1e3*eV),
                label=f'{E_gamma_keV} keV', linewidth=1.5)

    ax4.set_xlabel('散射角 (度)')
    ax4.set_ylabel('E\'_γ (keV)')
    ax4.set_title('Compton散射光子能量')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 二体衰变动量
    ax5 = axes[1, 1]
    m_pi0 = 135 * MeV / c**2

    M_range = np.linspace(1.01 * m_pi0, 5 * m_pi0, 100)
    p_decay = [two_body_decay_momentum(M, m_pi0, m_pi0) for M in M_range]

    ax5.plot(M_range * c**2 / MeV, np.array(p_decay) * c / MeV, 'b-', linewidth=2)
    ax5.set_xlabel('M (MeV/c²)')
    ax5.set_ylabel('p* (MeV/c)')
    ax5.set_title('二体衰变 (π⁰ π⁰)')
    ax5.grid(True, alpha=0.3)

    # 6. 阈值能量
    ax6 = axes[1, 2]
    reactions = ['e⁺e⁻对', 'μ⁺μ⁻对', 'π⁺π⁻对', 'pp̄对']
    m_mu = 105.7 * MeV / c**2
    m_pi = 139.6 * MeV / c**2

    thresholds = [
        2 * m_e * c**2 / MeV,
        2 * m_mu * c**2 / MeV,
        2 * m_pi * c**2 / MeV,
        2 * m_p * c**2 / MeV
    ]

    ax6.barh(reactions, thresholds, alpha=0.7)
    ax6.set_xlabel('阈值能量 (MeV)')
    ax6.set_title('粒子对产生阈值')
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('relativistic_collisions.png', dpi=150)
    print("图像已保存为 relativistic_collisions.png")
    plt.show()


# =============================================================================
# 验证函数
# =============================================================================
def verify():
    """
    验证所有练习的正确性 Verify all exercises

    检查内容 Checks:
    6.1 能量动量关系 E² = (pc)² + (mc²)²
    6.2 不变质量计算
    6.3 对撞机vs固定靶能量比较
    6.4 反质子产生阈能
    6.5 二体衰变动力学
    6.6 康普顿散射
    """
    all_passed = True

    # 检查 6.1 - 能量动量关系
    v = 0.8 * c
    E = relativistic_energy(m_e, v)
    p = relativistic_momentum(m_e, v)

    E_check = energy_from_momentum(p, m_e)
    if not np.isclose(E, E_check, rtol=0.01):
        print("错误 6.1 能量动量关系 E² = (pc)² + (mc²)² 验证失败")
        all_passed = False
    else:
        print(f"通过 6.1 能量动量关系正确 (E = {E/(m_e*c**2):.2f} m_e c²)")

    # 检查 6.2 - 不变质量
    E1 = 1 * GeV
    E2 = 1 * GeV
    p1 = p2 = E1 / c  # 光子

    M_head = invariant_mass_two_particles(E1, E2, p1, p2, np.pi)
    if M_head <= 0:
        print("错误 6.2 双光子对头碰撞的不变质量应为正")
        all_passed = False
    else:
        print(f"通过 6.2 不变质量正确 (对头光子: M = {M_head*c**2/GeV:.2f} GeV/c²)")

    # 检查 6.3 - 质心系能量
    E_beam = 7000 * GeV  # LHC 能量
    sqrt_s_coll, sqrt_s_fix = collider_vs_fixed_target(E_beam)

    if sqrt_s_coll <= sqrt_s_fix:
        print("错误 6.3 对撞机的质心能量应远高于固定靶")
        all_passed = False
    else:
        print(f"通过 6.3 质心能量比较正确 (对撞机: {sqrt_s_coll/GeV:.0f} GeV vs 固定靶: {sqrt_s_fix/GeV:.0f} GeV)")

    # 检查 6.4 - 反质子阈能
    E_th_antiproton = antiproton_production_threshold()
    expected_th = 7 * m_p * c**2

    if not np.isclose(E_th_antiproton, expected_th, rtol=0.1):
        print("错误 6.4 反质子产生阈能应为 7m_p c²")
        all_passed = False
    else:
        print(f"通过 6.4 阈能正确 (反质子产生: {E_th_antiproton/GeV:.2f} GeV)")

    # 检查 6.5 - 二体衰变
    m_pi0 = 135 * MeV / c**2
    M_parent = 500 * MeV / c**2

    p_star = two_body_decay_momentum(M_parent, m_pi0, m_pi0)
    E1, E2 = two_body_decay_energies(M_parent, m_pi0, m_pi0)

    if not np.isclose(E1 + E2, M_parent * c**2, rtol=0.01):
        print("错误 6.5 二体衰变能量不守恒")
        all_passed = False
    else:
        print(f"通过 6.5 二体衰变正确 (质心系动量 p* = {p_star*c/MeV:.1f} MeV/c)")

    # 检查 6.6 - 康普顿散射
    E_gamma = 511e3 * eV  # 0.511 MeV
    theta = np.pi  # 背散射（180度）

    E_scattered = compton_scattered_energy(E_gamma, theta)
    expected = E_gamma / (1 + 2 * E_gamma / (m_e * c**2))

    if not np.isclose(E_scattered, expected, rtol=0.01):
        print("错误 6.6 康普顿背散射能量计算错误")
        all_passed = False
    else:
        print(f"通过 6.6 康普顿散射正确 (背散射能量: E' = {E_scattered/eV/1e3:.1f} keV)")

    if all_passed:
        print("\n所有测试通过！正在生成可视化图像...")
        try:
            plot_relativistic_collisions()
        except Exception as ex:
            print(f"可视化生成失败: {ex}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("相对论性粒子碰撞 Relativistic Particle Collisions")
    print("=" * 50)
    verify()
