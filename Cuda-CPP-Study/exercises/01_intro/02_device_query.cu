// 练习 2: 设备查询
//
// 目标: 学习如何查询 CUDA 设备的属性
//
// 任务:
// 1. 获取系统中 CUDA 设备的数量
// 2. 获取第一个设备的属性
// 3. 打印关键信息（名称、计算能力、全局内存等）

#include <stdio.h>
#include <cuda_runtime.h>

int main() {
    int deviceCount = 0;

    // TODO: 获取设备数量
    // 提示: 使用 cudaGetDeviceCount(&deviceCount)

    printf("检测到 %d 个 CUDA 设备\n", deviceCount);

    if (deviceCount == 0) {
        printf("⚠️  警告: 没有检测到 CUDA 设备\n");
        printf("TEST_PASSED\n");  // 即使没有 GPU 也算通过（用于 CI）
        return 0;
    }

    // TODO: 获取设备 0 的属性
    // 提示: 使用 cudaDeviceProp 结构体
    // 提示: 使用 cudaGetDeviceProperties()
    cudaDeviceProp prop;

    printf("\n设备 0: %s\n", prop.name);

    // TODO: 打印以下信息
    // - 计算能力 (major.minor)
    // - 全局内存大小 (GB)
    // - 每个 block 的最大线程数
    // - SM (Streaming Multiprocessor) 数量
    // - 时钟频率

    printf("  计算能力: %d.%d\n", prop.major, prop.minor);
    // 添加更多属性...

    printf("\nTEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
