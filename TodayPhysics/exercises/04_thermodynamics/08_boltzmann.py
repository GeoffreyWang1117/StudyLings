"""
玻尔兹曼方程 Boltzmann Equation
难度 Difficulty: ★★★★★

学习目标 Learning Objectives:
- 理解玻尔兹曼输运方程
- 掌握弛豫时间近似
- 分析输运现象

HINT: 玻尔兹曼方程: ∂f/∂t + v·∇f + F/m·∂f/∂v = (∂f/∂t)_coll
HINT: H定理: dH/dt ≤ 0（熵增原理）
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint, quad
from scipy.special import gamma as gamma_func
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import k_B, m_e, e, hbar

# I AM NOT DONE

# =============================================================================
# 练习 8.1: 麦克斯韦-玻尔兹曼分布
# Exercise 8.1: Maxwell-Boltzmann Distribution
# =============================================================================
def maxwell_boltzmann_velocity(v, m, T):
    """
    麦克斯韦-玻尔兹曼速度分布
    f(v) = 4π n (m/2πk_BT)^(3/2) v² exp(-mv²/2k_BT)

    归一化: ∫f(v)dv = n
    返回概率密度（假设n=1）
    """
    # TODO: 计算速度分布
    prefactor = 4 * np.pi * (m / (2 * np.pi * k_B * T))**(3/2)
    exponential = np.exp(-m * v**2 / (2 * k_B * T))
    return prefactor * v**2 * exponential

def most_probable_speed(m, T):
    """
    最概然速率
    v_p = √(2k_BT/m)
    """
    return np.sqrt(2 * k_B * T / m)

def mean_speed(m, T):
    """
    平均速率
    <v> = √(8k_BT/(πm))
    """
    return np.sqrt(8 * k_B * T / (np.pi * m))

def rms_speed(m, T):
    """
    均方根速率
    v_rms = √(3k_BT/m)
    """
    return np.sqrt(3 * k_B * T / m)


# =============================================================================
# 练习 8.2: 弛豫时间近似
# Exercise 8.2: Relaxation Time Approximation
# =============================================================================
def relaxation_time_approximation(f, f_eq, tau):
    """
    碰撞项的弛豫时间近似
    (∂f/∂t)_coll = -(f - f_eq)/τ
    """
    # TODO: 计算碰撞项
    return -(f - f_eq) / tau

def approach_equilibrium(f0, f_eq, tau, t):
    """
    趋近平衡的解
    f(t) = f_eq + (f0 - f_eq)exp(-t/τ)
    """
    return f_eq + (f0 - f_eq) * np.exp(-t / tau)

def mean_free_path(n, sigma):
    """
    平均自由程
    λ = 1/(nσ)

    n: 数密度
    sigma: 碰撞截面
    """
    return 1 / (n * sigma)

def collision_frequency(n, sigma, v_mean):
    """
    碰撞频率
    ν = nσ<v>
    """
    return n * sigma * v_mean


# =============================================================================
# 练习 8.3: 电导率
# Exercise 8.3: Electrical Conductivity
# =============================================================================
def drude_conductivity(n, tau, m=m_e):
    """
    德鲁德模型电导率
    σ = ne²τ/m
    """
    return n * e**2 * tau / m

def mobility(tau, m=m_e):
    """
    迁移率
    μ = eτ/m
    """
    return e * tau / m

def drift_velocity(E, mu):
    """
    漂移速度
    v_d = μE
    """
    return mu * E

def resistivity(sigma):
    """
    电阻率
    ρ = 1/σ
    """
    return 1 / sigma


# =============================================================================
# 练习 8.4: 热导率
# Exercise 8.4: Thermal Conductivity
# =============================================================================
def thermal_conductivity_kinetic(n, v_mean, lambda_mfp, c_v):
    """
    动力学理论热导率
    κ = (1/3)n<v>λc_v

    c_v: 每粒子热容
    """
    return (1/3) * n * v_mean * lambda_mfp * c_v

def wiedemann_franz(sigma, T, L=2.44e-8):
    """
    维德曼-弗朗兹定律
    κ/σ = LT

    L: 洛伦兹数 ≈ 2.44×10⁻⁸ WΩ/K²
    """
    return L * T * sigma

def phonon_thermal_conductivity(C, v, l):
    """
    声子热导率
    κ = (1/3)Cvl

    C: 热容（每体积）
    v: 声速
    l: 声子平均自由程
    """
    return (1/3) * C * v * l


# =============================================================================
# 练习 8.5: 粘滞系数
# Exercise 8.5: Viscosity
# =============================================================================
def viscosity_kinetic(n, m, v_mean, lambda_mfp):
    """
    动力学理论粘滞系数
    η = (1/3)nm<v>λ
    """
    return (1/3) * n * m * v_mean * lambda_mfp

def viscosity_temperature_dependence(T, T0, eta0, s=0.5):
    """
    粘滞系数的温度依赖（Sutherland模型简化）
    η ∝ T^(1/2+s)
    """
    return eta0 * (T / T0)**(0.5 + s)

def prandtl_number(eta, c_p, kappa):
    """
    普朗特数
    Pr = ηc_p/κ
    """
    return eta * c_p / kappa


# =============================================================================
# 练习 8.6: H定理
# Exercise 8.6: H-Theorem
# =============================================================================
def h_function(f, v_grid):
    """
    玻尔兹曼H函数
    H = ∫f ln(f) dv
    """
    # 避免log(0)
    f_safe = np.maximum(f, 1e-100)
    integrand = f_safe * np.log(f_safe)
    return np.trapezoid(integrand, v_grid)

def entropy_from_h(H):
    """
    熵与H函数的关系
    S = -k_B H
    """
    return -k_B * H

def check_h_theorem(H_initial, H_final):
    """
    验证H定理
    H应随时间减小或保持不变
    """
    return H_final <= H_initial + 1e-10  # 允许数值误差

def equilibrium_entropy(N, V, T, m):
    """
    理想气体平衡态熵（Sackur-Tetrode方程简化）
    """
    n = N / V
    thermal_wavelength = np.sqrt(2 * np.pi * hbar**2 / (m * k_B * T))
    return N * k_B * (2.5 + np.log(V / (N * thermal_wavelength**3)))


# =============================================================================
# 可视化
# =============================================================================
def plot_boltzmann():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 麦克斯韦-玻尔兹曼分布
    ax1 = axes[0, 0]
    m = 28 * 1.66e-27  # N2分子
    v = np.linspace(0, 1500, 500)

    for T in [200, 300, 500]:
        f_v = maxwell_boltzmann_velocity(v, m, T)
        ax1.plot(v, f_v, label=f'T={T}K', linewidth=2)

        v_p = most_probable_speed(m, T)
        ax1.axvline(x=v_p, linestyle='--', alpha=0.5)

    ax1.set_xlabel('速度 v (m/s)')
    ax1.set_ylabel('f(v)')
    ax1.set_title('麦克斯韦-玻尔兹曼分布')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 弛豫过程
    ax2 = axes[0, 1]
    tau = 1e-12  # ps
    t = np.linspace(0, 10e-12, 200)

    f0 = 2
    f_eq = 1
    f_t = approach_equilibrium(f0, f_eq, tau, t)

    ax2.plot(t * 1e12, f_t, 'b-', linewidth=2)
    ax2.axhline(y=f_eq, color='r', linestyle='--', label='平衡态')
    ax2.axvline(x=tau * 1e12, color='g', linestyle='--', label='τ')
    ax2.set_xlabel('时间 (ps)')
    ax2.set_ylabel('f')
    ax2.set_title('弛豫过程')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 电导率vs温度
    ax3 = axes[0, 2]
    T = np.linspace(100, 500, 100)

    # 简化模型：τ与T成反比（声子散射主导）
    n = 1e28
    tau_0 = 1e-14
    tau_T = tau_0 * 300 / T

    sigma = [drude_conductivity(n, t) for t in tau_T]

    ax3.plot(T, np.array(sigma) / 1e6, 'b-', linewidth=2)
    ax3.set_xlabel('温度 (K)')
    ax3.set_ylabel('电导率 (MS/m)')
    ax3.set_title('电导率温度依赖')
    ax3.grid(True, alpha=0.3)

    # 4. 维德曼-弗朗兹定律
    ax4 = axes[1, 0]
    T = np.linspace(50, 500, 100)
    sigma_model = 1e7  # 固定电导率

    kappa = [wiedemann_franz(sigma_model, Ti) for Ti in T]
    ratio = np.array(kappa) / (sigma_model * T)

    ax4.plot(T, ratio * 1e8, 'b-', linewidth=2)
    ax4.axhline(y=2.44, color='r', linestyle='--', label='L = 2.44×10⁻⁸ WΩ/K²')
    ax4.set_xlabel('温度 (K)')
    ax4.set_ylabel('κ/(σT) (×10⁻⁸ WΩ/K²)')
    ax4.set_title('维德曼-弗朗兹定律')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 特征速率比较
    ax5 = axes[1, 1]
    T = np.linspace(100, 500, 100)

    v_p = [most_probable_speed(m, Ti) for Ti in T]
    v_mean = [mean_speed(m, Ti) for Ti in T]
    v_rms = [rms_speed(m, Ti) for Ti in T]

    ax5.plot(T, v_p, 'b-', linewidth=2, label='v_p (最概然)')
    ax5.plot(T, v_mean, 'g-', linewidth=2, label='<v> (平均)')
    ax5.plot(T, v_rms, 'r-', linewidth=2, label='v_rms')
    ax5.set_xlabel('温度 (K)')
    ax5.set_ylabel('速率 (m/s)')
    ax5.set_title('特征速率')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. H函数演化
    ax6 = axes[1, 2]
    # 模拟非平衡分布趋近平衡
    v_grid = np.linspace(0, 1000, 200)
    t_steps = np.linspace(0, 5, 50)

    # 初始：双峰分布
    f_initial = 0.5 * maxwell_boltzmann_velocity(v_grid, m, 200) + \
                0.5 * maxwell_boltzmann_velocity(v_grid, m, 400)
    f_eq = maxwell_boltzmann_velocity(v_grid, m, 300)

    H_vals = []
    for t in t_steps:
        f_t = f_eq + (f_initial - f_eq) * np.exp(-t)
        H = h_function(f_t, v_grid)
        H_vals.append(H)

    ax6.plot(t_steps, H_vals, 'b-', linewidth=2)
    ax6.set_xlabel('时间 (arb.)')
    ax6.set_ylabel('H')
    ax6.set_title('H函数演化（H定理）')
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('boltzmann.png', dpi=150)
    print("图像已保存为 boltzmann.png")
    plt.show()


def verify():
    all_passed = True

    m = 28 * 1.66e-27  # N2
    T = 300

    # Check 8.1
    v_p = most_probable_speed(m, T)
    v_mean = mean_speed(m, T)
    v_rms = rms_speed(m, T)
    if not (v_p < v_mean < v_rms):
        print("❌ 8.1 速率关系应为 v_p < <v> < v_rms")
        all_passed = False
    else:
        print(f"✓ 8.1 麦克斯韦-玻尔兹曼分布正确 (v_p={v_p:.0f}, <v>={v_mean:.0f}, v_rms={v_rms:.0f} m/s)")

    # Check 8.2
    tau = 1e-12
    f_t = approach_equilibrium(2, 1, tau, tau)
    if not np.isclose(f_t, 1 + np.exp(-1), rtol=0.01):
        print("❌ 8.2 弛豫过程错误")
        all_passed = False
    else:
        print(f"✓ 8.2 弛豫时间近似正确")

    # Check 8.3
    n = 1e28
    tau = 1e-14
    sigma = drude_conductivity(n, tau)
    if sigma <= 0:
        print("❌ 8.3 电导率应为正")
        all_passed = False
    else:
        print(f"✓ 8.3 德鲁德电导率正确 (σ = {sigma:.2e} S/m)")

    # Check 8.4
    kappa = wiedemann_franz(sigma, T)
    L = kappa / (sigma * T)
    if not np.isclose(L, 2.44e-8, rtol=0.01):
        print("❌ 8.4 洛伦兹数错误")
        all_passed = False
    else:
        print(f"✓ 8.4 热导率正确 (L = {L:.2e} WΩ/K²)")

    # Check 8.5
    eta = viscosity_kinetic(n, m, v_mean, 1e-7)
    if eta <= 0:
        print("❌ 8.5 粘滞系数应为正")
        all_passed = False
    else:
        print(f"✓ 8.5 粘滞系数正确")

    # Check 8.6
    v_grid = np.linspace(1, 1000, 200)
    f = maxwell_boltzmann_velocity(v_grid, m, T)
    H = h_function(f, v_grid)
    S = entropy_from_h(H)
    if S <= 0:
        print("❌ 8.6 熵应为正（平衡态）")
        all_passed = False
    else:
        print(f"✓ 8.6 H定理验证正确")

    if all_passed:
        print("\n🎉 所有测试通过！")
        try:
            plot_boltzmann()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("玻尔兹曼方程 Boltzmann Equation")
    print("=" * 50)
    verify()
