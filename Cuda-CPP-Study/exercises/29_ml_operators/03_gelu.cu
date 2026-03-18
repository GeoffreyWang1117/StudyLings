/**
 * 练习 293: GELU 激活函数
 * 学习目标: 实现 GELU 激活函数
 */

#include <cuda_runtime.h>
#include <stdio.h>

__global__ void gelu(float *input, float *output, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= n) return;

    float x = input[idx];
    // GELU(x) = x * Φ(x) ≈ 0.5 * x * (1 + tanh(√(2/π) * (x + 0.044715 * x^3)))
    float tanh_input = 0.7978845608f * (x + 0.044715f * x * x * x);
    output[idx] = 0.5f * x * (1.0f + tanhf(tanh_input));
}

int main() {
    printf("=== GELU 激活函数 ===\n");
    printf("任务: 实现 GELU(x) = x * Φ(x)\n");
    return 0;
}
