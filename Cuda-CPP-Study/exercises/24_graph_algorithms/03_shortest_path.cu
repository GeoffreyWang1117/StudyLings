/**
 * 练习 243: GPU 最短路径 (Single-Source Shortest Path)
 *
 * 学习目标：
 * - 实现 GPU 加速的 Bellman-Ford 或 Dijkstra 算法
 * - 理解边松弛操作的并行化
 */

#include <cuda_runtime.h>
#include <stdio.h>
#include <limits.h>

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// TODO: Bellman-Ford 边松弛 Kernel
__global__ void bellman_ford_kernel(int *row_offsets, int *column_indices,
                                     float *weights, float *distances,
                                     bool *updated, int num_nodes) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    if (tid >= num_nodes) return;

    // 对每个节点的所有出边进行松弛
    int start = row_offsets[tid];
    int end = row_offsets[tid + 1];

    for (int i = start; i < end; i++) {
        int neighbor = column_indices[i];
        float new_dist = distances[tid] + weights[i];

        if (new_dist < distances[neighbor]) {
            atomicMin((int*)&distances[neighbor], __float_as_int(new_dist));
            *updated = true;
        }
    }
}

int main() {
    printf("=== GPU 最短路径算法 ===\n");
    printf("任务: 实现 Single-Source Shortest Path\n");

    return 0;
}

/**
 * 编译: nvcc -o shortest_path 03_shortest_path.cu
 * 知识点: Bellman-Ford, 边松弛, 原子操作
 */
