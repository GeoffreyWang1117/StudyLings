// 练习 27: 内存拷贝
//
// 目标: 掌握不同类型的内存拷贝
//
// 任务:
// 1. Host to Device 拷贝
// 2. Device to Host 拷贝
// 3. Device to Device 拷贝

#include <stdio.h>
#include <cuda_runtime.h>

#define N 100
#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

int main() {
    float *h_src, *h_dst;
    float *d_src, *d_dst;
    size_t bytes = N * sizeof(float);

    // 分配内存
    h_src = (float*)malloc(bytes);
    h_dst = (float*)malloc(bytes);
    CUDA_CHECK(cudaMalloc(&d_src, bytes));
    CUDA_CHECK(cudaMalloc(&d_dst, bytes));

    // 初始化主机数据
    for (int i = 0; i < N; i++) {
        h_src[i] = i * 3.14f;
    }

    // TODO: 1. Host to Device 拷贝
    // CUDA_CHECK(cudaMemcpy(...));

    // TODO: 2. Device to Device 拷贝
    // CUDA_CHECK(cudaMemcpy(..., cudaMemcpyDeviceToDevice));

    // TODO: 3. Device to Host 拷贝
    // CUDA_CHECK(cudaMemcpy(..., cudaMemcpyDeviceToHost));

    // 验证
    bool success = true;
    for (int i = 0; i < N; i++) {
        if (h_dst[i] != h_src[i]) {
            printf("错误 at %d\n", i);
            success = false;
            break;
        }
    }

    // 清理
    CUDA_CHECK(cudaFree(d_src));
    CUDA_CHECK(cudaFree(d_dst));
    free(h_src);
    free(h_dst);

    if (success) {
        printf("内存拷贝正确!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}

// I AM NOT DONE
