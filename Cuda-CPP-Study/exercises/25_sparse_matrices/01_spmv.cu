/**
 * 练习 251: 稀疏矩阵-向量乘法 (SpMV)
 * 学习目标: 实现 CSR 格式的 SpMV, 理解稀疏矩阵优化
 */

#include <cuda_runtime.h>
#include <stdio.h>

__global__ void spmv_csr(int *row_ptr, int *col_ind, float *values,
                          float *x, float *y, int num_rows) {
    int row = blockIdx.x * blockDim.x + threadIdx.x;
    if (row >= num_rows) return;

    float sum = 0.0f;
    for (int i = row_ptr[row]; i < row_ptr[row + 1]; i++) {
        sum += values[i] * x[col_ind[i]];
    }
    y[row] = sum;
}

int main() {
    printf("=== 稀疏矩阵-向量乘法 (SpMV) ===\n");
    printf("任务: 实现 CSR 格式的 SpMV\n");
    return 0;
}
