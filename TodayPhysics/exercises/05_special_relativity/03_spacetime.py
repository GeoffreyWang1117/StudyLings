"""
时空与闵可夫斯基几何 Spacetime and Minkowski Geometry
难度 Difficulty: ★★★★

学习目标 Learning Objectives:
- 理解闵可夫斯基时空的几何结构
  Understand the geometric structure of Minkowski spacetime
- 掌握时空间隔和因果结构的判断
  Master spacetime intervals and causal structure
- 分析世界线和固有时的计算
  Analyze worldlines and proper time calculations
- 理解光锥和因果关联
  Understand light cones and causal connections

物理背景 Physical Background:
闵可夫斯基时空是狭义相对论的几何框架，由三维空间和一维时间组成四维时空。
时空间隔 ds² 是洛伦兹不变量，在所有惯性参考系中保持相同。

时空可以根据间隔分为三个区域：
- 类时 (timelike): ds² > 0，两事件可由亚光速信号连接
- 类空 (spacelike): ds² < 0，两事件无法有因果关联
- 类光 (lightlike/null): ds² = 0，光信号连接的事件

光锥 (light cone) 是以某事件为顶点的所有类光方向的集合。
未来光锥内的事件可被该事件影响，过去光锥内的事件可影响该事件。

关键公式 Key Formulas:
- 时空间隔: ds² = c²dt² - dx² - dy² - dz² (度规符号约定 +,-,-,-)
- 固有时: dτ = ds/c = dt√(1 - v²/c²) = dt/γ
- 世界线长度: τ = ∫dτ（沿世界线积分得到固有时）

单位说明 Units:
- 时空坐标: (ct, x, y, z)，使用自然单位时 c=1
- 固有时: s (秒)
- 时空间隔: m² 或 s²（取决于约定）
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import c

# I AM NOT DONE

# =============================================================================
# 练习 3.1: 时空间隔
# Exercise 3.1: Spacetime Interval
#
# 物理背景：时空间隔是闵可夫斯基时空中的"距离"概念。
# 与欧几里得空间不同，时空间隔可以为正、负或零。
# 时空间隔是洛伦兹不变量，所有惯性观测者测得相同值。
#
# Physical background: Spacetime interval is the "distance" in Minkowski space.
# Unlike Euclidean space, it can be positive, negative, or zero.
# It is a Lorentz invariant - all inertial observers measure the same value.
# =============================================================================

def spacetime_interval(event1, event2):
    """
    计算两事件之间的时空间隔 Calculate spacetime interval between two events

    公式 Formula: ds² = c²(Δt)² - (Δx)² - (Δy)² - (Δz)²

    参数 Parameters:
        event1: 第一个事件 (t, x, y, z)，时间单位 s，空间单位 m
        event2: 第二个事件 (t, x, y, z)

    返回 Returns:
        ds_squared: 时空间隔的平方 (m²)

    物理意义：
    - ds² > 0: 类时间隔，两事件可由亚光速信号连接
    - ds² = 0: 类光间隔，光信号恰好连接两事件
    - ds² < 0: 类空间隔，两事件无法有因果关联
    """
    dt = event2[0] - event1[0]  # 时间差 (s)
    dx = event2[1] - event1[1]  # x 方向空间差 (m)
    dy = event2[2] - event1[2]  # y 方向空间差 (m)
    dz = event2[3] - event1[3]  # z 方向空间差 (m)

    # TODO: 计算时空间隔
    # 使用度规符号约定 (+,-,-,-)
    ds_squared = (c * dt)**2 - dx**2 - dy**2 - dz**2
    return ds_squared


def classify_interval(ds_squared):
    """
    分类时空间隔 Classify spacetime interval

    分类标准 Classification:
    - ds² > 0: 类时 (timelike) - 时间分离占主导
    - ds² = 0: 类光 (lightlike/null) - 光信号连接
    - ds² < 0: 类空 (spacelike) - 空间分离占主导

    参数 Parameters:
        ds_squared: 时空间隔的平方 (m²)

    返回 Returns:
        str: 'timelike', 'lightlike', 或 'spacelike'

    因果结构意义:
    - 类时：可以存在因果关系，存在参考系使两事件发生在同一地点
    - 类光：光信号恰好能从一个事件传到另一个
    - 类空：不可能有因果关系，存在参考系使两事件同时发生
    """
    if ds_squared > 0:
        return 'timelike'
    elif np.isclose(ds_squared, 0, atol=1e-20):
        return 'lightlike'
    else:
        return 'spacelike'


# =============================================================================
# 练习 3.2: 固有时
# Exercise 3.2: Proper Time
#
# 物理背景：固有时是沿世界线运动的时钟测量的时间。
# 它是该时钟经历的"真实"时间，与参考系无关。
# 对于类时间隔，固有时是两事件间的最大时间间隔。
#
# Physical background: Proper time is the time measured by a clock
# moving along the worldline. It is frame-independent.
# =============================================================================

def proper_time(ds_squared):
    """
    从时空间隔计算固有时 Calculate proper time from spacetime interval

    公式 Formula: τ = √(ds²)/c

    参数 Parameters:
        ds_squared: 时空间隔的平方 (m²)，必须 > 0 (类时)

    返回 Returns:
        tau: 固有时 (s)

    注意：只有类时间隔才有固有时的物理意义。
    类空间隔对应固有长度，而非固有时。
    """
    if ds_squared < 0:
        raise ValueError("类空间隔没有固有时 Spacelike interval has no proper time")
    return np.sqrt(ds_squared) / c


def proper_time_moving_clock(v, t_lab):
    """
    计算运动时钟的固有时 Calculate proper time for a moving clock

    公式 Formula: τ = t_lab/γ = t_lab √(1 - v²/c²)

    参数 Parameters:
        v: 时钟相对于实验室的速度 (m/s)
        t_lab: 实验室参考系中的时间 (s)

    返回 Returns:
        tau: 运动时钟显示的时间（固有时）(s)

    物理解释：
    - 运动时钟走得慢，τ < t_lab
    - 当 v = 0.6c 时，γ = 1.25，所以 τ = 0.8 t_lab
    - 这是时间膨胀效应的另一种表述
    """
    gamma = 1 / np.sqrt(1 - (v/c)**2)
    return t_lab / gamma


# =============================================================================
# 练习 3.3: 世界线
# Exercise 3.3: World Lines
#
# 物理背景：世界线是粒子在时空中的轨迹。
# 在时空图中，纵轴通常是时间（或 ct），横轴是空间。
# 静止粒子的世界线是垂直线，运动粒子的世界线是倾斜线。
# 光的世界线在 (ct, x) 图中斜率为 ±1。
#
# Physical background: A worldline is the trajectory of a particle in spacetime.
# A particle at rest has a vertical worldline; moving particles have tilted lines.
# =============================================================================

def world_line_inertial(v, t_range, x0=0):
    """
    匀速运动粒子的世界线 Worldline of a particle in uniform motion

    公式 Formula: x(t) = x₀ + vt

    参数 Parameters:
        v: 速度 (m/s)
        t_range: 时间范围数组 (s)
        x0: 初始位置 (m)

    返回 Returns:
        (t, x): 时间和位置数组

    在时空图中，惯性运动的世界线是直线。
    斜率 dx/dt = v，在 (ct,x) 图中斜率为 v/c = β。
    """
    t = np.array(t_range)
    x = x0 + v * t
    return t, x


def world_line_accelerated(a, t_range, x0=0, v0=0):
    """
    恒加速度运动的世界线（非相对论近似）
    Worldline with constant acceleration (non-relativistic)

    公式 Formula: x(t) = x₀ + v₀t + ½at²

    参数 Parameters:
        a: 加速度 (m/s²)
        t_range: 时间范围数组 (s)
        x0: 初始位置 (m)
        v0: 初始速度 (m/s)

    返回 Returns:
        (t, x): 时间和位置数组

    注意：这是非相对论公式，当速度接近 c 时需要用双曲运动。
    """
    t = np.array(t_range)
    x = x0 + v0 * t + 0.5 * a * t**2
    return t, x


def hyperbolic_motion(a, tau_range):
    """
    相对论恒固有加速度运动（双曲运动）
    Relativistic motion with constant proper acceleration (hyperbolic motion)

    公式 Formulas:
        x(τ) = (c²/a)[cosh(aτ/c) - 1]
        t(τ) = (c/a)sinh(aτ/c)

    参数 Parameters:
        a: 固有加速度 proper acceleration (m/s²)
        tau_range: 固有时范围数组 (s)

    返回 Returns:
        (t, x): 坐标时和位置数组

    物理意义：
    - 固有加速度 a 是加速度计测量的加速度（不随时间变化）
    - 在时空图中轨迹是双曲线，因此称为双曲运动
    - 速度趋近光速但永远达不到：v = c tanh(aτ/c)
    - 例：a = g ≈ 10 m/s² 时，c/a ≈ 1 年
    """
    tau = np.array(tau_range)
    x = (c**2 / a) * (np.cosh(a * tau / c) - 1)
    t = (c / a) * np.sinh(a * tau / c)
    return t, x


# =============================================================================
# 练习 3.4: 光锥
# Exercise 3.4: Light Cone
#
# 物理背景：光锥是以某事件为顶点的所有光线世界线的集合。
# 光锥将时空分为三个区域：
# - 未来光锥内部：该事件可以影响的所有事件（绝对未来）
# - 过去光锥内部：可以影响该事件的所有事件（绝对过去）
# - 光锥外部：与该事件没有因果关联（绝对别处）
#
# Physical background: The light cone separates spacetime into:
# - Absolute future: events that can be influenced
# - Absolute past: events that can influence
# - Elsewhere: causally disconnected events
# =============================================================================

def light_cone_future(t_range):
    """
    计算未来光锥边界 Calculate future light cone boundary

    公式 Formula: x = ±ct, t > 0

    参数 Parameters:
        t_range: 时间范围数组 (s)

    返回 Returns:
        (t, x_plus, x_minus): 时间和两条光锥边界的位置

    在 (ct, x) 图中，未来光锥是从原点向上的两条 45° 线。
    """
    t = np.array(t_range)
    t = t[t >= 0]  # 只取未来（t > 0）
    x_plus = c * t   # 向右传播的光
    x_minus = -c * t  # 向左传播的光
    return t, x_plus, x_minus


def light_cone_past(t_range):
    """
    计算过去光锥边界 Calculate past light cone boundary

    公式 Formula: x = ±ct, t < 0

    参数 Parameters:
        t_range: 时间范围数组 (s)

    返回 Returns:
        (t, x_plus, x_minus): 时间和两条光锥边界的位置

    在 (ct, x) 图中，过去光锥是从原点向下的两条 45° 线。
    """
    t = np.array(t_range)
    t = t[t <= 0]  # 只取过去（t < 0）
    x_plus = c * t
    x_minus = -c * t
    return t, x_plus, x_minus


def is_causally_connected(event1, event2):
    """
    判断两事件是否因果关联 Determine if two events are causally connected

    判断标准 Criterion:
    - 类时间隔 (ds² > 0): 有因果关联，一个事件可影响另一个
    - 类光间隔 (ds² = 0): 有因果关联，光信号恰好连接
    - 类空间隔 (ds² < 0): 无因果关联，不可能相互影响

    参数 Parameters:
        event1: 第一个事件 (t, x, y, z)
        event2: 第二个事件 (t, x, y, z)

    返回 Returns:
        bool: True 表示有因果关联，False 表示无因果关联

    物理意义：如果两事件因果关联，则存在某个参考系使得
    它们发生在同一地点（对于类时间隔）。
    """
    ds_sq = spacetime_interval(event1, event2)
    return ds_sq >= 0  # 类时或类光都有因果关联


# =============================================================================
# 练习 3.5: 长度收缩与同时性
# Exercise 3.5: Length Contraction and Simultaneity
#
# 物理背景：长度收缩和同时性的相对性是相互关联的效应。
# 测量长度需要同时测量两端的位置，但"同时"在不同参考系中不同。
# 这解释了为什么运动物体在运动方向上变短。
#
# Physical background: Length contraction and relativity of simultaneity
# are related effects. Measuring length requires "simultaneous" measurements
# at both ends, but "simultaneous" differs between reference frames.
# =============================================================================

def length_contraction(L0, v):
    """
    计算长度收缩 Calculate length contraction

    公式 Formula: L = L₀/γ = L₀√(1 - v²/c²)

    参数 Parameters:
        L0: 固有长度 proper length (m)，物体静止时测量的长度
        v: 物体相对于观测者的速度 (m/s)

    返回 Returns:
        L: 收缩后的长度 (m)，观测者测量的长度

    物理解释：
    - 收缩只发生在运动方向，垂直方向长度不变
    - 当 v = 0.6c 时，L = 0.8 L₀
    - 当 v = 0.9c 时，L ≈ 0.44 L₀
    """
    gamma = 1 / np.sqrt(1 - (v/c)**2)
    return L0 / gamma


def simultaneity_shift(L0, v):
    """
    计算同时性偏移 Calculate simultaneity shift

    公式 Formula: Δt' = γvL₀/c²

    参数 Parameters:
        L0: 物体的固有长度 (m)
        v: 物体相对于观测者的速度 (m/s)

    返回 Returns:
        delta_t_prime: 时间差 (s)

    物理意义：
    在物体静止参考系中同时发生的两端事件，
    在相对运动的参考系中不同时。
    后端事件发生在前端事件之前（沿运动方向）。
    这就是"前端同时落后"效应。
    """
    gamma = 1 / np.sqrt(1 - (v/c)**2)
    return gamma * v * L0 / c**2


# =============================================================================
# 练习 3.6: 双生子佯谬
# Exercise 3.6: Twin Paradox
#
# 物理背景：双生子佯谬是狭义相对论最著名的"悖论"。
# 一对双胞胎，一个留在地球，一个乘飞船远行后返回。
# 由于时间膨胀，旅行者回来时比留在地球的双胞胎年轻。
#
# "佯谬"解释：为什么不能说地球在运动而旅行者静止？
# 答案：对称性被打破了！旅行者必须加速转向，经历了非惯性系。
# 可以用固有时（世界线长度）来理解：惯性运动的世界线最长。
#
# Physical background: The twin paradox is a famous thought experiment.
# The traveling twin ages less due to time dilation.
# The asymmetry comes from the traveler's acceleration during turnaround.
# =============================================================================

def twin_paradox_ages(v, T_earth):
    """
    计算双生子佯谬中的年龄差异 Calculate age difference in twin paradox

    简化模型：假设瞬间转向（忽略加速度时间）

    参数 Parameters:
        v: 旅行速度 (m/s)，去程和返程相同
        T_earth: 地球时间（往返总时间）(s 或年)

    返回 Returns:
        (T_earth, T_traveler): 地球双胞胎和旅行双胞胎的年龄增加

    计算方法：
    - 地球时间: T_earth（输入）
    - 旅行者固有时: T_traveler = T_earth/γ

    例如：若 v = 0.8c，T_earth = 10年
    则 γ = 5/3，T_traveler = 6年
    旅行者比地球双胞胎年轻 4 年！
    """
    gamma = 1 / np.sqrt(1 - (v/c)**2)
    T_traveler = T_earth / gamma
    return T_earth, T_traveler


# =============================================================================
# 可视化
# =============================================================================
def plot_spacetime():
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # 1. 闵可夫斯基图
    ax1 = axes[0, 0]

    # 光锥
    t = np.linspace(-2, 2, 100)
    ax1.fill_between(t, -c*np.abs(t), c*np.abs(t), alpha=0.2, color='yellow', label='类时区域')
    ax1.plot(t, c*t, 'y-', linewidth=2, label='光锥')
    ax1.plot(t, -c*t, 'y-', linewidth=2)

    # 世界线
    t_wl, x_wl = world_line_inertial(0.5*c, t)
    ax1.plot(t_wl, x_wl/c, 'b-', linewidth=2, label='v=0.5c')
    t_wl2, x_wl2 = world_line_inertial(0.8*c, t)
    ax1.plot(t_wl2, x_wl2/c, 'r-', linewidth=2, label='v=0.8c')

    ax1.set_xlabel('ct')
    ax1.set_ylabel('x')
    ax1.set_title('闵可夫斯基时空图')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_aspect('equal')
    ax1.set_xlim(-2, 2)
    ax1.set_ylim(-2, 2)

    # 2. 双曲运动
    ax2 = axes[0, 1]
    a = 10  # m/s²
    tau = np.linspace(-5, 5, 500)
    t_hyp, x_hyp = hyperbolic_motion(a, tau)

    ax2.plot(t_hyp, x_hyp, 'b-', linewidth=2)
    ax2.plot(t_hyp, c*t_hyp, 'y--', linewidth=1, alpha=0.5, label='光锥')
    ax2.set_xlabel('t (s)')
    ax2.set_ylabel('x (m)')
    ax2.set_title(f'双曲运动 (a = {a} m/s²)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 长度收缩
    ax3 = axes[1, 0]
    v_range = np.linspace(0, 0.99, 100) * c
    L0 = 1  # 固有长度
    L = [length_contraction(L0, v) for v in v_range]

    ax3.plot(v_range/c, L, 'b-', linewidth=2)
    ax3.set_xlabel('v/c')
    ax3.set_ylabel('L/L₀')
    ax3.set_title('长度收缩')
    ax3.grid(True, alpha=0.3)

    # 4. 双生子佯谬
    ax4 = axes[1, 1]
    T_earth = 20  # 地球年
    v_range = np.linspace(0.1, 0.99, 100) * c

    ages = [twin_paradox_ages(v, T_earth) for v in v_range]
    T_traveler = [age[1] for age in ages]

    ax4.plot(v_range/c, [T_earth]*len(v_range), 'b--', label='地球双胞胎', linewidth=2)
    ax4.plot(v_range/c, T_traveler, 'r-', label='旅行双胞胎', linewidth=2)
    ax4.set_xlabel('v/c')
    ax4.set_ylabel('年龄 (年)')
    ax4.set_title('双生子佯谬')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('spacetime.png', dpi=150)
    print("图像已保存为 spacetime.png")
    plt.show()


def verify():
    """
    验证所有练习的正确性 Verify all exercises

    检查内容 Checks:
    3.1 时空间隔分类（类时/类空/类光）
    3.2 固有时计算
    3.3 世界线计算
    3.4 因果关联判断
    3.5 长度收缩
    3.6 双生子佯谬（旅行者更年轻）
    """
    all_passed = True

    # 检查 3.1 - 时空间隔
    event1 = (0, 0, 0, 0)
    event2 = (1, c*0.5, 0, 0)  # c²(1)² - (0.5c)² > 0，类时间隔
    ds_sq = spacetime_interval(event1, event2)
    if classify_interval(ds_sq) != 'timelike':
        print("错误 3.1 时空间隔分类错误，应为类时(timelike)")
        all_passed = False
    else:
        print("通过 3.1 时空间隔分类正确（类时间隔）")

    # 检查 3.2 - 固有时
    tau = proper_time_moving_clock(0.6*c, 1)
    expected_tau = 0.8  # γ = 1.25, τ = 1/1.25 = 0.8
    if not np.isclose(tau, expected_tau, rtol=0.01):
        print("错误 3.2 固有时计算错误")
        all_passed = False
    else:
        print(f"通过 3.2 固有时正确 (v=0.6c 时 τ = {tau:.2f}s，坐标时 1s)")

    # 检查 3.3 - 世界线
    t_range = np.linspace(0, 1, 100)
    t, x = world_line_inertial(0.5*c, t_range)
    if not np.isclose(x[-1], 0.5*c, rtol=0.01):
        print("错误 3.3 世界线计算错误")
        all_passed = False
    else:
        print("通过 3.3 匀速世界线正确 (x = vt)")

    # 检查 3.4 - 因果关联
    e1 = (0, 0, 0, 0)
    e2_causal = (1, 0.5*c, 0, 0)     # 类时，有因果关联
    e2_not_causal = (1, 2*c, 0, 0)   # 类空，无因果关联
    if not is_causally_connected(e1, e2_causal):
        print("错误 3.4 类时间隔应有因果关联")
        all_passed = False
    elif is_causally_connected(e1, e2_not_causal):
        print("错误 3.4 类空间隔不应有因果关联")
        all_passed = False
    else:
        print("通过 3.4 因果结构判断正确")

    # 检查 3.5 - 长度收缩
    L = length_contraction(1, 0.6*c)
    expected_L = 0.8  # L = L₀/γ = 1/1.25 = 0.8
    if not np.isclose(L, expected_L, rtol=0.01):
        print("错误 3.5 长度收缩计算错误")
        all_passed = False
    else:
        print(f"通过 3.5 长度收缩正确 (v=0.6c 时 L = {L:.2f} L₀)")

    # 检查 3.6 - 双生子佯谬
    T_e, T_t = twin_paradox_ages(0.8*c, 10)
    if not T_t < T_e:
        print("错误 3.6 双生子佯谬：旅行者应比地球双胞胎年轻")
        all_passed = False
    else:
        print(f"通过 3.6 双生子佯谬正确 (地球: {T_e:.1f}, 旅行者: {T_t:.1f})")

    if all_passed:
        print("\n所有测试通过！正在生成可视化图像...")
        try:
            plot_spacetime()
        except Exception as e:
            print(f"可视化生成失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("时空与闵可夫斯基几何 Spacetime Geometry")
    print("=" * 50)
    verify()
