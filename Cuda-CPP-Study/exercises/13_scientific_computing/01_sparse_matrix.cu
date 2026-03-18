// 练习 131: 稀疏矩阵向量乘法 (SpMV)
//
// 目标: 实现 CSR 格式的稀疏矩阵乘法
//
// 任务:
// 1. 理解 CSR (Compressed Sparse Row) 格式
// 2. 实现 y = A * x (A 是稀疏矩阵)
// 3. 优化 warp 级别的访问

#include <stdio.h>
#include <cuda_runtime.h>

#define N 1000      // 矩阵大小
#define NNZ 5000    // 非零元素数量
#define BLOCK_SIZE 256

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// CSR 格式说明:
// values[NNZ]: 非零元素的值
// col_indices[NNZ]: 每个非零元素的列索引
// row_ptr[N+1]: 每行的起始位置

// TODO: 实现 CSR SpMV
__global__ void spmv_csr(int *row_ptr, int *col_indices, float *values,
                         float *x, float *y, int num_rows) {
    int row = blockIdx.x * blockDim.x + threadIdx.x;

    if (row < num_rows) {
        float sum = 0.0f;

        // TODO: 遍历该行的所有非零元素
        // int row_start = row_ptr[row];
        // int row_end = row_ptr[row + 1];
        //
        // for (int i = row_start; i < row_end; i++) {
        //     int col = col_indices[i];
        //     sum += values[i] * x[col];
        // }
        //
        // y[row] = sum;
    }
}

// 生成稀疏矩阵（CSR 格式）
void generate_sparse_matrix(int *row_ptr, int *col_indices, float *values,
                            int num_rows, int nnz) {
    int elements_per_row = nnz / num_rows;

    row_ptr[0] = 0;
    for (int i = 0; i < num_rows; i++) {
        row_ptr[i + 1] = row_ptr[i] + elements_per_row;
    }

    for (int i = 0; i < nnz; i++) {
        col_indices[i] = rand() % num_rows;
        values[i] = (float)rand() / RAND_MAX;
    }
}

int main() {
    int *h_row_ptr, *h_col_indices;
    float *h_values, *h_x, *h_y;
    int *d_row_ptr, *d_col_indices;
    float *d_values, *d_x, *d_y;

    h_row_ptr = (int*)malloc((N + 1) * sizeof(int));
    h_col_indices = (int*)malloc(NNZ * sizeof(int));
    h_values = (float*)malloc(NNZ * sizeof(float));
    h_x = (float*)malloc(N * sizeof(float));
    h_y = (float*)malloc(N * sizeof(float));

    // 生成稀疏矩阵
    generate_sparse_matrix(h_row_ptr, h_col_indices, h_values, N, NNZ);

    // 初始化向量 x
    for (int i = 0; i < N; i++) {
        h_x[i] = 1.0f;
    }

    CUDA_CHECK(cudaMalloc(&d_row_ptr, (N + 1) * sizeof(int)));
    CUDA_CHECK(cudaMalloc(&d_col_indices, NNZ * sizeof(int)));
    CUDA_CHECK(cudaMalloc(&d_values, NNZ * sizeof(float)));
    CUDA_CHECK(cudaMalloc(&d_x, N * sizeof(float)));
    CUDA_CHECK(cudaMalloc(&d_y, N * sizeof(float)));

    CUDA_CHECK(cudaMemcpy(d_row_ptr, h_row_ptr, (N + 1) * sizeof(int), cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_col_indices, h_col_indices, NNZ * sizeof(int), cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_values, h_values, NNZ * sizeof(float), cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_x, h_x, N * sizeof(float), cudaMemcpyHostToDevice));

    int grid_size = (N + BLOCK_SIZE - 1) / BLOCK_SIZE;
    spmv_csr<<<grid_size, BLOCK_SIZE>>>(d_row_ptr, d_col_indices, d_values, d_x, d_y, N);
    CUDA_CHECK(cudaDeviceSynchronize());

    CUDA_CHECK(cudaMemcpy(h_y, d_y, N * sizeof(float), cudaMemcpyDeviceToHost));

    // 简单验证：结果不应该全为0
    bool success = false;
    for (int i = 0; i < N; i++) {
        if (h_y[i] > 0.0f) {
            success = true;
            break;
        }
    }

    printf("结果样本: y[0] = %f, y[1] = %f\n", h_y[0], h_y[1]);

    CUDA_CHECK(cudaFree(d_row_ptr));
    CUDA_CHECK(cudaFree(d_col_indices));
    CUDA_CHECK(cudaFree(d_values));
    CUDA_CHECK(cudaFree(d_x));
    CUDA_CHECK(cudaFree(d_y));
    free(h_row_ptr);
    free(h_col_indices);
    free(h_values);
    free(h_x);
    free(h_y);

    if (success) {
        printf("稀疏矩阵乘法完成!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}

// I AM NOT DONE
