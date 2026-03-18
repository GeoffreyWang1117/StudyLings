"""
量子电动力学入门 QED Introduction
难度 Difficulty: ★★★★★

================================================================================
学习目标 Learning Objectives
================================================================================
- 理解量子电动力学(QED)的基本结构和费曼规则
  Understand the basic structure of QED and Feynman rules
- 掌握费曼传播子（光子和电子）的形式和物理意义
  Master Feynman propagators (photon and electron) and their physical meaning
- 计算基本散射过程：库仑散射、康普顿散射、正负电子湮灭
  Calculate basic scattering processes: Coulomb, Compton, pair annihilation

================================================================================
物理背景 Physical Background
================================================================================
量子电动力学(QED)是描述电磁相互作用的量子场论，是第一个成功的量子场论。
它描述电子、正电子与光子之间的相互作用，精度达到10^-12量级。

QED (Quantum Electrodynamics) is the quantum field theory describing
electromagnetic interactions, the first successful QFT with precision ~10^-12.

核心概念 Key Concepts:
1. 费曼图 Feynman Diagrams: 可视化量子过程的工具
2. 传播子 Propagators: 描述粒子的传播（虚粒子）
3. 顶点 Vertices: 描述相互作用点，每个顶点贡献因子 ieγ^μ
4. 散射振幅 Scattering Amplitude: 由费曼图规则计算

费曼规则 Feynman Rules (动量空间):
- 光子传播子: D_μν(q) = -ig_μν/(q² + iε)
- 电子传播子: S(p) = i(γ·p + m)/(p² - m² + iε)
- QED顶点: Γ^μ = ieγ^μ
- 外线因子: 入射/出射电子 u/ū, 光子 ε_μ

重要散射过程 Important Processes:
- 卢瑟福散射: e⁻ + 核 → e⁻ + 核 (库仑散射)
- 莫特散射: 考虑自旋的相对论性电子散射
- 康普顿散射: γ + e⁻ → γ + e⁻
- 穆勒散射: e⁻ + e⁻ → e⁻ + e⁻
- 巴巴散射: e⁺ + e⁻ → e⁺ + e⁻
- 正负电子湮灭: e⁺ + e⁻ → γ + γ

HINT: QED顶点: ieγ^μ，精细结构常数 α ≈ 1/137
HINT: 光子传播子: -ig_μν/(q² + iε)，iε保证因果性
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma as gamma_func
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import hbar, c, m_e, e, epsilon_0, alpha, MeV

# I AM NOT DONE

# 精细结构常数
alpha_em = alpha  # ≈ 1/137

# =============================================================================
# 练习 11.1: 费曼传播子
# Exercise 11.1: Feynman Propagators
#
# 物理背景 Physical Background:
# 传播子描述虚粒子在两点之间的传播，是量子场论的核心对象。
# 光子传播子来自麦克斯韦方程的格林函数，在费曼规范下形式简单。
# 电子传播子来自狄拉克方程的格林函数，包含γ矩阵结构。
#
# 公式 Formulas:
# - 光子: D_μν(q) = -ig_μν/(q² + iε)  [费曼规范]
# - 电子: S(p) = i(γ·p + m)/(p² - m² + iε)
# - iε项保证费曼因果边界条件
#
# 物理意义: 传播子的极点对应物理粒子（在壳条件 p² = m²）
# =============================================================================
def photon_propagator(q, mu, nu):
    """
    计算光子传播子（费曼规范）Calculate photon propagator (Feynman gauge)

    公式 Formula: D_μν(q) = -ig_μν / (q² + iε)

    参数 Parameters:
        q: 四动量 [E/c, px, py, pz]，单位自然单位制
        mu, nu: 洛伦兹指标 (0,1,2,3)

    返回 Returns:
        D_μν(q): 传播子矩阵元（复数）

    物理意义: 光子传播子描述虚光子的传播，出现在所有电磁相互作用中
    """
    # TODO: 计算光子传播子
    eta = np.diag([1, -1, -1, -1])
    q_squared = q[0]**2 - q[1]**2 - q[2]**2 - q[3]**2 + 1j * 1e-10

    return -1j * eta[mu, nu] / q_squared

def electron_propagator(p, m):
    """
    电子传播子
    S(p) = i(γ·p + m) / (p² - m² + iε)

    返回 4x4 矩阵
    """
    # γ矩阵
    sigma_1 = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma_2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma_3 = np.array([[1, 0], [0, -1]], dtype=complex)
    I2 = np.eye(2, dtype=complex)
    O2 = np.zeros((2, 2), dtype=complex)

    gamma_0 = np.block([[I2, O2], [O2, -I2]])
    gamma_1 = np.block([[O2, sigma_1], [-sigma_1, O2]])
    gamma_2 = np.block([[O2, sigma_2], [-sigma_2, O2]])
    gamma_3 = np.block([[O2, sigma_3], [-sigma_3, O2]])

    # γ·p
    slash_p = gamma_0 * p[0] - gamma_1 * p[1] - gamma_2 * p[2] - gamma_3 * p[3]

    # p² - m²
    p_squared = p[0]**2 - p[1]**2 - p[2]**2 - p[3]**2
    denominator = p_squared - m**2 + 1j * 1e-10

    return 1j * (slash_p + m * np.eye(4)) / denominator


# =============================================================================
# 练习 11.2: QED顶点
# Exercise 11.2: QED Vertex
# =============================================================================
def qed_vertex(mu):
    """
    QED顶点因子
    Γ^μ = ieγ^μ
    """
    # TODO: 返回顶点因子
    sigma_1 = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma_2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma_3 = np.array([[1, 0], [0, -1]], dtype=complex)
    I2 = np.eye(2, dtype=complex)
    O2 = np.zeros((2, 2), dtype=complex)

    gamma = [
        np.block([[I2, O2], [O2, -I2]]),
        np.block([[O2, sigma_1], [-sigma_1, O2]]),
        np.block([[O2, sigma_2], [-sigma_2, O2]]),
        np.block([[O2, sigma_3], [-sigma_3, O2]])
    ]

    return 1j * np.sqrt(4 * np.pi * alpha_em) * gamma[mu]

def vertex_correction_factor(q_squared):
    """
    顶点修正因子（一阶近似）
    F_1(q²) ≈ 1 - α/(3π) ln(|q²|/m²)
    """
    m = 1  # 归一化
    if abs(q_squared) < 1e-10:
        return 1.0

    correction = 1 - alpha_em / (3 * np.pi) * np.log(abs(q_squared) / m**2)
    return correction


# =============================================================================
# 练习 11.3: 库仑散射
# Exercise 11.3: Coulomb Scattering
# =============================================================================
def rutherford_cross_section(E, theta, Z=1):
    """
    卢瑟福散射截面（经典）
    dσ/dΩ = (Zα/2E)² / sin⁴(θ/2)
    """
    return (Z * alpha_em / (2 * E))**2 / np.sin(theta/2)**4

def mott_cross_section(E, theta, m=m_e):
    """
    莫特散射截面（相对论电子）
    包含自旋效应
    dσ/dΩ = (dσ/dΩ)_Rutherford × [1 - β²sin²(θ/2)]
    """
    gamma_val = E / (m * c**2) + 1
    beta = np.sqrt(1 - 1/gamma_val**2)

    rutherford = rutherford_cross_section(E, theta)
    spin_factor = 1 - beta**2 * np.sin(theta/2)**2

    return rutherford * spin_factor

def form_factor_correction(q_squared, R):
    """
    形状因子修正（有限尺寸效应）
    F(q²) = exp(-q²R²/6)
    """
    return np.exp(-abs(q_squared) * R**2 / 6)


# =============================================================================
# 练习 11.4: 电子-电子散射
# Exercise 11.4: Electron-Electron Scattering
# =============================================================================
def moller_cross_section(E_cm, theta):
    """
    穆勒散射截面（e⁻e⁻ → e⁻e⁻）
    高能近似（m→0）
    """
    s = E_cm**2  # 质心系能量平方
    cos_theta = np.cos(theta)

    # 简化公式
    sigma = (alpha_em**2 / s) * \
            (1 + cos_theta**2) / (1 - cos_theta**2)**2

    return sigma

def bhabha_cross_section(E_cm, theta):
    """
    Bhabha散射截面（e⁺e⁻ → e⁺e⁻）
    """
    s = E_cm**2
    cos_theta = np.cos(theta)
    t = -s * (1 - cos_theta) / 2

    # s道和t道干涉
    sigma = (alpha_em**2 / s) * \
            ((1 + cos_theta**2) / (1 - cos_theta)**2 +
             (1 + cos_theta) / 2)

    return sigma


# =============================================================================
# 练习 11.5: 康普顿散射
# Exercise 11.5: Compton Scattering
# =============================================================================
def klein_nishina(E_gamma, theta, m=m_e):
    """
    Klein-Nishina公式
    康普顿散射微分截面

    E_gamma: 入射光子能量
    theta: 散射角
    """
    # TODO: 计算Klein-Nishina截面
    r_e = alpha_em * hbar / (m * c)  # 电子经典半径
    x = E_gamma / (m * c**2)  # 无量纲能量

    cos_theta = np.cos(theta)
    P = 1 / (1 + x * (1 - cos_theta))  # 能量比

    # Klein-Nishina公式
    dsigma = 0.5 * r_e**2 * P**2 * (P + 1/P - np.sin(theta)**2)

    return dsigma

def compton_wavelength_shift(theta, m=m_e):
    """
    康普顿波长位移
    Δλ = (h/mc)(1 - cos θ)
    """
    lambda_c = hbar / (m * c)  # 康普顿波长
    return lambda_c * (1 - np.cos(theta))

def compton_scattered_energy(E_gamma, theta, m=m_e):
    """
    散射光子能量
    E' = E / [1 + (E/mc²)(1 - cos θ)]
    """
    x = E_gamma / (m * c**2)
    return E_gamma / (1 + x * (1 - np.cos(theta)))


# =============================================================================
# 练习 11.6: 正负电子湮灭
# Exercise 11.6: Electron-Positron Annihilation
# =============================================================================
def pair_annihilation_cross_section(E_cm):
    """
    e⁺e⁻ → γγ 截面
    高能极限: σ ∝ 1/E²
    """
    r_e = alpha_em * hbar / (m_e * c)

    # 低能近似
    v = np.sqrt(1 - (2 * m_e * c**2 / E_cm)**2) if E_cm > 2 * m_e * c**2 else 0

    if v < 1e-10:
        return 0

    sigma = np.pi * r_e**2 / v * \
            ((3 - v**4) / (2 * v) * np.log((1 + v) / (1 - v)) - 2 + v**2)

    return sigma

def pair_production_threshold(m=m_e):
    """
    正负电子对产生阈能
    E_th = 2mc²（在质心系）
    """
    return 2 * m * c**2

def annihilation_photon_energy(E_cm):
    """
    湮灭光子能量（质心系）
    每个光子 E_γ = E_cm/2
    """
    return E_cm / 2


# =============================================================================
# 可视化
# =============================================================================
def plot_qed_basics():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 穆勒vs巴巴散射
    ax1 = axes[0, 0]
    theta = np.linspace(0.1, np.pi - 0.1, 100)
    E_cm = 10  # 归一化

    moller = [moller_cross_section(E_cm, t) for t in theta]
    bhabha = [bhabha_cross_section(E_cm, t) for t in theta]

    ax1.semilogy(np.degrees(theta), moller, 'b-', linewidth=2, label='e⁻e⁻ (Moller)')
    ax1.semilogy(np.degrees(theta), bhabha, 'r-', linewidth=2, label='e⁺e⁻ (Bhabha)')
    ax1.set_xlabel('散射角 (度)')
    ax1.set_ylabel('dσ/dΩ (arb.)')
    ax1.set_title('电子散射截面')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. Klein-Nishina
    ax2 = axes[0, 1]

    for E_ratio in [0.1, 1, 10]:
        E_gamma = E_ratio * m_e * c**2
        kn = [klein_nishina(E_gamma, t) for t in theta]
        ax2.plot(np.degrees(theta), kn, label=f'E/mc² = {E_ratio}', linewidth=2)

    ax2.set_xlabel('散射角 (度)')
    ax2.set_ylabel('dσ/dΩ')
    ax2.set_title('Klein-Nishina公式')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 康普顿散射能量
    ax3 = axes[0, 2]
    E_gamma = m_e * c**2  # 511 keV

    E_scattered = [compton_scattered_energy(E_gamma, t) / (m_e * c**2) for t in theta]

    ax3.plot(np.degrees(theta), E_scattered, 'b-', linewidth=2)
    ax3.axhline(y=0.5, color='r', linestyle='--', label='E\'/E_0 = 1/2')
    ax3.set_xlabel('散射角 (度)')
    ax3.set_ylabel("E'/mc²")
    ax3.set_title('康普顿散射能量')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 莫特vs卢瑟福
    ax4 = axes[1, 0]
    E = 1 * MeV  # 1 MeV电子
    theta_mott = np.linspace(0.1, np.pi, 100)

    ruth = [rutherford_cross_section(E, t) for t in theta_mott]
    mott = [mott_cross_section(E, t) for t in theta_mott]

    ax4.semilogy(np.degrees(theta_mott), ruth, 'b--', linewidth=2, label='Rutherford')
    ax4.semilogy(np.degrees(theta_mott), mott, 'r-', linewidth=2, label='Mott')
    ax4.set_xlabel('散射角 (度)')
    ax4.set_ylabel('dσ/dΩ (arb.)')
    ax4.set_title('莫特散射修正')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 正负电子湮灭截面
    ax5 = axes[1, 1]
    E_cm_vals = np.linspace(1.1, 10, 100) * (2 * m_e * c**2)

    sigma_ann = [pair_annihilation_cross_section(E) * 1e28 for E in E_cm_vals]  # barn

    ax5.plot(E_cm_vals / (m_e * c**2), sigma_ann, 'b-', linewidth=2)
    ax5.set_xlabel('E_cm / mc²')
    ax5.set_ylabel('σ (×10⁻²⁸ m²)')
    ax5.set_title('e⁺e⁻ → γγ 截面')
    ax5.grid(True, alpha=0.3)

    # 6. 费曼图示意（用箭头和线）
    ax6 = axes[1, 2]
    ax6.set_xlim(-2, 2)
    ax6.set_ylim(-2, 2)

    # 电子线
    ax6.annotate('', xy=(0, 0), xytext=(-1.5, 1),
                arrowprops=dict(arrowstyle='->', color='blue', lw=2))
    ax6.annotate('', xy=(1.5, 1), xytext=(0, 0),
                arrowprops=dict(arrowstyle='->', color='blue', lw=2))

    # 光子线（波浪）
    x_photon = np.linspace(0, 1.5, 50)
    y_photon = -1 + 0.1 * np.sin(20 * x_photon)
    ax6.plot(x_photon, y_photon, 'r-', linewidth=2)

    # 顶点
    ax6.scatter([0], [0], s=100, c='black', zorder=5)

    ax6.text(-1.2, 1.2, 'e⁻', fontsize=12)
    ax6.text(1.2, 1.2, 'e⁻', fontsize=12)
    ax6.text(1.2, -0.7, 'γ', fontsize=12)
    ax6.text(0.2, -0.3, 'ieγ^μ', fontsize=10)

    ax6.set_title('QED顶点示意')
    ax6.axis('off')

    plt.tight_layout()
    plt.savefig('qed_basics.png', dpi=150)
    print("图像已保存为 qed_basics.png")
    plt.show()


def verify():
    all_passed = True

    # Check 11.1
    q = [1, 0, 0, 0]
    D = photon_propagator(q, 0, 0)
    if np.imag(D) == 0:
        print("❌ 11.1 光子传播子应有虚部")
        all_passed = False
    else:
        print(f"✓ 11.1 费曼传播子正确")

    # Check 11.2
    Gamma = qed_vertex(0)
    if Gamma.shape != (4, 4):
        print("❌ 11.2 QED顶点维度错误")
        all_passed = False
    else:
        print(f"✓ 11.2 QED顶点正确 (∝ ieγ^μ)")

    # Check 11.3
    sigma_ruth = rutherford_cross_section(1, np.pi/4)
    if sigma_ruth <= 0:
        print("❌ 11.3 卢瑟福截面应为正")
        all_passed = False
    else:
        print(f"✓ 11.3 库仑散射正确")

    # Check 11.4
    sigma_moller = moller_cross_section(10, np.pi/2)
    sigma_bhabha = bhabha_cross_section(10, np.pi/2)
    if sigma_moller <= 0 or sigma_bhabha <= 0:
        print("❌ 11.4 散射截面应为正")
        all_passed = False
    else:
        print(f"✓ 11.4 电子-电子散射正确")

    # Check 11.5
    delta_lambda = compton_wavelength_shift(np.pi)
    lambda_c = hbar / (m_e * c)
    if not np.isclose(delta_lambda, 2 * lambda_c, rtol=0.01):
        print("❌ 11.5 康普顿位移θ=π时应为2λ_c")
        all_passed = False
    else:
        print(f"✓ 11.5 康普顿散射正确 (Δλ_max = 2λ_c)")

    # Check 11.6
    E_th = pair_production_threshold()
    if E_th != 2 * m_e * c**2:
        print("❌ 11.6 对产生阈能应为2mc²")
        all_passed = False
    else:
        print(f"✓ 11.6 正负电子湮灭正确 (E_th = {E_th/MeV:.3f} MeV)")

    if all_passed:
        print("\n🎉 所有测试通过！")
        try:
            plot_qed_basics()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("量子电动力学入门 QED Introduction")
    print("=" * 50)
    verify()
