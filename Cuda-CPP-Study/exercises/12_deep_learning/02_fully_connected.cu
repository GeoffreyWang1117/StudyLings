// 练习 122: 全连接层
//
// 目标: 实现全连接层的前向和反向传播
//
// 任务:
// 1. 实现矩阵乘法 Y = XW + b
// 2. 实现反向传播计算梯度
// 3. 优化内存访问

#include <stdio.h>
#include <cuda_runtime.h>

#define BATCH_SIZE 128
#define INPUT_DIM 784   // 28x28
#define OUTPUT_DIM 256
#define TILE_SIZE 16

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// TODO: 实现全连接层 forward
// Y = XW + b
// X: [batch_size, input_dim]
// W: [input_dim, output_dim]
// b: [output_dim]
// Y: [batch_size, output_dim]
__global__ void fc_forward(float *X, float *W, float *b, float *Y,
                           int batch_size, int input_dim, int output_dim) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;  // batch
    int col = blockIdx.x * blockDim.x + threadIdx.x;  // output neuron

    if (row < batch_size && col < output_dim) {
        float sum = 0.0f;

        // TODO: 计算 Y[row][col] = sum(X[row][k] * W[k][col]) + b[col]
        // for (int k = 0; k < input_dim; k++) {
        //     sum += X[row * input_dim + k] * W[k * output_dim + col];
        // }
        // Y[row * output_dim + col] = sum + b[col];
    }
}

// TODO: 实现全连接层 backward
// 计算三个梯度:
// 1. dL/dX = dL/dY * W^T
// 2. dL/dW = X^T * dL/dY
// 3. dL/db = sum(dL/dY, axis=0)
__global__ void fc_backward_input(float *grad_Y, float *W, float *grad_X,
                                  int batch_size, int input_dim, int output_dim) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    if (row < batch_size && col < input_dim) {
        float sum = 0.0f;
        // TODO: grad_X[row][col] = sum(grad_Y[row][k] * W[col][k])
        // for (int k = 0; k < output_dim; k++) {
        //     sum += grad_Y[row * output_dim + k] * W[col * output_dim + k];
        // }
        // grad_X[row * input_dim + col] = sum;
    }
}

int main() {
    float *h_X, *h_W, *h_b, *h_Y;
    float *d_X, *d_W, *d_b, *d_Y;

    size_t x_bytes = BATCH_SIZE * INPUT_DIM * sizeof(float);
    size_t w_bytes = INPUT_DIM * OUTPUT_DIM * sizeof(float);
    size_t b_bytes = OUTPUT_DIM * sizeof(float);
    size_t y_bytes = BATCH_SIZE * OUTPUT_DIM * sizeof(float);

    h_X = (float*)malloc(x_bytes);
    h_W = (float*)malloc(w_bytes);
    h_b = (float*)malloc(b_bytes);
    h_Y = (float*)malloc(y_bytes);

    // 初始化
    for (int i = 0; i < BATCH_SIZE * INPUT_DIM; i++) {
        h_X[i] = 0.01f;
    }
    for (int i = 0; i < INPUT_DIM * OUTPUT_DIM; i++) {
        h_W[i] = 0.01f;
    }
    for (int i = 0; i < OUTPUT_DIM; i++) {
        h_b[i] = 0.1f;
    }

    CUDA_CHECK(cudaMalloc(&d_X, x_bytes));
    CUDA_CHECK(cudaMalloc(&d_W, w_bytes));
    CUDA_CHECK(cudaMalloc(&d_b, b_bytes));
    CUDA_CHECK(cudaMalloc(&d_Y, y_bytes));

    CUDA_CHECK(cudaMemcpy(d_X, h_X, x_bytes, cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_W, h_W, w_bytes, cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_b, h_b, b_bytes, cudaMemcpyHostToDevice));

    dim3 blockDim(TILE_SIZE, TILE_SIZE);
    dim3 gridDim((OUTPUT_DIM + TILE_SIZE - 1) / TILE_SIZE,
                 (BATCH_SIZE + TILE_SIZE - 1) / TILE_SIZE);

    fc_forward<<<gridDim, blockDim>>>(d_X, d_W, d_b, d_Y,
                                      BATCH_SIZE, INPUT_DIM, OUTPUT_DIM);
    CUDA_CHECK(cudaDeviceSynchronize());

    CUDA_CHECK(cudaMemcpy(h_Y, d_Y, y_bytes, cudaMemcpyDeviceToHost));

    // 验证：所有输出应该大于0（因为有bias）
    bool success = true;
    for (int i = 0; i < BATCH_SIZE * OUTPUT_DIM; i++) {
        if (h_Y[i] <= 0.0f) {
            printf("错误: Y[%d] = %f\n", i, h_Y[i]);
            success = false;
            break;
        }
    }

    printf("输出样本: Y[0][0] = %f\n", h_Y[0]);

    CUDA_CHECK(cudaFree(d_X));
    CUDA_CHECK(cudaFree(d_W));
    CUDA_CHECK(cudaFree(d_b));
    CUDA_CHECK(cudaFree(d_Y));
    free(h_X);
    free(h_W);
    free(h_b);
    free(h_Y);

    if (success) {
        printf("全连接层 forward 正确!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}

// I AM NOT DONE
