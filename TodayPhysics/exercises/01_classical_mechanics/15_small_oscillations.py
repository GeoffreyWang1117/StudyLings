"""
小振动与简正模 Small Oscillations and Normal Modes
难度 Difficulty: ★★★★

================================================================================
学习目标 Learning Objectives
================================================================================
- 理解小振动近似和线性化方法
  Understand small oscillation approximation and linearization methods
- 掌握简正模分析和本征值问题
  Master normal mode analysis and eigenvalue problems
- 计算耦合振子系统的本征频率和简正模
  Calculate eigenfrequencies and normal modes of coupled oscillator systems
- 应用于分子振动和晶格动力学
  Apply to molecular vibrations and lattice dynamics

================================================================================
物理背景 Physical Background
================================================================================
小振动理论研究系统在平衡点附近的微小扰动，将非线性问题线性化。

1. 小振动近似 Small Oscillation Approximation:
   - 在稳定平衡点附近，势能可以展开为二次型
   - V ≈ V₀ + (1/2)Σ V_ij q_i q_j（忽略高阶项）
   - 动能也是广义速度的二次型: T = (1/2)Σ T_ij q̇_i q̇_j

2. 本征值问题 Eigenvalue Problem:
   运动方程: T·q̈ + V·q = 0
   假设解 q = a·exp(iωt)，得到:
   (V - ω²T)·a = 0
   本征方程: det(V - ω²T) = 0

3. 简正模 Normal Modes:
   - 每个本征值ω²对应一个简正模
   - 简正模是系统的"固有振动模式"
   - 任意运动可以分解为简正模的叠加
   - N自由度系统有N个简正模

4. 简正坐标 Normal Coordinates:
   - 通过适当的线性变换解耦运动方程
   - 每个简正坐标独立做简谐振动
   - Q̈_i + ω_i²Q_i = 0

5. 晶格振动 Lattice Vibrations:
   - 声学支: ω(k=0) = 0（整体平移模式）
   - 光学支: ω(k=0) ≠ 0（相对运动模式）
   - 色散关系: ω = ω(k)

6. 应用 Applications:
   - 分子振动光谱（红外和拉曼）
   - 固体的热容（德拜模型）
   - 结构工程中的振动分析

HINT: 拉格朗日量在平衡点展开: L = (1/2)T_ij q̇_i q̇_j - (1/2)V_ij q_i q_j
HINT: 本征方程: det(V - ω²T) = 0
HINT: 简正模将耦合振动分解为独立的简谐振动
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import g

# I AM NOT DONE

# =============================================================================
# 练习 15.1: 二自由度耦合振子
# Exercise 15.1: Two Coupled Oscillators
# =============================================================================
# 两个通过弹簧耦合的振子是简正模分析的典型例子
# 系统有两个简正模：同相模式和反相模式

def coupled_oscillator_frequencies(m1, m2, k1, k2, k_c):
    """
    计算两个耦合振子的本征频率 Eigenfrequencies of Coupled Oscillators

    系统配置:
    墙-[k1]-m1-[k_c]-m2-[k2]-墙

    求解广义本征值问题:
    V·a = ω²·T·a
    其中T是质量矩阵，V是刚度矩阵

    对于等质量等弹簧的特殊情况:
    - 低频模: 同相振动（两质点同方向）
    - 高频模: 反相振动（两质点反方向）

    参数 Parameters:
        m1, m2: 两个振子的质量 [kg]
        k1, k2: 连接墙壁的弹簧常数 [N/m]
        k_c: 耦合弹簧常数 [N/m]
    返回 Returns:
        (omega1, omega2): 两个本征频率（从小到大）[rad/s]
    """
    # TODO: 构建质量矩阵T和势能矩阵V
    T = np.array([[m1, 0], [0, m2]])
    V = np.array([[k1 + k_c, -k_c], [-k_c, k2 + k_c]])

    # 求解广义本征值问题: V·a = ω²·T·a
    eigenvalues, eigenvectors = eigh(V, T)
    omega = np.sqrt(eigenvalues)

    return omega[0], omega[1]

def coupled_oscillator_modes(m1, m2, k1, k2, k_c):
    """
    计算两个耦合振子的简正模 Normal Modes

    简正模（本征矢量）描述了振动模式的形态
    第一列对应低频模，第二列对应高频模

    返回 Returns:
        本征矢量矩阵（各列为简正模）
    """
    T = np.array([[m1, 0], [0, m2]])
    V = np.array([[k1 + k_c, -k_c], [-k_c, k2 + k_c]])

    eigenvalues, eigenvectors = eigh(V, T)
    return eigenvectors


# =============================================================================
# 练习 15.2: 三原子分子振动
# Exercise 15.2: Triatomic Molecule Vibrations
# =============================================================================
def triatomic_linear_frequencies(m1, m2, m3, k12, k23):
    """
    线性三原子分子的振动频率
    例如: CO2 (O=C=O)

    返回: 两个振动模式的频率（排除平移模式）
    """
    # TODO: 3x3矩阵问题
    T = np.diag([m1, m2, m3])
    V = np.array([
        [k12, -k12, 0],
        [-k12, k12 + k23, -k23],
        [0, -k23, k23]
    ])

    eigenvalues, eigenvectors = eigh(V, T)
    # 第一个本征值应接近0（平移模式）
    omega = np.sqrt(np.maximum(eigenvalues, 0))
    return omega[1], omega[2]  # 非零频率

def triatomic_modes_description():
    """
    描述三原子分子的振动模式
    """
    modes = {
        "symmetric_stretch": "对称伸缩: 两端原子同相振动",
        "asymmetric_stretch": "反对称伸缩: 两端原子反相振动",
        "bending": "弯曲模式: 垂直于分子轴"
    }
    return modes


# =============================================================================
# 练习 15.3: 双摆小振动
# Exercise 15.3: Small Oscillations of Double Pendulum
# =============================================================================
def double_pendulum_frequencies(m1, m2, L1, L2, g_val=g):
    """
    双摆小振动的本征频率
    m1, m2: 质量
    L1, L2: 摆长
    """
    # TODO: 构建小振动矩阵
    # 质量矩阵（动能）
    T = np.array([
        [(m1 + m2) * L1**2, m2 * L1 * L2],
        [m2 * L1 * L2, m2 * L2**2]
    ])

    # 势能矩阵
    V = np.array([
        [(m1 + m2) * g_val * L1, 0],
        [0, m2 * g_val * L2]
    ])

    eigenvalues, _ = eigh(V, T)
    omega = np.sqrt(eigenvalues)
    return omega[0], omega[1]

def double_pendulum_modes(m1, m2, L1, L2, g_val=g):
    """
    双摆小振动的简正模
    """
    T = np.array([
        [(m1 + m2) * L1**2, m2 * L1 * L2],
        [m2 * L1 * L2, m2 * L2**2]
    ])

    V = np.array([
        [(m1 + m2) * g_val * L1, 0],
        [0, m2 * g_val * L2]
    ])

    _, eigenvectors = eigh(V, T)
    return eigenvectors


# =============================================================================
# 练习 15.4: 晶格振动（一维单原子链）
# Exercise 15.4: Lattice Vibrations (1D Monatomic Chain)
# =============================================================================
# 一维单原子链是固体物理中声子理论的起点
# 它展示了色散关系的基本概念

def monatomic_chain_dispersion(k, m, K, a):
    """
    一维单原子链的色散关系 Dispersion Relation

    ω(k) = 2√(K/m)|sin(ka/2)|

    特点:
    - k=0: ω=0（整体平移模式，声学支）
    - k=±π/a: ω_max = 2√(K/m)（布里渊区边界）
    - 周期性: ω(k) = ω(k + 2π/a)

    第一布里渊区: -π/a ≤ k ≤ π/a

    参数 Parameters:
        k: 波矢 [1/m]
        m: 原子质量 [kg]
        K: 弹簧常数 [N/m]
        a: 晶格常数 [m]
    返回 Returns:
        角频率 ω [rad/s]
    """
    # TODO: 计算色散关系
    omega = 2 * np.sqrt(K / m) * np.abs(np.sin(k * a / 2))
    return omega

def group_velocity_chain(k, m, K, a):
    """
    群速度 Group Velocity
    v_g = dω/dk

    物理意义: 波包（能量）传播的速度
    - k=0附近: v_g ≈ a√(K/m)（声速）
    - 布里渊区边界: v_g = 0（驻波）
    """
    omega_max = 2 * np.sqrt(K / m)
    v_g = omega_max * (a / 2) * np.cos(k * a / 2) * np.sign(np.sin(k * a / 2))
    return v_g


# =============================================================================
# 练习 15.5: 晶格振动（一维双原子链）
# Exercise 15.5: Lattice Vibrations (1D Diatomic Chain)
# =============================================================================
# 双原子链出现声学支和光学支两种模式
# 这是理解离子晶体振动和红外吸收的基础

def diatomic_chain_dispersion(k, m1, m2, K, a):
    """
    一维双原子链的色散关系 Diatomic Chain Dispersion

    两条色散曲线:
    1. 声学支 (acoustic branch): ω → 0 当 k → 0
       - 两种原子同相振动
       - 类似于连续介质中的声波

    2. 光学支 (optical branch): ω ≠ 0 当 k = 0
       - 两种原子反相振动
       - 可以与红外光耦合（离子晶体）

    参数 Parameters:
        k: 波矢 [1/m]
        m1, m2: 两种原子的质量 [kg]
        K: 弹簧常数 [N/m]
        a: 晶格常数（包含两个原子）[m]
    返回 Returns:
        (omega_acoustic, omega_optical): 声学支和光学支的频率 [rad/s]
    """
    # TODO: 计算两支色散关系
    mu = m1 * m2 / (m1 + m2)  # 约化质量
    M = m1 + m2

    term1 = K / mu
    term2 = K * np.sqrt(1/m1**2 + 1/m2**2 + 2*np.cos(k*a)/(m1*m2))

    omega_minus = np.sqrt(term1 - K * np.sqrt((1/m1 + 1/m2)**2 - 4*np.sin(k*a/2)**2/(m1*m2)))
    omega_plus = np.sqrt(term1 + K * np.sqrt((1/m1 + 1/m2)**2 - 4*np.sin(k*a/2)**2/(m1*m2)))

    return omega_minus, omega_plus

def optical_gap(m1, m2, K):
    """
    光学支和声学支之间的能隙 Optical-Acoustic Gap

    在布里渊区边界(k = π/a)，两支之间存在频率间隙
    间隙的存在意味着某些频率的振动无法在晶体中传播

    对于红外吸收：
    - 频率在光学支范围内的光可以被吸收
    - 频率在间隙内的光可以透过
    """
    omega_opt_min = np.sqrt(2 * K / max(m1, m2))
    omega_ac_max = np.sqrt(2 * K / min(m1, m2))
    return omega_opt_min - omega_ac_max


# =============================================================================
# 练习 15.6: N耦合振子链
# Exercise 15.6: N Coupled Oscillators Chain
# =============================================================================
def n_oscillator_chain_matrix(N, m, k, boundary='fixed'):
    """
    构建N个耦合振子的矩阵
    boundary: 'fixed'(固定端) 或 'periodic'(周期性)

    返回: 质量矩阵T和势能矩阵V
    """
    T = m * np.eye(N)
    V = np.zeros((N, N))

    # 对角元
    for i in range(N):
        if boundary == 'fixed':
            if i == 0 or i == N-1:
                V[i, i] = 2 * k
            else:
                V[i, i] = 2 * k
        else:  # periodic
            V[i, i] = 2 * k

    # 非对角元
    for i in range(N-1):
        V[i, i+1] = -k
        V[i+1, i] = -k

    if boundary == 'periodic':
        V[0, N-1] = -k
        V[N-1, 0] = -k

    return T, V

def n_oscillator_frequencies(N, m, k, boundary='fixed'):
    """
    计算N个耦合振子的所有本征频率
    """
    T, V = n_oscillator_chain_matrix(N, m, k, boundary)
    eigenvalues, _ = eigh(V, T)
    omega = np.sqrt(np.maximum(eigenvalues, 0))
    return np.sort(omega)


# =============================================================================
# 可视化
# =============================================================================
def plot_small_oscillations():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 耦合振子频率vs耦合强度
    ax1 = axes[0, 0]
    k_c_vals = np.linspace(0, 2, 100)
    m, k = 1, 1

    omega1_list = []
    omega2_list = []
    for k_c in k_c_vals:
        w1, w2 = coupled_oscillator_frequencies(m, m, k, k, k_c)
        omega1_list.append(w1)
        omega2_list.append(w2)

    ax1.plot(k_c_vals, omega1_list, 'b-', linewidth=2, label='ω₁ (同相)')
    ax1.plot(k_c_vals, omega2_list, 'r-', linewidth=2, label='ω₂ (反相)')
    ax1.set_xlabel('耦合常数 k_c')
    ax1.set_ylabel('本征频率 ω')
    ax1.set_title('耦合振子本征频率')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 双摆频率vs质量比
    ax2 = axes[0, 1]
    m_ratio = np.linspace(0.1, 5, 100)
    L = 1

    omega1_dp = []
    omega2_dp = []
    for mr in m_ratio:
        w1, w2 = double_pendulum_frequencies(1, mr, L, L)
        omega1_dp.append(w1)
        omega2_dp.append(w2)

    ax2.plot(m_ratio, omega1_dp, 'b-', linewidth=2, label='ω₁')
    ax2.plot(m_ratio, omega2_dp, 'r-', linewidth=2, label='ω₂')
    ax2.set_xlabel('m₂/m₁')
    ax2.set_ylabel('本征频率 ω (rad/s)')
    ax2.set_title('双摆本征频率')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 单原子链色散关系
    ax3 = axes[0, 2]
    k_wave = np.linspace(-np.pi, np.pi, 200)
    m, K, a = 1, 1, 1

    omega_mono = monatomic_chain_dispersion(k_wave, m, K, a)
    ax3.plot(k_wave, omega_mono, 'b-', linewidth=2)
    ax3.set_xlabel('ka')
    ax3.set_ylabel('ω')
    ax3.set_title('单原子链色散关系')
    ax3.set_xlim(-np.pi, np.pi)
    ax3.grid(True, alpha=0.3)

    # 4. 双原子链色散关系
    ax4 = axes[1, 0]
    m1, m2 = 1, 2

    omega_ac = []
    omega_opt = []
    for kv in k_wave:
        w_ac, w_opt = diatomic_chain_dispersion(kv, m1, m2, K, a)
        omega_ac.append(w_ac)
        omega_opt.append(w_opt)

    ax4.plot(k_wave, omega_ac, 'b-', linewidth=2, label='声学支')
    ax4.plot(k_wave, omega_opt, 'r-', linewidth=2, label='光学支')
    ax4.set_xlabel('ka')
    ax4.set_ylabel('ω')
    ax4.set_title('双原子链色散关系')
    ax4.legend()
    ax4.set_xlim(-np.pi, np.pi)
    ax4.grid(True, alpha=0.3)

    # 5. N振子频率谱
    ax5 = axes[1, 1]
    N_vals = [5, 10, 20]

    for N in N_vals:
        freqs = n_oscillator_frequencies(N, 1, 1, 'fixed')
        ax5.plot(range(1, N+1), freqs, 'o-', label=f'N={N}', markersize=4)

    ax5.set_xlabel('模式序号')
    ax5.set_ylabel('本征频率 ω')
    ax5.set_title('N振子链频率谱')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. 简正模形态
    ax6 = axes[1, 2]
    N = 10
    T, V = n_oscillator_chain_matrix(N, 1, 1, 'fixed')
    _, modes = eigh(V, T)

    x = np.arange(1, N+1)
    for i in [0, 4, 9]:
        ax6.plot(x, modes[:, i], 'o-', label=f'模式 {i+1}', linewidth=1.5, markersize=4)

    ax6.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    ax6.set_xlabel('振子序号')
    ax6.set_ylabel('振幅')
    ax6.set_title('简正模形态 (N=10)')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('small_oscillations.png', dpi=150)
    print("图像已保存为 small_oscillations.png")
    plt.show()


def verify():
    all_passed = True

    # Check 15.1
    m, k = 1, 1
    w1, w2 = coupled_oscillator_frequencies(m, m, k, k, 0)
    if not np.isclose(w1, w2, rtol=0.01):
        print("❌ 15.1 无耦合时两频率应相等")
        all_passed = False
    else:
        print(f"✓ 15.1 耦合振子正确 (k_c=0: ω₁=ω₂={w1:.3f})")

    # Check 15.2
    m = 1
    w1, w2 = triatomic_linear_frequencies(m, m, m, k, k)
    if w1 <= 0 or w2 <= 0:
        print("❌ 15.2 三原子分子频率应为正")
        all_passed = False
    else:
        print(f"✓ 15.2 三原子分子正确 (ω₁={w1:.3f}, ω₂={w2:.3f})")

    # Check 15.3
    L = 1
    w1, w2 = double_pendulum_frequencies(m, m, L, L)
    omega_single = np.sqrt(g / L)
    if w1 > 2 * omega_single or w2 > 2 * omega_single:
        print("❌ 15.3 双摆频率不合理")
        all_passed = False
    else:
        print(f"✓ 15.3 双摆小振动正确 (ω₁={w1:.3f}, ω₂={w2:.3f})")

    # Check 15.4
    omega_max = monatomic_chain_dispersion(np.pi, m, k, 1)
    expected_max = 2 * np.sqrt(k / m)
    if not np.isclose(omega_max, expected_max, rtol=0.01):
        print("❌ 15.4 单原子链色散关系错误")
        all_passed = False
    else:
        print(f"✓ 15.4 单原子链正确 (ω_max={omega_max:.3f})")

    # Check 15.5
    w_ac, w_opt = diatomic_chain_dispersion(0, 1, 2, k, 1)
    if w_ac != 0:
        print("❌ 15.5 声学支k=0时ω应为0")
        all_passed = False
    else:
        print(f"✓ 15.5 双原子链正确 (声学支k=0: ω=0)")

    # Check 15.6
    N = 10
    freqs = n_oscillator_frequencies(N, m, k)
    if len(freqs) != N:
        print("❌ 15.6 N振子链应有N个本征频率")
        all_passed = False
    else:
        print(f"✓ 15.6 N振子链正确 ({N}个本征频率)")

    if all_passed:
        print("\n🎉 所有测试通过！")
        try:
            plot_small_oscillations()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("小振动与简正模 Small Oscillations and Normal Modes")
    print("=" * 50)
    verify()
