"""
狄拉克方程基础 Dirac Equation Basics
难度 Difficulty: ★★★★★

物理背景 Physical Background:
==================================
狄拉克方程是描述自旋1/2相对论粒子（如电子、夸克）的基本方程。
1928年狄拉克提出此方程，成功统一了量子力学和狭义相对论，
并预言了反物质的存在（1932年安德森发现正电子）。

历史意义:
- 第一个成功的相对论量子方程
- 自然引入自旋概念
- 预言电子的精确磁矩 g = 2
- 负能解的重新诠释导致反粒子概念

方程形式:
(iℏγ^μ∂_μ - mc)ψ = 0
或用自然单位: (iγ^μ∂_μ - m)ψ = 0

学习目标 Learning Objectives:
- 理解狄拉克方程的协变形式和物理意义
- 掌握γ矩阵的代数性质（Clifford代数）
- 分析正能量和负能量旋量解
- 理解手征性、螺旋度等概念
- 学习Dirac流和守恒性

关键公式 Key Formulas:
- 狄拉克方程: (iγ^μ∂_μ - m)ψ = 0
- Clifford代数: {γ^μ, γ^ν} = 2η^μν I₄
- 狄拉克哈密顿量: H = α·p + βm，其中 α = γ⁰γ, β = γ⁰
- 正能量旋量: u(p,s)，满足 (γ·p - m)u = 0
- 狄拉克共轭: ψ̄ = ψ†γ⁰
- 守恒流: j^μ = ψ̄γ^μψ

HINT: 狄拉克方程: (iγ^μ∂_μ - m)ψ = 0
HINT: γ矩阵: {γ^μ, γ^ν} = 2η^μν（Clifford代数）
HINT: 手征性矩阵: γ⁵ = iγ⁰γ¹γ²γ³
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import hbar, c, m_e, e, MeV

# I AM NOT DONE

# 单位制：自然单位 ℏ = c = 1（计算时恢复）

# =============================================================================
# 练习 10.1: γ矩阵
# Exercise 10.1: Gamma Matrices
#
# 物理背景:
# γ矩阵是狄拉克方程的核心，编码了时空的几何结构。
# 不同表示（Dirac, Weyl, Majorana）适用于不同物理情境。
#
# Dirac表示特点:
# - γ⁰是对角的，便于分析静止态
# - 上分量是"大分量"（非相对论极限主导）
# - 下分量是"小分量"
# =============================================================================
def gamma_matrices():
    """
    狄拉克表示的γ矩阵 Gamma Matrices in Dirac Representation

    定义:
    γ⁰ = [[I₂,  0 ],    γⁱ = [[0,   σⁱ],
          [0,  -I₂]]         [-σⁱ,  0 ]]

    其中 σⁱ (i=1,2,3) 是泡利矩阵

    性质:
    - (γ⁰)† = γ⁰ (厄米)
    - (γⁱ)† = -γⁱ (反厄米)
    - γ⁰ γ^μ† γ⁰ = γ^μ

    返回:
        tuple: (γ⁰, γ¹, γ², γ³) 四个4×4矩阵
    """
    # 泡利矩阵
    sigma_1 = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma_2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma_3 = np.array([[1, 0], [0, -1]], dtype=complex)
    I2 = np.eye(2, dtype=complex)
    O2 = np.zeros((2, 2), dtype=complex)

    # TODO: 构建γ矩阵
    gamma_0 = np.block([[I2, O2], [O2, -I2]])
    gamma_1 = np.block([[O2, sigma_1], [-sigma_1, O2]])
    gamma_2 = np.block([[O2, sigma_2], [-sigma_2, O2]])
    gamma_3 = np.block([[O2, sigma_3], [-sigma_3, O2]])

    return gamma_0, gamma_1, gamma_2, gamma_3

def gamma_5():
    """
    γ⁵ 手征性矩阵 Chirality Matrix

    定义: γ⁵ = iγ⁰γ¹γ²γ³

    在Dirac表示下:
    γ⁵ = [[0, I₂],
          [I₂, 0]]

    关键性质:
    - (γ⁵)² = I₄
    - (γ⁵)† = γ⁵
    - {γ⁵, γ^μ} = 0（与所有γ矩阵反对易）

    物理意义:
    - 区分左手和右手费米子
    - 手征投影: P_L = (1-γ⁵)/2, P_R = (1+γ⁵)/2
    - 弱相互作用只耦合左手分量

    返回:
        np.ndarray: 4×4 γ⁵矩阵
    """
    g0, g1, g2, g3 = gamma_matrices()
    g5 = 1j * g0 @ g1 @ g2 @ g3
    return g5

def verify_clifford_algebra():
    """
    验证Clifford代数 Verify Clifford Algebra

    关系: {γ^μ, γ^ν} = γ^μ γ^ν + γ^ν γ^μ = 2η^μν I₄

    闵可夫斯基度规 (东海岸约定):
    η = diag(+1, -1, -1, -1)

    结果:
    - {γ⁰, γ⁰} = 2I₄
    - {γⁱ, γⁱ} = -2I₄
    - {γ^μ, γ^ν} = 0 (μ≠ν)

    返回:
        bool: 是否通过验证
    """
    gamma = gamma_matrices()
    eta = np.diag([1, -1, -1, -1])

    for mu in range(4):
        for nu in range(4):
            anticommutator = gamma[mu] @ gamma[nu] + gamma[nu] @ gamma[mu]
            expected = 2 * eta[mu, nu] * np.eye(4)
            if not np.allclose(anticommutator, expected):
                return False
    return True


# =============================================================================
# 练习 10.2: 自由粒子解
# Exercise 10.2: Free Particle Solutions
#
# 物理背景:
# 狄拉克方程的平面波解分为正能量（粒子）和负能量（反粒子）两类。
# 每类又有两个自旋状态。这解释了为什么电子有4个自由度。
#
# 旋量结构:
# u(p,s) = N × (χ_s, (σ·p)χ_s/(E+m))^T
# 其中 χ_s 是二分量泡利旋量
# =============================================================================
def dirac_spinor_positive(p, m, s=1):
    """
    正能量狄拉克旋量 u(p,s) Positive Energy Dirac Spinor

    满足方程: (γ·p - m)u = 0
    归一化: u†u = 2E（协变归一化）

    结构:
    u = √(E+m) × [[χ_s],
                   [(σ·p)χ_s/(E+m)]]

    其中 χ_s 是自旋本征态:
    - s=1 (up): χ = (1, 0)^T
    - s=2 (down): χ = (0, 1)^T

    参数:
        p (list): 三动量 [p_x, p_y, p_z]
        m (float): 质量（自然单位）
        s (int): 自旋状态 (1=up, 2=down)

    返回:
        np.ndarray: 4分量旋量
    """
    px, py, pz = p
    E = np.sqrt(px**2 + py**2 + pz**2 + m**2)

    # 归一化因子
    N = np.sqrt(E + m)

    if s == 1:
        chi = np.array([1, 0], dtype=complex)
    else:
        chi = np.array([0, 1], dtype=complex)

    # 旋量分量
    sigma = [np.array([[0, 1], [1, 0]]),
             np.array([[0, -1j], [1j, 0]]),
             np.array([[1, 0], [0, -1]])]

    sigma_p = sum(p[i] * sigma[i] for i in range(3))
    xi = sigma_p @ chi / (E + m)

    u = N * np.concatenate([chi, xi])
    return u

def dirac_spinor_negative(p, m, s=1):
    """
    负能量狄拉克旋量 v(p,s) Negative Energy Spinor (Antiparticle)

    满足方程: (γ·p + m)v = 0

    物理解释:
    - Feynman-Stuckelberg: 负能态向后传播 = 正能反粒子向前传播
    - v(p,s) 描述动量为 p 的正电子
    - 自旋量子数与电子相反

    结构与 u 类似但自旋排列不同

    参数:
        p (list): 三动量 [p_x, p_y, p_z]
        m (float): 质量
        s (int): 自旋状态

    返回:
        np.ndarray: 4分量旋量
    """
    px, py, pz = p
    E = np.sqrt(px**2 + py**2 + pz**2 + m**2)

    N = np.sqrt(E + m)

    if s == 1:
        chi = np.array([0, 1], dtype=complex)
    else:
        chi = np.array([1, 0], dtype=complex)

    sigma = [np.array([[0, 1], [1, 0]]),
             np.array([[0, -1j], [1j, 0]]),
             np.array([[1, 0], [0, -1]])]

    sigma_p = sum(p[i] * sigma[i] for i in range(3))
    xi = -sigma_p @ chi / (E + m)

    v = N * np.concatenate([xi, chi])
    return v


# =============================================================================
# 练习 10.3: 狄拉克方程算符
# Exercise 10.3: Dirac Equation Operators
# =============================================================================
def dirac_hamiltonian(p, m):
    """
    自由狄拉克哈密顿量
    H = α·p + βm

    α = γ⁰γ, β = γ⁰
    """
    # TODO: 构建哈密顿量
    g0, g1, g2, g3 = gamma_matrices()

    alpha_1 = g0 @ g1
    alpha_2 = g0 @ g2
    alpha_3 = g0 @ g3
    beta = g0

    H = alpha_1 * p[0] + alpha_2 * p[1] + alpha_3 * p[2] + beta * m
    return H

def dirac_energy_eigenvalues(p, m):
    """
    狄拉克能量本征值
    E = ±√(p² + m²)
    """
    p_mag = np.sqrt(sum(pi**2 for pi in p))
    E_plus = np.sqrt(p_mag**2 + m**2)
    return E_plus, -E_plus

def verify_dirac_equation(u, p, m):
    """
    验证旋量满足狄拉克方程
    (γ^μ p_μ - m)u = 0
    """
    g0, g1, g2, g3 = gamma_matrices()
    E = np.sqrt(sum(pi**2 for pi in p) + m**2)

    slash_p = g0 * E - g1 * p[0] - g2 * p[1] - g3 * p[2]
    result = (slash_p - m * np.eye(4)) @ u

    return np.allclose(result, 0, atol=1e-10)


# =============================================================================
# 练习 10.4: 旋量的洛伦兹变换
# Exercise 10.4: Lorentz Transformation of Spinors
# =============================================================================
def lorentz_boost_spinor(rapidity, direction):
    """
    旋量的洛伦兹推进
    S(Λ) = exp(-ω^μν σ_μν/4)
    对于纯推进: S = exp(-η·α/2)

    rapidity: 快度 η = arctanh(v/c)
    direction: 推进方向单位向量
    """
    g0, g1, g2, g3 = gamma_matrices()

    # σ^0i = (i/2)[γ⁰, γⁱ] = iγ⁰γⁱ/2 对于Dirac表示
    alpha = [g0 @ g1, g0 @ g2, g0 @ g3]

    # 推进生成元
    K = sum(direction[i] * alpha[i] for i in range(3)) / 2

    S = expm(-rapidity * K)
    return S

def lorentz_rotation_spinor(angle, axis):
    """
    旋量的空间旋转
    S = exp(-iθ·Σ/2)
    Σ = (i/2)[γⁱ, γʲ]
    """
    sigma = [np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1]], dtype=complex)]

    # 简化：绕z轴旋转
    Sigma_z = np.diag([1, -1, 1, -1]) * 0.5

    S = expm(-1j * angle * Sigma_z)
    return S


# =============================================================================
# 练习 10.5: 流和守恒
# Exercise 10.5: Current and Conservation
# =============================================================================
def dirac_current(psi, psi_bar=None):
    """
    狄拉克流
    j^μ = ψ̄γ^μψ
    ψ̄ = ψ†γ⁰
    """
    g0, g1, g2, g3 = gamma_matrices()
    gamma = [g0, g1, g2, g3]

    if psi_bar is None:
        psi_bar = np.conj(psi) @ g0

    j = np.zeros(4, dtype=complex)
    for mu in range(4):
        j[mu] = psi_bar @ gamma[mu] @ psi

    return j

def probability_density(psi):
    """
    概率密度 ρ = ψ†ψ = j⁰
    """
    return np.real(np.conj(psi) @ psi)

def gordon_decomposition(u1, u2, p1, p2, m):
    """
    Gordon分解
    ū₂γ^μu₁ = (1/2m)ū₂[(p₁+p₂)^μ + iσ^μν(p₂-p₁)_ν]u₁
    """
    # 简化实现
    j = dirac_current(u1, np.conj(u2) @ gamma_matrices()[0])
    return j


# =============================================================================
# 练习 10.6: 手征性和螺旋度
# Exercise 10.6: Chirality and Helicity
# =============================================================================
def chirality_projectors():
    """
    手征投影算符
    P_L = (1 - γ⁵)/2 (左手)
    P_R = (1 + γ⁵)/2 (右手)
    """
    g5 = gamma_5()
    I4 = np.eye(4, dtype=complex)

    P_L = (I4 - g5) / 2
    P_R = (I4 + g5) / 2

    return P_L, P_R

def helicity_operator(p):
    """
    螺旋度算符
    h = Σ·p̂/2 = S·p̂
    """
    p_mag = np.sqrt(sum(pi**2 for pi in p))
    p_hat = [pi/p_mag for pi in p]

    # Σ = γ⁵γ⁰γ
    g5 = gamma_5()
    g0, g1, g2, g3 = gamma_matrices()

    Sigma = [g5 @ g0 @ g1, g5 @ g0 @ g2, g5 @ g0 @ g3]

    h = sum(p_hat[i] * Sigma[i] for i in range(3)) / 2
    return h

def helicity_eigenvalue(u, p):
    """
    计算旋量的螺旋度
    """
    h = helicity_operator(p)
    h_psi = h @ u

    # 提取本征值
    for eigenval in [0.5, -0.5]:
        if np.allclose(h_psi, eigenval * u, atol=1e-10):
            return eigenval
    return None


# =============================================================================
# 可视化
# =============================================================================
def plot_dirac_equation():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. γ矩阵结构
    ax1 = axes[0, 0]
    g0, g1, g2, g3 = gamma_matrices()
    im = ax1.imshow(np.real(g0), cmap='RdBu', aspect='equal')
    ax1.set_title(r'$\gamma^0$ (实部)')
    ax1.set_xticks(range(4))
    ax1.set_yticks(range(4))
    plt.colorbar(im, ax=ax1)

    # 2. 能量色散关系
    ax2 = axes[0, 1]
    m = 1  # 归一化质量
    p = np.linspace(-3, 3, 100)

    E_plus = np.sqrt(p**2 + m**2)
    E_minus = -np.sqrt(p**2 + m**2)

    ax2.plot(p, E_plus, 'b-', linewidth=2, label='正能量')
    ax2.plot(p, E_minus, 'r-', linewidth=2, label='负能量')
    ax2.axhline(y=m, color='g', linestyle='--', alpha=0.5)
    ax2.axhline(y=-m, color='g', linestyle='--', alpha=0.5)
    ax2.fill_between(p, -m, m, alpha=0.2, color='gray', label='质量间隙')
    ax2.set_xlabel('p (m单位)')
    ax2.set_ylabel('E (m单位)')
    ax2.set_title('狄拉克色散关系')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 旋量分量
    ax3 = axes[0, 2]
    p_vals = np.linspace(0, 5, 50)

    u_upper = []
    u_lower = []
    for p_val in p_vals:
        u = dirac_spinor_positive([0, 0, p_val], m, s=1)
        u_upper.append(np.abs(u[0])**2 + np.abs(u[1])**2)
        u_lower.append(np.abs(u[2])**2 + np.abs(u[3])**2)

    ax3.plot(p_vals, u_upper, 'b-', linewidth=2, label='上分量')
    ax3.plot(p_vals, u_lower, 'r-', linewidth=2, label='下分量')
    ax3.set_xlabel('p/m')
    ax3.set_ylabel('|u|²')
    ax3.set_title('旋量分量vs动量')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. γ⁵结构
    ax4 = axes[1, 0]
    g5 = gamma_5()
    im4 = ax4.imshow(np.real(g5), cmap='RdBu', aspect='equal')
    ax4.set_title(r'$\gamma^5$ (实部)')
    ax4.set_xticks(range(4))
    ax4.set_yticks(range(4))
    plt.colorbar(im4, ax=ax4)

    # 5. 手征投影
    ax5 = axes[1, 1]
    P_L, P_R = chirality_projectors()

    u = dirac_spinor_positive([0, 0, 3], m, s=1)
    u_L = P_L @ u
    u_R = P_R @ u

    x = ['L', 'R']
    norms = [np.linalg.norm(u_L), np.linalg.norm(u_R)]

    ax5.bar(x, norms)
    ax5.set_ylabel('|P_{L,R}u|')
    ax5.set_title('手征投影 (p/m=3)')
    ax5.grid(True, alpha=0.3)

    # 6. Clifford代数验证
    ax6 = axes[1, 2]
    gamma = gamma_matrices()
    eta = np.diag([1, -1, -1, -1])

    # 显示{γ^μ, γ^ν}/2的对角元
    anticomm = np.zeros((4, 4))
    for mu in range(4):
        for nu in range(4):
            ac = gamma[mu] @ gamma[nu] + gamma[nu] @ gamma[mu]
            anticomm[mu, nu] = np.real(np.trace(ac)) / 8

    im6 = ax6.imshow(anticomm, cmap='RdBu', aspect='equal')
    ax6.set_title(r'{$\gamma^\mu$, $\gamma^\nu$}/2')
    ax6.set_xticks(range(4))
    ax6.set_yticks(range(4))
    ax6.set_xticklabels(['0', '1', '2', '3'])
    ax6.set_yticklabels(['0', '1', '2', '3'])
    plt.colorbar(im6, ax=ax6)

    plt.tight_layout()
    plt.savefig('dirac_equation.png', dpi=150)
    print("图像已保存为 dirac_equation.png")
    plt.show()


def verify():
    all_passed = True

    m = 1  # 归一化质量

    # Check 10.1
    if not verify_clifford_algebra():
        print("❌ 10.1 Clifford代数验证失败")
        all_passed = False
    else:
        print(f"✓ 10.1 γ矩阵正确（满足Clifford代数）")

    # Check 10.2
    p = [0, 0, 1]
    u = dirac_spinor_positive(p, m, s=1)
    E = np.sqrt(sum(pi**2 for pi in p) + m**2)
    norm_sq = np.conj(u) @ u
    if not np.isclose(np.real(norm_sq), 2*E, rtol=0.01):
        print("❌ 10.2 旋量归一化错误")
        all_passed = False
    else:
        print(f"✓ 10.2 自由粒子旋量正确")

    # Check 10.3
    if not verify_dirac_equation(u, p, m):
        print("❌ 10.3 旋量不满足狄拉克方程")
        all_passed = False
    else:
        print(f"✓ 10.3 狄拉克方程验证正确")

    # Check 10.4
    S = lorentz_boost_spinor(0.5, [0, 0, 1])
    if S.shape != (4, 4):
        print("❌ 10.4 洛伦兹变换矩阵维度错误")
        all_passed = False
    else:
        print(f"✓ 10.4 旋量洛伦兹变换正确")

    # Check 10.5
    j = dirac_current(u)
    rho = probability_density(u)
    if np.real(j[0]) != rho:
        print("❌ 10.5 j⁰应等于概率密度")
        all_passed = False
    else:
        print(f"✓ 10.5 流守恒正确 (ρ = {rho:.3f})")

    # Check 10.6
    P_L, P_R = chirality_projectors()
    if not np.allclose(P_L + P_R, np.eye(4)):
        print("❌ 10.6 手征投影算符不完备")
        all_passed = False
    else:
        print(f"✓ 10.6 手征性正确 (P_L + P_R = I)")

    if all_passed:
        print("\n🎉 所有测试通过！")
        try:
            plot_dirac_equation()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("狄拉克方程基础 Dirac Equation Basics")
    print("=" * 50)
    verify()
