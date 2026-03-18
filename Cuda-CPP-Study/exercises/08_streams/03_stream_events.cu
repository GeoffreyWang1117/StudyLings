// 练习 83: 流和事件
//
// 目标: 使用事件进行计时和同步
//
// 任务:
// 1. 创建 CUDA 事件
// 2. 测量 kernel 执行时间
// 3. 使用事件同步流

#include <stdio.h>
#include <cuda_runtime.h>

#define N 1000000
#define BLOCK_SIZE 256

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

__global__ void vector_add(float *a, float *b, float *c, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        c[idx] = a[idx] + b[idx];
    }
}

int main() {
    float *d_a, *d_b, *d_c;
    size_t bytes = N * sizeof(float);

    CUDA_CHECK(cudaMalloc(&d_a, bytes));
    CUDA_CHECK(cudaMalloc(&d_b, bytes));
    CUDA_CHECK(cudaMalloc(&d_c, bytes));

    // TODO: 创建事件
    cudaEvent_t start, stop;
    // CUDA_CHECK(cudaEventCreate(&start));
    // CUDA_CHECK(cudaEventCreate(&stop));

    int grid_size = (N + BLOCK_SIZE - 1) / BLOCK_SIZE;

    // TODO: 记录开始事件
    // CUDA_CHECK(cudaEventRecord(start));

    vector_add<<<grid_size, BLOCK_SIZE>>>(d_a, d_b, d_c, N);

    // TODO: 记录结束事件
    // CUDA_CHECK(cudaEventRecord(stop));

    // TODO: 等待事件完成
    // CUDA_CHECK(cudaEventSynchronize(stop));

    // TODO: 计算经过的时间
    float milliseconds = 0;
    // CUDA_CHECK(cudaEventElapsedTime(&milliseconds, start, stop));

    printf("Kernel 执行时间: %.3f ms\n", milliseconds);

    // TODO: 销毁事件
    // CUDA_CHECK(cudaEventDestroy(start));
    // CUDA_CHECK(cudaEventDestroy(stop));

    CUDA_CHECK(cudaFree(d_a));
    CUDA_CHECK(cudaFree(d_b));
    CUDA_CHECK(cudaFree(d_c));

    printf("TEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
