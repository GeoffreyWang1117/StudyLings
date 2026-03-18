"""
能量与动量 Energy and Momentum
难度 Difficulty: ★★

================================================================================
学习目标 Learning Objectives
================================================================================
- 理解动能、势能和机械能守恒定律
  Understand kinetic energy, potential energy, and conservation of mechanical energy
- 掌握动量和冲量的概念及其物理意义
  Master the concepts of momentum and impulse and their physical meanings
- 应用能量和动量守恒定律解决碰撞问题
  Apply conservation laws to solve collision problems

================================================================================
物理背景 Physical Background
================================================================================
能量和动量是物理学中两个最重要的守恒量：

1. 动能 Kinetic Energy (KE):
   物体由于运动而具有的能量：KE = (1/2)mv²
   单位：焦耳 (J) = kg·m²/s²

2. 势能 Potential Energy (PE):
   - 重力势能：PE = mgh（h为相对参考面的高度）
   - 弹性势能：PE = (1/2)kx²（k为弹簧劲度系数，x为形变量）

3. 机械能守恒 Conservation of Mechanical Energy:
   当只有保守力（如重力、弹簧力）做功时：
   E_total = KE + PE = 常数

4. 动量 Momentum:
   p = mv（向量），单位：kg·m/s
   动量守恒：系统不受外力时，总动量不变

5. 碰撞 Collisions:
   - 弹性碰撞：动量和动能都守恒
   - 非弹性碰撞：动量守恒，动能部分损失
   - 完全非弹性碰撞：碰撞后物体粘在一起

核心公式 Key Formulas:
- 动能: KE = (1/2)mv²
- 重力势能: PE = mgh
- 弹性势能: PE = (1/2)kx²
- 动量: p = mv
- 功率: P = F·v = dW/dt

HINT: 机械能守恒: E = KE + PE = 常数（无非保守力做功时）
HINT: 动量守恒: p_total = 常数（无外力时）
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])

# I AM NOT DONE

g = 9.8  # m/s²

# =============================================================================
# 练习 3.1: 动能
# Exercise 3.1: Kinetic Energy
# =============================================================================
# 物理背景 Physical Background:
# 动能是物体由于运动而具有的能量。动能与质量成正比，与速度的平方成正比。
# 这意味着速度加倍时，动能会变为原来的4倍。
#
# 题目 Problem:
# 一个质量 m = 2 kg 的物体以速度 v = 5 m/s 运动
# A mass of 2 kg moves at 5 m/s
# 计算动能 KE
# Calculate the kinetic energy KE
#
# 公式 Formula: KE = (1/2)mv²
# 单位 Unit: 焦耳 (J) = kg·m²/s²

m1 = 2.0  # 质量 mass，单位：kg
v1 = 5.0  # 速度 velocity，单位：m/s

# TODO: 计算动能 KE
# 提示：直接使用公式 KE = 0.5 * m * v**2
KE = None  # 修改这里 (单位：J)


# =============================================================================
# 练习 3.2: 重力势能
# Exercise 3.2: Gravitational Potential Energy
# =============================================================================
# 物理背景 Physical Background:
# 重力势能是物体由于位置（高度）而具有的能量，是相对量，需要选择参考面。
# 物体升高时，外力对物体做正功，重力势能增加；
# 物体下降时，重力对物体做正功，重力势能减少。
#
# 题目 Problem:
# 一个质量 m = 3 kg 的物体位于高度 h = 10 m
# A mass of 3 kg is at a height of 10 m
# 计算相对于地面的重力势能
# Calculate the gravitational potential energy relative to the ground
#
# 公式 Formula: PE = mgh（取地面为零势能面）
# 单位 Unit: 焦耳 (J)

m2 = 3.0  # 质量 mass，单位：kg
h = 10.0  # 高度 height，单位：m（相对地面）

# TODO: 计算势能 PE
# 提示：PE = m * g * h
PE = None  # 修改这里 (单位：J)


# =============================================================================
# 练习 3.3: 机械能守恒 - 自由落体
# Exercise 3.3: Conservation of Energy - Free Fall
# =============================================================================
# 物理背景 Physical Background:
# 机械能守恒定律是能量守恒的特例。当只有重力（保守力）做功时，
# 物体的动能和势能可以相互转化，但总机械能保持不变。
#
# 自由落体过程中：
# - 初态（顶端）：动能=0，势能=mgh，总能量=mgh
# - 末态（落地）：动能=(1/2)mv²，势能=0，总能量=(1/2)mv²
# - 由能量守恒：mgh = (1/2)mv²，解得 v = sqrt(2gh)
#
# 题目 Problem:
# 一个物体从高度 h = 20 m 自由下落（忽略空气阻力）
# An object falls freely from height h = 20 m (ignore air resistance)
# 使用能量守恒计算落地时的速度
# Calculate the speed when it hits the ground using energy conservation
#
# 公式 Formula: v = sqrt(2gh)
# 单位 Unit: m/s

h3 = 20.0  # 下落高度 fall height，单位：m

# TODO: 计算落地速度 v_final
# 提示：v = np.sqrt(2 * g * h3)
v_final = None  # 修改这里 (单位：m/s)


# =============================================================================
# 练习 3.4: 弹性碰撞
# Exercise 3.4: Elastic Collision
# =============================================================================
# 物理背景 Physical Background:
# 弹性碰撞是指碰撞过程中动能守恒的碰撞（没有能量损失）。
# 同时满足动量守恒和动能守恒两个条件：
# - 动量守恒：m1*v1 + m2*v2 = m1*v1' + m2*v2'
# - 动能守恒：(1/2)m1*v1² + (1/2)m2*v2² = (1/2)m1*v1'² + (1/2)m2*v2'²
#
# 联立求解可得一维弹性碰撞公式：
# v1' = ((m1-m2)*v1 + 2*m2*v2) / (m1+m2)
# v2' = ((m2-m1)*v2 + 2*m1*v1) / (m1+m2)
#
# 题目 Problem:
# 一维弹性碰撞 1D elastic collision:
# 物体1: m1 = 2 kg, v1 = 4 m/s (向右为正)
# 物体2: m2 = 3 kg, v2 = -1 m/s (向左，故为负)
# Object 1: m1 = 2 kg, v1 = 4 m/s (rightward positive)
# Object 2: m2 = 3 kg, v2 = -1 m/s (leftward, negative)
#
# 计算碰撞后的速度 Calculate velocities after collision
#
# 单位 Unit: m/s

m_1 = 2.0   # 物体1质量，单位：kg
m_2 = 3.0   # 物体2质量，单位：kg
v_1 = 4.0   # 物体1碰撞前速度，单位：m/s（正=向右）
v_2 = -1.0  # 物体2碰撞前速度，单位：m/s（负=向左）

# TODO: 计算碰撞后的速度 v1_after 和 v2_after
# 提示：使用上面给出的弹性碰撞公式
v1_after = None  # 修改这里 (物体1碰撞后速度，单位：m/s)
v2_after = None  # 修改这里 (物体2碰撞后速度，单位：m/s)


# =============================================================================
# 练习 3.5: 非弹性碰撞
# Exercise 3.5: Inelastic Collision
# =============================================================================
# 物理背景 Physical Background:
# 完全非弹性碰撞是指碰撞后两物体粘在一起运动的碰撞。
# 此时动量守恒，但动能不守恒（部分动能转化为热能、声能等）。
#
# 动量守恒：m1*v1 + m2*v2 = (m1+m2)*v_common
# 解得：v_common = (m1*v1 + m2*v2) / (m1+m2)
#
# 动能损失计算：
# ΔKE = KE_before - KE_after
#     = (1/2)*m1*v1² + (1/2)*m2*v2² - (1/2)*(m1+m2)*v_common²
#
# 题目 Problem:
# 完全非弹性碰撞 Perfectly inelastic collision:
# 物体1: m1 = 4 kg, v1 = 6 m/s
# 物体2: m2 = 2 kg, v2 = 0 m/s（静止）
# Object 1: m1 = 4 kg, v1 = 6 m/s
# Object 2: m2 = 2 kg, v2 = 0 m/s (at rest)
#
# 计算碰撞后共同速度和损失的动能
# Calculate common velocity and kinetic energy lost
#
# 单位 Unit: 速度-m/s，能量-J

m_a = 4.0  # 物体1质量，单位：kg
m_b = 2.0  # 物体2质量，单位：kg
v_a = 6.0  # 物体1碰撞前速度，单位：m/s
v_b = 0.0  # 物体2碰撞前速度（静止），单位：m/s

# TODO: 计算碰撞后的共同速度 v_common 和损失的动能 delta_KE
# 提示：先用动量守恒计算 v_common，再计算碰撞前后的动能差
v_common = None  # 修改这里 (共同速度，单位：m/s)
delta_KE = None  # 修改这里 (损失的动能，正值，单位：J)


# =============================================================================
# 练习 3.6: 弹簧势能
# Exercise 3.6: Spring Potential Energy
# =============================================================================
# 物理背景 Physical Background:
# 弹簧势能（弹性势能）是弹簧由于形变而储存的能量。
# 当弹簧被压缩或拉伸时，它储存势能；释放时，势能转化为动能。
#
# 弹簧势能：PE = (1/2)kx²
# 其中 k 是弹簧劲度系数（又称弹性系数），x 是形变量（压缩或拉伸量）
#
# 能量守恒：弹簧完全释放时，所有势能转化为动能
# (1/2)kx² = (1/2)mv²
# 解得：v = sqrt(k/m) * x
#
# 题目 Problem:
# 弹簧劲度系数 k = 200 N/m，被压缩 x = 0.1 m
# Spring constant k = 200 N/m, compressed by x = 0.1 m
# 释放后推动质量 m = 0.5 kg 的物体
# After release, it pushes a mass of 0.5 kg
# 计算物体获得的最大速度（弹簧完全释放时）
# Calculate the maximum speed (when spring fully releases)
#
# 公式 Formula: v_max = sqrt(k*x²/m) = x*sqrt(k/m)
# 单位 Unit: m/s

k = 200.0        # 弹簧劲度系数 spring constant，单位：N/m
x_compress = 0.1  # 压缩量 compression，单位：m
m_obj = 0.5      # 物体质量 object mass，单位：kg

# TODO: 计算最大速度 v_max
# 提示：由能量守恒 (1/2)kx² = (1/2)mv²，解得 v = sqrt(kx²/m)
v_max = None  # 修改这里 (单位：m/s)


# =============================================================================
# 练习 3.7: 功率
# Exercise 3.7: Power
# =============================================================================
# 物理背景 Physical Background:
# 功率是做功的速率，表示能量转化或传递的快慢。
# 瞬时功率：P = dW/dt = F·v（力与速度的点积）
# 对于恒力和匀速运动：P = F * v
#
# 当汽车匀速行驶时，发动机提供的驱动力等于阻力（二力平衡），
# 此时发动机输出功率 = 驱动力 × 速度 = 阻力 × 速度
#
# 题目 Problem:
# 汽车以恒定速度 v = 20 m/s 行驶（匀速，发动机力=阻力）
# A car travels at constant speed v = 20 m/s
# 受到的阻力为 F_drag = 500 N
# Air drag force is 500 N
# 计算发动机输出功率
# Calculate the engine power output
#
# 公式 Formula: P = F * v
# 单位 Unit: 瓦特 (W) = J/s；1 kW = 1000 W

v_car = 20.0    # 汽车速度 car velocity，单位：m/s
F_drag = 500.0  # 阻力 drag force，单位：N

# TODO: 计算功率 P（瓦特）
# 提示：匀速时驱动力=阻力，P = F_drag * v_car
P = None  # 修改这里 (单位：W)


# =============================================================================
# 验证函数 Verification Function - 不要修改 Do not modify
# =============================================================================
def verify():
    """
    验证所有练习的答案是否正确
    Verify all exercises
    """
    all_passed = True

    # 检查 3.1: 动能
    # Check 3.1: Kinetic Energy
    expected_KE = 0.5 * m1 * v1**2  # = 25 J
    if KE is None or not np.isclose(KE, expected_KE):
        print("❌ 3.1 动能计算错误 Kinetic energy calculation incorrect")
        print(f"   期望 Expected: {expected_KE} J, 得到 Got: {KE}")
        all_passed = False
    else:
        print(f"✓ 3.1 动能正确 (KE = {expected_KE} J)")

    # 检查 3.2: 重力势能
    # Check 3.2: Gravitational Potential Energy
    expected_PE = m2 * g * h  # = 294 J
    if PE is None or not np.isclose(PE, expected_PE):
        print("❌ 3.2 势能计算错误 Potential energy calculation incorrect")
        print(f"   期望 Expected: {expected_PE} J, 得到 Got: {PE}")
        all_passed = False
    else:
        print(f"✓ 3.2 势能正确 (PE = {expected_PE} J)")

    # 检查 3.3: 自由落体
    # Check 3.3: Free Fall
    expected_v_final = np.sqrt(2 * g * h3)  # ≈ 19.8 m/s
    if v_final is None or not np.isclose(v_final, expected_v_final, rtol=0.01):
        print("❌ 3.3 自由落体速度错误 Free fall velocity incorrect")
        print(f"   期望 Expected: {expected_v_final:.2f} m/s, 得到 Got: {v_final}")
        all_passed = False
    else:
        print(f"✓ 3.3 自由落体正确 (v = sqrt(2gh) = {expected_v_final:.2f} m/s)")

    # 检查 3.4: 弹性碰撞
    # Check 3.4: Elastic Collision
    expected_v1_after = ((m_1 - m_2) * v_1 + 2 * m_2 * v_2) / (m_1 + m_2)  # = -1.6
    expected_v2_after = ((m_2 - m_1) * v_2 + 2 * m_1 * v_1) / (m_1 + m_2)  # = 3.4
    if v1_after is None or v2_after is None:
        print("❌ 3.4 弹性碰撞错误 - 未完成 Elastic collision - incomplete")
        all_passed = False
    elif not np.isclose(v1_after, expected_v1_after, rtol=0.01) or \
         not np.isclose(v2_after, expected_v2_after, rtol=0.01):
        print("❌ 3.4 弹性碰撞错误 Elastic collision calculation incorrect")
        print(f"   期望 v1' Expected: {expected_v1_after:.2f} m/s, 得到 Got: {v1_after}")
        print(f"   期望 v2' Expected: {expected_v2_after:.2f} m/s, 得到 Got: {v2_after}")
        all_passed = False
    else:
        print(f"✓ 3.4 弹性碰撞正确 (v1' = {expected_v1_after:.2f} m/s, v2' = {expected_v2_after:.2f} m/s)")

    # 检查 3.5: 非弹性碰撞
    # Check 3.5: Inelastic Collision
    expected_v_common = (m_a * v_a + m_b * v_b) / (m_a + m_b)  # = 4 m/s
    KE_before = 0.5 * m_a * v_a**2 + 0.5 * m_b * v_b**2
    KE_after = 0.5 * (m_a + m_b) * expected_v_common**2
    expected_delta_KE = KE_before - KE_after  # = 24 J
    if v_common is None or delta_KE is None:
        print("❌ 3.5 非弹性碰撞错误 - 未完成 Inelastic collision - incomplete")
        all_passed = False
    elif not np.isclose(v_common, expected_v_common) or \
         not np.isclose(delta_KE, expected_delta_KE, rtol=0.01):
        print("❌ 3.5 非弹性碰撞错误 Inelastic collision calculation incorrect")
        print(f"   期望共同速度 Expected v: {expected_v_common} m/s, 得到 Got: {v_common}")
        print(f"   期望动能损失 Expected ΔKE: {expected_delta_KE} J, 得到 Got: {delta_KE}")
        all_passed = False
    else:
        print(f"✓ 3.5 非弹性碰撞正确 (v = {expected_v_common} m/s, ΔKE = {expected_delta_KE} J)")

    # 检查 3.6: 弹簧势能
    # Check 3.6: Spring Potential Energy
    expected_v_max = np.sqrt(k * x_compress**2 / m_obj)  # = 2 m/s
    if v_max is None or not np.isclose(v_max, expected_v_max):
        print("❌ 3.6 弹簧势能转换错误 Spring energy conversion incorrect")
        print(f"   期望 Expected: {expected_v_max} m/s, 得到 Got: {v_max}")
        all_passed = False
    else:
        print(f"✓ 3.6 弹簧势能正确 (v_max = {expected_v_max} m/s)")

    # 检查 3.7: 功率
    # Check 3.7: Power
    expected_P = F_drag * v_car  # = 10000 W
    if P is None or not np.isclose(P, expected_P):
        print("❌ 3.7 功率计算错误 Power calculation incorrect")
        print(f"   期望 Expected: {expected_P} W, 得到 Got: {P}")
        all_passed = False
    else:
        print(f"✓ 3.7 功率正确 (P = {expected_P} W = {expected_P/1000} kW)")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("能量与动量 Energy and Momentum")
    print("=" * 50)
    verify()
