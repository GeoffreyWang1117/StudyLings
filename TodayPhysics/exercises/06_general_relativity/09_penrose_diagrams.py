"""
彭罗斯图与因果结构 Penrose Diagrams and Causal Structure
难度 Difficulty: ★★★★★

学习目标 Learning Objectives:
- 理解时空的共形结构和彭罗斯图的构造方法
- 掌握因果关系：类时、类空、类光分离
- 分析不同时空的全局因果结构：闵可夫斯基、史瓦西、克尔、de Sitter
- 理解各类视界：事件视界、视在视界、粒子视界、宇宙学视界

物理背景 Physical Background:
彭罗斯图（conformal diagram）是Roger Penrose发明的强大工具，
用于可视化时空的全局因果结构。通过共形变换，无穷大被"拉近"到
有限区域，使我们能够在一张图上看到整个时空的结构。

共形变换的关键性质 Key Property of Conformal Transformation:
共形变换 ds'² = Ω²ds² 保持因果结构：
  - 类光测地线（光线）仍是45°直线
  - 类时曲线仍在光锥内
  - 类空曲线仍在光锥外

彭罗斯图的无穷远结构 Infinity Structure:
  - i⁺ (future timelike infinity): 时间正无穷
  - i⁻ (past timelike infinity): 时间负无穷
  - i⁰ (spatial infinity): 空间无穷远
  - I⁺ (future null infinity, "scri plus"): 未来类光无穷远
  - I⁻ (past null infinity, "scri minus"): 过去类光无穷远

关键坐标变换 Key Coordinate Transformations:
  - 彭罗斯坐标: U = arctan(u), V = arctan(v)，其中 u = t+r, v = t-r
  - 乌龟坐标（史瓦西）: r* = r + r_s ln(r/r_s - 1)
  - Kruskal-Szekeres坐标: U = -e^(-u/2r_s), V = e^(v/2r_s)

单位说明 Units:
  - 坐标通常无量纲化（以r_s、M或H⁻¹为单位）
  - 彭罗斯时间/空间坐标: 弧度 (rad)，范围 [-π/2, π/2]
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import G, c

# I AM NOT DONE

# =============================================================================
# 练习 9.1: 共形变换
# Exercise 9.1: Conformal Transformations
# =============================================================================
def minkowski_to_penrose(t, r):
    """
    闵可夫斯基时空到彭罗斯坐标
    U = arctan(t + r), V = arctan(t - r)
    T' = (U + V)/2, R' = (U - V)/2
    """
    u = t + r  # 出射类光坐标
    v = t - r  # 入射类光坐标

    U = np.arctan(u)
    V = np.arctan(v)

    T_prime = (U + V) / 2
    R_prime = (U - V) / 2

    return T_prime, R_prime

def penrose_to_minkowski(T_prime, R_prime):
    """
    彭罗斯坐标到闵可夫斯基时空
    """
    U = T_prime + R_prime
    V = T_prime - R_prime

    u = np.tan(U)
    v = np.tan(V)

    t = (u + v) / 2
    r = (u - v) / 2

    return t, r

def conformal_factor(t, r, a=1):
    """
    共形因子
    Ω² = cos²U × cos²V = 1/((1+u²)(1+v²))
    """
    u = t + r
    v = t - r
    return 1 / ((1 + u**2) * (1 + v**2))


# =============================================================================
# 练习 9.2: 因果结构
# Exercise 9.2: Causal Structure
# =============================================================================
def is_timelike_separated(t1, r1, t2, r2):
    """
    判断两事件是否类时分离
    Δs² = -(Δt)² + (Δr)² < 0 类时
    """
    ds2 = -(t2 - t1)**2 + (r2 - r1)**2
    return ds2 < 0

def is_spacelike_separated(t1, r1, t2, r2):
    """
    判断两事件是否类空分离
    Δs² > 0 类空
    """
    ds2 = -(t2 - t1)**2 + (r2 - r1)**2
    return ds2 > 0

def is_null_separated(t1, r1, t2, r2, tol=1e-10):
    """
    判断两事件是否类光分离
    Δs² = 0 类光
    """
    ds2 = -(t2 - t1)**2 + (r2 - r1)**2
    return np.abs(ds2) < tol

def light_cone_future(t0, r0, t_range):
    """
    未来光锥
    r = r0 ± (t - t0)
    """
    r_out = r0 + (t_range - t0)  # 出射
    r_in = np.abs(r0 - (t_range - t0))  # 入射
    return r_out, r_in


# =============================================================================
# 练习 9.3: 闵可夫斯基时空无穷远
# Exercise 9.3: Minkowski Spacetime Infinities
# =============================================================================
def spatial_infinity():
    """
    空间无穷远 i⁰
    r → ∞, t = const
    彭罗斯图中: T' = 0, R' = π/2
    """
    return 0, np.pi/2

def future_timelike_infinity():
    """
    未来类时无穷远 i⁺
    t → +∞, r = const
    彭罗斯图中: T' = π/2, R' = 0
    """
    return np.pi/2, 0

def past_timelike_infinity():
    """
    过去类时无穷远 i⁻
    t → -∞, r = const
    彭罗斯图中: T' = -π/2, R' = 0
    """
    return -np.pi/2, 0

def future_null_infinity(R_prime):
    """
    未来类光无穷远 I⁺ (scri plus)
    u → +∞
    彭罗斯图中: T' + R' = π/2
    """
    return np.pi/2 - R_prime

def past_null_infinity(R_prime):
    """
    过去类光无穷远 I⁻ (scri minus)
    v → -∞
    彭罗斯图中: T' - R' = -π/2
    """
    return -np.pi/2 + R_prime


# =============================================================================
# 练习 9.4: 史瓦西时空
# Exercise 9.4: Schwarzschild Spacetime
# =============================================================================
def schwarzschild_tortoise(r, r_s):
    """
    乌龟坐标
    r* = r + r_s ln(r/r_s - 1)
    """
    if r <= r_s:
        return -np.inf
    return r + r_s * np.log(r / r_s - 1)

def schwarzschild_eddington_finkelstein_v(t, r, r_s):
    """
    Eddington-Finkelstein入射坐标
    v = t + r*
    """
    r_star = schwarzschild_tortoise(r, r_s)
    return t + r_star

def kruskal_coordinates(t, r, r_s):
    """
    Kruskal-Szekeres坐标（区域I: r > r_s）
    U = -exp(-u/(2r_s)), V = exp(v/(2r_s))
    """
    r_star = schwarzschild_tortoise(r, r_s)
    u = t - r_star
    v = t + r_star

    U = -np.exp(-u / (2 * r_s))
    V = np.exp(v / (2 * r_s))

    return U, V

def schwarzschild_penrose_coordinates(U, V):
    """
    史瓦西彭罗斯坐标
    使用 arctan 压缩
    """
    U_prime = np.arctan(U)
    V_prime = np.arctan(V)

    T = (U_prime + V_prime) / 2
    R = (V_prime - U_prime) / 2

    return T, R


# =============================================================================
# 练习 9.5: 视界
# Exercise 9.5: Horizons
# =============================================================================
def event_horizon_schwarzschild(M):
    """
    史瓦西事件视界
    r_h = 2GM/c²
    """
    return 2 * G * M / c**2

def apparent_horizon(M, a=0):
    """
    视在视界（克尔情况）
    r_+ = M + √(M² - a²)
    """
    M_geom = G * M / c**2
    return M_geom + np.sqrt(M_geom**2 - a**2)

def cosmological_horizon(H):
    """
    宇宙学视界（de Sitter）
    r_H = c/H
    """
    return c / H

def cauchy_horizon_kerr(M, a):
    """
    柯西视界（克尔内视界）
    r_- = M - √(M² - a²)
    """
    M_geom = G * M / c**2
    if a > M_geom:
        return None
    return M_geom - np.sqrt(M_geom**2 - a**2)


# =============================================================================
# 练习 9.6: 宇宙学彭罗斯图
# Exercise 9.6: Cosmological Penrose Diagrams
# =============================================================================
def de_sitter_conformal_time(a, H):
    """
    de Sitter共形时间
    η = -1/(aH)
    """
    return -1 / (a * H)

def frw_conformal_time_integral(a, H0, Omega_m, Omega_Lambda):
    """
    FRW宇宙共形时间积分（简化）
    η = ∫ da/(a²H(a))
    """
    # 简化：仅考虑物质主导
    return 2 / (H0 * np.sqrt(Omega_m) * np.sqrt(a))

def particle_horizon_comoving(eta):
    """
    粒子视界（共动距离）
    χ_ph = c × η
    """
    return c * eta

def event_horizon_cosmological(eta_final, eta_now):
    """
    事件视界（宇宙学）
    χ_eh = c × (η_final - η_now)
    """
    return c * (eta_final - eta_now)


# =============================================================================
# 可视化
# =============================================================================
def plot_penrose_diagrams():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 闵可夫斯基彭罗斯图
    ax1 = axes[0, 0]

    # 边界
    R = np.linspace(0, np.pi/2, 100)
    I_plus = np.pi/2 - R
    I_minus = -np.pi/2 + R

    ax1.plot(R, I_plus, 'b-', linewidth=2, label='I⁺')
    ax1.plot(R, I_minus, 'b-', linewidth=2, label='I⁻')
    ax1.plot([0, 0], [-np.pi/2, np.pi/2], 'k-', linewidth=1)
    ax1.plot([np.pi/2], [0], 'ko', markersize=10, label='i⁰')
    ax1.plot([0], [np.pi/2], 'ro', markersize=10, label='i⁺')
    ax1.plot([0], [-np.pi/2], 'go', markersize=10, label='i⁻')

    # 等时线
    for t in [-2, -1, 0, 1, 2]:
        r = np.linspace(0, 10, 100)
        T, R_p = minkowski_to_penrose(t, r)
        valid = (R_p >= 0) & (R_p <= np.pi/2) & (np.abs(T) <= np.pi/2 - R_p)
        ax1.plot(R_p[valid], T[valid], 'g--', alpha=0.5, linewidth=0.5)

    # 等r线
    for r0 in [0.5, 1, 2, 5]:
        t = np.linspace(-10, 10, 100)
        T, R_p = minkowski_to_penrose(t, r0)
        valid = (R_p >= 0) & (R_p <= np.pi/2) & (np.abs(T) <= np.pi/2 - R_p)
        ax1.plot(R_p[valid], T[valid], 'r--', alpha=0.5, linewidth=0.5)

    ax1.set_xlabel("R'")
    ax1.set_ylabel("T'")
    ax1.set_title('闵可夫斯基彭罗斯图')
    ax1.set_xlim(0, np.pi/2 + 0.1)
    ax1.set_ylim(-np.pi/2 - 0.1, np.pi/2 + 0.1)
    ax1.set_aspect('equal')
    ax1.legend(loc='upper right', fontsize=8)

    # 2. 因果结构
    ax2 = axes[0, 1]

    # 事件P
    t0, r0 = 0, 0
    ax2.plot(r0, t0, 'ko', markersize=10, label='P')

    # 光锥
    t_range = np.linspace(0, 2, 100)
    r_out, r_in = light_cone_future(t0, r0, t_range)
    ax2.plot(r_out, t_range, 'b-', linewidth=2, label='未来光锥')
    ax2.plot(-r_out, t_range, 'b-', linewidth=2)

    t_past = np.linspace(-2, 0, 100)
    ax2.plot(-(t_past), t_past, 'r-', linewidth=2, label='过去光锥')
    ax2.plot(t_past, t_past, 'r-', linewidth=2)

    # 标记区域
    ax2.fill_between([0, 2], [0, 2], [0, 0], alpha=0.2, color='green', label='类时未来')
    ax2.fill_between([0, -2], [0, 2], [0, 0], alpha=0.2, color='green')

    ax2.set_xlabel('r')
    ax2.set_ylabel('t')
    ax2.set_title('因果结构（光锥）')
    ax2.set_xlim(-2.5, 2.5)
    ax2.set_ylim(-2.5, 2.5)
    ax2.set_aspect('equal')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 史瓦西乌龟坐标
    ax3 = axes[0, 2]
    r_s = 1
    r = np.linspace(1.01 * r_s, 10 * r_s, 200)

    r_star = [schwarzschild_tortoise(ri, r_s) for ri in r]

    ax3.plot(r/r_s, r_star, 'b-', linewidth=2)
    ax3.axvline(x=1, color='r', linestyle='--', label='视界')
    ax3.set_xlabel('r/r_s')
    ax3.set_ylabel('r*/r_s')
    ax3.set_title('乌龟坐标')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 史瓦西彭罗斯图（简化）
    ax4 = axes[1, 0]

    # 视界（45度线）
    ax4.plot([0, 1], [0, 1], 'r-', linewidth=3, label='事件视界')
    ax4.plot([0, 1], [0, -1], 'b-', linewidth=3, label='过去视界')

    # 奇点
    ax4.plot([0, 1], [1, 1], 'k-', linewidth=3, label='奇点')
    ax4.plot([0, 1], [-1, -1], 'k--', linewidth=3)

    # 无穷远
    ax4.plot([1, 2], [1, 0], 'g-', linewidth=2, label='I⁺')
    ax4.plot([1, 2], [-1, 0], 'g-', linewidth=2)

    ax4.plot([2], [0], 'ko', markersize=8, label='i⁰')

    ax4.set_xlabel('U')
    ax4.set_ylabel('V')
    ax4.set_title('史瓦西彭罗斯图（示意）')
    ax4.legend(fontsize=8)
    ax4.set_aspect('equal')

    # 5. 克尔黑洞结构
    ax5 = axes[1, 1]
    M = 1
    a_range = np.linspace(0, 0.99, 100)

    r_plus = [apparent_horizon(M, a * G * M / c**2) / (G * M / c**2) for a in a_range]
    r_minus = []
    for a in a_range:
        r_m = cauchy_horizon_kerr(M, a * G * M / c**2)
        if r_m is not None:
            r_minus.append(r_m / (G * M / c**2))
        else:
            r_minus.append(0)

    ax5.plot(a_range, r_plus, 'b-', linewidth=2, label='外视界 r₊')
    ax5.plot(a_range, r_minus, 'r-', linewidth=2, label='内视界 r₋')
    ax5.axhline(y=2, color='g', linestyle='--', alpha=0.5, label='史瓦西')
    ax5.set_xlabel('a/(GM/c²)')
    ax5.set_ylabel('r/(GM/c²)')
    ax5.set_title('克尔黑洞视界')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. de Sitter彭罗斯图
    ax6 = axes[1, 2]

    # de Sitter边界
    ax6.plot([0, 1], [1, 0], 'b-', linewidth=2, label='I⁺')
    ax6.plot([0, 1], [-1, 0], 'b-', linewidth=2, label='I⁻')
    ax6.plot([0, -1], [1, 0], 'b-', linewidth=2)
    ax6.plot([0, -1], [-1, 0], 'b-', linewidth=2)

    # 原点
    ax6.plot([0], [0], 'ko', markersize=8)

    # 视界
    ax6.plot([0, 1], [0, 1], 'r--', linewidth=2, label='宇宙学视界')
    ax6.plot([0, -1], [0, 1], 'r--', linewidth=2)

    ax6.set_xlabel('χ')
    ax6.set_ylabel('η')
    ax6.set_title('de Sitter彭罗斯图')
    ax6.legend(fontsize=8)
    ax6.set_aspect('equal')

    plt.tight_layout()
    plt.savefig('penrose_diagrams.png', dpi=150)
    print("图像已保存为 penrose_diagrams.png")
    plt.show()


def verify():
    """
    验证所有练习的正确性
    Verify all exercises for correctness
    """
    all_passed = True

    # 检查 9.1 - 共形变换 Conformal transformation
    T, R = minkowski_to_penrose(0, 0)
    if T != 0 or R != 0:
        print("错误 9.1: 时空原点应映射到彭罗斯图原点")
        all_passed = False
    else:
        print("正确 9.1: 共形变换")

    # 检查 9.2 - 因果结构 Causal structure
    if not is_timelike_separated(0, 0, 1, 0):
        print("错误 9.2: 当 |Delta_t| > |Delta_r| 时应为类时分离")
        all_passed = False
    else:
        print("正确 9.2: 因果结构判断")

    # 检查 9.3 - 无穷远 Infinity
    T_i0, R_i0 = spatial_infinity()
    if not (T_i0 == 0 and np.isclose(R_i0, np.pi/2)):
        print("错误 9.3: 空间无穷远 i^0 应位于 (T=0, R=pi/2)")
        all_passed = False
    else:
        print("正确 9.3: 无穷远结构 (i^0 at R' = pi/2)")

    # 检查 9.4 - 史瓦西时空/乌龟坐标 Schwarzschild spacetime
    r_s = 1  # 以史瓦西半径为单位
    r_star = schwarzschild_tortoise(2 * r_s, r_s)
    if r_star <= 2 * r_s:
        print("错误 9.4: 乌龟坐标 r* 应大于 r（由于对数项）")
        all_passed = False
    else:
        print(f"正确 9.4: 史瓦西时空 (r* = {r_star:.2f})")

    # 检查 9.5 - 事件视界 Event horizon
    from utils.constants import M_sun
    r_h = event_horizon_schwarzschild(M_sun)
    expected = 2 * G * M_sun / c**2
    if not np.isclose(r_h, expected, rtol=0.01):
        print("错误 9.5: 事件视界计算不正确，请检查公式 r_h = 2GM/c²")
        all_passed = False
    else:
        print(f"正确 9.5: 事件视界 (r_h = {r_h:.0f} m)")

    # 检查 9.6 - 宇宙学视界 Cosmological horizon
    H = 70 * 1000 / (3.086e22)  # 70 km/s/Mpc 转换为 SI 单位
    r_H = cosmological_horizon(H)
    if r_H <= 0:
        print("错误 9.6: 宇宙学视界应为正值")
        all_passed = False
    else:
        print(f"正确 9.6: 宇宙学彭罗斯图 (r_H = {r_H/3.086e25:.1f} Gpc)")

    if all_passed:
        print("\n所有测试通过！")
        try:
            plot_penrose_diagrams()
        except Exception as e:
            print(f"可视化失败: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("彭罗斯图与因果结构 Penrose Diagrams and Causal Structure")
    print("=" * 50)
    verify()
