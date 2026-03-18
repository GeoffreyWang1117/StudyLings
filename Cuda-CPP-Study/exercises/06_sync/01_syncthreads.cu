// 练习 56: __syncthreads() 基础
//
// 目标: 理解和使用 __syncthreads()
//
// 任务:
// 1. 使用 __syncthreads() 同步 block 内所有线程
// 2. 实现需要同步的算法
// 3. 理解同步的必要性

#include <stdio.h>
#include <cuda_runtime.h>

#define N 256
#define BLOCK_SIZE 256

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// TODO: 实现反转数组的 kernel
// 使用共享内存和同步
__global__ void reverse_array(int *input, int *output, int n) {
    __shared__ int temp[BLOCK_SIZE];

    int tid = threadIdx.x;
    int idx = blockIdx.x * blockDim.x + tid;

    // TODO: 加载到共享内存
    // if (idx < n) {
    //     temp[tid] = input[idx];
    // }

    // TODO: 同步！确保所有线程都加载完成
    // __syncthreads();

    // TODO: 写入反转位置
    // if (idx < n) {
    //     output[idx] = temp[blockDim.x - 1 - tid];
    // }
}

int main() {
    int *h_input, *h_output;
    int *d_input, *d_output;
    size_t bytes = N * sizeof(int);

    h_input = (int*)malloc(bytes);
    h_output = (int*)malloc(bytes);

    // 初始化
    for (int i = 0; i < N; i++) {
        h_input[i] = i;
    }

    CUDA_CHECK(cudaMalloc(&d_input, bytes));
    CUDA_CHECK(cudaMalloc(&d_output, bytes));
    CUDA_CHECK(cudaMemcpy(d_input, h_input, bytes, cudaMemcpyHostToDevice));

    reverse_array<<<1, BLOCK_SIZE>>>(d_input, d_output, N);
    CUDA_CHECK(cudaDeviceSynchronize());

    CUDA_CHECK(cudaMemcpy(h_output, d_output, bytes, cudaMemcpyDeviceToHost));

    // 验证
    bool success = true;
    for (int i = 0; i < N; i++) {
        int expected = N - 1 - i;
        if (h_output[i] != expected) {
            printf("错误 at %d: got %d, expected %d\n", i, h_output[i], expected);
            success = false;
            break;
        }
    }

    CUDA_CHECK(cudaFree(d_input));
    CUDA_CHECK(cudaFree(d_output));
    free(h_input);
    free(h_output);

    if (success) {
        printf("同步使用正确!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}

// I AM NOT DONE
