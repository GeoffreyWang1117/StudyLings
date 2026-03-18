"""
多普勒效应 Doppler Effect
难度 Difficulty: ★★★

学习目标 Learning Objectives:
- 理解声波和光波的多普勒效应及其区别
  Understand Doppler effect for sound and light waves
- 掌握观测频率和波长的变化规律
  Master the changes in observed frequency and wavelength
- 分析超音速运动中的冲击波和马赫锥
  Analyze shock waves and Mach cone in supersonic motion
- 应用多普勒效应于雷达测速、医学超声和天文红移
  Apply Doppler effect to radar, ultrasound, and astronomical redshift

物理背景 Physical Background:
多普勒效应是指波源与观察者相对运动时，观测到的波的频率发生变化的现象。

声学多普勒效应：
f' = f₀ × (v_medium + v_observer) / (v_medium + v_source)
符号约定：
- v_observer > 0: 观察者向声源运动
- v_source > 0: 声源远离观察者

关键特点：
- 靠近时频率升高（蓝移）
- 远离时频率降低（红移）
- 当声源速度等于声速时，f' → ∞（声锥形成）

光学多普勒效应：
- 经典近似（v << c）：Δf/f ≈ v/c
- 需要考虑相对论效应（时间膨胀）
- 宇宙学红移：z = (λ_obs - λ_emit) / λ_emit

应用领域：
- 交通雷达测速
- 医学超声血流检测
- 天文学距离测量（哈勃定律）
- 多普勒气象雷达

HINT: 声波多普勒: f' = f(v + v_r)/(v + v_s)
HINT: 靠近时频率升高，远离时频率降低
HINT: 马赫数: M = v/c_sound
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import c

# I AM NOT DONE

# 声速（空气中，20°C）
c_sound = 343  # m/s

# =============================================================================
# 练习 6.1: 声波多普勒效应
# Exercise 6.1: Acoustic Doppler Effect
# =============================================================================
def doppler_frequency_sound(f_source, v_source, v_receiver, v_medium=c_sound):
    """
    声波的多普勒效应
    f' = f × (v_medium + v_receiver) / (v_medium + v_source)

    约定：
    - 接收者向声源移动为正
    - 声源向接收者移动为负（离开为正）

    f_source: 声源频率
    v_source: 声源速度（正=远离接收者）
    v_receiver: 接收者速度（正=向声源移动）
    v_medium: 介质中的声速
    """
    # TODO: 计算多普勒频率
    f_observed = f_source * (v_medium + v_receiver) / (v_medium + v_source)
    return f_observed


def doppler_wavelength_sound(wavelength_source, v_source, v_medium=c_sound):
    """
    声源运动时的波长变化
    λ' = λ × (v_medium + v_source) / v_medium
    """
    # TODO: 计算波长变化
    wavelength_observed = wavelength_source * (v_medium + v_source) / v_medium
    return wavelength_observed


def frequency_shift_sound(f_source, v_relative, approaching=True):
    """
    简化的多普勒频移（声源和接收者相对运动）
    """
    # TODO: 计算频移
    if approaching:
        # 靠近时，频率升高
        f_observed = f_source * c_sound / (c_sound - abs(v_relative))
    else:
        # 远离时，频率降低
        f_observed = f_source * c_sound / (c_sound + abs(v_relative))
    return f_observed


# =============================================================================
# 练习 6.2: 马赫数和声锥
# Exercise 6.2: Mach Number and Mach Cone
# =============================================================================
def mach_number(v, v_sound=c_sound):
    """
    计算马赫数
    M = v/c_sound
    """
    return v / v_sound


def mach_cone_angle(M):
    """
    马赫锥半角
    sin(θ) = 1/M (M > 1)
    """
    if M <= 1:
        return np.pi / 2  # 没有马赫锥
    # TODO: 计算马赫锥半角
    theta = np.arcsin(1 / M)
    return theta


def supersonic_boom_distance(v, v_sound, t):
    """
    超音速物体经过t秒后，声锥在地面的位置
    返回声锥到物体正下方的距离
    """
    M = mach_number(v, v_sound)
    if M <= 1:
        return 0
    theta = mach_cone_angle(M)
    # TODO: 计算距离
    # 物体位置
    x_object = v * t
    # 声锥与地面的交点到物体的水平距离
    distance = x_object * np.tan(theta)
    return distance


# =============================================================================
# 练习 6.3: 经典光学多普勒效应
# Exercise 6.3: Classical Optical Doppler Effect
# =============================================================================
def doppler_frequency_light_classical(f_source, v_relative, approaching=True):
    """
    经典（非相对论）光学多普勒效应
    f' = f(1 ± v/c)

    注意：这只是近似，精确计算需要相对论效应
    """
    if approaching:
        f_observed = f_source * (1 + v_relative / c)
    else:
        f_observed = f_source * (1 - v_relative / c)
    return f_observed


def wavelength_shift(wavelength_source, v_relative, approaching=True):
    """
    波长变化（红移/蓝移）
    Δλ/λ = v/c (非相对论近似)
    """
    # TODO: 计算波长变化
    if approaching:
        # 蓝移
        wavelength_observed = wavelength_source * (1 - v_relative / c)
    else:
        # 红移
        wavelength_observed = wavelength_source * (1 + v_relative / c)
    return wavelength_observed


def redshift_parameter(wavelength_observed, wavelength_emitted):
    """
    红移参数
    z = (λ_obs - λ_emit) / λ_emit = Δλ/λ
    """
    # TODO: 计算红移参数
    z = (wavelength_observed - wavelength_emitted) / wavelength_emitted
    return z


def velocity_from_redshift(z):
    """
    从红移参数计算退行速度（非相对论近似）
    v = zc
    """
    return z * c


# =============================================================================
# 练习 6.4: 雷达测速
# Exercise 6.4: Radar Speed Measurement
# =============================================================================
def radar_doppler_shift(f_radar, v_target, angle=0):
    """
    雷达多普勒测速
    由于波往返，频移加倍
    Δf = 2f × v cos(θ) / c

    angle: 目标运动方向与雷达视线的夹角
    """
    # TODO: 计算频移
    delta_f = 2 * f_radar * v_target * np.cos(angle) / c
    return delta_f


def speed_from_radar(f_radar, delta_f, angle=0):
    """
    从雷达频移计算速度
    v = Δf × c / (2f × cos(θ))
    """
    # TODO: 计算速度
    v = delta_f * c / (2 * f_radar * np.cos(angle))
    return v


def police_radar_reading(f_radar, v_car, v_police=0, same_direction=True):
    """
    警用雷达测速读数
    考虑警车自身运动
    """
    # 相对速度
    if same_direction:
        v_relative = v_car - v_police
    else:
        v_relative = v_car + v_police

    delta_f = radar_doppler_shift(f_radar, abs(v_relative))
    return delta_f, v_relative


# =============================================================================
# 练习 6.5: 医学超声多普勒
# Exercise 6.5: Medical Ultrasound Doppler
# =============================================================================
def ultrasound_doppler(f_ultrasound, v_blood, angle, c_tissue=1540):
    """
    医学超声多普勒血流测速
    Δf = 2f × v × cos(θ) / c_tissue

    c_tissue: 组织中的声速 (~1540 m/s)
    """
    # TODO: 计算频移
    delta_f = 2 * f_ultrasound * v_blood * np.cos(angle) / c_tissue
    return delta_f


def blood_velocity(f_ultrasound, delta_f, angle, c_tissue=1540):
    """
    从超声多普勒频移计算血流速度
    """
    # TODO: 计算血流速度
    v = delta_f * c_tissue / (2 * f_ultrasound * np.cos(angle))
    return v


# =============================================================================
# 练习 6.6: 运动方向角
# Exercise 6.6: Direction of Motion
# =============================================================================
def doppler_with_angle(f_source, v_source, theta, v_medium=c_sound):
    """
    声源沿任意方向运动时的多普勒效应
    只有径向分量产生多普勒效应
    v_radial = v × cos(θ)
    """
    # TODO: 计算径向分量产生的多普勒效应
    v_radial = v_source * np.cos(theta)
    f_observed = f_source * v_medium / (v_medium + v_radial)
    return f_observed


def time_varying_frequency(f_source, v_source, d_min, t, v_medium=c_sound):
    """
    声源匀速直线运动时，接收者听到的频率随时间变化
    d_min: 声源最近距离
    t: 时间（t=0时声源在最近点）
    """
    # 声源位置（沿直线运动）
    x = v_source * t
    # 到接收者的距离
    r = np.sqrt(x**2 + d_min**2)
    # 径向速度
    v_radial = v_source * x / r

    # TODO: 计算瞬时频率
    f_observed = f_source * v_medium / (v_medium + v_radial)
    return f_observed


# =============================================================================
# 练习 6.7: 哈勃定律
# Exercise 6.7: Hubble's Law
# =============================================================================
H0 = 70  # 哈勃常数 km/s/Mpc

def hubble_velocity(distance):
    """
    哈勃定律
    v = H₀ × d

    distance: 以Mpc为单位
    返回: 以km/s为单位的速度
    """
    return H0 * distance


def hubble_distance(z, H0=70):
    """
    从红移估算距离（非相对论近似）
    d = v/H₀ = zc/H₀
    """
    # TODO: 计算距离 (Mpc)
    v = z * c / 1000  # 转换为 km/s
    d = v / H0  # Mpc
    return d


def cosmic_redshift_wavelength(wavelength_emit, z):
    """
    宇宙学红移
    λ_obs = λ_emit × (1 + z)
    """
    return wavelength_emit * (1 + z)


# =============================================================================
# 可视化
# =============================================================================
def plot_doppler():
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    # 1. 声源运动的多普勒效应
    ax1 = axes[0, 0]
    f0 = 1000  # Hz
    v_range = np.linspace(-300, 300, 100)  # 正=远离

    f_observed = [doppler_frequency_sound(f0, v, 0) for v in v_range]
    ax1.plot(v_range, f_observed, 'b-', linewidth=2)
    ax1.axhline(y=f0, color='r', linestyle='--', label='f₀')
    ax1.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    ax1.set_xlabel('Source velocity (m/s)')
    ax1.set_ylabel('Observed frequency (Hz)')
    ax1.set_title('声波多普勒效应')
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    # 2. 马赫锥
    ax2 = axes[0, 1]
    M_range = np.linspace(1.01, 5, 100)
    angles = [np.degrees(mach_cone_angle(M)) for M in M_range]
    ax2.plot(M_range, angles, 'r-', linewidth=2)
    ax2.set_xlabel('Mach number')
    ax2.set_ylabel('Cone half-angle (degrees)')
    ax2.set_title('马赫锥半角')
    ax2.grid(True, alpha=0.3)

    # 3. 警笛经过时的频率变化
    ax3 = axes[0, 2]
    v_siren = 30  # 30 m/s
    f_siren = 800  # Hz
    d_min = 20  # 最近距离 20 m

    t_range = np.linspace(-3, 3, 500)
    f_heard = [time_varying_frequency(f_siren, v_siren, d_min, t) for t in t_range]
    ax3.plot(t_range, f_heard, 'g-', linewidth=2)
    ax3.axhline(y=f_siren, color='r', linestyle='--', label='f₀')
    ax3.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Frequency (Hz)')
    ax3.set_title('警笛经过时的频率变化')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 红移和蓝移
    ax4 = axes[1, 0]
    wavelength = np.linspace(400, 700, 100)  # 可见光 nm
    v_rel = 0.1 * c  # 0.1c
    wavelength_red = wavelength_shift(wavelength * 1e-9, v_rel, approaching=False) * 1e9
    wavelength_blue = wavelength_shift(wavelength * 1e-9, v_rel, approaching=True) * 1e9

    ax4.plot(wavelength, wavelength, 'k-', label='Rest', linewidth=2)
    ax4.plot(wavelength, wavelength_red, 'r-', label='Redshift', linewidth=2)
    ax4.plot(wavelength, wavelength_blue, 'b-', label='Blueshift', linewidth=2)
    ax4.set_xlabel('Rest wavelength (nm)')
    ax4.set_ylabel('Observed wavelength (nm)')
    ax4.set_title('光学多普勒效应 (v=0.1c)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 雷达多普勒
    ax5 = axes[1, 1]
    f_radar = 10e9  # 10 GHz
    v_target_range = np.linspace(0, 50, 100)  # 0-50 m/s

    delta_f = [radar_doppler_shift(f_radar, v) / 1e3 for v in v_target_range]  # kHz
    ax5.plot(v_target_range * 3.6, delta_f, 'b-', linewidth=2)  # 转换为 km/h
    ax5.set_xlabel('Target speed (km/h)')
    ax5.set_ylabel('Frequency shift (kHz)')
    ax5.set_title('雷达多普勒频移')
    ax5.grid(True, alpha=0.3)

    # 6. 哈勃图
    ax6 = axes[1, 2]
    z_range = np.linspace(0, 0.1, 100)
    distances = [hubble_distance(z) for z in z_range]
    velocities = [z * c / 1000 for z in z_range]  # km/s

    ax6.plot(distances, velocities, 'r-', linewidth=2)
    ax6.set_xlabel('Distance (Mpc)')
    ax6.set_ylabel('Recession velocity (km/s)')
    ax6.set_title('哈勃定律')
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('doppler_effect.png', dpi=150)
    print("图像已保存为 doppler_effect.png")
    plt.show()


def verify():
    """
    验证所有练习的正确性
    Verify all exercises
    """
    all_passed = True

    # 检查 6.1 - 声波多普勒 Check acoustic Doppler
    f0 = 1000  # 声源频率 1000 Hz
    v_source = -30  # 向接收者运动（负号表示靠近）
    f_obs = doppler_frequency_sound(f0, v_source, 0)
    expected = f0 * c_sound / (c_sound + v_source)
    if not np.isclose(f_obs, expected, rtol=0.01):
        print("错误 6.1: 声波多普勒效应计算错误，请检查公式")
        all_passed = False
    else:
        print(f"通过 6.1: 声波多普勒正确 (f₀=1000Hz, 声源以30m/s靠近 → f'={f_obs:.1f}Hz)")

    # 检查 6.2 - 马赫锥 Check Mach cone
    M = 2.0  # 马赫数为2
    theta = mach_cone_angle(M)
    expected_theta = np.arcsin(1/M)
    if not np.isclose(theta, expected_theta, rtol=0.01):
        print("错误 6.2: 马赫锥半角计算错误，请检查公式 sin(θ) = 1/M")
        all_passed = False
    else:
        print(f"通过 6.2: 马赫锥正确 (M=2 时马赫锥半角 θ={np.degrees(theta):.1f}°)")

    # 检查 6.3 - 光学多普勒和红移 Check optical Doppler/redshift
    wavelength_H_alpha = 656.3e-9  # 氢原子 Hα 谱线波长
    v = 0.01 * c  # 退行速度为光速的1%
    wavelength_obs = wavelength_shift(wavelength_H_alpha, v, approaching=False)
    z = redshift_parameter(wavelength_obs, wavelength_H_alpha)
    if not np.isclose(z, 0.01, rtol=0.01):
        print("错误 6.3: 光学红移计算错误，请检查红移参数公式 z = Δλ/λ")
        all_passed = False
    else:
        print(f"通过 6.3: 光学多普勒正确 (退行速度0.01c → 红移 z = {z:.4f})")

    # 检查 6.4 - 雷达测速 Check radar speed measurement
    f_radar = 10e9  # 雷达频率 10 GHz
    v_car = 30  # 目标速度 30 m/s
    delta_f = radar_doppler_shift(f_radar, v_car)
    v_measured = speed_from_radar(f_radar, delta_f)
    if not np.isclose(v_measured, v_car, rtol=0.01):
        print("错误 6.4: 雷达测速计算错误，注意往返路径使频移加倍")
        all_passed = False
    else:
        print(f"通过 6.4: 雷达测速正确 (v={v_car}m/s → 频移Δf={delta_f/1e3:.1f}kHz)")

    # 检查 6.5 - 医学超声 Check medical ultrasound
    f_us = 5e6  # 超声频率 5 MHz
    v_blood = 0.5  # 血流速度 0.5 m/s
    angle = np.radians(45)  # 探头与血管夹角 45°
    delta_f_us = ultrasound_doppler(f_us, v_blood, angle)
    v_calc = blood_velocity(f_us, delta_f_us, angle)
    if not np.isclose(v_calc, v_blood, rtol=0.01):
        print("错误 6.5: 超声多普勒计算错误，注意角度因子 cos(θ)")
        all_passed = False
    else:
        print(f"通过 6.5: 超声多普勒正确 (血流频移 Δf={delta_f_us:.1f}Hz)")

    # 检查 6.7 - 哈勃定律 Check Hubble's law
    z = 0.05  # 红移
    d = hubble_distance(z)
    v_expected = z * c / 1000  # km/s
    d_expected = v_expected / H0  # Mpc
    if not np.isclose(d, d_expected, rtol=0.01):
        print("错误 6.7: 哈勃定律计算错误，请检查 d = v/H₀ = zc/H₀")
        all_passed = False
    else:
        print(f"通过 6.7: 哈勃定律正确 (红移z=0.05 → 距离d={d:.0f} Mpc)")

    if all_passed:
        print("\n全部测试通过！正在生成可视化图像...")
        print("All tests passed! Generating visualization...")
        try:
            plot_doppler()
        except Exception as e:
            print(f"可视化失败 Visualization failed: {e}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("多普勒效应 Doppler Effect")
    print("=" * 50)
    verify()
