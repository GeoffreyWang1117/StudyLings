// 练习 3: CUDA 错误处理
//
// 目标: 学习如何正确处理 CUDA 错误
//
// 任务:
// 1. 创建一个错误检查宏
// 2. 使用该宏检查 CUDA API 调用
// 3. 处理和报告错误

#include <stdio.h>
#include <cuda_runtime.h>
#include <stdlib.h>

// TODO: 实现错误检查宏
// 提示: 宏应该检查 cudaError_t 返回值
// 提示: 如果有错误，打印错误信息并退出
#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error at %s:%d - %s\n", \
                    __FILE__, __LINE__, cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

__global__ void simple_kernel() {
    printf("Kernel running on GPU\n");
}

int main() {
    printf("测试 CUDA 错误处理...\n");

    // TODO: 使用 CUDA_CHECK 宏检查以下操作

    // 1. 获取设备数量
    int deviceCount;
    CUDA_CHECK(cudaGetDeviceCount(&deviceCount));

    if (deviceCount > 0) {
        // 2. 设置设备
        CUDA_CHECK(cudaSetDevice(0));

        // 3. 分配内存
        float *d_data;
        // TODO: 使用 CUDA_CHECK 检查 cudaMalloc

        // 4. 调用 kernel
        simple_kernel<<<1, 1>>>();

        // 5. 检查 kernel 启动错误
        // TODO: 使用 CUDA_CHECK 检查 cudaGetLastError()

        // 6. 同步设备
        // TODO: 使用 CUDA_CHECK 检查 cudaDeviceSynchronize()

        // 7. 释放内存
        // TODO: 使用 CUDA_CHECK 检查 cudaFree
    }

    printf("所有操作成功完成!\n");
    printf("TEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
