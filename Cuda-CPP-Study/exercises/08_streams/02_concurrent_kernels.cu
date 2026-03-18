// 练习 82: 并发 Kernel 执行
//
// 目标: 使用流并发执行多个 kernel
//
// 任务:
// 1. 创建多个流
// 2. 在不同流中启动 kernel
// 3. 观察并发执行

#include <stdio.h>
#include <cuda_runtime.h>

#define N 1000000
#define NUM_STREAMS 4
#define BLOCK_SIZE 256

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

__global__ void compute_kernel(float *data, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        // 模拟计算密集型操作
        float result = data[idx];
        for (int i = 0; i < 1000; i++) {
            result = sinf(result) * cosf(result);
        }
        data[idx] = result;
    }
}

int main() {
    // TODO: 创建流
    cudaStream_t streams[NUM_STREAMS];
    // for (int i = 0; i < NUM_STREAMS; i++) {
    //     CUDA_CHECK(cudaStreamCreate(&streams[i]));
    // }

    // 为每个流分配数据
    float *d_data[NUM_STREAMS];
    int elements_per_stream = N / NUM_STREAMS;
    size_t bytes_per_stream = elements_per_stream * sizeof(float);

    for (int i = 0; i < NUM_STREAMS; i++) {
        CUDA_CHECK(cudaMalloc(&d_data[i], bytes_per_stream));
    }

    int grid_size = (elements_per_stream + BLOCK_SIZE - 1) / BLOCK_SIZE;

    // TODO: 在不同流中启动 kernel
    // for (int i = 0; i < NUM_STREAMS; i++) {
    //     compute_kernel<<<grid_size, BLOCK_SIZE, 0, streams[i]>>>(
    //         d_data[i], elements_per_stream);
    // }

    // 同步所有流
    CUDA_CHECK(cudaDeviceSynchronize());

    // 清理
    for (int i = 0; i < NUM_STREAMS; i++) {
        CUDA_CHECK(cudaFree(d_data[i]));
        // TODO: 销毁流
        // CUDA_CHECK(cudaStreamDestroy(streams[i]));
    }

    printf("并发 kernel 执行完成!\n");
    printf("TEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
