"""
双生子佯谬与固有时 Twin Paradox and Proper Time
难度 Difficulty: ★★★★

学习目标 Learning Objectives:
- 深入理解固有时和坐标时的物理区别
  Deeply understand the physical difference between proper time and coordinate time
- 掌握双生子佯谬的正确解释
  Master the correct explanation of the twin paradox
- 分析加速参考系和非惯性系效应
  Analyze accelerating frames and non-inertial effects
- 理解世界线长度与固有时的关系
  Understand the relationship between worldline length and proper time

物理背景 Physical Background:
双生子佯谬是狭义相对论中最著名的思想实验。一对双胞胎，一个留在地球，
另一个乘高速飞船远行后返回。由于时间膨胀，旅行者回来时比留守者年轻。

"佯谬"的来源：
如果运动是相对的，为什么不能说是地球在运动而飞船静止？
那样地球双胞胎应该更年轻才对，产生矛盾。

正确解释：
1. 对称性被打破：旅行者必须加速转向，经历非惯性运动
2. 从时空几何理解：惯性运动的世界线在类时间隔中是最长的
3. 固有时是沿世界线的积分：τ = ∫dτ = ∫dt√(1 - v²/c²)
4. 旅行者的世界线是折线，固有时较短

关键概念 Key Concepts:
- 固有时 Proper time: 沿世界线运动的时钟测量的时间，是洛伦兹不变量
- 坐标时 Coordinate time: 在特定参考系中定义的时间坐标
- 世界线 Worldline: 粒子在时空中的轨迹
- 固有加速度 Proper acceleration: 加速度计测量的加速度

关键公式 Key Formulas:
- 固有时微分: dτ = dt/γ = dt√(1 - v²/c²)
- 世界线固有时: τ = ∫√(1 - v(t)²/c²)dt
- 双曲运动: x = (c²/a)[cosh(aτ/c) - 1], t = (c/a)sinh(aτ/c)
- 恒加速度下速度: v = c·tanh(aτ/c)

单位说明 Units:
- 时间: s 或年 (1年 ≈ 3.156×10⁷ s)
- 加速度: m/s² (1g ≈ 9.81 m/s²)
- 距离: m 或光年 (1 光年 ≈ 9.46×10¹⁵ m)
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import c

# I AM NOT DONE

# =============================================================================
# 练习 5.1: 固有时基础
# Exercise 5.1: Proper Time Basics
#
# 物理背景：固有时是沿世界线运动的时钟测量的时间。
# 它是洛伦兹不变量，所有观测者都同意同一时钟的固有时读数。
# 坐标时取决于参考系选择，不同观测者可能不同意。
#
# Physical background: Proper time is measured by a clock moving along
# the worldline. It's a Lorentz invariant - all observers agree on it.
# =============================================================================

def lorentz_factor(v):
    """
    计算洛伦兹因子 Calculate Lorentz factor

    公式 Formula: γ = 1/√(1 - v²/c²)

    γ 是时间膨胀因子，也是质量增加因子。
    """
    return 1 / np.sqrt(1 - (v/c)**2)


def proper_time_interval(dt, v):
    """
    计算固有时间隔 Calculate proper time interval

    公式 Formula: dτ = dt/γ = dt√(1 - v²/c²)

    参数 Parameters:
        dt: 坐标时间隔 (s)，在参考系中测量的时间
        v: 运动物体的速度 (m/s)

    返回 Returns:
        dtau: 固有时间隔 (s)，运动时钟测量的时间

    物理解释：运动的时钟走得慢，固有时 < 坐标时
    """
    gamma = lorentz_factor(v)
    return dt / gamma


def coordinate_time_interval(dtau, v):
    """
    从固有时计算坐标时 Calculate coordinate time from proper time

    公式 Formula: dt = γdτ

    参数 Parameters:
        dtau: 固有时间隔 (s)
        v: 运动速度 (m/s)

    返回 Returns:
        dt: 坐标时间隔 (s)

    这是时间膨胀公式的另一种表述
    """
    gamma = lorentz_factor(v)
    return gamma * dtau


def time_dilation_factor(v):
    """
    计算时间膨胀因子 Calculate time dilation factor

    公式 Formula: dt/dτ = γ

    返回时间膨胀的倍数：在参考系中过 γ 秒时，运动时钟只过 1 秒
    """
    return lorentz_factor(v)


# =============================================================================
# 练习 5.2: 经典双生子佯谬
# Exercise 5.2: Classic Twin Paradox
#
# 物理背景：经典双生子佯谬设定
# 一对双胞胎年龄相同，一个留在地球（惯性系），另一个乘火箭远行后返回。
# 假设火箭以恒定速度 v 飞行（忽略加速减速过程），往返总坐标时间为 T_trip。
#
# 关键结果：
# - 地球时间 = T_trip（坐标时）
# - 旅行者时间 = T_trip/γ（固有时）
# - 旅行者比地球人年轻 ΔT = T_trip(1 - 1/γ)
#
# Physical background: Classic twin paradox setup
# One twin stays on Earth (inertial frame), another travels and returns.
# Traveler ages less due to time dilation.
# =============================================================================
def twin_paradox_earth_age(T_trip, v):
    """
    地球双胞胎的年龄增加 Earth twin's age increase

    参数 Parameters:
        T_trip: 往返总旅行时间（地球坐标时）(s 或 年)
        v: 旅行速度 (m/s)

    返回 Returns:
        地球人经历的时间（等于 T_trip）

    说明：地球双胞胎始终处于惯性系，直接测量坐标时
    """
    return T_trip


def twin_paradox_traveler_age(T_trip, v):
    """
    旅行双胞胎的年龄增加（固有时）Traveler's age increase (proper time)

    公式 Formula: τ_traveler = T_trip/γ = T_trip√(1 - v²/c²)

    参数 Parameters:
        T_trip: 往返总时间（地球坐标系）(s 或 年)
        v: 旅行速度 (m/s)

    返回 Returns:
        旅行者经历的固有时

    物理解释：由于时间膨胀，运动时钟走得慢，τ < T_trip
    这解释了为什么旅行者回来时更年轻
    """
    gamma = lorentz_factor(v)
    return T_trip / gamma


def age_difference(T_trip, v):
    """
    年龄差异 Age difference

    公式 Formula: ΔT = T_trip - τ = T_trip(1 - 1/γ)

    参数 Parameters:
        T_trip: 往返总时间（地球系）
        v: 旅行速度

    返回 Returns:
        地球人与旅行者的年龄差（地球人更老）

    数值示例：v = 0.8c 时，γ = 5/3，旅行20年后差8年
    """
    gamma = lorentz_factor(v)
    return T_trip * (1 - 1/gamma)


def twin_travel_distance(T_trip, v):
    """
    旅行距离（单程）One-way travel distance

    公式 Formula: d = v × T_trip/2

    参数 Parameters:
        T_trip: 往返总时间
        v: 旅行速度

    返回 Returns:
        单程距离（地球参考系测量）

    注意：这是地球系中测量的距离。旅行者测量的距离因长度收缩而更短：
    d' = d/γ
    """
    return v * T_trip / 2


# =============================================================================
# 练习 5.3: 带加速度的双生子
# Exercise 5.3: Twin Paradox with Acceleration
#
# 物理背景：真实的双生子佯谬需要考虑加速度
# 旅行者必须经历加速（离开）、减速（到达目的地）、
# 再加速（返回）、最后减速（抵达地球）四个阶段。
#
# 恒定固有加速度（双曲运动 Hyperbolic Motion）：
# 飞船上的加速度计始终显示相同读数 a，这是"固有加速度"。
# 从地球看，飞船加速度随速度增加而减小（趋近光速时趋于零）。
#
# 重要公式：
# - 坐标时 → 固有时: τ = (c/a)arcsinh(at/c)
# - 固有时 → 坐标时: t = (c/a)sinh(aτ/c)
# - 速度: v = at/√(1 + (at/c)²)，永不超过 c
# - 位置: x = (c²/a)(√(1 + (at/c)²) - 1)
#
# Physical background: Real twin paradox with acceleration phases
# Uses hyperbolic motion with constant proper acceleration.
# =============================================================================
def proper_time_uniform_acceleration(t_coord, a_proper):
    """
    恒定固有加速度下的固有时 Proper time under uniform acceleration

    公式 Formula: τ = (c/a)arcsinh(at/c)

    参数 Parameters:
        t_coord: 坐标时 (s)，地球参考系中的时间
        a_proper: 固有加速度 (m/s²)，飞船加速度计读数

    返回 Returns:
        tau: 固有时 (s)，飞船时钟测量的时间

    物理说明：固有时总是小于坐标时（τ < t）
    """
    return (c / a_proper) * np.arcsinh(a_proper * t_coord / c)


def coordinate_time_from_proper_accel(tau, a_proper):
    """
    从固有时计算坐标时 Coordinate time from proper time

    公式 Formula: t = (c/a)sinh(aτ/c)

    这是上一函数的逆运算。
    当 τ → ∞ 时，t 呈指数增长：地球上经过很长时间，飞船上只过了有限时间。
    """
    return (c / a_proper) * np.sinh(a_proper * tau / c)


def velocity_uniform_acceleration(t_coord, a_proper):
    """
    恒定固有加速度下的速度 Velocity under uniform acceleration

    公式 Formula: v = at/√(1 + (at/c)²)

    参数 Parameters:
        t_coord: 坐标时 (s)
        a_proper: 固有加速度 (m/s²)

    返回 Returns:
        v: 速度 (m/s)

    物理特性：
    - t → 0 时，v ≈ at（牛顿极限）
    - t → ∞ 时，v → c（永不超过光速）
    - 相对论效应自动保证因果性
    """
    at = a_proper * t_coord
    return at / np.sqrt(1 + (at/c)**2)


def position_uniform_acceleration(t_coord, a_proper):
    """
    恒定固有加速度下的位置 Position under uniform acceleration

    公式 Formula: x = (c²/a)(√(1 + (at/c)²) - 1)

    参数 Parameters:
        t_coord: 坐标时 (s)
        a_proper: 固有加速度 (m/s²)

    返回 Returns:
        x: 位置 (m)

    几何意义：世界线是双曲线 x² - c²t² = (c²/a)²
    这称为"双曲运动"或"Rindler运动"
    """
    at = a_proper * t_coord
    return (c**2 / a_proper) * (np.sqrt(1 + (at/c)**2) - 1)


def four_phase_trip_proper_time(d, a_proper):
    """
    四阶段加速旅程的固有时 Proper time for four-phase trip

    旅程四阶段 Four phases:
    1. 加速离开地球 Accelerate away
    2. 减速到达目的地 Decelerate to destination
    3. 加速返回 Accelerate back
    4. 减速到达地球 Decelerate to Earth

    参数 Parameters:
        d: 单程距离 (m)
        a_proper: 固有加速度 (m/s²)

    返回 Returns:
        总固有时 (s)

    计算方法：每阶段飞行距离 d/2，
    从 d/2 = (c²/a)(cosh(aτ/c) - 1) 求解 τ
    总固有时 = 4τ

    实际应用：1g 加速飞往比邻星（4.3光年），
    飞船上只需约 3.6 年，地球上过了约 6 年
    """
    # 每阶段距离 = d/2（加速到中点，减速到终点）
    # d/2 = (c²/a)(cosh(aτ/c) - 1)
    # 求解得: τ = (c/a)arccosh(1 + ad/(2c²))
    tau_phase = (c / a_proper) * np.arccosh(1 + a_proper * d / (2 * c**2))
    return 4 * tau_phase


# =============================================================================
# 练习 5.4: 世界线与时空图
# Exercise 5.4: Worldlines and Spacetime Diagrams
#
# 物理背景：时空图是理解相对论的重要工具
# 闵可夫斯基时空图以时间 t（或 ct）为纵轴，空间 x 为横轴。
#
# 世界线 Worldline:
# 粒子在时空中的轨迹称为世界线。
# - 静止粒子：垂直线（只随时间变化）
# - 匀速运动：斜直线（斜率 = c/v）
# - 光子：45°线（斜率 = 1，当 ct 为纵轴时）
#
# 固有时与世界线长度:
# 沿世界线的固有时是洛伦兹不变量：
# τ = ∫dτ = ∫√(dt² - dx²/c²)
# 关键结论：惯性运动（直线世界线）的固有时最长！
# 这就是双生子佯谬中旅行者更年轻的几何原因。
#
# Physical background: Spacetime diagrams and worldlines
# Proper time along worldline is invariant and maximized for inertial motion.
# =============================================================================
def worldline_stationary(t_range):
    """
    静止观察者的世界线 Worldline of stationary observer

    公式 Formula: x = 0 for all t

    静止观察者的世界线是垂直线（沿时间轴）
    这是最简单的世界线，固有时 = 坐标时
    """
    return np.zeros_like(t_range)


def worldline_uniform_velocity(t_range, v, x0=0):
    """
    匀速运动的世界线 Worldline of uniform motion

    公式 Formula: x = x₀ + vt

    参数 Parameters:
        t_range: 时间数组 (s)
        v: 速度 (m/s)
        x0: 初始位置 (m)

    返回 Returns:
        x_range: 位置数组 (m)

    在时空图中，匀速运动是斜直线
    斜率 = v/c（当纵轴为 ct 时）
    """
    return x0 + v * t_range


def worldline_proper_length(t_range, x_range):
    """
    世界线的固有长度（固有时）Proper length of worldline

    公式 Formula: τ = ∫√(c²dt² - dx²)/c = ∫dτ

    参数 Parameters:
        t_range: 时间数组 (s)
        x_range: 位置数组 (m)

    返回 Returns:
        total_tau: 总固有时 (s)

    物理意义：
    - 固有时是沿世界线的"时空距离"
    - 对于类时世界线（|dx/dt| < c），固有时 > 0
    - 惯性运动（直线）的固有时最大（双生子佯谬的几何解释）
    - 弯曲的世界线（加速运动）固有时更短
    """
    if len(t_range) < 2:
        return 0

    total_tau = 0
    for i in range(len(t_range) - 1):
        dt = t_range[i+1] - t_range[i]
        dx = x_range[i+1] - x_range[i]

        # ds² = c²dt² - dx² > 0 表示类时间隔
        ds_squared = c**2 * dt**2 - dx**2
        if ds_squared > 0:
            total_tau += np.sqrt(ds_squared) / c

    return total_tau


def light_cone(t0, x0, t_range):
    """
    光锥 Light cone

    公式 Formula: x = x₀ ± c(t - t₀)

    参数 Parameters:
        t0: 事件时间坐标
        x0: 事件空间坐标
        t_range: 时间数组

    返回 Returns:
        (x_right, x_left): 光锥右侧和左侧的两条线

    物理意义：
    - 光锥是所有经过事件 (t₀, x₀) 的光信号轨迹
    - 光锥内部（类时区域）：可以通过亚光速信号到达
    - 光锥外部（类空区域）：无法通过因果联系
    - 光锥本身（类光）：只有光信号能到达
    - 未来光锥：事件可以影响的区域
    - 过去光锥：可以影响该事件的区域
    """
    x_future_right = x0 + c * (t_range - t0)
    x_future_left = x0 - c * (t_range - t0)
    return x_future_right, x_future_left


# =============================================================================
# 练习 5.5: 多普勒效应与双生子
# Exercise 5.5: Doppler Effect and Twin Paradox
#
# 物理背景：多普勒分析提供了理解双生子佯谬的另一种视角
#
# 相对论多普勒效应：
# - 接近时（蓝移）: f_obs = f_source × √((1+β)/(1-β)) > f_source
# - 远离时（红移）: f_obs = f_source × √((1-β)/(1+β)) < f_source
#
# 双生子佯谬的多普勒解释：
# 假设地球每秒发送一个信号（如年度贺卡）
# - 旅行者去程收到红移信号（频率低，间隔长）
# - 旅行者返程收到蓝移信号（频率高，间隔短）
# - 地球人始终看到旅行者信号红移（去程）然后蓝移（返程）
#
# 关键：旅行者在转向点立即切换看到的频率（从红移到蓝移）
# 地球人看到这个切换有延迟（光传播时间）
# 这种不对称导致最终的年龄差异
#
# Physical background: Doppler analysis of twin paradox
# =============================================================================
def relativistic_doppler_approaching(f_source, v):
    """
    相对论多普勒效应（接近）Relativistic Doppler - approaching

    公式 Formula: f_obs = f_source × √((1+β)/(1-β))

    参数 Parameters:
        f_source: 信号源频率 (Hz)
        v: 相对速度（接近为正）(m/s)

    返回 Returns:
        f_obs: 观测频率 (Hz)

    物理效应：蓝移，观测频率高于源频率
    例：v = 0.6c 时，f_obs = 2 × f_source
    """
    beta = v / c
    return f_source * np.sqrt((1 + beta) / (1 - beta))


def relativistic_doppler_receding(f_source, v):
    """
    相对论多普勒效应（远离）Relativistic Doppler - receding

    公式 Formula: f_obs = f_source × √((1-β)/(1+β))

    参数 Parameters:
        f_source: 信号源频率 (Hz)
        v: 相对速度（远离为正）(m/s)

    返回 Returns:
        f_obs: 观测频率 (Hz)

    物理效应：红移，观测频率低于源频率
    例：v = 0.6c 时，f_obs = 0.5 × f_source
    对称性：f_approaching × f_receding = f_source²
    """
    beta = v / c
    return f_source * np.sqrt((1 - beta) / (1 + beta))


def signals_sent_by_earth(T_trip, f_signal):
    """
    地球发送的信号总数 Total signals sent by Earth

    公式 Formula: N = f_signal × T_trip

    参数 Parameters:
        T_trip: 地球时间（旅行总时间）
        f_signal: 信号发送频率（如每年1次）

    返回 Returns:
        N: 信号总数

    这代表地球人度过的时间单位数
    """
    return f_signal * T_trip


def signals_received_by_traveler(T_trip, v, f_signal):
    """
    旅行者接收的信号总数 Total signals received by traveler

    参数 Parameters:
        T_trip: 地球坐标时间
        v: 旅行速度
        f_signal: 信号发送频率

    返回 Returns:
        N: 接收到的信号总数

    重要结论：
    - 去程：收到红移信号（看起来地球时间变慢）
    - 返程：收到蓝移信号（看起来地球时间变快）
    - 无论如何，最终收到的信号总数 = 地球发送的信号总数
    - 这证明旅行者确实错过了一些地球时间（自己更年轻）

    这提供了不需要复杂数学就能理解双生子佯谬的直观方法
    """
    gamma = lorentz_factor(v)
    tau_trip = T_trip / gamma
    d = v * T_trip / 2

    # 去程和返程固有时各占一半
    tau_out = tau_trip / 2
    tau_back = tau_trip / 2

    # 信号总数守恒：发出多少就收到多少
    # 只是接收的时间分布不同（去程慢，返程快）
    return f_signal * T_trip


# =============================================================================
# 练习 5.6: 惯性系与非惯性系
# Exercise 5.6: Inertial and Non-Inertial Frames
#
# 物理背景：双生子佯谬的关键在于区分惯性系和非惯性系
#
# 惯性系 Inertial Frame:
# - 牛顿第一定律成立的参考系
# - 没有加速度的自由运动观测者
# - 狭义相对论只处理惯性系之间的变换
#
# 非惯性系 Non-Inertial Frame:
# - 加速运动的参考系
# - 存在惯性力（假力）
# - 需要广义相对论来完整描述
#
# 等效原理 Equivalence Principle:
# 加速度和引力在局部不可区分（爱因斯坦发展广义相对论的起点）
# 加速参考系中会出现等效的"引力"时间膨胀
#
# Rindler视界：
# 恒加速观察者在后方距离 d = c²/a 处存在视界
# 该视界后方的信号永远无法追上观察者
# 这是黑洞事件视界的平坦时空类比
#
# Physical background: Breaking symmetry through acceleration
# The traveling twin experiences acceleration, which is absolute.
# =============================================================================
def is_inertial_frame(acceleration):
    """
    判断是否为惯性系 Check if frame is inertial

    公式 Formula: |a| = 0 → 惯性系

    参数 Parameters:
        acceleration: 加速度 (m/s²)

    返回 Returns:
        True 如果是惯性系，False 如果不是

    物理意义：加速度是绝对的，可以通过加速度计测量
    这打破了双生子之间的"对称性"
    """
    return np.abs(acceleration) < 1e-10


def equivalent_gravitational_field(a_proper):
    """
    等效引力场（等效原理）Equivalent gravitational field

    公式 Formula: g_equiv = a_proper

    参数 Parameters:
        a_proper: 固有加速度 (m/s²)

    返回 Returns:
        等效引力场强度 (m/s²)

    等效原理（爱因斯坦）：
    在封闭的电梯中，无法区分：
    1. 电梯在引力场中静止
    2. 电梯在无引力空间中加速上升
    这是广义相对论的基础思想
    """
    return a_proper


def gravitational_time_dilation(delta_h, g):
    """
    引力时间膨胀（弱场近似）Gravitational time dilation

    公式 Formula: dτ/dt ≈ 1 + gh/c²

    参数 Parameters:
        delta_h: 高度差 (m)
        g: 引力场强度 / 等效加速度 (m/s²)

    返回 Returns:
        时间膨胀因子

    物理效应：
    - 高处的时钟走得快（离引力源远）
    - 低处的时钟走得慢（离引力源近）
    - 这解释了加速阶段对双生子年龄的额外贡献
    - GPS卫星需要修正此效应（每天约45微秒）
    """
    return 1 + g * delta_h / c**2


def rindler_horizon_distance(a_proper):
    """
    Rindler视界距离 Rindler horizon distance

    公式 Formula: d_horizon = c²/a

    参数 Parameters:
        a_proper: 固有加速度 (m/s²)

    返回 Returns:
        视界距离 (m)

    物理意义：
    - 恒加速观察者后方存在视界
    - 该视界后方的光信号永远追不上观察者
    - 这是黑洞事件视界的平坦时空类比
    - 例：1g 加速时，视界在后方约 1 光年处

    Rindler时空是描述加速观察者的坐标系
    """
    return c**2 / a_proper


def break_symmetry_explanation():
    """
    打破对称性的解释 Explanation of symmetry breaking

    双生子佯谬的关键：为什么情况不对称？

    返回 Returns:
        详细解释字符串
    """
    explanation = """
    双生子佯谬的对称性被打破是因为：

    1. 加速度是绝对的
       - 旅行者必须转向（加速度）
       - 加速度计能测量到这个加速度
       - 地球观测者加速度为零

    2. 世界线几何不同
       - 地球：直线世界线（惯性运动）
       - 旅行者：折线世界线（非惯性运动）
       - 直线是最长的类时世界线（固有时最大）

    3. 参考系切换
       - 旅行者在转向点切换惯性系
       - 这导致对"同时"的重新定义
       - 地球双胞胎始终处于同一惯性系

    4. 可操作的判据
       - 谁感受到加速度，谁就更年轻
       - 这与直觉"运动使你年轻"一致

    5. 从广义相对论角度
       - 加速度等效于引力场
       - 旅行者在"等效引力场"中
       - 引力时间膨胀导致额外的年龄差异
    """
    return explanation


# =============================================================================
# 可视化
# =============================================================================
def plot_twin_paradox():
    """绘制双生子佯谬相关图"""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 时间膨胀因子
    ax1 = axes[0, 0]
    v = np.linspace(0, 0.99, 100) * c

    gamma = [lorentz_factor(vi) for vi in v]
    tau_ratio = [1/g for g in gamma]  # τ/t = 1/γ

    ax1.plot(v/c, gamma, 'b-', label='γ', linewidth=2)
    ax1.plot(v/c, tau_ratio, 'r-', label='τ/t = 1/γ', linewidth=2)
    ax1.set_xlabel('v/c')
    ax1.set_ylabel('因子')
    ax1.set_title('时间膨胀')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 10)

    # 2. 时空图
    ax2 = axes[0, 1]
    T_trip = 10  # 年
    v_travel = 0.8 * c  # ly/年

    # 地球双胞胎世界线
    t_earth = np.linspace(0, T_trip, 100)
    x_earth = worldline_stationary(t_earth)

    # 旅行者世界线
    t_out = np.linspace(0, T_trip/2, 50)
    x_out = v_travel * t_out

    t_back = np.linspace(T_trip/2, T_trip, 50)
    x_back = v_travel * T_trip/2 - v_travel * (t_back - T_trip/2)

    ax2.plot(x_earth, t_earth, 'b-', label='地球双胞胎', linewidth=2)
    ax2.plot(x_out, t_out, 'r-', label='旅行者', linewidth=2)
    ax2.plot(x_back, t_back, 'r-', linewidth=2)

    # 光锥
    t_lc = np.linspace(0, T_trip, 100)
    x_lc_r, x_lc_l = light_cone(0, 0, t_lc)
    ax2.plot(x_lc_r, t_lc, 'y--', alpha=0.5, linewidth=1)
    ax2.plot(x_lc_l, t_lc, 'y--', alpha=0.5, linewidth=1)

    ax2.set_xlabel('x (光年)')
    ax2.set_ylabel('t (年)')
    ax2.set_title('时空图 (c = 1 光年/年)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_aspect('equal')

    # 3. 年龄差异 vs 速度
    ax3 = axes[0, 2]
    T_trip = 20  # 年
    v_range = np.linspace(0.1, 0.99, 50) * c

    age_earth = [twin_paradox_earth_age(T_trip, vi) for vi in v_range]
    age_traveler = [twin_paradox_traveler_age(T_trip, vi) for vi in v_range]
    age_diff = [age_difference(T_trip, vi) for vi in v_range]

    ax3.plot(v_range/c, age_earth, 'b-', label='地球年龄增加', linewidth=2)
    ax3.plot(v_range/c, age_traveler, 'r-', label='旅行者年龄增加', linewidth=2)
    ax3.plot(v_range/c, age_diff, 'g--', label='年龄差', linewidth=2)
    ax3.set_xlabel('v/c')
    ax3.set_ylabel('年龄 (年)')
    ax3.set_title(f'双生子佯谬 (T_trip = {T_trip}年)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 恒定加速度运动
    ax4 = axes[1, 0]
    a = 9.81  # 1g
    t_coord = np.linspace(0, 5, 100) * (c/a)  # 以 c/a 为单位

    tau = [proper_time_uniform_acceleration(ti, a) for ti in t_coord]
    v = [velocity_uniform_acceleration(ti, a) for ti in t_coord]

    ax4.plot(t_coord * a / c, np.array(tau) * a / c, 'b-', label='τ/(c/a)', linewidth=2)
    ax4.plot(t_coord * a / c, np.array(v)/c, 'r-', label='v/c', linewidth=2)
    ax4.set_xlabel('t/(c/a)')
    ax4.set_ylabel('值')
    ax4.set_title('恒定固有加速度 (1g)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 多普勒信号
    ax5 = axes[1, 1]
    beta_range = np.linspace(0.1, 0.9, 50)

    doppler_red = [relativistic_doppler_receding(1, b*c) for b in beta_range]
    doppler_blue = [relativistic_doppler_approaching(1, b*c) for b in beta_range]

    ax5.semilogy(beta_range, doppler_blue, 'b-', label='接近（蓝移）', linewidth=2)
    ax5.semilogy(beta_range, doppler_red, 'r-', label='远离（红移）', linewidth=2)
    ax5.axhline(y=1, color='k', linestyle='--', alpha=0.5)
    ax5.set_xlabel('β = v/c')
    ax5.set_ylabel('f_obs/f_source')
    ax5.set_title('相对论多普勒效应')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. 星际旅行所需时间
    ax6 = axes[1, 2]
    d_range = np.array([4.3, 10, 100, 1000, 10000])  # 光年
    labels = ['比邻星', '10 ly', '100 ly', '1000 ly', '10000 ly']

    for i, (d, label) in enumerate(zip(d_range, labels)):
        v_fracs = np.linspace(0.5, 0.999, 50)
        tau_trips = []
        for v_frac in v_fracs:
            v = v_frac * c
            T_coord = 2 * d * 9.461e15 / v  # 坐标时（秒）
            T_coord_years = T_coord / (365.25 * 24 * 3600)
            tau = twin_paradox_traveler_age(T_coord_years, v)
            tau_trips.append(tau)

        if i < 3:
            ax6.semilogy(v_fracs, tau_trips, label=label, linewidth=1.5)

    ax6.set_xlabel('v/c')
    ax6.set_ylabel('旅行者年龄增加 (年)')
    ax6.set_title('星际旅行固有时')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('twin_paradox.png', dpi=150)
    print("图像已保存为 twin_paradox.png")
    plt.show()


# =============================================================================
# 验证函数
# =============================================================================
def verify():
    """Verify all exercises"""
    all_passed = True

    # Check 5.1 - Proper time
    v = 0.6 * c
    gamma = lorentz_factor(v)
    dt = 10  # years

    dtau = proper_time_interval(dt, v)
    expected_dtau = dt / gamma

    if not np.isclose(dtau, expected_dtau, rtol=0.01):
        print("X 5.1 固有时计算错误")
        all_passed = False
    else:
        print(f"V 5.1 固有时正确 (γ(0.6c) = {gamma:.3f}, dτ = {dtau:.2f}年)")

    # Check 5.2 - Classic twin paradox
    T_trip = 20  # years
    v = 0.8 * c

    age_e = twin_paradox_earth_age(T_trip, v)
    age_t = twin_paradox_traveler_age(T_trip, v)

    if age_t >= age_e:
        print("X 5.2 旅行者应该更年轻")
        all_passed = False
    else:
        print(f"V 5.2 双生子佯谬正确 (地球: {age_e:.1f}年, 旅行者: {age_t:.1f}年)")

    # Check 5.3 - Accelerated motion
    a = 9.81  # 1g
    t_test = c / a  # 约1年

    tau = proper_time_uniform_acceleration(t_test, a)
    v_test = velocity_uniform_acceleration(t_test, a)

    if v_test >= c:
        print("X 5.3 速度不能超过光速")
        all_passed = False
    else:
        print(f"V 5.3 加速运动正确 (1g加速1年: v = {v_test/c:.3f}c)")

    # Check 5.4 - Worldline
    t_range = np.linspace(0, 10, 100)
    v_wl = 0.5 * c
    x_range = worldline_uniform_velocity(t_range, v_wl)

    tau_wl = worldline_proper_length(t_range, x_range)
    expected_tau = 10 / lorentz_factor(v_wl)

    if not np.isclose(tau_wl, expected_tau, rtol=0.1):
        print("X 5.4 世界线长度错误")
        all_passed = False
    else:
        print(f"V 5.4 世界线计算正确")

    # Check 5.5 - Doppler effect
    f_source = 1
    v_doppler = 0.5 * c

    f_blue = relativistic_doppler_approaching(f_source, v_doppler)
    f_red = relativistic_doppler_receding(f_source, v_doppler)

    # 检验对称性: f_blue × f_red = f_source²
    if not np.isclose(f_blue * f_red, f_source**2, rtol=0.01):
        print("X 5.5 多普勒效应对称性错误")
        all_passed = False
    else:
        print(f"V 5.5 多普勒效应正确 (蓝移: {f_blue:.2f}, 红移: {f_red:.2f})")

    # Check 5.6 - Non-inertial frames
    a_test = 9.81
    d_horizon = rindler_horizon_distance(a_test)

    if d_horizon <= 0:
        print("X 5.6 Rindler视界距离应为正")
        all_passed = False
    else:
        print(f"V 5.6 非惯性系正确 (1g Rindler视界: {d_horizon/c**2*a_test:.2f} c²/a)")

    if all_passed:
        print("\n所有测试通过！正在生成可视化...")
        try:
            plot_twin_paradox()
        except Exception as ex:
            print(f"可视化生成失败: {ex}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("双生子佯谬与固有时 Twin Paradox and Proper Time")
    print("=" * 50)
    verify()
