// 练习 6: 简单向量加法
//
// 目标: 实现基本的向量加法 C = A + B
//
// 任务:
// 1. 实现向量加法 kernel
// 2. 分配设备内存
// 3. 拷贝数据到设备
// 4. 执行 kernel
// 5. 拷贝结果回主机

#include <stdio.h>
#include <cuda_runtime.h>

#define N 1024
#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// TODO: 实现向量加法 kernel
// 提示: 每个线程计算一个元素
// 提示: 使用 threadIdx.x 获取线程索引
__global__ void vector_add(float *a, float *b, float *c, int n) {
    // 你的代码在这里
}

int main() {
    float *h_a, *h_b, *h_c;  // 主机数组
    float *d_a, *d_b, *d_c;  // 设备数组
    size_t bytes = N * sizeof(float);

    // 分配主机内存
    h_a = (float*)malloc(bytes);
    h_b = (float*)malloc(bytes);
    h_c = (float*)malloc(bytes);

    // 初始化输入数组
    for (int i = 0; i < N; i++) {
        h_a[i] = i;
        h_b[i] = i * 2.0f;
    }

    // TODO: 分配设备内存
    // 提示: 使用 cudaMalloc

    // TODO: 拷贝数据到设备
    // 提示: 使用 cudaMemcpy with cudaMemcpyHostToDevice

    // TODO: 调用 kernel
    // 提示: 使用足够的线程来处理 N 个元素
    // 提示: 可以从 <<<1, N>>> 开始（如果 N <= 1024）

    // TODO: 拷贝结果回主机
    // 提示: 使用 cudaMemcpy with cudaMemcpyDeviceToHost

    // 验证结果
    bool success = true;
    for (int i = 0; i < N; i++) {
        float expected = h_a[i] + h_b[i];
        if (fabs(h_c[i] - expected) > 1e-5) {
            printf("错误: h_c[%d] = %f, 期望 %f\n", i, h_c[i], expected);
            success = false;
            break;
        }
    }

    // TODO: 释放设备内存

    // 释放主机内存
    free(h_a);
    free(h_b);
    free(h_c);

    if (success) {
        printf("向量加法正确!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}

// I AM NOT DONE
