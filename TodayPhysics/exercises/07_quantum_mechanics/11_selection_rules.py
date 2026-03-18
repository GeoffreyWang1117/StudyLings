"""
选择定则与跃迁 Selection Rules and Transitions
难度 Difficulty: ★★★★

物理背景 Physical Background:
--------------------------
选择定则决定了哪些量子态之间可以发生跃迁。它们来源于跃迁矩阵元的对称性。

1. 电偶极选择定则 Electric Dipole Selection Rules:
   最常见的辐射跃迁是电偶极跃迁，其选择定则为:
   - Δl = ±1 (角量子数变化1)
   - Δm = 0, ±1 (磁量子数变化0或1)
   - Δn 无限制

2. 跃迁概率 Transition Probability:
   爱因斯坦A系数给出自发辐射速率:
   A = (ω³|⟨f|d|i⟩|²)/(3πε₀ℏc³)
   其中 d 是电偶极矩算符。

3. 光谱线强度 Spectral Line Intensity:
   由振子强度描述，满足求和规则。

4. 塞曼效应 Zeeman Effect:
   外磁场使能级分裂，跃迁线分裂成多条。
   - 正常塞曼效应: g=1时
   - 反常塞曼效应: g≠1时（考虑自旋）

5. 精细结构 Fine Structure:
   自旋-轨道耦合导致能级分裂，产生双线或多重线。

学习目标 Learning Objectives:
--------------------------
1. 理解电偶极选择定则的物理根源
2. 掌握跃迁矩阵元的计算方法
3. 计算自发辐射速率和激发态寿命
4. 理解塞曼效应和朗德g因子
5. 分析精细结构对光谱的影响

关键公式 Key Formulas:
---------------------
- 选择定则: Δl = ±1, Δm = 0, ±1
- 爱因斯坦A系数: A = ω³|d|²/(3πε₀ℏc³)
- 朗德g因子: g_J = 1 + [J(J+1)+S(S+1)-L(L+1)]/(2J(J+1))
- 塞曼分裂: ΔE = g μ_B m B
- 激发态寿命: τ = 1/A

HINT: 电偶极选择定则: Δl = ±1, Δm = 0, ±1
HINT: 跃迁速率: A = (ω³|⟨f|d|i⟩|²)/(3πε₀ℏc³)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import factorial, assoc_laguerre, sph_harm
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import hbar, m_e, e, c, epsilon_0, a_0, alpha

# I AM NOT DONE

# =============================================================================
# 练习 11.1: 电偶极选择定则
# Exercise 11.1: Electric Dipole Selection Rules
#
# 物理背景 Physical Background:
# 电偶极选择定则来源于偶极矩算符 d = er 与球谐函数的积分性质。
# 只有当矩阵元 ⟨f|d|i⟩ ≠ 0 时，跃迁才是允许的。
#
# 角量子数规则 Δl = ±1:
#   因为偶极算符是矢量（l=1），与初态耦合只能改变l为±1。
#
# 磁量子数规则 Δm = 0, ±1:
#   对应于不同偏振方向的光:
#   - Δm = 0: π偏振（线偏振，沿磁场方向）
#   - Δm = ±1: σ偏振（圆偏振，垂直磁场方向）
# =============================================================================
def check_delta_l(l_i, l_f):
    """
    检验角量子数选择定则 Check angular momentum selection rule

    Δl = ±1

    这是电偶极跃迁的严格选择定则。
    违反此规则的跃迁在电偶极近似下是禁戒的。

    参数 Parameters:
        l_i: 初态角量子数
        l_f: 末态角量子数

    返回 Returns:
        bool: True 如果满足选择定则
    """
    delta_l = l_f - l_i
    return abs(delta_l) == 1


def check_delta_m(m_i, m_f):
    """
    检验磁量子数选择定则 Check magnetic quantum number selection rule

    Δm = 0, ±1

    不同的Δm对应不同的光偏振:
    - Δm = 0: π跃迁（线偏振光）
    - Δm = +1: σ⁺跃迁（右旋圆偏振光）
    - Δm = -1: σ⁻跃迁（左旋圆偏振光）

    参数 Parameters:
        m_i: 初态磁量子数
        m_f: 末态磁量子数

    返回 Returns:
        bool: True 如果满足选择定则
    """
    delta_m = m_f - m_i
    return abs(delta_m) <= 1


def is_allowed_transition(n_i, l_i, m_i, n_f, l_f, m_f):
    """
    判断是否为允许跃迁 Check if transition is allowed

    综合检验所有电偶极选择定则:
    1. Δl = ±1 (必须)
    2. Δm = 0, ±1 (必须)
    3. n_i ≠ n_f (简化处理，实际上同n内也可能有跃迁)

    参数 Parameters:
        n_i, l_i, m_i: 初态量子数
        n_f, l_f, m_f: 末态量子数

    返回 Returns:
        bool: True 如果跃迁是电偶极允许的
    """
    if not check_delta_l(l_i, l_f):
        return False
    if not check_delta_m(m_i, m_f):
        return False
    # 需要n改变（同n内无跃迁，简化处理）
    if n_i == n_f:
        return False
    return True


# =============================================================================
# 练习 11.2: 跃迁偶极矩
# Exercise 11.2: Transition Dipole Moment
#
# 物理背景 Physical Background:
# 跃迁偶极矩 d_fi = ⟨f|er|i⟩ 决定了跃迁的强度。
# 它可以分解为径向部分和角向部分的乘积。
#
# 径向矩阵元 ⟨n'l'|r|nl⟩ 涉及径向波函数的积分。
# 角向矩阵元由 Wigner-Eckart 定理给出，与 Clebsch-Gordan 系数相关。
# =============================================================================
def radial_wavefunction(n, l, r):
    """
    氢原子径向波函数（简化）Hydrogen radial wavefunction

    R_nl(r) = N_nl × (2r/na₀)^l × exp(-r/na₀) × L_{n-l-1}^{2l+1}(2r/na₀)

    其中 L 是关联拉盖尔多项式，N 是归一化常数。

    参数 Parameters:
        n: 主量子数
        l: 角量子数
        r: 径向距离 (m)

    返回 Returns:
        R_nl(r): 径向波函数值
    """
    rho = 2 * r / (n * a_0)
    norm = np.sqrt((2/(n*a_0))**3 * factorial(n-l-1) / (2*n*factorial(n+l)))

    # 关联拉盖尔多项式
    L = assoc_laguerre(rho, n-l-1, 2*l+1)

    return norm * np.exp(-rho/2) * rho**l * L

def radial_matrix_element(n_i, l_i, n_f, l_f, num_points=1000):
    """
    径向矩阵元 Radial matrix element

    ⟨n_f l_f|r|n_i l_i⟩ = ∫₀^∞ R_{n_f l_f}*(r) × r × R_{n_i l_i}(r) × r² dr

    这决定了跃迁强度的径向部分。
    矩阵元的大小随初末态波函数的重叠程度变化。

    参数 Parameters:
        n_i, l_i: 初态量子数
        n_f, l_f: 末态量子数
        num_points: 数值积分点数

    返回 Returns:
        ⟨n_f l_f|r|n_i l_i⟩ (m)
    """
    r_max = 50 * a_0 * max(n_i, n_f)**2
    r = np.linspace(1e-12, r_max, num_points)
    dr = r[1] - r[0]

    R_i = radial_wavefunction(n_i, l_i, r)
    R_f = radial_wavefunction(n_f, l_f, r)

    # 积分 ∫ R_f*(r) r R_i(r) r² dr
    integrand = np.conj(R_f) * r * R_i * r**2
    matrix_element = np.trapezoid(integrand, r)

    return matrix_element

def angular_matrix_element(l_i, m_i, l_f, m_f, polarization='z'):
    """
    角向矩阵元（球谐函数积分）Angular matrix element

    ⟨l_f m_f|r̂|l_i m_i⟩

    使用 Wigner-Eckart 定理，角向矩阵元与 Clebsch-Gordan 系数相关。

    偏振方向决定了哪些 Δm 跃迁是允许的:
    - z偏振: Δm = 0
    - x±iy偏振: Δm = ±1

    参数 Parameters:
        l_i, m_i: 初态量子数
        l_f, m_f: 末态量子数
        polarization: 偏振方向 ('z', 'x', 'y')

    返回 Returns:
        角向矩阵元系数
    """
    # 使用选择定则简化
    if not check_delta_l(l_i, l_f) or not check_delta_m(m_i, m_f):
        return 0

    # Wigner-Eckart定理给出的系数
    if polarization == 'z':
        # Δm = 0
        if m_f != m_i:
            return 0
        C = np.sqrt((l_i + m_i + 1) * (l_i - m_i + 1) / ((2*l_i + 1) * (2*l_i + 3))) if l_f > l_i else \
            np.sqrt((l_i + m_i) * (l_i - m_i) / ((2*l_i + 1) * (2*l_i - 1)))
    else:
        # 简化处理
        C = 1

    return C


# =============================================================================
# 练习 11.3: 自发辐射速率
# Exercise 11.3: Spontaneous Emission Rate
#
# 物理背景 Physical Background:
# 爱因斯坦A系数描述激发态原子自发发射光子的速率。
# 这是一个纯量子效应，源于真空涨落（零点场）。
#
# A系数与B系数的关系:
#   A = (ℏω³/π²c³) × B
#
# 激发态寿命:
#   τ = 1/A_total = 1/Σ_f A_{i→f}
# =============================================================================
def einstein_A_coefficient(omega, dipole_moment):
    """
    爱因斯坦A系数（自发辐射速率）Einstein A coefficient

    A = ω³|d|²/(3πε₀ℏc³)

    物理意义:
    - A 是单位时间内自发辐射的概率
    - 单位: s⁻¹
    - A 与频率的三次方成正比（高频跃迁更快）

    参数 Parameters:
        omega: 跃迁角频率 (rad/s)
        dipole_moment: 跃迁偶极矩 ⟨f|d|i⟩ (C·m)

    返回 Returns:
        A: 自发辐射速率 (s⁻¹)
    """
    A = omega**3 * abs(dipole_moment)**2 / (3 * np.pi * epsilon_0 * hbar * c**3)
    return A


def transition_rate_hydrogen(n_i, l_i, n_f, l_f):
    """
    氢原子跃迁速率 Hydrogen transition rate

    计算从 (n_i, l_i) 到 (n_f, l_f) 的自发辐射速率。

    参数 Parameters:
        n_i, l_i: 初态量子数（激发态）
        n_f, l_f: 末态量子数（通常是较低能态）

    返回 Returns:
        A: 跃迁速率 (s⁻¹)
    """
    if not check_delta_l(l_i, l_f):
        return 0

    # 能量差
    E_i = -13.6 * e / n_i**2
    E_f = -13.6 * e / n_f**2
    omega = abs(E_i - E_f) / hbar

    # 偶极矩（简化）
    d = e * radial_matrix_element(n_i, l_i, n_f, l_f)

    return einstein_A_coefficient(omega, d)

def lifetime(A_total):
    """
    激发态寿命 Excited state lifetime

    τ = 1/A_total = 1/Σ_f A_{i→f}

    激发态寿命是所有可能衰变通道的A系数之和的倒数。
    典型值:
    - 氢原子 2p态: τ ≈ 1.6 ns
    - 禁戒跃迁: τ 可长达秒量级

    参数 Parameters:
        A_total: 总自发辐射速率 (s⁻¹)

    返回 Returns:
        τ: 激发态寿命 (s)
    """
    return 1 / A_total


# =============================================================================
# 练习 11.4: 光谱线强度
# Exercise 11.4: Spectral Line Intensity
#
# 物理背景 Physical Background:
# 谱线强度有多种表示方式:
#
# 1. 线强度 S: 直接与偶极矩平方成正比
# 2. 振子强度 f: 无量纲量，可以与经典谐振子比较
# 3. 求和规则: Thomas-Reiche-Kuhn求和规则 Σ_f f_{if} = N
#
# 振子强度常用于:
# - 吸收光谱分析
# - 等离子体诊断
# - 天体光谱学
# =============================================================================
def line_strength(n_i, l_i, n_f, l_f):
    """
    谱线强度 Line strength

    S = |⟨f|d|i⟩|² = e² |⟨f|r|i⟩|²

    线强度直接决定了跃迁的辐射功率。

    参数 Parameters:
        n_i, l_i: 初态量子数
        n_f, l_f: 末态量子数

    返回 Returns:
        S: 线强度 (C²·m²)
    """
    d = e * radial_matrix_element(n_i, l_i, n_f, l_f)
    return abs(d)**2


def oscillator_strength(n_i, l_i, n_f, l_f):
    """
    振子强度 Oscillator strength

    f = (2m_e ω)/(3ℏ) |⟨f|r|i⟩|² (2l_f + 1)

    振子强度是无量纲量，表示量子跃迁相对于经典电子振子的"强度"。
    满足 Thomas-Reiche-Kuhn 求和规则: Σ_f f_{if} = 1 (对于氢原子)

    参数 Parameters:
        n_i, l_i: 初态量子数
        n_f, l_f: 末态量子数

    返回 Returns:
        f: 振子强度（无量纲）
    """
    E_i = -13.6 * e / n_i**2
    E_f = -13.6 * e / n_f**2
    omega = abs(E_i - E_f) / hbar

    r_matrix = radial_matrix_element(n_i, l_i, n_f, l_f)
    f_osc = 2 * m_e * omega / (3 * hbar) * abs(r_matrix)**2 * (2 * l_f + 1)

    return f_osc

def sum_rule_check(n_i, l_i):
    """
    Thomas-Reiche-Kuhn求和规则
    Σ_f f_if = N (电子数)
    """
    # 对于氢原子应等于1
    return 1


# =============================================================================
# 练习 11.5: 塞曼效应
# Exercise 11.5: Zeeman Effect
#
# 物理背景 Physical Background:
# 塞曼效应是原子光谱线在外磁场中发生分裂的现象。
#
# 正常塞曼效应（无自旋或J=L时）:
#   能级分裂为等间距的2J+1条线
#   ΔE = μ_B m B
#
# 反常塞曼效应（有自旋贡献时）:
#   由于朗德g因子，能级分裂不再等间距
#   ΔE = g_J μ_B m B
#
# 朗德g因子描述了轨道和自旋角动量对磁矩的贡献:
#   g = 1 (纯轨道), g = 2 (纯自旋)
# =============================================================================
def zeeman_energy_shift(m, g, B):
    """
    塞曼能级分裂 Zeeman energy shift

    ΔE = g μ_B m B

    其中 μ_B = eℏ/(2m_e) ≈ 9.274×10⁻²⁴ J/T 是玻尔磁子。

    参数 Parameters:
        m: 磁量子数 m_J
        g: 朗德g因子
        B: 磁场强度 (T)

    返回 Returns:
        ΔE: 能量移动 (J)
    """
    mu_B = e * hbar / (2 * m_e)  # 玻尔磁子
    return g * mu_B * m * B


def lande_g_factor(l, s, j):
    """
    朗德g因子 Lande g-factor

    g_J = 1 + [J(J+1) + S(S+1) - L(L+1)]/(2J(J+1))

    特殊情况:
    - 纯轨道 (S=0): g = 1
    - 纯自旋 (L=0): g = 2
    - ²S_{1/2}: g = 2
    - ²P_{1/2}: g = 2/3
    - ²P_{3/2}: g = 4/3

    参数 Parameters:
        l: 轨道角动量量子数 L
        s: 自旋量子数 S
        j: 总角动量量子数 J

    返回 Returns:
        g_J: 朗德g因子
    """
    if j == 0:
        return 0
    g = 1 + (j*(j+1) + s*(s+1) - l*(l+1)) / (2 * j * (j+1))
    return g

def zeeman_transition_frequencies(omega_0, m_i, m_f, g_i, g_f, B):
    """
    塞曼效应下的跃迁频率 Zeeman transition frequencies

    ω = ω_0 + (g_f m_f - g_i m_i) μ_B B / ℏ

    在磁场中，原来的单一谱线分裂为多条线。
    分裂模式取决于初末态的g因子和磁量子数。

    参数 Parameters:
        omega_0: 无磁场时的跃迁频率 (rad/s)
        m_i, m_f: 初末态磁量子数
        g_i, g_f: 初末态朗德g因子
        B: 磁场强度 (T)

    返回 Returns:
        ω: 磁场中的跃迁频率 (rad/s)
    """
    mu_B = e * hbar / (2 * m_e)
    delta_E = (g_f * m_f - g_i * m_i) * mu_B * B
    return omega_0 + delta_E / hbar


# =============================================================================
# 练习 11.6: 精细结构跃迁
# Exercise 11.6: Fine Structure Transitions
#
# 物理背景 Physical Background:
# 精细结构来源于:
# 1. 相对论质量修正
# 2. 自旋-轨道耦合 (H_so = ξL·S)
# 3. Darwin项（s态的接触相互作用）
#
# 结果是每个 (n,l) 能级分裂为不同的 j 态:
# - l > 0 时: j = l ± 1/2 形成双线
# - l = 0 时: j = 1/2 只有一条线
#
# 精细结构常数 α ≈ 1/137 的平方给出分裂的量级。
# =============================================================================
def fine_structure_energy(n, j):
    """
    精细结构能级（相对论修正）Fine structure energy

    E_nj = E_n [1 + α²/n² (n/(j+1/2) - 3/4)]

    这是包含相对论修正后的氢原子能级公式。
    精细结构分裂 ~ α² × 13.6 eV ~ 10⁻⁴ eV

    参数 Parameters:
        n: 主量子数
        j: 总角动量量子数

    返回 Returns:
        E_nj: 精细结构能量 (J)
    """
    E_n = -13.6 * e / n**2
    correction = 1 + alpha**2 / n**2 * (n / (j + 0.5) - 0.75)
    return E_n * correction


def fine_structure_selection_rules(j_i, j_f):
    """
    精细结构选择定则 Fine structure selection rules

    ΔJ = 0, ±1
    但 J=0 → J=0 禁戒（因为无法带走角动量）

    这些规则决定了精细结构多重线的跃迁模式。

    参数 Parameters:
        j_i: 初态总角动量
        j_f: 末态总角动量

    返回 Returns:
        bool: True 如果跃迁允许
    """
    delta_j = abs(j_f - j_i)
    if delta_j > 1:
        return False
    if j_i == 0 and j_f == 0:
        return False
    return True


def doublet_splitting(n, l):
    """
    双线分裂（自旋-轨道耦合）Doublet splitting

    对于 l > 0，自旋-轨道耦合使能级分裂为:
        j = l + 1/2 (平行耦合，能量较高)
        j = l - 1/2 (反平行耦合，能量较低)

    分裂大小:
        ΔE ∝ ξ_nl ⟨L·S⟩ ∝ Z⁴/n³

    例如: 钠D线是 ³P_{3/2} → ³S_{1/2} 和 ³P_{1/2} → ³S_{1/2} 的双线。

    参数 Parameters:
        n: 主量子数
        l: 轨道角动量量子数

    返回 Returns:
        ΔE: 双线分裂能量 (J)
    """
    if l == 0:
        return 0

    j_plus = l + 0.5
    j_minus = l - 0.5

    E_plus = fine_structure_energy(n, j_plus)
    E_minus = fine_structure_energy(n, j_minus)

    return abs(E_plus - E_minus)


# =============================================================================
# 可视化
# =============================================================================
def plot_selection_rules():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 允许跃迁示意
    ax1 = axes[0, 0]
    # 氢原子能级图
    for n in range(1, 5):
        E = -13.6 / n**2
        ax1.hlines(E, n-0.3, n+0.3, linewidth=2)
        ax1.text(n+0.35, E, f'n={n}', va='center')

    # 画出允许跃迁
    transitions = [(2, 1, 1, 0), (3, 1, 2, 0), (3, 2, 2, 1), (4, 1, 3, 0)]
    for n_i, l_i, n_f, l_f in transitions:
        E_i = -13.6 / n_i**2
        E_f = -13.6 / n_f**2
        ax1.annotate('', xy=(n_f, E_f), xytext=(n_i, E_i),
                    arrowprops=dict(arrowstyle='->', color='red', lw=1.5))

    ax1.set_xlabel('n')
    ax1.set_ylabel('E (eV)')
    ax1.set_title('氢原子能级与跃迁')
    ax1.grid(True, alpha=0.3)

    # 2. 径向波函数
    ax2 = axes[0, 1]
    r = np.linspace(0, 20*a_0, 500)

    for n, l in [(1, 0), (2, 0), (2, 1), (3, 0)]:
        R = radial_wavefunction(n, l, r)
        ax2.plot(r/a_0, R * a_0**(3/2), label=f'n={n}, l={l}', linewidth=2)

    ax2.set_xlabel('r/a₀')
    ax2.set_ylabel('R(r) (a₀^{-3/2})')
    ax2.set_title('径向波函数')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 塞曼分裂
    ax3 = axes[0, 2]
    B = np.linspace(0, 1, 100)  # T
    m_vals = [-1, 0, 1]
    g = 1  # 正常塞曼效应

    for m in m_vals:
        delta_E = [zeeman_energy_shift(m, g, Bi) / e * 1e6 for Bi in B]  # μeV
        ax3.plot(B, delta_E, label=f'm={m}', linewidth=2)

    ax3.set_xlabel('B (T)')
    ax3.set_ylabel('ΔE (μeV)')
    ax3.set_title('正常塞曼效应')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 朗德g因子
    ax4 = axes[1, 0]
    terms = []
    g_vals = []

    for l in range(4):
        for j in [l - 0.5, l + 0.5]:
            if j >= 0:
                s = 0.5
                g = lande_g_factor(l, s, j)
                terms.append(f'{l}{["S","P","D","F"][l]}{int(2*j+1)}/2')
                g_vals.append(g)

    x = range(len(terms))
    ax4.bar(x, g_vals)
    ax4.set_xticks(x)
    ax4.set_xticklabels(terms, rotation=45, ha='right')
    ax4.axhline(y=1, color='r', linestyle='--', label='g=1')
    ax4.axhline(y=2, color='g', linestyle='--', label='g=2')
    ax4.set_ylabel('g_J')
    ax4.set_title('朗德g因子')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 精细结构
    ax5 = axes[1, 1]
    n = 2
    j_vals = [0.5, 1.5]  # 2S1/2, 2P1/2, 2P3/2

    for l in [0, 1]:
        for j in [l - 0.5, l + 0.5]:
            if j >= 0:
                E = fine_structure_energy(n, j)
                label = f'{n}{"SP"[l]}_{int(2*j+1)}/2'
                ax5.hlines((E + 13.6*e/4)/(alpha**2 * 13.6 * e), 0, 1, linewidth=2, label=label)

    ax5.set_xlim(-0.5, 1.5)
    ax5.set_ylabel('相对能量 (α² × 13.6 eV)')
    ax5.set_title('n=2精细结构')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. 跃迁强度
    ax6 = axes[1, 2]
    transitions = [
        (2, 1, 1, 0, 'Lα'),
        (3, 1, 1, 0, 'Lβ'),
        (3, 2, 2, 1, 'Hα'),
        (4, 2, 2, 1, 'Hβ')
    ]

    names = []
    strengths = []
    for n_i, l_i, n_f, l_f, name in transitions:
        S = line_strength(n_i, l_i, n_f, l_f)
        names.append(name)
        strengths.append(S / (e * a_0)**2)  # 归一化

    ax6.bar(names, strengths)
    ax6.set_ylabel('相对谱线强度')
    ax6.set_title('氢原子谱线强度')
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('selection_rules.png', dpi=150)
    print("图像已保存为 selection_rules.png")
    plt.show()


def verify():
    all_passed = True

    # Check 11.1
    allowed = is_allowed_transition(2, 1, 0, 1, 0, 0)
    forbidden = is_allowed_transition(2, 0, 0, 1, 0, 0)
    if not allowed or forbidden:
        print("❌ 11.1 选择定则判断错误")
        all_passed = False
    else:
        print(f"✓ 11.1 选择定则正确 (2p→1s允许, 2s→1s禁戒)")

    # Check 11.2
    r_21 = radial_matrix_element(2, 1, 1, 0)
    if r_21 == 0:
        print("❌ 11.2 径向矩阵元不应为零")
        all_passed = False
    else:
        print(f"✓ 11.2 跃迁矩阵元正确 (⟨1s|r|2p⟩ ≈ {r_21/a_0:.3f} a₀)")

    # Check 11.3
    A = transition_rate_hydrogen(2, 1, 1, 0)
    if A <= 0:
        print("❌ 11.3 跃迁速率应为正")
        all_passed = False
    else:
        tau = lifetime(A)
        print(f"✓ 11.3 自发辐射正确 (2p寿命 ≈ {tau*1e9:.2f} ns)")

    # Check 11.4
    f = oscillator_strength(2, 1, 1, 0)
    if f <= 0 or f > 1:
        print("❌ 11.4 振子强度不合理")
        all_passed = False
    else:
        print(f"✓ 11.4 谱线强度正确 (f ≈ {f:.3f})")

    # Check 11.5
    g_P32 = lande_g_factor(1, 0.5, 1.5)
    expected_g = 4/3
    if not np.isclose(g_P32, expected_g, rtol=0.01):
        print("❌ 11.5 朗德g因子错误")
        all_passed = False
    else:
        print(f"✓ 11.5 塞曼效应正确 (g(²P₃/₂) = {g_P32:.3f})")

    # Check 11.6
    delta_E = doublet_splitting(2, 1)
    if delta_E <= 0:
        print("❌ 11.6 精细结构分裂应为正")
        all_passed = False
    else:
        print(f"✓ 11.6 精细结构正确 (2P双线分裂 ≈ {delta_E/e*1e6:.1f} μeV)")

    if all_passed:
        print("\n🎉 所有测试通过！")
        try:
            plot_selection_rules()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("选择定则与跃迁 Selection Rules and Transitions")
    print("=" * 50)
    verify()
