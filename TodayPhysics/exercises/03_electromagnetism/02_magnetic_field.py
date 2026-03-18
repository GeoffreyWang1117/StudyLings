"""
磁场与洛伦兹力 Magnetic Field and Lorentz Force
难度 Difficulty: ★★★

学习目标 Learning Objectives:
- 理解毕奥-萨伐尔定律和磁场的产生 (Understand Biot-Savart law)
- 掌握带电粒子在磁场中的运动规律 (Motion of charged particles in B field)
- 分析安培力和载流导线间的相互作用 (Ampere force analysis)
- 理解磁偶极矩和霍尔效应 (Magnetic dipole moment and Hall effect)

物理背景 Physical Background:
磁场是运动电荷（电流）产生的场，它对运动电荷施加洛伦兹力。
与电场不同，磁场不对静止电荷作用，磁场线总是闭合的（无磁单极子）。

核心公式 Key Formulas:
- 毕奥-萨伐尔定律 Biot-Savart Law: dB = (μ₀/4π) × (I dl × r̂) / r²
- 洛伦兹力 Lorentz Force: F = q(E + v × B) [N]
- 直导线磁场: B = μ₀I / (2πr) [T]
- 圆环轴上磁场: B = μ₀IR² / (2(R² + z²)^(3/2)) [T]
- 回旋半径 Cyclotron radius: r = mv / (|q|B) [m]
- 回旋频率 Cyclotron frequency: ω = |q|B / m [rad/s]

物理常数 Physical Constants:
- 真空磁导率 μ₀ = 4π×10⁻⁷ H/m (Vacuum permeability)
- 电子质量 m_e = 9.11×10⁻³¹ kg
- 质子质量 m_p = 1.67×10⁻²⁷ kg

单位说明 Units:
- 磁场强度: T (特斯拉) = Wb/m² = kg/(A·s²)
- 磁通量: Wb (韦伯) = V·s
- 1 Gauss = 10⁻⁴ T
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import mu_0, e, m_e, m_p, c

# I AM NOT DONE

# =============================================================================
# 练习 2.1: 直线电流的磁场
# Exercise 2.1: Magnetic Field of Straight Wire
# =============================================================================
# 物理背景 Physical Background:
# 无限长直导线产生环绕导线的环形磁场。
# 磁场方向由右手定则确定：大拇指指向电流方向，四指环绕方向即为磁场方向。
#
# 核心公式 Key Formula:
# B = μ₀I / (2πr)
# 这个结果可通过安培环路定律推导得到。
#
# 应用: 电力传输线、同轴电缆、电磁铁

def magnetic_field_wire(I, r):
    """
    无限长直导线产生的磁场
    Magnetic field from an infinitely long straight wire

    参数 Parameters:
        I: 电流 [A] (安培)
        r: 到导线的垂直距离 [m]

    返回 Returns:
        磁场强度 B [T] (特斯拉)

    公式 Formula:
        B = μ₀I / (2πr)
        由安培环路定律推导: ∮B·dl = μ₀I_enc
    """
    # TODO: 计算磁场 (Calculate magnetic field)
    B = mu_0 * I / (2 * np.pi * r)
    return B

def magnetic_field_direction_wire(I_direction, r_direction):
    """
    用右手定则确定磁场方向
    Determine B-field direction using right-hand rule

    右手定则: 大拇指指向电流方向，四指弯曲方向即为磁场方向
    Right-hand rule: Thumb points along current, fingers curl in B direction
    """
    B_dir = np.cross(I_direction, r_direction)
    return B_dir / np.linalg.norm(B_dir)


# =============================================================================
# 练习 2.2: 圆环电流的磁场
# Exercise 2.2: Magnetic Field of Circular Loop
# =============================================================================
# 物理背景 Physical Background:
# 圆形电流环是最简单的磁偶极子模型，广泛用于理解原子磁矩。
# 在轴线上磁场可精确求解，远离时表现为磁偶极子场。
#
# 应用: 电磁铁、电机、MRI线圈、原子磁矩模型

def magnetic_field_loop_axis(I, R, z):
    """
    圆环电流在轴线上的磁场
    Magnetic field on the axis of a circular current loop

    参数 Parameters:
        I: 电流 [A]
        R: 线圈半径 [m]
        z: 距圆心沿轴向距离 [m]

    返回 Returns:
        轴向磁场 B [T]

    公式 Formula:
        B = μ₀IR² / (2(R² + z²)^(3/2))
        在圆心处 (z=0): B = μ₀I / (2R)
    """
    # TODO: 计算磁场 (Calculate magnetic field)
    B = mu_0 * I * R**2 / (2 * (R**2 + z**2)**1.5)
    return B

def magnetic_dipole_moment(I, A):
    """
    磁偶极矩（电流环的磁矩）
    Magnetic dipole moment of a current loop

    公式 Formula:
        μ = IA [A·m²]
        方向由右手定则确定，垂直于线圈平面

    物理意义: 描述磁场源的强度，类似于电偶极矩
    """
    return I * A


# =============================================================================
# 练习 2.3: 洛伦兹力
# Exercise 2.3: Lorentz Force
# =============================================================================
# 物理背景 Physical Background:
# 洛伦兹力是电磁场对运动电荷的总作用力。
# 电场力 qE 做功，磁场力 qv×B 不做功（总是垂直于速度）。
#
# 核心公式 Key Formula:
# F = q(E + v × B)
# 磁力特点: 只改变速度方向，不改变速率（动能不变）

def lorentz_force(q, v, E, B):
    """
    洛伦兹力 - 电磁场对运动电荷的总作用力
    Lorentz force - total EM force on a moving charge

    参数 Parameters:
        q: 电荷量 [C]
        v: 速度向量 [vx, vy, vz] [m/s]
        E: 电场向量 [Ex, Ey, Ez] [V/m]
        B: 磁场向量 [Bx, By, Bz] [T]

    返回 Returns:
        力向量 [Fx, Fy, Fz] [N]

    公式 Formula:
        F = q(E + v × B)
        电场力 qE 做功，磁场力 qv×B 不做功
    """
    v = np.array(v)
    E = np.array(E)
    B = np.array(B)
    # TODO: 计算洛伦兹力 (Calculate Lorentz force)
    F = q * (E + np.cross(v, B))
    return F

def magnetic_force(q, v, B):
    """
    纯磁力（无电场时）
    Pure magnetic force (when E = 0)

    特点: 磁力总是垂直于速度，因此不做功
    F ⊥ v → dW = F·ds = 0
    """
    return q * np.cross(v, B)


# =============================================================================
# 练习 2.4: 带电粒子在磁场中的圆周运动
# Exercise 2.4: Charged Particle in Magnetic Field
# =============================================================================
# 物理背景 Physical Background:
# 当带电粒子以垂直于磁场的速度运动时，磁力提供向心力，粒子做匀速圆周运动。
# 这是回旋加速器、质谱仪等设备的工作原理。
#
# 重要特点 Key Features:
# 1. 回旋频率只与 q/m 和 B 有关，与速度无关
# 2. 回旋半径与速度成正比
# 3. 动能守恒（磁力不做功）
#
# 应用: 回旋加速器、质谱仪、磁约束聚变

def cyclotron_radius(m, v, q, B):
    """
    回旋半径（拉莫尔半径）
    Cyclotron radius (Larmor radius)

    参数 Parameters:
        m: 粒子质量 [kg]
        v: 垂直于B的速度分量 [m/s]
        q: 电荷量 [C]
        B: 磁场强度 [T]

    返回 Returns:
        回旋半径 [m]

    推导 Derivation:
        qvB = mv²/r → r = mv/(|q|B)
    """
    # TODO: 计算回旋半径 (Calculate cyclotron radius)
    r = m * v / (abs(q) * B)
    return r

def cyclotron_frequency(q, B, m):
    """
    回旋角频率
    Cyclotron angular frequency

    公式 Formula:
        ω = |q|B / m [rad/s]

    重要: 频率与速度无关！这是回旋加速器能工作的关键
    """
    # TODO: 计算回旋频率 (Calculate cyclotron frequency)
    omega = abs(q) * B / m
    return omega

def cyclotron_period(q, B, m):
    """
    回旋周期
    Cyclotron period

    公式 Formula:
        T = 2πm / (|q|B) = 2π/ω [s]

    与速度无关，这使得粒子可被同步加速
    """
    return 2 * np.pi * m / (abs(q) * B)


# =============================================================================
# 练习 2.5: 螺旋运动
# Exercise 2.5: Helical Motion
# =============================================================================
# 物理背景 Physical Background:
# 当粒子速度与磁场有夹角时，运动分解为:
# - 垂直分量: 做圆周运动
# - 平行分量: 匀速直线运动
# 合成为螺旋运动
#
# 应用: 地球辐射带、磁镜、等离子体约束

def helical_pitch(v_parallel, T):
    """
    螺旋运动的螺距
    Pitch of helical motion

    螺距 = 平行速度 × 周期
    p = v_∥ × T

    这是粒子完成一个回旋周期后沿B方向前进的距离
    """
    return v_parallel * T

def decompose_velocity(v, B):
    """
    将速度分解为平行和垂直于磁场的分量
    Decompose velocity into parallel and perpendicular components

    返回 Returns:
        v_parallel: 平行于B的分量（决定轴向运动）
        v_perp: 垂直于B的分量（决定回旋运动）

    v = v_∥ + v_⊥
    """
    v = np.array(v)
    B = np.array(B)
    B_unit = B / np.linalg.norm(B)
    v_parallel = np.dot(v, B_unit) * B_unit
    v_perp = v - v_parallel
    return v_parallel, v_perp


# =============================================================================
# 练习 2.6: 霍尔效应
# Exercise 2.6: Hall Effect
# =============================================================================
# 物理背景 Physical Background:
# 霍尔效应：载流导体在磁场中产生横向电压。
# 这是由于载流子受洛伦兹力偏转，在导体两侧积累电荷。
#
# 应用 Applications:
# - 测量磁场（霍尔传感器）
# - 测量载流子密度和类型
# - 判断材料是n型还是p型半导体
#
# 霍尔电压符号可判断载流子类型！

def hall_voltage(I, B, n, q, t):
    """
    霍尔电压
    Hall voltage

    参数 Parameters:
        I: 电流 [A]
        B: 磁场 [T]
        n: 载流子密度 [m⁻³]
        q: 载流子电荷 [C]
        t: 导体厚度（垂直于I和B）[m]

    返回 Returns:
        霍尔电压 V_H [V]

    公式 Formula:
        V_H = IB / (n|q|t)

    物理解释: 洛伦兹力使载流子偏转，产生横向电场
    """
    # TODO: 计算霍尔电压 (Calculate Hall voltage)
    V_H = I * B / (n * abs(q) * t)
    return V_H

def hall_coefficient(n, q):
    """
    霍尔系数
    Hall coefficient

    公式 Formula:
        R_H = 1/(nq) [m³/C]

    符号判断:
        R_H > 0: p型（空穴导电）
        R_H < 0: n型（电子导电）
    """
    return 1 / (n * q)


# =============================================================================
# 练习 2.7: 安培力
# Exercise 2.7: Ampere Force
# =============================================================================
# 物理背景 Physical Background:
# 载流导线在磁场中受力（安培力），这是电动机的工作原理。
# 两根平行导线间的力用于定义安培单位。
#
# 核心公式 Key Formulas:
# - 单根导线: F = BIL sin(θ)
# - 两平行导线: F/L = μ₀I₁I₂ / (2πd)
#
# 方向判断 Direction:
# - 同向电流相吸
# - 反向电流相斥

def force_on_wire(I, L, B, theta=np.pi/2):
    """
    载流导线在磁场中受的安培力
    Ampere force on a current-carrying wire in magnetic field

    参数 Parameters:
        I: 电流 [A]
        L: 导线长度 [m]
        B: 磁场强度 [T]
        theta: 导线与磁场夹角 [rad]，默认90°

    返回 Returns:
        力的大小 [N]

    公式 Formula:
        F = BIL sin(θ)
        当 θ = 90° 时力最大
    """
    # TODO: 计算安培力 (Calculate Ampere force)
    F = B * I * L * np.sin(theta)
    return F

def force_between_wires(I1, I2, L, d):
    """
    两平行载流导线间的作用力
    Force between two parallel current-carrying wires

    参数 Parameters:
        I1, I2: 两导线电流 [A]
        L: 导线长度 [m]
        d: 导线间距 [m]

    返回 Returns:
        力的大小 [N]

    公式 Formula:
        F/L = μ₀I₁I₂ / (2πd)

    方向: 同向电流相吸，反向电流相斥
    Note: 这个公式用于定义安培单位！
    """
    # TODO: 计算两导线间的力 (Calculate force between wires)
    F_per_L = mu_0 * I1 * I2 / (2 * np.pi * d)
    return F_per_L * L


# =============================================================================
# 可视化
# =============================================================================
def plot_magnetic():
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. 直导线磁场
    ax1 = axes[0, 0]
    r = np.linspace(0.01, 0.5, 100)
    B_wire = magnetic_field_wire(10, r)
    ax1.plot(r*100, B_wire*1e4, 'b-', linewidth=2)
    ax1.set_xlabel('r (cm)')
    ax1.set_ylabel('B (Gauss)')
    ax1.set_title('直导线磁场 Wire Magnetic Field (I=10A)')
    ax1.grid(True, alpha=0.3)

    # 2. 圆环轴线磁场
    ax2 = axes[0, 1]
    z = np.linspace(-0.2, 0.2, 100)
    R = 0.05  # 5 cm
    B_loop = magnetic_field_loop_axis(10, R, z)
    ax2.plot(z*100, B_loop*1e4, 'r-', linewidth=2)
    ax2.set_xlabel('z (cm)')
    ax2.set_ylabel('B (Gauss)')
    ax2.set_title(f'圆环磁场 Loop Field (R={R*100}cm, I=10A)')
    ax2.grid(True, alpha=0.3)

    # 3. 回旋运动轨迹
    ax3 = axes[1, 0]
    B = 0.1  # T
    v = 1e6  # m/s
    r_cyc = cyclotron_radius(m_e, v, e, B)
    theta = np.linspace(0, 4*np.pi, 500)
    x = r_cyc * np.cos(theta) * 1e3  # mm
    y = r_cyc * np.sin(theta) * 1e3
    ax3.plot(x, y, 'b-', linewidth=1)
    ax3.set_xlabel('x (mm)')
    ax3.set_ylabel('y (mm)')
    ax3.set_title(f'电子回旋运动 (B={B}T, v={v:.0e}m/s)')
    ax3.set_aspect('equal')
    ax3.grid(True, alpha=0.3)

    # 4. 回旋半径vs能量
    ax4 = axes[1, 1]
    KE = np.linspace(1, 1000, 100) * e * 1e3  # 1-1000 keV
    v_e = np.sqrt(2 * KE / m_e)
    r_e = cyclotron_radius(m_e, v_e, e, 1.0)  # B = 1T
    ax4.loglog(KE/(e*1e3), r_e*1e3, 'b-', label='Electron')

    v_p = np.sqrt(2 * KE / m_p)
    r_p = cyclotron_radius(m_p, v_p, e, 1.0)
    ax4.loglog(KE/(e*1e3), r_p*1e3, 'r-', label='Proton')

    ax4.set_xlabel('Kinetic Energy (keV)')
    ax4.set_ylabel('Cyclotron radius (mm)')
    ax4.set_title('回旋半径vs动能 (B=1T)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('magnetic_field.png', dpi=150)
    print("图像已保存为 magnetic_field.png")
    plt.show()


def verify():
    """
    验证所有练习的正确性
    Verify correctness of all exercises
    """
    all_passed = True

    # 检查 2.1 - 直导线磁场 (Check wire magnetic field)
    B = magnetic_field_wire(10, 0.05)
    expected = mu_0 * 10 / (2 * np.pi * 0.05)
    if not np.isclose(B, expected, rtol=0.01):
        print("❌ 2.1 直导线磁场计算错误")
        print("   提示: 检查公式 B = μ₀I/(2πr) 是否正确实现")
        all_passed = False
    else:
        print(f"✓ 2.1 直导线磁场正确 (B = {B*1e4:.2f} Gauss)")

    # 检查 2.2 - 圆环磁场 (Check loop magnetic field)
    B_center = magnetic_field_loop_axis(1, 0.1, 0)
    expected = mu_0 * 1 / (2 * 0.1)
    if not np.isclose(B_center, expected, rtol=0.01):
        print("❌ 2.2 圆环中心磁场计算错误")
        print("   提示: 在z=0处，公式简化为 B = μ₀I/(2R)")
        all_passed = False
    else:
        print(f"✓ 2.2 圆环磁场正确（圆心处验证通过）")

    # 检查 2.3 - 洛伦兹力 (Check Lorentz force)
    F = lorentz_force(e, [1e6, 0, 0], [0, 0, 0], [0, 0, 1])
    expected_F = e * 1e6 * 1  # F_y = qv_xB_z (叉乘结果)
    if not np.isclose(F[1], expected_F, rtol=0.01):
        print("❌ 2.3 洛伦兹力计算错误")
        print("   提示: 检查叉乘 v × B 是否正确")
        all_passed = False
    else:
        print(f"✓ 2.3 洛伦兹力正确（F = q(v × B) 验证通过）")

    # 检查 2.4 - 回旋半径 (Check cyclotron radius)
    r = cyclotron_radius(m_e, 1e6, e, 0.1)
    expected_r = m_e * 1e6 / (e * 0.1)
    if not np.isclose(r, expected_r, rtol=0.01):
        print("❌ 2.4 回旋半径计算错误")
        print("   提示: r = mv/(|q|B)")
        all_passed = False
    else:
        print(f"✓ 2.4 回旋半径正确 (r = {r*1e3:.3f} mm)")

    # 检查 2.6 - 霍尔效应 (Check Hall effect)
    V_H = hall_voltage(1, 0.1, 1e28, e, 0.001)
    if V_H <= 0:
        print("❌ 2.6 霍尔电压计算错误（应为正值）")
        all_passed = False
    else:
        print(f"✓ 2.6 霍尔效应正确 (V_H = {V_H*1e6:.2f} μV)")

    # 检查 2.7 - 安培力 (Check Ampere force)
    F_wires = force_between_wires(10, 10, 1, 0.01)
    expected = mu_0 * 100 / (2 * np.pi * 0.01)
    if not np.isclose(F_wires, expected, rtol=0.01):
        print("❌ 2.7 两导线间安培力计算错误")
        print("   提示: F = μ₀I₁I₂L/(2πd)")
        all_passed = False
    else:
        print(f"✓ 2.7 安培力正确（同向电流相吸）")

    if all_passed:
        print("\n🎉 所有测试通过！")
        try:
            plot_magnetic()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("磁场与洛伦兹力 Magnetic Field")
    print("=" * 50)
    verify()
