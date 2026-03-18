/**
 * 练习 233: Warp Match 函数
 *
 * 学习目标：
 * - 掌握 __match_any_sync() 和 __match_all_sync()
 * - 理解 Warp 内数据分组和匹配机制
 * - 实现高效的数据去重和分组
 *
 * 任务：
 * 1. 使用 __match_any_sync() 查找相同值的线程
 * 2. 使用 __match_all_sync() 检查所有线程值是否相同
 * 3. 实现 Warp 级别的去重
 * 4. 实现 Warp 级别的直方图统计
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

// TODO 1: 使用 __match_any_sync() 查找相同值
__global__ void find_duplicates(int *data, int *group_ids, int n) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    if (tid >= n) return;

    int val = data[tid];
    int lane = threadIdx.x % WARP_SIZE;

    // TODO: 使用 __match_any_sync() 找到具有相同值的线程
    // 提示：unsigned int match_mask = __match_any_sync(0xffffffff, val);


    // 每组的第一个线程（最低位的线程）作为组代表
    int group_leader = __ffs(match_mask) - 1;  // Find first set bit

    group_ids[tid] = group_leader;
}

// TODO 2: 使用 __match_all_sync() 检查所有值是否相同
__global__ void check_uniform(int *data, int *results, int n) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    int warp_id = tid / WARP_SIZE;

    if (tid >= n) return;

    int val = data[tid];
    int lane = threadIdx.x % WARP_SIZE;

    // TODO: 使用 __match_all_sync() 检查是否所有线程值相同
    // 提示：unsigned int match_mask;
    //       int is_uniform = __match_all_sync(0xffffffff, val, &match_mask);


    if (lane == 0) {
        results[warp_id] = is_uniform;
    }
}

// TODO 3: Warp 级别去重
__global__ void warp_unique(int *input, int *output, int *output_count, int n) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    if (tid >= n) return;

    int val = input[tid];
    int lane = threadIdx.x % WARP_SIZE;

    // TODO: 使用 __match_any_sync() 查找相同值
    // unsigned int match_mask = __match_any_sync(0xffffffff, val);


    // 只有每组的第一个线程写入结果
    int is_first = (__ffs(match_mask) - 1 == lane);

    if (is_first) {
        // 简化版：直接写入（实际需要原子操作或前缀和）
        int warp_id = tid / WARP_SIZE;
        int pos = warp_id * WARP_SIZE + lane;
        output[pos] = val;
    }

    // 统计唯一值数量
    if (lane == 0) {
        int warp_id = tid / WARP_SIZE;
        // 计算有多少个不同的值（每组的第一个线程）
        unsigned int ballot = __ballot_sync(0xffffffff, is_first);
        output_count[warp_id] = __popc(ballot);
    }
}

// TODO 4: Warp 级别直方图（计数相同值）
__global__ void warp_histogram(int *data, int *histogram, int n, int num_bins) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    if (tid >= n) return;

    int val = data[tid];
    int lane = threadIdx.x % WARP_SIZE;

    // TODO: 使用 __match_any_sync() 统计每个值的出现次数
    // unsigned int match_mask = __match_any_sync(0xffffffff, val);
    // int count = __popc(match_mask);


    // 每组的第一个线程更新直方图
    int is_first = (__ffs(match_mask) - 1 == lane);
    if (is_first && val < num_bins) {
        atomicAdd(&histogram[val], count);
    }
}

// 示例：使用 Match 优化数据库风格的 Group By
__global__ void group_by_aggregate(int *keys, float *values, float *results, int n) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    if (tid >= n) return;

    int key = keys[tid];
    float val = values[tid];
    int lane = threadIdx.x % WARP_SIZE;

    // TODO: 查找具有相同 key 的线程
    // unsigned int match_mask = __match_any_sync(0xffffffff, key);


    // 在匹配的线程间聚合值
    float sum = val;
    // 使用 shuffle 在组内求和
    for (int offset = 1; offset < WARP_SIZE; offset *= 2) {
        float other = __shfl_down_sync(match_mask, sum, offset);
        if (lane + offset < WARP_SIZE && ((match_mask >> (lane + offset)) & 1)) {
            sum += other;
        }
    }

    // 每组的第一个线程写入结果
    int is_first = (__ffs(match_mask) - 1 == lane);
    if (is_first) {
        results[key] = sum;
    }
}

int main() {
    const int N = 128;
    const int NUM_BINS = 10;
    size_t bytes = N * sizeof(int);

    // 分配内存
    int *h_data = (int*)malloc(bytes);
    int *h_results = (int*)malloc(bytes);
    int *h_histogram = (int*)calloc(NUM_BINS, sizeof(int));

    int *d_data, *d_results, *d_histogram;
    CUDA_CHECK(cudaMalloc(&d_data, bytes));
    CUDA_CHECK(cudaMalloc(&d_results, bytes));
    CUDA_CHECK(cudaMalloc(&d_histogram, NUM_BINS * sizeof(int)));

    // 初始化测试数据（重复值）
    for (int i = 0; i < N; i++) {
        h_data[i] = i % NUM_BINS;  // 0-9 重复
    }
    CUDA_CHECK(cudaMemcpy(d_data, h_data, bytes, cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemset(d_histogram, 0, NUM_BINS * sizeof(int)));

    printf("=== Warp Match 函数测试 ===\n\n");

    // 测试 1: 查找重复值
    find_duplicates<<<1, N>>>(d_data, d_results, N);
    CUDA_CHECK(cudaMemcpy(h_results, d_results, bytes, cudaMemcpyDeviceToHost));

    printf("测试 1: __match_any_sync() - 查找相同值的线程\n");
    printf("前 32 个元素的组 ID:\n");
    for (int i = 0; i < 32 && i < N; i++) {
        printf("%d ", h_results[i]);
        if ((i + 1) % 16 == 0) printf("\n");
    }
    printf("\n");

    // 测试 2: 检查是否所有值相同
    int uniform_data[N];
    for (int i = 0; i < N; i++) uniform_data[i] = 5;
    CUDA_CHECK(cudaMemcpy(d_data, uniform_data, bytes, cudaMemcpyHostToDevice));

    check_uniform<<<1, N>>>(d_data, d_results, N);
    CUDA_CHECK(cudaMemcpy(h_results, d_results, (N / WARP_SIZE) * sizeof(int),
                         cudaMemcpyDeviceToHost));

    printf("\n测试 2: __match_all_sync() - 检查所有值是否相同\n");
    printf("所有 warps 的值都相同: %s\n", h_results[0] ? "是" : "否");

    // 测试 3: Warp 级别直方图
    CUDA_CHECK(cudaMemcpy(d_data, h_data, bytes, cudaMemcpyHostToDevice));
    warp_histogram<<<1, N>>>(d_data, d_histogram, N, NUM_BINS);
    CUDA_CHECK(cudaMemcpy(h_histogram, d_histogram, NUM_BINS * sizeof(int),
                         cudaMemcpyDeviceToHost));

    printf("\n测试 3: Warp 级别直方图\n");
    for (int i = 0; i < NUM_BINS; i++) {
        printf("Bin %d: %d 次\n", i, h_histogram[i]);
    }

    printf("\nWarp Match 函数总结：\n");
    printf("✓ __match_any_sync()  - 查找具有相同值的线程掩码\n");
    printf("✓ __match_all_sync() - 检查所有线程值是否相同\n");
    printf("✓ 应用：去重、分组、直方图、Group By 聚合\n");
    printf("✓ 相比传统方法，无需 Shared Memory 和同步\n");
    printf("✓ 特别适合数据库风格的操作\n");

    // 清理
    free(h_data);
    free(h_results);
    free(h_histogram);
    CUDA_CHECK(cudaFree(d_data));
    CUDA_CHECK(cudaFree(d_results));
    CUDA_CHECK(cudaFree(d_histogram));

    return 0;
}

/**
 * 编译命令：
 * nvcc -arch=sm_70 -o warp_match 03_warp_match.cu
 *
 * 注意：__match_any/all_sync 需要 Volta (SM 7.0) 及以上
 *
 * 知识点：
 * 1. __match_any_sync(mask, value) - 返回具有相同 value 的线程掩码
 * 2. __match_all_sync(mask, value, &pred) - 检查所有线程是否有相同 value
 * 3. __ffs(x) - 查找最低位的 1（Find First Set）
 * 4. 应用场景：去重、分组、直方图、数据库操作
 * 5. 需要 Volta 架构及以上（CC >= 7.0）
 */
