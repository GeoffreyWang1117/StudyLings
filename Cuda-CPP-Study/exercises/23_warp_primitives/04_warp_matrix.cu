/**
 * 练习 234: Warp 级别矩阵操作 (WMMA 入门)
 *
 * 学习目标：
 * - 理解 Warp 级别的协作计算
 * - 使用 Warp Primitives 实现高效矩阵转置
 * - 为学习 Tensor Core WMMA 打基础
 *
 * 任务：
 * 1. 使用 Warp Shuffle 实现矩阵转置
 * 2. 实现 Warp 级别的矩阵乘法（小矩阵）
 * 3. 对比不同实现的性能
 */

#include <cuda_runtime.h>
#include <stdio.h>
#include <stdlib.h>

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error at %s:%d - %s\n", __FILE__, __LINE__, \
                    cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

#define WARP_SIZE 32

// TODO 1: 使用 Warp Shuffle 实现 8x8 矩阵转置
// 每个 warp 处理一个 8x8 小矩阵（使用前 64 个线程中的某些）
__global__ void transpose_8x8_shuffle(float *input, float *output, int n) {
    int warp_id = (blockIdx.x * blockDim.x + threadIdx.x) / WARP_SIZE;
    int lane = threadIdx.x % WARP_SIZE;

    // 每个 warp 处理一个 8x8 矩阵
    int base_row = (warp_id / (n / 8)) * 8;
    int base_col = (warp_id % (n / 8)) * 8;

    // 每个线程负责一个元素（前 64 个 lane）
    if (lane < 64) {
        int local_row = lane / 8;
        int local_col = lane % 8;

        int global_row = base_row + local_row;
        int global_col = base_col + local_col;

        // TODO: 读取输入元素
        // float val = input[global_row * n + global_col];


        // TODO: 使用 shuffle 进行转置
        // 提示：转置意味着 (row, col) -> (col, row)
        // 可以通过巧妙的 shuffle 模式实现
        // 这里简化为直接写入（练习：尝试用 shuffle 优化）
        // output[global_col * n + global_row] = val;

    }
}

// TODO 2: Warp 级别的 4x4 矩阵乘法
// C = A * B，每个矩阵 4x4，每个 warp 的前 16 个线程参与
__device__ void warp_matmul_4x4(float *A, float *B, float *C) {
    int lane = threadIdx.x % WARP_SIZE;

    if (lane < 16) {
        int row = lane / 4;
        int col = lane % 4;

        float sum = 0.0f;

        // TODO: 计算 C[row][col] = sum(A[row][k] * B[k][col])
        for (int k = 0; k < 4; k++) {
            // 提示：使用 __shfl_sync() 广播 A 和 B 的元素
            // float a_val = A[row * 4 + k];
            // float b_val = B[k * 4 + col];
            // sum += a_val * b_val;
        }

        C[row * 4 + col] = sum;
    }
}

// TODO 3: Warp 级别的向量点积（使用 Shuffle 归约）
__device__ float warp_dot_product(float *vec_a, float *vec_b, int size) {
    int lane = threadIdx.x % WARP_SIZE;

    float local_sum = 0.0f;

    // 每个线程处理一部分元素
    for (int i = lane; i < size; i += WARP_SIZE) {
        local_sum += vec_a[i] * vec_b[i];
    }

    // TODO: 使用 Warp Shuffle 归约求和
    // 提示：for (int offset = 16; offset > 0; offset /= 2) {
    //          local_sum += __shfl_down_sync(0xffffffff, local_sum, offset);
    //       }


    return local_sum;  // lane 0 holds the final result
}

// TODO 4: 使用 Warp 协作计算外积
__global__ void warp_outer_product(float *vec_a, float *vec_b, float *matrix, int n) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    int warp_id = tid / WARP_SIZE;
    int lane = threadIdx.x % WARP_SIZE;

    // 每个 warp 计算部分外积
    int elements_per_warp = (n * n + WARP_SIZE - 1) / WARP_SIZE;

    for (int e = 0; e < elements_per_warp; e++) {
        int idx = warp_id * WARP_SIZE * elements_per_warp + e * WARP_SIZE + lane;
        if (idx < n * n) {
            int row = idx / n;
            int col = idx % n;

            // TODO: 使用 shuffle 广播向量元素
            // 提示：float a = vec_a[row];
            //       float b = vec_b[col];
            //       matrix[idx] = a * b;

        }
    }
}

// 传统方法对比：Shared Memory 矩阵转置
__global__ void transpose_shared(float *input, float *output, int n) {
    __shared__ float tile[32][33];  // +1 避免 bank conflicts

    int x = blockIdx.x * 32 + threadIdx.x;
    int y = blockIdx.y * 32 + threadIdx.y;

    if (x < n && y < n) {
        tile[threadIdx.y][threadIdx.x] = input[y * n + x];
    }

    __syncthreads();

    x = blockIdx.y * 32 + threadIdx.x;
    y = blockIdx.x * 32 + threadIdx.y;

    if (x < n && y < n) {
        output[y * n + x] = tile[threadIdx.x][threadIdx.y];
    }
}

int main() {
    const int N = 256;
    size_t bytes = N * N * sizeof(float);

    // 分配内存
    float *h_input = (float*)malloc(bytes);
    float *h_output = (float*)malloc(bytes);

    float *d_input, *d_output;
    CUDA_CHECK(cudaMalloc(&d_input, bytes));
    CUDA_CHECK(cudaMalloc(&d_output, bytes));

    // 初始化矩阵
    for (int i = 0; i < N * N; i++) {
        h_input[i] = (float)i;
    }
    CUDA_CHECK(cudaMemcpy(d_input, h_input, bytes, cudaMemcpyHostToDevice));

    printf("=== Warp 级别矩阵操作测试 ===\n");
    printf("矩阵规模: %d x %d\n\n", N, N);

    // 测试转置性能
    cudaEvent_t start, stop;
    CUDA_CHECK(cudaEventCreate(&start));
    CUDA_CHECK(cudaEventCreate(&stop));

    // Shared Memory 方法
    dim3 block(32, 32);
    dim3 grid((N + 31) / 32, (N + 31) / 32);

    CUDA_CHECK(cudaEventRecord(start));
    transpose_shared<<<grid, block>>>(d_input, d_output, N);
    CUDA_CHECK(cudaEventRecord(stop));
    CUDA_CHECK(cudaEventSynchronize(stop));

    float time_shared = 0;
    CUDA_CHECK(cudaEventElapsedTime(&time_shared, start, stop));

    printf("矩阵转置性能对比:\n");
    printf("Shared Memory 方法: %.3f ms\n", time_shared);

    // 验证结果
    CUDA_CHECK(cudaMemcpy(h_output, d_output, bytes, cudaMemcpyDeviceToHost));
    bool correct = true;
    for (int i = 0; i < N && correct; i++) {
        for (int j = 0; j < N && correct; j++) {
            int orig_idx = i * N + j;
            int trans_idx = j * N + i;
            if (h_output[trans_idx] != h_input[orig_idx]) {
                correct = false;
            }
        }
    }
    printf("转置结果: %s\n\n", correct ? "✓ 正确" : "✗ 错误");

    printf("Warp 矩阵操作总结：\n");
    printf("✓ Warp Shuffle 可用于小矩阵的快速操作\n");
    printf("✓ 适合 4x4, 8x8 等小矩阵（可放入寄存器）\n");
    printf("✓ 为 Tensor Core WMMA 提供基础理解\n");
    printf("✓ Warp 协作模式：所有线程共同完成一个任务\n");
    printf("✓ 相比 Shared Memory，减少内存访问和同步\n");

    // 清理
    free(h_input);
    free(h_output);
    CUDA_CHECK(cudaFree(d_input));
    CUDA_CHECK(cudaFree(d_output));
    CUDA_CHECK(cudaEventDestroy(start));
    CUDA_CHECK(cudaEventDestroy(stop));

    return 0;
}

/**
 * 编译命令：
 * nvcc -o warp_matrix 04_warp_matrix.cu
 *
 * 知识点：
 * 1. Warp Shuffle 可实现小矩阵的快速操作
 * 2. Warp 级别协作：32 个线程共同完成任务
 * 3. 适用于频繁的小矩阵运算（AI、图形学）
 * 4. 为理解 Tensor Core WMMA API 打基础
 * 5. Warp 级别操作通常比 Shared Memory 更快
 * 6. 限制：只适合小矩阵（受 Warp 大小限制）
 */
