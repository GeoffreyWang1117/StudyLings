"""
信号处理与滤波器 Signal Processing and Filters
难度 Difficulty: ★★★★

学习目标 Learning Objectives:
- 理解信号的时域和频域分析方法
  Understand time-domain and frequency-domain signal analysis
- 掌握各类滤波器（低通、高通、带通）的设计原理
  Master design principles of various filters (lowpass, highpass, bandpass)
- 分析采样定理、奈奎斯特频率和混叠现象
  Analyze sampling theorem, Nyquist frequency, and aliasing
- 理解卷积、相关和窗函数在信号处理中的应用
  Understand convolution, correlation, and window functions

物理背景 Physical Background:
信号处理是将数学工具应用于信号分析和变换的学科，
在通信、音频、图像处理等领域有广泛应用。

傅里叶变换：
- 将时域信号分解为不同频率的正弦分量
- FFT（快速傅里叶变换）是高效的数值算法
- 频谱分析揭示信号的频率成分

采样定理（奈奎斯特-香农定理）：
要完整恢复带限信号，采样率必须大于最高频率的两倍
f_s > 2f_max
否则会产生混叠（aliasing），高频信号被误识为低频

滤波器：
- 低通滤波器：允许低频通过，衰减高频
- 高通滤波器：允许高频通过，衰减低频
- 带通滤波器：只允许特定频带通过
- 传递函数 H(ω) = 输出/输入 描述滤波器特性

重要概念：
- 截止频率 ω_c：-3dB 点（功率降为一半）
- 品质因子 Q：带通滤波器的带宽特性
- 相位响应：滤波器引起的相位延迟

HINT: 奈奎斯特频率: f_N = f_s/2
HINT: 低通滤波器传递函数: H(ω) = 1/(1 + iω/ω_c)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft, fftfreq
from scipy.signal import butter, lfilter, freqz
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])
from utils.constants import c

# I AM NOT DONE

# =============================================================================
# 练习 9.1: 傅里叶变换
# Exercise 9.1: Fourier Transform
# =============================================================================
def compute_fft(signal, dt):
    """
    计算信号的傅里叶变换
    返回频率数组和复数频谱
    """
    # TODO: 计算FFT
    N = len(signal)
    spectrum = fft(signal)
    freqs = fftfreq(N, dt)

    return freqs, spectrum

def power_spectrum(signal, dt):
    """
    计算功率谱密度
    PSD = |X(f)|²/N
    """
    freqs, spectrum = compute_fft(signal, dt)
    N = len(signal)
    psd = np.abs(spectrum)**2 / N
    return freqs, psd

def inverse_fft(spectrum):
    """
    逆傅里叶变换
    """
    return ifft(spectrum)


# =============================================================================
# 练习 9.2: 采样定理
# Exercise 9.2: Sampling Theorem
# =============================================================================
def nyquist_frequency(sample_rate):
    """
    奈奎斯特频率
    f_N = f_s / 2
    """
    return sample_rate / 2

def check_aliasing(signal_freq, sample_rate):
    """
    检查是否发生混叠
    当信号频率 > 奈奎斯特频率时发生混叠
    """
    f_N = nyquist_frequency(sample_rate)
    return signal_freq > f_N

def alias_frequency(signal_freq, sample_rate):
    """
    计算混叠后的表观频率
    f_alias = |f - n*f_s|，取最小正值
    """
    f_N = nyquist_frequency(sample_rate)
    if signal_freq <= f_N:
        return signal_freq

    # 折叠回奈奎斯特范围
    f_alias = signal_freq % sample_rate
    if f_alias > f_N:
        f_alias = sample_rate - f_alias
    return f_alias


# =============================================================================
# 练习 9.3: 低通滤波器
# Exercise 9.3: Low-Pass Filter
# =============================================================================
def lowpass_transfer_function(omega, omega_c):
    """
    一阶低通滤波器传递函数
    H(ω) = 1 / (1 + iω/ω_c)
    """
    # TODO: 计算传递函数
    return 1 / (1 + 1j * omega / omega_c)

def lowpass_gain(omega, omega_c):
    """
    低通滤波器增益
    |H(ω)| = 1 / √(1 + (ω/ω_c)²)
    """
    H = lowpass_transfer_function(omega, omega_c)
    return np.abs(H)

def lowpass_phase(omega, omega_c):
    """
    低通滤波器相位
    φ(ω) = -arctan(ω/ω_c)
    """
    return -np.arctan(omega / omega_c)

def butterworth_lowpass(signal, cutoff, sample_rate, order=4):
    """
    巴特沃斯低通滤波器
    """
    nyq = nyquist_frequency(sample_rate)
    normalized_cutoff = cutoff / nyq
    b, a = butter(order, normalized_cutoff, btype='low')
    filtered = lfilter(b, a, signal)
    return filtered


# =============================================================================
# 练习 9.4: 高通和带通滤波器
# Exercise 9.4: High-Pass and Band-Pass Filters
# =============================================================================
def highpass_transfer_function(omega, omega_c):
    """
    一阶高通滤波器传递函数
    H(ω) = iω/ω_c / (1 + iω/ω_c)
    """
    return (1j * omega / omega_c) / (1 + 1j * omega / omega_c)

def bandpass_transfer_function(omega, omega_low, omega_high):
    """
    带通滤波器传递函数（级联高通和低通）
    """
    H_low = lowpass_transfer_function(omega, omega_high)
    H_high = highpass_transfer_function(omega, omega_low)
    return H_low * H_high

def quality_factor(omega_0, bandwidth):
    """
    品质因子 Q = ω₀/Δω
    """
    return omega_0 / bandwidth

def resonant_filter(omega, omega_0, Q):
    """
    谐振滤波器
    H(ω) = 1 / (1 + iQ(ω/ω₀ - ω₀/ω))
    """
    x = omega / omega_0
    return 1 / (1 + 1j * Q * (x - 1/x))


# =============================================================================
# 练习 9.5: 卷积和相关
# Exercise 9.5: Convolution and Correlation
# =============================================================================
def convolve_signals(signal1, signal2):
    """
    信号卷积
    (f*g)(t) = ∫f(τ)g(t-τ)dτ
    """
    # 使用FFT卷积定理
    N = len(signal1) + len(signal2) - 1

    F1 = fft(signal1, N)
    F2 = fft(signal2, N)

    result = ifft(F1 * F2)
    return np.real(result)

def cross_correlation(signal1, signal2):
    """
    互相关函数
    R_xy(τ) = ∫x(t)y(t+τ)dt
    """
    # 互相关 = x与y翻转的卷积
    return convolve_signals(signal1, signal2[::-1])

def autocorrelation(signal):
    """
    自相关函数
    R_xx(τ) = ∫x(t)x(t+τ)dt
    """
    return cross_correlation(signal, signal)


# =============================================================================
# 练习 9.6: 窗函数
# Exercise 9.6: Window Functions
# =============================================================================
def rectangular_window(N):
    """
    矩形窗
    """
    return np.ones(N)

def hanning_window(N):
    """
    汉宁窗
    w(n) = 0.5(1 - cos(2πn/(N-1)))
    """
    n = np.arange(N)
    return 0.5 * (1 - np.cos(2 * np.pi * n / (N - 1)))

def hamming_window(N):
    """
    汉明窗
    w(n) = 0.54 - 0.46cos(2πn/(N-1))
    """
    n = np.arange(N)
    return 0.54 - 0.46 * np.cos(2 * np.pi * n / (N - 1))

def blackman_window(N):
    """
    布莱克曼窗
    """
    n = np.arange(N)
    return 0.42 - 0.5 * np.cos(2 * np.pi * n / (N - 1)) + \
           0.08 * np.cos(4 * np.pi * n / (N - 1))

def apply_window(signal, window_func):
    """
    对信号应用窗函数
    """
    N = len(signal)
    window = window_func(N)
    return signal * window


# =============================================================================
# 可视化
# =============================================================================
def plot_signal_processing():
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # 1. 信号和频谱
    ax1 = axes[0, 0]
    sample_rate = 1000
    dt = 1 / sample_rate
    t = np.arange(0, 1, dt)

    # 复合信号
    signal = np.sin(2 * np.pi * 50 * t) + 0.5 * np.sin(2 * np.pi * 120 * t) + \
             0.2 * np.random.randn(len(t))

    ax1.plot(t[:200], signal[:200], 'b-', linewidth=1)
    ax1.set_xlabel('时间 (s)')
    ax1.set_ylabel('幅度')
    ax1.set_title('复合信号')
    ax1.grid(True, alpha=0.3)

    # 2. 功率谱
    ax2 = axes[0, 1]
    freqs, psd = power_spectrum(signal, dt)

    ax2.semilogy(freqs[:len(freqs)//2], psd[:len(psd)//2], 'b-', linewidth=1)
    ax2.set_xlabel('频率 (Hz)')
    ax2.set_ylabel('功率谱密度')
    ax2.set_title('功率谱')
    ax2.set_xlim(0, 200)
    ax2.grid(True, alpha=0.3)

    # 3. 低通滤波器响应
    ax3 = axes[0, 2]
    omega = np.logspace(-1, 2, 500)
    omega_c = 10

    gain = [lowpass_gain(w, omega_c) for w in omega]

    ax3.semilogx(omega, 20 * np.log10(gain), 'b-', linewidth=2)
    ax3.axhline(y=-3, color='r', linestyle='--', label='-3dB')
    ax3.axvline(x=omega_c, color='g', linestyle='--', label='ω_c')
    ax3.set_xlabel('ω (rad/s)')
    ax3.set_ylabel('增益 (dB)')
    ax3.set_title('低通滤波器频率响应')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. 滤波效果
    ax4 = axes[1, 0]
    filtered = butterworth_lowpass(signal, 80, sample_rate)

    ax4.plot(t[:200], signal[:200], 'b-', alpha=0.5, label='原始')
    ax4.plot(t[:200], filtered[:200], 'r-', linewidth=2, label='滤波后')
    ax4.set_xlabel('时间 (s)')
    ax4.set_ylabel('幅度')
    ax4.set_title('低通滤波效果')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 窗函数
    ax5 = axes[1, 1]
    N = 64

    windows = [
        ('矩形', rectangular_window(N)),
        ('汉宁', hanning_window(N)),
        ('汉明', hamming_window(N)),
        ('布莱克曼', blackman_window(N))
    ]

    for name, w in windows:
        ax5.plot(w, label=name, linewidth=2)

    ax5.set_xlabel('样本')
    ax5.set_ylabel('幅度')
    ax5.set_title('窗函数')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    # 6. 混叠演示
    ax6 = axes[1, 2]
    t_fine = np.linspace(0, 1, 10000)
    f_signal = 80  # Hz
    signal_fine = np.sin(2 * np.pi * f_signal * t_fine)

    # 不同采样率
    for fs in [200, 100, 60]:
        t_sampled = np.arange(0, 1, 1/fs)
        signal_sampled = np.sin(2 * np.pi * f_signal * t_sampled)
        ax6.plot(t_sampled[:30], signal_sampled[:30], 'o-',
                label=f'f_s={fs}Hz', markersize=4)

    ax6.plot(t_fine[:1000], signal_fine[:1000], 'k-', alpha=0.3, label='原始')
    ax6.set_xlabel('时间 (s)')
    ax6.set_ylabel('幅度')
    ax6.set_title(f'采样与混叠 (f={f_signal}Hz)')
    ax6.legend()
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('signal_processing.png', dpi=150)
    print("图像已保存为 signal_processing.png")
    plt.show()


def verify():
    """
    验证所有练习的正确性
    Verify all exercises
    """
    all_passed = True

    sample_rate = 1000  # 采样率 1000 Hz
    dt = 1 / sample_rate

    # 检查 9.1 - 傅里叶变换 Check FFT
    t = np.arange(0, 1, dt)
    signal = np.sin(2 * np.pi * 50 * t)  # 50 Hz 正弦波
    freqs, spectrum = compute_fft(signal, dt)
    peak_freq = np.abs(freqs[np.argmax(np.abs(spectrum[:len(spectrum)//2]))])
    if not np.isclose(peak_freq, 50, rtol=0.05):
        print("错误 9.1: FFT 未能正确检测信号频率")
        all_passed = False
    else:
        print(f"通过 9.1: 傅里叶变换正确（检测到主频 {peak_freq:.1f} Hz）")

    # 检查 9.2 - 采样定理 Check sampling theorem
    f_N = nyquist_frequency(sample_rate)
    if f_N != 500:
        print("错误 9.2: 奈奎斯特频率计算错误，应为 f_s/2 = 500 Hz")
        all_passed = False
    else:
        alias = alias_frequency(600, sample_rate)
        print(f"通过 9.2: 采样定理正确 (奈奎斯特频率 f_N = {f_N} Hz, 600Hz混叠为 → {alias}Hz)")

    # 检查 9.3 - 低通滤波器 Check lowpass filter
    omega_c = 100  # 截止频率 100 rad/s
    gain_dc = lowpass_gain(0, omega_c)  # 直流增益
    gain_cutoff = lowpass_gain(omega_c, omega_c)  # 截止频率处增益
    if not np.isclose(gain_dc, 1, rtol=0.01) or not np.isclose(gain_cutoff, 1/np.sqrt(2), rtol=0.01):
        print("错误 9.3: 低通滤波器增益错误，截止频率处应为 1/√2 ≈ 0.707（-3dB点）")
        all_passed = False
    else:
        print(f"通过 9.3: 低通滤波器正确 (截止频率处增益 |H(ω_c)| = {gain_cutoff:.3f} ≈ -3dB)")

    # 检查 9.4 - 品质因子 Check quality factor
    Q = quality_factor(1000, 100)  # ω₀=1000, 带宽=100
    if Q != 10:
        print("错误 9.4: 品质因子计算错误，Q = ω₀/Δω = 1000/100 = 10")
        all_passed = False
    else:
        print(f"通过 9.4: 带通滤波器正确 (品质因子 Q = {Q})")

    # 检查 9.5 - 卷积和相关 Check convolution and correlation
    delta = np.zeros(100)
    delta[50] = 1  # 单位冲激
    auto = autocorrelation(delta)
    if np.argmax(auto) != 149:  # 卷积后长度为 2N-1
        print("错误 9.5: 自相关计算错误")
        all_passed = False
    else:
        print(f"通过 9.5: 卷积和相关正确")

    # 检查 9.6 - 窗函数 Check window functions
    N = 64
    hann = hanning_window(N)
    if not np.isclose(hann[0], 0, atol=0.01) or not np.isclose(hann[N//2], 1, rtol=0.01):
        print("错误 9.6: 汉宁窗特性错误，边缘应为0，中心应为1")
        all_passed = False
    else:
        print(f"通过 9.6: 窗函数正确（汉宁窗边缘为0，中心为1）")

    if all_passed:
        print("\n全部测试通过！正在生成可视化图像...")
        print("All tests passed! Generating visualization...")
        try:
            plot_signal_processing()
        except Exception as e:
            print(f"可视化失败 Visualization failed: {e}")

    return all_passed

if __name__ == "__main__":
    print("=" * 50)
    print("信号处理与滤波器 Signal Processing and Filters")
    print("=" * 50)
    verify()
