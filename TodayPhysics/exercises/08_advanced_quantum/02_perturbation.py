"""
微扰论 Perturbation Theory
难度 Difficulty: ★★★★★

学习目标 Learning Objectives:
- 理解定态微扰论的基本原理和适用条件
- 掌握非简并情况下的一阶和二阶能量修正计算
- 理解简并微扰论的处理方法
- 应用于斯塔克效应、塞曼效应等实例

物理背景 Physical Background:
1. 微扰论是处理无法精确求解问题的近似方法
2. 基本思想: H = H₀ + λH'，其中 H' 是小微扰
3. 将能量和波函数按 λ 展开: E = E⁽⁰⁾ + λE⁽¹⁾ + λ²E⁽²⁾ + ...
4. 适用条件: |⟨m|H'|n⟩| << |E_n⁽⁰⁾ - E_m⁽⁰⁾|

关键公式 Key Formulas:
- 一阶能量修正: E_n⁽¹⁾ = ⟨n⁰|H'|n⁰⟩
- 二阶能量修正: E_n⁽²⁾ = Σ_{m≠n} |⟨m⁰|H'|n⁰⟩|² / (E_n⁰ - E_m⁰)
- 一阶波函数: |n⁽¹⁾⟩ = Σ_{m≠n} |m⁰⟩⟨m⁰|H'|n⁰⟩ / (E_n⁰ - E_m⁰)

物理应用:
- 斯塔克效应: 原子在外电场中的能级分裂
- 塞曼效应: 原子在磁场中的能级分裂
- 范德瓦尔斯力: 分子间相互作用
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import hbar, m_e, e, a_0, eV

# I AM NOT DONE

# =============================================================================
# 练习 2.1: 非简并微扰论 - 一阶修正 First Order Correction
#
# 物理背景:
# 一阶微扰只需要未微扰的波函数，是微扰势的"平均值"
# 物理意义: 微扰对能级的直接影响（期望值）
#
# 公式: E_n⁽¹⁾ = ⟨n⁰|H'|n⁰⟩ = ∫ψ_n*(x) H'(x) ψ_n(x) dx
# =============================================================================
def first_order_energy(psi_n, H_prime, x, dx):
    """
    计算一阶能量修正 First order energy correction

    参数 Parameters:
        psi_n: 第n个未微扰态波函数
        H_prime: 微扰哈密顿量（与x同维度的数组）
        x: 空间坐标数组
        dx: 空间步长

    返回 Returns:
        E1: 一阶能量修正，单位与H_prime相同（通常为焦耳J或电子伏eV）

    公式: E_n⁽¹⁾ = ⟨n|H'|n⟩ = ∫ψ_n* H' ψ_n dx
    """
    # TODO: 计算矩阵元（数值积分）
    # 提示: 被积函数为 ψ_n* × H' × ψ_n
    integrand = np.conj(psi_n) * H_prime * psi_n
    E1 = np.sum(integrand) * dx
    return np.real(E1)


# =============================================================================
# 练习 2.2: 二阶能量修正 Second Order Energy Correction
#
# 物理背景:
# 二阶修正反映了微扰导致的态混合效应
# 通过虚跃迁到其他能级再返回，产生额外能量贡献
#
# 重要性质:
# - 基态的二阶修正总是负的（变分原理）
# - 分母为能量差，简并时发散（需用简并微扰论）
#
# 公式: E_n⁽²⁾ = Σ_{m≠n} |⟨m⁰|H'|n⁰⟩|² / (E_n⁰ - E_m⁰)
# =============================================================================
def second_order_energy(n, psi_list, E0_list, H_prime, x, dx):
    """
    计算二阶能量修正 Second order energy correction

    参数 Parameters:
        n: 目标态的量子数索引（从0开始）
        psi_list: 所有未微扰态波函数列表
        E0_list: 所有未微扰能量列表，单位J或eV
        H_prime: 微扰哈密顿量数组
        x: 空间坐标数组
        dx: 空间步长

    返回 Returns:
        E2: 二阶能量修正，与E0_list单位相同

    注意: 需要对所有 m≠n 的态求和，截断态数会影响精度
    """
    E2 = 0
    psi_n = psi_list[n]
    E_n = E0_list[n]

    for m in range(len(psi_list)):
        if m != n:
            psi_m = psi_list[m]
            E_m = E0_list[m]
            # TODO: 计算跃迁矩阵元 ⟨m|H'|n⟩ 并累加二阶修正
            # 提示: 注意分母的符号
            matrix_element = np.sum(np.conj(psi_m) * H_prime * psi_n) * dx
            E2 += np.abs(matrix_element)**2 / (E_n - E_m)

    return np.real(E2)


# =============================================================================
# 练习 2.3: 一阶波函数修正 First Order Wavefunction Correction
#
# 物理背景:
# 微扰使原来的本征态"混入"其他态的成分
# 混入程度由跃迁矩阵元和能量差决定
#
# 物理意义:
# - 能量差越小，混入越多（近简并态影响大）
# - 矩阵元越大，混入越多（耦合越强）
#
# 公式: |n⁽¹⁾⟩ = Σ_{m≠n} |m⁰⟩ ⟨m⁰|H'|n⁰⟩ / (E_n⁰ - E_m⁰)
# =============================================================================
def first_order_wavefunction(n, psi_list, E0_list, H_prime, x, dx):
    """
    计算一阶波函数修正 First order wavefunction correction

    参数 Parameters:
        n: 目标态的量子数索引
        psi_list: 所有未微扰态波函数列表
        E0_list: 所有未微扰能量列表
        H_prime: 微扰哈密顿量数组
        x: 空间坐标数组
        dx: 空间步长

    返回 Returns:
        psi_correction: 一阶波函数修正，与原波函数同维度

    修正后的波函数: ψ_n = ψ_n⁽⁰⁾ + ψ_n⁽¹⁾ + O(λ²)
    注意: 修正后的波函数不再归一化，需重新归一化
    """
    psi_n = psi_list[n]
    E_n = E0_list[n]
    psi_correction = np.zeros_like(psi_n)

    for m in range(len(psi_list)):
        if m != n:
            psi_m = psi_list[m]
            E_m = E0_list[m]
            # 计算跃迁矩阵元
            matrix_element = np.sum(np.conj(psi_m) * H_prime * psi_n) * dx
            # 按权重混入第m个态
            psi_correction += psi_m * matrix_element / (E_n - E_m)

    return psi_correction


# =============================================================================
# 练习 2.4: 无限深势阱中的微扰 Perturbation in Infinite Square Well
#
# 物理背景:
# 无限深势阱是最简单的束缚态问题，精确解已知
# 添加微扰后，可用微扰论研究能级和波函数的变化
#
# 未微扰解:
# - 波函数: ψ_n(x) = √(2/L) sin(nπx/L)
# - 能量: E_n = n²π²ℏ²/(2mL²)
# =============================================================================
def infinite_well_wavefunctions(L, N_states, N_points=500):
    """
    生成无限深势阱的波函数和能量 Generate infinite well solutions

    参数 Parameters:
        L: 势阱宽度，单位 m
        N_states: 生成的态数目
        N_points: 空间离散点数

    返回 Returns:
        x: 空间坐标数组
        dx: 空间步长
        psi_list: 波函数列表（已归一化）
        E_list: 能量列表，单位 J

    能量公式: E_n = n²π²ℏ²/(2m_e L²)
    """
    x = np.linspace(0, L, N_points)
    dx = x[1] - x[0]

    psi_list = []
    E_list = []

    for n in range(1, N_states + 1):
        # 归一化波函数
        psi = np.sqrt(2/L) * np.sin(n * np.pi * x / L)
        # 能量本征值
        E = (n * np.pi * hbar)**2 / (2 * m_e * L**2)
        psi_list.append(psi)
        E_list.append(E)

    return x, dx, psi_list, E_list


def delta_perturbation(x, L, V0, width=0.01):
    """
    势阱中心的δ函数型微扰 Delta-function perturbation

    用窄高斯函数近似δ函数: δ(x) ≈ exp(-x²/2σ²)/(σ√(2π))

    参数 Parameters:
        x: 空间坐标数组
        L: 势阱宽度
        V0: 微扰强度，单位 J 或 eV
        width: 高斯宽度参数（相对于L的比例）

    返回 Returns:
        H_prime: 微扰势能数组

    物理意义: 模拟势阱中心的杂质或缺陷
    """
    center = L / 2
    sigma = width * L
    return V0 * np.exp(-(x - center)**2 / (2 * sigma**2)) / (sigma * np.sqrt(2 * np.pi))


# =============================================================================
# 练习 2.5: 谐振子微扰 Harmonic Oscillator Perturbation
#
# 物理背景:
# 实际分子振动势能不是严格的抛物线，包含非谐项
# 最常见的非谐微扰是 H' = λx⁴（四次项）
#
# 解析结果（利用升降算符）:
# E_n⁽¹⁾ = (3λℏ²/4m²ω²)(2n² + 2n + 1)
#
# 物理意义: 非谐项使高激发态能级间隔减小
# =============================================================================
def anharmonic_perturbation_energy(n, omega, lambda_param):
    """
    计算非谐微扰的一阶能量修正 Anharmonic perturbation energy

    微扰形式: H' = λx⁴

    参数 Parameters:
        n: 谐振子量子数 (n = 0, 1, 2, ...)
        omega: 谐振子角频率，单位 rad/s
        lambda_param: 非谐项系数，单位 J/m⁴

    返回 Returns:
        E1: 一阶能量修正，单位 J

    公式: E_n⁽¹⁾ = (3λℏ²/4m²ω²)(2n² + 2n + 1)
    推导需要用到 ⟨n|x⁴|n⟩ 的计算（利用升降算符）
    """
    # TODO: 计算一阶非谐修正
    # 提示: 使用给定的解析公式
    E1 = (3 * lambda_param * hbar**2 / (4 * m_e**2 * omega**2)) * (2*n**2 + 2*n + 1)
    return E1


# =============================================================================
# 练习 2.6: 简并微扰论 Degenerate Perturbation Theory
#
# 物理背景:
# 当未微扰能级简并时，普通微扰论的分母为零，失效
# 必须先在简并子空间内对角化微扰 H'
#
# 处理步骤:
# 1. 找出简并子空间的基态 {|n,α⟩}
# 2. 构建简并子空间内的微扰矩阵 H'_αβ = ⟨n,α|H'|n,β⟩
# 3. 对角化得到正确的零阶态和一阶能量修正
#
# 应用: 氢原子的斯塔克效应（n=2能级）、晶场分裂等
# =============================================================================
def degenerate_perturbation(H0, H_prime):
    """
    简并微扰论处理 Degenerate perturbation theory

    参数 Parameters:
        H0: 未微扰哈密顿量（简并子空间内，可忽略）
        H_prime: 简并子空间内的微扰矩阵

    返回 Returns:
        energies: 一阶能量修正（微扰矩阵的本征值）
        vectors: 正确的零阶本征态（微扰矩阵的本征向量）

    注意: 这里假设已经构建好简并子空间内的微扰矩阵
    """
    # 对 H' 在简并子空间内对角化
    energies, vectors = eigh(H_prime)
    return energies, vectors


# =============================================================================
# 练习 2.7: 斯塔克效应（二阶）Stark Effect (Second Order)
#
# 物理背景:
# 斯塔克效应是原子在外电场中能级发生移动和分裂的现象
# - 线性斯塔克效应: ΔE ∝ E（简并态，如氢原子 n≥2）
# - 二次斯塔克效应: ΔE ∝ E²（非简并态，如基态）
#
# 氢原子基态是非简并的（s态），一阶修正为零（宇称对称性）
# 二阶修正由极化率决定: ΔE = -αE²/2
#
# 氢原子基态极化率: α = (9/2)×4πε₀a₀³ ≈ 4.5 a₀³（原子单位）
# =============================================================================
def stark_shift_ground_state(E_field):
    """
    计算氢原子基态的二阶斯塔克效应 Quadratic Stark shift

    参数 Parameters:
        E_field: 外加电场强度，单位 V/m

    返回 Returns:
        delta_E: 能量移动，单位 J（负值表示能量降低）

    公式: ΔE = -αE²/2
    其中 α 是原子极化率，对氢原子基态 α ≈ 4.5 a₀³

    物理解释:
    外电场诱导原子产生电偶极矩 p = αE
    诱导偶极与电场的相互作用能为 -pE/2 = -αE²/2
    """
    # 氢原子基态极化率（SI单位）
    # α = 4.5 × a₀³ × 4πε₀（转换到SI单位）
    alpha_H = 4.5 * a_0**3 * 4 * np.pi * 8.854e-12  # SI单位: C²·m²/J
    # TODO: 计算能量移动 ΔE = -αE²/2
    delta_E = -0.5 * alpha_H * E_field**2
    return delta_E


# =============================================================================
# 可视化 Visualization
# 绘制微扰势能、能量修正、波函数修正等图像
# =============================================================================
def plot_perturbation():
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    L = 1e-9  # 1 nm
    N_states = 10
    x, dx, psi_list, E_list = infinite_well_wavefunctions(L, N_states)

    # 微扰：势阱中心的势垒
    V0 = 0.1 * eV
    H_prime = delta_perturbation(x, L, V0)

    # 1. 微扰势
    ax1 = axes[0, 0]
    ax1.plot(x*1e9, H_prime/eV, 'r-', linewidth=2)
    ax1.fill_between(x*1e9, 0, H_prime/eV, alpha=0.3)
    ax1.set_xlabel('x (nm)')
    ax1.set_ylabel("H' (eV)")
    ax1.set_title('微扰势能')
    ax1.grid(True, alpha=0.3)

    # 2. 能量修正
    ax2 = axes[0, 1]
    E1_list = [first_order_energy(psi, H_prime, x, dx) for psi in psi_list]
    E2_list = [second_order_energy(n, psi_list, E_list, H_prime, x, dx) for n in range(N_states)]

    n_range = range(1, N_states + 1)
    ax2.bar(np.array(list(n_range)) - 0.2, np.array(E1_list)/eV, 0.4, label='1st order')
    ax2.bar(np.array(list(n_range)) + 0.2, np.array(E2_list)/eV, 0.4, label='2nd order')
    ax2.set_xlabel('n')
    ax2.set_ylabel('Energy correction (eV)')
    ax2.set_title('能量修正')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 波函数修正
    ax3 = axes[1, 0]
    n = 0  # 基态
    psi0 = psi_list[n]
    psi1 = first_order_wavefunction(n, psi_list, E_list, H_prime, x, dx)

    ax3.plot(x*1e9, psi0**2 / 1e9, 'b-', label='|ψ⁰|²', linewidth=2)
    ax3.plot(x*1e9, (psi0 + psi1)**2 / 1e9, 'r--', label='|ψ⁰+ψ¹|²', linewidth=2)
    ax3.set_xlabel('x (nm)')
    ax3.set_ylabel('Probability density')
    ax3.set_title('基态波函数修正')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 斯塔克效应
    ax4 = axes[1, 1]
    E_field = np.linspace(0, 1e9, 100)  # V/m
    delta_E = [stark_shift_ground_state(E)/eV * 1e6 for E in E_field]

    ax4.plot(E_field/1e6, delta_E, 'g-', linewidth=2)
    ax4.set_xlabel('Electric field (MV/m)')
    ax4.set_ylabel('Energy shift (μeV)')
    ax4.set_title('氢原子斯塔克效应（基态）')
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('perturbation.png', dpi=150)
    print("图像已保存为 perturbation.png")
    plt.show()


def verify():
    """验证所有练习的正确性 Verify all exercises"""
    all_passed = True

    L = 1e-9
    N_states = 5
    x, dx, psi_list, E_list = infinite_well_wavefunctions(L, N_states)
    V0 = 0.1 * eV
    H_prime = delta_perturbation(x, L, V0)

    # 检查 2.1: 一阶能量修正
    E1 = first_order_energy(psi_list[0], H_prime, x, dx)
    if E1 == 0:
        print("错误 2.1: 一阶能量修正不应为零，请检查积分计算")
        all_passed = False
    else:
        print(f"通过 2.1: 一阶能量修正正确 (E₁⁽¹⁾ = {E1/eV*1000:.2f} meV)")

    # 检查 2.2: 二阶能量修正
    E2 = second_order_energy(0, psi_list, E_list, H_prime, x, dx)
    if E2 >= 0:
        print("错误 2.2: 基态二阶修正应为负值（变分原理保证）")
        all_passed = False
    else:
        print(f"通过 2.2: 二阶能量修正正确 (E₁⁽²⁾ = {E2/eV*1000:.4f} meV)")

    # 检查 2.3: 波函数修正
    psi1 = first_order_wavefunction(0, psi_list, E_list, H_prime, x, dx)
    if np.max(np.abs(psi1)) == 0:
        print("错误 2.3: 波函数修正不应为零，请检查态混合计算")
        all_passed = False
    else:
        print("通过 2.3: 波函数修正正确")

    # 检查 2.5: 非谐微扰
    E1_anharmonic = anharmonic_perturbation_energy(0, 1e15, 1e40)
    if E1_anharmonic <= 0:
        print("错误 2.5: 非谐修正 λx⁴ 应使能量升高（正值）")
        all_passed = False
    else:
        print("通过 2.5: 谐振子非谐微扰正确")

    # 检查 2.7: 斯塔克效应
    delta_E = stark_shift_ground_state(1e8)
    if delta_E >= 0:
        print("错误 2.7: 斯塔克效应应降低基态能量（负值）")
        all_passed = False
    else:
        print(f"通过 2.7: 斯塔克效应正确 (ΔE < 0)")

    if all_passed:
        print("\n所有测试通过！")
        try:
            plot_perturbation()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("微扰论 Perturbation Theory")
    print("=" * 50)
    verify()
