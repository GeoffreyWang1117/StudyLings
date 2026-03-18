// 练习 19: Grid-Stride 循环
//
// 目标: 实现 grid-stride 循环处理大数组
//
// 任务:
// 1. 理解 grid-stride 模式
// 2. 处理比线程数更多的元素
// 3. 实现可扩展的 kernel

#include <stdio.h>
#include <cuda_runtime.h>

#define N 10000
#define BLOCK_SIZE 256

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// TODO: 实现 grid-stride 循环
// 即使数组很大，也能用较少的线程处理
__global__ void square_array(float *data, int n) {
    // TODO: 计算起始索引和步长
    // int idx = blockIdx.x * blockDim.x + threadIdx.x;
    // int stride = blockDim.x * gridDim.x;

    // TODO: 使用 grid-stride 循环
    // for (int i = idx; i < n; i += stride) {
    //     data[i] = data[i] * data[i];
    // }
}

int main() {
    float *h_data, *d_data;
    size_t bytes = N * sizeof(float);

    h_data = (float*)malloc(bytes);

    // 初始化
    for (int i = 0; i < N; i++) {
        h_data[i] = i;
    }

    CUDA_CHECK(cudaMalloc(&d_data, bytes));
    CUDA_CHECK(cudaMemcpy(d_data, h_data, bytes, cudaMemcpyHostToDevice));

    // 使用少量的 blocks（远少于需要的数量）
    int num_blocks = 32;  // 远小于 (N + BLOCK_SIZE - 1) / BLOCK_SIZE
    square_array<<<num_blocks, BLOCK_SIZE>>>(d_data, N);
    CUDA_CHECK(cudaDeviceSynchronize());

    CUDA_CHECK(cudaMemcpy(h_data, d_data, bytes, cudaMemcpyDeviceToHost));

    // 验证
    bool success = true;
    for (int i = 0; i < N; i++) {
        float expected = i * i;
        if (fabsf(h_data[i] - expected) > 1e-3) {
            printf("错误 at %d: got %f, expected %f\n", i, h_data[i], expected);
            success = false;
            break;
        }
    }

    CUDA_CHECK(cudaFree(d_data));
    free(h_data);

    if (success) {
        printf("Grid-stride 循环正确!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}

// I AM NOT DONE
