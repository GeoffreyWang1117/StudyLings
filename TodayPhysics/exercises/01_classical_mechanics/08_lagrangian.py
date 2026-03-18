"""
拉格朗日力学 Lagrangian Mechanics
难度 Difficulty: ★★★★★

================================================================================
学习目标 Learning Objectives
================================================================================
- 理解广义坐标和拉格朗日量的概念
  Understand generalized coordinates and the Lagrangian
- 掌握欧拉-拉格朗日方程的推导和应用
  Master the Euler-Lagrange equation and its applications
- 将拉格朗日方法应用于约束系统
  Apply Lagrangian methods to constrained systems
- 识别循环坐标和对应的守恒量
  Identify cyclic coordinates and corresponding conservation laws

================================================================================
物理背景 Physical Background
================================================================================
拉格朗日力学是经典力学的高级形式，用能量而非力来描述运动。

1. 广义坐标 Generalized Coordinates:
   用最少数量的独立变量描述系统配置
   例：单摆用角度θ描述，而不是笛卡尔坐标(x, y)

2. 拉格朗日量 Lagrangian:
   L = T - V（动能减势能）
   L是广义坐标q、广义速度q̇和时间t的函数

3. 欧拉-拉格朗日方程 Euler-Lagrange Equation:
   d/dt(∂L/∂q̇) - ∂L/∂q = 0
   这是变分原理（最小作用量原理）的结果

4. 循环坐标与守恒量 Cyclic Coordinates:
   如果L不显含某广义坐标q，则∂L/∂q̇是守恒量（广义动量）
   例：角动量守恒对应角度φ不显含于L

5. 优点 Advantages:
   - 自动处理约束
   - 便于选择最方便的坐标
   - 能量守恒自然满足
   - 容易识别守恒量

6. 双摆 Double Pendulum:
   经典的混沌系统例子，拉格朗日方法大大简化了方程推导

HINT: 拉格朗日量 L = T - V（动能 - 势能）
HINT: 欧拉-拉格朗日方程: d/dt(∂L/∂q̇) - ∂L/∂q = 0
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import sympy as sp
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])

# I AM NOT DONE

g = 9.8  # m/s²

# =============================================================================
# 练习 8.1: 简单摆的拉格朗日量
# Exercise 8.1: Lagrangian of Simple Pendulum
# =============================================================================
# 广义坐标: θ (角度)
# 动能: T = (1/2)m(Lθ̇)² = (1/2)mL²θ̇²
# 势能: V = -mgL cos(θ) (选取悬挂点为零势能点)
# 拉格朗日量: L = T - V

def pendulum_kinetic_energy(m, L, theta_dot):
    """单摆动能"""
    # TODO: 计算动能
    T = 0.5 * m * L**2 * theta_dot**2
    return T

def pendulum_potential_energy(m, L, theta, g=9.8):
    """单摆势能（相对于最低点）"""
    # TODO: 计算势能
    V = m * g * L * (1 - np.cos(theta))
    return V

def pendulum_lagrangian(m, L, theta, theta_dot, g=9.8):
    """单摆拉格朗日量"""
    T = pendulum_kinetic_energy(m, L, theta_dot)
    V = pendulum_potential_energy(m, L, theta, g)
    # TODO: 计算拉格朗日量
    Lag = T - V
    return Lag


# =============================================================================
# 练习 8.2: 欧拉-拉格朗日方程推导
# Exercise 8.2: Euler-Lagrange Equation
# =============================================================================
# 对于单摆: d/dt(mL²θ̇) + mgL sin(θ) = 0
# 即: θ̈ = -(g/L) sin(θ)

def pendulum_equation_of_motion(theta, g, L):
    """
    返回单摆运动方程右边: θ̈ = -(g/L)sin(θ)
    """
    # TODO: 返回角加速度
    theta_ddot = -(g / L) * np.sin(theta)
    return theta_ddot

def simulate_pendulum(theta0, omega0, L, t_span, dt=0.01, g=9.8):
    """
    模拟单摆运动
    状态: [θ, θ̇]
    """
    def derivatives(state, t):
        theta, omega = state
        theta_dot = omega
        omega_dot = pendulum_equation_of_motion(theta, g, L)
        return [theta_dot, omega_dot]

    t = np.arange(t_span[0], t_span[1], dt)
    solution = odeint(derivatives, [theta0, omega0], t)
    return t, solution[:, 0], solution[:, 1]


# =============================================================================
# 练习 8.3: 双摆系统
# Exercise 8.3: Double Pendulum System
# =============================================================================
# 双摆是混沌系统的经典例子

def double_pendulum_derivatives(state, t, m1, m2, L1, L2, g=9.8):
    """
    双摆运动方程
    state = [θ1, θ2, ω1, ω2]
    """
    theta1, theta2, omega1, omega2 = state
    delta = theta2 - theta1

    # 复杂的运动方程（从拉格朗日方程导出）
    den1 = (m1 + m2) * L1 - m2 * L1 * np.cos(delta)**2
    den2 = (L2 / L1) * den1

    # TODO: 计算角加速度（这是简化形式）
    theta1_dot = omega1
    theta2_dot = omega2

    omega1_dot = (m2 * L1 * omega1**2 * np.sin(delta) * np.cos(delta) +
                  m2 * g * np.sin(theta2) * np.cos(delta) +
                  m2 * L2 * omega2**2 * np.sin(delta) -
                  (m1 + m2) * g * np.sin(theta1)) / den1

    omega2_dot = (-m2 * L2 * omega2**2 * np.sin(delta) * np.cos(delta) +
                  (m1 + m2) * g * np.sin(theta1) * np.cos(delta) -
                  (m1 + m2) * L1 * omega1**2 * np.sin(delta) -
                  (m1 + m2) * g * np.sin(theta2)) / den2

    return [theta1_dot, theta2_dot, omega1_dot, omega2_dot]

def simulate_double_pendulum(theta1_0, theta2_0, L1, L2, m1, m2, t_end=20, dt=0.01):
    """模拟双摆"""
    t = np.arange(0, t_end, dt)
    state0 = [theta1_0, theta2_0, 0, 0]  # 初始角速度为0
    solution = odeint(double_pendulum_derivatives, state0, t, args=(m1, m2, L1, L2))
    return t, solution


# =============================================================================
# 练习 8.4: 广义坐标与约束
# Exercise 8.4: Generalized Coordinates and Constraints
# =============================================================================
# 斜面上的滑块（约束：只能沿斜面运动）
# 广义坐标：沿斜面的位移 s
# 动能: T = (1/2)mṡ²
# 势能: V = -mgs sin(α)（α是斜面倾角）

def inclined_plane_lagrangian(m, s_dot, s, alpha, g=9.8):
    """斜面滑块的拉格朗日量"""
    T = 0.5 * m * s_dot**2
    V = m * g * s * np.sin(alpha)  # s增加，高度增加
    # TODO: 返回拉格朗日量
    L = T - V
    return L

def inclined_plane_acceleration(alpha, g=9.8):
    """斜面滑块的加速度（从E-L方程得到）"""
    # s̈ = -g sin(α)
    # TODO: 返回加速度
    a = -g * np.sin(alpha)
    return a


# =============================================================================
# 练习 8.5: 循环坐标与守恒量
# Exercise 8.5: Cyclic Coordinates and Conservation
# =============================================================================
# 如果 L 不显含某广义坐标 q，则 ∂L/∂q̇ = 常数（广义动量守恒）
# 例：中心力场中的角动量守恒

def central_force_lagrangian(m, r, r_dot, phi_dot, V_r):
    """
    中心力场的拉格朗日量（极坐标）
    T = (1/2)m(ṙ² + r²φ̇²)
    V = V(r) 只依赖于 r
    """
    T = 0.5 * m * (r_dot**2 + r**2 * phi_dot**2)
    # TODO: 返回拉格朗日量
    L = T - V_r
    return L

def angular_momentum_conservation(m, r, phi_dot):
    """
    循环坐标 φ 对应的守恒量（角动量）
    p_φ = ∂L/∂φ̇ = mr²φ̇
    """
    # TODO: 计算角动量
    L_angular = m * r**2 * phi_dot
    return L_angular


# =============================================================================
# 练习 8.6: 哈密顿量
# Exercise 8.6: Hamiltonian
# =============================================================================
# H = Σpq̇ - L = T + V (对于自然系统)
# 哈密顿量通常等于总能量

def hamiltonian_pendulum(m, L, theta, theta_dot, g=9.8):
    """单摆的哈密顿量"""
    T = pendulum_kinetic_energy(m, L, theta_dot)
    V = pendulum_potential_energy(m, L, theta, g)
    # TODO: 计算哈密顿量（总能量）
    H = T + V
    return H


# =============================================================================
# 可视化
# =============================================================================
def plot_lagrangian():
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # 1. 单摆相空间
    ax1 = axes[0, 0]
    t, theta, omega = simulate_pendulum(np.pi/4, 0, 1.0, (0, 10))
    ax1.plot(theta, omega)
    ax1.set_xlabel('θ (rad)')
    ax1.set_ylabel('ω (rad/s)')
    ax1.set_title('单摆相空间 Pendulum Phase Space')
    ax1.grid(True, alpha=0.3)

    # 2. 双摆轨迹
    ax2 = axes[0, 1]
    t, sol = simulate_double_pendulum(np.pi/2, np.pi/2, 1.0, 1.0, 1.0, 1.0, t_end=20)
    x2 = np.sin(sol[:, 0]) + np.sin(sol[:, 1])
    y2 = -np.cos(sol[:, 0]) - np.cos(sol[:, 1])
    ax2.plot(x2, y2, 'b-', linewidth=0.5, alpha=0.7)
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.set_title('双摆第二摆锤轨迹 Double Pendulum')
    ax2.set_aspect('equal')
    ax2.grid(True, alpha=0.3)

    # 3. 能量守恒验证
    ax3 = axes[1, 0]
    H = [hamiltonian_pendulum(1.0, 1.0, theta[i], omega[i]) for i in range(len(t))]
    ax3.plot(t, H)
    ax3.set_xlabel('t (s)')
    ax3.set_ylabel('H (J)')
    ax3.set_title('哈密顿量守恒 Hamiltonian Conservation')
    ax3.grid(True, alpha=0.3)

    # 4. 双摆混沌对比
    ax4 = axes[1, 1]
    _, sol1 = simulate_double_pendulum(np.pi/2, np.pi/2, 1.0, 1.0, 1.0, 1.0)
    _, sol2 = simulate_double_pendulum(np.pi/2 + 0.001, np.pi/2, 1.0, 1.0, 1.0, 1.0)
    ax4.plot(sol1[:, 0], label='θ₁(0) = π/2')
    ax4.plot(sol2[:, 0], label='θ₁(0) = π/2 + 0.001')
    ax4.set_xlabel('Step')
    ax4.set_ylabel('θ₁ (rad)')
    ax4.set_title('双摆混沌敏感性 Chaos Sensitivity')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('lagrangian_mechanics.png', dpi=150)
    print("图像已保存为 lagrangian_mechanics.png")
    plt.show()


def verify():
    all_passed = True

    # Check 8.1
    L_test = pendulum_lagrangian(1.0, 1.0, 0, 1.0)
    T_test = 0.5 * 1.0 * 1.0**2 * 1.0**2
    V_test = 1.0 * 9.8 * 1.0 * (1 - np.cos(0))
    if not np.isclose(L_test, T_test - V_test, rtol=0.01):
        print("❌ 8.1 拉格朗日量错误")
        all_passed = False
    else:
        print("✓ 8.1 拉格朗日量正确")

    # Check 8.2
    theta_ddot = pendulum_equation_of_motion(np.pi/6, 9.8, 1.0)
    expected = -9.8 * np.sin(np.pi/6)
    if not np.isclose(theta_ddot, expected, rtol=0.01):
        print("❌ 8.2 运动方程错误")
        all_passed = False
    else:
        print("✓ 8.2 欧拉-拉格朗日方程正确")

    # Check 8.4
    a = inclined_plane_acceleration(np.pi/6)
    if not np.isclose(a, -9.8 * 0.5, rtol=0.01):
        print("❌ 8.4 斜面加速度错误")
        all_passed = False
    else:
        print("✓ 8.4 约束系统正确")

    # Check 8.5
    L_ang = angular_momentum_conservation(1.0, 2.0, 3.0)
    if not np.isclose(L_ang, 12.0, rtol=0.01):
        print("❌ 8.5 角动量计算错误")
        all_passed = False
    else:
        print("✓ 8.5 守恒量正确")

    # Check 8.6 - Energy conservation
    t, theta, omega = simulate_pendulum(0.5, 0, 1.0, (0, 5))
    H_initial = hamiltonian_pendulum(1.0, 1.0, theta[0], omega[0])
    H_final = hamiltonian_pendulum(1.0, 1.0, theta[-1], omega[-1])
    if abs(H_final - H_initial) / H_initial > 0.01:
        print("❌ 8.6 能量不守恒")
        all_passed = False
    else:
        print("✓ 8.6 哈密顿量守恒正确")

    if all_passed:
        print("\n🎉 所有测试通过！")
        try:
            plot_lagrangian()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("拉格朗日力学 Lagrangian Mechanics")
    print("=" * 50)
    verify()
