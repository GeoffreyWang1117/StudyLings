/**
 * 练习 132: 蒙特卡洛模拟
 * 学习目标: 使用 cuRAND 实现蒙特卡洛方法
 */

#include <cuda_runtime.h>
#include <curand_kernel.h>
#include <stdio.h>

__global__ void monte_carlo_pi(float *results, int samples_per_thread) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;

    curandState state;
    curand_init(1234, tid, 0, &state);

    int inside = 0;
    for (int i = 0; i < samples_per_thread; i++) {
        float x = curand_uniform(&state);
        float y = curand_uniform(&state);

        if (x * x + y * y <= 1.0f) {
            inside++;
        }
    }

    results[tid] = (float)inside / samples_per_thread;
}

int main() {
    printf("=== 蒙特卡洛模拟 ===\n");
    printf("任务: 使用蒙特卡洛方法估算 π\n");
    printf("编译: nvcc -o monte_carlo 02_monte_carlo.cu -lcurand\n");
    return 0;
}
