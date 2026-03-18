"""
电磁光学 Electromagnetic Optics
难度 Difficulty: ★★★★

学习目标 Learning Objectives:
- 理解光的电磁本质：光是电磁波 (Understand electromagnetic nature of light)
- 掌握菲涅尔方程和反射/折射现象 (Master Fresnel equations and reflection/refraction)
- 理解偏振态及其数学描述（琼斯矢量）(Understand polarization and Jones vectors)
- 分析双折射晶体中的光传播 (Analyze light propagation in birefringent crystals)
- 掌握薄膜干涉和增透膜设计 (Master thin film interference and AR coating design)
- 理解光学各向异性效应 (Understand optical anisotropy effects)

物理背景 Physical Background:
1. 光的电磁本质 Electromagnetic nature of light:
   - 麦克斯韦方程组预言光是电磁波（1865年）
   - 光速 c = 1/√(ε₀μ₀) ≈ 3×10⁸ m/s
   - 能流密度由坡印廷矢量描述：S = E × H

2. 反射与折射 Reflection and refraction:
   - 斯涅尔定律：n₁sinθ₁ = n₂sinθ₂
   - 菲涅尔方程描述振幅反射/透射系数
   - 布儒斯特角：p偏振光完全透射
   - 全反射：从光密介质到光疏介质

3. 偏振 Polarization:
   - 线偏振、圆偏振、椭圆偏振
   - 马吕斯定律：I = I₀cos²θ
   - 琼斯矢量/矩阵：偏振态的数学描述

4. 双折射 Birefringence:
   - 各向异性晶体具有两个折射率 n_o 和 n_e
   - 寻常光和非寻常光沿不同方向传播
   - 波片：λ/4 片、λ/2 片

5. 薄膜光学 Thin film optics:
   - 干涉增强或减弱反射
   - 增透膜：n = √(n₁n₂)，厚度 d = λ/(4n)

核心公式 Key Formulas:
- 时间平均强度 Time-averaged intensity: I = (1/2)ε₀cn|E₀|²
- 菲涅尔反射系数 Fresnel (s-pol): r_s = (n₁cosθ₁ - n₂cosθ₂)/(n₁cosθ₁ + n₂cosθ₂)
- 布儒斯特角 Brewster angle: tanθ_B = n₂/n₁
- 马吕斯定律 Malus' law: I = I₀cos²θ
- 波片相位延迟 Waveplate retardation: Γ = 2πdΔn/λ
- 增透膜条件 AR coating: n = √(n₁n₂), d = λ/(4n)
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import c, epsilon_0, mu_0

# I AM NOT DONE

# =============================================================================
# 练习 13.1: 光的电磁场描述
# Exercise 13.1: Electromagnetic Description of Light
#
# 物理背景 Physical Background:
# 光是横向电磁波，电场和磁场相互垂直且都垂直于传播方向
# 麦克斯韦于1865年从电磁理论推导出电磁波的存在
#
# 平面波的复数表示 Complex representation:
# E = E₀ exp(i(k·r - ωt)) ê
# - k: 波矢（方向为传播方向，大小 |k| = 2π/λ = ω/c）
# - ω: 角频率 = 2πf
# - ê: 偏振方向单位矢量
#
# 能量传输 Energy transport:
# - 坡印廷矢量 S = E × H 表示能流密度
# - 时间平均强度 I = <S> = (1/2)ε₀cn|E₀|²
# - 辐射压强 P = I/c（吸收）或 P = 2I/c（全反射）
# =============================================================================
def plane_wave_electric_field(E0, k, omega, r, t, polarization='x'):
    """
    计算平面波电场 Calculate plane wave electric field

    公式 Formula: E = E₀ exp(i(k·r - ωt)) ê

    参数 Parameters:
        E0: float - 电场振幅 electric field amplitude [V/m]
        k: array - 波矢 wave vector [rad/m]
        omega: float - 角频率 angular frequency [rad/s]
        r: array - 位置矢量 position vector [m]
        t: float - 时间 time [s]
        polarization: str - 偏振方向 polarization direction ('x' or 'y')

    返回 Returns:
        array - 电场矢量 electric field vector [V/m]（复数形式）
    """
    phase = np.dot(k, r) - omega * t
    if polarization == 'x':
        return E0 * np.exp(1j * phase) * np.array([1, 0, 0])
    elif polarization == 'y':
        return E0 * np.exp(1j * phase) * np.array([0, 1, 0])
    return E0 * np.exp(1j * phase)

def poynting_vector(E, H):
    """
    计算坡印廷矢量 Calculate Poynting vector

    公式 Formula: S = E × H

    参数 Parameters:
        E: array - 电场矢量 electric field vector [V/m]
        H: array - 磁场矢量 magnetic field vector [A/m]

    返回 Returns:
        array - 坡印廷矢量（能流密度）Poynting vector [W/m²]

    物理意义 Physical meaning:
    - 方向：电磁能量传播方向
    - 大小：单位面积上单位时间内通过的能量
    """
    return np.cross(E, H)

def time_averaged_intensity(E0, n=1):
    """
    计算时间平均光强 Calculate time-averaged intensity

    公式 Formula: I = (1/2)ε₀cn|E₀|²

    参数 Parameters:
        E0: float - 电场振幅 electric field amplitude [V/m]
        n: float - 介质折射率 refractive index（默认为1，真空）

    返回 Returns:
        float - 光强 intensity [W/m²]

    物理意义 Physical meaning:
    - 光强与电场振幅的平方成正比
    - 在介质中，光强还与折射率 n 成正比
    """
    return 0.5 * epsilon_0 * c * n * np.abs(E0)**2

def radiation_pressure(I, reflectivity=0):
    """
    计算辐射压强 Calculate radiation pressure

    公式 Formula: P = (I/c)(1 + R)

    参数 Parameters:
        I: float - 光强 intensity [W/m²]
        reflectivity: float - 反射率 reflectivity（0-1）

    返回 Returns:
        float - 辐射压强 radiation pressure [Pa]

    物理意义 Physical meaning:
    - R = 0（完全吸收）：P = I/c（光子动量全部转移）
    - R = 1（完全反射）：P = 2I/c（光子动量反向，两倍冲量）
    - 太阳光对地球表面的辐射压约 4.6 μPa
    """
    return I / c * (1 + reflectivity)


# =============================================================================
# 练习 13.2: 菲涅尔方程
# Exercise 13.2: Fresnel Equations
#
# 物理背景 Physical Background:
# 菲涅尔方程描述光在两种介质界面处的反射和透射
# 由奥古斯丁·菲涅尔于1823年导出
#
# 偏振定义 Polarization definitions:
# - s偏振（垂直偏振）：电场垂直于入射面
# - p偏振（平行偏振）：电场平行于入射面
#
# 特殊角度 Special angles:
# - 布儒斯特角：p偏振光完全透射，反射光为纯s偏振
# - 临界角：全反射发生的最小入射角（仅当 n₁ > n₂）
#
# 应用 Applications:
# - 偏光太阳镜：利用布儒斯特角减少眩光
# - 光纤：利用全反射传导光信号
# - 棱镜：分光和偏振控制
# =============================================================================
def snell_law(n1, n2, theta1):
    """
    计算折射角（斯涅尔定律）Calculate refraction angle (Snell's law)

    公式 Formula: n₁sinθ₁ = n₂sinθ₂

    参数 Parameters:
        n1: float - 入射介质折射率 refractive index of incident medium
        n2: float - 折射介质折射率 refractive index of refracted medium
        theta1: float - 入射角 angle of incidence [rad]

    返回 Returns:
        float or None - 折射角 refraction angle [rad]
                        全反射时返回 None

    注意 Note:
    - 当 n₁sinθ₁ > n₂ 时发生全反射
    - 此时无折射光线，返回 None
    """
    sin_theta2 = n1 * np.sin(theta1) / n2
    if np.abs(sin_theta2) > 1:
        return None  # 全反射
    return np.arcsin(sin_theta2)

def fresnel_rs(n1, n2, theta1):
    """
    计算s偏振反射系数 Calculate s-polarized reflection coefficient

    公式 Formula: r_s = (n₁cosθ₁ - n₂cosθ₂)/(n₁cosθ₁ + n₂cosθ₂)

    参数 Parameters:
        n1: float - 入射介质折射率 refractive index of incident medium
        n2: float - 折射介质折射率 refractive index of refracted medium
        theta1: float - 入射角 angle of incidence [rad]

    返回 Returns:
        float - s偏振振幅反射系数 s-polarized amplitude reflection coefficient

    物理意义 Physical meaning:
    - 正值：反射波与入射波同相
    - 负值：反射波与入射波反相
    - |r_s|²：s偏振反射率
    """
    theta2 = snell_law(n1, n2, theta1)
    if theta2 is None:
        return 1  # 全反射
    numerator = n1 * np.cos(theta1) - n2 * np.cos(theta2)
    denominator = n1 * np.cos(theta1) + n2 * np.cos(theta2)
    return numerator / denominator

def fresnel_rp(n1, n2, theta1):
    """
    计算p偏振反射系数 Calculate p-polarized reflection coefficient

    公式 Formula: r_p = (n₂cosθ₁ - n₁cosθ₂)/(n₂cosθ₁ + n₁cosθ₂)

    参数 Parameters:
        n1: float - 入射介质折射率 refractive index of incident medium
        n2: float - 折射介质折射率 refractive index of refracted medium
        theta1: float - 入射角 angle of incidence [rad]

    返回 Returns:
        float - p偏振振幅反射系数 p-polarized amplitude reflection coefficient

    物理意义 Physical meaning:
    - 在布儒斯特角处，r_p = 0（完全透射）
    - |r_p|²：p偏振反射率
    """
    theta2 = snell_law(n1, n2, theta1)
    if theta2 is None:
        return 1
    numerator = n2 * np.cos(theta1) - n1 * np.cos(theta2)
    denominator = n2 * np.cos(theta1) + n1 * np.cos(theta2)
    return numerator / denominator

def brewster_angle(n1, n2):
    """
    计算布儒斯特角 Calculate Brewster angle

    公式 Formula: tanθ_B = n₂/n₁

    参数 Parameters:
        n1: float - 入射介质折射率 refractive index of incident medium
        n2: float - 折射介质折射率 refractive index of refracted medium

    返回 Returns:
        float - 布儒斯特角 Brewster angle [rad]

    物理意义 Physical meaning:
    - 在此角度，p偏振光完全透射，无反射
    - 反射光为纯s偏振
    - 空气-玻璃界面约 56°
    - 应用：偏振片、激光谐振腔窗口
    """
    return np.arctan(n2 / n1)

def critical_angle(n1, n2):
    """
    计算全反射临界角 Calculate critical angle for total internal reflection

    公式 Formula: sinθ_c = n₂/n₁ (当 n₁ > n₂)

    参数 Parameters:
        n1: float - 入射介质折射率 refractive index of incident medium
        n2: float - 折射介质折射率 refractive index of refracted medium

    返回 Returns:
        float - 临界角 critical angle [rad]
                若 n₁ ≤ n₂，返回 π/2（无全反射）

    物理意义 Physical meaning:
    - 只有从光密到光疏介质才有全反射
    - θ > θ_c 时发生全反射
    - 玻璃-空气界面约 42°
    - 应用：光纤、棱镜、钻石的闪耀
    """
    if n1 <= n2:
        return np.pi / 2  # 无全反射
    return np.arcsin(n2 / n1)


# =============================================================================
# 练习 13.3: 偏振
# Exercise 13.3: Polarization
#
# 物理背景 Physical Background:
# 偏振描述电磁波电场矢量振动的方向特性
# 光是横波，电场振动垂直于传播方向
#
# 偏振类型 Types of polarization:
# 1. 线偏振：电场沿固定方向振动
# 2. 圆偏振：电场矢量端点画圆（右旋/左旋）
# 3. 椭圆偏振：电场矢量端点画椭圆
#
# 琼斯矢量 Jones vector:
# 用复数二元矢量描述偏振态：J = [E_x, E_y]ᵀ
# - 线偏振（θ角）：[cosθ, sinθ]ᵀ
# - 右旋圆偏振：[1, -i]ᵀ/√2
# - 左旋圆偏振：[1, i]ᵀ/√2
#
# 琼斯矩阵 Jones matrix:
# 描述光学元件对偏振态的作用
# 输出偏振态 = 琼斯矩阵 × 输入偏振态
# =============================================================================
def malus_law(I0, theta):
    """
    计算通过偏振片后的光强（马吕斯定律）
    Calculate transmitted intensity through polarizer (Malus' law)

    公式 Formula: I = I₀cos²θ

    参数 Parameters:
        I0: float - 入射线偏振光强度 incident linearly polarized intensity [W/m²]
        theta: float - 偏振片透光轴与入射偏振方向的夹角 angle [rad]

    返回 Returns:
        float - 透射光强度 transmitted intensity [W/m²]

    物理意义 Physical meaning:
    - θ = 0°: I = I₀（透光轴平行，完全透射）
    - θ = 90°: I = 0（透光轴垂直，完全阻挡）
    - θ = 45°: I = I₀/2
    """
    return I0 * np.cos(theta)**2

def jones_vector_linear(theta):
    """
    生成线偏振光的琼斯矢量 Generate Jones vector for linearly polarized light

    参数 Parameters:
        theta: float - 偏振方向与x轴的夹角 polarization angle [rad]

    返回 Returns:
        array - 归一化琼斯矢量 normalized Jones vector [cosθ, sinθ]ᵀ

    示例 Examples:
    - θ = 0: 水平偏振 [1, 0]ᵀ
    - θ = π/2: 垂直偏振 [0, 1]ᵀ
    - θ = π/4: 45°偏振 [1, 1]ᵀ/√2
    """
    return np.array([np.cos(theta), np.sin(theta)])

def jones_vector_circular(handedness='right'):
    """
    生成圆偏振光的琼斯矢量 Generate Jones vector for circularly polarized light

    参数 Parameters:
        handedness: str - 旋转方向 'right'（右旋）或 'left'（左旋）

    返回 Returns:
        array - 归一化琼斯矢量 normalized Jones vector（复数）

    旋向约定 Handedness convention:
    - 右旋（RCP）：电场矢量顺时针旋转（向光源看）
    - 左旋（LCP）：电场矢量逆时针旋转
    """
    if handedness == 'right':
        return np.array([1, -1j]) / np.sqrt(2)
    return np.array([1, 1j]) / np.sqrt(2)

def jones_matrix_polarizer(theta=0):
    """
    生成线偏振片的琼斯矩阵 Generate Jones matrix for linear polarizer

    参数 Parameters:
        theta: float - 透光轴方向（与x轴夹角）transmission axis angle [rad]

    返回 Returns:
        array - 2×2 琼斯矩阵 Jones matrix

    矩阵形式 Matrix form:
    P(θ) = [cos²θ    cosθsinθ]
           [cosθsinθ   sin²θ ]
    """
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c**2, c*s], [c*s, s**2]])

def jones_matrix_waveplate(phase_delay, fast_axis=0):
    """
    生成波片的琼斯矩阵 Generate Jones matrix for waveplate

    参数 Parameters:
        phase_delay: float - 快慢轴之间的相位延迟 phase retardation [rad]
                     π/2: 四分之一波片（λ/4）
                     π: 半波片（λ/2）
        fast_axis: float - 快轴方向（与x轴夹角）fast axis angle [rad]

    返回 Returns:
        array - 2×2 琼斯矩阵 Jones matrix（复数）

    物理意义 Physical meaning:
    - λ/4 波片：线偏振 ↔ 圆偏振转换
    - λ/2 波片：偏振方向旋转2θ
    """
    c, s = np.cos(fast_axis), np.sin(fast_axis)
    exp_phi = np.exp(1j * phase_delay)
    return np.array([[c**2 + s**2*exp_phi, c*s*(1-exp_phi)],
                     [c*s*(1-exp_phi), s**2 + c**2*exp_phi]])


# =============================================================================
# 练习 13.4: 双折射
# Exercise 13.4: Birefringence
#
# 物理背景 Physical Background:
# 双折射是各向异性晶体中光传播的特殊现象
# 晶体对不同偏振方向的光具有不同的折射率
#
# 光轴与两种光线 Optical axis and two rays:
# - 寻常光（o光）：遵循斯涅尔定律，折射率 n_o 与方向无关
# - 非寻常光（e光）：折射率 n_e 随传播方向变化
#
# 晶体分类 Crystal classification:
# - 正单轴晶体：n_e > n_o（如石英、冰）
# - 负单轴晶体：n_e < n_o（如方解石）
#
# 波片 Waveplates:
# - 利用 o 光和 e 光的光程差产生相位延迟
# - λ/4 波片：相位差 π/2，线偏振 ↔ 圆偏振
# - λ/2 波片：相位差 π，偏振方向旋转
#
# 典型晶体 Typical crystals:
# - 石英：n_o = 1.544, n_e = 1.553, Δn = 0.009
# - 方解石：n_o = 1.658, n_e = 1.486, Δn = -0.172
# =============================================================================
def birefringence(n_e, n_o):
    """
    计算双折射率 Calculate birefringence

    公式 Formula: Δn = n_e - n_o

    参数 Parameters:
        n_e: float - 非寻常光折射率 extraordinary refractive index
        n_o: float - 寻常光折射率 ordinary refractive index

    返回 Returns:
        float - 双折射率 birefringence

    分类 Classification:
    - Δn > 0: 正单轴晶体（石英、冰）
    - Δn < 0: 负单轴晶体（方解石）
    """
    return n_e - n_o

def extraordinary_index(n_e, n_o, theta):
    """
    计算非寻常光折射率（与光轴夹角θ）
    Calculate extraordinary index vs optical axis angle

    公式 Formula: 1/n_e'² = cos²θ/n_o² + sin²θ/n_e²

    参数 Parameters:
        n_e: float - 主轴方向非寻常光折射率 principal extraordinary index
        n_o: float - 寻常光折射率 ordinary index
        theta: float - 光传播方向与光轴的夹角 angle to optical axis [rad]

    返回 Returns:
        float - 有效非寻常光折射率 effective extraordinary index

    物理意义 Physical meaning:
    - θ = 0（沿光轴）：n_e' = n_o（无双折射）
    - θ = 90°（垂直光轴）：n_e' = n_e
    """
    return 1 / np.sqrt(np.cos(theta)**2/n_o**2 + np.sin(theta)**2/n_e**2)

def waveplate_retardation(d, delta_n, wavelength):
    """
    计算波片相位延迟 Calculate waveplate phase retardation

    公式 Formula: Γ = 2πd×Δn/λ

    参数 Parameters:
        d: float - 波片厚度 waveplate thickness [m]
        delta_n: float - 双折射率 birefringence
        wavelength: float - 光波长 wavelength [m]

    返回 Returns:
        float - 相位延迟 phase retardation [rad]

    典型值 Typical values:
    - Γ = π/2: 四分之一波片
    - Γ = π: 半波片
    """
    return 2 * np.pi * d * delta_n / wavelength

def quarter_wave_plate_thickness(delta_n, wavelength):
    """
    计算四分之一波片厚度 Calculate quarter-wave plate thickness

    公式 Formula: d = λ/(4Δn)

    参数 Parameters:
        delta_n: float - 双折射率 birefringence
        wavelength: float - 设计波长 design wavelength [m]

    返回 Returns:
        float - 波片厚度 waveplate thickness [m]

    示例 Example:
    - 石英 @ 550nm：d ≈ 15 μm（0阶）
    - 实际使用多阶波片以获得合理厚度
    """
    return wavelength / (4 * delta_n)


# =============================================================================
# 练习 13.5: 薄膜干涉
# Exercise 13.5: Thin Film Interference
#
# 物理背景 Physical Background:
# 薄膜干涉是光在薄膜两表面反射产生的干涉效应
# 是增透膜、高反射镜、滤光片等光学元件的基础
#
# 干涉条件 Interference conditions:
# - 光程差：Δ = 2nd cosθ（包括折射角效应）
# - 相位差：δ = 2πnd/λ（正入射时）
# - 还需考虑界面反射时的半波损失
#
# 增透膜 Anti-reflection (AR) coating:
# - 目标：使反射为零
# - 条件1：膜厚 d = λ/(4n)（四分之一波长）
# - 条件2：折射率 n = √(n₁n₂)（阻抗匹配）
# - 常用材料：MgF₂ (n≈1.38), SiO₂ (n≈1.46)
#
# 多层膜 Multilayer films:
# - 交替堆叠高低折射率材料
# - 传输矩阵法计算反射/透射
# - 应用：高反射镜、带通滤波器、分束器
# =============================================================================
def thin_film_reflectance(n0, n1, n2, d, wavelength, theta=0):
    """
    计算单层薄膜反射率 Calculate single-layer thin film reflectance

    公式 Formula:
    r = (r₁₂ + r₂₃exp(2iδ))/(1 + r₁₂r₂₃exp(2iδ))
    δ = 2πn₁d/λ (正入射时)

    参数 Parameters:
        n0: float - 入射介质折射率 incident medium index
        n1: float - 薄膜折射率 film index
        n2: float - 基底折射率 substrate index
        d: float - 薄膜厚度 film thickness [m]
        wavelength: float - 光波长 wavelength [m]
        theta: float - 入射角 angle of incidence [rad]（未使用，保留接口）

    返回 Returns:
        float - 反射率 reflectance R = |r|²

    物理意义 Physical meaning:
    - 两界面反射光的相干叠加
    - 相位差决定干涉加强或减弱
    """
    r12 = (n0 - n1) / (n0 + n1)
    r23 = (n1 - n2) / (n1 + n2)
    delta = 2 * np.pi * n1 * d / wavelength

    r = (r12 + r23 * np.exp(2j * delta)) / (1 + r12 * r23 * np.exp(2j * delta))
    return np.abs(r)**2

def antireflection_coating_thickness(n_coating, wavelength):
    """
    计算增透膜厚度 Calculate AR coating thickness

    公式 Formula: d = λ/(4n)

    参数 Parameters:
        n_coating: float - 增透膜折射率 AR coating index
        wavelength: float - 设计波长 design wavelength [m]

    返回 Returns:
        float - 增透膜厚度 AR coating thickness [m]

    物理意义 Physical meaning:
    - 四分之一波长厚度使两束反射光相差 π（半波长）
    - 结合折射率匹配条件，可实现零反射
    """
    return wavelength / (4 * n_coating)

def antireflection_coating_index(n1, n2):
    """
    计算理想增透膜折射率 Calculate ideal AR coating index

    公式 Formula: n_coating = √(n₁ × n₂)

    参数 Parameters:
        n1: float - 入射介质折射率 incident medium index
        n2: float - 基底折射率 substrate index

    返回 Returns:
        float - 理想增透膜折射率 ideal AR coating index

    示例 Example:
    - 空气(n=1) - 玻璃(n=1.5): n_AR = 1.22
    - 常用 MgF₂ (n=1.38) 接近此值
    """
    return np.sqrt(n1 * n2)

def multilayer_reflectance(n_list, d_list, wavelength):
    """
    计算多层膜反射率（传输矩阵法）
    Calculate multilayer film reflectance (transfer matrix method)

    参数 Parameters:
        n_list: list - 各层折射率列表 [入射介质, 膜1, 膜2, ..., 基底]
        d_list: list - 各膜层厚度列表 [d1, d2, ...]（不含入射介质和基底）
        wavelength: float - 光波长 wavelength [m]

    返回 Returns:
        float - 反射率 reflectance R

    方法说明 Method:
    - 使用特征矩阵（传输矩阵）方法
    - 每层的矩阵：M = [cos(δ), i·sin(δ)/n; i·n·sin(δ), cos(δ)]
    - 总矩阵：M_total = M₁ × M₂ × ... × M_N
    """
    # 简化：需要至少3个介质（入射、膜层、基底）
    if len(n_list) < 3:
        return 0

    # 使用特征矩阵方法
    M = np.eye(2, dtype=complex)
    for n, d in zip(n_list[1:-1], d_list):
        delta = 2 * np.pi * n * d / wavelength
        m = np.array([[np.cos(delta), 1j*np.sin(delta)/n],
                      [1j*n*np.sin(delta), np.cos(delta)]])
        M = M @ m

    n0, ns = n_list[0], n_list[-1]
    r = (n0*M[0,0] + n0*ns*M[0,1] - M[1,0] - ns*M[1,1]) / \
        (n0*M[0,0] + n0*ns*M[0,1] + M[1,0] + ns*M[1,1])
    return np.abs(r)**2


# =============================================================================
# 练习 13.6: 光学各向异性
# Exercise 13.6: Optical Anisotropy
#
# 物理背景 Physical Background:
# 某些材料在外场作用下表现出光学各向异性
# 这些效应是光调制器、隔离器等器件的基础
#
# 电光效应 Electro-optic effects:
# 1. 普克尔斯效应（线性电光效应）
#    - Δn ∝ E（折射率变化与电场成正比）
#    - 仅存在于无反演对称性的晶体中
#    - 应用：EOM（电光调制器）、Q开关
#
# 2. 克尔效应（二次电光效应）
#    - Δn ∝ E²（所有材料都有）
#    - 应用：克尔盒、光学快门
#
# 磁光效应 Magneto-optic effects:
# 1. 法拉第效应
#    - 偏振面随磁场旋转：θ = VBL
#    - 非互易性：正向和反向旋转方向相同
#    - 应用：光隔离器、磁场传感
#
# 2. 科顿-穆顿效应
#    - 磁场诱导的线性双折射：Δn ∝ B²
# =============================================================================
def kerr_effect_birefringence(K, E, wavelength):
    """
    计算克尔效应诱导的双折射 Calculate Kerr effect induced birefringence

    公式 Formula: Δn = KλE²

    参数 Parameters:
        K: float - 克尔常数 Kerr constant [m/V²]
        E: float - 电场强度 electric field [V/m]
        wavelength: float - 光波长 wavelength [m]

    返回 Returns:
        float - 诱导的双折射率 induced birefringence

    物理意义 Physical meaning:
    - 二次电光效应，所有材料都存在
    - 各向同性材料在电场中变为各向异性
    - 响应速度快（~ps级）
    - 典型材料：CS₂, 硝基苯
    """
    return K * wavelength * E**2

def pockels_effect_phase(r, E, L, wavelength, n0):
    """
    计算普克尔斯效应相位调制 Calculate Pockels effect phase modulation

    公式 Formula: Δφ = πn₀³rEL/λ

    参数 Parameters:
        r: float - 电光系数 electro-optic coefficient [m/V]
        E: float - 电场强度 electric field [V/m]
        L: float - 晶体长度 crystal length [m]
        wavelength: float - 光波长 wavelength [m]
        n0: float - 晶体折射率 crystal refractive index

    返回 Returns:
        float - 相位调制量 phase modulation [rad]

    半波电压 Half-wave voltage:
    V_π = λd/(2n₀³rL)（产生π相位差的电压）

    典型材料 Typical materials:
    - LiNbO₃: r₃₃ ≈ 30 pm/V
    - KDP: r₆₃ ≈ 10 pm/V
    """
    return np.pi * n0**3 * r * E * L / wavelength

def faraday_rotation(V, B, L):
    """
    计算法拉第旋转角 Calculate Faraday rotation angle

    公式 Formula: θ = VBL

    参数 Parameters:
        V: float - 费尔德常数 Verdet constant [rad/(T·m)]
        B: float - 磁场强度 magnetic field [T]
        L: float - 介质长度 medium length [m]

    返回 Returns:
        float - 偏振旋转角 polarization rotation angle [rad]

    物理意义 Physical meaning:
    - 磁场沿光传播方向时，偏振面发生旋转
    - 非互易效应：往返光旋转方向相同（角度加倍）
    - 应用：光隔离器（防止反射光返回激光器）

    典型费尔德常数 Typical Verdet constants:
    - TGG (铽镓石榴石): V ≈ -40 rad/(T·m) @ 1064nm
    - 重火石玻璃: V ≈ 20 rad/(T·m)
    """
    return V * B * L

def cotton_mouton_effect(C, B, L):
    """
    计算科顿-穆顿效应（磁致双折射）
    Calculate Cotton-Mouton effect (magnetic birefringence)

    公式 Formula: Δn = CB²

    参数 Parameters:
        C: float - 科顿-穆顿常数 Cotton-Mouton constant [T⁻²]
        B: float - 磁场强度 magnetic field [T]
        L: float - 介质长度（未使用，保留接口）medium length [m]

    返回 Returns:
        float - 诱导的双折射率 induced birefringence

    物理意义 Physical meaning:
    - 磁场垂直于光传播方向时产生
    - 类似于电场的克尔效应（二次效应）
    - 主要存在于液体和气体中
    """
    return C * B**2


# =============================================================================
# 可视化
# =============================================================================
def plot_electromagnetic_optics():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 菲涅尔反射系数
    ax1 = axes[0, 0]
    theta = np.linspace(0, np.pi/2 - 0.01, 200)
    n1, n2 = 1.0, 1.5

    Rs = [np.abs(fresnel_rs(n1, n2, t))**2 for t in theta]
    Rp = [np.abs(fresnel_rp(n1, n2, t))**2 for t in theta]
    theta_B = brewster_angle(n1, n2)

    ax1.plot(np.degrees(theta), Rs, 'b-', label='R_s', linewidth=2)
    ax1.plot(np.degrees(theta), Rp, 'r-', label='R_p', linewidth=2)
    ax1.axvline(x=np.degrees(theta_B), color='g', linestyle='--',
                label=f'布儒斯特角 {np.degrees(theta_B):.1f}°')
    ax1.set_xlabel('入射角 (度)')
    ax1.set_ylabel('反射率')
    ax1.set_title('菲涅尔反射 (n₁=1, n₂=1.5)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 马吕斯定律
    ax2 = axes[0, 1]
    theta = np.linspace(0, 2*np.pi, 200)

    I = [malus_law(1, t) for t in theta]

    ax2.polar(theta, I)
    ax2.set_title('马吕斯定律 I = I₀cos²θ')

    # 3. 薄膜反射率
    ax3 = axes[0, 2]
    wavelength = np.linspace(400, 700, 200) * 1e-9
    n0, n1, n2 = 1.0, 1.38, 1.5  # 空气-MgF2-玻璃
    d = 550e-9 / (4 * n1)  # 四分之一波长 @ 550nm

    R = [thin_film_reflectance(n0, n1, n2, d, wl) for wl in wavelength]

    ax3.plot(wavelength * 1e9, np.array(R) * 100, 'b-', linewidth=2)
    ax3.set_xlabel('波长 (nm)')
    ax3.set_ylabel('反射率 (%)')
    ax3.set_title('增透膜反射率')
    ax3.grid(True, alpha=0.3)

    # 4. 双折射
    ax4 = axes[1, 0]
    theta = np.linspace(0, np.pi/2, 100)
    n_o, n_e = 1.544, 1.553  # 石英

    n_e_prime = [extraordinary_index(n_e, n_o, t) for t in theta]

    ax4.plot(np.degrees(theta), [n_o]*len(theta), 'b-', label='n_o', linewidth=2)
    ax4.plot(np.degrees(theta), n_e_prime, 'r-', label="n_e'(θ)", linewidth=2)
    ax4.set_xlabel('与光轴夹角 (度)')
    ax4.set_ylabel('折射率')
    ax4.set_title('双折射晶体 (石英)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 偏振态（琼斯矢量表示）
    ax5 = axes[1, 1]
    t = np.linspace(0, 2*np.pi, 200)

    # 线偏振
    Ex_lin = np.cos(t)
    Ey_lin = np.zeros_like(t)

    # 圆偏振
    Ex_circ = np.cos(t)
    Ey_circ = np.sin(t)

    # 椭圆偏振
    Ex_ell = np.cos(t)
    Ey_ell = 0.5 * np.sin(t + np.pi/4)

    ax5.plot(Ex_lin, Ey_lin, 'b-', label='线偏振', linewidth=2)
    ax5.plot(Ex_circ, Ey_circ, 'r-', label='圆偏振', linewidth=2)
    ax5.plot(Ex_ell, Ey_ell, 'g--', label='椭圆偏振', linewidth=2)
    ax5.set_xlabel('E_x')
    ax5.set_ylabel('E_y')
    ax5.set_title('偏振态')
    ax5.set_aspect('equal')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. 全反射与临界角
    ax6 = axes[1, 2]
    n1_range = np.linspace(1.01, 2.5, 100)
    n2 = 1.0

    theta_c = [np.degrees(critical_angle(n1, n2)) for n1 in n1_range]

    ax6.plot(n1_range, theta_c, 'b-', linewidth=2)
    ax6.axhline(y=np.degrees(critical_angle(1.5, 1.0)), color='r',
                linestyle='--', alpha=0.5, label='玻璃 (n=1.5)')
    ax6.set_xlabel('n₁')
    ax6.set_ylabel('临界角 (度)')
    ax6.set_title('全反射临界角 (n₂=1)')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('electromagnetic_optics.png', dpi=150)
    print("图像已保存为 electromagnetic_optics.png")
    plt.show()


def verify():
    """
    验证函数 Verification function
    检查所有电磁光学练习的实现是否正确
    """
    all_passed = True
    print("\n" + "="*50)
    print("验证电磁光学计算 Verifying Electromagnetic Optics")
    print("="*50 + "\n")

    # ===========================================
    # 检查 13.1: 光的电磁场描述
    # ===========================================
    I = time_averaged_intensity(1)  # E₀ = 1 V/m
    if I <= 0:
        print("❌ 13.1 光强应为正值")
        print("   提示：I = (1/2)ε₀cn|E₀|²")
        print("   确保所有物理常数正确")
        all_passed = False
    else:
        print(f"✓ 13.1 电磁场描述正确")
        print(f"   E₀ = 1 V/m 时，I = {I:.2e} W/m²")

    # ===========================================
    # 检查 13.2: 菲涅尔方程
    # ===========================================
    theta_B = brewster_angle(1.0, 1.5)
    expected = np.arctan(1.5)
    if not np.isclose(theta_B, expected, rtol=0.01):
        print("❌ 13.2 布儒斯特角计算错误")
        print("   提示：tanθ_B = n₂/n₁")
        print(f"   期望: {np.degrees(expected):.1f}°, 计算: {np.degrees(theta_B):.1f}°")
        all_passed = False
    else:
        print(f"✓ 13.2 菲涅尔方程正确")
        print(f"   空气-玻璃界面 θ_B = {np.degrees(theta_B):.1f}°")
        theta_c = critical_angle(1.5, 1.0)
        print(f"   全反射临界角 θ_c = {np.degrees(theta_c):.1f}°")

    # ===========================================
    # 检查 13.3: 偏振（马吕斯定律）
    # ===========================================
    I0 = malus_law(1, 0)
    I45 = malus_law(1, np.pi/4)
    I90 = malus_law(1, np.pi/2)
    if not np.isclose(I0, 1, rtol=0.01):
        print("❌ 13.3 马吕斯定律错误：θ=0时应有I=I₀")
        print("   提示：I = I₀cos²θ")
        all_passed = False
    elif not np.isclose(I45, 0.5, rtol=0.01):
        print("❌ 13.3 马吕斯定律错误：θ=45°时应有I=I₀/2")
        all_passed = False
    elif not np.isclose(I90, 0, atol=1e-10):
        print("❌ 13.3 马吕斯定律错误：θ=90°时应有I=0")
        all_passed = False
    else:
        print("✓ 13.3 偏振正确（马吕斯定律）")
        print("   I(0°) = I₀, I(45°) = I₀/2, I(90°) = 0 ✓")

    # ===========================================
    # 检查 13.4: 双折射
    # ===========================================
    delta_n = 0.009  # 石英的双折射率
    wavelength = 550e-9
    d = quarter_wave_plate_thickness(delta_n, wavelength)
    if d <= 0 or d > 1e-3:
        print("❌ 13.4 波片厚度不合理")
        print("   提示：d = λ/(4Δn)")
        print(f"   对于石英(Δn={delta_n}) @ 550nm，d 应约为 15 μm")
        all_passed = False
    else:
        print(f"✓ 13.4 双折射正确")
        print(f"   石英 λ/4 波片厚度 d ≈ {d*1e6:.1f} μm @ {wavelength*1e9:.0f}nm")

    # ===========================================
    # 检查 13.5: 薄膜干涉
    # ===========================================
    n_ar = antireflection_coating_index(1.0, 1.5)
    expected = np.sqrt(1.5)
    if not np.isclose(n_ar, expected, rtol=0.01):
        print("❌ 13.5 增透膜折射率计算错误")
        print("   提示：n_AR = √(n₁×n₂)")
        print(f"   期望: {expected:.3f}, 计算: {n_ar:.3f}")
        all_passed = False
    else:
        d_ar = antireflection_coating_thickness(n_ar, 550e-9)
        print(f"✓ 13.5 薄膜干涉正确")
        print(f"   空气-玻璃理想增透膜: n = {n_ar:.3f}")
        print(f"   膜厚 @ 550nm: d = {d_ar*1e9:.1f} nm")

    # ===========================================
    # 检查 13.6: 光学各向异性
    # ===========================================
    V = 1e-5  # 费尔德常数（弱玻璃的典型值）
    B = 1  # 1 T
    L = 0.1  # 10 cm
    theta_F = faraday_rotation(V, B, L)
    if theta_F < 0:
        print("❌ 13.6 法拉第旋转角符号错误")
        print("   提示：θ = VBL，当V>0, B>0, L>0时，θ>0")
        all_passed = False
    else:
        print(f"✓ 13.6 光学各向异性正确")
        print(f"   法拉第旋转: θ = VBL = {np.degrees(theta_F):.4f}°")
        print(f"   (V = {V} rad/(T·m), B = {B} T, L = {L} m)")

    # ===========================================
    # 总结
    # ===========================================
    print("\n" + "-"*50)
    if all_passed:
        print("所有测试通过！电磁光学计算正确。")
        print("-"*50)
        print("\n正在生成可视化图像...")
        try:
            plot_electromagnetic_optics()
        except Exception as e:
            print(f"可视化失败: {e}")
    else:
        print("部分测试未通过，请检查上述错误提示。")
        print("-"*50)
        print("\n学习建议 Study Tips:")
        print("1. 光强：I = (1/2)ε₀cn|E₀|² 与电场振幅平方成正比")
        print("2. 菲涅尔方程：区分 s 偏振和 p 偏振")
        print("3. 马吕斯定律：I = I₀cos²θ 描述偏振片透射")
        print("4. 双折射：波片厚度 d = λ/(4Δn) 产生 π/2 相位差")
        print("5. 增透膜：n = √(n₁n₂)，d = λ/(4n)")
        print("6. 法拉第效应：θ = VBL，非互易性是关键")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("电磁光学 Electromagnetic Optics")
    print("=" * 50)
    verify()
