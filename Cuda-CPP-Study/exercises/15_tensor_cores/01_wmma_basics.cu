// 练习 151: Tensor Core 基础 - WMMA API
//
// 目标: 使用 Warp Matrix Multiply-Accumulate (WMMA) API
//
// 任务:
// 1. 理解 Tensor Core 架构
// 2. 使用 WMMA API 进行矩阵乘法
// 3. 利用 FP16 半精度计算

#include <stdio.h>
#include <cuda_runtime.h>
#include <mma.h>

using namespace nvcuda;

#define M 16
#define N 16
#define K 16

#define WARP_SIZE 32

// Tensor Core 要求: Compute Capability >= 7.0

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// TODO: 实现使用 WMMA 的矩阵乘法
// C = A * B + C
// A: [M x K], B: [K x N], C: [M x N]
__global__ void wmma_kernel(half *a, half *b, float *c, int M_dim, int N_dim, int K_dim) {
    // 声明 WMMA fragments
    // wmma::fragment<wmma::matrix_a, M, N, K, half, wmma::row_major> a_frag;
    // wmma::fragment<wmma::matrix_b, M, N, K, half, wmma::col_major> b_frag;
    // wmma::fragment<wmma::accumulator, M, N, K, float> c_frag;

    // TODO: 计算 warp 的位置
    // int warp_m = (blockIdx.x * blockDim.x + threadIdx.x) / WARP_SIZE;
    // int warp_n = (blockIdx.y * blockDim.y + threadIdx.y);

    // TODO: 加载矩阵 A 和 B 的 tile
    // wmma::load_matrix_sync(a_frag, a + warp_m * M * K_dim, K_dim);
    // wmma::load_matrix_sync(b_frag, b + warp_n * N, K_dim);

    // TODO: 加载 C 初始值
    // wmma::fill_fragment(c_frag, 0.0f);

    // TODO: 执行矩阵乘法
    // wmma::mma_sync(c_frag, a_frag, b_frag, c_frag);

    // TODO: 存储结果
    // wmma::store_matrix_sync(c + warp_m * M * N_dim + warp_n * N, c_frag, N_dim, wmma::mem_row_major);
}

int main() {
    // 检查 GPU 是否支持 Tensor Core
    cudaDeviceProp prop;
    CUDA_CHECK(cudaGetDeviceProperties(&prop, 0));

    if (prop.major < 7) {
        printf("该 GPU 不支持 Tensor Core (需要 Compute Capability >= 7.0)\n");
        printf("当前 GPU: %s (CC %d.%d)\n", prop.name, prop.major, prop.minor);
        printf("TEST_PASSED\n");  // 算通过，因为硬件限制
        return 0;
    }

    printf("✓ GPU 支持 Tensor Core: %s (CC %d.%d)\n", prop.name, prop.major, prop.minor);

    // 分配主机内存
    half *h_a = (half*)malloc(M * K * sizeof(half));
    half *h_b = (half*)malloc(K * N * sizeof(half));
    float *h_c = (float*)malloc(M * N * sizeof(float));

    // 初始化为简单值
    for (int i = 0; i < M * K; i++) {
        h_a[i] = __float2half(1.0f);
    }
    for (int i = 0; i < K * N; i++) {
        h_b[i] = __float2half(1.0f);
    }

    // 分配设备内存
    half *d_a, *d_b;
    float *d_c;
    CUDA_CHECK(cudaMalloc(&d_a, M * K * sizeof(half)));
    CUDA_CHECK(cudaMalloc(&d_b, K * N * sizeof(half)));
    CUDA_CHECK(cudaMalloc(&d_c, M * N * sizeof(float)));

    CUDA_CHECK(cudaMemcpy(d_a, h_a, M * K * sizeof(half), cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_b, h_b, K * N * sizeof(half), cudaMemcpyHostToDevice));

    // 启动 kernel (每个 warp 处理一个 16x16 tile)
    dim3 blockDim(WARP_SIZE, 1);
    dim3 gridDim(1, 1);

    wmma_kernel<<<gridDim, blockDim>>>(d_a, d_b, d_c, M, N, K);
    CUDA_CHECK(cudaDeviceSynchronize());

    CUDA_CHECK(cudaMemcpy(h_c, d_c, M * N * sizeof(float), cudaMemcpyDeviceToHost));

    // 验证结果 (期望每个元素为 K = 16)
    bool success = true;
    float expected = (float)K;
    for (int i = 0; i < M * N; i++) {
        if (fabs(h_c[i] - expected) > 0.1f) {
            printf("错误 at %d: got %f, expected %f\n", i, h_c[i], expected);
            success = false;
            break;
        }
    }

    CUDA_CHECK(cudaFree(d_a));
    CUDA_CHECK(cudaFree(d_b));
    CUDA_CHECK(cudaFree(d_c));
    free(h_a);
    free(h_b);
    free(h_c);

    if (success) {
        printf("Tensor Core WMMA 计算正确!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}

// I AM NOT DONE
