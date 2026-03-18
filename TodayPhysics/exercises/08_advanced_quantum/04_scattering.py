"""
散射理论 Scattering Theory (Born Approximation)
难度 Difficulty: ★★★★★

学习目标 Learning Objectives:
- 理解量子散射的基本概念和物理图像
- 掌握Born近似的推导和适用条件
- 学习分波展开和相移分析方法
- 理解光学定理和低能散射特性

物理背景 Physical Background:
1. 散射是研究粒子相互作用的基本实验手段
2. 入射平面波 + 势场 → 出射平面波 + 散射球面波
3. 散射幅 f(θ) 包含相互作用的全部信息
4. 微分散射截面 dσ/dΩ = |f(θ)|² 是可测量量

关键公式 Key Formulas:
- 散射波函数: ψ ~ e^(ikz) + f(θ)e^(ikr)/r
- 动量转移: q = |k' - k| = 2k sin(θ/2)
- Born近似散射幅: f(θ) = -(2m/ℏ²)∫V(r)sin(qr)/(qr) r²dr
- 分波展开: f(θ) = (1/k)Σ_l (2l+1)e^(iδₗ)sin(δₗ)Pₗ(cosθ)
- 光学定理: σ_total = (4π/k)Im[f(0)]

重要应用:
- 卢瑟福散射: 发现原子核
- 电子散射: 测量核结构
- 中子散射: 材料结构分析
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad, dblquad
from scipy.special import spherical_jn, legendre
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import hbar, m_e, e, epsilon_0, a_0

# I AM NOT DONE

# =============================================================================
# 练习 1.1: 散射动量转移 Momentum Transfer in Scattering
#
# 物理背景:
# 弹性散射中，入射粒子动量为 ℏk，散射后动量为 ℏk'
# 弹性散射保证 |k| = |k'|（能量守恒）
# 动量转移决定了散射幅对势能的傅里叶分量的探测
#
# 几何关系:
# q = |k' - k| = 2k sin(θ/2)
# θ = 0: 前向散射，q = 0
# θ = π: 后向散射，q = 2k（最大动量转移）
# =============================================================================
def momentum_transfer(k, theta):
    """
    计算散射动量转移 Momentum transfer in scattering

    参数 Parameters:
        k: 入射波矢大小，单位 m⁻¹
        theta: 散射角，单位弧度

    返回 Returns:
        q: 动量转移大小，单位 m⁻¹

    公式: q = 2k sin(θ/2)
    物理意义: q 越大，探测的距离尺度越小
    """
    # TODO: 计算动量转移（使用几何关系）
    q = 2 * k * np.sin(theta / 2)
    return q


def energy_to_wavenumber(E, m):
    """
    动能转换为波数 Energy to wavenumber

    参数 Parameters:
        E: 动能，单位 J
        m: 粒子质量，单位 kg

    返回 Returns:
        k: 波数，单位 m⁻¹

    公式: k = √(2mE)/ℏ，来自德布罗意关系
    """
    return np.sqrt(2 * m * E) / hbar


def wavenumber_to_energy(k, m):
    """
    波数转换为动能 Wavenumber to energy

    公式: E = ℏ²k²/(2m)
    """
    return hbar**2 * k**2 / (2 * m)


# =============================================================================
# 练习 1.2: Born近似散射幅 Born Approximation Scattering Amplitude
#
# 物理背景:
# Born近似是弱散射的一阶近似，假设散射波很弱
# 散射幅正比于势能的傅里叶变换
#
# 适用条件:
# - 弱势: V₀ma²/ℏ² << 1
# - 或高能: V₀ma/(ℏ²k) << 1
#
# 对于球对称势 V(r):
# f(θ) = -(2m/ℏ²) ∫₀^∞ V(r) sin(qr)/(q) r dr
# =============================================================================
def born_amplitude_spherical(V_func, k, theta, r_max=10*a_0, n_points=1000):
    """
    计算球对称势的Born近似散射幅 Born amplitude for spherical potential

    参数 Parameters:
        V_func: 势能函数 V(r)，输入r返回势能值
        k: 入射波矢，单位 m⁻¹
        theta: 散射角，单位弧度
        r_max: 积分上限，默认 10a₀

    返回 Returns:
        f: 散射幅，单位 m

    公式: f(θ) = -(2m/ℏ²) ∫V(r) sin(qr)/q · r dr
    """
    q = momentum_transfer(k, theta)

    if q < 1e-10:  # 小角度极限 q→0
        # sin(qr)/q → r，所以 f(0) = -(2m/ℏ²) ∫V(r)r² dr
        def integrand_zero(r):
            return V_func(r) * r**2
        result, _ = quad(integrand_zero, 0, r_max)
        return -(2 * m_e / hbar**2) * result

    # TODO: 计算Born散射幅（数值积分）
    def integrand(r):
        if r < 1e-15:
            return 0
        return V_func(r) * np.sin(q * r) / q * r

    result, _ = quad(integrand, 0, r_max)
    f = -(2 * m_e / hbar**2) * result
    return f


def born_amplitude_yukawa(k, theta, V0, mu):
    """
    Yukawa势的Born近似解析散射幅 Yukawa potential Born amplitude

    Yukawa势: V(r) = V₀ exp(-μr)/r
    描述带屏蔽的核力或介子交换势

    参数 Parameters:
        k: 入射波矢，单位 m⁻¹
        theta: 散射角，单位弧度
        V0: 势能强度，单位 J
        mu: 屏蔽参数（逆程），单位 m⁻¹

    返回 Returns:
        f: 散射幅，单位 m

    解析公式: f(θ) = -2mV₀/[ℏ²(q² + μ²)]
    当 μ→0 时退化为库仑势结果
    """
    q = momentum_transfer(k, theta)

    # TODO: 计算解析散射幅
    f = -2 * m_e * V0 / (hbar**2 * (q**2 + mu**2))
    return f


def born_amplitude_coulomb(k, theta, Z1, Z2):
    """
    库仑势的Born近似散射幅 Coulomb potential Born amplitude

    这给出经典卢瑟福公式的量子版本

    参数 Parameters:
        k: 入射波矢，单位 m⁻¹
        theta: 散射角，单位弧度
        Z1, Z2: 散射粒子和靶核的电荷数

    返回 Returns:
        f: 散射幅，单位 m

    公式: f(θ) = -Z₁Z₂e²m/(2ε₀ℏ²q²)
    注意: 库仑势是长程力，严格来说Born近似需要修正
    """
    q = momentum_transfer(k, theta)
    if q < 1e-10:
        return np.inf  # 前向散射发散

    # TODO: 计算库仑散射幅
    f = -Z1 * Z2 * e**2 * m_e / (2 * epsilon_0 * hbar**2 * q**2)
    return f


# =============================================================================
# 练习 1.3: 散射截面 Scattering Cross Section
#
# 物理背景:
# 散射截面是描述散射概率的有效面积
# - 微分截面 dσ/dΩ: 单位立体角的散射概率
# - 总截面 σ: 所有方向的积分
#
# 卢瑟福散射:
# 1911年盖革-马斯登实验揭示了原子核的存在
# 卢瑟福公式 dσ/dΩ ∝ 1/sin⁴(θ/2) 在小角度发散
# =============================================================================
def differential_cross_section(f):
    """
    计算微分散射截面 Differential cross section

    参数 Parameters:
        f: 散射幅（复数）

    返回 Returns:
        dσ/dΩ = |f(θ)|²，单位 m²/sr

    这是实验可测量的量，表示散射到单位立体角的概率
    """
    return np.abs(f)**2


def rutherford_cross_section(k, theta, Z1, Z2):
    """
    计算卢瑟福散射截面 Rutherford scattering cross section

    参数 Parameters:
        k: 入射波矢，单位 m⁻¹
        theta: 散射角，单位弧度
        Z1, Z2: 电荷数

    返回 Returns:
        dσ/dΩ，单位 m²/sr

    公式: dσ/dΩ = (Z₁Z₂e²/16πε₀E)² / sin⁴(θ/2)

    特点:
    - 小角度发散（库仑力是长程力）
    - 与能量E成反比的平方
    - 与电荷乘积的平方成正比
    """
    E = wavenumber_to_energy(k, m_e)
    if np.sin(theta / 2) < 1e-10:
        return np.inf

    # TODO: 计算Rutherford截面
    prefactor = (Z1 * Z2 * e**2 / (16 * np.pi * epsilon_0 * E))**2
    sigma = prefactor / np.sin(theta / 2)**4
    return sigma


def total_cross_section(f_func, k, n_theta=100):
    """
    计算总散射截面 Total cross section

    参数 Parameters:
        f_func: 散射幅函数 f(k, theta)
        k: 入射波矢
        n_theta: 角度积分点数

    返回 Returns:
        σ_total，单位 m²

    公式: σ = ∫|f(θ)|² dΩ = 2π∫₀^π |f(θ)|² sin(θ) dθ

    物理意义: 总散射概率，与入射通量之比给出散射率
    """
    theta_array = np.linspace(0.001, np.pi - 0.001, n_theta)
    dtheta = theta_array[1] - theta_array[0]

    integrand = [differential_cross_section(f_func(k, theta)) * np.sin(theta)
                 for theta in theta_array]

    sigma = 2 * np.pi * np.sum(integrand) * dtheta
    return sigma


# =============================================================================
# 练习 1.4: 分波展开 Partial Wave Expansion
#
# 物理背景:
# 对于球对称势，波函数可按角动量量子数l展开
# 每个分波有确定的角动量，独立被散射
#
# 物理图像:
# - 入射平面波可展开为球面波 Σ_l (2l+1)i^l j_l(kr) P_l(cosθ)
# - 每个分波被势场移相 δ_l（相移）
# - 散射幅由相移确定
#
# 相移的物理意义:
# - δ_l > 0: 吸引势（波函数被拉进去）
# - δ_l < 0: 排斥势（波函数被推出去）
# =============================================================================
def partial_wave_amplitude(l, delta_l):
    """
    单个分波的散射幅贡献 Partial wave amplitude

    参数 Parameters:
        l: 角动量量子数
        delta_l: 第l个分波的相移

    返回 Returns:
        不含1/k的分波振幅因子

    公式: f_l = (2l+1) e^(iδ_l) sin(δ_l)
    """
    return (2*l + 1) * np.exp(1j * delta_l) * np.sin(delta_l)


def scattering_amplitude_partial_wave(k, theta, delta_list):
    """
    用分波展开计算总散射幅 Total amplitude from partial waves

    参数 Parameters:
        k: 入射波矢
        theta: 散射角
        delta_list: 各分波相移列表 [δ₀, δ₁, δ₂, ...]

    返回 Returns:
        f(θ): 散射幅（复数）

    公式: f(θ) = (1/k) Σ_l (2l+1) e^(iδ_l) sin(δ_l) P_l(cosθ)

    注意: 需要包含足够多的分波（直到 δ_l ≈ 0）
    """
    cos_theta = np.cos(theta)
    f = 0

    for l, delta_l in enumerate(delta_list):
        P_l = legendre(l)(cos_theta)  # 勒让德多项式
        f += (2*l + 1) * np.exp(1j * delta_l) * np.sin(delta_l) * P_l

    return f / k


def phase_shift_hard_sphere(k, a, l):
    """
    计算硬球势的相移 Phase shift for hard sphere potential

    硬球势: V(r) = ∞ (r<a), 0 (r>a)
    边界条件: ψ(a) = 0

    参数 Parameters:
        k: 入射波矢
        a: 硬球半径
        l: 角动量量子数

    返回 Returns:
        δ_l: 第l个分波的相移

    公式:
    - l=0: δ₀ = -ka（s波）
    - 低能近似: δ_l ≈ (ka)^(2l+1) / [(2l+1)!!]²
    """
    ka = k * a

    if l == 0:
        # TODO: 计算s波相移（硬球势的精确结果）
        delta = -ka
    else:
        # 低能近似: 高角动量分波被离心势垒压制
        double_factorial = 1
        for i in range(1, 2*l + 2, 2):
            double_factorial *= i
        delta = ka**(2*l + 1) / double_factorial**2

    return delta


# =============================================================================
# 练习 1.5: 光学定理 Optical Theorem
#
# 物理背景:
# 光学定理是概率守恒（幺正性）的直接结果
# 它联系了前向散射幅与总截面
#
# 物理意义:
# 入射波的减弱（由于散射）必须等于散射到各方向的总流量
# 这反映在前向散射幅的虚部（与入射波的干涉消耗）
#
# 公式: σ_total = (4π/k) Im[f(0)]
# =============================================================================
def optical_theorem_check(f_forward, sigma_total, k):
    """
    验证光学定理 Verify optical theorem

    参数 Parameters:
        f_forward: 前向散射幅 f(θ=0)
        sigma_total: 独立计算的总截面
        k: 入射波矢

    返回 Returns:
        bool: 光学定理是否满足（相对误差<10%）

    光学定理: σ_total = (4π/k) Im[f(0)]
    """
    lhs = sigma_total
    rhs = (4 * np.pi / k) * np.imag(f_forward)

    return np.isclose(lhs, rhs, rtol=0.1)


def total_cross_section_from_forward(f_forward, k):
    """
    用光学定理从前向散射幅计算总截面 Total cross section via optical theorem

    参数 Parameters:
        f_forward: 前向散射幅 f(0)（复数）
        k: 入射波矢

    返回 Returns:
        σ_total: 总散射截面

    这是实验上测量总截面的重要方法
    """
    return (4 * np.pi / k) * np.imag(f_forward)


# =============================================================================
# 练习 1.6: 低能散射 Low Energy Scattering
#
# 物理背景:
# 低能极限 (ka << 1) 下，只有s波 (l=0) 重要
# 散射由两个参数描述: 散射长度a 和 有效程r_eff
#
# 有效程展开:
# k cot(δ₀) = -1/a + r_eff k²/2 + ...
#
# 散射长度的物理意义:
# - a > 0: 有效排斥（如硬球）
# - a < 0: 有效吸引
# - |a| → ∞: 临界束缚态（共振）
#
# 低能总截面: σ = 4πa²（与能量无关）
# =============================================================================
def scattering_length(delta_0, k):
    """
    从s波相移计算散射长度 Scattering length from s-wave phase shift

    参数 Parameters:
        delta_0: s波相移
        k: 入射波矢

    返回 Returns:
        a: 散射长度，单位 m

    公式: a = -lim_{k→0} tan(δ₀)/k
    注意: 需要在低能极限下计算才有意义
    """
    if k < 1e-10:
        return np.nan
    return -np.tan(delta_0) / k


def effective_range_expansion(k, a, r_eff):
    """
    有效程展开 Effective range expansion

    参数 Parameters:
        k: 入射波矢
        a: 散射长度
        r_eff: 有效程

    返回 Returns:
        cot(δ₀): s波相移的余切

    公式: k cot(δ₀) = -1/a + r_eff k²/2
    这是低能散射的普适参数化
    """
    return (-1/a + r_eff * k**2 / 2) / k


def low_energy_cross_section(a):
    """
    计算低能s波总截面 Low energy total cross section

    参数 Parameters:
        a: 散射长度，单位 m

    返回 Returns:
        σ: 总截面，单位 m²

    公式: σ = 4πa²

    物理意义: 低能时截面与能量无关，仅由散射长度决定
    这解释了为什么冷中子可以有很大的散射截面
    """
    return 4 * np.pi * a**2


# =============================================================================
# 练习 1.7: Born级数 Born Series
#
# 物理背景:
# Born近似是迭代解的首项，完整解是Born级数
# f = f₁ + f₂ + f₃ + ... (微扰展开)
#
# 有效性条件:
# 1. 弱势条件: V₀ma²/ℏ² << 1
#    势能远小于动能尺度
#
# 2. 高能条件: V₀ma/(ℏ²k) << 1
#    入射粒子能量远大于势能
#
# 至少满足一个条件，Born近似才可靠
# =============================================================================
def born_series_validity(V0, k, a):
    """
    检验Born近似有效性 Check Born approximation validity

    参数 Parameters:
        V0: 势能强度，单位 J
        k: 入射波矢，单位 m⁻¹
        a: 势能作用范围，单位 m

    返回 Returns:
        (weak_param, high_energy_param): 两个无量纲参数

    判据:
    - weak_param << 1: 弱势极限，Born近似有效
    - high_energy_param << 1: 高能极限，Born近似有效
    至少一个参数远小于1时，Born近似可信
    """
    weak_param = V0 * m_e * a**2 / hbar**2
    high_energy_param = V0 * m_e * a / (hbar**2 * k)

    return weak_param, high_energy_param


def second_born_correction(V_func, k, theta, r_max=10*a_0):
    """
    估算二阶Born修正 Estimate second Born correction

    二阶Born涉及复杂的双重积分
    f₂ ∝ ∫∫ V(r)G(r,r')V(r') d³r d³r'
    其中G是自由传播子

    参数 Parameters:
        V_func: 势能函数
        k: 入射波矢
        theta: 散射角
        r_max: 积分截断

    返回 Returns:
        f: 这里仅返回一阶结果（完整二阶计算较复杂）

    物理意义: 二阶修正描述多次散射效应
    """
    # 第一Born近似
    f1 = born_amplitude_spherical(V_func, k, theta, r_max)

    # 二阶修正通常与一阶相比是 O(V₀ma/(ℏ²k))
    # 这里只返回一阶结果
    return f1


# =============================================================================
# 可视化 Visualization
# 绘制卢瑟福散射、Yukawa势散射、相移、总截面等图像
# =============================================================================
def plot_scattering():
    """绘制散射理论相关图像"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # 散射参数
    E = 10 * e  # 10 eV
    k = energy_to_wavenumber(E, m_e)

    # 1. Rutherford散射
    ax1 = axes[0, 0]
    theta_range = np.linspace(0.1, np.pi - 0.1, 200)
    Z1, Z2 = 2, 79  # alpha粒子打金

    sigma_ruth = [rutherford_cross_section(k, theta, Z1, Z2) / a_0**2
                  for theta in theta_range]

    ax1.semilogy(theta_range * 180 / np.pi, sigma_ruth, 'b-', linewidth=2)
    ax1.set_xlabel('Scattering angle (degrees)')
    ax1.set_ylabel('d_sigma/d_Omega (a_0^2)')
    ax1.set_title('Rutherford散射截面')
    ax1.grid(True, alpha=0.3)

    # 2. Yukawa势散射
    ax2 = axes[0, 1]
    V0 = 1 * e  # 1 eV
    mu_values = [0.5/a_0, 1/a_0, 2/a_0]

    for mu in mu_values:
        f_values = [np.abs(born_amplitude_yukawa(k, theta, V0, mu))**2 / a_0**2
                    for theta in theta_range]
        ax2.plot(theta_range * 180 / np.pi, f_values,
                label=f'mu*a_0 = {mu*a_0:.1f}', linewidth=2)

    ax2.set_xlabel('Scattering angle (degrees)')
    ax2.set_ylabel('d_sigma/d_Omega (a_0^2)')
    ax2.set_title('Yukawa势散射 (Born近似)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_yscale('log')

    # 3. 分波相移
    ax3 = axes[1, 0]
    a_sphere = 0.5 * a_0  # 硬球半径
    k_range = np.linspace(0.1/a_0, 5/a_0, 100)

    for l in range(4):
        delta_l = [phase_shift_hard_sphere(k, a_sphere, l) for k in k_range]
        ax3.plot(k_range * a_0, delta_l, label=f'l={l}', linewidth=2)

    ax3.set_xlabel('k * a_0')
    ax3.set_ylabel('Phase shift (rad)')
    ax3.set_title('硬球势相移')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 总截面 vs 能量
    ax4 = axes[1, 1]
    E_range = np.logspace(-1, 2, 50) * e  # 0.1 to 100 eV
    k_range = [energy_to_wavenumber(E, m_e) for E in E_range]

    # Yukawa势总截面
    V0 = 0.1 * e
    mu = 1 / a_0

    def f_yukawa(k, theta):
        return born_amplitude_yukawa(k, theta, V0, mu)

    sigma_list = [total_cross_section(f_yukawa, k) / a_0**2 for k in k_range]

    ax4.loglog(E_range / e, sigma_list, 'b-', linewidth=2)
    ax4.set_xlabel('Energy (eV)')
    ax4.set_ylabel('Total cross section (a_0^2)')
    ax4.set_title('总散射截面 vs 能量')
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('scattering.png', dpi=150)
    print("图像已保存为 scattering.png")
    plt.show()


# =============================================================================
# 验证函数 Verification
# =============================================================================
def verify():
    """验证所有练习的正确性 Verify all exercises"""
    all_passed = True

    E = 10 * e  # 10 eV 入射能量
    k = energy_to_wavenumber(E, m_e)

    # 检查 1.1: 动量转移
    theta = np.pi / 2  # 90度散射
    q = momentum_transfer(k, theta)
    expected_q = np.sqrt(2) * k  # q = 2k*sin(45°) = √2 k
    if not np.isclose(q, expected_q, rtol=0.01):
        print("错误 1.1: 动量转移计算错误，90度散射时 q 应等于 √2 k")
        all_passed = False
    else:
        print("通过 1.1: 动量转移正确")

    # 检查 1.2: Born散射幅
    V0 = 1 * e
    mu = 1 / a_0
    f_yukawa = born_amplitude_yukawa(k, np.pi/4, V0, mu)
    if f_yukawa == 0:
        print("错误 1.2: Born散射幅不应为零")
        all_passed = False
    else:
        print("通过 1.2: Born散射幅正确")

    # 检查 1.3: 卢瑟福截面
    Z1, Z2 = 1, 1
    theta = np.pi / 2
    sigma_ruth = rutherford_cross_section(k, theta, Z1, Z2)
    if sigma_ruth <= 0 or np.isinf(sigma_ruth):
        print("错误 1.3: 卢瑟福截面计算错误")
        all_passed = False
    else:
        print(f"通过 1.3: 卢瑟福截面正确 (90度: {sigma_ruth/a_0**2:.2e} a₀²)")

    # 检查 1.4: 分波相移
    a_sphere = 0.5 * a_0
    delta_0 = phase_shift_hard_sphere(k, a_sphere, 0)
    if delta_0 == 0:
        print("错误 1.4: s波相移不应为零")
        all_passed = False
    else:
        print(f"通过 1.4: 分波相移正确 (δ₀ = {delta_0:.3f} rad)")

    # 检查 1.5: 光学定理验证
    delta_list = [phase_shift_hard_sphere(k, a_sphere, l) for l in range(5)]
    f_0 = scattering_amplitude_partial_wave(k, 0, delta_list)
    sigma_partial = 4 * np.pi / k**2 * sum((2*l+1) * np.sin(delta_list[l])**2
                                            for l in range(len(delta_list)))
    sigma_optical = (4 * np.pi / k) * np.imag(f_0)
    if not np.isclose(sigma_partial, sigma_optical, rtol=0.1):
        print(f"错误 1.5: 光学定理两边不相等")
        all_passed = False
    else:
        print("通过 1.5: 光学定理验证成功")

    # 检查 1.6: 低能散射
    a_scatt = scattering_length(delta_0, k)
    sigma_low = low_energy_cross_section(a_sphere)
    if sigma_low <= 0:
        print("错误 1.6: 低能截面应为正值")
        all_passed = False
    else:
        print(f"通过 1.6: 低能散射正确 (σ = 4πa²)")

    # 检查 1.7: Born有效性
    weak, high = born_series_validity(V0, k, a_0)
    if weak < 0 or high < 0:
        print("错误 1.7: Born有效性参数应为正值")
        all_passed = False
    else:
        print(f"通过 1.7: Born有效性参数正确 (弱势参数: {weak:.2f}, 高能参数: {high:.2f})")

    if all_passed:
        print("\n所有测试通过！")
        try:
            plot_scattering()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("散射理论 Scattering Theory")
    print("=" * 50)
    verify()
