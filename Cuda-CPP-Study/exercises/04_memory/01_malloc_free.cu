// 练习 26: 设备内存分配
//
// 目标: 正确使用 cudaMalloc 和 cudaFree
//
// 任务:
// 1. 分配不同大小的设备内存
// 2. 检查分配是否成功
// 3. 正确释放内存

#include <stdio.h>
#include <cuda_runtime.h>

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            return 1; \
        } \
    } while(0)

int main() {
    // TODO: 分配不同类型和大小的设备内存

    // 1. 分配 1MB 的 float 数组
    float *d_floats;
    size_t float_size = 1024 * 1024 * sizeof(float);
    // TODO: 使用 cudaMalloc 分配

    // 2. 分配 1000 个 int 的数组
    int *d_ints;
    // TODO: 分配内存

    // 3. 分配一个复杂结构体数组
    struct Vector3 {
        float x, y, z;
    };
    Vector3 *d_vectors;
    size_t num_vectors = 500;
    // TODO: 分配内存

    // 验证内存已分配（通过尝试获取内存信息）
    size_t free_mem, total_mem;
    cudaMemGetInfo(&free_mem, &total_mem);
    printf("GPU 内存: %.2f MB 可用 / %.2f MB 总计\n",
           free_mem / 1024.0 / 1024.0,
           total_mem / 1024.0 / 1024.0);

    // TODO: 释放所有分配的内存
    // 提示: 使用 cudaFree

    printf("所有内存操作成功!\n");
    printf("TEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
