"""
自旋与泡利矩阵 Spin and Pauli Matrices
难度 Difficulty: ★★★★★

学习目标 Learning Objectives:
- 理解电子自旋的量子力学描述（自旋是粒子的内禀角动量，无经典对应）
- 掌握泡利矩阵的数学性质和物理意义
- 分析自旋测量和斯特恩-盖拉赫实验的量子行为
- 理解布洛赫球表示和自旋进动

物理背景 Physical Background:
1. 自旋是量子力学特有的概念，电子自旋量子数 s = 1/2
2. 自旋角动量 S = (ℏ/2)σ，其中 σ 是泡利矩阵向量
3. 自旋在任意方向的测量只能得到 ±ℏ/2 两个值
4. 布洛赫球提供了二能级系统的几何表示
5. 拉莫尔进动描述自旋在磁场中的运动，角频率 ω = γB

关键公式 Key Formulas:
- 泡利矩阵反对易关系: {σᵢ, σⱼ} = 2δᵢⱼI
- 泡利矩阵对易关系: [σᵢ, σⱼ] = 2iεᵢⱼₖσₖ
- 自旋期望值: ⟨S⟩ = (ℏ/2)⟨σ⟩
- 布洛赫球参数化: |ψ⟩ = cos(θ/2)|↑⟩ + e^(iφ)sin(θ/2)|↓⟩
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import hbar

# I AM NOT DONE

# =============================================================================
# 练习 1.1: 泡利矩阵 Pauli Matrices
#
# 物理背景:
# 泡利矩阵是描述自旋-1/2粒子的基本工具，它们是2×2厄米矩阵
# 满足 σᵢ² = I（幺正性）和特殊的对易/反对易关系
#
# 三个泡利矩阵:
#   σₓ = |0 1|    σᵧ = |0 -i|    σᵤ = |1  0|
#       |1 0|        |i  0|        |0 -1|
#
# 本征值都是 ±1，对应自旋测量的 ±ℏ/2
# =============================================================================
def pauli_x():
    """
    泡利 σₓ 矩阵 Pauli sigma-x matrix

    本征值: +1 对应 |+x⟩，-1 对应 |-x⟩
    物理意义: 对应 x 方向自旋测量算符
    """
    return np.array([[0, 1], [1, 0]], dtype=complex)

def pauli_y():
    """
    泡利 σᵧ 矩阵 Pauli sigma-y matrix

    本征值: +1 对应 |+y⟩，-1 对应 |-y⟩
    物理意义: 对应 y 方向自旋测量算符
    """
    return np.array([[0, -1j], [1j, 0]], dtype=complex)

def pauli_z():
    """
    泡利 σᵤ 矩阵 Pauli sigma-z matrix

    本征值: +1 对应 |↑⟩，-1 对应 |↓⟩
    物理意义: 对应 z 方向自旋测量算符（通常选为对角基）
    """
    return np.array([[1, 0], [0, -1]], dtype=complex)

def spin_operator(direction):
    """
    自旋算符 Spin operator: S = (ℏ/2)σ

    参数 Parameters:
        direction: 'x', 'y', or 'z' - 自旋方向

    返回 Returns:
        S: 2×2 自旋算符矩阵，单位为 J·s

    物理意义: 自旋算符的本征值为 ±ℏ/2 ≈ ±5.27×10⁻³⁵ J·s
    """
    if direction == 'x':
        sigma = pauli_x()
    elif direction == 'y':
        sigma = pauli_y()
    else:
        sigma = pauli_z()
    return (hbar / 2) * sigma


# =============================================================================
# 练习 1.2: 自旋态 Spin States
#
# 物理背景:
# 自旋态是二维复希尔伯特空间中的向量，通常用 |↑⟩ 和 |↓⟩ 作为基
# 任意自旋态可以写成: |ψ⟩ = α|↑⟩ + β|↓⟩，其中 |α|² + |β|² = 1
#
# 斯特恩-盖拉赫实验:
# 银原子束通过非均匀磁场时分裂成两束，证明了自旋的量子化
# =============================================================================
def spin_up():
    """
    自旋向上态 Spin-up state: |↑⟩ = |+z⟩

    这是 σᵤ 的本征态，本征值为 +1
    在 z 方向测量必得 +ℏ/2
    """
    return np.array([1, 0], dtype=complex)

def spin_down():
    """
    自旋向下态 Spin-down state: |↓⟩ = |-z⟩

    这是 σᵤ 的本征态，本征值为 -1
    在 z 方向测量必得 -ℏ/2
    """
    return np.array([0, 1], dtype=complex)

def spin_plus_x():
    """
    x方向自旋向上态: |+x⟩ = (|↑⟩ + |↓⟩)/√2

    这是 σₓ 的本征态，本征值为 +1
    在 z 方向测量得 ±ℏ/2 的概率各为 50%
    """
    return np.array([1, 1], dtype=complex) / np.sqrt(2)

def spin_minus_x():
    """
    x方向自旋向下态: |-x⟩ = (|↑⟩ - |↓⟩)/√2

    这是 σₓ 的本征态，本征值为 -1
    在 z 方向测量得 ±ℏ/2 的概率各为 50%
    """
    return np.array([1, -1], dtype=complex) / np.sqrt(2)


# =============================================================================
# 练习 1.3: 测量概率 Measurement Probability
#
# 物理背景:
# 量子测量遵循玻恩规则 (Born's rule):
# 测量得到本征值 aₙ 的概率 P(aₙ) = |⟨aₙ|ψ⟩|²
#
# 对于自旋测量:
# - 沿任意方向 n̂ 测量，只能得到 ±ℏ/2
# - 测量后态坍缩到对应的本征态
# =============================================================================
def measurement_probability(state, eigenstate):
    """
    计算测量得到特定本征态的概率 Measurement probability

    参数 Parameters:
        state: 当前量子态 |ψ⟩
        eigenstate: 目标本征态 |aₙ⟩

    返回 Returns:
        probability: 概率 P = |⟨aₙ|ψ⟩|²，范围 [0, 1]

    公式: P = |⟨eigenstate|state⟩|² (玻恩规则)
    """
    state = np.array(state, dtype=complex)
    eigenstate = np.array(eigenstate, dtype=complex)
    # TODO: 计算概率（使用内积的模方）
    # 提示: np.vdot 计算复共轭内积，np.abs 取模
    amplitude = np.vdot(eigenstate, state)  # 内积 ⟨eigenstate|state⟩
    probability = np.abs(amplitude)**2
    return probability

def expectation_value_spin(state, direction):
    """
    计算自旋期望值 Spin expectation value: ⟨S⟩ = ⟨ψ|S|ψ⟩

    参数 Parameters:
        state: 自旋态 |ψ⟩
        direction: 'x', 'y', 'z' - 测量方向

    返回 Returns:
        exp_val: 期望值，单位 J·s，范围 [-ℏ/2, +ℏ/2]

    物理意义: 多次测量结果的统计平均
    """
    S = spin_operator(direction)
    state = np.array(state, dtype=complex)
    # TODO: 计算期望值 ⟨ψ|S|ψ⟩
    # 提示: 先计算 S|ψ⟩，再与 |ψ⟩ 做内积
    exp_val = np.vdot(state, S @ state)
    return np.real(exp_val)


# =============================================================================
# 练习 1.4: 泡利矩阵的性质 Properties of Pauli Matrices
#
# 重要代数关系:
# 1. 反对易关系: {σᵢ, σⱼ} = σᵢσⱼ + σⱼσᵢ = 2δᵢⱼI
#    - 当 i=j 时，{σᵢ, σᵢ} = 2σᵢ² = 2I
#    - 当 i≠j 时，{σᵢ, σⱼ} = 0（反对易）
#
# 2. 对易关系: [σᵢ, σⱼ] = 2iεᵢⱼₖσₖ
#    - [σₓ, σᵧ] = 2iσᵤ
#    - [σᵧ, σᵤ] = 2iσₓ
#    - [σᵤ, σₓ] = 2iσᵧ
#
# 这些关系是 SU(2) 李代数的基础
# =============================================================================
def verify_anticommutation(sigma_i, sigma_j):
    """
    验证反对易关系 Verify anticommutation relation

    计算反对易子: {σᵢ, σⱼ} = σᵢσⱼ + σⱼσᵢ

    期望结果:
    - i = j 时: 返回 2I（单位矩阵的两倍）
    - i ≠ j 时: 返回零矩阵
    """
    anticomm = sigma_i @ sigma_j + sigma_j @ sigma_i
    return anticomm

def verify_commutation(sigma_i, sigma_j):
    """
    验证对易关系 Verify commutation relation

    计算对易子: [σᵢ, σⱼ] = σᵢσⱼ - σⱼσᵢ

    期望结果: [σᵢ, σⱼ] = 2iεᵢⱼₖσₖ
    例如: [σₓ, σᵧ] = 2iσᵤ
    """
    comm = sigma_i @ sigma_j - sigma_j @ sigma_i
    return comm

def pauli_square():
    """
    验证泡利矩阵平方等于单位阵 Verify σᵢ² = I

    这是泡利矩阵的幺正性质，每个泡利矩阵都是其自身的逆
    """
    I = np.eye(2, dtype=complex)
    sx, sy, sz = pauli_x(), pauli_y(), pauli_z()
    return np.allclose(sx @ sx, I) and np.allclose(sy @ sy, I) and np.allclose(sz @ sz, I)


# =============================================================================
# 练习 1.5: 布洛赫球 Bloch Sphere
#
# 物理背景:
# 布洛赫球是纯自旋态的几何表示，球面上的每个点对应一个自旋态
#
# 参数化:
#   |ψ⟩ = cos(θ/2)|↑⟩ + e^(iφ)sin(θ/2)|↓⟩
#   - θ: 极角（0到π），θ=0 对应 |↑⟩，θ=π 对应 |↓⟩
#   - φ: 方位角（0到2π），决定赤道平面上的位置
#
# 布洛赫矢量:
#   r⃗ = (⟨σₓ⟩, ⟨σᵧ⟩, ⟨σᵤ⟩) = (sinθcosφ, sinθsinφ, cosθ)
#   纯态位于球面 |r⃗| = 1，混合态位于球内 |r⃗| < 1
# =============================================================================
def state_to_bloch(state):
    """
    将自旋态转换为布洛赫球坐标 State to Bloch coordinates

    参数 Parameters:
        state: 二分量自旋态向量

    返回 Returns:
        (theta, phi): 布洛赫球坐标
            theta: 极角 [0, π]，单位弧度
            phi: 方位角 [0, 2π]，单位弧度
    """
    state = np.array(state, dtype=complex)
    state = state / np.linalg.norm(state)  # 归一化

    # θ 由 |α| = cos(θ/2) 决定
    theta = 2 * np.arccos(np.abs(state[0]))
    # φ 是两个分量相位差
    if np.abs(state[1]) < 1e-10:
        phi = 0
    else:
        phi = np.angle(state[1]) - np.angle(state[0])

    return theta, phi

def bloch_to_state(theta, phi):
    """
    从布洛赫球坐标构建自旋态 Bloch coordinates to state

    参数 Parameters:
        theta: 极角，范围 [0, π]，单位弧度
        phi: 方位角，范围 [0, 2π]，单位弧度

    返回 Returns:
        state: 归一化的自旋态向量

    公式: |ψ⟩ = cos(θ/2)|↑⟩ + e^(iφ)sin(θ/2)|↓⟩
    """
    # TODO: 根据布洛赫球参数化公式构建量子态
    state = np.array([
        np.cos(theta / 2),
        np.exp(1j * phi) * np.sin(theta / 2)
    ], dtype=complex)
    return state

def bloch_vector(state):
    """
    计算布洛赫矢量 Bloch vector: r⃗ = (⟨σₓ⟩, ⟨σᵧ⟩, ⟨σᵤ⟩)

    参数 Parameters:
        state: 自旋态向量

    返回 Returns:
        vec: 三维布洛赫矢量，纯态时 |vec| = 1

    物理意义: 布洛赫矢量指向自旋极化方向
    """
    state = np.array(state, dtype=complex)
    sx = np.real(np.vdot(state, pauli_x() @ state))
    sy = np.real(np.vdot(state, pauli_y() @ state))
    sz = np.real(np.vdot(state, pauli_z() @ state))
    return np.array([sx, sy, sz])


# =============================================================================
# 练习 1.6: 自旋进动 Spin Precession
#
# 物理背景:
# 自旋在磁场中的运动称为拉莫尔进动 (Larmor precession)
#
# 哈密顿量: H = -γS⃗·B⃗ = -μ⃗·B⃗
#   - γ: 旋磁比 (gyromagnetic ratio)
#   - 电子: γₑ ≈ 1.76×10¹¹ rad/(s·T)
#   - μ⃗ = γS⃗: 磁矩
#
# 拉莫尔频率: ω_L = γB
#   - 自旋绕磁场方向进动，周期 T = 2π/ω_L
#
# 时间演化算符: U(t) = exp(-iHt/ℏ) = exp(iγB⃗·σ⃗t/2)
# =============================================================================
def spin_precession(state0, B, t, gamma=1.76e11):
    """
    计算磁场中自旋进动 Spin precession in magnetic field

    参数 Parameters:
        state0: 初始自旋态
        B: 磁场向量 [Bx, By, Bz]，单位 Tesla (T)
        t: 演化时间，单位秒 (s)
        gamma: 旋磁比，默认为电子值 1.76×10¹¹ rad/(s·T)

    返回 Returns:
        state_t: 时间 t 后的自旋态

    物理过程:
        自旋绕磁场方向以拉莫尔频率 ω = γB 进动
        对于 1 T 磁场，电子自旋周期约 36 ps
    """
    B = np.array(B)
    B_mag = np.linalg.norm(B)
    if B_mag < 1e-10:
        return state0

    # 拉莫尔角频率
    omega = gamma * B_mag
    B_unit = B / B_mag

    # 构造 σ⃗·B̂ 算符
    # 旋转算符 (绕B轴旋转): U = exp(-iωt σ·B̂/2)
    sigma_dot_B = (B_unit[0] * pauli_x() +
                   B_unit[1] * pauli_y() +
                   B_unit[2] * pauli_z())

    # 利用泡利矩阵的指数公式: exp(iθ n̂·σ⃗) = cos(θ)I + i sin(θ) n̂·σ⃗
    U = np.cos(omega * t / 2) * np.eye(2) - 1j * np.sin(omega * t / 2) * sigma_dot_B

    # TODO: 计算演化后的态 |ψ(t)⟩ = U(t)|ψ(0)⟩
    state_t = U @ state0
    return state_t


# =============================================================================
# 可视化 Visualization
# 绘制布洛赫球、测量概率、自旋进动等图像
# =============================================================================
def plot_spin():
    fig = plt.figure(figsize=(14, 10))

    # 1. 布洛赫球
    ax1 = fig.add_subplot(221, projection='3d')

    # 绘制球面
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 25)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    ax1.plot_wireframe(x, y, z, alpha=0.2, color='gray')

    # 标记特殊态
    states = {
        '|↑⟩': spin_up(),
        '|↓⟩': spin_down(),
        '|+x⟩': spin_plus_x(),
        '|-x⟩': spin_minus_x()
    }
    colors = ['blue', 'red', 'green', 'orange']

    for (name, state), color in zip(states.items(), colors):
        vec = bloch_vector(state)
        ax1.quiver(0, 0, 0, vec[0], vec[1], vec[2], color=color, arrow_length_ratio=0.1)
        ax1.scatter(*vec, color=color, s=50)
        ax1.text(vec[0]*1.2, vec[1]*1.2, vec[2]*1.2, name)

    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_zlabel('z')
    ax1.set_title('布洛赫球 Bloch Sphere')

    # 2. 测量概率
    ax2 = fig.add_subplot(222)
    theta = np.linspace(0, np.pi, 100)
    state_theta = [bloch_to_state(t, 0) for t in theta]
    prob_up = [measurement_probability(s, spin_up()) for s in state_theta]
    prob_down = [measurement_probability(s, spin_down()) for s in state_theta]

    ax2.plot(np.degrees(theta), prob_up, 'b-', label='P(↑)', linewidth=2)
    ax2.plot(np.degrees(theta), prob_down, 'r-', label='P(↓)', linewidth=2)
    ax2.set_xlabel('θ (degrees)')
    ax2.set_ylabel('Probability')
    ax2.set_title('测量概率vs极角')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 自旋进动
    ax3 = fig.add_subplot(223)
    B = [0, 0, 1]  # 沿z轴磁场
    state0 = spin_plus_x()  # 初态沿+x
    t_range = np.linspace(0, 4*np.pi/1.76e11, 100)

    sx_t = []
    sy_t = []
    for t in t_range:
        state_t = spin_precession(state0, B, t)
        vec = bloch_vector(state_t)
        sx_t.append(vec[0])
        sy_t.append(vec[1])

    ax3.plot(t_range*1e12, sx_t, 'b-', label='⟨σₓ⟩', linewidth=2)
    ax3.plot(t_range*1e12, sy_t, 'r-', label='⟨σᵧ⟩', linewidth=2)
    ax3.set_xlabel('t (ps)')
    ax3.set_ylabel('Expectation')
    ax3.set_title('自旋进动 (B沿z)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 泡利矩阵可视化
    ax4 = fig.add_subplot(224)
    matrices = [pauli_x(), pauli_y(), pauli_z()]
    names = ['σₓ', 'σᵧ', 'σᵤ']

    for i, (mat, name) in enumerate(zip(matrices, names)):
        ax4.text(i*1.5, 2, name, fontsize=14, ha='center')
        ax4.text(i*1.5 - 0.3, 1, f'{mat[0,0]:.0f}', fontsize=10)
        ax4.text(i*1.5 + 0.3, 1, f'{mat[0,1]}', fontsize=10)
        ax4.text(i*1.5 - 0.3, 0.5, f'{mat[1,0]}', fontsize=10)
        ax4.text(i*1.5 + 0.3, 0.5, f'{mat[1,1]:.0f}', fontsize=10)

    ax4.set_xlim(-1, 4)
    ax4.set_ylim(0, 3)
    ax4.axis('off')
    ax4.set_title('泡利矩阵 Pauli Matrices')

    plt.tight_layout()
    plt.savefig('spin.png', dpi=150)
    print("图像已保存为 spin.png")
    plt.show()


def verify():
    """验证所有练习的正确性 Verify all exercises"""
    all_passed = True

    # 检查 1.1: 泡利矩阵性质
    sx, sy, sz = pauli_x(), pauli_y(), pauli_z()
    if not pauli_square():
        print("错误 1.1: 泡利矩阵平方不等于单位阵，请检查矩阵定义")
        all_passed = False
    else:
        print("通过 1.1: 泡利矩阵正确 (σ² = I)")

    # 检查 1.2: 自旋态正交性
    up = spin_up()
    down = spin_down()
    if not np.isclose(np.vdot(up, down), 0):
        print("错误 1.2: 自旋态不正交，|↑⟩和|↓⟩的内积应为0")
        all_passed = False
    else:
        print("通过 1.2: 自旋态正确（正交归一）")

    # 检查 1.3: 测量概率
    prob = measurement_probability(spin_plus_x(), spin_up())
    if not np.isclose(prob, 0.5, rtol=0.01):
        print("错误 1.3: 测量概率计算错误，|+x⟩态测量z方向应有50%概率得|↑⟩")
        all_passed = False
    else:
        print("通过 1.3: 测量概率正确 (|+x⟩测量z: P(↑) = 0.5)")

    # 检查 1.4: 反对易关系
    anticomm = verify_anticommutation(sx, sy)
    if not np.allclose(anticomm, np.zeros((2,2))):
        print("错误 1.4: 反对易关系错误，{σₓ,σᵧ}应为零矩阵")
        all_passed = False
    else:
        print("通过 1.4: 泡利矩阵性质正确 ({σₓ,σᵧ} = 0)")

    # 检查 1.5: 布洛赫球坐标
    theta, phi = state_to_bloch(spin_up())
    if not np.isclose(theta, 0, atol=0.01):
        print("错误 1.5: 布洛赫球坐标错误，|↑⟩态应对应θ=0（北极）")
        all_passed = False
    else:
        print("通过 1.5: 布洛赫球坐标转换正确")

    # 检查 1.6: 自旋进动
    state_prec = spin_precession(spin_plus_x(), [0,0,1], np.pi/1.76e11)
    vec = bloch_vector(state_prec)
    # 经过半个周期，应该转到接近-x方向
    if vec[0] > 0:
        print("错误 1.6: 自旋进动方向错误，半周期后应从+x转向-x")
        all_passed = False
    else:
        print("通过 1.6: 自旋进动正确")

    if all_passed:
        print("\n所有测试通过！")
        try:
            plot_spin()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("自旋与泡利矩阵 Spin and Pauli Matrices")
    print("=" * 50)
    verify()
