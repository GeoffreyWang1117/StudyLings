"""
衍射 Diffraction
难度 Difficulty: ★★★★

学习目标 Learning Objectives:
- 理解惠更斯-菲涅尔原理及其物理意义
  Understand Huygens-Fresnel principle and its physical meaning
- 掌握单缝衍射的强度分布规律
  Master the intensity distribution of single-slit diffraction
- 分析双缝干涉和多缝光栅的衍射图样
  Analyze diffraction patterns of double-slit and multi-slit gratings
- 计算瑞利判据和光学系统分辨率
  Calculate Rayleigh criterion and optical resolution
- 了解薄膜干涉和迈克尔逊干涉仪原理
  Understand thin-film interference and Michelson interferometer

物理背景 Physical Background:
衍射是波绕过障碍物或通过小孔时偏离直线传播的现象，
是波动性的重要证据。

惠更斯-菲涅尔原理：
波阵面上每一点都可看作新的子波源，子波的包络面即为新波阵面。
子波的相干叠加形成衍射图样。

衍射类型：
1. 夫琅禾费衍射（远场衍射）：
   - 光源和观察屏在无穷远（平行光）
   - 菲涅尔数 F = a²/(λL) << 1
   - 数学处理简单

2. 菲涅尔衍射（近场衍射）：
   - 光源或观察屏在有限距离
   - 菲涅尔数 F ~ 1
   - 需要考虑球面波效应

关键公式：
- 单缝衍射暗纹：a sin(θ) = mλ, m = ±1, ±2, ...
- 光栅明纹：d sin(θ) = mλ, m = 0, ±1, ±2, ...
- 瑞利判据：θ_min = 1.22λ/D

HINT: 单缝衍射: I = I₀(sin(β)/β)², β = (πa sin(θ))/λ
HINT: 双缝干涉: I = 4I₀cos²(δ/2), δ = (2πd sin(θ))/λ
HINT: 光栅方程: d sin(θ) = mλ
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import c

# I AM NOT DONE

# =============================================================================
# 练习 5.1: 单缝衍射
# Exercise 5.1: Single Slit Diffraction
# =============================================================================
def single_slit_intensity(theta, a, wavelength, I0=1.0):
    """
    单缝衍射强度分布 (夫琅禾费衍射)
    I(θ) = I₀ (sin(β)/β)²
    β = (πa sin(θ))/λ

    a: 缝宽
    wavelength: 波长
    theta: 衍射角
    """
    # TODO: 计算强度分布
    beta = np.pi * a * np.sin(theta) / wavelength

    # 处理 β=0 的情况 (sinc(0) = 1)
    intensity = np.where(np.abs(beta) < 1e-10,
                         I0,
                         I0 * (np.sin(beta) / beta)**2)
    return intensity


def single_slit_minima(a, wavelength, m_max=5):
    """
    单缝衍射暗纹位置
    a sin(θ) = mλ, m = ±1, ±2, ...
    """
    minima = []
    for m in range(1, m_max + 1):
        sin_theta = m * wavelength / a
        if abs(sin_theta) <= 1:
            theta = np.arcsin(sin_theta)
            minima.append((m, theta))
    return minima


def single_slit_central_width(a, wavelength):
    """
    中央亮纹的角宽度 (第一级暗纹之间)
    2θ₁ = 2 arcsin(λ/a) ≈ 2λ/a (小角度)
    """
    # TODO: 计算中央亮纹宽度
    sin_theta1 = wavelength / a
    if abs(sin_theta1) <= 1:
        theta1 = np.arcsin(sin_theta1)
        return 2 * theta1
    else:
        return np.pi  # 整个半空间


# =============================================================================
# 练习 5.2: 双缝干涉
# Exercise 5.2: Double Slit Interference
# =============================================================================
def double_slit_intensity(theta, d, wavelength, I0=1.0):
    """
    双缝干涉强度分布 (忽略单缝衍射包络)
    I(θ) = 4I₀ cos²(δ/2)
    δ = (2πd sin(θ))/λ

    d: 缝间距
    """
    # TODO: 计算强度分布
    delta = 2 * np.pi * d * np.sin(theta) / wavelength
    intensity = 4 * I0 * np.cos(delta / 2)**2
    return intensity


def double_slit_with_diffraction(theta, a, d, wavelength, I0=1.0):
    """
    双缝干涉 + 单缝衍射包络
    I(θ) = 单缝衍射包络 × 双缝干涉因子
    """
    # TODO: 计算完整的强度分布
    single_envelope = single_slit_intensity(theta, a, wavelength, 1.0)
    double_interference = double_slit_intensity(theta, d, wavelength, 1.0)
    intensity = I0 * single_envelope * double_interference / 4  # 归一化
    return intensity


def double_slit_maxima(d, wavelength, m_max=5):
    """
    双缝干涉明纹位置
    d sin(θ) = mλ, m = 0, ±1, ±2, ...
    """
    maxima = []
    for m in range(-m_max, m_max + 1):
        sin_theta = m * wavelength / d
        if abs(sin_theta) <= 1:
            theta = np.arcsin(sin_theta)
            maxima.append((m, theta))
    return maxima


# =============================================================================
# 练习 5.3: 多缝光栅
# Exercise 5.3: Diffraction Grating
# =============================================================================
def grating_intensity(theta, N, d, wavelength, I0=1.0):
    """
    N缝光栅的强度分布
    I(θ) = I₀ (sin(Nγ)/sin(γ))²
    γ = (πd sin(θ))/λ
    """
    gamma = np.pi * d * np.sin(theta) / wavelength

    # TODO: 计算光栅强度分布
    # 处理 γ=mπ 的特殊情况（主极大）
    intensity = np.zeros_like(theta)
    for i, g in enumerate(gamma):
        if np.abs(np.sin(g)) < 1e-10:
            intensity[i] = I0 * N**2
        else:
            intensity[i] = I0 * (np.sin(N * g) / np.sin(g))**2

    return intensity


def grating_with_slit_diffraction(theta, N, a, d, wavelength, I0=1.0):
    """
    光栅衍射（包含单缝衍射包络）
    """
    single_envelope = single_slit_intensity(theta, a, wavelength, 1.0)
    grating_pattern = grating_intensity(theta, N, d, wavelength, 1.0)
    intensity = I0 * single_envelope * grating_pattern / N**2  # 归一化
    return intensity


def grating_equation(d, theta, m=1):
    """
    光栅方程求波长
    d sin(θ) = mλ
    """
    # TODO: 计算波长
    wavelength = d * np.sin(theta) / m
    return wavelength


def grating_resolving_power(N, m):
    """
    光栅的分辨本领
    R = λ/Δλ = mN
    """
    return m * N


# =============================================================================
# 练习 5.4: 圆孔衍射和瑞利判据
# Exercise 5.4: Circular Aperture Diffraction and Rayleigh Criterion
# =============================================================================
def airy_disk_angle(D, wavelength):
    """
    艾里斑第一暗环的角半径
    sin(θ) ≈ θ = 1.22λ/D

    D: 圆孔直径
    """
    # TODO: 计算艾里斑角半径
    theta = 1.22 * wavelength / D
    return theta


def rayleigh_resolution(D, wavelength):
    """
    瑞利判据：最小可分辨角
    θ_min = 1.22λ/D
    """
    return airy_disk_angle(D, wavelength)


def telescope_resolution(D, wavelength, f):
    """
    望远镜的线分辨率
    d = f × θ_min = 1.22λf/D

    f: 焦距
    """
    # TODO: 计算线分辨率
    theta_min = rayleigh_resolution(D, wavelength)
    d = f * theta_min
    return d


# =============================================================================
# 练习 5.5: 菲涅尔衍射
# Exercise 5.5: Fresnel Diffraction
# =============================================================================
def fresnel_number(a, wavelength, L):
    """
    菲涅尔数
    F = a²/(λL)
    a: 孔径
    L: 观察距离

    F >> 1: 几何光学区
    F ~ 1: 菲涅尔衍射区
    F << 1: 夫琅禾费衍射区
    """
    # TODO: 计算菲涅尔数
    F = a**2 / (wavelength * L)
    return F


def fresnel_zone_radius(n, wavelength, r, rp):
    """
    第n个菲涅尔半波带的半径
    ρ_n = √(nλrr'/(r+r'))

    r: 光源到孔的距离
    rp: 孔到观察点的距离
    """
    # TODO: 计算菲涅尔带半径
    rho_n = np.sqrt(n * wavelength * r * rp / (r + rp))
    return rho_n


# =============================================================================
# 练习 5.6: 薄膜干涉
# Exercise 5.6: Thin Film Interference
# =============================================================================
def thin_film_path_difference(n, d, theta):
    """
    薄膜干涉的光程差
    Δ = 2nd cos(θ')

    n: 薄膜折射率
    d: 薄膜厚度
    theta: 入射角
    """
    # 折射角
    sin_theta_prime = np.sin(theta) / n
    if np.any(np.abs(sin_theta_prime) > 1):
        return np.inf
    cos_theta_prime = np.sqrt(1 - sin_theta_prime**2)

    # TODO: 计算光程差
    delta = 2 * n * d * cos_theta_prime
    return delta


def thin_film_constructive(n, d, theta, m, half_wave_loss=True):
    """
    薄膜干涉相长的波长
    考虑半波损失
    """
    path_diff = thin_film_path_difference(n, d, theta)

    if half_wave_loss:
        # 相长: Δ = (m + 1/2)λ → λ = 2Δ/(2m+1)
        wavelength = 2 * path_diff / (2 * m + 1)
    else:
        # 相长: Δ = mλ → λ = Δ/m
        wavelength = path_diff / m if m > 0 else np.inf

    return wavelength


# =============================================================================
# 练习 5.7: 迈克尔逊干涉仪
# Exercise 5.7: Michelson Interferometer
# =============================================================================
def michelson_path_difference(d):
    """
    迈克尔逊干涉仪的光程差
    Δ = 2d (d为臂长差)
    """
    return 2 * d


def michelson_fringe_shift(delta_d, wavelength):
    """
    移动反射镜后的条纹移动数
    N = 2Δd/λ
    """
    # TODO: 计算条纹移动数
    N = 2 * delta_d / wavelength
    return N


def measure_wavelength_michelson(N, delta_d):
    """
    用迈克尔逊干涉仪测量波长
    λ = 2Δd/N
    """
    return 2 * delta_d / N


# =============================================================================
# 可视化
# =============================================================================
def plot_diffraction():
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    wavelength = 500e-9  # 500 nm
    theta = np.linspace(-0.1, 0.1, 1000)

    # 1. 单缝衍射
    ax1 = axes[0, 0]
    for a in [10e-6, 20e-6, 50e-6]:
        I = single_slit_intensity(theta, a, wavelength)
        ax1.plot(np.degrees(theta), I, label=f'a = {a*1e6:.0f} μm')
    ax1.set_xlabel('θ (degrees)')
    ax1.set_ylabel('I/I₀')
    ax1.set_title('单缝衍射 Single Slit')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 双缝干涉
    ax2 = axes[0, 1]
    a, d = 10e-6, 50e-6
    I_double = double_slit_with_diffraction(theta, a, d, wavelength)
    ax2.plot(np.degrees(theta), I_double, 'b-', linewidth=1)
    ax2.set_xlabel('θ (degrees)')
    ax2.set_ylabel('I/I₀')
    ax2.set_title(f'双缝干涉 (a={a*1e6:.0f}μm, d={d*1e6:.0f}μm)')
    ax2.grid(True, alpha=0.3)

    # 3. 多缝光栅
    ax3 = axes[0, 2]
    d = 5e-6
    for N in [2, 5, 10, 20]:
        I = grating_intensity(theta, N, d, wavelength)
        I = I / N**2  # 归一化
        ax3.plot(np.degrees(theta), I, label=f'N = {N}', linewidth=1)
    ax3.set_xlabel('θ (degrees)')
    ax3.set_ylabel('I/I₀ (normalized)')
    ax3.set_title('多缝光栅衍射')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 衍射极限
    ax4 = axes[1, 0]
    D_values = np.linspace(1e-3, 10e-3, 100)
    theta_min = [rayleigh_resolution(D, wavelength) for D in D_values]
    ax4.semilogy(D_values * 1e3, np.array(theta_min) * 1e6, 'r-', linewidth=2)
    ax4.set_xlabel('Aperture D (mm)')
    ax4.set_ylabel('θ_min (μrad)')
    ax4.set_title('瑞利判据分辨角')
    ax4.grid(True, alpha=0.3)

    # 5. 薄膜干涉（不同厚度）
    ax5 = axes[1, 1]
    n_film = 1.5
    thicknesses = np.linspace(100e-9, 500e-9, 100)
    wavelengths_visible = np.linspace(400e-9, 700e-9, 100)
    d_mesh, lambda_mesh = np.meshgrid(thicknesses, wavelengths_visible)
    path_diff = 2 * n_film * d_mesh
    # 干涉条件（近似）
    m_eff = path_diff / lambda_mesh
    intensity = np.cos(np.pi * m_eff)**2
    im = ax5.contourf(thicknesses * 1e9, wavelengths_visible * 1e9, intensity, 20, cmap='RdYlBu')
    ax5.set_xlabel('Film thickness (nm)')
    ax5.set_ylabel('Wavelength (nm)')
    ax5.set_title('薄膜干涉')
    plt.colorbar(im, ax=ax5, label='Intensity')

    # 6. 光栅光谱
    ax6 = axes[1, 2]
    # 模拟白光通过光栅后的光谱
    d_grating = 2e-6
    wavelengths = np.array([400, 500, 600, 700]) * 1e-9
    colors = ['violet', 'green', 'orange', 'red']
    for wl, color in zip(wavelengths, colors):
        theta_diff = np.linspace(-0.3, 0.3, 1000)
        I = grating_intensity(theta_diff, 100, d_grating, wl)
        I = I / I.max()
        ax6.plot(np.degrees(theta_diff), I, color=color, linewidth=1,
                 label=f'{wl*1e9:.0f} nm', alpha=0.7)
    ax6.set_xlabel('θ (degrees)')
    ax6.set_ylabel('I (normalized)')
    ax6.set_title('光栅光谱分离')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('diffraction.png', dpi=150)
    print("图像已保存为 diffraction.png")
    plt.show()


def verify():
    """
    验证所有练习的正确性
    Verify all exercises
    """
    all_passed = True
    wavelength = 500e-9  # 500 nm（绿光）

    # 检查 5.1 - 单缝衍射 Check single-slit diffraction
    a = 20e-6  # 缝宽 20 μm
    minima = single_slit_minima(a, wavelength)
    expected_theta1 = np.arcsin(wavelength / a)
    if len(minima) == 0 or not np.isclose(minima[0][1], expected_theta1, rtol=0.01):
        print("错误 5.1: 单缝衍射暗纹位置计算错误，请检查公式 a sin(θ) = mλ")
        all_passed = False
    else:
        print(f"通过 5.1: 单缝衍射正确 (第一暗纹位置: θ = {np.degrees(minima[0][1]):.3f}°)")

    # 检查 5.2 - 双缝干涉 Check double-slit interference
    d = 50e-6  # 缝间距 50 μm
    maxima = double_slit_maxima(d, wavelength)
    if len(maxima) < 3:
        print("错误 5.2: 双缝干涉明纹数量不足，请检查光栅方程")
        all_passed = False
    else:
        print(f"通过 5.2: 双缝干涉正确（检测到 {len(maxima)} 个可见明纹）")

    # 检查 5.3 - 光栅分辨本领 Check grating resolving power
    N, d = 1000, 2e-6  # 1000条刻线，光栅常数 2 μm
    R = grating_resolving_power(N, 1)
    if not np.isclose(R, N, rtol=0.01):
        print("错误 5.3: 光栅分辨本领计算错误，一级光谱应为 R = mN = N")
        all_passed = False
    else:
        print(f"通过 5.3: 光栅分辨本领正确 (R = mN = {R})")

    # 检查 5.4 - 瑞利判据 Check Rayleigh criterion
    D = 5e-3  # 孔径 5 mm
    theta_min = rayleigh_resolution(D, wavelength)
    expected = 1.22 * wavelength / D
    if not np.isclose(theta_min, expected, rtol=0.01):
        print("错误 5.4: 瑞利判据计算错误，请检查公式 θ_min = 1.22λ/D")
        all_passed = False
    else:
        print(f"通过 5.4: 瑞利判据正确 (最小分辨角 θ_min = {theta_min*1e6:.2f} μrad)")

    # 检查 5.5 - 菲涅尔数 Check Fresnel number
    a, L = 1e-3, 1.0  # 孔径 1 mm，距离 1 m
    F = fresnel_number(a, wavelength, L)
    expected_F = a**2 / (wavelength * L)
    if not np.isclose(F, expected_F, rtol=0.01):
        print("错误 5.5: 菲涅尔数计算错误，请检查公式 F = a²/(λL)")
        all_passed = False
    else:
        regime = "夫琅禾费衍射" if F < 1 else ("菲涅尔衍射" if F < 100 else "几何光学")
        print(f"通过 5.5: 菲涅尔数正确 (F = {F:.2f}，属于{regime}区)")

    # 检查 5.7 - 迈克尔逊干涉仪 Check Michelson interferometer
    delta_d = 0.5e-3  # 反射镜移动 0.5 mm
    N_fringes = michelson_fringe_shift(delta_d, wavelength)
    expected_N = 2 * delta_d / wavelength
    if not np.isclose(N_fringes, expected_N, rtol=0.01):
        print("错误 5.7: 条纹移动数计算错误，请检查公式 N = 2Δd/λ")
        all_passed = False
    else:
        print(f"通过 5.7: 迈克尔逊干涉仪正确 (移动 {N_fringes:.0f} 条条纹)")

    if all_passed:
        print("\n全部测试通过！正在生成可视化图像...")
        print("All tests passed! Generating visualization...")
        try:
            plot_diffraction()
        except Exception as e:
            print(f"可视化失败 Visualization failed: {e}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("衍射 Diffraction")
    print("=" * 50)
    verify()
