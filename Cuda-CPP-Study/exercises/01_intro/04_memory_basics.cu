// 练习 4: 内存分配基础
//
// 目标: 学习基本的设备内存分配和释放
//
// 任务:
// 1. 分配设备内存
// 2. 初始化设备内存
// 3. 正确释放内存

#include <stdio.h>
#include <cuda_runtime.h>

#define N 100
#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

int main() {
    float *d_array;
    float h_value = 3.14f;

    // TODO: 分配设备内存
    // 提示: 使用 cudaMalloc(&d_array, size)

    // TODO: 将所有元素初始化为 h_value
    // 提示: 使用 cudaMemset 或 cudaMemcpy

    // 验证: 拷贝一个元素回来检查
    float h_check;
    CUDA_CHECK(cudaMemcpy(&h_check, d_array, sizeof(float), cudaMemcpyDeviceToHost));

    // TODO: 释放设备内存
    // 提示: 使用 cudaFree(d_array)

    if (h_check == h_value) {
        printf("内存操作正确!\n");
        printf("TEST_PASSED\n");
        return 0;
    } else {
        printf("TEST_FAILED\n");
        return 1;
    }
}

// I AM NOT DONE
