// 练习 67: 占用率优化
//
// 目标: 理解和优化占用率
//
// 任务:
// 1. 理解占用率的概念
// 2. 调整 block 大小以优化占用率
// 3. 使用 cudaOccupancyMaxPotentialBlockSize

#include <stdio.h>
#include <cuda_runtime.h>

#define N 1000000

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

__global__ void simple_kernel(float *data, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        data[idx] = data[idx] * 2.0f + 1.0f;
    }
}

int main() {
    float *d_data;
    CUDA_CHECK(cudaMalloc(&d_data, N * sizeof(float)));

    // TODO: 使用 cudaOccupancyMaxPotentialBlockSize 获取最优配置
    int minGridSize, blockSize;
    // CUDA_CHECK(cudaOccupancyMaxPotentialBlockSize(
    //     &minGridSize, &blockSize, simple_kernel, 0, 0));

    // 手动设置（先用这个）
    blockSize = 256;
    minGridSize = (N + blockSize - 1) / blockSize;

    printf("推荐的 block 大小: %d\n", blockSize);
    printf("最小 grid 大小: %d\n", minGridSize);

    // 计算占用率
    int maxActiveBlocks;
    CUDA_CHECK(cudaOccupancyMaxActiveBlocksPerMultiprocessor(
        &maxActiveBlocks, simple_kernel, blockSize, 0));

    cudaDeviceProp prop;
    CUDA_CHECK(cudaGetDeviceProperties(&prop, 0));

    float occupancy = (maxActiveBlocks * blockSize) /
                      (float)prop.maxThreadsPerMultiProcessor;
    printf("理论占用率: %.2f%%\n", occupancy * 100);

    // 运行 kernel
    simple_kernel<<<minGridSize, blockSize>>>(d_data, N);
    CUDA_CHECK(cudaDeviceSynchronize());

    CUDA_CHECK(cudaFree(d_data));

    printf("TEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
