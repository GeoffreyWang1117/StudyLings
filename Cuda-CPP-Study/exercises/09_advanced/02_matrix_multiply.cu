// 练习 92: 矩阵乘法
//
// 目标: 使用共享内存实现高效的矩阵乘法
//
// 任务:
// 1. 实现基础矩阵乘法 C = A * B
// 2. 使用分块（tiling）技术
// 3. 利用共享内存减少全局内存访问

#include <stdio.h>
#include <cuda_runtime.h>

#define WIDTH 512
#define TILE_SIZE 16

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// TODO: 实现使用共享内存的矩阵乘法
__global__ void matrix_multiply(float *A, float *B, float *C, int width) {
    __shared__ float tile_A[TILE_SIZE][TILE_SIZE];
    __shared__ float tile_B[TILE_SIZE][TILE_SIZE];

    int row = blockIdx.y * TILE_SIZE + threadIdx.y;
    int col = blockIdx.x * TILE_SIZE + threadIdx.x;

    float sum = 0.0f;

    // TODO: 遍历所有 tiles
    // for (int t = 0; t < width / TILE_SIZE; t++) {
    //     // 加载 tile 到共享内存
    //     tile_A[threadIdx.y][threadIdx.x] = A[row * width + t * TILE_SIZE + threadIdx.x];
    //     tile_B[threadIdx.y][threadIdx.x] = B[(t * TILE_SIZE + threadIdx.y) * width + col];
    //
    //     __syncthreads();
    //
    //     // 计算部分乘积
    //     for (int k = 0; k < TILE_SIZE; k++) {
    //         sum += tile_A[threadIdx.y][k] * tile_B[k][threadIdx.x];
    //     }
    //
    //     __syncthreads();
    // }

    // TODO: 写入结果
    // if (row < width && col < width) {
    //     C[row * width + col] = sum;
    // }
}

// CPU 参考实现
void matrix_multiply_cpu(float *A, float *B, float *C, int width) {
    for (int i = 0; i < width; i++) {
        for (int j = 0; j < width; j++) {
            float sum = 0.0f;
            for (int k = 0; k < width; k++) {
                sum += A[i * width + k] * B[k * width + j];
            }
            C[i * width + j] = sum;
        }
    }
}

int main() {
    float *h_A, *h_B, *h_C, *h_C_ref;
    float *d_A, *d_B, *d_C;
    size_t bytes = WIDTH * WIDTH * sizeof(float);

    h_A = (float*)malloc(bytes);
    h_B = (float*)malloc(bytes);
    h_C = (float*)malloc(bytes);
    h_C_ref = (float*)malloc(bytes);

    // 初始化矩阵
    for (int i = 0; i < WIDTH * WIDTH; i++) {
        h_A[i] = 1.0f;
        h_B[i] = 1.0f;
    }

    // 计算 CPU 参考结果（小矩阵）
    if (WIDTH <= 64) {
        matrix_multiply_cpu(h_A, h_B, h_C_ref, WIDTH);
    }

    CUDA_CHECK(cudaMalloc(&d_A, bytes));
    CUDA_CHECK(cudaMalloc(&d_B, bytes));
    CUDA_CHECK(cudaMalloc(&d_C, bytes));

    CUDA_CHECK(cudaMemcpy(d_A, h_A, bytes, cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_B, h_B, bytes, cudaMemcpyHostToDevice));

    dim3 blockDim(TILE_SIZE, TILE_SIZE);
    dim3 gridDim(WIDTH / TILE_SIZE, WIDTH / TILE_SIZE);

    matrix_multiply<<<gridDim, blockDim>>>(d_A, d_B, d_C, WIDTH);
    CUDA_CHECK(cudaDeviceSynchronize());

    CUDA_CHECK(cudaMemcpy(h_C, d_C, bytes, cudaMemcpyDeviceToHost));

    // 验证（简单检查：所有元素应该是 WIDTH）
    bool success = true;
    float expected = (float)WIDTH;
    for (int i = 0; i < WIDTH * WIDTH; i++) {
        if (fabsf(h_C[i] - expected) > 0.1f) {
            printf("错误 at %d: got %f, expected %f\n", i, h_C[i], expected);
            success = false;
            break;
        }
    }

    CUDA_CHECK(cudaFree(d_A));
    CUDA_CHECK(cudaFree(d_B));
    CUDA_CHECK(cudaFree(d_C));
    free(h_A);
    free(h_B);
    free(h_C);
    free(h_C_ref);

    if (success) {
        printf("矩阵乘法正确!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}

// I AM NOT DONE
