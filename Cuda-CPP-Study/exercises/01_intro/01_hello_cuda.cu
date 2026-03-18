// 练习 1: Hello CUDA
//
// 目标: 编写你的第一个 CUDA 程序，在 GPU 上打印 "Hello from GPU!"
//
// 任务:
// 1. 实现 hello_kernel 函数，在 GPU 上打印消息
// 2. 正确调用 kernel
// 3. 同步设备以确保输出被刷新
//
// 注意: 不要删除 I AM NOT DONE 注释，直到你完成了练习

#include <stdio.h>
#include <cuda_runtime.h>

// TODO: 实现这个 kernel 函数
// 提示: 使用 __global__ 关键字定义 kernel
// 提示: 在 kernel 中可以使用 printf()
__global__ void hello_kernel() {
    // 你的代码在这里
}

int main() {
    printf("从 CPU 启动 CUDA kernel...\n");

    // TODO: 调用 kernel
    // 提示: 使用 <<<blocks, threads>>> 语法
    // 提示: 从 1 个 block, 1 个 thread 开始

    // TODO: 同步设备
    // 提示: 使用 cudaDeviceSynchronize()

    printf("Kernel 执行完成!\n");

    // 测试验证
    printf("TEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
