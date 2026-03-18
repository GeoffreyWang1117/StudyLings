// 参考答案 16: 理解线程索引

#include <stdio.h>
#include <cuda_runtime.h>

#define N 256
#define THREADS_PER_BLOCK 64

__global__ void print_indices(int *indices) {
    // 计算全局线程索引
    int global_idx = blockIdx.x * blockDim.x + threadIdx.x;

    if (global_idx < N) {
        indices[global_idx] = global_idx;
    }
}

int main() {
    int *h_indices, *d_indices;
    size_t bytes = N * sizeof(int);

    h_indices = (int*)malloc(bytes);
    cudaMalloc(&d_indices, bytes);

    // 计算需要的 block 数量
    int num_blocks = (N + THREADS_PER_BLOCK - 1) / THREADS_PER_BLOCK;

    // 调用 kernel
    print_indices<<<num_blocks, THREADS_PER_BLOCK>>>(d_indices);
    cudaDeviceSynchronize();

    cudaMemcpy(h_indices, d_indices, bytes, cudaMemcpyDeviceToHost);

    // 验证
    bool success = true;
    for (int i = 0; i < N; i++) {
        if (h_indices[i] != i) {
            printf("错误: indices[%d] = %d, 期望 %d\n", i, h_indices[i], i);
            success = false;
            break;
        }
    }

    cudaFree(d_indices);
    free(h_indices);

    if (success) {
        printf("线程索引计算正确!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}
