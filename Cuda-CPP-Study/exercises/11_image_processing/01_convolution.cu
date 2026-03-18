// 练习 111: 2D 卷积
//
// 目标: 实现 2D 图像卷积操作
//
// 任务:
// 1. 实现基础 2D 卷积
// 2. 使用共享内存优化
// 3. 处理边界条件

#include <stdio.h>
#include <cuda_runtime.h>
#include <math.h>

#define WIDTH 512
#define HEIGHT 512
#define KERNEL_SIZE 3
#define KERNEL_RADIUS (KERNEL_SIZE / 2)
#define TILE_SIZE 16

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// 常量内存存储卷积核
__constant__ float d_kernel[KERNEL_SIZE * KERNEL_SIZE];

// TODO: 实现 2D 卷积 kernel
__global__ void convolution_2d(float *input, float *output, int width, int height) {
    // 使用共享内存存储 tile
    __shared__ float tile[TILE_SIZE + 2*KERNEL_RADIUS][TILE_SIZE + 2*KERNEL_RADIUS];

    int tx = threadIdx.x;
    int ty = threadIdx.y;
    int col = blockIdx.x * TILE_SIZE + tx;
    int row = blockIdx.y * TILE_SIZE + ty;

    // TODO: 加载数据到共享内存（包括 halo）
    // 每个线程负责加载一个或多个元素
    // for (int i = ty; i < TILE_SIZE + 2*KERNEL_RADIUS; i += blockDim.y) {
    //     for (int j = tx; j < TILE_SIZE + 2*KERNEL_RADIUS; j += blockDim.x) {
    //         int img_row = blockIdx.y * TILE_SIZE + i - KERNEL_RADIUS;
    //         int img_col = blockIdx.x * TILE_SIZE + j - KERNEL_RADIUS;
    //
    //         if (img_row >= 0 && img_row < height && img_col >= 0 && img_col < width) {
    //             tile[i][j] = input[img_row * width + img_col];
    //         } else {
    //             tile[i][j] = 0.0f;  // 边界填充0
    //         }
    //     }
    // }
    // __syncthreads();

    // TODO: 计算卷积
    // if (row < height && col < width) {
    //     float sum = 0.0f;
    //     for (int i = 0; i < KERNEL_SIZE; i++) {
    //         for (int j = 0; j < KERNEL_SIZE; j++) {
    //             int tile_row = ty + i;
    //             int tile_col = tx + j;
    //             sum += tile[tile_row][tile_col] * d_kernel[i * KERNEL_SIZE + j];
    //         }
    //     }
    //     output[row * width + col] = sum;
    // }
}

int main() {
    float *h_input, *h_output;
    float *d_input, *d_output;
    size_t bytes = WIDTH * HEIGHT * sizeof(float);

    h_input = (float*)malloc(bytes);
    h_output = (float*)malloc(bytes);

    // 初始化输入图像（简单的渐变）
    for (int i = 0; i < HEIGHT; i++) {
        for (int j = 0; j < WIDTH; j++) {
            h_input[i * WIDTH + j] = (float)(i + j) / (WIDTH + HEIGHT);
        }
    }

    // 定义卷积核（边缘检测）
    float h_kernel[KERNEL_SIZE * KERNEL_SIZE] = {
        -1, -1, -1,
        -1,  8, -1,
        -1, -1, -1
    };

    // 拷贝卷积核到常量内存
    CUDA_CHECK(cudaMemcpyToSymbol(d_kernel, h_kernel, KERNEL_SIZE * KERNEL_SIZE * sizeof(float)));

    CUDA_CHECK(cudaMalloc(&d_input, bytes));
    CUDA_CHECK(cudaMalloc(&d_output, bytes));

    CUDA_CHECK(cudaMemcpy(d_input, h_input, bytes, cudaMemcpyHostToDevice));

    dim3 blockDim(TILE_SIZE, TILE_SIZE);
    dim3 gridDim((WIDTH + TILE_SIZE - 1) / TILE_SIZE,
                 (HEIGHT + TILE_SIZE - 1) / TILE_SIZE);

    convolution_2d<<<gridDim, blockDim>>>(d_input, d_output, WIDTH, HEIGHT);
    CUDA_CHECK(cudaDeviceSynchronize());

    CUDA_CHECK(cudaMemcpy(h_output, d_output, bytes, cudaMemcpyDeviceToHost));

    // 简单验证：检查中心区域不全为0
    bool success = false;
    for (int i = HEIGHT/2 - 10; i < HEIGHT/2 + 10; i++) {
        for (int j = WIDTH/2 - 10; j < WIDTH/2 + 10; j++) {
            if (fabsf(h_output[i * WIDTH + j]) > 0.001f) {
                success = true;
                break;
            }
        }
        if (success) break;
    }

    CUDA_CHECK(cudaFree(d_input));
    CUDA_CHECK(cudaFree(d_output));
    free(h_input);
    free(h_output);

    if (success) {
        printf("卷积计算完成!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}

// I AM NOT DONE
