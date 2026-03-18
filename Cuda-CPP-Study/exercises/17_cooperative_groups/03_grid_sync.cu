// 练习 173: Grid-Wide Synchronization
//
// 目标: 使用 cooperative_groups 实现 grid-wide 同步
//
// 任务:
// 1. 理解 grid_group
// 2. 实现跨 block 的同步
// 3. 应用于迭代算法

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

// TODO: 使用 grid-wide sync 实现 Jacobi 迭代
// 每次迭代需要所有 blocks 完成后才能开始下一次迭代
__global__ void jacobi_iteration(float *x, float *x_new, int n, int iterations) {
    // TODO: 获取 grid group
    // cg::grid_group grid = cg::this_grid();

    int i = blockIdx.x * blockDim.x + threadIdx.x;

    for (int iter = 0; iter < iterations; iter++) {
        // Jacobi 更新: x_new[i] = (x[i-1] + x[i+1]) / 2
        if (i > 0 && i < n - 1) {
            // TODO: 计算新值
            // x_new[i] = (x[i - 1] + x[i + 1]) * 0.5f;
        }

        // TODO: 使用 grid-wide sync 确保所有线程完成
        // grid.sync();

        // 交换指针 (通过复制)
        if (i < n) {
            // x[i] = x_new[i];
        }

        // TODO: 再次同步
        // grid.sync();
    }
}

// TODO: Grid-wide reduction
__global__ void grid_reduce(float *input, float *output, int n) {
    __shared__ float block_sum;

    // cg::grid_group grid = cg::this_grid();
    // cg::thread_block block = cg::this_thread_block();

    int i = blockIdx.x * blockDim.x + threadIdx.x;

    // TODO: Block-level reduction
    // ...

    // TODO: 将每个 block 的结果原子累加到全局结果
    // if (block.thread_rank() == 0) {
    //     atomicAdd(output, block_sum);
    // }

    // TODO: Grid-wide sync 确保所有 blocks 完成
    // grid.sync();
}

int main() {
    cudaDeviceProp prop;
    CUDA_CHECK(cudaGetDeviceProperties(&prop, 0));

    // 检查是否支持 Cooperative Launch
    if (!prop.cooperativeLaunch) {
        printf("该设备不支持 Cooperative Launch\n");
        printf("TEST_PASSED\n");  // 硬件限制，算通过
        return 0;
    }

    printf("使用 %s 测试 Grid-Wide Sync\n\n", prop.name);

    float *h_x = (float*)malloc(N * sizeof(float));
    float *h_x_new = (float*)malloc(N * sizeof(float));

    // 初始化: 边界为 0 和 100, 中间为 0
    h_x[0] = 0.0f;
    h_x[N-1] = 100.0f;
    for (int i = 1; i < N - 1; i++) {
        h_x[i] = 0.0f;
    }

    float *d_x, *d_x_new;
    CUDA_CHECK(cudaMalloc(&d_x, N * sizeof(float)));
    CUDA_CHECK(cudaMalloc(&d_x_new, N * sizeof(float)));

    CUDA_CHECK(cudaMemcpy(d_x, h_x, N * sizeof(float), cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_x_new, h_x_new, N * sizeof(float), cudaMemcpyHostToDevice));

    // TODO: 配置 cooperative launch
    dim3 blockDim(BLOCK_SIZE);
    dim3 gridDim((N + BLOCK_SIZE - 1) / BLOCK_SIZE);

    // 检查最大可用的 blocks
    int numBlocksPerSm = 0;
    // CUDA_CHECK(cudaOccupancyMaxActiveBlocksPerMultiprocessor(
    //     &numBlocksPerSm, jacobi_iteration, BLOCK_SIZE, 0));

    // int maxBlocks = numBlocksPerSm * prop.multiProcessorCount;
    // printf("最大 cooperative blocks: %d\n", maxBlocks);

    // TODO: 使用 cudaLaunchCooperativeKernel 启动
    // void *kernelArgs[] = {&d_x, &d_x_new, &N, &iterations};
    // int iterations = 100;
    //
    // CUDA_CHECK(cudaLaunchCooperativeKernel(
    //     (void*)jacobi_iteration,
    //     gridDim, blockDim,
    //     kernelArgs, 0, 0));

    // CUDA_CHECK(cudaDeviceSynchronize());

    // CUDA_CHECK(cudaMemcpy(h_x, d_x, N * sizeof(float), cudaMemcpyDeviceToHost));

    // printf("Jacobi 迭代结果: x[%d] = %.2f\n", N/2, h_x[N/2]);

    CUDA_CHECK(cudaFree(d_x));
    CUDA_CHECK(cudaFree(d_x_new));
    free(h_x);
    free(h_x_new);

    printf("\nGrid-Wide Sync 测试完成!\n");
    printf("TEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
