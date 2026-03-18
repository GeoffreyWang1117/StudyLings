// 练习 10: 元素级操作
//
// 目标: 实现向量的元素级操作
//
// 任务:
// 1. 实现 sigmoid 函数: f(x) = 1 / (1 + exp(-x))
// 2. 使用数学函数库
// 3. 处理边界情况

#include <stdio.h>
#include <cuda_runtime.h>
#include <math.h>

#define N 1000
#define BLOCK_SIZE 256

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// TODO: 实现 sigmoid kernel
// 提示: 使用 expf() 函数
__global__ void sigmoid(float *input, float *output, int n) {
    // int idx = blockIdx.x * blockDim.x + threadIdx.x;

    // if (idx < n) {
    //     output[idx] = 1.0f / (1.0f + expf(-input[idx]));
    // }
}

// CPU 参考实现
float sigmoid_cpu(float x) {
    return 1.0f / (1.0f + expf(-x));
}

int main() {
    float *h_input, *h_output;
    float *d_input, *d_output;
    size_t bytes = N * sizeof(float);

    h_input = (float*)malloc(bytes);
    h_output = (float*)malloc(bytes);

    // 初始化: 范围 [-5, 5]
    for (int i = 0; i < N; i++) {
        h_input[i] = -5.0f + (10.0f * i / N);
    }

    CUDA_CHECK(cudaMalloc(&d_input, bytes));
    CUDA_CHECK(cudaMalloc(&d_output, bytes));

    CUDA_CHECK(cudaMemcpy(d_input, h_input, bytes, cudaMemcpyHostToDevice));

    int grid_size = (N + BLOCK_SIZE - 1) / BLOCK_SIZE;
    sigmoid<<<grid_size, BLOCK_SIZE>>>(d_input, d_output, N);
    CUDA_CHECK(cudaDeviceSynchronize());

    CUDA_CHECK(cudaMemcpy(h_output, d_output, bytes, cudaMemcpyDeviceToHost));

    // 验证
    bool success = true;
    for (int i = 0; i < N; i++) {
        float expected = sigmoid_cpu(h_input[i]);
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
        printf("Sigmoid 计算正确!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}

// I AM NOT DONE
