/**
 * 练习 242: GPU PageRank 算法
 *
 * 学习目标：
 * - 实现并行 PageRank 算法
 * - 理解迭代图算法的 GPU 优化
 * - 处理图的稀疏矩阵运算
 */

#include <cuda_runtime.h>
#include <stdio.h>
#include <math.h>

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// TODO: PageRank 迭代 Kernel
__global__ void pagerank_kernel(int *row_offsets, int *column_indices,
                                 float *old_ranks, float *new_ranks,
                                 int *out_degrees, int num_nodes, float damping) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    if (tid >= num_nodes) return;

    float sum = 0.0f;

    // 累加所有指向当前节点的贡献
    int start = row_offsets[tid];
    int end = row_offsets[tid + 1];

    for (int i = start; i < end; i++) {
        int neighbor = column_indices[i];
        sum += old_ranks[neighbor] / out_degrees[neighbor];
    }

    new_ranks[tid] = (1.0f - damping) / num_nodes + damping * sum;
}

// TODO: 计算误差
__global__ void compute_error(float *old_ranks, float *new_ranks, float *errors,
                               int num_nodes) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    if (tid >= num_nodes) return;

    errors[tid] = fabsf(new_ranks[tid] - old_ranks[tid]);
}

int main() {
    printf("=== GPU PageRank 实现 ===\n");
    printf("任务: 实现完整的 PageRank 算法\n");
    printf("提示: 使用迭代方法直到收敛\n");

    return 0;
}

/**
 * 编译: nvcc -o pagerank 02_pagerank.cu
 * 知识点: PageRank, 迭代收敛, 稀疏矩阵乘法
 */
