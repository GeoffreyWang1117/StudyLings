// 综合项目 1: MNIST 手写数字识别推理引擎
//
// 目标: 实现一个完整的深度学习推理引擎
//
// 任务:
// 1. 实现全连接层、ReLU、Softmax
// 2. 加载预训练权重
// 3. 批量推理优化
// 4. 性能分析与优化
//
// 网络结构: 784 -> 128 -> 64 -> 10
// 输入: 28x28 灰度图像
// 输出: 10个类别的概率
//
// 这个项目整合了你学到的所有知识:
// - Kernel 编程
// - 内存管理
// - Shared memory 优化
// - cuBLAS 加速
// - 性能分析

#include <stdio.h>
#include <cuda_runtime.h>
#include <cublas_v2.h>
#include <math.h>
#include <stdlib.h>

#define INPUT_SIZE 784   // 28x28
#define HIDDEN1_SIZE 128
#define HIDDEN2_SIZE 64
#define OUTPUT_SIZE 10
#define BATCH_SIZE 32

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

#define CUBLAS_CHECK(call) \
    do { \
        cublasStatus_t status = call; \
        if (status != CUBLAS_STATUS_SUCCESS) { \
            fprintf(stderr, "cuBLAS Error\n"); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// TODO: ReLU 激活函数
__global__ void relu_kernel(float *data, int size) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    // if (idx < size) {
    //     data[idx] = fmaxf(0.0f, data[idx]);
    // }
}

// TODO: Softmax (数值稳定版本)
__global__ void softmax_kernel(float *data, int batch_size, int num_classes) {
    int batch_idx = blockIdx.x;

    if (batch_idx < batch_size) {
        float *batch_data = data + batch_idx * num_classes;

        // 找最大值
        float max_val = batch_data[0];
        for (int i = 1; i < num_classes; i++) {
            max_val = fmaxf(max_val, batch_data[i]);
        }

        // 计算 exp 和 sum
        float sum = 0.0f;
        for (int i = 0; i < num_classes; i++) {
            batch_data[i] = expf(batch_data[i] - max_val);
            sum += batch_data[i];
        }

        // 归一化
        for (int i = 0; i < num_classes; i++) {
            batch_data[i] /= sum;
        }
    }
}

// 神经网络结构
struct NeuralNetwork {
    // 权重
    float *d_W1, *d_W2, *d_W3;  // 权重矩阵
    float *d_b1, *d_b2, *d_b3;  // 偏置

    // 中间层输出
    float *d_hidden1, *d_hidden2, *d_output;

    cublasHandle_t cublas_handle;
};

// TODO: 初始化网络
void init_network(NeuralNetwork *net) {
    // 分配权重内存
    CUDA_CHECK(cudaMalloc(&net->d_W1, INPUT_SIZE * HIDDEN1_SIZE * sizeof(float)));
    CUDA_CHECK(cudaMalloc(&net->d_W2, HIDDEN1_SIZE * HIDDEN2_SIZE * sizeof(float)));
    CUDA_CHECK(cudaMalloc(&net->d_W3, HIDDEN2_SIZE * OUTPUT_SIZE * sizeof(float)));

    CUDA_CHECK(cudaMalloc(&net->d_b1, HIDDEN1_SIZE * sizeof(float)));
    CUDA_CHECK(cudaMalloc(&net->d_b2, HIDDEN2_SIZE * sizeof(float)));
    CUDA_CHECK(cudaMalloc(&net->d_b3, OUTPUT_SIZE * sizeof(float)));

    // 分配中间层内存
    CUDA_CHECK(cudaMalloc(&net->d_hidden1, BATCH_SIZE * HIDDEN1_SIZE * sizeof(float)));
    CUDA_CHECK(cudaMalloc(&net->d_hidden2, BATCH_SIZE * HIDDEN2_SIZE * sizeof(float)));
    CUDA_CHECK(cudaMalloc(&net->d_output, BATCH_SIZE * OUTPUT_SIZE * sizeof(float)));

    // TODO: 初始化权重（随机或加载预训练权重）
    // 这里用随机初始化演示

    CUBLAS_CHECK(cublasCreate(&net->cublas_handle));
}

// TODO: 前向传播
void forward(NeuralNetwork *net, float *d_input, float *d_output, int batch_size) {
    float alpha = 1.0f, beta = 0.0f;

    // TODO: 第一层: input -> hidden1
    // hidden1 = W1^T * input + b1
    // CUBLAS_CHECK(cublasSgemm(net->cublas_handle,
    //     CUBLAS_OP_T, CUBLAS_OP_N,
    //     HIDDEN1_SIZE, batch_size, INPUT_SIZE,
    //     &alpha,
    //     net->d_W1, INPUT_SIZE,
    //     d_input, INPUT_SIZE,
    //     &beta,
    //     net->d_hidden1, HIDDEN1_SIZE));

    // 加偏置和 ReLU
    // add_bias_kernel<<<...>>>(net->d_hidden1, net->d_b1, ...);
    // relu_kernel<<<...>>>(net->d_hidden1, batch_size * HIDDEN1_SIZE);

    // TODO: 第二层: hidden1 -> hidden2
    // 类似实现...

    // TODO: 第三层: hidden2 -> output
    // 类似实现...

    // TODO: Softmax
    // softmax_kernel<<<batch_size, 1>>>(net->d_output, batch_size, OUTPUT_SIZE);
}

// TODO: 推理
void inference(NeuralNetwork *net, float *images, int *predictions, int num_images) {
    float *d_input;
    CUDA_CHECK(cudaMalloc(&d_input, BATCH_SIZE * INPUT_SIZE * sizeof(float)));

    for (int i = 0; i < num_images; i += BATCH_SIZE) {
        int batch = (i + BATCH_SIZE <= num_images) ? BATCH_SIZE : (num_images - i);

        // 复制输入
        CUDA_CHECK(cudaMemcpy(d_input, images + i * INPUT_SIZE,
                              batch * INPUT_SIZE * sizeof(float),
                              cudaMemcpyHostToDevice));

        // 前向传播
        forward(net, d_input, net->d_output, batch);

        // 复制输出并找最大值
        float *h_output = (float*)malloc(batch * OUTPUT_SIZE * sizeof(float));
        CUDA_CHECK(cudaMemcpy(h_output, net->d_output,
                              batch * OUTPUT_SIZE * sizeof(float),
                              cudaMemcpyDeviceToHost));

        for (int j = 0; j < batch; j++) {
            int max_idx = 0;
            float max_prob = h_output[j * OUTPUT_SIZE];
            for (int k = 1; k < OUTPUT_SIZE; k++) {
                if (h_output[j * OUTPUT_SIZE + k] > max_prob) {
                    max_prob = h_output[j * OUTPUT_SIZE + k];
                    max_idx = k;
                }
            }
            predictions[i + j] = max_idx;
        }

        free(h_output);
    }

    CUDA_CHECK(cudaFree(d_input));
}

int main() {
    printf("=== MNIST 推理引擎 ===\n\n");

    NeuralNetwork net;
    init_network(&net);

    // TODO: 生成测试数据
    int num_test_images = 100;
    float *test_images = (float*)malloc(num_test_images * INPUT_SIZE * sizeof(float));
    int *predictions = (int*)malloc(num_test_images * sizeof(int));

    // 随机生成测试图像
    for (int i = 0; i < num_test_images * INPUT_SIZE; i++) {
        test_images[i] = (float)rand() / RAND_MAX;
    }

    printf("开始推理 %d 张图像...\n", num_test_images);
    inference(&net, test_images, predictions, num_test_images);

    printf("推理完成!\n\n");

    printf("预测结果 (前10个):\n");
    for (int i = 0; i < 10; i++) {
        printf("图像 %d: 类别 %d\n", i, predictions[i]);
    }

    printf("\n项目要点:\n");
    printf("1. 使用 cuBLAS 加速矩阵乘法\n");
    printf("2. Kernel fusion 减少内存访问\n");
    printf("3. 批量处理提高吞吐量\n");
    printf("4. 使用 Nsight 分析性能瓶颈\n");

    printf("\n扩展任务:\n");
    printf("- 支持 CNN (卷积神经网络)\n");
    printf("- 使用 cuDNN 加速\n");
    printf("- INT8 量化推理\n");
    printf("- TensorRT 集成\n");

    // 清理
    free(test_images);
    free(predictions);

    printf("\nTEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
