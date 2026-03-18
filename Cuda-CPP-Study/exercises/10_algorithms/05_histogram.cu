/**
 * 练习 105: 并行直方图统计
 * 学习目标: 使用原子操作实现高效直方图
 */

#include <cuda_runtime.h>
#include <stdio.h>

__global__ void histogram_atomic(unsigned char *data, int *hist, int n, int num_bins) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;

    if (tid < n) {
        int bin = data[tid] * num_bins / 256;
        atomicAdd(&hist[bin], 1);
    }
}

int main() {
    printf("=== 并行直方图 ===\n");
    printf("任务: 实现直方图统计\n");
    return 0;
}
