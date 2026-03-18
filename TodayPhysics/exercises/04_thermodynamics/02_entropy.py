"""
熵与热力学第二定律 Entropy and Second Law of Thermodynamics
难度 Difficulty: ★★★★

学习目标 Learning Objectives:
- 理解熵的热力学定义和统计意义
  Understand thermodynamic and statistical definitions of entropy
- 掌握熵增原理（热力学第二定律的数学表述）
  Master the law of entropy increase (mathematical statement of the 2nd law)
- 分析不可逆过程中的熵产生
  Analyze entropy production in irreversible processes
- 理解吉布斯自由能和自发过程判据
  Understand Gibbs free energy and criterion for spontaneous processes
- 掌握各种热力学势及其应用
  Master various thermodynamic potentials and their applications

物理背景 Physical Background:
熵是热力学中最深刻的概念之一。从宏观角度，熵衡量能量"品质"的退化；
从微观角度，熵衡量系统的"无序程度"或微观态数目。

热力学第二定律指出：孤立系统的熵永不减少。这解释了为什么热量自发地
从高温物体传向低温物体，而不会反向进行。

HINT: 熵的热力学定义: dS = δQ_rev/T（可逆过程）
HINT: 熵增原理: ΔS_universe ≥ 0（孤立系统熵永不减少）
HINT: 玻尔兹曼熵公式: S = k_B ln(W)（W 是微观态数目）
HINT: 吉布斯自由能: G = H - TS，ΔG < 0 表示自发过程
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import R, k_B, N_A

# I AM NOT DONE

# =============================================================================
# 练习 2.1: 熵的热力学定义
# Exercise 2.1: Thermodynamic Definition of Entropy
# =============================================================================
# 熵的热力学定义（克劳修斯定义）Thermodynamic definition (Clausius):
#   dS = δQ_rev / T
#   只有可逆过程才能用此公式直接计算熵变
#
# 熵是状态函数 Entropy is a state function:
#   熵变只取决于初末态，与路径无关
#   即使过程不可逆，也可以设计可逆路径来计算熵变
#
# 理想气体熵变公式 Entropy change for ideal gas:
#   ΔS = nCv ln(T₂/T₁) + nR ln(V₂/V₁)  （一般情况）
#   ΔS = nCp ln(T₂/T₁) - nR ln(P₂/P₁)  （另一形式）

def entropy_change_isothermal(n, T, V1, V2):
    """
    理想气体等温过程的熵变 Entropy change in isothermal process

    公式 Formula: ΔS = nR ln(V₂/V₁) = -nR ln(P₂/P₁)

    参数 Parameters:
        n: 物质的量 (mol) - Amount of substance
        T: 温度 (K) - Temperature（此参数用于保持接口一致性）
        V1: 初始体积 (m³) - Initial volume
        V2: 末态体积 (m³) - Final volume

    返回 Returns:
        delta_S: 熵变 (J/K) - Entropy change

    物理意义 Physical meaning:
        等温膨胀时熵增（V₂ > V₁，ΔS > 0）
        等温压缩时熵减（V₂ < V₁，ΔS < 0）
    """
    # TODO: 计算等温过程的熵变
    # TODO: Calculate entropy change in isothermal process
    delta_S = n * R * np.log(V2 / V1)
    return delta_S

def entropy_change_isobaric(n, Cp, T1, T2):
    """
    等压过程的熵变 Entropy change in isobaric process

    公式 Formula: ΔS = nCp ln(T₂/T₁)

    参数 Parameters:
        n: 物质的量 (mol) - Amount of substance
        Cp: 定压摩尔热容 (J/(mol·K)) - Molar heat capacity at constant P
        T1: 初始温度 (K) - Initial temperature
        T2: 末态温度 (K) - Final temperature

    返回 Returns:
        delta_S: 熵变 (J/K) - Entropy change
    """
    return n * Cp * np.log(T2 / T1)

def entropy_change_isochoric(n, Cv, T1, T2):
    """
    等容过程的熵变 Entropy change in isochoric process

    公式 Formula: ΔS = nCv ln(T₂/T₁)

    参数 Parameters:
        n: 物质的量 (mol) - Amount of substance
        Cv: 定容摩尔热容 (J/(mol·K)) - Molar heat capacity at constant V
        T1: 初始温度 (K) - Initial temperature
        T2: 末态温度 (K) - Final temperature

    返回 Returns:
        delta_S: 熵变 (J/K) - Entropy change
    """
    return n * Cv * np.log(T2 / T1)


# =============================================================================
# 练习 2.2: 热传导的熵产生
# Exercise 2.2: Entropy Production in Heat Transfer
# =============================================================================
# 热传导是典型的不可逆过程 Heat conduction is a typical irreversible process
#
# 当热量 Q 从高温物体（Th）自发传到低温物体（Tc）时：
# When heat Q flows spontaneously from hot body (Th) to cold body (Tc):
#   - 高温物体熵变: ΔS_hot = -Q/Th < 0（放热，熵减）
#   - 低温物体熵变: ΔS_cold = Q/Tc > 0（吸热，熵增）
#   - 宇宙总熵变: ΔS_total = Q(1/Tc - 1/Th) > 0
#
# 熵产生说明这是不可逆过程，热量不会自发地从低温流向高温

def entropy_change_heat_transfer(Q, T_hot, T_cold):
    """
    热量Q从高温物体传到低温物体的熵变 Entropy change in heat transfer

    公式 Formula:
        ΔS_hot = -Q/T_hot（高温物体放热，熵减）
        ΔS_cold = Q/T_cold（低温物体吸热，熵增）
        ΔS_total = Q(1/T_cold - 1/T_hot) > 0（总熵增）

    参数 Parameters:
        Q: 传递的热量 (J) - Heat transferred (positive value)
        T_hot: 高温物体温度 (K) - Temperature of hot body
        T_cold: 低温物体温度 (K) - Temperature of cold body

    返回 Returns:
        delta_S_total: 宇宙总熵变 (J/K) - Total entropy change
        delta_S_hot: 高温物体熵变 (J/K) - Entropy change of hot body
        delta_S_cold: 低温物体熵变 (J/K) - Entropy change of cold body

    重要结论 Key result:
        ΔS_total > 0 证明热传导是不可逆过程
        The positive total entropy change proves irreversibility
    """
    delta_S_hot = -Q / T_hot  # 高温物体熵减
    delta_S_cold = Q / T_cold  # 低温物体熵增
    # TODO: 计算宇宙总熵变（应为正值）
    # TODO: Calculate total entropy change (should be positive)
    delta_S_total = delta_S_hot + delta_S_cold
    return delta_S_total, delta_S_hot, delta_S_cold


# =============================================================================
# 练习 2.3: 混合过程的熵变
# Exercise 2.3: Entropy of Mixing
# =============================================================================
# 混合熵描述不同物质混合时的熵增 Mixing entropy describes entropy increase
#
# 理想气体混合 Ideal gas mixing:
#   两种不同的理想气体在相同 T、P 下混合，即使没有热量交换，熵也会增加
#   这是因为每种气体现在占据了更大的体积，微观态数目增加
#
# 吉布斯悖论 Gibbs paradox:
#   如果两种气体完全相同，则混合熵为零（无法区分的粒子）

def entropy_of_mixing_ideal_gas(n1, n2):
    """
    两种理想气体混合的熵变 Entropy of mixing for ideal gases

    公式 Formula: ΔS_mix = -R(n₁ln(x₁) + n₂ln(x₂))
    其中 x_i = n_i/(n₁+n₂) 是摩尔分数

    参数 Parameters:
        n1: 气体1的物质的量 (mol) - Amount of gas 1
        n2: 气体2的物质的量 (mol) - Amount of gas 2

    返回 Returns:
        delta_S: 混合熵 (J/K) - Entropy of mixing

    物理意义 Physical meaning:
        混合熵总是正的（x < 1 时 ln(x) < 0）
        表明混合是自发过程
    """
    n_total = n1 + n2
    x1 = n1 / n_total  # 气体1的摩尔分数
    x2 = n2 / n_total  # 气体2的摩尔分数
    # TODO: 计算混合熵（注意：由于 ln(x) < 0，所以 ΔS > 0）
    # TODO: Calculate mixing entropy (Note: since ln(x) < 0, ΔS > 0)
    delta_S = -R * (n1 * np.log(x1) + n2 * np.log(x2))
    return delta_S

def entropy_of_mixing_temperature(m1, c1, T1, m2, c2, T2):
    """
    不同温度物体热接触达到热平衡的熵变 Entropy change when bodies at different temperatures reach equilibrium

    参数 Parameters:
        m1: 物体1质量 (kg) - Mass of body 1
        c1: 物体1比热容 (J/(kg·K)) - Specific heat of body 1
        T1: 物体1初始温度 (K) - Initial temperature of body 1
        m2: 物体2质量 (kg) - Mass of body 2
        c2: 物体2比热容 (J/(kg·K)) - Specific heat of body 2
        T2: 物体2初始温度 (K) - Initial temperature of body 2

    返回 Returns:
        delta_S_total: 总熵变 (J/K) - Total entropy change
        T_f: 最终平衡温度 (K) - Final equilibrium temperature

    推导 Derivation:
        由能量守恒求出最终温度，再分别计算各物体的熵变
    """
    # 由能量守恒计算最终温度 Final temperature from energy conservation
    T_f = (m1 * c1 * T1 + m2 * c2 * T2) / (m1 * c1 + m2 * c2)
    # 各物体熵变 Entropy change of each body
    delta_S1 = m1 * c1 * np.log(T_f / T1)
    delta_S2 = m2 * c2 * np.log(T_f / T2)
    return delta_S1 + delta_S2, T_f


# =============================================================================
# 练习 2.4: 自由膨胀
# Exercise 2.4: Free Expansion
# =============================================================================
# 自由膨胀（焦耳实验）是重要的不可逆过程
# Free expansion (Joule experiment) is an important irreversible process
#
# 过程描述 Process description:
#   气体从体积 V₁ 自由膨胀到体积 V₂（真空膨胀）
#   - 没有对外做功: W = 0（无外压）
#   - 绝热容器: Q = 0
#   - 由热力学第一定律: ΔU = Q - W = 0
#   - 理想气体内能只与 T 有关，故 ΔT = 0
#
# 熵变计算 Entropy calculation:
#   虽然过程不可逆，但熵是状态函数
#   可以设计等温可逆膨胀（初末态相同）来计算熵变
#   ΔS = nR ln(V₂/V₁) > 0

def entropy_change_free_expansion(n, V1, V2):
    """
    理想气体自由膨胀的熵变 Entropy change in free expansion

    过程特点 Process characteristics:
        Q = W = 0（绝热自由膨胀）
        ΔU = 0（理想气体）
        ΔT = 0（温度不变）
        但 ΔS > 0！（不可逆过程）

    公式 Formula: ΔS = nR ln(V₂/V₁)

    参数 Parameters:
        n: 物质的量 (mol) - Amount of substance
        V1: 初始体积 (m³) - Initial volume
        V2: 末态体积 (m³) - Final volume

    返回 Returns:
        delta_S: 熵变 (J/K) - Entropy change

    物理意义 Physical meaning:
        这说明熵增不仅仅是因为吸热，而是因为系统变得更"无序"
        分子可能占据的空间增大，微观态数目增加
    """
    # TODO: 计算自由膨胀的熵变（与等温可逆膨胀相同）
    # TODO: Calculate entropy change (same as reversible isothermal expansion)
    delta_S = n * R * np.log(V2 / V1)
    return delta_S


# =============================================================================
# 练习 2.5: 玻尔兹曼熵公式
# Exercise 2.5: Boltzmann Entropy Formula
# =============================================================================
# 玻尔兹曼熵公式连接了热力学熵和统计力学
# Boltzmann entropy formula bridges thermodynamics and statistical mechanics
#
# 公式 Formula: S = k_B ln(W)
# 其中 W 是与宏观态相容的微观态数目（热力学概率）
#
# 这个公式刻在玻尔兹曼的墓碑上，是物理学中最深刻的公式之一
# This formula is engraved on Boltzmann's tombstone
#
# 物理意义 Physical meaning:
#   - W 越大，系统越"无序"，熵越大
#   - 高熵态有更多实现方式，所以更可能出现
#   - 这解释了为什么宏观上系统总是向高熵方向演化

def boltzmann_entropy(W):
    """
    玻尔兹曼熵 Boltzmann entropy

    公式 Formula: S = k_B ln(W)

    参数 Parameters:
        W: 微观态数目（热力学概率）- Number of microstates

    返回 Returns:
        S: 熵 (J/K) - Entropy

    注意 Note:
        W 必须是正整数（或非常大的正数）
        k_B ≈ 1.38×10⁻²³ J/K 是玻尔兹曼常数
    """
    # TODO: 计算玻尔兹曼熵
    # TODO: Calculate Boltzmann entropy
    S = k_B * np.log(W)
    return S

def microstate_count_ideal_gas(V, N):
    """
    理想气体微观态数目与体积的关系 Microstate count vs volume for ideal gas

    公式 Formula: W ∝ V^N（简化关系）

    参数 Parameters:
        V: 体积 (m³) - Volume
        N: 粒子数 - Number of particles

    返回 Returns:
        相对微观态数目（比例关系）

    说明 Explanation:
        每个粒子可以在体积 V 内任意位置，有 V 种可能
        N 个独立粒子总共有 V^N 种可能的空间配置
        这解释了为什么自由膨胀会增加熵
    """
    return V**N


# =============================================================================
# 练习 2.6: 吉布斯自由能
# Exercise 2.6: Gibbs Free Energy
# =============================================================================
# 吉布斯自由能是恒温恒压条件下判断过程自发性的判据
# Gibbs free energy is the criterion for spontaneity at constant T and P
#
# 定义 Definition: G = H - TS = U + PV - TS
#
# 自发性判据 Spontaneity criterion:
#   - ΔG < 0: 过程自发进行（放出自由能）
#   - ΔG = 0: 平衡状态
#   - ΔG > 0: 过程不自发（需要外界做功）
#
# ΔG = ΔH - TΔS 的物理意义:
#   - ΔH < 0（放热）有利于自发
#   - ΔS > 0（熵增）有利于自发
#   - 温度 T 决定熵项的权重

def gibbs_free_energy(H, T, S):
    """
    吉布斯自由能 Gibbs free energy

    公式 Formula: G = H - TS

    参数 Parameters:
        H: 焓 (J) - Enthalpy
        T: 温度 (K) - Temperature
        S: 熵 (J/K) - Entropy

    返回 Returns:
        G: 吉布斯自由能 (J) - Gibbs free energy
    """
    return H - T * S

def gibbs_change_reaction(delta_H, T, delta_S):
    """
    反应的吉布斯自由能变化 Gibbs free energy change for a reaction

    公式 Formula: ΔG = ΔH - TΔS

    参数 Parameters:
        delta_H: 反应焓变 (J) - Enthalpy change
        T: 温度 (K) - Temperature
        delta_S: 反应熵变 (J/K) - Entropy change

    返回 Returns:
        delta_G: 吉布斯自由能变化 (J) - Change in Gibbs free energy

    判据 Criterion:
        ΔG < 0: 反应自发进行 (spontaneous)
        ΔG = 0: 平衡 (equilibrium)
        ΔG > 0: 反应不自发 (non-spontaneous)
    """
    return delta_H - T * delta_S

def is_spontaneous(delta_G):
    """
    判断反应是否自发 Check if reaction is spontaneous

    参数 Parameters:
        delta_G: 吉布斯自由能变化 (J)

    返回 Returns:
        bool: True 表示自发反应，False 表示非自发
    """
    return delta_G < 0


# =============================================================================
# 练习 2.7: 热力学势
# Exercise 2.7: Thermodynamic Potentials
# =============================================================================
# 热力学势是描述系统状态的特征函数
# Thermodynamic potentials are characteristic functions of the system state
#
# 四种主要热力学势 Four main thermodynamic potentials:
#   1. 内能 U(S, V): dU = TdS - PdV
#   2. 焓 H(S, P) = U + PV: dH = TdS + VdP
#   3. 亥姆霍兹自由能 F(T, V) = U - TS: dF = -SdT - PdV
#   4. 吉布斯自由能 G(T, P) = H - TS: dG = -SdT + VdP
#
# 每种势适用于不同的约束条件：
#   - 恒 S、V 下：使 U 最小
#   - 恒 S、P 下：使 H 最小
#   - 恒 T、V 下：使 F 最小
#   - 恒 T、P 下：使 G 最小

def helmholtz_free_energy(U, T, S):
    """
    亥姆霍兹自由能 Helmholtz free energy

    公式 Formula: F = U - TS

    参数 Parameters:
        U: 内能 (J) - Internal energy
        T: 温度 (K) - Temperature
        S: 熵 (J/K) - Entropy

    返回 Returns:
        F: 亥姆霍兹自由能 (J) - Helmholtz free energy

    应用 Application:
        恒温恒容过程中，ΔF < 0 表示过程自发
        在统计力学中，F = -kT ln(Z)，Z 是配分函数
    """
    return U - T * S

def enthalpy(U, P, V):
    """
    焓 Enthalpy

    公式 Formula: H = U + PV

    参数 Parameters:
        U: 内能 (J) - Internal energy
        P: 压强 (Pa) - Pressure
        V: 体积 (m³) - Volume

    返回 Returns:
        H: 焓 (J) - Enthalpy

    应用 Application:
        恒压过程中吸收的热量等于焓变: Q_P = ΔH
        化学反应热通常用焓变表示
    """
    return U + P * V


# =============================================================================
# 可视化 Visualization
# =============================================================================
def plot_entropy():
    """
    绘制熵相关图表 Plot entropy-related diagrams

    包含四个子图 Contains four subplots:
    1. 等温膨胀的熵变与体积比的关系
    2. 热传导的熵产生与温度的关系
    3. 吉布斯自由能与自发性判据
    4. 混合熵与组成的关系
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. 等温膨胀的熵变
    ax1 = axes[0, 0]
    V_ratio = np.linspace(1, 10, 100)
    delta_S = entropy_change_isothermal(1, 300, 1, V_ratio)
    ax1.plot(V_ratio, delta_S, 'b-', linewidth=2)
    ax1.set_xlabel('V₂/V₁')
    ax1.set_ylabel('ΔS (J/K)')
    ax1.set_title('等温膨胀熵变')
    ax1.grid(True, alpha=0.3)

    # 2. 热传导熵产生
    ax2 = axes[0, 1]
    T_cold_range = np.linspace(250, 350, 100)
    T_hot = 400
    Q = 1000  # J
    delta_S_total = [entropy_change_heat_transfer(Q, T_hot, Tc)[0] for Tc in T_cold_range]
    ax2.plot(T_cold_range, delta_S_total, 'r-', linewidth=2)
    ax2.axhline(y=0, color='k', linestyle='--')
    ax2.set_xlabel('T_cold (K)')
    ax2.set_ylabel('ΔS_total (J/K)')
    ax2.set_title('热传导的熵产生 (T_hot=400K)')
    ax2.grid(True, alpha=0.3)

    # 3. 吉布斯自由能与自发性
    ax3 = axes[1, 0]
    T_range = np.linspace(200, 600, 100)
    delta_H = -50000  # J (放热)
    delta_S = 100  # J/K (熵增)
    delta_G = gibbs_change_reaction(delta_H, T_range, delta_S)
    ax3.plot(T_range, delta_G/1000, 'g-', linewidth=2)
    ax3.axhline(y=0, color='r', linestyle='--')
    ax3.fill_between(T_range, delta_G/1000, 0, where=delta_G<0, alpha=0.3, color='green', label='Spontaneous')
    ax3.set_xlabel('T (K)')
    ax3.set_ylabel('ΔG (kJ)')
    ax3.set_title('吉布斯自由能判据')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 混合熵
    ax4 = axes[1, 1]
    x1 = np.linspace(0.01, 0.99, 100)
    n_total = 1
    n1 = x1 * n_total
    n2 = (1 - x1) * n_total
    S_mix = [entropy_of_mixing_ideal_gas(n1[i], n2[i]) for i in range(len(x1))]
    ax4.plot(x1, S_mix, 'b-', linewidth=2)
    ax4.set_xlabel('x₁ (mole fraction)')
    ax4.set_ylabel('ΔS_mix (J/K)')
    ax4.set_title('混合熵')
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('entropy.png', dpi=150)
    print("图像已保存为 entropy.png")
    plt.show()


def verify():
    """
    验证所有练习的正确性 Verify all exercises

    测试内容 Tests:
    2.1 等温过程熵变
    2.2 热传导熵产生
    2.3 混合熵
    2.4 自由膨胀熵变
    2.5 玻尔兹曼熵
    2.6 吉布斯自由能
    """
    all_passed = True

    # 检查 2.1 - 等温熵变
    delta_S = entropy_change_isothermal(1, 300, 1, 2)
    expected = R * np.log(2)
    if not np.isclose(delta_S, expected, rtol=0.01):
        print("错误 2.1: 等温熵变计算错误")
        print(f"  期望: {expected:.2f} J/K, 实际得到: {delta_S:.2f} J/K")
        all_passed = False
    else:
        print(f"通过 2.1: 等温熵变正确 (体积加倍时 ΔS = {delta_S:.2f} J/K)")

    # 检查 2.2 - 热传导熵产生
    delta_S_total, _, _ = entropy_change_heat_transfer(1000, 400, 300)
    if delta_S_total <= 0:
        print("错误 2.2: 热传导熵产生应为正值（不可逆过程）")
        print(f"  实际得到: ΔS = {delta_S_total:.4f} J/K")
        all_passed = False
    else:
        print(f"通过 2.2: 热传导熵产生正确 (ΔS = {delta_S_total:.4f} J/K > 0)")

    # 检查 2.3 - 混合熵
    delta_S_mix = entropy_of_mixing_ideal_gas(1, 1)
    expected = -R * 2 * np.log(0.5)  # = 2R*ln(2)
    if not np.isclose(delta_S_mix, expected, rtol=0.01):
        print("错误 2.3: 混合熵计算错误")
        print(f"  期望: {expected:.2f} J/K, 实际得到: {delta_S_mix:.2f} J/K")
        all_passed = False
    else:
        print(f"通过 2.3: 混合熵正确 (等量混合时 ΔS = {delta_S_mix:.2f} J/K)")

    # 检查 2.4 - 自由膨胀
    delta_S_free = entropy_change_free_expansion(1, 1, 2)
    if delta_S_free <= 0:
        print("错误 2.4: 自由膨胀熵变应为正值（不可逆过程）")
        print(f"  实际得到: ΔS = {delta_S_free:.2f} J/K")
        all_passed = False
    else:
        print(f"通过 2.4: 自由膨胀熵变正确 (ΔS = {delta_S_free:.2f} J/K > 0)")

    # 检查 2.5 - 玻尔兹曼熵
    S = boltzmann_entropy(1e23)
    if S <= 0:
        print("错误 2.5: 玻尔兹曼熵计算错误（微观态数为正时熵应为正）")
        all_passed = False
    else:
        print(f"通过 2.5: 玻尔兹曼熵正确 (W=10²³ 时 S = {S:.2e} J/K)")

    # 检查 2.6 - 吉布斯自由能
    delta_G = gibbs_change_reaction(-50000, 300, 100)  # 放热且熵增
    if delta_G >= 0:
        print("错误 2.6: 吉布斯自由能计算错误")
        print(f"  放热(ΔH<0)且熵增(ΔS>0)的反应应有 ΔG<0")
        all_passed = False
    else:
        is_spont = is_spontaneous(delta_G)
        status = "自发" if is_spont else "非自发"
        print(f"通过 2.6: 吉布斯自由能正确 (ΔG = {delta_G/1000:.1f} kJ, {status})")

    if all_passed:
        print("\n所有测试通过！")
        try:
            plot_entropy()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("熵与热力学第二定律 Entropy")
    print("=" * 50)
    verify()
