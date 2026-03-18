// 练习 101: 前缀和（扫描）
//
// 目标: 实现并行前缀和算法
//
// 任务:
// 1. 实现 inclusive scan (包含当前元素)
// 2. 使用 work-efficient 算法
// 3. 处理任意大小的数组

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

// TODO: 实现 block 级别的 scan
__global__ void scan_block(int *input, int *output, int *block_sums, int n) {
    __shared__ int temp[BLOCK_SIZE * 2];

    int tid = threadIdx.x;
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    // TODO: 加载数据到共享内存
    // temp[tid] = (idx < n) ? input[idx] : 0;
    // __syncthreads();

    // TODO: Up-sweep (reduce) phase
    // for (int stride = 1; stride < blockDim.x; stride *= 2) {
    //     int index = (tid + 1) * stride * 2 - 1;
    //     if (index < blockDim.x) {
    //         temp[index] += temp[index - stride];
    //     }
    //     __syncthreads();
    // }

    // TODO: 保存 block sum
    // if (tid == blockDim.x - 1 && block_sums != nullptr) {
    //     block_sums[blockIdx.x] = temp[tid];
    // }

    // TODO: Down-sweep phase
    // if (tid == blockDim.x - 1) temp[tid] = 0;
    // __syncthreads();

    // for (int stride = blockDim.x / 2; stride > 0; stride /= 2) {
    //     int index = (tid + 1) * stride * 2 - 1;
    //     if (index < blockDim.x) {
    //         int t = temp[index - stride];
    //         temp[index - stride] = temp[index];
    //         temp[index] += t;
    //     }
    //     __syncthreads();
    // }

    // TODO: 写回结果
    // if (idx < n) {
    //     output[idx] = temp[tid];
    // }
}

int main() {
    int *h_input, *h_output, *h_expected;
    int *d_input, *d_output;

    h_input = (int*)malloc(N * sizeof(int));
    h_output = (int*)malloc(N * sizeof(int));
    h_expected = (int*)malloc(N * sizeof(int));

    // 初始化为 1
    for (int i = 0; i < N; i++) {
        h_input[i] = 1;
    }

    // CPU 参考实现
    h_expected[0] = h_input[0];
    for (int i = 1; i < N; i++) {
        h_expected[i] = h_expected[i-1] + h_input[i];
    }

    CUDA_CHECK(cudaMalloc(&d_input, N * sizeof(int)));
    CUDA_CHECK(cudaMalloc(&d_output, N * sizeof(int)));

    CUDA_CHECK(cudaMemcpy(d_input, h_input, N * sizeof(int), cudaMemcpyHostToDevice));

    int grid_size = (N + BLOCK_SIZE - 1) / BLOCK_SIZE;
    scan_block<<<grid_size, BLOCK_SIZE>>>(d_input, d_output, nullptr, N);
    CUDA_CHECK(cudaDeviceSynchronize());

    CUDA_CHECK(cudaMemcpy(h_output, d_output, N * sizeof(int), cudaMemcpyDeviceToHost));

    // 验证（简化版，仅检查单个 block）
    bool success = true;
    int check_size = min(N, BLOCK_SIZE);
    for (int i = 0; i < check_size; i++) {
        if (h_output[i] != h_expected[i]) {
            printf("错误 at %d: got %d, expected %d\n", i, h_output[i], h_expected[i]);
            success = false;
            break;
        }
    }

    CUDA_CHECK(cudaFree(d_input));
    CUDA_CHECK(cudaFree(d_output));
    free(h_input);
    free(h_output);
    free(h_expected);

    if (success) {
        printf("前缀和计算正确!\n");
        printf("TEST_PASSED\n");
    } else {
        printf("TEST_FAILED\n");
    }

    return success ? 0 : 1;
}

// I AM NOT DONE
