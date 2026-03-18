// 练习 29: 统一内存（Unified Memory）
//
// 目标: 使用统一内存简化编程
//
// 任务:
// 1. 分配统一内存
// 2. 在主机和设备之间无需显式拷贝
// 3. 理解统一内存的限制

#include <stdio.h>
#include <cuda_runtime.h>

#define N 1000
#define BLOCK_SIZE 256

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

__global__ void increment(int *data, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        data[idx] += 1;
    }
}

int main() {
    int *data;  // 统一内存指针

    // TODO: 分配统一内存
    // 提示: 使用 cudaMallocManaged
    // CUDA_CHECK(cudaMallocManaged(&data, N * sizeof(int)));

    // 在主机上初始化（无需拷贝！）
    for (int i = 0; i < N; i++) {
        data[i] = i;
    }

    // 在设备上处理
    int grid_size = (N + BLOCK_SIZE - 1) / BLOCK_SIZE;
    increment<<<grid_size, BLOCK_SIZE>>>(data, N);

    // TODO: 等待 GPU 完成
    // 提示: cudaDeviceSynchronize() 很重要！
    // CUDA_CHECK(cudaDeviceSynchronize());

    // 在主机上读取结果（无需拷贝！）
    bool success = true;
    for (int i = 0; i < N; i++) {
        if (data[i] != i + 1) {
            printf("错误 at %d: got %d, expected %d\n", i, data[i], i + 1);
            success = false;
            break;
        }
    }

    // TODO: 释放统一内存
    // 提示: 使用 cudaFree（和设备内存一样）
    // CUDA_CHECK(cudaFree(data));

    if (success) {
        printf("统一内存使用正确!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}

// I AM NOT DONE
