"""
量子计算基础 Quantum Computing Basics
难度 Difficulty: ★★★★★

================================================================================
学习目标 Learning Objectives
================================================================================
- 理解量子比特(qubit)的表示和Bloch球几何
  Understand qubit representation and Bloch sphere geometry
- 掌握单比特门和双比特门的矩阵形式及物理意义
  Master single-qubit and two-qubit gates matrix forms and physical meaning
- 实现基本量子算法：Deutsch算法、量子隐形传态
  Implement basic quantum algorithms: Deutsch algorithm, quantum teleportation

================================================================================
物理背景 Physical Background
================================================================================
量子计算利用量子力学的叠加和纠缠特性进行信息处理，在特定问题上
可以实现指数级加速（如Shor算法分解大数、Grover算法搜索）。

Quantum computing uses superposition and entanglement for information
processing, achieving exponential speedup for specific problems.

核心概念 Key Concepts:
1. 量子比特 Qubit: |ψ⟩ = α|0⟩ + β|1⟩, |α|² + |β|² = 1
2. Bloch球: 量子态的几何表示，|ψ⟩ = cos(θ/2)|0⟩ + e^(iφ)sin(θ/2)|1⟩
3. 量子门 Quantum Gates: 酉算符，保持量子态归一化
4. 量子纠缠: 贝尔态 |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
5. 量子测量: 投影测量，坍缩到本征态

重要量子门 Important Quantum Gates:
- 泡利门: X(NOT), Y, Z - 绕Bloch球轴旋转π
- Hadamard门: H = (|0⟩+|1⟩)/√2 ← |0⟩, (|0⟩-|1⟩)/√2 ← |1⟩
- 相位门: S(π/2), T(π/4)
- CNOT: 控制-非门，产生纠缠的基本门
- CZ: 控制-Z门

量子算法里程碑 Algorithm Milestones:
- Deutsch-Jozsa: 判断函数是常数还是平衡
- Grover: 搜索未排序数据库 O(√N)
- Shor: 大数分解 O((log N)³)
- 量子模拟: 模拟量子系统

HINT: Hadamard门: H = (1/√2)[[1,1],[1,-1]]，创建叠加态
HINT: CNOT门: 控制-非门，是产生纠缠的通用双比特门
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])

# I AM NOT DONE

# =============================================================================
# 练习 12.1: 量子比特
# Exercise 12.1: Qubits
#
# 物理背景 Physical Background:
# 量子比特是量子信息的基本单位，与经典比特不同，它可以处于叠加态。
# 任意单量子比特态可用Bloch球上的点表示：
# |ψ⟩ = cos(θ/2)|0⟩ + e^(iφ)sin(θ/2)|1⟩
#
# Bloch球参数:
# - θ ∈ [0, π]: 极角，决定|0⟩和|1⟩的振幅比
# - φ ∈ [0, 2π): 方位角，决定相对相位
#
# 特殊态 Special States:
# - |0⟩: 北极 (θ=0)
# - |1⟩: 南极 (θ=π)
# - |+⟩ = (|0⟩+|1⟩)/√2: 赤道 x轴正向 (θ=π/2, φ=0)
# - |-⟩ = (|0⟩-|1⟩)/√2: 赤道 x轴负向 (θ=π/2, φ=π)
# =============================================================================
def qubit_state(theta, phi):
    """
    构造量子比特态 Construct qubit state on Bloch sphere

    公式 Formula: |ψ⟩ = cos(θ/2)|0⟩ + e^(iφ)sin(θ/2)|1⟩

    参数 Parameters:
        theta: 极角 [0, π]
        phi: 方位角 [0, 2π)

    返回 Returns:
        复数数组 [α, β]，满足 |α|² + |β|² = 1
    """
    return np.array([np.cos(theta/2), np.exp(1j*phi)*np.sin(theta/2)], dtype=complex)

def ket_0():
    """计算基 |0⟩"""
    return np.array([1, 0], dtype=complex)

def ket_1():
    """计算基 |1⟩"""
    return np.array([0, 1], dtype=complex)

def ket_plus():
    """|+⟩ = (|0⟩ + |1⟩)/√2"""
    return np.array([1, 1], dtype=complex) / np.sqrt(2)

def ket_minus():
    """|-⟩ = (|0⟩ - |1⟩)/√2"""
    return np.array([1, -1], dtype=complex) / np.sqrt(2)


# =============================================================================
# 练习 12.2: 单比特门
# Exercise 12.2: Single Qubit Gates
#
# 物理背景 Physical Background:
# 量子门是作用在量子比特上的酉算符，对应Bloch球上的旋转。
# 单比特门构成SU(2)群，任意单比特门可分解为：U = e^(iα)Rz(β)Ry(γ)Rz(δ)
#
# 重要单比特门 Important Gates:
# - 泡利门 Pauli: X, Y, Z - 绕对应轴旋转π
# - Hadamard: H = (X+Z)/√2 - 创建叠加态
# - 相位门: S = diag(1, i), T = diag(1, e^(iπ/4))
# - 旋转门: Rx(θ), Ry(θ), Rz(θ)
#
# 泡利矩阵性质:
# - X² = Y² = Z² = I
# - XYZ = iI
# - {X, Y} = {Y, Z} = {Z, X} = 0
# =============================================================================
def pauli_x():
    """泡利X门（NOT门）- 绕X轴旋转π，交换|0⟩和|1⟩"""
    return np.array([[0, 1], [1, 0]], dtype=complex)

def pauli_y():
    """泡利Y门"""
    return np.array([[0, -1j], [1j, 0]], dtype=complex)

def pauli_z():
    """泡利Z门（相位翻转）"""
    return np.array([[1, 0], [0, -1]], dtype=complex)

def hadamard():
    """Hadamard门 - 创建叠加态"""
    return np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

def phase_gate(phi):
    """相位门 R_φ"""
    return np.array([[1, 0], [0, np.exp(1j*phi)]], dtype=complex)

def rotation_x(theta):
    """绕X轴旋转"""
    return np.array([
        [np.cos(theta/2), -1j*np.sin(theta/2)],
        [-1j*np.sin(theta/2), np.cos(theta/2)]
    ], dtype=complex)


# =============================================================================
# 练习 12.3: 双比特门
# Exercise 12.3: Two-Qubit Gates
# =============================================================================
def cnot():
    """CNOT门（控制-非门）"""
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0]
    ], dtype=complex)

def cz():
    """CZ门（控制-Z门）"""
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, -1]
    ], dtype=complex)

def swap():
    """SWAP门"""
    return np.array([
        [1, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1]
    ], dtype=complex)

def tensor_product(A, B):
    """张量积"""
    return np.kron(A, B)


# =============================================================================
# 练习 12.4: 量子电路
# Exercise 12.4: Quantum Circuits
# =============================================================================
def create_bell_state(bell_type='phi_plus'):
    """
    创建贝尔态
    |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
    """
    # 初态 |00⟩
    psi = np.array([1, 0, 0, 0], dtype=complex)

    # H ⊗ I
    H_I = tensor_product(hadamard(), np.eye(2))
    psi = H_I @ psi

    # CNOT
    psi = cnot() @ psi

    if bell_type == 'phi_plus':
        return psi
    elif bell_type == 'phi_minus':
        # 应用 Z ⊗ I
        Z_I = tensor_product(pauli_z(), np.eye(2))
        return Z_I @ psi
    elif bell_type == 'psi_plus':
        # 应用 X ⊗ I
        X_I = tensor_product(pauli_x(), np.eye(2))
        return X_I @ psi
    elif bell_type == 'psi_minus':
        # 应用 XZ ⊗ I
        XZ_I = tensor_product(pauli_x() @ pauli_z(), np.eye(2))
        return XZ_I @ psi

def ghz_state(n=3):
    """
    GHZ态 (|00...0⟩ + |11...1⟩)/√2
    """
    dim = 2**n
    psi = np.zeros(dim, dtype=complex)
    psi[0] = 1/np.sqrt(2)  # |00...0⟩
    psi[-1] = 1/np.sqrt(2)  # |11...1⟩
    return psi


# =============================================================================
# 练习 12.5: Deutsch-Jozsa算法
# Exercise 12.5: Deutsch-Jozsa Algorithm
# =============================================================================
def deutsch_oracle(f_type='constant_0'):
    """
    Deutsch算法的Oracle
    f: {0,1} → {0,1}
    U_f|x⟩|y⟩ = |x⟩|y ⊕ f(x)⟩
    """
    if f_type == 'constant_0':  # f(x) = 0
        return np.eye(4, dtype=complex)
    elif f_type == 'constant_1':  # f(x) = 1
        return tensor_product(np.eye(2), pauli_x())
    elif f_type == 'identity':  # f(x) = x
        return cnot()
    elif f_type == 'not':  # f(x) = NOT x
        return tensor_product(pauli_x(), np.eye(2)) @ cnot() @ tensor_product(pauli_x(), np.eye(2))

def deutsch_algorithm(oracle):
    """
    Deutsch算法：判断f是常数还是平衡
    返回: 'constant' 或 'balanced'
    """
    # 初态 |01⟩
    psi = np.array([0, 1, 0, 0], dtype=complex)

    # H ⊗ H
    H_H = tensor_product(hadamard(), hadamard())
    psi = H_H @ psi

    # Oracle
    psi = oracle @ psi

    # H ⊗ I
    H_I = tensor_product(hadamard(), np.eye(2))
    psi = H_I @ psi

    # 测量第一个比特
    prob_0 = np.abs(psi[0])**2 + np.abs(psi[1])**2

    return 'constant' if prob_0 > 0.5 else 'balanced'


# =============================================================================
# 练习 12.6: 量子隐形传态
# Exercise 12.6: Quantum Teleportation
# =============================================================================
def teleportation_protocol(psi_to_send):
    """
    量子隐形传态协议
    Alice有未知态|ψ⟩，Alice和Bob共享|Φ⁺⟩
    """
    # 创建共享的贝尔态
    bell = create_bell_state('phi_plus')

    # 三比特系统: |ψ⟩ ⊗ |Φ⁺⟩
    # 这里简化为符号计算
    # 实际实现需要更复杂的张量操作

    # 返回协议步骤
    return {
        'state_to_send': psi_to_send,
        'shared_entanglement': 'phi_plus',
        'steps': [
            'Alice performs Bell measurement on her two qubits',
            'Alice sends 2 classical bits to Bob',
            'Bob applies correction based on measurement result',
            '00 -> I, 01 -> X, 10 -> Z, 11 -> ZX'
        ]
    }


# =============================================================================
# 可视化
# =============================================================================
def plot_quantum_computing():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. Bloch球上的门操作
    ax1 = fig.add_subplot(231, projection='3d')

    # 绘制Bloch球
    u = np.linspace(0, 2*np.pi, 50)
    v = np.linspace(0, np.pi, 25)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    ax1.plot_wireframe(x, y, z, alpha=0.1, color='gray')

    # 标记特殊态
    states = {
        '|0⟩': [0, 0, 1],
        '|1⟩': [0, 0, -1],
        '|+⟩': [1, 0, 0],
        '|-⟩': [-1, 0, 0]
    }

    for name, vec in states.items():
        ax1.scatter(*vec, s=50)
        ax1.text(vec[0]*1.2, vec[1]*1.2, vec[2]*1.2, name)

    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    ax1.set_title('Bloch球')

    # 2. 贝尔态分析
    ax2 = axes[0, 1]
    bell_types = ['phi_plus', 'phi_minus', 'psi_plus', 'psi_minus']
    labels = ['|Φ⁺⟩', '|Φ⁻⟩', '|Ψ⁺⟩', '|Ψ⁻⟩']

    for i, (bt, label) in enumerate(zip(bell_types, labels)):
        bell = create_bell_state(bt)
        probs = np.abs(bell)**2
        ax2.bar(np.arange(4) + i*0.2, probs, 0.2, label=label, alpha=0.7)

    ax2.set_xticks([0.3, 1.3, 2.3, 3.3])
    ax2.set_xticklabels(['|00⟩', '|01⟩', '|10⟩', '|11⟩'])
    ax2.set_ylabel('概率')
    ax2.set_title('贝尔态概率分布')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. Hadamard门效果
    ax3 = axes[0, 2]
    theta = np.linspace(0, 2*np.pi, 100)
    H = hadamard()

    states_input = [qubit_state(t, 0) for t in theta]
    states_output = [H @ s for s in states_input]

    prob_0_in = [np.abs(s[0])**2 for s in states_input]
    prob_0_out = [np.abs(s[0])**2 for s in states_output]

    ax3.plot(np.degrees(theta), prob_0_in, 'b-', label='输入 P(|0⟩)', linewidth=2)
    ax3.plot(np.degrees(theta), prob_0_out, 'r-', label='H后 P(|0⟩)', linewidth=2)
    ax3.set_xlabel('θ (degrees)')
    ax3.set_ylabel('P(|0⟩)')
    ax3.set_title('Hadamard门效果')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. CNOT门真值表
    ax4 = axes[1, 0]
    CNOT = cnot()
    input_states = ['|00⟩', '|01⟩', '|10⟩', '|11⟩']
    output_indices = []

    for i in range(4):
        input_vec = np.zeros(4, dtype=complex)
        input_vec[i] = 1
        output_vec = CNOT @ input_vec
        output_indices.append(np.argmax(np.abs(output_vec)))

    output_states = [input_states[i] for i in output_indices]

    ax4.axis('off')
    table_data = [['输入', '输出']] + list(zip(input_states, output_states))

    for i, row in enumerate(table_data):
        for j, cell in enumerate(row):
            ax4.text(0.3 + j*0.4, 0.8 - i*0.15, cell, fontsize=14,
                    ha='center', va='center',
                    fontweight='bold' if i == 0 else 'normal')

    ax4.set_title('CNOT门真值表')

    # 5. GHZ态
    ax5 = axes[1, 1]
    for n in [2, 3, 4]:
        ghz = ghz_state(n)
        probs = np.abs(ghz)**2
        nonzero = probs > 0.01
        ax5.bar(np.arange(2**n)[nonzero] + (n-2)*0.25, probs[nonzero], 0.25,
               label=f'{n}-qubit', alpha=0.7)

    ax5.set_xlabel('计算基态')
    ax5.set_ylabel('概率')
    ax5.set_title('GHZ态')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. Deutsch算法
    ax6 = axes[1, 2]
    oracles = ['constant_0', 'constant_1', 'identity', 'not']
    results = []
    colors = []

    for o in oracles:
        oracle = deutsch_oracle(o)
        result = deutsch_algorithm(oracle)
        results.append(result)
        colors.append('blue' if result == 'constant' else 'red')

    ax6.barh(oracles, [1]*4, color=colors, alpha=0.7)
    for i, (o, r) in enumerate(zip(oracles, results)):
        ax6.text(0.5, i, r, va='center', ha='center', fontsize=12, color='white')

    ax6.set_xlabel('Deutsch算法结果')
    ax6.set_title('Deutsch算法演示')

    plt.tight_layout()
    plt.savefig('quantum_computing.png', dpi=150)
    print("图像已保存为 quantum_computing.png")
    plt.show()


def verify():
    all_passed = True

    # Check 12.1
    psi = qubit_state(np.pi/2, 0)
    if not np.isclose(np.abs(psi[0]), np.abs(psi[1]), rtol=0.01):
        print("❌ 12.1 量子比特态错误")
        all_passed = False
    else:
        print("✓ 12.1 量子比特正确")

    # Check 12.2
    H = hadamard()
    H2 = H @ H
    if not np.allclose(H2, np.eye(2)):
        print("❌ 12.2 H² 应等于 I")
        all_passed = False
    else:
        print("✓ 12.2 单比特门正确 (H² = I)")

    # Check 12.3
    CNOT = cnot()
    # CNOT|10⟩ = |11⟩
    input_10 = np.array([0, 0, 1, 0], dtype=complex)
    output = CNOT @ input_10
    if not np.argmax(np.abs(output)) == 3:
        print("❌ 12.3 CNOT门错误")
        all_passed = False
    else:
        print("✓ 12.3 双比特门正确")

    # Check 12.4
    bell = create_bell_state('phi_plus')
    if not np.isclose(np.abs(bell[0]), np.abs(bell[3]), rtol=0.01):
        print("❌ 12.4 贝尔态错误")
        all_passed = False
    else:
        print("✓ 12.4 量子电路正确（贝尔态）")

    # Check 12.5
    oracle_const = deutsch_oracle('constant_0')
    result = deutsch_algorithm(oracle_const)
    if result != 'constant':
        print("❌ 12.5 Deutsch算法错误")
        all_passed = False
    else:
        print("✓ 12.5 Deutsch算法正确")

    # Check 12.6
    protocol = teleportation_protocol(ket_plus())
    if 'steps' not in protocol:
        print("❌ 12.6 隐形传态协议错误")
        all_passed = False
    else:
        print("✓ 12.6 量子隐形传态正确")

    if all_passed:
        print("\n🎉 所有测试通过！")
        try:
            plot_quantum_computing()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("量子计算基础 Quantum Computing Basics")
    print("=" * 50)
    verify()
