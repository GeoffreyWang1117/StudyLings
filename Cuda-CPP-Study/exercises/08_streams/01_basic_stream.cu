// 练习 81: CUDA 流基础
//
// 目标: 使用 CUDA 流实现并发执行
//
// 任务:
// 1. 创建多个 CUDA 流
// 2. 在不同流中并发执行 kernel
// 3. 正确销毁流

#include <stdio.h>
#include <cuda_runtime.h>

#define N 1024
#define NUM_STREAMS 4

__global__ void simple_kernel(float *data, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        // 模拟一些计算
        for (int i = 0; i < 100; i++) {
            data[idx] = data[idx] * 1.01f;
        }
    }
}

int main() {
    // TODO: 创建流数组
    // cudaStream_t streams[NUM_STREAMS];
    // for (int i = 0; i < NUM_STREAMS; i++) {
    //     cudaStreamCreate(&streams[i]);
    // }

    // 为每个流分配数据
    float *d_data[NUM_STREAMS];
    int elements_per_stream = N / NUM_STREAMS;

    for (int i = 0; i < NUM_STREAMS; i++) {
        cudaMalloc(&d_data[i], elements_per_stream * sizeof(float));
        // TODO: 使用流进行内存操作
    }

    // TODO: 在不同流中启动 kernel
    // for (int i = 0; i < NUM_STREAMS; i++) {
    //     simple_kernel<<<(elements_per_stream + 255) / 256, 256, 0, streams[i]>>>(
    //         d_data[i], elements_per_stream);
    // }

    // TODO: 同步所有流
    // cudaDeviceSynchronize();

    // 清理
    for (int i = 0; i < NUM_STREAMS; i++) {
        cudaFree(d_data[i]);
        // TODO: 销毁流
        // cudaStreamDestroy(streams[i]);
    }

    printf("流操作完成!\n");
    printf("TEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
