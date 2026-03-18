// 练习 183: Compute Sanitizer 内存错误检测
//
// 目标: 使用 Compute Sanitizer 检测内存错误
//
// 任务:
// 1. 检测越界访问
// 2. 检测未初始化内存
// 3. 检测数据竞争
//
// 使用方法:
// 1. 编译: nvcc -g -G -o sanitizer_demo 03_compute_sanitizer.cu
// 2. Memcheck: compute-sanitizer --tool memcheck ./sanitizer_demo
// 3. Racecheck: compute-sanitizer --tool racecheck ./sanitizer_demo
// 4. Initcheck: compute-sanitizer --tool initcheck ./sanitizer_demo
//
// 注意: -g -G 启用调试信息，对于错误定位很重要

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

// 错误 1: 数组越界访问
__global__ void out_of_bounds_access(int *data, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    // TODO: 这里故意越界，Compute Sanitizer 会检测到
    // 修复: 添加边界检查
    // if (idx < n) {
        data[idx + 1] = idx;  // 可能越界!
    // }
}

// 错误 2: 未初始化内存读取
__global__ void uninitialized_read(int *input, int *output, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    if (idx < n) {
        // input 可能未初始化
        output[idx] = input[idx] * 2;
    }
}

// 错误 3: 数据竞争 (race condition)
__global__ void race_condition(int *counter) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    // TODO: 多个线程同时写入，没有同步
    // 修复: 使用 atomicAdd
    *counter = *counter + 1;  // 数据竞争!
    // atomicAdd(counter, 1);  // 正确方式
}

// 错误 4: Shared memory 越界
__global__ void shared_memory_overflow(int *output) {
    __shared__ int shared_data[256];

    int idx = threadIdx.x;

    // TODO: 可能越界
    shared_data[idx + 10] = idx;  // 如果 idx >= 246 就越界
    __syncthreads();

    if (idx < 256) {
        output[idx] = shared_data[idx];
    }
}

// 错误 5: Bank conflict（虽然不是错误，但影响性能）
__global__ void bank_conflict_demo(float *output) {
    __shared__ float shared[256];

    int tid = threadIdx.x;

    // 2-way bank conflict
    shared[tid * 2] = tid;
    __syncthreads();

    output[tid] = shared[tid * 2];
}

// TODO: 修复上面的错误
__global__ void fixed_kernel(int *data, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    // 正确的边界检查
    if (idx < n) {
        data[idx] = idx;
    }
}

int main() {
    printf("Compute Sanitizer 内存错误检测示例\n");
    printf("=========================================\n\n");

    int *d_data, *d_input, *d_output, *d_counter;
    CUDA_CHECK(cudaMalloc(&d_data, N * sizeof(int)));
    CUDA_CHECK(cudaMalloc(&d_input, N * sizeof(int)));
    CUDA_CHECK(cudaMalloc(&d_output, N * sizeof(int)));
    CUDA_CHECK(cudaMalloc(&d_counter, sizeof(int)));

    dim3 blockDim(BLOCK_SIZE);
    dim3 gridDim((N + BLOCK_SIZE - 1) / BLOCK_SIZE);

    printf("测试 1: 越界访问\n");
    out_of_bounds_access<<<gridDim, blockDim>>>(d_data, N);
    CUDA_CHECK(cudaDeviceSynchronize());

    printf("测试 2: 未初始化内存\n");
    uninitialized_read<<<gridDim, blockDim>>>(d_input, d_output, N);
    CUDA_CHECK(cudaDeviceSynchronize());

    printf("测试 3: 数据竞争\n");
    race_condition<<<gridDim, blockDim>>>(d_counter);
    CUDA_CHECK(cudaDeviceSynchronize());

    printf("测试 4: Shared memory 越界\n");
    shared_memory_overflow<<<1, 256>>>(d_output);
    CUDA_CHECK(cudaDeviceSynchronize());

    CUDA_CHECK(cudaFree(d_data));
    CUDA_CHECK(cudaFree(d_input));
    CUDA_CHECK(cudaFree(d_output));
    CUDA_CHECK(cudaFree(d_counter));

    printf("\n使用 Compute Sanitizer 检测错误:\n\n");

    printf("1. Memcheck (内存错误):\n");
    printf("   compute-sanitizer --tool memcheck ./sanitizer_demo\n");
    printf("   检测: 越界访问、非法内存访问、内存泄漏\n\n");

    printf("2. Racecheck (数据竞争):\n");
    printf("   compute-sanitizer --tool racecheck ./sanitizer_demo\n");
    printf("   检测: shared/global memory 的数据竞争\n\n");

    printf("3. Initcheck (未初始化内存):\n");
    printf("   compute-sanitizer --tool initcheck ./sanitizer_demo\n");
    printf("   检测: 读取未初始化的内存\n\n");

    printf("4. Synccheck (同步错误):\n");
    printf("   compute-sanitizer --tool synccheck ./sanitizer_demo\n");
    printf("   检测: 不当的同步使用\n\n");

    printf("提示: 使用 -g -G 编译获得更详细的错误信息\n");

    printf("\nTEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
