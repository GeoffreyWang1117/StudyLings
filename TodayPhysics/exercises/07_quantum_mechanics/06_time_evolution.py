"""
时间演化 Time Evolution (Schrodinger and Heisenberg Pictures)
难度 Difficulty: ★★★★

物理背景 Physical Background:
--------------------------
量子力学有三种等价的表述方式（绘景）：
1. 薛定谔绘景：态随时间演化，算符不变
2. 海森堡绘景：算符随时间演化，态不变
3. 相互作用绘景：态和算符都演化（用于微扰论）

时间演化算符：
U(t) = exp(-i*H*t/hbar)
性质：幺正性 U^dagger*U = I，合成性 U(t1+t2) = U(t2)*U(t1)

重要应用：
- Rabi振荡：二能级系统在周期性外场中的行为
- Larmor进动：自旋在磁场中的进动
- 守恒量：若 [H,A]=0，则 A 不随时间变化

学习目标 Learning Objectives:
--------------------------
1. 掌握时间演化算符的构造和性质
2. 理解薛定谔绘景中态的演化
3. 理解海森堡绘景中算符的演化
4. 分析二能级系统和Rabi振荡
5. 了解相互作用绘景的应用
6. 理解守恒量与对称性的关系
7. 计算磁场中自旋的Larmor进动

关键公式 Key Formulas:
--------------------
- 时间演化算符: U(t) = exp(-i*H*t/hbar)
- 薛定谔方程: i*hbar*d|psi>/dt = H|psi>
- 海森堡方程: dA_H/dt = (i/hbar)[H, A_H]
- Rabi频率: Omega_R = 2|V|/hbar
- Rabi振荡: P_2(t) = (V²/W²)*sin²(W*t/hbar)，W = sqrt(Delta² + V²)
- Larmor频率: omega_L = gamma*B
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import hbar, m_e, e

# I AM NOT DONE

# =============================================================================
# 练习 1.1: 时间演化算符
# Exercise 1.1: Time Evolution Operator
# =============================================================================
def time_evolution_operator(H, t):
    """
    计算时间演化算符
    U(t) = exp(-iHt/hbar)

    对于时间无关的哈密顿量
    """
    # TODO: 计算时间演化算符
    U = expm(-1j * H * t / hbar)
    return U


def verify_unitarity(U):
    """
    验证时间演化算符的幺正性
    U^+ U = U U^+ = I
    """
    I = np.eye(len(U))
    return (np.allclose(U.conj().T @ U, I) and
            np.allclose(U @ U.conj().T, I))


def composition_property(H, t1, t2):
    """
    验证合成性质
    U(t1 + t2) = U(t2) U(t1)
    """
    U_t1 = time_evolution_operator(H, t1)
    U_t2 = time_evolution_operator(H, t2)
    U_total = time_evolution_operator(H, t1 + t2)

    return np.allclose(U_total, U_t2 @ U_t1)


# =============================================================================
# 练习 1.2: 薛定谔绘景
# Exercise 1.2: Schrodinger Picture
# =============================================================================
def evolve_state_schrodinger(psi_0, H, t):
    """
    薛定谔绘景中态的时间演化
    |psi(t)> = U(t)|psi(0)>
    """
    U = time_evolution_operator(H, t)
    return U @ psi_0


def expectation_value_schrodinger(A, psi_t):
    """
    薛定谔绘景中可观测量的期望值
    <A>(t) = <psi(t)|A|psi(t)>
    算符A不随时间变化
    """
    return np.real(np.conj(psi_t) @ A @ psi_t)


def probability_amplitude(psi_t, basis_state):
    """
    测量得到basis_state的概率幅
    c_n(t) = <n|psi(t)>
    """
    return np.vdot(basis_state, psi_t)


def probability(psi_t, basis_state):
    """
    测量得到basis_state的概率
    P_n(t) = |<n|psi(t)>|²
    """
    return np.abs(probability_amplitude(psi_t, basis_state))**2


# =============================================================================
# 练习 1.3: 海森堡绘景
# Exercise 1.3: Heisenberg Picture
# =============================================================================
def operator_heisenberg(A_S, H, t):
    """
    海森堡绘景中算符的时间演化
    A_H(t) = U^+(t) A_S U(t)
    """
    U = time_evolution_operator(H, t)
    U_dag = U.conj().T

    # TODO: 计算海森堡算符
    A_H = U_dag @ A_S @ U
    return A_H


def heisenberg_equation_of_motion(A, H):
    """
    海森堡运动方程（不含显式时间依赖）
    dA/dt = (i/hbar)[H, A]

    返回: dA/dt 的矩阵表示
    """
    # TODO: 计算运动方程
    commutator = H @ A - A @ H
    dA_dt = 1j / hbar * commutator
    return dA_dt


def verify_heisenberg_equation(A_S, H, t, dt=1e-18):
    """
    数值验证海森堡方程
    """
    # 数值导数
    A_t = operator_heisenberg(A_S, H, t)
    A_t_dt = operator_heisenberg(A_S, H, t + dt)
    dA_dt_numerical = (A_t_dt - A_t) / dt

    # 解析导数（在t时刻）
    dA_dt_analytical = heisenberg_equation_of_motion(A_t, H)

    return np.allclose(dA_dt_numerical, dA_dt_analytical, rtol=0.1)


# =============================================================================
# 练习 1.4: 二能级系统
# Exercise 1.4: Two-Level System
# =============================================================================
def two_level_hamiltonian(E1, E2, V=0):
    """
    二能级系统哈密顿量
    H = E1|1><1| + E2|2><2| + V(|1><2| + |2><1|)
    """
    H = np.array([[E1, V],
                  [V, E2]], dtype=complex)
    return H


def rabi_frequency(V):
    """
    Rabi频率（共振情况）
    Omega_R = 2|V|/hbar
    """
    return 2 * np.abs(V) / hbar


def two_level_evolution(psi_0, E1, E2, V, t_array):
    """
    二能级系统的时间演化
    返回各时刻的态
    """
    H = two_level_hamiltonian(E1, E2, V)
    states = []

    for t in t_array:
        psi_t = evolve_state_schrodinger(psi_0, H, t)
        states.append(psi_t)

    return np.array(states)


def rabi_oscillation(E1, E2, V, t):
    """
    Rabi振荡：初态为|1>时，处于|2>的概率
    P_2(t) = (V²/W²) sin²(Wt/hbar)
    其中 W = sqrt((E1-E2)²/4 + V²)
    """
    delta = (E1 - E2) / 2
    W = np.sqrt(delta**2 + V**2)

    # TODO: 计算振荡概率
    P_2 = (V**2 / W**2) * np.sin(W * t / hbar)**2
    return P_2


# =============================================================================
# 练习 1.5: 相互作用绘景
# Exercise 1.5: Interaction Picture
# =============================================================================
def interaction_picture_state(psi_S, H_0, t):
    """
    相互作用绘景中的态
    |psi_I(t)> = U_0^+(t)|psi_S(t)>
    其中 U_0(t) = exp(-iH_0*t/hbar)
    """
    U_0 = time_evolution_operator(H_0, t)
    U_0_dag = U_0.conj().T

    return U_0_dag @ psi_S


def interaction_picture_operator(A_S, H_0, t):
    """
    相互作用绘景中的算符
    A_I(t) = U_0^+(t) A_S U_0(t)
    """
    U_0 = time_evolution_operator(H_0, t)
    U_0_dag = U_0.conj().T

    return U_0_dag @ A_S @ U_0


def effective_hamiltonian_interaction(V_S, H_0, t):
    """
    相互作用绘景中的有效哈密顿量
    H_I(t) = U_0^+(t) V_S U_0(t)
    """
    return interaction_picture_operator(V_S, H_0, t)


# =============================================================================
# 练习 1.6: 守恒量
# Exercise 1.6: Constants of Motion
# =============================================================================
def is_constant_of_motion(A, H):
    """
    判断A是否为守恒量
    [H, A] = 0 时 A 是守恒量
    """
    commutator = H @ A - A @ H
    return np.allclose(commutator, 0)


def energy_expectation(psi_t, H):
    """
    能量期望值（应为常数）
    <E>(t) = <psi(t)|H|psi(t)>
    """
    return expectation_value_schrodinger(H, psi_t)


def verify_energy_conservation(psi_0, H, t_array):
    """
    验证能量守恒
    """
    E_0 = energy_expectation(psi_0, H)
    for t in t_array:
        psi_t = evolve_state_schrodinger(psi_0, H, t)
        E_t = energy_expectation(psi_t, H)
        if not np.isclose(E_t, E_0, rtol=1e-6):
            return False
    return True


# =============================================================================
# 练习 1.7: 自旋进动
# Exercise 1.7: Spin Precession
# =============================================================================
def spin_hamiltonian(B, gamma):
    """
    磁场中自旋的哈密顿量
    H = -gamma * B * S_z = -(gamma*hbar/2) * B * sigma_z
    B: 沿z方向的磁场
    gamma: 旋磁比
    """
    sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
    return -gamma * hbar / 2 * B * sigma_z


def larmor_frequency(B, gamma):
    """
    Larmor进动频率
    omega_L = gamma * B
    """
    return gamma * B


def spin_expectation_values(psi_0, B, gamma, t_array):
    """
    计算自旋各分量期望值随时间的变化
    返回 <S_x>(t), <S_y>(t), <S_z>(t)
    """
    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)

    S_x = hbar / 2 * sigma_x
    S_y = hbar / 2 * sigma_y
    S_z = hbar / 2 * sigma_z

    H = spin_hamiltonian(B, gamma)

    Sx_list, Sy_list, Sz_list = [], [], []

    for t in t_array:
        psi_t = evolve_state_schrodinger(psi_0, H, t)
        Sx_list.append(expectation_value_schrodinger(S_x, psi_t))
        Sy_list.append(expectation_value_schrodinger(S_y, psi_t))
        Sz_list.append(expectation_value_schrodinger(S_z, psi_t))

    return np.array(Sx_list), np.array(Sy_list), np.array(Sz_list)


# =============================================================================
# 可视化
# =============================================================================
def plot_time_evolution():
    """绘制时间演化相关图"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # 1. Rabi振荡
    ax1 = axes[0, 0]
    E1, E2 = 0, 0  # 共振
    V = 0.1 * e  # 0.1 eV
    T_rabi = 2 * np.pi * hbar / (2 * V)
    t_array = np.linspace(0, 3 * T_rabi, 200)

    P_2 = [rabi_oscillation(E1, E2, V, t) for t in t_array]

    ax1.plot(t_array / T_rabi, P_2, 'b-', linewidth=2)
    ax1.set_xlabel('t / T_Rabi')
    ax1.set_ylabel('P_2(t)')
    ax1.set_title('Rabi振荡 (共振)')
    ax1.grid(True, alpha=0.3)

    # 2. 失谐Rabi振荡
    ax2 = axes[0, 1]
    detunings = [0, 0.5, 1.0, 2.0]  # 相对于V的失谐

    for delta_ratio in detunings:
        delta = delta_ratio * V
        E1, E2 = delta, 0
        P_2 = [rabi_oscillation(E1, E2, V, t) for t in t_array]
        ax2.plot(t_array / T_rabi, P_2, label=f'Delta/V = {delta_ratio}', linewidth=2)

    ax2.set_xlabel('t / T_Rabi')
    ax2.set_ylabel('P_2(t)')
    ax2.set_title('失谐Rabi振荡')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 自旋进动
    ax3 = axes[1, 0]
    B = 1  # Tesla
    gamma = e / m_e  # 电子旋磁比
    omega_L = larmor_frequency(B, gamma)
    T_L = 2 * np.pi / omega_L

    t_spin = np.linspace(0, 2 * T_L, 200)

    # 初态: |+x> = (|up> + |down>)/sqrt(2)
    psi_0 = np.array([1, 1], dtype=complex) / np.sqrt(2)
    Sx, Sy, Sz = spin_expectation_values(psi_0, B, gamma, t_spin)

    ax3.plot(t_spin / T_L, Sx / (hbar/2), 'r-', label='<S_x>/S', linewidth=2)
    ax3.plot(t_spin / T_L, Sy / (hbar/2), 'g-', label='<S_y>/S', linewidth=2)
    ax3.plot(t_spin / T_L, Sz / (hbar/2), 'b-', label='<S_z>/S', linewidth=2)
    ax3.set_xlabel('t / T_Larmor')
    ax3.set_ylabel('Spin expectation / (hbar/2)')
    ax3.set_title('自旋Larmor进动')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 自旋在Bloch球上的轨迹
    ax4 = fig.add_subplot(2, 2, 4, projection='3d')

    ax4.plot(Sx / (hbar/2), Sy / (hbar/2), Sz / (hbar/2), 'b-', linewidth=2)
    ax4.scatter([Sx[0] / (hbar/2)], [Sy[0] / (hbar/2)], [Sz[0] / (hbar/2)],
               s=100, c='r', marker='o', label='t=0')

    # 画Bloch球
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    x_sphere = np.outer(np.cos(u), np.sin(v))
    y_sphere = np.outer(np.sin(u), np.sin(v))
    z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))
    ax4.plot_surface(x_sphere, y_sphere, z_sphere, alpha=0.1, color='gray')

    ax4.set_xlabel('S_x')
    ax4.set_ylabel('S_y')
    ax4.set_zlabel('S_z')
    ax4.set_title('Bloch球上的进动')
    ax4.legend()

    plt.tight_layout()
    plt.savefig('time_evolution.png', dpi=150)
    print("图像已保存为 time_evolution.png")
    plt.show()


# =============================================================================
# 验证函数
# =============================================================================
def verify():
    """Verify all exercises"""
    all_passed = True

    # Test Hamiltonian
    E1, E2, V = 1.0 * e, 0.5 * e, 0.1 * e
    H = two_level_hamiltonian(E1, E2, V)

    # Check 1.1 - Time evolution operator
    t = 1e-15  # 1 fs
    U = time_evolution_operator(H, t)
    if not verify_unitarity(U):
        print("X 1.1 时间演化算符不是幺正的")
        all_passed = False
    else:
        print("V 1.1 时间演化算符幺正性正确")

    # Check composition property
    t1, t2 = 0.5e-15, 0.3e-15
    if not composition_property(H, t1, t2):
        print("X 1.1 合成性质验证失败")
        all_passed = False
    else:
        print("V 1.1 合成性质正确 U(t1+t2) = U(t2)U(t1)")

    # Check 1.2 - Schrodinger picture
    psi_0 = np.array([1, 0], dtype=complex)  # 初态 |1>
    psi_t = evolve_state_schrodinger(psi_0, H, t)
    norm = np.linalg.norm(psi_t)
    if not np.isclose(norm, 1):
        print("X 1.2 薛定谔绘景态未归一")
        all_passed = False
    else:
        print("V 1.2 薛定谔绘景正确")

    # Check 1.3 - Heisenberg picture
    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    if not verify_heisenberg_equation(sigma_x, H, t):
        print("X 1.3 海森堡方程验证失败")
        all_passed = False
    else:
        print("V 1.3 海森堡绘景正确")

    # Check 1.4 - Rabi oscillation
    E1, E2 = 0, 0  # 共振
    omega_R = rabi_frequency(V)
    T_rabi = 2 * np.pi / omega_R
    P_half = rabi_oscillation(E1, E2, V, T_rabi / 2)
    if not np.isclose(P_half, 1, atol=0.01):
        print("X 1.4 Rabi振荡错误")
        all_passed = False
    else:
        print(f"V 1.4 Rabi振荡正确 (T_Rabi = {T_rabi*1e15:.2f} fs)")

    # Check 1.5 - Interaction picture
    H_0 = two_level_hamiltonian(E1, E2, 0)
    psi_I = interaction_picture_state(psi_t, H_0, t)
    norm_I = np.linalg.norm(psi_I)
    if not np.isclose(norm_I, 1):
        print("X 1.5 相互作用绘景态未归一")
        all_passed = False
    else:
        print("V 1.5 相互作用绘景正确")

    # Check 1.6 - Energy conservation
    t_test = np.linspace(0, 1e-14, 20)
    if not verify_energy_conservation(psi_0, H, t_test):
        print("X 1.6 能量不守恒")
        all_passed = False
    else:
        print("V 1.6 能量守恒正确")

    # Check 1.7 - Spin precession
    B = 1
    gamma = e / m_e
    omega_L = larmor_frequency(B, gamma)
    if omega_L <= 0:
        print("X 1.7 Larmor频率错误")
        all_passed = False
    else:
        print(f"V 1.7 自旋进动正确 (omega_L = {omega_L:.2e} rad/s)")

    if all_passed:
        print("\n所有测试通过！正在生成可视化...")
        try:
            plot_time_evolution()
        except Exception as e:
            print(f"可视化生成失败: {e}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("时间演化 Time Evolution")
    print("=" * 50)
    verify()
