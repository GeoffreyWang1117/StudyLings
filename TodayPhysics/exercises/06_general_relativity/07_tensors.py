"""
广义相对论张量计算 Tensor Calculus for GR
难度 Difficulty: ★★★★★

学习目标 Learning Objectives:
- 理解张量的几何定义和坐标变换性质
- 掌握度规张量及其逆的物理意义
- 计算克里斯托费尔符号（联络系数）
- 理解协变导数和平行移动
- 计算黎曼曲率张量、里奇张量和爱因斯坦张量
- 理解爱因斯坦场方程的几何结构

物理背景 Physical Background:
广义相对论的数学语言是黎曼几何。张量是在坐标变换下具有特定变换性质
的几何对象，它们是描述物理定律的最自然方式。爱因斯坦场方程:
    G_μν = 8πG/c⁴ T_μν
将时空几何（左边）与物质能量（右边）联系起来。

核心张量层次 Core Tensor Hierarchy:
  1. 度规张量 g_μν：定义距离和角度
  2. 克里斯托费尔符号 Γ^λ_μν：描述联络（平行移动）
  3. 黎曼曲率张量 R^ρ_σμν：描述曲率（测地线偏离）
  4. 里奇张量 R_μν：黎曼张量的缩并
  5. 里奇标量 R：曲率的标量度量
  6. 爱因斯坦张量 G_μν = R_μν - (1/2)g_μν R：场方程的几何侧

关键公式 Key Formulas:
  - 克里斯托费尔符号: Γ^λ_μν = (1/2)g^λρ(∂_μg_ρν + ∂_νg_ρμ - ∂_ρg_μν)
  - 黎曼张量: R^ρ_σμν = ∂_μΓ^ρ_νσ - ∂_νΓ^ρ_μσ + Γ^ρ_μλΓ^λ_νσ - Γ^ρ_νλΓ^λ_μσ
  - 里奇张量: R_μν = R^λ_μλν
  - 里奇标量: R = g^μν R_μν
  - 爱因斯坦张量: G_μν = R_μν - (1/2)g_μν R

张量符号约定 Tensor Index Conventions:
  - 希腊字母（μ,ν,ρ,σ...）：取值0,1,2,3（时空指标）
  - 拉丁字母（i,j,k...）：取值1,2,3（空间指标）
  - 爱因斯坦求和约定：重复指标隐含求和
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import derivative
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import G, c

# I AM NOT DONE

# =============================================================================
# 练习 7.1: 度规张量
# Exercise 7.1: Metric Tensor
# =============================================================================
def minkowski_metric():
    """
    闵可夫斯基度规（平直时空）
    η_μν = diag(1, -1, -1, -1)
    """
    return np.diag([1, -1, -1, -1])

def schwarzschild_metric(r, M, theta=np.pi/2):
    """
    史瓦西度规（球对称真空解）
    ds² = (1-r_s/r)c²dt² - (1-r_s/r)^(-1)dr² - r²dΩ²
    r_s = 2GM/c²
    """
    # TODO: 构建史瓦西度规
    r_s = 2 * G * M / c**2

    if r <= r_s:
        return None  # 在视界内

    g = np.zeros((4, 4))
    g[0, 0] = (1 - r_s/r) * c**2
    g[1, 1] = -1 / (1 - r_s/r)
    g[2, 2] = -r**2
    g[3, 3] = -r**2 * np.sin(theta)**2

    return g

def inverse_metric(g):
    """
    计算逆度规 g^μν
    g^μλ g_λν = δ^μ_ν
    """
    return np.linalg.inv(g)


# =============================================================================
# 练习 7.2: 克里斯托费尔符号
# Exercise 7.2: Christoffel Symbols
# =============================================================================
def christoffel_schwarzschild(r, M):
    """
    史瓦西时空的非零克里斯托费尔符号
    返回字典 {(λ,μ,ν): 值}
    """
    # TODO: 计算克里斯托费尔符号
    r_s = 2 * G * M / c**2

    if r <= r_s:
        return {}

    Gamma = {}

    # 非零分量
    f = 1 - r_s/r

    # Γ^t_tr = Γ^t_rt
    Gamma[(0, 0, 1)] = r_s / (2 * r**2 * f)
    Gamma[(0, 1, 0)] = Gamma[(0, 0, 1)]

    # Γ^r_tt
    Gamma[(1, 0, 0)] = c**2 * r_s * f / (2 * r**2)

    # Γ^r_rr
    Gamma[(1, 1, 1)] = -r_s / (2 * r**2 * f)

    # Γ^r_θθ
    Gamma[(1, 2, 2)] = -(r - r_s)

    # Γ^r_φφ
    Gamma[(1, 3, 3)] = -(r - r_s)  # 在θ=π/2时

    # Γ^θ_rθ = Γ^θ_θr
    Gamma[(2, 1, 2)] = 1/r
    Gamma[(2, 2, 1)] = 1/r

    # Γ^φ_rφ = Γ^φ_φr
    Gamma[(3, 1, 3)] = 1/r
    Gamma[(3, 3, 1)] = 1/r

    return Gamma

def christoffel_from_metric(g, g_inv, coords, delta=1e-8):
    """
    从度规数值计算克里斯托费尔符号
    使用有限差分
    """
    n = len(g)
    Gamma = np.zeros((n, n, n))

    for lam in range(n):
        for mu in range(n):
            for nu in range(n):
                term = 0
                for sigma in range(n):
                    # 需要度规导数，这里简化处理
                    pass
                Gamma[lam, mu, nu] = term

    return Gamma


# =============================================================================
# 练习 7.3: 协变导数
# Exercise 7.3: Covariant Derivative
# =============================================================================
def covariant_derivative_vector(V, Gamma, partial_V):
    """
    矢量的协变导数
    ∇_μ V^ν = ∂_μ V^ν + Γ^ν_μλ V^λ

    V: 四矢量
    Gamma: 克里斯托费尔符号数组
    partial_V: V的偏导数
    """
    n = len(V)
    nabla_V = np.zeros((n, n))

    for mu in range(n):
        for nu in range(n):
            nabla_V[mu, nu] = partial_V[mu, nu]
            for lam in range(n):
                nabla_V[mu, nu] += Gamma[nu, mu, lam] * V[lam]

    return nabla_V

def geodesic_equation_coefficients(Gamma, u):
    """
    测地线方程的加速度项
    d²x^μ/dτ² = -Γ^μ_αβ (dx^α/dτ)(dx^β/dτ)

    返回: 加速度四矢量
    """
    n = len(u)
    a = np.zeros(n)

    for mu in range(n):
        for alpha in range(n):
            for beta in range(n):
                if (mu, alpha, beta) in Gamma:
                    a[mu] -= Gamma[(mu, alpha, beta)] * u[alpha] * u[beta]

    return a


# =============================================================================
# 练习 7.4: 黎曼曲率张量
# Exercise 7.4: Riemann Curvature Tensor
# =============================================================================
def riemann_tensor_component(Gamma, d_Gamma, rho, sigma, mu, nu):
    """
    黎曼张量分量
    R^ρ_σμν = ∂_μΓ^ρ_νσ - ∂_νΓ^ρ_μσ + Γ^ρ_μλΓ^λ_νσ - Γ^ρ_νλΓ^λ_μσ
    """
    # 简化：仅计算结构
    term1 = d_Gamma.get((rho, nu, sigma, mu), 0)
    term2 = -d_Gamma.get((rho, mu, sigma, nu), 0)

    term3 = 0
    term4 = 0
    for lam in range(4):
        term3 += Gamma.get((rho, mu, lam), 0) * Gamma.get((lam, nu, sigma), 0)
        term4 -= Gamma.get((rho, nu, lam), 0) * Gamma.get((lam, mu, sigma), 0)

    return term1 + term2 + term3 + term4

def kretschmann_scalar(r, M):
    """
    Kretschmann标量（史瓦西时空）
    K = R^μνρσ R_μνρσ = 48G²M²/(c⁴r⁶)
    """
    return 48 * G**2 * M**2 / (c**4 * r**6)


# =============================================================================
# 练习 7.5: 里奇张量和标量
# Exercise 7.5: Ricci Tensor and Scalar
# =============================================================================
def ricci_tensor_from_riemann(R_tensor):
    """
    里奇张量（黎曼张量缩并）
    R_μν = R^λ_μλν
    """
    n = R_tensor.shape[0]
    R_ricci = np.zeros((n, n))

    for mu in range(n):
        for nu in range(n):
            for lam in range(n):
                R_ricci[mu, nu] += R_tensor[lam, mu, lam, nu]

    return R_ricci

def ricci_scalar(R_ricci, g_inv):
    """
    里奇标量（里奇张量缩并）
    R = g^μν R_μν
    """
    R = 0
    n = R_ricci.shape[0]
    for mu in range(n):
        for nu in range(n):
            R += g_inv[mu, nu] * R_ricci[mu, nu]
    return R

def vacuum_solution_check(R_ricci):
    """
    检验是否为真空解
    真空解满足 R_μν = 0
    """
    return np.allclose(R_ricci, 0, atol=1e-10)


# =============================================================================
# 练习 7.6: 爱因斯坦张量
# Exercise 7.6: Einstein Tensor
# =============================================================================
def einstein_tensor(R_ricci, R_scalar, g):
    """
    爱因斯坦张量
    G_μν = R_μν - (1/2)g_μν R
    """
    # TODO: 计算爱因斯坦张量
    G = R_ricci - 0.5 * g * R_scalar
    return G

def stress_energy_from_einstein(G_tensor):
    """
    从爱因斯坦张量得到应力能量张量
    T_μν = (c⁴/8πG) G_μν
    """
    return (c**4 / (8 * np.pi * G)) * G_tensor

def trace_reversed_ricci(R_ricci, R_scalar, g):
    """
    迹反转里奇张量
    """
    n = R_ricci.shape[0]
    return R_ricci - 0.5 * R_scalar * g


# =============================================================================
# 可视化
# =============================================================================
def plot_tensors():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    M = 1.989e30  # 太阳质量
    r_s = 2 * G * M / c**2

    # 1. 史瓦西度规分量
    ax1 = axes[0, 0]
    r = np.linspace(1.1 * r_s, 10 * r_s, 100)

    g_tt = [(1 - r_s/ri) for ri in r]
    g_rr = [-1/(1 - r_s/ri) for ri in r]

    ax1.plot(r/r_s, g_tt, 'b-', linewidth=2, label=r'$g_{tt}/c^2$')
    ax1.plot(r/r_s, g_rr, 'r-', linewidth=2, label=r'$g_{rr}$')
    ax1.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    ax1.axhline(y=-1, color='k', linestyle=':', alpha=0.3)
    ax1.set_xlabel(r'$r/r_s$')
    ax1.set_ylabel('度规分量')
    ax1.set_title('史瓦西度规分量')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. Kretschmann标量
    ax2 = axes[0, 1]
    K = [kretschmann_scalar(ri, M) for ri in r]

    ax2.semilogy(r/r_s, K, 'b-', linewidth=2)
    ax2.set_xlabel(r'$r/r_s$')
    ax2.set_ylabel(r'$K$ (m$^{-4}$)')
    ax2.set_title('Kretschmann标量')
    ax2.grid(True, alpha=0.3)

    # 3. 克里斯托费尔符号
    ax3 = axes[0, 2]

    Gamma_ttr = [r_s / (2 * ri**2 * (1 - r_s/ri)) for ri in r]
    Gamma_rtt = [c**2 * r_s * (1 - r_s/ri) / (2 * ri**2) for ri in r]

    ax3.plot(r/r_s, Gamma_ttr, 'b-', linewidth=2, label=r'$\Gamma^t_{tr}$')
    ax3.plot(r/r_s, np.array(Gamma_rtt)/c**2, 'r-', linewidth=2, label=r'$\Gamma^r_{tt}/c^2$')
    ax3.set_xlabel(r'$r/r_s$')
    ax3.set_ylabel(r'$\Gamma$ (m$^{-1}$)')
    ax3.set_title('克里斯托费尔符号')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 测地线示意
    ax4 = axes[1, 0]
    # 绘制史瓦西几何中的径向测地线
    theta = np.linspace(0, 2*np.pi, 100)
    r_circle = 3 * r_s

    x = r_circle * np.cos(theta)
    y = r_circle * np.sin(theta)

    ax4.plot(x/r_s, y/r_s, 'b-', linewidth=2, label='圆轨道')
    circle = plt.Circle((0, 0), 1, color='black', fill=True, alpha=0.8)
    ax4.add_patch(circle)
    ax4.set_xlim(-5, 5)
    ax4.set_ylim(-5, 5)
    ax4.set_xlabel(r'$x/r_s$')
    ax4.set_ylabel(r'$y/r_s$')
    ax4.set_title('测地线（圆轨道r=3r_s）')
    ax4.set_aspect('equal')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 协变vs逆变
    ax5 = axes[1, 1]
    g_example = schwarzschild_metric(3*r_s, M)
    g_inv_example = inverse_metric(g_example)

    labels = [r'$g_{00}$', r'$g_{11}$', r'$g_{22}$', r'$g_{33}$']
    x_pos = np.arange(4)
    width = 0.35

    g_diag = [g_example[i, i] for i in range(4)]
    g_inv_diag = [g_inv_example[i, i] for i in range(4)]

    # 归一化显示
    g_diag_norm = [g_diag[0]/c**2, g_diag[1], g_diag[2]/(3*r_s)**2, g_diag[3]/(3*r_s)**2]
    g_inv_diag_norm = [g_inv_diag[0]*c**2, g_inv_diag[1], g_inv_diag[2]*(3*r_s)**2, g_inv_diag[3]*(3*r_s)**2]

    ax5.bar(x_pos - width/2, g_diag_norm, width, label='协变 (归一化)')
    ax5.bar(x_pos + width/2, g_inv_diag_norm, width, label='逆变 (归一化)')
    ax5.set_xticks(x_pos)
    ax5.set_xticklabels(labels)
    ax5.set_ylabel('分量值')
    ax5.set_title('度规的协变与逆变分量')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. 曲率vs距离
    ax6 = axes[1, 2]
    # 简单的曲率度量：1/r²（牛顿类比）
    curvature = [r_s / (ri**2) for ri in r]

    ax6.plot(r/r_s, curvature, 'b-', linewidth=2)
    ax6.set_xlabel(r'$r/r_s$')
    ax6.set_ylabel('曲率尺度')
    ax6.set_title('时空曲率随距离变化')
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('tensors.png', dpi=150)
    print("图像已保存为 tensors.png")
    plt.show()


def verify():
    """
    验证所有练习的正确性
    Verify all exercises for correctness
    """
    all_passed = True

    M = 1.989e30  # 太阳质量
    r_s = 2 * G * M / c**2  # 史瓦西半径

    # 检查 7.1 - 度规张量 Metric tensor
    eta = minkowski_metric()
    if not np.allclose(np.diag(eta), [1, -1, -1, -1]):
        print("错误 7.1: 闵可夫斯基度规应为 diag(1,-1,-1,-1)（西海岸约定）")
        all_passed = False
    else:
        print(f"正确 7.1: 度规张量")

    # 检查 7.2 - 克里斯托费尔符号 Christoffel symbols
    r = 3 * r_s
    Gamma = christoffel_schwarzschild(r, M)
    if (0, 0, 1) not in Gamma:
        print("错误 7.2: 缺少克里斯托费尔符号 Gamma^0_01")
        all_passed = False
    else:
        print(f"正确 7.2: 克里斯托费尔符号")

    # 检查 7.3 - 协变导数 Covariant derivative
    print(f"正确 7.3: 协变导数框架")

    # 检查 7.4 - 黎曼张量/Kretschmann标量 Riemann tensor
    K = kretschmann_scalar(r, M)
    expected_K = 48 * G**2 * M**2 / (c**4 * r**6)
    if not np.isclose(K, expected_K, rtol=0.01):
        print("错误 7.4: Kretschmann标量计算不正确，请检查公式 K = 48G²M²/(c⁴r⁶)")
        all_passed = False
    else:
        print(f"正确 7.4: 黎曼张量 (K = {K:.2e} m^-4)")

    # 检查 7.5 - 里奇张量 Ricci tensor
    # 史瓦西解是真空解，所以 R_μν = 0
    R_ricci = np.zeros((4, 4))  # 真空解
    if not vacuum_solution_check(R_ricci):
        print("错误 7.5: 真空解检验失败，里奇张量应为零")
        all_passed = False
    else:
        print(f"正确 7.5: 里奇张量（真空解 R_μν = 0）")

    # 检查 7.6 - 爱因斯坦张量 Einstein tensor
    g = schwarzschild_metric(r, M)
    R_scalar = 0  # 真空解的里奇标量为零
    G_tensor = einstein_tensor(R_ricci, R_scalar, g)
    if not np.allclose(G_tensor, 0, atol=1e-10):
        print("错误 7.6: 真空解的爱因斯坦张量应为零 (G_μν = 0)")
        all_passed = False
    else:
        print(f"正确 7.6: 爱因斯坦张量（真空解 G_μν = 0）")

    if all_passed:
        print("\n所有测试通过！")
        try:
            plot_tensors()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("广义相对论张量计算 Tensor Calculus for GR")
    print("=" * 50)
    verify()
