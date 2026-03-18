// 练习 161: CUDA Graphs 基础
//
// 目标: 使用 CUDA Graphs 减少 kernel 启动开销
//
// 任务:
// 1. 理解 CUDA Graphs 的概念
// 2. 使用 Stream Capture 创建 graph
// 3. 对比性能提升

#include <stdio.h>
#include <cuda_runtime.h>
#include <time.h>

#define N 1000000
#define ITERATIONS 1000
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

__global__ void vectorAdd(float *a, float *b, float *c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) {
        c[i] = a[i] + b[i];
    }
}

__global__ void vectorMul(float *a, float *b, float *c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) {
        c[i] = a[i] * b[i];
    }
}

int main() {
    cudaDeviceProp prop;
    CUDA_CHECK(cudaGetDeviceProperties(&prop, 0));

    printf("使用 %s 测试 CUDA Graphs\n\n", prop.name);

    float *d_a, *d_b, *d_c, *d_temp;
    CUDA_CHECK(cudaMalloc(&d_a, N * sizeof(float)));
    CUDA_CHECK(cudaMalloc(&d_b, N * sizeof(float)));
    CUDA_CHECK(cudaMalloc(&d_c, N * sizeof(float)));
    CUDA_CHECK(cudaMalloc(&d_temp, N * sizeof(float)));

    dim3 blockDim(BLOCK_SIZE);
    dim3 gridDim((N + BLOCK_SIZE - 1) / BLOCK_SIZE);

    // 初始化数据
    cudaStream_t stream;
    CUDA_CHECK(cudaStreamCreate(&stream));

    // 方法 1: 传统方式 - 重复启动 kernels
    double start = get_time();
    for (int i = 0; i < ITERATIONS; i++) {
        vectorAdd<<<gridDim, blockDim, 0, stream>>>(d_a, d_b, d_temp, N);
        vectorMul<<<gridDim, blockDim, 0, stream>>>(d_temp, d_b, d_c, N);
    }
    CUDA_CHECK(cudaStreamSynchronize(stream));
    double traditional_time = get_time() - start;

    printf("传统方式时间: %.3f ms\n", traditional_time * 1000);

    // TODO: 方法 2 - 使用 CUDA Graph
    // 1. 创建 graph
    cudaGraph_t graph;
    cudaGraphExec_t graphExec;

    // 2. 使用 Stream Capture 记录操作序列
    // CUDA_CHECK(cudaStreamBeginCapture(stream, cudaStreamCaptureModeGlobal));
    // vectorAdd<<<gridDim, blockDim, 0, stream>>>(d_a, d_b, d_temp, N);
    // vectorMul<<<gridDim, blockDim, 0, stream>>>(d_temp, d_b, d_c, N);
    // CUDA_CHECK(cudaStreamEndCapture(stream, &graph));

    // 3. 实例化 graph
    // CUDA_CHECK(cudaGraphInstantiate(&graphExec, graph, NULL, NULL, 0));

    // 4. 重复执行 graph
    // start = get_time();
    // for (int i = 0; i < ITERATIONS; i++) {
    //     CUDA_CHECK(cudaGraphLaunch(graphExec, stream));
    // }
    // CUDA_CHECK(cudaStreamSynchronize(stream));
    // double graph_time = get_time() - start;

    // printf("CUDA Graph 时间: %.3f ms\n", graph_time * 1000);
    // printf("加速比: %.2fx\n", traditional_time / graph_time);

    // TODO: 清理
    // CUDA_CHECK(cudaGraphExecDestroy(graphExec));
    // CUDA_CHECK(cudaGraphDestroy(graph));

    CUDA_CHECK(cudaStreamDestroy(stream));
    CUDA_CHECK(cudaFree(d_a));
    CUDA_CHECK(cudaFree(d_b));
    CUDA_CHECK(cudaFree(d_c));
    CUDA_CHECK(cudaFree(d_temp));

    printf("\nCUDA Graphs 基础测试完成!\n");
    printf("TEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
