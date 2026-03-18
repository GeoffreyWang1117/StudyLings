// 练习 3: CUDA 错误处理 - 参考解决方案

#include <stdio.h>
#include <cuda_runtime.h>
#include <stdlib.h>

// 错误检查宏 - CUDA 编程的最佳实践
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

    // 1. 获取设备数量
    int deviceCount;
    CUDA_CHECK(cudaGetDeviceCount(&deviceCount));

    if (deviceCount > 0) {
        // 2. 设置设备
        CUDA_CHECK(cudaSetDevice(0));

        // 3. 分配内存
        float *d_data;
        CUDA_CHECK(cudaMalloc(&d_data, 1024 * sizeof(float)));

        // 4. 调用 kernel
        simple_kernel<<<1, 1>>>();

        // 5. 检查 kernel 启动错误
        CUDA_CHECK(cudaGetLastError());

        // 6. 同步设备
        CUDA_CHECK(cudaDeviceSynchronize());

        // 7. 释放内存
        CUDA_CHECK(cudaFree(d_data));
    }

    printf("所有操作成功完成!\n");
    printf("TEST_PASSED\n");
    return 0;
}
