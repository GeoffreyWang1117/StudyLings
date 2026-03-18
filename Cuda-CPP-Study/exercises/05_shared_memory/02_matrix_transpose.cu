// 练习 42: 使用共享内存的矩阵转置
//
// 目标: 使用共享内存优化矩阵转置
//
// 任务:
// 1. 使用共享内存作为中间缓冲
// 2. 实现合并内存访问
// 3. 避免 bank 冲突

#include <stdio.h>
#include <cuda_runtime.h>

#define WIDTH 1024
#define HEIGHT 1024
#define TILE_SIZE 32

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// TODO: 实现使用共享内存的矩阵转置
__global__ void transpose_shared(float *input, float *output, int width, int height) {
    // TODO: 声明共享内存 tile
    // __shared__ float tile[TILE_SIZE][TILE_SIZE];

    // TODO: 计算输入和输出位置
    // int x = blockIdx.x * TILE_SIZE + threadIdx.x;
    // int y = blockIdx.y * TILE_SIZE + threadIdx.y;

    // TODO: 读取到共享内存
    // if (x < width && y < height) {
    //     tile[threadIdx.y][threadIdx.x] = input[y * width + x];
    // }

    // __syncthreads();

    // TODO: 计算转置后的位置
    // int x_transpose = blockIdx.y * TILE_SIZE + threadIdx.x;
    // int y_transpose = blockIdx.x * TILE_SIZE + threadIdx.y;

    // TODO: 写入到输出
    // if (x_transpose < height && y_transpose < width) {
    //     output[y_transpose * height + x_transpose] = tile[threadIdx.x][threadIdx.y];
    // }
}

int main() {
    float *h_input, *h_output, *d_input, *d_output;
    size_t bytes = WIDTH * HEIGHT * sizeof(float);

    h_input = (float*)malloc(bytes);
    h_output = (float*)malloc(bytes);

    // 初始化
    for (int i = 0; i < HEIGHT; i++) {
        for (int j = 0; j < WIDTH; j++) {
            h_input[i * WIDTH + j] = i * WIDTH + j;
        }
    }

    CUDA_CHECK(cudaMalloc(&d_input, bytes));
    CUDA_CHECK(cudaMalloc(&d_output, bytes));
    CUDA_CHECK(cudaMemcpy(d_input, h_input, bytes, cudaMemcpyHostToDevice));

    dim3 blockDim(TILE_SIZE, TILE_SIZE);
    dim3 gridDim((WIDTH + TILE_SIZE - 1) / TILE_SIZE,
                 (HEIGHT + TILE_SIZE - 1) / TILE_SIZE);

    transpose_shared<<<gridDim, blockDim>>>(d_input, d_output, WIDTH, HEIGHT);
    CUDA_CHECK(cudaDeviceSynchronize());

    CUDA_CHECK(cudaMemcpy(h_output, d_output, bytes, cudaMemcpyDeviceToHost));

    // 验证
    bool success = true;
    for (int i = 0; i < HEIGHT; i++) {
        for (int j = 0; j < WIDTH; j++) {
            float expected = j * HEIGHT + i;
            if (h_output[i * HEIGHT + j] != expected) {
                printf("错误 at (%d, %d)\n", i, j);
                success = false;
                break;
            }
        }
        if (!success) break;
    }

    CUDA_CHECK(cudaFree(d_input));
    CUDA_CHECK(cudaFree(d_output));
    free(h_input);
    free(h_output);

    if (success) {
        printf("共享内存矩阵转置正确!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}

// I AM NOT DONE
