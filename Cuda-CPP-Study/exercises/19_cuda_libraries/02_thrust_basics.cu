// 练习 192: Thrust 基础 - STL 风格的 CUDA 编程
//
// 目标: 使用 Thrust 库进行高效的并行算法
//
// 任务:
// 1. 使用 Thrust 向量进行数据管理
// 2. 使用 Thrust 算法 (sort, reduce, transform)
// 3. 对比手写 CUDA kernel
//
// Thrust 是 C++ 模板库，提供类似 STL 的接口，自动优化 GPU 代码

#include <thrust/host_vector.h>
#include <thrust/device_vector.h>
#include <thrust/sort.h>
#include <thrust/reduce.h>
#include <thrust/transform.h>
#include <thrust/functional.h>
#include <thrust/execution_policy.h>
#include <iostream>
#include <time.h>

#define N (1 << 20)  // 1M elements

double get_time() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

// 自定义函数对象
struct square {
    __host__ __device__
    float operator()(float x) const {
        return x * x;
    }
};

int main() {
    std::cout << "Thrust 基础: STL 风格的 GPU 编程\n";
    std::cout << "数据量: " << N << " 个元素\n\n";

    // TODO: 1. 创建和初始化 Thrust 向量
    // 提示: thrust::host_vector 用于主机数据
    // 提示: thrust::device_vector 用于设备数据

    // 主机向量
    // thrust::host_vector<float> h_vec(N);

    // 初始化随机数据
    // for (int i = 0; i < N; i++) {
    //     h_vec[i] = static_cast<float>(rand() % 1000);
    // }

    // TODO: 将数据传输到设备
    // thrust::device_vector<float> d_vec = h_vec;

    std::cout << "测试 1: Reduction (求和)\n";
    // TODO: 使用 thrust::reduce 计算总和
    // float sum = thrust::reduce(d_vec.begin(), d_vec.end(), 0.0f, thrust::plus<float>());
    // std::cout << "Sum: " << sum << "\n\n";

    std::cout << "测试 2: Transformation (平方)\n";
    // TODO: 使用 thrust::transform 对每个元素平方
    // thrust::device_vector<float> d_result(N);
    // thrust::transform(d_vec.begin(), d_vec.end(), d_result.begin(), square());

    // 验证结果
    // thrust::host_vector<float> h_result = d_result;
    // std::cout << "原始值: " << h_vec[0] << " -> 平方后: " << h_result[0] << "\n\n";

    std::cout << "测试 3: Sorting (排序)\n";
    double start = get_time();
    // TODO: 使用 thrust::sort 排序
    // thrust::sort(d_vec.begin(), d_vec.end());
    double thrust_time = get_time() - start;

    std::cout << "Thrust 排序时间: " << thrust_time * 1000 << " ms\n";

    // 验证排序结果
    // thrust::host_vector<float> h_sorted = d_vec;
    // std::cout << "前5个元素: ";
    // for (int i = 0; i < 5; i++) {
    //     std::cout << h_sorted[i] << " ";
    // }
    // std::cout << "\n\n";

    std::cout << "测试 4: 组合操作 - Transform Reduce\n";
    // TODO: 计算平方和 (transform + reduce)
    // float sum_of_squares = thrust::transform_reduce(
    //     d_vec.begin(), d_vec.end(),
    //     square(),
    //     0.0f,
    //     thrust::plus<float>());

    // std::cout << "平方和: " << sum_of_squares << "\n\n";

    std::cout << "测试 5: 自定义 Lambda (C++11)\n";
    // TODO: 使用 lambda 表达式
    // thrust::transform(d_vec.begin(), d_vec.end(), d_result.begin(),
    //     [] __device__ (float x) { return x * 2.0f + 1.0f; });

    std::cout << "Thrust 的优势:\n";
    std::cout << "- 代码简洁，类似 C++ STL\n";
    std::cout << "- 自动内存管理\n";
    std::cout << "- 高性能实现\n";
    std::cout << "- 支持主机和设备执行\n";

    std::cout << "\nThrust 测试完成!\n";
    std::cout << "TEST_PASSED\n";
    return 0;
}

// I AM NOT DONE
