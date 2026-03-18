"""
量子谐振子 Quantum Harmonic Oscillator
难度 Difficulty: ★★★★

物理背景 Physical Background:
--------------------------
量子谐振子是量子力学中最重要的模型之一，原因如下：
1. 任何势能函数在极小值附近都可近似为谐振子势
2. 晶格振动（声子）本质上是量子谐振子
3. 电磁场的量子化也基于谐振子（光子）

谐振子的量子化导致几个关键结果：
- 能级量子化且等间距：E_n = (n + 1/2)*hbar*omega
- 零点能存在：E_0 = hbar*omega/2 > 0
- 基态达到不确定性原理的下界：Delta_x * Delta_p = hbar/2

升降算符方法（代数方法）：
- 降算符: a|n> = sqrt(n)|n-1>（湮灭一个能量量子）
- 升算符: a^dagger|n> = sqrt(n+1)|n+1>（产生一个能量量子）
- 数算符: N = a^dagger * a，N|n> = n|n>

学习目标 Learning Objectives:
--------------------------
1. 掌握量子谐振子能级公式和波函数表达式
2. 理解零点能的物理意义（不确定性原理的结果）
3. 熟练使用升降算符求解问题
4. 理解相干态及其经典对应
5. 分析波函数的时间演化

关键公式 Key Formulas:
--------------------
- 能级: E_n = (n + 1/2)*hbar*omega
- 特征长度: x_0 = sqrt(hbar/(m*omega))
- 波函数: psi_n(x) = N_n * H_n(x/x_0) * exp(-x^2/(2x_0^2))
- 升降算符: a = (x/x_0 + i*p*x_0/hbar)/sqrt(2)
- 相干态: |alpha> = exp(-|alpha|^2/2) * sum_n (alpha^n/sqrt(n!)) |n>
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import hermite
from math import factorial
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import hbar, m_e

# I AM NOT DONE

# =============================================================================
# 练习 4.1: 能级
# Exercise 4.1: Energy Levels
# -----------------------------------------------------------------------------
# 物理背景：谐振子能级是等间距的，间隔为 hbar*omega
# 这与经典谐振子频率 omega 相同，是对应原理的体现
#
# 能级特点：
# - 基态能量 E_0 = hbar*omega/2 > 0（零点能）
# - 相邻能级间隔 Delta_E = hbar*omega = h*f（普朗克假设！）
# - n 可解释为"能量量子"的数目
# =============================================================================
def energy_level(n, omega):
    """
    计算量子谐振子第 n 能级的能量

    公式: E_n = (n + 1/2) * hbar * omega

    参数 Parameters:
        n: 量子数（非负整数 n = 0, 1, 2, ...）
        omega: 角频率 (rad/s)

    返回 Returns:
        E_n: 能量 (J)

    物理意义：
    - n=0 是基态，能量为 hbar*omega/2（不是零！）
    - n 可理解为谐振子中激发的能量量子数目
    - 等间距能级使谐振子在量子场论中特别重要
    """
    # TODO: 根据公式计算能级
    return (n + 0.5) * hbar * omega


def zero_point_energy(omega):
    """
    计算零点能 Calculate zero-point energy

    公式: E_0 = hbar*omega/2

    物理意义：
    - 即使在绝对零度，谐振子仍有能量（零点涨落）
    - 这是不确定性原理的直接结果：粒子不能同时静止于势阱底部
    - Delta_x * Delta_p >= hbar/2 禁止了零能态
    """
    return 0.5 * hbar * omega


# =============================================================================
# 练习 4.2: 波函数
# Exercise 4.2: Wave Functions
# -----------------------------------------------------------------------------
# 物理背景：谐振子波函数由厄米多项式乘以高斯包络组成
#
# 波函数结构：psi_n(x) = N_n × H_n(xi) × exp(-xi^2/2)
# 其中：
# - N_n 是归一化常数
# - H_n 是厄米多项式（决定节点数）
# - exp(-xi^2/2) 是高斯包络（保证波函数衰减）
# - xi = x/x_0 是无量纲坐标
#
# 波函数特点：
# - 第 n 态有 n 个节点
# - 基态 n=0 是纯高斯函数，无节点
# - 高能态波函数更加展开
# =============================================================================
def characteristic_length(m, omega):
    """
    计算谐振子的特征长度

    公式: x_0 = sqrt(hbar/(m*omega))

    物理意义：
    - x_0 是基态波函数的特征宽度
    - 量子涨落使粒子平均偏离平衡位置约 x_0
    - x_0 定义了从量子区域到经典区域的尺度
    """
    return np.sqrt(hbar / (m * omega))


def hermite_polynomial(n, x):
    """
    计算厄米多项式 H_n(x)

    厄米多项式由 scipy.special.hermite 返回的多项式对象计算

    前几个厄米多项式：
    - H_0(x) = 1
    - H_1(x) = 2x
    - H_2(x) = 4x^2 - 2
    - H_3(x) = 8x^3 - 12x

    厄米多项式的节点数等于其阶数 n
    """
    H = hermite(n)  # 返回多项式对象
    return H(x)


def harmonic_wavefunction(n, x, m, omega):
    """
    计算谐振子第 n 态的波函数

    公式: psi_n(x) = (m*omega/(pi*hbar))^(1/4) × (1/sqrt(2^n * n!))
                     × H_n(xi) × exp(-xi^2/2)
    其中无量纲坐标 xi = x/x_0 = x*sqrt(m*omega/hbar)

    参数 Parameters:
        n: 量子数（n = 0, 1, 2, ...）
        x: 位置数组 (m)
        m: 粒子质量 (kg)
        omega: 角频率 (rad/s)

    返回 Returns:
        psi: 波函数数组

    归一化条件：integral |psi_n|^2 dx = 1
    正交性：integral psi_m* psi_n dx = delta_{mn}
    """
    x0 = characteristic_length(m, omega)
    xi = x / x0  # 无量纲坐标

    # 归一化常数
    norm = (m * omega / (np.pi * hbar))**0.25 / np.sqrt(2**n * factorial(n))

    # 波函数 = 归一化常数 × 厄米多项式 × 高斯包络
    H_n = hermite_polynomial(n, xi)
    psi = norm * H_n * np.exp(-xi**2 / 2)

    return psi


# =============================================================================
# 练习 4.3: 升降算符
# Exercise 4.3: Ladder Operators
# -----------------------------------------------------------------------------
# 物理背景：升降算符是量子谐振子的代数方法的核心
#
# 定义：
# a = (x/x_0 + i*p*x_0/hbar) / sqrt(2)  （降算符/湮灭算符）
# a^dagger = (x/x_0 - i*p*x_0/hbar) / sqrt(2)  （升算符/产生算符）
#
# 对易关系：[a, a^dagger] = 1
#
# 作用规则：
# a|n> = sqrt(n)|n-1>  （降低一个能级）
# a^dagger|n> = sqrt(n+1)|n+1>  （升高一个能级）
# a|0> = 0  （基态被湮灭算符作用得零）
#
# 哈密顿量：H = hbar*omega*(a^dagger*a + 1/2) = hbar*omega*(N + 1/2)
# =============================================================================
def lowering_operator_coefficient(n):
    """
    计算降算符作用在 |n> 上的系数

    公式: a|n> = sqrt(n)|n-1>

    参数 Parameters:
        n: 初态的量子数

    返回 Returns:
        sqrt(n): 系数（n=0时返回0）

    物理意义：降算符"湮灭"一个能量量子
    对基态作用得零：a|0> = 0（没有能量量子可以湮灭）
    """
    if n == 0:
        return 0  # 基态被降算符湮灭
    return np.sqrt(n)


def raising_operator_coefficient(n):
    """
    计算升算符作用在 |n> 上的系数

    公式: a^dagger|n> = sqrt(n+1)|n+1>

    参数 Parameters:
        n: 初态的量子数

    返回 Returns:
        sqrt(n+1): 系数

    物理意义：升算符"产生"一个能量量子
    从真空态（基态）可以产生任意激发态：
    |n> = (a^dagger)^n / sqrt(n!) |0>
    """
    return np.sqrt(n + 1)


def number_operator_expectation(n):
    """
    计算数算符在 |n> 态中的期望值

    公式: <n|N|n> = <n|a^dagger * a|n> = n

    数算符 N = a^dagger * a 的本征值正好是量子数 n
    这就是 n 被称为"粒子数"或"量子数"的原因

    能量可写成：E_n = hbar*omega*(n + 1/2)
    """
    return n


# =============================================================================
# 练习 4.4: 位置和动量算符
# Exercise 4.4: Position and Momentum Operators
# -----------------------------------------------------------------------------
# 物理背景：位置和动量期望值及其涨落
#
# 由对称性：
# <x> = 0（波函数关于原点对称或反对称）
# <p> = 0（同样的对称性理由）
#
# 方差（涨落）：
# <x^2> = (n + 1/2) * hbar/(m*omega) = (n + 1/2) * x_0^2
# <p^2> = (n + 1/2) * m*hbar*omega = (n + 1/2) * (hbar/x_0)^2
#
# 不确定性乘积：
# Delta_x * Delta_p = (n + 1/2) * hbar >= hbar/2
# 基态 n=0 恰好达到海森堡不确定性下界！
# =============================================================================
def position_expectation(n, m, omega):
    """
    计算位置期望值

    公式: <x> = 0（对所有本征态）

    物理意义：由于势能 V(x) = (1/2)m*omega^2*x^2 关于 x=0 对称，
    波函数的概率分布也关于原点对称，因此 <x> = 0
    """
    return 0


def position_variance(n, m, omega):
    """
    计算位置方差（位置平方的期望值）

    公式: <x^2> = (n + 1/2) * hbar/(m*omega) = (n + 1/2) * x_0^2

    参数 Parameters:
        n: 量子数
        m: 粒子质量 (kg)
        omega: 角频率 (rad/s)

    返回 Returns:
        <x^2>: 位置方差 (m^2)

    物理意义：粒子位置涨落的大小，随 n 增加而增大
    Delta_x = sqrt(<x^2>) = x_0 * sqrt(n + 1/2)
    """
    return (n + 0.5) * hbar / (m * omega)


def momentum_variance(n, m, omega):
    """
    计算动量方差（动量平方的期望值）

    公式: <p^2> = (n + 1/2) * m*hbar*omega

    参数 Parameters:
        n: 量子数
        m: 粒子质量 (kg)
        omega: 角频率 (rad/s)

    返回 Returns:
        <p^2>: 动量方差 (kg^2·m^2/s^2)

    注意：能量 E = <p^2>/(2m) + (1/2)m*omega^2*<x^2>
          = (n+1/2)*hbar*omega/2 + (n+1/2)*hbar*omega/2
          = (n+1/2)*hbar*omega（动能和势能各占一半！）
    """
    return (n + 0.5) * m * hbar * omega


def uncertainty_product(n):
    """
    计算不确定性乘积 Delta_x * Delta_p

    公式: Delta_x * Delta_p = (n + 1/2) * hbar

    参数 Parameters:
        n: 量子数

    返回 Returns:
        不确定性乘积 (J·s)

    物理意义：
    - 基态 n=0: Delta_x * Delta_p = hbar/2（达到海森堡下界！）
    - 激发态: Delta_x * Delta_p > hbar/2（超过下界）

    谐振子基态是"最小不确定态"的典型例子
    """
    return (n + 0.5) * hbar


# =============================================================================
# 练习 4.5: 相干态
# Exercise 4.5: Coherent States
# -----------------------------------------------------------------------------
# 物理背景：相干态是"最接近经典"的量子态
#
# 相干态定义：降算符的本征态 a|alpha> = alpha|alpha>
# 展开式：|alpha> = exp(-|alpha|^2/2) * sum_n (alpha^n/sqrt(n!)) |n>
#
# 相干态的特殊性质：
# 1. 粒子数分布是泊松分布：P(n) = |alpha|^(2n) * exp(-|alpha|^2) / n!
# 2. 平均粒子数：<n> = |alpha|^2
# 3. 位置和动量期望值随时间作简谐振动（经典运动！）
# 4. 不确定性关系达到下界：Delta_x * Delta_p = hbar/2（与 alpha 无关）
#
# 应用：激光场是相干态的近似
# =============================================================================
def coherent_state_amplitude(alpha, n_max=50):
    """
    计算相干态在数态基底 |n> 上的展开系数

    公式: |alpha> = exp(-|alpha|^2/2) * sum_n (alpha^n/sqrt(n!)) |n>
    系数: c_n = exp(-|alpha|^2/2) * alpha^n / sqrt(n!)

    参数 Parameters:
        alpha: 相干态参数（复数），|alpha|^2 是平均粒子数
        n_max: 展开截断（包含足够多的项以保证精度）

    返回 Returns:
        coefficients: 各能级的概率幅数组

    概率分布：P(n) = |c_n|^2 是泊松分布，均值为 |alpha|^2
    """
    coefficients = []
    norm = np.exp(-np.abs(alpha)**2 / 2)  # 归一化因子

    for n in range(n_max):
        c_n = norm * alpha**n / np.sqrt(factorial(n))
        coefficients.append(c_n)

    return np.array(coefficients)


def coherent_state_wavefunction(alpha, x, m, omega):
    """
    计算相干态的位置空间波函数

    相干态是多个定态的叠加：psi(x) = sum_n c_n * psi_n(x)

    参数 Parameters:
        alpha: 相干态参数
        x: 位置数组 (m)
        m: 粒子质量 (kg)
        omega: 角频率 (rad/s)

    返回 Returns:
        psi: 波函数数组（复数）

    相干态波函数是高斯波包，中心在 <x> = sqrt(2*hbar/(m*omega)) * Re(alpha)
    """
    amplitudes = coherent_state_amplitude(alpha)
    psi = np.zeros_like(x, dtype=complex)

    for n, c_n in enumerate(amplitudes):
        psi += c_n * harmonic_wavefunction(n, x, m, omega)

    return psi


def coherent_state_mean_n(alpha):
    """
    计算相干态的平均粒子数（平均能量量子数）

    公式: <n> = <alpha|N|alpha> = |alpha|^2

    参数 Parameters:
        alpha: 相干态参数

    返回 Returns:
        <n>: 平均粒子数

    物理意义：
    - |alpha| 越大，平均粒子数越多，态越"经典"
    - alpha = 0 对应真空态（基态）
    """
    return np.abs(alpha)**2


# =============================================================================
# 练习 4.6: 时间演化
# Exercise 4.6: Time Evolution
# -----------------------------------------------------------------------------
# 物理背景：量子态的时间演化由薛定谔方程决定
#
# 对于能量本征态：|n, t> = exp(-i*E_n*t/hbar) |n>
# 对于一般叠加态：|psi(t)> = sum_n c_n * exp(-i*E_n*t/hbar) |n>
#
# 相干态的时间演化特别有趣：
# - 位置期望值作简谐振动：<x(t)> = <x(0)>*cos(omega*t) + <p(0)>/(m*omega)*sin(omega*t)
# - 不确定性保持不变：Delta_x(t) = Delta_x(0)
# - 相干态在时间演化下保持为相干态！（只是 alpha 参数旋转）
#
# 这就是为什么相干态被称为"最经典"的量子态
# =============================================================================
def wavefunction_time_evolution(psi_0_coeffs, omega, t):
    """
    计算波函数的时间演化

    公式: |psi(t)> = sum_n c_n * exp(-i*E_n*t/hbar) |n>

    参数 Parameters:
        psi_0_coeffs: 初态在数态基底的展开系数数组
        omega: 角频率 (rad/s)
        t: 时间 (s)

    返回 Returns:
        evolved_coeffs: 演化后的展开系数数组

    物理意义：
    - 每个本征态获得相位因子 exp(-i*E_n*t/hbar)
    - 不同能级的相位演化速度不同
    - 这导致波包的形状可能随时间变化（除了相干态等特殊情况）
    """
    evolved_coeffs = []
    for n, c_n in enumerate(psi_0_coeffs):
        E_n = energy_level(n, omega)
        phase = np.exp(-1j * E_n * t / hbar)  # 时间演化相位因子
        evolved_coeffs.append(c_n * phase)
    return np.array(evolved_coeffs)


def coherent_state_oscillation(alpha, omega, t):
    """
    计算相干态位置期望值的时间演化（归一化形式）

    公式: <x(t)>/sqrt(2*hbar/(m*omega)) = |alpha| * cos(omega*t - phi)
    其中 phi = arg(alpha) 是 alpha 的相位

    参数 Parameters:
        alpha: 相干态参数
        omega: 角频率 (rad/s)
        t: 时间 (s)

    返回 Returns:
        归一化的位置期望值

    物理意义：
    - 相干态的位置期望值作简谐振动
    - 振动频率正是经典频率 omega
    - 振幅与 |alpha| 成正比
    - 这正是经典谐振子的行为！
    """
    phase = np.angle(alpha)  # alpha 的相位角
    amplitude = np.abs(alpha)
    return amplitude * np.cos(omega * t - phase)


# =============================================================================
# 可视化
# =============================================================================
def plot_quantum_harmonic_oscillator():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    m = m_e
    omega = 1e15  # rad/s
    x0 = characteristic_length(m, omega)
    x = np.linspace(-5*x0, 5*x0, 500)

    # 1. 波函数
    ax1 = axes[0, 0]
    for n in range(5):
        psi = harmonic_wavefunction(n, x, m, omega)
        offset = energy_level(n, omega) / (hbar * omega)
        ax1.plot(x/x0, np.abs(psi)**2 * x0 + offset, label=f'n={n}')
        ax1.axhline(y=offset, color='gray', linestyle='--', alpha=0.3)

    ax1.set_xlabel('x/x₀')
    ax1.set_ylabel('|ψ|² + E_n/(ℏω)')
    ax1.set_title('谐振子波函数')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 概率密度
    ax2 = axes[0, 1]
    for n in [0, 1, 5, 10]:
        psi = harmonic_wavefunction(n, x, m, omega)
        ax2.plot(x/x0, np.abs(psi)**2 * x0, label=f'n={n}', linewidth=2)

    ax2.set_xlabel('x/x₀')
    ax2.set_ylabel('|ψ|² × x₀')
    ax2.set_title('概率密度')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 相干态
    ax3 = axes[0, 2]
    for alpha in [1, 2, 3]:
        psi = coherent_state_wavefunction(alpha, x, m, omega)
        ax3.plot(x/x0, np.abs(psi)**2 * x0, label=f'α={alpha}', linewidth=2)

    ax3.set_xlabel('x/x₀')
    ax3.set_ylabel('|ψ|² × x₀')
    ax3.set_title('相干态波函数')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 相干态的粒子数分布
    ax4 = axes[1, 0]
    for alpha in [1, 2, 3]:
        coeffs = coherent_state_amplitude(alpha, n_max=20)
        probs = np.abs(coeffs)**2
        ax4.bar(np.arange(len(probs)) + (alpha-2)*0.25, probs, width=0.25,
               label=f'α={alpha}', alpha=0.7)

    ax4.set_xlabel('n')
    ax4.set_ylabel('P(n)')
    ax4.set_title('相干态粒子数分布（泊松分布）')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 不确定性
    ax5 = axes[1, 1]
    n_range = range(20)
    delta_x = [np.sqrt(position_variance(n, m, omega)) / x0 for n in n_range]
    delta_p = [np.sqrt(momentum_variance(n, m, omega)) * x0 / hbar for n in n_range]
    product = [uncertainty_product(n) / hbar for n in n_range]

    ax5.plot(n_range, delta_x, 'b-', label='Δx/x₀', linewidth=2)
    ax5.plot(n_range, delta_p, 'r-', label='Δp·x₀/ℏ', linewidth=2)
    ax5.plot(n_range, product, 'g--', label='Δx·Δp/ℏ', linewidth=2)
    ax5.axhline(y=0.5, color='k', linestyle=':', alpha=0.5, label='最小不确定性')
    ax5.set_xlabel('n')
    ax5.set_ylabel('不确定性')
    ax5.set_title('不确定性关系')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. 相干态振荡
    ax6 = axes[1, 2]
    alpha = 3
    t = np.linspace(0, 4*np.pi/omega, 200)
    x_mean = [coherent_state_oscillation(alpha, omega, ti) for ti in t]

    ax6.plot(t * omega, x_mean, 'b-', linewidth=2)
    ax6.set_xlabel('ωt')
    ax6.set_ylabel('⟨x⟩/√(2ℏ/mω)')
    ax6.set_title('相干态的经典振荡')
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('quantum_harmonic_oscillator.png', dpi=150)
    print("图像已保存为 quantum_harmonic_oscillator.png")
    plt.show()


def verify():
    """验证所有练习的正确性 Verify all exercises"""
    all_passed = True

    omega = 1e15  # 角频率 rad/s
    m = m_e       # 电子质量

    # 检查 4.1 - 能级间距
    E_0 = energy_level(0, omega)
    E_1 = energy_level(1, omega)
    if not np.isclose(E_1 - E_0, hbar * omega, rtol=0.01):
        print("错误 4.1: 能级间距应为 hbar*omega")
        print(f"  计算得到 Delta_E = {(E_1-E_0)/(hbar*omega):.4f} * hbar*omega")
        all_passed = False
    else:
        print(f"通过 4.1: 能级正确 (Delta_E = hbar*omega)")

    # 检查 4.2 - 波函数归一化
    x0 = characteristic_length(m, omega)
    x = np.linspace(-5*x0, 5*x0, 1000)
    psi_0 = harmonic_wavefunction(0, x, m, omega)
    norm = np.trapz(np.abs(psi_0)**2, x)
    if not np.isclose(norm, 1, rtol=0.01):
        print("错误 4.2: 波函数未正确归一化")
        print(f"  integral |psi|^2 dx = {norm:.4f}，应为 1")
        all_passed = False
    else:
        print("通过 4.2: 波函数归一化正确")

    # 检查 4.3 - 升算符系数
    if raising_operator_coefficient(0) != 1:
        print("错误 4.3: 升算符系数错误")
        print(f"  a^dagger|0> 的系数应为 sqrt(1) = 1")
        all_passed = False
    else:
        print("通过 4.3: 升降算符正确")

    # 检查 4.4 - 基态不确定性乘积
    delta_x_sq = position_variance(0, m, omega)
    delta_p_sq = momentum_variance(0, m, omega)
    product = np.sqrt(delta_x_sq * delta_p_sq)
    if not np.isclose(product, hbar/2, rtol=0.01):
        print("错误 4.4: 基态不确定性乘积应为 hbar/2（最小不确定态）")
        print(f"  计算得到 Delta_x * Delta_p = {product/hbar:.4f} * hbar")
        all_passed = False
    else:
        print("通过 4.4: 不确定性关系正确（基态达到最小值 hbar/2）")

    # 检查 4.5 - 相干态平均粒子数
    alpha = 2
    mean_n = coherent_state_mean_n(alpha)
    if not np.isclose(mean_n, 4, rtol=0.01):
        print("错误 4.5: 相干态平均粒子数应为 |alpha|^2")
        print(f"  alpha=2 时 <n> 应为 4，计算得到 {mean_n}")
        all_passed = False
    else:
        print(f"通过 4.5: 相干态正确 (<n> = |alpha|^2 = {mean_n})")

    # 检查 4.6 - 时间演化
    coeffs = coherent_state_amplitude(alpha)
    T = 2 * np.pi / omega  # 周期
    evolved = wavefunction_time_evolution(coeffs, omega, T)
    if len(evolved) == 0:
        print("错误 4.6: 时间演化计算失败")
        all_passed = False
    else:
        print("通过 4.6: 时间演化正确")

    if all_passed:
        print("\n所有测试通过！正在生成可视化...")
        try:
            plot_quantum_harmonic_oscillator()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("量子谐振子 Quantum Harmonic Oscillator")
    print("=" * 50)
    verify()
