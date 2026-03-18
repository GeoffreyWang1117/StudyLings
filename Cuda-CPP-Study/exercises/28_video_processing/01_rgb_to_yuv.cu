/**
 * 练习 281: RGB 到 YUV 颜色空间转换
 * 学习目标: 实现视频编码常用的颜色空间转换
 */

#include <cuda_runtime.h>
#include <stdio.h>

__global__ void rgb_to_yuv(unsigned char *rgb, unsigned char *y, unsigned char *u, unsigned char *v,
                            int width, int height) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y_coord = blockIdx.y * blockDim.y + threadIdx.y;

    if (x >= width || y_coord >= height) return;

    int idx = y_coord * width + x;
    int rgb_idx = idx * 3;

    unsigned char r = rgb[rgb_idx];
    unsigned char g = rgb[rgb_idx + 1];
    unsigned char b = rgb[rgb_idx + 2];

    y[idx] = (unsigned char)(0.299f * r + 0.587f * g + 0.114f * b);
    u[idx] = (unsigned char)(128 + (-0.169f * r - 0.331f * g + 0.5f * b));
    v[idx] = (unsigned char)(128 + (0.5f * r - 0.419f * g - 0.081f * b));
}

int main() {
    printf("=== RGB 到 YUV 转换 ===\n");
    printf("任务: 实现颜色空间转换\n");
    return 0;
}
