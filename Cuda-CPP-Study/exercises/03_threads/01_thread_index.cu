// 练习 16: 理解线程索引
//
// 目标: 掌握如何计算全局线程ID
//
// 任务:
// 1. 理解 blockIdx, blockDim, threadIdx 的关系
// 2. 计算一维全局索引
// 3. 使用多个 block

#include <stdio.h>
#include <cuda_runtime.h>

#define N 256
#define THREADS_PER_BLOCK 64

// TODO: 完成这个 kernel
// 每个线程应该将其全局ID写入数组
__global__ void print_indices(int *indices) {
    // TODO: 计算全局线程索引
    // 公式: global_idx = blockIdx.x * blockDim.x + threadIdx.x
    int global_idx = 0; // 修改这里

    // 将索引写入数组
    if (global_idx < N) {
        indices[global_idx] = global_idx;
    }
}

int main() {
    int *h_indices, *d_indices;
    size_t bytes = N * sizeof(int);

    h_indices = (int*)malloc(bytes);
    cudaMalloc(&d_indices, bytes);

    // TODO: 计算需要多少个 block
    int num_blocks = 1; // 修改这里

    // 调用 kernel
    print_indices<<<num_blocks, THREADS_PER_BLOCK>>>(d_indices);
    cudaDeviceSynchronize();

    // 拷贝结果
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

// I AM NOT DONE
