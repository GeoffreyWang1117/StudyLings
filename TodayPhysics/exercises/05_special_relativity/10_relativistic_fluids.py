"""
相对论流体力学 Relativistic Fluid Dynamics
难度 Difficulty: ★★★★★

学习目标 Learning Objectives:
- 理解相对论能动张量的构造和物理意义
  Understand the stress-energy tensor construction and meaning
- 掌握完美流体的相对论方程
  Master relativistic equations for perfect fluids
- 分析相对论激波和跳跃条件
  Analyze relativistic shocks and jump conditions
- 理解相对论喷流和辐射流体
  Understand relativistic jets and radiation hydrodynamics

物理背景 Physical Background:
相对论流体力学在天体物理中至关重要：
- 伽马射线暴、活动星系核喷流（洛伦兹因子可达数百）
- 中子星合并、黑洞吸积盘
- 早期宇宙（辐射主导时期）
- 重离子碰撞产生的夸克-胶子等离子体

能动张量 Stress-Energy Tensor:
完美流体的能动张量: T^μν = (ρ + P)u^μu^ν + Pg^μν
其中 ρ 是固有能量密度，P 是压强，u^μ 是四速度

守恒方程:
∂_μT^μν = 0 (能量动量守恒)
∂_μ(nu^μ) = 0 (粒子数守恒)

状态方程 Equation of State:
- 非相对论理想气体: P = nkT, ρ ≈ nmc²
- 极端相对论: P = ρ/3, c_s = c/√3
- 辐射主导: P = u_rad/3, Γ = 4/3

关键公式 Key Formulas:
- 能动张量: T^μν = (ρ + P)u^μu^ν + Pg^μν
- 实验室系能量密度: T⁰⁰ = γ²(ρ + P) - P
- 动量密度: T⁰ⁱ = γ²(ρ + P)vⁱ/c
- 相对论声速: c_s² = (∂P/∂ρ)_s ≤ c²
- 聚束效应: D = 1/(γ(1 - β cos θ))

单位说明 Units:
- 能量密度: J/m³ = Pa
- 压强: Pa
- 速度: m/s
- 光度: W
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import c, k_B

# I AM NOT DONE

# =============================================================================
# 练习 10.1: 相对论能动张量
# Exercise 10.1: Relativistic Energy-Momentum Tensor
#
# 物理背景：能动张量是描述物质分布的核心量
#
# 完美流体能动张量：
# T^μν = (ρ + P)u^μu^ν + Pg^μν
# 其中 ρ 是固有能量密度，P 是压强，u^μ 是四速度
#
# 能动张量的物理意义：
# - T^00: 能量密度
# - T^0i: 动量密度（能量流）
# - T^i0: 能量流（动量密度）
# - T^ij: 动量流（应力张量）
#
# 在流体静止系中：
# T^μν = diag(ρ, P, P, P)
# 变换到实验室系后各分量混合
#
# Physical background: Stress-energy tensor for perfect fluids
# =============================================================================
def perfect_fluid_stress_energy(rho, P, u_mu, g_inv):
    """
    完美流体能动张量 Perfect fluid stress-energy tensor

    公式 Formula: T^μν = (ρ + P)u^μu^ν + Pg^μν

    参数 Parameters:
        rho: 固有能量密度 (J/m³)
        P: 压强 (Pa)
        u_mu: 四速度 u^μ
        g_inv: 逆度规 g^μν（闵可夫斯基时空为 diag(1,-1,-1,-1)）

    返回 Returns:
        T: 4×4 能动张量 T^μν

    物理意义：
    - ρ + P = w 是焓密度（enthalpy density）
    - 在流体静止系中 u^μ = (c,0,0,0)，T^μν = diag(ρc², P, P, P)
    - 能动张量满足守恒方程 ∂_μT^μν = 0
    """
    w = rho + P  # 焓密度
    T = np.zeros((4, 4))
    for mu in range(4):
        for nu in range(4):
            T[mu, nu] = w * u_mu[mu] * u_mu[nu] + P * g_inv[mu, nu]
    return T

def energy_density_lab_frame(rho, P, gamma):
    """
    实验室系能量密度 Energy density in lab frame

    公式 Formula: T⁰⁰ = γ²(ρ + P) - P = γ²ρ + (γ² - 1)P

    参数 Parameters:
        rho: 固有能量密度 (J/m³)
        P: 压强 (Pa)
        gamma: 洛伦兹因子

    返回 Returns:
        T⁰⁰: 实验室系能量密度 (J/m³)

    物理解释：
    - γ²ρ: 能量密度的洛伦兹收缩贡献
    - (γ² - 1)P: 压强对能量密度的相对论贡献
    - 高速流体的能量密度显著增加
    """
    return gamma**2 * (rho + P) - P

def momentum_density(rho, P, gamma, v):
    """
    动量密度 Momentum density

    公式 Formula: T⁰ⁱ = γ²(ρ + P)v/c

    参数 Parameters:
        rho: 固有能量密度 (J/m³)
        P: 压强 (Pa)
        gamma: 洛伦兹因子
        v: 流体速度 (m/s)

    返回 Returns:
        g = T⁰ⁱ/c: 动量密度 (kg/(m²·s))

    物理意义：
    - 动量密度 = 能量流/c²
    - 压强也携带动量（相对论效应）
    - 这是焓密度 (ρ + P) 而非仅能量密度参与的原因
    """
    return gamma**2 * (rho + P) * v / c

def pressure_tensor_isotropic(P, gamma):
    """
    各向同性压力张量（静止流体）Isotropic pressure tensor

    公式 Formula: T^ij = Pδ^ij（流体静止时）

    参数 Parameters:
        P: 压强 (Pa)
        gamma: 洛伦兹因子（此简化版本未使用）

    返回 Returns:
        3×3 空间应力张量

    注意：运动流体的应力张量不再是对角的
    完整变换需要考虑速度方向的各向异性
    """
    return P * np.eye(3)


# =============================================================================
# 练习 10.2: 相对论流体方程
# Exercise 10.2: Relativistic Fluid Equations
#
# 物理背景：相对论流体力学的基本方程
#
# 守恒方程：
# 1. 粒子数守恒: ∂_μ(nu^μ) = 0
# 2. 能动量守恒: ∂_μT^μν = 0（四个方程）
#
# 这些方程是牛顿流体方程的相对论推广：
# - 连续性方程 → 粒子数守恒
# - 纳维-斯托克斯方程 → 能动量守恒的空间分量
# - 能量方程 → 能动量守恒的时间分量
#
# 重要量：
# - 固有密度 ρ: 流体静止系中测量的能量密度
# - 压强 P: 各向同性压力
# - 焓密度 w = ρ + P: 出现在动量通量中
#
# Physical background: Conservation equations for relativistic fluids
# =============================================================================
def continuity_equation(n, u_mu, d_mu_n, d_mu_u):
    """
    粒子数守恒 Particle number conservation

    公式 Formula: ∂_μ(nu^μ) = 0
    展开: n∂_μu^μ + u^μ∂_μn = 0

    参数 Parameters:
        n: 固有粒子数密度 (1/m³)
        u_mu: 四速度 u^μ
        d_mu_n: n 的四维梯度 [∂n/∂(ct), ∂n/∂x, ∂n/∂y, ∂n/∂z]
        d_mu_u: u^μ 的四维散度

    返回 Returns:
        守恒方程的值（应该为零）

    物理意义：粒子数是守恒量（无湮灭或产生）
    """
    return np.sum(n * d_mu_u + u_mu * d_mu_n)

def energy_momentum_conservation(T, d_mu_T):
    """
    能动量守恒 Energy-momentum conservation

    公式 Formula: ∂_μT^μν = 0

    参数 Parameters:
        T: 4×4 能动张量
        d_mu_T: T^μν 对第一个指标的导数（4×4×4 张量）

    返回 Returns:
        四个守恒方程的值（四维矢量，应该都为零）

    物理意义：
    - ν=0: 能量守恒
    - ν=1,2,3: 动量守恒（三个方向）
    """
    return np.sum(d_mu_T, axis=0)

def relativistic_euler(rho, P, v, d_rho, d_P, d_v, gamma):
    """
    相对论欧拉方程（简化）Relativistic Euler equation

    公式 Formula（一维简化）:
    ∂(γρ)/∂t + ∂(γρv)/∂x = 0（质量通量形式）

    参数 Parameters:
        rho: 固有密度
        P: 压强
        v: 速度
        d_rho, d_P, d_v: 各量的导数（此简化版本未完全使用）
        gamma: 洛伦兹因子

    返回 Returns:
        质量通量 γρv

    完整的相对论欧拉方程非常复杂，
    包含焓密度、压强梯度、惯性项等
    """
    return gamma * rho * v

def enthalpy_per_particle(rho, P, n):
    """
    每粒子焓 Enthalpy per particle

    公式 Formula: h = (ρ + P)/n

    参数 Parameters:
        rho: 能量密度 (J/m³)
        P: 压强 (Pa)
        n: 粒子数密度 (1/m³)

    返回 Returns:
        h: 每粒子焓 (J)

    物理意义：
    - 焓 = 内能 + PV 功
    - 在相对论流体中，焓密度 w = ρ + P 是动量通量的关键
    - 每粒子焓是热力学分析的重要量
    """
    return (rho + P) / n


# =============================================================================
# 练习 10.3: 状态方程
# Exercise 10.3: Equation of State
#
# 物理背景：状态方程连接热力学量
#
# 常见的状态方程：
#
# 1. 非相对论理想气体:
#    P = nkT
#    ρ ≈ nmc²（静止质量能量主导）
#
# 2. 极端相对论气体（热运动能量 >> mc²）:
#    P = ρ/3
#    声速 c_s = c/√3 ≈ 0.577c
#
# 3. 辐射主导:
#    P = u/3 = aT⁴/3
#    绝热指数 Γ = 4/3
#
# 4. 多方气体:
#    P = Kρ^Γ
#    绝热过程的简化模型
#
# 因果性约束：声速不能超过光速！
# c_s² = (∂P/∂ρ)_s ≤ c²
#
# Physical background: Equations of state for relativistic matter
# =============================================================================
def ideal_gas_eos(n, T, m):
    """
    理想气体状态方程 Ideal gas equation of state

    公式 Formula:
    P = nk_BT
    ρ = nmc² + (3/2)nk_BT（非相对论极限）

    参数 Parameters:
        n: 粒子数密度 (1/m³)
        T: 温度 (K)
        m: 粒子质量 (kg)

    返回 Returns:
        (P, rho): 压强 (Pa) 和能量密度 (J/m³)

    物理意义：
    - nmc²: 静止质量能量密度
    - (3/2)nk_BT: 热动能密度（单原子气体）
    - 非相对论时 ρ ≈ nmc² >> P
    """
    P = n * k_B * T
    rho = n * m * c**2 + 1.5 * n * k_B * T
    return P, rho

def ultrarelativistic_eos(rho):
    """
    极端相对论状态方程 Ultrarelativistic equation of state

    公式 Formula: P = ρ/3

    参数 Parameters:
        rho: 能量密度 (J/m³)

    返回 Returns:
        P: 压强 (Pa)

    物理背景：
    - 当粒子热运动能量 >> mc² 时适用
    - 光子气体、早期宇宙、夸克-胶子等离子体
    - 声速 c_s = c/√3 ≈ 0.577c
    - 绝热指数 Γ = 4/3
    """
    return rho / 3

def polytropic_eos(rho, K, Gamma):
    """
    多方状态方程 Polytropic equation of state

    公式 Formula: P = Kρ^Γ

    参数 Parameters:
        rho: 能量密度 (J/m³)
        K: 多方常数
        Gamma: 多方指数

    返回 Returns:
        P: 压强 (Pa)

    常见的 Γ 值：
    - Γ = 5/3: 非相对论单原子理想气体
    - Γ = 4/3: 相对论气体、辐射
    - Γ = 2: 某些中子星模型

    用于简化复杂的热力学计算
    """
    return K * rho**Gamma

def sound_speed_relativistic(rho, P, d_P_d_rho):
    """
    相对论声速 Relativistic sound speed

    公式 Formula: c_s² = (∂P/∂ρ)_s

    参数 Parameters:
        rho: 能量密度 (J/m³)（此版本未使用）
        P: 压强 (Pa)（此版本未使用）
        d_P_d_rho: dP/dρ 在等熵条件下

    返回 Returns:
        c_s: 声速 (m/s)

    因果性约束：c_s ≤ c（声速不能超过光速）
    - 极端相对论: c_s = c/√3
    - 非相对论理想气体: c_s = √(ΓP/ρ) << c

    违反因果性意味着状态方程物理上不合理
    """
    c_s_squared = d_P_d_rho
    return np.sqrt(c_s_squared) if c_s_squared <= c**2 else c


# =============================================================================
# 练习 10.4: 相对论激波
# Exercise 10.4: Relativistic Shocks
#
# 物理背景：激波是流体中的不连续面
#
# 激波特点：
# - 激波阵面两侧的物理量（密度、压强、速度）不连续
# - 激波传播速度超过上游声速（超声速流动）
# - 激波使熵增加（不可逆过程）
#
# Hugoniot 跳跃条件：
# 跨越激波面的守恒律：
# - 质量通量守恒: [ρu^μ n_μ] = 0
# - 能动量通量守恒: [T^μν n_ν] = 0
#
# 相对论激波的特殊性：
# - 压缩比有相对论上限
# - Taub 绝热线代替经典 Hugoniot 曲线
# - 在天体物理中极为重要（伽马射线暴、超新星）
#
# Physical background: Relativistic shock waves and jump conditions
# =============================================================================
def hugoniot_jump_conditions(rho1, P1, v1, rho2, P2, v2):
    """
    Hugoniot 跳跃条件 Hugoniot jump conditions

    公式 Formula:
    [ρu^μ n_μ] = 0（质量通量守恒）
    [T^μν n_ν] = 0（能动量通量守恒）

    参数 Parameters:
        rho1, P1, v1: 上游（激波前）状态
        rho2, P2, v2: 下游（激波后）状态

    返回 Returns:
        质量通量差（应为零满足守恒）

    物理意义：
    - 质量通量 = γρv 在激波面两侧相等
    - 动量通量和能量通量同样守恒
    - 但熵增加（不可逆压缩）
    """
    gamma1 = 1 / np.sqrt(1 - v1**2 / c**2)
    gamma2 = 1 / np.sqrt(1 - v2**2 / c**2)

    flux1 = gamma1 * rho1 * v1
    flux2 = gamma2 * rho2 * v2

    return np.abs(flux1 - flux2)

def shock_compression_ratio(Gamma, M):
    """
    激波压缩比（非相对论极限）Shock compression ratio

    公式 Formula: ρ₂/ρ₁ = (Γ+1)M²/((Γ-1)M² + 2)

    参数 Parameters:
        Gamma: 绝热指数
        M: 马赫数（上游速度/声速）

    返回 Returns:
        密度压缩比 ρ₂/ρ₁

    极限行为：
    - M → 1: 压缩比 → 1（无激波）
    - M → ∞: 压缩比 → (Γ+1)/(Γ-1)
      - Γ = 5/3: 最大压缩比 = 4
      - Γ = 4/3: 最大压缩比 = 7

    相对论修正会改变这些极限值
    """
    return (Gamma + 1) * M**2 / ((Gamma - 1) * M**2 + 2)

def relativistic_mach_number(v, c_s):
    """
    相对论马赫数 Relativistic Mach number

    公式 Formula: M_rel = γ_s v / (c_s γ_v)
    简化形式: M_rel ∝ v/c_s × 相对论修正因子

    参数 Parameters:
        v: 流体速度 (m/s)
        c_s: 声速 (m/s)

    返回 Returns:
        M: 相对论马赫数

    注意：
    - 经典马赫数 M = v/c_s
    - 相对论修正涉及两个洛伦兹因子
    - 当 v 和 c_s 都接近 c 时，修正显著
    """
    gamma_s = 1 / np.sqrt(1 - c_s**2 / c**2)
    return v / c_s * np.sqrt(1 - v**2/c**2) * gamma_s

def taub_adiabat(h1, h2, P1, P2, rho1, rho2):
    """
    Taub 绝热线（相对论 Hugoniot 曲线）Taub adiabat

    公式 Formula: h₁² - h₂² = (P₁ - P₂)(1/ρ₁ + 1/ρ₂)

    参数 Parameters:
        h1, h2: 上下游每粒子焓
        P1, P2: 上下游压强
        rho1, rho2: 上下游密度

    返回 Returns:
        Taub 绝热线方程的值（应为零满足跳跃条件）

    物理意义：
    - 这是相对论版本的 Hugoniot 绝热线
    - 连接激波前后的热力学状态
    - 与等熵线不同（激波产生熵）
    - 在高能天体物理中用于分析相对论激波
    """
    return h1**2 - h2**2 - (P1 - P2) * (1/rho1 + 1/rho2)


# =============================================================================
# 练习 10.5: 相对论喷流
# Exercise 10.5: Relativistic Jets
#
# 物理背景：宇宙中最极端的流体运动
#
# 相对论喷流出现在：
# - 活动星系核 (AGN): γ ~ 10-50
# - 伽马射线暴 (GRB): γ ~ 100-1000
# - 微类星体: γ ~ 几
#
# 关键物理效应：
#
# 1. 动能光度:
#    L_kin = γ²ρc²vA >> ½ρv³A（牛顿）
#    相对论喷流携带巨大能量
#
# 2. 相对论聚束效应 (Beaming):
#    辐射集中在前进方向的 1/γ 锥角内
#    亮度增强 D⁴，其中 D = 1/(γ(1-βcosθ))
#    这使得朝向我们的喷流极其明亮
#
# 3. 视超光速运动:
#    喷流侧向运动看起来超过光速！
#    这是投影效应，不违反相对论
#
# Physical background: Relativistic jets in astrophysics
# =============================================================================
def lorentz_factor(v):
    """
    洛伦兹因子 Lorentz factor

    公式 Formula: γ = 1/√(1 - v²/c²)

    参数 Parameters:
        v: 速度 (m/s)

    返回 Returns:
        γ: 洛伦兹因子

    典型值：
    - AGN 喷流: γ ~ 10-50
    - GRB 喷流: γ ~ 100-1000
    """
    return 1 / np.sqrt(1 - v**2 / c**2)

def jet_kinetic_luminosity(rho, v, A):
    """
    喷流动能光度 Jet kinetic luminosity

    公式 Formula: L_kin = γ²ρc²vA

    参数 Parameters:
        rho: 固有能量密度 (J/m³)
        v: 喷流速度 (m/s)
        A: 喷流截面积 (m²)

    返回 Returns:
        L_kin: 动能光度（功率）(W)

    与牛顿极限的比较：
    - 牛顿: L = ½ρv³A
    - 相对论: L = γ²ρc²vA >> ½ρv³A（当 v → c）
    - 因子 γ² 使相对论喷流能量巨大

    典型值：AGN 喷流 L ~ 10³⁸ - 10⁴⁵ W
    """
    gamma = lorentz_factor(v)
    return gamma**2 * rho * c**2 * v * A

def jet_momentum_flux(rho, P, v, A):
    """
    喷流动量通量 Jet momentum flux

    公式 Formula: F = (γ²(ρ + P)v² + P)A

    参数 Parameters:
        rho: 能量密度 (J/m³)
        P: 压强 (Pa)
        v: 速度 (m/s)
        A: 截面积 (m²)

    返回 Returns:
        F: 动量通量（力）(N)

    物理意义：
    - 这是喷流对外界施加的推力
    - 焓密度 (ρ + P) 参与而非仅能量密度
    - 喷流与周围介质的相互作用取决于此
    """
    gamma = lorentz_factor(v)
    return (gamma**2 * (rho + P) * v**2 + P) * A

def relativistic_beaming(theta, gamma):
    """
    相对论聚束效应 Relativistic beaming

    公式 Formula:
    增强因子 D = 1/(γ(1 - βcosθ))
    亮度增强 = D⁴（连续谱）或 D³（单能）

    参数 Parameters:
        theta: 观测角（与喷流轴的夹角）(rad)
        gamma: 洛伦兹因子

    返回 Returns:
        D⁴: 聚束增强因子

    物理效应：
    - θ = 0（正对喷流）: D = γ(1+β) ≈ 2γ
      亮度增强 ~ 16γ⁴（极其明亮！）
    - θ = 1/γ: D ~ 1
    - θ = π（背对喷流）: D ~ 1/(2γ)
      亮度减弱 ~ (2γ)⁻⁴（几乎看不见）

    这解释了为什么我们只看到朝向我们的喷流
    """
    beta = np.sqrt(1 - 1/gamma**2)
    D = 1 / (gamma * (1 - beta * np.cos(theta)))
    return D**4


# =============================================================================
# 练习 10.6: 辐射流体
# Exercise 10.6: Radiation Hydrodynamics
#
# 物理背景：当辐射压强与气体压强可比或主导时
#
# 辐射的热力学性质：
# - 能量密度: u = aT⁴（Stefan-Boltzmann 定律）
# - 压强: P = u/3 = aT⁴/3
# - 绝热指数: Γ = 4/3（不同于单原子气体的 5/3）
#
# 辐射主导的物理环境：
# - 恒星内部（特别是大质量恒星）
# - 早期宇宙（复合之前）
# - 吸积盘内区
# - 超新星爆发
#
# 爱丁顿光度：
# 辐射压与引力平衡时的临界光度
# L_Edd = 4πGMm_p c/σ_T ≈ 1.3×10³⁸(M/M_☉) W
# 超过此光度，辐射会吹走物质
#
# Physical background: Radiation-dominated hydrodynamics
# =============================================================================
def radiation_pressure(T):
    """
    辐射压强 Radiation pressure

    公式 Formula: P_rad = aT⁴/3
    其中 a = 4σ/c 是辐射常数

    参数 Parameters:
        T: 温度 (K)

    返回 Returns:
        P_rad: 辐射压强 (Pa)

    数值：
    - a = 7.566×10⁻¹⁶ J/(m³·K⁴)
    - 太阳中心 (T ~ 1.5×10⁷ K): P_rad ~ 10¹³ Pa
    - 但仍远小于气体压强

    辐射压强随 T⁴ 增长，高温时变得重要
    """
    sigma = 5.67e-8  # Stefan-Boltzmann 常数
    a = 4 * sigma / c  # 辐射常数
    return a * T**4 / 3

def radiation_energy_density(T):
    """
    辐射能量密度 Radiation energy density

    公式 Formula: u_rad = aT⁴

    参数 Parameters:
        T: 温度 (K)

    返回 Returns:
        u_rad: 能量密度 (J/m³)

    物理意义：
    - 黑体辐射场的能量密度
    - 与压强的关系: P = u/3（各向同性辐射）
    - 早期宇宙的主要能量成分
    """
    sigma = 5.67e-8
    a = 4 * sigma / c
    return a * T**4

def eddington_luminosity(M):
    """
    爱丁顿光度 Eddington luminosity

    公式 Formula: L_Edd = 4πGMm_p c/σ_T

    参数 Parameters:
        M: 天体质量 (kg)

    返回 Returns:
        L_Edd: 爱丁顿光度 (W)

    物理意义：
    - 辐射压向外推力 = 引力向内拉力时的光度
    - L > L_Edd 时，辐射压会吹走吸积物质
    - 限制了黑洞吸积率和恒星最大质量

    数值估计：
    L_Edd ≈ 1.3×10³⁸ (M/M_☉) W
    即 3.3×10⁴ (M/M_☉) L_☉

    活动星系核的光度常接近或超过 L_Edd
    """
    from utils.constants import G, m_p
    sigma_T = 6.65e-29  # Thomson 散射截面
    return 4 * np.pi * G * M * m_p * c / sigma_T

def radiation_dominated_eos():
    """
    辐射主导状态方程 Radiation-dominated EOS

    公式 Formula:
    P = ρ/3（辐射主导时）
    绝热指数 Γ = 4/3

    返回 Returns:
        Γ = 4/3

    物理意义：
    - Γ = 4/3 是辐射气体的绝热指数
    - 不同于单原子气体的 Γ = 5/3
    - 影响恒星稳定性和宇宙学演化
    - Γ < 4/3 的恒星不稳定（会坍缩或爆炸）
    """
    return 4/3


# =============================================================================
# 可视化
# =============================================================================
def plot_relativistic_fluids():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 能量密度vs速度
    ax1 = axes[0, 0]
    v = np.linspace(0, 0.99, 100) * c
    rho_0 = 1  # 固有密度
    P = 0.1 * rho_0 * c**2

    gamma = [lorentz_factor(vi) for vi in v]
    T_00 = [energy_density_lab_frame(rho_0 * c**2, P, g) for g in gamma]

    ax1.plot(v/c, np.array(T_00)/(rho_0*c**2), 'b-', linewidth=2)
    ax1.set_xlabel('v/c')
    ax1.set_ylabel('T⁰⁰/(ρ₀c²)')
    ax1.set_title('相对论能量密度')
    ax1.set_yscale('log')
    ax1.grid(True, alpha=0.3)

    # 2. 声速vs状态方程
    ax2 = axes[0, 1]
    Gamma_range = np.linspace(1.1, 2, 100)

    # 多方气体声速 c_s² = ΓP/ρ
    # 极端相对论时 c_s² = c²/3
    c_s = [c * np.sqrt((G - 1) / G) for G in Gamma_range]

    ax2.plot(Gamma_range, np.array(c_s)/c, 'b-', linewidth=2)
    ax2.axhline(y=1/np.sqrt(3), color='r', linestyle='--', label='极端相对论')
    ax2.axhline(y=1, color='g', linestyle=':', label='c')
    ax2.set_xlabel('Γ')
    ax2.set_ylabel('c_s/c')
    ax2.set_title('声速（理想气体）')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 激波压缩比
    ax3 = axes[0, 2]
    M = np.linspace(1, 10, 100)

    for Gamma in [4/3, 5/3, 2]:
        ratio = [shock_compression_ratio(Gamma, m) for m in M]
        ax3.plot(M, ratio, label=f'Γ={Gamma:.2f}', linewidth=2)

    ax3.set_xlabel('马赫数 M')
    ax3.set_ylabel('压缩比 ρ₂/ρ₁')
    ax3.set_title('激波压缩比')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 相对论聚束
    ax4 = axes[1, 0]
    theta = np.linspace(0, np.pi, 200)

    for gamma in [2, 5, 10]:
        D4 = [relativistic_beaming(t, gamma) for t in theta]
        ax4.semilogy(np.degrees(theta), D4, label=f'γ={gamma}', linewidth=2)

    ax4.set_xlabel('θ (度)')
    ax4.set_ylabel('增强因子 D⁴')
    ax4.set_title('相对论聚束效应')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 喷流光度vs速度
    ax5 = axes[1, 1]
    v = np.linspace(0.1, 0.999, 100) * c
    rho = 1e-10  # kg/m³
    A = 1e30  # m²

    L_kin = [jet_kinetic_luminosity(rho, vi, A) for vi in v]
    L_kin_nr = [0.5 * rho * vi**3 * A for vi in v]  # 非相对论

    ax5.semilogy(v/c, L_kin, 'b-', linewidth=2, label='相对论')
    ax5.semilogy(v/c, L_kin_nr, 'r--', linewidth=2, label='非相对论')
    ax5.set_xlabel('v/c')
    ax5.set_ylabel('L_kin (W)')
    ax5.set_title('喷流动能光度')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. 辐射vs物质压强
    ax6 = axes[1, 2]
    T = np.logspace(5, 9, 100)  # K
    n = 1e20  # m⁻³
    m = 1.67e-27  # kg

    P_rad = [radiation_pressure(t) for t in T]
    P_gas = [n * k_B * t for t in T]

    ax6.loglog(T, P_rad, 'r-', linewidth=2, label='辐射压')
    ax6.loglog(T, P_gas, 'b-', linewidth=2, label='气体压')
    ax6.set_xlabel('温度 (K)')
    ax6.set_ylabel('压强 (Pa)')
    ax6.set_title('辐射vs气体压强')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('relativistic_fluids.png', dpi=150)
    print("图像已保存为 relativistic_fluids.png")
    plt.show()


def verify():
    """
    验证所有练习的正确性 Verify all exercises

    检查内容 Checks:
    10.1 能动张量计算
    10.2 流体方程（焓计算）
    10.3 状态方程（极端相对论）
    10.4 激波压缩比
    10.5 相对论聚束效应
    10.6 辐射压强
    """
    all_passed = True

    # 检查 10.1 - 能动张量
    gamma = 2
    v = c * np.sqrt(1 - 1/gamma**2)
    rho, P = 1, 0.1
    T_00 = energy_density_lab_frame(rho, P, gamma)
    expected = gamma**2 * (rho + P) - P
    if not np.isclose(T_00, expected, rtol=0.01):
        print("错误 10.1 能动张量 T⁰⁰ 计算不正确，检查公式 γ²(ρ+P) - P")
        all_passed = False
    else:
        print(f"通过 10.1 能动张量正确 (T⁰⁰ = {T_00:.2f})")

    # 检查 10.2 - 流体方程
    h = enthalpy_per_particle(1e-10, 1e-11, 1e10)
    if h <= 0:
        print("错误 10.2 每粒子焓 h = (ρ+P)/n 应为正值")
        all_passed = False
    else:
        print("通过 10.2 流体方程正确（焓计算正确）")

    # 检查 10.3 - 状态方程
    P_ur = ultrarelativistic_eos(3)
    if not np.isclose(P_ur, 1, rtol=0.01):
        print("错误 10.3 极端相对论状态方程应满足 P = ρ/3")
        all_passed = False
    else:
        print("通过 10.3 状态方程正确 (P = ρ/3)")

    # 检查 10.4 - 激波
    ratio = shock_compression_ratio(5/3, 1)
    if not np.isclose(ratio, 1, rtol=0.01):
        print("错误 10.4 马赫数 M=1 时压缩比应为 1（无激波）")
        all_passed = False
    else:
        print("通过 10.4 激波压缩比正确")

    # 检查 10.5 - 相对论聚束
    D4 = relativistic_beaming(0, 10)
    if D4 <= 1:
        print("错误 10.5 正向聚束（θ=0）时亮度应显著增强")
        all_passed = False
    else:
        print(f"通过 10.5 相对论喷流正确 (D⁴(0°) = {D4:.0f})")

    # 检查 10.6 - 辐射流体
    P_rad = radiation_pressure(1e6)
    if P_rad <= 0:
        print("错误 10.6 辐射压强 P = aT⁴/3 应为正值")
        all_passed = False
    else:
        print(f"通过 10.6 辐射流体正确 (P_rad(10⁶K) = {P_rad:.2e} Pa)")

    if all_passed:
        print("\n所有测试通过！正在生成可视化图像...")
        try:
            plot_relativistic_fluids()
        except Exception as e:
            print(f"可视化生成失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("相对论流体力学 Relativistic Fluid Dynamics")
    print("=" * 50)
    verify()
