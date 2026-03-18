"""
超材料与左手材料 Metamaterials and Left-Handed Materials
难度 Difficulty: ★★★★★

学习目标 Learning Objectives:
- 理解负折射率材料的物理基础 (Understand physics of negative index materials)
- 掌握超材料的电磁响应特性 (Master EM response of metamaterials)
- 分析Drude模型和谐振磁导率 (Analyze Drude model and resonant permeability)
- 理解完美透镜和超分辨成像 (Understand perfect lens and super-resolution imaging)
- 掌握变换光学和隐身斗篷原理 (Master transformation optics and cloaking)
- 了解超材料的实际结构设计 (Learn metamaterial structure design)

物理背景 Physical Background:
1. 左手材料 Left-Handed Materials (LHM):
   - Veselago于1968年理论预言：当 ε < 0 且 μ < 0 时，n < 0
   - 电场E、磁场H、波矢k构成左手坐标系（故名"左手材料"）
   - 相速度与群速度（能流）反向
   - 2000年由Smith等人首次实验实现

2. 负折射 Negative Refraction:
   - 折射光与入射光在法线同侧（异常折射）
   - 斯涅尔定律仍成立：n₁sinθ₁ = n₂sinθ₂
   - 当 n₂ < 0 时，θ₂ < 0

3. Drude模型 Drude Model:
   - 金属介电函数：ε(ω) = 1 - ω_p²/(ω² + iγω)
   - ω < ω_p 时，ε < 0（等离子体频率以下）
   - 金属线阵列可实现有效负介电常数

4. 谐振磁导率 Resonant Permeability:
   - 分裂环谐振器(SRR)可产生负磁导率
   - μ(ω) = 1 - Fω²/(ω² - ω_m² + iγω)
   - 在谐振频率附近 μ < 0

5. 完美透镜 Perfect Lens:
   - n = -1 的平板可放大倏逝波
   - 理论上可实现亚波长分辨率
   - 由Pendry于2000年提出

6. 变换光学 Transformation Optics:
   - 坐标变换等效于介质参数的调控
   - 隐身斗篷：光线绕过物体传播
   - 需要各向异性、非均匀的材料参数

核心公式 Key Formulas:
- 折射率 Refractive index: n = ±√(εμ)，ε<0且μ<0时取负号
- Drude介电函数 Drude permittivity: ε(ω) = 1 - ω_p²/ω²
- 等离子体频率 Plasma frequency: ω_p = √(n_e e²/(ε₀m))
- 完美透镜 Perfect lens (n=-1): 焦距 f = 板厚 d
- 品质因数 Figure of Merit: FOM = |Re(n)|/Im(n)
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import c, epsilon_0, mu_0

# I AM NOT DONE

# =============================================================================
# 练习 14.1: 负折射率
# Exercise 14.1: Negative Refractive Index
# =============================================================================
def refractive_index(epsilon_r, mu_r):
    """
    复折射率
    n = ±√(εμ)
    当 ε < 0 且 μ < 0 时，n < 0
    """
    n_squared = epsilon_r * mu_r
    n = np.sqrt(n_squared + 0j)
    # 负折射条件
    if np.real(epsilon_r) < 0 and np.real(mu_r) < 0:
        return -np.abs(n)
    return n

def snell_law_negative(n1, n2, theta1):
    """
    斯涅尔定律（包括负折射）
    n₁sinθ₁ = n₂sinθ₂
    负折射时折射角为负
    """
    sin_theta2 = n1 * np.sin(theta1) / n2
    if np.abs(sin_theta2) > 1:
        return None
    return np.arcsin(sin_theta2)

def phase_velocity(epsilon_r, mu_r):
    """
    相速度
    v_p = c/n
    """
    n = refractive_index(epsilon_r, mu_r)
    return c / np.abs(n)

def group_velocity_sign(epsilon_r, mu_r, d_epsilon, d_mu, d_omega):
    """
    群速度方向
    在左手材料中，群速度与相速度方向相反
    """
    n = refractive_index(epsilon_r, mu_r)
    # 简化：假设色散使群速度与相速度反向
    if np.real(n) < 0:
        return -1  # 反向
    return 1


# =============================================================================
# 练习 14.2: Drude模型介电函数
# Exercise 14.2: Drude Model Permittivity
# =============================================================================
def drude_permittivity(omega, omega_p, gamma=0):
    """
    Drude模型介电函数
    ε(ω) = 1 - ω_p²/(ω² + iγω)
    ω_p: 等离子体频率
    γ: 阻尼系数
    """
    return 1 - omega_p**2 / (omega**2 + 1j * gamma * omega)

def drude_permeability(omega, omega_m, F=0.5, gamma=0):
    """
    谐振磁导率（分裂环谐振器）
    μ(ω) = 1 - Fω²/(ω² - ω_m² + iγω)
    """
    return 1 - F * omega**2 / (omega**2 - omega_m**2 + 1j * gamma * omega)

def plasma_frequency(n_e, m_eff, epsilon_r=1):
    """
    等离子体频率
    ω_p = √(n_e e²/(ε₀ε_r m_eff))
    """
    e = 1.6e-19
    return np.sqrt(n_e * e**2 / (epsilon_0 * epsilon_r * m_eff))

def negative_index_bandwidth(omega_p, omega_m):
    """
    负折射率频带
    当 ε < 0 且 μ < 0 时
    """
    # 简化：假设在 ω_m < ω < ω_p 范围内
    return omega_p - omega_m


# =============================================================================
# 练习 14.3: 完美透镜
# Exercise 14.3: Perfect Lens
# =============================================================================
def perfect_lens_focal_length(d, n=-1):
    """
    完美透镜焦距
    对于 n = -1 的平板，f = d（板厚）
    """
    if n == -1:
        return d
    return np.inf

def evanescent_wave_amplification(k_x, k_0, d, n=-1):
    """
    倏逝波放大
    完美透镜可放大倏逝波，恢复亚波长信息
    """
    if n != -1:
        return 0
    k_z = np.sqrt(k_0**2 - k_x**2 + 0j)
    if np.real(k_z) == 0:  # 倏逝波
        return np.exp(np.abs(np.imag(k_z)) * d)
    return 1

def superlens_resolution(wavelength):
    """
    超透镜理论分辨率
    理论上可突破衍射极限
    """
    return wavelength / 10  # 理论可达 λ/10 量级

def transfer_function_perfect_lens(k_x, k_0, d):
    """
    完美透镜传递函数
    所有空间频率分量相位一致
    """
    k_z = np.sqrt(k_0**2 - k_x**2 + 0j)
    return np.exp(1j * k_z * d) * np.exp(-1j * k_z * d)  # = 1


# =============================================================================
# 练习 14.4: 变换光学
# Exercise 14.4: Transformation Optics
# =============================================================================
def coordinate_transformation_cloak(r, R1, R2):
    """
    隐身斗篷坐标变换
    将 r < R1 区域压缩到 R1 < r' < R2
    r' = R1 + r(R2 - R1)/R2
    """
    return R1 + r * (R2 - R1) / R2

def cloak_permittivity_radial(r, R1, R2):
    """
    斗篷材料径向介电常数
    ε_r = μ_r = (r - R1)/r
    """
    if r <= R1:
        return 0  # 内部隐藏区域
    return (r - R1) / r

def cloak_permittivity_theta(r, R1, R2):
    """
    斗篷材料角向介电常数
    ε_θ = μ_θ = r/(r - R1)
    """
    if r <= R1:
        return np.inf
    return r / (r - R1)

def effective_medium_parameter(epsilon_1, epsilon_2, f):
    """
    有效介质近似
    ε_eff = f×ε₁ + (1-f)×ε₂ (Maxwell-Garnett)
    f: 填充因子
    """
    return f * epsilon_1 + (1 - f) * epsilon_2


# =============================================================================
# 练习 14.5: 超材料结构
# Exercise 14.5: Metamaterial Structures
# =============================================================================
def split_ring_resonance(L, C):
    """
    分裂环谐振器（SRR）谐振频率
    ω_0 = 1/√(LC)
    """
    return 1 / np.sqrt(L * C)

def wire_medium_plasma_freq(a, r_wire):
    """
    金属线阵列等效等离子体频率
    ω_p² = 2πc²/(a² ln(a/r))
    a: 线间距
    r_wire: 线半径
    """
    return np.sqrt(2 * np.pi * c**2 / (a**2 * np.log(a / r_wire)))

def fishnet_structure_index(omega, omega_e, omega_m, gamma_e, gamma_m):
    """
    渔网结构等效折射率
    """
    epsilon = drude_permittivity(omega, omega_e, gamma_e)
    mu = drude_permeability(omega, omega_m, 0.5, gamma_m)
    return refractive_index(epsilon, mu)

def unit_cell_size_requirement(wavelength, n_eff):
    """
    单元格尺寸要求
    a << λ/|n|（有效介质条件）
    """
    return wavelength / (10 * np.abs(n_eff))


# =============================================================================
# 练习 14.6: 应用
# Exercise 14.6: Applications
# =============================================================================
def negative_refraction_beam_shift(theta, d, n=-1):
    """
    负折射光束位移
    Δx = d × tan(θ_r) - d × tan(-θ_t)
    """
    theta_t = snell_law_negative(1, n, theta)
    if theta_t is None:
        return 0
    return d * (np.tan(theta) + np.tan(theta_t))

def hyperlens_magnification(R_inner, R_outer):
    """
    超透镜放大率
    M = R_outer/R_inner
    """
    return R_outer / R_inner

def absorber_impedance_matching(epsilon_r, mu_r):
    """
    完美吸收体阻抗匹配条件
    Z = Z_0 = √(μ₀/ε₀) 当 μ_r = ε_r
    """
    Z_0 = np.sqrt(mu_0 / epsilon_0)
    Z = Z_0 * np.sqrt(mu_r / epsilon_r)
    return np.abs(Z - Z_0) / Z_0  # 阻抗失配

def figure_of_merit(n_real, n_imag):
    """
    品质因数（负折射率材料）
    FOM = |Re(n)|/Im(n)
    """
    return np.abs(n_real) / np.abs(n_imag)


# =============================================================================
# 可视化
# =============================================================================
def plot_metamaterials():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. Drude介电函数
    ax1 = axes[0, 0]
    omega = np.linspace(0.1, 3, 200)
    omega_p = 1

    eps = [drude_permittivity(w, omega_p, 0.1) for w in omega]
    eps_real = [np.real(e) for e in eps]
    eps_imag = [np.imag(e) for e in eps]

    ax1.plot(omega/omega_p, eps_real, 'b-', label="ε' (实部)", linewidth=2)
    ax1.plot(omega/omega_p, eps_imag, 'r--', label="ε'' (虚部)", linewidth=2)
    ax1.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax1.axvline(x=1, color='g', linestyle=':', alpha=0.5, label='ω_p')
    ax1.set_xlabel('ω/ω_p')
    ax1.set_ylabel('ε')
    ax1.set_title('Drude介电函数')
    ax1.set_ylim(-5, 2)
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 负折射
    ax2 = axes[0, 1]
    theta = np.linspace(0, np.pi/2 - 0.1, 100)

    # 正常折射
    theta_t_pos = [np.degrees(snell_law_negative(1, 1.5, t)) for t in theta]
    # 负折射
    theta_t_neg = [np.degrees(snell_law_negative(1, -1.5, t)) for t in theta]

    ax2.plot(np.degrees(theta), theta_t_pos, 'b-', label='n = 1.5', linewidth=2)
    ax2.plot(np.degrees(theta), theta_t_neg, 'r-', label='n = -1.5', linewidth=2)
    ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax2.set_xlabel('入射角 (度)')
    ax2.set_ylabel('折射角 (度)')
    ax2.set_title('正折射 vs 负折射')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 折射率频谱
    ax3 = axes[0, 2]
    omega = np.linspace(0.5, 2, 200)
    omega_p, omega_m = 1.5, 1.0

    n_list = []
    for w in omega:
        eps = drude_permittivity(w, omega_p, 0.05)
        mu = drude_permeability(w, omega_m, 0.5, 0.05)
        n = refractive_index(eps, mu)
        n_list.append(n)

    n_real = [np.real(n) for n in n_list]
    n_imag = [np.imag(n) for n in n_list]

    ax3.plot(omega, n_real, 'b-', label="Re(n)", linewidth=2)
    ax3.plot(omega, n_imag, 'r--', label="Im(n)", linewidth=2)
    ax3.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax3.axvline(x=omega_m, color='g', linestyle=':', alpha=0.5, label='ω_m')
    ax3.axvline(x=omega_p, color='orange', linestyle=':', alpha=0.5, label='ω_p')
    ax3.set_xlabel('ω')
    ax3.set_ylabel('n')
    ax3.set_title('超材料折射率频谱')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 斗篷材料参数
    ax4 = axes[1, 0]
    R1, R2 = 1, 2
    r = np.linspace(R1 + 0.01, R2, 100)

    eps_r = [cloak_permittivity_radial(ri, R1, R2) for ri in r]
    eps_theta = [cloak_permittivity_theta(ri, R1, R2) for ri in r]

    ax4.plot(r, eps_r, 'b-', label='ε_r = μ_r', linewidth=2)
    ax4.plot(r, eps_theta, 'r-', label='ε_θ = μ_θ', linewidth=2)
    ax4.axvline(x=R1, color='g', linestyle='--', alpha=0.5, label='R₁')
    ax4.axvline(x=R2, color='orange', linestyle='--', alpha=0.5, label='R₂')
    ax4.set_xlabel('r')
    ax4.set_ylabel('材料参数')
    ax4.set_title('隐身斗篷材料参数')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 完美透镜成像
    ax5 = axes[1, 1]
    # 示意图
    x = np.linspace(-2, 4, 500)
    d = 1  # 透镜厚度

    # 物点
    ax5.plot(-1, 0, 'ro', markersize=10, label='物点')
    # 透镜
    ax5.axvspan(0, d, alpha=0.3, color='blue', label='n=-1透镜')
    # 像点
    ax5.plot(2, 0, 'g^', markersize=10, label='像点')
    # 光线
    ax5.plot([-1, 0], [0, 0.5], 'r-', linewidth=1)
    ax5.plot([0, d], [0.5, 0], 'r-', linewidth=1)  # 负折射
    ax5.plot([d, 2], [0, 0], 'r-', linewidth=1)

    ax5.set_xlim(-2, 3)
    ax5.set_ylim(-1, 1)
    ax5.set_xlabel('x')
    ax5.set_ylabel('y')
    ax5.set_title('完美透镜成像 (n=-1)')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. 品质因数
    ax6 = axes[1, 2]
    n_imag_range = np.linspace(0.01, 0.5, 100)
    n_real = -1

    FOM = [figure_of_merit(n_real, ni) for ni in n_imag_range]

    ax6.semilogy(n_imag_range, FOM, 'b-', linewidth=2)
    ax6.axhline(y=1, color='r', linestyle='--', alpha=0.5, label='FOM = 1')
    ax6.set_xlabel("Im(n)")
    ax6.set_ylabel('FOM = |Re(n)|/Im(n)')
    ax6.set_title('超材料品质因数')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('metamaterials.png', dpi=150)
    print("图像已保存为 metamaterials.png")
    plt.show()


def verify():
    all_passed = True

    # Check 14.1
    n = refractive_index(-1, -1)
    if np.real(n) >= 0:
        print("❌ 14.1 ε<0且μ<0时折射率应为负")
        all_passed = False
    else:
        print(f"✓ 14.1 负折射率正确 (n = {np.real(n):.1f})")

    # Check 14.2
    eps = drude_permittivity(0.5, 1)
    if np.real(eps) >= 0:
        print("❌ 14.2 ω<ω_p时介电常数应为负")
        all_passed = False
    else:
        print(f"✓ 14.2 Drude模型正确 (ε(ω<ω_p) < 0)")

    # Check 14.3
    f = perfect_lens_focal_length(1, n=-1)
    if f != 1:
        print("❌ 14.3 n=-1平板焦距应等于板厚")
        all_passed = False
    else:
        print("✓ 14.3 完美透镜正确 (f = d)")

    # Check 14.4
    eps_r = cloak_permittivity_radial(1.5, 1, 2)
    if eps_r <= 0 or eps_r >= 1:
        print("❌ 14.4 斗篷材料参数不合理")
        all_passed = False
    else:
        print(f"✓ 14.4 变换光学正确 (ε_r = {eps_r:.2f})")

    # Check 14.5
    omega_0 = split_ring_resonance(1e-9, 1e-12)
    if omega_0 <= 0:
        print("❌ 14.5 SRR谐振频率应为正")
        all_passed = False
    else:
        print(f"✓ 14.5 超材料结构正确 (ω_0 = {omega_0:.2e} rad/s)")

    # Check 14.6
    FOM = figure_of_merit(-1, 0.1)
    if FOM <= 0:
        print("❌ 14.6 品质因数应为正")
        all_passed = False
    else:
        print(f"✓ 14.6 品质因数正确 (FOM = {FOM:.1f})")

    if all_passed:
        print("\n🎉 所有测试通过！")
        try:
            plot_metamaterials()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("超材料与左手材料 Metamaterials and Left-Handed Materials")
    print("=" * 50)
    verify()
