"""
超导与迈斯纳效应 Superconductivity and Meissner Effect
难度 Difficulty: ★★★★★

学习目标 Learning Objectives:
- 理解超导电性基本特征：零电阻和完全抗磁性 (Understand basic superconductivity features)
- 掌握迈斯纳效应和伦敦方程的物理意义 (Master Meissner effect and London equations)
- 分析I型和II型超导体的区别 (Analyze Type-I and Type-II superconductors)
- 理解BCS理论：库珀对与能隙 (Understand BCS theory: Cooper pairs and energy gap)
- 掌握约瑟夫森效应及其应用 (Master Josephson effect and applications)

物理背景 Physical Background:
1. 超导态的两个基本特征 Two fundamental features of superconductivity:
   - 零电阻态：电阻完全消失，电流无损耗传输
   - 完全抗磁性（迈斯纳效应）：磁场被完全排斥出超导体

2. 临界参数 Critical parameters:
   - 临界温度 T_c：超导转变温度
   - 临界磁场 H_c：破坏超导态的磁场强度
   - 临界电流 I_c：能维持超导态的最大电流

3. 伦敦方程 London equations:
   - 描述超导体内电磁场行为的唯象方程
   - 预测磁场在表面的指数衰减（伦敦穿透深度 λ_L）

4. Ginzburg-Landau理论 GL Theory:
   - 引入序参量描述超导态
   - 定义相干长度 ξ（超导电子波函数的空间变化尺度）
   - GL参数 κ = λ_L/ξ 区分I型（κ < 1/√2）和II型（κ > 1/√2）超导体

5. BCS理论 BCS Theory:
   - 微观理论：电子通过晶格振动（声子）形成库珀对
   - 能隙 Δ(0) = 1.764 k_B T_c
   - 相干长度 ξ_0 = ℏv_F/(πΔ)

核心公式 Key Formulas:
- 伦敦穿透深度 London penetration depth: λ_L = √(m_s/(μ₀n_s(2e)²))
- 迈斯纳效应 Meissner effect: B(x) = B₀exp(-x/λ_L)
- I型临界磁场 Type-I critical field: H_c(T) = H_c(0)[1-(T/T_c)²]
- 磁通量子 Flux quantum: Φ₀ = h/(2e) ≈ 2.07×10⁻¹⁵ Wb
- 直流约瑟夫森效应 DC Josephson: I = I_c sin(φ)
- 交流约瑟夫森效应 AC Josephson: f = 2eV/h

重要常数 Important Constants:
- 磁通量子 Φ₀ = 2.07×10⁻¹⁵ Wb
- 典型伦敦穿透深度：Al ~50nm, Nb ~40nm, YBCO ~150nm
- 典型临界温度：Al 1.2K, Nb 9.2K, YBCO 93K, BSCCO 110K
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import kv as bessel_k
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import mu_0, epsilon_0, k_B, e, m_e, hbar, h

# I AM NOT DONE

# 超导相关常数
Phi_0 = h / (2 * e)  # 磁通量子

# =============================================================================
# 练习 12.1: 伦敦穿透深度
# Exercise 12.1: London Penetration Depth
#
# 物理背景 Physical Background:
# 伦敦穿透深度描述外磁场进入超导体内部的衰减特征长度
# 在该深度内，磁场衰减为表面值的 1/e
# 它反映了超导电流产生的抗磁响应能力
#
# 公式 Formula: λ_L = √(m_s / (μ₀ n_s q²))
# - m_s: 超流载流子质量（库珀对质量 ≈ 2m_e）
# - n_s: 超导电子密度 [m⁻³]
# - q: 库珀对电荷 = 2e
#
# 典型值 Typical values:
# - 铝(Al): λ_L ≈ 50 nm, T_c = 1.2 K
# - 铌(Nb): λ_L ≈ 40 nm, T_c = 9.2 K
# - YBCO: λ_L ≈ 150 nm, T_c = 93 K
# =============================================================================
def london_penetration_depth(n_s, m_s=2*m_e):
    """
    计算伦敦穿透深度 Calculate London penetration depth

    公式 Formula: λ_L = √(m_s / (μ₀ n_s (2e)²))

    参数 Parameters:
        n_s: float - 超导电子密度 superconducting electron density [m⁻³]
        m_s: float - 库珀对有效质量 Cooper pair effective mass [kg]
                     默认值 2m_e（两个电子组成的库珀对）

    返回 Returns:
        float - 伦敦穿透深度 London penetration depth [m]

    物理意义 Physical meaning:
    - 表征磁场穿透超导体表面的深度
    - 与超导电子密度的平方根成反比
    - 温度升高时，n_s 减小，λ_L 增大
    """
    # TODO: 计算伦敦穿透深度
    # 提示：使用库珀对电荷 q = 2e
    lambda_L = np.sqrt(m_s / (mu_0 * n_s * (2*e)**2))
    return lambda_L

def magnetic_field_decay(x, B0, lambda_L):
    """
    计算超导体内磁场衰减（迈斯纳效应）
    Calculate magnetic field decay inside superconductor (Meissner effect)

    公式 Formula: B(x) = B₀ exp(-x/λ_L)

    参数 Parameters:
        x: float/array - 距超导体表面的深度 depth from surface [m]
        B0: float - 表面磁场强度 surface magnetic field [T]
        lambda_L: float - 伦敦穿透深度 London penetration depth [m]

    返回 Returns:
        float/array - 深度x处的磁场 magnetic field at depth x [T]

    物理意义 Physical meaning:
    - 磁场在进入超导体后指数衰减
    - 在深度 x = λ_L 处，磁场衰减到表面值的 1/e ≈ 37%
    - 在深度 x = 5λ_L 处，磁场基本为零（~0.7%）
    """
    return B0 * np.exp(-x / lambda_L)


# =============================================================================
# 练习 12.2: 临界磁场
# Exercise 12.2: Critical Magnetic Field
#
# 物理背景 Physical Background:
# 超导态只能在一定磁场强度以下维持
# 超过临界磁场，超导态被破坏，材料回到正常态
#
# I型超导体 Type-I Superconductor:
# - 具有单一临界磁场 H_c
# - H < H_c: 完全迈斯纳态（磁场完全排斥）
# - H > H_c: 正常态
# - 例如：Al, Pb, Sn, Hg
#
# 临界磁场温度依赖 Temperature dependence:
# H_c(T) ≈ H_c(0)[1 - (T/T_c)²]
# - 近抛物线关系
# - T = 0 时达到最大值 H_c(0)
# - T = T_c 时降为零
# =============================================================================
def critical_field_type1(T, Tc, Hc0):
    """
    计算I型超导体临界磁场的温度依赖
    Calculate temperature dependence of critical field for Type-I superconductor

    公式 Formula: H_c(T) = H_c(0)[1 - (T/T_c)²]

    参数 Parameters:
        T: float - 温度 temperature [K]
        Tc: float - 临界温度 critical temperature [K]
        Hc0: float - 零温临界磁场 critical field at T=0 [A/m]

    返回 Returns:
        float - 温度T下的临界磁场 critical field at temperature T [A/m]

    物理意义 Physical meaning:
    - 描述超导态与正常态的边界
    - 超导凝聚能与热能的竞争决定了这个关系
    """
    # TODO: 计算临界磁场
    # 注意：T >= Tc 时，超导态不存在，返回 0
    if T >= Tc:
        return 0
    return Hc0 * (1 - (T / Tc)**2)

def condensation_energy(Hc, mu=mu_0):
    """
    计算超导凝聚能密度 Calculate superconducting condensation energy density

    公式 Formula: u = μ₀H_c²/2

    参数 Parameters:
        Hc: float - 临界磁场 critical field [A/m]
        mu: float - 真空磁导率 vacuum permeability [H/m]

    返回 Returns:
        float - 凝聚能密度 condensation energy density [J/m³]

    物理意义 Physical meaning:
    - 超导态相对于正常态的能量降低
    - 等于将超导态转变为正常态所需的能量
    - 也等于维持迈斯纳效应所需排斥磁场的能量
    """
    return mu * Hc**2 / 2


# =============================================================================
# 练习 12.3: II型超导体
# Exercise 12.3: Type-II Superconductors
#
# 物理背景 Physical Background:
# II型超导体允许磁场以量子化涡旋形式部分穿透
# 这使得它们能在更高磁场下保持超导性，具有重要应用价值
#
# Ginzburg-Landau参数 κ = λ_L/ξ:
# - λ_L: 伦敦穿透深度（磁场穿透尺度）
# - ξ: 相干长度（序参量变化尺度）
# - κ < 1/√2 ≈ 0.71: I型超导体
# - κ > 1/√2: II型超导体
#
# II型超导体的三个区域 Three regions:
# 1. H < H_c1: 迈斯纳态（完全抗磁）
# 2. H_c1 < H < H_c2: 混合态（磁通涡旋晶格）
# 3. H > H_c2: 正常态
#
# 典型II型超导体：Nb-Ti, Nb₃Sn, YBCO, BSCCO
# =============================================================================
def ginzburg_landau_parameter(lambda_L, xi):
    """
    计算Ginzburg-Landau参数 Calculate GL parameter

    公式 Formula: κ = λ_L / ξ

    参数 Parameters:
        lambda_L: float - 伦敦穿透深度 London penetration depth [m]
        xi: float - 相干长度 coherence length [m]

    返回 Returns:
        float - GL参数 κ（无量纲 dimensionless）

    分类标准 Classification:
    - κ < 1/√2 ≈ 0.71: I型超导体（界面能为正，磁场突变）
    - κ > 1/√2: II型超导体（界面能为负，允许涡旋态）
    - κ = 1/√2: 临界点
    """
    return lambda_L / xi

def lower_critical_field(Phi0, lambda_L):
    """
    计算下临界磁场 H_c1 Calculate lower critical field

    公式 Formula: H_c1 ≈ Φ₀/(4πλ_L²) [简化公式，精确公式含ln(κ)项]

    参数 Parameters:
        Phi0: float - 磁通量子 flux quantum [Wb]
        lambda_L: float - 伦敦穿透深度 London penetration depth [m]

    返回 Returns:
        float - 下临界磁场 lower critical field [A/m]

    物理意义 Physical meaning:
    - 第一个磁通涡旋开始进入超导体的磁场
    - H < H_c1 时，超导体处于完全迈斯纳态
    - H > H_c1 时，形成磁通涡旋（混合态）
    """
    # 简化公式（忽略 ln(κ) 因子）
    return Phi0 / (4 * np.pi * lambda_L**2)

def upper_critical_field(Phi0, xi):
    """
    计算上临界磁场 H_c2 Calculate upper critical field

    公式 Formula: H_c2 = Φ₀ / (2πξ²)

    参数 Parameters:
        Phi0: float - 磁通量子 flux quantum [Wb]
        xi: float - 相干长度 coherence length [m]

    返回 Returns:
        float - 上临界磁场 upper critical field [A/m]

    物理意义 Physical meaning:
    - 超导态完全消失的磁场
    - 涡旋核心开始重叠时，超导性被破坏
    - H_c2 与相干长度的平方成反比
    - 高温超导体的 H_c2 可达数十特斯拉
    """
    return Phi0 / (2 * np.pi * xi**2)


# =============================================================================
# 练习 12.4: 磁通涡旋
# Exercise 12.4: Magnetic Vortices (Abrikosov Vortex)
#
# 物理背景 Physical Background:
# 在II型超导体的混合态中，磁场以量子化涡旋形式存在
# 每个涡旋携带一个磁通量子 Φ₀ = h/(2e) ≈ 2.07×10⁻¹⁵ Wb
#
# 涡旋结构 Vortex structure:
# - 涡旋核心：半径约 ξ，超导序参量为零，正常态
# - 超流环绕：半径约 λ_L，超导电流围绕核心流动
# - 磁场分布：中心最强，向外按修正贝塞尔函数 K₀ 衰减
#
# Abrikosov涡旋晶格 Abrikosov vortex lattice:
# - 涡旋间相互排斥，形成有序晶格（通常为三角晶格）
# - 涡旋密度与外加磁场成正比：n_v = B/Φ₀
# - 晶格间距 a = √(2Φ₀/(√3 B))（三角晶格）
#
# 1957年阿布里科索夫(Abrikosov)预言，2003年获诺贝尔物理学奖
# =============================================================================
def vortex_magnetic_field(r, lambda_L, Phi0=Phi_0):
    """
    计算单个磁通涡旋的磁场分布 Calculate magnetic field of a single vortex

    公式 Formula: B(r) = (Φ₀/2πλ_L²) K₀(r/λ_L)
    - K₀: 第零阶修正贝塞尔函数 Modified Bessel function of the second kind

    参数 Parameters:
        r: float - 距涡旋中心的距离 distance from vortex center [m]
        lambda_L: float - 伦敦穿透深度 London penetration depth [m]
        Phi0: float - 磁通量子 flux quantum [Wb]

    返回 Returns:
        float - 距离r处的磁场强度 magnetic field at distance r [T]

    物理意义 Physical meaning:
    - r → 0 时，B 趋于对数发散（实际受涡旋核心 ξ 截断）
    - r >> λ_L 时，B 指数衰减
    - 涡旋总磁通 = Φ₀（量子化）
    """
    if r < 1e-10:
        # 小r时使用近似：K₀(x) ≈ -ln(x/2) - γ（γ为欧拉常数）
        return Phi0 / (2 * np.pi * lambda_L**2) * np.log(lambda_L / 1e-10)
    return (Phi0 / (2 * np.pi * lambda_L**2)) * bessel_k(0, r / lambda_L)

def vortex_density(B, Phi0=Phi_0):
    """
    计算磁通涡旋密度 Calculate vortex density

    公式 Formula: n_v = B / Φ₀

    参数 Parameters:
        B: float - 平均磁场 average magnetic field [T]
        Phi0: float - 磁通量子 flux quantum [Wb]

    返回 Returns:
        float - 涡旋面密度 vortex areal density [m⁻²]

    示例 Example:
    - B = 1 T 时，n_v ≈ 4.8×10¹⁴ m⁻² ≈ 48 涡旋/μm²
    """
    return B / Phi0

def vortex_lattice_spacing(B, Phi0=Phi_0):
    """
    计算磁通涡旋晶格间距（三角晶格）
    Calculate vortex lattice spacing (triangular lattice)

    公式 Formula: a = √(2Φ₀/(√3 B))

    参数 Parameters:
        B: float - 平均磁场 average magnetic field [T]
        Phi0: float - 磁通量子 flux quantum [Wb]

    返回 Returns:
        float - 涡旋晶格间距 vortex lattice spacing [m]

    物理意义 Physical meaning:
    - 三角晶格是能量最低的配置
    - 间距随磁场增加而减小
    - 当 a ≈ ξ 时，涡旋核心重叠，趋近 H_c2
    """
    return np.sqrt(2 * Phi0 / (np.sqrt(3) * B))


# =============================================================================
# 练习 12.5: BCS能隙
# Exercise 12.5: BCS Energy Gap
#
# 物理背景 Physical Background:
# BCS理论（Bardeen-Cooper-Schrieffer, 1957）是超导的微观理论
# 核心思想：电子通过声子交换形成库珀对，凝聚到能量更低的状态
#
# 库珀对 Cooper pairs:
# - 两个电子通过晶格振动（声子）间接吸引
# - 形成自旋单态、动量相反的电子对
# - 所有库珀对凝聚到相同的量子态（宏观量子相干）
#
# 能隙 Energy gap:
# - 超导态与激发态之间存在能隙 2Δ
# - 这是超导体零电阻的根本原因
# - 能隙随温度升高而减小，在 T_c 处消失
#
# BCS基本公式 BCS fundamental formulas:
# - 零温能隙：Δ(0) = 1.764 k_B T_c（弱耦合极限）
# - 相干长度：ξ₀ = ℏv_F/(πΔ)（库珀对空间尺度）
#
# 1972年BCS三人获诺贝尔物理学奖
# =============================================================================
def bcs_gap_zero_temp(Tc):
    """
    计算BCS理论零温能隙 Calculate BCS energy gap at zero temperature

    公式 Formula: Δ(0) = 1.764 k_B T_c

    参数 Parameters:
        Tc: float - 临界温度 critical temperature [K]

    返回 Returns:
        float - 零温能隙 energy gap at T=0 [J]

    物理意义 Physical meaning:
    - 1.764 是弱耦合BCS理论的普适常数
    - 强耦合超导体（如Pb）的比值可达 2.0 以上
    - 能隙 Δ 决定了超导体的热力学性质
    """
    return 1.764 * k_B * Tc

def bcs_gap_temperature(T, Tc, Delta0):
    """
    计算BCS能隙的温度依赖 Calculate temperature dependence of BCS gap

    公式 Formula: Δ(T) ≈ Δ(0) tanh(1.74√(T_c/T - 1))
    （近似公式，适用于整个温度范围）

    参数 Parameters:
        T: float - 温度 temperature [K]
        Tc: float - 临界温度 critical temperature [K]
        Delta0: float - 零温能隙 energy gap at T=0 [J]

    返回 Returns:
        float - 温度T下的能隙 energy gap at temperature T [J]

    温度行为 Temperature behavior:
    - T = 0: Δ = Δ(0)
    - T → T_c: Δ → 0（二级相变）
    - 接近 T_c 时：Δ ∝ √(1 - T/T_c)
    """
    if T >= Tc:
        return 0  # 超导态消失
    if T < 1e-10:
        return Delta0  # 避免除零
    return Delta0 * np.tanh(1.74 * np.sqrt(Tc / T - 1))

def coherence_length_bcs(hbar_val, vF, Delta0):
    """
    计算BCS相干长度 Calculate BCS coherence length

    公式 Formula: ξ₀ = ℏv_F / (πΔ)

    参数 Parameters:
        hbar_val: float - 约化普朗克常数 reduced Planck constant [J·s]
        vF: float - 费米速度 Fermi velocity [m/s]
        Delta0: float - 能隙 energy gap [J]

    返回 Returns:
        float - BCS相干长度 BCS coherence length [m]

    物理意义 Physical meaning:
    - 库珀对电子之间的平均间距
    - 超导序参量空间变化的特征尺度
    - 典型值：Al ~1600nm, Nb ~40nm, YBCO ~1-2nm
    - 高温超导体相干长度很短（量子涨落效应强）
    """
    return hbar_val * vF / (np.pi * Delta0)


# =============================================================================
# 练习 12.6: 约瑟夫森效应
# Exercise 12.6: Josephson Effect
#
# 物理背景 Physical Background:
# 约瑟夫森效应是两个超导体通过薄弱连接（隧道结、点接触等）
# 产生的宏观量子现象，由Brian Josephson于1962年预言
#
# 直流约瑟夫森效应 DC Josephson Effect:
# - 零电压下可有超导电流通过
# - 电流取决于两侧超导体的相位差：I = I_c sin(φ)
# - I_c: 临界电流（最大无损耗电流）
#
# 交流约瑟夫森效应 AC Josephson Effect:
# - 加直流电压V时，产生交流超导电流
# - 振荡频率：f = 2eV/h（约瑟夫森关系）
# - 1μV 对应约 483.6 MHz
#
# Shapiro台阶 Shapiro Steps:
# - 施加微波时，I-V曲线出现台阶
# - 台阶电压：V_n = nhf/(2e)
# - 用于电压基准和精密测量
#
# 应用 Applications:
# - SQUID（超导量子干涉仪）：极灵敏磁场探测
# - 电压基准：定义伏特
# - 量子比特：超导量子计算
#
# 1973年约瑟夫森获诺贝尔物理学奖
# =============================================================================
def josephson_dc_current(Ic, phi):
    """
    计算直流约瑟夫森效应电流 Calculate DC Josephson current

    公式 Formula: I = I_c sin(φ)

    参数 Parameters:
        Ic: float - 临界电流 critical current [A]
        phi: float/array - 相位差 phase difference [rad]

    返回 Returns:
        float/array - 约瑟夫森电流 Josephson current [A]

    物理意义 Physical meaning:
    - 无电压时的超导隧穿电流
    - 电流与相位差呈正弦关系
    - |I| < I_c 时结处于零电压态
    - |I| > I_c 时结切换到有限电压态
    """
    # TODO: 计算约瑟夫森电流
    return Ic * np.sin(phi)

def josephson_ac_frequency(V):
    """
    计算交流约瑟夫森效应频率 Calculate AC Josephson frequency

    公式 Formula: f = 2eV/h

    参数 Parameters:
        V: float - 结两端直流电压 DC voltage across junction [V]

    返回 Returns:
        float - 振荡频率 oscillation frequency [Hz]

    约瑟夫森常数 Josephson constant:
    K_J = 2e/h ≈ 483.5979 GHz/mV

    物理意义 Physical meaning:
    - 电压驱动相位演化：dφ/dt = 2eV/ℏ
    - 极精确的电压-频率转换
    - 用于定义SI伏特和精密频率测量
    """
    return 2 * e * V / h

def shapiro_step_voltage(n, f):
    """
    计算Shapiro台阶电压 Calculate Shapiro step voltage

    公式 Formula: V_n = nhf/(2e)

    参数 Parameters:
        n: int - 台阶序号 step index (n = 0, 1, 2, ...)
        f: float - 外加微波频率 applied microwave frequency [Hz]

    返回 Returns:
        float - 第n阶台阶电压 voltage of n-th step [V]

    物理意义 Physical meaning:
    - 相位锁定现象：约瑟夫森振荡与外加微波同步
    - 台阶电压只取决于频率和基本常数
    - 用于建立电压基准（精度可达 10⁻¹⁰）
    """
    return n * h * f / (2 * e)


# =============================================================================
# 可视化
# =============================================================================
def plot_superconductivity():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 迈斯纳效应 - 磁场穿透
    ax1 = axes[0, 0]
    n_s = 1e28  # m⁻³
    lambda_L = london_penetration_depth(n_s)
    x = np.linspace(0, 5 * lambda_L, 200)
    B0 = 1

    B = magnetic_field_decay(x, B0, lambda_L)
    ax1.plot(x / lambda_L, B / B0, 'b-', linewidth=2)
    ax1.fill_between(x / lambda_L, 0, B / B0, alpha=0.3)
    ax1.axhline(y=np.exp(-1), color='r', linestyle='--', label='1/e')
    ax1.set_xlabel('x / λ_L')
    ax1.set_ylabel('B / B₀')
    ax1.set_title('迈斯纳效应：磁场穿透')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 临界磁场vs温度
    ax2 = axes[0, 1]
    Tc = 9.2  # K (Nb)
    Hc0 = 2e5  # A/m
    T = np.linspace(0, Tc, 100)

    Hc = [critical_field_type1(t, Tc, Hc0) for t in T]
    ax2.plot(T / Tc, np.array(Hc) / Hc0, 'b-', linewidth=2)
    ax2.fill_between(T / Tc, 0, np.array(Hc) / Hc0, alpha=0.3, label='超导态')
    ax2.set_xlabel('T / T_c')
    ax2.set_ylabel('H_c / H_c(0)')
    ax2.set_title('I型超导体临界磁场')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. II型超导体相图
    ax3 = axes[0, 2]
    # 示意图
    T_norm = np.linspace(0, 1, 100)
    Hc1 = 1 - T_norm**2
    Hc2 = 10 * (1 - T_norm**2)

    ax3.plot(T_norm, Hc1, 'g-', linewidth=2, label='H_c1')
    ax3.plot(T_norm, Hc2, 'r-', linewidth=2, label='H_c2')
    ax3.fill_between(T_norm, 0, Hc1, alpha=0.3, label='迈斯纳态')
    ax3.fill_between(T_norm, Hc1, Hc2, alpha=0.3, label='混合态')
    ax3.set_xlabel('T / T_c')
    ax3.set_ylabel('H / H_c(0)')
    ax3.set_title('II型超导体相图')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 磁通涡旋磁场分布
    ax4 = axes[1, 0]
    lambda_L = 50e-9  # 50 nm
    r = np.linspace(1e-9, 5 * lambda_L, 200)

    B_vortex = [vortex_magnetic_field(ri, lambda_L) for ri in r]
    ax4.semilogy(r * 1e9, B_vortex, 'b-', linewidth=2)
    ax4.set_xlabel('r (nm)')
    ax4.set_ylabel('B (T)')
    ax4.set_title('单涡旋磁场分布')
    ax4.grid(True, alpha=0.3)

    # 5. BCS能隙温度依赖
    ax5 = axes[1, 1]
    Tc = 9.2
    Delta0 = bcs_gap_zero_temp(Tc)
    T = np.linspace(0.01, Tc, 100)

    Delta = [bcs_gap_temperature(t, Tc, Delta0) / Delta0 for t in T]
    ax5.plot(T / Tc, Delta, 'b-', linewidth=2)
    ax5.set_xlabel('T / T_c')
    ax5.set_ylabel('Δ(T) / Δ(0)')
    ax5.set_title('BCS能隙温度依赖')
    ax5.grid(True, alpha=0.3)

    # 6. 约瑟夫森电流
    ax6 = axes[1, 2]
    phi = np.linspace(-2 * np.pi, 2 * np.pi, 200)
    Ic = 1  # 归一化

    I = josephson_dc_current(Ic, phi)
    ax6.plot(phi / np.pi, I / Ic, 'b-', linewidth=2)
    ax6.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax6.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    ax6.set_xlabel('φ / π')
    ax6.set_ylabel('I / I_c')
    ax6.set_title('直流约瑟夫森效应')
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('superconductivity.png', dpi=150)
    print("图像已保存为 superconductivity.png")
    plt.show()


def verify():
    """
    验证函数 Verification function
    检查所有超导物理练习的实现是否正确
    """
    all_passed = True
    print("\n" + "="*50)
    print("验证超导物理计算 Verifying Superconductivity Calculations")
    print("="*50 + "\n")

    # ===========================================
    # 检查 12.1: 伦敦穿透深度
    # ===========================================
    n_s = 1e28  # 典型超导电子密度 typical superconducting electron density
    lambda_L = london_penetration_depth(n_s)
    if lambda_L <= 0 or lambda_L > 1e-6:
        print("❌ 12.1 伦敦穿透深度不合理")
        print("   提示：检查公式 λ_L = √(m_s/(μ₀n_s(2e)²))")
        print("   - 确保使用库珀对电荷 q = 2e")
        print("   - 穿透深度通常在 10-200 nm 范围")
        all_passed = False
    else:
        print(f"✓ 12.1 伦敦穿透深度正确 (λ_L = {lambda_L*1e9:.1f} nm)")
        print(f"   参考值：Nb ≈ 40 nm, Al ≈ 50 nm")

    # ===========================================
    # 检查 12.2: I型超导体临界磁场
    # ===========================================
    Tc, Hc0 = 9.2, 2e5  # 铌的参数 Nb parameters
    Hc_half = critical_field_type1(Tc/2, Tc, Hc0)
    expected = Hc0 * (1 - 0.25)  # T = Tc/2 时，(T/Tc)² = 0.25
    if not np.isclose(Hc_half, expected, rtol=0.01):
        print("❌ 12.2 临界磁场计算错误")
        print("   提示：H_c(T) = H_c(0)[1 - (T/T_c)²]")
        print(f"   期望值: {expected:.0f} A/m, 计算值: {Hc_half:.0f} A/m")
        all_passed = False
    else:
        print(f"✓ 12.2 临界磁场正确 (H_c(T_c/2) = {Hc_half:.0f} A/m)")

    # ===========================================
    # 检查 12.3: Ginzburg-Landau参数
    # ===========================================
    kappa = ginzburg_landau_parameter(100e-9, 40e-9)
    if kappa < 1/np.sqrt(2):
        print("❌ 12.3 GL参数分类错误")
        print(f"   计算的 κ = {kappa:.2f}")
        print(f"   判据：κ > 1/√2 ≈ 0.71 为II型超导体")
        all_passed = False
    else:
        sc_type = "II型" if kappa > 1/np.sqrt(2) else "I型"
        print(f"✓ 12.3 GL参数正确 (κ = {kappa:.2f}, {sc_type}超导体)")

    # ===========================================
    # 检查 12.4: 磁通涡旋密度
    # ===========================================
    n_v = vortex_density(1)  # 1 T 磁场
    expected_n = 1 / Phi_0
    if not np.isclose(n_v, expected_n, rtol=0.01):
        print("❌ 12.4 涡旋密度计算错误")
        print("   提示：n_v = B/Φ₀")
        print(f"   Φ₀ = h/(2e) ≈ {Phi_0:.2e} Wb")
        all_passed = False
    else:
        print(f"✓ 12.4 涡旋密度正确 (B=1T 时 n_v = {n_v:.2e} m⁻²)")
        print(f"   即约 {n_v/1e12:.1f} 个涡旋/μm²")

    # ===========================================
    # 检查 12.5: BCS能隙
    # ===========================================
    Delta0 = bcs_gap_zero_temp(Tc)
    expected_ratio = 1.764
    actual_ratio = Delta0 / (k_B * Tc)
    if not np.isclose(actual_ratio, expected_ratio, rtol=0.01):
        print("❌ 12.5 BCS能隙比值错误")
        print(f"   期望 Δ(0)/k_BT_c = 1.764（弱耦合BCS）")
        print(f"   计算值: {actual_ratio:.3f}")
        all_passed = False
    else:
        print(f"✓ 12.5 BCS能隙正确 (Δ(0)/k_BT_c = {actual_ratio:.3f})")
        print(f"   Δ(0) = {Delta0/e*1000:.3f} meV (对于 Tc = {Tc} K)")

    # ===========================================
    # 检查 12.6: 约瑟夫森效应
    # ===========================================
    I = josephson_dc_current(1, np.pi/2)
    if not np.isclose(I, 1, rtol=0.01):
        print("❌ 12.6 约瑟夫森电流错误")
        print("   提示：I = I_c sin(φ)")
        print("   当 φ = π/2 时，I 应等于 I_c")
        all_passed = False
    else:
        f_J = josephson_ac_frequency(1e-6)  # 1 μV
        K_J = 2 * e / h  # 约瑟夫森常数
        print(f"✓ 12.6 约瑟夫森效应正确")
        print(f"   直流效应: I(φ=π/2) = I_c ✓")
        print(f"   交流效应: 1 μV → {f_J/1e6:.2f} MHz")
        print(f"   约瑟夫森常数 K_J = {K_J/1e9:.4f} GHz/mV")

    # ===========================================
    # 总结
    # ===========================================
    print("\n" + "-"*50)
    if all_passed:
        print("所有测试通过！超导物理计算正确。")
        print("-"*50)
        print("\n正在生成可视化图像...")
        try:
            plot_superconductivity()
        except Exception as e:
            print(f"可视化失败: {e}")
    else:
        print("部分测试未通过，请检查上述错误提示。")
        print("-"*50)
        print("\n学习建议 Study Tips:")
        print("1. 伦敦穿透深度：注意库珀对电荷是 2e")
        print("2. 临界磁场：理解超导态与热激发的竞争")
        print("3. GL参数：κ 值决定超导体类型")
        print("4. 涡旋密度：每个涡旋携带一个磁通量子")
        print("5. BCS能隙：1.764 是弱耦合极限的普适常数")
        print("6. 约瑟夫森效应：宏观量子相干的直接体现")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("超导与迈斯纳效应 Superconductivity and Meissner Effect")
    print("=" * 50)
    verify()
