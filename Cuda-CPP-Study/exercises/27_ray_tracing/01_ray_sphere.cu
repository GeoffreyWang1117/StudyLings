/**
 * 练习 271: 光线-球体相交测试
 * 学习目标: 实现基础光线追踪相交计算
 */

#include <cuda_runtime.h>
#include <stdio.h>

struct Ray {
    float3 origin;
    float3 direction;
};

struct Sphere {
    float3 center;
    float radius;
    float3 color;
};

__device__ bool ray_sphere_intersect(Ray ray, Sphere sphere, float *t) {
    float3 oc = make_float3(ray.origin.x - sphere.center.x,
                             ray.origin.y - sphere.center.y,
                             ray.origin.z - sphere.center.z);

    float a = ray.direction.x * ray.direction.x +
              ray.direction.y * ray.direction.y +
              ray.direction.z * ray.direction.z;

    float b = 2.0f * (oc.x * ray.direction.x +
                       oc.y * ray.direction.y +
                       oc.z * ray.direction.z);

    float c = oc.x * oc.x + oc.y * oc.y + oc.z * oc.z - sphere.radius * sphere.radius;

    float discriminant = b * b - 4 * a * c;

    if (discriminant < 0) return false;

    *t = (-b - sqrtf(discriminant)) / (2.0f * a);
    return true;
}

int main() {
    printf("=== 光线-球体相交 ===\n");
    printf("任务: 实现光线追踪基础\n");
    return 0;
}
