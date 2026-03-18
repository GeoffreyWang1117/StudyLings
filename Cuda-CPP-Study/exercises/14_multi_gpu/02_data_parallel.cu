// 练习 142: Multi-GPU 数据并行
//
// 目标: 在多个 GPU 上并行处理数据
//
// 任务:
// 1. 将数据分配到多个 GPU
// 2. 在每个 GPU 上执行计算
// 3. 收集结果

#include <stdio.h>
#include <cuda_runtime.h>

#define N 10000000  // 总数据量
#define BLOCK_SIZE 256

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

__global__ void vector_square(float *input, float *output, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        output[idx] = input[idx] * input[idx];
    }
}

int main() {
    int deviceCount;
    CUDA_CHECK(cudaGetDeviceCount(&deviceCount));

    if (deviceCount == 0) {
        printf("没有可用的 GPU\n");
        printf("TEST_PASSED\n");
        return 0;
    }

    printf("使用 %d 个 GPU 进行数据并行计算\n\n", deviceCount);

    // 为每个 GPU 分配数据
    int data_per_gpu = N / deviceCount;
    float *h_input, *h_output;

    h_input = (float*)malloc(N * sizeof(float));
    h_output = (float*)malloc(N * sizeof(float));

    // 初始化输入数据
    for (int i = 0; i < N; i++) {
        h_input[i] = i * 0.001f;
    }

    // TODO: 为每个 GPU 分配内存和数据
    float **d_input = (float**)malloc(deviceCount * sizeof(float*));
    float **d_output = (float**)malloc(deviceCount * sizeof(float*));

    for (int dev = 0; dev < deviceCount; dev++) {
        // TODO: 切换到设备 dev
        // CUDA_CHECK(cudaSetDevice(dev));

        // TODO: 在设备上分配内存
        // CUDA_CHECK(cudaMalloc(&d_input[dev], data_per_gpu * sizeof(float)));
        // CUDA_CHECK(cudaMalloc(&d_output[dev], data_per_gpu * sizeof(float)));

        // TODO: 拷贝数据到设备
        // CUDA_CHECK(cudaMemcpy(d_input[dev],
        //                       h_input + dev * data_per_gpu,
        //                       data_per_gpu * sizeof(float),
        //                       cudaMemcpyHostToDevice));

        // TODO: 启动 kernel
        // int grid_size = (data_per_gpu + BLOCK_SIZE - 1) / BLOCK_SIZE;
        // vector_square<<<grid_size, BLOCK_SIZE>>>(d_input[dev], d_output[dev], data_per_gpu);
    }

    // TODO: 同步所有设备
    for (int dev = 0; dev < deviceCount; dev++) {
        // CUDA_CHECK(cudaSetDevice(dev));
        // CUDA_CHECK(cudaDeviceSynchronize());
    }

    // TODO: 收集结果
    for (int dev = 0; dev < deviceCount; dev++) {
        // CUDA_CHECK(cudaSetDevice(dev));
        // CUDA_CHECK(cudaMemcpy(h_output + dev * data_per_gpu,
        //                       d_output[dev],
        //                       data_per_gpu * sizeof(float),
        //                       cudaMemcpyDeviceToHost));
    }

    // 验证结果
    bool success = true;
    for (int i = 0; i < N; i++) {
        float expected = h_input[i] * h_input[i];
        if (fabsf(h_output[i] - expected) > 1e-5) {
            printf("错误 at %d\n", i);
            success = false;
            break;
        }
    }

    // 清理
    for (int dev = 0; dev < deviceCount; dev++) {
        // CUDA_CHECK(cudaSetDevice(dev));
        // CUDA_CHECK(cudaFree(d_input[dev]));
        // CUDA_CHECK(cudaFree(d_output[dev]));
    }

    free(d_input);
    free(d_output);
    free(h_input);
    free(h_output);

    if (success) {
        printf("Multi-GPU 数据并行计算正确!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}

// I AM NOT DONE
