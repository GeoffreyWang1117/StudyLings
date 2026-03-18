// 练习 191: cuBLAS 基础 - 矩阵乘法
//
// 目标: 使用 cuBLAS 库进行高性能线性代数运算
//
// 任务:
// 1. 初始化 cuBLAS 库
// 2. 使用 cublasSgemm 执行矩阵乘法
// 3. 对比手写 kernel 的性能
//
// 编译: nvcc -o cublas_demo 01_cublas_basics.cu -lcublas
//
// cuBLAS 是 CUDA 提供的线性代数库，高度优化，通常比手写 kernel 快

#include <stdio.h>
#include <cuda_runtime.h>
#include <cublas_v2.h>
#include <time.h>

#define M 1024
#define N 1024
#define K 1024

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

#define CUBLAS_CHECK(call) \
    do { \
        cublasStatus_t status = call; \
        if (status != CUBLAS_STATUS_SUCCESS) { \
            fprintf(stderr, "cuBLAS Error: %d\n", status); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

double get_time() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

// 简单的手写矩阵乘法 kernel (未优化)
__global__ void naive_gemm(float *A, float *B, float *C, int M, int N, int K) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    if (row < M && col < N) {
        float sum = 0.0f;
        for (int i = 0; i < K; i++) {
            sum += A[row * K + i] * B[i * N + col];
        }
        C[row * N + col] = sum;
    }
}

int main() {
    printf("cuBLAS 基础: 矩阵乘法\n");
    printf("矩阵大小: %d x %d x %d\n\n", M, K, N);

    // 分配主机内存
    float *h_A = (float*)malloc(M * K * sizeof(float));
    float *h_B = (float*)malloc(K * N * sizeof(float));
    float *h_C = (float*)malloc(M * N * sizeof(float));

    // 初始化矩阵
    for (int i = 0; i < M * K; i++) h_A[i] = (float)(rand() % 100) / 100.0f;
    for (int i = 0; i < K * N; i++) h_B[i] = (float)(rand() % 100) / 100.0f;

    // 分配设备内存
    float *d_A, *d_B, *d_C;
    CUDA_CHECK(cudaMalloc(&d_A, M * K * sizeof(float)));
    CUDA_CHECK(cudaMalloc(&d_B, K * N * sizeof(float)));
    CUDA_CHECK(cudaMalloc(&d_C, M * N * sizeof(float)));

    CUDA_CHECK(cudaMemcpy(d_A, h_A, M * K * sizeof(float), cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_B, h_B, K * N * sizeof(float), cudaMemcpyHostToDevice));

    // TODO: 方法 1 - 使用 cuBLAS
    printf("方法 1: cuBLAS\n");

    // 1. 创建 cuBLAS handle
    cublasHandle_t handle;
    // CUBLAS_CHECK(cublasCreate(&handle));

    // 2. 定义标量参数
    float alpha = 1.0f;
    float beta = 0.0f;

    // 3. 调用 cublasSgemm 执行矩阵乘法
    // C = alpha * A * B + beta * C
    // 注意: cuBLAS 使用列主序 (column-major)，需要转置
    // TODO: 实现 cublasSgemm 调用
    // CUBLAS_CHECK(cublasSgemm(handle,
    //     CUBLAS_OP_N, CUBLAS_OP_N,
    //     N, M, K,
    //     &alpha,
    //     d_B, N,
    //     d_A, K,
    //     &beta,
    //     d_C, N));

    double start = get_time();
    // cublasSgemm(...);  // 重复调用测试性能
    CUDA_CHECK(cudaDeviceSynchronize());
    double cublas_time = get_time() - start;

    // printf("cuBLAS 时间: %.3f ms\n", cublas_time * 1000);

    // 方法 2: 手写 kernel
    printf("\n方法 2: 简单 kernel\n");
    dim3 blockDim(16, 16);
    dim3 gridDim((N + 15) / 16, (M + 15) / 16);

    start = get_time();
    naive_gemm<<<gridDim, blockDim>>>(d_A, d_B, d_C, M, N, K);
    CUDA_CHECK(cudaDeviceSynchronize());
    double naive_time = get_time() - start;

    printf("手写 kernel 时间: %.3f ms\n", naive_time * 1000);
    printf("加速比: %.2fx\n", naive_time / cublas_time);

    // 计算性能指标
    double flops = 2.0 * M * N * K;  // 矩阵乘法的浮点操作数
    // double gflops = flops / (cublas_time * 1e9);
    // printf("cuBLAS 性能: %.2f GFLOPS\n", gflops);

    // 清理
    // CUBLAS_CHECK(cublasDestroy(handle));
    CUDA_CHECK(cudaFree(d_A));
    CUDA_CHECK(cudaFree(d_B));
    CUDA_CHECK(cudaFree(d_C));
    free(h_A);
    free(h_B);
    free(h_C);

    printf("\ncuBLAS 矩阵乘法完成!\n");
    printf("TEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
