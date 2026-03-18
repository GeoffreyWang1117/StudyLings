// 练习 5: 数据传输
//
// 目标: 掌握主机和设备之间的数据传输
//
// 任务:
// 1. 将数据从主机拷贝到设备
// 2. 在设备上修改数据
// 3. 将结果拷贝回主机

#include <stdio.h>
#include <cuda_runtime.h>

#define N 10
#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

__global__ void increment(int *data, int n) {
    int idx = threadIdx.x;
    if (idx < n) {
        data[idx] += 1;
    }
}

int main() {
    int h_data[N];
    int h_result[N];
    int *d_data;

    // 初始化主机数据
    for (int i = 0; i < N; i++) {
        h_data[i] = i;
    }

    // TODO: 分配设备内存

    // TODO: 拷贝数据到设备
    // 提示: cudaMemcpy(..., cudaMemcpyHostToDevice)

    // 调用 kernel
    increment<<<1, N>>>(d_data, N);
    CUDA_CHECK(cudaDeviceSynchronize());

    // TODO: 拷贝结果回主机
    // 提示: cudaMemcpy(..., cudaMemcpyDeviceToHost)

    // TODO: 释放设备内存

    // 验证
    bool success = true;
    for (int i = 0; i < N; i++) {
        if (h_result[i] != h_data[i] + 1) {
            printf("错误 at %d: got %d, expected %d\n", i, h_result[i], h_data[i] + 1);
            success = false;
            break;
        }
    }

    if (success) {
        printf("数据传输正确!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}

// I AM NOT DONE
