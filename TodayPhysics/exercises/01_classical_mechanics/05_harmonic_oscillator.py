"""
简谐振动与阻尼振动 Simple Harmonic Motion and Damped Oscillation
难度 Difficulty: ★★★

================================================================================
学习目标 Learning Objectives
================================================================================
- 理解简谐运动的数学描述和物理特征
  Understand the mathematical description and physical characteristics of SHM
- 分析阻尼振动的三种情况（欠阻尼、临界阻尼、过阻尼）
  Analyze three cases of damped oscillation (under-, critical-, over-damped)
- 数值求解二阶常微分方程
  Numerically solve second-order ordinary differential equations
- 理解受迫振动和共振现象
  Understand driven oscillation and resonance

================================================================================
物理背景 Physical Background
================================================================================
1. 简谐振动 Simple Harmonic Motion (SHM):
   最基本的振动形式，满足胡克定律 F = -kx 的系统都会做简谐运动。
   - 运动方程: m(d²x/dt²) = -kx，即 d²x/dt² + ω²x = 0
   - 角频率: ω = sqrt(k/m)
   - 周期: T = 2π/ω = 2π*sqrt(m/k)
   - 解: x(t) = A*cos(ωt + φ)，A是振幅，φ是初相位

2. 阻尼振动 Damped Oscillation:
   考虑阻力（与速度成正比）的振动：m(d²x/dt²) + b(dx/dt) + kx = 0
   定义阻尼系数 γ = b/(2m)，固有频率 ω₀ = sqrt(k/m)
   方程变为: d²x/dt² + 2γ(dx/dt) + ω₀²x = 0

   三种情况 Three cases:
   - 欠阻尼 Underdamped (γ < ω₀): 振荡衰减，x = Ae^(-γt)cos(ω't + φ)
   - 临界阻尼 Critically damped (γ = ω₀): 最快回到平衡，无振荡
   - 过阻尼 Overdamped (γ > ω₀): 缓慢回到平衡，无振荡

3. 受迫振动 Driven Oscillation:
   外加周期驱动力: d²x/dt² + 2γ(dx/dt) + ω₀²x = F₀cos(ω_d·t)/m
   当驱动频率 ω_d 接近固有频率 ω₀ 时，发生共振。

4. 能量 Energy:
   - 动能: KE = (1/2)mv² = (1/2)m(dx/dt)²
   - 势能: PE = (1/2)kx²
   - 简谐振动中总能量守恒: E = KE + PE = (1/2)kA² = 常数

HINT: 简谐运动方程: d²x/dt² + ω²x = 0，解为 x = A*cos(ωt + φ)
HINT: 阻尼振动方程: d²x/dt² + 2γ*(dx/dt) + ω₀²x = 0
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.physics_helpers import integrate_ode

# I AM NOT DONE

# =============================================================================
# 练习 5.1: 简谐振动的解析解
# Exercise 5.1: Analytical Solution of SHM
# =============================================================================
# 物理背景 Physical Background:
# 弹簧振子是简谐运动的典型例子。弹簧对物体的恢复力 F = -kx 满足胡克定律。
# 由牛顿第二定律：m(d²x/dt²) = -kx
# 这是一个二阶线性常微分方程，解为正弦函数。
#
# 由初始条件确定振幅和相位 Determining amplitude and phase from initial conditions:
# 一般解: x(t) = A*cos(ωt + φ)
# 初始位移: x(0) = A*cos(φ) = x0
# 初始速度: v(0) = -Aω*sin(φ) = v0
# 振幅: A = sqrt(x0² + (v0/ω)²)
#
# 题目 Problem:
# 弹簧振子: 质量 m = 0.5 kg, 劲度系数 k = 50 N/m
# Spring-mass system: mass m = 0.5 kg, spring constant k = 50 N/m
# 初始位移 x0 = 0.1 m, 初始速度 v0 = 0
# Initial displacement x0 = 0.1 m, initial velocity v0 = 0
#
# 计算 Calculate:
# 1) 角频率 ω = sqrt(k/m)，单位: rad/s
# 2) 周期 T = 2π/ω，单位: s
# 3) 振幅 A，单位: m

m = 0.5   # 质量 mass，单位：kg
k = 50.0  # 弹簧劲度系数 spring constant，单位：N/m
x0 = 0.1  # 初始位移 initial displacement，单位：m
v0 = 0.0  # 初始速度 initial velocity，单位：m/s

# TODO: 计算角频率 omega, 周期 T, 振幅 A
# 提示：ω = sqrt(k/m)，T = 2π/ω，A = sqrt(x0² + (v0/ω)²)
omega = None  # 修改这里 (单位：rad/s)
T = None      # 修改这里 (单位：s)
A = None      # 修改这里 (单位：m，提示: A = sqrt(x0² + (v0/ω)²))


# =============================================================================
# 练习 5.2: 简谐振动的数值模拟
# Exercise 5.2: Numerical Simulation of SHM
# =============================================================================
# 物理背景 Physical Background:
# 数值求解微分方程需要将高阶方程转化为一阶方程组。
#
# 将二阶微分方程转化为一阶方程组 Converting to first-order system:
# 原方程: d²x/dt² = -ω²x
# 引入辅助变量 v = dx/dt
# 得到方程组: dx/dt = v, dv/dt = -ω²x
#
# 状态向量 State vector: y = [x, v]
# 导数: dy/dt = [v, -ω²x]
#
# 这种转化方法适用于所有高阶微分方程的数值求解。

def shm_derivatives(y, t, omega_sq):
    """
    简谐振动的导数函数
    Derivative function for simple harmonic motion

    参数 Parameters:
        y: 状态向量 [x, v]（位移和速度）
        t: 时间（此问题中未使用，但保留以兼容ODE求解器）
        omega_sq: ω²（角频率的平方）

    返回 Returns:
        导数数组 [dx/dt, dv/dt] = [v, -ω²x]
    """
    x, v = y
    # 简谐振动: dv/dt = -ω²x（恢复加速度）
    dxdt = v
    dvdt = -omega_sq * x
    return np.array([dxdt, dvdt])


def simulate_shm(x0, v0, omega, t_end=5.0, dt=0.001):
    """模拟简谐振动"""
    omega_sq = omega**2
    y0 = np.array([x0, v0])

    def dydt(y, t):
        return shm_derivatives(y, t, omega_sq)

    t, y = integrate_ode(dydt, y0, (0, t_end), dt, method='rk4')
    return t, y[:, 0], y[:, 1]  # t, x, v


# 运行模拟
if omega is not None:
    t_shm, x_shm, v_shm = simulate_shm(x0, v0, omega)


# =============================================================================
# 练习 5.3: 阻尼振动
# Exercise 5.3: Damped Oscillation
# =============================================================================
# 物理背景 Physical Background:
# 实际的振动系统都有能量损耗（如摩擦、空气阻力），导致振动逐渐衰减。
# 假设阻尼力与速度成正比：F_damping = -b*v
#
# 阻尼振动方程 Damped oscillation equation:
# m(d²x/dt²) + b(dx/dt) + kx = 0
# 令 γ = b/(2m)（阻尼系数），ω₀ = sqrt(k/m)（固有角频率）
# 得：d²x/dt² + 2γ(dx/dt) + ω₀²x = 0
#
# 三种阻尼情况 Three damping cases:
# 1. 欠阻尼 Underdamped (γ < ω₀):
#    解: x = Ae^(-γt)cos(ω't + φ)，其中 ω' = sqrt(ω₀² - γ²)
#    系统振荡，但振幅指数衰减
#
# 2. 临界阻尼 Critically damped (γ = ω₀):
#    解: x = (A + Bt)e^(-γt)
#    系统最快回到平衡位置，无振荡
#
# 3. 过阻尼 Overdamped (γ > ω₀):
#    解: x = Ae^(-α₁t) + Be^(-α₂t)
#    系统缓慢回到平衡，无振荡

omega_0 = 10.0        # 固有角频率 natural frequency，单位：rad/s
gamma_under = 1.0     # 欠阻尼系数 underdamped (γ < ω₀)
gamma_critical = 10.0  # 临界阻尼系数 critically damped (γ = ω₀)
gamma_over = 20.0     # 过阻尼系数 overdamped (γ > ω₀)


def damped_derivatives(y, t, gamma, omega_0_sq):
    """
    阻尼振动的导数函数
    Derivative function for damped oscillation

    参数 Parameters:
        y: 状态向量 [x, v]
        t: 时间
        gamma: 阻尼系数 γ
        omega_0_sq: ω₀²（固有角频率的平方）

    返回 Returns:
        导数数组 [dx/dt, dv/dt]
        其中 dv/dt = -2γv - ω₀²x（包含阻尼项和恢复力项）
    """
    x, v = y
    # 阻尼振动: dv/dt = -2γv - ω₀²x
    # -2γv: 阻尼力项（与速度成正比，方向相反）
    # -ω₀²x: 恢复力项（与位移成正比，指向平衡位置）
    dxdt = v
    dvdt = -2 * gamma * v - omega_0_sq * x
    return np.array([dxdt, dvdt])


def simulate_damped(x0, v0, gamma, omega_0, t_end=3.0, dt=0.001):
    """模拟阻尼振动"""
    omega_0_sq = omega_0**2
    y0 = np.array([x0, v0])

    def dydt(y, t):
        return damped_derivatives(y, t, gamma, omega_0_sq)

    t, y = integrate_ode(dydt, y0, (0, t_end), dt, method='rk4')
    return t, y[:, 0], y[:, 1]


# 运行三种阻尼情况的模拟
t_under, x_under, _ = simulate_damped(x0, v0, gamma_under, omega_0)
t_crit, x_crit, _ = simulate_damped(x0, v0, gamma_critical, omega_0)
t_over, x_over, _ = simulate_damped(x0, v0, gamma_over, omega_0)


# =============================================================================
# 练习 5.4: 能量分析
# Exercise 5.4: Energy Analysis
# =============================================================================
# 物理背景 Physical Background:
# 在简谐振动中，能量在动能和势能之间不断转化，但总机械能保持不变。
#
# 能量公式 Energy formulas:
# - 动能 Kinetic Energy: KE = (1/2)mv²
# - 势能 Potential Energy: PE = (1/2)kx²
# - 总能量 Total Energy: E = KE + PE = (1/2)kA²（等于初始时刻的总能量）
#
# 能量转化 Energy conversion:
# - 平衡位置(x=0): KE最大，PE=0
# - 最大位移处(x=±A): KE=0，PE最大
# - 总能量始终等于 (1/2)kA²
#
# 数值模拟中能量守恒是检验算法精度的重要指标。

def calculate_energies(x, v, m, k):
    """
    计算简谐振动的动能、势能和总能量
    Calculate kinetic, potential, and total energy for SHM

    参数 Parameters:
        x: 位移（可以是数组）
        v: 速度（可以是数组）
        m: 质量
        k: 弹簧劲度系数

    返回 Returns:
        KE: 动能 (J)
        PE: 势能 (J)
        E: 总能量 (J)

    注意: 对于理想简谐振动，总能量 E 应该是常数
    """
    # 动能: KE = (1/2)mv²
    KE = 0.5 * m * v**2
    # 势能: PE = (1/2)kx²
    PE = 0.5 * k * x**2
    # 总能量: E = KE + PE
    E = KE + PE
    return KE, PE, E


# 计算能量（如果已完成模拟）
if omega is not None:
    KE_shm, PE_shm, E_shm = calculate_energies(x_shm, v_shm, m, k)


# =============================================================================
# 练习 5.5: 受迫振动与共振
# Exercise 5.5: Driven Oscillation and Resonance
# =============================================================================
# 物理背景 Physical Background:
# 受迫振动是指系统在外部周期性驱动力作用下的振动。
#
# 受迫振动方程 Driven oscillation equation:
# m(d²x/dt²) + b(dx/dt) + kx = F₀cos(ω_d·t)
# 即: d²x/dt² + 2γ(dx/dt) + ω₀²x = (F₀/m)cos(ω_d·t)
#
# 稳态解 Steady-state solution:
# x(t) = A(ω_d)cos(ω_d·t - φ)
# 振幅: A(ω_d) = (F₀/m) / sqrt((ω₀²-ω_d²)² + 4γ²ω_d²)
#
# 共振 Resonance:
# - 当驱动频率 ω_d 接近固有频率 ω₀ 时，振幅急剧增大
# - 共振频率 ω_r = sqrt(ω₀² - 2γ²)（对于小阻尼近似等于 ω₀）
# - 共振时振幅: A_max ≈ F₀/(2mγω₀)（与阻尼成反比）
#
# 应用: 乐器共鸣、收音机调谐、建筑物抗震设计等

def driven_derivatives(y, t, gamma, omega_0_sq, F0_over_m, omega_d):
    """
    受迫振动的导数函数
    Derivative function for driven oscillation

    参数 Parameters:
        y: 状态向量 [x, v]
        t: 时间（驱动力是时间的函数）
        gamma: 阻尼系数
        omega_0_sq: 固有角频率的平方
        F0_over_m: 驱动力幅度/质量
        omega_d: 驱动频率

    返回 Returns:
        导数数组 [dx/dt, dv/dt]
    """
    x, v = y
    # 驱动力项（周期性外力）
    driving_force = F0_over_m * np.cos(omega_d * t)
    dxdt = v
    # dv/dt = -2γv - ω₀²x + (F₀/m)cos(ω_d·t)
    dvdt = -2 * gamma * v - omega_0_sq * x + driving_force
    return np.array([dxdt, dvdt])


def simulate_driven(x0, v0, gamma, omega_0, F0_over_m, omega_d, t_end=10.0, dt=0.001):
    """模拟受迫振动"""
    omega_0_sq = omega_0**2
    y0 = np.array([x0, v0])

    def dydt(y, t):
        return driven_derivatives(y, t, gamma, omega_0_sq, F0_over_m, omega_d)

    t, y = integrate_ode(dydt, y0, (0, t_end), dt, method='rk4')
    return t, y[:, 0], y[:, 1]


# 模拟共振和非共振情况
F0_over_m = 1.0  # 驱动力幅度/质量
gamma_driven = 0.5  # 小阻尼

# 共振: ω_d = ω₀
t_res, x_res, _ = simulate_driven(0, 0, gamma_driven, omega_0, F0_over_m, omega_0)
# 非共振: ω_d = 0.5*ω₀
t_nonres, x_nonres, _ = simulate_driven(0, 0, gamma_driven, omega_0, F0_over_m, 0.5*omega_0)


# =============================================================================
# 可视化
# =============================================================================
def plot_all():
    """绘制所有振动图像"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. 简谐振动
    ax1 = axes[0, 0]
    if omega is not None:
        ax1.plot(t_shm, x_shm, 'b-', label='Numerical')
        # 解析解
        t_exact = np.linspace(0, 5, 1000)
        x_exact = A * np.cos(omega * t_exact)
        ax1.plot(t_exact, x_exact, 'r--', label='Analytical', alpha=0.7)
    ax1.set_xlabel('t (s)')
    ax1.set_ylabel('x (m)')
    ax1.set_title('简谐振动 Simple Harmonic Motion')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 阻尼振动对比
    ax2 = axes[0, 1]
    ax2.plot(t_under, x_under, 'b-', label=f'Underdamped (γ={gamma_under})')
    ax2.plot(t_crit, x_crit, 'g-', label=f'Critical (γ={gamma_critical})')
    ax2.plot(t_over, x_over, 'r-', label=f'Overdamped (γ={gamma_over})')
    ax2.set_xlabel('t (s)')
    ax2.set_ylabel('x (m)')
    ax2.set_title('阻尼振动 Damped Oscillation')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 能量守恒
    ax3 = axes[1, 0]
    if omega is not None:
        ax3.plot(t_shm, KE_shm, 'r-', label='KE', alpha=0.7)
        ax3.plot(t_shm, PE_shm, 'b-', label='PE', alpha=0.7)
        ax3.plot(t_shm, E_shm, 'k--', label='Total E', linewidth=2)
    ax3.set_xlabel('t (s)')
    ax3.set_ylabel('Energy (J)')
    ax3.set_title('能量守恒 Energy Conservation')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 受迫振动与共振
    ax4 = axes[1, 1]
    ax4.plot(t_res, x_res, 'r-', label=f'Resonance (ω_d = ω₀)', alpha=0.8)
    ax4.plot(t_nonres, x_nonres, 'b-', label=f'Off-resonance (ω_d = 0.5ω₀)', alpha=0.8)
    ax4.set_xlabel('t (s)')
    ax4.set_ylabel('x (m)')
    ax4.set_title('受迫振动与共振 Driven Oscillation & Resonance')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('harmonic_oscillator.png', dpi=150)
    print("图像已保存为 harmonic_oscillator.png")
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

    # 检查 5.1: 解析解
    # Check 5.1: Analytical Solution
    expected_omega = np.sqrt(k / m)
    expected_T = 2 * np.pi / expected_omega
    expected_A = np.sqrt(x0**2 + (v0 / expected_omega)**2) if expected_omega != 0 else x0

    if omega is None or T is None or A is None:
        print("❌ 5.1 解析解未完成 Analytical solution incomplete")
        all_passed = False
    elif not np.isclose(omega, expected_omega, rtol=0.01):
        print(f"❌ 5.1 角频率错误 Angular frequency incorrect")
        print(f"   期望 Expected: {expected_omega:.2f} rad/s, 得到 Got: {omega}")
        all_passed = False
    elif not np.isclose(T, expected_T, rtol=0.01):
        print(f"❌ 5.1 周期错误 Period incorrect")
        print(f"   期望 Expected: {expected_T:.4f} s, 得到 Got: {T}")
        all_passed = False
    elif not np.isclose(A, expected_A, rtol=0.01):
        print(f"❌ 5.1 振幅错误 Amplitude incorrect")
        print(f"   期望 Expected: {expected_A:.4f} m, 得到 Got: {A}")
        all_passed = False
    else:
        print(f"✓ 5.1 解析解正确 (ω={expected_omega:.2f} rad/s, T={expected_T:.4f} s, A={expected_A:.4f} m)")

    # 检查 5.2: 简谐振动模拟
    # Check 5.2: SHM Simulation
    if omega is not None and len(x_shm) > 100:
        max_x = np.max(np.abs(x_shm))
        if np.abs(max_x - A) / A > 0.05:
            print(f"❌ 5.2 简谐振动模拟振幅误差过大 SHM amplitude error too large")
            print(f"   期望 Expected: {A:.4f} m, 得到 Got: {max_x:.4f} m")
            all_passed = False
        else:
            print(f"✓ 5.2 简谐振动模拟正确 SHM simulation correct")
    else:
        print("❌ 5.2 简谐振动模拟未完成 SHM simulation incomplete")
        all_passed = False

    # 检查 5.3: 阻尼振动
    # Check 5.3: Damped Oscillation
    if len(x_under) > 100:
        sign_changes = np.sum(np.diff(np.sign(x_under[100:])) != 0)
        if sign_changes < 2:
            print("❌ 5.3 欠阻尼应该有振荡 Underdamped should oscillate")
            all_passed = False
        else:
            print("✓ 5.3 阻尼振动模拟正确 Damped oscillation correct")
    else:
        print("❌ 5.3 阻尼振动模拟未完成 Damped oscillation incomplete")
        all_passed = False

    # 检查 5.4: 能量守恒
    # Check 5.4: Energy Conservation
    if omega is not None and len(E_shm) > 100:
        E_variation = (np.max(E_shm) - np.min(E_shm)) / E_shm[0]
        if E_variation > 0.01:  # 1%容差
            print(f"❌ 5.4 能量不守恒 Energy not conserved")
            print(f"   变化率 Variation: {E_variation*100:.2f}%")
            all_passed = False
        else:
            print(f"✓ 5.4 能量守恒验证正确 (变化率 < 1%)")
    else:
        print("❌ 5.4 能量分析未完成 Energy analysis incomplete")
        all_passed = False

    # 检查 5.5: 共振
    # Check 5.5: Resonance
    if len(x_res) > 100:
        amp_res = np.max(np.abs(x_res[-1000:]))  # 稳态振幅
        amp_nonres = np.max(np.abs(x_nonres[-1000:]))
        if amp_res <= amp_nonres:
            print("❌ 5.5 共振振幅应该大于非共振 Resonance amplitude should be larger")
            all_passed = False
        else:
            print(f"✓ 5.5 共振现象正确 (共振振幅 {amp_res:.3f} > 非共振 {amp_nonres:.3f})")
    else:
        print("❌ 5.5 受迫振动模拟未完成 Driven oscillation incomplete")
        all_passed = False

    if all_passed:
        print("\n所有测试通过！正在生成可视化... All tests passed!")
        try:
            plot_all()
        except Exception as e:
            print(f"可视化生成失败 Visualization failed: {e}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("简谐振动与阻尼振动 Harmonic Oscillator")
    print("=" * 50)
    verify()
