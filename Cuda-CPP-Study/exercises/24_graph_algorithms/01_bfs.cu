/**
 * 练习 241: 并行广度优先搜索 (BFS)
 *
 * 学习目标：
 * - 实现 GPU 加速的 BFS 算法
 * - 理解图遍历的并行化策略
 * - 使用原子操作和队列数据结构
 */

#include <cuda_runtime.h>
#include <stdio.h>
#include <stdlib.h>

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// CSR 格式存储图
struct Graph {
    int num_nodes;
    int num_edges;
    int *row_offsets;     // 每个节点的边起始位置
    int *column_indices;  // 边的目标节点
};

// TODO 1: BFS Kernel - Level Synchronous 方法
__global__ void bfs_kernel(int *row_offsets, int *column_indices,
                            int *levels, bool *visited, bool *frontier,
                            bool *next_frontier, int num_nodes, int current_level) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    if (tid >= num_nodes) return;

    // 如果当前节点在 frontier 中
    if (frontier[tid]) {
        // TODO: 遍历所有邻居
        int start = row_offsets[tid];
        int end = row_offsets[tid + 1];

        for (int i = start; i < end; i++) {
            int neighbor = column_indices[i];

            // 如果邻居未访问过
            if (!visited[neighbor]) {
                // 标记为已访问，加入下一层 frontier
                visited[neighbor] = true;
                next_frontier[neighbor] = true;
                levels[neighbor] = current_level + 1;
            }
        }

        // 当前节点处理完毕
        frontier[tid] = false;
    }
}

// TODO 2: 检查 frontier 是否为空
__global__ void check_frontier(bool *frontier, bool *has_next, int num_nodes) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    if (tid >= num_nodes) return;

    if (frontier[tid]) {
        *has_next = true;
    }
}

void bfs_gpu(Graph &graph, int source, int *levels) {
    // 分配 GPU 内存
    int *d_row_offsets, *d_column_indices;
    int *d_levels;
    bool *d_visited, *d_frontier, *d_next_frontier;
    bool *d_has_next;

    CUDA_CHECK(cudaMalloc(&d_row_offsets, (graph.num_nodes + 1) * sizeof(int)));
    CUDA_CHECK(cudaMalloc(&d_column_indices, graph.num_edges * sizeof(int)));
    CUDA_CHECK(cudaMalloc(&d_levels, graph.num_nodes * sizeof(int)));
    CUDA_CHECK(cudaMalloc(&d_visited, graph.num_nodes * sizeof(bool)));
    CUDA_CHECK(cudaMalloc(&d_frontier, graph.num_nodes * sizeof(bool)));
    CUDA_CHECK(cudaMalloc(&d_next_frontier, graph.num_nodes * sizeof(bool)));
    CUDA_CHECK(cudaMalloc(&d_has_next, sizeof(bool)));

    // 拷贝图数据
    CUDA_CHECK(cudaMemcpy(d_row_offsets, graph.row_offsets,
                          (graph.num_nodes + 1) * sizeof(int), cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_column_indices, graph.column_indices,
                          graph.num_edges * sizeof(int), cudaMemcpyHostToDevice));

    // 初始化
    CUDA_CHECK(cudaMemset(d_levels, -1, graph.num_nodes * sizeof(int)));
    CUDA_CHECK(cudaMemset(d_visited, 0, graph.num_nodes * sizeof(bool)));
    CUDA_CHECK(cudaMemset(d_frontier, 0, graph.num_nodes * sizeof(bool)));

    // 设置源节点
    int init_level = 0;
    bool init_visited = true;
    bool init_frontier = true;
    CUDA_CHECK(cudaMemcpy(&d_levels[source], &init_level, sizeof(int), cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(&d_visited[source], &init_visited, sizeof(bool), cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(&d_frontier[source], &init_frontier, sizeof(bool), cudaMemcpyHostToDevice));

    int threadsPerBlock = 256;
    int blocksPerGrid = (graph.num_nodes + threadsPerBlock - 1) / threadsPerBlock;

    int current_level = 0;
    bool has_next = true;

    // TODO 3: Level Synchronous BFS 主循环
    while (has_next) {
        CUDA_CHECK(cudaMemset(d_next_frontier, 0, graph.num_nodes * sizeof(bool)));

        // 执行 BFS 一层
        bfs_kernel<<<blocksPerGrid, threadsPerBlock>>>(
            d_row_offsets, d_column_indices, d_levels, d_visited,
            d_frontier, d_next_frontier, graph.num_nodes, current_level);

        // 交换 frontier
        bool *temp = d_frontier;
        d_frontier = d_next_frontier;
        d_next_frontier = temp;

        // 检查是否还有节点要处理
        has_next = false;
        CUDA_CHECK(cudaMemcpy(d_has_next, &has_next, sizeof(bool), cudaMemcpyHostToDevice));
        check_frontier<<<blocksPerGrid, threadsPerBlock>>>(d_frontier, d_has_next, graph.num_nodes);
        CUDA_CHECK(cudaMemcpy(&has_next, d_has_next, sizeof(bool), cudaMemcpyDeviceToHost));

        current_level++;
    }

    // 拷贝结果
    CUDA_CHECK(cudaMemcpy(levels, d_levels, graph.num_nodes * sizeof(int), cudaMemcpyDeviceToHost));

    // 释放内存
    CUDA_CHECK(cudaFree(d_row_offsets));
    CUDA_CHECK(cudaFree(d_column_indices));
    CUDA_CHECK(cudaFree(d_levels));
    CUDA_CHECK(cudaFree(d_visited));
    CUDA_CHECK(cudaFree(d_frontier));
    CUDA_CHECK(cudaFree(d_next_frontier));
    CUDA_CHECK(cudaFree(d_has_next));
}

int main() {
    // 创建测试图（Grid Graph 8x8）
    const int GRID_SIZE = 8;
    const int NUM_NODES = GRID_SIZE * GRID_SIZE;

    Graph graph;
    graph.num_nodes = NUM_NODES;
    graph.num_edges = (GRID_SIZE - 1) * GRID_SIZE * 2;  // 横向和纵向边

    graph.row_offsets = (int*)malloc((NUM_NODES + 1) * sizeof(int));
    graph.column_indices = (int*)malloc(graph.num_edges * sizeof(int));

    // 构建 Grid Graph 的 CSR 表示
    int edge_idx = 0;
    for (int i = 0; i < NUM_NODES; i++) {
        graph.row_offsets[i] = edge_idx;
        int row = i / GRID_SIZE;
        int col = i % GRID_SIZE;

        // 右邻居
        if (col < GRID_SIZE - 1) {
            graph.column_indices[edge_idx++] = i + 1;
        }
        // 下邻居
        if (row < GRID_SIZE - 1) {
            graph.column_indices[edge_idx++] = i + GRID_SIZE;
        }
    }
    graph.row_offsets[NUM_NODES] = edge_idx;

    int *levels = (int*)malloc(NUM_NODES * sizeof(int));

    printf("=== GPU BFS 测试 ===\n");
    printf("图规模: %d 节点, %d 边\n\n", NUM_NODES, graph.num_edges);

    bfs_gpu(graph, 0, levels);

    printf("从节点 0 的 BFS 结果（前 16 个节点）:\n");
    for (int i = 0; i < 16 && i < NUM_NODES; i++) {
        printf("节点 %2d: Level %d\n", i, levels[i]);
    }

    free(graph.row_offsets);
    free(graph.column_indices);
    free(levels);

    return 0;
}

/**
 * 编译: nvcc -o bfs 01_bfs.cu
 *
 * 知识点：
 * - Level Synchronous BFS
 * - Frontier 管理
 * - 图的 CSR (Compressed Sparse Row) 表示
 * - GPU 图遍历优化
 */
