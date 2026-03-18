"""
密度矩阵 Density Matrix
难度 Difficulty: ★★★★★

学习目标 Learning Objectives:
- 理解密度矩阵的物理意义和数学性质
- 区分纯态和混合态，掌握纯度和熵的概念
- 学习开放量子系统和退相干过程
- 理解约化密度矩阵与量子纠缠的关系

物理背景 Physical Background:
1. 密度矩阵是描述量子态最一般的方式
   - 纯态: ρ = |ψ⟩⟨ψ|（完全量子态信息）
   - 混合态: ρ = Σᵢ pᵢ|ψᵢ⟩⟨ψᵢ|（统计混合或纠缠子系统）
2. 密度矩阵的基本性质:
   - 厄米性: ρ† = ρ
   - 正定性: 所有本征值 ≥ 0
   - 归一化: Tr(ρ) = 1
3. 退相干是量子-经典过渡的关键

关键公式 Key Formulas:
- 期望值: ⟨A⟩ = Tr(ρA)
- 纯度: γ = Tr(ρ²)，纯态γ=1，混合态γ<1
- 冯诺依曼熵: S = -Tr(ρ ln ρ)
- 刘维尔方程: dρ/dt = -i/ℏ [H, ρ]
- Lindblad方程: dρ/dt = -i/ℏ [H, ρ] + Σₖ γₖ(LₖρLₖ† - ½{Lₖ†Lₖ, ρ})
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm, logm
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import hbar, k_B

# I AM NOT DONE

# =============================================================================
# 练习 1.1: 密度矩阵构建 Constructing Density Matrix
#
# 物理背景:
# 密度矩阵（密度算符）是量子态最一般的表示
# - 纯态: 系统处于确定的量子态 |ψ⟩
# - 混合态: 系统以概率 pᵢ 处于态 |ψᵢ⟩（经典概率叠加）
#
# 纯态与混合态的区别:
# - 纯态来自量子叠加: |ψ⟩ = α|0⟩ + β|1⟩
# - 混合态来自经典不确定性: p₁|ψ₁⟩⟨ψ₁| + p₂|ψ₂⟩⟨ψ₂|
# =============================================================================
def pure_state_density_matrix(psi):
    """
    构建纯态密度矩阵 Pure state density matrix

    参数 Parameters:
        psi: 态向量 |ψ⟩（需归一化）

    返回 Returns:
        rho: 密度矩阵 ρ = |ψ⟩⟨ψ|

    性质: Tr(ρ²) = 1（纯态判据）
    """
    psi = np.array(psi, dtype=complex)
    # TODO: 构建密度矩阵（外积）
    rho = np.outer(psi, np.conj(psi))
    return rho


def mixed_state_density_matrix(states, probabilities):
    """
    构建混合态密度矩阵 Mixed state density matrix

    参数 Parameters:
        states: 态向量列表 [|ψ₁⟩, |ψ₂⟩, ...]
        probabilities: 对应概率列表 [p₁, p₂, ...]，需满足 Σpᵢ = 1

    返回 Returns:
        rho: 密度矩阵 ρ = Σᵢ pᵢ|ψᵢ⟩⟨ψᵢ|

    物理意义: 经典地不知道系统处于哪个态
    例如: 偏振光通过偏振片后的混合态
    """
    dim = len(states[0])
    rho = np.zeros((dim, dim), dtype=complex)

    # TODO: 构建混合态密度矩阵（加权求和）
    for psi, p in zip(states, probabilities):
        psi = np.array(psi, dtype=complex)
        rho += p * np.outer(psi, np.conj(psi))

    return rho


def verify_density_matrix(rho):
    """
    验证密度矩阵的三个基本性质 Verify density matrix properties

    1. 厄米性: ρ† = ρ（可观测量的期望值为实数）
    2. 正半定: 所有本征值 ≥ 0（概率非负）
    3. 迹归一: Tr(ρ) = 1（总概率为1）

    返回 Returns:
        bool: 是否满足所有性质
    """
    is_hermitian = np.allclose(rho, rho.conj().T)
    eigenvalues = np.linalg.eigvalsh(rho)
    is_positive = np.all(eigenvalues >= -1e-10)
    trace_one = np.isclose(np.trace(rho), 1)

    return is_hermitian and is_positive and trace_one


# =============================================================================
# 练习 1.2: 纯度和熵 Purity and Entropy
#
# 物理背景:
# 纯度和熵是量化"混合程度"的两种方式
#
# 纯度 γ = Tr(ρ²):
# - γ = 1: 纯态（完全量子信息）
# - γ = 1/d: 最大混合态（完全无信息，d是维度）
#
# 冯诺依曼熵 S = -Tr(ρ ln ρ):
# - S = 0: 纯态
# - S = ln(d): 最大混合态
# - S 是信息论中香农熵的量子推广
# =============================================================================
def purity(rho):
    """
    计算密度矩阵的纯度 Purity of density matrix

    参数 Parameters:
        rho: 密度矩阵

    返回 Returns:
        γ = Tr(ρ²)，范围 [1/d, 1]

    判据:
    - γ = 1: 纯态
    - 1/d < γ < 1: 部分混合
    - γ = 1/d: 最大混合态（如完全去极化）
    """
    # TODO: 计算纯度（矩阵乘法后取迹）
    return np.real(np.trace(rho @ rho))


def is_pure_state(rho):
    """
    判断密度矩阵是否描述纯态 Check if pure state

    纯态判据: Tr(ρ²) = 1（等价于ρ² = ρ）
    """
    return np.isclose(purity(rho), 1)


def von_neumann_entropy(rho):
    """
    计算冯诺依曼熵 von Neumann entropy

    参数 Parameters:
        rho: 密度矩阵

    返回 Returns:
        S = -Tr(ρ ln ρ) = -Σᵢ λᵢ ln λᵢ

    物理意义:
    - 测量系统"不确定性"或"信息缺失"
    - 对于纠缠态，约化态的熵量化纠缠程度

    单位: 自然单位（nats），用 log₂ 则为 bits
    """
    eigenvalues = np.linalg.eigvalsh(rho)
    # 过滤掉零本征值（避免 log(0)）
    eigenvalues = eigenvalues[eigenvalues > 1e-15]

    # TODO: 计算熵 S = -Σ λᵢ ln(λᵢ)
    S = -np.sum(eigenvalues * np.log(eigenvalues))
    return S


def linear_entropy(rho):
    """
    计算线性熵 Linear entropy

    S_L = 1 - Tr(ρ²) = 1 - γ

    线性熵是冯诺依曼熵的线性近似，计算更简单
    范围 [0, 1-1/d]
    """
    return 1 - purity(rho)


# =============================================================================
# 练习 1.3: 期望值和测量 Expectation Values and Measurement
#
# 物理背景:
# 密度矩阵形式的期望值公式更一般，适用于纯态和混合态
# ⟨A⟩ = Tr(ρA)
#
# 测量过程:
# 1. 得到结果i的概率: P(i) = Tr(ρPᵢ)
# 2. 测量后态（塌缩）: ρ' = PᵢρPᵢ/Tr(PᵢρPᵢ)
# 其中 Pᵢ 是结果i对应的投影算符
# =============================================================================
def expectation_value(rho, A):
    """
    计算可观测量的期望值 Expectation value of observable

    参数 Parameters:
        rho: 密度矩阵
        A: 可观测量（厄米矩阵）

    返回 Returns:
        ⟨A⟩ = Tr(ρA)，实数

    这是量子力学中最基本的预测公式
    """
    return np.real(np.trace(rho @ A))


def measurement_probabilities(rho, projectors):
    """
    计算测量各结果的概率 Measurement probabilities

    参数 Parameters:
        rho: 密度矩阵
        projectors: 投影算符列表 [P₁, P₂, ...]

    返回 Returns:
        probs: 各结果的概率数组

    玻恩规则: P(i) = Tr(ρPᵢ)
    投影算符满足: ΣPᵢ = I, PᵢPⱼ = δᵢⱼPᵢ
    """
    probs = []
    for P in projectors:
        probs.append(np.real(np.trace(rho @ P)))
    return np.array(probs)


def post_measurement_state(rho, projector):
    """
    计算测量后的态 Post-measurement state

    参数 Parameters:
        rho: 测量前的密度矩阵
        projector: 测量结果对应的投影算符 P

    返回 Returns:
        rho': 测量后的密度矩阵 = PρP/Tr(PρP)
        如果该结果概率为0，返回 None

    这是量子态塌缩的密度矩阵描述
    """
    rho_new = projector @ rho @ projector
    trace = np.trace(rho_new)
    if trace < 1e-15:
        return None  # 测量结果概率为0
    return rho_new / trace


# =============================================================================
# 练习 1.4: 时间演化 Time Evolution
#
# 物理背景:
# 1. 封闭系统（刘维尔方程）:
#    dρ/dt = -i/ℏ [H, ρ]
#    解: ρ(t) = U(t)ρ(0)U†(t)，保持纯度不变
#
# 2. 开放系统（Lindblad方程）:
#    dρ/dt = -i/ℏ [H, ρ] + Σₖ γₖ(LₖρLₖ† - ½{Lₖ†Lₖ, ρ})
#    描述退相干、耗散等不可逆过程
#    纯度会下降，熵会增加
# =============================================================================
def liouville_evolution(rho_0, H, t):
    """
    封闭系统的刘维尔演化 Liouville evolution (closed system)

    参数 Parameters:
        rho_0: 初始密度矩阵
        H: 哈密顿量，单位 J
        t: 演化时间，单位 s

    返回 Returns:
        rho_t: 时刻t的密度矩阵 = U(t)ρ₀U†(t)

    性质: 保持纯度不变，熵不变（可逆过程）
    """
    U = expm(-1j * H * t / hbar)  # 时间演化算符
    U_dag = U.conj().T

    # TODO: 计算演化后的密度矩阵（夹心公式）
    rho_t = U @ rho_0 @ U_dag
    return rho_t


def lindblad_equation(rho, H, L_ops, gamma):
    """
    Lindblad主方程（开放系统）Lindblad master equation

    参数 Parameters:
        rho: 当前密度矩阵
        H: 系统哈密顿量
        L_ops: Lindblad算符列表 [L₁, L₂, ...]
        gamma: 耗散率

    返回 Returns:
        dρ/dt: 密度矩阵的时间导数

    方程: dρ/dt = -i/ℏ[H,ρ] + γΣₖ(LₖρLₖ† - ½{Lₖ†Lₖ,ρ})

    常见Lindblad算符:
    - 退相位: L = σz（损失相位信息）
    - 自发辐射: L = σ₋（损失能量）
    - 热化: L₁ = σ₊, L₂ = σ₋（热浴）
    """
    # 幺正部分（可逆）
    commutator = H @ rho - rho @ H
    drho_dt = -1j / hbar * commutator

    # 耗散部分（不可逆，Lindblad形式）
    for L in L_ops:
        L_dag = L.conj().T
        L_dag_L = L_dag @ L

        drho_dt += gamma * (L @ rho @ L_dag -
                           0.5 * (L_dag_L @ rho + rho @ L_dag_L))

    return drho_dt


# =============================================================================
# 练习 1.5: 约化密度矩阵和纠缠 Reduced Density Matrix and Entanglement
#
# 物理背景:
# 当我们只能访问复合系统的一部分时，需要约化密度矩阵
# ρ_A = Tr_B(ρ_AB)（对B求偏迹）
#
# 纠缠与约化态:
# - 直积态: ρ_AB = ρ_A ⊗ ρ_B → 约化态是纯态
# - 纠缠态: 约化态是混合态（信息"隐藏"在关联中）
# - 纠缠熵: S(ρ_A) 量化纠缠程度
#
# 对于最大纠缠态（如Bell态），S(ρ_A) = ln(2) ≈ 0.693
# =============================================================================
def partial_trace_A(rho_AB, dim_A, dim_B):
    """
    对子系统A求偏迹 Partial trace over A

    参数 Parameters:
        rho_AB: 复合系统密度矩阵
        dim_A, dim_B: 子系统维度

    返回 Returns:
        ρ_B = Tr_A(ρ_AB): B的约化密度矩阵

    约化密度矩阵描述子系统的局域性质
    """
    rho_AB = rho_AB.reshape(dim_A, dim_B, dim_A, dim_B)

    # TODO: 计算约化密度矩阵（对A的指标求迹）
    rho_B = np.trace(rho_AB, axis1=0, axis2=2)
    return rho_B


def partial_trace_B(rho_AB, dim_A, dim_B):
    """
    对子系统B求偏迹 Partial trace over B

    返回 ρ_A = Tr_B(ρ_AB): A的约化密度矩阵
    """
    rho_AB = rho_AB.reshape(dim_A, dim_B, dim_A, dim_B)
    rho_A = np.trace(rho_AB, axis1=1, axis2=3)
    return rho_A


def entanglement_entropy(rho_AB, dim_A, dim_B):
    """
    计算纠缠熵 Entanglement entropy

    参数 Parameters:
        rho_AB: 复合系统密度矩阵（应为纯态）
        dim_A, dim_B: 子系统维度

    返回 Returns:
        S_A = -Tr(ρ_A ln ρ_A): 约化态的冯诺依曼熵

    对于纯态，纠缠熵量化A和B之间的纠缠
    S_A = S_B（对纯态成立）
    """
    rho_A = partial_trace_B(rho_AB, dim_A, dim_B)
    return von_neumann_entropy(rho_A)


def is_separable_pure(psi_AB, dim_A, dim_B):
    """
    判断纯态是否可分离 Check if pure state is separable

    可分离态: |ψ_AB⟩ = |ψ_A⟩ ⊗ |ψ_B⟩
    不可分离 = 纠缠态

    判据: 约化密度矩阵是纯态 ⟺ 可分离
    """
    rho_AB = pure_state_density_matrix(psi_AB)
    rho_A = partial_trace_B(rho_AB, dim_A, dim_B)
    return is_pure_state(rho_A)


# =============================================================================
# 练习 1.6: 热态 Thermal State
#
# 物理背景:
# 热平衡态是统计力学的核心概念
# 正则系综: ρ = exp(-βH)/Z，β = 1/(k_B T)
# Z = Tr(exp(-βH)) 是配分函数
#
# 性质:
# - T → 0: 趋向基态（纯态）
# - T → ∞: 趋向最大混合态（所有能级等概率）
# - 热力学量可从配分函数导出
# =============================================================================
def thermal_density_matrix(H, T):
    """
    计算热平衡态密度矩阵 Thermal equilibrium density matrix

    参数 Parameters:
        H: 哈密顿量矩阵
        T: 温度，单位 K

    返回 Returns:
        ρ = exp(-H/k_B T)/Z: 正则系综密度矩阵

    极限情况:
    - T → 0: 基态（纯态）
    - T → ∞: I/d（最大混合态，d是维度）
    """
    if T < 1e-10:  # T → 0 极限: 纯基态
        eigenvalues, eigenvectors = np.linalg.eigh(H)
        ground_state = eigenvectors[:, 0]
        return pure_state_density_matrix(ground_state)

    # TODO: 计算热态密度矩阵
    beta = 1 / (k_B * T)  # 逆温度
    exp_H = expm(-beta * H)  # Boltzmann因子
    Z = np.trace(exp_H)  # 配分函数
    rho = exp_H / Z  # 归一化

    return rho


def partition_function(H, T):
    """
    计算配分函数 Partition function

    Z = Tr(exp(-H/k_B T)) = Σᵢ exp(-Eᵢ/k_B T)

    配分函数包含系统的全部热力学信息:
    - 自由能: F = -k_B T ln Z
    - 内能: U = -∂ln Z/∂β
    - 熵: S = k_B(ln Z + βU)
    """
    beta = 1 / (k_B * T)
    exp_H = expm(-beta * H)
    return np.real(np.trace(exp_H))


def thermal_energy(H, T):
    """
    计算热平衡态的平均能量 Thermal average energy

    ⟨E⟩ = Tr(ρH) = Σᵢ Eᵢ pᵢ

    其中 pᵢ = exp(-βEᵢ)/Z 是Boltzmann分布
    """
    rho = thermal_density_matrix(H, T)
    return expectation_value(rho, H)


def specific_heat(H, T, dT=0.01):
    """
    计算比热容 Specific heat（数值导数）

    C = d⟨E⟩/dT

    比热容反映系统吸收热量的能力
    """
    E_plus = thermal_energy(H, T + dT/2)
    E_minus = thermal_energy(H, T - dT/2)
    return (E_plus - E_minus) / dT


# =============================================================================
# 练习 1.7: Bloch球表示 Bloch Sphere Representation
#
# 物理背景:
# 任意二能级系统密度矩阵可参数化为:
# ρ = (I + r⃗·σ⃗)/2
# 其中 r⃗ = (rₓ, rᵧ, rᵤ) 是Bloch向量
#
# Bloch球几何:
# - |r⃗| = 1: 球面上的点 → 纯态
# - |r⃗| < 1: 球内的点 → 混合态
# - |r⃗| = 0: 球心 → 最大混合态 I/2
#
# Bloch向量方向代表自旋极化方向
# =============================================================================
def density_matrix_to_bloch(rho):
    """
    密度矩阵转Bloch向量 Density matrix to Bloch vector

    参数 Parameters:
        rho: 2×2 密度矩阵

    返回 Returns:
        r⃗ = (rₓ, rᵧ, rᵤ): Bloch向量

    公式: rᵢ = Tr(ρσᵢ)，其中σᵢ是泡利矩阵
    """
    sigma_x = np.array([[0, 1], [1, 0]])
    sigma_y = np.array([[0, -1j], [1j, 0]])
    sigma_z = np.array([[1, 0], [0, -1]])

    # TODO: 计算Bloch向量分量（泡利矩阵期望值）
    r_x = np.real(np.trace(rho @ sigma_x))
    r_y = np.real(np.trace(rho @ sigma_y))
    r_z = np.real(np.trace(rho @ sigma_z))

    return np.array([r_x, r_y, r_z])


def bloch_to_density_matrix(r):
    """
    Bloch向量转密度矩阵 Bloch vector to density matrix

    参数 Parameters:
        r: Bloch向量 (rₓ, rᵧ, rᵤ)

    返回 Returns:
        ρ = (I + r⃗·σ⃗)/2

    物理态要求 |r⃗| ≤ 1
    """
    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
    I = np.eye(2, dtype=complex)

    rho = (I + r[0]*sigma_x + r[1]*sigma_y + r[2]*sigma_z) / 2
    return rho


def bloch_vector_length(r):
    """
    计算Bloch向量长度 Bloch vector length

    |r⃗| 与纯度的关系: γ = (1 + |r⃗|²)/2

    判据:
    - |r⃗| = 1: 纯态（Bloch球面）
    - |r⃗| < 1: 混合态（Bloch球内）
    - |r⃗| = 0: 最大混合态（球心）
    """
    return np.linalg.norm(r)


# =============================================================================
# 可视化 Visualization
# 绘制Bloch球、热态占据、退相干过程等图像
# =============================================================================
def plot_density_matrix():
    """绘制密度矩阵相关图像"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # 1. 纯态和混合态的Bloch球
    ax1 = fig.add_subplot(2, 2, 1, projection='3d')

    # 画Bloch球
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    x_sphere = np.outer(np.cos(u), np.sin(v))
    y_sphere = np.outer(np.sin(u), np.sin(v))
    z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))
    ax1.plot_surface(x_sphere, y_sphere, z_sphere, alpha=0.1, color='gray')

    # 纯态: |+>
    psi_plus = np.array([1, 1]) / np.sqrt(2)
    rho_pure = pure_state_density_matrix(psi_plus)
    r_pure = density_matrix_to_bloch(rho_pure)
    ax1.scatter(*r_pure, s=100, c='b', marker='o', label='Pure state')

    # 混合态
    rho_mixed = mixed_state_density_matrix(
        [[1, 0], [0, 1]], [0.7, 0.3])
    r_mixed = density_matrix_to_bloch(rho_mixed)
    ax1.scatter(*r_mixed, s=100, c='r', marker='s', label='Mixed state')

    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    ax1.set_title('Bloch球表示')
    ax1.legend()

    # 2. 热态能级占据
    ax2 = axes[0, 1]
    # 三能级系统
    E = np.array([0, 1, 2]) * 1e-21  # 能级 (J)
    H = np.diag(E)
    T_range = np.linspace(0.01, 2, 100) * 1e-21 / k_B

    populations = []
    for T in T_range:
        rho = thermal_density_matrix(H, T)
        pop = np.diag(rho).real
        populations.append(pop)

    populations = np.array(populations)

    for i in range(3):
        ax2.plot(T_range * k_B / 1e-21, populations[:, i],
                label=f'E_{i}', linewidth=2)

    ax2.set_xlabel('k_B T / E_gap')
    ax2.set_ylabel('Population')
    ax2.set_title('热态能级占据')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 纯度随退相干的演化
    ax3 = axes[1, 0]

    # 初始纯态
    psi_0 = np.array([1, 1]) / np.sqrt(2)
    rho_0 = pure_state_density_matrix(psi_0)

    # 退相干（Lindblad演化）
    H = np.array([[0, 0], [0, 1e-20]])  # 简单哈密顿量
    L = np.array([[1, 0], [0, -1]])  # 退相位噪声

    gamma_values = [0, 0.1, 0.5, 1.0]
    t_range = np.linspace(0, 5, 100) * 1e-15

    for gamma in gamma_values:
        purity_list = []
        rho = rho_0.copy()
        dt = t_range[1] - t_range[0]

        for t in t_range:
            purity_list.append(purity(rho))
            drho = lindblad_equation(rho, H, [L], gamma * 1e15)
            rho = rho + drho * dt

        ax3.plot(t_range * 1e15, purity_list, label=f'gamma = {gamma}', linewidth=2)

    ax3.set_xlabel('Time (fs)')
    ax3.set_ylabel('Purity')
    ax3.set_title('退相干过程中的纯度')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 约化密度矩阵（Bell态）
    ax4 = axes[1, 1]

    # Bell态 |00> + |11>
    psi_bell = np.array([1, 0, 0, 1]) / np.sqrt(2)
    rho_bell = pure_state_density_matrix(psi_bell)
    rho_A = partial_trace_B(rho_bell, 2, 2)

    # 可视化约化密度矩阵
    im = ax4.imshow(np.abs(rho_A), cmap='Blues')
    ax4.set_xticks([0, 1])
    ax4.set_yticks([0, 1])
    ax4.set_xticklabels(['|0>', '|1>'])
    ax4.set_yticklabels(['|0>', '|1>'])
    ax4.set_title(f'Bell态的约化密度矩阵 (S = {entanglement_entropy(rho_bell, 2, 2):.3f})')
    plt.colorbar(im, ax=ax4)

    plt.tight_layout()
    plt.savefig('density_matrix.png', dpi=150)
    print("图像已保存为 density_matrix.png")
    plt.show()


# =============================================================================
# 验证函数 Verification
# =============================================================================
def verify():
    """验证所有练习的正确性 Verify all exercises"""
    all_passed = True

    # 检查 1.1: 密度矩阵构建
    psi = np.array([1, 0])
    rho_pure = pure_state_density_matrix(psi)
    if not verify_density_matrix(rho_pure):
        print("错误 1.1: 纯态密度矩阵不满足基本性质")
        all_passed = False
    else:
        print("通过 1.1: 密度矩阵构建正确")

    # 检查 1.2: 纯度计算
    p = purity(rho_pure)
    if not np.isclose(p, 1):
        print("错误 1.2: 纯态纯度应为1")
        all_passed = False
    else:
        rho_mixed = mixed_state_density_matrix([[1, 0], [0, 1]], [0.5, 0.5])
        p_mixed = purity(rho_mixed)
        print(f"通过 1.2: 纯度计算正确 (纯态: {p:.1f}, 最大混合态: {p_mixed:.2f})")

    # 检查 1.3: 期望值
    sigma_z = np.array([[1, 0], [0, -1]])
    exp_z = expectation_value(rho_pure, sigma_z)
    if not np.isclose(exp_z, 1):
        print("错误 1.3: |0⟩态的σᵤ期望值应为+1")
        all_passed = False
    else:
        print("通过 1.3: 期望值计算正确")

    # 检查 1.4: 刘维尔演化
    H = np.array([[0, 1], [1, 0]]) * 1e-20
    t = 1e-15
    rho_t = liouville_evolution(rho_pure, H, t)
    if not verify_density_matrix(rho_t):
        print("错误 1.4: 刘维尔演化后密度矩阵不满足基本性质")
        all_passed = False
    else:
        print("通过 1.4: 时间演化正确（保持密度矩阵性质）")

    # 检查 1.5: 约化密度矩阵
    psi_bell = np.array([1, 0, 0, 1]) / np.sqrt(2)
    rho_bell = pure_state_density_matrix(psi_bell)
    rho_A = partial_trace_B(rho_bell, 2, 2)

    S_ent = entanglement_entropy(rho_bell, 2, 2)
    if not np.isclose(S_ent, np.log(2), rtol=0.01):
        print("错误 1.5: Bell态纠缠熵应为 ln(2)")
        all_passed = False
    else:
        print(f"通过 1.5: 约化密度矩阵正确 (Bell态纠缠熵 = ln2 ≈ {S_ent:.3f})")

    # 检查 1.6: 热态
    E = np.array([0, 1]) * 1e-21
    H = np.diag(E)
    T = 1e-21 / k_B  # k_B T = 能隙

    rho_thermal = thermal_density_matrix(H, T)
    if not verify_density_matrix(rho_thermal):
        print("错误 1.6: 热态密度矩阵不满足基本性质")
        all_passed = False
    else:
        pop = np.diag(rho_thermal).real
        print(f"通过 1.6: 热态正确 (T=E/k_B时能级占据: {pop[0]:.3f}, {pop[1]:.3f})")

    # 检查 1.7: Bloch球表示
    psi = np.array([1, 0])
    rho = pure_state_density_matrix(psi)
    r = density_matrix_to_bloch(rho)
    r_length = bloch_vector_length(r)

    if not np.isclose(r_length, 1):
        print("错误 1.7: 纯态的Bloch向量长度应为1")
        all_passed = False
    else:
        print(f"通过 1.7: Bloch球表示正确 (纯态|r⃗| = {r_length:.3f})")

    if all_passed:
        print("\n所有测试通过！")
        try:
            plot_density_matrix()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("密度矩阵 Density Matrix")
    print("=" * 50)
    verify()
