// 参考答案 41: 共享内存基础

#include <stdio.h>
#include <cuda_runtime.h>

#define BLOCK_SIZE 256

__global__ void block_sum(float *input, float *output, int n) {
    __shared__ float shared_data[BLOCK_SIZE];

    int tid = threadIdx.x;
    int global_idx = blockIdx.x * blockDim.x + tid;

    // 加载数据到共享内存
    if (global_idx < n) {
        shared_data[tid] = input[global_idx];
    } else {
        shared_data[tid] = 0.0f;
    }

    __syncthreads();

    // 树形归约
    for (int stride = blockDim.x / 2; stride > 0; stride >>= 1) {
        if (tid < stride) {
            shared_data[tid] += shared_data[tid + stride];
        }
        __syncthreads();
    }

    // 第一个线程写入结果
    if (tid == 0) {
        output[blockIdx.x] = shared_data[0];
    }
}

int main() {
    const int N = 1024;
    float *h_input, *h_output;
    float *d_input, *d_output;

    h_input = (float*)malloc(N * sizeof(float));
    int num_blocks = (N + BLOCK_SIZE - 1) / BLOCK_SIZE;
    h_output = (float*)malloc(num_blocks * sizeof(float));

    for (int i = 0; i < N; i++) {
        h_input[i] = 1.0f;
    }

    cudaMalloc(&d_input, N * sizeof(float));
    cudaMalloc(&d_output, num_blocks * sizeof(float));

    cudaMemcpy(d_input, h_input, N * sizeof(float), cudaMemcpyHostToDevice);

    block_sum<<<num_blocks, BLOCK_SIZE>>>(d_input, d_output, N);
    cudaDeviceSynchronize();

    cudaMemcpy(h_output, d_output, num_blocks * sizeof(float), cudaMemcpyDeviceToHost);

    // 验证
    bool success = true;
    for (int i = 0; i < num_blocks; i++) {
        float expected = (i == num_blocks - 1 && N % BLOCK_SIZE != 0) ?
                         (N % BLOCK_SIZE) : BLOCK_SIZE;
        if (h_output[i] != expected) {
            printf("错误: block %d sum = %f, 期望 %f\n", i, h_output[i], expected);
            success = false;
            break;
        }
    }

    cudaFree(d_input);
    cudaFree(d_output);
    free(h_input);
    free(h_output);

    if (success) {
        printf("共享内存求和正确!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}
