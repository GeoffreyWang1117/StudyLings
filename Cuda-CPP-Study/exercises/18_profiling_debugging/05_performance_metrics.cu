// 练习 185: 性能指标解读与优化
//
// 目标: 理解和优化关键性能指标
//
// 任务:
// 1. 计算理论性能上限
// 2. 测量实际性能
// 3. 分析优化空间
//
// 关键指标:
// - 占用率 (Occupancy)
// - 带宽利用率 (Bandwidth Utilization)
// - 计算吞吐量 (Compute Throughput)
// - IPC (Instructions Per Cycle)
// - Warp Efficiency

#include <stdio.h>
#include <cuda_runtime.h>
#include <time.h>

#define N (1 << 24)  // 16M
#define BLOCK_SIZE 256

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

// 测试内存带宽
__global__ void bandwidth_test(float *input, float *output, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        output[idx] = input[idx];
    }
}

// 测试计算吞吐量
__global__ void compute_throughput_test(float *data, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        float x = data[idx];
        // FMA 操作
        #pragma unroll
        for (int i = 0; i < 100; i++) {
            x = x * 1.01f + 0.5f;  // FMA
        }
        data[idx] = x;
    }
}

// TODO: 分析和优化这个 kernel 的占用率
__global__ void analyze_occupancy(float *data, int n) {
    // 查看这个 kernel 的资源使用
    __shared__ float shared[1024];  // Shared memory 使用

    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    int tid = threadIdx.x;

    // 寄存器使用
    float reg1, reg2, reg3, reg4;

    if (idx < n) {
        shared[tid] = data[idx];
        __syncthreads();

        reg1 = shared[tid];
        reg2 = shared[(tid + 1) % BLOCK_SIZE];
        reg3 = shared[(tid + 2) % BLOCK_SIZE];
        reg4 = shared[(tid + 3) % BLOCK_SIZE];

        data[idx] = reg1 + reg2 + reg3 + reg4;
    }
}

// 计算理论带宽
void calculate_theoretical_bandwidth(cudaDeviceProp &prop) {
    // 理论峰值带宽 = 内存时钟频率 * 内存总线宽度 * 2 (DDR)
    double memory_clock_khz = prop.memoryClockRate;  // kHz
    double memory_bus_width = prop.memoryBusWidth;    // bits

    double bandwidth_gb_s = (memory_clock_khz * 1000.0) *
                            (memory_bus_width / 8.0) * 2.0 / 1e9;

    printf("理论内存带宽: %.2f GB/s\n", bandwidth_gb_s);
}

// 计算理论计算吞吐量
void calculate_theoretical_flops(cudaDeviceProp &prop) {
    // 理论峰值 FLOPS = SM数量 * 时钟频率 * 每周期FMA操作数
    int sm_count = prop.multiProcessorCount;
    double clock_ghz = prop.clockRate / 1e6;  // GHz

    // 每个SM每周期的FP32 FMA操作数（取决于架构）
    int ops_per_clock = 64;  // 这是估计值，实际取决于具体架构

    double peak_tflops = sm_count * clock_ghz * ops_per_clock * 2.0 / 1000.0;

    printf("理论计算峰值 (FP32): ~%.2f TFLOPS\n", peak_tflops);
}

int main() {
    printf("性能指标分析与优化\n");
    printf("=========================================\n\n");

    cudaDeviceProp prop;
    CUDA_CHECK(cudaGetDeviceProperties(&prop, 0));

    printf("GPU: %s\n", prop.name);
    printf("Compute Capability: %d.%d\n", prop.major, prop.minor);
    printf("SM 数量: %d\n", prop.multiProcessorCount);
    printf("时钟频率: %.2f GHz\n", prop.clockRate / 1e6);
    printf("内存时钟: %.2f GHz\n", prop.memoryClockRate / 1e6);
    printf("内存总线宽度: %d bits\n\n", prop.memoryBusWidth);

    calculate_theoretical_bandwidth(prop);
    calculate_theoretical_flops(prop);
    printf("\n");

    float *d_input, *d_output;
    CUDA_CHECK(cudaMalloc(&d_input, N * sizeof(float)));
    CUDA_CHECK(cudaMalloc(&d_output, N * sizeof(float)));

    dim3 blockDim(BLOCK_SIZE);
    dim3 gridDim((N + BLOCK_SIZE - 1) / BLOCK_SIZE);

    // 测试 1: 内存带宽
    printf("测试 1: 内存带宽\n");
    double start = get_time();
    bandwidth_test<<<gridDim, blockDim>>>(d_input, d_output, N);
    CUDA_CHECK(cudaDeviceSynchronize());
    double elapsed = get_time() - start;

    double bytes_transferred = 2.0 * N * sizeof(float);  // 读 + 写
    double bandwidth_gb_s = bytes_transferred / (elapsed * 1e9);

    printf("实际带宽: %.2f GB/s\n", bandwidth_gb_s);
    printf("时间: %.3f ms\n\n", elapsed * 1000);

    // 测试 2: 计算吞吐量
    printf("测试 2: 计算吞吐量\n");
    start = get_time();
    compute_throughput_test<<<gridDim, blockDim>>>(d_output, N);
    CUDA_CHECK(cudaDeviceSynchronize());
    elapsed = get_time() - start;

    double flops = N * 100.0 * 2.0;  // 100次FMA，每次2个操作
    double tflops = flops / (elapsed * 1e12);

    printf("计算吞吐量: %.2f TFLOPS\n", tflops);
    printf("时间: %.3f ms\n\n", elapsed * 1000);

    // TODO: 测试占用率
    printf("测试 3: 占用率分析\n");
    analyze_occupancy<<<gridDim, blockDim>>>(d_output, N);
    CUDA_CHECK(cudaDeviceSynchronize());

    // 计算理论占用率
    // TODO: 使用 cudaOccupancyMaxActiveBlocksPerMultiprocessor
    int maxActiveBlocks;
    CUDA_CHECK(cudaOccupancyMaxActiveBlocksPerMultiprocessor(
        &maxActiveBlocks, analyze_occupancy, BLOCK_SIZE, 1024 * sizeof(float)));

    double occupancy = (maxActiveBlocks * BLOCK_SIZE) /
                       (double)prop.maxThreadsPerMultiProcessor;

    printf("理论占用率: %.1f%%\n", occupancy * 100);
    printf("每个 SM 最大活跃 blocks: %d\n\n", maxActiveBlocks);

    CUDA_CHECK(cudaFree(d_input));
    CUDA_CHECK(cudaFree(d_output));

    printf("优化建议:\n");
    printf("1. 带宽优化:\n");
    printf("   - 使用合并内存访问\n");
    printf("   - 增加每线程的工作量\n");
    printf("   - 使用 shared memory 减少全局内存访问\n\n");

    printf("2. 计算优化:\n");
    printf("   - 增加算术强度 (计算/内存比)\n");
    printf("   - 使用 FMA 指令\n");
    printf("   - 减少分支divergence\n\n");

    printf("3. 占用率优化:\n");
    printf("   - 减少寄存器使用\n");
    printf("   - 减少 shared memory 使用\n");
    printf("   - 调整 block 大小\n\n");

    printf("使用 Nsight Compute 查看详细指标:\n");
    printf("ncu --metrics sm__throughput.avg.pct_of_peak_sustained_elapsed,\\\n");
    printf("     dram__throughput.avg.pct_of_peak_sustained_elapsed,\\\n");
    printf("     sm__warps_active.avg.pct_of_peak_sustained_active \\\n");
    printf("     ./metrics_demo\n\n");

    printf("TEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
