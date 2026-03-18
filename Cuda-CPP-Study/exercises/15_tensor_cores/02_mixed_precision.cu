// 练习 152: 混合精度矩阵乘法
//
// 目标: 使用 FP16/FP32 混合精度加速训练
//
// 任务:
// 1. 实现 FP16 输入 + FP32 累加
// 2. 比较性能差异
// 3. 理解精度权衡

#include <stdio.h>
#include <cuda_runtime.h>
#include <mma.h>
#include <time.h>

using namespace nvcuda;

#define MATRIX_M 256
#define MATRIX_N 256
#define MATRIX_K 256

#define WMMA_M 16
#define WMMA_N 16
#define WMMA_K 16

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

double get_time() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

// TODO: 实现混合精度矩阵乘法
// 输入: FP16, 累加: FP32, 输出: FP32
__global__ void mixed_precision_matmul(
    half *A, half *B, float *C,
    int M, int N, int K) {

    // TODO: 使用 WMMA API
    // 1. 声明 fragments
    // 2. 遍历 K 维度进行分块
    // 3. 累加结果
}

// 传统 FP32 矩阵乘法（用于对比）
__global__ void fp32_matmul(float *A, float *B, float *C, int M, int N, int K) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    if (row < M && col < N) {
        float sum = 0.0f;
        for (int k = 0; k < K; k++) {
            sum += A[row * K + k] * B[k * N + col];
        }
        C[row * N + col] = sum;
    }
}

int main() {
    cudaDeviceProp prop;
    CUDA_CHECK(cudaGetDeviceProperties(&prop, 0));

    if (prop.major < 7) {
        printf("需要 Compute Capability >= 7.0 支持 Tensor Core\n");
        printf("TEST_PASSED\n");
        return 0;
    }

    printf("使用 %s 进行混合精度测试\n\n", prop.name);

    // 分配内存
    size_t size_A = MATRIX_M * MATRIX_K * sizeof(half);
    size_t size_B = MATRIX_K * MATRIX_N * sizeof(half);
    size_t size_C = MATRIX_M * MATRIX_N * sizeof(float);

    half *h_A = (half*)malloc(size_A);
    half *h_B = (half*)malloc(size_B);
    float *h_C = (float*)malloc(size_C);

    // 初始化
    for (int i = 0; i < MATRIX_M * MATRIX_K; i++) {
        h_A[i] = __float2half((float)rand() / RAND_MAX);
    }
    for (int i = 0; i < MATRIX_K * MATRIX_N; i++) {
        h_B[i] = __float2half((float)rand() / RAND_MAX);
    }

    half *d_A, *d_B;
    float *d_C;
    CUDA_CHECK(cudaMalloc(&d_A, size_A));
    CUDA_CHECK(cudaMalloc(&d_B, size_B));
    CUDA_CHECK(cudaMalloc(&d_C, size_C));

    CUDA_CHECK(cudaMemcpy(d_A, h_A, size_A, cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_B, h_B, size_B, cudaMemcpyHostToDevice));

    // 测试 Tensor Core 性能
    dim3 blockDim(32, 4);
    dim3 gridDim((MATRIX_N + WMMA_N - 1) / WMMA_N,
                 (MATRIX_M + WMMA_M - 1) / WMMA_M);

    double start = get_time();
    mixed_precision_matmul<<<gridDim, blockDim>>>(d_A, d_B, d_C, MATRIX_M, MATRIX_N, MATRIX_K);
    CUDA_CHECK(cudaDeviceSynchronize());
    double tc_time = get_time() - start;

    CUDA_CHECK(cudaMemcpy(h_C, d_C, size_C, cudaMemcpyDeviceToHost));

    printf("Tensor Core (混合精度) 时间: %.3f ms\n", tc_time * 1000);
    printf("吞吐量: %.2f TFLOPS\n",
           (2.0 * MATRIX_M * MATRIX_N * MATRIX_K) / (tc_time * 1e12));

    CUDA_CHECK(cudaFree(d_A));
    CUDA_CHECK(cudaFree(d_B));
    CUDA_CHECK(cudaFree(d_C));
    free(h_A);
    free(h_B);
    free(h_C);

    printf("\n混合精度加速演示完成!\n");
    printf("TEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
