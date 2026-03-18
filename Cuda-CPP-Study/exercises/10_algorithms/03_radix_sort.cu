// 练习 103: 基数排序 (Radix Sort)
//
// 目标: 实现并行基数排序
//
// 任务:
// 1. 实现按位排序
// 2. 使用 scan 进行位置计算
// 3. 实现稳定排序

#include <stdio.h>
#include <cuda_runtime.h>

#define N 1024
#define BLOCK_SIZE 256
#define BITS 4  // 每次处理4位

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// TODO: 实现提取指定位的值
__device__ int get_digit(int value, int bit_pos) {
    // return (value >> bit_pos) & ((1 << BITS) - 1);
    return 0;  // 修改这里
}

// TODO: 实现一趟基数排序
__global__ void radix_sort_pass(int *input, int *output, int *histogram, int bit_pos, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    if (idx < n) {
        // TODO: 获取当前元素的数字
        // int digit = get_digit(input[idx], bit_pos);

        // TODO: 计算在输出数组中的位置
        // （需要先计算 histogram 和 prefix sum）
    }
}

int main() {
    int *h_input, *h_output;
    int *d_input, *d_output, *d_histogram;

    h_input = (int*)malloc(N * sizeof(int));
    h_output = (int*)malloc(N * sizeof(int));

    // 初始化随机数据
    for (int i = 0; i < N; i++) {
        h_input[i] = rand() % 10000;
    }

    CUDA_CHECK(cudaMalloc(&d_input, N * sizeof(int)));
    CUDA_CHECK(cudaMalloc(&d_output, N * sizeof(int)));
    CUDA_CHECK(cudaMalloc(&d_histogram, (1 << BITS) * sizeof(int)));

    CUDA_CHECK(cudaMemcpy(d_input, h_input, N * sizeof(int), cudaMemcpyHostToDevice));

    // TODO: 实现多趟基数排序
    // int num_bits = 32;  // int 的位数
    // for (int bit = 0; bit < num_bits; bit += BITS) {
    //     radix_sort_pass<<<...>>>(d_input, d_output, d_histogram, bit, N);
    //     // 交换输入输出
    //     int *temp = d_input;
    //     d_input = d_output;
    //     d_output = temp;
    // }

    CUDA_CHECK(cudaMemcpy(h_output, d_input, N * sizeof(int), cudaMemcpyDeviceToHost));

    // 验证
    bool success = true;
    for (int i = 0; i < N - 1; i++) {
        if (h_output[i] > h_output[i + 1]) {
            success = false;
            break;
        }
    }

    CUDA_CHECK(cudaFree(d_input));
    CUDA_CHECK(cudaFree(d_output));
    CUDA_CHECK(cudaFree(d_histogram));
    free(h_input);
    free(h_output);

    if (success) {
        printf("基数排序正确!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}

// I AM NOT DONE
