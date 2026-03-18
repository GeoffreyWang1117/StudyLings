/**
 * 练习 223: Unified Memory 并发访问
 *
 * 学习目标：
 * - 理解 CPU 和 GPU 并发访问统一内存的机制
 * - 使用 Streams 实现多 Kernel 并发
 * - 处理统一内存的数据一致性问题
 *
 * 任务：
 * 1. 实现多个 stream 并发执行不同的 kernel
 * 2. 确保 CPU 和 GPU 访问的同步
 * 3. 使用 cudaStreamAttachMemAsync() 管理内存归属
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

__global__ void process_partition(float *data, int offset, int n, float scale) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        int global_idx = offset + idx;
        data[global_idx] = data[global_idx] * scale + 1.0f;
    }
}

int main() {
    const int N = 1 << 22;  // 4M elements
    const int NUM_STREAMS = 4;
    const int PARTITION_SIZE = N / NUM_STREAMS;
    size_t bytes = N * sizeof(float);

    // 分配统一内存
    float *data;
    CUDA_CHECK(cudaMallocManaged(&data, bytes));

    // 初始化数据
    for (int i = 0; i < N; i++) {
        data[i] = (float)i;
    }

    // TODO 1: 创建多个 CUDA streams
    cudaStream_t streams[NUM_STREAMS];
    // 提示：for (int i = 0; i < NUM_STREAMS; i++)
    //          cudaStreamCreate(&streams[i]);


    printf("=== Unified Memory 并发访问测试 ===\n");
    printf("数据规模: %d elements, 分成 %d 个分区\n\n", N, NUM_STREAMS);

    // TODO 2: 为每个 stream 附加对应的内存分区
    // 提示：cudaStreamAttachMemAsync(stream, data + offset,
    //                                 partition_bytes, cudaMemAttachSingle);


    cudaEvent_t start, stop;
    CUDA_CHECK(cudaEventCreate(&start));
    CUDA_CHECK(cudaEventCreate(&stop));

    CUDA_CHECK(cudaEventRecord(start));

    // TODO 3: 在每个 stream 上启动 kernel
    int threadsPerBlock = 256;
    for (int i = 0; i < NUM_STREAMS; i++) {
        int offset = i * PARTITION_SIZE;
        int blocksPerGrid = (PARTITION_SIZE + threadsPerBlock - 1) / threadsPerBlock;

        // 提示：process_partition<<<blocksPerGrid, threadsPerBlock, 0, streams[i]>>>
        //          (data, offset, PARTITION_SIZE, 2.0f);
    }

    CUDA_CHECK(cudaEventRecord(stop));

    // TODO 4: 等待所有 streams 完成
    // 提示：for (int i = 0; i < NUM_STREAMS; i++)
    //          cudaStreamSynchronize(streams[i]);


    float milliseconds = 0;
    CUDA_CHECK(cudaEventElapsedTime(&milliseconds, start, stop));

    printf("并发执行时间: %.3f ms\n\n", milliseconds);

    // TODO 5: 验证结果（CPU 访问）
    printf("验证结果...\n");
    bool success = true;
    // 注意：在 CPU 访问前，确保 GPU 已完成
    CUDA_CHECK(cudaDeviceSynchronize());

    for (int i = 0; i < N; i++) {
        float expected = (float)i * 2.0f + 1.0f;
        if (fabsf(data[i] - expected) > 1e-5) {
            success = false;
            printf("✗ data[%d] = %f, expected %f\n", i, data[i], expected);
            break;
        }
    }

    if (success) {
        printf("✓ 所有数据验证通过！\n\n");
    }

    // 清理
    for (int i = 0; i < NUM_STREAMS; i++) {
        CUDA_CHECK(cudaStreamDestroy(streams[i]));
    }
    CUDA_CHECK(cudaEventDestroy(start));
    CUDA_CHECK(cudaEventDestroy(stop));
    CUDA_CHECK(cudaFree(data));

    printf("关键要点：\n");
    printf("1. 使用 cudaStreamAttachMemAsync() 可以精确控制内存归属\n");
    printf("2. 不同 stream 可以并发访问不同内存区域\n");
    printf("3. CPU 访问前必须确保 GPU 操作完成（cudaDeviceSynchronize）\n");
    printf("4. Unified Memory 自动处理 CPU-GPU 数据一致性\n");

    return 0;
}

/**
 * 编译命令：
 * nvcc -o um_concurrent 03_um_concurrent.cu
 *
 * 知识点：
 * 1. cudaStreamAttachMemAsync() - 将内存附加到特定 stream
 * 2. cudaMemAttachGlobal - 全局访问（默认）
 * 3. cudaMemAttachSingle - 单 stream 访问
 * 4. 多 stream 可以并发处理不同内存分区
 * 5. CPU-GPU 同步是确保数据一致性的关键
 */
