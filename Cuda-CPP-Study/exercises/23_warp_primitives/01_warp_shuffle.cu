/**
 * 练习 231: Warp Shuffle 操作
 *
 * 学习目标：
 * - 掌握 __shfl_sync(), __shfl_up_sync(), __shfl_down_sync(), __shfl_xor_sync()
 * - 理解 Warp 内线程通信机制
 * - 实现高效的 Warp 级别归约
 *
 * 任务：
 * 1. 使用 Warp Shuffle 实现快速求和
 * 2. 对比 Warp Shuffle 与 Shared Memory 的性能
 * 3. 实现 Warp 级别的最大值/最小值查找
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

// TODO 1: 实现 Warp Shuffle 归约求和
__device__ float warp_reduce_sum(float val) {
    // 提示：使用 __shfl_down_sync() 实现树状归约
    // for (int offset = 16; offset > 0; offset /= 2) {
    //     val += __shfl_down_sync(0xffffffff, val, offset);
    // }
    // return val;
    return 0.0f;  // 替换为实际实现
}

// 方法 1: 使用 Warp Shuffle
__global__ void sum_warp_shuffle(float *input, float *output, int n) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    int lane = threadIdx.x % WARP_SIZE;
    int warp_id = threadIdx.x / WARP_SIZE;

    float val = (tid < n) ? input[tid] : 0.0f;

    // TODO: 调用 warp_reduce_sum
    // val = warp_reduce_sum(val);

    // 每个 warp 的第一个线程写入结果
    if (lane == 0) {
        output[blockIdx.x * (blockDim.x / WARP_SIZE) + warp_id] = val;
    }
}

// 方法 2: 使用 Shared Memory（对比）
__global__ void sum_shared_memory(float *input, float *output, int n) {
    __shared__ float shared[256];
    int tid = blockIdx.x * blockDim.x + threadIdx.x;

    shared[threadIdx.x] = (tid < n) ? input[tid] : 0.0f;
    __syncthreads();

    // 树状归约
    for (int stride = blockDim.x / 2; stride > 0; stride >>= 1) {
        if (threadIdx.x < stride) {
            shared[threadIdx.x] += shared[threadIdx.x + stride];
        }
        __syncthreads();
    }

    if (threadIdx.x == 0) {
        output[blockIdx.x] = shared[0];
    }
}

// TODO 2: 实现 Warp Shuffle 最大值归约
__device__ float warp_reduce_max(float val) {
    // 提示：使用 __shfl_down_sync() 和 fmaxf()
    // for (int offset = 16; offset > 0; offset /= 2) {
    //     val = fmaxf(val, __shfl_down_sync(0xffffffff, val, offset));
    // }
    // return val;
    return 0.0f;  // 替换为实际实现
}

// TODO 3: 实现 Warp 广播
__global__ void warp_broadcast_demo(float *data, int n) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    if (tid >= n) return;

    float val = data[tid];

    // 提示：使用 __shfl_sync(mask, val, srcLane) 从 lane 0 广播
    // float broadcast_val = __shfl_sync(0xffffffff, val, 0);


    data[tid] = broadcast_val;
}

// TODO 4: 实现 Warp XOR Shuffle（用于 Butterfly 模式）
__global__ void warp_xor_demo(float *data, int n) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    if (tid >= n) return;

    float val = data[tid];
    int lane = threadIdx.x % WARP_SIZE;

    // 提示：__shfl_xor_sync() 可实现对称交换
    // float partner_val = __shfl_xor_sync(0xffffffff, val, 1);  // XOR with 1


    data[tid] = partner_val;
}

int main() {
    const int N = 1 << 20;  // 1M elements
    size_t bytes = N * sizeof(float);

    // 分配内存
    float *h_input = (float*)malloc(bytes);
    float *d_input, *d_output_shuffle, *d_output_shared;

    CUDA_CHECK(cudaMalloc(&d_input, bytes));
    CUDA_CHECK(cudaMalloc(&d_output_shuffle, bytes));
    CUDA_CHECK(cudaMalloc(&d_output_shared, bytes));

    // 初始化数据
    for (int i = 0; i < N; i++) {
        h_input[i] = 1.0f;
    }
    CUDA_CHECK(cudaMemcpy(d_input, h_input, bytes, cudaMemcpyHostToDevice));

    int threadsPerBlock = 256;
    int blocksPerGrid = (N + threadsPerBlock - 1) / threadsPerBlock;

    printf("=== Warp Shuffle 性能测试 ===\n");
    printf("数据规模: %d elements\n\n", N);

    // 测试 Warp Shuffle
    cudaEvent_t start, stop;
    CUDA_CHECK(cudaEventCreate(&start));
    CUDA_CHECK(cudaEventCreate(&stop));

    CUDA_CHECK(cudaEventRecord(start));
    sum_warp_shuffle<<<blocksPerGrid, threadsPerBlock>>>(d_input, d_output_shuffle, N);
    CUDA_CHECK(cudaEventRecord(stop));
    CUDA_CHECK(cudaEventSynchronize(stop));

    float time_shuffle = 0;
    CUDA_CHECK(cudaEventElapsedTime(&time_shuffle, start, stop));

    // 测试 Shared Memory
    CUDA_CHECK(cudaEventRecord(start));
    sum_shared_memory<<<blocksPerGrid, threadsPerBlock>>>(d_input, d_output_shared, N);
    CUDA_CHECK(cudaEventRecord(stop));
    CUDA_CHECK(cudaEventSynchronize(stop));

    float time_shared = 0;
    CUDA_CHECK(cudaEventElapsedTime(&time_shared, start, stop));

    printf("Warp Shuffle:   %.3f ms\n", time_shuffle);
    printf("Shared Memory:  %.3f ms\n", time_shared);
    printf("加速比:         %.2fx\n\n", time_shared / time_shuffle);

    printf("Warp Shuffle 优势：\n");
    printf("✓ 无需 Shared Memory，节省片上资源\n");
    printf("✓ 无需 __syncthreads()，减少同步开销\n");
    printf("✓ 低延迟，寄存器间直接通信\n");
    printf("✓ 适用于 Warp 级别的归约、扫描、广播\n");

    // 清理
    free(h_input);
    CUDA_CHECK(cudaFree(d_input));
    CUDA_CHECK(cudaFree(d_output_shuffle));
    CUDA_CHECK(cudaFree(d_output_shared));
    CUDA_CHECK(cudaEventDestroy(start));
    CUDA_CHECK(cudaEventDestroy(stop));

    return 0;
}

/**
 * 编译命令：
 * nvcc -o warp_shuffle 01_warp_shuffle.cu
 *
 * 知识点：
 * 1. __shfl_sync(mask, val, srcLane) - 从指定 lane 读取
 * 2. __shfl_up_sync(mask, val, delta) - 从较低 lane 读取
 * 3. __shfl_down_sync(mask, val, delta) - 从较高 lane 读取
 * 4. __shfl_xor_sync(mask, val, laneMask) - XOR 模式
 * 5. mask: 参与线程掩码（通常 0xffffffff 表示全部）
 * 6. Warp Shuffle 比 Shared Memory 更快、更节省资源
 */
