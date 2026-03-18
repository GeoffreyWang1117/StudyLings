"""
量子测量 Quantum Measurement
难度 Difficulty: ★★★★★

物理背景 Physical Background:
--------------------------
量子测量是量子力学最核心也最具争议的问题之一。它涉及量子系统与经典测量设备的相互作用。

1. 测量公设 Measurement Postulate:
   - 测量可观测量A，结果必是其本征值之一
   - 概率: P(a_n) = |⟨a_n|ψ⟩|²
   - 测量后态坍缩到对应本征态 |a_n⟩

2. 密度矩阵 Density Matrix:
   纯态: ρ = |ψ⟩⟨ψ|, Tr(ρ²) = 1
   混合态: ρ = Σᵢ pᵢ|ψᵢ⟩⟨ψᵢ|, Tr(ρ²) < 1

   混合态描述:
   - 系统的经典统计混合
   - 与环境纠缠的子系统

3. 量子退相干 Quantum Decoherence:
   开放系统与环境相互作用导致量子相干性丢失。
   密度矩阵的非对角元衰减: ρ_12(t) → 0
   这解释了为何宏观物体表现为经典行为。

4. 不确定性原理 Uncertainty Principle:
   对于不对易的可观测量 [A,B] ≠ 0:
   ΔA·ΔB ≥ ½|⟨[A,B]⟩|

5. 弱测量和量子Zeno效应 Weak Measurement & Zeno Effect:
   - 弱测量: 最小扰动测量，可得超出本征值范围的弱值
   - Zeno效应: 频繁测量抑制量子演化

学习目标 Learning Objectives:
--------------------------
1. 理解测量公设及其物理含义
2. 掌握密度矩阵的性质和应用
3. 理解量子退相干机制
4. 计算不确定性乘积
5. 了解弱测量和量子Zeno效应

关键公式 Key Formulas:
---------------------
- 测量概率: P(a) = |⟨a|ψ⟩|²
- 期望值: ⟨A⟩ = ⟨ψ|A|ψ⟩ = Tr(ρA)
- 纯度: Tr(ρ²), 纯态=1, 最大混合态=1/d
- 方差: (ΔA)² = ⟨A²⟩ - ⟨A⟩²
- 退相干: ρ₁₂(t) = ρ₁₂(0)exp(-γt)

HINT: 测量概率: P(a) = |⟨a|ψ⟩|²
HINT: 密度矩阵: ρ = Σᵢ pᵢ|ψᵢ⟩⟨ψᵢ|
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import hbar

# I AM NOT DONE

# =============================================================================
# 练习 12.1: 测量公设
# Exercise 12.1: Measurement Postulate
#
# 物理背景 Physical Background:
# 量子力学的测量公设描述了测量过程:
#
# 1. 测量一个可观测量，结果只能是该算符的本征值
# 2. 得到本征值 a_n 的概率是 |⟨a_n|ψ⟩|²
# 3. 测量后，系统"坍缩"到对应的本征态
#
# 波函数坍缩是量子力学最具争议的问题之一，
# 涉及到量子-经典边界和测量问题的诠释。
# =============================================================================
def measurement_probability(psi, eigenstate):
    """
    测量概率 Measurement probability

    P = |⟨eigenstate|ψ⟩|²

    根据玻恩规则，测量得到某本征值的概率
    等于态矢在对应本征态上投影的模方。

    参数 Parameters:
        psi: 量子态 (归一化的复数向量)
        eigenstate: 本征态 (归一化的复数向量)

    返回 Returns:
        P: 概率 (0到1之间)
    """
    amplitude = np.vdot(eigenstate, psi)
    return np.abs(amplitude)**2


def collapse_state(psi, eigenstate):
    """
    测量后态坍缩到本征态 State collapse after measurement

    测量得到某本征值后，系统状态投影到对应本征态。
    这是量子力学的"投影公设"。

    参数 Parameters:
        psi: 测量前的态（未使用，保留接口）
        eigenstate: 测量结果对应的本征态

    返回 Returns:
        归一化的坍缩后态
    """
    return eigenstate / np.linalg.norm(eigenstate)


def expectation_value(psi, operator):
    """
    期望值 Expectation value

    ⟨A⟩ = ⟨ψ|A|ψ⟩

    期望值是多次测量结果的统计平均。
    对于矩阵形式: ⟨A⟩ = ψ† A ψ

    参数 Parameters:
        psi: 量子态
        operator: 可观测量对应的厄米算符（矩阵形式）

    返回 Returns:
        ⟨A⟩: 期望值（实数）
    """
    return np.real(np.vdot(psi, operator @ psi))


# =============================================================================
# 练习 12.2: 密度矩阵
# Exercise 12.2: Density Matrix
#
# 物理背景 Physical Background:
# 密度矩阵（密度算符）是描述量子态更一般的方式:
#
# 纯态: ρ = |ψ⟩⟨ψ|
#   - 完全确定的量子态
#   - Tr(ρ²) = 1
#
# 混合态: ρ = Σᵢ pᵢ|ψᵢ⟩⟨ψᵢ|
#   - 经典概率混合
#   - 或与环境纠缠后的约化态
#   - Tr(ρ²) < 1
#
# 密度矩阵的优点:
# - 统一描述纯态和混合态
# - 自然处理开放系统
# - 适合描述退相干过程
# =============================================================================
def pure_state_density_matrix(psi):
    """
    纯态密度矩阵 Pure state density matrix

    ρ = |ψ⟩⟨ψ|

    纯态的密度矩阵是秩为1的投影算符。
    对角元给出各基矢的占据概率，非对角元给出相干性。

    参数 Parameters:
        psi: 纯态波函数

    返回 Returns:
        ρ: 密度矩阵
    """
    return np.outer(psi, np.conj(psi))


def mixed_state_density_matrix(states, probabilities):
    """
    混合态密度矩阵 Mixed state density matrix

    ρ = Σᵢ pᵢ|ψᵢ⟩⟨ψᵢ|

    混合态描述我们对系统状态的经典不确定性。
    例如: 自旋处于|↑⟩态的概率为p，|↓⟩态的概率为1-p。

    参数 Parameters:
        states: 可能态的列表
        probabilities: 对应概率列表 (和为1)

    返回 Returns:
        ρ: 混合态密度矩阵
    """
    n = len(states[0])
    rho = np.zeros((n, n), dtype=complex)
    for psi, p in zip(states, probabilities):
        rho += p * np.outer(psi, np.conj(psi))
    return rho


def density_matrix_purity(rho):
    """
    纯度 Purity

    Tr(ρ²)

    纯度量化了态的"纯粹程度":
    - 纯态: Tr(ρ²) = 1
    - 最大混合态: Tr(ρ²) = 1/d (d是希尔伯特空间维度)

    纯度越低，态越混合（信息越少）。

    参数 Parameters:
        rho: 密度矩阵

    返回 Returns:
        Tr(ρ²): 纯度
    """
    return np.real(np.trace(rho @ rho))


# =============================================================================
# 练习 12.3: 不确定性原理
# Exercise 12.3: Uncertainty Principle
#
# 物理背景 Physical Background:
# 海森堡不确定性原理是量子力学的基本特征之一。
# 对于不对易的可观测量，不存在同时具有确定值的态:
#
#   ΔA · ΔB ≥ ½|⟨[A,B]⟩|
#
# 最著名的例子:
#   Δx · Δp ≥ ℏ/2 (因为 [x,p] = iℏ)
#
# 这不是测量精度的限制，而是量子态的内在性质。
# =============================================================================
def variance(psi, operator):
    """
    方差 Variance

    (ΔA)² = ⟨A²⟩ - ⟨A⟩²

    方差量化了测量结果的散布程度。
    方差为零意味着态是该可观测量的本征态。

    参数 Parameters:
        psi: 量子态
        operator: 可观测量算符

    返回 Returns:
        (ΔA)²: 方差
    """
    A_mean = expectation_value(psi, operator)
    A2_mean = expectation_value(psi, operator @ operator)
    return A2_mean - A_mean**2


def uncertainty_product(psi, A, B):
    """
    不确定性乘积 Uncertainty product

    ΔA × ΔB

    对于不对易的可观测量，不确定性乘积有下界:
    ΔA·ΔB ≥ ½|⟨[A,B]⟩|

    相干态达到最小不确定性（等号成立）。

    参数 Parameters:
        psi: 量子态
        A, B: 两个可观测量算符

    返回 Returns:
        ΔA·ΔB: 不确定性乘积
    """
    delta_A = np.sqrt(max(0, variance(psi, A)))
    delta_B = np.sqrt(max(0, variance(psi, B)))
    return delta_A * delta_B


def commutator(A, B):
    """
    对易子 Commutator

    [A, B] = AB - BA

    对易子的性质:
    - [A,B] = 0: A和B可同时对角化，有共同本征态
    - [A,B] ≠ 0: A和B不可同时确定

    例如: [x,p] = iℏ 导致位置-动量不确定性

    参数 Parameters:
        A, B: 两个算符（矩阵形式）

    返回 Returns:
        [A,B]: 对易子矩阵
    """
    return A @ B - B @ A


# =============================================================================
# 练习 12.4: 量子退相干
# Exercise 12.4: Quantum Decoherence
#
# 物理背景 Physical Background:
# 量子退相干是开放量子系统中量子相干性丢失的过程。
# 当量子系统与环境相互作用时，系统-环境整体处于纠缠态，
# 但对系统的约化描述表现为混合态。
#
# 退相干过程:
# 1. 密度矩阵的非对角元指数衰减
# 2. 对角元（概率）在经典分布中守恒
# 3. 量子叠加态变成经典混合态
#
# 退相干是理解量子-经典边界的关键:
# - 解释了薛定谔猫佯谬
# - 是量子计算的主要障碍
# =============================================================================
def decoherence_rate(gamma, n_th=0):
    """
    退相干率 Decoherence rate

    Γ_dec = γ(2n_th + 1)

    其中:
    - γ: 基础耗散率
    - n_th: 热平衡时的玻色子占据数

    低温极限 (n_th → 0): Γ_dec = γ
    高温极限 (n_th >> 1): Γ_dec ≈ 2γn_th ∝ T

    参数 Parameters:
        gamma: 耗散率 (s⁻¹)
        n_th: 热占据数

    返回 Returns:
        Γ_dec: 退相干率 (s⁻¹)
    """
    return gamma * (2 * n_th + 1)


def density_matrix_evolution_lindblad(rho, H, L_ops, dt):
    """
    Lindblad主方程演化（简化）Lindblad master equation evolution

    dρ/dt = -i[H,ρ]/ℏ + Σₖ(Lₖ ρ Lₖ† - ½{Lₖ†Lₖ, ρ})

    第一项: 幺正演化（薛定谔方程）
    第二项: 耗散项（与环境相互作用）

    Lindblad形式保证了:
    - ρ 保持正定
    - Tr(ρ) = 1 守恒
    - 完全正性

    参数 Parameters:
        rho: 密度矩阵
        H: 哈密顿量
        L_ops: Lindblad算符列表
        dt: 时间步长 (s)

    返回 Returns:
        rho_new: 演化后的密度矩阵
    """
    # 幺正部分 Unitary part
    rho_new = rho - 1j * dt / hbar * commutator(H, rho)

    # 耗散部分 Dissipative part
    for L in L_ops:
        L_dag = np.conj(L.T)
        rho_new += dt * (L @ rho @ L_dag - 0.5 * (L_dag @ L @ rho + rho @ L_dag @ L))

    return rho_new


def off_diagonal_decay(rho_12_0, gamma, t):
    """
    非对角元衰减 Off-diagonal decay

    ρ₁₂(t) = ρ₁₂(0)exp(-γt)

    非对角元编码了量子相干性。
    它们的衰减标志着量子叠加态向经典混合态的转变。

    典型时间尺度:
    - 原子: ~ μs 到 ms
    - 超导量子比特: ~ μs
    - 宏观物体: ~ fs (极快)

    参数 Parameters:
        rho_12_0: 初始非对角元
        gamma: 退相干率 (s⁻¹)
        t: 时间 (s)

    返回 Returns:
        ρ₁₂(t): 衰减后的非对角元
    """
    return rho_12_0 * np.exp(-gamma * t)


# =============================================================================
# 练习 12.5: 弱测量
# Exercise 12.5: Weak Measurement
#
# 物理背景 Physical Background:
# 弱测量是一种对系统扰动最小的测量方式。
# 通过弱耦合测量设备，可以获得"弱值"：
#
#   A_w = ⟨ψ_f|A|ψ_i⟩ / ⟨ψ_f|ψ_i⟩
#
# 弱值的特点:
# - 可以是复数
# - 可以超出本征值范围（"异常弱值"）
# - 当 ⟨ψ_f|ψ_i⟩ → 0 时可以很大
#
# 应用:
# - 高精度测量（信号放大）
# - 量子态层析
# - Hardy佯谬等量子基础研究
# =============================================================================
def weak_value(psi_i, A, psi_f):
    """
    弱值 Weak value

    A_w = ⟨ψ_f|A|ψ_i⟩ / ⟨ψ_f|ψ_i⟩

    其中 |ψ_i⟩ 是预选态，|ψ_f⟩ 是后选态。

    弱值可以超出可观测量的本征值范围！
    例如自旋1/2系统的弱值可以是100。

    参数 Parameters:
        psi_i: 初态（预选）
        A: 可观测量算符
        psi_f: 末态（后选）

    返回 Returns:
        A_w: 弱值（可能是复数）
    """
    numerator = np.vdot(psi_f, A @ psi_i)
    denominator = np.vdot(psi_f, psi_i)
    if np.abs(denominator) < 1e-10:
        return np.inf
    return numerator / denominator


def weak_measurement_shift(A_w, g):
    """
    弱测量导致的指针偏移 Pointer shift in weak measurement

    Δx ∝ g × Re(A_w)

    弱值的实部决定测量指针的平均偏移。
    通过后选择，可以实现信号放大。

    参数 Parameters:
        A_w: 弱值
        g: 耦合强度

    返回 Returns:
        Δx: 指针偏移（相对值）
    """
    return g * np.real(A_w)


# =============================================================================
# 练习 12.6: 量子Zeno效应
# Exercise 12.6: Quantum Zeno Effect
#
# 物理背景 Physical Background:
# 量子Zeno效应: 频繁测量可以"冻结"量子系统的演化。
# 名称来自芝诺悖论（飞矢不动）。
#
# 物理机制:
# - 短时间内，衰变概率 ∝ t² (非指数)
# - 每次测量将态投影回初态
# - n次测量后: P_survive ≈ (1 - (t/n)²)^n → 1 当 n → ∞
#
# 实验验证:
# - 离子阱中的能级演化
# - 光学系统中的极化演化
#
# 反Zeno效应:
# - 某些条件下，测量反而加速衰变
# - 取决于能谱的具体结构
# =============================================================================
def zeno_survival_probability(p_decay_single, n_measurements):
    """
    量子Zeno效应存活概率 Quantum Zeno survival probability

    频繁测量抑制量子态衰变。

    无测量: P_survive = 1 - p_decay
    n次测量: P_survive ≈ (1 - p/n)^n → 1 当 n → ∞

    这被称为"看着壶水不开"效应。

    参数 Parameters:
        p_decay_single: 无测量时的衰变概率
        n_measurements: 测量次数

    返回 Returns:
        P_survive: 存活概率
    """
    if n_measurements == 0:
        return 1 - p_decay_single
    p_per_interval = p_decay_single / n_measurements
    return (1 - p_per_interval)**n_measurements


def anti_zeno_rate(p_decay, n_measurements):
    """
    反Zeno效应（某些情况下测量加速衰变）Anti-Zeno effect

    在某些系统中（取决于能谱结构），
    测量反而会加速量子态的衰变。

    这发生在:
    - 能谱有特定的功率律形式
    - 测量率处于特定范围

    参数 Parameters:
        p_decay: 基础衰变概率
        n_measurements: 测量次数

    返回 Returns:
        增强后的衰变率
    """
    # 简化模型
    return p_decay * (1 + 0.1 * n_measurements)


# =============================================================================
# 可视化
# =============================================================================
def plot_measurement():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 测量概率
    ax1 = axes[0, 0]
    # 自旋1/2系统
    theta = np.linspace(0, np.pi, 100)
    psi = np.array([1, 0], dtype=complex)  # |↑⟩
    up_z = np.array([1, 0], dtype=complex)
    down_z = np.array([0, 1], dtype=complex)

    p_up = []
    p_down = []
    for t in theta:
        psi_rotated = np.array([np.cos(t/2), np.sin(t/2)], dtype=complex)
        p_up.append(measurement_probability(psi_rotated, up_z))
        p_down.append(measurement_probability(psi_rotated, down_z))

    ax1.plot(np.degrees(theta), p_up, 'b-', label='P(↑)', linewidth=2)
    ax1.plot(np.degrees(theta), p_down, 'r-', label='P(↓)', linewidth=2)
    ax1.set_xlabel('θ (degrees)')
    ax1.set_ylabel('概率')
    ax1.set_title('测量概率 vs 态参数')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 密度矩阵纯度
    ax2 = axes[0, 1]
    p = np.linspace(0, 0.5, 100)

    purity = []
    for pi in p:
        states = [np.array([1, 0]), np.array([0, 1])]
        probs = [1-pi, pi]
        rho = mixed_state_density_matrix(states, probs)
        purity.append(density_matrix_purity(rho))

    ax2.plot(p, purity, 'g-', linewidth=2)
    ax2.axhline(y=1, color='b', linestyle='--', alpha=0.5, label='纯态')
    ax2.axhline(y=0.5, color='r', linestyle='--', alpha=0.5, label='最大混合')
    ax2.set_xlabel('混合概率 p')
    ax2.set_ylabel('纯度 Tr(ρ²)')
    ax2.set_title('密度矩阵纯度')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 退相干
    ax3 = axes[0, 2]
    t = np.linspace(0, 5, 100)
    gamma = 1

    rho_12 = [np.abs(off_diagonal_decay(1, gamma, ti))**2 for ti in t]

    ax3.plot(t, rho_12, 'purple', linewidth=2)
    ax3.set_xlabel('γt')
    ax3.set_ylabel('|ρ₁₂|²')
    ax3.set_title('非对角元退相干')
    ax3.grid(True, alpha=0.3)

    # 4. 不确定性关系
    ax4 = axes[1, 0]
    # 相干态参数α
    alpha = np.linspace(0.1, 5, 100)

    # 简化：不确定性乘积
    uncertainty = [1/2] * len(alpha)  # 相干态达到最小

    ax4.plot(alpha, uncertainty, 'b-', linewidth=2, label='相干态')
    ax4.axhline(y=0.5, color='r', linestyle='--', alpha=0.5, label='ℏ/2 (最小)')
    ax4.set_xlabel('|α|')
    ax4.set_ylabel('Δx·Δp/ℏ')
    ax4.set_title('不确定性乘积')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 量子Zeno效应
    ax5 = axes[1, 1]
    n_meas = np.arange(1, 50)
    p_decay = 0.5

    p_survive = [zeno_survival_probability(p_decay, n) for n in n_meas]

    ax5.plot(n_meas, p_survive, 'orange', linewidth=2)
    ax5.axhline(y=1-p_decay, color='k', linestyle='--', alpha=0.5, label='无测量')
    ax5.set_xlabel('测量次数')
    ax5.set_ylabel('存活概率')
    ax5.set_title('量子Zeno效应')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. 弱值
    ax6 = axes[1, 2]
    # σ_z 的弱值随后选态变化
    sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
    psi_i = np.array([1, 1], dtype=complex) / np.sqrt(2)  # |+x⟩

    theta_f = np.linspace(0.1, np.pi-0.1, 100)
    weak_vals = []
    for t in theta_f:
        psi_f = np.array([np.cos(t/2), np.sin(t/2)], dtype=complex)
        w = weak_value(psi_i, sigma_z, psi_f)
        weak_vals.append(np.real(w))

    ax6.plot(np.degrees(theta_f), weak_vals, 'cyan', linewidth=2)
    ax6.axhline(y=1, color='b', linestyle='--', alpha=0.5, label='σ_z本征值')
    ax6.axhline(y=-1, color='r', linestyle='--', alpha=0.5)
    ax6.set_xlabel('后选态角度 θ')
    ax6.set_ylabel('弱值 Re(σ_z)_w')
    ax6.set_title('弱值（可超出本征值范围）')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('measurement.png', dpi=150)
    print("图像已保存为 measurement.png")
    plt.show()


def verify():
    all_passed = True

    # Check 12.1
    psi = np.array([1, 0], dtype=complex)
    eigenstate = np.array([1, 0], dtype=complex)
    p = measurement_probability(psi, eigenstate)
    if not np.isclose(p, 1.0, rtol=0.01):
        print("❌ 12.1 测量概率错误")
        all_passed = False
    else:
        print("✓ 12.1 测量公设正确")

    # Check 12.2
    rho_pure = pure_state_density_matrix(psi)
    purity = density_matrix_purity(rho_pure)
    if not np.isclose(purity, 1.0, rtol=0.01):
        print("❌ 12.2 纯态纯度应为1")
        all_passed = False
    else:
        print("✓ 12.2 密度矩阵正确")

    # Check 12.3
    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
    comm = commutator(sigma_x, sigma_z)
    if np.allclose(comm, np.zeros((2, 2))):
        print("❌ 12.3 σ_x和σ_z不对易")
        all_passed = False
    else:
        print("✓ 12.3 不确定性原理正确")

    # Check 12.4
    rho_12 = off_diagonal_decay(1, 1, 1)
    expected = np.exp(-1)
    if not np.isclose(np.abs(rho_12), expected, rtol=0.01):
        print("❌ 12.4 退相干衰减错误")
        all_passed = False
    else:
        print("✓ 12.4 量子退相干正确")

    # Check 12.5
    psi_i = np.array([1, 0], dtype=complex)
    psi_f = np.array([1, 0], dtype=complex)
    A = np.array([[1, 0], [0, -1]], dtype=complex)
    w = weak_value(psi_i, A, psi_f)
    if not np.isclose(np.real(w), 1, rtol=0.01):
        print("❌ 12.5 弱值错误")
        all_passed = False
    else:
        print("✓ 12.5 弱测量正确")

    # Check 12.6
    p_survive = zeno_survival_probability(0.5, 100)
    if not p_survive > 0.5:
        print("❌ 12.6 Zeno效应应增加存活概率")
        all_passed = False
    else:
        print(f"✓ 12.6 量子Zeno效应正确 (P_survive = {p_survive:.3f})")

    if all_passed:
        print("\n🎉 所有测试通过！")
        try:
            plot_measurement()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("量子测量 Quantum Measurement")
    print("=" * 50)
    verify()
