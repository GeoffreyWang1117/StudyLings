// 练习 141: Multi-GPU 设备查询
//
// 目标: 检测和查询多个 GPU
//
// 任务:
// 1. 枚举所有可用的 GPU
// 2. 获取每个 GPU 的属性
// 3. 检查 P2P 能力

#include <stdio.h>
#include <cuda_runtime.h>

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

int main() {
    int deviceCount = 0;

    // TODO: 获取 GPU 数量
    // CUDA_CHECK(cudaGetDeviceCount(&deviceCount));

    printf("检测到 %d 个 CUDA 设备\n\n", deviceCount);

    if (deviceCount == 0) {
        printf("没有检测到 CUDA 设备\n");
        printf("TEST_PASSED\n");  // 即使没有GPU也算通过
        return 0;
    }

    // TODO: 遍历所有设备
    for (int dev = 0; dev < deviceCount; dev++) {
        cudaDeviceProp prop;
        // CUDA_CHECK(cudaGetDeviceProperties(&prop, dev));

        printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
        printf("设备 %d: %s\n", dev, prop.name);
        printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");
        printf("  计算能力: %d.%d\n", prop.major, prop.minor);
        printf("  全局内存: %.2f GB\n", prop.totalGlobalMem / 1e9);
        printf("  SM 数量: %d\n", prop.multiProcessorCount);
        printf("  每个SM最大线程数: %d\n", prop.maxThreadsPerMultiProcessor);
        printf("  Warp 大小: %d\n", prop.warpSize);
        printf("  支持并发 kernels: %s\n", prop.concurrentKernels ? "是" : "否");
        printf("  支持统一寻址: %s\n", prop.unifiedAddressing ? "是" : "否");
        printf("\n");
    }

    // TODO: 检查 P2P (Peer-to-Peer) 访问能力
    if (deviceCount > 1) {
        printf("P2P 访问矩阵:\n");
        printf("     ");
        for (int i = 0; i < deviceCount; i++) {
            printf("GPU%d ", i);
        }
        printf("\n");

        for (int i = 0; i < deviceCount; i++) {
            printf("GPU%d ", i);
            for (int j = 0; j < deviceCount; j++) {
                if (i == j) {
                    printf("  -  ");
                } else {
                    int canAccess;
                    // TODO: 检查 GPU i 能否访问 GPU j
                    // CUDA_CHECK(cudaDeviceCanAccessPeer(&canAccess, i, j));
                    canAccess = 0;  // 临时值
                    printf(" %s ", canAccess ? "√" : "×");
                }
            }
            printf("\n");
        }
    }

    printf("\nTEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
