// 练习 182: Nsight Compute Kernel 性能分析
//
// 目标: 使用 Nsight Compute 深度分析 kernel 性能
//
// 任务:
// 1. 理解 kernel 性能指标
// 2. 分析内存带宽和计算吞吐量
// 3. 根据建议优化 kernel
//
// 使用方法:
// 1. 编译: nvcc -o ncu_demo 02_nsight_compute.cu -lineinfo
// 2. 分析: ncu --set full -o profile ./ncu_demo
// 3. 查看: ncu-ui profile.ncu-rep
//
// 或使用命令行查看关键指标:
// ncu --metrics sm__throughput.avg.pct_of_peak_sustained_elapsed,\
//      dram__throughput.avg.pct_of_peak_sustained_elapsed \
//      ./ncu_demo

#include <stdio.h>
#include <cuda_runtime.h>

#define N (1 << 24)  // 16M elements
#define BLOCK_SIZE 256

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// 示例 1: 内存带宽受限的 kernel
__global__ void memory_bound_kernel(float *a, float *b, float *c, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        // 简单操作，受内存带宽限制
        c[idx] = a[idx] + b[idx];
    }
}

// 示例 2: 计算受限的 kernel
__global__ void compute_bound_kernel(float *a, float *b, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        float x = a[idx];
        // 大量计算
        for (int i = 0; i < 1000; i++) {
            x = sinf(x) * cosf(x) + sqrtf(x);
        }
        b[idx] = x;
    }
}

// TODO: 优化这个 kernel
// 问题: 非合并的内存访问
__global__ void uncoalesced_access(float *input, float *output, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        // 糟糕的访问模式: stride 访问
        int stride = 32;
        if (idx * stride < n) {
            output[idx] = input[idx * stride];
        }
    }
}

// TODO: 优化版本 - 合并访问
__global__ void coalesced_access(float *input, float *output, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        // 连续访问
        // output[idx] = input[idx];
    }
}

// TODO: 分析这个 kernel 的占用率
__global__ void low_occupancy_kernel(float *data, int n) {
    // 使用过多的 shared memory 或寄存器
    __shared__ float shared[4096];  // 16KB shared memory

    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    int tid = threadIdx.x;

    if (idx < n) {
        shared[tid] = data[idx];
        __syncthreads();

        // 一些计算
        float sum = 0.0f;
        for (int i = 0; i < 256; i++) {
            sum += shared[i];
        }

        data[idx] = sum;
    }
}

// TODO: 优化占用率
__global__ void improved_occupancy_kernel(float *data, int n) {
    // 使用更少的 shared memory
    __shared__ float shared[256];

    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    int tid = threadIdx.x;

    // if (idx < n && tid < 256) {
    //     shared[tid] = data[idx];
    //     __syncthreads();
    //
    //     float sum = shared[tid];
    //     data[idx] = sum;
    // }
}

int main() {
    printf("Nsight Compute Kernel 分析示例\n");
    printf("=========================================\n\n");

    float *d_a, *d_b, *d_c;
    CUDA_CHECK(cudaMalloc(&d_a, N * sizeof(float)));
    CUDA_CHECK(cudaMalloc(&d_b, N * sizeof(float)));
    CUDA_CHECK(cudaMalloc(&d_c, N * sizeof(float)));

    dim3 blockDim(BLOCK_SIZE);
    dim3 gridDim((N + BLOCK_SIZE - 1) / BLOCK_SIZE);

    printf("测试 1: 内存带宽受限 kernel\n");
    memory_bound_kernel<<<gridDim, blockDim>>>(d_a, d_b, d_c, N);
    CUDA_CHECK(cudaDeviceSynchronize());

    printf("测试 2: 计算受限 kernel\n");
    compute_bound_kernel<<<gridDim, blockDim>>>(d_a, d_b, N);
    CUDA_CHECK(cudaDeviceSynchronize());

    printf("测试 3: 非合并内存访问\n");
    uncoalesced_access<<<gridDim, blockDim>>>(d_a, d_b, N);
    CUDA_CHECK(cudaDeviceSynchronize());

    printf("测试 4: 低占用率 kernel\n");
    low_occupancy_kernel<<<gridDim, blockDim>>>(d_a, N);
    CUDA_CHECK(cudaDeviceSynchronize());

    CUDA_CHECK(cudaFree(d_a));
    CUDA_CHECK(cudaFree(d_b));
    CUDA_CHECK(cudaFree(d_c));

    printf("\n使用 Nsight Compute 分析:\n");
    printf("1. 基础分析:\n");
    printf("   ncu ./ncu_demo\n\n");
    printf("2. 详细分析:\n");
    printf("   ncu --set full -o profile ./ncu_demo\n\n");
    printf("3. 重点观察指标:\n");
    printf("   - SM Throughput (计算单元利用率)\n");
    printf("   - Memory Throughput (内存带宽利用率)\n");
    printf("   - Occupancy (占用率)\n");
    printf("   - Warp Stall Reasons (warp 停滞原因)\n");
    printf("   - Memory Access Patterns (内存访问模式)\n\n");

    printf("TEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
