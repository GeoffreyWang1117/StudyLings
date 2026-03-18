// 练习 9: 矩阵加法
//
// 目标: 使用 2D 网格实现矩阵加法
//
// 任务:
// 1. 实现矩阵加法 C = A + B
// 2. 使用 2D 线程块和网格
// 3. 正确处理边界

#include <stdio.h>
#include <cuda_runtime.h>

#define WIDTH 64
#define HEIGHT 64
#define BLOCK_SIZE 16

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// TODO: 实现矩阵加法 kernel
__global__ void matrix_add(float *a, float *b, float *c, int width, int height) {
    // TODO: 计算行和列索引
    // int col = blockIdx.x * blockDim.x + threadIdx.x;
    // int row = blockIdx.y * blockDim.y + threadIdx.y;

    // TODO: 边界检查并执行加法
    // if (row < height && col < width) {
    //     int idx = row * width + col;
    //     c[idx] = a[idx] + b[idx];
    // }
}

int main() {
    float *h_a, *h_b, *h_c;
    float *d_a, *d_b, *d_c;
    size_t bytes = WIDTH * HEIGHT * sizeof(float);

    // 分配主机内存
    h_a = (float*)malloc(bytes);
    h_b = (float*)malloc(bytes);
    h_c = (float*)malloc(bytes);

    // 初始化
    for (int i = 0; i < WIDTH * HEIGHT; i++) {
        h_a[i] = i * 1.0f;
        h_b[i] = i * 2.0f;
    }

    // 分配设备内存
    CUDA_CHECK(cudaMalloc(&d_a, bytes));
    CUDA_CHECK(cudaMalloc(&d_b, bytes));
    CUDA_CHECK(cudaMalloc(&d_c, bytes));

    // 拷贝数据
    CUDA_CHECK(cudaMemcpy(d_a, h_a, bytes, cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_b, h_b, bytes, cudaMemcpyHostToDevice));

    // TODO: 设置 2D 网格和块
    dim3 blockDim(BLOCK_SIZE, BLOCK_SIZE);
    dim3 gridDim(1, 1);  // 修改这里

    // 调用 kernel
    matrix_add<<<gridDim, blockDim>>>(d_a, d_b, d_c, WIDTH, HEIGHT);
    CUDA_CHECK(cudaDeviceSynchronize());

    // 拷贝结果
    CUDA_CHECK(cudaMemcpy(h_c, d_c, bytes, cudaMemcpyDeviceToHost));

    // 验证
    bool success = true;
    for (int i = 0; i < WIDTH * HEIGHT; i++) {
        float expected = h_a[i] + h_b[i];
        if (fabsf(h_c[i] - expected) > 1e-5) {
            printf("错误 at %d: got %f, expected %f\n", i, h_c[i], expected);
            success = false;
            break;
        }
    }

    // 清理
    CUDA_CHECK(cudaFree(d_a));
    CUDA_CHECK(cudaFree(d_b));
    CUDA_CHECK(cudaFree(d_c));
    free(h_a);
    free(h_b);
    free(h_c);

    if (success) {
        printf("矩阵加法正确!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}

// I AM NOT DONE
