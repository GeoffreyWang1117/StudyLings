/**
 * 练习 222: Unified Memory 预取优化
 *
 * 学习目标：
 * - 使用 cudaMemPrefetchAsync() 进行数据预取
 * - 理解预取对性能的影响
 * - 学习 cudaMemAdvise() 提示系统优化策略
 *
 * 任务：
 * 1. 对比有无预取的性能差异
 * 2. 使用 cudaMemPrefetchAsync() 提前迁移数据
 * 3. 使用 cudaMemAdvise() 设置内存访问提示
 * 4. 测量并对比执行时间
 */

#include <cuda_runtime.h>
#include <stdio.h>
#include <stdlib.h>

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error at %s:%d - %s\n", __FILE__, __LINE__, \
                    cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

__global__ void compute_intensive(float *data, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        // 计算密集型操作
        float value = data[idx];
        for (int i = 0; i < 100; i++) {
            value = sqrtf(value * value + 1.0f);
        }
        data[idx] = value;
    }
}

float benchmark_no_prefetch(float *data, int n) {
    int threadsPerBlock = 256;
    int blocksPerGrid = (n + threadsPerBlock - 1) / threadsPerBlock;

    cudaEvent_t start, stop;
    CUDA_CHECK(cudaEventCreate(&start));
    CUDA_CHECK(cudaEventCreate(&stop));

    CUDA_CHECK(cudaEventRecord(start));
    compute_intensive<<<blocksPerGrid, threadsPerBlock>>>(data, n);
    CUDA_CHECK(cudaEventRecord(stop));
    CUDA_CHECK(cudaEventSynchronize(stop));

    float milliseconds = 0;
    CUDA_CHECK(cudaEventElapsedTime(&milliseconds, start, stop));

    CUDA_CHECK(cudaEventDestroy(start));
    CUDA_CHECK(cudaEventDestroy(stop));

    return milliseconds;
}

float benchmark_with_prefetch(float *data, int n, int device) {
    int threadsPerBlock = 256;
    int blocksPerGrid = (n + threadsPerBlock - 1) / threadsPerBlock;

    // TODO 1: 使用 cudaMemPrefetchAsync() 预取数据到 GPU
    // 提示：cudaMemPrefetchAsync(data, n * sizeof(float), device, 0);


    cudaEvent_t start, stop;
    CUDA_CHECK(cudaEventCreate(&start));
    CUDA_CHECK(cudaEventCreate(&stop));

    CUDA_CHECK(cudaEventRecord(start));
    compute_intensive<<<blocksPerGrid, threadsPerBlock>>>(data, n);
    CUDA_CHECK(cudaEventRecord(stop));
    CUDA_CHECK(cudaEventSynchronize(stop));

    float milliseconds = 0;
    CUDA_CHECK(cudaEventElapsedTime(&milliseconds, start, stop));

    CUDA_CHECK(cudaEventDestroy(start));
    CUDA_CHECK(cudaEventDestroy(stop));

    return milliseconds;
}

float benchmark_with_advise(float *data, int n, int device) {
    // TODO 2: 使用 cudaMemAdvise() 设置访问提示
    // 提示 1: cudaMemAdvise(data, n * sizeof(float),
    //                        cudaMemAdviseSetReadMostly, device);
    // 提示 2: cudaMemAdvise(data, n * sizeof(float),
    //                        cudaMemAdviseSetPreferredLocation, device);


    int threadsPerBlock = 256;
    int blocksPerGrid = (n + threadsPerBlock - 1) / threadsPerBlock;

    CUDA_CHECK(cudaMemPrefetchAsync(data, n * sizeof(float), device, 0));

    cudaEvent_t start, stop;
    CUDA_CHECK(cudaEventCreate(&start));
    CUDA_CHECK(cudaEventCreate(&stop));

    CUDA_CHECK(cudaEventRecord(start));
    compute_intensive<<<blocksPerGrid, threadsPerBlock>>>(data, n);
    CUDA_CHECK(cudaEventRecord(stop));
    CUDA_CHECK(cudaEventSynchronize(stop));

    float milliseconds = 0;
    CUDA_CHECK(cudaEventElapsedTime(&milliseconds, start, stop));

    CUDA_CHECK(cudaEventDestroy(start));
    CUDA_CHECK(cudaEventDestroy(stop));

    return milliseconds;
}

int main() {
    const int N = 1 << 24;  // 16M elements
    size_t bytes = N * sizeof(float);

    int device;
    CUDA_CHECK(cudaGetDevice(&device));

    // 分配统一内存
    float *data;
    CUDA_CHECK(cudaMallocManaged(&data, bytes));

    // 初始化数据
    for (int i = 0; i < N; i++) {
        data[i] = 1.0f;
    }

    printf("=== Unified Memory 预取性能对比 ===\n");
    printf("数据规模: %d elements (%.2f MB)\n\n", N, bytes / 1024.0f / 1024.0f);

    // TODO 3: 运行三种基准测试并对比
    float time_no_prefetch = benchmark_no_prefetch(data, n);
    printf("1. 无预取:        %.3f ms\n", time_no_prefetch);

    float time_with_prefetch = benchmark_with_prefetch(data, n, device);
    printf("2. 使用预取:      %.3f ms  (加速 %.2fx)\n",
           time_with_prefetch, time_no_prefetch / time_with_prefetch);

    float time_with_advise = benchmark_with_advise(data, n, device);
    printf("3. 预取+内存提示: %.3f ms  (加速 %.2fx)\n\n",
           time_with_advise, time_no_prefetch / time_with_advise);

    printf("优化建议：\n");
    printf("✓ 使用 cudaMemPrefetchAsync() 提前迁移数据\n");
    printf("✓ 使用 cudaMemAdvise() 告诉驱动访问模式\n");
    printf("✓ cudaMemAdviseSetReadMostly: 只读数据\n");
    printf("✓ cudaMemAdviseSetPreferredLocation: 设置首选位置\n");
    printf("✓ cudaMemAdviseSetAccessedBy: 指定访问设备\n");

    CUDA_CHECK(cudaFree(data));

    return 0;
}

/**
 * 编译命令：
 * nvcc -o um_prefetch 02_um_prefetch.cu
 *
 * 知识点：
 * 1. cudaMemPrefetchAsync() - 异步预取数据
 * 2. cudaMemAdvise() - 提供内存访问提示
 * 3. 预取可显著减少首次访问延迟
 * 4. 内存提示帮助驱动做出更好的优化决策
 * 5. 在 Pascal+ 架构上效果最佳
 */
