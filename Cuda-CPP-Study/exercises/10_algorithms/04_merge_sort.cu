/**
 * 练习 104: 并行归并排序
 * 学习目标: 实现 GPU 归并排序算法
 */

#include <cuda_runtime.h>
#include <stdio.h>

__global__ void merge_kernel(int *input, int *output, int n, int width) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    int start = 2 * tid * width;

    if (start >= n) return;

    int mid = min(start + width, n);
    int end = min(start + 2 * width, n);

    // TODO: 实现归并逻辑
}

int main() {
    printf("=== 并行归并排序 ===\n");
    printf("任务: 实现 Bottom-Up Merge Sort\n");
    return 0;
}
