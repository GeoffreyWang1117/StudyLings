// 练习 17: 二维线程网格
//
// 目标: 使用二维线程网格处理矩阵
//
// 任务:
// 1. 理解 2D 线程组织
// 2. 计算行和列索引
// 3. 实现矩阵转置

#include <stdio.h>
#include <cuda_runtime.h>

#define WIDTH 32
#define HEIGHT 32

// TODO: 实现矩阵转置 kernel
// 提示: 使用 blockIdx.x, blockIdx.y, threadIdx.x, threadIdx.y
__global__ void transpose(float *input, float *output, int width, int height) {
    // TODO: 计算列索引
    // int col = blockIdx.x * blockDim.x + threadIdx.x;

    // TODO: 计算行索引
    // int row = blockIdx.y * blockDim.y + threadIdx.y;

    // TODO: 边界检查并执行转置
    // output[col * height + row] = input[row * width + col];
}

int main() {
    float *h_input, *h_output, *d_input, *d_output;
    size_t bytes = WIDTH * HEIGHT * sizeof(float);

    h_input = (float*)malloc(bytes);
    h_output = (float*)malloc(bytes);

    // 初始化矩阵
    for (int i = 0; i < HEIGHT; i++) {
        for (int j = 0; j < WIDTH; j++) {
            h_input[i * WIDTH + j] = i * WIDTH + j;
        }
    }

    cudaMalloc(&d_input, bytes);
    cudaMalloc(&d_output, bytes);
    cudaMemcpy(d_input, h_input, bytes, cudaMemcpyHostToDevice);

    // TODO: 设置 2D 线程块和网格
    dim3 blockDim(16, 16);  // 16x16 线程块
    dim3 gridDim(1, 1);     // 修改这里以覆盖整个矩阵

    transpose<<<gridDim, blockDim>>>(d_input, d_output, WIDTH, HEIGHT);
    cudaDeviceSynchronize();

    cudaMemcpy(h_output, d_output, bytes, cudaMemcpyDeviceToHost);

    // 验证转置
    bool success = true;
    for (int i = 0; i < HEIGHT; i++) {
        for (int j = 0; j < WIDTH; j++) {
            float expected = j * HEIGHT + i;  // 转置后的值
            if (h_output[i * WIDTH + j] != expected) {
                printf("错误 at (%d, %d)\n", i, j);
                success = false;
                break;
            }
        }
        if (!success) break;
    }

    cudaFree(d_input);
    cudaFree(d_output);
    free(h_input);
    free(h_output);

    if (success) {
        printf("矩阵转置正确!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}

// I AM NOT DONE
