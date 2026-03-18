// 练习 112: 高斯模糊
//
// 目标: 实现可分离的高斯模糊滤波器
//
// 任务:
// 1. 实现 1D 高斯卷积
// 2. 利用可分离性优化（先行后列）
// 3. 比较性能差异

#include <stdio.h>
#include <cuda_runtime.h>
#include <math.h>

#define WIDTH 1024
#define HEIGHT 1024
#define KERNEL_SIZE 5
#define KERNEL_RADIUS (KERNEL_SIZE / 2)
#define BLOCK_SIZE 16

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

__constant__ float d_gaussian_kernel[KERNEL_SIZE];

// TODO: 实现水平方向的高斯模糊
__global__ void gaussian_blur_horizontal(float *input, float *output, int width, int height) {
    int col = blockIdx.x * blockDim.x + threadIdx.x;
    int row = blockIdx.y * blockDim.y + threadIdx.y;

    if (row < height && col < width) {
        float sum = 0.0f;

        // TODO: 应用 1D 高斯核（水平方向）
        // for (int i = -KERNEL_RADIUS; i <= KERNEL_RADIUS; i++) {
        //     int sample_col = col + i;
        //     // 边界处理：clamp
        //     sample_col = max(0, min(width - 1, sample_col));
        //     sum += input[row * width + sample_col] * d_gaussian_kernel[i + KERNEL_RADIUS];
        // }
        // output[row * width + col] = sum;
    }
}

// TODO: 实现垂直方向的高斯模糊
__global__ void gaussian_blur_vertical(float *input, float *output, int width, int height) {
    int col = blockIdx.x * blockDim.x + threadIdx.x;
    int row = blockIdx.y * blockDim.y + threadIdx.y;

    if (row < height && col < width) {
        float sum = 0.0f;

        // TODO: 应用 1D 高斯核（垂直方向）
        // for (int i = -KERNEL_RADIUS; i <= KERNEL_RADIUS; i++) {
        //     int sample_row = row + i;
        //     // 边界处理：clamp
        //     sample_row = max(0, min(height - 1, sample_row));
        //     sum += input[sample_row * width + col] * d_gaussian_kernel[i + KERNEL_RADIUS];
        // }
        // output[row * width + col] = sum;
    }
}

// 生成 1D 高斯核
void generate_gaussian_kernel(float *kernel, int size, float sigma) {
    float sum = 0.0f;
    int radius = size / 2;

    for (int i = 0; i < size; i++) {
        int x = i - radius;
        kernel[i] = expf(-(x * x) / (2.0f * sigma * sigma));
        sum += kernel[i];
    }

    // 归一化
    for (int i = 0; i < size; i++) {
        kernel[i] /= sum;
    }
}

int main() {
    float *h_input, *h_output, *h_temp;
    float *d_input, *d_output, *d_temp;
    size_t bytes = WIDTH * HEIGHT * sizeof(float);

    h_input = (float*)malloc(bytes);
    h_output = (float*)malloc(bytes);
    h_temp = (float*)malloc(bytes);

    // 初始化输入图像
    for (int i = 0; i < HEIGHT; i++) {
        for (int j = 0; j < WIDTH; j++) {
            h_input[i * WIDTH + j] = (i % 32 < 16) ? 1.0f : 0.0f;  // 条纹图案
        }
    }

    // 生成高斯核
    float h_kernel[KERNEL_SIZE];
    generate_gaussian_kernel(h_kernel, KERNEL_SIZE, 1.5f);

    printf("高斯核: ");
    for (int i = 0; i < KERNEL_SIZE; i++) {
        printf("%.4f ", h_kernel[i]);
    }
    printf("\n");

    CUDA_CHECK(cudaMemcpyToSymbol(d_gaussian_kernel, h_kernel, KERNEL_SIZE * sizeof(float)));

    CUDA_CHECK(cudaMalloc(&d_input, bytes));
    CUDA_CHECK(cudaMalloc(&d_output, bytes));
    CUDA_CHECK(cudaMalloc(&d_temp, bytes));

    CUDA_CHECK(cudaMemcpy(d_input, h_input, bytes, cudaMemcpyHostToDevice));

    dim3 blockDim(BLOCK_SIZE, BLOCK_SIZE);
    dim3 gridDim((WIDTH + BLOCK_SIZE - 1) / BLOCK_SIZE,
                 (HEIGHT + BLOCK_SIZE - 1) / BLOCK_SIZE);

    // 两趟卷积：先水平后垂直
    gaussian_blur_horizontal<<<gridDim, blockDim>>>(d_input, d_temp, WIDTH, HEIGHT);
    gaussian_blur_vertical<<<gridDim, blockDim>>>(d_temp, d_output, WIDTH, HEIGHT);
    CUDA_CHECK(cudaDeviceSynchronize());

    CUDA_CHECK(cudaMemcpy(h_output, d_output, bytes, cudaMemcpyDeviceToHost));

    // 验证：模糊后的图像应该更平滑
    float input_variance = 0.0f;
    float output_variance = 0.0f;
    for (int i = 1; i < HEIGHT - 1; i++) {
        for (int j = 1; j < WIDTH - 1; j++) {
            int idx = i * WIDTH + j;
            input_variance += fabsf(h_input[idx] - h_input[idx + 1]);
            output_variance += fabsf(h_output[idx] - h_output[idx + 1]);
        }
    }

    bool success = output_variance < input_variance;

    CUDA_CHECK(cudaFree(d_input));
    CUDA_CHECK(cudaFree(d_output));
    CUDA_CHECK(cudaFree(d_temp));
    free(h_input);
    free(h_output);
    free(h_temp);

    if (success) {
        printf("高斯模糊正确! (方差降低: %.2f -> %.2f)\n", input_variance, output_variance);
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}

// I AM NOT DONE
