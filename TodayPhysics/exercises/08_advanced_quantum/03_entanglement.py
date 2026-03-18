"""
量子纠缠与贝尔不等式 Quantum Entanglement and Bell Inequality
难度 Difficulty: ★★★★★

学习目标 Learning Objectives:
- 理解量子纠缠的物理本质和数学描述
- 掌握贝尔态的构造和性质
- 学习CHSH不等式及其量子违背
- 理解量子非定域性与EPR悖论

物理背景 Physical Background:
1. 量子纠缠是量子力学最神秘的特征之一
2. 纠缠态不能写成乘积态: |ψ⟩_AB ≠ |ψ⟩_A ⊗ |ψ⟩_B
3. 测量一个粒子会瞬间影响另一个粒子的状态（非定域关联）
4. 1964年贝尔提出可检验的不等式，区分量子力学与隐变量理论

关键公式 Key Formulas:
- 贝尔态（最大纠缠态）:
  |Φ±⟩ = (|00⟩ ± |11⟩)/√2
  |Ψ±⟩ = (|01⟩ ± |10⟩)/√2
- CHSH不等式: S = E(a,b) - E(a,b') + E(a',b) + E(a',b')
  经典极限: |S| ≤ 2
  量子极限: |S| ≤ 2√2（奇雷尔松边界）
- 纠缠熵: S(ρ_A) = -Tr(ρ_A log ρ_A)

历史意义:
- EPR悖论（1935）: 爱因斯坦等质疑量子力学完备性
- 贝尔定理（1964）: 证明局域隐变量理论与量子力学不相容
- 阿斯佩实验（1982）: 首次验证贝尔不等式违背
- 2022年诺贝尔物理学奖授予量子纠缠实验研究
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])

# I AM NOT DONE

# =============================================================================
# 练习 3.1: 两比特态 Two-Qubit States
#
# 物理背景:
# 两个量子比特的联合希尔伯特空间是各自空间的张量积
# H_AB = H_A ⊗ H_B，维度为 2×2 = 4
#
# 计算基: |00⟩, |01⟩, |10⟩, |11⟩
# 第一个数字是A粒子的状态，第二个是B粒子的状态
# =============================================================================
def tensor_product(state1, state2):
    """
    计算两个态的张量积 Tensor product: |ψ₁⟩⊗|ψ₂⟩

    参数 Parameters:
        state1: 第一个子系统的态向量
        state2: 第二个子系统的态向量

    返回 Returns:
        联合系统的态向量，维度为 dim1 × dim2
    """
    return np.kron(state1, state2)

def computational_basis():
    """
    返回两比特计算基 Computational basis states

    返回 Returns:
        (|00⟩, |01⟩, |10⟩, |11⟩) 四个正交归一化基向量

    这些态是直积态（非纠缠态）
    任意两比特态可写成: |ψ⟩ = α|00⟩ + β|01⟩ + γ|10⟩ + δ|11⟩
    """
    ket_0 = np.array([1, 0], dtype=complex)  # |0⟩
    ket_1 = np.array([0, 1], dtype=complex)  # |1⟩

    ket_00 = tensor_product(ket_0, ket_0)  # |00⟩ = [1,0,0,0]
    ket_01 = tensor_product(ket_0, ket_1)  # |01⟩ = [0,1,0,0]
    ket_10 = tensor_product(ket_1, ket_0)  # |10⟩ = [0,0,1,0]
    ket_11 = tensor_product(ket_1, ket_1)  # |11⟩ = [0,0,0,1]

    return ket_00, ket_01, ket_10, ket_11


# =============================================================================
# 练习 3.2: 贝尔态 Bell States
#
# 物理背景:
# 贝尔态是四个最大纠缠的两比特态，构成正交完备基
# 它们在量子信息中有核心地位（量子隐形传态、超密编码等）
#
# 四个贝尔态:
#   |Φ⁺⟩ = (|00⟩ + |11⟩)/√2  - 自旋三重态之一
#   |Φ⁻⟩ = (|00⟩ - |11⟩)/√2  - 自旋三重态之一
#   |Ψ⁺⟩ = (|01⟩ + |10⟩)/√2  - 自旋三重态之一
#   |Ψ⁻⟩ = (|01⟩ - |10⟩)/√2  - 自旋单态（反对称）
#
# 性质: 纠缠熵都为1 bit（最大纠缠）
# =============================================================================
def bell_phi_plus():
    """
    贝尔态 |Φ⁺⟩ = (|00⟩ + |11⟩)/√2

    两粒子在z方向测量结果完全相关（同为0或同为1）
    纠缠熵 = 1 bit
    """
    ket_00, _, _, ket_11 = computational_basis()
    return (ket_00 + ket_11) / np.sqrt(2)

def bell_phi_minus():
    """
    贝尔态 |Φ⁻⟩ = (|00⟩ - |11⟩)/√2

    与|Φ⁺⟩性质类似，但有不同的相位关系
    """
    ket_00, _, _, ket_11 = computational_basis()
    return (ket_00 - ket_11) / np.sqrt(2)

def bell_psi_plus():
    """
    贝尔态 |Ψ⁺⟩ = (|01⟩ + |10⟩)/√2

    两粒子在z方向测量结果完全反相关（一个0一个1）
    """
    _, ket_01, ket_10, _ = computational_basis()
    return (ket_01 + ket_10) / np.sqrt(2)

def bell_psi_minus():
    """
    贝尔态 |Ψ⁻⟩ = (|01⟩ - |10⟩)/√2

    自旋单态（singlet state），反对称态
    在任意方向测量都完全反相关
    这是量子力学中最著名的纠缠态（EPR态）
    """
    _, ket_01, ket_10, _ = computational_basis()
    return (ket_01 - ket_10) / np.sqrt(2)


# =============================================================================
# 练习 3.3: 纠缠判据 Entanglement Criterion
#
# 物理背景:
# 判断态是否纠缠的方法:
# 1. 纠缠熵: 约化密度矩阵的冯诺依曼熵 S(ρ_A)
#    - 直积态: S = 0
#    - 最大纠缠态: S = log₂(d)（d是子系统维度）
#
# 2. 施密特分解: |ψ⟩ = Σᵢ λᵢ |aᵢ⟩|bᵢ⟩
#    - 只有一个非零λ: 直积态
#    - 多个非零λ: 纠缠态
#
# 约化密度矩阵: ρ_A = Tr_B(ρ_AB)
# =============================================================================
def partial_trace_B(rho):
    """
    对第二个子系统求偏迹 Partial trace over subsystem B

    参数 Parameters:
        rho: 4×4 两比特密度矩阵

    返回 Returns:
        rho_A: 2×2 约化密度矩阵

    公式: (ρ_A)_ij = Σ_k ρ_{ik,jk}
    对于两比特系统，索引映射: 00→0, 01→1, 10→2, 11→3
    """
    # 假设2×2子系统
    rho_A = np.zeros((2, 2), dtype=complex)
    rho_A[0, 0] = rho[0, 0] + rho[1, 1]  # ⟨0|ρ_A|0⟩ = ρ₀₀,₀₀ + ρ₀₁,₀₁
    rho_A[0, 1] = rho[0, 2] + rho[1, 3]  # ⟨0|ρ_A|1⟩
    rho_A[1, 0] = rho[2, 0] + rho[3, 1]  # ⟨1|ρ_A|0⟩
    rho_A[1, 1] = rho[2, 2] + rho[3, 3]  # ⟨1|ρ_A|1⟩
    return rho_A

def von_neumann_entropy(rho):
    """
    计算冯诺依曼熵 von Neumann entropy

    参数 Parameters:
        rho: 密度矩阵

    返回 Returns:
        S: 熵值，单位 bit（以2为底）

    公式: S = -Tr(ρ log₂ ρ) = -Σᵢ λᵢ log₂ λᵢ
    其中 λᵢ 是ρ的本征值
    """
    eigenvalues = np.linalg.eigvalsh(rho)
    eigenvalues = eigenvalues[eigenvalues > 1e-10]  # 避免 log(0)
    return -np.sum(eigenvalues * np.log2(eigenvalues))

def entanglement_entropy(state):
    """
    计算纠缠熵 Entanglement entropy

    参数 Parameters:
        state: 两比特纯态向量

    返回 Returns:
        S: 纠缠熵，单位 bit

    对于纯态，纠缠熵等于约化密度矩阵的冯诺依曼熵
    范围: [0, 1] bit（对于两比特系统）
    - S = 0: 直积态（无纠缠）
    - S = 1: 最大纠缠态（贝尔态）
    """
    rho = np.outer(state, np.conj(state))  # 构建密度矩阵
    rho_A = partial_trace_B(rho)           # 约化密度矩阵
    return von_neumann_entropy(rho_A)


# =============================================================================
# 练习 3.4: CHSH不等式 CHSH Inequality
#
# 物理背景:
# CHSH不等式是贝尔不等式的一种可实验验证的形式
# 由 Clauser, Horne, Shimony, Holt 于1969年提出
#
# 实验设置:
# - Alice和Bob各持有一个粒子
# - Alice选择测量设置 a₁ 或 a₂
# - Bob选择测量设置 b₁ 或 b₂
# - 每次测量结果为 ±1
#
# 关联函数: E(a,b) = P(同号) - P(异号)
# CHSH不等式: S = E(a₁,b₁) - E(a₁,b₂) + E(a₂,b₁) + E(a₂,b₂)
# - 局域隐变量理论: |S| ≤ 2
# - 量子力学: |S| ≤ 2√2 ≈ 2.828（奇雷尔松边界）
# =============================================================================
def pauli_z():
    """泡利σᵤ矩阵"""
    return np.array([[1, 0], [0, -1]], dtype=complex)

def pauli_x():
    """泡利σₓ矩阵"""
    return np.array([[0, 1], [1, 0]], dtype=complex)

def rotation_operator(theta):
    """
    xz平面内的自旋测量算符 Spin measurement in xz-plane

    参数 Parameters:
        theta: 测量方向与z轴的夹角，单位弧度

    返回 Returns:
        2×2 测量算符: cos(θ)σᵤ + sin(θ)σₓ

    本征值为±1，对应测量结果
    """
    return np.cos(theta) * pauli_z() + np.sin(theta) * pauli_x()

def correlation(state, A, B):
    """
    计算两粒子测量关联函数 Correlation function

    参数 Parameters:
        state: 两比特态向量
        A: Alice的测量算符（2×2矩阵）
        B: Bob的测量算符（2×2矩阵）

    返回 Returns:
        E(A,B) = ⟨ψ|A⊗B|ψ⟩，范围 [-1, 1]

    物理意义: 两粒子测量结果的乘积期望值
    """
    operator = np.kron(A, B)
    return np.real(np.vdot(state, operator @ state))

def chsh_value(state, a1, a2, b1, b2):
    """
    计算CHSH值 CHSH value

    参数 Parameters:
        state: 两比特态向量
        a1, a2: Alice的两个测量角度
        b1, b2: Bob的两个测量角度

    返回 Returns:
        S: CHSH值

    公式: S = E(a₁,b₁) - E(a₁,b₂) + E(a₂,b₁) + E(a₂,b₂)

    判据:
    - |S| ≤ 2: 可由局域隐变量理论解释
    - |S| > 2: 违背贝尔不等式，证明量子非定域性
    """
    A1 = rotation_operator(a1)
    A2 = rotation_operator(a2)
    B1 = rotation_operator(b1)
    B2 = rotation_operator(b2)

    # TODO: 计算CHSH值（四个关联函数的组合）
    S = (correlation(state, A1, B1) - correlation(state, A1, B2) +
         correlation(state, A2, B1) + correlation(state, A2, B2))
    return S


# =============================================================================
# 练习 3.5: 最大违背 Maximum Violation
#
# 物理背景:
# 量子力学预言的最大CHSH值为 2√2 ≈ 2.828
# 这个值称为奇雷尔松边界 (Tsirelson bound)
#
# 最优测量角度（对于|Φ⁺⟩态）:
# - Alice: a₁ = 0, a₂ = π/2
# - Bob: b₁ = π/4, b₂ = -π/4
# 这样每个关联函数都贡献 cos(π/4) = 1/√2
# =============================================================================
def optimal_chsh_angles():
    """
    返回最大违背CHSH不等式的测量角度 Optimal CHSH angles

    返回 Returns:
        (a1, a2, b1, b2): 四个测量角度

    对于|Φ⁺⟩态，这些角度给出 S = 2√2
    角度选择使得相邻测量方向夹角都是π/4
    """
    return 0, np.pi/2, np.pi/4, -np.pi/4

def maximum_chsh_violation():
    """
    量子力学允许的CHSH最大值 Maximum quantum CHSH value

    返回 Returns:
        2√2 ≈ 2.828

    这是量子力学的理论极限（奇雷尔松边界）
    超过此值需要违反相对论（超光速信号传递）
    """
    return 2 * np.sqrt(2)


# =============================================================================
# 练习 3.6: 量子隐形传态 Quantum Teleportation
#
# 物理背景:
# 量子隐形传态利用纠缠和经典通信传递量子态
# 由 Bennett 等人于1993年提出
#
# 协议步骤:
# 1. Alice和Bob预先共享贝尔态 |Φ⁺⟩_23
# 2. Alice持有要传送的未知态 |ψ⟩_1 = α|0⟩ + β|1⟩
# 3. Alice对粒子1和2进行贝尔测量，得到2比特经典信息
# 4. Alice将测量结果通过经典信道告诉Bob
# 5. Bob根据收到的信息对粒子3施加相应酉变换
#
# 重要性质:
# - 不违反相对论（需要经典通信）
# - 原态在传送过程中被破坏（不可克隆定理）
# - 是量子密钥分发和量子网络的基础
# =============================================================================
def teleportation_protocol(state_to_send, shared_bell_state=None):
    """
    量子隐形传态协议描述 Quantum teleportation protocol

    参数 Parameters:
        state_to_send: 要传送的未知量子态 |ψ⟩ = α|0⟩ + β|1⟩
        shared_bell_state: Alice和Bob共享的纠缠态（默认|Φ⁺⟩）

    返回 Returns:
        协议描述字符串

    Bob的修正操作（取决于Alice的贝尔测量结果）:
    - 测量结果 00: 施加 I（不变）
    - 测量结果 01: 施加 X（比特翻转）
    - 测量结果 10: 施加 Z（相位翻转）
    - 测量结果 11: 施加 ZX
    """
    if shared_bell_state is None:
        shared_bell_state = bell_phi_plus()

    # 三量子比特态: |ψ⟩₁ ⊗ |Φ⁺⟩₂₃
    # Alice对粒子1和2做贝尔基测量
    # Bob根据经典信息对粒子3做修正

    return "协议: Alice进行贝尔基测量，发送2比特经典信息，Bob施加相应修正操作"


# =============================================================================
# 可视化 Visualization
# 绘制CHSH值、纠缠熵、关联函数等图像
# =============================================================================
def plot_entanglement():
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. CHSH值vs角度
    ax1 = axes[0, 0]
    theta_range = np.linspace(0, np.pi, 100)
    bell_state = bell_phi_plus()

    S_values = []
    for theta in theta_range:
        S = chsh_value(bell_state, 0, np.pi/2, theta, theta - np.pi/2)
        S_values.append(S)

    ax1.plot(np.degrees(theta_range), S_values, 'b-', linewidth=2)
    ax1.axhline(y=2, color='r', linestyle='--', label='Classical limit')
    ax1.axhline(y=2*np.sqrt(2), color='g', linestyle='--', label='Quantum limit')
    ax1.set_xlabel('θ (degrees)')
    ax1.set_ylabel('CHSH value S')
    ax1.set_title('CHSH值随测量角度变化')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 纠缠熵
    ax2 = axes[0, 1]
    # 参数化态 |ψ⟩ = cos(θ)|00⟩ + sin(θ)|11⟩
    theta_ent = np.linspace(0, np.pi/2, 100)
    ket_00, _, _, ket_11 = computational_basis()

    entropy_values = []
    for theta in theta_ent:
        state = np.cos(theta) * ket_00 + np.sin(theta) * ket_11
        S = entanglement_entropy(state)
        entropy_values.append(S)

    ax2.plot(np.degrees(theta_ent), entropy_values, 'r-', linewidth=2)
    ax2.axhline(y=1, color='g', linestyle='--', label='Max (Bell state)')
    ax2.set_xlabel('θ (degrees)')
    ax2.set_ylabel('Entanglement entropy (bits)')
    ax2.set_title('纠缠熵 vs 态参数')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 贝尔态关联
    ax3 = axes[1, 0]
    states = {
        '|Φ⁺⟩': bell_phi_plus(),
        '|Φ⁻⟩': bell_phi_minus(),
        '|Ψ⁺⟩': bell_psi_plus(),
        '|Ψ⁻⟩': bell_psi_minus()
    }

    theta_b = np.linspace(0, 2*np.pi, 100)
    for name, state in states.items():
        corr = [correlation(state, pauli_z(), rotation_operator(t)) for t in theta_b]
        ax3.plot(np.degrees(theta_b), corr, label=name, linewidth=2)

    ax3.set_xlabel('θ_B (degrees)')
    ax3.set_ylabel('Correlation E(Z, θ_B)')
    ax3.set_title('贝尔态的关联函数')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 乘积态vs纠缠态
    ax4 = axes[1, 1]
    # 乘积态 |++⟩
    ket_plus = np.array([1, 1], dtype=complex) / np.sqrt(2)
    product_state = tensor_product(ket_plus, ket_plus)

    S_product = []
    S_entangled = []
    for theta in theta_range:
        S_p = chsh_value(product_state, 0, np.pi/2, theta, theta - np.pi/2)
        S_e = chsh_value(bell_state, 0, np.pi/2, theta, theta - np.pi/2)
        S_product.append(S_p)
        S_entangled.append(S_e)

    ax4.plot(np.degrees(theta_range), S_product, 'b-', label='Product state', linewidth=2)
    ax4.plot(np.degrees(theta_range), S_entangled, 'r-', label='Bell state', linewidth=2)
    ax4.axhline(y=2, color='k', linestyle='--', alpha=0.5)
    ax4.set_xlabel('θ (degrees)')
    ax4.set_ylabel('CHSH value S')
    ax4.set_title('乘积态vs纠缠态')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('entanglement.png', dpi=150)
    print("图像已保存为 entanglement.png")
    plt.show()


def verify():
    """验证所有练习的正确性 Verify all exercises"""
    all_passed = True

    # 检查 3.1: 计算基
    ket_00, ket_01, ket_10, ket_11 = computational_basis()
    if not np.isclose(np.linalg.norm(ket_00), 1):
        print("错误 3.1: 计算基未归一化，请检查张量积计算")
        all_passed = False
    else:
        print("通过 3.1: 两比特计算基正确")

    # 检查 3.2: 贝尔态
    phi_plus = bell_phi_plus()
    if not np.isclose(np.linalg.norm(phi_plus), 1):
        print("错误 3.2: 贝尔态未归一化，请检查归一化因子")
        all_passed = False
    else:
        print("通过 3.2: 贝尔态构造正确")

    # 检查 3.3: 纠缠熵
    S_ent = entanglement_entropy(phi_plus)
    if not np.isclose(S_ent, 1, rtol=0.01):
        print(f"错误 3.3: 贝尔态纠缠熵应为1 bit（最大纠缠），得到 {S_ent:.3f}")
        all_passed = False
    else:
        print(f"通过 3.3: 纠缠熵正确 (贝尔态: S = {S_ent:.3f} bit)")

    # 检查 3.4: CHSH不等式
    a1, a2, b1, b2 = optimal_chsh_angles()
    S = chsh_value(phi_plus, a1, a2, b1, b2)
    if not np.isclose(abs(S), 2*np.sqrt(2), rtol=0.01):
        print(f"错误 3.4: CHSH值 {S:.3f} 不等于理论值 ±2√2")
        all_passed = False
    else:
        print(f"通过 3.4: CHSH不等式正确 (S = {S:.3f}，违背经典极限2)")

    # 检查 3.5: 最大违背
    max_viol = maximum_chsh_violation()
    if not np.isclose(max_viol, 2.828, rtol=0.01):
        print("错误 3.5: 奇雷尔松边界值计算错误")
        all_passed = False
    else:
        print(f"通过 3.5: 量子最大违背 = 2√2 ≈ {max_viol:.3f}")

    if all_passed:
        print("\n所有测试通过！")
        try:
            plot_entanglement()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("量子纠缠与贝尔不等式 Entanglement & Bell")
    print("=" * 50)
    verify()
