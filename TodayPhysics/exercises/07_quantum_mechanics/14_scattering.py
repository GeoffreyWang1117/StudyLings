"""
量子散射理论 Quantum Scattering Theory
难度 Difficulty: ★★★★★

物理背景 Physical Background:
--------------------------
量子散射理论描述粒子与势场或其他粒子碰撞的过程。
它是核物理、粒子物理、原子物理实验分析的基础。

1. 散射截面 Scattering Cross Section:
   微分截面: dσ/dΩ = |f(θ)|²
   其中 f(θ) 是散射振幅，描述不同方向的散射概率。
   总截面: σ_total = ∫dσ/dΩ dΩ

2. 光学定理 Optical Theorem:
   σ_total = 4π/k × Im[f(0)]
   联系了前向散射振幅与总截面，体现概率守恒。

3. 分波分析 Partial Wave Analysis:
   将散射振幅展开为分波:
   f(θ) = Σₗ (2l+1) fₗ Pₗ(cosθ)
   每个分波由相移 δₗ 描述: fₗ = exp(iδₗ)sin(δₗ)/k

4. 玻恩近似 Born Approximation:
   弱散射极限下的微扰结果:
   f(q) = -m/(2πℏ²) ∫V(r)exp(iq·r)d³r
   其中 q 是动量转移。

5. 共振散射 Resonance Scattering:
   当入射能量接近准束缚态时，截面显著增强。
   Breit-Wigner公式描述共振形状。

学习目标 Learning Objectives:
--------------------------
1. 理解散射截面的物理意义
2. 掌握分波方法和相移分析
3. 应用玻恩近似计算散射振幅
4. 理解共振散射和Breit-Wigner公式
5. 了解S矩阵形式化
6. 理解Levinson定理

关键公式 Key Formulas:
---------------------
- 微分截面: dσ/dΩ = |f(θ)|²
- 光学定理: σ_total = 4π/k × Im[f(0)]
- 分波展开: σ = 4π/k² Σₗ(2l+1)sin²δₗ
- 相移: S_l = exp(2iδₗ)
- 玻恩近似: f(q) ∝ Ṽ(q) (势的傅里叶变换)

HINT: 微分截面: dσ/dΩ = |f(θ)|²
HINT: 光学定理: σ_total = 4π/k × Im[f(0)]
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import spherical_jn, spherical_yn
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import hbar, m_e

# I AM NOT DONE

# =============================================================================
# 练习 14.1: 散射基础
# Exercise 14.1: Scattering Basics
#
# 物理背景 Physical Background:
# 散射实验是探测微观世界的主要方法。
# 通过测量散射粒子的角分布，可以推断靶粒子的结构。
#
# 散射振幅 f(θ) 是描述散射过程的核心量:
# - 它是入射波和散射波之间的联系
# - 包含了势场的全部信息
# - 散射远场波函数: ψ ~ e^{ikz} + f(θ)e^{ikr}/r
# =============================================================================
def differential_cross_section(f_theta):
    """
    微分散射截面 Differential cross section

    dσ/dΩ = |f(θ)|²

    物理意义:
    散射到立体角 dΩ 的概率正比于 dσ/dΩ。
    单位通常是 barn (1 barn = 10⁻²⁴ cm²)

    参数 Parameters:
        f_theta: 散射振幅 f(θ)

    返回 Returns:
        dσ/dΩ: 微分截面 (m²/sr)
    """
    return np.abs(f_theta)**2


def total_cross_section_from_amplitude(f_forward, k):
    """
    光学定理 Optical theorem

    σ_total = 4π/k × Im[f(0)]

    这是量子力学中最优美的定理之一:
    前向散射振幅的虚部决定了总截面。
    来源于概率守恒（幺正性）。

    参数 Parameters:
        f_forward: 前向散射振幅 f(θ=0)
        k: 入射波矢 (1/m)

    返回 Returns:
        σ_total: 总散射截面 (m²)
    """
    return 4 * np.pi / k * np.imag(f_forward)


def wave_vector(E, m=m_e):
    """
    入射波矢 Wave vector

    k = √(2mE)/ℏ

    波矢与德布罗意波长的关系: k = 2π/λ

    参数 Parameters:
        E: 动能 (J)
        m: 粒子质量 (kg)

    返回 Returns:
        k: 波矢 (1/m)
    """
    return np.sqrt(2 * m * E) / hbar


def scattering_length(k, delta_0):
    """
    散射长度（低能极限）Scattering length

    a = -tan(δ₀)/k → -δ₀/k (当 δ₀ << 1)

    散射长度描述低能s波散射的强度。
    - a > 0: 等效排斥势
    - a < 0: 等效吸引势（可能有束缚态）
    - a → ±∞: 共振

    参数 Parameters:
        k: 波矢 (1/m)
        delta_0: s波 (l=0) 相移

    返回 Returns:
        a: 散射长度 (m)
    """
    return -np.tan(delta_0) / k


# =============================================================================
# 练习 14.2: 分波分析
# Exercise 14.2: Partial Wave Analysis
#
# 物理背景 Physical Background:
# 分波分析将散射问题按角动量量子数分解。
# 对于球对称势，不同 l 的分波独立散射。
#
# 每个分波只引入一个相移 δₗ:
# - δₗ 描述了散射波相对于自由波的相位变化
# - 势的全部信息编码在相移中
#
# 低能散射主要由 l=0 (s波) 主导，
# 因为较高 l 的分波被离心势垒压制。
# =============================================================================
def phase_shift_hard_sphere(l, k, a):
    """
    硬球散射相移 Hard sphere phase shift

    tan(δ_l) = j_l(ka)/n_l(ka)

    硬球 (V=∞ 当 r<a) 是最简单的散射模型。
    波函数在 r=a 处必须为零（边界条件）。

    参数 Parameters:
        l: 角动量量子数
        k: 波矢 (1/m)
        a: 硬球半径 (m)

    返回 Returns:
        δ_l: 第l分波的相移 (rad)
    """
    x = k * a
    return np.arctan(spherical_jn(l, x) / spherical_yn(l, x))


def partial_wave_amplitude(l, delta_l, k):
    """
    分波振幅 Partial wave amplitude

    f_l = (2l+1)/k × exp(iδ_l)sin(δ_l) × P_l(cosθ)

    这里返回与角度无关的部分 (2l+1)exp(iδ_l)sin(δ_l)/k。

    当 δ_l = π/2 时，该分波达到最大散射（幺正极限）。

    参数 Parameters:
        l: 角动量量子数
        delta_l: 相移 (rad)
        k: 波矢 (1/m)

    返回 Returns:
        分波振幅（不含 P_l）
    """
    return (2*l + 1) / k * np.exp(1j * delta_l) * np.sin(delta_l)


def total_cross_section_partial_waves(k, delta_list):
    """
    总截面（分波求和）Total cross section from partial waves

    σ = 4π/k² × Σₗ(2l+1)sin²(δ_l)

    每个分波的最大贡献是 4π(2l+1)/k²（幺正极限）。
    低能时只有少数分波有显著贡献。

    参数 Parameters:
        k: 波矢 (1/m)
        delta_list: 各分波相移列表

    返回 Returns:
        σ: 总散射截面 (m²)
    """
    sigma = 0
    for l, delta in enumerate(delta_list):
        sigma += (2*l + 1) * np.sin(delta)**2
    return 4 * np.pi / k**2 * sigma

def scattering_amplitude_partial_waves(theta, k, delta_list):
    """
    散射振幅（分波展开）Scattering amplitude from partial waves

    f(θ) = (1/k)Σₗ(2l+1)exp(iδ_l)sin(δ_l)P_l(cosθ)

    P_l 是勒让德多项式，描述各分波的角分布:
    - l=0: 各向同性
    - l=1: 前后不对称
    - l=2: 四叶分布...

    参数 Parameters:
        theta: 散射角 (rad)
        k: 波矢 (1/m)
        delta_list: 各分波相移列表

    返回 Returns:
        f(θ): 散射振幅（复数）
    """
    from scipy.special import legendre
    f = 0
    cos_theta = np.cos(theta)
    for l, delta in enumerate(delta_list):
        P_l = legendre(l)
        f += (2*l + 1) * np.exp(1j * delta) * np.sin(delta) * P_l(cos_theta)
    return f / k


# =============================================================================
# 练习 14.3: 玻恩近似
# Exercise 14.3: Born Approximation
#
# 物理背景 Physical Background:
# 玻恩近似是弱散射极限下的微扰结果。
# 它将散射振幅表示为势能的傅里叶变换:
#
#   f(q) = -m/(2πℏ²) ∫V(r)exp(iq·r)d³r
#
# 有效性条件:
# - 势能弱: V << E
# - 或高能散射: k很大
#
# 玻恩近似给出了许多解析结果:
# - 汤川势
# - 库仑势（卢瑟福公式）
# - 高斯势
# =============================================================================
def born_amplitude_yukawa(q, V0, mu, m=m_e):
    """
    汤川势的玻恩近似散射振幅 Born amplitude for Yukawa potential

    V(r) = V₀ exp(-μr)/r
    f(q) = -2m/(ℏ²) × V₀/(q² + μ²)

    汤川势描述了短程相互作用（如核力）。
    μ → 0 极限给出库仑势。

    参数 Parameters:
        q: 动量转移 (1/m)
        V0: 势强度 (J·m)
        mu: 屏蔽参数 (1/m)
        m: 粒子质量 (kg)

    返回 Returns:
        f(q): 散射振幅 (m)
    """
    return -2 * m / hbar**2 * V0 / (q**2 + mu**2)


def born_amplitude_coulomb(q, Z1, Z2, m=m_e):
    """
    库仑势的玻恩近似（卢瑟福公式）Rutherford formula

    f(θ) = -Z₁Z₂e²m/(2ℏ²q²)

    这重现了卢瑟福散射的经典结果！
    量子和经典给出相同的微分截面（特殊情况）。

    参数 Parameters:
        q: 动量转移 (1/m)
        Z1, Z2: 电荷数
        m: 约化质量 (kg)

    返回 Returns:
        f(q): 散射振幅 (m)
    """
    e = 1.6e-19
    return -Z1 * Z2 * e**2 * m / (2 * hbar**2 * q**2)


def momentum_transfer(k, theta):
    """
    动量转移 Momentum transfer

    q = 2k sin(θ/2) = |k_f - k_i|

    动量转移是弹性散射的重要参数:
    - 前向散射 θ=0: q=0
    - 后向散射 θ=π: q=2k (最大)

    参数 Parameters:
        k: 波矢 (1/m)
        theta: 散射角 (rad)

    返回 Returns:
        q: 动量转移 (1/m)
    """
    return 2 * k * np.sin(theta / 2)


def rutherford_cross_section(Z1, Z2, E, theta):
    """
    卢瑟福散射截面 Rutherford cross section

    dσ/dΩ = (Z₁Z₂e²/(4E))² × 1/sin⁴(θ/2)

    特点:
    - θ→0 时发散（被屏蔽效应截断）
    - 与经典结果完全相同
    - 1/E² 依赖性

    卢瑟福实验发现原子核就是基于这个公式。

    参数 Parameters:
        Z1, Z2: 电荷数
        E: 质心能量 (J)
        theta: 散射角 (rad)

    返回 Returns:
        dσ/dΩ: 微分截面 (m²/sr)
    """
    e = 1.6e-19
    prefactor = (Z1 * Z2 * e**2 / (4 * E))**2
    return prefactor / np.sin(theta/2)**4


# =============================================================================
# 练习 14.4: 共振散射
# Exercise 14.4: Resonance Scattering
#
# 物理背景 Physical Background:
# 共振散射发生在入射能量接近准束缚态（共振态）能量时。
# 散射截面显著增强，体现了共振态的形成和衰变。
#
# Breit-Wigner公式描述共振线形:
# - 能量在 E_r 处有极大值
# - 宽度 Γ 与共振态寿命相关: τ = ℏ/Γ
# - 是洛伦兹线型
#
# 例子:
# - 核反应中的复合核共振
# - 粒子物理中的不稳定粒子
# - 原子物理中的Feshbach共振
# =============================================================================
def breit_wigner_cross_section(E, E_r, Gamma, l=0):
    """
    Breit-Wigner共振截面 Breit-Wigner resonance cross section

    σ_l = π/k² × (2l+1) × (Γ/2)² / ((E-E_r)² + (Γ/2)²)

    洛伦兹线型，在 E = E_r 处达到最大值。
    半高宽 (FWHM) 等于 Γ。

    参数 Parameters:
        E: 入射能量 (J)
        E_r: 共振能量 (J)
        Gamma: 共振宽度 (J)
        l: 分波角动量

    返回 Returns:
        σ: 散射截面 (m²)
    """
    k = wave_vector(E)
    return np.pi / k**2 * (2*l + 1) * (Gamma/2)**2 / ((E - E_r)**2 + (Gamma/2)**2)


def resonance_phase_shift(E, E_r, Gamma, delta_bg=0):
    """
    共振相移 Resonance phase shift

    δ = δ_bg + arctan(Γ/2 / (E_r - E))

    共振附近相移快速变化 π:
    - E << E_r: δ → δ_bg
    - E = E_r: δ = δ_bg + π/2
    - E >> E_r: δ → δ_bg + π

    参数 Parameters:
        E: 入射能量 (J)
        E_r: 共振能量 (J)
        Gamma: 共振宽度 (J)
        delta_bg: 背景相移 (rad)

    返回 Returns:
        δ: 相移 (rad)
    """
    return delta_bg + np.arctan(Gamma/2 / (E_r - E))


def resonance_width_lifetime(Gamma):
    """
    共振宽度与寿命的关系 Width-lifetime relation

    τ = ℏ/Γ

    这是能量-时间不确定性关系的体现:
    ΔE · Δt ~ ℏ

    参数 Parameters:
        Gamma: 共振宽度 (J)

    返回 Returns:
        τ: 共振态寿命 (s)
    """
    return hbar / Gamma

def fano_profile(E, E_r, Gamma, q):
    """
    Fano线型
    σ ∝ (q + ε)² / (1 + ε²)
    ε = (E - E_r)/(Γ/2)
    """
    epsilon = (E - E_r) / (Gamma / 2)
    return (q + epsilon)**2 / (1 + epsilon**2)


# =============================================================================
# 练习 14.5: 散射矩阵
# Exercise 14.5: S-Matrix
# =============================================================================
def s_matrix_element(delta):
    """
    S矩阵元
    S_l = exp(2iδ_l)
    """
    return np.exp(2j * delta)

def t_matrix_element(delta, k):
    """
    T矩阵元
    T_l = (S_l - 1)/(2ik) = exp(iδ_l)sin(δ_l)/k
    """
    return np.exp(1j * delta) * np.sin(delta) / k

def unitarity_check(S):
    """
    S矩阵幺正性检验
    |S_l| = 1 对于弹性散射
    """
    return np.abs(np.abs(S) - 1) < 1e-10

def cross_section_from_s_matrix(k, S_list):
    """
    从S矩阵计算截面
    σ = π/k² × Σ(2l+1)|1-S_l|²
    """
    sigma = 0
    for l, S in enumerate(S_list):
        sigma += (2*l + 1) * np.abs(1 - S)**2
    return np.pi / k**2 * sigma


# =============================================================================
# 练习 14.6: 逆散射问题
# Exercise 14.6: Inverse Scattering
# =============================================================================
def levinson_theorem(n_bound, delta_0):
    """
    Levinson定理
    δ(0) = nπ (n: 束缚态数目)
    验证相移在k=0时的值
    """
    return np.abs(delta_0 - n_bound * np.pi) < 0.1

def effective_range_expansion(k, a, r_e):
    """
    有效程展开
    k cot(δ) = -1/a + r_e k²/2 + ...
    """
    return -1/a + r_e * k**2 / 2

def reconstruct_potential_delta(delta_func, k_max, n_points=100):
    """
    从相移重建势能（概念性）
    使用变分原理或Gel'fand-Levitan方程
    返回示意性结果
    """
    # 简化：假设方势阱
    k_arr = np.linspace(0.01, k_max, n_points)
    delta_arr = [delta_func(k) for k in k_arr]
    # 散射长度估计
    a = -np.tan(delta_arr[0]) / k_arr[0] if delta_arr[0] != 0 else 0
    return a


# =============================================================================
# 可视化
# =============================================================================
def plot_scattering():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 硬球散射相移
    ax1 = axes[0, 0]
    a = 1e-10  # 1 Å
    k = np.linspace(0.1, 5, 100) / a

    for l in [0, 1, 2]:
        delta = [phase_shift_hard_sphere(l, ki, a) for ki in k]
        ax1.plot(k * a, delta, label=f'l = {l}', linewidth=2)

    ax1.set_xlabel('ka')
    ax1.set_ylabel('δ_l (rad)')
    ax1.set_title('硬球散射相移')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 微分截面
    ax2 = axes[0, 1]
    theta = np.linspace(0.01, np.pi, 200)
    k = 1e10  # 1/m
    delta_list = [0.5, 0.2, 0.05]  # l=0,1,2相移

    f = [scattering_amplitude_partial_waves(t, k, delta_list) for t in theta]
    dcs = [differential_cross_section(fi) for fi in f]

    ax2.semilogy(np.degrees(theta), np.array(dcs) * 1e20, 'b-', linewidth=2)
    ax2.set_xlabel('θ (度)')
    ax2.set_ylabel('dσ/dΩ (Å²/sr)')
    ax2.set_title('微分散射截面')
    ax2.grid(True, alpha=0.3)

    # 3. Breit-Wigner共振
    ax3 = axes[0, 2]
    E_r = 1  # 相对能量单位
    Gamma = 0.1

    E = np.linspace(0.5, 1.5, 200)
    sigma = [breit_wigner_cross_section(e, E_r, Gamma) for e in E]

    ax3.plot(E, sigma, 'b-', linewidth=2)
    ax3.axvline(x=E_r, color='r', linestyle='--', alpha=0.5, label='E_r')
    ax3.axvline(x=E_r - Gamma/2, color='g', linestyle=':', alpha=0.5)
    ax3.axvline(x=E_r + Gamma/2, color='g', linestyle=':', alpha=0.5, label='FWHM')
    ax3.set_xlabel('E/E_r')
    ax3.set_ylabel('σ (arb.)')
    ax3.set_title('Breit-Wigner共振')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 卢瑟福散射
    ax4 = axes[1, 0]
    theta = np.linspace(0.1, np.pi - 0.1, 200)
    E = 5 * 1.6e-19  # 5 MeV

    sigma_R = [rutherford_cross_section(2, 79, E, t) for t in theta]  # α+Au

    ax4.semilogy(np.degrees(theta), np.array(sigma_R) * 1e28, 'b-', linewidth=2)
    ax4.set_xlabel('θ (度)')
    ax4.set_ylabel('dσ/dΩ (barn/sr)')
    ax4.set_title('卢瑟福散射 (α+Au)')
    ax4.grid(True, alpha=0.3)

    # 5. 共振相移
    ax5 = axes[1, 1]
    E = np.linspace(0.5, 1.5, 200)
    E_r = 1
    Gamma = 0.1

    delta = [resonance_phase_shift(e, E_r, Gamma) for e in E]

    ax5.plot(E, delta, 'b-', linewidth=2)
    ax5.axhline(y=np.pi/2, color='r', linestyle='--', alpha=0.5, label='π/2')
    ax5.axvline(x=E_r, color='g', linestyle=':', alpha=0.5, label='E_r')
    ax5.set_xlabel('E/E_r')
    ax5.set_ylabel('δ (rad)')
    ax5.set_title('共振相移')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. Fano线型
    ax6 = axes[1, 2]
    E = np.linspace(0.5, 1.5, 200)
    E_r = 1
    Gamma = 0.1

    for q in [-2, 0, 2, np.inf]:
        if q == np.inf:
            sigma = [1 / (1 + ((e-E_r)/(Gamma/2))**2) for e in E]
            label = 'q → ∞ (Lorentz)'
        else:
            sigma = [fano_profile(e, E_r, Gamma, q) for e in E]
            label = f'q = {q}'
        ax6.plot(E, sigma, label=label, linewidth=1.5)

    ax6.set_xlabel('E/E_r')
    ax6.set_ylabel('σ (arb.)')
    ax6.set_title('Fano线型')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('scattering.png', dpi=150)
    print("图像已保存为 scattering.png")
    plt.show()


def verify():
    all_passed = True

    # Check 14.1
    f = 1 + 0.5j
    dcs = differential_cross_section(f)
    expected = np.abs(f)**2
    if not np.isclose(dcs, expected, rtol=0.01):
        print("❌ 14.1 微分截面计算错误")
        all_passed = False
    else:
        print(f"✓ 14.1 散射基础正确 (dσ/dΩ = |f|²)")

    # Check 14.2
    delta_list = [0.5, 0.2, 0.05]
    k = 1e10
    sigma = total_cross_section_partial_waves(k, delta_list)
    if sigma <= 0:
        print("❌ 14.2 总截面应为正")
        all_passed = False
    else:
        print(f"✓ 14.2 分波分析正确 (σ = {sigma:.2e} m²)")

    # Check 14.3
    q = 1e10  # 1/m
    f_born = born_amplitude_yukawa(q, 1e-19, 1e10)
    if f_born == 0:
        print("❌ 14.3 玻恩近似振幅不应为零")
        all_passed = False
    else:
        print("✓ 14.3 玻恩近似正确")

    # Check 14.4
    Gamma = 1e-15  # J
    tau = resonance_width_lifetime(Gamma)
    expected_tau = hbar / Gamma
    if not np.isclose(tau, expected_tau, rtol=0.01):
        print("❌ 14.4 共振寿命公式错误")
        all_passed = False
    else:
        print(f"✓ 14.4 共振散射正确 (τ = ℏ/Γ)")

    # Check 14.5
    delta = 0.5
    S = s_matrix_element(delta)
    if not unitarity_check(S):
        print("❌ 14.5 S矩阵应为幺正")
        all_passed = False
    else:
        print("✓ 14.5 散射矩阵正确 (|S| = 1)")

    # Check 14.6
    # Levinson定理检验
    if levinson_theorem(0, 0):
        print("✓ 14.6 Levinson定理正确 (0束缚态 → δ(0)=0)")
    else:
        print("❌ 14.6 Levinson定理检验失败")
        all_passed = False

    if all_passed:
        print("\n🎉 所有测试通过！")
        try:
            plot_scattering()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("量子散射理论 Quantum Scattering Theory")
    print("=" * 50)
    verify()
