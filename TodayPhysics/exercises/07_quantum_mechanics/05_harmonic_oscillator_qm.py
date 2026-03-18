"""
量子谐振子 Quantum Harmonic Oscillator (Ladder Operators)
难度 Difficulty: ★★★★

物理背景 Physical Background:
--------------------------
本练习使用升降算符（代数方法）求解量子谐振子。
这种方法比直接求解薛定谔方程更为优雅，并揭示了谐振子的代数结构。

升降算符的定义：
- 降算符: a = sqrt(m*omega/(2*hbar))*(x + i*p/(m*omega))
- 升算符: a^dagger = sqrt(m*omega/(2*hbar))*(x - i*p/(m*omega))

代数结构：
- 对易关系: [a, a^dagger] = 1
- 哈密顿量: H = hbar*omega*(a^dagger*a + 1/2) = hbar*omega*(N + 1/2)
- 数算符: N = a^dagger*a，N|n> = n|n>

这种代数结构在量子场论中极为重要（场的量子化）

学习目标 Learning Objectives:
--------------------------
1. 掌握升降算符的矩阵表示
2. 理解粒子数算符和能级结构
3. 熟练计算波函数和概率密度
4. 理解对易关系及其物理意义
5. 掌握相干态的性质（最接近经典的量子态）
6. 了解位置和动量算符的升降算符表示
7. 理解量子态的时间演化

关键公式 Key Formulas:
--------------------
- 降算符作用: a|n> = sqrt(n)|n-1>, a|0> = 0
- 升算符作用: a^dagger|n> = sqrt(n+1)|n+1>
- 能级: E_n = hbar*omega*(n + 1/2)
- 位置算符: x = sqrt(hbar/(2m*omega))*(a + a^dagger)
- 动量算符: p = i*sqrt(hbar*m*omega/2)*(a^dagger - a)
- 相干态: |alpha> = exp(-|alpha|²/2)*sum_n (alpha^n/sqrt(n!))|n>
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import hermite
from scipy.linalg import expm
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import hbar, m_e

# I AM NOT DONE

# =============================================================================
# 练习 1.1: 升降算符的矩阵表示
# Exercise 1.1: Matrix Representation of Ladder Operators
# =============================================================================
def annihilation_operator(N_max):
    """
    湮灭算符 (降算符) a 的矩阵表示
    a|n> = sqrt(n)|n-1>
    在 |0>, |1>, ..., |N_max-1> 基底下

    返回 N_max x N_max 矩阵
    """
    a = np.zeros((N_max, N_max), dtype=complex)

    # TODO: 构建降算符矩阵
    for n in range(1, N_max):
        a[n - 1, n] = np.sqrt(n)

    return a


def creation_operator(N_max):
    """
    产生算符 (升算符) a^+ 的矩阵表示
    a^+|n> = sqrt(n+1)|n+1>
    """
    a = annihilation_operator(N_max)
    return a.conj().T


def number_operator(N_max):
    """
    粒子数算符 N = a^+a
    N|n> = n|n>
    """
    a = annihilation_operator(N_max)
    a_dag = creation_operator(N_max)

    # TODO: 计算粒子数算符
    N = a_dag @ a
    return N


# =============================================================================
# 练习 1.2: 哈密顿量和能级
# Exercise 1.2: Hamiltonian and Energy Levels
# =============================================================================
def hamiltonian_qho(omega, N_max):
    """
    量子谐振子哈密顿量
    H = hbar*omega*(N + 1/2)
    """
    N = number_operator(N_max)
    I = np.eye(N_max)

    # TODO: 构建哈密顿量
    H = hbar * omega * (N + 0.5 * I)
    return H


def energy_levels(n, omega):
    """
    能级公式 E_n = hbar*omega*(n + 1/2)
    """
    return hbar * omega * (n + 0.5)


def zero_point_energy(omega):
    """
    零点能 E_0 = hbar*omega/2
    """
    return 0.5 * hbar * omega


# =============================================================================
# 练习 1.3: 波函数
# Exercise 1.3: Wave Functions
# =============================================================================
def qho_wavefunction(n, x, m, omega):
    """
    量子谐振子波函数
    psi_n(x) = (mw/(pi*hbar))^(1/4) * (1/sqrt(2^n n!)) * H_n(xi) * exp(-xi^2/2)
    其中 xi = sqrt(mw/hbar) * x
    H_n 是Hermite多项式
    """
    xi = np.sqrt(m * omega / hbar) * x

    # 归一化常数
    norm = (m * omega / (np.pi * hbar))**0.25
    norm *= 1 / np.sqrt(2**n * np.math.factorial(n))

    # Hermite多项式
    H_n = hermite(n)

    # TODO: 计算波函数
    psi = norm * H_n(xi) * np.exp(-xi**2 / 2)
    return psi


def probability_density(n, x, m, omega):
    """
    概率密度 |psi_n(x)|²
    """
    psi = qho_wavefunction(n, x, m, omega)
    return np.abs(psi)**2


def classical_turning_point(n, m, omega):
    """
    经典转折点 x_c，满足 E_n = (1/2)m*omega^2*x_c^2
    x_c = sqrt(2*E_n/(m*omega^2)) = sqrt(hbar*(2n+1)/(m*omega))
    """
    E_n = energy_levels(n, omega)
    return np.sqrt(2 * E_n / (m * omega**2))


# =============================================================================
# 练习 1.4: 对易关系
# Exercise 1.4: Commutation Relations
# =============================================================================
def commutator(A, B):
    """
    计算对易子 [A, B] = AB - BA
    """
    return A @ B - B @ A


def verify_commutation_a_adag(N_max):
    """
    验证 [a, a^+] = 1
    """
    a = annihilation_operator(N_max)
    a_dag = creation_operator(N_max)

    comm = commutator(a, a_dag)
    I = np.eye(N_max)

    # 注意: 由于截断，只有内部元素满足对易关系
    return np.allclose(comm[:-1, :-1], I[:-1, :-1])


def verify_H_N_commutation(omega, N_max):
    """
    验证 [H, N] = 0
    哈密顿量和粒子数算符对易
    """
    H = hamiltonian_qho(omega, N_max)
    N = number_operator(N_max)

    comm = commutator(H, N)
    return np.allclose(comm, 0)


# =============================================================================
# 练习 1.5: 相干态
# Exercise 1.5: Coherent States
# =============================================================================
def coherent_state(alpha, N_max):
    """
    相干态 |alpha> = exp(-|alpha|²/2) * sum_n (alpha^n/sqrt(n!)) |n>
    相干态是降算符的本征态: a|alpha> = alpha|alpha>
    """
    state = np.zeros(N_max, dtype=complex)

    # TODO: 构建相干态
    for n in range(N_max):
        state[n] = alpha**n / np.sqrt(np.math.factorial(n))

    # 归一化因子
    state *= np.exp(-np.abs(alpha)**2 / 2)
    return state


def verify_coherent_eigenvalue(alpha, N_max):
    """
    验证相干态是降算符的本征态
    a|alpha> = alpha|alpha>
    """
    a = annihilation_operator(N_max)
    state = coherent_state(alpha, N_max)

    a_state = a @ state
    expected = alpha * state

    return np.allclose(a_state, expected, atol=1e-6)


def coherent_state_mean_n(alpha):
    """
    相干态的平均粒子数
    <n> = |alpha|²
    """
    return np.abs(alpha)**2


def coherent_state_uncertainty_n(alpha):
    """
    相干态粒子数的不确定度
    Delta_n = |alpha|
    """
    return np.abs(alpha)


# =============================================================================
# 练习 1.6: 位置和动量期望值
# Exercise 1.6: Position and Momentum Expectation Values
# =============================================================================
def position_operator(m, omega, N_max):
    """
    位置算符 x = sqrt(hbar/(2m*omega)) * (a + a^+)
    """
    a = annihilation_operator(N_max)
    a_dag = creation_operator(N_max)

    # TODO: 计算位置算符
    coeff = np.sqrt(hbar / (2 * m * omega))
    x = coeff * (a + a_dag)
    return x


def momentum_operator(m, omega, N_max):
    """
    动量算符 p = i*sqrt(hbar*m*omega/2) * (a^+ - a)
    """
    a = annihilation_operator(N_max)
    a_dag = creation_operator(N_max)

    # TODO: 计算动量算符
    coeff = 1j * np.sqrt(hbar * m * omega / 2)
    p = coeff * (a_dag - a)
    return p


def expectation_value(A, state):
    """
    计算算符A在态|state>中的期望值
    <A> = <state|A|state>
    """
    return np.real(np.conj(state) @ A @ state)


def uncertainty_x(m, omega, n):
    """
    位置不确定度（能量本征态）
    Delta_x = sqrt(hbar(2n+1)/(2m*omega))
    """
    return np.sqrt(hbar * (2*n + 1) / (2 * m * omega))


def uncertainty_p(m, omega, n):
    """
    动量不确定度（能量本征态）
    Delta_p = sqrt(hbar*m*omega*(2n+1)/2)
    """
    return np.sqrt(hbar * m * omega * (2*n + 1) / 2)


# =============================================================================
# 练习 1.7: 时间演化
# Exercise 1.7: Time Evolution
# =============================================================================
def time_evolution_operator(omega, t, N_max):
    """
    时间演化算符 U(t) = exp(-iHt/hbar)
    对于 QHO: U(t) = exp(-i*omega*t*(N + 1/2))
    """
    H = hamiltonian_qho(omega, N_max)
    U = expm(-1j * H * t / hbar)
    return U


def evolved_state(initial_state, omega, t, N_max):
    """
    计算时间演化后的态
    |psi(t)> = U(t)|psi(0)>
    """
    U = time_evolution_operator(omega, t, N_max)
    return U @ initial_state


def coherent_state_evolution(alpha_0, omega, t):
    """
    相干态的时间演化
    |alpha(t)> = |alpha_0 * exp(-i*omega*t)> (忽略整体相位)
    相干态在演化中保持为相干态
    """
    return alpha_0 * np.exp(-1j * omega * t)


# =============================================================================
# 可视化
# =============================================================================
def plot_quantum_harmonic_oscillator():
    """绘制量子谐振子相关图"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    m = m_e
    omega = 1e15  # rad/s

    # 1. 波函数
    ax1 = axes[0, 0]
    x_range = np.linspace(-5, 5, 500)
    x_scale = np.sqrt(hbar / (m * omega))
    x = x_range * x_scale

    for n in range(5):
        psi = qho_wavefunction(n, x, m, omega)
        # 缩放并偏移以便显示
        offset = n + 0.5
        ax1.plot(x_range, np.abs(psi * x_scale)**0.5 * 2 + offset,
                label=f'n={n}', linewidth=2)
        ax1.axhline(y=offset, color='gray', linestyle='--', alpha=0.3)

    ax1.set_xlabel('x / x_0')
    ax1.set_ylabel('Energy / hbar*omega')
    ax1.set_title('波函数和能级')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 概率密度
    ax2 = axes[0, 1]
    for n in [0, 1, 2, 5, 10]:
        P = probability_density(n, x, m, omega)
        ax2.plot(x_range, P * x_scale, label=f'n={n}', linewidth=2)

    ax2.set_xlabel('x / x_0')
    ax2.set_ylabel('|psi|^2 * x_0')
    ax2.set_title('概率密度')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 相干态粒子数分布
    ax3 = axes[1, 0]
    alpha_values = [1, 2, 3]

    for alpha in alpha_values:
        state = coherent_state(alpha, 20)
        probs = np.abs(state)**2
        ax3.bar(np.arange(20) + 0.2 * (alpha - 2), probs, width=0.2,
               label=f'alpha={alpha}')

    ax3.set_xlabel('n')
    ax3.set_ylabel('P(n)')
    ax3.set_title('相干态的Poisson分布')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(-0.5, 15)

    # 4. 相空间演化
    ax4 = axes[1, 1]
    alpha_0 = 2 + 1j
    t_range = np.linspace(0, 2 * np.pi / omega, 100)

    Re_alpha = [np.real(coherent_state_evolution(alpha_0, omega, t)) for t in t_range]
    Im_alpha = [np.imag(coherent_state_evolution(alpha_0, omega, t)) for t in t_range]

    ax4.plot(Re_alpha, Im_alpha, 'b-', linewidth=2)
    ax4.scatter([np.real(alpha_0)], [np.imag(alpha_0)], s=100, c='r', marker='o',
               label='t=0', zorder=5)
    ax4.set_xlabel('Re(alpha)')
    ax4.set_ylabel('Im(alpha)')
    ax4.set_title('相干态在相空间的演化')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_aspect('equal')

    plt.tight_layout()
    plt.savefig('qho_ladder.png', dpi=150)
    print("图像已保存为 qho_ladder.png")
    plt.show()


# =============================================================================
# 验证函数
# =============================================================================
def verify():
    """Verify all exercises"""
    all_passed = True
    N_max = 20
    omega = 1e15  # rad/s
    m = m_e

    # Check 1.1 - Ladder operators
    N = number_operator(N_max)
    eigenvalues = np.diag(N)
    expected = np.arange(N_max)
    if not np.allclose(eigenvalues, expected):
        print("X 1.1 粒子数算符错误")
        all_passed = False
    else:
        print("V 1.1 升降算符矩阵正确")

    # Check 1.2 - Hamiltonian
    H = hamiltonian_qho(omega, N_max)
    E_diag = np.diag(H) / hbar / omega
    expected_E = np.arange(N_max) + 0.5
    if not np.allclose(E_diag, expected_E):
        print("X 1.2 哈密顿量错误")
        all_passed = False
    else:
        E_0 = zero_point_energy(omega)
        print(f"V 1.2 能级正确 (E_0 = {E_0/hbar/omega:.1f} hbar*omega)")

    # Check 1.3 - Wave function normalization
    x = np.linspace(-10, 10, 1000) * np.sqrt(hbar / (m * omega))
    dx = x[1] - x[0]
    for n in [0, 1, 2]:
        psi = qho_wavefunction(n, x, m, omega)
        norm = np.sum(np.abs(psi)**2) * dx
        if not np.isclose(norm, 1, atol=0.01):
            print(f"X 1.3 n={n} 波函数未归一化")
            all_passed = False
            break
    else:
        print("V 1.3 波函数归一化正确")

    # Check 1.4 - Commutation relations
    if not verify_commutation_a_adag(N_max):
        print("X 1.4 [a, a^+] = 1 验证失败")
        all_passed = False
    else:
        print("V 1.4 对易关系正确 [a, a^+] = 1")

    # Check 1.5 - Coherent state
    alpha = 2 + 1j
    if not verify_coherent_eigenvalue(alpha, N_max):
        print("X 1.5 相干态验证失败")
        all_passed = False
    else:
        mean_n = coherent_state_mean_n(alpha)
        print(f"V 1.5 相干态正确 (alpha={alpha}, <n>={mean_n:.1f})")

    # Check 1.6 - Uncertainty relation
    n = 0
    delta_x = uncertainty_x(m, omega, n)
    delta_p = uncertainty_p(m, omega, n)
    product = delta_x * delta_p
    if product < hbar / 2 - 1e-40:
        print("X 1.6 不确定性关系错误")
        all_passed = False
    else:
        print(f"V 1.6 不确定性关系正确 (Delta_x * Delta_p = {product/hbar:.2f} hbar)")

    # Check 1.7 - Time evolution
    period = 2 * np.pi / omega
    state_0 = np.zeros(N_max, dtype=complex)
    state_0[0] = 1  # 基态

    state_T = evolved_state(state_0, omega, period, N_max)
    # 经过一个周期后应该回到原态（可能有整体相位）
    phase = np.exp(-1j * omega * period / 2)  # 零点能相位
    if not np.allclose(state_T, phase * state_0, atol=1e-6):
        print("X 1.7 时间演化错误")
        all_passed = False
    else:
        print("V 1.7 时间演化正确")

    if all_passed:
        print("\n所有测试通过！正在生成可视化...")
        try:
            plot_quantum_harmonic_oscillator()
        except Exception as e:
            print(f"可视化生成失败: {e}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("量子谐振子 Quantum Harmonic Oscillator")
    print("=" * 50)
    verify()
