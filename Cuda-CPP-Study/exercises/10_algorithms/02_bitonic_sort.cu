// 练习 102: Bitonic Sort (双调排序)
//
// 目标: 实现并行双调排序算法
//
// 任务:
// 1. 理解双调排序原理
// 2. 实现 bitonic merge
// 3. 实现完整的排序

#include <stdio.h>
#include <cuda_runtime.h>
#include <stdlib.h>
#include <time.h>

#define N 512  // 必须是 2 的幂
#define BLOCK_SIZE 256

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// TODO: 实现 bitonic sort kernel
__global__ void bitonic_sort_step(int *data, int j, int k) {
    int idx = threadIdx.x + blockDim.x * blockIdx.x;
    int ixj = idx ^ j;

    if (ixj > idx) {
        if ((idx & k) == 0) {
            // TODO: 升序比较
            // if (data[idx] > data[ixj]) {
            //     // 交换
            //     int temp = data[idx];
            //     data[idx] = data[ixj];
            //     data[ixj] = temp;
            // }
        } else {
            // TODO: 降序比较
            // if (data[idx] < data[ixj]) {
            //     // 交换
            //     int temp = data[idx];
            //     data[idx] = data[ixj];
            //     data[ixj] = temp;
            // }
        }
    }
}

void bitonic_sort(int *d_data, int n) {
    // TODO: 实现 bitonic sort 的主循环
    // for (int k = 2; k <= n; k *= 2) {
    //     for (int j = k / 2; j > 0; j /= 2) {
    //         bitonic_sort_step<<<(n + BLOCK_SIZE - 1) / BLOCK_SIZE, BLOCK_SIZE>>>(d_data, j, k);
    //         cudaDeviceSynchronize();
    //     }
    // }
}

int main() {
    int *h_data, *d_data;

    h_data = (int*)malloc(N * sizeof(int));

    // 随机初始化
    srand(time(NULL));
    for (int i = 0; i < N; i++) {
        h_data[i] = rand() % 1000;
    }

    printf("排序前前10个元素: ");
    for (int i = 0; i < 10; i++) {
        printf("%d ", h_data[i]);
    }
    printf("\n");

    CUDA_CHECK(cudaMalloc(&d_data, N * sizeof(int)));
    CUDA_CHECK(cudaMemcpy(d_data, h_data, N * sizeof(int), cudaMemcpyHostToDevice));

    bitonic_sort(d_data, N);

    CUDA_CHECK(cudaMemcpy(h_data, d_data, N * sizeof(int), cudaMemcpyDeviceToHost));

    printf("排序后前10个元素: ");
    for (int i = 0; i < 10; i++) {
        printf("%d ", h_data[i]);
    }
    printf("\n");

    // 验证排序
    bool success = true;
    for (int i = 0; i < N - 1; i++) {
        if (h_data[i] > h_data[i + 1]) {
            printf("排序错误 at %d: %d > %d\n", i, h_data[i], h_data[i + 1]);
            success = false;
            break;
        }
    }

    CUDA_CHECK(cudaFree(d_data));
    free(h_data);

    if (success) {
        printf("排序正确!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}

// I AM NOT DONE
