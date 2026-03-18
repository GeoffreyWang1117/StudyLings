"""
牛顿运动定律 Newton's Laws of Motion
难度 Difficulty: ★★

================================================================================
学习目标 Learning Objectives
================================================================================
- 应用牛顿第一、第二、第三定律解决力学问题
  Apply Newton's First, Second, and Third Laws to solve mechanics problems
- 理解力、质量、加速度之间的定量关系
  Understand the quantitative relationship between force, mass, and acceleration
- 处理多个力的合成与分解问题
  Handle problems involving composition and resolution of multiple forces

================================================================================
物理背景 Physical Background
================================================================================
牛顿三大运动定律是经典力学的基石：

1. 牛顿第一定律（惯性定律）Newton's First Law (Law of Inertia):
   物体在没有外力作用时，保持静止或匀速直线运动状态。
   An object at rest stays at rest; an object in motion stays in uniform motion.

2. 牛顿第二定律 Newton's Second Law:
   F = ma，合外力等于质量乘以加速度。
   The net force equals mass times acceleration.
   这是力学问题求解的核心方程。

3. 牛顿第三定律（作用与反作用）Newton's Third Law:
   作用力与反作用力大小相等、方向相反、作用在不同物体上。
   For every action, there is an equal and opposite reaction.

核心公式 Key Formulas:
- 牛顿第二定律: F = ma，或 a = F/m
- 斜面分力: F_parallel = mg·sin(θ), F_normal = mg·cos(θ)
- 摩擦力: f = μN（N为法向力）
- 向心力: F_c = mv²/r = mω²r

HINT: F = ma 是牛顿第二定律的核心
HINT: 力的分解要考虑坐标系选择，通常选择沿运动方向和垂直方向
"""

import numpy as np
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])

# I AM NOT DONE

# =============================================================================
# 练习 2.1: 牛顿第二定律
# Exercise 2.1: Newton's Second Law
# =============================================================================
# 物理背景 Physical Background:
# 牛顿第二定律是经典力学最重要的定律，它建立了力与运动的定量关系。
# 当物体受到合外力作用时，会产生与力成正比、与质量成反比的加速度。
#
# 题目 Problem:
# 一个质量 m = 5 kg 的物体受到力 F = 20 N
# A mass of 5 kg experiences a force of 20 N
# 计算物体的加速度
# Calculate the acceleration of the object
#
# 公式 Formula: a = F / m
# 单位 Unit: 米每二次方秒 (m/s²)

m1 = 5.0  # 质量 mass，单位：kg
F1 = 20.0  # 力 force，单位：N

# TODO: 计算加速度 a1
# 提示：直接应用公式 a = F / m
a1 = None  # 修改这里 (单位: m/s²)


# =============================================================================
# 练习 2.2: 斜面上的物体
# Exercise 2.2: Object on an Inclined Plane
# =============================================================================
# 物理背景 Physical Background:
# 斜面问题是力学中的经典问题。需要将重力分解为平行于斜面和垂直于斜面的两个分量。
# 对于光滑（无摩擦）斜面，物体沿斜面方向只受重力的平行分量作用。
#
# 力的分解 Force decomposition:
# - 平行于斜面（下滑方向）: F_parallel = mg·sin(θ)
# - 垂直于斜面（被斜面支持力平衡）: F_normal = mg·cos(θ)
#
# 题目 Problem:
# 一个质量 m = 2 kg 的物体放在倾角 θ = 30° 的光滑斜面上
# A mass of 2 kg is placed on a frictionless inclined plane at 30°
# 计算物体沿斜面下滑的加速度
# Calculate the acceleration along the incline
#
# 公式 Formula: a = g·sin(θ)（沿斜面方向，质量约去）
# 单位 Unit: m/s²

m2 = 2.0  # 质量 mass，单位：kg
theta = np.radians(30)  # 斜面倾角，30度转换为弧度
g = 9.8  # 重力加速度，单位：m/s²

# TODO: 计算沿斜面方向的加速度 a2
# 提示：由 ma = mg·sin(θ)，得 a = g·sin(θ)
a2 = None  # 修改这里


# =============================================================================
# 练习 2.3: 多力作用
# Exercise 2.3: Multiple Forces
# =============================================================================
# 物理背景 Physical Background:
# 当物体同时受到多个力作用时，根据力的叠加原理，可以先求合力，
# 再用牛顿第二定律求加速度。合力是各分力的向量和。
#
# 题目 Problem:
# 一个质量 m = 3 kg 的物体同时受到三个力:
# A mass of 3 kg experiences three forces simultaneously:
# F1 = (4, 3) N, F2 = (2, -1) N, F3 = (-3, 2) N
# 计算合力和加速度向量
# Calculate the net force and acceleration vector
#
# 公式 Formula:
# F_net = F1 + F2 + F3（向量和）
# a = F_net / m（牛顿第二定律的向量形式）
# 单位 Unit: 合力-牛顿(N)，加速度-m/s²

m3 = 3.0  # 质量 mass，单位：kg
F_1 = np.array([4.0, 3.0])   # 力1，单位：N
F_2 = np.array([2.0, -1.0])  # 力2，单位：N
F_3 = np.array([-3.0, 2.0])  # 力3，单位：N

# TODO: 计算合力 F_net 和加速度向量 a3
# 提示：先将三个力向量相加得到合力，再除以质量得到加速度
F_net = None  # 修改这里
a3 = None  # 修改这里


# =============================================================================
# 练习 2.4: 连接体问题 - Atwood 机
# Exercise 2.4: Connected Bodies - Atwood Machine
# =============================================================================
# 物理背景 Physical Background:
# Atwood机是经典的连接体问题，用于研究牛顿第二定律在连接系统中的应用。
# 两个物体通过轻绳（质量忽略不计）和光滑定滑轮连接，绳子不可伸长，
# 因此两个物体的加速度大小相等。
#
# 受力分析 Force Analysis:
# 对较重物体 m2（下降）: m2*g - T = m2*a  （重力 - 张力 = 质量×加速度）
# 对较轻物体 m1（上升）: T - m1*g = m1*a  （张力 - 重力 = 质量×加速度）
#
# 联立方程解得 Solving simultaneously:
# 加速度: a = (m2-m1)/(m1+m2) * g
# 张力: T = 2*m1*m2/(m1+m2) * g
#
# 题目 Problem:
# 两个质量 m1 = 4 kg 和 m2 = 6 kg 的物体通过轻绳连接，绳子跨过光滑定滑轮
# Two masses (4 kg and 6 kg) connected by a light string over a frictionless pulley
# 计算系统的加速度和绳子的张力
# Calculate the system's acceleration and string tension
#
# 单位 Unit: 加速度-m/s²，张力-N

m_1 = 4.0  # 较轻物体质量 lighter mass，单位：kg
m_2 = 6.0  # 较重物体质量 heavier mass，单位：kg
g = 9.8    # 重力加速度，单位：m/s²

# TODO: 计算加速度 a_atwood 和张力 T
# 提示：使用上面推导的公式
a_atwood = None  # 修改这里
T = None  # 修改这里


# =============================================================================
# 练习 2.5: 摩擦力
# Exercise 2.5: Friction
# =============================================================================
# 物理背景 Physical Background:
# 摩擦力是两个接触面之间阻碍相对运动的力。
# - 静摩擦力：阻止物体开始运动，大小可变，最大值为 f_max = μ_s * N
# - 动摩擦力：物体运动时的摩擦力，大小为 f = μ_k * N
# 其中 N 是法向力（垂直于接触面的支持力），μ 是摩擦系数。
#
# 在水平面上：N = mg（法向力等于重力）
# 净力：F_net = F_push - f
# 加速度：a = F_net / m
#
# 题目 Problem:
# 一个质量 m = 10 kg 的物体放在水平面上，动摩擦系数 μ = 0.3
# A 10 kg mass on a horizontal surface with friction coefficient μ = 0.3
# 施加水平推力 F = 50 N
# A horizontal push force of 50 N is applied
# 计算：1) 摩擦力大小 2) 物体的加速度
# Calculate: 1) friction force 2) acceleration
#
# 公式 Formula:
# 摩擦力: f = μ * N = μ * m * g
# 加速度: a = (F_push - f) / m
# 单位 Unit: 摩擦力-N，加速度-m/s²

m5 = 10.0      # 质量 mass，单位：kg
mu = 0.3       # 动摩擦系数 coefficient of kinetic friction，无量纲
F_push = 50.0  # 推力 push force，单位：N
g = 9.8        # 重力加速度，单位：m/s²

# TODO: 计算摩擦力 f 和加速度 a5
# 提示：先计算摩擦力 f = μ * m * g，再计算净力和加速度
f = None  # 修改这里 (摩擦力，单位：N)
a5 = None  # 修改这里 (加速度，单位：m/s²)


# =============================================================================
# 练习 2.6: 向心力
# Exercise 2.6: Centripetal Force
# =============================================================================
# 物理背景 Physical Background:
# 做圆周运动的物体需要一个指向圆心的力来改变速度方向，这个力叫向心力。
# 向心力不是一种独立的力，而是由其他力（如绳子张力、重力、摩擦力等）提供。
#
# 向心加速度：物体做圆周运动时，速度方向不断改变，产生指向圆心的加速度。
# a_c = v²/r = ω²r（其中 ω 是角速度）
#
# 向心力：由牛顿第二定律，F_c = m * a_c
#
# 题目 Problem:
# 一个质量 m = 0.5 kg 的物体做圆周运动
# A mass of 0.5 kg is in circular motion
# 半径 r = 2 m，速度 v = 4 m/s
# Radius r = 2 m, speed v = 4 m/s
# 计算向心加速度和向心力
# Calculate centripetal acceleration and centripetal force
#
# 公式 Formula:
# 向心加速度: a_c = v² / r
# 向心力: F_c = m * a_c = m * v² / r
# 单位 Unit: 加速度-m/s²，力-N

m6 = 0.5  # 质量 mass，单位：kg
r = 2.0   # 圆周运动半径 radius，单位：m
v = 4.0   # 线速度 linear velocity，单位：m/s

# TODO: 计算向心加速度 a_c 和向心力 F_c
# 提示：a_c = v² / r，F_c = m * a_c
a_c = None  # 修改这里 (单位：m/s²)
F_c = None  # 修改这里 (单位：N)


# =============================================================================
# 验证函数 Verification Function - 不要修改 Do not modify
# =============================================================================
def verify():
    """
    验证所有练习的答案是否正确
    Verify all exercises
    """
    all_passed = True

    # 检查 2.1: 牛顿第二定律
    # Check 2.1: Newton's Second Law
    expected_a1 = 4.0  # F/m = 20/5 = 4
    if a1 is None or not np.isclose(a1, expected_a1):
        print("❌ 2.1 牛顿第二定律错误 Newton's Second Law incorrect")
        print(f"   期望 Expected: {expected_a1} m/s², 得到 Got: {a1}")
        all_passed = False
    else:
        print("✓ 2.1 牛顿第二定律正确 (a = 4 m/s²)")

    # 检查 2.2: 斜面问题
    # Check 2.2: Inclined Plane
    expected_a2 = g * np.sin(theta)  # ≈ 4.9 m/s²
    if a2 is None or not np.isclose(a2, expected_a2, rtol=0.01):
        print("❌ 2.2 斜面问题错误 Inclined plane calculation incorrect")
        print(f"   期望 Expected: {expected_a2:.2f} m/s², 得到 Got: {a2}")
        all_passed = False
    else:
        print(f"✓ 2.2 斜面问题正确 (a = g·sin(30°) = {expected_a2:.2f} m/s²)")

    # 检查 2.3: 多力作用
    # Check 2.3: Multiple Forces
    expected_F_net = np.array([3.0, 4.0])
    expected_a3 = expected_F_net / m3
    if F_net is None or a3 is None:
        print("❌ 2.3 多力作用错误 - 未完成 Multiple forces - incomplete")
        all_passed = False
    elif not np.allclose(F_net, expected_F_net) or not np.allclose(a3, expected_a3):
        print("❌ 2.3 多力作用错误 Multiple forces calculation incorrect")
        print(f"   期望合力 Expected F_net: {expected_F_net} N, 得到 Got: {F_net}")
        print(f"   期望加速度 Expected a: {expected_a3} m/s², 得到 Got: {a3}")
        all_passed = False
    else:
        print(f"✓ 2.3 多力作用正确 (F_net = {F_net} N, a = {a3} m/s²)")

    # 检查 2.4: Atwood机
    # Check 2.4: Atwood Machine
    expected_a_atwood = (m_2 - m_1) / (m_1 + m_2) * g  # = 0.2 * 9.8 = 1.96
    expected_T = 2 * m_1 * m_2 / (m_1 + m_2) * g  # = 47.04
    if a_atwood is None or T is None:
        print("❌ 2.4 Atwood机错误 - 未完成 Atwood machine - incomplete")
        all_passed = False
    elif not np.isclose(a_atwood, expected_a_atwood, rtol=0.01) or not np.isclose(T, expected_T, rtol=0.01):
        print("❌ 2.4 Atwood机错误 Atwood machine calculation incorrect")
        print(f"   期望加速度 Expected a: {expected_a_atwood:.2f} m/s², 得到 Got: {a_atwood}")
        print(f"   期望张力 Expected T: {expected_T:.2f} N, 得到 Got: {T}")
        all_passed = False
    else:
        print(f"✓ 2.4 Atwood机正确 (a = {expected_a_atwood:.2f} m/s², T = {expected_T:.2f} N)")

    # 检查 2.5: 摩擦力
    # Check 2.5: Friction
    expected_f = mu * m5 * g  # = 29.4 N
    expected_a5 = (F_push - expected_f) / m5  # = (50-29.4)/10 = 2.06
    if f is None or a5 is None:
        print("❌ 2.5 摩擦力错误 - 未完成 Friction - incomplete")
        all_passed = False
    elif not np.isclose(f, expected_f, rtol=0.01) or not np.isclose(a5, expected_a5, rtol=0.01):
        print("❌ 2.5 摩擦力错误 Friction calculation incorrect")
        print(f"   期望摩擦力 Expected f: {expected_f:.2f} N, 得到 Got: {f}")
        print(f"   期望加速度 Expected a: {expected_a5:.2f} m/s², 得到 Got: {a5}")
        all_passed = False
    else:
        print(f"✓ 2.5 摩擦力正确 (f = {expected_f:.2f} N, a = {expected_a5:.2f} m/s²)")

    # 检查 2.6: 向心力
    # Check 2.6: Centripetal Force
    expected_a_c = v**2 / r  # = 8 m/s²
    expected_F_c = m6 * expected_a_c  # = 4 N
    if a_c is None or F_c is None:
        print("❌ 2.6 向心力错误 - 未完成 Centripetal force - incomplete")
        all_passed = False
    elif not np.isclose(a_c, expected_a_c) or not np.isclose(F_c, expected_F_c):
        print("❌ 2.6 向心力错误 Centripetal force calculation incorrect")
        print(f"   期望向心加速度 Expected a_c: {expected_a_c} m/s², 得到 Got: {a_c}")
        print(f"   期望向心力 Expected F_c: {expected_F_c} N, 得到 Got: {F_c}")
        all_passed = False
    else:
        print(f"✓ 2.6 向心力正确 (a_c = {expected_a_c} m/s², F_c = {expected_F_c} N)")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("牛顿运动定律 Newton's Laws of Motion")
    print("=" * 50)
    verify()
