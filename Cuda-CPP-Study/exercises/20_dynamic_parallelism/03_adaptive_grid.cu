// 练习 203: 自适应网格细化
//
// 目标: 使用动态并行实现自适应并行
//
// 任务:
// 1. 根据计算结果动态调整并行粒度
// 2. 实现自适应网格细化
// 3. 理解工作负载平衡
//
// 编译: nvcc -arch=sm_35 -rdc=true -o adaptive 03_adaptive_grid.cu -lcudadevrt
//
// 应用场景: 光线追踪、自适应网格、树遍历等

#include <stdio.h>
#include <cuda_runtime.h>
#include <math.h>

#define GRID_SIZE 16
#define THRESHOLD 0.1
#define MAX_DEPTH 3

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// 复杂度评估函数 - 模拟某些区域需要更细致的计算
__device__ float evaluate_complexity(float x, float y) {
    // 在圆形区域内复杂度高
    float dx = x - 0.5f;
    float dy = y - 0.5f;
    float dist = sqrtf(dx * dx + dy * dy);

    // 距离中心越近，复杂度越高
    return (dist < 0.3f) ? 1.0f : 0.0f;
}

// 计算函数 - 模拟耗时计算
__device__ float compute(float x, float y, int iterations) {
    float result = 0.0f;
    for (int i = 0; i < iterations; i++) {
        result += sinf(x * i) * cosf(y * i);
    }
    return result;
}

// TODO: 自适应 kernel - 根据复杂度决定是否细分
__global__ void adaptive_compute(float *output, int x_start, int y_start,
                                  int size, int depth) {
    int idx = threadIdx.x + threadIdx.y * blockDim.x;

    if (idx == 0) {
        // 计算当前网格的中心点
        float x = (x_start + size / 2.0f) / GRID_SIZE;
        float y = (y_start + size / 2.0f) / GRID_SIZE;

        // 评估复杂度
        float complexity = evaluate_complexity(x, y);

        // TODO: 如果复杂度高且深度未达上限，细分为4个子网格
        if (complexity > THRESHOLD && depth < MAX_DEPTH && size > 1) {
            int half_size = size / 2;

            // 递归调用处理4个象限
            // adaptive_compute<<<1, 1>>>(output, x_start, y_start,
            //                            half_size, depth + 1);
            // adaptive_compute<<<1, 1>>>(output, x_start + half_size, y_start,
            //                            half_size, depth + 1);
            // adaptive_compute<<<1, 1>>>(output, x_start, y_start + half_size,
            //                            half_size, depth + 1);
            // adaptive_compute<<<1, 1>>>(output, x_start + half_size, y_start + half_size,
            //                            half_size, depth + 1);

            // cudaDeviceSynchronize();

            printf("Refined: [%d,%d] size=%d depth=%d complexity=%.2f\n",
                   x_start, y_start, size, depth, complexity);
        } else {
            // 复杂度低或已达最大深度，直接计算
            int iterations = (complexity > THRESHOLD) ? 1000 : 100;
            float result = compute(x, y, iterations);

            // 存储结果
            int out_idx = x_start + y_start * GRID_SIZE;
            if (out_idx < GRID_SIZE * GRID_SIZE) {
                output[out_idx] = result;
            }

            printf("Computed: [%d,%d] depth=%d iterations=%d result=%.2f\n",
                   x_start, y_start, depth, iterations, result);
        }
    }
}

int main() {
    cudaDeviceProp prop;
    CUDA_CHECK(cudaGetDeviceProperties(&prop, 0));

    printf("自适应网格细化\n");
    printf("GPU: %s\n", prop.name);
    printf("网格大小: %d x %d\n\n", GRID_SIZE, GRID_SIZE);

    if (prop.major < 3 || (prop.major == 3 && prop.minor < 5)) {
        printf("⚠️  该 GPU 不支持动态并行\n");
        printf("TEST_PASSED\n");
        return 0;
    }

    // 分配输出数组
    float *d_output;
    CUDA_CHECK(cudaMalloc(&d_output, GRID_SIZE * GRID_SIZE * sizeof(float)));
    CUDA_CHECK(cudaMemset(d_output, 0, GRID_SIZE * GRID_SIZE * sizeof(float)));

    // 启动自适应计算
    printf("开始自适应计算...\n\n");
    adaptive_compute<<<1, 1>>>(d_output, 0, 0, GRID_SIZE, 0);
    CUDA_CHECK(cudaGetLastError());
    CUDA_CHECK(cudaDeviceSynchronize());

    // 复制结果
    float *h_output = (float*)malloc(GRID_SIZE * GRID_SIZE * sizeof(float));
    CUDA_CHECK(cudaMemcpy(h_output, d_output, GRID_SIZE * GRID_SIZE * sizeof(float),
                          cudaMemcpyDeviceToHost));

    printf("\n结果网格 (部分):\n");
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            printf("%.2f ", h_output[i * GRID_SIZE + j]);
        }
        printf("\n");
    }

    printf("\n自适应并行的应用:\n");
    printf("- 光线追踪: 复杂场景细分\n");
    printf("- 碰撞检测: 层次包围盒\n");
    printf("- 科学计算: 自适应网格细化(AMR)\n");
    printf("- 树遍历: 八叉树/四叉树\n");

    CUDA_CHECK(cudaFree(d_output));
    free(h_output);

    printf("\n自适应网格测试完成!\n");
    printf("TEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
