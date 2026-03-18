"""
电场与电势 Electric Field and Potential
难度 Difficulty: ★★★

学习目标 Learning Objectives:
- 理解库仑定律和电场概念 (Understand Coulomb's law and electric field concepts)
- 计算点电荷和电荷分布产生的电场 (Calculate electric fields from point charges and charge distributions)
- 掌握电势的计算和物理意义 (Master potential calculation and physical meaning)
- 可视化电场线和等势线 (Visualize electric field lines and equipotential lines)
- 理解电场与电势的关系 E = -∇V (Understand the relationship between E and V)

物理背景 Physical Background:
电场是电荷周围空间的一种物质形态，任何电荷都在其周围激发电场。电场对放入其中的
其他电荷有力的作用。电势是描述电场能量特性的物理量，是标量场。

核心公式 Key Formulas:
- 库仑定律 Coulomb's Law: F = k*q1*q2/r² [N]
- 电场强度 Electric Field: E = F/q = k*Q/r² [N/C 或 V/m]
- 电势 Electric Potential: V = k*Q/r [V]
- 高斯定律 Gauss's Law: Φ = ∮E·dA = Q_enc/ε₀

物理常数 Physical Constants:
- 库仑常数 k = 8.99×10⁹ N·m²/C² (Coulomb constant)
- 真空介电常数 ε₀ = 8.85×10⁻¹² F/m (Vacuum permittivity)
- 元电荷 e = 1.60×10⁻¹⁹ C (Elementary charge)

单位说明 Units:
- 电场强度: N/C = V/m
- 电势: V (伏特)
- 电荷: C (库仑)
- 电通量: N·m²/C = V·m
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import k_e, epsilon_0, e

# I AM NOT DONE

# =============================================================================
# 练习 1.1: 点电荷的电场
# Exercise 1.1: Electric Field of Point Charge
# =============================================================================
# 物理背景 Physical Background:
# 点电荷是理想化模型，将电荷集中于一个几何点。
# 点电荷产生的电场呈球对称分布，场强与距离平方成反比。
#
# 核心公式 Key Formula:
# E = k*Q/r² (方向沿径向 r̂)
# 其中 k = 1/(4πε₀) = 8.99×10⁹ N·m²/C²
#
# 正电荷: 电场向外发散
# 负电荷: 电场向内汇聚

def point_charge_field(Q, r_vec):
    """
    计算点电荷在位置 r_vec 处产生的电场
    Calculate the electric field produced by a point charge at position r_vec

    参数 Parameters:
        Q: 电荷量 [C] (正值表示正电荷，负值表示负电荷)
           Charge amount (positive for positive charge)
        r_vec: 从电荷指向场点的位置向量 [x, y] [m]
               Position vector from charge to field point

    返回 Returns:
        电场向量 [Ex, Ey] [N/C 或 V/m]
        Electric field vector

    公式 Formula:
        E = k*Q/r² * r̂, 其中 r̂ = r_vec/|r_vec|
    """
    r = np.sqrt(r_vec[0]**2 + r_vec[1]**2)
    if r < 1e-10:  # 避免除以零 (Avoid division by zero)
        return np.array([0.0, 0.0])

    # TODO: 计算电场 (Calculate electric field)
    # 步骤 Steps:
    # 1. 计算电场大小: E = k*Q/r²
    # 2. 计算单位矢量: r̂ = r_vec/r
    # 3. 电场矢量: E_vec = E * r̂
    E_magnitude = k_e * Q / r**2
    E_vec = E_magnitude * r_vec / r  # 修改这里
    return E_vec


# 测试: 1 μC 电荷在 1 m 处的电场
Q_test = 1e-6  # 1 μC
r_test = np.array([1.0, 0.0])  # 1 m 沿 x 轴
E_test = point_charge_field(Q_test, r_test)


# =============================================================================
# 练习 1.2: 多电荷系统的电场
# Exercise 1.2: Electric Field from Multiple Charges
# =============================================================================
# 物理背景 Physical Background:
# 电场满足叠加原理：多个电荷产生的总电场等于各电荷单独产生电场的矢量和。
# 这是电磁学的基本原理之一，源于麦克斯韦方程的线性性。
#
# 叠加原理 Superposition Principle:
# E_total = E₁ + E₂ + E₃ + ... = Σ Eᵢ
# 注意：是矢量相加，不是标量相加！

def total_electric_field(charges, positions, field_point):
    """
    计算多个点电荷在场点产生的总电场（叠加原理）
    Calculate total electric field from multiple charges using superposition

    参数 Parameters:
        charges: 电荷量列表 [Q1, Q2, ...] [C]
                 List of charge values
        positions: 电荷位置列表 [[x1,y1], [x2,y2], ...] [m]
                   List of charge positions
        field_point: 场点位置 [x, y] [m]
                     Position where field is calculated

    返回 Returns:
        总电场向量 [Ex, Ey] [N/C]
        Total electric field vector

    物理意义 Physical Meaning:
        叠加原理是电磁学的基石，允许我们将复杂问题分解为简单问题的叠加
    """
    E_total = np.array([0.0, 0.0])

    # TODO: 对每个电荷计算电场并矢量求和 (Calculate and sum fields from each charge)
    # 应用叠加原理: E_total = Σ E_i
    for Q, pos in zip(charges, positions):
        r_vec = np.array(field_point) - np.array(pos)
        E = point_charge_field(Q, r_vec)
        E_total += E  # 修改这里（叠加原理 Superposition）

    return E_total


# 电偶极子: +q 和 -q 相距 d
q = 1e-9  # 1 nC
d = 0.1  # 10 cm
charges_dipole = [q, -q]
positions_dipole = [[d/2, 0], [-d/2, 0]]


# =============================================================================
# 练习 1.3: 电场线可视化
# Exercise 1.3: Electric Field Lines Visualization
# =============================================================================
# 物理背景 Physical Background:
# 电场线是用来形象描述电场的曲线，具有以下性质:
# 1. 电场线上每点的切线方向即为该点电场方向
# 2. 电场线的疏密程度表示电场强度的大小
# 3. 电场线从正电荷出发，终止于负电荷
# 4. 电场线不相交
#
# 可视化方法: 使用 matplotlib 的 streamplot 函数绘制流线图

def compute_field_grid(charges, positions, x_range, y_range, nx=50, ny=50):
    """
    计算二维网格上每个点的电场，用于电场线可视化
    Compute electric field on a 2D grid for visualization

    参数 Parameters:
        charges: 电荷量列表 [C]
        positions: 电荷位置列表 [m]
        x_range: x方向范围 [x_min, x_max] [m]
        y_range: y方向范围 [y_min, y_max] [m]
        nx, ny: x和y方向的网格点数

    返回 Returns:
        X, Y: 网格坐标 (meshgrid format)
        Ex, Ey: 对应点的电场分量 [N/C]
    """
    x = np.linspace(x_range[0], x_range[1], nx)
    y = np.linspace(y_range[0], y_range[1], ny)
    X, Y = np.meshgrid(x, y)

    Ex = np.zeros_like(X)
    Ey = np.zeros_like(Y)

    # TODO: 计算每个网格点的电场 (Compute field at each grid point)
    # 遍历所有网格点，调用 total_electric_field 函数
    for i in range(ny):
        for j in range(nx):
            E = total_electric_field(charges, positions, [X[i,j], Y[i,j]])
            Ex[i,j] = E[0]
            Ey[i,j] = E[1]

    return X, Y, Ex, Ey


# =============================================================================
# 练习 1.4: 电势
# Exercise 1.4: Electric Potential
# =============================================================================
# 物理背景 Physical Background:
# 电势是描述电场能量特性的标量场。
# 电势差(电压)表示单位正电荷从一点移动到另一点时电场力做的功。
#
# 核心公式 Key Formula:
# V = k*Q/r [V]
# 电势能: U = qV [J]
# 电场与电势关系: E = -∇V
#
# 重要性质 Key Properties:
# 1. 电势是标量，可以直接代数相加
# 2. 正电荷周围电势为正，负电荷周围电势为负
# 3. 等势面与电场线垂直

def point_charge_potential(Q, r):
    """
    计算点电荷在距离 r 处产生的电势
    Calculate electric potential at distance r from a point charge

    参数 Parameters:
        Q: 电荷量 [C]
        r: 距离 [m]

    返回 Returns:
        电势 V [V] (伏特)

    公式 Formula:
        V = k*Q/r = Q/(4πε₀r)

    物理意义: 将单位正电荷从无穷远处移到该点，电场力做的功
    """
    if r < 1e-10:
        return np.inf if Q > 0 else -np.inf
    # TODO: 返回电势 (Return the potential)
    return k_e * Q / r  # 修改这里


def total_potential(charges, positions, field_point):
    """
    计算多电荷系统在场点的总电势
    Calculate total potential from multiple charges

    物理原理 Physical Principle:
        电势是标量，直接代数相加（不是矢量和）
        V_total = V₁ + V₂ + V₃ + ... = Σ Vᵢ

    这比电场的矢量叠加简单得多！
    """
    V_total = 0.0

    # TODO: 计算总电势（标量相加，比电场简单！）
    # 遍历每个电荷，计算其产生的电势并累加
    for Q, pos in zip(charges, positions):
        r = np.sqrt((field_point[0] - pos[0])**2 + (field_point[1] - pos[1])**2)
        V_total += point_charge_potential(Q, r)  # 修改这里

    return V_total


def compute_potential_grid(charges, positions, x_range, y_range, nx=100, ny=100):
    """
    计算网格上的电势分布，用于绘制等势线
    Compute potential on a grid for equipotential line visualization
    """
    x = np.linspace(x_range[0], x_range[1], nx)
    y = np.linspace(y_range[0], y_range[1], ny)
    X, Y = np.meshgrid(x, y)
    V = np.zeros_like(X)

    for i in range(ny):
        for j in range(nx):
            V[i,j] = total_potential(charges, positions, [X[i,j], Y[i,j]])

    # 限制极值以便可视化 (Clip extreme values for visualization)
    V = np.clip(V, -1e6, 1e6)
    return X, Y, V


# =============================================================================
# 练习 1.5: 电场与电势的关系
# Exercise 1.5: Relationship Between E and V
# =============================================================================
# 物理背景 Physical Background:
# 电场是电势的负梯度，这是电磁学中最重要的关系之一。
# 电场总是指向电势降低最快的方向。
#
# 核心公式 Key Formula:
# E = -∇V = -(∂V/∂x, ∂V/∂y, ∂V/∂z)
# 分量形式: Ex = -∂V/∂x, Ey = -∂V/∂y, Ez = -∂V/∂z
#
# 数值方法 Numerical Method:
# 使用中心差分: Ex ≈ -(V(x+dx) - V(x-dx))/(2dx)
# numpy.gradient 函数自动实现此计算

def field_from_potential(V_grid, dx, dy):
    """
    从电势分布计算电场（数值梯度法）
    Calculate electric field from potential using numerical gradient

    参数 Parameters:
        V_grid: 电势网格数据 [V]
        dx: x方向网格间距 [m]
        dy: y方向网格间距 [m]

    返回 Returns:
        Ex, Ey: 电场分量 [N/C]

    核心公式 Formula:
        E = -∇V
        注意负号！电场指向电势降低的方向
    """
    # TODO: 使用 numpy.gradient 计算电场 (Use numpy.gradient to compute field)
    # 注意负号！E = -∇V (Note the negative sign!)
    # np.gradient 返回 (dV/dy, dV/dx) 的顺序
    dVdy, dVdx = np.gradient(V_grid, dy, dx)
    Ex = -dVdx  # 修改这里
    Ey = -dVdy  # 修改这里
    return Ex, Ey


# =============================================================================
# 练习 1.6: 电通量与高斯定律
# Exercise 1.6: Electric Flux and Gauss's Law
# =============================================================================
# 物理背景 Physical Background:
# 高斯定律是麦克斯韦方程组的第一个方程，表述了电场与电荷的基本关系。
# 它表明：通过任意闭合曲面的电通量正比于曲面内包围的电荷量。
#
# 核心公式 Key Formula:
# Φ = ∮ E·dA = Q_enc/ε₀
#
# 应用条件 Application:
# 高斯定律对任意电荷分布都成立，但只有在具有高度对称性时才便于计算:
# - 球对称: 点电荷、均匀带电球
# - 柱对称: 无限长带电直线
# - 平面对称: 无限大带电平面

def gauss_law_sphere(Q, r):
    """
    使用高斯定律计算球对称电荷分布的电场
    Calculate E for spherically symmetric charge using Gauss's law

    参数 Parameters:
        Q: 包围的电荷量 [C]
        r: 高斯球面半径 [m]

    返回 Returns:
        电场强度 E [N/C]

    推导 Derivation:
        高斯定律: Φ = ∮E·dA = Q/ε₀
        球对称性: E处处相等，方向径向
        ∮E·dA = E × 4πr² = Q/ε₀
        ∴ E = Q/(4πε₀r²)
    """
    # TODO: 使用高斯定律计算电场大小 (Use Gauss's law to calculate E)
    E = Q / (4 * np.pi * epsilon_0 * r**2)  # 修改这里
    return E


def verify_gauss_law(Q, r):
    """
    验证高斯定律: 计算通量并与理论值比较
    Verify Gauss's law: compare calculated flux with Q/ε₀

    验证条件 Verification:
        Φ_calculated = E × A = E × 4πr²
        Φ_expected = Q/ε₀
        两者应相等
    """
    E = gauss_law_sphere(Q, r)
    A = 4 * np.pi * r**2  # 球面面积
    # TODO: 计算通量 (Calculate flux)
    flux = E * A  # 修改这里: Φ = E × A (对于均匀场垂直穿过)
    expected_flux = Q / epsilon_0
    return flux, expected_flux


# =============================================================================
# 可视化
# =============================================================================
def plot_fields():
    """绘制电场和电势"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # 1. 单电荷电场线
    ax1 = axes[0, 0]
    Q_single = 1e-9
    charges_single = [Q_single]
    positions_single = [[0, 0]]
    X, Y, Ex, Ey = compute_field_grid(charges_single, positions_single,
                                       [-0.2, 0.2], [-0.2, 0.2], 20, 20)
    E_mag = np.sqrt(Ex**2 + Ey**2)
    ax1.streamplot(X, Y, Ex, Ey, color=np.log10(E_mag+1), cmap='viridis', density=1.5)
    ax1.plot(0, 0, 'ro', markersize=10, label='+Q')
    ax1.set_xlabel('x (m)')
    ax1.set_ylabel('y (m)')
    ax1.set_title('单电荷电场线 Single Charge Field')
    ax1.set_aspect('equal')
    ax1.legend()

    # 2. 电偶极子电场线
    ax2 = axes[0, 1]
    X, Y, Ex, Ey = compute_field_grid(charges_dipole, positions_dipole,
                                       [-0.2, 0.2], [-0.2, 0.2], 25, 25)
    E_mag = np.sqrt(Ex**2 + Ey**2)
    ax2.streamplot(X, Y, Ex, Ey, color=np.log10(E_mag+1), cmap='viridis', density=2)
    ax2.plot(d/2, 0, 'ro', markersize=10, label='+q')
    ax2.plot(-d/2, 0, 'bo', markersize=10, label='-q')
    ax2.set_xlabel('x (m)')
    ax2.set_ylabel('y (m)')
    ax2.set_title('电偶极子电场 Electric Dipole')
    ax2.set_aspect('equal')
    ax2.legend()

    # 3. 电势等势线（电偶极子）
    ax3 = axes[1, 0]
    X, Y, V = compute_potential_grid(charges_dipole, positions_dipole,
                                      [-0.15, 0.15], [-0.15, 0.15], 100, 100)
    levels = np.linspace(-500, 500, 21)
    cs = ax3.contour(X, Y, V, levels=levels, cmap='RdBu_r')
    ax3.clabel(cs, inline=True, fontsize=8, fmt='%.0f')
    ax3.plot(d/2, 0, 'ro', markersize=8)
    ax3.plot(-d/2, 0, 'bo', markersize=8)
    ax3.set_xlabel('x (m)')
    ax3.set_ylabel('y (m)')
    ax3.set_title('等势线 Equipotential Lines (V)')
    ax3.set_aspect('equal')

    # 4. 电场与电势关系验证
    ax4 = axes[1, 1]
    # 沿 x 轴绘制 E 和 -dV/dx
    x_line = np.linspace(-0.15, 0.15, 100)
    E_direct = []
    V_line = []
    for x in x_line:
        if abs(x - d/2) < 0.01 or abs(x + d/2) < 0.01:
            E_direct.append(np.nan)
            V_line.append(np.nan)
        else:
            E = total_electric_field(charges_dipole, positions_dipole, [x, 0])
            E_direct.append(E[0])
            V_line.append(total_potential(charges_dipole, positions_dipole, [x, 0]))

    E_direct = np.array(E_direct)
    V_line = np.array(V_line)
    dVdx = -np.gradient(V_line, x_line[1]-x_line[0])

    ax4.plot(x_line, E_direct, 'b-', label='E (direct)', linewidth=2)
    ax4.plot(x_line, dVdx, 'r--', label='-dV/dx', linewidth=2)
    ax4.set_xlabel('x (m)')
    ax4.set_ylabel('E_x (N/C)')
    ax4.set_title('E = -∇V 验证')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim(-5e5, 5e5)

    plt.tight_layout()
    plt.savefig('electric_field.png', dpi=150)
    print("图像已保存为 electric_field.png")
    plt.show()


# =============================================================================
# 验证函数
# =============================================================================
def verify():
    """
    验证所有练习的正确性
    Verify correctness of all exercises
    """
    all_passed = True

    # 检查 1.1 - 点电荷电场 (Check point charge field)
    expected_E = k_e * Q_test / 1.0**2  # E = kQ/r²
    if E_test is None or len(E_test) != 2:
        print("❌ 1.1 点电荷电场返回格式错误（应返回二维向量）")
        print("   错误原因: 函数应返回 [Ex, Ey] 格式的数组")
        all_passed = False
    elif not np.isclose(E_test[0], expected_E, rtol=0.01):
        print(f"❌ 1.1 点电荷电场错误: 期望 {expected_E:.2f} N/C, 得到 {E_test[0]:.2f} N/C")
        print("   提示: 检查公式 E = k*Q/r² 是否正确实现")
        all_passed = False
    else:
        print(f"✓ 1.1 点电荷电场正确 (E = {expected_E:.0f} N/C)")

    # 检查 1.2 - 多电荷系统 (Check multiple charges)
    # 在偶极子原点处，电场应沿+x到-x方向（从正电荷指向负电荷）
    E_dipole_origin = total_electric_field(charges_dipole, positions_dipole, [0, 0])
    # 电场在原点处从正电荷指向负电荷，即沿 -x 方向
    if E_dipole_origin[0] >= 0:
        print("❌ 1.2 电偶极子场方向错误（原点处应指向-x方向）")
        print("   物理解释: 在偶极子中心，电场从正电荷指向负电荷")
        all_passed = False
    else:
        print("✓ 1.2 多电荷系统电场正确（叠加原理验证通过）")

    # 检查 1.3 - 电场网格计算 (Check field grid computation)
    X, Y, Ex, Ey = compute_field_grid([1e-9], [[0,0]], [-0.1, 0.1], [-0.1, 0.1], 10, 10)
    if X.shape != (10, 10) or Ex.shape != (10, 10):
        print("❌ 1.3 电场网格计算错误（返回数组维度不正确）")
        all_passed = False
    else:
        print("✓ 1.3 电场网格计算正确（可用于可视化）")

    # 检查 1.4 - 电势 (Check potential)
    V_test = point_charge_potential(Q_test, 1.0)
    expected_V = k_e * Q_test / 1.0
    if not np.isclose(V_test, expected_V, rtol=0.01):
        print(f"❌ 1.4 电势计算错误: 期望 {expected_V:.0f} V, 得到 {V_test:.0f} V")
        print("   提示: 检查公式 V = k*Q/r 是否正确实现")
        all_passed = False
    else:
        print(f"✓ 1.4 电势计算正确 (V = {expected_V:.0f} V)")

    # 检查 1.5 - 从电势计算电场 (Check E from V)
    # 创建测试用例: V = x² + y²，则 E = -∇V = (-2x, -2y)
    x_test = np.linspace(-1, 1, 50)
    y_test = np.linspace(-1, 1, 50)
    X_test, Y_test = np.meshgrid(x_test, y_test)
    V_test_grid = X_test**2 + Y_test**2  # V = x² + y², 则 E = -2x, -2y
    Ex_test, Ey_test = field_from_potential(V_test_grid, x_test[1]-x_test[0], y_test[1]-y_test[0])
    # 在中心点 (0,0)，Ex 应该约等于 0
    center = len(x_test) // 2
    if not np.isclose(Ex_test[center, center], 0, atol=0.1):
        print("❌ 1.5 从电势计算电场错误（E = -∇V 关系验证失败）")
        print("   提示: 检查是否正确使用了负号")
        all_passed = False
    else:
        print("✓ 1.5 E = -∇V 计算正确（电场是电势的负梯度）")

    # 检查 1.6 - 高斯定律 (Check Gauss's law)
    flux, expected_flux = verify_gauss_law(1e-9, 0.1)
    if not np.isclose(flux, expected_flux, rtol=0.01):
        print(f"❌ 1.6 高斯定律验证失败: 计算通量 Φ={flux:.2e}, 理论值 Q/ε₀={expected_flux:.2e}")
        print("   提示: 检查通量计算公式 Φ = E × A")
        all_passed = False
    else:
        print(f"✓ 1.6 高斯定律验证正确 (Φ = Q/ε₀ = {expected_flux:.2e} N·m²/C)")

    if all_passed:
        print("\n🎉 所有测试通过！正在生成可视化...")
        try:
            plot_fields()
        except Exception as e:
            print(f"可视化生成失败: {e}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("电场与电势 Electric Field and Potential")
    print("=" * 50)
    verify()
