// 练习 124: Batch Normalization
//
// 目标: 实现 Batch Normalization 的前向和反向传播
//
// 任务:
// 1. 实现 BN 前向传播
// 2. 实现 BN 反向传播
// 3. 理解 running mean/variance

#include <stdio.h>
#include <cuda_runtime.h>
#include <math.h>

#define N 1024      // batch size
#define C 128       // channels
#define BLOCK_SIZE 256

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// TODO: Batch Normalization 前向传播
// y = gamma * (x - mean) / sqrt(variance + epsilon) + beta
__global__ void batchnorm_forward(
    float *x, float *y,
    float *gamma, float *beta,
    float *mean, float *variance,
    int batch_size, int channels,
    float epsilon) {

    int c = blockIdx.x * blockDim.x + threadIdx.x;

    if (c < channels) {
        // TODO: 计算该 channel 的均值
        // float sum = 0.0f;
        // for (int n = 0; n < batch_size; n++) {
        //     sum += x[n * channels + c];
        // }
        // mean[c] = sum / batch_size;

        // TODO: 计算该 channel 的方差
        // float var_sum = 0.0f;
        // for (int n = 0; n < batch_size; n++) {
        //     float diff = x[n * channels + c] - mean[c];
        //     var_sum += diff * diff;
        // }
        // variance[c] = var_sum / batch_size;

        // TODO: 归一化并应用缩放和偏移
        // float std = sqrtf(variance[c] + epsilon);
        // for (int n = 0; n < batch_size; n++) {
        //     int idx = n * channels + c;
        //     y[idx] = gamma[c] * (x[idx] - mean[c]) / std + beta[c];
        // }
    }
}

// TODO: Batch Normalization 反向传播
__global__ void batchnorm_backward(
    float *x, float *dy,
    float *dx, float *dgamma, float *dbeta,
    float *gamma, float *mean, float *variance,
    int batch_size, int channels,
    float epsilon) {

    int c = blockIdx.x * blockDim.x + threadIdx.x;

    if (c < channels) {
        float std = sqrtf(variance[c] + epsilon);

        // TODO: 计算 dgamma 和 dbeta
        // dgamma[c] = 0.0f;
        // dbeta[c] = 0.0f;
        // for (int n = 0; n < batch_size; n++) {
        //     int idx = n * channels + c;
        //     dbeta[c] += dy[idx];
        //     dgamma[c] += dy[idx] * (x[idx] - mean[c]) / std;
        // }

        // TODO: 计算 dx
        // float dmean = 0.0f;
        // float dvar = 0.0f;
        //
        // for (int n = 0; n < batch_size; n++) {
        //     int idx = n * channels + c;
        //     float x_norm = (x[idx] - mean[c]) / std;
        //     dmean += dy[idx] * gamma[c] * (-1.0f / std);
        //     dvar += dy[idx] * gamma[c] * x_norm * (-0.5f / variance[c]);
        // }
        //
        // for (int n = 0; n < batch_size; n++) {
        //     int idx = n * channels + c;
        //     float x_norm = (x[idx] - mean[c]) / std;
        //     dx[idx] = dy[idx] * gamma[c] / std +
        //              dvar * 2.0f * (x[idx] - mean[c]) / batch_size +
        //              dmean / batch_size;
        // }
    }
}

int main() {
    printf("Batch Normalization 测试\n\n");

    float *h_x = (float*)malloc(N * C * sizeof(float));
    float *h_y = (float*)malloc(N * C * sizeof(float));
    float *h_gamma = (float*)malloc(C * sizeof(float));
    float *h_beta = (float*)malloc(C * sizeof(float));

    // 初始化
    for (int i = 0; i < N * C; i++) {
        h_x[i] = (float)(rand() % 100) / 10.0f;
    }
    for (int i = 0; i < C; i++) {
        h_gamma[i] = 1.0f;
        h_beta[i] = 0.0f;
    }

    float *d_x, *d_y, *d_gamma, *d_beta, *d_mean, *d_variance;
    CUDA_CHECK(cudaMalloc(&d_x, N * C * sizeof(float)));
    CUDA_CHECK(cudaMalloc(&d_y, N * C * sizeof(float)));
    CUDA_CHECK(cudaMalloc(&d_gamma, C * sizeof(float)));
    CUDA_CHECK(cudaMalloc(&d_beta, C * sizeof(float)));
    CUDA_CHECK(cudaMalloc(&d_mean, C * sizeof(float)));
    CUDA_CHECK(cudaMalloc(&d_variance, C * sizeof(float)));

    CUDA_CHECK(cudaMemcpy(d_x, h_x, N * C * sizeof(float), cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_gamma, h_gamma, C * sizeof(float), cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_beta, h_beta, C * sizeof(float), cudaMemcpyHostToDevice));

    int grid_size = (C + BLOCK_SIZE - 1) / BLOCK_SIZE;
    float epsilon = 1e-5f;

    batchnorm_forward<<<grid_size, BLOCK_SIZE>>>(
        d_x, d_y, d_gamma, d_beta, d_mean, d_variance,
        N, C, epsilon);

    CUDA_CHECK(cudaDeviceSynchronize());

    CUDA_CHECK(cudaMemcpy(h_y, d_y, N * C * sizeof(float), cudaMemcpyDeviceToHost));

    printf("BN 前向传播样本: y[0] = %.3f, y[1] = %.3f\n", h_y[0], h_y[1]);

    CUDA_CHECK(cudaFree(d_x));
    CUDA_CHECK(cudaFree(d_y));
    CUDA_CHECK(cudaFree(d_gamma));
    CUDA_CHECK(cudaFree(d_beta));
    CUDA_CHECK(cudaFree(d_mean));
    CUDA_CHECK(cudaFree(d_variance));
    free(h_x);
    free(h_y);
    free(h_gamma);
    free(h_beta);

    printf("\nBatch Normalization 完成!\n");
    printf("TEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
