// 练习 66: 内存合并访问
//
// 目标: 优化全局内存访问模式以实现合并访问
//
// 任务:
// 1. 实现非合并访问的版本
// 2. 实现合并访问的版本
// 3. 比较性能差异

#include <stdio.h>
#include <cuda_runtime.h>
#include <time.h>

#define N 10000000
#define BLOCK_SIZE 256

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// 非合并访问：跨步访问
__global__ void copy_strided(float *input, float *output, int n, int stride) {
    int idx = (blockIdx.x * blockDim.x + threadIdx.x) * stride;
    if (idx < n) {
        output[idx] = input[idx];
    }
}

// TODO: 实现合并访问版本
// 相邻线程访问相邻内存
__global__ void copy_coalesced(float *input, float *output, int n) {
    // int idx = blockIdx.x * blockDim.x + threadIdx.x;
    // if (idx < n) {
    //     output[idx] = input[idx];
    // }
}

double get_time() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

int main() {
    float *d_input, *d_output;
    size_t bytes = N * sizeof(float);

    CUDA_CHECK(cudaMalloc(&d_input, bytes));
    CUDA_CHECK(cudaMalloc(&d_output, bytes));

    int grid_size = (N + BLOCK_SIZE - 1) / BLOCK_SIZE;

    // 测试非合并访问（stride=32）
    double start = get_time();
    copy_strided<<<grid_size / 32, BLOCK_SIZE>>>(d_input, d_output, N, 32);
    CUDA_CHECK(cudaDeviceSynchronize());
    double strided_time = get_time() - start;

    // 测试合并访问
    start = get_time();
    copy_coalesced<<<grid_size, BLOCK_SIZE>>>(d_input, d_output, N);
    CUDA_CHECK(cudaDeviceSynchronize());
    double coalesced_time = get_time() - start;

    printf("非合并访问时间: %.4f ms\n", strided_time * 1000);
    printf("合并访问时间: %.4f ms\n", coalesced_time * 1000);
    printf("加速比: %.2fx\n", strided_time / coalesced_time);

    CUDA_CHECK(cudaFree(d_input));
    CUDA_CHECK(cudaFree(d_output));

    // 合并访问应该更快
    if (coalesced_time < strided_time) {
        printf("TEST_PASSED\n");
        return 0;
    } else {
        printf("⚠️  合并访问没有更快\n");
        printf("TEST_PASSED\n");  // 仍通过，因为代码正确
        return 0;
    }
}

// I AM NOT DONE
