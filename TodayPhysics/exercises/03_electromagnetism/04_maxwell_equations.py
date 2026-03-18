"""
麦克斯韦方程组 Maxwell's Equations
难度 Difficulty: ★★★★

学习目标 Learning Objectives:
- 深入理解麦克斯韦方程组的物理意义 (Understand Maxwell's equations)
- 掌握位移电流的概念及其重要性 (Master displacement current)
- 理解电磁波的产生和传播 (EM wave generation and propagation)
- 分析电磁波在介质中的行为 (EM waves in media)

物理背景 Physical Background:
麦克斯韦方程组是电磁学的基石，统一了电学和磁学，预言了电磁波的存在。
爱因斯坦称麦克斯韦方程组为"物理学中最美的方程"。

麦克斯韦方程组 Maxwell's Equations (微分形式):
1. 高斯定律 Gauss's Law:         ∇·E = ρ/ε₀
   （电荷是电场的源）
2. 磁场高斯定律:                  ∇·B = 0
   （没有磁单极子，磁场线总是闭合的）
3. 法拉第定律 Faraday's Law:     ∇×E = -∂B/∂t
   （变化的磁场产生电场）
4. 安培-麦克斯韦定律:            ∇×B = μ₀J + μ₀ε₀∂E/∂t
   （电流和变化的电场产生磁场）

核心公式 Key Formulas:
- 电磁波速度: c = 1/√(ε₀μ₀) ≈ 3×10⁸ m/s
- 位移电流密度: J_d = ε₀∂E/∂t
- 波印廷矢量: S = E × H = E × B/μ₀ [W/m²]

单位说明 Units:
- 电场: V/m = N/C
- 磁场: T = Wb/m² = kg/(A·s²)
- 功率密度: W/m²
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import epsilon_0, mu_0, c

# I AM NOT DONE

# =============================================================================
# 练习 4.1: 高斯定律验证
# Exercise 4.1: Gauss's Law Verification
# =============================================================================
# 物理背景 Physical Background:
# 高斯定律是麦克斯韦第一方程，表述电场与电荷的关系。
# 积分形式: ∮E·dA = Q_enc/ε₀
# 微分形式: ∇·E = ρ/ε₀

def gauss_law_flux(Q):
    """
    高斯定律: 计算通过闭合曲面的电通量
    Gauss's Law: Electric flux through a closed surface

    参数 Parameters:
        Q: 闭合曲面内包围的总电荷 [C]

    返回 Returns:
        电通量 Φ_E [V·m = N·m²/C]

    公式 Formula:
        Φ_E = ∮E·dA = Q_enc/ε₀

    物理意义: 电通量只与包围的电荷有关，与曲面形状无关
    """
    # TODO: 计算电通量 (Calculate electric flux)
    Phi_E = Q / epsilon_0
    return Phi_E

def electric_field_sphere(Q, r):
    """
    球对称电荷分布外部的电场
    Electric field outside a spherically symmetric charge distribution

    由高斯定律推导: E × 4πr² = Q/ε₀
    """
    E = Q / (4 * np.pi * epsilon_0 * r**2)
    return E


# =============================================================================
# 练习 4.2: 位移电流
# Exercise 4.2: Displacement Current
# =============================================================================
# 物理背景 Physical Background:
# 位移电流是麦克斯韦的关键贡献！
# 没有位移电流，安培定律在电容器处失效。
# 位移电流使电磁波的存在成为可能。
#
# 历史意义: 麦克斯韦引入位移电流，统一了电磁学，预言了电磁波

def displacement_current_density(dE_dt):
    """
    位移电流密度
    Displacement current density

    参数 Parameters:
        dE_dt: 电场变化率 [V/(m·s)]

    返回 Returns:
        位移电流密度 J_d [A/m²]

    公式 Formula:
        J_d = ε₀ ∂E/∂t

    物理意义:
        变化的电场产生"位移电流"，效果等同于真实电流
        这使得安培定律在电容器处也成立
    """
    # TODO: 计算位移电流密度 (Calculate displacement current density)
    J_d = epsilon_0 * dE_dt
    return J_d

def displacement_current(A, dE_dt):
    """
    位移电流
    Displacement current

    I_d = ε₀ A ∂E/∂t = ε₀ ∂Φ_E/∂t
    """
    return epsilon_0 * A * dE_dt

def capacitor_displacement_current(C, dV_dt):
    """
    电容器中的位移电流
    Displacement current in a capacitor

    关键结论: 位移电流 = 传导电流
    I_d = C dV/dt = I_c

    这解释了为什么电流能"穿过"电容器
    """
    return C * dV_dt


# =============================================================================
# 练习 4.3: 电磁波速度
# Exercise 4.3: EM Wave Speed
# =============================================================================
# 物理背景 Physical Background:
# 麦克斯韦方程组预言电磁波以光速传播！
# 这是理论物理学最伟大的预言之一。
# 麦克斯韦由此推断光是一种电磁波。
#
# c = 1/√(ε₀μ₀) ≈ 2.998×10⁸ m/s

def em_wave_speed():
    """
    从麦克斯韦方程计算电磁波速度
    Calculate EM wave speed from Maxwell's equations

    返回 Returns:
        电磁波速度 c [m/s]

    公式 Formula:
        c = 1/√(ε₀μ₀)

    历史意义:
        麦克斯韦计算出此值与实测光速一致，
        从而推断光是电磁波的一种！
    """
    # TODO: 计算电磁波速度 (Calculate EM wave speed)
    c_calc = 1 / np.sqrt(epsilon_0 * mu_0)
    return c_calc

def verify_maxwell_relation():
    """
    验证麦克斯韦关系式 c = 1/√(ε₀μ₀)
    Verify Maxwell's relation
    """
    c_calc = em_wave_speed()
    return np.isclose(c_calc, c, rtol=0.01)


# =============================================================================
# 练习 4.4: 波动方程
# Exercise 4.4: Wave Equation
# =============================================================================
# 物理背景 Physical Background:
# 从麦克斯韦方程组可以推导出电磁波的波动方程:
# ∇²E = μ₀ε₀ ∂²E/∂t² = (1/c²) ∂²E/∂t²
#
# 这证明了电场和磁场可以自持传播，无需介质！
# 平面波解: E = E₀ sin(kx - ωt)，其中 ω/k = c

def wave_equation_solution(E0, k, omega, x, t):
    """
    电磁波平面波解
    Plane wave solution of EM wave equation

    参数 Parameters:
        E0: 电场振幅 [V/m]
        k: 波矢（波数）[rad/m]
        omega: 角频率 [rad/s]
        x: 位置 [m]
        t: 时间 [s]

    返回 Returns:
        电场 E(x,t) [V/m]

    公式 Formula:
        E = E₀ sin(kx - ωt)
        其中 ω/k = c（色散关系）
    """
    return E0 * np.sin(k * x - omega * t)

def verify_wave_equation(E0, k, omega, x, t, dx=1e-9, dt=1e-18):
    """
    数值验证波动方程 ∂²E/∂x² = (1/c²) ∂²E/∂t²
    Numerically verify the wave equation

    使用有限差分法计算二阶导数并验证关系
    """
    # 二阶空间导数 (Second spatial derivative)
    E_xp = wave_equation_solution(E0, k, omega, x + dx, t)
    E_xm = wave_equation_solution(E0, k, omega, x - dx, t)
    E_0 = wave_equation_solution(E0, k, omega, x, t)
    d2E_dx2 = (E_xp - 2*E_0 + E_xm) / dx**2

    # 二阶时间导数 (Second time derivative)
    E_tp = wave_equation_solution(E0, k, omega, x, t + dt)
    E_tm = wave_equation_solution(E0, k, omega, x, t - dt)
    d2E_dt2 = (E_tp - 2*E_0 + E_tm) / dt**2

    # 验证关系: 应有 d²E/dx² / d²E/dt² = 1/c²
    ratio = d2E_dx2 / d2E_dt2 if d2E_dt2 != 0 else 0
    return ratio  # 应该接近 1/c²


# =============================================================================
# 练习 4.5: 波印廷定理
# Exercise 4.5: Poynting Theorem
# =============================================================================
# 物理背景 Physical Background:
# 波印廷矢量描述电磁能量的流动方向和强度。
# 波印廷定理是电磁场的能量守恒定律。
#
# S = E × H = E × B/μ₀ [W/m²]
# 方向: 沿能量传播方向

def poynting_vector_magnitude(E, B):
    """
    波印廷矢量大小
    Magnitude of Poynting vector

    参数 Parameters:
        E: 电场强度 [V/m]
        B: 磁场强度 [T]

    返回 Returns:
        能流密度 S [W/m²]

    公式 Formula:
        S = |E × B|/μ₀ = EB/μ₀（对于垂直的E和B）
    """
    return E * B / mu_0

def energy_flux(E0):
    """
    电磁波的时间平均能流密度（强度）
    Time-averaged energy flux (intensity) of EM wave

    公式 Formula:
        <S> = E₀²/(2μ₀c) = (1/2)ε₀cE₀² [W/m²]

    对于电磁波: B₀ = E₀/c
    """
    return E0**2 / (2 * mu_0 * c)

def radiation_pressure(I):
    """
    辐射压强（完全吸收时）
    Radiation pressure (for complete absorption)

    公式 Formula:
        P = I/c [Pa]

    完全反射时: P = 2I/c

    应用: 太阳帆、光镊
    """
    return I / c


# =============================================================================
# 练习 4.6: 介质中的麦克斯韦方程
# Exercise 4.6: Maxwell's Equations in Media
# =============================================================================
# 物理背景 Physical Background:
# 在介质中，ε₀ → ε = ε₀ε_r，μ₀ → μ = μ₀μ_r
# 电磁波速度变慢，产生折射现象
#
# 折射率 n = c/v = √(ε_r μ_r)
# 对于非磁性材料 (μ_r ≈ 1): n ≈ √ε_r

def wave_speed_in_medium(epsilon_r, mu_r):
    """
    介质中的电磁波速度
    EM wave speed in a medium

    参数 Parameters:
        epsilon_r: 相对介电常数（无量纲）
        mu_r: 相对磁导率（无量纲）

    返回 Returns:
        波速 v [m/s]

    公式 Formula:
        v = c/n = c/√(ε_r μ_r) = 1/√(εμ)
    """
    # TODO: 计算介质中波速 (Calculate wave speed in medium)
    v = c / np.sqrt(epsilon_r * mu_r)
    return v

def refractive_index(epsilon_r, mu_r=1):
    """
    折射率
    Refractive index

    公式 Formula:
        n = √(ε_r μ_r)

    常见材料 Common materials:
        空气: n ≈ 1.0003
        水: n ≈ 1.33
        玻璃: n ≈ 1.5
        金刚石: n ≈ 2.4
    """
    return np.sqrt(epsilon_r * mu_r)


# =============================================================================
# 可视化
# =============================================================================
def plot_maxwell():
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. 电场和磁场的波动
    ax1 = axes[0, 0]
    wavelength = 500e-9
    k = 2 * np.pi / wavelength
    omega = c * k
    E0 = 1

    x = np.linspace(0, 3*wavelength, 500)
    t = 0
    E = wave_equation_solution(E0, k, omega, x, t)
    B = E / c

    ax1.plot(x*1e9, E, 'b-', label='E', linewidth=2)
    ax1.plot(x*1e9, B*c, 'r-', label='B×c', linewidth=2)
    ax1.set_xlabel('x (nm)')
    ax1.set_ylabel('Field')
    ax1.set_title('电磁波 E and B')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 位移电流
    ax2 = axes[0, 1]
    f = np.logspace(6, 12, 100)  # MHz to THz
    omega_f = 2 * np.pi * f
    # 位移电流密度相对于传导电流
    sigma = 1e7  # 导体电导率
    ratio = epsilon_0 * omega_f / sigma

    ax2.loglog(f/1e9, ratio, 'b-', linewidth=2)
    ax2.axhline(y=1, color='r', linestyle='--')
    ax2.set_xlabel('Frequency (GHz)')
    ax2.set_ylabel('ε₀ω/σ')
    ax2.set_title('位移电流vs传导电流比值')
    ax2.grid(True, alpha=0.3)

    # 3. 介质中的波速
    ax3 = axes[1, 0]
    epsilon_r = np.linspace(1, 10, 100)
    v = wave_speed_in_medium(epsilon_r, 1)
    ax3.plot(epsilon_r, v/1e8, 'b-', linewidth=2)
    ax3.set_xlabel('Relative permittivity ε_r')
    ax3.set_ylabel('Wave speed (×10⁸ m/s)')
    ax3.set_title('介质中电磁波速度')
    ax3.grid(True, alpha=0.3)

    # 4. 辐射压强
    ax4 = axes[1, 1]
    I = np.logspace(0, 12, 100)  # 1 W/m² to 1 TW/m²
    P = radiation_pressure(I)
    ax4.loglog(I, P, 'r-', linewidth=2)
    ax4.set_xlabel('Intensity (W/m²)')
    ax4.set_ylabel('Radiation pressure (Pa)')
    ax4.set_title('辐射压强')
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('maxwell_equations.png', dpi=150)
    print("图像已保存为 maxwell_equations.png")
    plt.show()


def verify():
    """
    验证所有练习的正确性
    Verify correctness of all exercises
    """
    all_passed = True

    # 检查 4.1 - 高斯定律 (Check Gauss's law)
    Phi = gauss_law_flux(1e-9)  # 1 nC
    expected = 1e-9 / epsilon_0
    if not np.isclose(Phi, expected, rtol=0.01):
        print("❌ 4.1 高斯定律验证错误")
        print("   提示: Φ = Q/ε₀")
        all_passed = False
    else:
        print(f"✓ 4.1 高斯定律正确 (Φ = {Phi:.2f} V·m)")

    # 检查 4.2 - 位移电流 (Check displacement current)
    J_d = displacement_current_density(1e12)  # 1 TV/m/s
    expected_J = epsilon_0 * 1e12
    if not np.isclose(J_d, expected_J, rtol=0.01):
        print("❌ 4.2 位移电流密度计算错误")
        print("   提示: J_d = ε₀ ∂E/∂t")
        all_passed = False
    else:
        print(f"✓ 4.2 位移电流正确（麦克斯韦贡献）")

    # 检查 4.3 - 电磁波速度 (Check EM wave speed)
    if not verify_maxwell_relation():
        print("❌ 4.3 c = 1/√(ε₀μ₀) 验证失败")
        print("   这是麦克斯韦的伟大发现！")
        all_passed = False
    else:
        print(f"✓ 4.3 电磁波速度正确 (c = {em_wave_speed():.3e} m/s = 光速)")

    # 检查 4.5 - 波印廷定理 (Check Poynting theorem)
    S = energy_flux(100)  # E₀ = 100 V/m
    if S <= 0:
        print("❌ 4.5 能流密度计算错误")
        all_passed = False
    else:
        print(f"✓ 4.5 波印廷定理正确 (<S> = {S:.2f} W/m²)")

    # 检查 4.6 - 介质中的方程 (Check equations in media)
    v_glass = wave_speed_in_medium(2.25, 1)  # 玻璃 ε_r = 2.25, n ≈ 1.5
    n = refractive_index(2.25)
    if not np.isclose(n, 1.5, rtol=0.01):
        print("❌ 4.6 折射率计算错误")
        print("   提示: n = √(ε_r μ_r)")
        all_passed = False
    else:
        print(f"✓ 4.6 介质方程正确 (玻璃: n = {n:.2f}, v = {v_glass/1e8:.2f}×10⁸ m/s)")

    if all_passed:
        print("\n🎉 所有测试通过！")
        try:
            plot_maxwell()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("麦克斯韦方程组 Maxwell's Equations")
    print("=" * 50)
    verify()
