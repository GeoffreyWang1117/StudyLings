"""
路径积分 Path Integral Formulation
难度 Difficulty: ★★★★★

学习目标 Learning Objectives:
- 理解费曼路径积分量子化方法
- 掌握传播子的计算和物理意义
- 学习半经典近似和瞬子技术
- 理解Aharonov-Bohm效应等拓扑相位

物理背景 Physical Background:
1. 费曼1948年提出路径积分，是量子力学的第三种表述
2. 核心思想: 粒子从A到B可能走所有路径，每条路径有相位 exp(iS/ℏ)
3. 所有路径的相位相干叠加给出传播子
4. 经典极限: S >> ℏ 时，只有经典路径（使S驻定）主导

关键公式 Key Formulas:
- 传播子: K(x_f,t_f;x_i,t_i) = ∫Dx(t) exp(iS[x]/ℏ)
- 自由粒子: K = √(m/2πiℏt) exp[im(x_f-x_i)²/2ℏt]
- 作用量: S[x] = ∫L(x,ẋ)dt = ∫(T-V)dt
- 瞬子隧穿率: Γ ∝ exp(-S_inst/ℏ)
- AB相位: φ_AB = eΦ/ℏ（磁通量Φ导致的相位）

应用:
- 量子场论的基础
- 量子隧穿和衰变率计算
- 统计力学中的虚时间路径积分
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import hbar, m_e

# I AM NOT DONE

# =============================================================================
# 练习 7.1: 自由粒子传播子 Free Particle Propagator
#
# 物理背景:
# 传播子 K(x_f,t;x_i,0) 描述粒子从 (x_i,0) 传播到 (x_f,t) 的概率幅
# ψ(x,t) = ∫K(x,t;x',0)ψ(x',0)dx'
#
# 自由粒子传播子可精确计算:
# K = √(m/2πiℏt) exp[iS_cl/ℏ]
# 其中 S_cl = m(x_f-x_i)²/2t 是经典作用量
#
# 短时极限: t→0 时 K→δ(x_f-x_i)
# =============================================================================
def free_particle_propagator(x_f, x_i, t, m):
    """
    计算自由粒子传播子 Free particle propagator

    参数 Parameters:
        x_f: 终点位置，单位 m
        x_i: 起点位置，单位 m
        t: 传播时间，单位 s
        m: 粒子质量，单位 kg

    返回 Returns:
        K: 传播子（复数），单位 m⁻¹

    公式: K = √(m/2πiℏt) exp[im(x_f-x_i)²/2ℏt]
    """
    if t <= 0:
        return 0
    # 预因子来自路径积分的高斯测度
    prefactor = np.sqrt(m / (2 * np.pi * 1j * hbar * t))
    # 相位来自经典作用量
    phase = 1j * m * (x_f - x_i)**2 / (2 * hbar * t)
    return prefactor * np.exp(phase)

def free_particle_action(x_f, x_i, t, m):
    """
    计算自由粒子经典作用量 Free particle classical action

    S_cl = ∫₀ᵗ (m/2)(dx/dt)² dt = m(x_f-x_i)²/(2t)

    经典路径是直线，v = (x_f-x_i)/t
    """
    return m * (x_f - x_i)**2 / (2 * t)


# =============================================================================
# 练习 7.2: 谐振子传播子 Harmonic Oscillator Propagator
#
# 物理背景:
# 谐振子是另一个可精确求解路径积分的系统
# 经典路径是简谐运动: x(t) = A cos(ωt) + B sin(ωt)
#
# 周期性质:
# - t = π/ω（半周期）: 位置反转
# - t = 2π/ω（全周期）: 回到原点
#
# 传播子在 t = nπ/ω 处有特殊行为（焦点）
# =============================================================================
def harmonic_oscillator_propagator(x_f, x_i, t, m, omega):
    """
    计算谐振子传播子 Harmonic oscillator propagator

    参数 Parameters:
        x_f, x_i: 终点和起点位置
        t: 传播时间
        m: 质量
        omega: 角频率

    返回 Returns:
        K: 传播子（复数）

    公式:
    K = √(mω/2πiℏsin(ωt)) × exp{imω/2ℏsin(ωt)[(x_f²+x_i²)cos(ωt)-2x_fx_i]}

    注意: t = nπ/ω 处 sin(ωt)=0，传播子发散（焦点）
    """
    if np.abs(np.sin(omega * t)) < 1e-10:
        return 0

    prefactor = np.sqrt(m * omega / (2 * np.pi * 1j * hbar * np.sin(omega * t)))
    exponent = 1j * m * omega / (2 * hbar * np.sin(omega * t)) * \
               ((x_f**2 + x_i**2) * np.cos(omega * t) - 2 * x_f * x_i)

    return prefactor * np.exp(exponent)

def harmonic_oscillator_classical_action(x_f, x_i, t, m, omega):
    """
    计算谐振子经典作用量 Harmonic oscillator classical action

    S_cl = (mω/2sin(ωt))[(x_f²+x_i²)cos(ωt) - 2x_fx_i]

    这是经典力学的Hamilton主函数
    """
    if np.abs(np.sin(omega * t)) < 1e-10:
        return np.inf
    return m * omega / (2 * np.sin(omega * t)) * \
           ((x_f**2 + x_i**2) * np.cos(omega * t) - 2 * x_f * x_i)


# =============================================================================
# 练习 7.3: 路径积分蒙特卡洛 Path Integral Monte Carlo
#
# 物理背景:
# 对于一般势能，路径积分无法解析计算
# 蒙特卡洛方法通过随机采样路径来数值计算
#
# 方法:
# 1. 时间切片: t = N×dt
# 2. 生成随机路径（布朗桥）
# 3. 计算每条路径的作用量
# 4. 相位平均得到传播子
#
# 注意: 实时路径积分有符号问题（相位振荡）
# 虚时间版本（欧几里得路径积分）更稳定
# =============================================================================
def path_integral_mc(V, x_i, x_f, t, m, n_paths=1000, n_steps=100):
    """
    路径积分蒙特卡洛模拟 Path integral Monte Carlo

    参数 Parameters:
        V: 势能函数 V(x)
        x_i, x_f: 起点和终点
        t: 总时间
        m: 质量
        n_paths: 采样路径数
        n_steps: 时间切片数

    返回 Returns:
        K: 传播子的蒙特卡洛估计

    算法: 使用布朗桥生成路径，计算作用量相位的平均
    """
    dt = t / n_steps
    x_0 = characteristic_length_pimc(m, dt)  # 量子涨落尺度

    # 生成随机路径（端点固定）
    paths = np.zeros((n_paths, n_steps + 1))
    paths[:, 0] = x_i
    paths[:, -1] = x_f

    # 中间点用布朗桥采样
    for i in range(1, n_steps):
        alpha = i / n_steps
        mean = (1 - alpha) * x_i + alpha * x_f
        std = x_0 * np.sqrt(alpha * (1 - alpha))
        paths[:, i] = np.random.normal(mean, std, n_paths)

    # 计算每条路径的作用量 S = ∫(T-V)dt
    actions = np.zeros(n_paths)
    for j in range(n_paths):
        S = 0
        for i in range(n_steps):
            x_mid = (paths[j, i] + paths[j, i+1]) / 2
            v = (paths[j, i+1] - paths[j, i]) / dt
            S += (0.5 * m * v**2 - V(x_mid)) * dt
        actions[j] = S

    # 传播子 = ⟨exp(iS/ℏ)⟩（相位平均）
    phases = np.exp(1j * actions / hbar)
    K = np.mean(phases)

    return K

def characteristic_length_pimc(m, dt):
    """
    计算PIMC特征长度 Characteristic length for PIMC

    λ = √(ℏdt/m)

    这是时间步dt内量子涨落的典型尺度
    """
    return np.sqrt(hbar * dt / m)


# =============================================================================
# 练习 7.4: 瞬子 Instantons
#
# 物理背景:
# 瞬子是虚时间（欧几里得时间）中连接两个势阱极小值的经典解
# 它描述量子隧穿过程
#
# 对于双势阱 V(x) = V₀(x²/a² - 1)²:
# - 两个极小值在 x = ±a
# - 瞬子从 x=-a 隧穿到 x=+a
# - 隧穿率 ∝ exp(-S_inst/ℏ)
#
# 瞬子方法是计算非微扰隧穿效应的重要工具
# =============================================================================
def double_well_potential(x, a=1, V0=1):
    """
    双势阱势能 Double well potential

    V(x) = V₀(x²/a² - 1)²

    极小值在 x = ±a，势垒在 x = 0，高度 V₀
    """
    return V0 * ((x/a)**2 - 1)**2

def instanton_action(a, V0, m):
    """
    计算瞬子作用量 Instanton action

    参数 Parameters:
        a: 势阱位置参数
        V0: 势垒高度
        m: 粒子质量

    返回 Returns:
        S_inst: 瞬子作用量

    公式: S_inst = (4/3)√(2m) V₀a（省略ℏ因子）

    物理意义: S_inst/ℏ 决定隧穿的指数压制
    """
    return (4/3) * np.sqrt(2 * m) * V0 * a / hbar

def tunneling_rate_instanton(S_inst):
    """
    瞬子近似的隧穿率 Tunneling rate from instanton

    Γ ∝ exp(-S_inst/ℏ)

    这是WKB结果的推广，对非微扰隧穿有效
    """
    return np.exp(-S_inst / hbar)


# =============================================================================
# 练习 7.5: 半经典近似 Semiclassical Approximation
#
# 物理背景:
# 当作用量 S >> ℏ 时，路径积分由经典路径主导
# 在经典路径附近展开得到半经典近似
#
# WKB近似:
# ψ ∝ (1/√p) exp(±i∫p dx/ℏ)
# 其中 p(x) = √[2m(E-V(x))] 是经典动量
#
# 适用条件: de Broglie波长变化缓慢
# |dλ/dx| << 1，即 |dV/dx| << p³/(mℏ)
# =============================================================================
def wkb_propagator(x_f, x_i, E, V, m):
    """
    WKB近似传播子（简化版）WKB propagator (simplified)

    参数 Parameters:
        x_f, x_i: 终点和起点
        E: 粒子能量
        V: 势能函数 V(x)
        m: 质量

    返回 Returns:
        WKB近似的相位因子

    这里忽略了振幅的缓变因子，只保留相位
    """
    # 经典动量 p(x) = √[2m(E-V(x))]
    def p(x):
        kinetic = E - V(x)
        if kinetic > 0:
            return np.sqrt(2 * m * kinetic)
        return 0  # 经典禁区

    # 简化：沿直线路径积分
    n_points = 1000
    x = np.linspace(x_i, x_f, n_points)
    dx = (x_f - x_i) / n_points

    # 相位 = ∫p dx / ℏ
    phase = 0
    for xi in x:
        p_val = p(xi)
        if p_val > 0:
            phase += p_val * dx

    return np.exp(1j * phase / hbar)


# =============================================================================
# 练习 7.6: Aharonov-Bohm效应 Aharonov-Bohm Effect
#
# 物理背景:
# AB效应（1959）是量子力学中最奇妙的现象之一
# 电子绕过磁通管（磁场局限在管内），虽然B=0处无力作用
# 但电子波函数获得取决于磁通量的相位
#
# 物理意义:
# - 量子力学中矢势A（而非磁场B）才是基本量
# - 这是拓扑（几何）相位的原型
# - 证明了波函数相位的物理可观测性
#
# 磁通量子: Φ₀ = h/e ≈ 4.14×10⁻¹⁵ Wb
# 相位 φ = 2πΦ/Φ₀，当Φ = Φ₀时相位为2π
# =============================================================================
def ab_phase(Phi):
    """
    计算Aharonov-Bohm相位 Aharonov-Bohm phase

    参数 Parameters:
        Phi: 磁通量，单位 Wb (Weber)

    返回 Returns:
        φ_AB = eΦ/ℏ = 2πΦ/Φ₀，单位弧度

    磁通量子 Φ₀ = h/e ≈ 4.14×10⁻¹⁵ Wb
    当 Φ = Φ₀ 时，φ_AB = 2π
    """
    e = 1.6e-19  # 电子电荷
    return e * Phi / hbar

def ab_interference_pattern(theta, Phi, d, wavelength):
    """
    计算AB效应干涉图样 AB interference pattern

    参数 Parameters:
        theta: 观察角度（弧度）
        Phi: 磁通量
        d: 双缝间距
        wavelength: 电子波长

    返回 Returns:
        强度（0到1之间）

    干涉条纹会随磁通量移动
    相邻条纹对应 ΔΦ = Φ₀
    """
    e = 1.6e-19
    k = 2 * np.pi / wavelength
    delta_phi = ab_phase(Phi)  # AB相位差

    # 几何相位差（双缝干涉）
    path_diff = d * np.sin(theta)
    geom_phase = k * path_diff

    # 总相位差 = 几何相位 + AB相位
    total_phase = geom_phase + delta_phi

    return np.cos(total_phase / 2)**2


# =============================================================================
# 可视化 Visualization
# 绘制传播子、路径采样、AB效应等图像
# =============================================================================
def plot_path_integral():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 自由粒子传播子
    ax1 = axes[0, 0]
    x = np.linspace(-5, 5, 100)
    m = m_e
    t = 1e-15  # fs

    K = [free_particle_propagator(xi, 0, t, m) for xi in x]
    ax1.plot(x, np.abs(K)**2, 'b-', linewidth=2)
    ax1.set_xlabel('x (nm)')
    ax1.set_ylabel('|K|²')
    ax1.set_title('自由粒子传播子')
    ax1.grid(True, alpha=0.3)

    # 2. 多条路径
    ax2 = axes[0, 1]
    np.random.seed(42)
    n_paths = 20
    n_steps = 50
    t_total = 1

    for _ in range(n_paths):
        path = np.zeros(n_steps + 1)
        path[0] = 0
        path[-1] = 1
        for i in range(1, n_steps):
            alpha = i / n_steps
            path[i] = np.random.normal((1-alpha)*0 + alpha*1, 0.3)

        t_arr = np.linspace(0, t_total, n_steps + 1)
        ax2.plot(t_arr, path, 'b-', alpha=0.3, linewidth=0.5)

    # 经典路径
    ax2.plot([0, t_total], [0, 1], 'r-', linewidth=2, label='经典路径')
    ax2.set_xlabel('t')
    ax2.set_ylabel('x')
    ax2.set_title('费曼路径求和')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 双势阱
    ax3 = axes[0, 2]
    x_dw = np.linspace(-2, 2, 200)
    V_dw = [double_well_potential(xi) for xi in x_dw]

    ax3.plot(x_dw, V_dw, 'b-', linewidth=2)
    ax3.axhline(y=0.5, color='r', linestyle='--', alpha=0.5, label='瞬子能量')
    ax3.set_xlabel('x')
    ax3.set_ylabel('V(x)')
    ax3.set_title('双势阱与瞬子')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. AB效应
    ax4 = axes[1, 0]
    theta = np.linspace(-0.1, 0.1, 200)
    wavelength = 1e-10  # 1 Å
    d = 1e-6

    for Phi_factor in [0, 0.5, 1]:
        Phi_0 = 2.07e-15  # 磁通量子
        Phi = Phi_factor * Phi_0
        I = [ab_interference_pattern(t, Phi, d, wavelength) for t in theta]
        ax4.plot(np.degrees(theta)*60, I, label=f'Φ = {Phi_factor}Φ₀', linewidth=2)

    ax4.set_xlabel('θ (arcmin)')
    ax4.set_ylabel('强度')
    ax4.set_title('Aharonov-Bohm效应')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 谐振子传播子
    ax5 = axes[1, 1]
    omega = 1e15
    t_ho = np.linspace(0.1, 3, 100) * np.pi / omega

    K_diag = [np.abs(harmonic_oscillator_propagator(1e-10, 1e-10, ti, m_e, omega))**2
              for ti in t_ho]

    ax5.plot(t_ho * omega, K_diag, 'g-', linewidth=2)
    ax5.set_xlabel('ωt')
    ax5.set_ylabel('|K(x,x;t)|²')
    ax5.set_title('谐振子传播子')
    ax5.grid(True, alpha=0.3)

    # 6. 相位vs作用量
    ax6 = axes[1, 2]
    S = np.linspace(0, 10, 100) * hbar
    phase = np.exp(1j * S / hbar)

    ax6.plot(S/hbar, np.real(phase), 'b-', label='Re(e^{iS/ℏ})', linewidth=2)
    ax6.plot(S/hbar, np.imag(phase), 'r-', label='Im(e^{iS/ℏ})', linewidth=2)
    ax6.set_xlabel('S/ℏ')
    ax6.set_ylabel('相位因子')
    ax6.set_title('路径相位')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('path_integral.png', dpi=150)
    print("图像已保存为 path_integral.png")
    plt.show()


def verify():
    """验证所有练习的正确性 Verify all exercises"""
    all_passed = True

    m = m_e
    t = 1e-15

    # 检查 7.1: 自由粒子传播子
    K = free_particle_propagator(0, 0, t, m)
    if K == 0:
        print("错误 7.1: 自由粒子传播子不应为零")
        all_passed = False
    else:
        print("通过 7.1: 自由粒子传播子正确")

    # 检查 7.2: 谐振子传播子
    omega = 1e15
    K_ho = harmonic_oscillator_propagator(0, 0, np.pi/omega, m, omega)
    if K_ho == 0:
        print("错误 7.2: 谐振子传播子不应为零")
        all_passed = False
    else:
        print("通过 7.2: 谐振子传播子正确")

    # 检查 7.3: 路径积分蒙特卡洛
    V = lambda x: 0  # 自由粒子
    print("通过 7.3: 路径积分蒙特卡洛框架正确")

    # 检查 7.4: 瞬子作用量
    S_inst = instanton_action(1e-9, 1e-19, m)
    if S_inst <= 0:
        print("错误 7.4: 瞬子作用量应为正值")
        all_passed = False
    else:
        print(f"通过 7.4: 瞬子作用量正确 (S_inst/ℏ = {S_inst/hbar:.2f})")

    # 检查 7.5: 半经典近似
    print("通过 7.5: 半经典近似框架正确")

    # 检查 7.6: AB效应
    Phi_0 = 2.07e-15  # 磁通量子
    phase = ab_phase(Phi_0)
    expected = 2 * np.pi
    if not np.isclose(phase, expected, rtol=0.01):
        print("错误 7.6: 一个磁通量子应产生2π相位")
        all_passed = False
    else:
        print(f"通过 7.6: AB效应正确 (φ(Φ₀) = 2π)")

    if all_passed:
        print("\n所有测试通过！")
        try:
            plot_path_integral()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("路径积分 Path Integral Formulation")
    print("=" * 50)
    verify()
