"""
哈密顿力学 Hamiltonian Mechanics
难度 Difficulty: ★★★★★

================================================================================
学习目标 Learning Objectives
================================================================================
- 理解哈密顿量和相空间的概念
  Understand Hamiltonian and phase space concepts
- 掌握正则方程（哈密顿方程）及其对称形式
  Master canonical equations (Hamilton's equations) and their symmetric form
- 分析正则变换、泊松括号和守恒量
  Analyze canonical transformations, Poisson brackets, and conserved quantities
- 理解刘维尔定理和相空间体积守恒
  Understand Liouville's theorem and phase space volume conservation

================================================================================
物理背景 Physical Background
================================================================================
哈密顿力学是经典力学的另一种表述，与拉格朗日力学等价但具有独特优势。

1. 哈密顿量 Hamiltonian:
   H(q, p, t) = Σpᵢq̇ᵢ - L（从拉格朗日量通过勒让德变换得到）
   对于自然系统（不显含时间的约束）: H = T + V = 总能量

2. 正则方程（哈密顿方程）Hamilton's Equations:
   q̇ᵢ = ∂H/∂pᵢ    (广义速度)
   ṗᵢ = -∂H/∂qᵢ   (广义力)
   对称优美的一阶微分方程组（vs 拉格朗日的二阶方程）

3. 相空间 Phase Space:
   - 以(q₁,...,qₙ, p₁,...,pₙ)为坐标的2n维空间
   - 系统状态对应相空间中的一点
   - 时间演化描述相空间中的轨迹

4. 泊松括号 Poisson Brackets:
   {f, g} = Σᵢ(∂f/∂qᵢ·∂g/∂pᵢ - ∂f/∂pᵢ·∂g/∂qᵢ)
   - 基本关系: {qᵢ, pⱼ} = δᵢⱼ, {qᵢ, qⱼ} = {pᵢ, pⱼ} = 0
   - 运动方程: df/dt = {f, H} + ∂f/∂t
   - 守恒量: {f, H} = 0 → f守恒

5. 正则变换 Canonical Transformation:
   保持正则方程形式不变的坐标变换
   - 作用-角变量: 简化周期运动问题
   - 生成函数方法

6. 刘维尔定理 Liouville's Theorem:
   相空间体积在哈密顿流下守恒
   dΓ/dt = 0（统计力学的基础）

HINT: 哈密顿量 H = Σpq̇ - L（勒让德变换）
HINT: 正则方程: q̇ = ∂H/∂p, ṗ = -∂H/∂q
HINT: 泊松括号: {f,g} = Σ(∂f/∂q·∂g/∂p - ∂f/∂p·∂g/∂q)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])

# I AM NOT DONE

g = 9.8  # m/s²

# =============================================================================
# 练习 12.1: 简谐振子的哈密顿量
# Exercise 12.1: Hamiltonian of Simple Harmonic Oscillator
# =============================================================================
# 简谐振子是哈密顿力学的最简单例子
# 相空间中的轨迹是椭圆（等能曲线）

def hamiltonian_sho(q, p, m, omega):
    """
    简谐振子的哈密顿量 SHO Hamiltonian
    H = p²/(2m) + (1/2)mω²q²
      = 动能 + 势能 = 总机械能

    相空间中等能线方程:
    p²/(2mE) + q²/(2E/mω²) = 1（椭圆）

    参数 Parameters:
        q: 广义坐标（位移）[m]
        p: 广义动量 [kg·m/s]
        m: 质量 [kg]
        omega: 角频率 [rad/s]
    返回 Returns:
        哈密顿量（总能量）[J]
    """
    # TODO: 计算哈密顿量（动能 + 势能）
    T = p**2 / (2 * m)  # 动能
    V = 0.5 * m * omega**2 * q**2  # 势能
    H = T + V
    return H


def canonical_equations_sho(state, t, m, omega):
    """
    简谐振子的正则方程 Canonical Equations for SHO

    哈密顿方程（对称形式）:
    q̇ = ∂H/∂p = p/m      (广义速度)
    ṗ = -∂H/∂q = -mω²q   (广义力，取负号)

    这是一阶线性ODE系统，解为谐振动
    """
    q, p = state
    # TODO: 计算哈密顿正则方程的右边
    q_dot = p / m            # ∂H/∂p
    p_dot = -m * omega**2 * q  # -∂H/∂q
    return [q_dot, p_dot]


def simulate_sho_hamiltonian(q0, p0, m, omega, t_span, dt=0.01):
    """
    使用哈密顿方程模拟简谐振子 Simulate SHO using Hamilton's Equations

    初始条件(q₀, p₀)确定相空间中的轨迹
    轨迹沿等能椭圆逆时针运动
    """
    t = np.arange(t_span[0], t_span[1], dt)
    solution = odeint(canonical_equations_sho, [q0, p0], t, args=(m, omega))
    return t, solution[:, 0], solution[:, 1]


# =============================================================================
# 练习 12.2: 单摆的哈密顿量
# Exercise 12.2: Hamiltonian of Simple Pendulum
# =============================================================================
def hamiltonian_pendulum(theta, p_theta, m, L, g=9.8):
    """
    单摆的哈密顿量
    H = p_θ²/(2mL²) + mgL(1 - cos(θ))
    """
    # TODO: 计算哈密顿量
    T = p_theta**2 / (2 * m * L**2)
    V = m * g * L * (1 - np.cos(theta))
    H = T + V
    return H


def canonical_equations_pendulum(state, t, m, L, g=9.8):
    """
    单摆的正则方程
    θ̇ = ∂H/∂p_θ = p_θ/(mL²)
    ṗ_θ = -∂H/∂θ = -mgL sin(θ)
    """
    theta, p_theta = state
    # TODO: 计算导数
    theta_dot = p_theta / (m * L**2)
    p_theta_dot = -m * g * L * np.sin(theta)
    return [theta_dot, p_theta_dot]


def simulate_pendulum_hamiltonian(theta0, p_theta0, m, L, t_span, dt=0.01, g=9.8):
    """使用哈密顿方程模拟单摆"""
    t = np.arange(t_span[0], t_span[1], dt)
    solution = odeint(canonical_equations_pendulum, [theta0, p_theta0], t, args=(m, L, g))
    return t, solution[:, 0], solution[:, 1]


# =============================================================================
# 练习 12.3: 相空间轨迹
# Exercise 12.3: Phase Space Trajectories
# =============================================================================
def phase_portrait_sho(m, omega, energy_levels, q_range):
    """
    绘制简谐振子的相空间等能线
    由 H = E，得到 p = ±√(2m(E - (1/2)mω²q²))
    """
    q = np.linspace(q_range[0], q_range[1], 200)
    trajectories = []

    for E in energy_levels:
        # TODO: 计算给定能量下的动量
        p_squared = 2 * m * (E - 0.5 * m * omega**2 * q**2)
        # 只取物理上有意义的部分
        valid = p_squared >= 0
        q_valid = q[valid]
        p_plus = np.sqrt(p_squared[valid])
        p_minus = -p_plus
        trajectories.append((q_valid, p_plus, p_minus))

    return trajectories


def phase_portrait_pendulum(m, L, energy_levels, theta_range, g=9.8):
    """
    绘制单摆的相空间等能线
    """
    theta = np.linspace(theta_range[0], theta_range[1], 500)
    trajectories = []

    for E in energy_levels:
        # TODO: 计算给定能量下的动量
        # H = p²/(2mL²) + mgL(1-cosθ) = E
        # p² = 2mL²(E - mgL(1-cosθ))
        p_squared = 2 * m * L**2 * (E - m * g * L * (1 - np.cos(theta)))
        valid = p_squared >= 0
        theta_valid = theta[valid]
        p_plus = np.sqrt(p_squared[valid])
        p_minus = -p_plus
        trajectories.append((theta_valid, p_plus, p_minus))

    return trajectories


# =============================================================================
# 练习 12.4: 泊松括号
# Exercise 12.4: Poisson Brackets
# =============================================================================
# 泊松括号是哈密顿力学的核心数学结构
# 它编码了正则变换的代数性质，是量子力学对易子的经典极限

def poisson_bracket_sho(f_q, f_p, g_q, g_p):
    """
    计算泊松括号 Calculate Poisson Bracket

    定义: {f, g} = ∂f/∂q · ∂g/∂p - ∂f/∂p · ∂g/∂q

    性质：
    - 反对称性: {f, g} = -{g, f}
    - 线性: {af + bg, h} = a{f, h} + b{g, h}
    - 莱布尼茨律: {fg, h} = f{g, h} + g{f, h}
    - 雅可比恒等式: {f, {g, h}} + {g, {h, f}} + {h, {f, g}} = 0

    参数 Parameters:
        f_q, f_p: 函数f对q和p的偏导数
        g_q, g_p: 函数g对q和p的偏导数
    返回 Returns:
        泊松括号 {f, g} 的值
    """
    # TODO: 计算泊松括号
    bracket = f_q * g_p - f_p * g_q
    return bracket


def verify_fundamental_brackets():
    """
    验证基本泊松括号关系 Verify Fundamental Poisson Brackets

    正则对易关系（经典版）:
    {qᵢ, pⱼ} = δᵢⱼ  (1 if i=j, 0 otherwise)
    {qᵢ, qⱼ} = 0
    {pᵢ, pⱼ} = 0

    这些关系定义了正则变换的标准
    """
    # {q, p}: q对q的导数=1, q对p的导数=0; p对q的导数=0, p对p的导数=1
    bracket_qp = poisson_bracket_sho(1, 0, 0, 1)

    # {q, q}
    bracket_qq = poisson_bracket_sho(1, 0, 1, 0)

    # {p, p}
    bracket_pp = poisson_bracket_sho(0, 1, 0, 1)

    return bracket_qp, bracket_qq, bracket_pp


def time_evolution_poisson(f_q, f_p, H_q, H_p):
    """
    使用泊松括号计算物理量的时间演化 Time Evolution via Poisson Bracket

    运动方程的泊松括号形式:
    df/dt = {f, H} + ∂f/∂t

    若f不显含时间且{f, H} = 0，则f是守恒量
    这是诺特定理的哈密顿版本
    """
    return poisson_bracket_sho(f_q, f_p, H_q, H_p)


# =============================================================================
# 练习 12.5: 正则变换
# Exercise 12.5: Canonical Transformation
# =============================================================================
# 正则变换是保持哈密顿方程形式不变的相空间坐标变换
# 关键性质: 变换后 {Q, P} = 1 仍成立

def canonical_transform_rotation(q, p, phi):
    """
    相空间旋转 Phase Space Rotation

    这是最简单的正则变换之一:
    Q = q cos(φ) + p sin(φ)
    P = -q sin(φ) + p cos(φ)

    几何意义: 在(q, p)平面上旋转角度φ
    可验证: {Q, P} = 1（正则性）
    """
    # TODO: 计算变换后的坐标
    Q = q * np.cos(phi) + p * np.sin(phi)
    P = -q * np.sin(phi) + p * np.cos(phi)
    return Q, P


def action_angle_sho(q, p, m, omega):
    """
    简谐振子的作用-角变量变换 Action-Angle Variables for SHO

    作用变量: J = E/ω = H/ω（守恒量，与能量成正比）
    角变量: θ = arctan(mωq/p)（等速增长，θ̇ = ω）

    优点：
    - J是守恒量，运动方程极度简化
    - θ随时间线性增长: θ(t) = θ₀ + ωt
    - 适用于微扰理论

    物理意义：
    - J = 相空间椭圆围成的面积/(2π)
    - θ参数化椭圆上的位置
    """
    E = hamiltonian_sho(q, p, m, omega)
    # TODO: 计算作用变量和角变量
    J = E / omega
    theta = np.arctan2(m * omega * q, p)
    return J, theta


def inverse_action_angle_sho(J, theta, m, omega):
    """
    从作用-角变量反变换回 (q, p) Inverse Transformation

    q = √(2J/(mω)) sin(θ)
    p = √(2Jmω) cos(θ)

    这表明相空间轨迹是以J为"半径"的圆
    （适当缩放后）
    """
    # TODO: 计算反变换（作用-角到普通坐标）
    q = np.sqrt(2 * J / (m * omega)) * np.sin(theta)
    p = np.sqrt(2 * J * m * omega) * np.cos(theta)
    return q, p


# =============================================================================
# 练习 12.6: 刘维尔定理
# Exercise 12.6: Liouville's Theorem
# =============================================================================
# 刘维尔定理是哈密顿力学的核心结果
# 它表明相空间体积在哈密顿流下守恒
# 这是统计力学中相空间概率密度守恒的基础

def liouville_volume_evolution(initial_points, m, omega, t_span, dt=0.01):
    """
    验证刘维尔定理 Verify Liouville's Theorem

    原理: 相空间中一团点在哈密顿演化下
    其围成的体积（面积，对于2D）保持不变

    虽然形状可能变形（拉伸、旋转），但体积守恒
    这是因为哈密顿流是不可压缩的: ∇·v = 0

    参数 Parameters:
        initial_points: 初始点集 [(q₁,p₁), (q₂,p₂), ...]
        m, omega: 简谐振子参数
        t_span: 时间范围
        dt: 时间步长
    返回 Returns:
        t: 时间数组
        trajectories: 每个点的轨迹
    """
    t = np.arange(t_span[0], t_span[1], dt)
    trajectories = []

    for q0, p0 in initial_points:
        _, q, p = simulate_sho_hamiltonian(q0, p0, m, omega, t_span, dt)
        trajectories.append(np.column_stack([q, p]))

    return t, trajectories


def compute_phase_area(points):
    """
    计算相空间中多边形的面积 Compute Phase Space Area

    使用鞋带公式（Shoelace Formula）:
    A = (1/2)|Σᵢ(xᵢyᵢ₊₁ - xᵢ₊₁yᵢ)|

    根据刘维尔定理，此面积在哈密顿演化下守恒
    """
    n = len(points)
    if n < 3:
        return 0

    # TODO: 使用鞋带公式计算多边形面积
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += points[i][0] * points[j][1]
        area -= points[j][0] * points[i][1]
    return abs(area) / 2


# =============================================================================
# 练习 12.7: 二维谐振子
# Exercise 12.7: 2D Harmonic Oscillator
# =============================================================================
def hamiltonian_2d_sho(qx, qy, px, py, m, omega_x, omega_y):
    """
    二维谐振子的哈密顿量
    H = px²/(2m) + py²/(2m) + (1/2)mωx²qx² + (1/2)mωy²qy²
    """
    # TODO: 计算哈密顿量
    T = (px**2 + py**2) / (2 * m)
    V = 0.5 * m * (omega_x**2 * qx**2 + omega_y**2 * qy**2)
    H = T + V
    return H


def canonical_equations_2d_sho(state, t, m, omega_x, omega_y):
    """
    二维谐振子的正则方程
    """
    qx, qy, px, py = state
    # TODO: 计算导数
    qx_dot = px / m
    qy_dot = py / m
    px_dot = -m * omega_x**2 * qx
    py_dot = -m * omega_y**2 * qy
    return [qx_dot, qy_dot, px_dot, py_dot]


def simulate_2d_sho(qx0, qy0, px0, py0, m, omega_x, omega_y, t_span, dt=0.01):
    """模拟二维谐振子"""
    t = np.arange(t_span[0], t_span[1], dt)
    initial = [qx0, qy0, px0, py0]
    solution = odeint(canonical_equations_2d_sho, initial, t, args=(m, omega_x, omega_y))
    return t, solution


# =============================================================================
# 可视化
# =============================================================================
def plot_hamiltonian():
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    m, omega = 1.0, 1.0
    L = 1.0

    # 1. 简谐振子相空间
    ax1 = axes[0, 0]
    energy_levels = [0.5, 1.0, 2.0, 4.0]
    trajectories = phase_portrait_sho(m, omega, energy_levels, (-3, 3))
    for i, (q, p_plus, p_minus) in enumerate(trajectories):
        ax1.plot(q, p_plus, 'b-', linewidth=1, label=f'E={energy_levels[i]}' if i==0 else '')
        ax1.plot(q, p_minus, 'b-', linewidth=1)
    ax1.set_xlabel('q')
    ax1.set_ylabel('p')
    ax1.set_title('简谐振子相空间')
    ax1.grid(True, alpha=0.3)
    ax1.set_aspect('equal')

    # 2. 单摆相空间
    ax2 = axes[0, 1]
    # 分离点能量
    E_sep = 2 * m * g * L  # 分离点能量
    energy_levels_pend = [0.5*E_sep, 0.8*E_sep, E_sep, 1.5*E_sep]
    trajectories_pend = phase_portrait_pendulum(m, L, energy_levels_pend, (-np.pi, np.pi))
    for q, p_plus, p_minus in trajectories_pend:
        ax2.plot(q, p_plus, 'r-', linewidth=1)
        ax2.plot(q, p_minus, 'r-', linewidth=1)
    ax2.set_xlabel('θ')
    ax2.set_ylabel('p_θ')
    ax2.set_title('单摆相空间')
    ax2.grid(True, alpha=0.3)

    # 3. 能量守恒验证
    ax3 = axes[0, 2]
    t, q, p = simulate_sho_hamiltonian(1.0, 0.0, m, omega, (0, 20))
    H = [hamiltonian_sho(q[i], p[i], m, omega) for i in range(len(t))]
    ax3.plot(t, H, 'g-', linewidth=2)
    ax3.set_xlabel('t')
    ax3.set_ylabel('H')
    ax3.set_title('哈密顿量守恒')
    ax3.grid(True, alpha=0.3)

    # 4. 相空间轨迹演化
    ax4 = axes[1, 0]
    t, q, p = simulate_sho_hamiltonian(1.5, 0.0, m, omega, (0, 10))
    ax4.plot(q, p, 'b-', linewidth=1.5)
    ax4.plot(q[0], p[0], 'go', markersize=10, label='Start')
    ax4.set_xlabel('q')
    ax4.set_ylabel('p')
    ax4.set_title('相空间轨迹')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_aspect('equal')

    # 5. 作用-角变量
    ax5 = axes[1, 1]
    theta_var = np.linspace(0, 2*np.pi, 100)
    J_val = 1.0
    q_aa, p_aa = inverse_action_angle_sho(J_val, theta_var, m, omega)
    ax5.plot(q_aa, p_aa, 'purple', linewidth=2)
    ax5.set_xlabel('q')
    ax5.set_ylabel('p')
    ax5.set_title('作用-角变量 (J=1)')
    ax5.grid(True, alpha=0.3)
    ax5.set_aspect('equal')

    # 6. 二维谐振子（利萨如图形）
    ax6 = axes[1, 2]
    omega_x, omega_y = 1.0, 2.0  # 频率比 1:2
    t, sol = simulate_2d_sho(1.0, 0.0, 0.0, 2.0, m, omega_x, omega_y, (0, 20))
    ax6.plot(sol[:, 0], sol[:, 1], 'r-', linewidth=1)
    ax6.set_xlabel('qx')
    ax6.set_ylabel('qy')
    ax6.set_title('二维谐振子 (ωx:ωy=1:2)')
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('hamiltonian_mechanics.png', dpi=150)
    print("图像已保存为 hamiltonian_mechanics.png")
    plt.show()


def verify():
    all_passed = True
    m, omega = 1.0, 1.0
    L = 1.0

    # Check 12.1 - 简谐振子哈密顿量
    H_test = hamiltonian_sho(1.0, 1.0, m, omega)
    expected_H = 0.5 * 1.0**2 / m + 0.5 * m * omega**2 * 1.0**2
    if not np.isclose(H_test, expected_H, rtol=0.01):
        print("❌ 12.1 简谐振子哈密顿量错误")
        all_passed = False
    else:
        print(f"✓ 12.1 简谐振子哈密顿量正确 (H = {H_test:.3f})")

    # Check 12.2 - 单摆哈密顿量
    H_pend = hamiltonian_pendulum(np.pi/4, 1.0, m, L)
    if H_pend <= 0:
        print("❌ 12.2 单摆哈密顿量错误")
        all_passed = False
    else:
        print(f"✓ 12.2 单摆哈密顿量正确 (H = {H_pend:.3f})")

    # Check 12.3 - 相空间轨迹和能量守恒
    t, q, p = simulate_sho_hamiltonian(1.0, 0.0, m, omega, (0, 10))
    H_initial = hamiltonian_sho(q[0], p[0], m, omega)
    H_final = hamiltonian_sho(q[-1], p[-1], m, omega)
    if abs(H_final - H_initial) / H_initial > 0.01:
        print("❌ 12.3 能量不守恒")
        all_passed = False
    else:
        print(f"✓ 12.3 相空间演化正确，能量守恒")

    # Check 12.4 - 泊松括号
    bracket_qp, bracket_qq, bracket_pp = verify_fundamental_brackets()
    if not (np.isclose(bracket_qp, 1) and np.isclose(bracket_qq, 0) and np.isclose(bracket_pp, 0)):
        print("❌ 12.4 基本泊松括号关系错误")
        all_passed = False
    else:
        print(f"✓ 12.4 泊松括号正确 ({{q,p}}={bracket_qp}, {{q,q}}={bracket_qq}, {{p,p}}={bracket_pp})")

    # Check 12.5 - 作用-角变量
    q_test, p_test = 1.0, 1.0
    J, theta = action_angle_sho(q_test, p_test, m, omega)
    q_back, p_back = inverse_action_angle_sho(J, theta, m, omega)
    if not (np.isclose(q_back, q_test, rtol=0.01) and np.isclose(p_back, p_test, rtol=0.01)):
        print("❌ 12.5 作用-角变量变换错误")
        all_passed = False
    else:
        print(f"✓ 12.5 作用-角变量正确 (J = {J:.3f})")

    # Check 12.7 - 二维谐振子
    H_2d = hamiltonian_2d_sho(1, 1, 1, 1, m, 1, 2)
    if H_2d <= 0:
        print("❌ 12.7 二维谐振子哈密顿量错误")
        all_passed = False
    else:
        print(f"✓ 12.7 二维谐振子正确 (H = {H_2d:.3f})")

    if all_passed:
        print("\n🎉 所有测试通过！")
        try:
            plot_hamiltonian()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("哈密顿力学 Hamiltonian Mechanics")
    print("=" * 50)
    verify()
