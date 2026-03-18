"""
电磁波 Electromagnetic Waves
难度 Difficulty: ★★★

学习目标 Learning Objectives:
- 理解电磁波的基本性质和传播特性
  Understand basic properties and propagation of EM waves
- 掌握波印廷矢量和能量流的计算
  Master Poynting vector and energy flow calculations
- 分析光的偏振态和偏振器的作用
  Analyze polarization states and polarizer effects
- 理解反射、折射和菲涅尔方程
  Understand reflection, refraction and Fresnel equations

物理背景 Physical Background:
电磁波是麦克斯韦方程组的波动解，由相互垂直的电场E和磁场B组成。

基本特性：
- 电磁波速度（真空中）：c = 1/√(ε₀μ₀) ≈ 3×10⁸ m/s
- 电场与磁场的关系：E = cB（振幅关系）
- E、B、k（传播方向）相互垂直，满足右手定则
- 电磁波是横波（振动方向垂直于传播方向）

能量与动量：
- 能量密度：u = ε₀E² = B²/μ₀（电场和磁场各贡献一半）
- 波印廷矢量：S = E × H = E × B/μ₀（能量流密度，单位 W/m²）
- 辐射压：p = S/c（光子动量产生的压力）
- 平均强度：I = <S> = (1/2)cε₀E₀²

偏振：
- 线偏振：E场振动方向固定
- 圆偏振：E场端点轨迹为圆
- 椭圆偏振：一般情况，E场端点轨迹为椭圆

HINT: 电磁波速度 c = 1/√(ε₀μ₀)
HINT: 波印廷矢量 S = E × H = (1/μ₀) E × B
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import c, epsilon_0, mu_0

# I AM NOT DONE

# =============================================================================
# 练习 4.1: 电磁波基本参数
# Exercise 4.1: Basic EM Wave Parameters
# =============================================================================
"""
电磁波谱覆盖广泛的频率范围，不同频段有不同的名称和应用：
- 无线电波：f < 3×10⁹ Hz (λ > 0.1 m)，通信
- 微波：3×10⁹ ~ 3×10¹¹ Hz，雷达、微波炉
- 红外：3×10¹¹ ~ 4×10¹⁴ Hz，热辐射
- 可见光：4×10¹⁴ ~ 7.5×10¹⁴ Hz (λ = 400~700 nm)
- 紫外：7.5×10¹⁴ ~ 3×10¹⁶ Hz，杀菌
- X射线：3×10¹⁶ ~ 3×10¹⁹ Hz，医学成像
- γ射线：f > 3×10¹⁹ Hz，核物理

所有电磁波在真空中以光速传播：c ≈ 299,792,458 m/s
"""
def wavelength_from_frequency(f):
    """
    从频率计算波长
    Calculate wavelength from frequency

    公式 Formula: λ = c/f
    参数 f: 频率 Frequency (Hz)
    返回: 波长 Wavelength (m)
    """
    return c / f

def frequency_from_wavelength(wavelength):
    """
    从波长计算频率
    Calculate frequency from wavelength

    公式 Formula: f = c/λ
    参数 wavelength: 波长 Wavelength (m)
    返回: 频率 Frequency (Hz)
    """
    return c / wavelength

def wave_number(wavelength):
    """
    计算波数（空间角频率）
    Calculate wave number

    公式 Formula: k = 2π/λ
    参数 wavelength: 波长 Wavelength (m)
    返回: 波数 Wave number (rad/m)
    """
    return 2 * np.pi / wavelength

def angular_frequency(f):
    """
    计算角频率
    Calculate angular frequency

    公式 Formula: ω = 2πf
    参数 f: 频率 Frequency (Hz)
    返回: 角频率 Angular frequency (rad/s)
    """
    return 2 * np.pi * f


# =============================================================================
# 练习 4.2: 电磁波场
# Exercise 4.2: EM Wave Fields
# =============================================================================
"""
平面电磁波是最简单的电磁波形式，等相面是垂直于传播方向的平面。

沿 +x 方向传播的 y 偏振平面波：
E = E₀ sin(kx - ωt) ŷ
B = (E₀/c) sin(kx - ωt) ẑ

重要关系：
- E 和 B 同相位（同时达到最大，同时为零）
- |E|/|B| = c（电场和磁场振幅的比值等于光速）
- E × B 指向传播方向（波印廷矢量方向）
"""
def plane_wave_E(E0, k, omega, x, t, polarization='y'):
    """
    计算平面电磁波的电场矢量
    Calculate electric field vector of plane EM wave

    参数 Parameters:
    - E0: 电场振幅 Electric field amplitude (V/m)
    - k: 波数 Wave number (rad/m)
    - omega: 角频率 Angular frequency (rad/s)
    - x: 位置 Position (m)
    - t: 时间 Time (s)
    - polarization: 偏振方向 Polarization direction ('y' 或 'z')

    返回 Returns:
    - E: 电场矢量 [Ex, Ey, Ez] (V/m)

    假设波沿 +x 方向传播
    """
    phase = k * x - omega * t
    if polarization == 'y':
        return np.array([0, E0 * np.sin(phase), 0])  # y偏振
    elif polarization == 'z':
        return np.array([0, 0, E0 * np.sin(phase)])  # z偏振

def plane_wave_B(E0, k, omega, x, t, polarization='y'):
    """
    计算平面电磁波的磁场矢量
    Calculate magnetic field vector of plane EM wave

    参数 Parameters:
    - E0: 电场振幅 Electric field amplitude (V/m)
    - k, omega, x, t: 同 plane_wave_E
    - polarization: 电场偏振方向

    返回 Returns:
    - B: 磁场矢量 [Bx, By, Bz] (T)

    磁场方向由 k × E 确定（右手定则）
    B₀ = E₀/c
    """
    B0 = E0 / c  # 磁场振幅
    phase = k * x - omega * t
    if polarization == 'y':
        # E 沿 y，k 沿 x，则 B 沿 z
        return np.array([0, 0, B0 * np.sin(phase)])
    elif polarization == 'z':
        # E 沿 z，k 沿 x，则 B 沿 -y
        return np.array([0, -B0 * np.sin(phase), 0])


# =============================================================================
# 练习 4.3: 波印廷矢量和能量
# Exercise 4.3: Poynting Vector and Energy
# =============================================================================
"""
电磁波的能量和动量传输：

能量密度：
u = u_E + u_B = (1/2)ε₀E² + B²/(2μ₀)
对于平面波，电场和磁场的能量密度相等：u_E = u_B

波印廷矢量（能量流密度）：
S = (1/μ₀) E × B = E × H
- 方向：能量传播方向（垂直于 E 和 B）
- 大小：单位面积单位时间通过的能量 (W/m²)

平均强度（辐照度）：
I = <S> = (1/2)cε₀E₀² = (1/2) E₀B₀/μ₀
对于正弦波，平均值是峰值的一半

辐射压（光压）：
p = S/c = u（完全吸收）
p = 2S/c = 2u（完全反射）
"""
def poynting_vector(E, B):
    """
    计算波印廷矢量（能量流密度）
    Calculate Poynting vector (energy flux density)

    参数 Parameters:
    - E: 电场矢量 Electric field vector (V/m)
    - B: 磁场矢量 Magnetic field vector (T)

    返回 Returns:
    - S: 波印廷矢量 Poynting vector (W/m²)

    公式 Formula: S = (1/μ₀) E × B
    """
    # TODO: 计算波印廷矢量，使用叉乘
    # TODO: Calculate Poynting vector using cross product
    S = np.cross(E, B) / mu_0
    return S

def energy_density_E(E):
    """
    计算电场能量密度
    Calculate electric field energy density

    公式 Formula: u_E = (1/2)ε₀E²
    返回: 能量密度 (J/m³)
    """
    E_mag = np.linalg.norm(E)  # 电场大小
    return 0.5 * epsilon_0 * E_mag**2

def energy_density_B(B):
    """
    计算磁场能量密度
    Calculate magnetic field energy density

    公式 Formula: u_B = B²/(2μ₀)
    返回: 能量密度 (J/m³)
    """
    B_mag = np.linalg.norm(B)  # 磁场大小
    return 0.5 * B_mag**2 / mu_0

def average_intensity(E0):
    """
    计算电磁波的平均强度（辐照度）
    Calculate average intensity (irradiance) of EM wave

    参数 Parameters:
    - E0: 电场振幅 Electric field amplitude (V/m)

    返回 Returns:
    - I: 平均强度 Average intensity (W/m²)

    公式 Formula: I = (1/2)cε₀E₀²
    说明：正弦波的时间平均值
    """
    return 0.5 * c * epsilon_0 * E0**2


# =============================================================================
# 练习 4.4: 折射定律
# Exercise 4.4: Refraction Law
# =============================================================================
"""
斯涅尔定律（折射定律）：
当光从一种介质进入另一种介质时，传播方向发生改变。

n₁ sin(θ₁) = n₂ sin(θ₂)

其中：
- n₁, n₂: 两种介质的折射率
- θ₁: 入射角（与法线的夹角）
- θ₂: 折射角

物理本质：光在不同介质中速度不同，v = c/n

全内反射：
当光从光密介质（高折射率）射向光疏介质（低折射率）时，
如果入射角大于临界角 θ_c，将发生全内反射。
sin(θ_c) = n₂/n₁

应用：光纤通信、棱镜、透镜设计
"""
def snells_law(n1, n2, theta1):
    """
    斯涅尔定律 - 计算折射角
    Snell's law - Calculate refraction angle

    参数 Parameters:
    - n1: 入射介质折射率 Refractive index of incident medium
    - n2: 折射介质折射率 Refractive index of refracted medium
    - theta1: 入射角 Incident angle (rad)

    返回 Returns:
    - theta2: 折射角 Refraction angle (rad)
    - None: 如果发生全反射 If total internal reflection occurs

    公式 Formula: n₁sin(θ₁) = n₂sin(θ₂)
    """
    sin_theta2 = n1 * np.sin(theta1) / n2
    if abs(sin_theta2) > 1:
        return None  # 全反射，无折射光
    return np.arcsin(sin_theta2)

def critical_angle(n1, n2):
    """
    计算全内反射的临界角
    Calculate critical angle for total internal reflection

    参数 Parameters:
    - n1: 入射介质折射率（光密介质）
    - n2: 出射介质折射率（光疏介质）

    返回 Returns:
    - theta_c: 临界角 Critical angle (rad)
    - None: 如果 n2 >= n1（不存在全反射）

    公式 Formula: sin(θ_c) = n₂/n₁
    条件：n₁ > n₂（从光密到光疏）
    """
    if n2 >= n1:
        return None  # 光从光疏射向光密，不存在临界角
    return np.arcsin(n2 / n1)

def refractive_index(c_medium):
    """
    从介质中光速计算折射率
    Calculate refractive index from light speed in medium

    公式 Formula: n = c/v
    参数 c_medium: 介质中的光速 Light speed in medium (m/s)
    返回: 折射率 Refractive index (无量纲)
    """
    return c / c_medium


# =============================================================================
# 练习 4.5: 菲涅尔方程
# Exercise 4.5: Fresnel Equations
# =============================================================================
"""
菲涅尔方程描述光在界面上的反射和透射特性。

偏振定义：
- s偏振（TE，横电）：电场垂直于入射面（包含入射、反射、透射光线的平面）
- p偏振（TM，横磁）：电场平行于入射面

反射系数（振幅比）：
r_s = (n₁cos(θ_i) - n₂cos(θ_t)) / (n₁cos(θ_i) + n₂cos(θ_t))
r_p = (n₂cos(θ_i) - n₁cos(θ_t)) / (n₂cos(θ_i) + n₁cos(θ_t))

反射率（功率比）：
R_s = |r_s|²
R_p = |r_p|²

布鲁斯特角：
当入射角等于布鲁斯特角时，p偏振光完全透射（r_p = 0）
tan(θ_B) = n₂/n₁
此时反射光完全是 s 偏振

应用：偏振太阳镜、防反射膜、激光窗口
"""
def fresnel_rs(n1, n2, theta_i):
    """
    计算 s 偏振（垂直偏振）的反射系数
    Calculate s-polarized (perpendicular) reflection coefficient

    参数 Parameters:
    - n1, n2: 入射和透射介质的折射率
    - theta_i: 入射角 Incident angle (rad)

    返回 Returns:
    - r_s: s偏振反射系数（振幅比，可为负）

    公式 Formula:
    r_s = (n₁cos(θ_i) - n₂cos(θ_t)) / (n₁cos(θ_i) + n₂cos(θ_t))
    """
    theta_t = snells_law(n1, n2, theta_i)
    if theta_t is None:
        return 1.0  # 全反射时反射率为1
    # TODO: 计算 s 偏振反射系数
    # TODO: Calculate s-polarized reflection coefficient
    r_s = (n1*np.cos(theta_i) - n2*np.cos(theta_t)) / (n1*np.cos(theta_i) + n2*np.cos(theta_t))
    return r_s

def fresnel_rp(n1, n2, theta_i):
    """
    计算 p 偏振（平行偏振）的反射系数
    Calculate p-polarized (parallel) reflection coefficient

    参数 Parameters:
    - n1, n2: 入射和透射介质的折射率
    - theta_i: 入射角 Incident angle (rad)

    返回 Returns:
    - r_p: p偏振反射系数（振幅比，可为负）

    公式 Formula:
    r_p = (n₂cos(θ_i) - n₁cos(θ_t)) / (n₂cos(θ_i) + n₁cos(θ_t))

    注意：在布鲁斯特角处 r_p = 0
    """
    theta_t = snells_law(n1, n2, theta_i)
    if theta_t is None:
        return 1.0  # 全反射
    r_p = (n2*np.cos(theta_i) - n1*np.cos(theta_t)) / (n2*np.cos(theta_i) + n1*np.cos(theta_t))
    return r_p

def brewster_angle(n1, n2):
    """
    计算布鲁斯特角（偏振角）
    Calculate Brewster's angle (polarization angle)

    公式 Formula: tan(θ_B) = n₂/n₁
    物理意义：p偏振光完全透射，无反射

    参数 Parameters:
    - n1: 入射介质折射率
    - n2: 透射介质折射率

    返回 Returns:
    - theta_B: 布鲁斯特角 Brewster's angle (rad)
    """
    return np.arctan(n2 / n1)


# =============================================================================
# 练习 4.6: 偏振
# Exercise 4.6: Polarization
# =============================================================================
"""
光的偏振状态描述电场矢量的振动方式：

1. 线偏振（线性偏振）：
   电场矢量始终在固定平面内振动
   E = E₀ cos(kx - ωt) ŷ

2. 圆偏振：
   电场矢量端点轨迹为圆，大小不变，方向旋转
   E = E₀[cos(kx-ωt)ŷ + sin(kx-ωt)ẑ]（右旋）
   E = E₀[cos(kx-ωt)ŷ - sin(kx-ωt)ẑ]（左旋）

3. 椭圆偏振：
   电场矢量端点轨迹为椭圆（最一般情况）

马吕斯定律：
线偏振光通过偏振片后的强度
I = I₀ cos²(θ)
其中 θ 是入射光偏振方向与偏振片透光轴的夹角

应用：
- 偏光太阳镜
- LCD 显示器
- 3D 电影
- 光学应力分析
"""
def malus_law(I0, theta):
    """
    马吕斯定律 - 计算通过偏振片后的光强
    Malus' law - Calculate intensity after polarizer

    参数 Parameters:
    - I0: 入射线偏振光强度 Incident polarized light intensity (W/m²)
    - theta: 偏振方向与透光轴的夹角 Angle between polarization and axis (rad)

    返回 Returns:
    - I: 透射光强度 Transmitted intensity (W/m²)

    公式 Formula: I = I₀ cos²(θ)
    特例：θ=0 时全透，θ=90° 时全阻
    """
    return I0 * np.cos(theta)**2

def circular_polarization(E0, k, omega, x, t, handedness='right'):
    """
    计算圆偏振光的电场矢量
    Calculate electric field of circularly polarized light

    参数 Parameters:
    - E0: 电场振幅 Electric field amplitude (V/m)
    - k: 波数 Wave number (rad/m)
    - omega: 角频率 Angular frequency (rad/s)
    - x: 位置 Position (m)
    - t: 时间 Time (s)
    - handedness: 旋向 'right'（右旋）或 'left'（左旋）

    返回 Returns:
    - E: 电场矢量 [Ex, Ey, Ez] (V/m)

    右旋定义：沿传播方向看，电场矢量顺时针旋转
    公式: E = E₀[cos(kx-ωt)ŷ ± sin(kx-ωt)ẑ]
    """
    phase = k * x - omega * t
    sign = 1 if handedness == 'right' else -1
    Ey = E0 * np.cos(phase)
    Ez = sign * E0 * np.sin(phase)
    return np.array([0, Ey, Ez])


# =============================================================================
# 可视化
# =============================================================================
def plot_em_waves():
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. 电磁波电场和磁场
    ax1 = axes[0, 0]
    wavelength = 500e-9  # 500 nm
    k = wave_number(wavelength)
    omega = angular_frequency(c / wavelength)
    E0 = 1.0

    x = np.linspace(0, 3*wavelength, 500)
    Ey = E0 * np.sin(k * x)
    Bz = (E0/c) * np.sin(k * x)

    ax1.plot(x*1e9, Ey, 'b-', label='E_y', linewidth=2)
    ax1.plot(x*1e9, Bz*c, 'r-', label='B_z × c', linewidth=2)
    ax1.set_xlabel('x (nm)')
    ax1.set_ylabel('Field')
    ax1.set_title('电磁波 E and B Fields')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 菲涅尔反射系数
    ax2 = axes[0, 1]
    n1, n2 = 1.0, 1.5  # 空气到玻璃
    theta = np.linspace(0, np.pi/2 - 0.01, 100)

    Rs = [fresnel_rs(n1, n2, t)**2 for t in theta]
    Rp = [fresnel_rp(n1, n2, t)**2 for t in theta]

    theta_B = brewster_angle(n1, n2)

    ax2.plot(np.degrees(theta), Rs, 'b-', label='R_s', linewidth=2)
    ax2.plot(np.degrees(theta), Rp, 'r-', label='R_p', linewidth=2)
    ax2.axvline(x=np.degrees(theta_B), color='g', linestyle='--',
                label=f'Brewster angle = {np.degrees(theta_B):.1f}°')
    ax2.set_xlabel('Incident angle (°)')
    ax2.set_ylabel('Reflectance')
    ax2.set_title('菲涅尔反射 Fresnel Reflection')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 马吕斯定律
    ax3 = axes[1, 0]
    theta_pol = np.linspace(0, np.pi, 100)
    I = malus_law(1.0, theta_pol)
    ax3.plot(np.degrees(theta_pol), I, 'b-', linewidth=2)
    ax3.set_xlabel('Polarizer angle (°)')
    ax3.set_ylabel('I/I₀')
    ax3.set_title("马吕斯定律 Malus' Law")
    ax3.grid(True, alpha=0.3)

    # 4. 圆偏振
    ax4 = axes[1, 1]
    t_circ = np.linspace(0, 2*np.pi/omega, 100)
    Ey_circ = E0 * np.cos(-omega * t_circ)
    Ez_circ = E0 * np.sin(-omega * t_circ)
    ax4.plot(Ey_circ, Ez_circ, 'b-', linewidth=2)
    ax4.set_xlabel('E_y')
    ax4.set_ylabel('E_z')
    ax4.set_title('右旋圆偏振 Right Circular Polarization')
    ax4.set_aspect('equal')
    ax4.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('electromagnetic_waves.png', dpi=150)
    print("图像已保存为 electromagnetic_waves.png")
    plt.show()


def verify():
    """
    验证所有练习的正确性
    Verify all exercises
    """
    all_passed = True

    # 检查 4.1 - 电磁波参数 Check EM wave parameters
    f = 6e14  # 绿光频率 Green light frequency (Hz)
    wavelength = wavelength_from_frequency(f)
    if not np.isclose(wavelength, 500e-9, rtol=0.01):
        print("错误 4.1: 波长计算错误，请检查公式 λ = c/f")
        all_passed = False
    else:
        print(f"通过 4.1: 波长计算正确 (f=6×10¹⁴Hz → λ={wavelength*1e9:.0f}nm)")

    # 检查 4.3 - 波印廷矢量和强度 Check Poynting vector and intensity
    E0 = 100  # V/m
    I = average_intensity(E0)
    expected_I = 0.5 * c * epsilon_0 * E0**2
    if not np.isclose(I, expected_I, rtol=0.01):
        print("错误 4.3: 平均强度计算错误，请检查公式 I = (1/2)cε₀E₀²")
        all_passed = False
    else:
        print(f"通过 4.3: 波印廷矢量/强度正确 (E₀=100V/m → I = {I:.2f} W/m²)")

    # 检查 4.4 - 斯涅尔定律 Check Snell's law
    theta2 = snells_law(1.0, 1.5, np.radians(30))
    expected = np.arcsin(np.sin(np.radians(30)) / 1.5)
    if not np.isclose(theta2, expected, rtol=0.01):
        print("错误 4.4: 斯涅尔定律计算错误，请检查公式 n₁sin(θ₁) = n₂sin(θ₂)")
        all_passed = False
    else:
        print(f"通过 4.4: 折射定律正确 (空气→玻璃: 30° → {np.degrees(theta2):.1f}°)")

    # 检查 4.5 - 菲涅尔方程 Check Fresnel equations
    theta_B = brewster_angle(1.0, 1.5)
    if not np.isclose(theta_B, np.arctan(1.5), rtol=0.01):
        print("错误 4.5: 布鲁斯特角计算错误，请检查公式 tan(θ_B) = n₂/n₁")
        all_passed = False
    else:
        print(f"通过 4.5: 菲涅尔方程正确 (布鲁斯特角 θ_B = {np.degrees(theta_B):.1f}°)")

    # 检查 4.6 - 偏振 Check polarization
    I_malus = malus_law(1.0, np.pi/4)
    if not np.isclose(I_malus, 0.5, rtol=0.01):
        print("错误 4.6: 马吕斯定律计算错误，请检查公式 I = I₀cos²(θ)")
        all_passed = False
    else:
        print("通过 4.6: 偏振（马吕斯定律）正确 (θ=45° → I/I₀=0.5)")

    if all_passed:
        print("\n全部测试通过！正在生成可视化图像...")
        print("All tests passed! Generating visualization...")
        try:
            plot_em_waves()
        except Exception as e:
            print(f"可视化失败 Visualization failed: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("电磁波 Electromagnetic Waves")
    print("=" * 50)
    verify()
