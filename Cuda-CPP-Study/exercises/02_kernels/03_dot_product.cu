// 练习 8: 向量点积
//
// 目标: 实现向量点积（内积）
//
// 任务:
// 1. 计算两个向量的点积 result = sum(A[i] * B[i])
// 2. 使用多个线程并行计算
// 3. 将部分结果归约到最终答案

#include <stdio.h>
#include <cuda_runtime.h>
#include <math.h>

#define N 1024
#define BLOCK_SIZE 256
#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// TODO: 实现点积 kernel
// 每个线程计算一个乘积，然后需要归约求和
__global__ void dot_product(float *a, float *b, float *partial_sums, int n) {
    __shared__ float temp[BLOCK_SIZE];

    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    int tid = threadIdx.x;

    // TODO: 计算部分乘积
    // if (idx < n) {
    //     temp[tid] = a[idx] * b[idx];
    // } else {
    //     temp[tid] = 0.0f;
    // }

    // __syncthreads();

    // TODO: 在共享内存中归约
    // for (int stride = blockDim.x / 2; stride > 0; stride >>= 1) {
    //     if (tid < stride) {
    //         temp[tid] += temp[tid + stride];
    //     }
    //     __syncthreads();
    // }

    // TODO: 第一个线程写入部分和
    // if (tid == 0) {
    //     partial_sums[blockIdx.x] = temp[0];
    // }
}

int main() {
    float *h_a, *h_b;
    float *d_a, *d_b, *d_partial;
    size_t bytes = N * sizeof(float);

    // 分配主机内存
    h_a = (float*)malloc(bytes);
    h_b = (float*)malloc(bytes);

    // 初始化
    for (int i = 0; i < N; i++) {
        h_a[i] = 1.0f;
        h_b[i] = 2.0f;
    }

    // 分配设备内存
    int num_blocks = (N + BLOCK_SIZE - 1) / BLOCK_SIZE;
    CUDA_CHECK(cudaMalloc(&d_a, bytes));
    CUDA_CHECK(cudaMalloc(&d_b, bytes));
    CUDA_CHECK(cudaMalloc(&d_partial, num_blocks * sizeof(float)));

    // 拷贝数据
    CUDA_CHECK(cudaMemcpy(d_a, h_a, bytes, cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_b, h_b, bytes, cudaMemcpyHostToDevice));

    // 调用 kernel
    dot_product<<<num_blocks, BLOCK_SIZE>>>(d_a, d_b, d_partial, N);
    CUDA_CHECK(cudaDeviceSynchronize());

    // 拷贝部分和回主机
    float *h_partial = (float*)malloc(num_blocks * sizeof(float));
    CUDA_CHECK(cudaMemcpy(h_partial, d_partial, num_blocks * sizeof(float), cudaMemcpyDeviceToHost));

    // 在 CPU 上完成最终归约
    float result = 0.0f;
    for (int i = 0; i < num_blocks; i++) {
        result += h_partial[i];
    }

    // 验证 (1.0 * 2.0 * N = 2048)
    float expected = 2.0f * N;
    bool success = fabsf(result - expected) < 1e-3;

    // 清理
    CUDA_CHECK(cudaFree(d_a));
    CUDA_CHECK(cudaFree(d_b));
    CUDA_CHECK(cudaFree(d_partial));
    free(h_a);
    free(h_b);
    free(h_partial);

    if (success) {
        printf("点积计算正确! 结果 = %.2f\n", result);
        printf("TEST_PASSED\n");
    } else {
        printf("错误: 得到 %.2f, 期望 %.2f\n", result, expected);
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}

// I AM NOT DONE
