"""
刚体力学 Rigid Body Mechanics
难度 Difficulty: ★★★★

================================================================================
学习目标 Learning Objectives
================================================================================
- 理解转动惯量和角动量的概念
  Understand the concepts of moment of inertia and angular momentum
- 掌握刚体定轴转动定律（转动版牛顿第二定律）
  Master the rotational dynamics of rigid bodies
- 分析滚动运动和角动量守恒
  Analyze rolling motion and conservation of angular momentum
- 应用平行轴定理计算转动惯量
  Apply the parallel axis theorem to calculate moment of inertia

================================================================================
物理背景 Physical Background
================================================================================
刚体力学研究不可形变物体的运动，是质点力学的推广。

1. 转动惯量 Moment of Inertia:
   I = Σmᵢrᵢ²（离散质点）或 I = ∫r²dm（连续体）
   - 衡量物体抵抗角加速度的能力
   - 不同形状有不同的转动惯量公式
   - 依赖于转轴位置

2. 常见形状的转动惯量（绕质心轴）:
   - 细棒绕中心: I = (1/12)ML²
   - 圆盘/实心圆柱: I = (1/2)MR²
   - 实心球体: I = (2/5)MR²
   - 圆环/空心圆柱: I = MR²

3. 平行轴定理 Parallel Axis Theorem:
   I = I_cm + Md²
   其中 d 是平行轴到质心轴的距离

4. 转动定律 Rotational Dynamics:
   τ = Iα（力矩 = 转动惯量 × 角加速度）
   类比 F = ma

5. 角动量守恒 Conservation of Angular Momentum:
   当外力矩为零时，L = Iω = 常数
   经典例子：滑冰运动员收手加速旋转

6. 滚动运动 Rolling Motion:
   纯滚动条件: v = ωR
   总动能: K = (1/2)Mv² + (1/2)Iω² = (1/2)(M + I/R²)v²

HINT: 转动惯量 I = Σmr²，是质量分布相对于转轴的度量
HINT: 角动量 L = Iω
HINT: 转动动能 K = (1/2)Iω²
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])

# I AM NOT DONE

# =============================================================================
# 练习 7.1: 转动惯量计算
# Exercise 7.1: Moment of Inertia
# =============================================================================
# 不同形状的转动惯量（绕质心轴）:
# 细棒(绕中心): I = (1/12)ML²
# 圆盘/圆柱: I = (1/2)MR²
# 球体: I = (2/5)MR²
# 圆环: I = MR²

def moment_of_inertia_rod(M, L):
    """细棒绕中心轴转动惯量"""
    # TODO: 计算转动惯量
    I = (1/12) * M * L**2
    return I

def moment_of_inertia_disk(M, R):
    """圆盘/实心圆柱绕中心轴转动惯量"""
    # TODO: 计算转动惯量
    I = (1/2) * M * R**2
    return I

def moment_of_inertia_sphere(M, R):
    """实心球体绕直径转动惯量"""
    # TODO: 计算转动惯量
    I = (2/5) * M * R**2
    return I

def moment_of_inertia_ring(M, R):
    """圆环绕中心轴转动惯量"""
    # TODO: 计算转动惯量
    I = M * R**2
    return I


# =============================================================================
# 练习 7.2: 平行轴定理
# Exercise 7.2: Parallel Axis Theorem
# =============================================================================
# I = I_cm + Md²
# I_cm: 绕质心轴的转动惯量, d: 平行轴到质心的距离

def parallel_axis_theorem(I_cm, M, d):
    """
    平行轴定理
    I = I_cm + Md²
    """
    # TODO: 计算平行轴转动惯量
    I = I_cm + M * d**2
    return I

# 例子: 细棒绕端点转动
M_rod = 2.0  # kg
L_rod = 1.0  # m
I_rod_center = moment_of_inertia_rod(M_rod, L_rod)
I_rod_end = parallel_axis_theorem(I_rod_center, M_rod, L_rod/2)


# =============================================================================
# 练习 7.3: 转动定律
# Exercise 7.3: Rotational Dynamics
# =============================================================================
# τ = Iα (力矩 = 转动惯量 × 角加速度)
# 类比 F = ma

def angular_acceleration(torque, I):
    """
    从力矩计算角加速度
    α = τ/I
    """
    # TODO: 计算角加速度
    alpha = torque / I
    return alpha

def torque_from_force(F, r, theta=np.pi/2):
    """
    力矩 τ = r × F = rF sin(θ)
    theta: 力与位置向量的夹角
    """
    # TODO: 计算力矩
    tau = r * F * np.sin(theta)
    return tau


# =============================================================================
# 练习 7.4: 角动量守恒
# Exercise 7.4: Conservation of Angular Momentum
# =============================================================================
# L = Iω = 常数 (无外力矩时)
# I₁ω₁ = I₂ω₂

def final_angular_velocity(I1, omega1, I2):
    """
    角动量守恒：计算转动惯量改变后的角速度
    I₁ω₁ = I₂ω₂
    """
    # TODO: 计算最终角速度
    omega2 = I1 * omega1 / I2
    return omega2

# 例子: 滑冰运动员收手
I_arms_out = 4.0  # kg·m² (手臂伸展)
I_arms_in = 1.0   # kg·m² (手臂收紧)
omega_initial = 2.0  # rad/s
omega_final = final_angular_velocity(I_arms_out, omega_initial, I_arms_in)


# =============================================================================
# 练习 7.5: 滚动运动
# Exercise 7.5: Rolling Motion
# =============================================================================
# 纯滚动条件: v = ωR
# 滚动动能: K = (1/2)Mv² + (1/2)Iω² = (1/2)(M + I/R²)v²

def rolling_kinetic_energy(M, v, I, R):
    """
    计算滚动物体的总动能
    K = (1/2)Mv² + (1/2)Iω²
    """
    omega = v / R
    # TODO: 计算总动能
    K_trans = 0.5 * M * v**2
    K_rot = 0.5 * I * omega**2
    K_total = K_trans + K_rot
    return K_total

def rolling_down_incline(M, R, I, h, g=9.8):
    """
    物体从高度h处沿斜面无滑滚下，求底部速度
    Mgh = (1/2)Mv² + (1/2)Iω² = (1/2)(M + I/R²)v²
    v = √(2gh / (1 + I/(MR²)))
    """
    # TODO: 计算底部速度
    v = np.sqrt(2 * g * h / (1 + I / (M * R**2)))
    return v


# =============================================================================
# 练习 7.6: 物理摆
# Exercise 7.6: Physical Pendulum
# =============================================================================
# 物理摆周期: T = 2π√(I/(Mgh))
# I: 绕悬挂点的转动惯量, h: 质心到悬挂点的距离

def physical_pendulum_period(I, M, h, g=9.8):
    """
    物理摆周期
    T = 2π√(I/(Mgh))
    """
    # TODO: 计算周期
    T = 2 * np.pi * np.sqrt(I / (M * g * h))
    return T


# =============================================================================
# 验证函数
# =============================================================================
def verify():
    all_passed = True

    # Check 7.1
    I_test = moment_of_inertia_disk(2.0, 0.5)
    if not np.isclose(I_test, 0.25, rtol=0.01):
        print("❌ 7.1 转动惯量错误")
        all_passed = False
    else:
        print(f"✓ 7.1 转动惯量正确 (圆盘: I = {I_test} kg·m²)")

    # Check 7.2
    if not np.isclose(I_rod_end, M_rod * L_rod**2 / 3, rtol=0.01):
        print("❌ 7.2 平行轴定理错误")
        all_passed = False
    else:
        print(f"✓ 7.2 平行轴定理正确 (棒绕端点: I = {I_rod_end:.4f} kg·m²)")

    # Check 7.3
    alpha = angular_acceleration(10.0, 2.0)
    if not np.isclose(alpha, 5.0, rtol=0.01):
        print("❌ 7.3 角加速度计算错误")
        all_passed = False
    else:
        print(f"✓ 7.3 转动定律正确")

    # Check 7.4
    if not np.isclose(omega_final, 8.0, rtol=0.01):
        print("❌ 7.4 角动量守恒错误")
        all_passed = False
    else:
        print(f"✓ 7.4 角动量守恒正确 (ω: {omega_initial} -> {omega_final} rad/s)")

    # Check 7.5
    v_sphere = rolling_down_incline(1.0, 0.1, 2/5 * 1.0 * 0.1**2, 1.0)
    v_expected = np.sqrt(2 * 9.8 * 1.0 / (1 + 2/5))
    if not np.isclose(v_sphere, v_expected, rtol=0.01):
        print("❌ 7.5 滚动运动错误")
        all_passed = False
    else:
        print(f"✓ 7.5 滚动运动正确 (球体滚下1m: v = {v_sphere:.2f} m/s)")

    # Check 7.6
    T_phys = physical_pendulum_period(I_rod_end, M_rod, L_rod/2)
    T_expected = 2 * np.pi * np.sqrt(I_rod_end / (M_rod * 9.8 * L_rod/2))
    if not np.isclose(T_phys, T_expected, rtol=0.01):
        print("❌ 7.6 物理摆错误")
        all_passed = False
    else:
        print(f"✓ 7.6 物理摆正确 (T = {T_phys:.3f} s)")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("刚体力学 Rigid Body Mechanics")
    print("=" * 50)
    verify()
