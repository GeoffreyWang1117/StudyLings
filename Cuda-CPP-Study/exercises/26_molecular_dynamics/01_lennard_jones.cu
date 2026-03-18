/**
 * 练习 261: Lennard-Jones 势能计算
 * 学习目标: 实现分子间相互作用力计算
 */

#include <cuda_runtime.h>
#include <stdio.h>

struct Particle {
    float3 position;
    float3 velocity;
    float3 force;
};

__global__ void compute_lj_forces(Particle *particles, int n, float epsilon, float sigma) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= n) return;

    float3 force = make_float3(0.0f, 0.0f, 0.0f);
    float3 pos_i = particles[i].position;

    for (int j = 0; j < n; j++) {
        if (i == j) continue;

        float3 pos_j = particles[j].position;
        float3 r = make_float3(pos_i.x - pos_j.x, pos_i.y - pos_j.y, pos_i.z - pos_j.z);
        float r2 = r.x*r.x + r.y*r.y + r.z*r.z;
        float r6 = r2 * r2 * r2;
        float r12 = r6 * r6;

        float f_magnitude = 24.0f * epsilon * (2.0f / r12 - 1.0f / r6) / r2;
        force.x += f_magnitude * r.x;
        force.y += f_magnitude * r.y;
        force.z += f_magnitude * r.z;
    }

    particles[i].force = force;
}

int main() {
    printf("=== Lennard-Jones 势能计算 ===\n");
    printf("任务: 实现分子动力学力计算\n");
    return 0;
}
