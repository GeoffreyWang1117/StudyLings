/**
 * 练习 224: Unified Memory 性能分析与调优
 *
 * 学习目标：
 * - 对比 Unified Memory 与传统 cudaMemcpy 的性能
 * - 理解页面故障（Page Fault）对性能的影响
 * - 学习最佳实践和优化策略
 *
 * 任务：
 * 1. 实现三种内存管理方式：传统、UM 无优化、UM 优化
 * 2. 测量并对比性能
 * 3. 分析性能差异的原因
 */

#include <cuda_runtime.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error at %s:%d - %s\n", __FILE__, __LINE__, \
                    cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

__global__ void matrix_multiply(float *A, float *B, float *C, int N) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    if (row < N && col < N) {
        float sum = 0.0f;
        for (int k = 0; k < N; k++) {
            sum += A[row * N + k] * B[k * N + col];
        }
        C[row * N + col] = sum;
    }
}

// 方法 1: 传统 cudaMalloc + cudaMemcpy
float benchmark_traditional(int N) {
    size_t bytes = N * N * sizeof(float);

    // Host 分配
    float *h_A = (float*)malloc(bytes);
    float *h_B = (float*)malloc(bytes);
    float *h_C = (float*)malloc(bytes);

    // 初始化
    for (int i = 0; i < N * N; i++) {
        h_A[i] = 1.0f;
        h_B[i] = 2.0f;
    }

    // Device 分配
    float *d_A, *d_B, *d_C;
    CUDA_CHECK(cudaMalloc(&d_A, bytes));
    CUDA_CHECK(cudaMalloc(&d_B, bytes));
    CUDA_CHECK(cudaMalloc(&d_C, bytes));

    cudaEvent_t start, stop;
    CUDA_CHECK(cudaEventCreate(&start));
    CUDA_CHECK(cudaEventCreate(&stop));

    CUDA_CHECK(cudaEventRecord(start));

    // H2D 拷贝
    CUDA_CHECK(cudaMemcpy(d_A, h_A, bytes, cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_B, h_B, bytes, cudaMemcpyHostToDevice));

    // Kernel
    dim3 block(16, 16);
    dim3 grid((N + 15) / 16, (N + 15) / 16);
    matrix_multiply<<<grid, block>>>(d_A, d_B, d_C, N);

    // D2H 拷贝
    CUDA_CHECK(cudaMemcpy(h_C, d_C, bytes, cudaMemcpyDeviceToHost));

    CUDA_CHECK(cudaEventRecord(stop));
    CUDA_CHECK(cudaEventSynchronize(stop));

    float milliseconds = 0;
    CUDA_CHECK(cudaEventElapsedTime(&milliseconds, start, stop));

    // 清理
    free(h_A); free(h_B); free(h_C);
    CUDA_CHECK(cudaFree(d_A));
    CUDA_CHECK(cudaFree(d_B));
    CUDA_CHECK(cudaFree(d_C));
    CUDA_CHECK(cudaEventDestroy(start));
    CUDA_CHECK(cudaEventDestroy(stop));

    return milliseconds;
}

// 方法 2: Unified Memory (无优化)
float benchmark_um_naive(int N) {
    size_t bytes = N * N * sizeof(float);

    float *A, *B, *C;
    CUDA_CHECK(cudaMallocManaged(&A, bytes));
    CUDA_CHECK(cudaMallocManaged(&B, bytes));
    CUDA_CHECK(cudaMallocManaged(&C, bytes));

    // TODO 1: 初始化数据（CPU 端）
    for (int i = 0; i < N * N; i++) {
        A[i] = 1.0f;
        B[i] = 2.0f;
    }

    cudaEvent_t start, stop;
    CUDA_CHECK(cudaEventCreate(&start));
    CUDA_CHECK(cudaEventCreate(&stop));

    CUDA_CHECK(cudaEventRecord(start));

    // TODO 2: 直接启动 kernel（无预取）
    dim3 block(16, 16);
    dim3 grid((N + 15) / 16, (N + 15) / 16);
    // 提示：matrix_multiply<<<grid, block>>>(A, B, C, N);


    CUDA_CHECK(cudaDeviceSynchronize());

    // TODO 3: CPU 端访问结果
    float result = C[0];  // 触发页面迁移

    CUDA_CHECK(cudaEventRecord(stop));
    CUDA_CHECK(cudaEventSynchronize(stop));

    float milliseconds = 0;
    CUDA_CHECK(cudaEventElapsedTime(&milliseconds, start, stop));

    CUDA_CHECK(cudaFree(A));
    CUDA_CHECK(cudaFree(B));
    CUDA_CHECK(cudaFree(C));
    CUDA_CHECK(cudaEventDestroy(start));
    CUDA_CHECK(cudaEventDestroy(stop));

    return milliseconds;
}

// 方法 3: Unified Memory (优化版)
float benchmark_um_optimized(int N) {
    size_t bytes = N * N * sizeof(float);
    int device;
    CUDA_CHECK(cudaGetDevice(&device));

    float *A, *B, *C;
    CUDA_CHECK(cudaMallocManaged(&A, bytes));
    CUDA_CHECK(cudaMallocManaged(&B, bytes));
    CUDA_CHECK(cudaMallocManaged(&C, bytes));

    // 初始化数据
    for (int i = 0; i < N * N; i++) {
        A[i] = 1.0f;
        B[i] = 2.0f;
    }

    // TODO 4: 设置内存访问提示
    // 提示：cudaMemAdvise(A, bytes, cudaMemAdviseSetReadMostly, device);


    cudaEvent_t start, stop;
    CUDA_CHECK(cudaEventCreate(&start));
    CUDA_CHECK(cudaEventCreate(&stop));

    // TODO 5: 预取数据到 GPU
    // 提示：cudaMemPrefetchAsync(A, bytes, device);


    CUDA_CHECK(cudaEventRecord(start));

    dim3 block(16, 16);
    dim3 grid((N + 15) / 16, (N + 15) / 16);
    matrix_multiply<<<grid, block>>>(A, B, C, N);

    CUDA_CHECK(cudaDeviceSynchronize());

    // 预取结果回 CPU
    CUDA_CHECK(cudaMemPrefetchAsync(C, bytes, cudaCpuDeviceId));
    float result = C[0];

    CUDA_CHECK(cudaEventRecord(stop));
    CUDA_CHECK(cudaEventSynchronize(stop));

    float milliseconds = 0;
    CUDA_CHECK(cudaEventElapsedTime(&milliseconds, start, stop));

    CUDA_CHECK(cudaFree(A));
    CUDA_CHECK(cudaFree(B));
    CUDA_CHECK(cudaFree(C));
    CUDA_CHECK(cudaEventDestroy(start));
    CUDA_CHECK(cudaEventDestroy(stop));

    return milliseconds;
}

int main() {
    const int N = 1024;
    size_t bytes = N * N * sizeof(float);

    printf("=== Unified Memory 性能对比分析 ===\n");
    printf("矩阵规模: %d x %d (%.2f MB)\n\n", N, N, bytes / 1024.0f / 1024.0f);

    float time_traditional = benchmark_traditional(N);
    printf("1. 传统方式 (cudaMalloc + cudaMemcpy): %.3f ms\n", time_traditional);

    float time_um_naive = benchmark_um_naive(N);
    printf("2. Unified Memory (无优化):           %.3f ms  (%.2fx)\n",
           time_um_naive, time_um_naive / time_traditional);

    float time_um_optimized = benchmark_um_optimized(N);
    printf("3. Unified Memory (优化):             %.3f ms  (%.2fx)\n\n",
           time_um_optimized, time_um_optimized / time_traditional);

    printf("性能分析：\n");
    if (time_um_naive > time_traditional * 1.5) {
        printf("⚠ 无优化的 UM 较慢，原因：页面故障开销\n");
    }
    if (time_um_optimized < time_um_naive * 0.8) {
        printf("✓ 优化后的 UM 显著改善，预取消除了页面故障\n");
    }

    printf("\n最佳实践：\n");
    printf("1. ✓ 使用 cudaMemPrefetchAsync() 提前迁移数据\n");
    printf("2. ✓ 使用 cudaMemAdvise() 提示访问模式\n");
    printf("3. ✓ 对只读数据使用 cudaMemAdviseSetReadMostly\n");
    printf("4. ✓ 合理规划 CPU-GPU 访问顺序\n");
    printf("5. ⚠ 避免频繁的 CPU-GPU 交替访问\n");

    return 0;
}

/**
 * 编译命令：
 * nvcc -o um_performance 04_um_performance.cu
 *
 * 知识点：
 * 1. Unified Memory 简化编程但可能影响性能
 * 2. 页面故障是主要性能瓶颈
 * 3. 预取和内存提示可以消除页面故障
 * 4. 优化后的 UM 性能接近甚至超过传统方式
 * 5. Pascal+ 架构支持按需页面迁移
 */
