"""
热机循环 Heat Engine Cycles (Otto and Diesel)
难度 Difficulty: ★★★

学习目标 Learning Objectives:
- 理解热机的工作原理和效率极限
  Understand working principles and efficiency limits of heat engines
- 掌握Otto循环（汽油机）和Diesel循环（柴油机）的分析
  Master analysis of Otto cycle (gasoline engine) and Diesel cycle (diesel engine)
- 比较不同热力学循环的性能特点
  Compare performance characteristics of different thermodynamic cycles
- 理解布雷顿循环（燃气轮机）和斯特林循环
  Understand Brayton cycle (gas turbine) and Stirling cycle
- 计算平均有效压力和功率输出
  Calculate mean effective pressure and power output

物理背景 Physical Background:
热机是将热能转化为机械功的装置。根据热力学第二定律，任何热机的效率
都不能超过工作在相同温度范围的卡诺热机的效率。

实际热机（如内燃机）的循环与卡诺循环不同，但可以通过简化的理想循环
来分析其理论效率上限。Otto循环描述汽油机（等容加热），Diesel循环
描述柴油机（等压加热）。

HINT: 卡诺效率: eta_Carnot = 1 - T_cold/T_hot（理论上限）
HINT: Otto效率: eta_Otto = 1 - 1/r^(gamma-1)，r是压缩比
HINT: Diesel效率取决于压缩比r和截止比r_c
HINT: 压缩比越高效率越高，但受限于爆震（汽油机）或材料强度（柴油机）
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import R

# I AM NOT DONE

# 空气的热力学参数（理想气体近似）Thermodynamic parameters of air (ideal gas approximation)
gamma = 1.4  # 绝热指数 γ = Cp/Cv（双原子气体如空气、N₂、O₂）
Cv = R / (gamma - 1)  # 定容摩尔热容 (J/mol·K)
Cp = gamma * R / (gamma - 1)  # 定压摩尔热容 (J/mol·K)

# =============================================================================
# 练习 1.1: 卡诺循环
# Exercise 1.1: Carnot Cycle
# =============================================================================
# 卡诺循环是理想化的可逆热机循环，由两个等温过程和两个绝热过程组成
# Carnot cycle: the ideal reversible heat engine with maximum efficiency
#
# 循环过程 Cycle Processes:
#   1→2: 等温膨胀（吸热 Q_H）Isothermal expansion at T_H
#   2→3: 绝热膨胀（温度降低）Adiabatic expansion
#   3→4: 等温压缩（放热 Q_C）Isothermal compression at T_C
#   4→1: 绝热压缩（温度升高）Adiabatic compression
#
# 卡诺定理 Carnot's Theorem:
#   所有工作在相同温度范围的热机中，卡诺热机效率最高

def carnot_efficiency(T_hot, T_cold):
    """
    卡诺效率（理想热机的最大效率）Carnot efficiency (maximum efficiency)

    公式 Formula: η = 1 - T_cold/T_hot = (T_hot - T_cold)/T_hot

    参数 Parameters:
        T_hot: 高温热源温度 (K) - Hot reservoir temperature
        T_cold: 低温热源温度 (K) - Cold reservoir temperature

    返回 Returns:
        eta: 卡诺效率（无量纲，0 到 1 之间）

    物理意义 Physical Meaning:
        - 效率只取决于温度比，与工作物质无关
        - T_cold → 0 时，η → 1（实际不可达）
        - T_cold = T_hot 时，η = 0（无温差则无法做功）
    """
    # TODO: 计算卡诺效率
    # TODO: Calculate Carnot efficiency
    eta = 1 - T_cold / T_hot
    return eta


def carnot_work(Q_hot, T_hot, T_cold):
    """
    卡诺热机做的功 Work output of Carnot engine

    公式 Formula: W = Q_hot × η = Q_hot × (1 - T_cold/T_hot)

    参数 Parameters:
        Q_hot: 从高温热源吸收的热量 (J) - Heat absorbed from hot reservoir
        T_hot: 高温热源温度 (K) - Hot reservoir temperature
        T_cold: 低温热源温度 (K) - Cold reservoir temperature

    返回 Returns:
        W: 对外做的净功 (J) - Net work output

    能量守恒 Energy Conservation:
        Q_hot = W + Q_cold
    """
    eta = carnot_efficiency(T_hot, T_cold)
    return Q_hot * eta


def carnot_cop_heat_pump(T_hot, T_cold):
    """
    卡诺热泵的制热系数 COP of Carnot heat pump

    公式 Formula: COP_HP = Q_hot/W = T_hot/(T_hot - T_cold)

    参数 Parameters:
        T_hot: 供暖温度（室内）(K) - Heating temperature (indoor)
        T_cold: 室外温度 (K) - Outdoor temperature

    返回 Returns:
        COP_HP: 制热系数（始终 > 1）- Coefficient of Performance for heating

    物理意义 Physical Meaning:
        COP > 1 说明热泵比直接电加热更高效
        例如 COP = 4 表示每消耗 1J 电能可传递 4J 热量
    """
    return T_hot / (T_hot - T_cold)


def carnot_cop_refrigerator(T_hot, T_cold):
    """
    卡诺制冷机的制冷系数 COP of Carnot refrigerator

    公式 Formula: COP_R = Q_cold/W = T_cold/(T_hot - T_cold)

    参数 Parameters:
        T_hot: 室外温度 (K) - Outdoor temperature
        T_cold: 制冷温度（冰箱内）(K) - Cooling temperature (inside refrigerator)

    返回 Returns:
        COP_R: 制冷系数 - Coefficient of Performance for refrigeration

    关系 Relationship:
        COP_HP = COP_R + 1
    """
    return T_cold / (T_hot - T_cold)


# =============================================================================
# 练习 1.2: Otto循环（汽油机）
# Exercise 1.2: Otto Cycle (Gasoline Engine)
# =============================================================================
# Otto循环是汽油机的理想热力学循环
# Otto cycle is the ideal thermodynamic cycle for gasoline engines
#
# 循环过程 Cycle Processes:
#   1→2: 绝热压缩（活塞上行，压缩混合气）Adiabatic compression
#   2→3: 等容加热（火花塞点火，瞬间燃烧）Isochoric heating (spark ignition)
#   3→4: 绝热膨胀（做功冲程）Adiabatic expansion (power stroke)
#   4→1: 等容放热（排气阀打开）Isochoric cooling (exhaust)
#
# 关键参数 Key Parameter:
#   压缩比 r = V_max/V_min（典型汽油机 r = 8-12）
#   压缩比越高，效率越高，但受爆震限制

def otto_efficiency(r, gamma=1.4):
    """
    Otto循环效率 Otto cycle efficiency

    公式 Formula: η = 1 - 1/r^(γ-1)

    参数 Parameters:
        r: 压缩比 V_max/V_min（无量纲）- Compression ratio
        gamma: 绝热指数 Cp/Cv，空气约为 1.4

    返回 Returns:
        eta: Otto循环效率 - Otto cycle efficiency

    典型值 Typical Values:
        r = 10, γ = 1.4: η ≈ 60%
        实际汽油机效率约 25-30%（各种损失）
    """
    # TODO: 计算 Otto 循环效率
    # TODO: Calculate Otto cycle efficiency
    eta = 1 - 1 / r**(gamma - 1)
    return eta


def otto_cycle_states(T1, P1, r, Q_in, n=1):
    """
    计算Otto循环的四个状态点 Calculate state points of Otto cycle

    循环过程 Cycle Processes:
        1→2: 绝热压缩 Adiabatic compression
        2→3: 等容加热 Isochoric heating
        3→4: 绝热膨胀 Adiabatic expansion
        4→1: 等容放热 Isochoric cooling

    参数 Parameters:
        T1: 初始温度 (K)，进气温度 - Initial temperature
        P1: 初始压力 (Pa)，约 1 atm - Initial pressure
        r: 压缩比 - Compression ratio
        Q_in: 输入热量 (J) - Heat input
        n: 物质的量 (mol) - Amount of substance

    返回 Returns:
        (T, P, V): 四个状态点的温度、压力、体积数组
    """
    # 状态1 (初始/进气后) State 1 (after intake)
    V1 = n * R * T1 / P1

    # 状态2 (绝热压缩后) State 2 (after adiabatic compression)
    V2 = V1 / r
    T2 = T1 * r**(gamma - 1)  # TV^(γ-1) = 常数
    P2 = P1 * r**gamma  # PV^γ = 常数

    # 状态3 (等容加热后/点火燃烧后) State 3 (after combustion)
    V3 = V2  # 等容过程
    # Q_in = n × Cv × (T3 - T2)
    T3 = T2 + Q_in / (n * Cv)
    P3 = P2 * T3 / T2  # 等容过程 P/T = 常数

    # 状态4 (绝热膨胀后/做功冲程结束) State 4 (after power stroke)
    V4 = V1  # 膨胀回原体积
    T4 = T3 / r**(gamma - 1)
    P4 = P3 / r**gamma

    T = [T1, T2, T3, T4]
    P = [P1, P2, P3, P4]
    V = [V1, V2, V3, V4]

    return np.array(T), np.array(P), np.array(V)


def otto_work_output(T1, r, Q_in, n=1):
    """
    Otto循环的净功 Net work of Otto cycle

    公式 Formula: W = Q_in × η

    参数 Parameters:
        T1: 初始温度 (K) - Initial temperature
        r: 压缩比 - Compression ratio
        Q_in: 输入热量 (J) - Heat input
        n: 物质的量 (mol) - Amount of substance

    返回 Returns:
        W: 净功 (J) - Net work output
    """
    eta = otto_efficiency(r)
    return Q_in * eta


# =============================================================================
# 练习 1.3: Diesel循环（柴油机）
# Exercise 1.3: Diesel Cycle (Diesel Engine)
# =============================================================================
# Diesel循环是柴油机的理想热力学循环
# Diesel cycle is the ideal thermodynamic cycle for diesel engines
#
# 循环过程 Cycle Processes:
#   1→2: 绝热压缩（只压缩空气，压缩比很高）Adiabatic compression
#   2→3: 等压加热（喷入柴油，燃烧膨胀）Isobaric heating (fuel injection)
#   3→4: 绝热膨胀（做功冲程）Adiabatic expansion
#   4→1: 等容放热（排气）Isochoric cooling
#
# 与Otto循环的区别 Difference from Otto:
#   - Diesel是等压加热（燃油连续喷射）
#   - Otto是等容加热（火花塞瞬间点火）
#   - Diesel压缩比更高（14-22），因为只压缩空气，无爆震问题

def diesel_efficiency(r, r_c, gamma=1.4):
    """
    Diesel循环效率 Diesel cycle efficiency

    公式 Formula: η = 1 - (1/r^(γ-1)) × (r_c^γ - 1)/(γ(r_c - 1))

    参数 Parameters:
        r: 压缩比 V_max/V_min（柴油机典型值 14-22）- Compression ratio
        r_c: 截止比 V_3/V_2，等压膨胀比（典型值 1.5-3）- Cutoff ratio
        gamma: 绝热指数 - Heat capacity ratio

    返回 Returns:
        eta: Diesel循环效率

    注意 Note:
        当 r_c → 1 时，Diesel效率趋近于Otto效率
        r_c 越大，燃烧时间越长，效率略有降低
    """
    # TODO: 计算 Diesel 循环效率
    # TODO: Calculate Diesel cycle efficiency
    factor = (r_c**gamma - 1) / (gamma * (r_c - 1))
    eta = 1 - (1 / r**(gamma - 1)) * factor
    return eta


def diesel_cycle_states(T1, P1, r, r_c, n=1):
    """
    计算Diesel循环的四个状态点 Calculate state points of Diesel cycle

    循环过程 Cycle Processes:
        1→2: 绝热压缩 Adiabatic compression
        2→3: 等压加热 Isobaric heating
        3→4: 绝热膨胀 Adiabatic expansion
        4→1: 等容放热 Isochoric cooling

    参数 Parameters:
        T1: 初始温度 (K) - Initial temperature
        P1: 初始压力 (Pa) - Initial pressure
        r: 压缩比 - Compression ratio
        r_c: 截止比 V_3/V_2 - Cutoff ratio
        n: 物质的量 (mol) - Amount of substance

    返回 Returns:
        (T, P, V): 四个状态点的温度、压力、体积数组
    """
    # 状态1 (初始) State 1
    V1 = n * R * T1 / P1

    # 状态2 (绝热压缩后) State 2 (压缩后温度很高，可点燃柴油)
    V2 = V1 / r
    T2 = T1 * r**(gamma - 1)  # 可达 700-900 K
    P2 = P1 * r**gamma

    # 状态3 (等压加热后/燃烧结束) State 3 (等压燃烧)
    P3 = P2  # 等压过程
    V3 = V2 * r_c  # 体积膨胀
    T3 = T2 * r_c  # 等压过程 V/T = 常数

    # 状态4 (绝热膨胀后) State 4
    V4 = V1
    # 膨胀比 = V4/V3 = V1/(V2 × r_c) = r/r_c
    expansion_ratio = r / r_c
    T4 = T3 / expansion_ratio**(gamma - 1)
    P4 = P3 / expansion_ratio**gamma

    T = [T1, T2, T3, T4]
    P = [P1, P2, P3, P4]
    V = [V1, V2, V3, V4]

    return np.array(T), np.array(P), np.array(V)


# =============================================================================
# 练习 1.4: 热量和功的计算
# Exercise 1.4: Heat and Work Calculation
# =============================================================================
# 热力学第一定律应用 Application of First Law:
#   ΔU = Q - W（系统内能变化 = 吸热 - 做功）
#
# 各过程的热量计算 Heat Calculation:
#   - 等容过程: Q = n × Cv × ΔT（体积不变，W = 0）
#   - 等压过程: Q = n × Cp × ΔT
#   - 绝热过程: Q = 0
#   - 等温过程: Q = W = nRT ln(V2/V1)

def heat_input_otto(T2, T3, n=1):
    """
    Otto循环的吸热量（等容加热过程）Heat input in Otto cycle

    公式 Formula: Q_in = n × Cv × (T3 - T2)

    参数 Parameters:
        T2: 压缩后温度 (K) - Temperature after compression
        T3: 燃烧后温度 (K) - Temperature after combustion
        n: 物质的量 (mol) - Amount of substance

    返回 Returns:
        Q_in: 吸热量 (J)，模拟燃烧释放的热量

    注意 Note:
        等容过程中 W = 0，所有热量用于增加内能
    """
    return n * Cv * (T3 - T2)


def heat_input_diesel(T2, T3, n=1):
    """
    Diesel循环的吸热量（等压加热过程）Heat input in Diesel cycle

    公式 Formula: Q_in = n × Cp × (T3 - T2)

    参数 Parameters:
        T2: 压缩后温度 (K) - Temperature after compression
        T3: 燃烧结束温度 (K) - Temperature after combustion
        n: 物质的量 (mol) - Amount of substance

    返回 Returns:
        Q_in: 吸热量 (J)

    注意 Note:
        等压过程中使用 Cp 而非 Cv，因为部分热量用于膨胀做功
    """
    return n * Cp * (T3 - T2)


def heat_rejected(T4, T1, n=1):
    """
    放热量（等容放热过程）Heat rejected in cycle

    公式 Formula: Q_out = n × Cv × (T4 - T1)

    参数 Parameters:
        T4: 膨胀后温度 (K) - Temperature after expansion
        T1: 初始温度 (K) - Initial temperature
        n: 物质的量 (mol) - Amount of substance

    返回 Returns:
        Q_out: 放热量 (J)，排放到低温热源（大气）的热量
    """
    return n * Cv * (T4 - T1)


def net_work_from_heat(Q_in, Q_out):
    """
    从热量计算净功 Net work from heat

    公式 Formula: W = Q_in - Q_out

    参数 Parameters:
        Q_in: 吸热量 (J) - Heat absorbed
        Q_out: 放热量 (J) - Heat rejected

    返回 Returns:
        W: 净功 (J) - Net work output

    物理意义 Physical Meaning:
        根据能量守恒，净功等于吸热减去放热
        效率 η = W/Q_in = 1 - Q_out/Q_in
    """
    return Q_in - Q_out


# =============================================================================
# 练习 1.5: 平均有效压力
# Exercise 1.5: Mean Effective Pressure
# =============================================================================
# 平均有效压力（MEP）是评价发动机性能的重要指标
# Mean Effective Pressure is a key parameter for engine performance comparison
#
# MEP 允许比较不同排量的发动机
# 自然吸气汽油机 MEP 约 8-11 bar
# 涡轮增压汽油机 MEP 可达 12-18 bar
# 柴油机 MEP 约 8-25 bar

def mean_effective_pressure(W, V_displacement):
    """
    平均有效压力 Mean Effective Pressure (MEP)

    公式 Formula: MEP = W / V_displacement

    参数 Parameters:
        W: 每循环净功 (J) - Net work per cycle
        V_displacement: 气缸排量 V_max - V_min (m³) - Displacement volume

    返回 Returns:
        MEP: 平均有效压力 (Pa) - Mean effective pressure

    物理意义 Physical Meaning:
        MEP 表示等效于在整个冲程中施加的恒定压力
        是衡量发动机"做功密度"的指标
    """
    return W / V_displacement


def power_output(W, rpm, n_cylinders=4, strokes=4):
    """
    发动机功率 Engine power output

    公式 Formula (四冲程): P = W × (rpm/60) × n_cylinders / 2

    参数 Parameters:
        W: 每循环每缸净功 (J) - Net work per cycle per cylinder
        rpm: 发动机转速 (转/分钟) - Engine speed
        n_cylinders: 气缸数 - Number of cylinders
        strokes: 冲程数（2或4）- Number of strokes per cycle

    返回 Returns:
        Power: 功率 (W) - Power output

    注意 Note:
        四冲程发动机：曲轴转两圈完成一个循环
        二冲程发动机：曲轴转一圈完成一个循环
    """
    # cycles_per_second: 每秒完成的工作循环数
    cycles_per_second = (rpm / 60) / (strokes / 2)
    return W * cycles_per_second * n_cylinders


# =============================================================================
# 练习 1.6: 压缩比优化
# Exercise 1.6: Compression Ratio Optimization
# =============================================================================
# 压缩比与效率的权衡 Trade-off between Compression Ratio and Efficiency:
#
# 理论上压缩比越高效率越高，但受到限制：
#   1. 汽油机：爆震（敲缸）限制，压缩比过高会导致混合气自燃
#      - 普通汽油（92号）: r ≈ 8-10
#      - 高标号汽油（95/98号）: r ≈ 10-12
#   2. 柴油机：材料强度限制（高压缩比产生高温高压）
#      - 典型 r = 14-22
#
# 辛烷值 Octane Number:
#   表示汽油抗爆性能，辛烷值越高，允许的压缩比越高

def optimal_compression_otto(T_max, T1, gamma=1.4):
    """
    给定最高温度限制计算最优压缩比
    Calculate optimal compression ratio given temperature limit

    公式 Formula: r_max = (T_max/T1)^(1/(γ-1))

    参数 Parameters:
        T_max: 允许的最高压缩温度 (K)，受自燃限制
        T1: 进气温度 (K) - Intake temperature
        gamma: 绝热指数 - Heat capacity ratio

    返回 Returns:
        r_max: 最大允许压缩比 - Maximum compression ratio

    注意 Note:
        实际压缩比还需考虑其他因素（材料强度、润滑等）
    """
    r_max = (T_max / T1)**(1 / (gamma - 1))
    return r_max


def efficiency_vs_compression_ratio():
    """
    计算效率与压缩比的关系 Calculate efficiency vs compression ratio

    返回 Returns:
        r_range: 压缩比范围 5-25
        eta_otto: Otto循环效率数组
        eta_diesel: Diesel循环效率数组（假设 r_c = 2）

    用途 Usage:
        用于绘制效率-压缩比曲线，比较不同循环的性能
    """
    r_range = np.linspace(5, 25, 100)
    eta_otto = [otto_efficiency(r) for r in r_range]
    # 对于 Diesel，假设截止比 r_c = 2
    eta_diesel = [diesel_efficiency(r, 2) for r in r_range]

    return r_range, np.array(eta_otto), np.array(eta_diesel)


def knocking_compression_ratio(octane_number):
    """
    根据辛烷值估算允许的压缩比 Estimate compression ratio from octane number

    公式 Formula (简化): r_max ≈ 4 + octane_number/10

    参数 Parameters:
        octane_number: 辛烷值（RON），如 92、95、98 号汽油

    返回 Returns:
        r_max: 估算的最大压缩比

    典型值 Typical Values:
        92号汽油: r ≈ 8.2
        95号汽油: r ≈ 9.5
        98号汽油: r ≈ 9.8

    注意 Note:
        这是简化的经验关系，实际还受发动机设计影响
    """
    return 4 + octane_number / 10


# =============================================================================
# 练习 1.7: 其他热力学循环
# Exercise 1.7: Other Thermodynamic Cycles
# =============================================================================
# 其他重要的热力学循环 Other Important Thermodynamic Cycles:
#
# 1. 布雷顿循环 Brayton Cycle（燃气轮机、喷气发动机）
#    - 两个等压过程 + 两个绝热过程
#    - 开式系统，连续流动
#
# 2. 斯特林循环 Stirling Cycle（斯特林发动机）
#    - 两个等温过程 + 两个等容过程 + 回热器
#    - 理论效率等于卡诺效率
#
# 3. 朗肯循环 Rankine Cycle（蒸汽轮机、火力发电）
#    - 相变循环，工质经历液-气-液转变
#    - 发电厂的主要循环形式

def brayton_efficiency(r_p, gamma=1.4):
    """
    布雷顿循环效率（燃气轮机）Brayton cycle efficiency

    公式 Formula: η = 1 - 1/r_p^((γ-1)/γ)

    参数 Parameters:
        r_p: 压力比 P_max/P_min（燃气轮机典型值 10-30）
        gamma: 绝热指数 - Heat capacity ratio

    返回 Returns:
        eta: 布雷顿循环效率

    应用 Applications:
        - 喷气发动机（航空）
        - 燃气轮机发电
        - 联合循环发电（燃气轮机 + 蒸汽轮机）
    """
    exponent = (gamma - 1) / gamma
    eta = 1 - 1 / r_p**exponent
    return eta


def stirling_efficiency(T_hot, T_cold):
    """
    理想斯特林循环效率 Ideal Stirling cycle efficiency

    公式 Formula: η = 1 - T_cold/T_hot（等于卡诺效率）

    参数 Parameters:
        T_hot: 高温热源温度 (K) - Hot source temperature
        T_cold: 低温热源温度 (K) - Cold sink temperature

    返回 Returns:
        eta: 斯特林循环效率

    注意 Note:
        - 理论上可达卡诺效率（通过回热器实现）
        - 实际效率通常为卡诺效率的 30-40%
        - 优点：外燃式，可使用多种热源，低噪音
    """
    return carnot_efficiency(T_hot, T_cold)


def rankine_efficiency(T_boiler, T_condenser, eta_turbine=0.85, eta_pump=0.80):
    """
    简化的朗肯循环效率估算 Simplified Rankine cycle efficiency estimate

    参数 Parameters:
        T_boiler: 锅炉温度 (K)，蒸汽产生温度 - Boiler temperature
        T_condenser: 冷凝器温度 (K) - Condenser temperature
        eta_turbine: 汽轮机效率（0.8-0.9）- Turbine efficiency
        eta_pump: 水泵效率（0.7-0.9）- Pump efficiency

    返回 Returns:
        eta: 朗肯循环效率估算值

    应用 Applications:
        - 火力发电厂（燃煤、燃气、核电）
        - 实际效率约 30-45%

    注意 Note:
        这是简化估算，实际需考虑过热、再热、回热等改进措施
    """
    eta_carnot = carnot_efficiency(T_boiler, T_condenser)
    # 实际效率通常是卡诺效率的 60-70%
    return eta_carnot * 0.65 * eta_turbine


# =============================================================================
# 可视化 Visualization
# =============================================================================
# 本节绘制热机循环相关的图表:
# 1. Otto循环的 P-V 图 - 展示四个冲程
# 2. 效率与压缩比的关系 - 比较 Otto 和 Diesel
# 3. 卡诺效率与温度的关系 - 不同热机的理论极限
# 4. Otto循环的 T-S 图 - 熵变分析

def plot_heat_engines():
    """
    绘制热机循环相关图表 Plot heat engine cycle diagrams

    包含4个子图 Contains 4 subplots:
        1. Otto循环 P-V 图
        2. 效率 vs 压缩比曲线
        3. 卡诺效率 vs 温度曲线
        4. Otto循环 T-S 图
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # 1. Otto循环 P-V图
    ax1 = axes[0, 0]
    T1, P1 = 300, 1e5  # 初始状态
    r = 10  # 压缩比
    Q_in = 1000  # J (假设n=1 mol的情况)

    T_otto, P_otto, V_otto = otto_cycle_states(T1, P1, r, Q_in)

    # 绘制循环
    V_plot = list(V_otto) + [V_otto[0]]
    P_plot = list(P_otto) + [P_otto[0]]

    # 绝热过程需要更多点
    V_12 = np.linspace(V_otto[0], V_otto[1], 50)
    P_12 = P_otto[0] * (V_otto[0] / V_12)**gamma

    V_34 = np.linspace(V_otto[2], V_otto[3], 50)
    P_34 = P_otto[2] * (V_otto[2] / V_34)**gamma

    ax1.plot(V_12 * 1e6, P_12 / 1e5, 'b-', linewidth=2)
    ax1.plot([V_otto[1], V_otto[2]] * np.array([1e6, 1e6]),
             [P_otto[1], P_otto[2]] / 1e5, 'r-', linewidth=2)
    ax1.plot(V_34 * 1e6, P_34 / 1e5, 'b-', linewidth=2)
    ax1.plot([V_otto[3], V_otto[0]] * np.array([1e6, 1e6]),
             [P_otto[3], P_otto[0]] / 1e5, 'r-', linewidth=2)

    for i, (v, p) in enumerate(zip(V_otto, P_otto)):
        ax1.scatter(v * 1e6, p / 1e5, s=100, zorder=5)
        ax1.annotate(f'{i+1}', (v * 1e6, p / 1e5), fontsize=12)

    ax1.set_xlabel('Volume (cm^3)')
    ax1.set_ylabel('Pressure (bar)')
    ax1.set_title(f'Otto Cycle (r={r}, eta={otto_efficiency(r)*100:.1f}%)')
    ax1.grid(True, alpha=0.3)

    # 2. 效率 vs 压缩比
    ax2 = axes[0, 1]
    r_range, eta_otto, eta_diesel = efficiency_vs_compression_ratio()

    ax2.plot(r_range, eta_otto * 100, 'b-', linewidth=2, label='Otto')
    ax2.plot(r_range, eta_diesel * 100, 'r-', linewidth=2, label='Diesel (r_c=2)')

    # 标注典型工作范围
    ax2.axvspan(8, 12, alpha=0.2, color='blue', label='Gasoline range')
    ax2.axvspan(14, 22, alpha=0.2, color='red', label='Diesel range')

    ax2.set_xlabel('Compression ratio r')
    ax2.set_ylabel('Efficiency (%)')
    ax2.set_title('热机效率 vs 压缩比')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 卡诺效率 vs 温度
    ax3 = axes[1, 0]
    T_cold = 300  # K
    T_hot_range = np.linspace(350, 1500, 100)

    eta_carnot = [carnot_efficiency(T_h, T_cold) * 100 for T_h in T_hot_range]

    ax3.plot(T_hot_range, eta_carnot, 'g-', linewidth=2)
    ax3.axvline(x=600, color='b', linestyle='--', alpha=0.5,
                label=f'Gasoline (~600K, {carnot_efficiency(600, 300)*100:.0f}%)')
    ax3.axvline(x=800, color='r', linestyle='--', alpha=0.5,
                label=f'Diesel (~800K, {carnot_efficiency(800, 300)*100:.0f}%)')
    ax3.axvline(x=1200, color='orange', linestyle='--', alpha=0.5,
                label=f'Gas turbine (~1200K, {carnot_efficiency(1200, 300)*100:.0f}%)')

    ax3.set_xlabel('T_hot (K)')
    ax3.set_ylabel('Carnot Efficiency (%)')
    ax3.set_title(f'卡诺效率 (T_cold = {T_cold} K)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. T-S 图
    ax4 = axes[1, 1]

    # Otto循环的T-S图（示意）
    T_otto_ts = [T_otto[0], T_otto[1], T_otto[2], T_otto[3], T_otto[0]]
    # 简化的熵变计算
    S_base = 0
    S_otto = [S_base]  # 状态1
    S_otto.append(S_base)  # 绝热压缩，等熵
    S_otto.append(S_base + Cv * np.log(T_otto[2] / T_otto[1]))  # 等容加热
    S_otto.append(S_otto[2])  # 绝热膨胀，等熵
    S_otto.append(S_base)  # 回到状态1

    ax4.plot(S_otto, T_otto_ts, 'b-', linewidth=2, marker='o')
    for i, (s, t) in enumerate(zip(S_otto[:-1], T_otto_ts[:-1])):
        ax4.annotate(f'{i+1}', (s, t), fontsize=12)

    ax4.set_xlabel('Entropy S (J/K)')
    ax4.set_ylabel('Temperature T (K)')
    ax4.set_title('Otto Cycle T-S Diagram')
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('heat_engines.png', dpi=150)
    print("图像已保存为 heat_engines.png")
    plt.show()


# =============================================================================
# 验证函数 Verification
# =============================================================================
def verify():
    """
    验证热机循环练习的正确性 Verify heat engine exercises

    测试内容 Test Contents:
        - 1.1 卡诺效率
        - 1.2 Otto循环效率
        - 1.3 Diesel循环效率
        - 1.4 热量计算
        - 1.5 平均有效压力
        - 1.6 效率与压缩比关系
        - 1.7 布雷顿循环效率
    """
    all_passed = True

    # 测试 1.1 - 卡诺效率 Carnot efficiency
    T_hot, T_cold = 600, 300
    eta_c = carnot_efficiency(T_hot, T_cold)
    if not np.isclose(eta_c, 0.5):
        print("错误 1.1: 卡诺效率计算错误")
        print(f"  当 T_hot = {T_hot}K, T_cold = {T_cold}K 时，效率应为 50%")
        print(f"  计算得到: {eta_c*100:.1f}%")
        all_passed = False
    else:
        print(f"通过 1.1: 卡诺效率正确 (eta = {eta_c*100:.1f}%)")

    # 测试 1.2 - Otto循环效率 Otto efficiency
    r = 10
    eta_otto = otto_efficiency(r)
    expected = 1 - 1 / r**(gamma - 1)
    if not np.isclose(eta_otto, expected, rtol=0.01):
        print("错误 1.2: Otto循环效率计算错误")
        print(f"  期望值: {expected*100:.1f}%, 计算值: {eta_otto*100:.1f}%")
        all_passed = False
    else:
        print(f"通过 1.2: Otto效率正确 (压缩比 r={r}: eta = {eta_otto*100:.1f}%)")

    # 测试 1.3 - Diesel循环效率 Diesel efficiency
    r_diesel = 18
    r_c = 2
    eta_diesel = diesel_efficiency(r_diesel, r_c)
    if eta_diesel <= 0 or eta_diesel >= 1:
        print("错误 1.3: Diesel循环效率应在 0 到 1 之间")
        print(f"  计算得到: {eta_diesel:.4f}")
        all_passed = False
    else:
        print(f"通过 1.3: Diesel效率正确 (r={r_diesel}, r_c={r_c}: eta = {eta_diesel*100:.1f}%)")

    # 测试 1.4 - 热量计算 Heat calculation
    T2, T3 = 700, 2000
    Q_in = heat_input_otto(T2, T3)
    if Q_in <= 0:
        print("错误 1.4: 吸热量应为正值")
        print("  提示: 加热过程中 T3 > T2，Q_in > 0")
        all_passed = False
    else:
        print(f"通过 1.4: 热量计算正确 (Q_in = {Q_in:.0f} J/mol)")

    # 测试 1.5 - 平均有效压力 Mean effective pressure
    W = 500  # J
    V_disp = 0.5e-3  # 500 cc = 0.5 L
    MEP = mean_effective_pressure(W, V_disp)
    if MEP <= 0:
        print("错误 1.5: 平均有效压力应为正值")
        all_passed = False
    else:
        print(f"通过 1.5: 平均有效压力正确 (MEP = {MEP/1e5:.2f} bar)")

    # 测试 1.6 - 压缩比优化 Compression ratio optimization
    r_range, eta_o, eta_d = efficiency_vs_compression_ratio()
    if not np.all(np.diff(eta_o) > 0):  # 效率应随压缩比单调增加
        print("错误 1.6: Otto效率应随压缩比单调增加")
        all_passed = False
    else:
        print("通过 1.6: 压缩比与效率关系正确（效率随压缩比增加）")

    # 测试 1.7 - 布雷顿循环 Brayton cycle
    r_p = 10
    eta_brayton = brayton_efficiency(r_p)
    if eta_brayton <= 0 or eta_brayton >= 1:
        print("错误 1.7: 布雷顿效率应在 0 到 1 之间")
        all_passed = False
    else:
        print(f"通过 1.7: 布雷顿循环正确 (压力比 r_p={r_p}: eta = {eta_brayton*100:.1f}%)")

    if all_passed:
        print("\n所有测试通过！")
        try:
            plot_heat_engines()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("热机循环 Heat Engine Cycles")
    print("=" * 50)
    verify()
