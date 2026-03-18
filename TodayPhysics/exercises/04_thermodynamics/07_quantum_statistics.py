"""
量子统计 Quantum Statistics
难度 Difficulty: ★★★★

学习目标 Learning Objectives:
- 理解玻色-爱因斯坦和费米-狄拉克分布的物理根源
  Understand physical origins of Bose-Einstein and Fermi-Dirac distributions
- 掌握玻色-爱因斯坦凝聚（BEC）现象
  Master Bose-Einstein condensation phenomenon
- 分析金属中的自由电子气体（费米气体）
  Analyze free electron gas in metals (Fermi gas)
- 理解光子气体和黑体辐射（普朗克分布）
  Understand photon gas and blackbody radiation (Planck distribution)
- 学习声子气体和德拜热容模型
  Learn phonon gas and Debye heat capacity model

物理背景 Physical Background:
量子统计考虑了量子力学中粒子的全同性原理。根据自旋，粒子分为：
- 费米子（半整数自旋）：遵守泡利不相容原理，每个量子态最多一个粒子
- 玻色子（整数自旋）：不受泡利原理限制，可以任意多粒子占据同一态

这导致了截然不同的低温行为：
- 费米气体即使在绝对零度也有压强（简并压）
- 玻色气体在临界温度以下发生凝聚（BEC）

HINT: 费米分布: n_FD = 1/(exp((E-μ)/kT) + 1)，E=μ时 n=0.5
HINT: 玻色分布: n_BE = 1/(exp((E-μ)/kT) - 1)，需要 E > μ
HINT: 光子和声子是玻色子，化学势为零
HINT: 费米能: E_F = (hbar²/2m)(3π²n)^(2/3)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.special import zeta
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import k_B, hbar, m_e, c, h

# I AM NOT DONE

# =============================================================================
# 练习 7.1: 量子分布函数
# Exercise 7.1: Quantum Distribution Functions
# =============================================================================
def bose_einstein_distribution(epsilon, mu, T):
    """
    玻色-爱因斯坦分布
    n_BE = 1/(exp((ε-μ)/(k_BT)) - 1)
    """
    if T == 0:
        return np.inf if epsilon <= mu else 0
    x = (epsilon - mu) / (k_B * T)
    if x > 700:  # 避免溢出
        return 0
    return 1 / (np.exp(x) - 1)

def fermi_dirac_distribution(epsilon, mu, T):
    """
    费米-狄拉克分布
    n_FD = 1/(exp((ε-μ)/(k_BT)) + 1)
    """
    if T == 0:
        return 1 if epsilon < mu else 0
    x = (epsilon - mu) / (k_B * T)
    if x > 700:
        return 0
    if x < -700:
        return 1
    return 1 / (np.exp(x) + 1)

def maxwell_boltzmann_distribution(epsilon, mu, T):
    """
    麦克斯韦-玻尔兹曼分布（经典极限）
    n_MB = exp(-(ε-μ)/(k_BT))
    """
    if T == 0:
        return 0
    x = (epsilon - mu) / (k_B * T)
    if x > 700:
        return 0
    return np.exp(-x)


# =============================================================================
# 练习 7.2: 费米气体
# Exercise 7.2: Fermi Gas
# =============================================================================
def fermi_energy(n, m=m_e):
    """
    费米能量
    E_F = (ℏ²/2m)(3π²n)^(2/3)
    n: 电子密度
    """
    return (hbar**2 / (2 * m)) * (3 * np.pi**2 * n)**(2/3)

def fermi_temperature(E_F):
    """
    费米温度
    T_F = E_F / k_B
    """
    return E_F / k_B

def fermi_momentum(n):
    """
    费米动量
    p_F = ℏ(3π²n)^(1/3)
    """
    return hbar * (3 * np.pi**2 * n)**(1/3)

def fermi_velocity(n, m=m_e):
    """
    费米速度
    v_F = p_F/m = ℏ(3π²n)^(1/3)/m
    """
    return fermi_momentum(n) / m


# =============================================================================
# 练习 7.3: 电子气体热容
# Exercise 7.3: Electron Gas Heat Capacity
# =============================================================================
def electronic_heat_capacity(T, T_F, n, V):
    """
    电子气体热容（低温近似）
    C_V = (π²/2) N k_B (T/T_F)
    """
    N = n * V
    return (np.pi**2 / 2) * N * k_B * (T / T_F)

def sommerfeld_coefficient(n, T_F):
    """
    索末菲系数 γ
    C_V = γT
    γ = (π²/2) n k_B / T_F
    """
    return (np.pi**2 / 2) * n * k_B / T_F

def degeneracy_pressure(n, m=m_e):
    """
    费米简并压
    P = (2/5) n E_F = (ℏ²/5m)(3π²)^(2/3) n^(5/3)
    """
    E_F = fermi_energy(n, m)
    return (2/5) * n * E_F


# =============================================================================
# 练习 7.4: 玻色-爱因斯坦凝聚
# Exercise 7.4: Bose-Einstein Condensation
# =============================================================================
def bec_critical_temperature(n, m):
    """
    BEC临界温度
    T_c = (2πℏ²/mk_B)(n/ζ(3/2))^(2/3)
    ζ(3/2) ≈ 2.612
    """
    zeta_3_2 = 2.612
    return (2 * np.pi * hbar**2 / (m * k_B)) * (n / zeta_3_2)**(2/3)

def bec_condensate_fraction(T, Tc):
    """
    凝聚体分数
    N_0/N = 1 - (T/T_c)^(3/2)
    """
    if T >= Tc:
        return 0
    return 1 - (T / Tc)**(3/2)

def thermal_de_broglie_wavelength(T, m):
    """
    热德布罗意波长
    λ_th = h/√(2πmk_BT)
    """
    return h / np.sqrt(2 * np.pi * m * k_B * T)

def phase_space_density(n, lambda_th):
    """
    相空间密度
    nλ³ ≥ ζ(3/2) 时发生BEC
    """
    return n * lambda_th**3


# =============================================================================
# 练习 7.5: 光子气体
# Exercise 7.5: Photon Gas
# =============================================================================
def planck_distribution(nu, T):
    """
    普朗克分布（光谱能量密度）
    u(ν) = (8πhν³/c³) × 1/(exp(hν/k_BT) - 1)
    """
    x = h * nu / (k_B * T)
    if x > 700:
        return 0
    return (8 * np.pi * h * nu**3 / c**3) / (np.exp(x) - 1)

def stefan_boltzmann_law(T):
    """
    斯特藩-玻尔兹曼定律
    u = aT⁴ = 4σT⁴/c
    σ = 5.67 × 10⁻⁸ W/(m²K⁴)
    """
    sigma = 5.67e-8
    return 4 * sigma * T**4 / c

def wien_displacement_law(T):
    """
    维恩位移定律
    λ_max T = 2.898 × 10⁻³ m·K
    返回峰值波长
    """
    b = 2.898e-3  # Wien常数
    return b / T

def photon_number_density(T):
    """
    光子数密度
    n = 2ζ(3)(k_BT/ℏc)³/π²
    ζ(3) ≈ 1.202
    """
    zeta_3 = 1.202
    return 2 * zeta_3 * (k_B * T / (hbar * c))**3 / np.pi**2


# =============================================================================
# 练习 7.6: 声子气体
# Exercise 7.6: Phonon Gas
# =============================================================================
def debye_heat_capacity(T, Theta_D, N):
    """
    德拜热容（近似）
    C_V = 9Nk_B(T/Θ_D)³ ∫₀^(Θ_D/T) x⁴eˣ/(eˣ-1)² dx
    """
    if T == 0:
        return 0

    x_D = Theta_D / T

    # 低温极限
    if x_D > 10:
        return (12 * np.pi**4 / 5) * N * k_B * (T / Theta_D)**3

    # 高温极限
    if x_D < 0.1:
        return 3 * N * k_B

    # 数值积分
    def integrand(x):
        if x < 1e-10:
            return x**2
        ex = np.exp(x)
        return x**4 * ex / (ex - 1)**2

    integral, _ = quad(integrand, 0, x_D)
    return 9 * N * k_B * (T / Theta_D)**3 * integral

def debye_temperature_from_sound(v_s, n):
    """
    从声速估计德拜温度
    Θ_D = (ℏv_s/k_B)(6π²n)^(1/3)
    """
    return (hbar * v_s / k_B) * (6 * np.pi**2 * n)**(1/3)

def phonon_mean_energy(T, Theta_D):
    """
    平均声子能量
    ⟨E⟩ = k_B T × f(Θ_D/T)
    """
    if T == 0:
        return 0
    x = Theta_D / T
    if x > 700:
        return 0
    return k_B * T / (np.exp(x) - 1) * x


# =============================================================================
# 可视化
# =============================================================================
def plot_quantum_statistics():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 三种分布比较
    ax1 = axes[0, 0]
    T = 300  # K
    mu = 0
    epsilon = np.linspace(-0.2, 1.0, 200) * k_B * T

    n_be = [bose_einstein_distribution(e, mu - 0.1*k_B*T, T) if e > mu - 0.1*k_B*T else 10
            for e in epsilon]
    n_fd = [fermi_dirac_distribution(e, mu, T) for e in epsilon]
    n_mb = [maxwell_boltzmann_distribution(e, mu, T) for e in epsilon]

    ax1.plot(epsilon/(k_B*T), n_fd, 'b-', label='费米-狄拉克', linewidth=2)
    ax1.plot(epsilon/(k_B*T), n_be, 'r-', label='玻色-爱因斯坦', linewidth=2)
    ax1.plot(epsilon/(k_B*T), n_mb, 'g--', label='麦克斯韦-玻尔兹曼', linewidth=2)
    ax1.set_xlabel('(ε-μ)/(k_BT)')
    ax1.set_ylabel('⟨n⟩')
    ax1.set_title('量子分布函数')
    ax1.set_ylim(0, 5)
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 费米分布温度依赖
    ax2 = axes[0, 1]
    E_F = 5.0  # eV (代表能量尺度)
    T_F = E_F * 1.6e-19 / k_B  # 费米温度

    epsilon = np.linspace(0, 2 * E_F, 200)

    for T_ratio in [0.01, 0.1, 0.5, 1.0]:
        T = T_ratio * T_F
        n = [fermi_dirac_distribution(e * 1.6e-19, E_F * 1.6e-19, T) for e in epsilon]
        ax2.plot(epsilon/E_F, n, label=f'T/T_F = {T_ratio}', linewidth=2)

    ax2.axvline(x=1, color='k', linestyle='--', alpha=0.5)
    ax2.set_xlabel('ε/E_F')
    ax2.set_ylabel('f(ε)')
    ax2.set_title('费米分布温度依赖')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. BEC凝聚分数
    ax3 = axes[0, 2]
    T_ratio = np.linspace(0, 1.5, 100)

    N0_N = [bec_condensate_fraction(t, 1) for t in T_ratio]

    ax3.plot(T_ratio, N0_N, 'b-', linewidth=2)
    ax3.axvline(x=1, color='r', linestyle='--', alpha=0.5, label='T_c')
    ax3.fill_between(T_ratio, 0, N0_N, alpha=0.3)
    ax3.set_xlabel('T/T_c')
    ax3.set_ylabel('N₀/N')
    ax3.set_title('玻色-爱因斯坦凝聚')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 普朗克分布
    ax4 = axes[1, 0]

    for T in [3000, 4000, 5000, 6000]:
        nu = np.logspace(13, 16, 500)
        u = [planck_distribution(n, T) for n in nu]
        ax4.loglog(nu, u, label=f'T = {T} K', linewidth=1.5)

    ax4.set_xlabel('频率 (Hz)')
    ax4.set_ylabel('u(ν) (J/m³/Hz)')
    ax4.set_title('普朗克黑体辐射')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 德拜热容
    ax5 = axes[1, 1]
    Theta_D = 400  # K (典型值)
    T = np.linspace(1, 500, 100)
    N = 6.022e23  # 1 mol

    C_V = [debye_heat_capacity(t, Theta_D, N) / (N * k_B) for t in T]

    ax5.plot(T/Theta_D, C_V, 'b-', linewidth=2)
    ax5.axhline(y=3, color='r', linestyle='--', alpha=0.5, label='Dulong-Petit')
    ax5.set_xlabel('T/Θ_D')
    ax5.set_ylabel('C_V/(Nk_B)')
    ax5.set_title('德拜热容')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. 电子气体性质
    ax6 = axes[1, 2]
    # 金属电子密度
    n = np.logspace(28, 29, 50)  # m⁻³

    E_F_vals = [fermi_energy(ni) / (1.6e-19) for ni in n]  # eV
    T_F_vals = [fermi_temperature(fermi_energy(ni)) for ni in n]  # K

    ax6.loglog(n, E_F_vals, 'b-', label='E_F (eV)', linewidth=2)
    ax6.set_xlabel('电子密度 (m⁻³)')
    ax6.set_ylabel('费米能 (eV)')
    ax6.set_title('金属费米能')

    ax6_twin = ax6.twinx()
    ax6_twin.loglog(n, T_F_vals, 'r--', label='T_F (K)', linewidth=2)
    ax6_twin.set_ylabel('费米温度 (K)', color='r')

    ax6.legend(loc='upper left')
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('quantum_statistics.png', dpi=150)
    print("图像已保存为 quantum_statistics.png")
    plt.show()


def verify():
    all_passed = True

    # Check 7.1
    T = 300
    mu = 0
    n_fd = fermi_dirac_distribution(mu, mu, T)
    if not np.isclose(n_fd, 0.5, rtol=0.01):
        print("❌ 7.1 费米分布在ε=μ处应为0.5")
        all_passed = False
    else:
        print("✓ 7.1 量子分布函数正确")

    # Check 7.2
    n = 8.5e28  # 铜的电子密度
    E_F = fermi_energy(n)
    expected_EF = 7.0 * 1.6e-19  # ~7 eV
    if not np.isclose(E_F, expected_EF, rtol=0.15):
        print(f"❌ 7.2 铜的费米能应约为7 eV, 得到 {E_F/1.6e-19:.1f} eV")
        all_passed = False
    else:
        print(f"✓ 7.2 费米气体正确 (E_F(Cu) ≈ {E_F/1.6e-19:.1f} eV)")

    # Check 7.3
    T_F = fermi_temperature(E_F)
    gamma = sommerfeld_coefficient(n, T_F)
    if gamma <= 0:
        print("❌ 7.3 索末菲系数应为正")
        all_passed = False
    else:
        print(f"✓ 7.3 电子热容正确 (γ = {gamma:.2e} J/(m³·K²))")

    # Check 7.4
    # 铷原子BEC
    m_Rb = 87 * 1.66e-27  # kg
    n_Rb = 1e19  # m⁻³
    Tc = bec_critical_temperature(n_Rb, m_Rb)
    if Tc <= 0 or Tc > 1e-3:
        print("❌ 7.4 BEC临界温度不合理")
        all_passed = False
    else:
        print(f"✓ 7.4 BEC正确 (T_c ≈ {Tc*1e9:.0f} nK)")

    # Check 7.5
    T = 5778  # 太阳表面温度
    lambda_max = wien_displacement_law(T)
    expected = 500e-9  # ~500 nm
    if not np.isclose(lambda_max, expected, rtol=0.1):
        print("❌ 7.5 维恩位移定律错误")
        all_passed = False
    else:
        print(f"✓ 7.5 光子气体正确 (λ_max(太阳) ≈ {lambda_max*1e9:.0f} nm)")

    # Check 7.6
    # 德拜热容高温极限
    N = 6.022e23
    C_high_T = debye_heat_capacity(1000, 400, N)
    expected_C = 3 * N * k_B
    if not np.isclose(C_high_T, expected_C, rtol=0.1):
        print("❌ 7.6 德拜热容高温极限应为3Nk_B")
        all_passed = False
    else:
        print("✓ 7.6 声子气体正确 (C_V → 3Nk_B)")

    if all_passed:
        print("\n🎉 所有测试通过！")
        try:
            plot_quantum_statistics()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("量子统计 Quantum Statistics")
    print("=" * 50)
    verify()
