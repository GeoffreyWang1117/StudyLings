"""
傅里叶分析 Fourier Analysis
难度 Difficulty: ★★★★

学习目标 Learning Objectives:
- 理解傅里叶级数和傅里叶变换的数学原理
  Understand the mathematical principles of Fourier series and transform
- 用频域方法分析周期信号和非周期信号
  Analyze periodic and aperiodic signals using frequency domain methods
- 理解频谱和功率谱的物理意义
  Understand the physical meaning of spectrum and power spectral density
- 掌握窗函数和短时傅里叶变换的应用
  Master window functions and Short-Time Fourier Transform (STFT)

物理背景 Physical Background:
傅里叶分析是信号处理和物理学的基础工具，其核心思想是：
任何周期函数都可以分解为不同频率正弦波的叠加。

傅里叶级数（周期函数）：
f(t) = a₀/2 + Σ[aₙcos(nωt) + bₙsin(nωt)]
其中 ω = 2π/T 是基频，n = 1,2,3... 是谐波次数

傅里叶变换（非周期函数）：
F(ω) = ∫f(t)·e^(-iωt)dt  （时域→频域）
f(t) = (1/2π)∫F(ω)·e^(iωt)dω  （频域→时域）

应用：
- 信号滤波与降噪
- 频谱分析（音频、振动）
- 图像处理
- 通信系统
- 量子力学（动量与位置表象转换）

HINT: 傅里叶级数: f(t) = Σ(an*cos(nωt) + bn*sin(nωt))
HINT: 傅里叶变换: F(ω) = ∫f(t)*e^(-iωt)dt
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import fft
import sys
sys.path.insert(0, str(__file__).rsplit('/', 3)[0])

# I AM NOT DONE

# =============================================================================
# 练习 2.1: 方波的傅里叶级数
# Exercise 2.1: Fourier Series of Square Wave
# =============================================================================
"""
物理背景：
方波是最常见的非正弦周期信号，在数字电路中广泛存在。
方波的傅里叶展开揭示了一个重要特性：只包含奇次谐波。

理想方波（振幅为1，周期为T）的傅里叶级数：
f(t) = (4/π) × [sin(ωt) + (1/3)sin(3ωt) + (1/5)sin(5ωt) + ...]
     = (4/π) × Σ(1/n)sin(nωt)，n = 1, 3, 5, ...

物理解释：
- 方波的对称性使得所有偶次谐波系数为零
- 高次谐波振幅按 1/n 衰减
- 方波的尖锐边缘需要无穷多高频分量来构建
- 吉布斯现象：有限项求和在边缘处出现过冲

应用：在电子学中，方波的频谱特性用于分析数字信号的带宽需求。
"""
def square_wave_fourier(t, omega, n_terms=10):
    """
    用傅里叶级数近似方波
    Approximate square wave using Fourier series

    参数 Parameters:
    - t: 时间数组 Time array (s)
    - omega: 基频角频率 Fundamental angular frequency (rad/s)，ω = 2π/T
    - n_terms: 使用的谐波项数 Number of harmonic terms

    返回 Returns:
    - result: 方波近似值 Approximation of square wave

    公式 Formula: f(t) = (4/π) × Σ(1/n)sin(nωt)，n = 1, 3, 5, ...
    注意：只包含奇数次谐波（n = 1, 3, 5, ...）
    """
    result = np.zeros_like(t)
    # TODO: 计算傅里叶级数前 n_terms 个奇次谐波项
    # TODO: Calculate first n_terms odd harmonics
    for n in range(1, 2*n_terms, 2):  # n = 1, 3, 5, ... 只取奇数
        result += (4 / np.pi) * (1 / n) * np.sin(n * omega * t)  # 修改这里
    return result


# =============================================================================
# 练习 2.2: 三角波的傅里叶级数
# Exercise 2.2: Fourier Series of Triangle Wave
# =============================================================================
"""
物理背景：
三角波是另一种常见的周期信号，其波形由直线段构成。
与方波相比，三角波的傅里叶级数收敛更快（高频分量衰减更快）。

三角波（振幅为1，周期为T）的傅里叶级数：
f(t) = (8/π²) × [sin(ωt) - (1/9)sin(3ωt) + (1/25)sin(5ωt) - ...]
     = (8/π²) × Σ((-1)^((n-1)/2)/n²)sin(nωt)，n = 1, 3, 5, ...

关键特点：
- 只有奇次谐波（与方波相同）
- 振幅按 1/n² 衰减（比方波的 1/n 衰减更快）
- 相邻奇次谐波符号交替（+, -, +, -...）
- 三角波的尖角需要较少高频分量，因为斜率有限

快速收敛意味着三角波可以用较少的谐波项近似。
"""
def triangle_wave_fourier(t, omega, n_terms=10):
    """
    用傅里叶级数近似三角波
    Approximate triangle wave using Fourier series

    参数 Parameters:
    - t: 时间数组 Time array (s)
    - omega: 基频角频率 Fundamental angular frequency (rad/s)
    - n_terms: 使用的谐波项数 Number of harmonic terms

    返回 Returns:
    - result: 三角波近似值 Approximation of triangle wave

    公式 Formula: f(t) = (8/π²) × Σ((-1)^i/n²)sin(nωt)
    其中 n = 1, 3, 5, ...（奇数），i = 0, 1, 2, ...（谐波索引）
    """
    result = np.zeros_like(t)
    # TODO: 计算傅里叶级数，注意符号交替和 1/n² 衰减
    # TODO: Calculate Fourier series with alternating signs and 1/n² decay
    for i, n in enumerate(range(1, 2*n_terms, 2)):
        sign = (-1)**i  # 交替符号 Alternating sign: +1, -1, +1, -1, ...
        result += (8 / np.pi**2) * (sign / n**2) * np.sin(n * omega * t)  # 修改这里
    return result


# =============================================================================
# 练习 2.3: 离散傅里叶变换 (DFT)
# Exercise 2.3: Discrete Fourier Transform
# =============================================================================
"""
物理背景：
离散傅里叶变换（DFT）是对采样信号进行频谱分析的基本工具。
快速傅里叶变换（FFT）是 DFT 的高效算法，复杂度从 O(N²) 降到 O(N·log N)。

DFT 的定义：
X[k] = Σ x[n]·e^(-i·2πkn/N)，n = 0, 1, ..., N-1

频率分辨率：
Δf = fs/N = 1/T
其中 fs 是采样率，N 是采样点数，T 是采样时长

奈奎斯特定理：
采样率 fs 必须大于信号最高频率的两倍，否则会产生混叠（aliasing）。
可分辨的最高频率：f_max = fs/2（奈奎斯特频率）

振幅谱的归一化：
单边振幅谱 = |X[k]| × 2/N（对于 k > 0）
直流分量（k=0）不需要乘2
"""
def compute_spectrum(signal, sample_rate):
    """
    计算信号的振幅频谱
    Compute amplitude spectrum of a signal

    参数 Parameters:
    - signal: 时域信号数组 Time-domain signal array
    - sample_rate: 采样率 Sampling rate (Hz)

    返回 Returns:
    - freqs_positive: 正频率数组 Positive frequency array (Hz)
    - amplitude: 归一化振幅谱 Normalized amplitude spectrum

    说明：返回单边频谱（只有正频率部分），振幅已归一化
    """
    n = len(signal)
    # TODO: 使用 FFT 计算频谱
    # TODO: Use FFT to compute spectrum
    # 使用 scipy.fft.fft 或 numpy.fft.fft
    spectrum = fft.fft(signal)  # 修改这里

    # 计算频率轴（FFT 输出的频率对应）
    # fftfreq 返回 [0, 1/N, 2/N, ..., (N/2-1)/N, -N/2/N, ..., -1/N] × fs
    freqs = fft.fftfreq(n, 1/sample_rate)

    # 取正频率部分的振幅（单边频谱）
    positive_mask = freqs >= 0
    freqs_positive = freqs[positive_mask]
    # 归一化：除以 N 得到真实振幅，乘以 2 补偿单边化（因为能量一半在负频率）
    amplitude = np.abs(spectrum[positive_mask]) * 2 / n

    return freqs_positive, amplitude


# 生成测试信号：多个正弦波叠加
# Generate test signal: superposition of multiple sine waves
sample_rate = 1000  # 采样率 Sampling rate (Hz)
t_signal = np.linspace(0, 1, sample_rate, endpoint=False)  # 1秒的采样时间

# 信号 = 50Hz(振幅1) + 120Hz(振幅0.5) + 300Hz(振幅0.3)
# Signal = 50Hz(amplitude 1) + 120Hz(amplitude 0.5) + 300Hz(amplitude 0.3)
signal_test = (1.0 * np.sin(2 * np.pi * 50 * t_signal) +
               0.5 * np.sin(2 * np.pi * 120 * t_signal) +
               0.3 * np.sin(2 * np.pi * 300 * t_signal))

freqs_test, amp_test = compute_spectrum(signal_test, sample_rate)


# =============================================================================
# 练习 2.4: 窗函数
# Exercise 2.4: Window Functions
# =============================================================================
"""
物理背景：
在对有限长信号进行 FFT 时，隐含假设信号是周期延拓的。
如果信号在窗口边界不连续，会产生频谱泄露（spectral leakage）。

窗函数的作用：
- 将信号在边缘平滑过渡到零，减少不连续性
- 代价是主瓣变宽（频率分辨率降低）和能量损失
- 不同窗函数在主瓣宽度和旁瓣抑制之间有不同权衡

常用窗函数：
1. 矩形窗（无窗）：最窄主瓣，但旁瓣最大
2. 汉宁窗（Hanning/Hann）：旁瓣衰减快，常用于频谱分析
3. 汉明窗（Hamming）：第一旁瓣抑制好，常用于滤波器设计
4. 布莱克曼窗（Blackman）：旁瓣最小，但主瓣最宽

选择原则：
- 需要高频率分辨率：用窄窗或矩形窗
- 需要抑制频率泄露：用汉宁/布莱克曼窗
"""
def hamming_window(N):
    """
    计算汉明窗
    Calculate Hamming window

    参数 Parameters:
    - N: 窗口长度 Window length (样本数)

    返回 Returns:
    - w: 窗函数数组 Window function array

    公式 Formula: w(n) = 0.54 - 0.46·cos(2πn/(N-1))
    特点：第一旁瓣约 -43dB，适合需要抑制近旁瓣的应用
    """
    n = np.arange(N)
    # TODO: 返回汉明窗，使用余弦公式
    # TODO: Return Hamming window using cosine formula
    return 0.54 - 0.46 * np.cos(2 * np.pi * n / (N - 1))  # 修改这里


def hanning_window(N):
    """
    计算汉宁窗（也称 Hann 窗）
    Calculate Hanning (Hann) window

    参数 Parameters:
    - N: 窗口长度 Window length (样本数)

    返回 Returns:
    - w: 窗函数数组 Window function array

    公式 Formula: w(n) = 0.5·(1 - cos(2πn/(N-1)))
    特点：边缘为零，旁瓣衰减快（-18dB/倍频程），是最常用的窗函数之一
    """
    n = np.arange(N)
    # TODO: 返回汉宁窗，使用余弦公式
    # TODO: Return Hanning window using cosine formula
    return 0.5 * (1 - np.cos(2 * np.pi * n / (N - 1)))  # 修改这里


# =============================================================================
# 练习 2.5: 短时傅里叶变换概念
# Exercise 2.5: Short-Time Fourier Transform Concept
# =============================================================================
"""
物理背景：
短时傅里叶变换（STFT）用于分析频率随时间变化的非平稳信号。
基本思想是将信号分成短时间窗口，对每个窗口分别做FFT。

STFT 定义：
X(t, f) = ∫ x(τ)·w(τ-t)·e^(-i2πfτ) dτ
其中 w 是窗函数，t 是时间中心

时频分辨率的不确定性原理（海森堡测不准原理的信号处理版本）：
Δt·Δf ≥ 1/(4π)
- 窗口越短，时间分辨率越好，但频率分辨率越差
- 窗口越长，频率分辨率越好，但时间分辨率越差

参数选择：
- window_size：窗口长度，影响频率分辨率 (Δf = fs/window_size)
- hop_size：窗口移动步长，影响时间分辨率和计算量
  通常取 hop_size = window_size/4 (75%重叠) 或 window_size/2 (50%重叠)

应用：语音识别、音乐分析、雷达信号处理、地震数据分析
"""
def simple_stft(signal, window_size, hop_size, sample_rate):
    """
    简化的短时傅里叶变换实现
    Simplified Short-Time Fourier Transform implementation

    参数 Parameters:
    - signal: 输入信号 Input signal
    - window_size: 窗口大小 Window size (样本数)
    - hop_size: 窗口移动步长 Hop size (样本数)
    - sample_rate: 采样率 Sample rate (Hz)

    返回 Returns:
    - times: 时间轴数组 Time axis array (s)
    - freqs: 频率轴数组 Frequency axis array (Hz)
    - spectrogram: 频谱图矩阵 Spectrogram matrix (|X(t,f)|)
    """
    # 计算窗口数量 Calculate number of windows
    n_windows = (len(signal) - window_size) // hop_size + 1
    # 使用汉明窗减少频谱泄露 Use Hamming window to reduce leakage
    window = hamming_window(window_size)

    # 频率轴（只取正频率部分）Frequency axis (positive frequencies only)
    freqs = fft.fftfreq(window_size, 1/sample_rate)[:window_size//2]
    # 时间轴（每个窗口中心时刻）Time axis (center of each window)
    times = np.arange(n_windows) * hop_size / sample_rate

    # 初始化频谱图矩阵 Initialize spectrogram matrix
    spectrogram = np.zeros((window_size // 2, n_windows))

    # 对每个时间窗口计算FFT Compute FFT for each time window
    for i in range(n_windows):
        start = i * hop_size
        # 提取窗口内信号并加窗 Extract windowed segment
        segment = signal[start:start + window_size] * window
        # 计算振幅谱 Compute magnitude spectrum
        spectrum = np.abs(fft.fft(segment))[:window_size // 2]
        spectrogram[:, i] = spectrum

    return times, freqs, spectrogram


# 创建一个 chirp 信号（频率随时间线性增加）
# Create a chirp signal (frequency increases linearly with time)
t_chirp = np.linspace(0, 2, 4000)  # 2秒，采样率2000Hz
# 频率从 50Hz 线性变化到 200Hz（线性调频信号）
# Linear FM: frequency sweeps from 50Hz to 200Hz
f_start, f_end = 50, 200
# 瞬时频率 f(t) = f_start + (f_end-f_start)/(2T) × t
# 相位 φ(t) = 2π∫f(t)dt = 2π[f_start×t + (f_end-f_start)/(4T)×t²]
chirp_signal = np.sin(2 * np.pi * (f_start * t_chirp +
                      (f_end - f_start) / 4 * t_chirp**2))


# =============================================================================
# 练习 2.6: 功率谱密度
# Exercise 2.6: Power Spectral Density
# =============================================================================
"""
物理背景：
功率谱密度（Power Spectral Density, PSD）描述信号功率在频率上的分布。
单位通常是 W/Hz 或 V²/Hz，表示单位频率带宽内的功率。

PSD 的定义：
S(f) = lim(T→∞) |X_T(f)|² / T
其中 X_T(f) 是有限时间 T 内信号的傅里叶变换

数值计算（周期图法）：
PSD ≈ |FFT|² / (N × fs)
其中 N 是采样点数，fs 是采样率

与振幅谱的关系：
- 振幅谱 |X(f)| 的单位是原信号单位（如 V）
- 功率谱 |X(f)|² 的单位是功率单位（如 V²）
- 功率谱密度归一化到单位频率带宽

Parseval 定理（能量守恒）：
时域总能量 = ∫|x(t)|²dt = ∫|X(f)|²df = 频域总能量

应用：噪声分析、振动测量、信号检测
"""
def compute_psd(signal, sample_rate):
    """
    计算功率谱密度（使用周期图法）
    Compute Power Spectral Density using periodogram method

    参数 Parameters:
    - signal: 输入信号 Input signal
    - sample_rate: 采样率 Sample rate (Hz)

    返回 Returns:
    - freqs: 正频率数组 Positive frequency array (Hz)
    - psd: 功率谱密度 Power spectral density (signal_unit²/Hz)

    公式 Formula: PSD = |FFT|² / (N × fs)
    """
    n = len(signal)
    spectrum = fft.fft(signal)
    # TODO: 计算功率谱密度
    # TODO: Compute power spectral density
    # |FFT|² 是功率谱，除以 N×fs 得到功率谱密度
    psd = np.abs(spectrum)**2 / (n * sample_rate)  # 修改这里

    # 取正频率部分 Take positive frequencies
    freqs = fft.fftfreq(n, 1/sample_rate)
    positive_mask = freqs >= 0

    return freqs[positive_mask], psd[positive_mask]


# 计算测试信号的 PSD
# Compute PSD of test signal
freqs_psd, psd_test = compute_psd(signal_test, sample_rate)


# =============================================================================
# 可视化
# =============================================================================
def plot_fourier():
    """绘制傅里叶分析结果"""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    omega = 2 * np.pi
    t = np.linspace(0, 2, 1000)

    # 1. 方波傅里叶级数收敛
    ax1 = axes[0, 0]
    for n in [1, 3, 10, 50]:
        y = square_wave_fourier(t, omega, n)
        ax1.plot(t, y, label=f'n={n}')
    ax1.set_xlabel('t')
    ax1.set_ylabel('f(t)')
    ax1.set_title('方波傅里叶级数收敛 Square Wave Convergence')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. 三角波傅里叶级数
    ax2 = axes[0, 1]
    for n in [1, 3, 10]:
        y = triangle_wave_fourier(t, omega, n)
        ax2.plot(t, y, label=f'n={n}')
    ax2.set_xlabel('t')
    ax2.set_ylabel('f(t)')
    ax2.set_title('三角波傅里叶级数 Triangle Wave')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. 频谱分析
    ax3 = axes[0, 2]
    ax3.stem(freqs_test[:200], amp_test[:200], linefmt='b-', markerfmt='bo', basefmt='k-')
    ax3.set_xlabel('Frequency (Hz)')
    ax3.set_ylabel('Amplitude')
    ax3.set_title('频谱 Frequency Spectrum')
    ax3.grid(True, alpha=0.3)

    # 4. 窗函数对比
    ax4 = axes[1, 0]
    N = 64
    ax4.plot(hamming_window(N), label='Hamming')
    ax4.plot(hanning_window(N), label='Hanning')
    ax4.plot(np.ones(N), '--', label='Rectangular')
    ax4.set_xlabel('Sample')
    ax4.set_ylabel('Amplitude')
    ax4.set_title('窗函数 Window Functions')
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    # 5. 频谱图 (STFT)
    ax5 = axes[1, 1]
    times_stft, freqs_stft, spectrogram = simple_stft(chirp_signal, 256, 64, 2000)
    ax5.pcolormesh(times_stft, freqs_stft, np.log10(spectrogram + 1e-10),
                   shading='auto', cmap='viridis')
    ax5.set_xlabel('Time (s)')
    ax5.set_ylabel('Frequency (Hz)')
    ax5.set_title('频谱图 (Chirp Signal) Spectrogram')

    # 6. 功率谱密度
    ax6 = axes[1, 2]
    ax6.semilogy(freqs_psd[:250], psd_test[:250])
    ax6.set_xlabel('Frequency (Hz)')
    ax6.set_ylabel('PSD')
    ax6.set_title('功率谱密度 Power Spectral Density')
    ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('fourier_analysis.png', dpi=150)
    print("图像已保存为 fourier_analysis.png")
    plt.show()


# =============================================================================
# 验证函数
# =============================================================================
def verify():
    """
    验证所有练习的正确性
    Verify all exercises
    """
    all_passed = True

    omega = 2 * np.pi  # 基频 1 Hz
    t_test = np.linspace(0, 1, 100)

    # 检查 2.1 - 方波傅里叶级数 Check square wave Fourier series
    y_square = square_wave_fourier(t_test, omega, n_terms=100)
    # 在 t = 0.25（四分之一周期处），方波应该接近 1
    expected_val = 1.0
    actual_val = y_square[25]  # t = 0.25
    if not np.isclose(actual_val, expected_val, atol=0.1):
        print("错误 2.1: 方波傅里叶级数计算错误，请检查公式 (4/π)×Σ(1/n)sin(nωt)")
        all_passed = False
    else:
        print("通过 2.1: 方波傅里叶级数正确")

    # 检查 2.2 - 三角波傅里叶级数 Check triangle wave
    y_tri = triangle_wave_fourier(t_test, omega, n_terms=100)
    if len(y_tri) != len(t_test):
        print("错误 2.2: 三角波输出数组长度与输入不匹配")
        all_passed = False
    else:
        print("通过 2.2: 三角波傅里叶级数正确")

    # 检查 2.3 - FFT 频谱分析 Check FFT spectrum analysis
    # 应该在 50, 120, 300 Hz 处找到峰值
    peak_indices = np.where(amp_test > 0.1)[0]
    peak_freqs = freqs_test[peak_indices]
    expected_peaks = [50, 120, 300]
    found_all = all(any(np.isclose(f, p, atol=5) for f in peak_freqs) for p in expected_peaks)
    if not found_all:
        print("错误 2.3: 频谱分析未能找到所有预期频率峰（应有 50, 120, 300 Hz）")
        all_passed = False
    else:
        print("通过 2.3: 频谱分析正确（检测到 50, 120, 300 Hz 频率分量）")

    # 检查 2.4 - 窗函数 Check window functions
    N = 64
    hamm = hamming_window(N)
    hann = hanning_window(N)
    # 窗函数应对称且最大值接近1
    if not (np.isclose(hamm[0], hamm[-1], atol=0.01) and
            np.isclose(hann[0], hann[-1], atol=0.01)):
        print("错误 2.4: 窗函数不满足对称性条件")
        all_passed = False
    elif not (0.9 < np.max(hamm) <= 1.0 and 0.9 < np.max(hann) <= 1.0):
        print("错误 2.4: 窗函数最大值应在 0.9 到 1.0 之间")
        all_passed = False
    else:
        print("通过 2.4: 窗函数（汉明窗和汉宁窗）正确")

    # 检查 2.5 - 短时傅里叶变换 Check STFT
    times_stft, freqs_stft, spectrogram = simple_stft(chirp_signal, 256, 64, 2000)
    if spectrogram.shape[1] < 10:
        print("错误 2.5: STFT 输出的频谱图窗口数过少")
        all_passed = False
    else:
        print("通过 2.5: 短时傅里叶变换正确")

    # 检查 2.6 - 功率谱密度 Check PSD
    if len(psd_test) != len(freqs_psd):
        print("错误 2.6: PSD 与频率数组长度不匹配")
        all_passed = False
    elif np.any(psd_test < 0):
        print("错误 2.6: 功率谱密度不应有负值（功率是非负量）")
        all_passed = False
    else:
        print("通过 2.6: 功率谱密度正确")

    if all_passed:
        print("\n全部测试通过！正在生成可视化图像...")
        print("All tests passed! Generating visualization...")
        try:
            plot_fourier()
        except Exception as e:
            print(f"可视化生成失败 Visualization failed: {e}")

    return all_passed


if __name__ == "__main__":
    print("=" * 50)
    print("傅里叶分析 Fourier Analysis")
    print("=" * 50)
    verify()
