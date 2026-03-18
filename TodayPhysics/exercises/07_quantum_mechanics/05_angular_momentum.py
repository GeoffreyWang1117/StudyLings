"""
角动量与自旋 Angular Momentum and Spin
难度 Difficulty: ★★★★

物理背景 Physical Background:
--------------------------
角动量是物理学中最重要的守恒量之一，与旋转对称性相关。
在量子力学中，角动量有两种类型：
1. 轨道角动量 L：与粒子的空间运动相关，l 取整数
2. 自旋角动量 S：粒子的内禀属性，s 可取半整数（如电子 s=1/2）

关键物理概念：
- 角动量量子化：L² 和 L_z 可同时测量
- 升降算符：改变磁量子数 m 而不改变总角动量 l
- 角动量耦合：两个角动量合成为总角动量
- 自旋-轨道耦合：导致精细结构能级分裂

学习目标 Learning Objectives:
--------------------------
1. 理解轨道角动量本征值和本征态
2. 掌握升降算符的作用规则
3. 熟悉球谐函数及其性质
4. 掌握角动量耦合的三角关系
5. 了解 Clebsch-Gordan 系数的选择定则
6. 理解自旋-轨道耦合的物理机制

关键公式 Key Formulas:
--------------------
- L² 本征值: L²|l,m> = hbar²l(l+1)|l,m>
- L_z 本征值: L_z|l,m> = hbar*m|l,m>
- 升算符: L_+|l,m> = hbar*sqrt((l-m)(l+m+1))|l,m+1>
- 降算符: L_-|l,m> = hbar*sqrt((l+m)(l-m+1))|l,m-1>
- 耦合规则: J = |j1-j2|, ..., j1+j2
- 自旋-轨道能量: E_so = (xi/2)[j(j+1)-l(l+1)-s(s+1)]hbar²
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import sph_harm
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import hbar

# I AM NOT DONE

# =============================================================================
# 练习 5.1: 角动量算符
# Exercise 5.1: Angular Momentum Operators
# =============================================================================
def L_squared_eigenvalue(l):
    """
    L² 的本征值 = ℏ²l(l+1)
    """
    return hbar**2 * l * (l + 1)

def Lz_eigenvalue(m):
    """
    L_z 的本征值 = ℏm
    """
    return hbar * m

def allowed_m_values(l):
    """
    给定l的允许m值: m = -l, -l+1, ..., l-1, l
    """
    return list(range(-l, l + 1))


# =============================================================================
# 练习 5.2: 升降算符
# Exercise 5.2: Ladder Operators
# =============================================================================
def L_plus_coefficient(l, m):
    """
    L₊|l,m⟩ = ℏ√((l-m)(l+m+1))|l,m+1⟩
    返回系数
    """
    if m >= l:
        return 0
    return hbar * np.sqrt((l - m) * (l + m + 1))

def L_minus_coefficient(l, m):
    """
    L₋|l,m⟩ = ℏ√((l+m)(l-m+1))|l,m-1⟩
    """
    if m <= -l:
        return 0
    return hbar * np.sqrt((l + m) * (l - m + 1))


# =============================================================================
# 练习 5.3: 球谐函数
# Exercise 5.3: Spherical Harmonics
# =============================================================================
def spherical_harmonic(l, m, theta, phi):
    """
    球谐函数 Y_l^m(θ, φ)
    """
    return sph_harm(m, l, phi, theta)

def spherical_harmonic_probability(l, m, theta, phi):
    """
    概率密度 |Y_l^m|²
    """
    Y = spherical_harmonic(l, m, theta, phi)
    return np.abs(Y)**2


# =============================================================================
# 练习 5.4: 角动量加法
# Exercise 5.4: Addition of Angular Momenta
# =============================================================================
def possible_total_j(j1, j2):
    """
    两个角动量j1和j2耦合后可能的总角动量j
    j = |j1-j2|, |j1-j2|+1, ..., j1+j2
    """
    j_min = abs(j1 - j2)
    j_max = j1 + j2
    # 处理半整数情况
    step = 1
    j_values = []
    j = j_min
    while j <= j_max + 1e-10:
        j_values.append(j)
        j += step
    return j_values

def total_states_count(j1, j2):
    """
    耦合态的总数 = (2j1+1)(2j2+1)
    """
    return int((2*j1 + 1) * (2*j2 + 1))


# =============================================================================
# 练习 5.5: 克莱布施-戈登系数
# Exercise 5.5: Clebsch-Gordan Coefficients
# =============================================================================
def cg_coefficient(j1, m1, j2, m2, j, m):
    """
    克莱布施-戈登系数 ⟨j1,m1;j2,m2|j,m⟩
    使用简化公式（仅适用于特定情况）
    """
    # 选择规则
    if m != m1 + m2:
        return 0
    if j < abs(j1 - j2) or j > j1 + j2:
        return 0
    if abs(m) > j or abs(m1) > j1 or abs(m2) > j2:
        return 0

    # 特殊情况: j1 = j2 = 1/2
    if j1 == 0.5 and j2 == 0.5:
        if j == 1:  # 三重态
            if m1 == 0.5 and m2 == 0.5 and m == 1:
                return 1
            elif m1 == -0.5 and m2 == -0.5 and m == -1:
                return 1
            elif m == 0:
                if m1 == 0.5 and m2 == -0.5:
                    return 1/np.sqrt(2)
                elif m1 == -0.5 and m2 == 0.5:
                    return 1/np.sqrt(2)
        elif j == 0 and m == 0:  # 单态
            if m1 == 0.5 and m2 == -0.5:
                return 1/np.sqrt(2)
            elif m1 == -0.5 and m2 == 0.5:
                return -1/np.sqrt(2)

    return None  # 一般情况需要更复杂的公式


# =============================================================================
# 练习 5.6: 自旋-轨道耦合
# Exercise 5.6: Spin-Orbit Coupling
# =============================================================================
def spin_orbit_energy(l, s, j, xi):
    """
    自旋-轨道耦合能量
    E_so = (ξ/2)[j(j+1) - l(l+1) - s(s+1)]ℏ²
    ξ: 耦合常数
    """
    E = (xi / 2) * (j*(j+1) - l*(l+1) - s*(s+1)) * hbar**2
    return E

def spectroscopic_notation(n, l, j):
    """
    光谱符号 nL_j
    """
    L_letters = ['S', 'P', 'D', 'F', 'G', 'H']
    L = L_letters[l] if l < len(L_letters) else f'({l})'
    return f"{n}{L}_{j}"


# =============================================================================
# 可视化
# =============================================================================
def plot_angular_momentum():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 球谐函数 |Y_l^m|²
    ax1 = axes[0, 0]
    theta = np.linspace(0, np.pi, 100)
    phi = 0

    for l, m in [(0, 0), (1, 0), (1, 1), (2, 0), (2, 2)]:
        prob = spherical_harmonic_probability(l, m, theta, phi)
        ax1.plot(np.degrees(theta), prob, label=f'l={l}, m={m}', linewidth=2)

    ax1.set_xlabel('θ (degrees)')
    ax1.set_ylabel('|Y_l^m|²')
    ax1.set_title('球谐函数概率密度')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 3D球谐函数
    ax2 = fig.add_subplot(232, projection='3d')
    theta_3d = np.linspace(0, np.pi, 50)
    phi_3d = np.linspace(0, 2*np.pi, 100)
    THETA, PHI = np.meshgrid(theta_3d, phi_3d)

    l, m = 2, 1
    Y = spherical_harmonic(l, m, THETA, PHI)
    R = np.abs(Y)**2

    X = R * np.sin(THETA) * np.cos(PHI)
    Y_plot = R * np.sin(THETA) * np.sin(PHI)
    Z = R * np.cos(THETA)

    ax2.plot_surface(X, Y_plot, Z, cmap='viridis', alpha=0.8)
    ax2.set_title(f'|Y_{l}^{m}|² 3D')

    # 3. 角动量矢量模型
    ax3 = fig.add_subplot(233, projection='3d')
    l = 2
    L = np.sqrt(l * (l + 1))

    # 绘制可能的L_z分量
    for m in allowed_m_values(l):
        L_z = m
        L_xy = np.sqrt(L**2 - L_z**2)
        phi_cone = np.linspace(0, 2*np.pi, 50)
        x_cone = L_xy * np.cos(phi_cone)
        y_cone = L_xy * np.sin(phi_cone)
        z_cone = np.full_like(phi_cone, L_z)
        ax3.plot(x_cone, y_cone, z_cone, 'b-', alpha=0.5)
        ax3.scatter([0], [0], [L_z], c='r', s=50)

    ax3.set_xlabel('L_x/ℏ')
    ax3.set_ylabel('L_y/ℏ')
    ax3.set_zlabel('L_z/ℏ')
    ax3.set_title(f'角动量空间量子化 (l={l})')

    # 4. 角动量加法
    ax4 = axes[1, 0]
    j1, j2 = 1, 0.5
    j_values = possible_total_j(j1, j2)

    # 绘制能级
    for i, j in enumerate(j_values):
        m_values = allowed_m_values(int(2*j)/2) if j % 1 else allowed_m_values(int(j))
        for m in m_values:
            ax4.scatter(i, m, c='blue', s=50)
        ax4.text(i, max(m_values) + 0.3, f'j={j}', ha='center')

    ax4.set_xticks([])
    ax4.set_ylabel('m')
    ax4.set_title(f'角动量耦合 ({j1}⊗{j2})')
    ax4.grid(True, alpha=0.3)

    # 5. 自旋-轨道分裂
    ax5 = axes[1, 1]
    xi = 1  # 任意单位
    l = 1  # p轨道
    s = 0.5

    # 无耦合能级
    E_0 = 0
    ax5.hlines(E_0, 0, 1, colors='gray', linestyles='--', label='无耦合')

    # 耦合后能级
    for j in possible_total_j(l, s):
        E = spin_orbit_energy(l, s, j, xi) / hbar**2
        label = spectroscopic_notation(2, l, j)
        ax5.hlines(E, 1.5, 2.5, linewidth=2, label=label)
        ax5.text(2.7, E, label)

    ax5.set_xlim(-0.5, 3.5)
    ax5.set_ylabel('E/(ξℏ²)')
    ax5.set_title('自旋-轨道分裂 (2p)')
    ax5.set_xticks([])
    ax5.grid(True, alpha=0.3)

    # 6. 升降算符作用
    ax6 = axes[1, 2]
    l = 2
    m_range = allowed_m_values(l)

    L_plus = [L_plus_coefficient(l, m) / hbar for m in m_range[:-1]]
    L_minus = [L_minus_coefficient(l, m) / hbar for m in m_range[1:]]

    ax6.bar(np.array(m_range[:-1]) - 0.15, L_plus, 0.3, label='L₊', alpha=0.7)
    ax6.bar(np.array(m_range[1:]) + 0.15, L_minus, 0.3, label='L₋', alpha=0.7)
    ax6.set_xlabel('m')
    ax6.set_ylabel('系数/ℏ')
    ax6.set_title(f'升降算符系数 (l={l})')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('angular_momentum.png', dpi=150)
    print("图像已保存为 angular_momentum.png")
    plt.show()


def verify():
    all_passed = True

    # Check 5.1
    L_sq = L_squared_eigenvalue(2)
    expected = hbar**2 * 2 * 3
    if not np.isclose(L_sq, expected, rtol=0.01):
        print("❌ 5.1 L²本征值错误")
        all_passed = False
    else:
        print(f"✓ 5.1 L²本征值正确")

    # Check 5.2
    coeff_plus = L_plus_coefficient(2, 1)
    expected_coeff = hbar * np.sqrt((2-1)*(2+1+1))
    if not np.isclose(coeff_plus, expected_coeff, rtol=0.01):
        print("❌ 5.2 升算符系数错误")
        all_passed = False
    else:
        print("✓ 5.2 升降算符正确")

    # Check 5.3
    # Y_0^0应该是常数
    Y_00 = spherical_harmonic(0, 0, np.pi/4, np.pi/4)
    expected_Y00 = 1 / (2 * np.sqrt(np.pi))
    if not np.isclose(np.abs(Y_00), expected_Y00, rtol=0.01):
        print("❌ 5.3 球谐函数Y_0^0错误")
        all_passed = False
    else:
        print("✓ 5.3 球谐函数正确")

    # Check 5.4
    j_vals = possible_total_j(1, 0.5)
    expected_j = [0.5, 1.5]
    if j_vals != expected_j:
        print("❌ 5.4 角动量耦合j值错误")
        all_passed = False
    else:
        print(f"✓ 5.4 角动量加法正确 (1⊗1/2 → {j_vals})")

    # Check 5.5
    cg = cg_coefficient(0.5, 0.5, 0.5, -0.5, 0, 0)
    if cg is None or not np.isclose(cg, 1/np.sqrt(2), rtol=0.01):
        print("❌ 5.5 CG系数错误")
        all_passed = False
    else:
        print("✓ 5.5 CG系数正确")

    # Check 5.6
    E_32 = spin_orbit_energy(1, 0.5, 1.5, 1)
    E_12 = spin_orbit_energy(1, 0.5, 0.5, 1)
    # 分裂应该为 3/2 ξℏ²
    splitting = (E_32 - E_12) / hbar**2
    if not np.isclose(splitting, 1.5, rtol=0.01):
        print("❌ 5.6 自旋-轨道分裂错误")
        all_passed = False
    else:
        print(f"✓ 5.6 自旋-轨道耦合正确 (分裂 = {splitting}ξℏ²)")

    if all_passed:
        print("\n🎉 所有测试通过！")
        try:
            plot_angular_momentum()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("角动量与自旋 Angular Momentum and Spin")
    print("=" * 50)
    verify()
