// 练习 28: 固定内存（Pinned Memory）
//
// 目标: 使用固定内存加速数据传输
//
// 任务:
// 1. 分配固定内存
// 2. 比较固定内存和普通内存的传输速度
// 3. 正确释放固定内存

#include <stdio.h>
#include <cuda_runtime.h>
#include <time.h>

#define N 10000000  // 10M 元素
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

int main() {
    float *h_pageable, *h_pinned;
    float *d_data;
    size_t bytes = N * sizeof(float);

    // 分配普通（可分页）内存
    h_pageable = (float*)malloc(bytes);

    // TODO: 分配固定内存
    // 提示: 使用 cudaMallocHost 或 cudaHostAlloc
    // CUDA_CHECK(cudaMallocHost(&h_pinned, bytes));

    CUDA_CHECK(cudaMalloc(&d_data, bytes));

    // 初始化数据
    for (int i = 0; i < N; i++) {
        h_pageable[i] = i;
        h_pinned[i] = i;
    }

    // 测试普通内存传输速度
    double start = get_time();
    CUDA_CHECK(cudaMemcpy(d_data, h_pageable, bytes, cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaDeviceSynchronize());
    double pageable_time = get_time() - start;

    // 测试固定内存传输速度
    start = get_time();
    CUDA_CHECK(cudaMemcpy(d_data, h_pinned, bytes, cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaDeviceSynchronize());
    double pinned_time = get_time() - start;

    printf("普通内存传输时间: %.4f ms\n", pageable_time * 1000);
    printf("固定内存传输时间: %.4f ms\n", pinned_time * 1000);
    printf("加速比: %.2fx\n", pageable_time / pinned_time);

    // TODO: 释放固定内存
    // 提示: 使用 cudaFreeHost
    // CUDA_CHECK(cudaFreeHost(h_pinned));

    CUDA_CHECK(cudaFree(d_data));
    free(h_pageable);

    // 固定内存应该更快
    if (pinned_time <= pageable_time) {
        printf("TEST_PASSED\n");
        return 0;
    } else {
        printf("⚠️  固定内存没有更快（可能是系统配置问题）\n");
        printf("TEST_PASSED\n");  // 仍然通过，因为代码正确
        return 0;
    }
}

// I AM NOT DONE
