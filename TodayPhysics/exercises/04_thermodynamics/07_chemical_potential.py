"""
化学势与吉布斯能 Chemical Potential and Gibbs Free Energy
难度 Difficulty: ★★★★

学习目标 Learning Objectives:
- 理解化学势的物理意义（粒子流动的驱动力）
  Understand physical meaning of chemical potential (driving force for particle flow)
- 掌握吉布斯自由能及其在判断自发过程中的应用
  Master Gibbs free energy and its application in determining spontaneous processes
- 分析相平衡条件和化学平衡条件
  Analyze phase equilibrium and chemical equilibrium conditions
- 理解溶液的非理想行为（活度、活度系数）
  Understand non-ideal behavior of solutions (activity, activity coefficient)
- 学习量子统计中的化学势（费米能等）
  Learn chemical potential in quantum statistics (Fermi energy, etc.)

物理背景 Physical Background:
化学势 μ 是单个粒子（或单位物质的量）的吉布斯自由能。它描述了
向系统添加一个粒子所需的自由能变化。

当两个系统接触时，粒子会从化学势高的一方流向化学势低的一方，
直到两边化学势相等（平衡）。这是相平衡和化学平衡的核心条件。

对于理想气体，化学势与压强的对数成线性关系。对于实际系统，
用逸度（fugacity）或活度（activity）来修正。

HINT: 化学势定义: μ = (∂G/∂N)_{T,P} = G_m（摩尔吉布斯能）
HINT: 相平衡条件: μ_α = μ_β（各相化学势相等）
HINT: 化学平衡条件: Σᵢ νᵢ μᵢ = 0
HINT: 理想气体: μ = μ⁰ + RT ln(P/P⁰)
HINT: Gibbs相律: F = C - P + 2（自由度 = 组分数 - 相数 + 2）
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import k_B, N_A, R, eV

# I AM NOT DONE

# =============================================================================
# 练习 7.1: 化学势基础
# Exercise 7.1: Chemical Potential Basics
# =============================================================================
def chemical_potential_ideal_gas(T, P, P0, mu0):
    """
    理想气体化学势
    μ = μ⁰(T) + k_BT ln(P/P⁰)
    """
    return mu0 + k_B * T * np.log(P / P0)


def chemical_potential_from_fugacity(T, f, f0, mu0):
    """
    实际气体化学势（用逸度）
    μ = μ⁰(T) + k_BT ln(f/f⁰)
    """
    return mu0 + k_B * T * np.log(f / f0)


def chemical_potential_solid(T, P, V_m, mu0):
    """
    固体化学势（近似不可压缩）
    μ = μ⁰(T) + V_m(P - P⁰)
    V_m: 摩尔体积
    """
    P0 = 1e5  # 标准压强
    return mu0 + V_m * (P - P0) / N_A


def sackur_tetrode_mu(T, P, m):
    """
    理想单原子气体化学势（Sackur-Tetrode）
    μ/k_BT = ln(nλ³) where λ = h/√(2πmk_BT)
    """
    h = 6.626e-34
    n = P / (k_B * T)  # 数密度
    thermal_wavelength = h / np.sqrt(2 * np.pi * m * k_B * T)
    return k_B * T * np.log(n * thermal_wavelength**3)


def electrochemical_potential(mu, z, phi):
    """
    电化学势
    μ̃ = μ + zeφ
    z: 电荷数
    φ: 电势
    """
    e = 1.6e-19
    return mu + z * e * phi


# =============================================================================
# 练习 7.2: 吉布斯自由能
# Exercise 7.2: Gibbs Free Energy
# =============================================================================
def gibbs_free_energy(U, P, V, T, S):
    """
    吉布斯自由能
    G = U + PV - TS = H - TS
    """
    return U + P * V - T * S


def gibbs_per_mole(H_m, T, S_m):
    """
    摩尔吉布斯能
    G_m = H_m - TS_m
    """
    return H_m - T * S_m


def gibbs_duhem_relation():
    """
    Gibbs-Duhem关系
    S dT - V dP + Σ N_i dμ_i = 0
    """
    return "SdT - VdP + Σ N_i dμ_i = 0"


def gibbs_energy_mixing_ideal(n1, n2, T):
    """
    理想混合的吉布斯能变化
    ΔG_mix = RT(n1 ln x1 + n2 ln x2)
    """
    n_total = n1 + n2
    x1 = n1 / n_total
    x2 = n2 / n_total

    # 避免log(0)
    if x1 > 0 and x2 > 0:
        return R * T * (n1 * np.log(x1) + n2 * np.log(x2))
    return 0


def entropy_mixing_ideal(n1, n2):
    """
    理想混合熵变
    ΔS_mix = -R(n1 ln x1 + n2 ln x2)
    """
    n_total = n1 + n2
    x1 = n1 / n_total
    x2 = n2 / n_total

    if x1 > 0 and x2 > 0:
        return -R * (n1 * np.log(x1) + n2 * np.log(x2))
    return 0


# =============================================================================
# 练习 7.3: 相平衡
# Exercise 7.3: Phase Equilibrium
# =============================================================================
def clausius_clapeyron(dP_dT, Delta_H, T, Delta_V):
    """
    Clausius-Clapeyron方程
    dP/dT = ΔH/(TΔV)
    """
    return Delta_H / (T * Delta_V)


def vapor_pressure_clausius_clapeyron(T, T0, P0, Delta_H_vap):
    """
    蒸汽压（Clausius-Clapeyron积分）
    ln(P/P₀) = -(ΔH_vap/R)(1/T - 1/T₀)
    """
    return P0 * np.exp(-(Delta_H_vap/R) * (1/T - 1/T0))


def antoine_equation(T, A, B, C):
    """
    Antoine方程（蒸汽压经验公式）
    log₁₀(P) = A - B/(T + C)
    P in mmHg, T in °C
    """
    return 10**(A - B / (T + C))


def raoult_law(P_star, x):
    """
    Raoult定律
    P = x × P*
    x: 摩尔分数
    P*: 纯组分蒸汽压
    """
    return x * P_star


def henry_law(k_H, x):
    """
    Henry定律
    P = k_H × x
    k_H: Henry常数
    """
    return k_H * x


def phase_rule(C, P_phases, F):
    """
    Gibbs相律
    F = C - P + 2
    F: 自由度
    C: 组分数
    P: 相数
    """
    return C - P_phases + 2


# =============================================================================
# 练习 7.4: 化学平衡
# Exercise 7.4: Chemical Equilibrium
# =============================================================================
def equilibrium_constant_pressure(Delta_G0, T):
    """
    平衡常数（压强形式）
    K_p = exp(-ΔG⁰/RT)
    """
    return np.exp(-Delta_G0 / (R * T))


def van_hoff_equation(K1, K2, T1, T2, Delta_H):
    """
    Van't Hoff方程
    ln(K2/K1) = -(ΔH/R)(1/T2 - 1/T1)
    """
    return np.log(K2/K1) - (-(Delta_H/R) * (1/T2 - 1/T1))


def gibbs_energy_reaction(Delta_G0, T, Q):
    """
    反应吉布斯能
    ΔG = ΔG⁰ + RT ln Q
    Q: 反应商
    """
    return Delta_G0 + R * T * np.log(Q)


def reaction_quotient(products, reactants, P_products, P_reactants, P0=1e5):
    """
    反应商
    Q = Π(P_i/P⁰)^νi
    """
    Q = 1
    for i, nu in enumerate(products):
        Q *= (P_products[i] / P0)**nu
    for i, nu in enumerate(reactants):
        Q /= (P_reactants[i] / P0)**nu
    return Q


def degree_of_dissociation(K_p, P, P0=1e5):
    """
    分解度（A ⇌ 2B 类型反应）
    α = √(K_p/(K_p + 4P/P⁰))
    """
    x = K_p * P0 / P
    return np.sqrt(x / (x + 4))


# =============================================================================
# 练习 7.5: 非理想混合物
# Exercise 7.5: Non-Ideal Mixtures
# =============================================================================
def activity(gamma, x):
    """
    活度
    a = γ × x
    γ: 活度系数
    """
    return gamma * x


def chemical_potential_real(mu0, T, a):
    """
    实际溶液化学势
    μ = μ⁰ + RT ln a
    """
    return mu0 + R * T * np.log(a)


def margules_equation_1param(x, A):
    """
    Margules单参数方程
    ln γ₁ = A x₂²
    ln γ₂ = A x₁²
    """
    x2 = 1 - x
    ln_gamma = A * x2**2
    return np.exp(ln_gamma)


def gibbs_excess_regular(x1, x2, w):
    """
    正规溶液过量吉布斯能
    G^E = w × x1 × x2
    w: 相互作用参数
    """
    return w * x1 * x2


def osmotic_pressure(c, T, M):
    """
    渗透压（van't Hoff）
    π = cRT/M = (n/V)RT
    c: 质量浓度 (kg/m³)
    M: 摩尔质量
    """
    return c * R * T / M


def boiling_point_elevation(K_b, m):
    """
    沸点升高
    ΔT_b = K_b × m
    m: 质量摩尔浓度
    """
    return K_b * m


def freezing_point_depression(K_f, m):
    """
    凝固点降低
    ΔT_f = K_f × m
    """
    return K_f * m


# =============================================================================
# 练习 7.6: 统计力学中的化学势
# Exercise 7.6: Chemical Potential in Statistical Mechanics
# =============================================================================
def fermi_dirac_mu(E, mu, T):
    """
    Fermi-Dirac分布
    f(E) = 1/(exp((E-μ)/k_BT) + 1)
    """
    x = (E - mu) / (k_B * T)
    if x > 700:
        return 0
    if x < -700:
        return 1
    return 1 / (np.exp(x) + 1)


def bose_einstein_mu(E, mu, T):
    """
    Bose-Einstein分布
    n(E) = 1/(exp((E-μ)/k_BT) - 1)
    注意: 玻色子 μ ≤ 0
    """
    x = (E - mu) / (k_B * T)
    if x > 700:
        return 0
    if x <= 0:
        return np.inf  # 凝聚
    return 1 / (np.exp(x) - 1)


def fermi_energy(n, m):
    """
    零温Fermi能
    E_F = (ℏ²/2m)(3π²n)^(2/3)
    """
    hbar = 1.055e-34
    return (hbar**2 / (2*m)) * (3 * np.pi**2 * n)**(2/3)


def chemical_potential_fermion_low_T(E_F, T):
    """
    低温费米子化学势
    μ ≈ E_F(1 - π²(k_BT/E_F)²/12)
    """
    return E_F * (1 - np.pi**2 * (k_B * T / E_F)**2 / 12)


def bec_critical_temperature(n, m):
    """
    玻色-爱因斯坦凝聚临界温度
    T_c = (2πℏ²/m k_B)(n/ζ(3/2))^(2/3)
    ζ(3/2) ≈ 2.612
    """
    hbar = 1.055e-34
    zeta_32 = 2.612
    return (2 * np.pi * hbar**2 / (m * k_B)) * (n / zeta_32)**(2/3)


# =============================================================================
# 可视化
# =============================================================================
def plot_chemical_potential():
    """绘制化学势相关图"""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 理想气体化学势 vs 压强
    ax1 = axes[0, 0]
    T = 300  # K
    P = np.logspace(-2, 2, 100) * 1e5  # 0.01 to 100 atm
    P0 = 1e5
    mu0 = 0

    mu = [chemical_potential_ideal_gas(T, p, P0, mu0) / (k_B * T) for p in P]

    ax1.semilogx(P/1e5, mu, 'b-', linewidth=2)
    ax1.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    ax1.axvline(x=1, color='r', linestyle='--', alpha=0.5, label='P⁰')
    ax1.set_xlabel('P (atm)')
    ax1.set_ylabel('μ/(k_BT)')
    ax1.set_title('理想气体化学势')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. Clausius-Clapeyron蒸汽压
    ax2 = axes[0, 1]
    T_range = np.linspace(250, 400, 100)

    # 水的参数
    T0 = 373.15
    P0 = 1e5
    Delta_H_vap = 40.65e3  # J/mol

    P_vapor = [vapor_pressure_clausius_clapeyron(T_val, T0, P0, Delta_H_vap)
               for T_val in T_range]

    ax2.semilogy(T_range, np.array(P_vapor)/1e5, 'b-', linewidth=2)
    ax2.axhline(y=1, color='r', linestyle='--', alpha=0.5, label='1 atm')
    ax2.set_xlabel('T (K)')
    ax2.set_ylabel('P (atm)')
    ax2.set_title('水的蒸汽压曲线')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 混合吉布斯能
    ax3 = axes[0, 2]
    x = np.linspace(0.01, 0.99, 100)
    T = 300

    # 理想混合
    n1 = x
    n2 = 1 - x
    G_mix_ideal = [gibbs_energy_mixing_ideal(n1i, n2i, T) for n1i, n2i in zip(n1, n2)]

    # 非理想混合
    w_values = [-5000, 0, 5000, 10000]
    for w in w_values:
        G_excess = [gibbs_excess_regular(n1i, n2i, w) for n1i, n2i in zip(n1, n2)]
        G_total = np.array(G_mix_ideal) + np.array(G_excess)
        ax3.plot(x, G_total, label=f'w = {w/1000:.0f} kJ/mol', linewidth=2)

    ax3.set_xlabel('x₁')
    ax3.set_ylabel('ΔG_mix (J/mol)')
    ax3.set_title('混合吉布斯能')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 平衡常数温度依赖
    ax4 = axes[1, 0]
    T_range = np.linspace(300, 1000, 100)

    # 不同反应焓
    for Delta_H in [-50e3, 0, 50e3]:
        Delta_G0_300 = 0  # 参考态
        K_300 = 1

        K_p = []
        for T_val in T_range:
            # Van't Hoff
            ln_K = np.log(K_300) - (Delta_H/R) * (1/T_val - 1/300)
            K_p.append(np.exp(ln_K))

        ax4.semilogy(T_range, K_p, label=f'ΔH = {Delta_H/1000:.0f} kJ/mol', linewidth=2)

    ax4.set_xlabel('T (K)')
    ax4.set_ylabel('K_p')
    ax4.set_title("Van't Hoff方程")
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. Fermi-Dirac和Bose-Einstein
    ax5 = axes[1, 1]
    E = np.linspace(-0.2, 0.2, 200)
    T = 300
    mu_val = 0

    f_FD = [fermi_dirac_mu(e * eV, mu_val, T) for e in E]
    f_BE = []
    for e in E:
        if e > 0:
            f_BE.append(bose_einstein_mu(e * eV, mu_val - 0.01*eV, T))
        else:
            f_BE.append(np.nan)

    ax5.plot(E, f_FD, 'b-', label='Fermi-Dirac', linewidth=2)
    ax5.plot(E, f_BE, 'r-', label='Bose-Einstein', linewidth=2)
    ax5.axvline(x=0, color='k', linestyle='--', alpha=0.5, label='μ')
    ax5.set_xlabel('(E - μ) (eV)')
    ax5.set_ylabel('⟨n⟩')
    ax5.set_title('量子统计分布')
    ax5.legend()
    ax5.set_xlim(-0.2, 0.2)
    ax5.set_ylim(0, 5)
    ax5.grid(True, alpha=0.3)

    # 6. 活度系数
    ax6 = axes[1, 2]
    x = np.linspace(0.01, 0.99, 100)

    for A in [-1, 0, 1, 2]:
        gamma = [margules_equation_1param(xi, A) for xi in x]
        ax6.plot(x, gamma, label=f'A = {A}', linewidth=2)

    ax6.axhline(y=1, color='k', linestyle='--', alpha=0.5)
    ax6.set_xlabel('x₁')
    ax6.set_ylabel('γ₁')
    ax6.set_title('Margules方程活度系数')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('chemical_potential.png', dpi=150)
    print("图像已保存为 chemical_potential.png")
    plt.show()


# =============================================================================
# 验证函数
# =============================================================================
def verify():
    """Verify all exercises"""
    all_passed = True

    T = 300
    P = 1e5
    P0 = 1e5
    mu0 = 0

    # Check 7.1 - Chemical potential
    mu = chemical_potential_ideal_gas(T, P, P0, mu0)

    if mu != 0:
        print("X 7.1 标准态化学势应为μ⁰")
        all_passed = False
    else:
        print(f"V 7.1 化学势正确 (μ(P⁰) = μ⁰)")

    # Check 7.2 - Gibbs energy mixing
    n1 = n2 = 1
    G_mix = gibbs_energy_mixing_ideal(n1, n2, T)

    if G_mix >= 0:
        print("X 7.2 理想混合吉布斯能应为负")
        all_passed = False
    else:
        print(f"V 7.2 吉布斯能正确 (ΔG_mix = {G_mix/1000:.2f} kJ/mol)")

    # Check 7.3 - Phase equilibrium
    T0 = 373.15
    Delta_H = 40.65e3
    P_vapor = vapor_pressure_clausius_clapeyron(T0, T0, P0, Delta_H)

    if not np.isclose(P_vapor, P0, rtol=0.01):
        print("X 7.3 沸点蒸汽压应等于P⁰")
        all_passed = False
    else:
        print(f"V 7.3 相平衡正确 (P(T_b) = P⁰)")

    # Check 7.4 - Chemical equilibrium
    Delta_G0 = 0
    K_p = equilibrium_constant_pressure(Delta_G0, T)

    if not np.isclose(K_p, 1, rtol=0.01):
        print("X 7.4 ΔG⁰=0时K应为1")
        all_passed = False
    else:
        print(f"V 7.4 化学平衡正确 (K(ΔG⁰=0) = {K_p:.2f})")

    # Check 7.5 - Activity
    gamma = 1.5
    x = 0.5
    a = activity(gamma, x)

    if not np.isclose(a, 0.75, rtol=0.01):
        print("X 7.5 活度计算错误")
        all_passed = False
    else:
        print(f"V 7.5 非理想混合物正确 (a = {a:.2f})")

    # Check 7.6 - Fermi-Dirac at mu
    f_mu = fermi_dirac_mu(0, 0, T)

    if not np.isclose(f_mu, 0.5, rtol=0.01):
        print("X 7.6 f(μ)应为0.5")
        all_passed = False
    else:
        print(f"V 7.6 统计力学正确 (f(E=μ) = {f_mu:.2f})")

    if all_passed:
        print("\n所有测试通过！正在生成可视化...")
        try:
            plot_chemical_potential()
        except Exception as ex:
            print(f"可视化生成失败: {ex}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("化学势与吉布斯能 Chemical Potential and Gibbs")
    print("=" * 50)
    verify()
