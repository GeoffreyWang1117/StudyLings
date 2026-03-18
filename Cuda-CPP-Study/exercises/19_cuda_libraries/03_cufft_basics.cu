// 练习 193: cuFFT 基础 - 快速傅里叶变换
//
// 目标: 使用 cuFFT 库进行频域分析
//
// 任务:
// 1. 使用 cuFFT 执行 1D FFT
// 2. 频域滤波（低通滤波器）
// 3. 逆变换回时域
//
// 编译: nvcc -o cufft_demo 03_cufft_basics.cu -lcufft
//
// FFT 在信号处理、图像处理、科学计算中广泛应用

#include <stdio.h>
#include <cuda_runtime.h>
#include <cufft.h>
#include <math.h>

#define N 1024
#define PI 3.14159265358979323846

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

#define CUFFT_CHECK(call) \
    do { \
        cufftResult result = call; \
        if (result != CUFFT_SUCCESS) { \
            fprintf(stderr, "cuFFT Error: %d\n", result); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// 生成测试信号: 正弦波 + 噪声
void generate_signal(float *signal, int n) {
    for (int i = 0; i < n; i++) {
        float t = (float)i / n;
        // 低频信号 (10 Hz) + 高频噪声 (100 Hz)
        signal[i] = sinf(2.0f * PI * 10.0f * t) +
                    0.5f * sinf(2.0f * PI * 100.0f * t);
    }
}

// 低通滤波器: 保留低频，去除高频
__global__ void lowpass_filter(cufftComplex *data, int n, float cutoff) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        // 频率索引
        int freq = (idx < n/2) ? idx : (n - idx);
        float normalized_freq = (float)freq / n;

        // 如果频率高于截止频率，置零
        if (normalized_freq > cutoff) {
            data[idx].x = 0.0f;
            data[idx].y = 0.0f;
        }
    }
}

int main() {
    printf("cuFFT 基础: 快速傅里叶变换\n");
    printf("信号长度: %d\n\n", N);

    // 分配主机内存
    float *h_signal = (float*)malloc(N * sizeof(float));
    cufftComplex *h_spectrum = (cufftComplex*)malloc(N * sizeof(cufftComplex));

    // 生成测试信号
    generate_signal(h_signal, N);

    printf("原始信号样本 (前5个): ");
    for (int i = 0; i < 5; i++) {
        printf("%.3f ", h_signal[i]);
    }
    printf("\n\n");

    // TODO: 分配设备内存
    cufftComplex *d_signal;
    // CUDA_CHECK(cudaMalloc(&d_signal, N * sizeof(cufftComplex)));

    // 将实数信号转换为复数（虚部为0）
    cufftComplex *h_complex = (cufftComplex*)malloc(N * sizeof(cufftComplex));
    for (int i = 0; i < N; i++) {
        h_complex[i].x = h_signal[i];
        h_complex[i].y = 0.0f;
    }

    // CUDA_CHECK(cudaMemcpy(d_signal, h_complex, N * sizeof(cufftComplex),
    //                       cudaMemcpyHostToDevice));

    // TODO: 1. 创建 cuFFT 计划
    printf("步骤 1: 创建 FFT 计划\n");
    cufftHandle plan;
    // CUFFT_CHECK(cufftPlan1d(&plan, N, CUFFT_C2C, 1));

    // TODO: 2. 执行正向 FFT (时域 -> 频域)
    printf("步骤 2: 执行正向 FFT\n");
    // CUFFT_CHECK(cufftExecC2C(plan, d_signal, d_signal, CUFFT_FORWARD));

    // TODO: 3. 在频域应用低通滤波器
    printf("步骤 3: 应用低通滤波器 (截止频率: 0.05)\n");
    int blockSize = 256;
    int gridSize = (N + blockSize - 1) / blockSize;
    // lowpass_filter<<<gridSize, blockSize>>>(d_signal, N, 0.05f);
    CUDA_CHECK(cudaDeviceSynchronize());

    // TODO: 4. 执行逆向 FFT (频域 -> 时域)
    printf("步骤 4: 执行逆向 FFT\n");
    // CUFFT_CHECK(cufftExecC2C(plan, d_signal, d_signal, CUFFT_INVERSE));

    // 复制回主机
    // CUDA_CHECK(cudaMemcpy(h_spectrum, d_signal, N * sizeof(cufftComplex),
    //                       cudaMemcpyDeviceToHost));

    // 归一化（cuFFT 的逆变换不自动归一化）
    // for (int i = 0; i < N; i++) {
    //     h_spectrum[i].x /= N;
    //     h_spectrum[i].y /= N;
    // }

    printf("\n滤波后信号样本 (前5个): ");
    for (int i = 0; i < 5; i++) {
        printf("%.3f ", h_spectrum[i].x);
    }
    printf("\n\n");

    // 对比原始信号和滤波信号
    printf("对比结果:\n");
    printf("  原始信号包含: 低频(10Hz) + 高频噪声(100Hz)\n");
    printf("  滤波后信号: 仅保留低频分量\n");

    // TODO: 清理
    // CUFFT_CHECK(cufftDestroy(plan));
    // CUDA_CHECK(cudaFree(d_signal));

    free(h_signal);
    free(h_complex);
    free(h_spectrum);

    printf("\ncuFFT 测试完成!\n");
    printf("TEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
