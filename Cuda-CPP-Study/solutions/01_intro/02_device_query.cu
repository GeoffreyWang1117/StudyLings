// 参考答案 2: 设备查询

#include <stdio.h>
#include <cuda_runtime.h>

int main() {
    int deviceCount = 0;

    // 获取设备数量
    cudaGetDeviceCount(&deviceCount);

    printf("检测到 %d 个 CUDA 设备\n", deviceCount);

    if (deviceCount == 0) {
        printf("⚠️  警告: 没有检测到 CUDA 设备\n");
        printf("TEST_PASSED\n");
        return 0;
    }

    // 获取设备属性
    cudaDeviceProp prop;
    cudaGetDeviceProperties(&prop, 0);

    printf("\n设备 0: %s\n", prop.name);
    printf("  计算能力: %d.%d\n", prop.major, prop.minor);
    printf("  全局内存: %.2f GB\n", prop.totalGlobalMem / 1024.0 / 1024.0 / 1024.0);
    printf("  每个 block 最大线程数: %d\n", prop.maxThreadsPerBlock);
    printf("  SM 数量: %d\n", prop.multiProcessorCount);
    printf("  时钟频率: %.2f GHz\n", prop.clockRate / 1e6);
    printf("  内存时钟频率: %.2f GHz\n", prop.memoryClockRate / 1e6);
    printf("  内存总线宽度: %d-bit\n", prop.memoryBusWidth);
    printf("  L2 缓存大小: %d KB\n", prop.l2CacheSize / 1024);
    printf("  共享内存/block: %zu KB\n", prop.sharedMemPerBlock / 1024);
    printf("  Warp 大小: %d\n", prop.warpSize);

    printf("\nTEST_PASSED\n");
    return 0;
}
