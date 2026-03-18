// 练习 201: 动态并行 - 嵌套 Kernel 调用
//
// 目标: 学习在 kernel 中启动其他 kernel
//
// 任务:
// 1. 实现父 kernel 调用子 kernel
// 2. 理解 cudaDeviceSynchronize() 在 device 端的使用
// 3. 处理嵌套并行的同步
//
// 编译: nvcc -arch=sm_35 -rdc=true -o dynamic_demo 01_nested_kernels.cu -lcudadevrt
//
// 注意: 动态并行需要 Compute Capability >= 3.5
// -rdc=true 启用可重定位设备代码

#include <stdio.h>
#include <cuda_runtime.h>

#define N 16

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// 子 kernel - 由父 kernel 在 GPU 上调用
__global__ void child_kernel(int *data, int depth) {
    int idx = threadIdx.x;
    printf("  Child kernel: depth=%d, thread=%d, value=%d\n",
           depth, idx, data[idx]);

    data[idx] *= 2;  // 修改数据
}

// TODO: 父 kernel - 在 GPU 上启动子 kernel
__global__ void parent_kernel(int *data, int depth) {
    int idx = threadIdx.x;

    if (idx == 0) {
        printf("Parent kernel: depth=%d, launching child...\n", depth);
    }

    // TODO: 在 kernel 中调用另一个 kernel
    // 语法与主机端相同: child_kernel<<<blocks, threads>>>(...);

    // if (idx == 0) {
    //     child_kernel<<<1, N>>>(data, depth + 1);
    // }

    // TODO: 在 device 端同步
    // 注意: 使用 cudaDeviceSynchronize() 等待子 kernel 完成
    // cudaDeviceSynchronize();

    __syncthreads();  // 确保所有线程到达这里

    if (idx == 0) {
        printf("Parent kernel: child completed\n");
    }
}

int main() {
    cudaDeviceProp prop;
    CUDA_CHECK(cudaGetDeviceProperties(&prop, 0));

    printf("动态并行测试\n");
    printf("GPU: %s\n", prop.name);
    printf("Compute Capability: %d.%d\n\n", prop.major, prop.minor);

    if (prop.major < 3 || (prop.major == 3 && prop.minor < 5)) {
        printf("⚠️  该 GPU 不支持动态并行 (需要 CC >= 3.5)\n");
        printf("TEST_PASSED\n");  // 硬件限制，仍算通过
        return 0;
    }

    // 准备数据
    int *h_data = (int*)malloc(N * sizeof(int));
    for (int i = 0; i < N; i++) {
        h_data[i] = i;
    }

    int *d_data;
    CUDA_CHECK(cudaMalloc(&d_data, N * sizeof(int)));
    CUDA_CHECK(cudaMemcpy(d_data, h_data, N * sizeof(int), cudaMemcpyHostToDevice));

    // 启动父 kernel
    printf("从主机启动父 kernel...\n");
    parent_kernel<<<1, N>>>(d_data, 0);
    CUDA_CHECK(cudaGetLastError());
    CUDA_CHECK(cudaDeviceSynchronize());

    // 检查结果
    CUDA_CHECK(cudaMemcpy(h_data, d_data, N * sizeof(int), cudaMemcpyDeviceToHost));

    printf("\n结果 (应该是原值 * 2):\n");
    for (int i = 0; i < N; i++) {
        printf("%d ", h_data[i]);
    }
    printf("\n");

    CUDA_CHECK(cudaFree(d_data));
    free(h_data);

    printf("\n动态并行测试完成!\n");
    printf("TEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
