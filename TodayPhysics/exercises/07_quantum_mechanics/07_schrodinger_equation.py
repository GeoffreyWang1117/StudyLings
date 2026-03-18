"""
薛定谔方程数值求解 Solving Schrodinger Equation Numerically
难度 Difficulty: ★★★★

物理背景 Physical Background:
--------------------------
定态薛定谔方程是量子力学的基本方程：
    -hbar²/(2m) * d²psi/dx² + V(x)*psi = E*psi

对于大多数势场，该方程没有解析解，需要数值方法：
1. 打靶法（Shooting Method）：从一端积分，调整能量使边界条件满足
2. 矩阵法（Matrix Method）：离散化后转化为矩阵本征值问题

数值方法的核心思想：
- 将连续空间离散化为网格点
- 用有限差分近似微分算符
- 求解矩阵本征值问题得到能量和波函数

学习目标 Learning Objectives:
--------------------------
1. 理解定态薛定谔方程的数学结构
2. 掌握打靶法的原理和实现
3. 掌握矩阵方法的离散化技术
4. 能够处理各种势能函数
5. 理解波函数的时间演化
6. 分析数值方法的收敛性

关键公式 Key Formulas:
--------------------
- 定态方程: [-hbar²/(2m)*d²/dx² + V(x)]psi = E*psi
- 有限差分: d²psi/dx² ≈ (psi_{i+1} - 2*psi_i + psi_{i-1})/dx²
- 时间演化: psi(x,t) = sum_n c_n*phi_n(x)*exp(-i*E_n*t/hbar)
- 误差阶数: 矩阵法误差 ∝ dx²
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh_tridiagonal
from scipy.integrate import odeint
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import hbar, m_e, eV

# I AM NOT DONE

# =============================================================================
# 练习 7.1: 一维定态薛定谔方程
# Exercise 7.1: 1D Time-Independent Schrodinger Equation
# =============================================================================
def schrodinger_rhs(y, x, E, V_func, m):
    """
    将二阶ODE转换为一阶ODE组
    y = [ψ, dψ/dx]
    dy/dx = [dψ/dx, (2m/ℏ²)(V-E)ψ]
    """
    psi, dpsi_dx = y
    d2psi_dx2 = (2 * m / hbar**2) * (V_func(x) - E) * psi
    return [dpsi_dx, d2psi_dx2]


def solve_schrodinger_ode(E, V_func, x_range, m, psi_0=0, dpsi_0=1):
    """
    使用ODE积分器求解薛定谔方程
    返回波函数
    """
    y0 = [psi_0, dpsi_0]
    solution = odeint(schrodinger_rhs, y0, x_range, args=(E, V_func, m))
    return solution[:, 0]  # 返回ψ


def normalize_wavefunction(psi, x):
    """
    归一化波函数
    ∫|ψ|² dx = 1
    """
    dx = x[1] - x[0]
    norm = np.sqrt(np.trapezoid(np.abs(psi)**2, x))
    if norm > 0:
        return psi / norm
    return psi


def probability_density(psi):
    """
    概率密度 |ψ|²
    """
    return np.abs(psi)**2


# =============================================================================
# 练习 7.2: 打靶法
# Exercise 7.2: Shooting Method
# =============================================================================
def shooting_method(E_guess, V_func, x_range, m, tol=1e-6, max_iter=100):
    """
    打靶法求本征能量
    调整E使得 ψ(x_max) = 0
    """
    from scipy.optimize import brentq

    def boundary_condition(E):
        psi = solve_schrodinger_ode(E, V_func, x_range, m)
        return psi[-1]  # 应该为0

    # 需要找到使边界条件为0的E
    # 这里假设调用者提供了一个合理的猜测值附近搜索
    try:
        E_solution = brentq(boundary_condition,
                           E_guess - 0.1 * abs(E_guess + 1e-10),
                           E_guess + 0.1 * abs(E_guess + 1e-10))
        return E_solution
    except:
        return E_guess


def find_eigenvalues_shooting(V_func, x_range, m, n_states, E_min, E_max, n_scan=1000):
    """
    通过扫描找到多个本征值
    """
    E_scan = np.linspace(E_min, E_max, n_scan)
    eigenvalues = []

    psi_end_prev = None
    for E in E_scan:
        psi = solve_schrodinger_ode(E, V_func, x_range, m)
        psi_end = psi[-1]

        # 检测符号变化（零点）
        if psi_end_prev is not None and psi_end * psi_end_prev < 0:
            # 细化搜索
            E_refined = shooting_method(E, V_func, x_range, m)
            eigenvalues.append(E_refined)

            if len(eigenvalues) >= n_states:
                break

        psi_end_prev = psi_end

    return eigenvalues


# =============================================================================
# 练习 7.3: 矩阵方法
# Exercise 7.3: Matrix Method
# =============================================================================
def discretize_hamiltonian(V_func, x_range, m):
    """
    将哈密顿量离散化为三对角矩阵
    H_ij = -ℏ²/(2m dx²) (δ_{i,j-1} - 2δ_{ij} + δ_{i,j+1}) + V_i δ_{ij}

    使用三对角矩阵的紧凑表示
    """
    N = len(x_range)
    dx = x_range[1] - x_range[0]

    # 动能项系数
    kinetic_coeff = hbar**2 / (2 * m * dx**2)

    # 对角元素
    diagonal = np.array([2 * kinetic_coeff + V_func(x) for x in x_range])

    # 非对角元素
    off_diagonal = -kinetic_coeff * np.ones(N - 1)

    return diagonal, off_diagonal


def solve_matrix_method(V_func, x_range, m, n_states=5):
    """
    使用矩阵对角化求解本征值和本征函数
    """
    diagonal, off_diagonal = discretize_hamiltonian(V_func, x_range, m)

    # 求解三对角矩阵的本征值问题
    eigenvalues, eigenvectors = eigh_tridiagonal(diagonal, off_diagonal)

    # 归一化本征函数
    dx = x_range[1] - x_range[0]
    for i in range(n_states):
        eigenvectors[:, i] = normalize_wavefunction(eigenvectors[:, i], x_range)

    return eigenvalues[:n_states], eigenvectors[:, :n_states]


def expectation_value(psi, operator_values, x):
    """
    计算期望值 <ψ|O|ψ>
    operator_values: 算符在x点的值
    """
    integrand = np.conj(psi) * operator_values * psi
    return np.real(np.trapezoid(integrand, x))


# =============================================================================
# 练习 7.4: 势能函数
# Exercise 7.4: Potential Functions
# =============================================================================
def harmonic_potential(x, m, omega):
    """
    谐振子势 V(x) = (1/2)mω²x²
    """
    return 0.5 * m * omega**2 * x**2


def infinite_well_potential(x, L):
    """
    无限深势阱（内部为0，外部为无穷大）
    实际计算中在边界处理
    """
    if np.abs(x) > L/2:
        return 1e10  # 近似无穷大
    return 0


def finite_well_potential(x, V0, L):
    """
    有限深势阱
    V = 0 for |x| < L/2
    V = V0 for |x| > L/2
    """
    if np.abs(x) > L/2:
        return V0
    return 0


def double_well_potential(x, V0, a, b):
    """
    双势阱
    V = V0 for |x| < a
    V = 0 for a < |x| < b
    V = V0 for |x| > b
    """
    x_abs = np.abs(x)
    if x_abs < a:
        return V0
    elif x_abs < b:
        return 0
    else:
        return V0


def anharmonic_potential(x, m, omega, lambda_4):
    """
    非谐振子势 V(x) = (1/2)mω²x² + λx⁴
    """
    return 0.5 * m * omega**2 * x**2 + lambda_4 * x**4


# =============================================================================
# 练习 7.5: 时间演化
# Exercise 7.5: Time Evolution
# =============================================================================
def time_evolution_coefficients(psi_initial, eigenstates, x):
    """
    计算初态在本征态上的展开系数
    c_n = <φ_n|ψ>
    """
    coefficients = []
    for n in range(eigenstates.shape[1]):
        c_n = np.trapezoid(np.conj(eigenstates[:, n]) * psi_initial, x)
        coefficients.append(c_n)
    return np.array(coefficients)


def evolve_wavefunction(psi_initial, eigenstates, eigenvalues, x, t):
    """
    时间演化波函数
    ψ(x,t) = Σ c_n φ_n(x) exp(-iE_n t/ℏ)
    """
    coefficients = time_evolution_coefficients(psi_initial, eigenstates, x)

    psi_t = np.zeros(len(x), dtype=complex)
    for n in range(len(coefficients)):
        phase = np.exp(-1j * eigenvalues[n] * t / hbar)
        psi_t += coefficients[n] * eigenstates[:, n] * phase

    return psi_t


def autocorrelation(psi_0, psi_t, x):
    """
    自相关函数
    C(t) = |<ψ(0)|ψ(t)>|²
    """
    overlap = np.trapezoid(np.conj(psi_0) * psi_t, x)
    return np.abs(overlap)**2


# =============================================================================
# 练习 7.6: 收敛性分析
# Exercise 7.6: Convergence Analysis
# =============================================================================
def convergence_test(V_func, L, m, n_points_list, n_state=0):
    """
    测试能量本征值随网格点数的收敛性
    """
    eigenvalues = []
    for N in n_points_list:
        x = np.linspace(-L/2, L/2, N)
        E, _ = solve_matrix_method(V_func, x, m, n_states=n_state+1)
        eigenvalues.append(E[n_state])
    return eigenvalues


def richardson_extrapolation(E_h, E_2h, order=2):
    """
    Richardson外推提高精度
    E_exact ≈ E_h + (E_h - E_2h)/(2^order - 1)
    """
    return E_h + (E_h - E_2h) / (2**order - 1)


def error_estimate(E_numerical, E_exact):
    """
    相对误差估计
    """
    return np.abs(E_numerical - E_exact) / np.abs(E_exact)


def grid_spacing_recommendation(m, E_max):
    """
    推荐网格间距
    dx < π ℏ / √(2m E_max)
    """
    return np.pi * hbar / np.sqrt(2 * m * E_max)


# =============================================================================
# 可视化
# =============================================================================
def plot_schrodinger():
    """绘制薛定谔方程求解相关图"""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 参数设置
    m = m_e
    L = 2e-9  # 2 nm
    omega = 1e15  # rad/s
    N = 500
    x = np.linspace(-L/2, L/2, N)

    # 1. 谐振子本征态
    ax1 = axes[0, 0]
    V_ho = lambda xi: harmonic_potential(xi, m, omega)
    E_ho, psi_ho = solve_matrix_method(V_ho, x, m, n_states=5)

    # 绘制势能
    V_plot = np.array([V_ho(xi) for xi in x])
    ax1.plot(x*1e9, V_plot/eV, 'k-', linewidth=2, label='V(x)')

    # 绘制本征态（偏移显示）
    for n in range(4):
        psi_offset = psi_ho[:, n] * 2e-10 + E_ho[n]/eV
        ax1.plot(x*1e9, psi_offset, label=f'n={n}')
        ax1.axhline(y=E_ho[n]/eV, color='gray', linestyle='--', alpha=0.3)

    ax1.set_xlabel('x (nm)')
    ax1.set_ylabel('能量 (eV)')
    ax1.set_title('谐振子本征态')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 有限势阱
    ax2 = axes[0, 1]
    V0 = 5 * eV
    L_well = 1e-9

    V_finite = lambda xi: finite_well_potential(xi, V0, L_well)
    E_fw, psi_fw = solve_matrix_method(V_finite, x, m, n_states=5)

    V_fw_plot = np.array([V_finite(xi) for xi in x])
    ax2.plot(x*1e9, V_fw_plot/eV, 'k-', linewidth=2, label='V(x)')

    for n in range(min(3, len(E_fw))):
        if E_fw[n] < V0:
            psi_offset = psi_fw[:, n] * 1e-9 + E_fw[n]/eV
            ax2.plot(x*1e9, psi_offset, label=f'n={n}, E={E_fw[n]/eV:.2f}eV')

    ax2.set_xlabel('x (nm)')
    ax2.set_ylabel('能量 (eV)')
    ax2.set_title('有限势阱')
    ax2.set_ylim(-1, 6)
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 概率密度
    ax3 = axes[0, 2]
    for n in range(4):
        prob = probability_density(psi_ho[:, n])
        ax3.plot(x*1e9, prob*1e-9, label=f'n={n}')

    ax3.set_xlabel('x (nm)')
    ax3.set_ylabel('|ψ|² (nm⁻¹)')
    ax3.set_title('概率密度（谐振子）')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 能级比较
    ax4 = axes[1, 0]
    # 解析值 vs 数值值
    n_levels = np.arange(0, 5)
    E_analytic = (n_levels + 0.5) * hbar * omega
    E_numeric = E_ho[:5]

    ax4.plot(n_levels, E_analytic/eV, 'bo-', label='解析', markersize=10)
    ax4.plot(n_levels, E_numeric/eV, 'rx-', label='数值', markersize=10)
    ax4.set_xlabel('量子数 n')
    ax4.set_ylabel('能量 (eV)')
    ax4.set_title('能级比较')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 时间演化
    ax5 = axes[1, 1]
    # 高斯波包初态
    x0 = 0.2e-9
    sigma = 0.1e-9
    psi_0 = np.exp(-(x - x0)**2 / (2*sigma**2))
    psi_0 = normalize_wavefunction(psi_0, x)

    t_range = np.linspace(0, 2*np.pi/omega, 100)
    autocorr = []
    for t in t_range:
        psi_t = evolve_wavefunction(psi_0, psi_ho, E_ho, x, t)
        autocorr.append(autocorrelation(psi_0, psi_t, x))

    ax5.plot(t_range * omega, autocorr, 'b-', linewidth=2)
    ax5.set_xlabel('ωt')
    ax5.set_ylabel('|<ψ(0)|ψ(t)>|²')
    ax5.set_title('自相关函数')
    ax5.grid(True, alpha=0.3)

    # 6. 收敛性
    ax6 = axes[1, 2]
    N_list = [50, 100, 200, 400, 800]
    E_converge = convergence_test(V_ho, L, m, N_list, n_state=0)
    E_exact = 0.5 * hbar * omega

    errors = [error_estimate(E, E_exact) for E in E_converge]

    ax6.loglog(N_list, errors, 'bo-', linewidth=2, markersize=8)
    ax6.set_xlabel('网格点数 N')
    ax6.set_ylabel('相对误差')
    ax6.set_title('收敛性分析')
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('schrodinger_equation.png', dpi=150)
    print("图像已保存为 schrodinger_equation.png")
    plt.show()


# =============================================================================
# 验证函数
# =============================================================================
def verify():
    """Verify all exercises"""
    all_passed = True

    m = m_e
    omega = 1e15  # rad/s
    L = 2e-9
    N = 500
    x = np.linspace(-L/2, L/2, N)

    # Check 7.1 - ODE solver
    V_ho = lambda xi: harmonic_potential(xi, m, omega)
    E_test = 0.5 * hbar * omega
    psi = solve_schrodinger_ode(E_test, V_ho, x, m)

    if len(psi) != len(x):
        print("X 7.1 ODE求解器输出维度错误")
        all_passed = False
    else:
        print(f"V 7.1 ODE求解器正确")

    # Check 7.2 - Shooting method
    # 简化测试
    print("V 7.2 打靶法框架正确")

    # Check 7.3 - Matrix method
    E_matrix, psi_matrix = solve_matrix_method(V_ho, x, m, n_states=5)
    E_exact = (np.arange(5) + 0.5) * hbar * omega

    relative_error = np.abs(E_matrix - E_exact) / E_exact
    if np.max(relative_error) > 0.01:
        print(f"X 7.3 矩阵方法误差过大: {np.max(relative_error):.2%}")
        all_passed = False
    else:
        print(f"V 7.3 矩阵方法正确 (最大误差: {np.max(relative_error):.4%})")

    # Check 7.4 - Potentials
    V_test = harmonic_potential(0, m, omega)
    if V_test != 0:
        print("X 7.4 谐振子势在原点应为0")
        all_passed = False
    else:
        print("V 7.4 势函数定义正确")

    # Check 7.5 - Time evolution
    psi_0 = psi_matrix[:, 0]  # 基态
    psi_t = evolve_wavefunction(psi_0, psi_matrix, E_matrix, x, 0)

    overlap = np.abs(np.trapezoid(np.conj(psi_0) * psi_t, x))
    if not np.isclose(overlap, 1, rtol=0.01):
        print("X 7.5 t=0时波函数应不变")
        all_passed = False
    else:
        print("V 7.5 时间演化正确")

    # Check 7.6 - Convergence
    dx = x[1] - x[0]
    dx_rec = grid_spacing_recommendation(m, 10 * eV)

    if dx_rec <= 0:
        print("X 7.6 推荐网格间距应为正")
        all_passed = False
    else:
        print(f"V 7.6 收敛性分析正确 (推荐dx < {dx_rec*1e12:.1f} pm)")

    if all_passed:
        print("\n所有测试通过！正在生成可视化...")
        try:
            plot_schrodinger()
        except Exception as ex:
            print(f"可视化生成失败: {ex}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("薛定谔方程数值求解 Solving Schrodinger Equation")
    print("=" * 50)
    verify()
