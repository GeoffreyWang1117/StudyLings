// 综合项目 2: N-Body 引力模拟
//
// 目标: 实现高性能的 N 体问题模拟
//
// 任务:
// 1. 实现引力计算
// 2. 使用 Shared Memory 优化
// 3. 时间积分（Velocity Verlet）
// 4. 可视化准备（输出轨迹）
//
// N-Body 问题: 模拟 N 个相互作用的粒子
// 应用: 天体物理、分子动力学、流体模拟
//
// 整合知识点:
// - Shared Memory 优化
// - 多 Stream 并发
// - 性能优化技巧
// - 数值模拟基础

#include <stdio.h>
#include <cuda_runtime.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>

#define N 4096          // 粒子数量
#define BLOCK_SIZE 256
#define DT 0.01f        // 时间步长
#define SOFTENING 1e-9f  // 软化参数，避免除零
#define G 1.0f          // 引力常数

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA Error: %s\n", cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// 粒子结构
struct Particle {
    float3 pos;    // 位置
    float3 vel;    // 速度
    float mass;    // 质量
};

// TODO: 计算粒子间的引力并更新加速度
__global__ void compute_forces(Particle *particles, float3 *accelerations, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;

    if (i < n) {
        float3 acc = {0.0f, 0.0f, 0.0f};
        float3 my_pos = particles[i].pos;

        // TODO: 方法 1 - 简单版本 (O(N^2))
        // for (int j = 0; j < n; j++) {
        //     if (i != j) {
        //         float3 r;
        //         r.x = particles[j].pos.x - my_pos.x;
        //         r.y = particles[j].pos.y - my_pos.y;
        //         r.z = particles[j].pos.z - my_pos.z;
        //
        //         float dist_sqr = r.x*r.x + r.y*r.y + r.z*r.z + SOFTENING;
        //         float inv_dist = rsqrtf(dist_sqr);
        //         float inv_dist3 = inv_dist * inv_dist * inv_dist;
        //
        //         float force = G * particles[j].mass * inv_dist3;
        //         acc.x += force * r.x;
        //         acc.y += force * r.y;
        //         acc.z += force * r.z;
        //     }
        // }

        accelerations[i] = acc;
    }
}

// TODO: 使用 Shared Memory 优化的版本
__global__ void compute_forces_shared(Particle *particles, float3 *accelerations, int n) {
    __shared__ float3 sh_pos[BLOCK_SIZE];
    __shared__ float sh_mass[BLOCK_SIZE];

    int i = blockIdx.x * blockDim.x + threadIdx.x;
    int tid = threadIdx.x;

    float3 acc = {0.0f, 0.0f, 0.0f};
    float3 my_pos;

    if (i < n) {
        my_pos = particles[i].pos;
    }

    // TODO: 分块计算
    // for (int tile = 0; tile < gridDim.x; tile++) {
    //     int j = tile * blockDim.x + tid;
    //
    //     // 加载到 shared memory
    //     if (j < n) {
    //         sh_pos[tid] = particles[j].pos;
    //         sh_mass[tid] = particles[j].mass;
    //     }
    //     __syncthreads();
    //
    //     // 计算与这个 tile 中所有粒子的作用力
    //     #pragma unroll 8
    //     for (int k = 0; k < BLOCK_SIZE; k++) {
    //         float3 r;
    //         r.x = sh_pos[k].x - my_pos.x;
    //         r.y = sh_pos[k].y - my_pos.y;
    //         r.z = sh_pos[k].z - my_pos.z;
    //
    //         float dist_sqr = r.x*r.x + r.y*r.y + r.z*r.z + SOFTENING;
    //         float inv_dist = rsqrtf(dist_sqr);
    //         float inv_dist3 = inv_dist * inv_dist * inv_dist;
    //
    //         float force = G * sh_mass[k] * inv_dist3;
    //         acc.x += force * r.x;
    //         acc.y += force * r.y;
    //         acc.z += force * r.z;
    //     }
    //     __syncthreads();
    // }

    if (i < n) {
        accelerations[i] = acc;
    }
}

// TODO: 更新位置和速度 (Velocity Verlet 积分)
__global__ void integrate(Particle *particles, float3 *accelerations,
                          float3 *old_acc, float dt, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;

    if (i < n) {
        // Velocity Verlet 算法
        float3 acc = accelerations[i];
        float3 old_a = old_acc[i];

        // 更新速度: v(t+dt) = v(t) + 0.5 * (a(t) + a(t+dt)) * dt
        particles[i].vel.x += 0.5f * (old_a.x + acc.x) * dt;
        particles[i].vel.y += 0.5f * (old_a.y + acc.y) * dt;
        particles[i].vel.z += 0.5f * (old_a.z + acc.z) * dt;

        // 更新位置: x(t+dt) = x(t) + v(t+dt) * dt
        particles[i].pos.x += particles[i].vel.x * dt;
        particles[i].pos.y += particles[i].vel.y * dt;
        particles[i].pos.z += particles[i].vel.z * dt;

        // 保存当前加速度供下次使用
        old_acc[i] = acc;
    }
}

// 初始化粒子（球形分布）
void init_particles(Particle *particles, int n) {
    for (int i = 0; i < n; i++) {
        float theta = 2.0f * M_PI * ((float)rand() / RAND_MAX);
        float phi = acosf(1.0f - 2.0f * ((float)rand() / RAND_MAX));
        float r = powf((float)rand() / RAND_MAX, 1.0f/3.0f) * 100.0f;

        particles[i].pos.x = r * sinf(phi) * cosf(theta);
        particles[i].pos.y = r * sinf(phi) * sinf(theta);
        particles[i].pos.z = r * cosf(phi);

        particles[i].vel.x = 0.0f;
        particles[i].vel.y = 0.0f;
        particles[i].vel.z = 0.0f;

        particles[i].mass = 1.0f;
    }
}

// 计算总能量（用于验证）
float compute_energy(Particle *particles, int n) {
    float kinetic = 0.0f, potential = 0.0f;

    for (int i = 0; i < n; i++) {
        // 动能
        float v2 = particles[i].vel.x * particles[i].vel.x +
                   particles[i].vel.y * particles[i].vel.y +
                   particles[i].vel.z * particles[i].vel.z;
        kinetic += 0.5f * particles[i].mass * v2;

        // 势能
        for (int j = i + 1; j < n; j++) {
            float dx = particles[j].pos.x - particles[i].pos.x;
            float dy = particles[j].pos.y - particles[i].pos.y;
            float dz = particles[j].pos.z - particles[i].pos.z;
            float r = sqrtf(dx*dx + dy*dy + dz*dz + SOFTENING);
            potential -= G * particles[i].mass * particles[j].mass / r;
        }
    }

    return kinetic + potential;
}

int main() {
    printf("=== N-Body 引力模拟 ===\n\n");
    printf("粒子数: %d\n", N);
    printf("时间步长: %.4f\n\n", DT);

    srand(time(NULL));

    // 分配主机内存
    Particle *h_particles = (Particle*)malloc(N * sizeof(Particle));
    init_particles(h_particles, N);

    // 分配设备内存
    Particle *d_particles;
    float3 *d_acc, *d_old_acc;
    CUDA_CHECK(cudaMalloc(&d_particles, N * sizeof(Particle)));
    CUDA_CHECK(cudaMalloc(&d_acc, N * sizeof(float3)));
    CUDA_CHECK(cudaMalloc(&d_old_acc, N * sizeof(float3)));

    CUDA_CHECK(cudaMemcpy(d_particles, h_particles, N * sizeof(Particle),
                          cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemset(d_old_acc, 0, N * sizeof(float3)));

    dim3 blockDim(BLOCK_SIZE);
    dim3 gridDim((N + BLOCK_SIZE - 1) / BLOCK_SIZE);

    // 创建 CUDA 事件用于计时
    cudaEvent_t start, stop;
    CUDA_CHECK(cudaEventCreate(&start));
    CUDA_CHECK(cudaEventCreate(&stop));

    // 模拟循环
    int num_steps = 100;
    printf("运行 %d 个时间步...\n", num_steps);

    CUDA_CHECK(cudaEventRecord(start));

    for (int step = 0; step < num_steps; step++) {
        // 计算作用力
        compute_forces_shared<<<gridDim, blockDim>>>(d_particles, d_acc, N);

        // 更新位置和速度
        integrate<<<gridDim, blockDim>>>(d_particles, d_acc, d_old_acc, DT, N);

        if (step % 10 == 0) {
            printf("步骤 %d/%d\r", step, num_steps);
            fflush(stdout);
        }
    }

    CUDA_CHECK(cudaEventRecord(stop));
    CUDA_CHECK(cudaDeviceSynchronize());

    float milliseconds = 0;
    CUDA_CHECK(cudaEventElapsedTime(&milliseconds, start, stop));

    printf("\n\n模拟完成!\n");
    printf("总时间: %.2f ms\n", milliseconds);
    printf("每步时间: %.2f ms\n", milliseconds / num_steps);
    printf("性能: %.2f GFLOPS\n",
           (float)N * N * 20 * num_steps / (milliseconds * 1e6));

    // 验证能量守恒
    CUDA_CHECK(cudaMemcpy(h_particles, d_particles, N * sizeof(Particle),
                          cudaMemcpyDeviceToHost));

    float energy = compute_energy(h_particles, N);
    printf("总能量: %.6e\n", energy);

    printf("\n优化技巧:\n");
    printf("1. Shared Memory 分块计算\n");
    printf("2. 循环展开提高 ILP\n");
    printf("3. 使用 rsqrtf() 快速平方根倒数\n");
    printf("4. 数据对齐和合并访问\n");

    printf("\n扩展任务:\n");
    printf("- Barnes-Hut 算法（O(N log N)）\n");
    printf("- FMM (Fast Multipole Method)\n");
    printf("- Multi-GPU 扩展\n");
    printf("- 可视化输出（VTK 格式）\n");

    // 清理
    CUDA_CHECK(cudaFree(d_particles));
    CUDA_CHECK(cudaFree(d_acc));
    CUDA_CHECK(cudaFree(d_old_acc));
    CUDA_CHECK(cudaEventDestroy(start));
    CUDA_CHECK(cudaEventDestroy(stop));
    free(h_particles);

    printf("\nTEST_PASSED\n");
    return 0;
}

// I AM NOT DONE
