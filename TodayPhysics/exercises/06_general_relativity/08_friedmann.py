"""
弗里德曼方程详解 Friedmann Equations Detailed
难度 Difficulty: ★★★★★

学习目标 Learning Objectives:
- 理解FLRW（Friedmann-Lemaitre-Robertson-Walker）度规的物理意义
- 掌握弗里德曼方程的推导、物理解释和数值求解
- 分析不同宇宙学模型：物质主导、辐射主导、暗能量主导
- 计算宇宙学距离（共动距离、光度距离、角直径距离）
- 理解宇宙膨胀的加速/减速历史

物理背景 Physical Background:
弗里德曼方程描述了均匀各向同性宇宙（宇宙学原理）的演化。
它是将爱因斯坦场方程应用于FLRW度规的结果。

FLRW度规 FLRW Metric:
ds² = -c²dt² + a(t)²[dr²/(1-kr²) + r²dΩ²]
其中 a(t) 是标度因子，k 是空间曲率（k=0平坦，k=+1闭合，k=-1开放）

宇宙演化时期 Epochs of Cosmic Evolution:
1. 辐射主导时期 (z > 3400): a(t) ∝ t^(1/2)
2. 物质主导时期 (3400 > z > 0.4): a(t) ∝ t^(2/3)
3. 暗能量主导时期 (z < 0.4): a(t) ∝ exp(H·t)

关键公式 Key Formulas:
  - 第一弗里德曼方程: H² = (8πGρ/3) - kc²/a² + Λc²/3
  - 第二弗里德曼方程: ä/a = -(4πG/3)(ρ + 3p/c²) + Λc²/3
  - 连续性方程: dρ/dt + 3H(ρ + p/c²) = 0
  - 状态方程: p = wρc²，其中 w=0(物质)，w=1/3(辐射)，w=-1(宇宙学常数)

单位说明 Units:
  - H₀ = 70 km/s/Mpc ≈ 2.27×10⁻¹⁸ s⁻¹
  - 1 Mpc = 3.086×10²² m
  - 1 Gyr = 3.15×10¹⁶ s
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint, quad
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import G, c, k_B

# I AM NOT DONE

# 宇宙学常数
H_0 = 70  # km/s/Mpc 哈勃常数
H_0_SI = H_0 * 1000 / (3.086e22)  # s⁻¹

# =============================================================================
# 练习 8.1: 哈勃参数
# Exercise 8.1: Hubble Parameter
# =============================================================================
def hubble_parameter(a, Omega_m, Omega_r, Omega_Lambda, Omega_k=0, H0=H_0_SI):
    """
    哈勃参数 H(a)
    H² = H₀²[Ω_r/a⁴ + Ω_m/a³ + Ω_k/a² + Ω_Λ]

    a: 标度因子（今天a=1）
    Omega_m: 物质密度参数
    Omega_r: 辐射密度参数
    Omega_Lambda: 暗能量密度参数
    Omega_k: 曲率参数
    """
    # TODO: 计算哈勃参数
    H_squared = H0**2 * (Omega_r/a**4 + Omega_m/a**3 + Omega_k/a**2 + Omega_Lambda)
    return np.sqrt(H_squared)

def hubble_time(H):
    """
    哈勃时间 t_H = 1/H
    """
    return 1 / H

def hubble_distance(H):
    """
    哈勃距离 d_H = c/H
    """
    return c / H


# =============================================================================
# 练习 8.2: 密度参数
# Exercise 8.2: Density Parameters
# =============================================================================
def critical_density(H):
    """
    临界密度 ρ_c = 3H²/(8πG)
    """
    return 3 * H**2 / (8 * np.pi * G)

def density_parameter(rho, rho_c):
    """
    密度参数 Ω = ρ/ρ_c
    """
    return rho / rho_c

def curvature_from_omega(Omega_total):
    """
    从总密度参数推断曲率
    Ω_total = 1: 平坦
    Ω_total > 1: 闭合 (k=+1)
    Ω_total < 1: 开放 (k=-1)
    """
    if np.isclose(Omega_total, 1, rtol=0.01):
        return 0, "平坦"
    elif Omega_total > 1:
        return 1, "闭合"
    else:
        return -1, "开放"


# =============================================================================
# 练习 8.3: 标度因子演化
# Exercise 8.3: Scale Factor Evolution
# =============================================================================
def friedmann_ode(a, t, Omega_m, Omega_r, Omega_Lambda, H0):
    """
    弗里德曼方程的ODE形式
    da/dt = a H(a)
    """
    if a <= 0:
        return 0
    Omega_k = 1 - Omega_m - Omega_r - Omega_Lambda
    H = hubble_parameter(a, Omega_m, Omega_r, Omega_Lambda, Omega_k, H0)
    return a * H

def solve_scale_factor(t_span, Omega_m, Omega_r, Omega_Lambda, H0=H_0_SI, a0=1e-10):
    """
    求解标度因子随时间的演化
    """
    t = np.linspace(t_span[0], t_span[1], 1000)
    a = odeint(friedmann_ode, a0, t, args=(Omega_m, Omega_r, Omega_Lambda, H0))
    return t, a.flatten()

def deceleration_parameter(a, Omega_m, Omega_r, Omega_Lambda, H0=H_0_SI):
    """
    减速参数 q = -aä/(ȧ)² = Ω_r/2 + Ω_m/2 - Ω_Λ（在a=1时）
    """
    q = Omega_r/a**4 / 2 + Omega_m/a**3 / 2 - Omega_Lambda
    H = hubble_parameter(a, Omega_m, Omega_r, Omega_Lambda, 0, H0)
    return q * H0**2 / H**2


# =============================================================================
# 练习 8.4: 宇宙年龄
# Exercise 8.4: Age of the Universe
# =============================================================================
def universe_age(Omega_m, Omega_r, Omega_Lambda, H0=H_0_SI):
    """
    宇宙年龄
    t_0 = ∫₀¹ da/(a H(a))
    """
    def integrand(a):
        if a <= 1e-10:
            return 0
        Omega_k = 1 - Omega_m - Omega_r - Omega_Lambda
        H = hubble_parameter(a, Omega_m, Omega_r, Omega_Lambda, Omega_k, H0)
        return 1 / (a * H)

    t0, _ = quad(integrand, 1e-10, 1, limit=100)
    return t0

def lookback_time(z, Omega_m, Omega_r, Omega_Lambda, H0=H_0_SI):
    """
    回溯时间（从红移z到今天）
    """
    def integrand(z_prime):
        a = 1 / (1 + z_prime)
        Omega_k = 1 - Omega_m - Omega_r - Omega_Lambda
        H = hubble_parameter(a, Omega_m, Omega_r, Omega_Lambda, Omega_k, H0)
        return 1 / ((1 + z_prime) * H)

    t_lb, _ = quad(integrand, 0, z, limit=100)
    return t_lb


# =============================================================================
# 练习 8.5: 共动距离
# Exercise 8.5: Comoving Distance
# =============================================================================
def comoving_distance(z, Omega_m, Omega_r, Omega_Lambda, H0=H_0_SI):
    """
    共动距离
    χ = c ∫₀ᶻ dz'/H(z')
    """
    def integrand(z_prime):
        a = 1 / (1 + z_prime)
        Omega_k = 1 - Omega_m - Omega_r - Omega_Lambda
        H = hubble_parameter(a, Omega_m, Omega_r, Omega_Lambda, Omega_k, H0)
        return c / H

    chi, _ = quad(integrand, 0, z, limit=100)
    return chi

def angular_diameter_distance(z, Omega_m, Omega_r, Omega_Lambda, H0=H_0_SI):
    """
    角直径距离
    d_A = χ/(1+z)
    """
    chi = comoving_distance(z, Omega_m, Omega_r, Omega_Lambda, H0)
    return chi / (1 + z)

def luminosity_distance(z, Omega_m, Omega_r, Omega_Lambda, H0=H_0_SI):
    """
    光度距离
    d_L = χ(1+z) = d_A(1+z)²
    """
    chi = comoving_distance(z, Omega_m, Omega_r, Omega_Lambda, H0)
    return chi * (1 + z)


# =============================================================================
# 练习 8.6: 不同宇宙模型
# Exercise 8.6: Different Cosmological Models
# =============================================================================
def matter_dominated_solution(t, H0):
    """
    物质主导宇宙解析解
    a(t) ∝ t^(2/3)
    """
    t0 = 2 / (3 * H0)
    return (t / t0)**(2/3)

def radiation_dominated_solution(t, H0):
    """
    辐射主导宇宙解析解
    a(t) ∝ t^(1/2)
    """
    t0 = 1 / (2 * H0)
    return (t / t0)**(1/2)

def de_sitter_solution(t, t0, H):
    """
    de Sitter宇宙（暗能量主导）
    a(t) = exp(H(t-t₀))
    """
    return np.exp(H * (t - t0))


# =============================================================================
# 可视化
# =============================================================================
def plot_friedmann():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 标准宇宙学参数
    Omega_m = 0.3
    Omega_r = 8.4e-5
    Omega_Lambda = 0.7

    # 1. 哈勃参数演化
    ax1 = axes[0, 0]
    a = np.linspace(0.01, 2, 200)
    H = [hubble_parameter(ai, Omega_m, Omega_r, Omega_Lambda) for ai in a]

    ax1.semilogy(a, np.array(H)/H_0_SI, 'b-', linewidth=2)
    ax1.axhline(y=1, color='r', linestyle='--', label='H₀')
    ax1.axvline(x=1, color='g', linestyle='--', label='今天')
    ax1.set_xlabel('标度因子 a')
    ax1.set_ylabel('H/H₀')
    ax1.set_title('哈勃参数演化')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 标度因子演化
    ax2 = axes[0, 1]
    # 不同模型
    t_gyr = np.linspace(0.01, 30, 200)  # Gyr
    t_s = t_gyr * 3.15e16  # 秒

    # 数值解
    a_num = []
    for ti in t_s:
        try:
            a_val = odeint(friedmann_ode, 1e-10, [0, ti],
                          args=(Omega_m, Omega_r, Omega_Lambda, H_0_SI))[-1, 0]
            a_num.append(min(a_val, 5))
        except:
            a_num.append(np.nan)

    ax2.plot(t_gyr, a_num, 'b-', linewidth=2, label='ΛCDM')

    # 仅物质
    a_matter = [matter_dominated_solution(ti, H_0_SI) for ti in t_s]
    ax2.plot(t_gyr, a_matter, 'r--', linewidth=2, label='仅物质')

    ax2.axhline(y=1, color='k', linestyle=':', alpha=0.5)
    ax2.set_xlabel('时间 (Gyr)')
    ax2.set_ylabel('标度因子 a')
    ax2.set_title('宇宙膨胀历史')
    ax2.set_ylim(0, 3)
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 减速参数
    ax3 = axes[0, 2]
    q = [deceleration_parameter(ai, Omega_m, Omega_r, Omega_Lambda) for ai in a]
    z = 1/a - 1

    ax3.plot(z[z > 0], np.array(q)[z > 0], 'b-', linewidth=2)
    ax3.axhline(y=0, color='r', linestyle='--')
    ax3.axvline(x=0.67, color='g', linestyle='--', label='加速开始 z≈0.67')
    ax3.set_xlabel('红移 z')
    ax3.set_ylabel('减速参数 q')
    ax3.set_title('加速/减速演化')
    ax3.set_xlim(0, 5)
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 距离-红移关系
    ax4 = axes[1, 0]
    z_vals = np.linspace(0.01, 3, 100)

    d_L = [luminosity_distance(zi, Omega_m, Omega_r, Omega_Lambda) / (3.086e22) for zi in z_vals]  # Mpc
    d_A = [angular_diameter_distance(zi, Omega_m, Omega_r, Omega_Lambda) / (3.086e22) for zi in z_vals]

    ax4.plot(z_vals, d_L, 'b-', linewidth=2, label='光度距离')
    ax4.plot(z_vals, d_A, 'r-', linewidth=2, label='角直径距离')
    ax4.set_xlabel('红移 z')
    ax4.set_ylabel('距离 (Mpc)')
    ax4.set_title('宇宙学距离')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 密度演化
    ax5 = axes[1, 1]
    rho_m = [Omega_m / ai**3 for ai in a]
    rho_r = [Omega_r / ai**4 for ai in a]
    rho_Lambda = [Omega_Lambda for _ in a]

    ax5.semilogy(a, rho_m, 'b-', linewidth=2, label='物质')
    ax5.semilogy(a, rho_r, 'r-', linewidth=2, label='辐射')
    ax5.semilogy(a, rho_Lambda, 'g-', linewidth=2, label='暗能量')
    ax5.axvline(x=1, color='k', linestyle='--', alpha=0.5)
    ax5.set_xlabel('标度因子 a')
    ax5.set_ylabel('Ω_i(a)')
    ax5.set_title('密度参数演化')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. 宇宙组成饼图
    ax6 = axes[1, 2]
    labels = ['暗能量 (Ω_Λ)', '暗物质', '重子物质', '辐射']
    sizes = [Omega_Lambda, 0.26, 0.04, Omega_r]
    colors = ['purple', 'blue', 'orange', 'yellow']

    ax6.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax6.set_title('今天的宇宙组成')

    plt.tight_layout()
    plt.savefig('friedmann.png', dpi=150)
    print("图像已保存为 friedmann.png")
    plt.show()


def verify():
    """
    验证所有练习的正确性
    Verify all exercises for correctness
    """
    all_passed = True

    # 标准宇宙学参数 Standard cosmological parameters
    Omega_m = 0.3       # 物质
    Omega_r = 8.4e-5    # 辐射
    Omega_Lambda = 0.7  # 暗能量

    # 检查 8.1 - 哈勃参数 Hubble parameter
    H_today = hubble_parameter(1, Omega_m, Omega_r, Omega_Lambda)
    if not np.isclose(H_today, H_0_SI, rtol=0.01):
        print("错误 8.1: 今天(a=1)的哈勃参数应等于 H_0")
        all_passed = False
    else:
        print(f"正确 8.1: 哈勃参数 (H_0 = {H_0} km/s/Mpc)")

    # 检查 8.2 - 临界密度 Critical density
    rho_c = critical_density(H_0_SI)
    expected_rho_c = 3 * H_0_SI**2 / (8 * np.pi * G)
    if not np.isclose(rho_c, expected_rho_c, rtol=0.01):
        print("错误 8.2: 临界密度计算不正确，请检查公式 rho_c = 3H²/(8πG)")
        all_passed = False
    else:
        print(f"正确 8.2: 临界密度 (rho_c = {rho_c:.2e} kg/m³)")

    # 检查 8.3 - 标度因子演化/减速参数 Scale factor evolution
    q = deceleration_parameter(1, Omega_m, Omega_r, Omega_Lambda)
    if q >= 0:
        print("错误 8.3: 当前宇宙应在加速膨胀，减速参数 q < 0")
        all_passed = False
    else:
        print(f"正确 8.3: 标度因子演化 (q_0 = {q:.3f}，宇宙在加速膨胀)")

    # 检查 8.4 - 宇宙年龄 Universe age
    t0 = universe_age(Omega_m, Omega_r, Omega_Lambda)
    t0_gyr = t0 / (3.15e16)  # 转换为 Gyr
    if not (12 < t0_gyr < 15):
        print(f"错误 8.4: 宇宙年龄应在12-15 Gyr之间，得到 {t0_gyr:.1f} Gyr")
        all_passed = False
    else:
        print(f"正确 8.4: 宇宙年龄 (t_0 = {t0_gyr:.2f} Gyr)")

    # 检查 8.5 - 距离对偶关系 Distance duality relation
    d_L = luminosity_distance(1, Omega_m, Omega_r, Omega_Lambda)
    d_A = angular_diameter_distance(1, Omega_m, Omega_r, Omega_Lambda)
    # 距离对偶: d_L = (1+z)² d_A
    if not np.isclose(d_L, d_A * 4, rtol=0.01):  # z=1 时 (1+z)² = 4
        print("错误 8.5: 距离对偶关系 d_L = (1+z)² d_A 未满足")
        all_passed = False
    else:
        print(f"正确 8.5: 共动距离 (d_L(z=1) = {d_L/3.086e25:.2f} Gpc)")

    # 检查 8.6 - 解析解 Analytic solutions
    a_m = matter_dominated_solution(1e17, H_0_SI)
    if a_m <= 0:
        print("错误 8.6: 物质主导解析解应为正值")
        all_passed = False
    else:
        print(f"正确 8.6: 解析解 (物质主导宇宙)")

    if all_passed:
        print("\n所有测试通过！")
        try:
            plot_friedmann()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("弗里德曼方程详解 Friedmann Equations Detailed")
    print("=" * 50)
    verify()
