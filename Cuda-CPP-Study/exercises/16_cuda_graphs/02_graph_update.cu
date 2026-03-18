// 练习 162: CUDA Graph 更新
//
// 目标: 动态更新 graph 参数
//
// 任务:
// 1. 创建可重用的 graph
// 2. 更新 kernel 参数
// 3. 避免重新创建 graph 的开销

#include <stdio.h>
#include <cuda_runtime.h>

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

__global__ void saxpy(float a, float *x, float *y, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) {
        y[i] = a * x[i] + y[i];
    }
}

int main() {
    printf("CUDA Graph 参数更新测试\n\n");

    float *d_x, *d_y;
    CUDA_CHECK(cudaMalloc(&d_x, N * sizeof(float)));
    CUDA_CHECK(cudaMalloc(&d_y, N * sizeof(float)));

    float *h_x = (float*)malloc(N * sizeof(float));
    float *h_y = (float*)malloc(N * sizeof(float));

    for (int i = 0; i < N; i++) {
        h_x[i] = 1.0f;
        h_y[i] = 2.0f;
    }

    CUDA_CHECK(cudaMemcpy(d_x, h_x, N * sizeof(float), cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_y, h_y, N * sizeof(float), cudaMemcpyHostToDevice));

    cudaStream_t stream;
    CUDA_CHECK(cudaStreamCreate(&stream));

    dim3 blockDim(BLOCK_SIZE);
    dim3 gridDim((N + BLOCK_SIZE - 1) / BLOCK_SIZE);

    // TODO: 创建初始 graph (a = 2.0)
    float a = 2.0f;
    cudaGraph_t graph;
    cudaGraphExec_t graphExec;

    // CUDA_CHECK(cudaStreamBeginCapture(stream, cudaStreamCaptureModeGlobal));
    // saxpy<<<gridDim, blockDim, 0, stream>>>(a, d_x, d_y, N);
    // CUDA_CHECK(cudaStreamEndCapture(stream, &graph));
    // CUDA_CHECK(cudaGraphInstantiate(&graphExec, graph, NULL, NULL, 0));

    // 执行
    // CUDA_CHECK(cudaGraphLaunch(graphExec, stream));
    // CUDA_CHECK(cudaStreamSynchronize(stream));

    // CUDA_CHECK(cudaMemcpy(h_y, d_y, N * sizeof(float), cudaMemcpyDeviceToHost));
    // printf("初始结果 (a=%.1f): y[0] = %.1f (期望: 4.0)\n", a, h_y[0]);

    // TODO: 更新 graph 参数
    // 方法 1: 使用 cudaGraphExecKernelNodeSetParams
    //
    // 1. 获取 graph 中的 kernel node
    // cudaGraphNode_t nodes[10];
    // size_t numNodes;
    // CUDA_CHECK(cudaGraphGetNodes(graph, nodes, &numNodes));
    //
    // 2. 更新 kernel 参数
    // cudaKernelNodeParams params;
    // CUDA_CHECK(cudaGraphKernelNodeGetParams(nodes[0], &params));
    //
    // float new_a = 3.0f;
    // void* args[] = {&new_a, &d_x, &d_y, &N};
    // params.kernelParams = args;
    //
    // CUDA_CHECK(cudaGraphExecKernelNodeSetParams(graphExec, nodes[0], &params));

    // 3. 执行更新后的 graph
    // CUDA_CHECK(cudaGraphLaunch(graphExec, stream));
    // CUDA_CHECK(cudaStreamSynchronize(stream));

    // CUDA_CHECK(cudaMemcpy(h_y, d_y, N * sizeof(float), cudaMemcpyDeviceToHost));
    // printf("更新后结果 (a=%.1f): y[0] = %.1f (期望: 7.0)\n", new_a, h_y[0]);

    // TODO: 清理
    // CUDA_CHECK(cudaGraphExecDestroy(graphExec));
    // CUDA_CHECK(cudaGraphDestroy(graph));

    CUDA_CHECK(cudaStreamDestroy(stream));
    CUDA_CHECK(cudaFree(d_x));
    CUDA_CHECK(cudaFree(d_y));
    free(h_x);
    free(h_y);

    printf("\nGraph 更新测试完成!\n");
    printf("TEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
