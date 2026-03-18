// 练习 57: 原子操作
//
// 目标: 使用原子操作避免竞态条件
//
// 任务:
// 1. 理解竞态条件问题
// 2. 使用 atomicAdd 解决问题
// 3. 实现直方图计算

#include <stdio.h>
#include <cuda_runtime.h>

#define N 10000
#define NUM_BINS 256
#define BLOCK_SIZE 256

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// TODO: 实现直方图计算
// 使用原子操作避免竞态条件
__global__ void histogram(unsigned char *data, unsigned int *bins, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    // TODO: 使用 atomicAdd 更新直方图
    // if (idx < n) {
    //     unsigned char value = data[idx];
    //     atomicAdd(&bins[value], 1);
    // }
}

int main() {
    unsigned char *h_data, *d_data;
    unsigned int *h_bins, *d_bins;

    h_data = (unsigned char*)malloc(N);
    h_bins = (unsigned int*)calloc(NUM_BINS, sizeof(unsigned int));

    // 初始化数据（随机值 0-255）
    for (int i = 0; i < N; i++) {
        h_data[i] = i % NUM_BINS;
    }

    CUDA_CHECK(cudaMalloc(&d_data, N));
    CUDA_CHECK(cudaMalloc(&d_bins, NUM_BINS * sizeof(unsigned int)));
    CUDA_CHECK(cudaMemset(d_bins, 0, NUM_BINS * sizeof(unsigned int)));

    CUDA_CHECK(cudaMemcpy(d_data, h_data, N, cudaMemcpyHostToDevice));

    int grid_size = (N + BLOCK_SIZE - 1) / BLOCK_SIZE;
    histogram<<<grid_size, BLOCK_SIZE>>>(d_data, d_bins, N);
    CUDA_CHECK(cudaDeviceSynchronize());

    CUDA_CHECK(cudaMemcpy(h_bins, d_bins, NUM_BINS * sizeof(unsigned int), cudaMemcpyDeviceToHost));

    // 验证：每个 bin 应该有相同数量
    bool success = true;
    unsigned int expected = N / NUM_BINS;
    for (int i = 0; i < NUM_BINS; i++) {
        if (h_bins[i] != expected) {
            printf("错误 bin %d: got %u, expected %u\n", i, h_bins[i], expected);
            success = false;
            break;
        }
    }

    CUDA_CHECK(cudaFree(d_data));
    CUDA_CHECK(cudaFree(d_bins));
    free(h_data);
    free(h_bins);

    if (success) {
        printf("原子操作使用正确!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}

// I AM NOT DONE
