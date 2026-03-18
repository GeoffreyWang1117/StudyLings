// 练习 143: GPU 间 P2P 数据传输
//
// 目标: 实现 GPU 之间的直接数据传输
//
// 任务:
// 1. 启用 P2P 访问
// 2. 在 GPU 间直接传输数据
// 3. 比较 P2P 和通过主机传输的性能

#include <stdio.h>
#include <cuda_runtime.h>
#include <time.h>

#define N 100000000  // 100M 元素
#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

double get_time() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

int main() {
    int deviceCount;
    CUDA_CHECK(cudaGetDeviceCount(&deviceCount));

    if (deviceCount < 2) {
        printf("需要至少 2 个 GPU 来测试 P2P\n");
        printf("当前系统只有 %d 个 GPU\n", deviceCount);
        printf("TEST_PASSED\n");  // 算通过，因为环境限制
        return 0;
    }

    printf("测试 GPU 0 和 GPU 1 之间的 P2P 传输\n\n");

    // TODO: 检查 P2P 访问能力
    int canAccessPeer;
    // CUDA_CHECK(cudaDeviceCanAccessPeer(&canAccessPeer, 0, 1));

    printf("GPU 0 -> GPU 1 P2P 访问: %s\n", canAccessPeer ? "支持" : "不支持");

    if (!canAccessPeer) {
        printf("该系统不支持 P2P，跳过测试\n");
        printf("TEST_PASSED\n");
        return 0;
    }

    // TODO: 启用 P2P 访问
    // CUDA_CHECK(cudaSetDevice(0));
    // CUDA_CHECK(cudaDeviceEnablePeerAccess(1, 0));

    size_t bytes = N * sizeof(float);
    float *d_data0, *d_data1, *h_temp;

    // 在两个 GPU 上分配内存
    CUDA_CHECK(cudaSetDevice(0));
    CUDA_CHECK(cudaMalloc(&d_data0, bytes));

    CUDA_CHECK(cudaSetDevice(1));
    CUDA_CHECK(cudaMalloc(&d_data1, bytes));

    h_temp = (float*)malloc(bytes);

    // 初始化 GPU 0 的数据
    CUDA_CHECK(cudaSetDevice(0));
    CUDA_CHECK(cudaMemset(d_data0, 1, bytes));

    // TODO: 测试 P2P 传输性能
    printf("\n性能测试 (传输 %.2f MB):\n", bytes / 1e6);

    // 方法 1: P2P 直接传输
    CUDA_CHECK(cudaSetDevice(0));
    double start = get_time();
    // TODO: GPU 0 -> GPU 1 直接传输
    // CUDA_CHECK(cudaMemcpyPeer(d_data1, 1, d_data0, 0, bytes));
    CUDA_CHECK(cudaDeviceSynchronize());
    double p2p_time = get_time() - start;

    // 方法 2: 通过主机传输
    CUDA_CHECK(cudaSetDevice(0));
    start = get_time();
    CUDA_CHECK(cudaMemcpy(h_temp, d_data0, bytes, cudaMemcpyDeviceToHost));
    CUDA_CHECK(cudaSetDevice(1));
    CUDA_CHECK(cudaMemcpy(d_data1, h_temp, bytes, cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaDeviceSynchronize());
    double host_time = get_time() - start;

    printf("  P2P 传输: %.3f ms (%.2f GB/s)\n",
           p2p_time * 1000, bytes / p2p_time / 1e9);
    printf("  主机传输: %.3f ms (%.2f GB/s)\n",
           host_time * 1000, bytes / host_time / 1e9);
    printf("  加速比: %.2fx\n", host_time / p2p_time);

    // 清理
    CUDA_CHECK(cudaSetDevice(0));
    // CUDA_CHECK(cudaDeviceDisablePeerAccess(1));
    CUDA_CHECK(cudaFree(d_data0));

    CUDA_CHECK(cudaSetDevice(1));
    CUDA_CHECK(cudaFree(d_data1));

    free(h_temp);

    printf("\nTEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
