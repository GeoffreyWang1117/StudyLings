"""
拓扑量子态 Topological Quantum Phases
难度 Difficulty: ★★★★★

================================================================================
学习目标 Learning Objectives
================================================================================
- 理解贝里相位的几何起源和物理意义
  Understand geometric origin and physical meaning of Berry phase
- 掌握贝里曲率和拓扑不变量（陈数、Z₂不变量）的计算
  Master Berry curvature and topological invariants (Chern number, Z₂)
- 分析拓扑绝缘体、量子霍尔效应和SSH模型
  Analyze topological insulators, quantum Hall effect, and SSH model

================================================================================
物理背景 Physical Background
================================================================================
拓扑物态是凝聚态物理的前沿领域。拓扑性质由全局几何特征决定，
不受局部微扰影响，使得拓扑材料具有稳健的边缘态和量子化输运。

Topological phases are frontier of condensed matter physics. Topological
properties are determined by global geometry, robust against local perturbations.

核心概念 Key Concepts:
1. 贝里相位 Berry Phase: γ = i∮⟨n|∇_R|n⟩·dR
   - 量子态绝热演化一圈后获得的几何相位
   - 等于参数空间包围立体角的一半 γ = -Ω/2

2. 贝里曲率 Berry Curvature: F = ∇ × A (A为贝里联络)
   - 动量空间的"磁场"，决定反常速度
   - 在韦尔点附近表现为磁单极子

3. 拓扑不变量 Topological Invariants:
   - 陈数 Chern Number: C = (1/2π)∫_BZ F d²k (整数)
   - Z₂不变量: 时间反演不变系统的拓扑分类
   - 缠绕数 Winding Number: 一维系统的拓扑指标

4. 体边对应 Bulk-Boundary Correspondence:
   - 体拓扑不变量 = 边缘态数目
   - 拓扑保护的边缘态不受杂质散射

重要系统 Important Systems:
- 整数量子霍尔效应: σ_xy = νe²/h (ν为整数)
- 拓扑绝缘体: 体绝缘、表面导电的狄拉克锥
- SSH模型: 一维拓扑绝缘体的玩具模型

HINT: 贝里相位: γ = i∮⟨n|∇_R|n⟩·dR，几何相位的量子版本
HINT: 陈数: C = (1/2π)∫_BZ F d²k，拓扑不变量必为整数
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import hbar, e, h

# I AM NOT DONE

# 磁通量子
Phi_0 = h / e

# =============================================================================
# 练习 13.1: 贝里相位
# Exercise 13.1: Berry Phase
#
# 物理背景 Physical Background:
# 当量子系统的哈密顿量缓慢变化一周后，波函数除动力学相位外还获得
# 几何相位（贝里相位），它只依赖于参数空间的路径，不依赖于速度。
#
# 对于二能级系统 H = B·σ（B为参数空间的"磁场"）：
# - 贝里相位 γ = -(1/2)∮(1-cosθ)dφ = -Ω/2
# - Ω是参数空间路径包围的立体角
#
# 物理实例 Physical Examples:
# - 磁场中的自旋进动（磁贝里相位）
# - Aharonov-Bohm效应（电磁贝里相位）
# - 分子中的几何相位
# =============================================================================
def berry_phase_two_level(theta_path, phi_path):
    """
    计算二能级系统的贝里相位 Calculate Berry phase for two-level system

    公式 Formula: γ = -(1/2)∮(1-cosθ)dφ

    参数 Parameters:
        theta_path: 极角路径 θ(t) 数组
        phi_path: 方位角路径 φ(t) 数组

    返回 Returns:
        gamma: 贝里相位（弧度）

    物理意义: 等于参数空间路径包围立体角的负一半
    """
    # 数值积分
    gamma = 0
    for i in range(len(phi_path) - 1):
        d_phi = phi_path[i+1] - phi_path[i]
        theta_avg = (theta_path[i] + theta_path[i+1]) / 2
        gamma -= 0.5 * (1 - np.cos(theta_avg)) * d_phi
    return gamma

def berry_phase_solid_angle(Omega):
    """
    贝里相位等于参数空间包围的立体角的一半
    γ = -Ω/2
    """
    return -Omega / 2

def aharonov_bohm_phase(Phi):
    """
    Aharonov-Bohm相位
    φ_AB = 2πΦ/Φ₀
    """
    return 2 * np.pi * Phi / Phi_0


# =============================================================================
# 练习 13.2: 贝里曲率
# Exercise 13.2: Berry Curvature
# =============================================================================
def berry_curvature_two_band(kx, ky, m, t=1):
    """
    二带模型的贝里曲率
    H = d(k)·σ, F = d·(∂_kx d × ∂_ky d) / (2|d|³)
    简化模型：d = (sin kx, sin ky, m + cos kx + cos ky)
    """
    dx = np.sin(kx)
    dy = np.sin(ky)
    dz = m + np.cos(kx) + np.cos(ky)

    # 偏导数
    ddx_dkx = np.cos(kx)
    ddx_dky = 0
    ddy_dkx = 0
    ddy_dky = np.cos(ky)
    ddz_dkx = -np.sin(kx)
    ddz_dky = -np.sin(ky)

    # 叉积
    cross_x = ddy_dkx * ddz_dky - ddy_dky * ddz_dkx
    cross_y = ddz_dkx * ddx_dky - ddz_dky * ddx_dkx
    cross_z = ddx_dkx * ddy_dky - ddx_dky * ddy_dkx

    # 点积和模
    d_mag = np.sqrt(dx**2 + dy**2 + dz**2)
    if d_mag < 1e-10:
        return 0

    F = (dx * cross_x + dy * cross_y + dz * cross_z) / (2 * d_mag**3)
    return F

def berry_curvature_monopole(kx, ky, kz, k0=0):
    """
    动量空间中的磁单极子贝里曲率
    F = k/(2|k|³) (对于韦尔点)
    """
    k = np.array([kx, ky, kz]) - k0
    k_mag = np.linalg.norm(k)
    if k_mag < 1e-10:
        return np.zeros(3)
    return k / (2 * k_mag**3)


# =============================================================================
# 练习 13.3: 陈数
# Exercise 13.3: Chern Number
# =============================================================================
def chern_number_numerical(berry_curvature_func, N=50):
    """
    数值计算陈数
    C = (1/2π)∫∫_BZ F(k) d²k
    """
    kx = np.linspace(-np.pi, np.pi, N)
    ky = np.linspace(-np.pi, np.pi, N)
    dk = (2 * np.pi / N)**2

    C = 0
    for i in range(N):
        for j in range(N):
            F = berry_curvature_func(kx[i], ky[j])
            C += F * dk

    return C / (2 * np.pi)

def chern_number_two_band(m):
    """
    二带模型的陈数
    C = sign(m)/2 × (|sign(m+2) - sign(m-2)|)
    m < -2: C = 0
    -2 < m < 0: C = 1
    0 < m < 2: C = -1
    m > 2: C = 0
    """
    if m < -2 or m > 2:
        return 0
    elif m < 0:
        return 1
    else:
        return -1

def z2_invariant(time_reversal_pairs):
    """
    Z₂拓扑不变量（简化）
    ν = Π δᵢ mod 2
    δᵢ: 时间反演不变点的奇偶性
    """
    product = 1
    for delta in time_reversal_pairs:
        product *= delta
    return (1 - product) // 2


# =============================================================================
# 练习 13.4: 量子霍尔效应
# Exercise 13.4: Quantum Hall Effect
#
# 物理背景 Physical Background:
# 1980年von Klitzing发现整数量子霍尔效应（诺贝尔奖1985）。
# 二维电子气在强磁场下，霍尔电导量子化为 σ_xy = νe²/h。
#
# 物理机制:
# 1. 朗道能级: E_n = ℏω_c(n + 1/2), ω_c = eB/m
# 2. 朗道能级简并度: g = eBA/h（与面积成正比）
# 3. 填充因子 ν = n_e/g = n_e h/(eB)
#
# 拓扑解释:
# - 霍尔电导 σ_xy = Ce²/h, C是陈数（整数）
# - 手征边缘态携带无耗散电流
# - 体边对应: |C| = 边缘态数目
#
# 典型数值 Typical Values:
# - 磁长度: l_B = √(ℏ/eB) ≈ 26nm @ B=1T
# - 朗道能级间距: ℏω_c ≈ 1.2meV @ B=1T
# =============================================================================
def hall_conductivity_quantized(nu):
    """
    计算量子化霍尔电导 Calculate quantized Hall conductivity

    公式 Formula: σ_xy = ν × e²/h

    参数 Parameters:
        nu: 填充因子（整数量子霍尔为整数，分数量子霍尔为分数如1/3）

    返回 Returns:
        σ_xy: 霍尔电导 [S]

    物理意义: 电导量子 e²/h ≈ 3.87×10⁻⁵ S，精度可达10⁻⁹
    """
    return nu * e**2 / h

def landau_level_energy(n, B, m=9.109e-31):
    """
    朗道能级
    E_n = ℏω_c(n + 1/2)
    ω_c = eB/m
    """
    omega_c = e * B / m
    return hbar * omega_c * (n + 0.5)

def magnetic_length(B):
    """
    磁长度
    l_B = √(ℏ/eB)
    """
    return np.sqrt(hbar / (e * B))

def degeneracy_per_landau_level(B, A):
    """
    朗道能级简并度
    g = BA/Φ₀ = eBA/h
    """
    return e * B * A / h


# =============================================================================
# 练习 13.5: 拓扑边缘态
# Exercise 13.5: Topological Edge States
# =============================================================================
def edge_state_dispersion_qhe(k, v_edge):
    """
    量子霍尔边缘态色散（手征）
    E(k) = ℏv_edge × k
    """
    return hbar * v_edge * k

def edge_conductance_quantized(n_edges):
    """
    边缘电导
    G = n × e²/h
    n: 手征边缘模式数
    """
    return n_edges * e**2 / h

def bulk_boundary_correspondence(chern_number):
    """
    体边对应：陈数等于手征边缘态数目
    |C| = |n_left - n_right|
    """
    return np.abs(chern_number)

def topological_surface_state_dirac(kx, ky, v_F=1e6):
    """
    拓扑绝缘体表面态（狄拉克锥）
    E = ±ℏv_F|k|
    """
    k = np.sqrt(kx**2 + ky**2)
    return hbar * v_F * k


# =============================================================================
# 练习 13.6: SSH模型
# Exercise 13.6: Su-Schrieffer-Heeger Model
#
# 物理背景 Physical Background:
# SSH模型是一维拓扑绝缘体的最简模型，原用于描述聚乙炔中的孤子。
# 它展示了拓扑物理的核心概念：拓扑相变、体边对应、零能边缘态。
#
# 模型设置:
# - 一维链，每个原胞两个原子(A,B)
# - v: 胞内跃迁（A-B）
# - w: 胞间跃迁（B-A of next cell）
#
# 拓扑相变:
# - |v| > |w|: 平庸相，缠绕数 W = 0
# - |v| < |w|: 拓扑相，缠绕数 W = 1
# - |v| = |w|: 相变点，能隙关闭
#
# 边缘态:
# - 拓扑相(W=1)有零能边缘态
# - 边缘态局域在链的两端
# - 受拓扑保护，对微扰稳定
# =============================================================================
def ssh_hamiltonian(k, v, w):
    """
    构造SSH模型哈密顿量 Construct SSH model Hamiltonian

    公式 Formula: H(k) = (v + w cos k)σ_x + w sin k σ_y

    参数 Parameters:
        k: 波矢（布里渊区 [-π, π]）
        v: 胞内跃迁强度
        w: 胞间跃迁强度

    返回 Returns:
        H: 2×2复矩阵

    物理意义: 动量空间中的有效哈密顿量，d(k)在d_x-d_y平面的轨迹决定缠绕数
    """
    h_x = v + w * np.cos(k)
    h_y = w * np.sin(k)
    return np.array([[0, h_x - 1j*h_y],
                     [h_x + 1j*h_y, 0]])

def ssh_band_structure(k, v, w):
    """
    SSH能带
    E = ±|v + w exp(ik)|
    """
    return np.sqrt((v + w * np.cos(k))**2 + (w * np.sin(k))**2)

def ssh_winding_number(v, w):
    """
    SSH模型缠绕数
    W = 0 if |v| > |w| (平庸)
    W = 1 if |v| < |w| (拓扑)
    """
    if np.abs(v) > np.abs(w):
        return 0
    return 1

def ssh_edge_states(v, w, N):
    """
    SSH开边界条件下的边缘态能量
    当 W = 1 时存在零能边缘态
    """
    W = ssh_winding_number(v, w)
    if W == 1:
        return [0, 0]  # 两端各一个零能态
    return []


# =============================================================================
# 可视化
# =============================================================================
def plot_topological():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 贝里曲率
    ax1 = axes[0, 0]
    N = 50
    kx = np.linspace(-np.pi, np.pi, N)
    ky = np.linspace(-np.pi, np.pi, N)
    KX, KY = np.meshgrid(kx, ky)

    m = -1  # 拓扑相
    F = np.array([[berry_curvature_two_band(kx[i], ky[j], m)
                   for j in range(N)] for i in range(N)])

    im = ax1.contourf(KX, KY, F, levels=20, cmap='RdBu_r')
    ax1.set_xlabel('k_x')
    ax1.set_ylabel('k_y')
    ax1.set_title(f'贝里曲率 (m={m})')
    plt.colorbar(im, ax=ax1)

    # 2. 陈数vs参数
    ax2 = axes[0, 1]
    m_range = np.linspace(-3, 3, 100)

    C = [chern_number_two_band(m) for m in m_range]

    ax2.plot(m_range, C, 'b-', linewidth=2)
    ax2.axvline(x=-2, color='r', linestyle='--', alpha=0.5)
    ax2.axvline(x=0, color='r', linestyle='--', alpha=0.5)
    ax2.axvline(x=2, color='r', linestyle='--', alpha=0.5)
    ax2.set_xlabel('m')
    ax2.set_ylabel('Chern number')
    ax2.set_title('拓扑相变')
    ax2.grid(True, alpha=0.3)

    # 3. 朗道能级
    ax3 = axes[0, 2]
    B = np.linspace(0.1, 10, 100)  # T

    for n in range(5):
        E = [landau_level_energy(n, b) / (1.6e-19 * 1e-3) for b in B]  # meV
        ax3.plot(B, E, label=f'n={n}', linewidth=1.5)

    ax3.set_xlabel('B (T)')
    ax3.set_ylabel('E (meV)')
    ax3.set_title('朗道能级')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 量子化霍尔电导
    ax4 = axes[1, 0]
    nu = np.arange(-5, 6)

    sigma_xy = [hall_conductivity_quantized(n) * h / e**2 for n in nu]

    ax4.step(nu, sigma_xy, 'b-', linewidth=2, where='mid')
    ax4.set_xlabel('填充因子 ν')
    ax4.set_ylabel('σ_xy (e²/h)')
    ax4.set_title('量子霍尔电导')
    ax4.grid(True, alpha=0.3)

    # 5. SSH能带
    ax5 = axes[1, 1]
    k = np.linspace(-np.pi, np.pi, 200)

    for v, w, label in [(1, 0.5, '平庸'), (0.5, 1, '拓扑')]:
        E_plus = [ssh_band_structure(ki, v, w) for ki in k]
        E_minus = [-e for e in E_plus]
        ax5.plot(k, E_plus, label=f'{label} (v={v}, w={w})', linewidth=2)
        ax5.plot(k, E_minus, linewidth=2)

    ax5.set_xlabel('k')
    ax5.set_ylabel('E')
    ax5.set_title('SSH模型能带')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. 拓扑绝缘体表面态
    ax6 = axes[1, 2]
    N = 50
    kx = np.linspace(-0.1, 0.1, N)
    ky = np.linspace(-0.1, 0.1, N)
    KX, KY = np.meshgrid(kx, ky)

    E = topological_surface_state_dirac(KX * 1e9, KY * 1e9) / (1.6e-19 * 1e-3)  # meV

    im = ax6.contourf(KX * 1e9, KY * 1e9, E, levels=20, cmap='viridis')
    ax6.set_xlabel('k_x (nm⁻¹)')
    ax6.set_ylabel('k_y (nm⁻¹)')
    ax6.set_title('拓扑表面态 (狄拉克锥)')
    plt.colorbar(im, ax=ax6, label='E (meV)')

    plt.tight_layout()
    plt.savefig('topological_phases.png', dpi=150)
    print("图像已保存为 topological_phases.png")
    plt.show()


def verify():
    all_passed = True

    # Check 13.1
    # 绕一圈的贝里相位应为立体角的一半
    theta_path = np.array([np.pi/2] * 101)
    phi_path = np.linspace(0, 2*np.pi, 101)
    gamma = berry_phase_two_level(theta_path, phi_path)
    # 对于 θ=π/2，立体角为 2π，贝里相位为 -π
    if not np.isclose(gamma, -np.pi, atol=0.1):
        print(f"❌ 13.1 贝里相位错误: {gamma:.2f}, 期望 -π")
        all_passed = False
    else:
        print(f"✓ 13.1 贝里相位正确 (γ = {gamma:.2f} ≈ -π)")

    # Check 13.2
    F = berry_curvature_two_band(0, 0, -1)
    if F == 0:
        print("❌ 13.2 贝里曲率在BZ中心不应为零（拓扑相）")
        all_passed = False
    else:
        print(f"✓ 13.2 贝里曲率正确 (F(0,0) = {F:.4f})")

    # Check 13.3
    C = chern_number_two_band(-1)
    if C != 1:
        print("❌ 13.3 m=-1时陈数应为1")
        all_passed = False
    else:
        print("✓ 13.3 陈数正确 (C = 1 when -2 < m < 0)")

    # Check 13.4
    sigma = hall_conductivity_quantized(1)
    expected = e**2 / h
    if not np.isclose(sigma, expected, rtol=0.01):
        print("❌ 13.4 量子化霍尔电导错误")
        all_passed = False
    else:
        print(f"✓ 13.4 量子霍尔效应正确 (σ_xy = e²/h)")

    # Check 13.5
    n_edge = bulk_boundary_correspondence(1)
    if n_edge != 1:
        print("❌ 13.5 体边对应错误")
        all_passed = False
    else:
        print("✓ 13.5 拓扑边缘态正确 (|C| = n_edge)")

    # Check 13.6
    W_triv = ssh_winding_number(1, 0.5)
    W_topo = ssh_winding_number(0.5, 1)
    if W_triv != 0 or W_topo != 1:
        print("❌ 13.6 SSH缠绕数错误")
        all_passed = False
    else:
        print("✓ 13.6 SSH模型正确 (W=0平庸, W=1拓扑)")

    if all_passed:
        print("\n🎉 所有测试通过！")
        try:
            plot_topological()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("拓扑量子态 Topological Quantum Phases")
    print("=" * 50)
    verify()
