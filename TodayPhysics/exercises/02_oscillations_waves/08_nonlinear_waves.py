"""
非线性波与孤子 Nonlinear Waves and Solitons
难度 Difficulty: ★★★★★

学习目标 Learning Objectives:
- 理解非线性波动方程及其与线性方程的本质区别
  Understand nonlinear wave equations and differences from linear ones
- 掌握孤子（soliton）的形成机制和特殊性质
  Master formation mechanism and special properties of solitons
- 分析KdV方程、非线性薛定谔方程等经典模型
  Analyze KdV equation, nonlinear Schrodinger equation, etc.
- 了解激波、调制不稳定性和怪波等现象
  Understand shock waves, modulational instability, and rogue waves

物理背景 Physical Background:
非线性波是指振幅影响波速或形状的波动。与线性波不同，
非线性效应可能导致波形畸变、激波形成或孤子产生。

孤子（Soliton）：
孤子是一种特殊的非线性波，具有粒子般的性质：
1. 传播时保持形状不变（色散与非线性效应平衡）
2. 碰撞后保持原有形状（仅有相移）
3. 速度与振幅相关

重要方程：

1. KdV方程（浅水波、离子声波）：
   ∂u/∂t + 6u·∂u/∂x + ∂³u/∂x³ = 0
   单孤子解：u = (c/2)·sech²[√c/2·(x-ct)]

2. 非线性薛定谔方程（光纤通信、玻色-爱因斯坦凝聚）：
   i·∂ψ/∂t + ∂²ψ/∂x² + 2|ψ|²ψ = 0
   亮孤子解：ψ = A·sech(Ax)·exp(iA²t)

3. Burgers方程（激波）：
   ∂u/∂t + u·∂u/∂x = 0
   特征线交汇形成间断（激波）

应用：光纤孤子通信、海啸建模、等离子体物理、超流体

HINT: KdV方程: ∂u/∂t + 6u∂u/∂x + ∂³u/∂x³ = 0
HINT: 孤子解: u(x,t) = (c/2)sech²(√c/2 × (x-ct))
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.fft import fft, ifft, fftfreq
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import c as c_light, hbar

# I AM NOT DONE

# =============================================================================
# 练习 8.1: KdV方程与孤子
# Exercise 8.1: KdV Equation and Solitons
# =============================================================================
def kdv_soliton(x, t, c, x0=0):
    """
    KdV方程单孤子解
    u(x,t) = (c/2)sech²(√(c)/2 × (x - ct - x0))
    c: 孤子速度/振幅参数
    """
    arg = np.sqrt(c) / 2 * (x - c * t - x0)
    return (c / 2) / np.cosh(arg)**2

def kdv_two_soliton(x, t, c1, c2, x01=0, x02=0):
    """
    KdV方程双孤子解（简化形式）
    展示孤子碰撞后保持形状
    """
    # 单独的孤子
    u1 = kdv_soliton(x, t, c1, x01)
    u2 = kdv_soliton(x, t, c2, x02)
    # 简化近似（实际解更复杂）
    return u1 + u2

def kdv_phase_shift(c1, c2):
    """
    KdV孤子碰撞相移
    Δx = 2/√c × ln(|(√c₁ - √c₂)/(√c₁ + √c₂)|)
    """
    return (2 / np.sqrt(c1)) * np.log(np.abs((np.sqrt(c1) - np.sqrt(c2)) /
                                             (np.sqrt(c1) + np.sqrt(c2))))


# =============================================================================
# 练习 8.2: 非线性薛定谔方程
# Exercise 8.2: Nonlinear Schrodinger Equation
# =============================================================================
def nls_bright_soliton(x, t, A, k=0, omega=0):
    """
    非线性薛定谔方程亮孤子
    ψ(x,t) = A sech(Ax) exp(i(kx - ωt))
    聚焦NLS: i∂ψ/∂t + ∂²ψ/∂x² + 2|ψ|²ψ = 0
    """
    envelope = A / np.cosh(A * x)
    phase = np.exp(1j * (k * x - omega * t))
    return envelope * phase

def nls_dark_soliton(x, t, u0, v):
    """
    非线性薛定谔方程暗孤子
    散焦NLS: i∂ψ/∂t + ∂²ψ/∂x² - 2|ψ|²ψ = 0
    """
    # 简化形式
    theta = np.arccos(v / u0)
    arg = u0 * np.sin(theta) * (x - v * t)
    return u0 * (np.cos(theta) * np.tanh(arg) + 1j * np.sin(theta))

def nls_soliton_power(A):
    """
    光孤子功率
    P = ∫|ψ|²dx = 2A
    """
    return 2 * A


# =============================================================================
# 练习 8.3: 冲击波
# Exercise 8.3: Shock Waves
# =============================================================================
def burgers_equation_shock(x, t, u_l, u_r, x0=0):
    """
    Burgers方程激波解
    无粘性情况下形成间断
    """
    # 激波速度
    s = (u_l + u_r) / 2
    shock_position = x0 + s * t
    return np.where(x < shock_position, u_l, u_r)

def shock_velocity(u_l, u_r):
    """
    Rankine-Hugoniot条件下的激波速度
    s = (f(u_r) - f(u_l))/(u_r - u_l) = (u_l + u_r)/2 对于Burgers方程
    """
    return (u_l + u_r) / 2

def rarefaction_wave(x, t, u_l, u_r, x0=0):
    """
    稀疏波（膨胀波）
    当 u_l < u_r 时出现
    """
    if t == 0:
        return np.where(x < x0, u_l, u_r)

    left = x0 + u_l * t
    right = x0 + u_r * t

    result = np.zeros_like(x, dtype=float)
    result[x <= left] = u_l
    result[x >= right] = u_r
    mask = (x > left) & (x < right)
    result[mask] = (x[mask] - x0) / t
    return result


# =============================================================================
# 练习 8.4: 调制不稳定性
# Exercise 8.4: Modulational Instability
# =============================================================================
def modulational_instability_growth(k, A0, beta2=-1, gamma=1):
    """
    调制不稳定性增长率
    Ω = |k|√(γP₀ - β₂²k⁴/4)
    当 β₂γ < 0 时存在
    """
    P0 = A0**2
    discriminant = gamma * P0 - beta2**2 * k**4 / 4
    if discriminant < 0:
        return 0
    return np.abs(k) * np.sqrt(discriminant)

def mi_critical_frequency(A0, beta2=-1, gamma=1):
    """
    调制不稳定性的临界频率
    k_c = √(2γP₀/|β₂|)
    """
    P0 = A0**2
    return np.sqrt(2 * gamma * P0 / np.abs(beta2))

def mi_peak_growth_rate(A0, beta2=-1, gamma=1):
    """
    最大增长率
    Ω_max = γP₀
    """
    return gamma * A0**2


# =============================================================================
# 练习 8.5: 怪波
# Exercise 8.5: Rogue Waves (Peregrine Soliton)
# =============================================================================
def peregrine_soliton(x, t, A0=1):
    """
    Peregrine孤子（一阶怪波解）
    ψ = A₀(1 - 4(1+2iA₀²t)/(1+4A₀²x²+4A₀⁴t²)) exp(iA₀²t)
    """
    numerator = 4 * (1 + 2j * A0**2 * t)
    denominator = 1 + 4 * A0**2 * x**2 + 4 * A0**4 * t**2
    return A0 * (1 - numerator / denominator) * np.exp(1j * A0**2 * t)

def rogue_wave_amplitude(A0):
    """
    怪波最大振幅
    |ψ|_max = 3A₀ (Peregrine孤子)
    """
    return 3 * A0

def akhmediev_breather(x, t, a=0.25, A0=1):
    """
    Akhmediev呼吸子
    空间周期性的怪波前驱
    0 < a < 0.5
    """
    omega = np.sqrt(8 * a * (1 - 2*a))
    k = 2 * np.sqrt(2 * a)

    cosh_term = np.cosh(omega * A0**2 * t)
    cos_term = np.cos(k * A0 * x)

    numerator = np.sqrt(2*a) * cos_term - 1j * omega * np.sinh(omega * A0**2 * t)
    denominator = cosh_term - np.sqrt(2*a) * cos_term

    return A0 * (1 + numerator / denominator) * np.exp(1j * A0**2 * t)


# =============================================================================
# 练习 8.6: 非线性光学效应
# Exercise 8.6: Nonlinear Optical Effects
# =============================================================================
def kerr_effect_refractive_index(n0, n2, I):
    """
    克尔效应折射率变化
    n = n₀ + n₂I
    n₂: 非线性折射率系数
    I: 光强
    """
    return n0 + n2 * I

def self_phase_modulation(phi0, n2, I, L, wavelength):
    """
    自相位调制引起的相移
    Δφ = (2π/λ) n₂ I L
    """
    return (2 * np.pi / wavelength) * n2 * I * L

def self_focusing_power(n0, n2, wavelength):
    """
    自聚焦临界功率
    P_cr ≈ 3.77λ²/(8πn₀n₂)
    """
    return 3.77 * wavelength**2 / (8 * np.pi * n0 * n2)

def four_wave_mixing_efficiency(chi3, L, I_pump):
    """
    四波混频效率（简化）
    η ∝ (χ³)² × I_pump² × L²
    """
    return chi3**2 * I_pump**2 * L**2


# =============================================================================
# 可视化
# =============================================================================
def plot_nonlinear_waves():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. KdV孤子
    ax1 = axes[0, 0]
    x = np.linspace(-20, 20, 500)

    for t in [0, 2, 4]:
        u = kdv_soliton(x, t, c=4, x0=-10)
        ax1.plot(x, u, label=f't = {t}', linewidth=2)

    ax1.set_xlabel('x')
    ax1.set_ylabel('u')
    ax1.set_title('KdV单孤子传播')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 孤子碰撞
    ax2 = axes[0, 1]
    x = np.linspace(-40, 40, 500)

    for t in [-5, 0, 5]:
        u1 = kdv_soliton(x, t, c=4, x0=-20)
        u2 = kdv_soliton(x, t, c=1, x0=-10)
        ax2.plot(x, u1 + u2, label=f't = {t}', linewidth=1.5)

    ax2.set_xlabel('x')
    ax2.set_ylabel('u')
    ax2.set_title('孤子碰撞（近似）')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. NLS亮孤子
    ax3 = axes[0, 2]
    x = np.linspace(-10, 10, 500)

    psi = nls_bright_soliton(x, 0, A=1)
    ax3.plot(x, np.abs(psi)**2, 'b-', label='|ψ|²', linewidth=2)
    ax3.plot(x, np.real(psi), 'r--', label='Re(ψ)', linewidth=1.5)
    ax3.plot(x, np.imag(psi), 'g--', label='Im(ψ)', linewidth=1.5)

    ax3.set_xlabel('x')
    ax3.set_ylabel('ψ')
    ax3.set_title('NLS亮孤子')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. Peregrine孤子（怪波）
    ax4 = axes[1, 0]
    x = np.linspace(-5, 5, 200)
    t = np.linspace(-2, 2, 200)
    X, T = np.meshgrid(x, t)

    psi = peregrine_soliton(X, T, A0=1)
    intensity = np.abs(psi)**2

    im = ax4.contourf(X, T, intensity, levels=20, cmap='hot')
    ax4.set_xlabel('x')
    ax4.set_ylabel('t')
    ax4.set_title('Peregrine孤子 |ψ|²')
    plt.colorbar(im, ax=ax4)

    # 5. 调制不稳定性增长率
    ax5 = axes[1, 1]
    k = np.linspace(0, 2, 100)

    for A0 in [0.5, 1.0, 1.5]:
        Omega = [modulational_instability_growth(ki, A0) for ki in k]
        ax5.plot(k, Omega, label=f'A₀ = {A0}', linewidth=2)

    ax5.set_xlabel('k')
    ax5.set_ylabel('Ω (增长率)')
    ax5.set_title('调制不稳定性')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. 激波vs稀疏波
    ax6 = axes[1, 2]
    x = np.linspace(-10, 10, 500)
    t = 2

    # 激波
    u_shock = burgers_equation_shock(x, t, u_l=2, u_r=0)
    # 稀疏波
    u_raref = rarefaction_wave(x, t, u_l=0, u_r=2)

    ax6.plot(x, u_shock, 'b-', label='激波 (u_L > u_R)', linewidth=2)
    ax6.plot(x, u_raref, 'r--', label='稀疏波 (u_L < u_R)', linewidth=2)
    ax6.set_xlabel('x')
    ax6.set_ylabel('u')
    ax6.set_title('Burgers方程解 (t=2)')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('nonlinear_waves.png', dpi=150)
    print("图像已保存为 nonlinear_waves.png")
    plt.show()


def verify():
    """
    验证所有练习的正确性
    Verify all exercises
    """
    all_passed = True

    # 检查 8.1 - KdV孤子 Check KdV soliton
    x = 0
    t = 0
    c = 4  # 孤子速度/振幅参数
    u = kdv_soliton(x, t, c)
    expected = c / 2  # 孤子峰值 = c/2
    if not np.isclose(u, expected, rtol=0.01):
        print("错误 8.1: KdV孤子峰值错误，峰值应为 c/2")
        all_passed = False
    else:
        print(f"通过 8.1: KdV孤子正确 (速度参数c={c} → 峰值 = c/2 = {u:.1f})")

    # 检查 8.2 - 非线性薛定谔孤子 Check NLS soliton
    A = 1
    psi = nls_bright_soliton(0, 0, A)
    if not np.isclose(np.abs(psi), A, rtol=0.01):
        print("错误 8.2: NLS亮孤子中心振幅错误")
        all_passed = False
    else:
        print(f"通过 8.2: NLS亮孤子正确 (中心振幅 |ψ(0)| = {np.abs(psi):.1f})")

    # 检查 8.3 - 激波 Check shock wave
    s = shock_velocity(2, 0)  # 左态 u_L=2, 右态 u_R=0
    if not np.isclose(s, 1, rtol=0.01):
        print("错误 8.3: 激波速度计算错误，Burgers方程激波速度 s = (u_L + u_R)/2")
        all_passed = False
    else:
        print(f"通过 8.3: 激波正确 (Rankine-Hugoniot条件 → 激波速度 s = {s:.1f})")

    # 检查 8.4 - 调制不稳定性 Check modulational instability
    k_c = mi_critical_frequency(A0=1)
    if k_c <= 0:
        print("错误 8.4: 调制不稳定性临界频率应为正值")
        all_passed = False
    else:
        print(f"通过 8.4: 调制不稳定性正确 (临界波数 k_c = {k_c:.2f})")

    # 检查 8.5 - 怪波 Check rogue wave
    amp_max = rogue_wave_amplitude(1)
    if not np.isclose(amp_max, 3, rtol=0.01):
        print("错误 8.5: Peregrine孤子（一阶怪波）最大振幅应为 3A₀")
        all_passed = False
    else:
        print(f"通过 8.5: 怪波正确 (Peregrine孤子最大振幅 = 3×背景振幅)")

    # 检查 8.6 - 非线性光学 Check nonlinear optics
    n = kerr_effect_refractive_index(1.5, 3e-20, 1e16)  # n₀=1.5, n₂=3e-20, I=1e16
    if n <= 1.5:
        print("错误 8.6: 克尔效应应使折射率增大（正n₂情况）")
        all_passed = False
    else:
        print(f"通过 8.6: 非线性光学正确 (克尔效应 → n = {n:.6f})")

    if all_passed:
        print("\n全部测试通过！正在生成可视化图像...")
        print("All tests passed! Generating visualization...")
        try:
            plot_nonlinear_waves()
        except Exception as e:
            print(f"可视化失败 Visualization failed: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("非线性波与孤子 Nonlinear Waves and Solitons")
    print("=" * 50)
    verify()
