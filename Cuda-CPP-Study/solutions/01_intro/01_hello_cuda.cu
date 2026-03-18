// 参考答案 1: Hello CUDA

#include <stdio.h>
#include <cuda_runtime.h>

__global__ void hello_kernel() {
    printf("Hello from GPU! Thread %d in block %d\n", threadIdx.x, blockIdx.x);
}

int main() {
    printf("从 CPU 启动 CUDA kernel...\n");

    // 调用 kernel：1 个 block，1 个 thread
    hello_kernel<<<1, 1>>>();

    // 同步设备以确保 printf 输出被刷新
    cudaDeviceSynchronize();

    printf("Kernel 执行完成!\n");
    printf("TEST_PASSED\n");
    return 0;
}
