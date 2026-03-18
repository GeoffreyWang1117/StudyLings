// 练习 125: 2D 卷积层
//
// 目标: 实现深度学习中的 2D 卷积
//
// 任务:
// 1. 实现 im2col + GEMM 卷积
// 2. 优化 shared memory 使用
// 3. 处理 padding 和 stride

#include <stdio.h>
#include <cuda_runtime.h>

#define BATCH 4
#define IN_C 3
#define IN_H 32
#define IN_W 32
#define OUT_C 16
#define K_H 3
#define K_W 3
#define PADDING 1
#define STRIDE 1

#define OUT_H ((IN_H + 2 * PADDING - K_H) / STRIDE + 1)
#define OUT_W ((IN_W + 2 * PADDING - K_W) / STRIDE + 1)

#define BLOCK_SIZE 16

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// TODO: 实现 2D 卷积前向传播
// Input: [N, C_in, H, W]
// Weight: [C_out, C_in, K_H, K_W]
// Output: [N, C_out, H_out, W_out]
__global__ void conv2d_forward(
    float *input, float *weight, float *bias, float *output,
    int batch, int in_c, int in_h, int in_w,
    int out_c, int k_h, int k_w,
    int padding, int stride) {

    int n = blockIdx.z;
    int oc = blockIdx.y;
    int oh = blockIdx.x / ((in_w + 2 * padding - k_w) / stride + 1);
    int ow = blockIdx.x % ((in_w + 2 * padding - k_w) / stride + 1);

    int tid = threadIdx.x;

    if (n < batch && oc < out_c) {
        float sum = 0.0f;

        // TODO: 遍历输入通道和卷积核
        // for (int ic = 0; ic < in_c; ic++) {
        //     for (int kh = 0; kh < k_h; kh++) {
        //         for (int kw = 0; kw < k_w; kw++) {
        //             int ih = oh * stride + kh - padding;
        //             int iw = ow * stride + kw - padding;
        //
        //             // 检查边界 (padding)
        //             if (ih >= 0 && ih < in_h && iw >= 0 && iw < in_w) {
        //                 int input_idx = ((n * in_c + ic) * in_h + ih) * in_w + iw;
        //                 int weight_idx = ((oc * in_c + ic) * k_h + kh) * k_w + kw;
        //                 sum += input[input_idx] * weight[weight_idx];
        //             }
        //         }
        //     }
        // }

        // TODO: 添加 bias
        // sum += bias[oc];

        // 存储结果
        // int out_h = (in_h + 2 * padding - k_h) / stride + 1;
        // int out_w = (in_w + 2 * padding - k_w) / stride + 1;
        // int output_idx = ((n * out_c + oc) * out_h + oh) * out_w + ow;
        // output[output_idx] = sum;
    }
}

// TODO: 使用 shared memory 优化的卷积
__global__ void conv2d_shared(
    float *input, float *weight, float *bias, float *output,
    int batch, int in_c, int in_h, int in_w,
    int out_c, int k_h, int k_w,
    int padding, int stride) {

    // TODO: 使用 shared memory 缓存输入 tile
    // __shared__ float tile[BLOCK_SIZE][BLOCK_SIZE];

    // TODO: 实现优化版本
}

int main() {
    printf("2D 卷积层测试\n");
    printf("输入: [%d, %d, %d, %d]\n", BATCH, IN_C, IN_H, IN_W);
    printf("卷积核: [%d, %d, %d, %d]\n", OUT_C, IN_C, K_H, K_W);
    printf("输出: [%d, %d, %d, %d]\n\n", BATCH, OUT_C, OUT_H, OUT_W);

    size_t input_size = BATCH * IN_C * IN_H * IN_W * sizeof(float);
    size_t weight_size = OUT_C * IN_C * K_H * K_W * sizeof(float);
    size_t bias_size = OUT_C * sizeof(float);
    size_t output_size = BATCH * OUT_C * OUT_H * OUT_W * sizeof(float);

    float *h_input = (float*)malloc(input_size);
    float *h_weight = (float*)malloc(weight_size);
    float *h_bias = (float*)malloc(bias_size);
    float *h_output = (float*)malloc(output_size);

    // 初始化
    for (int i = 0; i < BATCH * IN_C * IN_H * IN_W; i++) {
        h_input[i] = (float)(rand() % 10) / 10.0f;
    }
    for (int i = 0; i < OUT_C * IN_C * K_H * K_W; i++) {
        h_weight[i] = (float)(rand() % 10) / 10.0f;
    }
    for (int i = 0; i < OUT_C; i++) {
        h_bias[i] = 0.1f;
    }

    float *d_input, *d_weight, *d_bias, *d_output;
    CUDA_CHECK(cudaMalloc(&d_input, input_size));
    CUDA_CHECK(cudaMalloc(&d_weight, weight_size));
    CUDA_CHECK(cudaMalloc(&d_bias, bias_size));
    CUDA_CHECK(cudaMalloc(&d_output, output_size));

    CUDA_CHECK(cudaMemcpy(d_input, h_input, input_size, cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_weight, h_weight, weight_size, cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_bias, h_bias, bias_size, cudaMemcpyHostToDevice));

    dim3 blockDim(BLOCK_SIZE);
    dim3 gridDim(OUT_H * OUT_W, OUT_C, BATCH);

    conv2d_forward<<<gridDim, blockDim>>>(
        d_input, d_weight, d_bias, d_output,
        BATCH, IN_C, IN_H, IN_W,
        OUT_C, K_H, K_W,
        PADDING, STRIDE);

    CUDA_CHECK(cudaDeviceSynchronize());

    CUDA_CHECK(cudaMemcpy(h_output, d_output, output_size, cudaMemcpyDeviceToHost));

    printf("卷积结果样本: output[0][0][0][0] = %.3f\n", h_output[0]);

    CUDA_CHECK(cudaFree(d_input));
    CUDA_CHECK(cudaFree(d_weight));
    CUDA_CHECK(cudaFree(d_bias));
    CUDA_CHECK(cudaFree(d_output));
    free(h_input);
    free(h_weight);
    free(h_bias);
    free(h_output);

    printf("\n2D 卷积完成!\n");
    printf("TEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
