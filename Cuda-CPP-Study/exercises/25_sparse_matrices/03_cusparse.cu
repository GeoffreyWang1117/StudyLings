/**
 * 练习 253: cuSPARSE 库使用
 * 学习目标: 使用 cuSPARSE 库加速稀疏矩阵运算
 */

#include <cuda_runtime.h>
#include <cusparse.h>
#include <stdio.h>

int main() {
    printf("=== cuSPARSE 库使用 ===\n");
    printf("任务: 使用 cuSPARSE 执行稀疏矩阵运算\n");
    printf("编译: nvcc -o cusparse 03_cusparse.cu -lcusparse\n");
    return 0;
}
