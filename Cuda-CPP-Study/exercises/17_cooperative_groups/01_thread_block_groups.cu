// 练习 171: Cooperative Groups - Thread Block
//
// 目标: 使用 Cooperative Groups 改进线程协作
//
// 任务:
// 1. 理解 thread_block 和 thread_group
// 2. 使用 cooperative groups 实现 reduction
// 3. 对比传统 __syncthreads()

#include <stdio.h>
#include <cuda_runtime.h>
#include <cooperative_groups.h>

namespace cg = cooperative_groups;

#define N 1024
#define BLOCK_SIZE 256

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// 传统 reduction (使用 __syncthreads)
__global__ void traditional_reduce(float *input, float *output, int n) {
    __shared__ float sdata[BLOCK_SIZE];

    int tid = threadIdx.x;
    int i = blockIdx.x * blockDim.x + threadIdx.x;

    sdata[tid] = (i < n) ? input[i] : 0.0f;
    __syncthreads();

    for (int s = blockDim.x / 2; s > 0; s >>= 1) {
        if (tid < s) {
            sdata[tid] += sdata[tid + s];
        }
        __syncthreads();
    }

    if (tid == 0) {
        output[blockIdx.x] = sdata[0];
    }
}

// TODO: 使用 Cooperative Groups 实现 reduction
__global__ void cg_reduce(float *input, float *output, int n) {
    __shared__ float sdata[BLOCK_SIZE];

    // TODO: 获取 thread block group
    // cg::thread_block block = cg::this_thread_block();

    int tid = threadIdx.x;
    int i = blockIdx.x * blockDim.x + threadIdx.x;

    sdata[tid] = (i < n) ? input[i] : 0.0f;
    // TODO: 使用 block.sync() 替代 __syncthreads()
    // block.sync();

    // TODO: 使用 cooperative groups 进行 reduction
    // for (int s = block.size() / 2; s > 0; s >>= 1) {
    //     if (tid < s) {
    //         sdata[tid] += sdata[tid + s];
    //     }
    //     block.sync();
    // }

    // if (block.thread_rank() == 0) {
    //     output[blockIdx.x] = sdata[0];
    // }
}

int main() {
    printf("Cooperative Groups Thread Block 测试\n\n");

    float *h_input = (float*)malloc(N * sizeof(float));
    float *h_output = (float*)malloc((N / BLOCK_SIZE) * sizeof(float));

    // 初始化为1, 便于验证
    for (int i = 0; i < N; i++) {
        h_input[i] = 1.0f;
    }

    float *d_input, *d_output;
    CUDA_CHECK(cudaMalloc(&d_input, N * sizeof(float)));
    CUDA_CHECK(cudaMalloc(&d_output, (N / BLOCK_SIZE) * sizeof(float)));

    CUDA_CHECK(cudaMemcpy(d_input, h_input, N * sizeof(float), cudaMemcpyHostToDevice));

    dim3 blockDim(BLOCK_SIZE);
    dim3 gridDim(N / BLOCK_SIZE);

    // 测试传统方法
    traditional_reduce<<<gridDim, blockDim>>>(d_input, d_output, N);
    CUDA_CHECK(cudaDeviceSynchronize());

    CUDA_CHECK(cudaMemcpy(h_output, d_output, (N / BLOCK_SIZE) * sizeof(float),
                          cudaMemcpyDeviceToHost));

    float sum1 = 0.0f;
    for (int i = 0; i < N / BLOCK_SIZE; i++) {
        sum1 += h_output[i];
    }

    printf("传统方法结果: %.0f (期望: %d)\n", sum1, N);

    // TODO: 测试 Cooperative Groups 方法
    // cg_reduce<<<gridDim, blockDim>>>(d_input, d_output, N);
    // CUDA_CHECK(cudaDeviceSynchronize());

    // CUDA_CHECK(cudaMemcpy(h_output, d_output, (N / BLOCK_SIZE) * sizeof(float),
    //                       cudaMemcpyDeviceToHost));

    // float sum2 = 0.0f;
    // for (int i = 0; i < N / BLOCK_SIZE; i++) {
    //     sum2 += h_output[i];
    // }

    // printf("Cooperative Groups 结果: %.0f (期望: %d)\n", sum2, N);

    CUDA_CHECK(cudaFree(d_input));
    CUDA_CHECK(cudaFree(d_output));
    free(h_input);
    free(h_output);

    printf("\nCooperative Groups 基础测试完成!\n");
    printf("TEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
