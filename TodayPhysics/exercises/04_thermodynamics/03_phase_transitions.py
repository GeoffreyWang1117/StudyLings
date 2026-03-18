"""
相变 Phase Transitions
难度 Difficulty: ★★★★

学习目标 Learning Objectives:
- 理解相变的热力学描述和相平衡条件
  Understand thermodynamic description of phase transitions and equilibrium conditions
- 掌握克拉伯龙方程及其应用
  Master Clausius-Clapeyron equation and its applications
- 分析范德瓦尔斯气体和实际气体行为
  Analyze van der Waals gas and real gas behavior
- 计算临界点参数和约化状态方程
  Calculate critical point parameters and reduced equation of state
- 理解相图和三相点
  Understand phase diagrams and triple point

物理背景 Physical Background:
相变是物质在不同相态（固、液、气等）之间的转变。一级相变伴随着潜热
的吸收或释放，以及体积的突变（如沸腾、熔化）。二级相变没有潜热，
但比热、压缩系数等会发生突变（如超导转变）。

克拉伯龙方程描述了相边界上压强与温度的关系，是理解相图的关键。
范德瓦尔斯方程是描述实际气体行为的简单模型，能够定性描述气液相变。

HINT: 相平衡条件: μ₁ = μ₂（化学势相等）
HINT: 克拉伯龙方程: dP/dT = L/(T ΔV)，L 是潜热
HINT: 范德瓦尔斯方程: (P + a/V²)(V - b) = RT
HINT: 临界点条件: (∂P/∂V)_T = 0, (∂²P/∂V²)_T = 0
HINT: 对应态原理: 所有物质的约化状态方程形式相同
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import R, k_B, N_A

# I AM NOT DONE

# =============================================================================
# 练习 3.1: 相平衡条件
# Exercise 3.1: Phase Equilibrium Conditions
# =============================================================================
# 相平衡的热力学条件 Thermodynamic conditions for phase equilibrium:
#   1. 热平衡: T₁ = T₂（温度相等）
#   2. 力学平衡: P₁ = P₂（压强相等）
#   3. 化学平衡: μ₁ = μ₂（化学势相等）
#
# 化学势是单位物质的量的吉布斯自由能: μ = G/n
# 在相边界上，两相化学势相等，这决定了 P-T 相图中的相边界曲线

def chemical_potential_equality(mu1, mu2, tolerance=1e-10):
    """
    检验相平衡条件：化学势是否相等 Check phase equilibrium: chemical potential equality

    公式 Formula: μ₁ = μ₂

    参数 Parameters:
        mu1: 相1的化学势 (J/mol) - Chemical potential of phase 1
        mu2: 相2的化学势 (J/mol) - Chemical potential of phase 2
        tolerance: 允许的误差 - Allowed tolerance

    返回 Returns:
        bool: True 表示两相处于平衡
    """
    return np.abs(mu1 - mu2) < tolerance


def gibbs_free_energy_phase(H, T, S):
    """
    计算某相的吉布斯自由能 Calculate Gibbs free energy of a phase

    公式 Formula: G = H - TS

    参数 Parameters:
        H: 焓 (J) - Enthalpy
        T: 温度 (K) - Temperature
        S: 熵 (J/K) - Entropy

    返回 Returns:
        G: 吉布斯自由能 (J) - Gibbs free energy

    注意 Note:
        在恒温恒压下，系统自发向 G 减小的方向演化
        相变发生在两相 G 相等时
    """
    return H - T * S


def equilibrium_pressure(T, P0, L, T0, delta_V):
    """
    用克拉伯龙-克劳修斯方程计算平衡压力
    Calculate equilibrium pressure using Clausius-Clapeyron equation

    公式 Formula: ln(P/P₀) ≈ (L/R)(1/T₀ - 1/T)
    （假设气相为理想气体，液相体积可忽略）

    参数 Parameters:
        T: 目标温度 (K) - Target temperature
        P0: 参考压力 (Pa) - Reference pressure
        L: 相变潜热 (J/mol) - Latent heat of phase transition
        T0: 参考温度 (K) - Reference temperature
        delta_V: 体积变化（此处未使用简化形式）

    返回 Returns:
        P: 平衡压力 (Pa) - Equilibrium pressure
    """
    # TODO: 计算平衡压力（使用克拉伯龙-克劳修斯方程积分形式）
    # TODO: Calculate equilibrium pressure using integrated C-C equation
    ln_P_ratio = (L / R) * (1/T0 - 1/T)
    P = P0 * np.exp(ln_P_ratio)
    return P


# =============================================================================
# 练习 3.2: 克拉伯龙方程
# Exercise 3.2: Clausius-Clapeyron Equation
# =============================================================================
# 克拉伯龙方程是描述相边界曲线斜率的基本方程
# Clausius-Clapeyron equation describes the slope of phase boundary curves
#
# 精确形式 Exact form: dP/dT = L/(T ΔV) = ΔS/ΔV
#   - L: 相变潜热（汽化热、熔化热等）
#   - ΔV: 相变时的体积变化
#   - ΔS = L/T: 相变熵变
#
# 对于液-气相变，若假设气体为理想气体且 V_液 << V_气:
#   dP/dT ≈ LP/(RT²)
# 积分得克拉伯龙-克劳修斯方程:
#   ln(P₂/P₁) = -(L/R)(1/T₂ - 1/T₁)

def clausius_clapeyron_slope(L, T, delta_V):
    """
    克拉伯龙方程斜率 Clausius-Clapeyron equation slope

    公式 Formula: dP/dT = L/(T × ΔV)

    参数 Parameters:
        L: 相变潜热 (J/mol) - Latent heat of phase transition
        T: 温度 (K) - Temperature
        delta_V: 相变时的摩尔体积变化 (m³/mol) - Molar volume change

    返回 Returns:
        dP_dT: 相边界斜率 (Pa/K) - Slope of phase boundary

    物理意义 Physical meaning:
        - 大多数物质熔化时 ΔV > 0，故 dP/dT > 0（压力增大时熔点升高）
        - 水的反常：熔化时 ΔV < 0，故 dP/dT < 0（压力增大时熔点降低）
    """
    # TODO: 计算克拉伯龙方程斜率
    # TODO: Calculate Clausius-Clapeyron slope
    dP_dT = L / (T * delta_V)
    return dP_dT


def vapor_pressure(T, P0, T0, L_vap):
    """
    蒸汽压的克拉伯龙-克劳修斯方程 Vapor pressure from Clausius-Clapeyron

    公式 Formula: ln(P/P₀) = -(L/R)(1/T - 1/T₀)

    参数 Parameters:
        T: 目标温度 (K) - Target temperature
        P0: 参考点压力 (Pa) - Reference pressure
        T0: 参考点温度 (K) - Reference temperature
        L_vap: 汽化潜热 (J/mol) - Latent heat of vaporization

    返回 Returns:
        P: 该温度下的蒸汽压 (Pa) - Vapor pressure at temperature T

    假设 Assumptions:
        - 气相为理想气体
        - 液相体积远小于气相体积
        - 潜热不随温度变化
    """
    # TODO: 计算蒸汽压
    # TODO: Calculate vapor pressure
    ln_ratio = -(L_vap / R) * (1/T - 1/T0)
    P = P0 * np.exp(ln_ratio)
    return P


def boiling_point_elevation(P, P0, T0, L_vap):
    """
    计算沸点随压力的变化 Calculate boiling point change with pressure

    从克拉伯龙-克劳修斯方程反解温度
    ln(P/P₀) = -(L/R)(1/T - 1/T₀)
    解得: 1/T = 1/T₀ - (R/L)ln(P/P₀)

    参数 Parameters:
        P: 目标压力 (Pa) - Target pressure
        P0: 参考压力，通常取 1 atm (Pa) - Reference pressure
        T0: 参考沸点，通常取常压沸点 (K) - Reference boiling point
        L_vap: 汽化潜热 (J/mol) - Latent heat of vaporization

    返回 Returns:
        T: 该压力下的沸点 (K) - Boiling point at pressure P

    应用 Applications:
        - 高山上水的沸点降低（气压低）
        - 高压锅内水的沸点升高（气压高）
    """
    inv_T = 1/T0 - (R/L_vap) * np.log(P/P0)
    T = 1 / inv_T
    return T


def latent_heat_from_slope(dP_dT, T, delta_V):
    """
    从克拉伯龙方程斜率计算潜热 Calculate latent heat from C-C slope

    公式 Formula: L = T × ΔV × (dP/dT)

    参数 Parameters:
        dP_dT: 相边界斜率 (Pa/K) - Phase boundary slope
        T: 温度 (K) - Temperature
        delta_V: 摩尔体积变化 (m³/mol) - Molar volume change

    返回 Returns:
        L: 相变潜热 (J/mol) - Latent heat
    """
    return T * delta_V * dP_dT


# =============================================================================
# 练习 3.3: 范德瓦尔斯方程
# Exercise 3.3: Van der Waals Equation
# =============================================================================
# 范德瓦尔斯方程是对理想气体状态方程的修正
# Van der Waals equation modifies the ideal gas law to account for:
#
# 1. 分子间吸引力 Intermolecular attraction:
#    压强修正项 -an²/V²，使压强降低
#    参数 a 与分子间吸引力强度有关
#
# 2. 分子自身体积 Molecular volume:
#    体积修正项 (V - nb)，有效体积减小
#    参数 b 约等于分子自身占据的体积
#
# 方程形式 Equation form:
#   (P + an²/V²)(V - nb) = nRT
#   或: P = nRT/(V - nb) - an²/V²

def van_der_waals_pressure(V, T, a, b, n=1):
    """
    范德瓦尔斯方程计算压强 Van der Waals pressure

    公式 Formula: P = nRT/(V - nb) - an²/V²

    参数 Parameters:
        V: 体积 (m³) - Volume
        T: 温度 (K) - Temperature
        a: 吸引力参数 (Pa·m⁶/mol²) - Attraction parameter
        b: 分子体积参数 (m³/mol) - Molecular volume parameter
        n: 物质的量 (mol) - Amount of substance

    返回 Returns:
        P: 压强 (Pa) - Pressure

    典型值 Typical values (for CO₂):
        a ≈ 0.364 Pa·m⁶/mol²
        b ≈ 4.27×10⁻⁵ m³/mol
    """
    # TODO: 使用范德瓦尔斯方程计算压强
    # TODO: Calculate pressure using van der Waals equation
    P = n * R * T / (V - n * b) - a * n**2 / V**2
    return P


def van_der_waals_isotherms(V_range, T_values, a, b, n=1):
    """
    计算范德瓦尔斯等温线 Calculate van der Waals isotherms

    参数 Parameters:
        V_range: 体积数组 (m³) - Volume array
        T_values: 温度列表 (K) - List of temperatures
        a, b: 范德瓦尔斯参数 - Van der Waals parameters
        n: 物质的量 (mol) - Amount of substance

    返回 Returns:
        isotherms: 各温度对应的压强数组列表 - List of pressure arrays

    注意 Note:
        在临界温度以下，等温线会出现不稳定区域（∂P/∂V > 0）
        实际系统中这部分被气液共存区代替
    """
    isotherms = []
    for T in T_values:
        P = van_der_waals_pressure(V_range, T, a, b, n)
        isotherms.append(P)
    return isotherms


def reduced_van_der_waals(Vr, Tr):
    """
    约化范德瓦尔斯方程（对应态原理）Reduced van der Waals equation

    公式 Formula: Pr = 8Tr/(3Vr - 1) - 3/Vr²

    参数 Parameters:
        Vr: 约化体积 V/Vc - Reduced volume
        Tr: 约化温度 T/Tc - Reduced temperature

    返回 Returns:
        Pr: 约化压强 P/Pc - Reduced pressure

    对应态原理 Law of Corresponding States:
        用约化参数表示时，所有物质遵循相同的状态方程
        这说明范德瓦尔斯方程具有普适性
    """
    # TODO: 计算约化压强
    # TODO: Calculate reduced pressure
    Pr = 8 * Tr / (3 * Vr - 1) - 3 / Vr**2
    return Pr


# =============================================================================
# 练习 3.4: 临界点
# Exercise 3.4: Critical Point
# =============================================================================
# 临界点是气液相变消失的点，超过临界点后气液无法区分
# Critical point is where gas-liquid phase transition disappears
#
# 临界点条件（等温线的拐点）Critical point conditions:
#   (∂P/∂V)_T = 0  （斜率为零）
#   (∂²P/∂V²)_T = 0  （拐点）
#
# 将这两个条件应用于范德瓦尔斯方程，可以求出临界参数
# Applying these conditions to vdW equation gives critical parameters

def critical_parameters(a, b):
    """
    计算范德瓦尔斯气体的临界参数 Calculate critical parameters for vdW gas

    公式 Formulas:
        Tc = 8a/(27Rb)   临界温度
        Pc = a/(27b²)    临界压强
        Vc = 3b          临界摩尔体积

    参数 Parameters:
        a: 吸引力参数 (Pa·m⁶/mol²) - Attraction parameter
        b: 分子体积参数 (m³/mol) - Molecular volume parameter

    返回 Returns:
        Tc: 临界温度 (K) - Critical temperature
        Pc: 临界压强 (Pa) - Critical pressure
        Vc: 临界摩尔体积 (m³/mol) - Critical molar volume

    示例 Example (CO₂):
        a = 0.364, b = 4.27e-5
        Tc ≈ 304 K, Pc ≈ 7.4 MPa
    """
    # TODO: 计算临界参数
    # TODO: Calculate critical parameters
    Tc = 8 * a / (27 * R * b)
    Pc = a / (27 * b**2)
    Vc = 3 * b
    return Tc, Pc, Vc


def critical_compressibility_factor():
    """
    范德瓦尔斯气体的临界压缩因子 Critical compressibility factor for vdW gas

    公式 Formula: Zc = PcVc/(RTc) = 3/8 = 0.375

    返回 Returns:
        Zc: 临界压缩因子（无量纲）

    注意 Note:
        实际气体的 Zc 通常在 0.23-0.29 之间
        范德瓦尔斯的 0.375 偏高，说明模型有局限性
    """
    return 3/8


def van_der_waals_from_critical(Tc, Pc):
    """
    从临界参数反算范德瓦尔斯常数 Calculate vdW constants from critical parameters

    公式 Formulas:
        a = 27R²Tc²/(64Pc)
        b = RTc/(8Pc)

    参数 Parameters:
        Tc: 临界温度 (K) - Critical temperature
        Pc: 临界压强 (Pa) - Critical pressure

    返回 Returns:
        a: 吸引力参数 (Pa·m⁶/mol²)
        b: 分子体积参数 (m³/mol)

    应用 Application:
        如果知道物质的临界点数据，可以估算其 vdW 参数
    """
    # TODO: 从临界参数计算 a 和 b
    # TODO: Calculate a and b from critical parameters
    a = 27 * R**2 * Tc**2 / (64 * Pc)
    b = R * Tc / (8 * Pc)
    return a, b


def reduced_parameters(T, P, V, Tc, Pc, Vc):
    """
    计算约化参数 Calculate reduced parameters

    公式 Formulas:
        Tr = T/Tc（约化温度）
        Pr = P/Pc（约化压强）
        Vr = V/Vc（约化体积）

    参数 Parameters:
        T, P, V: 实际状态参数
        Tc, Pc, Vc: 临界参数

    返回 Returns:
        Tr, Pr, Vr: 约化参数（无量纲）

    应用 Application:
        对应态原理：用约化参数表示时，不同物质行为相似
    """
    Tr = T / Tc
    Pr = P / Pc
    Vr = V / Vc
    return Tr, Pr, Vr


# =============================================================================
# 练习 3.5: 麦克斯韦构造
# Exercise 3.5: Maxwell Construction
# =============================================================================
# 麦克斯韦构造（等面积法则）Maxwell Construction (Equal Area Rule):
#
# 范德瓦尔斯等温线在临界温度以下会出现不稳定区域（∂P/∂V > 0），
# 这在物理上是不可能的。实际系统中，这部分被水平的气液共存线代替。
#
# 麦克斯韦等面积法则 Maxwell Equal Area Rule:
#   在 P-V 图上，水平共存线与等温线围成的上下两个区域面积相等
#   数学表达: ∫[V_l to V_g] (P_sat - P_vdW) dV = 0
#
# 物理意义 Physical Meaning:
#   这保证了从液相到气相的吉布斯自由能变化为零（两相平衡）
#   ΔG = ∫V dP = 0

def maxwell_equal_area(V_range, P_isotherm, P_sat):
    """
    麦克斯韦等面积法则 Maxwell Equal Area Rule

    公式 Formula: ∫[V_l to V_g] (P_sat - P_vdW) dV = 0

    参数 Parameters:
        V_range: 体积数组 (m³) - Volume array
        P_isotherm: 等温线压强数组 (Pa) - Isotherm pressure array
        P_sat: 候选饱和蒸汽压 (Pa) - Candidate saturation pressure

    返回 Returns:
        area_diff: 上下面积差 - Difference between upper and lower areas

    注意 Note:
        找到使 area_diff = 0 的 P_sat 即为真正的饱和蒸汽压
    """
    # TODO: 找到 P = P_sat 与等温线的三个交点，计算面积差
    # TODO: Find three intersections of P = P_sat with isotherm, calculate area difference
    # 实际实现需要数值方法
    pass


def coexistence_volumes(V_range, T, a, b, n=1):
    """
    计算气液共存时的两相体积 Calculate coexisting liquid and gas volumes

    范德瓦尔斯方程变形为 V 的三次方程:
    V³ - (nb + nRT/P)V² + (an²/P)V - an³b/P = 0

    参数 Parameters:
        V_range: 体积搜索范围 (m³) - Volume search range
        T: 温度 (K)，需低于临界温度 - Temperature (must be below Tc)
        a, b: 范德瓦尔斯参数 - Van der Waals parameters
        n: 物质的量 (mol) - Amount of substance

    返回 Returns:
        V_liquid: 液相摩尔体积 (m³/mol) - Liquid molar volume
        V_gas: 气相摩尔体积 (m³/mol) - Gas molar volume

    注意 Note:
        三次方程的三个根分别对应：
        - 最小根：液相体积
        - 中间根：不稳定状态（物理上不存在）
        - 最大根：气相体积
    """
    # TODO: 求解三次方程得到共存体积
    # TODO: Solve cubic equation to get coexistence volumes
    pass


# =============================================================================
# 练习 3.6: 相图
# Exercise 3.6: Phase Diagrams
# =============================================================================
# 相图（P-T 图）Phase Diagram (P-T Diagram):
#
# 相图展示了物质在不同压强和温度下的相态，以及相边界
#
# 重要特征点 Important Features:
#   1. 三相点 Triple Point: 固、液、气三相共存的唯一 (P,T) 点
#      水的三相点: T = 273.16 K, P = 611.73 Pa
#   2. 临界点 Critical Point: 气液相变消失的终点
#      超过临界点后，物质处于超临界态
#   3. 相边界曲线 Phase Boundaries: 两相共存的 P-T 曲线
#
# 相边界斜率 Phase Boundary Slopes:
#   - 固-液边界: 通常 dP/dT > 0（冰是例外，dP/dT < 0）
#   - 液-气边界: 始终 dP/dT > 0
#   - 固-气边界: 始终 dP/dT > 0

def triple_point_conditions(P_triple, T_triple):
    """
    三相点条件 Triple Point Conditions

    在三相点，固、液、气三相同时共存，满足:
    μ_solid = μ_liquid = μ_gas

    参数 Parameters:
        P_triple: 三相点压力 (Pa) - Triple point pressure
        T_triple: 三相点温度 (K) - Triple point temperature

    返回 Returns:
        (P_triple, T_triple): 三相点坐标

    典型值 Typical Values:
        水: T = 273.16 K, P = 611.73 Pa
        CO₂: T = 216.55 K, P = 5.18 atm
    """
    return P_triple, T_triple


def phase_boundary_solid_liquid(T, P0, T0, L_fusion, delta_V_fusion):
    """
    固液相边界（用克拉伯龙方程）Solid-Liquid Phase Boundary

    公式 Formula: P = P₀ + (L_fusion / (T × ΔV)) × (T - T₀)

    参数 Parameters:
        T: 温度 (K) - Temperature
        P0: 参考点压力，通常取三相点 (Pa) - Reference pressure
        T0: 参考点温度 (K) - Reference temperature
        L_fusion: 熔化潜热 (J/mol) - Latent heat of fusion
        delta_V_fusion: 熔化时的体积变化 (m³/mol) - Volume change on melting

    返回 Returns:
        P: 固液平衡压力 (Pa) - Solid-liquid equilibrium pressure

    注意 Note:
        - 大多数物质: ΔV > 0, 故 dP/dT > 0（压力增大使熔点升高）
        - 水的反常: ΔV < 0, 故 dP/dT < 0（压力增大使冰点降低）
          这解释了冰刀滑冰的物理原理
    """
    dP_dT = clausius_clapeyron_slope(L_fusion, T, delta_V_fusion)
    P = P0 + dP_dT * (T - T0)
    return P


def phase_boundary_liquid_gas(T, P0, T0, L_vap):
    """
    液气相边界（克拉伯龙-克劳修斯方程）Liquid-Gas Phase Boundary

    使用克拉伯龙-克劳修斯方程计算蒸汽压曲线

    参数 Parameters:
        T: 温度 (K) - Temperature
        P0: 参考点压力 (Pa) - Reference pressure
        T0: 参考点温度，通常取沸点 (K) - Reference temperature
        L_vap: 汽化潜热 (J/mol) - Latent heat of vaporization

    返回 Returns:
        P: 蒸汽压（液气平衡压力）(Pa) - Vapor pressure
    """
    return vapor_pressure(T, P0, T0, L_vap)


def phase_at_PT(P, T, P_triple, T_triple, P_critical, T_critical,
                solid_liquid_func, liquid_gas_func):
    """
    判断给定 (P,T) 下的相态 Determine phase at given (P,T)

    参数 Parameters:
        P: 压力 (Pa) - Pressure
        T: 温度 (K) - Temperature
        P_triple, T_triple: 三相点坐标 - Triple point
        P_critical, T_critical: 临界点坐标 - Critical point
        solid_liquid_func: 固液边界函数 P = f(T)
        liquid_gas_func: 液气边界函数 P = f(T)

    返回 Returns:
        str: 相态 ("solid", "liquid", "gas", "supercritical")

    注意 Note:
        这是简化模型，实际相图可能更复杂（如多晶型）
    """
    if T < T_triple:
        return "solid" if P > liquid_gas_func(T) else "gas"
    elif T > T_critical:
        return "supercritical"
    else:
        P_sl = solid_liquid_func(T)
        P_lg = liquid_gas_func(T)
        if P > P_sl:
            return "solid"
        elif P > P_lg:
            return "liquid"
        else:
            return "gas"


# =============================================================================
# 练习 3.7: 潜热和相变焓
# Exercise 3.7: Latent Heat and Phase Transition Enthalpy
# =============================================================================
# 相变潜热 Latent Heat of Phase Transition:
#
# 潜热是相变过程中系统吸收或释放的热量，用于克服分子间作用力
# 而不改变温度。
#
# 类型 Types:
#   - 熔化热 L_fusion: 固→液 (冰的熔化热 ≈ 6.01 kJ/mol)
#   - 汽化热 L_vap: 液→气 (水的汽化热 ≈ 40.7 kJ/mol)
#   - 升华热 L_sub: 固→气 (L_sub ≈ L_fusion + L_vap)
#
# 基尔霍夫方程 Kirchhoff's Equation:
#   描述潜热随温度的变化: dL/dT = ΔCp
#   积分形式: L(T) = L(T₀) + ΔCp(T - T₀)

def latent_heat_vaporization(T, L0, T0, delta_Cp=0):
    """
    汽化潜热随温度的变化（基尔霍夫方程）
    Temperature dependence of latent heat (Kirchhoff's Equation)

    公式 Formula: L(T) = L(T₀) + ΔCp × (T - T₀)

    参数 Parameters:
        T: 目标温度 (K) - Target temperature
        L0: 参考温度下的潜热 (J/mol) - Latent heat at reference temperature
        T0: 参考温度 (K) - Reference temperature
        delta_Cp: 两相热容差 Cp,gas - Cp,liquid (J/mol·K)

    返回 Returns:
        L: 温度 T 下的潜热 (J/mol) - Latent heat at temperature T

    注意 Note:
        - 一般 ΔCp < 0（气相热容小于液相），潜热随温度升高而减小
        - 在临界点，L → 0（气液无法区分）
    """
    # TODO: 计算温度 T 下的潜热
    # TODO: Calculate latent heat at temperature T
    L = L0 + delta_Cp * (T - T0)
    return L


def entropy_of_vaporization(L, T):
    """
    相变熵 Entropy of Phase Transition

    公式 Formula: ΔS = L / T

    参数 Parameters:
        L: 相变潜热 (J/mol) - Latent heat
        T: 相变温度 (K) - Phase transition temperature

    返回 Returns:
        delta_S: 相变熵 (J/mol·K) - Entropy change

    物理意义 Physical Meaning:
        相变熵反映了相变前后分子有序度的变化
        - 熔化熵 ≈ 10 J/mol·K（较小）
        - 汽化熵 ≈ 85 J/mol·K（较大，气体无序度高）
    """
    return L / T


def trouton_rule():
    """
    特鲁顿规则 Trouton's Rule

    经验规律: 大多数非缔合液体在常压沸点的汽化熵约为 85 J/(mol·K)
    Empirical rule: ΔS_vap ≈ 85 J/(mol·K) for most non-associated liquids

    返回 Returns:
        85 J/(mol·K) - Trouton constant

    例外 Exceptions:
        - 水: ΔS ≈ 109 J/mol·K（氢键导致液相更有序）
        - 汞: ΔS ≈ 94 J/mol·K
        - 低沸点气体: ΔS 较小
    """
    return 85  # J/(mol·K)


def estimate_boiling_point_trouton(L_vap):
    """
    用特鲁顿规则估算沸点 Estimate boiling point using Trouton's Rule

    公式 Formula: T_b ≈ L_vap / 85

    参数 Parameters:
        L_vap: 汽化潜热 (J/mol) - Latent heat of vaporization

    返回 Returns:
        T_b: 估算的沸点 (K) - Estimated boiling point

    示例 Example:
        苯的 L_vap ≈ 30.7 kJ/mol
        估算 T_b ≈ 30700/85 ≈ 361 K（实际 353 K）
    """
    return L_vap / trouton_rule()


# =============================================================================
# 可视化 Visualization
# =============================================================================
# 本节绘制相变相关的图表:
# 1. 水的蒸汽压曲线 - 展示蒸汽压随温度的指数增长
# 2. CO₂的范德瓦尔斯等温线 - 展示临界点附近的行为
# 3. 约化状态图 - 展示对应态原理的普适性
# 4. 克拉伯龙方程斜率 - dP/dT 随温度的变化
# 5. 水的相图 - P-T 图上的相边界
# 6. 汽化熵比较 - 验证特鲁顿规则

def plot_phase_transitions():
    """
    绘制相变相关图表 Plot phase transition diagrams

    包含6个子图 Contains 6 subplots:
        1. 蒸汽压曲线 Vapor pressure curve
        2. 范德瓦尔斯等温线 Van der Waals isotherms
        3. 约化状态图 Reduced equation of state
        4. 克拉伯龙斜率 Clausius-Clapeyron slope
        5. 水的相图 Water phase diagram
        6. 汽化熵（特鲁顿规则）Entropy of vaporization
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    # 水的参数（近似值）Water parameters (approximate)
    L_vap_water = 40660  # J/mol，水的汽化热
    T_boiling = 373.15  # K，水的沸点
    P_atm = 101325  # Pa，标准大气压

    # CO2的范德瓦尔斯参数 Van der Waals parameters for CO₂
    a_CO2 = 0.3640  # Pa·m⁶/mol²，吸引力参数
    b_CO2 = 4.267e-5  # m³/mol，分子体积参数

    # 1. 蒸汽压曲线
    ax1 = axes[0, 0]
    T_range = np.linspace(273, 473, 200)
    P_vap = [vapor_pressure(T, P_atm, T_boiling, L_vap_water) / 1000 for T in T_range]

    ax1.plot(T_range - 273, P_vap, 'b-', linewidth=2)
    ax1.axhline(y=101.325, color='r', linestyle='--', label='1 atm')
    ax1.set_xlabel('Temperature (°C)')
    ax1.set_ylabel('Vapor Pressure (kPa)')
    ax1.set_title('水的蒸汽压曲线')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 范德瓦尔斯等温线
    ax2 = axes[0, 1]
    Tc, Pc, Vc = critical_parameters(a_CO2, b_CO2)
    V_range = np.linspace(1.1*b_CO2, 10*Vc, 500)

    T_ratios = [0.85, 0.9, 0.95, 1.0, 1.1]
    for Tr in T_ratios:
        T = Tr * Tc
        P = van_der_waals_pressure(V_range, T, a_CO2, b_CO2)
        # 限制P的范围以便可视化
        P = np.clip(P, -1e6, 2*Pc)
        ax2.plot(V_range*1e6, P/1e6, label=f'T/Tc = {Tr}', linewidth=1.5)

    ax2.axhline(y=Pc/1e6, color='k', linestyle='--', alpha=0.5)
    ax2.set_xlabel('V (cm³/mol)')
    ax2.set_ylabel('P (MPa)')
    ax2.set_title('CO₂范德瓦尔斯等温线')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-1, 15)

    # 3. 约化状态图
    ax3 = axes[0, 2]
    Vr_range = np.linspace(0.4, 4, 200)
    Tr_values = [0.85, 0.9, 0.95, 1.0, 1.1, 1.2]

    for Tr in Tr_values:
        Pr = reduced_van_der_waals(Vr_range, Tr)
        Pr = np.clip(Pr, -0.5, 3)
        ax3.plot(Vr_range, Pr, label=f'Tr = {Tr}', linewidth=1.5)

    ax3.axhline(y=1, color='k', linestyle='--', alpha=0.5)
    ax3.axvline(x=1, color='k', linestyle='--', alpha=0.5)
    ax3.set_xlabel('Vr = V/Vc')
    ax3.set_ylabel('Pr = P/Pc')
    ax3.set_title('约化状态图（对应态原理）')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim(-0.5, 3)

    # 4. 克拉伯龙斜率
    ax4 = axes[1, 0]
    T_range = np.linspace(300, 400, 100)
    # 假设ΔV_vap = RT/P（理想气体）
    delta_V = R * T_range / P_atm
    dP_dT = [clausius_clapeyron_slope(L_vap_water, T, dV) for T, dV in zip(T_range, delta_V)]

    ax4.plot(T_range - 273, dP_dT, 'g-', linewidth=2)
    ax4.set_xlabel('Temperature (°C)')
    ax4.set_ylabel('dP/dT (Pa/K)')
    ax4.set_title('克拉伯龙方程斜率')
    ax4.grid(True, alpha=0.3)

    # 5. 相图示意（水的P-T图）
    ax5 = axes[1, 1]
    # 简化的水相图
    T_triple = 273.16  # K
    P_triple = 611.73  # Pa
    T_critical = 647.1  # K
    P_critical = 22.064e6  # Pa

    # 固-液线（近似直线，斜率为负）
    T_sl = np.linspace(T_triple, 300, 50)
    P_sl = P_triple + (-1e7) * (T_sl - T_triple)  # 简化

    # 液-气线
    T_lg = np.linspace(T_triple, T_critical, 100)
    P_lg = [vapor_pressure(T, P_atm, 373.15, L_vap_water) for T in T_lg]

    # 固-气线（升华）
    T_sg = np.linspace(200, T_triple, 50)
    L_sub = 51000  # 升华热 J/mol
    P_sg = [vapor_pressure(T, P_triple, T_triple, L_sub) for T in T_sg]

    ax5.semilogy(T_sl - 273, np.abs(P_sl)/1e3, 'b-', label='Solid-Liquid', linewidth=2)
    ax5.semilogy(T_lg - 273, np.array(P_lg)/1e3, 'r-', label='Liquid-Gas', linewidth=2)
    ax5.semilogy(T_sg - 273, np.array(P_sg)/1e3, 'g-', label='Solid-Gas', linewidth=2)
    ax5.plot(T_triple - 273, P_triple/1e3, 'ko', markersize=10, label='Triple Point')
    ax5.plot(T_critical - 273, P_critical/1e3, 'r*', markersize=15, label='Critical Point')

    ax5.set_xlabel('Temperature (°C)')
    ax5.set_ylabel('Pressure (kPa)')
    ax5.set_title('水的相图（示意）')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. 汽化熵（特鲁顿规则）
    ax6 = axes[1, 2]
    # 各种物质的汽化数据
    substances = ['H₂O', 'C₂H₅OH', 'C₆H₆', 'CCl₄', 'Hg']
    L_vap_values = [40660, 38600, 30720, 29820, 59150]  # J/mol
    T_bp_values = [373.15, 351.4, 353.2, 349.9, 629.9]  # K

    delta_S = [L/T for L, T in zip(L_vap_values, T_bp_values)]

    ax6.bar(substances, delta_S, color='steelblue', alpha=0.7)
    ax6.axhline(y=85, color='r', linestyle='--', label='Trouton (85 J/mol·K)')
    ax6.set_ylabel('ΔS_vap (J/mol·K)')
    ax6.set_title('汽化熵（特鲁顿规则）')
    ax6.legend()
    ax6.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('phase_transitions.png', dpi=150)
    print("图像已保存为 phase_transitions.png")
    plt.show()


def verify():
    """
    验证相变练习的正确性 Verify phase transition exercises

    测试内容 Test Contents:
        - 3.2 克拉伯龙方程斜率
        - 3.3 范德瓦尔斯方程压力计算
        - 3.4 临界参数和压缩因子
        - 3.6 约化范德瓦尔斯方程
        - 3.7 汽化熵计算
    """
    all_passed = True

    # 测试 3.2 - 克拉伯龙方程 Clausius-Clapeyron equation
    L = 40660  # J/mol (水的汽化热 latent heat of water)
    T = 373.15  # K (水的沸点 boiling point)
    delta_V = R * T / 101325  # 近似为理想气体 approximate as ideal gas
    dP_dT = clausius_clapeyron_slope(L, T, delta_V)
    if dP_dT <= 0:
        print("错误 3.2: 克拉伯龙方程斜率应为正值")
        print("  提示: 汽化时 L > 0, ΔV > 0，故 dP/dT > 0")
        all_passed = False
    else:
        print(f"通过 3.2: 克拉伯龙方程正确 (dP/dT = {dP_dT:.1f} Pa/K)")

    # 测试 3.3 - 范德瓦尔斯方程 Van der Waals equation
    a, b = 0.3640, 4.267e-5  # CO2 的参数
    V_test = 1e-3  # m³
    T_test = 300  # K
    P_vdw = van_der_waals_pressure(V_test, T_test, a, b)
    P_ideal = R * T_test / V_test
    if P_vdw >= P_ideal:
        print("错误 3.3: 范德瓦尔斯压力应低于理想气体压力")
        print("  提示: 在此体积下，分子间吸引力占主导，使压力降低")
        print(f"  P_vdW = {P_vdw/1e6:.3f} MPa, P_ideal = {P_ideal/1e6:.3f} MPa")
        all_passed = False
    else:
        print(f"通过 3.3: 范德瓦尔斯方程正确 (P_vdW = {P_vdw/1e6:.3f} MPa)")

    # 测试 3.4 - 临界参数 Critical parameters
    Tc, Pc, Vc = critical_parameters(a, b)
    Zc = Pc * Vc / (R * Tc)
    if not np.isclose(Zc, 0.375, rtol=0.01):
        print("错误 3.4: 临界压缩因子应为 3/8 = 0.375")
        print(f"  计算得到的 Zc = {Zc:.4f}")
        print("  提示: 检查 Tc, Pc, Vc 的计算公式")
        all_passed = False
    else:
        print(f"通过 3.4: 临界参数正确 (Tc={Tc:.1f}K, Pc={Pc/1e6:.2f}MPa, Zc={Zc:.3f})")

    # 测试 3.4 续 - 从临界参数反算 Reverse calculation from critical parameters
    a_back, b_back = van_der_waals_from_critical(Tc, Pc)
    if not (np.isclose(a_back, a, rtol=0.01) and np.isclose(b_back, b, rtol=0.01)):
        print("错误 3.4: 从临界参数反算范德瓦尔斯常数不一致")
        print(f"  原始: a = {a}, b = {b}")
        print(f"  反算: a = {a_back}, b = {b_back}")
        all_passed = False
    else:
        print("通过 3.4: 临界参数反算正确")

    # 测试 3.6 - 约化方程 Reduced equation
    Pr = reduced_van_der_waals(1, 1)  # 在临界点 at critical point
    if not np.isclose(Pr, 1, rtol=0.01):
        print("错误 3.6: 约化方程在临界点应给出 Pr = 1")
        print(f"  计算得到的 Pr = {Pr:.4f}")
        print("  提示: 在 Vr = Tr = 1 时，Pr 也应为 1")
        all_passed = False
    else:
        print("通过 3.6: 约化范德瓦尔斯方程正确")

    # 测试 3.7 - 特鲁顿规则 Trouton's rule
    delta_S_water = entropy_of_vaporization(40660, 373.15)
    if not np.isclose(delta_S_water, 109, rtol=0.1):  # 水略高于85
        print("错误 3.7: 汽化熵计算错误")
        print("  提示: ΔS = L / T")
        all_passed = False
    else:
        print(f"通过 3.7: 汽化熵正确 (水的汽化熵 = {delta_S_water:.1f} J/mol·K)")

    if all_passed:
        print("\n所有测试通过！")
        try:
            plot_phase_transitions()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("相变 Phase Transitions")
    print("=" * 50)
    verify()
