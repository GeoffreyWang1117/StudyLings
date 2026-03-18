// 练习 18: 三维线程网格
//
// 目标: 使用三维线程网格处理 3D 数据
//
// 任务:
// 1. 理解 3D 线程组织
// 2. 计算 x, y, z 索引
// 3. 实现 3D 数据初始化

#include <stdio.h>
#include <cuda_runtime.h>

#define SIZE_X 32
#define SIZE_Y 32
#define SIZE_Z 16
#define BLOCK_SIZE 8

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// TODO: 实现 3D 数据初始化 kernel
// 每个元素设置为 x + y*SIZE_X + z*SIZE_X*SIZE_Y
__global__ void init_3d(float *data, int size_x, int size_y, int size_z) {
    // TODO: 计算 3D 索引
    // int x = blockIdx.x * blockDim.x + threadIdx.x;
    // int y = blockIdx.y * blockDim.y + threadIdx.y;
    // int z = blockIdx.z * blockDim.z + threadIdx.z;

    // TODO: 边界检查并计算线性索引
    // if (x < size_x && y < size_y && z < size_z) {
    //     int idx = x + y * size_x + z * size_x * size_y;
    //     data[idx] = idx;
    // }
}

int main() {
    float *h_data, *d_data;
    size_t total_elements = SIZE_X * SIZE_Y * SIZE_Z;
    size_t bytes = total_elements * sizeof(float);

    h_data = (float*)malloc(bytes);
    CUDA_CHECK(cudaMalloc(&d_data, bytes));

    // TODO: 设置 3D 网格和块
    dim3 blockDim(BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
    dim3 gridDim(1, 1, 1);  // 修改这里

    init_3d<<<gridDim, blockDim>>>(d_data, SIZE_X, SIZE_Y, SIZE_Z);
    CUDA_CHECK(cudaDeviceSynchronize());

    CUDA_CHECK(cudaMemcpy(h_data, d_data, bytes, cudaMemcpyDeviceToHost));

    // 验证
    bool success = true;
    for (int i = 0; i < total_elements; i++) {
        if (h_data[i] != i) {
            printf("错误 at %d: got %f, expected %d\n", i, h_data[i], i);
            success = false;
            break;
        }
    }

    CUDA_CHECK(cudaFree(d_data));
    free(h_data);

    if (success) {
        printf("3D 线程网格正确!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}

// I AM NOT DONE
