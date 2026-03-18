"""
涨落与响应 Fluctuations and Response
难度 Difficulty: ★★★★★

学习目标 Learning Objectives:
- 理解热力学涨落
- 掌握涨落-耗散定理
- 分析响应函数

HINT: 能量涨落: <(ΔE)²> = k_BT²C_V
HINT: 涨落-耗散定理: S(ω) = 2k_BTχ''(ω)/ω
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.fft import fft, ifft, fftfreq
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import k_B, hbar, m_e

# I AM NOT DONE

# =============================================================================
# 练习 9.1: 热力学涨落
# Exercise 9.1: Thermodynamic Fluctuations
# =============================================================================
def energy_fluctuation(T, C_V):
    """
    能量涨落
    <(ΔE)²> = k_B T² C_V
    """
    # TODO: 计算能量涨落
    return k_B * T**2 * C_V

def number_fluctuation(N, T, mu, kappa_T):
    """
    粒子数涨落（巨正则系综）
    <(ΔN)²> = k_BT (∂N/∂μ)_T = k_BT N² κ_T/V

    kappa_T: 等温压缩率
    """
    return k_B * T * N**2 * kappa_T

def volume_fluctuation(V, T, kappa_T):
    """
    体积涨落
    <(ΔV)²> = k_BT V κ_T
    """
    return k_B * T * V * kappa_T

def relative_fluctuation(delta_X_squared, X):
    """
    相对涨落
    σ_X/X = √(<ΔX²>)/X
    """
    return np.sqrt(delta_X_squared) / X


# =============================================================================
# 练习 9.2: 涨落-耗散定理
# Exercise 9.2: Fluctuation-Dissipation Theorem
# =============================================================================
def power_spectral_density(chi_imag, omega, T):
    """
    功率谱密度（涨落-耗散定理）
    S(ω) = 2k_BT χ''(ω)/ω

    chi_imag: 复响应函数的虚部
    """
    if abs(omega) < 1e-10:
        return 0
    return 2 * k_B * T * chi_imag / omega

def classical_fluctuation_dissipation(chi_imag, omega, T):
    """
    经典涨落-耗散定理
    S(ω) = (2k_BT/ω) χ''(ω)
    """
    return power_spectral_density(chi_imag, omega, T)

def quantum_fluctuation_dissipation(chi_imag, omega, T):
    """
    量子涨落-耗散定理
    S(ω) = ℏ[n(ω) + 1]χ''(ω)/π
    其中 n(ω) = 1/(exp(ℏω/k_BT) - 1)
    """
    if abs(omega) < 1e-10:
        return 0

    x = hbar * omega / (k_B * T)
    if x > 100:
        n = 0
    elif x < -100:
        n = -1
    else:
        n = 1 / (np.exp(x) - 1) if x > 0.01 else k_B * T / (hbar * omega) - 0.5

    return hbar * (n + 1) * chi_imag / np.pi


# =============================================================================
# 练习 9.3: 线性响应
# Exercise 9.3: Linear Response
# =============================================================================
def susceptibility_harmonic(omega, omega_0, gamma):
    """
    谐振子响应函数
    χ(ω) = 1/(ω₀² - ω² - iγω)
    """
    # TODO: 计算复响应函数
    return 1 / (omega_0**2 - omega**2 - 1j * gamma * omega)

def real_susceptibility(omega, omega_0, gamma):
    """
    响应函数实部 χ'(ω)
    """
    chi = susceptibility_harmonic(omega, omega_0, gamma)
    return np.real(chi)

def imaginary_susceptibility(omega, omega_0, gamma):
    """
    响应函数虚部 χ''(ω)（与耗散相关）
    """
    chi = susceptibility_harmonic(omega, omega_0, gamma)
    return np.imag(chi)

def response_function(chi, F_omega):
    """
    响应 X(ω) = χ(ω)F(ω)
    """
    return chi * F_omega


# =============================================================================
# 练习 9.4: 朗之万方程
# Exercise 9.4: Langevin Equation
# =============================================================================
def langevin_step(x, v, dt, gamma, T, m):
    """
    朗之万方程的欧拉步
    m dv/dt = -γv + η(t)
    <η(t)η(t')> = 2γk_BT δ(t-t')
    """
    # 随机力
    sigma = np.sqrt(2 * gamma * k_B * T * dt)
    eta = np.random.normal(0, sigma)

    # 速度更新
    v_new = v - (gamma/m) * v * dt + eta / m

    # 位置更新
    x_new = x + v_new * dt

    return x_new, v_new

def langevin_trajectory(x0, v0, t_span, dt, gamma, T, m):
    """
    生成朗之万轨迹
    """
    t = np.arange(t_span[0], t_span[1], dt)
    x = np.zeros(len(t))
    v = np.zeros(len(t))

    x[0], v[0] = x0, v0

    for i in range(1, len(t)):
        x[i], v[i] = langevin_step(x[i-1], v[i-1], dt, gamma, T, m)

    return t, x, v

def diffusion_coefficient_langevin(gamma, T, m):
    """
    朗之万粒子的扩散系数
    D = k_BT/(mγ)
    """
    return k_B * T / (m * gamma)


# =============================================================================
# 练习 9.5: 自相关函数
# Exercise 9.5: Autocorrelation Functions
# =============================================================================
def velocity_autocorrelation(t, gamma, T, m):
    """
    速度自相关函数
    <v(t)v(0)> = (k_BT/m)exp(-γt/m)
    """
    return (k_B * T / m) * np.exp(-gamma * t / m)

def position_correlation(t, D, gamma, m):
    """
    位置均方位移
    <[x(t) - x(0)]²> = 2Dt（长时间极限）
    """
    tau = m / gamma
    if t < tau:
        # 短时间惯性区
        return (k_B * T / m) * t**2
    else:
        # 长时间扩散区
        return 2 * D * t

def green_kubo_relation(v_acf, dt):
    """
    格林-久保关系
    D = ∫₀^∞ <v(t)v(0)> dt
    """
    return np.trapezoid(v_acf, dx=dt)


# =============================================================================
# 练习 9.6: 临界涨落
# Exercise 9.6: Critical Fluctuations
# =============================================================================
def correlation_length(T, T_c, xi_0, nu=0.5):
    """
    关联长度（临界点附近）
    ξ = ξ₀|t|^(-ν)
    t = (T - T_c)/T_c
    """
    t = (T - T_c) / T_c
    if abs(t) < 1e-10:
        return np.inf
    return xi_0 * abs(t)**(-nu)

def susceptibility_critical(T, T_c, chi_0, gamma_exp=1):
    """
    临界点附近磁化率发散
    χ = χ₀|t|^(-γ)
    """
    t = (T - T_c) / T_c
    if abs(t) < 1e-10:
        return np.inf
    return chi_0 * abs(t)**(-gamma_exp)

def order_parameter(T, T_c, M_0, beta=0.5):
    """
    序参量（T < T_c时）
    M = M₀|t|^β
    """
    if T >= T_c:
        return 0
    t = (T_c - T) / T_c
    return M_0 * t**beta


# =============================================================================
# 可视化
# =============================================================================
def plot_fluctuations():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 能量涨落vs温度
    ax1 = axes[0, 0]
    T = np.linspace(100, 500, 100)
    C_V = 3 * k_B * 1e23  # 大致1mol粒子

    delta_E = [np.sqrt(energy_fluctuation(Ti, C_V)) for Ti in T]

    ax1.plot(T, np.array(delta_E) / k_B, 'b-', linewidth=2)
    ax1.set_xlabel('温度 (K)')
    ax1.set_ylabel('ΔE/k_B (K)')
    ax1.set_title('能量涨落')
    ax1.grid(True, alpha=0.3)

    # 2. 响应函数
    ax2 = axes[0, 1]
    omega_0 = 1
    gamma = 0.2
    omega = np.linspace(0.01, 3, 500)

    chi_real = [real_susceptibility(w, omega_0, gamma) for w in omega]
    chi_imag = [imaginary_susceptibility(w, omega_0, gamma) for w in omega]

    ax2.plot(omega, chi_real, 'b-', linewidth=2, label="χ' (实部)")
    ax2.plot(omega, chi_imag, 'r-', linewidth=2, label="χ'' (虚部)")
    ax2.axvline(x=omega_0, color='g', linestyle='--', alpha=0.5)
    ax2.set_xlabel('ω')
    ax2.set_ylabel('χ')
    ax2.set_title('谐振子响应函数')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 功率谱密度
    ax3 = axes[0, 2]
    T_val = 300

    S_classical = [power_spectral_density(imaginary_susceptibility(w, omega_0, gamma), w, T_val)
                   if w > 0.01 else 0 for w in omega]

    ax3.semilogy(omega, np.abs(S_classical), 'b-', linewidth=2)
    ax3.set_xlabel('ω')
    ax3.set_ylabel('S(ω)')
    ax3.set_title('功率谱密度')
    ax3.grid(True, alpha=0.3)

    # 4. 朗之万轨迹
    ax4 = axes[1, 0]
    np.random.seed(42)
    m = 1e-20
    gamma_L = 1e-12
    T_L = 300
    dt = 1e-15
    t_span = [0, 1e-12]

    t, x, v = langevin_trajectory(0, 0, t_span, dt, gamma_L, T_L, m)

    ax4.plot(t * 1e12, x * 1e9, 'b-', linewidth=0.5)
    ax4.set_xlabel('时间 (ps)')
    ax4.set_ylabel('位置 (nm)')
    ax4.set_title('布朗运动轨迹')
    ax4.grid(True, alpha=0.3)

    # 5. 速度自相关
    ax5 = axes[1, 1]
    tau = m / gamma_L
    t_acf = np.linspace(0, 5*tau, 200)

    v_acf = velocity_autocorrelation(t_acf, gamma_L, T_L, m)
    v_acf_norm = v_acf / (k_B * T_L / m)

    ax5.plot(t_acf / tau, v_acf_norm, 'b-', linewidth=2)
    ax5.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    ax5.set_xlabel('t/τ')
    ax5.set_ylabel('<v(t)v(0)>/<v²>')
    ax5.set_title('速度自相关函数')
    ax5.grid(True, alpha=0.3)

    # 6. 临界涨落
    ax6 = axes[1, 2]
    T_c = 647  # K (水的临界点)
    T_range = np.linspace(600, 700, 200)
    xi_0 = 1e-9

    xi = [correlation_length(Ti, T_c, xi_0) for Ti in T_range]
    chi = [susceptibility_critical(Ti, T_c, 1) for Ti in T_range]

    ax6.semilogy(T_range, xi, 'b-', linewidth=2, label='关联长度 ξ')
    ax6.axvline(x=T_c, color='r', linestyle='--', label='T_c')
    ax6.set_xlabel('温度 (K)')
    ax6.set_ylabel('ξ (m)')
    ax6.set_title('临界涨落')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('fluctuations.png', dpi=150)
    print("图像已保存为 fluctuations.png")
    plt.show()


def verify():
    all_passed = True

    T = 300

    # Check 9.1
    C_V = 3 * k_B  # 单粒子
    delta_E_sq = energy_fluctuation(T, C_V)
    expected = k_B * T**2 * C_V
    if not np.isclose(delta_E_sq, expected, rtol=0.01):
        print("❌ 9.1 能量涨落公式错误")
        all_passed = False
    else:
        print(f"✓ 9.1 热力学涨落正确")

    # Check 9.2
    omega_0, gamma = 1, 0.1
    chi_imag = imaginary_susceptibility(omega_0, omega_0, gamma)
    S = power_spectral_density(chi_imag, omega_0, T)
    if S <= 0:
        print("❌ 9.2 功率谱密度应为正")
        all_passed = False
    else:
        print(f"✓ 9.2 涨落-耗散定理正确")

    # Check 9.3
    chi = susceptibility_harmonic(0, omega_0, gamma)
    if not np.isclose(np.real(chi), 1/omega_0**2, rtol=0.01):
        print("❌ 9.3 静态响应χ(0)错误")
        all_passed = False
    else:
        print(f"✓ 9.3 线性响应正确 (χ(0) = {np.real(chi):.3f})")

    # Check 9.4
    m = 1e-20
    gamma_L = 1e-12
    D = diffusion_coefficient_langevin(gamma_L, T, m)
    expected_D = k_B * T / (m * gamma_L)
    if not np.isclose(D, expected_D, rtol=0.01):
        print("❌ 9.4 扩散系数错误")
        all_passed = False
    else:
        print(f"✓ 9.4 朗之万方程正确 (D = {D:.2e} m²/s)")

    # Check 9.5
    v_acf_0 = velocity_autocorrelation(0, gamma_L, T, m)
    expected_v2 = k_B * T / m
    if not np.isclose(v_acf_0, expected_v2, rtol=0.01):
        print("❌ 9.5 速度自相关t=0时应等于<v²>")
        all_passed = False
    else:
        print(f"✓ 9.5 自相关函数正确 (<v²> = {v_acf_0:.2e} m²/s²)")

    # Check 9.6
    T_c = 647
    xi = correlation_length(646, T_c, 1e-9)
    if xi <= 1e-9:
        print("❌ 9.6 临界点附近关联长度应发散")
        all_passed = False
    else:
        print(f"✓ 9.6 临界涨落正确 (T→T_c时 ξ→∞)")

    if all_passed:
        print("\n🎉 所有测试通过！")
        try:
            plot_fluctuations()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("涨落与响应 Fluctuations and Response")
    print("=" * 50)
    verify()
