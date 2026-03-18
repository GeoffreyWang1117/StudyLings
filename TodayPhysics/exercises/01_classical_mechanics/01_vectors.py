"""
向量基础 Vector Basics
难度 Difficulty: ★

================================================================================
学习目标 Learning Objectives
================================================================================
- 理解向量的表示和基本运算（加法、减法、数乘）
  Understand vector representation and basic operations (addition, subtraction, scalar multiplication)
- 掌握点积和叉积的物理意义及计算方法
  Master the physical meaning and calculation of dot product and cross product
- 使用 NumPy 进行高效的向量计算
  Use NumPy for efficient vector calculations

================================================================================
物理背景 Physical Background
================================================================================
向量是物理学中描述具有大小和方向的量的基本工具。在力学中，力、速度、
加速度、位移等都是向量。掌握向量运算是学习物理学的基础。

Vectors are fundamental tools in physics for describing quantities with both
magnitude and direction. In mechanics, force, velocity, acceleration, and
displacement are all vectors.

核心公式 Key Formulas:
- 向量模长 Magnitude: |a| = sqrt(a_x² + a_y² + a_z²)
- 单位向量 Unit vector: â = a / |a|
- 点积 Dot product: a·b = |a||b|cos(θ) = a_x*b_x + a_y*b_y + a_z*b_z
- 叉积 Cross product: |a×b| = |a||b|sin(θ)，方向由右手定则确定
- 功 Work: W = F·d（力与位移的点积）
- 力矩 Torque: τ = r×F（位置向量与力的叉积）

HINT: 向量点积 a·b = |a||b|cos(θ)，结果是标量
HINT: 向量叉积 a×b 的模等于 |a||b|sin(θ)，结果是向量
"""

import numpy as np
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.physics_helpers import magnitude, unit_vector, angle_between

# I AM NOT DONE

# =============================================================================
# 练习 1.1: 向量加法
# Exercise 1.1: Vector Addition
# =============================================================================
# 物理背景 Physical Background:
# 当多个力同时作用于一个物体时，它们的效果等效于一个合力。
# 合力等于各分力的向量和。这是力的叠加原理的体现。
#
# 题目 Problem:
# 力 F1 = (3, 4) N，力 F2 = (-1, 2) N
# Force F1 = (3, 4) N, Force F2 = (-1, 2) N
# 计算合力 F_total = F1 + F2
# Calculate the resultant force F_total = F1 + F2
#
# 公式 Formula: F_total = F1 + F2 (向量加法，对应分量相加)
# 单位 Unit: 牛顿 (N)

F1 = np.array([3.0, 4.0])  # 力向量1，单位：N
F2 = np.array([-1.0, 2.0])  # 力向量2，单位：N

# TODO: 计算合力 F_total
# 提示：使用 NumPy 的向量加法，直接用 + 运算符
F_total = None  # 修改这里


# =============================================================================
# 练习 1.2: 向量模长
# Exercise 1.2: Vector Magnitude
# =============================================================================
# 物理背景 Physical Background:
# 向量的模长表示向量的大小。对于位移向量，模长就是两点间的直线距离。
# 对于速度向量，模长就是速率。
#
# 题目 Problem:
# 计算位移向量 r = (3, 4, 12) 的模长（距离）
# Calculate the magnitude of displacement vector r = (3, 4, 12)
#
# 公式 Formula: |r| = sqrt(x² + y² + z²)
# 单位 Unit: 米 (m)

r = np.array([3.0, 4.0, 12.0])  # 位移向量，单位：m

# TODO: 计算 r 的模长
# 提示：使用 np.linalg.norm(r) 或 np.sqrt(np.sum(r**2))
r_magnitude = None  # 修改这里


# =============================================================================
# 练习 1.3: 单位向量
# Exercise 1.3: Unit Vector
# =============================================================================
# 物理背景 Physical Background:
# 单位向量是模长为1的向量，仅表示方向。在物理中常用来表示某个物理量的方向。
# 例如，运动方向、力的方向等。
#
# 题目 Problem:
# 求速度向量 v = (6, 8) m/s 的方向（单位向量）
# Find the direction (unit vector) of velocity v = (6, 8) m/s
#
# 公式 Formula: v_hat = v / |v|（向量除以其模长）
# 单位 Unit: 无量纲（纯方向）

v = np.array([6.0, 8.0])  # 速度向量，单位：m/s

# TODO: 计算 v 的单位向量
# 提示：先计算模长，再用向量除以模长
v_unit = None  # 修改这里


# =============================================================================
# 练习 1.4: 点积 - 计算功
# Exercise 1.4: Dot Product - Calculate Work
# =============================================================================
# 物理背景 Physical Background:
# 功是力在位移方向上的分量与位移大小的乘积。当力与位移方向一致时，
# 功为正（正功）；当力与位移方向相反时，功为负（负功）；
# 当力与位移垂直时，功为零。
#
# 点积的几何意义：a·b = |a||b|cos(θ)
# 物理意义：表示一个向量在另一个向量方向上的投影乘以另一个向量的模长
#
# 题目 Problem:
# 力 F = (5, 3) N 作用下物体位移 d = (4, 0) m
# Force F = (5, 3) N, displacement d = (4, 0) m
# 计算功 W = F · d
# Calculate work W = F · d
#
# 公式 Formula: W = F·d = Fx*dx + Fy*dy
# 单位 Unit: 焦耳 (J) = N·m

F = np.array([5.0, 3.0])  # 力向量，单位：N
d = np.array([4.0, 0.0])  # 位移向量，单位：m

# TODO: 使用点积计算功 W
# 提示：使用 np.dot(F, d) 或 F @ d
W = None  # 修改这里


# =============================================================================
# 练习 1.5: 叉积 - 计算力矩
# Exercise 1.5: Cross Product - Calculate Torque
# =============================================================================
# 物理背景 Physical Background:
# 力矩（转矩）描述力使物体绕某点或某轴旋转的能力。力矩等于位置向量与力的叉积。
# 力矩的方向由右手定则确定：四指从 r 转向 F，大拇指指向即为 τ 的方向。
#
# 叉积的几何意义：|a×b| = |a||b|sin(θ)
# 结果是一个向量，垂直于 a 和 b 构成的平面
#
# 题目 Problem:
# 位置向量 r = (2, 0, 0) m，力 F = (0, 5, 0) N
# Position vector r = (2, 0, 0) m, Force F = (0, 5, 0) N
# 计算力矩 τ = r × F
# Calculate torque τ = r × F
#
# 公式 Formula: τ = r × F（叉积）
# 单位 Unit: 牛顿·米 (N·m)

r_pos = np.array([2.0, 0.0, 0.0])  # 位置向量（从转轴到力作用点），单位：m
F_force = np.array([0.0, 5.0, 0.0])  # 力向量，单位：N

# TODO: 使用叉积计算力矩 τ
# 提示：使用 np.cross(r_pos, F_force)
tau = None  # 修改这里


# =============================================================================
# 练习 1.6: 向量夹角
# Exercise 1.6: Angle Between Vectors
# =============================================================================
# 物理背景 Physical Background:
# 两个向量之间的夹角在物理中经常用到，例如计算功时需要知道力与位移的夹角，
# 分析碰撞时需要知道入射角和反射角等。
#
# 利用点积公式：a·b = |a||b|cos(θ)
# 可以反解出夹角：θ = arccos(a·b / (|a||b|))
#
# 题目 Problem:
# 计算向量 a = (1, 0) 和 b = (1, 1) 之间的夹角（弧度）
# Calculate the angle between a = (1, 0) and b = (1, 1) in radians
#
# 公式 Formula: θ = arccos(a·b / (|a||b|))
# 单位 Unit: 弧度 (rad)

a = np.array([1.0, 0.0])
b = np.array([1.0, 1.0])

# TODO: 计算夹角 theta（弧度）
# 提示：先计算点积和两个向量的模长，然后用 np.arccos()
# 或者直接使用 angle_between 辅助函数
theta = None  # 修改这里


# =============================================================================
# 验证函数 Verification Function - 不要修改 Do not modify
# =============================================================================
def verify():
    """
    验证所有练习的答案是否正确
    Verify all exercises
    """
    all_passed = True

    # 检查 1.1: 向量加法
    # Check 1.1: Vector Addition
    expected_F_total = np.array([2.0, 6.0])
    if F_total is None or not np.allclose(F_total, expected_F_total):
        print("❌ 1.1 向量加法错误 Vector addition incorrect")
        print(f"   期望 Expected: {expected_F_total}, 得到 Got: {F_total}")
        all_passed = False
    else:
        print("✓ 1.1 向量加法正确 Vector addition correct")

    # 检查 1.2: 向量模长
    # Check 1.2: Vector Magnitude
    if r_magnitude is None or not np.isclose(r_magnitude, 13.0):
        print("❌ 1.2 向量模长错误 Vector magnitude incorrect")
        print(f"   期望 Expected: 13.0 m, 得到 Got: {r_magnitude}")
        all_passed = False
    else:
        print("✓ 1.2 向量模长正确 (|r| = 13.0 m)")

    # 检查 1.3: 单位向量
    # Check 1.3: Unit Vector
    expected_v_unit = np.array([0.6, 0.8])
    if v_unit is None or not np.allclose(v_unit, expected_v_unit):
        print("❌ 1.3 单位向量错误 Unit vector incorrect")
        print(f"   期望 Expected: {expected_v_unit}, 得到 Got: {v_unit}")
        all_passed = False
    else:
        print("✓ 1.3 单位向量正确 Unit vector correct")

    # 检查 1.4: 功的计算
    # Check 1.4: Work Calculation
    if W is None or not np.isclose(W, 20.0):
        print("❌ 1.4 功计算错误 Work calculation incorrect")
        print(f"   期望 Expected: 20.0 J, 得到 Got: {W}")
        all_passed = False
    else:
        print("✓ 1.4 功计算正确 Work correct (W = 20 J)")

    # 检查 1.5: 力矩计算
    # Check 1.5: Torque Calculation
    expected_tau = np.array([0.0, 0.0, 10.0])
    if tau is None or not np.allclose(tau, expected_tau):
        print("❌ 1.5 力矩计算错误 Torque calculation incorrect")
        print(f"   期望 Expected: {expected_tau} N·m, 得到 Got: {tau}")
        all_passed = False
    else:
        print("✓ 1.5 力矩计算正确 Torque correct (τ = 10 N·m, z轴正向)")

    # 检查 1.6: 向量夹角
    # Check 1.6: Angle Between Vectors
    expected_theta = np.pi / 4  # 45度 = π/4 弧度
    if theta is None or not np.isclose(theta, expected_theta):
        print("❌ 1.6 向量夹角错误 Angle calculation incorrect")
        print(f"   期望 Expected: {expected_theta:.4f} rad (45°), 得到 Got: {theta}")
        all_passed = False
    else:
        print("✓ 1.6 向量夹角正确 Angle correct (θ = π/4 rad = 45°)")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("向量基础 Vector Basics")
    print("=" * 50)
    verify()
