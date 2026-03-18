// 练习 91: 归约操作
//
// 目标: 实现高效的并行归约（求和）
//
// 任务:
// 1. 使用共享内存实现归约
// 2. 避免 warp 分化
// 3. 优化 bank 冲突

#include <stdio.h>
#include <cuda_runtime.h>

#define N 1048576  // 1M 元素
#define BLOCK_SIZE 256

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// TODO: 实现高效的归约 kernel
__global__ void reduce_sum(float *input, float *output, int n) {
    __shared__ float sdata[BLOCK_SIZE];

    int tid = threadIdx.x;
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    // TODO: 加载数据到共享内存
    // sdata[tid] = (idx < n) ? input[idx] : 0.0f;
    // __syncthreads();

    // TODO: 树形归约
    // for (unsigned int s = blockDim.x / 2; s > 0; s >>= 1) {
    //     if (tid < s) {
    //         sdata[tid] += sdata[tid + s];
    //     }
    //     __syncthreads();
    // }

    // TODO: 第一个线程写入结果
    // if (tid == 0) {
    //     output[blockIdx.x] = sdata[0];
    // }
}

int main() {
    float *h_input, *h_output;
    float *d_input, *d_output;
    size_t bytes = N * sizeof(float);

    h_input = (float*)malloc(bytes);

    // 初始化为 1，总和应该是 N
    for (int i = 0; i < N; i++) {
        h_input[i] = 1.0f;
    }

    int num_blocks = (N + BLOCK_SIZE - 1) / BLOCK_SIZE;
    h_output = (float*)malloc(num_blocks * sizeof(float));

    CUDA_CHECK(cudaMalloc(&d_input, bytes));
    CUDA_CHECK(cudaMalloc(&d_output, num_blocks * sizeof(float)));

    CUDA_CHECK(cudaMemcpy(d_input, h_input, bytes, cudaMemcpyHostToDevice));

    // 第一次归约
    reduce_sum<<<num_blocks, BLOCK_SIZE>>>(d_input, d_output, N);
    CUDA_CHECK(cudaDeviceSynchronize());

    CUDA_CHECK(cudaMemcpy(h_output, d_output, num_blocks * sizeof(float), cudaMemcpyDeviceToHost));

    // CPU 端完成最终归约
    float total = 0.0f;
    for (int i = 0; i < num_blocks; i++) {
        total += h_output[i];
    }

    printf("归约结果: %.0f (期望: %d)\n", total, N);

    bool success = (fabsf(total - N) < 0.1f);

    CUDA_CHECK(cudaFree(d_input));
    CUDA_CHECK(cudaFree(d_output));
    free(h_input);
    free(h_output);

    if (success) {
        printf("归约计算正确!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}

// I AM NOT DONE
