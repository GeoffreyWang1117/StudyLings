/**
 * 练习 232: Warp Vote 函数
 *
 * 学习目标：
 * - 掌握 __all_sync(), __any_sync(), __ballot_sync()
 * - 理解 Warp 级别的条件判断和投票机制
 * - 实现 Warp 级别的分支优化
 *
 * 任务：
 * 1. 使用 __all_sync() 检查所有线程条件
 * 2. 使用 __any_sync() 检查任意线程条件
 * 3. 使用 __ballot_sync() 收集线程投票结果
 * 4. 实现 Warp 级别的数据过滤
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

// TODO 1: 使用 __all_sync() 检查所有线程是否满足条件
__global__ void check_all_positive(float *data, int *results, int n) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    int warp_id = tid / WARP_SIZE;

    if (tid >= n) return;

    float val = data[tid];

    // TODO: 使用 __all_sync() 检查 warp 内所有值是否为正
    // 提示：int all_positive = __all_sync(0xffffffff, val > 0.0f);


    // 每个 warp 的第一个线程写入结果
    int lane = threadIdx.x % WARP_SIZE;
    if (lane == 0) {
        results[warp_id] = all_positive;
    }
}

// TODO 2: 使用 __any_sync() 检查是否存在满足条件的线程
__global__ void check_any_negative(float *data, int *results, int n) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    int warp_id = tid / WARP_SIZE;

    if (tid >= n) return;

    float val = data[tid];

    // TODO: 使用 __any_sync() 检查 warp 内是否存在负值
    // 提示：int any_negative = __any_sync(0xffffffff, val < 0.0f);


    int lane = threadIdx.x % WARP_SIZE;
    if (lane == 0) {
        results[warp_id] = any_negative;
    }
}

// TODO 3: 使用 __ballot_sync() 收集投票结果
__global__ void count_positives_ballot(float *data, int *counts, int n) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    int warp_id = tid / WARP_SIZE;

    if (tid >= n) return;

    float val = data[tid];

    // TODO: 使用 __ballot_sync() 获取哪些线程满足条件
    // 提示：unsigned int ballot = __ballot_sync(0xffffffff, val > 0.0f);


    // 统计置位数量（即正值数量）
    int count = __popc(ballot);  // Population count

    int lane = threadIdx.x % WARP_SIZE;
    if (lane == 0) {
        counts[warp_id] = count;
    }
}

// TODO 4: 实现 Warp 级别的压缩（Stream Compaction）
__global__ void warp_compact(float *input, float *output, int *output_size, int n) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    if (tid >= n) return;

    float val = input[tid];
    int lane = threadIdx.x % WARP_SIZE;

    // 只保留正值
    int predicate = (val > 0.0f);

    // TODO: 使用 __ballot_sync() 获取满足条件的线程掩码
    // unsigned int mask = __ballot_sync(0xffffffff, predicate);


    // 计算当前线程在输出中的位置（前缀和）
    unsigned int lane_mask = (1u << lane) - 1;
    int position = __popc(mask & lane_mask);

    // 如果当前线程满足条件，写入输出
    if (predicate) {
        int warp_id = tid / WARP_SIZE;
        int warp_offset = warp_id * WARP_SIZE;  // 简化版，实际需要原子操作
        output[warp_offset + position] = val;
    }

    // 统计输出数量
    if (lane == 0) {
        int warp_id = tid / WARP_SIZE;
        output_size[warp_id] = __popc(mask);
    }
}

// TODO 5: 使用 Vote 函数优化分支
__global__ void optimized_branch(float *data, int n) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    if (tid >= n) return;

    float val = data[tid];
    bool needs_processing = (val > 100.0f);

    // TODO: 检查 warp 内是否有线程需要处理
    // if (__any_sync(0xffffffff, needs_processing)) {
    //     if (needs_processing) {
    //         // 执行昂贵的计算
    //         val = sqrtf(val * val + 1.0f);
    //     }
    // }


    data[tid] = val;
}

int main() {
    const int N = 1024;
    const int NUM_WARPS = N / WARP_SIZE;
    size_t bytes = N * sizeof(float);
    size_t result_bytes = NUM_WARPS * sizeof(int);

    // 分配内存
    float *h_data = (float*)malloc(bytes);
    int *h_results = (int*)malloc(result_bytes);

    float *d_data;
    int *d_results;

    CUDA_CHECK(cudaMalloc(&d_data, bytes));
    CUDA_CHECK(cudaMalloc(&d_results, result_bytes));

    // 初始化测试数据
    for (int i = 0; i < N; i++) {
        h_data[i] = (i % 10 == 0) ? -1.0f : (float)(i + 1);
    }
    CUDA_CHECK(cudaMemcpy(d_data, h_data, bytes, cudaMemcpyHostToDevice));

    printf("=== Warp Vote 函数测试 ===\n\n");

    // 测试 __all_sync()
    check_all_positive<<<1, N>>>(d_data, d_results, N);
    CUDA_CHECK(cudaMemcpy(h_results, d_results, result_bytes, cudaMemcpyDeviceToHost));
    printf("测试 1: __all_sync() - 检查所有值为正\n");
    int all_positive_warps = 0;
    for (int i = 0; i < NUM_WARPS; i++) {
        if (h_results[i]) all_positive_warps++;
    }
    printf("  %d / %d warps 全部为正值\n\n", all_positive_warps, NUM_WARPS);

    // 测试 __any_sync()
    check_any_negative<<<1, N>>>(d_data, d_results, N);
    CUDA_CHECK(cudaMemcpy(h_results, d_results, result_bytes, cudaMemcpyDeviceToHost));
    printf("测试 2: __any_sync() - 检查是否存在负值\n");
    int any_negative_warps = 0;
    for (int i = 0; i < NUM_WARPS; i++) {
        if (h_results[i]) any_negative_warps++;
    }
    printf("  %d / %d warps 包含负值\n\n", any_negative_warps, NUM_WARPS);

    // 测试 __ballot_sync()
    count_positives_ballot<<<1, N>>>(d_data, d_results, N);
    CUDA_CHECK(cudaMemcpy(h_results, d_results, result_bytes, cudaMemcpyDeviceToHost));
    printf("测试 3: __ballot_sync() - 统计正值数量\n");
    int total_positives = 0;
    for (int i = 0; i < NUM_WARPS; i++) {
        total_positives += h_results[i];
    }
    printf("  总共 %d 个正值\n\n", total_positives);

    printf("Warp Vote 函数总结：\n");
    printf("✓ __all_sync()   - 所有线程满足条件时返回 true\n");
    printf("✓ __any_sync()   - 任一线程满足条件时返回 true\n");
    printf("✓ __ballot_sync()- 返回线程投票位掩码\n");
    printf("✓ __popc()       - 统计位掩码中的 1 的数量\n");
    printf("✓ 可用于分支优化、数据压缩、条件执行\n");

    // 清理
    free(h_data);
    free(h_results);
    CUDA_CHECK(cudaFree(d_data));
    CUDA_CHECK(cudaFree(d_results));

    return 0;
}

/**
 * 编译命令：
 * nvcc -o warp_vote 02_warp_vote.cu
 *
 * 知识点：
 * 1. __all_sync(mask, predicate) - 所有线程满足条件
 * 2. __any_sync(mask, predicate) - 任一线程满足条件
 * 3. __ballot_sync(mask, predicate) - 返回投票位掩码
 * 4. __popc(x) - 计算 x 中 1 的个数
 * 5. 可用于 Warp 级别的条件判断和分支优化
 * 6. 减少 Warp 分歧，提高执行效率
 */
