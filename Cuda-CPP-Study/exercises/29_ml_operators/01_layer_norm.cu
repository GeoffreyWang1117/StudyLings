/**
 * 练习 292: Layer Normalization
 * 学习目标: 实现 Layer Norm 算子
 */

#include <cuda_runtime.h>
#include <stdio.h>

__global__ void layer_norm(float *input, float *output, float *gamma, float *beta,
                            int batch_size, int features, float epsilon) {
    int batch_idx = blockIdx.x;
    if (batch_idx >= batch_size) return;

    // TODO: 计算均值和方差
    // TODO: 归一化
    // TODO: 应用 gamma 和 beta
}

int main() {
    printf("=== Layer Normalization ===\n");
    printf("任务: 实现 LayerNorm 算子\n");
    return 0;
}
