/**
 * 练习 291: Attention 机制实现
 * 学习目标: 实现 Transformer 的核心 Attention 算子
 */

#include <cuda_runtime.h>
#include <stdio.h>

__global__ void scaled_dot_product_attention(float *Q, float *K, float *V,
                                               float *output, int seq_len, int d_k) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= seq_len) return;

    // TODO: 实现 Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) V
}

int main() {
    printf("=== Scaled Dot-Product Attention ===\n");
    printf("任务: 实现 Transformer Attention 算子\n");
    return 0;
}
