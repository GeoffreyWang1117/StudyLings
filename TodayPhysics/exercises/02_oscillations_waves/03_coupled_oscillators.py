"""
耦合振子与简正模式 Coupled Oscillators and Normal Modes
难度 Difficulty: ★★★★

学习目标 Learning Objectives:
- 理解耦合振子系统的动力学行为
  Understand the dynamics of coupled oscillator systems
- 求解简正模式和简正频率（本征值问题）
  Solve for normal modes and normal frequencies (eigenvalue problem)
- 分析能量在振子间的周期性转移（拍频现象）
  Analyze periodic energy transfer between oscillators (beat phenomenon)
- 理解色散关系和群速度的概念
  Understand dispersion relation and group velocity concepts

物理背景 Physical Background:
耦合振子是多体振动系统的基础模型，广泛应用于：
- 分子振动（如 CO₂ 分子的振动模式）
- 晶格动力学（声子、热传导）
- 电路中的耦合 LC 振荡器
- 机械系统的振动分析

核心概念：
1. 简正模式（Normal Mode）：系统中所有振子以相同频率振动的特殊模式
2. 简正频率（Normal Frequency）：简正模式对应的振动频率
3. 模式叠加：任意运动都可分解为简正模式的线性组合
4. 拍频：当两个简正频率接近时，能量在振子间周期性转移

数学方法：
运动方程 mẍ = -Kx 可写成矩阵形式
求解 det(K - mω²I) = 0 得到简正频率
对应的本征向量给出简正模式

HINT: 耦合运动方程形成矩阵本征值问题
HINT: 简正模式是所有振子同频振动的模式
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.linalg import eigh
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])

# I AM NOT DONE

# =============================================================================
# 练习 3.1: 两个耦合振子
# Exercise 3.1: Two Coupled Oscillators
# =============================================================================
"""
物理模型：
两个质量为 m 的物体通过弹簧连接在一条直线上
  墙 ===k=== [m₁] ===κ=== [m₂] ===k=== 墙

弹簧常数：
- k: 连接墙壁的外侧弹簧（回复力）[N/m]
- κ (kappa): 中间耦合弹簧（振子间相互作用）[N/m]

运动方程：
m·ẍ₁ = -k·x₁ - κ·(x₁ - x₂)  →  m·ẍ₁ = -(k+κ)x₁ + κx₂
m·ẍ₂ = -k·x₂ - κ·(x₂ - x₁)  →  m·ẍ₂ = κx₁ - (k+κ)x₂

矩阵形式：ẍ = -M·x，其中
M = (1/m) × [(k+κ)  -κ  ]
            [-κ    (k+κ)]
"""
def coupled_oscillator_matrix(k, kappa, m):
    """
    构建耦合振子的系数矩阵 M
    Build coefficient matrix M for coupled oscillators

    参数 Parameters:
    - k: 外侧弹簧常数 Outer spring constant (N/m)
    - kappa: 耦合弹簧常数 Coupling spring constant (N/m)
    - m: 振子质量 Oscillator mass (kg)

    返回 Returns:
    - M: 2×2 系数矩阵，满足 ẍ = -M·x

    矩阵的本征值给出 ω²，本征向量给出简正模式
    """
    # TODO: 构建系数矩阵
    # TODO: Build the coefficient matrix
    M = np.array([
        [(k + kappa)/m, -kappa/m],
        [-kappa/m, (k + kappa)/m]
    ])
    return M

def normal_frequencies(k, kappa, m):
    """
    计算两个简正频率
    Calculate the two normal frequencies

    参数 Parameters:
    - k: 外侧弹簧常数 Outer spring constant (N/m)
    - kappa: 耦合弹簧常数 Coupling spring constant (N/m)
    - m: 振子质量 Oscillator mass (kg)

    返回 Returns:
    - omega1: 同相模式频率 In-phase mode frequency (rad/s)
    - omega2: 反相模式频率 Out-of-phase mode frequency (rad/s)

    物理解释：
    - 同相模式 (ω₁)：两振子同方向运动，中间弹簧不伸缩，ω₁² = k/m
    - 反相模式 (ω₂)：两振子反方向运动，中间弹簧额外贡献，ω₂² = (k + 2κ)/m
    """
    # TODO: 计算两个简正频率
    # TODO: Calculate two normal frequencies
    omega1 = np.sqrt(k / m)  # 同相模式 In-phase mode
    omega2 = np.sqrt((k + 2*kappa) / m)  # 反相模式 Out-of-phase mode
    return omega1, omega2


# =============================================================================
# 练习 3.2: 简正模式
# Exercise 3.2: Normal Modes
# =============================================================================
"""
物理背景：
简正模式是系统的本征振动方式，每个模式中所有振子以相同频率振动。

两振子系统的简正模式：
1. 同相模式（对称模式）：
   - 模式向量：[1, 1]（归一化后 [1/√2, 1/√2]）
   - 两振子同方向运动
   - 中间耦合弹簧不伸缩
   - 频率较低：ω₁ = √(k/m)

2. 反相模式（反对称模式）：
   - 模式向量：[1, -1]（归一化后 [1/√2, -1/√2]）
   - 两振子反方向运动
   - 中间耦合弹簧额外贡献回复力
   - 频率较高：ω₂ = √((k+2κ)/m)

简正模式的正交性：mode1 · mode2 = 0
任意运动 = c₁·mode1·cos(ω₁t) + c₂·mode2·cos(ω₂t)
"""
def normal_modes(k, kappa, m):
    """
    返回归一化的简正模式向量
    Return normalized normal mode vectors

    参数 Parameters:
    - k, kappa, m: 系统参数（此处实际不影响模式形状）

    返回 Returns:
    - mode1: 同相模式向量 In-phase mode vector (归一化)
    - mode2: 反相模式向量 Out-of-phase mode vector (归一化)

    注意：对于对称系统，模式向量与参数值无关，只取决于对称性
    """
    # TODO: 返回归一化的模式向量
    # TODO: Return normalized mode vectors
    mode1 = np.array([1, 1]) / np.sqrt(2)  # 同相模式 In-phase: 两振子同向
    mode2 = np.array([1, -1]) / np.sqrt(2)  # 反相模式 Out-of-phase: 两振子反向
    return mode1, mode2


# =============================================================================
# 练习 3.3: 耦合振子模拟
# Exercise 3.3: Coupled Oscillator Simulation
# =============================================================================
"""
数值模拟方法：
使用 scipy.integrate.odeint 求解常微分方程组。
需要将二阶方程转化为一阶方程组：

原方程：
m·ẍ₁ = -(k+κ)x₁ + κx₂
m·ẍ₂ = κx₁ - (k+κ)x₂

引入速度变量 v₁ = ẋ₁, v₂ = ẋ₂，得到一阶方程组：
ẋ₁ = v₁
ẋ₂ = v₂
v̇₁ = -(k+κ)/m·x₁ + κ/m·x₂
v̇₂ = κ/m·x₁ - (k+κ)/m·x₂

状态向量：state = [x₁, x₂, v₁, v₂]
"""
def coupled_oscillator_derivatives(state, t, k, kappa, m):
    """
    计算耦合振子的状态导数（用于 odeint）
    Compute state derivatives for coupled oscillators (for odeint)

    参数 Parameters:
    - state: 状态向量 [x1, x2, v1, v2]
             x1, x2: 位移 Displacements (m)
             v1, v2: 速度 Velocities (m/s)
    - t: 时间 Time (s)（odeint 需要，这里不直接使用）
    - k: 外侧弹簧常数 Outer spring constant (N/m)
    - kappa: 耦合弹簧常数 Coupling spring constant (N/m)
    - m: 质量 Mass (kg)

    返回 Returns:
    - [ẋ₁, ẋ₂, v̇₁, v̇₂]: 状态导数向量 State derivatives
    """
    x1, x2, v1, v2 = state

    # TODO: 根据运动方程计算加速度
    # TODO: Calculate accelerations from equations of motion
    a1 = -(k + kappa) * x1 / m + kappa * x2 / m  # 振子1的加速度
    a2 = kappa * x1 / m - (k + kappa) * x2 / m   # 振子2的加速度

    return [v1, v2, a1, a2]

def simulate_coupled_oscillators(x1_0, x2_0, v1_0, v2_0, k, kappa, m, t_end=20, dt=0.01):
    """
    模拟耦合振子的运动
    Simulate coupled oscillator motion

    参数 Parameters:
    - x1_0, x2_0: 初始位移 Initial displacements (m)
    - v1_0, v2_0: 初始速度 Initial velocities (m/s)
    - k, kappa, m: 系统参数 System parameters
    - t_end: 模拟结束时间 End time (s)
    - dt: 时间步长 Time step (s)

    返回 Returns:
    - t: 时间数组 Time array
    - x1, x2: 两个振子的位移历史 Displacement histories
    """
    t = np.arange(0, t_end, dt)
    state0 = [x1_0, x2_0, v1_0, v2_0]
    solution = odeint(coupled_oscillator_derivatives, state0, t, args=(k, kappa, m))
    return t, solution[:, 0], solution[:, 1]


# =============================================================================
# 练习 3.4: 拍频现象
# Exercise 3.4: Beat Phenomenon
# =============================================================================
"""
物理背景：
当耦合较弱时（κ << k），两个简正频率接近，会产生拍频现象。

考虑初始条件：只激发振子1（x₁(0)=A, x₂(0)=0）
用简正模式展开：
x₁(t) = (A/2)[cos(ω₁t) + cos(ω₂t)] = A·cos((ω₁-ω₂)t/2)·cos((ω₁+ω₂)t/2)
x₂(t) = (A/2)[cos(ω₁t) - cos(ω₂t)] = A·sin((ω₁-ω₂)t/2)·sin((ω₁+ω₂)t/2)

物理现象：
- 振子1的振幅从 A 逐渐减小到 0
- 同时振子2的振幅从 0 增大到 A
- 能量完全转移后，过程反转
- 转移周期 T = 2π/|ω₁ - ω₂|

应用：
- Wilberforce 摆（扭转-伸缩耦合）
- 双摆系统
- 量子态的拉比振荡
"""
def beat_frequency(omega1, omega2):
    """
    计算拍频（角频率）
    Calculate beat frequency

    参数 Parameters:
    - omega1: 第一个简正频率 First normal frequency (rad/s)
    - omega2: 第二个简正频率 Second normal frequency (rad/s)

    返回 Returns:
    - omega_beat: 拍频 Beat frequency (rad/s)

    公式 Formula: ω_beat = |ω₁ - ω₂|
    """
    return abs(omega1 - omega2)

def energy_transfer_period(omega1, omega2):
    """
    计算能量完全转移的周期
    Calculate the period for complete energy transfer

    参数 Parameters:
    - omega1: 第一个简正频率 First normal frequency (rad/s)
    - omega2: 第二个简正频率 Second normal frequency (rad/s)

    返回 Returns:
    - T: 能量转移周期 Energy transfer period (s)

    公式 Formula: T = 2π/|ω₁ - ω₂|
    物理意义：能量从振子1完全转移到振子2再转回的时间
    """
    omega_beat = beat_frequency(omega1, omega2)
    if omega_beat < 1e-10:  # 避免除零
        return np.inf  # 无耦合时能量不转移
    return 2 * np.pi / omega_beat


# =============================================================================
# 练习 3.5: N个耦合振子
# Exercise 3.5: N Coupled Oscillators
# =============================================================================
"""
物理模型：
N 个质量为 m 的振子排成一条链，两端固定在墙上。
墙 ===k=== [1] ===κ=== [2] ===κ=== ... ===κ=== [N] ===k=== 墙

边界条件：两端固定（x₀ = xₙ₊₁ = 0）

运动方程：
- 振子1: m·ẍ₁ = -k·x₁ - κ·(x₁-x₂) = -(k+κ)x₁ + κx₂
- 中间振子i: m·ẍᵢ = -κ·(xᵢ-xᵢ₋₁) - κ·(xᵢ-xᵢ₊₁) = κxᵢ₋₁ - 2κxᵢ + κxᵢ₊₁
- 振子N: m·ẍₙ = -κ·(xₙ-xₙ₋₁) - k·xₙ = κxₙ₋₁ - (k+κ)xₙ

这是晶格动力学和固体物理的基础模型。
当 N → ∞ 时，得到连续介质的波动方程。
"""
def coupled_chain_matrix(N, k, kappa, m):
    """
    构建 N 个振子链的系数矩阵
    Build coefficient matrix for N-oscillator chain

    参数 Parameters:
    - N: 振子数量 Number of oscillators
    - k: 连接墙壁的弹簧常数 Spring constant to walls (N/m)
    - kappa: 振子间耦合弹簧常数 Coupling spring constant (N/m)
    - m: 振子质量 Oscillator mass (kg)

    返回 Returns:
    - M: N×N 系数矩阵，满足 ẍ = -M·x
    """
    M = np.zeros((N, N))
    for i in range(N):
        # 对角元：内部振子受两个耦合弹簧，边界振子受一个耦合弹簧和一个墙壁弹簧
        M[i, i] = (k + 2*kappa) / m if (i > 0 and i < N-1) else (k + kappa) / m
        # 非对角元：耦合项
        if i > 0:
            M[i, i-1] = -kappa / m
        if i < N-1:
            M[i, i+1] = -kappa / m
    # 边界修正（端点振子只连接一个耦合弹簧）
    M[0, 0] = (k + kappa) / m
    M[N-1, N-1] = (k + kappa) / m
    return M

def find_normal_modes_chain(N, k, kappa, m):
    """
    求解 N 振子链的简正频率和模式
    Find normal frequencies and modes for N-oscillator chain

    参数 Parameters:
    - N: 振子数量 Number of oscillators
    - k, kappa, m: 系统参数 System parameters

    返回 Returns:
    - frequencies: N 个简正频率数组 Array of N normal frequencies (rad/s)
    - eigenvectors: 简正模式矩阵 Normal mode matrix (每列是一个模式)

    说明：使用 scipy.linalg.eigh 求解对称矩阵的本征值问题
    """
    M = coupled_chain_matrix(N, k, kappa, m)
    # TODO: 求解本征值问题 M·v = ω²·v
    # TODO: Solve eigenvalue problem M·v = ω²·v
    # eigh 返回升序排列的本征值
    eigenvalues, eigenvectors = eigh(M)
    # 本征值 = ω²，取平方根得到频率
    frequencies = np.sqrt(eigenvalues)
    return frequencies, eigenvectors


# =============================================================================
# 练习 3.6: 色散关系
# Exercise 3.6: Dispersion Relation
# =============================================================================
"""
物理背景：
色散关系描述波的角频率 ω 与波数 q 的关系，是理解波动传播的关键。

无限长振子链的色散关系：
假设解的形式为 xₙ = A·exp[i(qna - ωt)]
代入运动方程得：ω² = (k/m) + (4κ/m)·sin²(qa/2)

布里渊区：
由于晶格的周期性，波数只需考虑 -π/a < q ≤ π/a（第一布里渊区）
超出此范围的波等效于区内的波

特殊情况：
- q = 0（长波极限）：ω = √(k/m)，群速度最大
- q = π/a（布里渊区边界）：ω = √((k+4κ)/m)，群速度为零

群速度和相速度：
- 相速度 v_p = ω/q：等相面的传播速度
- 群速度 v_g = dω/dq：波包（能量）的传播速度

在色散介质中，v_g ≠ v_p，波包会在传播中展宽。
"""
def dispersion_relation(q, a, k, kappa, m):
    """
    计算色散关系 ω(q)
    Calculate dispersion relation ω(q)

    参数 Parameters:
    - q: 波数 Wave number (rad/m)
    - a: 晶格常数（振子间距）Lattice constant (m)
    - k: 外侧弹簧常数 Outer spring constant (N/m)
    - kappa: 耦合弹簧常数 Coupling spring constant (N/m)
    - m: 振子质量 Oscillator mass (kg)

    返回 Returns:
    - omega: 角频率 Angular frequency (rad/s)

    公式 Formula: ω² = (k/m) + (4κ/m)·sin²(qa/2)
    """
    # TODO: 计算色散关系
    # TODO: Calculate dispersion relation
    omega_sq = k/m + (4*kappa/m) * np.sin(q*a/2)**2
    return np.sqrt(omega_sq)

def group_velocity(q, a, k, kappa, m):
    """
    计算群速度 v_g = dω/dq
    Calculate group velocity

    参数 Parameters:
    - q: 波数 Wave number (rad/m)
    - a: 晶格常数 Lattice constant (m)
    - k, kappa, m: 系统参数 System parameters

    返回 Returns:
    - v_g: 群速度 Group velocity (m/s)

    公式推导：
    ω² = k/m + (4κ/m)·sin²(qa/2)
    2ω·dω/dq = (4κ/m)·2·sin(qa/2)·cos(qa/2)·(a/2) = (κa/m)·sin(qa)
    v_g = dω/dq = (κa/m)·sin(qa) / (2ω) = (κa sin(qa)) / (m·ω)
    """
    omega = dispersion_relation(q, a, k, kappa, m)
    # TODO: 计算群速度
    # TODO: Calculate group velocity
    v_g = (kappa * a / m) * np.sin(q * a) / omega
    return v_g


# =============================================================================
# 可视化
# =============================================================================
def plot_coupled_oscillators():
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    k, kappa, m = 1.0, 0.2, 1.0

    # 1. 两个耦合振子 - 只激发第一个
    ax1 = axes[0, 0]
    t, x1, x2 = simulate_coupled_oscillators(1.0, 0, 0, 0, k, kappa, m)
    ax1.plot(t, x1, 'b-', label='x₁')
    ax1.plot(t, x2, 'r-', label='x₂')
    ax1.set_xlabel('t')
    ax1.set_ylabel('x')
    ax1.set_title('耦合振子 - 能量转移 Energy Transfer')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 同相模式
    ax2 = axes[0, 1]
    t, x1, x2 = simulate_coupled_oscillators(1.0, 1.0, 0, 0, k, kappa, m)
    ax2.plot(t, x1, 'b-', label='x₁')
    ax2.plot(t, x2, 'r--', label='x₂')
    ax2.set_xlabel('t')
    ax2.set_ylabel('x')
    ax2.set_title('同相模式 In-Phase Mode')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. N振子链的简正模式
    ax3 = axes[1, 0]
    N = 10
    freqs, modes = find_normal_modes_chain(N, k, kappa, m)
    for i in [0, 1, 2, N-1]:
        ax3.plot(range(N), modes[:, i], 'o-', label=f'ω = {freqs[i]:.2f}')
    ax3.set_xlabel('Oscillator index')
    ax3.set_ylabel('Amplitude')
    ax3.set_title(f'{N}振子链的简正模式 Normal Modes')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 色散关系
    ax4 = axes[1, 1]
    a = 1.0
    q = np.linspace(-np.pi/a, np.pi/a, 200)
    omega = dispersion_relation(q, a, k, kappa, m)
    ax4.plot(q, omega, 'b-', linewidth=2)
    ax4.set_xlabel('q (1/a)')
    ax4.set_ylabel('ω')
    ax4.set_title('色散关系 Dispersion Relation')
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('coupled_oscillators.png', dpi=150)
    print("图像已保存为 coupled_oscillators.png")
    plt.show()


def verify():
    """
    验证所有练习的正确性
    Verify all exercises
    """
    all_passed = True
    k, kappa, m = 1.0, 0.2, 1.0  # 测试参数

    # 检查 3.1 - 简正频率 Check normal frequencies
    omega1, omega2 = normal_frequencies(k, kappa, m)
    expected_omega1 = np.sqrt(k/m)
    expected_omega2 = np.sqrt((k + 2*kappa)/m)
    if not (np.isclose(omega1, expected_omega1, rtol=0.01) and
            np.isclose(omega2, expected_omega2, rtol=0.01)):
        print("错误 3.1: 简正频率计算错误")
        print(f"  期望：ω₁={expected_omega1:.3f}, ω₂={expected_omega2:.3f}")
        print(f"  得到：ω₁={omega1:.3f}, ω₂={omega2:.3f}")
        all_passed = False
    else:
        print(f"通过 3.1: 简正频率正确 (ω₁={omega1:.3f} rad/s, ω₂={omega2:.3f} rad/s)")

    # 检查 3.2 - 简正模式 Check normal modes
    mode1, mode2 = normal_modes(k, kappa, m)
    if not (np.isclose(np.linalg.norm(mode1), 1, rtol=0.01) and
            np.isclose(np.dot(mode1, mode2), 0, atol=0.01)):
        print("错误 3.2: 简正模式不满足正交归一条件")
        all_passed = False
    else:
        print("通过 3.2: 简正模式正确（满足正交归一条件）")

    # 检查 3.4 - 拍频周期 Check beat period
    T_beat = energy_transfer_period(omega1, omega2)
    if T_beat <= 0 or T_beat == np.inf:
        print("错误 3.4: 能量转移周期计算错误")
        all_passed = False
    else:
        print(f"通过 3.4: 拍频正确 (能量转移周期 T = {T_beat:.2f} s)")

    # 检查 3.5 - N振子链 Check N-oscillator chain
    N = 5
    freqs, modes = find_normal_modes_chain(N, k, kappa, m)
    if len(freqs) != N:
        print(f"错误 3.5: {N}振子链应有 {N} 个简正频率，实际得到 {len(freqs)} 个")
        all_passed = False
    else:
        print(f"通过 3.5: {N}振子链正确（求得 {N} 个简正频率）")

    # 检查 3.6 - 色散关系 Check dispersion relation
    omega_q = dispersion_relation(np.pi/2, 1.0, k, kappa, m)
    if omega_q <= 0:
        print("错误 3.6: 色散关系返回非正频率")
        all_passed = False
    else:
        print(f"通过 3.6: 色散关系正确 (q=π/2 时 ω={omega_q:.3f} rad/s)")

    if all_passed:
        print("\n全部测试通过！正在生成可视化图像...")
        print("All tests passed! Generating visualization...")
        try:
            plot_coupled_oscillators()
        except Exception as e:
            print(f"可视化失败 Visualization failed: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("耦合振子与简正模式 Coupled Oscillators")
    print("=" * 50)
    verify()
