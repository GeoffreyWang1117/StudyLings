// 练习 43: 1D 模板操作
//
// 目标: 使用共享内存实现 1D 模板（stencil）计算
//
// 任务:
// 1. 实现 1D 模板：output[i] = input[i-1] + input[i] + input[i+1]
// 2. 使用共享内存减少全局内存访问
// 3. 处理边界条件

#include <stdio.h>
#include <cuda_runtime.h>

#define N 10000
#define BLOCK_SIZE 256
#define RADIUS 1  // 模板半径

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// TODO: 实现 1D 模板 kernel
__global__ void stencil_1d(float *input, float *output, int n) {
    // TODO: 声明共享内存（需要包含 halo 区域）
    // __shared__ float temp[BLOCK_SIZE + 2 * RADIUS];

    int global_idx = blockIdx.x * blockDim.x + threadIdx.x;
    int local_idx = threadIdx.x + RADIUS;

    // TODO: 加载数据到共享内存
    // 1. 加载主要数据
    // if (global_idx < n) {
    //     temp[local_idx] = input[global_idx];
    // }

    // 2. 加载左 halo
    // if (threadIdx.x < RADIUS) {
    //     if (global_idx >= RADIUS) {
    //         temp[local_idx - RADIUS] = input[global_idx - RADIUS];
    //     } else {
    //         temp[local_idx - RADIUS] = 0.0f;
    //     }
    // }

    // 3. 加载右 halo
    // if (threadIdx.x >= blockDim.x - RADIUS) {
    //     if (global_idx + RADIUS < n) {
    //         temp[local_idx + RADIUS] = input[global_idx + RADIUS];
    //     } else {
    //         temp[local_idx + RADIUS] = 0.0f;
    //     }
    // }

    // __syncthreads();

    // TODO: 计算模板结果
    // if (global_idx < n) {
    //     float result = 0.0f;
    //     for (int offset = -RADIUS; offset <= RADIUS; offset++) {
    //         result += temp[local_idx + offset];
    //     }
    //     output[global_idx] = result;
    // }
}

int main() {
    float *h_input, *h_output;
    float *d_input, *d_output;
    size_t bytes = N * sizeof(float);

    h_input = (float*)malloc(bytes);
    h_output = (float*)malloc(bytes);

    // 初始化为 1
    for (int i = 0; i < N; i++) {
        h_input[i] = 1.0f;
    }

    CUDA_CHECK(cudaMalloc(&d_input, bytes));
    CUDA_CHECK(cudaMalloc(&d_output, bytes));
    CUDA_CHECK(cudaMemcpy(d_input, h_input, bytes, cudaMemcpyHostToDevice));

    int grid_size = (N + BLOCK_SIZE - 1) / BLOCK_SIZE;
    stencil_1d<<<grid_size, BLOCK_SIZE>>>(d_input, d_output, N);
    CUDA_CHECK(cudaDeviceSynchronize());

    CUDA_CHECK(cudaMemcpy(h_output, d_output, bytes, cudaMemcpyDeviceToHost));

    // 验证：大部分元素应该是 3.0
    bool success = true;
    for (int i = 1; i < N - 1; i++) {
        float expected = 3.0f;  // 1 + 1 + 1
        if (fabsf(h_output[i] - expected) > 1e-5) {
            printf("错误 at %d: got %f, expected %f\n", i, h_output[i], expected);
            success = false;
            break;
        }
    }

    CUDA_CHECK(cudaFree(d_input));
    CUDA_CHECK(cudaFree(d_output));
    free(h_input);
    free(h_output);

    if (success) {
        printf("1D 模板计算正确!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}

// I AM NOT DONE
