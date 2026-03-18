// 练习 153: Tensor Core GEMM 优化
//
// 目标: 优化大规模矩阵乘法性能
//
// 任务:
// 1. 使用 Tensor Core 实现高性能 GEMM
// 2. 优化 tile 大小和 warp 布局
// 3. 达到接近理论峰值性能

#include <stdio.h>
#include <cuda_runtime.h>
#include <mma.h>
#include <time.h>

using namespace nvcuda;

#define MATRIX_M 4096
#define MATRIX_N 4096
#define MATRIX_K 4096

#define WMMA_M 16
#define WMMA_N 16
#define WMMA_K 16

// Tile 配置
#define BLOCK_M 128
#define BLOCK_N 128
#define BLOCK_K 32

#define WARP_M (BLOCK_M / WMMA_M)
#define WARP_N (BLOCK_N / WMMA_N)

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

// TODO: 实现优化的 Tensor Core GEMM
// C = alpha * A * B + beta * C
__global__ void optimized_tensor_gemm(
    half *A, half *B, float *C,
    int M, int N, int K,
    float alpha, float beta) {

    // TODO: 计算 warp 和 block 的位置
    // int warpM = (blockIdx.x * blockDim.x + threadIdx.x) / warpSize;
    // int warpN = (blockIdx.y * blockDim.y + threadIdx.y);

    // TODO: 声明 WMMA fragments
    // wmma::fragment<wmma::matrix_a, WMMA_M, WMMA_N, WMMA_K, half, wmma::row_major> a_frag;
    // wmma::fragment<wmma::matrix_b, WMMA_M, WMMA_N, WMMA_K, half, wmma::row_major> b_frag;
    // wmma::fragment<wmma::accumulator, WMMA_M, WMMA_N, WMMA_K, float> acc_frag;
    // wmma::fragment<wmma::accumulator, WMMA_M, WMMA_N, WMMA_K, float> c_frag;

    // TODO: 初始化累加器
    // wmma::fill_fragment(acc_frag, 0.0f);

    // TODO: 分块遍历 K 维度
    // for (int k = 0; k < K; k += WMMA_K) {
    //     // 加载 A 和 B 的 tiles
    //     // 执行矩阵乘法累加
    // }

    // TODO: 如果 beta != 0, 加载并累加原始 C
    // if (beta != 0.0f) {
    //     wmma::load_matrix_sync(c_frag, C + ..., N, wmma::mem_row_major);
    //     for (int i = 0; i < c_frag.num_elements; i++) {
    //         acc_frag.x[i] = alpha * acc_frag.x[i] + beta * c_frag.x[i];
    //     }
    // }

    // TODO: 存储结果
}

// CPU 参考实现
void cpu_gemm(half *A, half *B, float *C, int M, int N, int K) {
    for (int i = 0; i < M; i++) {
        for (int j = 0; j < N; j++) {
            float sum = 0.0f;
            for (int k = 0; k < K; k++) {
                sum += __half2float(A[i * K + k]) * __half2float(B[k * N + j]);
            }
            C[i * N + j] = sum;
        }
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

    printf("使用 %s 进行 GEMM 优化测试\n", prop.name);
    printf("矩阵大小: %d x %d x %d\n\n", MATRIX_M, MATRIX_K, MATRIX_N);

    // 分配内存
    size_t size_A = MATRIX_M * MATRIX_K * sizeof(half);
    size_t size_B = MATRIX_K * MATRIX_N * sizeof(half);
    size_t size_C = MATRIX_M * MATRIX_N * sizeof(float);

    half *h_A = (half*)malloc(size_A);
    half *h_B = (half*)malloc(size_B);
    float *h_C = (float*)malloc(size_C);
    float *h_C_ref = (float*)malloc(size_C);

    // 初始化
    for (int i = 0; i < MATRIX_M * MATRIX_K; i++) {
        h_A[i] = __float2half((float)(rand() % 10) / 10.0f);
    }
    for (int i = 0; i < MATRIX_K * MATRIX_N; i++) {
        h_B[i] = __float2half((float)(rand() % 10) / 10.0f);
    }

    half *d_A, *d_B;
    float *d_C;
    CUDA_CHECK(cudaMalloc(&d_A, size_A));
    CUDA_CHECK(cudaMalloc(&d_B, size_B));
    CUDA_CHECK(cudaMalloc(&d_C, size_C));

    CUDA_CHECK(cudaMemcpy(d_A, h_A, size_A, cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_B, h_B, size_B, cudaMemcpyHostToDevice));

    // 配置 kernel
    dim3 blockDim(128, 4);
    dim3 gridDim((MATRIX_N + BLOCK_N - 1) / BLOCK_N,
                 (MATRIX_M + BLOCK_M - 1) / BLOCK_M);

    // Warm up
    optimized_tensor_gemm<<<gridDim, blockDim>>>(d_A, d_B, d_C,
                                                  MATRIX_M, MATRIX_N, MATRIX_K,
                                                  1.0f, 0.0f);
    CUDA_CHECK(cudaDeviceSynchronize());

    // 性能测试
    double start = get_time();
    optimized_tensor_gemm<<<gridDim, blockDim>>>(d_A, d_B, d_C,
                                                  MATRIX_M, MATRIX_N, MATRIX_K,
                                                  1.0f, 0.0f);
    CUDA_CHECK(cudaDeviceSynchronize());
    double elapsed = get_time() - start;

    CUDA_CHECK(cudaMemcpy(h_C, d_C, size_C, cudaMemcpyDeviceToHost));

    // 计算性能指标
    double flops = 2.0 * MATRIX_M * MATRIX_N * MATRIX_K;
    double tflops = flops / (elapsed * 1e12);

    printf("Tensor Core GEMM 性能:\n");
    printf("  时间: %.3f ms\n", elapsed * 1000);
    printf("  吞吐量: %.2f TFLOPS\n", tflops);

    // 计算理论峰值 (粗略估计)
    double peak_tflops = prop.multiProcessorCount *
                         (prop.clockRate * 1e-6) *
                         64.0 / 1000.0;  // 每SM每周期64 FP16 FMA操作
    printf("  理论峰值: ~%.2f TFLOPS (FP16)\n", peak_tflops);
    printf("  效率: %.1f%%\n", (tflops / peak_tflops) * 100);

    CUDA_CHECK(cudaFree(d_A));
    CUDA_CHECK(cudaFree(d_B));
    CUDA_CHECK(cudaFree(d_C));
    free(h_A);
    free(h_B);
    free(h_C);
    free(h_C_ref);

    printf("\nGEMM 优化测试完成!\n");
    printf("TEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
