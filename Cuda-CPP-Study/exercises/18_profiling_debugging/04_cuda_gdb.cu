// 练习 184: cuda-gdb 调试工具
//
// 目标: 学习使用 cuda-gdb 调试 CUDA 程序
//
// 任务:
// 1. 设置断点
// 2. 检查线程状态
// 3. 查看变量值
//
// 使用方法:
// 1. 编译: nvcc -g -G -o gdb_demo 04_cuda_gdb.cu
// 2. 启动: cuda-gdb ./gdb_demo
// 3. 常用命令:
//    - break kernel_name : 在 kernel 设置断点
//    - run                : 运行程序
//    - cuda thread        : 查看当前 CUDA 线程
//    - cuda block         : 查看当前 block
//    - cuda kernel        : 列出所有 kernel
//    - print variable     : 打印变量
//    - continue           : 继续执行
//
// 高级命令:
//    - cuda thread (0,0,5) : 切换到特定线程
//    - info cuda threads   : 显示所有线程
//    - set cuda memcheck on: 启用内存检查

#include <stdio.h>
#include <cuda_runtime.h>

#define N 1024
#define BLOCK_SIZE 256

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// 一个包含 bug 的 kernel，用于调试演示
__global__ void buggy_kernel(int *data, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    // Bug: 忘记检查边界
    // TODO: 在 cuda-gdb 中设置断点，检查这里的 idx 值
    data[idx] = idx * 2;

    // Bug: 条件错误
    if (idx < n / 2) {  // 应该是 idx < n
        data[idx] = data[idx] + 1;
    }
}

// 演示 shared memory 调试
__global__ void shared_memory_debug(int *input, int *output, int n) {
    __shared__ int shared_data[BLOCK_SIZE];

    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    int tid = threadIdx.x;

    // TODO: 在 cuda-gdb 中检查 shared_data 的值
    if (idx < n) {
        shared_data[tid] = input[idx];
    }
    __syncthreads();

    // 反向写入
    if (idx < n) {
        output[idx] = shared_data[BLOCK_SIZE - 1 - tid];
    }
}

// 演示 reduction，用于单步调试
__global__ void debug_reduction(int *input, int *output, int n) {
    __shared__ int shared_sum[BLOCK_SIZE];

    int tid = threadIdx.x;
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    // 加载数据
    shared_sum[tid] = (idx < n) ? input[idx] : 0;
    __syncthreads();

    // TODO: 在 cuda-gdb 中单步执行这个 reduction
    // 观察每个线程的 shared_sum 值
    for (int s = blockDim.x / 2; s > 0; s >>= 1) {
        if (tid < s) {
            shared_sum[tid] += shared_sum[tid + s];
        }
        __syncthreads();
    }

    if (tid == 0) {
        output[blockIdx.x] = shared_sum[0];
    }
}

int main() {
    printf("cuda-gdb 调试示例\n");
    printf("=========================================\n\n");

    int *h_data = (int*)malloc(N * sizeof(int));
    int *h_output = (int*)malloc(N * sizeof(int));

    for (int i = 0; i < N; i++) {
        h_data[i] = i;
    }

    int *d_data, *d_input, *d_output;
    CUDA_CHECK(cudaMalloc(&d_data, N * sizeof(int)));
    CUDA_CHECK(cudaMalloc(&d_input, N * sizeof(int)));
    CUDA_CHECK(cudaMalloc(&d_output, N * sizeof(int)));

    CUDA_CHECK(cudaMemcpy(d_input, h_data, N * sizeof(int), cudaMemcpyHostToDevice));

    dim3 blockDim(BLOCK_SIZE);
    dim3 gridDim((N + BLOCK_SIZE - 1) / BLOCK_SIZE);

    printf("启动 kernel...\n");

    // 测试 1: 有 bug 的 kernel
    buggy_kernel<<<gridDim, blockDim>>>(d_data, N);
    CUDA_CHECK(cudaDeviceSynchronize());

    // 测试 2: shared memory 调试
    shared_memory_debug<<<gridDim, blockDim>>>(d_input, d_output, N);
    CUDA_CHECK(cudaDeviceSynchronize());

    // 测试 3: reduction 调试
    debug_reduction<<<gridDim, blockDim>>>(d_input, d_output, N);
    CUDA_CHECK(cudaDeviceSynchronize());

    CUDA_CHECK(cudaMemcpy(h_output, d_output, N * sizeof(int), cudaMemcpyDeviceToHost));

    printf("前 10 个结果: ");
    for (int i = 0; i < 10; i++) {
        printf("%d ", h_output[i]);
    }
    printf("\n\n");

    CUDA_CHECK(cudaFree(d_data));
    CUDA_CHECK(cudaFree(d_input));
    CUDA_CHECK(cudaFree(d_output));
    free(h_data);
    free(h_output);

    printf("cuda-gdb 调试步骤:\n\n");

    printf("1. 启动调试器:\n");
    printf("   cuda-gdb ./gdb_demo\n\n");

    printf("2. 设置断点:\n");
    printf("   (cuda-gdb) break buggy_kernel\n");
    printf("   (cuda-gdb) break shared_memory_debug\n\n");

    printf("3. 运行程序:\n");
    printf("   (cuda-gdb) run\n\n");

    printf("4. 检查线程信息:\n");
    printf("   (cuda-gdb) cuda thread\n");
    printf("   (cuda-gdb) cuda block\n");
    printf("   (cuda-gdb) info cuda threads\n\n");

    printf("5. 切换到特定线程:\n");
    printf("   (cuda-gdb) cuda thread (0,0,5)\n");
    printf("   (cuda-gdb) print idx\n");
    printf("   (cuda-gdb) print shared_data[tid]\n\n");

    printf("6. 单步执行:\n");
    printf("   (cuda-gdb) next  # 下一行\n");
    printf("   (cuda-gdb) step  # 进入函数\n\n");

    printf("7. 查看内存:\n");
    printf("   (cuda-gdb) print data[0]@10  # 打印数组前10个元素\n\n");

    printf("TEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
