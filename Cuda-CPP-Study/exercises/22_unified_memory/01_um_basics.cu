/**
 * 练习 221: Unified Memory 基础
 *
 * 学习目标：
 * - 理解统一内存（Unified Memory）的概念
 * - 使用 cudaMallocManaged() 分配统一内存
 * - 理解 CPU 和 GPU 自动迁移数据的机制
 *
 * 任务：
 * 1. 使用 cudaMallocManaged() 分配内存
 * 2. 在 CPU 端初始化数组
 * 3. 在 GPU 端处理数据（向量加法）
 * 4. 在 CPU 端读取结果
 * 5. 对比 Unified Memory 与传统方式的代码简洁性
 */

#include <cuda_runtime.h>
#include <stdio.h>
#include <stdlib.h>

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error at %s:%d - %s\n", __FILE__, __LINE__, \
                    cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// TODO: 实现向量加法 kernel
__global__ void vector_add(float *a, float *b, float *c, int n) {
    // 提示：计算全局索引并执行加法
    // int i = blockIdx.x * blockDim.x + threadIdx.x;
    // if (i < n) c[i] = a[i] + b[i];
}

int main() {
    const int N = 1 << 20;  // 1M elements
    size_t bytes = N * sizeof(float);

    float *a, *b, *c;

    // TODO 1: 使用 cudaMallocManaged() 分配统一内存
    // 提示：cudaMallocManaged((void**)&a, bytes);


    // TODO 2: 在 CPU 端初始化数据
    printf("Initializing data on CPU...\n");
    // 提示：直接访问 a[i], b[i]，就像普通指针一样


    // TODO 3: 在 GPU 端执行计算
    int threadsPerBlock = 256;
    int blocksPerGrid = (N + threadsPerBlock - 1) / threadsPerBlock;

    printf("Launching kernel on GPU...\n");
    // 提示：vector_add<<<blocksPerGrid, threadsPerBlock>>>(a, b, c, N);


    // TODO 4: 等待 GPU 完成
    // 提示：cudaDeviceSynchronize();


    // TODO 5: 在 CPU 端验证结果
    printf("Verifying results on CPU...\n");
    bool success = true;
    for (int i = 0; i < N; i++) {
        // 提示：检查 c[i] 是否等于 a[i] + b[i]
    }

    if (success) {
        printf("✓ Unified Memory 测试通过！\n");
    } else {
        printf("✗ 验证失败\n");
    }

    // TODO 6: 释放统一内存
    // 提示：cudaFree(a); cudaFree(b); cudaFree(c);


    printf("\n优势对比：\n");
    printf("传统方式需要：cudaMalloc, cudaMemcpy (H2D), kernel, cudaMemcpy (D2H), cudaFree\n");
    printf("统一内存只需：cudaMallocManaged, kernel, cudaFree\n");
    printf("代码更简洁，自动处理数据迁移！\n");

    return 0;
}

/**
 * 编译命令：
 * nvcc -o um_basics 01_um_basics.cu
 *
 * 运行命令：
 * ./um_basics
 *
 * 知识点：
 * 1. Unified Memory 在 Pascal 及以上架构表现最佳
 * 2. 自动按需页面迁移（Page Migration）
 * 3. CPU 和 GPU 可以直接访问同一指针
 * 4. 系统会自动处理数据一致性
 * 5. 简化了内存管理代码
 */
