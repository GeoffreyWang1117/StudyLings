// 练习 123: Softmax 层
//
// 目标: 实现数值稳定的 Softmax
//
// 任务:
// 1. 实现 Softmax: p_i = exp(x_i) / sum(exp(x_j))
// 2. 使用 max trick 避免溢出
// 3. 实现反向传播

#include <stdio.h>
#include <cuda_runtime.h>

#define BATCH_SIZE 128
#define NUM_CLASSES 10
#define BLOCK_SIZE 256

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// TODO: 实现数值稳定的 Softmax
// 使用 max trick: softmax(x) = softmax(x - max(x))
__global__ void softmax_forward(float *input, float *output, int batch_size, int num_classes) {
    int batch_idx = blockIdx.x;

    if (batch_idx < batch_size) {
        // TODO: 1. 找到该样本的最大值
        float max_val = -INFINITY;
        // for (int i = 0; i < num_classes; i++) {
        //     max_val = fmaxf(max_val, input[batch_idx * num_classes + i]);
        // }

        // TODO: 2. 计算 exp(x - max) 和 sum
        float sum = 0.0f;
        // for (int i = 0; i < num_classes; i++) {
        //     int idx = batch_idx * num_classes + i;
        //     float exp_val = expf(input[idx] - max_val);
        //     output[idx] = exp_val;
        //     sum += exp_val;
        // }

        // TODO: 3. 归一化
        // for (int i = 0; i < num_classes; i++) {
        //     output[batch_idx * num_classes + i] /= sum;
        // }
    }
}

// TODO: Softmax backward
// grad_input[i] = output[i] * (grad_output[i] - sum(output * grad_output))
__global__ void softmax_backward(float *output, float *grad_output, float *grad_input,
                                 int batch_size, int num_classes) {
    int batch_idx = blockIdx.x;

    if (batch_idx < batch_size) {
        // TODO: 计算 sum(output * grad_output)
        float sum = 0.0f;
        // for (int i = 0; i < num_classes; i++) {
        //     int idx = batch_idx * num_classes + i;
        //     sum += output[idx] * grad_output[idx];
        // }

        // TODO: 计算梯度
        // for (int i = 0; i < num_classes; i++) {
        //     int idx = batch_idx * num_classes + i;
        //     grad_input[idx] = output[idx] * (grad_output[idx] - sum);
        // }
    }
}

int main() {
    float *h_input, *h_output;
    float *d_input, *d_output;
    size_t bytes = BATCH_SIZE * NUM_CLASSES * sizeof(float);

    h_input = (float*)malloc(bytes);
    h_output = (float*)malloc(bytes);

    // 初始化（模拟 logits）
    for (int i = 0; i < BATCH_SIZE; i++) {
        for (int j = 0; j < NUM_CLASSES; j++) {
            h_input[i * NUM_CLASSES + j] = (float)rand() / RAND_MAX * 10.0f - 5.0f;
        }
    }

    CUDA_CHECK(cudaMalloc(&d_input, bytes));
    CUDA_CHECK(cudaMalloc(&d_output, bytes));

    CUDA_CHECK(cudaMemcpy(d_input, h_input, bytes, cudaMemcpyHostToDevice));

    softmax_forward<<<BATCH_SIZE, 1>>>(d_input, d_output, BATCH_SIZE, NUM_CLASSES);
    CUDA_CHECK(cudaDeviceSynchronize());

    CUDA_CHECK(cudaMemcpy(h_output, d_output, bytes, cudaMemcpyDeviceToHost));

    // 验证：每行的和应该接近1
    bool success = true;
    for (int i = 0; i < BATCH_SIZE; i++) {
        float sum = 0.0f;
        for (int j = 0; j < NUM_CLASSES; j++) {
            sum += h_output[i * NUM_CLASSES + j];

            // 每个概率应该在 [0, 1]
            if (h_output[i * NUM_CLASSES + j] < 0.0f ||
                h_output[i * NUM_CLASSES + j] > 1.0f) {
                printf("错误: 概率超出范围\n");
                success = false;
                break;
            }
        }

        if (fabsf(sum - 1.0f) > 1e-4) {
            printf("错误: 第 %d 行的和 = %f (应为 1.0)\n", i, sum);
            success = false;
            break;
        }
    }

    if (success) {
        printf("第一个样本的 Softmax 输出: ");
        for (int i = 0; i < NUM_CLASSES; i++) {
            printf("%.4f ", h_output[i]);
        }
        printf("\n");
    }

    CUDA_CHECK(cudaFree(d_input));
    CUDA_CHECK(cudaFree(d_output));
    free(h_input);
    free(h_output);

    if (success) {
        printf("Softmax 计算正确!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}

// I AM NOT DONE
