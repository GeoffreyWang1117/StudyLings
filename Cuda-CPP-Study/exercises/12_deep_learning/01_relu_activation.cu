// 练习 121: ReLU 激活函数
//
// 目标: 实现 ReLU 及其反向传播
//
// 任务:
// 1. 实现 ReLU forward: f(x) = max(0, x)
// 2. 实现 ReLU backward: df/dx = x > 0 ? 1 : 0
// 3. 融合前向和反向计算

#include <stdio.h>
#include <cuda_runtime.h>

#define N 1000000
#define BLOCK_SIZE 256

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// TODO: 实现 ReLU forward
__global__ void relu_forward(float *input, float *output, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    // if (idx < n) {
    //     output[idx] = fmaxf(0.0f, input[idx]);
    // }
}

// TODO: 实现 ReLU backward
__global__ void relu_backward(float *input, float *grad_output, float *grad_input, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    // if (idx < n) {
    //     grad_input[idx] = (input[idx] > 0.0f) ? grad_output[idx] : 0.0f;
    // }
}

// TODO: 融合版本：同时保存 forward 结果和计算 backward
__global__ void relu_forward_backward(float *input, float *output,
                                       float *grad_output, float *grad_input, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        // Forward
        float val = input[idx];
        output[idx] = fmaxf(0.0f, val);

        // Backward (如果有梯度输入)
        if (grad_output != nullptr) {
            grad_input[idx] = (val > 0.0f) ? grad_output[idx] : 0.0f;
        }
    }
}

int main() {
    float *h_input, *h_output, *h_grad_out, *h_grad_in;
    float *d_input, *d_output, *d_grad_out, *d_grad_in;
    size_t bytes = N * sizeof(float);

    h_input = (float*)malloc(bytes);
    h_output = (float*)malloc(bytes);
    h_grad_out = (float*)malloc(bytes);
    h_grad_in = (float*)malloc(bytes);

    // 初始化输入（包含正负值）
    for (int i = 0; i < N; i++) {
        h_input[i] = (float)i - N / 2;  // -500000 到 500000
        h_grad_out[i] = 1.0f;  // 假设上游梯度为1
    }

    CUDA_CHECK(cudaMalloc(&d_input, bytes));
    CUDA_CHECK(cudaMalloc(&d_output, bytes));
    CUDA_CHECK(cudaMalloc(&d_grad_out, bytes));
    CUDA_CHECK(cudaMalloc(&d_grad_in, bytes));

    CUDA_CHECK(cudaMemcpy(d_input, h_input, bytes, cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_grad_out, h_grad_out, bytes, cudaMemcpyHostToDevice));

    int grid_size = (N + BLOCK_SIZE - 1) / BLOCK_SIZE;

    // Forward pass
    relu_forward<<<grid_size, BLOCK_SIZE>>>(d_input, d_output, N);

    // Backward pass
    relu_backward<<<grid_size, BLOCK_SIZE>>>(d_input, d_grad_out, d_grad_in, N);

    CUDA_CHECK(cudaDeviceSynchronize());

    CUDA_CHECK(cudaMemcpy(h_output, d_output, bytes, cudaMemcpyDeviceToHost));
    CUDA_CHECK(cudaMemcpy(h_grad_in, d_grad_in, bytes, cudaMemcpyDeviceToHost));

    // 验证
    bool success = true;
    for (int i = 0; i < N; i++) {
        // Forward check
        float expected_out = (h_input[i] > 0.0f) ? h_input[i] : 0.0f;
        if (fabsf(h_output[i] - expected_out) > 1e-5) {
            printf("Forward错误 at %d\n", i);
            success = false;
            break;
        }

        // Backward check
        float expected_grad = (h_input[i] > 0.0f) ? 1.0f : 0.0f;
        if (fabsf(h_grad_in[i] - expected_grad) > 1e-5) {
            printf("Backward错误 at %d\n", i);
            success = false;
            break;
        }
    }

    CUDA_CHECK(cudaFree(d_input));
    CUDA_CHECK(cudaFree(d_output));
    CUDA_CHECK(cudaFree(d_grad_out));
    CUDA_CHECK(cudaFree(d_grad_in));
    free(h_input);
    free(h_output);
    free(h_grad_out);
    free(h_grad_in);

    if (success) {
        printf("ReLU forward & backward 正确!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}

// I AM NOT DONE
