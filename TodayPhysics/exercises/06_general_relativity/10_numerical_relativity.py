"""
数值相对论基础 Numerical Relativity Basics
难度 Difficulty: ★★★★★

学习目标 Learning Objectives:
- 理解ADM 3+1分解：将4维时空分解为3维空间的时间演化
- 掌握约束方程（Hamiltonian和动量约束）及其物理意义
- 了解BSSN格式及其稳定性优势
- 学习黑洞初始数据的构造方法
- 理解引力波波形提取的基本原理
- 认识数值稳定性（CFL条件）和收敛性测试

物理背景 Physical Background:
数值相对论是求解爱因斯坦场方程的数值方法。2005年突破后，它成为
研究双黑洞并合、双中子星并合等强引力现象的核心工具，为引力波
天文学提供了理论波形模板。

3+1分解（ADM分解）ADM 3+1 Decomposition:
将4维时空度规分解为：
  - 塌陷函数 (lapse) α：时间流逝速率
  - 位移矢量 (shift) β^i：空间坐标如何随时间移动
  - 3维度规 γ_ij：空间几何
  - 外曲率 K_ij：空间如何嵌入时空

约束方程 Constraint Equations:
爱因斯坦方程的一部分不涉及时间导数，而是空间切片上必须满足的约束：
  - Hamiltonian约束: R + K² - K_ij K^ij = 16πρ
  - 动量约束: D_j K^j_i - D_i K = 8π S_i

关键公式 Key Formulas:
  - ADM度规: ds² = -α²dt² + γ_ij(dx^i + β^i dt)(dx^j + β^j dt)
  - 外曲率: K_ij = -(1/2α)(∂_t γ_ij - D_i β_j - D_j β_i)
  - BSSN共形因子: φ = (1/12)ln(det(γ))
  - CFL条件: Δt ≤ CFL × Δx/c

数值方法 Numerical Methods:
  - 有限差分法（时间演化）
  - 谱方法（椭圆方程求解）
  - 自适应网格细化（AMR）
  - 切除技术（处理奇点）
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import G, c

# I AM NOT DONE

# =============================================================================
# 练习 10.1: 3+1分解
# Exercise 10.1: 3+1 Decomposition
# =============================================================================
def adm_metric_component(alpha, beta, gamma_ij, i, j, t_component=False):
    """
    ADM度规分量
    g_00 = -α² + β^k β_k
    g_0i = β_i
    g_ij = γ_ij
    """
    if t_component:
        if i == 0 and j == 0:
            beta_sq = np.sum(beta**2)
            return -alpha**2 + beta_sq
        elif i == 0 or j == 0:
            idx = j if i == 0 else i
            return beta[idx - 1]
    return gamma_ij[i, j]

def lapse_function_harmonic(alpha_prev, dt, K):
    """
    谐波切片条件
    ∂_t α = -α² K
    """
    return alpha_prev - alpha_prev**2 * K * dt

def shift_vector_gamma_driver(beta_prev, B_prev, dt, eta=1):
    """
    Gamma-driver移动条件（简化）
    ∂_t β^i = (3/4) B^i
    ∂_t B^i = ∂_t Γ^i - η B^i
    """
    return beta_prev + 0.75 * B_prev * dt

def extrinsic_curvature_from_embedding(gamma_ij, d_gamma_dt, alpha, beta):
    """
    外曲率定义
    K_ij = -(1/2α)(∂_t γ_ij - L_β γ_ij)
    简化：假设 β = 0
    """
    return -d_gamma_dt / (2 * alpha)


# =============================================================================
# 练习 10.2: 约束方程
# Exercise 10.2: Constraint Equations
# =============================================================================
def hamiltonian_constraint(R_3, K, K_ij, rho=0):
    """
    Hamiltonian约束
    H = R^(3) + K² - K_ij K^ij - 16πρ = 0
    """
    K_sq = np.sum(K_ij**2)
    return R_3 + K**2 - K_sq - 16 * np.pi * rho

def momentum_constraint(D_j_K, D_i_K_ij, S_i=0):
    """
    动量约束
    M_i = D_j K^j_i - D_i K - 8π S_i = 0
    """
    return D_j_K - D_i_K_ij - 8 * np.pi * S_i

def constraint_violation(H, M):
    """
    约束违反度量
    """
    return np.sqrt(H**2 + np.sum(M**2))

def conformal_flatness_initial_data(psi, rho, K=0):
    """
    共形平坦初始数据
    γ_ij = ψ⁴ δ_ij
    需要求解 ∇²ψ = -2πρψ⁵ (Lichnerowicz方程)
    """
    # 简化：真空、时刻对称
    return psi**4 * np.eye(3)


# =============================================================================
# 练习 10.3: BSSN格式
# Exercise 10.3: BSSN Formalism
# =============================================================================
def conformal_metric(gamma_ij):
    """
    共形度规
    γ̃_ij = e^(-4φ) γ_ij
    φ = (1/12) ln(det(γ))
    """
    det_gamma = np.linalg.det(gamma_ij)
    phi = np.log(det_gamma) / 12
    return np.exp(-4 * phi) * gamma_ij, phi

def conformal_connection_functions(gamma_tilde_ij, d_gamma_tilde):
    """
    共形联络函数
    Γ̃^i = γ̃^jk Γ̃^i_jk = -∂_j γ̃^ij
    """
    # 简化：假设平坦背景
    return -np.sum(d_gamma_tilde, axis=1)

def traceless_extrinsic_curvature(K_ij, K, gamma_ij):
    """
    无迹外曲率
    Ã_ij = K_ij - (1/3)γ_ij K
    """
    return K_ij - gamma_ij * K / 3

def bssn_evolution_phi(phi, alpha, K, dt):
    """
    BSSN演化：共形因子
    ∂_t φ = -(1/6) α K + β^i ∂_i φ
    简化：β = 0
    """
    return phi - (1/6) * alpha * K * dt


# =============================================================================
# 练习 10.4: 黑洞初始数据
# Exercise 10.4: Black Hole Initial Data
# =============================================================================
def schwarzschild_isotropic_conformal(r, M):
    """
    史瓦西黑洞等距坐标共形因子
    ψ = 1 + M/(2r)
    """
    return 1 + M / (2 * r)

def brill_lindquist_conformal(r1, r2, M1, M2, r):
    """
    Brill-Lindquist双黑洞初始数据
    ψ = 1 + M₁/(2|r-r₁|) + M₂/(2|r-r₂|)
    """
    d1 = np.linalg.norm(r - r1)
    d2 = np.linalg.norm(r - r2)
    return 1 + M1 / (2 * d1) + M2 / (2 * d2)

def bowen_york_momentum(P, S, r):
    """
    Bowen-York外曲率（简化）
    给予黑洞线动量P和自旋S
    """
    r_mag = np.linalg.norm(r)
    n = r / r_mag
    # 简化形式
    K_P = 3 / (2 * r_mag**2) * (np.outer(P, n) + np.outer(n, P) - np.eye(3) * np.dot(P, n))
    return K_P

def apparent_horizon_finder_spherical(psi, r_range, threshold=0.1):
    """
    球对称视在视界查找器（简化）
    θ = 0（expansion vanishes）
    """
    for r in r_range:
        # 简化：当 ψ(r) 满足某条件时
        if psi(r) > 2:  # 粗略近似
            return r
    return None


# =============================================================================
# 练习 10.5: 引力波提取
# Exercise 10.5: Gravitational Wave Extraction
# =============================================================================
def weyl_scalar_psi4(h_plus, h_cross, dt):
    """
    Weyl标量 ψ₄
    ψ₄ = ∂²h/∂t² = ∂²(h₊ - ih×)/∂t²
    """
    # 数值二阶导数
    d2h_plus = np.gradient(np.gradient(h_plus, dt), dt)
    d2h_cross = np.gradient(np.gradient(h_cross, dt), dt)
    return d2h_plus - 1j * d2h_cross

def strain_from_psi4(psi4, t, f_low=10):
    """
    从ψ₄恢复应变
    h = ∫∫ ψ₄ dt²（需要滤波）
    """
    dt = t[1] - t[0]
    # 两次积分
    psi4_int = np.cumsum(psi4) * dt
    h = np.cumsum(psi4_int) * dt
    return h

def spin_weighted_spherical_harmonic_22(theta, phi):
    """
    自旋权重球谐函数 ₋₂Y₂₂
    ₋₂Y₂₂ = √(5/64π) (1+cosθ)² e^(2iφ)
    """
    return np.sqrt(5 / (64 * np.pi)) * (1 + np.cos(theta))**2 * np.exp(2j * phi)

def multipole_decomposition(data_theta_phi, l, m, theta, phi, weights):
    """
    多极分解
    h_lm = ∫ h(θ,φ) Ȳ_lm(θ,φ) sinθ dθ dφ
    """
    Y_lm = spin_weighted_spherical_harmonic_22(theta, phi)
    return np.sum(data_theta_phi * np.conj(Y_lm) * weights)


# =============================================================================
# 练习 10.6: 稳定性与收敛
# Exercise 10.6: Stability and Convergence
# =============================================================================
def courant_condition(dx, dt, c_char=1):
    """
    CFL条件
    Δt ≤ CFL × Δx/c
    """
    return dt <= dx / c_char

def richardson_extrapolation(f_h, f_2h, f_4h, order=2):
    """
    Richardson外推
    f_exact ≈ f_h + (f_h - f_2h)/(2^p - 1)
    """
    return f_h + (f_h - f_2h) / (2**order - 1)

def convergence_factor(e_h, e_2h, expected_order=2):
    """
    收敛因子
    Q = e_2h / e_h = 2^p
    """
    if np.abs(e_h) < 1e-15:
        return np.inf
    return e_2h / e_h

def kreiss_oliger_dissipation(u, epsilon=0.1, order=4):
    """
    Kreiss-Oliger数值耗散
    用于抑制高频噪声
    """
    # 四阶耗散算子（简化：一维）
    dissipation = np.zeros_like(u)
    for i in range(2, len(u) - 2):
        dissipation[i] = epsilon * (u[i-2] - 4*u[i-1] + 6*u[i] - 4*u[i+1] + u[i+2])
    return u - dissipation


# =============================================================================
# 可视化
# =============================================================================
def plot_numerical_relativity():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 共形因子（单黑洞）
    ax1 = axes[0, 0]
    M = 1
    r = np.linspace(0.5 * M, 10 * M, 100)

    psi = [schwarzschild_isotropic_conformal(ri, M) for ri in r]

    ax1.plot(r/M, psi, 'b-', linewidth=2)
    ax1.axvline(x=0.5, color='r', linestyle='--', label='喉部 r=M/2')
    ax1.set_xlabel('r/M')
    ax1.set_ylabel('ψ')
    ax1.set_title('史瓦西共形因子')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. Brill-Lindquist双黑洞
    ax2 = axes[0, 1]
    M1, M2 = 0.5, 0.5
    d = 4  # 初始分离

    x = np.linspace(-6, 6, 100)
    y = np.linspace(-6, 6, 100)
    X, Y = np.meshgrid(x, y)

    r1 = np.array([-d/2, 0, 0])
    r2 = np.array([d/2, 0, 0])

    psi_grid = np.zeros_like(X)
    for i in range(len(x)):
        for j in range(len(y)):
            r_point = np.array([X[i,j], Y[i,j], 0])
            psi_grid[i,j] = brill_lindquist_conformal(r1, r2, M1, M2, r_point)

    im = ax2.contourf(X, Y, psi_grid, levels=20, cmap='viridis')
    ax2.plot(-d/2, 0, 'ro', markersize=10, label='BH1')
    ax2.plot(d/2, 0, 'ro', markersize=10, label='BH2')
    ax2.set_xlabel('x/M')
    ax2.set_ylabel('y/M')
    ax2.set_title('双黑洞共形因子')
    plt.colorbar(im, ax=ax2)

    # 3. 引力波波形（模拟）
    ax3 = axes[0, 2]
    t = np.linspace(0, 100, 1000)
    # 模拟旋近-并合-铃振波形
    omega_0 = 0.05
    tau = 10

    # 旋近
    h_inspiral = 0.1 * np.exp(t/50) * np.sin(omega_0 * t * (1 + t/100))
    # 铃振
    h_ringdown = 0.5 * np.exp(-(t - 50)**2 / (2*tau**2)) * np.sin(0.2 * (t - 50))

    h = np.where(t < 50, h_inspiral, h_ringdown)

    ax3.plot(t, h, 'b-', linewidth=1)
    ax3.axvline(x=50, color='r', linestyle='--', alpha=0.5, label='并合')
    ax3.set_xlabel('t/M')
    ax3.set_ylabel('h')
    ax3.set_title('引力波波形（示意）')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 切片条件
    ax4 = axes[1, 0]
    K_range = np.linspace(-1, 1, 100)
    alpha_0 = 1
    dt = 0.1

    alpha_harmonic = [lapse_function_harmonic(alpha_0, dt, K) for K in K_range]

    ax4.plot(K_range, alpha_harmonic, 'b-', linewidth=2)
    ax4.axhline(y=1, color='r', linestyle='--', alpha=0.5, label='α=1')
    ax4.set_xlabel('K')
    ax4.set_ylabel('α(t+dt)')
    ax4.set_title('谐波切片条件')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 收敛性测试
    ax5 = axes[1, 1]
    h_values = np.array([0.1, 0.05, 0.025, 0.0125])
    # 模拟误差（假设二阶收敛）
    errors = 0.01 * h_values**2

    ax5.loglog(h_values, errors, 'bo-', linewidth=2, markersize=8, label='数值误差')
    ax5.loglog(h_values, 0.01 * h_values**2, 'r--', linewidth=1, label='二阶收敛')
    ax5.set_xlabel('网格间距 h')
    ax5.set_ylabel('误差')
    ax5.set_title('收敛性测试')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. 约束违反
    ax6 = axes[1, 2]
    t = np.linspace(0, 100, 1000)
    # 模拟约束违反演化
    H_violation = 1e-10 * np.exp(0.01 * t)  # 指数增长（不稳定）
    H_stable = 1e-10 * np.ones_like(t)  # 稳定

    ax6.semilogy(t, H_violation, 'r-', linewidth=2, label='不稳定')
    ax6.semilogy(t, H_stable, 'b-', linewidth=2, label='稳定')
    ax6.set_xlabel('t/M')
    ax6.set_ylabel('||H||')
    ax6.set_title('Hamiltonian约束违反')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('numerical_relativity.png', dpi=150)
    print("图像已保存为 numerical_relativity.png")
    plt.show()


def verify():
    """
    验证所有练习的正确性
    Verify all exercises for correctness
    """
    all_passed = True

    # 检查 10.1 - 3+1分解 ADM decomposition
    alpha, beta = 1, np.array([0, 0, 0])  # 闵可夫斯基时空的规范选择
    gamma = np.eye(3)  # 平坦空间度规
    g_00 = adm_metric_component(alpha, beta, gamma, 0, 0, t_component=True)
    if not np.isclose(g_00, -1, rtol=0.01):
        print("错误 10.1: 对于闵可夫斯基时空（alpha=1, beta=0），g_00应为-1")
        all_passed = False
    else:
        print("正确 10.1: 3+1分解")

    # 检查 10.2 - 约束方程 Constraint equations
    H = hamiltonian_constraint(0, 0, np.zeros((3, 3)), 0)
    if H != 0:
        print("错误 10.2: 平坦空间的Hamiltonian约束应恒为0")
        all_passed = False
    else:
        print("正确 10.2: 约束方程")

    # 检查 10.3 - BSSN格式 BSSN formalism
    gamma = np.eye(3)  # 单位度规
    gamma_tilde, phi = conformal_metric(gamma)
    if phi != 0:
        print("错误 10.3: 对于单位度规，共形因子 phi 应为0 (det(gamma)=1)")
        all_passed = False
    else:
        print("正确 10.3: BSSN格式")

    # 检查 10.4 - 黑洞初始数据 Black hole initial data
    psi = schwarzschild_isotropic_conformal(1, 1)  # r = M 时
    if not np.isclose(psi, 1.5, rtol=0.01):
        print("错误 10.4: 等距坐标下 r=M 时共形因子 psi = 1 + M/(2r) = 1.5")
        all_passed = False
    else:
        print(f"正确 10.4: 黑洞初始数据 (psi(M) = {psi:.2f})")

    # 检查 10.5 - 引力波提取 Gravitational wave extraction
    theta, phi = np.pi/4, 0
    Y = spin_weighted_spherical_harmonic_22(theta, phi)
    if np.abs(Y) == 0:
        print("错误 10.5: 自旋权重球谐函数在 theta=pi/4 处不应为零")
        all_passed = False
    else:
        print("正确 10.5: 引力波提取")

    # 检查 10.6 - 稳定性条件 Stability conditions
    if not courant_condition(0.1, 0.05, 1):  # dx=0.1, dt=0.05, c=1
        print("错误 10.6: CFL条件 dt <= dx/c 应满足 (0.05 <= 0.1)")
        all_passed = False
    else:
        print("正确 10.6: 稳定性条件 (CFL)")

    if all_passed:
        print("\n所有测试通过！")
        try:
            plot_numerical_relativity()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("数值相对论基础 Numerical Relativity Basics")
    print("=" * 50)
    verify()
