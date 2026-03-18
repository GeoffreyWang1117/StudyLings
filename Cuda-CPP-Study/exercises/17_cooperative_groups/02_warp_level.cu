// 练习 172: Cooperative Groups - Warp Level
//
// 目标: 使用 warp-level primitives
//
// 任务:
// 1. 理解 coalesced_threads 和 tiled_partition
// 2. 实现 warp-level reduction
// 3. 避免 warp divergence

#include <stdio.h>
#include <cuda_runtime.h>
#include <cooperative_groups.h>

namespace cg = cooperative_groups;

#define N 1024
#define BLOCK_SIZE 256

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// TODO: 使用 warp-level shuffle 实现 reduction
__device__ float warp_reduce(float val) {
    // TODO: 获取 warp
    // cg::coalesced_group warp = cg::coalesced_threads();

    // TODO: 使用 shfl_down 进行 reduction
    // for (int offset = warp.size() / 2; offset > 0; offset /= 2) {
    //     val += warp.shfl_down(val, offset);
    // }

    // return val;
    return 0.0f;  // 临时返回值
}

// TODO: 使用 tiled_partition 实现 block-level reduction
__global__ void warp_reduce_kernel(float *input, float *output, int n) {
    __shared__ float warp_sums[BLOCK_SIZE / 32];

    // TODO: 获取 thread block 和计算全局索引
    // cg::thread_block block = cg::this_thread_block();
    int i = blockIdx.x * blockDim.x + threadIdx.x;

    // 加载数据并进行 warp-level reduction
    float val = (i < n) ? input[i] : 0.0f;
    // val = warp_reduce(val);

    // TODO: 每个 warp 的第一个线程写入 shared memory
    // int warp_id = threadIdx.x / 32;
    // int lane = threadIdx.x % 32;
    // if (lane == 0) {
    //     warp_sums[warp_id] = val;
    // }
    // block.sync();

    // TODO: 第一个 warp 对所有 warp 的结果进行最终 reduction
    // if (warp_id == 0) {
    //     val = (lane < blockDim.x / 32) ? warp_sums[lane] : 0.0f;
    //     val = warp_reduce(val);
    //
    //     if (lane == 0) {
    //         output[blockIdx.x] = val;
    //     }
    // }
}

// TODO: 使用 tiled_partition 分割线程组
__global__ void tiled_partition_demo(int *data, int n) {
    // TODO: 创建 4-thread tiles
    // cg::thread_block block = cg::this_thread_block();
    // cg::thread_block_tile<4> tile4 = cg::tiled_partition<4>(block);

    int i = blockIdx.x * blockDim.x + threadIdx.x;

    if (i < n) {
        // TODO: 在 tile 内进行通信
        // int value = data[i];
        // int sum = 0;

        // 收集 tile 内所有线程的值
        // for (int j = 0; j < tile4.size(); j++) {
        //     sum += tile4.shfl(value, j);
        // }

        // data[i] = sum;
    }
}

int main() {
    printf("Cooperative Groups Warp-Level 测试\n\n");

    // 测试 warp reduction
    float *h_input = (float*)malloc(N * sizeof(float));
    float *h_output = (float*)malloc((N / BLOCK_SIZE) * sizeof(float));

    for (int i = 0; i < N; i++) {
        h_input[i] = 1.0f;
    }

    float *d_input, *d_output;
    CUDA_CHECK(cudaMalloc(&d_input, N * sizeof(float)));
    CUDA_CHECK(cudaMalloc(&d_output, (N / BLOCK_SIZE) * sizeof(float)));

    CUDA_CHECK(cudaMemcpy(d_input, h_input, N * sizeof(float), cudaMemcpyHostToDevice));

    dim3 blockDim(BLOCK_SIZE);
    dim3 gridDim(N / BLOCK_SIZE);

    warp_reduce_kernel<<<gridDim, blockDim>>>(d_input, d_output, N);
    CUDA_CHECK(cudaDeviceSynchronize());

    CUDA_CHECK(cudaMemcpy(h_output, d_output, (N / BLOCK_SIZE) * sizeof(float),
                          cudaMemcpyDeviceToHost));

    float sum = 0.0f;
    for (int i = 0; i < N / BLOCK_SIZE; i++) {
        sum += h_output[i];
    }

    printf("Warp Reduction 结果: %.0f (期望: %d)\n", sum, N);

    // 测试 tiled partition
    int *h_data = (int*)malloc(16 * sizeof(int));
    for (int i = 0; i < 16; i++) {
        h_data[i] = i;
    }

    int *d_data;
    CUDA_CHECK(cudaMalloc(&d_data, 16 * sizeof(int)));
    CUDA_CHECK(cudaMemcpy(d_data, h_data, 16 * sizeof(int), cudaMemcpyHostToDevice));

    tiled_partition_demo<<<1, 16>>>(d_data, 16);
    CUDA_CHECK(cudaDeviceSynchronize());

    CUDA_CHECK(cudaMemcpy(h_data, d_data, 16 * sizeof(int), cudaMemcpyDeviceToHost));

    printf("\nTiled Partition 演示结果:\n");
    for (int i = 0; i < 16; i += 4) {
        printf("Tile %d: [%d, %d, %d, %d]\n", i/4,
               h_data[i], h_data[i+1], h_data[i+2], h_data[i+3]);
    }

    CUDA_CHECK(cudaFree(d_input));
    CUDA_CHECK(cudaFree(d_output));
    CUDA_CHECK(cudaFree(d_data));
    free(h_input);
    free(h_output);
    free(h_data);

    printf("\nWarp-Level Cooperative Groups 测试完成!\n");
    printf("TEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
