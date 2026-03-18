"""
流体力学基础 Fluid Mechanics Basics
难度 Difficulty: ★★★

================================================================================
学习目标 Learning Objectives
================================================================================
- 理解流体静力学和静水压强
  Understand fluid statics and hydrostatic pressure
- 掌握伯努利方程及其应用
  Master Bernoulli's equation and its applications
- 了解粘性流体和雷诺数的概念
  Understand viscous fluids and Reynolds number
- 应用连续性方程解决流动问题
  Apply continuity equation to flow problems

================================================================================
物理背景 Physical Background
================================================================================
流体力学研究液体和气体的运动规律。

1. 流体静力学 Fluid Statics:
   静水压强: P = P₀ + ρgh
   压强随深度线性增加，与容器形状无关

2. 阿基米德原理 Archimedes' Principle:
   浮力 F_b = ρ_fluid × V_displaced × g
   浮力等于排开流体的重量

3. 连续性方程 Continuity Equation:
   对于不可压缩流体: A₁v₁ = A₂v₂
   管道变窄时流速增加

4. 伯努利方程 Bernoulli's Equation:
   P + (1/2)ρv² + ρgh = 常数
   - P: 静压强
   - (1/2)ρv²: 动压强
   - ρgh: 重力势压
   适用条件：理想流体（无粘性）、稳态流动、沿流线

5. 托里拆利定理 Torricelli's Theorem:
   容器底部小孔的出流速度: v = sqrt(2gh)
   是伯努利方程的特例

6. 粘性流动 Viscous Flow:
   - 泊肃叶定律: Q = πR⁴ΔP/(8ηL)
   - 雷诺数 Re = ρvL/η（判断层流/湍流）
   - 斯托克斯阻力: F = 6πηRv

HINT: 伯努利方程: P + (1/2)ρv² + ρgh = 常数（沿流线）
HINT: 连续性方程: A₁v₁ = A₂v₂（体积流量守恒）
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])

# I AM NOT DONE

g = 9.8  # m/s²
rho_water = 1000  # kg/m³

# =============================================================================
# 练习 9.1: 流体静力学
# Exercise 9.1: Fluid Statics
# =============================================================================
# 流体静压强: P = P₀ + ρgh

def pressure_at_depth(P0, rho, h, g=9.8):
    """
    计算深度 h 处的压强
    P = P₀ + ρgh
    """
    # TODO: 计算压强
    P = P0 + rho * g * h
    return P

def buoyant_force(rho_fluid, V_displaced, g=9.8):
    """
    阿基米德浮力
    F_b = ρ_fluid * V * g
    """
    # TODO: 计算浮力
    F_b = rho_fluid * V_displaced * g
    return F_b


# =============================================================================
# 练习 9.2: 连续性方程
# Exercise 9.2: Continuity Equation
# =============================================================================
# 对于不可压缩流体: A₁v₁ = A₂v₂

def flow_velocity(A1, v1, A2):
    """
    由连续性方程计算流速
    v₂ = A₁v₁/A₂
    """
    # TODO: 计算流速
    v2 = A1 * v1 / A2
    return v2

def volume_flow_rate(A, v):
    """
    体积流量 Q = Av
    """
    # TODO: 计算流量
    Q = A * v
    return Q


# =============================================================================
# 练习 9.3: 伯努利方程
# Exercise 9.3: Bernoulli's Equation
# =============================================================================
# P₁ + (1/2)ρv₁² + ρgh₁ = P₂ + (1/2)ρv₂² + ρgh₂

def bernoulli_pressure(P1, v1, h1, v2, h2, rho, g=9.8):
    """
    用伯努利方程计算 P2
    """
    # TODO: 计算 P2
    P2 = P1 + 0.5 * rho * (v1**2 - v2**2) + rho * g * (h1 - h2)
    return P2

def torricelli_velocity(h, g=9.8):
    """
    托里拆利定理：容器底部小孔的出流速度
    v = √(2gh)
    """
    # TODO: 计算出流速度
    v = np.sqrt(2 * g * h)
    return v


# =============================================================================
# 练习 9.4: 文丘里管
# Exercise 9.4: Venturi Tube
# =============================================================================
# 文丘里管用于测量流速

def venturi_velocity(A1, A2, delta_P, rho):
    """
    通过压差计算文丘里管流速
    v₁ = √(2ΔP / (ρ((A₁/A₂)² - 1)))
    """
    # TODO: 计算流速
    v1 = np.sqrt(2 * delta_P / (rho * ((A1/A2)**2 - 1)))
    return v1


# =============================================================================
# 练习 9.5: 粘性流体
# Exercise 9.5: Viscous Flow
# =============================================================================
# 泊肃叶定律（圆管层流）: Q = πR⁴ΔP / (8ηL)
# η: 动力粘度

def poiseuille_flow(R, delta_P, eta, L):
    """
    泊肃叶流量公式
    Q = πR⁴ΔP / (8ηL)
    """
    # TODO: 计算流量
    Q = np.pi * R**4 * delta_P / (8 * eta * L)
    return Q

def reynolds_number(rho, v, L, eta):
    """
    雷诺数 Re = ρvL/η
    Re < 2300: 层流
    Re > 4000: 湍流
    """
    # TODO: 计算雷诺数
    Re = rho * v * L / eta
    return Re


# =============================================================================
# 练习 9.6: 斯托克斯阻力
# Exercise 9.6: Stokes Drag
# =============================================================================
# 小球在粘性流体中的阻力: F = 6πηRv

def stokes_drag(eta, R, v):
    """
    斯托克斯阻力
    F = 6πηRv
    """
    # TODO: 计算阻力
    F = 6 * np.pi * eta * R * v
    return F

def terminal_velocity_sphere(rho_sphere, rho_fluid, R, eta, g=9.8):
    """
    小球在流体中的终端速度
    v_t = 2R²g(ρ_sphere - ρ_fluid) / (9η)
    """
    # TODO: 计算终端速度
    v_t = 2 * R**2 * g * (rho_sphere - rho_fluid) / (9 * eta)
    return v_t


# =============================================================================
# 验证函数
# =============================================================================
def verify():
    all_passed = True

    # Check 9.1
    P_atm = 101325  # Pa
    P_10m = pressure_at_depth(P_atm, rho_water, 10)
    if not np.isclose(P_10m, P_atm + rho_water * g * 10, rtol=0.01):
        print("❌ 9.1 流体静压强错误")
        all_passed = False
    else:
        print(f"✓ 9.1 流体静压强正确 (水下10m: P = {P_10m/1e3:.1f} kPa)")

    # Check 9.2
    v2 = flow_velocity(1e-2, 2.0, 0.5e-2)
    if not np.isclose(v2, 4.0, rtol=0.01):
        print("❌ 9.2 连续性方程错误")
        all_passed = False
    else:
        print(f"✓ 9.2 连续性方程正确 (面积减半，流速加倍)")

    # Check 9.3
    v_torr = torricelli_velocity(5.0)
    expected = np.sqrt(2 * 9.8 * 5)
    if not np.isclose(v_torr, expected, rtol=0.01):
        print("❌ 9.3 托里拆利定理错误")
        all_passed = False
    else:
        print(f"✓ 9.3 伯努利方程正确 (h=5m出流: v = {v_torr:.2f} m/s)")

    # Check 9.5
    Re = reynolds_number(1000, 1.0, 0.1, 0.001)
    if not np.isclose(Re, 1e5, rtol=0.01):
        print("❌ 9.5 雷诺数错误")
        all_passed = False
    else:
        print(f"✓ 9.5 粘性流体正确 (Re = {Re:.0f})")

    # Check 9.6
    # 水中小球 (ρ=2500 kg/m³, R=1mm, η=0.001 Pa·s)
    v_t = terminal_velocity_sphere(2500, 1000, 0.001, 0.001)
    if v_t <= 0:
        print("❌ 9.6 终端速度错误")
        all_passed = False
    else:
        print(f"✓ 9.6 斯托克斯阻力正确 (终端速度: {v_t:.4f} m/s)")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("流体力学基础 Fluid Mechanics")
    print("=" * 50)
    verify()
