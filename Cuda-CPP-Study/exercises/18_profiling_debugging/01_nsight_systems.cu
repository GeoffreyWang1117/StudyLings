// 练习 181: Nsight Systems 系统级性能分析
//
// 目标: 使用 Nsight Systems 分析程序性能
//
// 任务:
// 1. 学习使用 nsys 命令行工具
// 2. 分析 CPU/GPU 时间线
// 3. 识别性能瓶颈
//
// 使用方法:
// 1. 编译程序: nvcc -o nsight_demo 01_nsight_systems.cu
// 2. 运行分析: nsys profile --stats=true ./nsight_demo
// 3. 查看报告: nsys-ui report1.nsys-rep (或使用命令行查看统计)
//
// 重点观察:
// - Kernel 执行时间
// - 内存传输时间
// - CPU/GPU 空闲时间
// - Stream 并发情况

#include <stdio.h>
#include <cuda_runtime.h>

#define N (1 << 20)  // 1M elements
#define BLOCK_SIZE 256

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// 一个简单的 kernel（故意未优化）
__global__ void inefficient_kernel(float *data, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        // 多次内存访问（非合并）
        for (int i = 0; i < 100; i++) {
            data[idx] = data[idx] * 1.01f;
        }
    }
}

// 优化后的 kernel
__global__ void optimized_kernel(float *data, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        float val = data[idx];
        // 减少内存访问
        for (int i = 0; i < 100; i++) {
            val = val * 1.01f;
        }
        data[idx] = val;
    }
}

// TODO: 添加一些故意的性能问题，让学生通过 Nsight Systems 发现
void problematic_code() {
    float *d_data;
    CUDA_CHECK(cudaMalloc(&d_data, N * sizeof(float)));

    dim3 blockDim(BLOCK_SIZE);
    dim3 gridDim((N + BLOCK_SIZE - 1) / BLOCK_SIZE);

    // 问题 1: 同步的内存传输（阻塞）
    float *h_data = (float*)malloc(N * sizeof(float));
    for (int i = 0; i < N; i++) h_data[i] = 1.0f;

    // TODO: 这里使用同步传输，会阻塞 CPU
    // 观察: Nsight Systems 会显示 CPU 等待
    CUDA_CHECK(cudaMemcpy(d_data, h_data, N * sizeof(float), cudaMemcpyHostToDevice));

    // 问题 2: Kernel 启动没有并发
    inefficient_kernel<<<gridDim, blockDim>>>(d_data, N);
    CUDA_CHECK(cudaDeviceSynchronize());

    // 问题 3: 同步传输回主机
    CUDA_CHECK(cudaMemcpy(h_data, d_data, N * sizeof(float), cudaMemcpyDeviceToHost));

    CUDA_CHECK(cudaFree(d_data));
    free(h_data);
}

// TODO: 改进版本 - 使用异步操作和流
void improved_code() {
    float *d_data;
    CUDA_CHECK(cudaMalloc(&d_data, N * sizeof(float)));

    // 使用 pinned memory 支持异步传输
    float *h_data;
    CUDA_CHECK(cudaMallocHost(&h_data, N * sizeof(float)));
    for (int i = 0; i < N; i++) h_data[i] = 1.0f;

    cudaStream_t stream;
    CUDA_CHECK(cudaStreamCreate(&stream));

    dim3 blockDim(BLOCK_SIZE);
    dim3 gridDim((N + BLOCK_SIZE - 1) / BLOCK_SIZE);

    // 异步传输和执行
    // CUDA_CHECK(cudaMemcpyAsync(d_data, h_data, N * sizeof(float),
    //                            cudaMemcpyHostToDevice, stream));
    // optimized_kernel<<<gridDim, blockDim, 0, stream>>>(d_data, N);
    // CUDA_CHECK(cudaMemcpyAsync(h_data, d_data, N * sizeof(float),
    //                            cudaMemcpyDeviceToHost, stream));

    CUDA_CHECK(cudaStreamSynchronize(stream));
    CUDA_CHECK(cudaStreamDestroy(stream));

    CUDA_CHECK(cudaFreeHost(h_data));
    CUDA_CHECK(cudaFree(d_data));
}

int main() {
    printf("Nsight Systems 性能分析示例\n");
    printf("=========================================\n\n");

    printf("运行问题代码...\n");
    problematic_code();

    printf("运行改进代码...\n");
    // improved_code();

    printf("\n分析步骤:\n");
    printf("1. 使用以下命令运行分析:\n");
    printf("   nsys profile --stats=true -o report ./nsight_demo\n\n");
    printf("2. 观察以下指标:\n");
    printf("   - CUDA API 调用时间\n");
    printf("   - Kernel 执行时间\n");
    printf("   - 内存传输时间\n");
    printf("   - CPU/GPU 利用率\n\n");
    printf("3. 在 GUI 中查看时间线:\n");
    printf("   nsys-ui report.nsys-rep\n\n");

    printf("TEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
