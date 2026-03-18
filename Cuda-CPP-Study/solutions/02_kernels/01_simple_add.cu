// 参考答案 6: 简单向量加法

#include <stdio.h>
#include <cuda_runtime.h>
#include <math.h>

#define N 1024
#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

__global__ void vector_add(float *a, float *b, float *c, int n) {
    int idx = threadIdx.x;
    if (idx < n) {
        c[idx] = a[idx] + b[idx];
    }
}

int main() {
    float *h_a, *h_b, *h_c;
    float *d_a, *d_b, *d_c;
    size_t bytes = N * sizeof(float);

    // 分配主机内存
    h_a = (float*)malloc(bytes);
    h_b = (float*)malloc(bytes);
    h_c = (float*)malloc(bytes);

    // 初始化
    for (int i = 0; i < N; i++) {
        h_a[i] = i;
        h_b[i] = i * 2.0f;
    }

    // 分配设备内存
    CUDA_CHECK(cudaMalloc(&d_a, bytes));
    CUDA_CHECK(cudaMalloc(&d_b, bytes));
    CUDA_CHECK(cudaMalloc(&d_c, bytes));

    // 拷贝到设备
    CUDA_CHECK(cudaMemcpy(d_a, h_a, bytes, cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_b, h_b, bytes, cudaMemcpyHostToDevice));

    // 调用 kernel
    vector_add<<<1, N>>>(d_a, d_b, d_c, N);
    CUDA_CHECK(cudaGetLastError());
    CUDA_CHECK(cudaDeviceSynchronize());

    // 拷贝结果
    CUDA_CHECK(cudaMemcpy(h_c, d_c, bytes, cudaMemcpyDeviceToHost));

    // 验证
    bool success = true;
    for (int i = 0; i < N; i++) {
        float expected = h_a[i] + h_b[i];
        if (fabsf(h_c[i] - expected) > 1e-5) {
            printf("错误: h_c[%d] = %f, 期望 %f\n", i, h_c[i], expected);
            success = false;
            break;
        }
    }

    // 释放内存
    CUDA_CHECK(cudaFree(d_a));
    CUDA_CHECK(cudaFree(d_b));
    CUDA_CHECK(cudaFree(d_c));
    free(h_a);
    free(h_b);
    free(h_c);

    if (success) {
        printf("向量加法正确!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}
