"""
非平衡态热力学 Non-equilibrium Thermodynamics
难度 Difficulty: ★★★★

学习目标 Learning Objectives:
- 理解熵产生和不可逆过程
- 掌握Onsager关系
- 分析热电效应和耦合输运

HINT: 熵产生率: σ = Σᵢ JᵢXᵢ ≥ 0
HINT: Onsager关系: Lᵢⱼ = Lⱼᵢ
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import k_B, e

# I AM NOT DONE

# =============================================================================
# 练习 8.1: 熵产生
# Exercise 8.1: Entropy Production
# =============================================================================
def entropy_production_rate(J, X):
    """
    熵产生率（局域）
    σ = Σᵢ Jᵢ × Xᵢ
    J: 流（热流、粒子流等）
    X: 热力学力（温度梯度、化学势梯度等）
    """
    return np.sum(np.array(J) * np.array(X))

def heat_conduction_entropy(J_q, T, grad_T):
    """
    热传导的熵产生
    σ = J_q × (-∇T/T²)
    """
    X_q = -grad_T / T**2
    return J_q * X_q

def diffusion_entropy(J_n, grad_mu, T):
    """
    扩散的熵产生
    σ = J_n × (-∇μ/T)
    """
    X_n = -grad_mu / T
    return J_n * X_n


# =============================================================================
# 练习 8.2: 线性唯象关系
# Exercise 8.2: Linear Phenomenological Relations
# =============================================================================
def linear_flux(L, X):
    """
    线性输运关系
    Jᵢ = Σⱼ Lᵢⱼ Xⱼ
    L: Onsager系数矩阵
    X: 热力学力向量
    """
    return np.dot(L, X)

def onsager_matrix_2x2(L11, L12, L22):
    """
    构造满足Onsager互易关系的2×2矩阵
    L₁₂ = L₂₁
    """
    return np.array([[L11, L12],
                     [L12, L22]])

def verify_onsager_reciprocity(L):
    """
    验证Onsager互易关系
    Lᵢⱼ = Lⱼᵢ
    """
    return np.allclose(L, L.T)


# =============================================================================
# 练习 8.3: 热电效应
# Exercise 8.3: Thermoelectric Effects
# =============================================================================
def seebeck_coefficient(delta_V, delta_T):
    """
    塞贝克系数
    S = -ΔV/ΔT (开路条件)
    """
    return -delta_V / delta_T

def peltier_coefficient(S, T):
    """
    珀尔帖系数
    Π = ST (开尔文关系)
    """
    return S * T

def thomson_coefficient(S, T, dS_dT):
    """
    汤姆孙系数
    τ = T × dS/dT
    """
    return T * dS_dT

def thermoelectric_figure_of_merit(S, sigma, kappa, T):
    """
    热电优值
    ZT = S²σT/κ
    S: 塞贝克系数
    σ: 电导率
    κ: 热导率
    """
    return S**2 * sigma * T / kappa


# =============================================================================
# 练习 8.4: 热电器件
# Exercise 8.4: Thermoelectric Devices
# =============================================================================
def thermoelectric_efficiency_max(ZT, T_h, T_c):
    """
    热电发电机最大效率
    η_max = (T_h-T_c)/T_h × (√(1+ZT)-1)/(√(1+ZT)+T_c/T_h)
    """
    carnot = (T_h - T_c) / T_h
    sqrt_1_ZT = np.sqrt(1 + ZT)
    return carnot * (sqrt_1_ZT - 1) / (sqrt_1_ZT + T_c / T_h)

def thermoelectric_cop_max(ZT, T_h, T_c):
    """
    热电制冷机最大COP
    COP_max = T_c/(T_h-T_c) × (√(1+ZT)-T_h/T_c)/(√(1+ZT)+1)
    """
    carnot_cop = T_c / (T_h - T_c)
    sqrt_1_ZT = np.sqrt(1 + ZT)
    return carnot_cop * (sqrt_1_ZT - T_h / T_c) / (sqrt_1_ZT + 1)

def peltier_cooling_rate(I, Pi, R, K, delta_T):
    """
    珀尔帖制冷率
    Q_c = ΠI - I²R/2 - KΔT
    Π: 珀尔帖系数
    R: 电阻
    K: 热导
    """
    return Pi * np.abs(I) - I**2 * R / 2 - K * delta_T


# =============================================================================
# 练习 8.5: 扩散与迁移
# Exercise 8.5: Diffusion and Drift
# =============================================================================
def einstein_relation(D, T):
    """
    爱因斯坦关系
    D/μ = k_BT/e
    返回迁移率 μ = eD/(k_BT)
    """
    return e * D / (k_B * T)

def nernst_einstein_conductivity(n, D, T):
    """
    Nernst-Einstein电导率
    σ = ne²D/(k_BT)
    """
    return n * e**2 * D / (k_B * T)

def drift_diffusion_current(n, mu, E, D, grad_n):
    """
    漂移-扩散电流密度
    J = neμE - eD∇n
    """
    return n * e * mu * E - e * D * grad_n

def ionic_conductivity_arrhenius(sigma_0, E_a, T):
    """
    离子电导率的阿伦尼乌斯关系
    σ = σ₀ exp(-E_a/(k_BT))
    """
    return sigma_0 * np.exp(-E_a / (k_B * T))


# =============================================================================
# 练习 8.6: 涨落耗散定理
# Exercise 8.6: Fluctuation-Dissipation Theorem
# =============================================================================
def nyquist_noise_power(R, T, bandwidth):
    """
    尼奎斯特噪声功率
    P = 4k_BTR × Δf
    """
    return 4 * k_B * T * R * bandwidth

def johnson_noise_voltage(R, T, bandwidth):
    """
    约翰逊噪声电压（RMS）
    V_rms = √(4k_BTRΔf)
    """
    return np.sqrt(4 * k_B * T * R * bandwidth)

def fluctuation_dissipation_susceptibility(chi_static, omega, gamma, T):
    """
    涨落耗散定理：响应函数与涨落谱关系
    S(ω) = (2k_BT/ω) Im[χ(ω)]
    """
    # 简化的Lorentzian响应
    chi_imag = chi_static * omega * gamma / (omega**2 + gamma**2)
    return (2 * k_B * T / omega) * chi_imag if omega != 0 else 0

def brownian_diffusion(T, eta, r):
    """
    布朗粒子扩散系数（Stokes-Einstein）
    D = k_BT/(6πηr)
    """
    return k_B * T / (6 * np.pi * eta * r)


# =============================================================================
# 可视化
# =============================================================================
def plot_nonequilibrium():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 熵产生vs不可逆性
    ax1 = axes[0, 0]
    grad_T = np.linspace(0.1, 10, 100)  # K/m
    T = 300  # K
    kappa = 400  # W/(m·K) 铜

    # 傅里叶定律: J_q = -κ∇T
    J_q = kappa * grad_T
    sigma = [heat_conduction_entropy(j, T, g) for j, g in zip(J_q, grad_T)]

    ax1.plot(grad_T, sigma, 'b-', linewidth=2)
    ax1.set_xlabel('温度梯度 (K/m)')
    ax1.set_ylabel('熵产生率 (W/(m³·K))')
    ax1.set_title('热传导熵产生')
    ax1.grid(True, alpha=0.3)

    # 2. 热电效率vs ZT
    ax2 = axes[0, 1]
    ZT = np.linspace(0.1, 5, 100)
    T_h, T_c = 600, 300

    eta = [thermoelectric_efficiency_max(zt, T_h, T_c) * 100 for zt in ZT]
    carnot = (T_h - T_c) / T_h * 100

    ax2.plot(ZT, eta, 'b-', linewidth=2, label='热电效率')
    ax2.axhline(y=carnot, color='r', linestyle='--', label=f'卡诺效率 ({carnot:.0f}%)')
    ax2.set_xlabel('ZT')
    ax2.set_ylabel('效率 (%)')
    ax2.set_title('热电发电机效率')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 珀尔帖制冷
    ax3 = axes[0, 2]
    I = np.linspace(0, 5, 100)
    Pi = 0.05  # V
    R = 0.01  # Ω
    K = 1     # W/K
    delta_T = 20  # K

    Q_c = [peltier_cooling_rate(i, Pi, R, K, delta_T) for i in I]

    ax3.plot(I, Q_c, 'b-', linewidth=2)
    ax3.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax3.set_xlabel('电流 (A)')
    ax3.set_ylabel('制冷功率 (W)')
    ax3.set_title('珀尔帖制冷')
    ax3.grid(True, alpha=0.3)

    # 4. 离子电导率温度依赖
    ax4 = axes[1, 0]
    T = np.linspace(300, 1000, 100)
    E_a = 0.5 * 1.6e-19  # 0.5 eV
    sigma_0 = 1e6  # S/m

    sigma = [ionic_conductivity_arrhenius(sigma_0, E_a, t) for t in T]

    ax4.semilogy(1000/T, sigma, 'b-', linewidth=2)
    ax4.set_xlabel('1000/T (K⁻¹)')
    ax4.set_ylabel('电导率 (S/m)')
    ax4.set_title('阿伦尼乌斯电导率')
    ax4.grid(True, alpha=0.3)

    # 5. 约翰逊噪声
    ax5 = axes[1, 1]
    R_range = np.logspace(1, 6, 100)  # 10 Ω to 1 MΩ
    T = 300
    bandwidth = 1e6  # 1 MHz

    V_noise = [johnson_noise_voltage(r, T, bandwidth) * 1e6 for r in R_range]  # μV

    ax5.loglog(R_range/1e3, V_noise, 'b-', linewidth=2)
    ax5.set_xlabel('电阻 (kΩ)')
    ax5.set_ylabel('噪声电压 (μV)')
    ax5.set_title(f'约翰逊噪声 (T={T}K, Δf=1MHz)')
    ax5.grid(True, alpha=0.3)

    # 6. 布朗运动扩散
    ax6 = axes[1, 2]
    r = np.logspace(-9, -6, 100)  # 1nm to 1μm
    T = 300
    eta = 1e-3  # 水的粘度

    D = [brownian_diffusion(T, eta, ri) for ri in r]

    ax6.loglog(r * 1e9, D, 'b-', linewidth=2)
    ax6.set_xlabel('粒子半径 (nm)')
    ax6.set_ylabel('扩散系数 (m²/s)')
    ax6.set_title('布朗粒子扩散')
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('nonequilibrium.png', dpi=150)
    print("图像已保存为 nonequilibrium.png")
    plt.show()


def verify():
    all_passed = True

    # Check 8.1
    J = [1, 2]
    X = [0.1, 0.2]
    sigma = entropy_production_rate(J, X)
    expected = 0.1 + 0.4
    if not np.isclose(sigma, expected, rtol=0.01):
        print("❌ 8.1 熵产生率计算错误")
        all_passed = False
    elif sigma < 0:
        print("❌ 8.1 熵产生率应非负")
        all_passed = False
    else:
        print(f"✓ 8.1 熵产生正确 (σ = {sigma:.2f})")

    # Check 8.2
    L = onsager_matrix_2x2(1.0, 0.5, 2.0)
    if not verify_onsager_reciprocity(L):
        print("❌ 8.2 Onsager矩阵不满足互易关系")
        all_passed = False
    else:
        print("✓ 8.2 Onsager关系正确")

    # Check 8.3
    S = -200e-6  # V/K (典型n型半导体)
    T = 300
    Pi = peltier_coefficient(S, T)
    if not np.isclose(Pi, S * T, rtol=0.01):
        print("❌ 8.3 开尔文关系错误")
        all_passed = False
    else:
        print(f"✓ 8.3 热电效应正确 (Π = ST = {Pi*1000:.1f} mV)")

    # Check 8.4
    ZT = 1.0
    eta = thermoelectric_efficiency_max(ZT, 600, 300)
    if eta <= 0 or eta >= (600-300)/600:
        print("❌ 8.4 热电效率应在0和卡诺效率之间")
        all_passed = False
    else:
        print(f"✓ 8.4 热电器件正确 (η = {eta*100:.1f}%)")

    # Check 8.5
    D = 1e-9  # m²/s
    mu = einstein_relation(D, 300)
    expected_mu = e * D / (k_B * 300)
    if not np.isclose(mu, expected_mu, rtol=0.01):
        print("❌ 8.5 爱因斯坦关系错误")
        all_passed = False
    else:
        print(f"✓ 8.5 扩散迁移正确 (μ = {mu:.2e} m²/(V·s))")

    # Check 8.6
    V_noise = johnson_noise_voltage(1e3, 300, 1e6)
    if V_noise <= 0:
        print("❌ 8.6 约翰逊噪声应为正")
        all_passed = False
    else:
        print(f"✓ 8.6 涨落耗散正确 (V_noise = {V_noise*1e6:.2f} μV)")

    if all_passed:
        print("\n🎉 所有测试通过！")
        try:
            plot_nonequilibrium()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("非平衡态热力学 Non-equilibrium Thermodynamics")
    print("=" * 50)
    verify()
