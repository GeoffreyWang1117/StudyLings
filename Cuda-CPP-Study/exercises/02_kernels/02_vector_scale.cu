// 练习 7: 向量缩放
//
// 目标: 实现向量缩放 B = scale * A
//
// 任务:
// 1. 实现向量缩放 kernel
// 2. 处理不能被 block 大小整除的数组
// 3. 添加边界检查

#include <stdio.h>
#include <cuda_runtime.h>
#include <math.h>

#define N 10000  // 注意: 不是 2 的幂
#define BLOCK_SIZE 256
#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// TODO: 实现向量缩放 kernel
// 提示: 需要处理全局索引计算
// 提示: 必须添加边界检查 (idx < n)
__global__ void vector_scale(float *input, float *output, float scale, int n) {
    // TODO: 计算全局线程索引
    // int idx = ???

    // TODO: 边界检查并执行缩放
}

int main() {
    float *h_input, *h_output;
    float *d_input, *d_output;
    float scale = 3.14f;
    size_t bytes = N * sizeof(float);

    // 分配和初始化主机内存
    h_input = (float*)malloc(bytes);
    h_output = (float*)malloc(bytes);

    for (int i = 0; i < N; i++) {
        h_input[i] = i * 0.5f;
    }

    // 分配设备内存
    CUDA_CHECK(cudaMalloc(&d_input, bytes));
    CUDA_CHECK(cudaMalloc(&d_output, bytes));

    // 拷贝到设备
    CUDA_CHECK(cudaMemcpy(d_input, h_input, bytes, cudaMemcpyHostToDevice));

    // TODO: 计算 grid 大小
    // 提示: 需要向上取整以覆盖所有元素
    // 提示: grid_size = (N + BLOCK_SIZE - 1) / BLOCK_SIZE
    int grid_size = 1; // 修改这里

    // 调用 kernel
    vector_scale<<<grid_size, BLOCK_SIZE>>>(d_input, d_output, scale, N);
    CUDA_CHECK(cudaGetLastError());
    CUDA_CHECK(cudaDeviceSynchronize());

    // 拷贝结果
    CUDA_CHECK(cudaMemcpy(h_output, d_output, bytes, cudaMemcpyDeviceToHost));

    // 验证
    bool success = true;
    for (int i = 0; i < N; i++) {
        float expected = h_input[i] * scale;
        if (fabsf(h_output[i] - expected) > 1e-5) {
            printf("错误 at %d: got %f, expected %f\n", i, h_output[i], expected);
            success = false;
            break;
        }
    }

    // 清理
    CUDA_CHECK(cudaFree(d_input));
    CUDA_CHECK(cudaFree(d_output));
    free(h_input);
    free(h_output);

    if (success) {
        printf("向量缩放正确!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}

// I AM NOT DONE
