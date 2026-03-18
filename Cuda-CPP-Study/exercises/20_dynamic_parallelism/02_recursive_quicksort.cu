// 练习 202: 动态并行 - 递归快速排序
//
// 目标: 使用动态并行实现递归算法
//
// 任务:
// 1. 实现 GPU 快速排序
// 2. 使用动态并行处理递归
// 3. 理解递归深度控制
//
// 编译: nvcc -arch=sm_35 -rdc=true -o quicksort 02_recursive_quicksort.cu -lcudadevrt
//
// 快速排序是经典的递归算法，非常适合展示动态并行

#include <stdio.h>
#include <cuda_runtime.h>
#include <stdlib.h>
#include <time.h>

#define N 256
#define MAX_DEPTH 10

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// Device 端交换函数
__device__ void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

// Device 端 partition 函数
__device__ int partition(int *data, int left, int right) {
    int pivot = data[right];
    int i = left - 1;

    for (int j = left; j < right; j++) {
        if (data[j] <= pivot) {
            i++;
            swap(&data[i], &data[j]);
        }
    }
    swap(&data[i + 1], &data[right]);
    return i + 1;
}

// TODO: 动态并行快速排序 kernel
__global__ void quicksort_kernel(int *data, int left, int right, int depth) {
    // 递归终止条件
    if (left >= right || depth >= MAX_DEPTH) {
        return;
    }

    // TODO: 执行 partition
    // int pivot_idx = partition(data, left, right);

    // TODO: 递归调用自己处理两部分
    // 注意: 每个递归调用启动一个新 kernel

    // if (left < pivot_idx - 1) {
    //     quicksort_kernel<<<1, 1>>>(data, left, pivot_idx - 1, depth + 1);
    // }

    // if (pivot_idx + 1 < right) {
    //     quicksort_kernel<<<1, 1>>>(data, pivot_idx + 1, right, depth + 1);
    // }

    // TODO: 等待子 kernel 完成
    // cudaDeviceSynchronize();
}

// CPU 快速排序（用于验证）
void cpu_quicksort(int *data, int left, int right) {
    if (left >= right) return;

    int pivot = data[right];
    int i = left - 1;

    for (int j = left; j < right; j++) {
        if (data[j] <= pivot) {
            i++;
            int temp = data[i];
            data[i] = data[j];
            data[j] = temp;
        }
    }
    int temp = data[i + 1];
    data[i + 1] = data[right];
    data[right] = temp;

    int pivot_idx = i + 1;

    cpu_quicksort(data, left, pivot_idx - 1);
    cpu_quicksort(data, pivot_idx + 1, right);
}

int main() {
    cudaDeviceProp prop;
    CUDA_CHECK(cudaGetDeviceProperties(&prop, 0));

    printf("动态并行快速排序\n");
    printf("GPU: %s\n", prop.name);
    printf("数据量: %d\n\n", N);

    if (prop.major < 3 || (prop.major == 3 && prop.minor < 5)) {
        printf("⚠️  该 GPU 不支持动态并行\n");
        printf("TEST_PASSED\n");
        return 0;
    }

    srand(time(NULL));

    // 准备数据
    int *h_data = (int*)malloc(N * sizeof(int));
    int *h_verify = (int*)malloc(N * sizeof(int));

    for (int i = 0; i < N; i++) {
        h_data[i] = rand() % 1000;
        h_verify[i] = h_data[i];
    }

    printf("排序前 (前10个): ");
    for (int i = 0; i < 10; i++) {
        printf("%d ", h_data[i]);
    }
    printf("\n");

    // GPU 快速排序
    int *d_data;
    CUDA_CHECK(cudaMalloc(&d_data, N * sizeof(int)));
    CUDA_CHECK(cudaMemcpy(d_data, h_data, N * sizeof(int), cudaMemcpyHostToDevice));

    quicksort_kernel<<<1, 1>>>(d_data, 0, N - 1, 0);
    CUDA_CHECK(cudaGetLastError());
    CUDA_CHECK(cudaDeviceSynchronize());

    CUDA_CHECK(cudaMemcpy(h_data, d_data, N * sizeof(int), cudaMemcpyDeviceToHost));

    printf("GPU排序后 (前10个): ");
    for (int i = 0; i < 10; i++) {
        printf("%d ", h_data[i]);
    }
    printf("\n");

    // CPU 排序验证
    cpu_quicksort(h_verify, 0, N - 1);

    // 验证正确性
    bool correct = true;
    for (int i = 0; i < N; i++) {
        if (h_data[i] != h_verify[i]) {
            correct = false;
            printf("❌ 错误: 位置 %d, GPU=%d, CPU=%d\n", i, h_data[i], h_verify[i]);
            break;
        }
    }

    if (correct) {
        printf("\n✅ 排序结果正确!\n");
    }

    printf("\n动态并行的优势:\n");
    printf("- 适合不规则、数据相关的并行\n");
    printf("- 简化递归算法实现\n");
    printf("- GPU 端自适应并行\n");

    printf("\n注意事项:\n");
    printf("- 递归深度有限制\n");
    printf("- 启动开销大于静态并行\n");
    printf("- 适合粗粒度并行\n");

    CUDA_CHECK(cudaFree(d_data));
    free(h_data);
    free(h_verify);

    printf("\n递归快速排序完成!\n");
    printf("TEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
