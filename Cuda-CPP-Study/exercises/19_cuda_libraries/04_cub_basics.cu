// 练习 194: CUB 基础 - CUDA 高性能 Primitives
//
// 目标: 使用 CUB 库的高性能构建块
//
// 任务:
// 1. 使用 CUB 进行 block-level reduction
// 2. 使用 CUB 进行 device-level scan
// 3. 对比手写实现的性能
//
// CUB (CUDA Unbound) 提供高性能的 CUDA primitive 操作

#include <stdio.h>
#include <cuda_runtime.h>
#include <cub/cub.cuh>
#include <time.h>

#define N (1 << 20)  // 1M
#define BLOCK_SIZE 256

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

double get_time() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

// TODO: 示例 1 - Block-level Reduction
__global__ void cub_block_reduce(int *input, int *output, int n) {
    // 使用 CUB 的 BlockReduce
    typedef cub::BlockReduce<int, BLOCK_SIZE> BlockReduce;
    __shared__ typename BlockReduce::TempStorage temp_storage;

    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    int value = (idx < n) ? input[idx] : 0;

    // TODO: 使用 CUB 进行 block reduction
    // int aggregate = BlockReduce(temp_storage).Sum(value);

    // 每个 block 的第一个线程写入结果
    // if (threadIdx.x == 0) {
    //     output[blockIdx.x] = aggregate;
    // }
}

// 手写的简单 reduction（用于对比）
__global__ void naive_reduce(int *input, int *output, int n) {
    __shared__ int sdata[BLOCK_SIZE];

    int tid = threadIdx.x;
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    sdata[tid] = (idx < n) ? input[idx] : 0;
    __syncthreads();

    for (int s = blockDim.x / 2; s > 0; s >>= 1) {
        if (tid < s) {
            sdata[tid] += sdata[tid + s];
        }
        __syncthreads();
    }

    if (tid == 0) {
        output[blockIdx.x] = sdata[0];
    }
}

int main() {
    printf("CUB 基础: 高性能 Primitives\n");
    printf("数据量: %d\n\n", N);

    // 准备数据
    int *h_input = (int*)malloc(N * sizeof(int));
    for (int i = 0; i < N; i++) {
        h_input[i] = 1;  // 所有元素为1，便于验证
    }

    int *d_input;
    CUDA_CHECK(cudaMalloc(&d_input, N * sizeof(int)));
    CUDA_CHECK(cudaMemcpy(d_input, h_input, N * sizeof(int), cudaMemcpyHostToDevice));

    int num_blocks = (N + BLOCK_SIZE - 1) / BLOCK_SIZE;
    int *d_output;
    CUDA_CHECK(cudaMalloc(&d_output, num_blocks * sizeof(int)));

    // TODO: 测试 1 - CUB Block Reduction
    printf("测试 1: CUB Block Reduction\n");
    double start = get_time();
    cub_block_reduce<<<num_blocks, BLOCK_SIZE>>>(d_input, d_output, N);
    CUDA_CHECK(cudaDeviceSynchronize());
    double cub_time = get_time() - start;

    printf("CUB Reduction 时间: %.3f ms\n", cub_time * 1000);

    // 测试 2 - 手写 Reduction
    printf("\n测试 2: 手写 Reduction\n");
    start = get_time();
    naive_reduce<<<num_blocks, BLOCK_SIZE>>>(d_input, d_output, N);
    CUDA_CHECK(cudaDeviceSynchronize());
    double naive_time = get_time() - start;

    printf("手写 Reduction 时间: %.3f ms\n", naive_time * 1000);
    printf("加速比: %.2fx\n", naive_time / cub_time);

    // TODO: 测试 3 - Device-level Scan (Prefix Sum)
    printf("\n测试 3: CUB Device Scan (Prefix Sum)\n");

    int *d_scan_output;
    CUDA_CHECK(cudaMalloc(&d_scan_output, N * sizeof(int)));

    // 确定临时存储大小
    void *d_temp_storage = NULL;
    size_t temp_storage_bytes = 0;

    // TODO: 调用 CUB DeviceScan
    // cub::DeviceScan::InclusiveSum(d_temp_storage, temp_storage_bytes,
    //                                d_input, d_scan_output, N);

    // 分配临时存储
    // CUDA_CHECK(cudaMalloc(&d_temp_storage, temp_storage_bytes));

    // 执行 scan
    start = get_time();
    // cub::DeviceScan::InclusiveSum(d_temp_storage, temp_storage_bytes,
    //                                d_input, d_scan_output, N);
    CUDA_CHECK(cudaDeviceSynchronize());
    double scan_time = get_time() - start;

    printf("CUB Scan 时间: %.3f ms\n", scan_time * 1000);

    // 验证结果
    int *h_scan_output = (int*)malloc(N * sizeof(int));
    CUDA_CHECK(cudaMemcpy(h_scan_output, d_scan_output, N * sizeof(int),
                          cudaMemcpyDeviceToHost));

    printf("前缀和前5个结果: ");
    for (int i = 0; i < 5; i++) {
        printf("%d ", h_scan_output[i]);
    }
    printf("\n(期望: 1 2 3 4 5)\n");

    // TODO: 测试 4 - Device-level Sort
    printf("\n测试 4: CUB Device Sort\n");

    // 初始化随机数据
    for (int i = 0; i < N; i++) {
        h_input[i] = rand() % 1000;
    }
    CUDA_CHECK(cudaMemcpy(d_input, h_input, N * sizeof(int), cudaMemcpyHostToDevice));

    int *d_sorted;
    CUDA_CHECK(cudaMalloc(&d_sorted, N * sizeof(int)));

    // TODO: 使用 CUB 排序
    // cub::DeviceRadixSort::SortKeys(d_temp_storage, temp_storage_bytes,
    //                                 d_input, d_sorted, N);

    start = get_time();
    // cub::DeviceRadixSort::SortKeys(...);
    CUDA_CHECK(cudaDeviceSynchronize());
    double sort_time = get_time() - start;

    printf("CUB Sort 时间: %.3f ms\n", sort_time * 1000);

    printf("\nCUB 的优势:\n");
    printf("- 高度优化的性能\n");
    printf("- 支持 warp/block/device 级别\n");
    printf("- 模板化，灵活易用\n");
    printf("- 已集成到 CUDA Toolkit\n");

    // 清理
    CUDA_CHECK(cudaFree(d_input));
    CUDA_CHECK(cudaFree(d_output));
    CUDA_CHECK(cudaFree(d_scan_output));
    CUDA_CHECK(cudaFree(d_sorted));
    // CUDA_CHECK(cudaFree(d_temp_storage));
    free(h_input);
    free(h_scan_output);

    printf("\nCUB 测试完成!\n");
    printf("TEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
