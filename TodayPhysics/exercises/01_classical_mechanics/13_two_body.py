"""
二体问题 Two-Body Problem
难度 Difficulty: ★★★★

================================================================================
学习目标 Learning Objectives
================================================================================
- 理解质心坐标系和相对运动分解
  Understand center of mass frame and relative motion decomposition
- 掌握约化质量概念及其应用
  Master the reduced mass concept and its applications
- 分析弹性和非弹性碰撞问题
  Analyze elastic and inelastic collision problems
- 计算二体引力系统的轨道运动
  Calculate orbital motion in two-body gravitational systems

================================================================================
物理背景 Physical Background
================================================================================
二体问题是分析力学的经典问题，将两个相互作用粒子的运动分解为
质心运动和相对运动两个独立部分。

1. 约化质量 Reduced Mass:
   μ = m₁m₂/(m₁+m₂)
   - 将二体问题等效为单体问题
   - 相对运动遵循: μr̈ = F(r)
   - 极限情况: m₁ >> m₂ 时 μ ≈ m₂

2. 质心坐标系 Center of Mass Frame:
   质心位置: R = (m₁r₁ + m₂r₂)/M
   相对位置: r = r₁ - r₂
   质心速度: V_cm = (m₁v₁ + m₂v₂)/M（守恒）

3. 能量分解 Energy Decomposition:
   总动能 = 质心动能 + 相对运动动能
   K = (1/2)MV²_cm + (1/2)μv²_rel

4. 弹性碰撞 Elastic Collision:
   - 动量守恒: m₁v₁ + m₂v₂ = m₁v₁' + m₂v₂'
   - 动能守恒: K_i = K_f
   - 等质量碰撞: 速度交换

5. 非弹性碰撞 Inelastic Collision:
   - 恢复系数: e = (v₂' - v₁')/(v₁ - v₂)
   - e = 1: 完全弹性
   - e = 0: 完全非弹性（粘连）
   - 能量损失: ΔK = (1/2)μv²_rel(1-e²)

6. 二体引力问题 Two-Body Gravitational Problem:
   - 两个天体绕共同质心运动
   - 轨道周期: T = 2π√(a³/G(m₁+m₂))
   - 每个天体的轨道半长轴之比: a₁/a₂ = m₂/m₁

HINT: 约化质量: μ = m₁m₂/(m₁+m₂)
HINT: 质心: R = (m₁r₁ + m₂r₂)/(m₁+m₂)
HINT: 质心系中碰撞后速度方向反转
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import G

# I AM NOT DONE

# =============================================================================
# 练习 13.1: 约化质量
# Exercise 13.1: Reduced Mass
# =============================================================================
# 约化质量是二体问题的核心概念
# 它将两体相互作用问题简化为等效的单体问题

def reduced_mass(m1, m2):
    """
    约化质量 Reduced Mass
    μ = m₁m₂/(m₁+m₂)

    物理意义：
    - 相对运动的"有效质量"
    - μr̈ = F(r)（r为相对位置）

    极限情况：
    - m₁ = m₂: μ = m/2（等质量）
    - m₁ >> m₂: μ ≈ m₂（重粒子近似静止）

    应用：
    - 氢原子中电子的运动
    - 双星系统的相对运动
    - 碰撞问题的能量分析
    """
    # TODO: 计算约化质量
    return m1 * m2 / (m1 + m2)

def total_mass(m1, m2):
    """
    总质量 Total Mass
    M = m₁ + m₂

    质心以恒定速度运动（动量守恒）
    """
    return m1 + m2


# =============================================================================
# 练习 13.2: 质心坐标
# Exercise 13.2: Center of Mass Coordinates
# =============================================================================
def center_of_mass(m1, r1, m2, r2):
    """
    质心位置 R = (m₁r₁ + m₂r₂)/(m₁+m₂)
    """
    M = total_mass(m1, m2)
    return (m1 * r1 + m2 * r2) / M

def relative_position(r1, r2):
    """相对位置 r = r₁ - r₂"""
    return r1 - r2

def lab_to_cm(m1, r1, v1, m2, r2, v2):
    """
    从实验室系转换到质心系
    返回: (R, V_cm, r, v_rel)
    """
    M = total_mass(m1, m2)
    R = center_of_mass(m1, r1, m2, r2)
    V_cm = (m1 * v1 + m2 * v2) / M
    r = relative_position(r1, r2)
    v_rel = v1 - v2
    return R, V_cm, r, v_rel


# =============================================================================
# 练习 13.3: 二体引力问题
# Exercise 13.3: Two-Body Gravitational Problem
# =============================================================================
def two_body_equations(state, t, m1, m2):
    """
    二体引力方程
    state = [x1, y1, vx1, vy1, x2, y2, vx2, vy2]
    """
    x1, y1, vx1, vy1, x2, y2, vx2, vy2 = state

    r = np.sqrt((x2-x1)**2 + (y2-y1)**2)
    r_vec = np.array([x2-x1, y2-y1])

    # 加速度
    a1 = G * m2 / r**3 * r_vec
    a2 = -G * m1 / r**3 * r_vec

    return [vx1, vy1, a1[0], a1[1], vx2, vy2, a2[0], a2[1]]

def orbital_period_two_body(m1, m2, a):
    """
    二体轨道周期 T = 2π√(a³/G(m₁+m₂))
    """
    M = total_mass(m1, m2)
    return 2 * np.pi * np.sqrt(a**3 / (G * M))


# =============================================================================
# 练习 13.4: 弹性碰撞
# Exercise 13.4: Elastic Collision
# =============================================================================
# 弹性碰撞: 动量守恒 + 动能守恒
# 完全确定碰撞后的速度（一维情况）

def elastic_collision_1d(m1, v1, m2, v2):
    """
    一维弹性碰撞后的速度 1D Elastic Collision Final Velocities

    由动量和动能守恒联立求解:
    v₁' = ((m₁-m₂)v₁ + 2m₂v₂)/(m₁+m₂)
    v₂' = ((m₂-m₁)v₂ + 2m₁v₁)/(m₁+m₂)

    特殊情况：
    - m₁ = m₂: 速度交换（v₁' = v₂, v₂' = v₁）
    - m₂ >> m₁: v₁' ≈ -v₁ + 2v₂（如球撞墙）
    - v₂ = 0: v₁' = (m₁-m₂)v₁/(m₁+m₂)

    参数 Parameters:
        m1, m2: 两粒子的质量 [kg]
        v1, v2: 碰撞前速度 [m/s]
    返回 Returns:
        (v1_final, v2_final): 碰撞后速度 [m/s]
    """
    M = m1 + m2
    v1_final = ((m1 - m2) * v1 + 2 * m2 * v2) / M
    v2_final = ((m2 - m1) * v2 + 2 * m1 * v1) / M
    return v1_final, v2_final

def elastic_collision_cm(m1, v1, m2, v2):
    """
    质心系中的弹性碰撞 Elastic Collision in CM Frame

    质心系的优势：
    - 动量守恒自动满足（质心系总动量 = 0）
    - 弹性碰撞只是速度方向反转，大小不变
    - 分析更加简洁

    步骤：
    1. 变换到质心系
    2. 速度反向（大小不变）
    3. 变换回实验室系
    """
    mu = reduced_mass(m1, m2)
    M = total_mass(m1, m2)

    v_cm = (m1 * v1 + m2 * v2) / M  # 质心速度
    v1_cm = v1 - v_cm  # 质心系中粒子1的速度
    v2_cm = v2 - v_cm  # 质心系中粒子2的速度

    # 弹性碰撞: 质心系中速度反转
    v1_cm_final = -v1_cm
    v2_cm_final = -v2_cm

    # 转回实验室系（加上质心速度）
    v1_final = v1_cm_final + v_cm
    v2_final = v2_cm_final + v_cm

    return v1_final, v2_final


# =============================================================================
# 练习 13.5: 非弹性碰撞
# Exercise 13.5: Inelastic Collision
# =============================================================================
# 非弹性碰撞：动量守恒，但动能有损失
# 恢复系数e衡量碰撞的"弹性程度"

def inelastic_collision(m1, v1, m2, v2, e=0):
    """
    非弹性碰撞 Inelastic Collision

    恢复系数定义: e = (v₂' - v₁')/(v₁ - v₂)
    - e = 1: 完全弹性（无能量损失）
    - e = 0: 完全非弹性（两物体粘连）
    - 0 < e < 1: 部分弹性（有能量损失）

    碰撞后速度:
    v₁' = v_cm - m₂·e·v_rel/M
    v₂' = v_cm + m₁·e·v_rel/M

    参数 Parameters:
        m1, m2: 质量 [kg]
        v1, v2: 碰撞前速度 [m/s]
        e: 恢复系数（默认0表示完全非弹性）
    返回 Returns:
        (v1_final, v2_final): 碰撞后速度 [m/s]
    """
    M = m1 + m2
    v_cm = (m1 * v1 + m2 * v2) / M  # 质心速度（守恒）

    # 相对速度
    v_rel = v1 - v2

    # 使用恢复系数计算碰撞后速度
    v1_final = v_cm - m2 * e * v_rel / M
    v2_final = v_cm + m1 * e * v_rel / M

    return v1_final, v2_final

def energy_loss(m1, v1, m2, v2, e):
    """
    碰撞能量损失 Energy Loss in Collision

    ΔK = (1/2)μv_rel²(1-e²)

    物理意义：
    - 只有相对运动动能可能损失（质心动能守恒）
    - e=1时无损失，e=0时损失最大
    - 损失的能量转化为热能、声音、形变等

    参数 Parameters:
        m1, m2: 质量 [kg]
        v1, v2: 碰撞前速度 [m/s]
        e: 恢复系数
    返回 Returns:
        能量损失 [J]
    """
    mu = reduced_mass(m1, m2)
    v_rel = v1 - v2
    return 0.5 * mu * v_rel**2 * (1 - e**2)


# =============================================================================
# 练习 13.6: 散射角
# Exercise 13.6: Scattering Angle
# =============================================================================
def scattering_angle_cm(m1, m2, theta_lab):
    """
    实验室系到质心系的散射角转换
    对于静止靶(m2):
    tan(θ_lab) = sin(θ_cm)/(cos(θ_cm) + m1/m2)
    """
    # 逆求解较复杂，这里提供简化版
    ratio = m1 / m2
    if ratio >= 1:
        return theta_lab * 2  # 近似
    return theta_lab

def impact_parameter(b, m1, m2, v_rel, potential='hard_sphere', R=1):
    """
    给定冲击参数的散射角
    """
    if potential == 'hard_sphere':
        if b > R:
            return 0  # 无散射
        return np.pi - 2 * np.arcsin(b / R)
    return 0


# =============================================================================
# 可视化
# =============================================================================
def plot_two_body():
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # 1. 二体轨道
    ax1 = axes[0, 0]
    m1 = 1e30
    m2 = 0.5e30
    # 初始条件
    r0 = 1e11
    v0 = np.sqrt(G * (m1 + m2) / r0) * 0.8

    state0 = [0, 0, 0, 0, r0, 0, 0, v0]
    t = np.linspace(0, orbital_period_two_body(m1, m2, r0) * 2, 1000)

    sol = odeint(two_body_equations, state0, t, args=(m1, m2))

    ax1.plot(sol[:, 0]/1e11, sol[:, 1]/1e11, 'b-', label='m₁', linewidth=2)
    ax1.plot(sol[:, 4]/1e11, sol[:, 5]/1e11, 'r-', label='m₂', linewidth=2)

    # 质心
    R_x = (m1*sol[:, 0] + m2*sol[:, 4]) / (m1 + m2)
    R_y = (m1*sol[:, 1] + m2*sol[:, 5]) / (m1 + m2)
    ax1.scatter(R_x[::100]/1e11, R_y[::100]/1e11, c='green', s=10, label='质心')

    ax1.set_xlabel('x (×10¹¹ m)')
    ax1.set_ylabel('y (×10¹¹ m)')
    ax1.set_title('二体引力轨道')
    ax1.legend()
    ax1.axis('equal')
    ax1.grid(True, alpha=0.3)

    # 2. 弹性碰撞
    ax2 = axes[0, 1]
    m1, m2 = 1, 2
    v1_initial = np.linspace(-2, 2, 100)
    v2_initial = 0

    v1_finals = []
    v2_finals = []
    for v1 in v1_initial:
        v1f, v2f = elastic_collision_1d(m1, v1, m2, v2_initial)
        v1_finals.append(v1f)
        v2_finals.append(v2f)

    ax2.plot(v1_initial, v1_finals, 'b-', label='v₁\'', linewidth=2)
    ax2.plot(v1_initial, v2_finals, 'r-', label='v₂\'', linewidth=2)
    ax2.plot(v1_initial, v1_initial, 'k--', alpha=0.3, label='v₁ (初始)')
    ax2.set_xlabel('v₁ (初始)')
    ax2.set_ylabel('v (末态)')
    ax2.set_title(f'弹性碰撞 (m₁={m1}, m₂={m2})')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 恢复系数
    ax3 = axes[1, 0]
    e_values = np.linspace(0, 1, 100)
    m1, m2 = 1, 1
    v1, v2 = 2, 0

    energy_losses = [energy_loss(m1, v1, m2, v2, e) for e in e_values]
    initial_energy = 0.5 * m1 * v1**2

    ax3.plot(e_values, np.array(energy_losses)/initial_energy * 100, 'g-', linewidth=2)
    ax3.set_xlabel('恢复系数 e')
    ax3.set_ylabel('能量损失 (%)')
    ax3.set_title('非弹性碰撞能量损失')
    ax3.grid(True, alpha=0.3)

    # 4. 约化质量
    ax4 = axes[1, 1]
    m1 = 1
    m2_range = np.linspace(0.1, 10, 100)
    mu = [reduced_mass(m1, m2) for m2 in m2_range]

    ax4.plot(m2_range, mu, 'b-', linewidth=2)
    ax4.axhline(y=m1, color='r', linestyle='--', alpha=0.5, label='m₁')
    ax4.axhline(y=m1/2, color='g', linestyle='--', alpha=0.5, label='m₁/2')
    ax4.set_xlabel('m₂/m₁')
    ax4.set_ylabel('μ/m₁')
    ax4.set_title('约化质量')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('two_body.png', dpi=150)
    print("图像已保存为 two_body.png")
    plt.show()


def verify():
    all_passed = True

    # Check 13.1
    mu = reduced_mass(1, 1)
    if not np.isclose(mu, 0.5, rtol=0.01):
        print("❌ 13.1 约化质量错误")
        all_passed = False
    else:
        print(f"✓ 13.1 约化质量正确 (μ(1,1) = {mu})")

    # Check 13.2
    R = center_of_mass(1, np.array([0, 0]), 1, np.array([2, 0]))
    if not np.allclose(R, [1, 0], rtol=0.01):
        print("❌ 13.2 质心位置错误")
        all_passed = False
    else:
        print("✓ 13.2 质心坐标正确")

    # Check 13.3
    T = orbital_period_two_body(1e30, 1e30, 1e11)
    if T <= 0:
        print("❌ 13.3 轨道周期错误")
        all_passed = False
    else:
        print(f"✓ 13.3 二体轨道正确")

    # Check 13.4
    v1f, v2f = elastic_collision_1d(1, 2, 1, 0)
    # 等质量情况下速度交换
    if not np.isclose(v1f, 0, atol=0.01) or not np.isclose(v2f, 2, rtol=0.01):
        print("❌ 13.4 弹性碰撞错误")
        all_passed = False
    else:
        print("✓ 13.4 弹性碰撞正确（等质量速度交换）")

    # Check 13.5
    v1f, v2f = inelastic_collision(1, 2, 1, 0, e=0)
    v_cm = 1  # (1*2 + 1*0)/2
    if not np.isclose(v1f, v_cm, rtol=0.01) or not np.isclose(v2f, v_cm, rtol=0.01):
        print("❌ 13.5 完全非弹性碰撞错误")
        all_passed = False
    else:
        print("✓ 13.5 非弹性碰撞正确")

    # Check 13.6
    dE = energy_loss(1, 2, 1, 0, e=0)
    expected_dE = 0.5 * 0.5 * 4  # μ=0.5, v_rel=2
    if not np.isclose(dE, expected_dE, rtol=0.01):
        print("❌ 13.6 能量损失计算错误")
        all_passed = False
    else:
        print(f"✓ 13.6 能量损失正确 (ΔK = {dE})")

    if all_passed:
        print("\n🎉 所有测试通过！")
        try:
            plot_two_body()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("二体问题 Two-Body Problem")
    print("=" * 50)
    verify()
