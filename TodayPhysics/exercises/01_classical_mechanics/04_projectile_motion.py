"""
抛体运动模拟 Projectile Motion Simulation
难度 Difficulty: ★★★

================================================================================
学习目标 Learning Objectives
================================================================================
- 使用数值方法模拟抛体运动（欧拉法、龙格-库塔法）
  Simulate projectile motion using numerical methods (Euler, RK4)
- 理解解析解与数值解的关系和误差
  Understand the relationship between analytical and numerical solutions
- 可视化运动轨迹并分析空气阻力的影响
  Visualize trajectories and analyze the effect of air resistance

================================================================================
物理背景 Physical Background
================================================================================
抛体运动是物体在重力作用下的运动，是经典力学的基础问题。

1. 理想抛体运动（忽略空气阻力）Ideal Projectile (no air resistance):
   - 水平方向：匀速运动，x = v0*cos(θ)*t
   - 垂直方向：匀变速运动，y = v0*sin(θ)*t - (1/2)g*t²
   - 轨迹为抛物线

2. 解析公式 Analytical Formulas:
   - 最大高度: H = (v0*sin(θ))² / (2g)
   - 飞行时间: T = 2*v0*sin(θ) / g
   - 水平射程: R = v0² * sin(2θ) / g
   - 最大射程角度: θ = 45°

3. 数值方法 Numerical Methods:
   - 欧拉法 Euler: 一阶精度，y_{n+1} = y_n + dt * f(y_n, t_n)
   - 龙格-库塔法 RK4: 四阶精度，更准确但计算量更大

4. 带空气阻力 With Air Resistance:
   - 阻力与速度成正比: F_drag = -b*v
   - 阻力与速度平方成正比: F_drag = -c*v*|v|（更现实）
   - 需要用数值方法求解

运动方程 Equations of Motion:
dx/dt = vx,  dy/dt = vy
dvx/dt = 0 (无阻力) 或 -b*vx/m (有阻力)
dvy/dt = -g (无阻力) 或 -g - b*vy/m (有阻力)

HINT: 抛体运动可分解为水平和垂直两个独立运动
HINT: 状态向量 y = [x, y, vx, vy]，导数 dy/dt = [vx, vy, ax, ay]
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.physics_helpers import rk4_step

# I AM NOT DONE

g = 9.8  # m/s²

# =============================================================================
# 练习 4.1: 解析解 - 理想抛体运动
# Exercise 4.1: Analytical Solution - Ideal Projectile
# =============================================================================
# 物理背景 Physical Background:
# 理想抛体运动忽略空气阻力，可以得到解析解。
# 抛体运动可分解为水平方向的匀速运动和垂直方向的匀变速运动。
#
# 推导过程 Derivation:
# - 水平分速度: vx = v0*cos(θ)（恒定）
# - 垂直分速度: vy = v0*sin(θ) - g*t
# - 到达最高点时 vy = 0，此时 t = v0*sin(θ)/g
# - 最大高度: H = vy_初² / (2g) = (v0*sin(θ))² / (2g)
# - 飞行时间（上升+下降）: T = 2*v0*sin(θ) / g
# - 射程: R = vx * T = v0*cos(θ) * 2*v0*sin(θ)/g = v0²*sin(2θ)/g
#
# 题目 Problem:
# 以初速度 v0 = 20 m/s，角度 θ = 45° 抛出
# Launch at v0 = 20 m/s, angle θ = 45°
# 计算：1) 最大高度 2) 飞行时间 3) 水平射程
# Calculate: 1) max height 2) flight time 3) horizontal range
#
# 公式 Formulas:
# H_max = (v0*sin(θ))² / (2g)
# T = 2*v0*sin(θ) / g
# R = v0² * sin(2θ) / g
#
# 单位 Unit: 高度-m，时间-s，射程-m

v0 = 20.0  # 初速度 initial velocity，单位：m/s
theta = np.radians(45)  # 抛射角度，45度转为弧度

# TODO: 计算 H_max (最大高度), T_flight (飞行时间), R (射程)
# 提示：使用 np.sin() 和 np.cos()，注意角度已转为弧度
H_max = None    # 修改这里 (最大高度，单位：m)
T_flight = None  # 修改这里 (飞行时间，单位：s)
R = None        # 修改这里 (水平射程，单位：m)


# =============================================================================
# 练习 4.2: 数值模拟 - 欧拉法
# Exercise 4.2: Numerical Simulation - Euler Method
# =============================================================================
# 物理背景 Physical Background:
# 欧拉法是最简单的数值积分方法，基于一阶泰勒展开。
# 它用当前时刻的导数来估计下一时刻的状态，误差为 O(dt²)。
#
# 数值方法原理 Numerical Method:
# 将连续的微分方程离散化：y_{n+1} = y_n + dt * f(y_n, t_n)
# 其中 f(y, t) = dy/dt 是状态向量的时间导数
#
# 状态向量 State vector: y = [x, y, vx, vy]
# - x, y: 位置坐标
# - vx, vy: 速度分量
#
# 导数 Derivatives: dy/dt = [vx, vy, ax, ay]
# - dx/dt = vx (位置变化率 = 速度)
# - dy/dt = vy
# - dvx/dt = 0 (水平方向无力)
# - dvy/dt = -g (重力加速度)

def projectile_derivatives(y, t):
    """
    计算抛体运动的导数（无空气阻力）
    Calculate derivatives for projectile motion (no air resistance)

    参数 Parameters:
        y: 状态向量 [x, y, vx, vy]
        t: 时间（本问题中未使用，但保留以兼容ODE求解器）

    返回 Returns:
        导数数组 [dx/dt, dy/dt, dvx/dt, dvy/dt] = [vx, vy, 0, -g]
    """
    x, y_pos, vx, vy = y
    # TODO: 返回导数数组 [vx, vy, 0, -g]
    # 提示：水平方向无加速度(ax=0)，垂直方向加速度为-g
    return np.array([0, 0, 0, 0])  # 修改这里


def euler_simulate(v0, theta, dt=0.01):
    """
    使用欧拉法模拟抛体运动
    Simulate projectile motion using Euler method

    参数 Parameters:
        v0: 初速度大小 (m/s)
        theta: 抛射角度 (弧度)
        dt: 时间步长 (s)

    返回 Returns:
        times: 时间数组
        trajectory: 轨迹数组，每行为 [x, y, vx, vy]
    """
    # 初始条件 Initial conditions
    vx0 = v0 * np.cos(theta)  # 初始水平速度
    vy0 = v0 * np.sin(theta)  # 初始垂直速度
    y = np.array([0.0, 0.0, vx0, vy0])  # 状态向量 [x, y, vx, vy]

    trajectory = [y.copy()]
    t = 0
    times = [t]

    # 欧拉法循环：直到物体落地 (y < 0)
    # Euler loop: until object hits ground (y < 0)
    while y[1] >= 0:
        # 欧拉步进 Euler step: y_new = y_old + dt * dy/dt
        dydt = projectile_derivatives(y, t)
        y = y + dt * dydt  # 欧拉法更新

        t += dt
        trajectory.append(y.copy())
        times.append(t)

    return np.array(times), np.array(trajectory)


# 运行模拟
times_euler, traj_euler = euler_simulate(v0, theta)


# =============================================================================
# 练习 4.3: 数值模拟 - 四阶龙格-库塔法
# Exercise 4.3: Numerical Simulation - RK4 Method
# =============================================================================
# 物理背景 Physical Background:
# 四阶龙格-库塔法（RK4）是更精确的数值积分方法，局部误差为 O(dt⁵)。
# 它通过计算多个中间点的斜率来提高精度。
#
# RK4算法 Algorithm:
# k1 = f(y_n, t_n)
# k2 = f(y_n + dt/2 * k1, t_n + dt/2)
# k3 = f(y_n + dt/2 * k2, t_n + dt/2)
# k4 = f(y_n + dt * k3, t_n + dt)
# y_{n+1} = y_n + dt/6 * (k1 + 2*k2 + 2*k3 + k4)
#
# 优点：比欧拉法更准确，适用于大多数常微分方程问题

def rk4_simulate(v0, theta, dt=0.01):
    """
    使用四阶龙格-库塔法模拟抛体运动
    Simulate projectile motion using RK4 method

    参数 Parameters:
        v0: 初速度大小 (m/s)
        theta: 抛射角度 (弧度)
        dt: 时间步长 (s)

    返回 Returns:
        times: 时间数组
        trajectory: 轨迹数组

    注意: RK4比欧拉法更精确，相同步长下误差更小
    """
    vx0 = v0 * np.cos(theta)
    vy0 = v0 * np.sin(theta)
    y = np.array([0.0, 0.0, vx0, vy0])

    trajectory = [y.copy()]
    t = 0
    times = [t]

    while y[1] >= 0:
        # 使用 rk4_step 函数进行积分
        # rk4_step 已在 physics_helpers 中实现
        y = rk4_step(y, projectile_derivatives, dt, t)

        t += dt
        trajectory.append(y.copy())
        times.append(t)

    return np.array(times), np.array(trajectory)


# 运行 RK4 模拟
times_rk4, traj_rk4 = rk4_simulate(v0, theta)


# =============================================================================
# 练习 4.4: 带空气阻力的抛体运动
# Exercise 4.4: Projectile with Air Resistance
# =============================================================================
# 物理背景 Physical Background:
# 实际的抛体运动会受到空气阻力的影响。常见的阻力模型：
# 1. 线性阻力（低速）: F_drag = -b*v（与速度成正比）
# 2. 二次阻力（高速）: F_drag = -c*v*|v|（与速度平方成正比）
#
# 本练习使用线性阻力模型：
# 水平方向: m*ax = -b*vx → ax = -(b/m)*vx
# 垂直方向: m*ay = -m*g - b*vy → ay = -g - (b/m)*vy
#
# 空气阻力的影响 Effects of Air Resistance:
# - 减小最大高度
# - 减小水平射程
# - 轨迹不再是抛物线，下降段更陡
# - 需要数值方法求解（无解析解）

def projectile_with_drag(y, t, b_over_m=0.1):
    """
    带空气阻力的抛体运动导数（线性阻力模型）
    Derivatives for projectile motion with linear air resistance

    参数 Parameters:
        y: 状态向量 [x, y, vx, vy]
        t: 时间
        b_over_m: 阻力系数/质量 (b/m)，单位：1/s

    返回 Returns:
        导数数组 [vx, vy, ax, ay]

    物理解释 Physical Interpretation:
        b_over_m 越大，阻力越强，射程和高度越小
    """
    x, y_pos, vx, vy = y

    # 带阻力的加速度 Acceleration with drag
    # ax = -(b/m)*vx（水平方向，阻力减速）
    # ay = -g - (b/m)*vy（垂直方向，重力+阻力）
    ax = -b_over_m * vx
    ay = -g - b_over_m * vy

    return np.array([vx, vy, ax, ay])


def simulate_with_drag(v0, theta, b_over_m=0.1, dt=0.01):
    """
    模拟带空气阻力的抛体运动
    Simulate projectile motion with air resistance

    参数 Parameters:
        v0: 初速度大小 (m/s)
        theta: 抛射角度 (弧度)
        b_over_m: 阻力系数/质量 (1/s)
        dt: 时间步长 (s)

    返回 Returns:
        trajectory: 轨迹数组

    注意 Note:
        使用RK4方法求解，因为带阻力的方程没有解析解
    """
    vx0 = v0 * np.cos(theta)
    vy0 = v0 * np.sin(theta)
    y = np.array([0.0, 0.0, vx0, vy0])

    trajectory = [y.copy()]
    t = 0

    # 模拟直到物体落地
    while y[1] >= 0 or t < 0.1:  # 确保至少运行一会儿
        y = rk4_step(y, lambda y, t: projectile_with_drag(y, t, b_over_m), dt, t)
        t += dt
        trajectory.append(y.copy())
        if t > 10:  # 安全退出，防止无限循环
            break

    return np.array(trajectory)


# 运行带阻力的模拟
traj_drag = simulate_with_drag(v0, theta, b_over_m=0.1)


# =============================================================================
# 可视化
# =============================================================================
def plot_trajectories():
    """绘制所有轨迹对比图"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 左图：轨迹对比
    ax1 = axes[0]
    ax1.plot(traj_euler[:, 0], traj_euler[:, 1], 'b-', label='Euler', alpha=0.7)
    ax1.plot(traj_rk4[:, 0], traj_rk4[:, 1], 'r--', label='RK4', alpha=0.7)
    ax1.plot(traj_drag[:, 0], traj_drag[:, 1], 'g-.', label='With Drag', alpha=0.7)

    # 解析解
    t_exact = np.linspace(0, T_flight if T_flight else 3, 100)
    x_exact = v0 * np.cos(theta) * t_exact
    y_exact = v0 * np.sin(theta) * t_exact - 0.5 * g * t_exact**2
    ax1.plot(x_exact, y_exact, 'k:', label='Exact', linewidth=2)

    ax1.set_xlabel('x (m)')
    ax1.set_ylabel('y (m)')
    ax1.set_title('抛体运动轨迹对比 Projectile Trajectories')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(bottom=-0.5)

    # 右图：速度随时间变化
    ax2 = axes[1]
    v_euler = np.sqrt(traj_euler[:, 2]**2 + traj_euler[:, 3]**2)
    v_rk4 = np.sqrt(traj_rk4[:, 2]**2 + traj_rk4[:, 3]**2)
    ax2.plot(times_euler, v_euler, 'b-', label='Euler', alpha=0.7)
    ax2.plot(times_rk4, v_rk4, 'r--', label='RK4', alpha=0.7)
    ax2.set_xlabel('t (s)')
    ax2.set_ylabel('|v| (m/s)')
    ax2.set_title('速度大小随时间变化 Speed vs Time')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('projectile_motion.png', dpi=150)
    print("图像已保存为 projectile_motion.png")
    plt.show()


# =============================================================================
# 验证函数 Verification Function - 不要修改 Do not modify
# =============================================================================
def verify():
    """
    验证所有练习的答案是否正确
    Verify all exercises
    """
    all_passed = True

    # 检查 4.1: 解析解
    # Check 4.1: Analytical Solution
    expected_H = (v0 * np.sin(theta))**2 / (2 * g)
    expected_T = 2 * v0 * np.sin(theta) / g
    expected_R = v0**2 * np.sin(2 * theta) / g

    if H_max is None or T_flight is None or R is None:
        print("❌ 4.1 解析解未完成 Analytical solution incomplete")
        all_passed = False
    elif not np.isclose(H_max, expected_H, rtol=0.01):
        print(f"❌ 4.1 最大高度错误 Max height incorrect")
        print(f"   期望 Expected: {expected_H:.2f} m, 得到 Got: {H_max}")
        all_passed = False
    elif not np.isclose(T_flight, expected_T, rtol=0.01):
        print(f"❌ 4.1 飞行时间错误 Flight time incorrect")
        print(f"   期望 Expected: {expected_T:.2f} s, 得到 Got: {T_flight}")
        all_passed = False
    elif not np.isclose(R, expected_R, rtol=0.01):
        print(f"❌ 4.1 射程错误 Range incorrect")
        print(f"   期望 Expected: {expected_R:.2f} m, 得到 Got: {R}")
        all_passed = False
    else:
        print(f"✓ 4.1 解析解正确 (H={expected_H:.2f}m, T={expected_T:.2f}s, R={expected_R:.2f}m)")

    # 检查 4.2: 欧拉法模拟
    # Check 4.2: Euler Method Simulation
    if len(traj_euler) < 10:
        print("❌ 4.2 欧拉法模拟未完成或数据不足 Euler simulation incomplete")
        all_passed = False
    else:
        euler_range = traj_euler[-1, 0]
        if abs(euler_range - expected_R) / expected_R > 0.1:  # 10%容差（欧拉法精度较低）
            print(f"❌ 4.2 欧拉法射程误差过大 Euler range error too large")
            print(f"   期望 Expected: ~{expected_R:.2f} m, 得到 Got: {euler_range:.2f} m")
            all_passed = False
        else:
            print(f"✓ 4.2 欧拉法模拟正确 (射程 Range: {euler_range:.2f} m)")

    # 检查 4.3: RK4模拟
    # Check 4.3: RK4 Simulation
    if len(traj_rk4) < 10:
        print("❌ 4.3 RK4模拟未完成或数据不足 RK4 simulation incomplete")
        all_passed = False
    else:
        rk4_range = traj_rk4[-1, 0]
        if abs(rk4_range - expected_R) / expected_R > 0.05:  # 5%容差（RK4更精确）
            print(f"❌ 4.3 RK4射程误差过大 RK4 range error too large")
            print(f"   期望 Expected: ~{expected_R:.2f} m, 得到 Got: {rk4_range:.2f} m")
            all_passed = False
        else:
            print(f"✓ 4.3 RK4模拟正确 (射程 Range: {rk4_range:.2f} m)")

    # 检查 4.4: 带阻力模拟
    # Check 4.4: Simulation with Drag
    if len(traj_drag) < 10:
        print("❌ 4.4 带阻力模拟未完成 Drag simulation incomplete")
        all_passed = False
    else:
        drag_range = traj_drag[-1, 0]
        # 有阻力时射程应该小于无阻力
        if drag_range >= expected_R:
            print(f"❌ 4.4 带阻力射程应小于无阻力 With drag, range should be less")
            print(f"   {drag_range:.2f} m >= {expected_R:.2f} m")
            all_passed = False
        else:
            print(f"✓ 4.4 带阻力模拟正确 (射程 Range: {drag_range:.2f} m < {expected_R:.2f} m)")

    if all_passed:
        print("\n所有测试通过！正在生成可视化... All tests passed! Generating visualization...")
        try:
            plot_trajectories()
        except Exception as e:
            print(f"可视化生成失败 Visualization failed: {e}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("抛体运动模拟 Projectile Motion Simulation")
    print("=" * 50)
    verify()
