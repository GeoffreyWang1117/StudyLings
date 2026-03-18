#include "exercise_manager.h"
#include "progress.h"
#include <iostream>
#include <fstream>
#include <filesystem>
#include <algorithm>

namespace fs = std::filesystem;

ExerciseManager::ExerciseManager() {}

bool ExerciseManager::initialize() {
    load_exercises();

    if (exercises_.empty()) {
        std::cerr << "警告: 没有找到练习" << std::endl;
        return false;
    }

    std::cout << "✅ 已加载 " << exercises_.size() << " 个练习" << std::endl;
    return true;
}

void ExerciseManager::load_exercises() {
    exercises_.clear();

    // 加载各个主题的练习
    add_intro_exercises();
    add_kernel_exercises();
    add_thread_exercises();
    add_memory_exercises();
    add_shared_memory_exercises();
    add_sync_exercises();
    add_optimization_exercises();
    add_stream_exercises();
    add_advanced_exercises();
    add_algorithm_exercises();
    add_image_processing_exercises();
    add_deep_learning_exercises();
    add_scientific_computing_exercises();
    add_multi_gpu_exercises();
    add_tensor_cores_exercises();
    add_cuda_graphs_exercises();
    add_cooperative_groups_exercises();
    add_profiling_debugging_exercises();
    add_cuda_libraries_exercises();
    add_dynamic_parallelism_exercises();
    add_projects_exercises();
    add_unified_memory_exercises();
    add_warp_primitives_exercises();
    add_graph_algorithms_exercises();
    add_sparse_matrices_exercises();
    add_molecular_dynamics_exercises();
    add_ray_tracing_exercises();
    add_video_processing_exercises();
    add_ml_operators_exercises();

    // 按编号排序
    std::sort(exercises_.begin(), exercises_.end(),
              [](const Exercise& a, const Exercise& b) {
                  return a.number < b.number;
              });
}

void ExerciseManager::add_intro_exercises() {
    // 练习 1-5: CUDA 基础
    exercises_.push_back({
        1, "01_intro", "hello_cuda",
        "exercises/01_intro/01_hello_cuda.cu",
        "编写你的第一个 CUDA 程序：在 GPU 上打印 Hello World",
        {
            "提示 1: 使用 printf() 可以在 CUDA kernel 中打印信息",
            "提示 2: 需要调用 cudaDeviceSynchronize() 确保输出被刷新",
            "提示 3: kernel 调用格式: kernel_name<<<blocks, threads>>>()"
        },
        "solutions/01_intro/01_hello_cuda.cu"
    });

    exercises_.push_back({
        2, "01_intro", "device_query",
        "exercises/01_intro/02_device_query.cu",
        "查询 GPU 设备属性：获取并打印 GPU 信息",
        {
            "提示 1: 使用 cudaGetDeviceCount() 获取 GPU 数量",
            "提示 2: 使用 cudaGetDeviceProperties() 获取设备属性",
            "提示 3: cudaDeviceProp 结构包含所有设备信息"
        },
        "solutions/01_intro/02_device_query.cu"
    });

    exercises_.push_back({
        3, "01_intro", "error_handling",
        "exercises/01_intro/03_error_handling.cu",
        "CUDA 错误处理：正确检查和处理 CUDA API 错误",
        {
            "提示 1: 每个 CUDA API 调用都返回 cudaError_t",
            "提示 2: 使用 cudaGetErrorString() 获取错误描述",
            "提示 3: 创建一个宏来简化错误检查"
        },
        "solutions/01_intro/03_error_handling.cu"
    });

    exercises_.push_back({
        4, "01_intro", "memory_basics",
        "exercises/01_intro/04_memory_basics.cu",
        "学习基本的设备内存分配和释放",
        {
            "提示 1: 使用 cudaMalloc 分配设备内存",
            "提示 2: 使用 cudaMemset 或 cudaMemcpy 初始化",
            "提示 3: 使用 cudaFree 释放内存"
        },
        "solutions/01_intro/04_memory_basics.cu"
    });

    exercises_.push_back({
        5, "01_intro", "data_transfer",
        "exercises/01_intro/05_data_transfer.cu",
        "掌握主机和设备之间的数据传输",
        {
            "提示 1: cudaMemcpy 用于数据传输",
            "提示 2: 注意传输方向参数",
            "提示 3: 记得同步设备"
        },
        "solutions/01_intro/05_data_transfer.cu"
    });
}

void ExerciseManager::add_kernel_exercises() {
    // 练习 6-10: 内核函数基础
    exercises_.push_back({
        6, "02_kernels", "simple_add",
        "exercises/02_kernels/01_simple_add.cu",
        "简单的向量加法：实现 A + B = C",
        {
            "提示 1: 每个线程处理一个元素",
            "提示 2: 使用 threadIdx.x 获取线程索引",
            "提示 3: 记得分配设备内存并拷贝数据"
        },
        "solutions/02_kernels/01_simple_add.cu"
    });

    exercises_.push_back({
        7, "02_kernels", "vector_scale",
        "exercises/02_kernels/02_vector_scale.cu",
        "向量缩放：将向量的每个元素乘以标量",
        {
            "提示 1: kernel 可以接受标量参数",
            "提示 2: 确保不越界访问",
            "提示 3: 使用 if (idx < N) 进行边界检查"
        },
        "solutions/02_kernels/02_vector_scale.cu"
    });

    exercises_.push_back({
        8, "02_kernels", "dot_product",
        "exercises/02_kernels/03_dot_product.cu",
        "向量点积：实现向量内积运算",
        {
            "提示 1: 需要归约操作",
            "提示 2: 使用共享内存加速",
            "提示 3: 树形归约模式"
        },
        "solutions/02_kernels/03_dot_product.cu"
    });

    exercises_.push_back({
        9, "02_kernels", "matrix_add",
        "exercises/02_kernels/04_matrix_add.cu",
        "矩阵加法：使用 2D 线程网格",
        {
            "提示 1: 使用 2D 线程块",
            "提示 2: 计算行列索引",
            "提示 3: 注意边界检查"
        },
        "solutions/02_kernels/04_matrix_add.cu"
    });

    exercises_.push_back({
        10, "02_kernels", "element_wise",
        "exercises/02_kernels/05_element_wise.cu",
        "元素级操作：实现 sigmoid 函数",
        {
            "提示 1: 使用数学函数库",
            "提示 2: expf() 计算指数",
            "提示 3: 注意数值稳定性"
        },
        "solutions/02_kernels/05_element_wise.cu"
    });
}

void ExerciseManager::add_thread_exercises() {
    // 练习 16-19: 线程和块
    exercises_.push_back({
        16, "03_threads", "thread_index",
        "exercises/03_threads/01_thread_index.cu",
        "理解线程索引：计算全局线程 ID",
        {
            "提示 1: 全局索引 = blockIdx.x * blockDim.x + threadIdx.x",
            "提示 2: 这是最常用的索引计算模式",
            "提示 3: 注意区分 blockIdx 和 threadIdx"
        },
        "solutions/03_threads/01_thread_index.cu"
    });

    exercises_.push_back({
        17, "03_threads", "2d_threads",
        "exercises/03_threads/02_2d_threads.cu",
        "二维线程网格：处理矩阵数据",
        {
            "提示 1: 使用 threadIdx.y 和 blockIdx.y",
            "提示 2: 行索引和列索引需要分别计算",
            "提示 3: idx = row * width + col"
        },
        "solutions/03_threads/02_2d_threads.cu"
    });

    exercises_.push_back({
        18, "03_threads", "3d_threads",
        "exercises/03_threads/03_3d_threads.cu",
        "三维线程网格：处理 3D 数据",
        {
            "提示 1: 使用 threadIdx.z 和 blockIdx.z",
            "提示 2: 计算 x, y, z 三个索引",
            "提示 3: 线性索引 = x + y*width + z*width*height"
        },
        "solutions/03_threads/03_3d_threads.cu"
    });

    exercises_.push_back({
        19, "03_threads", "grid_stride",
        "exercises/03_threads/04_grid_stride.cu",
        "Grid-Stride 循环：处理大数组",
        {
            "提示 1: stride = gridDim.x * blockDim.x",
            "提示 2: 使用 for 循环处理多个元素",
            "提示 3: 这种模式更灵活和可扩展"
        },
        "solutions/03_threads/04_grid_stride.cu"
    });
}

void ExerciseManager::add_memory_exercises() {
    // 练习 26-29: 内存管理
    exercises_.push_back({
        26, "04_memory", "malloc_free",
        "exercises/04_memory/01_malloc_free.cu",
        "设备内存分配：使用 cudaMalloc 和 cudaFree",
        {
            "提示 1: cudaMalloc 需要传递指针的地址",
            "提示 2: 总是检查返回值",
            "提示 3: 记得在程序结束前 cudaFree"
        },
        "solutions/04_memory/01_malloc_free.cu"
    });

    exercises_.push_back({
        27, "04_memory", "memcpy",
        "exercises/04_memory/02_memcpy.cu",
        "内存拷贝：主机和设备之间传输数据",
        {
            "提示 1: cudaMemcpy 需要指定传输方向",
            "提示 2: cudaMemcpyHostToDevice 和 cudaMemcpyDeviceToHost",
            "提示 3: 拷贝大小以字节为单位"
        },
        "solutions/04_memory/02_memcpy.cu"
    });

    exercises_.push_back({
        28, "04_memory", "pinned_memory",
        "exercises/04_memory/03_pinned_memory.cu",
        "固定内存：使用 pinned memory 加速传输",
        {
            "提示 1: 使用 cudaMallocHost 分配",
            "提示 2: 固定内存传输更快",
            "提示 3: 使用 cudaFreeHost 释放"
        },
        "solutions/04_memory/03_pinned_memory.cu"
    });

    exercises_.push_back({
        29, "04_memory", "unified_memory",
        "exercises/04_memory/04_unified_memory.cu",
        "统一内存：简化内存管理",
        {
            "提示 1: 使用 cudaMallocManaged",
            "提示 2: 主机和设备自动迁移",
            "提示 3: 记得同步设备"
        },
        "solutions/04_memory/04_unified_memory.cu"
    });
}

void ExerciseManager::add_shared_memory_exercises() {
    // 练习 41-43: 共享内存
    exercises_.push_back({
        41, "05_shared_memory", "basic_shared",
        "exercises/05_shared_memory/01_basic_shared.cu",
        "共享内存基础：使用 __shared__ 关键字",
        {
            "提示 1: __shared__ 变量在 block 内所有线程共享",
            "提示 2: 共享内存比全局内存快得多",
            "提示 3: 需要使用 __syncthreads() 同步"
        },
        "solutions/05_shared_memory/01_basic_shared.cu"
    });

    exercises_.push_back({
        42, "05_shared_memory", "matrix_transpose",
        "exercises/05_shared_memory/02_matrix_transpose.cu",
        "矩阵转置：使用共享内存优化",
        {
            "提示 1: 使用 tile 分块",
            "提示 2: 共享内存作为中间缓冲",
            "提示 3: 避免 bank 冲突"
        },
        "solutions/05_shared_memory/02_matrix_transpose.cu"
    });

    exercises_.push_back({
        43, "05_shared_memory", "1d_stencil",
        "exercises/05_shared_memory/03_1d_stencil.cu",
        "1D 模板操作：使用共享内存处理 halo",
        {
            "提示 1: 加载主要数据和 halo 区域",
            "提示 2: 同步后计算",
            "提示 3: 处理边界条件"
        },
        "solutions/05_shared_memory/03_1d_stencil.cu"
    });
}

void ExerciseManager::add_sync_exercises() {
    // 练习 56-57: 同步
    exercises_.push_back({
        56, "06_sync", "syncthreads",
        "exercises/06_sync/01_syncthreads.cu",
        "线程同步：使用 __syncthreads()",
        {
            "提示 1: __syncthreads() 是 block 内的栅栏",
            "提示 2: 所有线程必须都能到达同步点",
            "提示 3: 不能在条件语句的一个分支中使用"
        },
        "solutions/06_sync/01_syncthreads.cu"
    });

    exercises_.push_back({
        57, "06_sync", "atomic_operations",
        "exercises/06_sync/02_atomic_operations.cu",
        "原子操作：避免竞态条件",
        {
            "提示 1: 使用 atomicAdd, atomicMax 等",
            "提示 2: 原子操作保证线程安全",
            "提示 3: 直方图计算是典型应用"
        },
        "solutions/06_sync/02_atomic_operations.cu"
    });
}

void ExerciseManager::add_optimization_exercises() {
    // 练习 66-67: 性能优化
    exercises_.push_back({
        66, "07_optimization", "coalescing",
        "exercises/07_optimization/01_coalescing.cu",
        "内存合并访问：优化全局内存访问模式",
        {
            "提示 1: 相邻线程应访问相邻内存",
            "提示 2: 对齐访问可以提高性能",
            "提示 3: 使用 nvidia-smi 或 nsight 分析"
        },
        "solutions/07_optimization/01_coalescing.cu"
    });

    exercises_.push_back({
        67, "07_optimization", "occupancy",
        "exercises/07_optimization/02_occupancy.cu",
        "占用率优化：调整 block 大小",
        {
            "提示 1: 使用 cudaOccupancyMaxPotentialBlockSize",
            "提示 2: 平衡资源使用",
            "提示 3: 测量实际占用率"
        },
        "solutions/07_optimization/02_occupancy.cu"
    });
}

void ExerciseManager::add_stream_exercises() {
    // 练习 81-83: CUDA 流
    exercises_.push_back({
        81, "08_streams", "basic_stream",
        "exercises/08_streams/01_basic_stream.cu",
        "CUDA 流基础：创建和使用流",
        {
            "提示 1: 使用 cudaStreamCreate() 创建流",
            "提示 2: kernel 可以指定在哪个流中执行",
            "提示 3: 不同流中的操作可以并发执行"
        },
        "solutions/08_streams/01_basic_stream.cu"
    });

    exercises_.push_back({
        82, "08_streams", "concurrent_kernels",
        "exercises/08_streams/02_concurrent_kernels.cu",
        "并发 Kernel：在不同流中并发执行",
        {
            "提示 1: 为每个流创建独立数据",
            "提示 2: 在流中启动 kernel",
            "提示 3: 使用事件测量性能"
        },
        "solutions/08_streams/02_concurrent_kernels.cu"
    });

    exercises_.push_back({
        83, "08_streams", "stream_events",
        "exercises/08_streams/03_stream_events.cu",
        "流和事件：计时和同步",
        {
            "提示 1: cudaEventCreate 创建事件",
            "提示 2: cudaEventRecord 记录时间点",
            "提示 3: cudaEventElapsedTime 计算时间差"
        },
        "solutions/08_streams/03_stream_events.cu"
    });
}

void ExerciseManager::add_advanced_exercises() {
    // 练习 91-92: 高级特性
    exercises_.push_back({
        91, "09_advanced", "reduction",
        "exercises/09_advanced/01_reduction.cu",
        "归约操作：实现高效的求和归约",
        {
            "提示 1: 使用共享内存减少全局内存访问",
            "提示 2: 使用树形归约模式",
            "提示 3: 避免 warp 分化"
        },
        "solutions/09_advanced/01_reduction.cu"
    });

    exercises_.push_back({
        92, "09_advanced", "matrix_multiply",
        "exercises/09_advanced/02_matrix_multiply.cu",
        "矩阵乘法：使用共享内存优化",
        {
            "提示 1: 使用 tiling 技术",
            "提示 2: 共享内存存储 tile",
            "提示 3: 减少全局内存访问"
        },
        "solutions/09_advanced/02_matrix_multiply.cu"
    });
}

const Exercise* ExerciseManager::get_exercise(int number) const {
    auto it = std::find_if(exercises_.begin(), exercises_.end(),
                          [number](const Exercise& e) {
                              return e.number == number;
                          });

    return it != exercises_.end() ? &(*it) : nullptr;
}

const Exercise* ExerciseManager::get_next_incomplete() const {
    ProgressTracker progress;

    for (const auto& ex : exercises_) {
        if (!progress.is_completed(ex.number)) {
            return &ex;
        }
    }

    return nullptr; // 所有练习都已完成
}

void ExerciseManager::list_exercises() const {
    ProgressTracker progress;

    std::cout << "\n📚 CUDA C++ 练习列表:\n" << std::endl;
    std::cout << "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" << std::endl;

    std::string current_topic;
    for (const auto& ex : exercises_) {
        if (ex.topic != current_topic) {
            current_topic = ex.topic;
            std::cout << "\n📂 " << current_topic << std::endl;
        }

        std::string status = progress.is_completed(ex.number) ? "✅" : "⏳";
        std::cout << "  " << status << " " << ex.get_display_name() << std::endl;
        std::cout << "     " << ex.description << std::endl;
    }

    std::cout << "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" << std::endl;

    int completed = progress.get_completed_count();
    int total = exercises_.size();
    std::cout << "\n进度: " << completed << "/" << total
              << " (" << (completed * 100 / total) << "%)" << std::endl;
}

void ExerciseManager::reset_exercise(int number) {
    const Exercise* ex = get_exercise(number);
    if (!ex) {
        std::cerr << "❌ 练习 " << number << " 不存在" << std::endl;
        return;
    }

    // 这里应该从备份恢复原始文件
    // 简化实现：提示用户手动恢复
    std::cout << "⚠️  要重置练习 " << ex->get_display_name() << "，请从 git 恢复:" << std::endl;
    std::cout << "    git checkout " << ex->file_path << std::endl;
}

void ExerciseManager::show_solution(int number) const {
    const Exercise* ex = get_exercise(number);
    if (!ex) {
        std::cerr << "❌ 练习 " << number << " 不存在" << std::endl;
        return;
    }

    std::cout << "⚠️  查看答案会影响学习效果，确定要继续吗？(y/N): ";
    std::string response;
    std::getline(std::cin, response);

    if (response != "y" && response != "Y") {
        std::cout << "已取消" << std::endl;
        return;
    }

    std::ifstream file(ex->solution_path);
    if (!file.is_open()) {
        std::cerr << "❌ 无法打开答案文件: " << ex->solution_path << std::endl;
        return;
    }

    std::cout << "\n" << "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" << std::endl;
    std::cout << "📖 " << ex->get_display_name() << " - 参考答案" << std::endl;
    std::cout << "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n" << std::endl;

    std::string line;
    while (std::getline(file, line)) {
        std::cout << line << std::endl;
    }

    std::cout << "\n" << "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" << std::endl;
}

void ExerciseManager::add_algorithm_exercises() {
    // 练习 101-103: 高级算法
    exercises_.push_back({
        101, "10_algorithms", "prefix_sum",
        "exercises/10_algorithms/01_prefix_sum.cu",
        "前缀和（扫描）：实现并行 scan 算法",
        {
            "提示 1: 使用 work-efficient scan",
            "提示 2: Up-sweep 和 Down-sweep 两个阶段",
            "提示 3: 处理 power-of-2 大小"
        },
        "solutions/10_algorithms/01_prefix_sum.cu"
    });

    exercises_.push_back({
        102, "10_algorithms", "bitonic_sort",
        "exercises/10_algorithms/02_bitonic_sort.cu",
        "Bitonic Sort：并行双调排序",
        {
            "提示 1: 理解 bitonic 序列性质",
            "提示 2: 递归地合并 bitonic 序列",
            "提示 3: 使用位操作优化"
        },
        "solutions/10_algorithms/02_bitonic_sort.cu"
    });

    exercises_.push_back({
        103, "10_algorithms", "radix_sort",
        "exercises/10_algorithms/03_radix_sort.cu",
        "基数排序：实现并行基数排序",
        {
            "提示 1: 按位处理",
            "提示 2: 使用 scan 计算位置",
            "提示 3: 保持稳定性"
        },
        "solutions/10_algorithms/03_radix_sort.cu"
    });

    exercises_.push_back({
        104, "10_algorithms", "merge_sort",
        "exercises/10_algorithms/04_merge_sort.cu",
        "并行归并排序",
        {
            "提示 1: Bottom-Up Merge Sort",
            "提示 2: 每层归并独立并行",
            "提示 3: 双缓冲技术"
        },
        "solutions/10_algorithms/04_merge_sort.cu"
    });

    exercises_.push_back({
        105, "10_algorithms", "histogram",
        "exercises/10_algorithms/05_histogram.cu",
        "并行直方图统计",
        {
            "提示 1: 使用原子操作",
            "提示 2: Shared Memory 私有化减少冲突",
            "提示 3: 最后合并到全局直方图"
        },
        "solutions/10_algorithms/05_histogram.cu"
    });

    exercises_.push_back({
        106, "10_algorithms", "parallel_reduction",
        "exercises/10_algorithms/06_parallel_reduction.cu",
        "高级并行归约优化",
        {
            "提示 1: Warp Shuffle 归约",
            "提示 2: Sequential addressing",
            "提示 3: 完全展开循环"
        },
        "solutions/10_algorithms/06_parallel_reduction.cu"
    });
}

void ExerciseManager::add_image_processing_exercises() {
    // 练习 111-112: 图像处理
    exercises_.push_back({
        111, "11_image_processing", "convolution",
        "exercises/11_image_processing/01_convolution.cu",
        "2D 卷积：实现图像卷积操作",
        {
            "提示 1: 使用 tiling 和共享内存",
            "提示 2: 处理 halo 区域",
            "提示 3: 常量内存存储卷积核"
        },
        "solutions/11_image_processing/01_convolution.cu"
    });

    exercises_.push_back({
        112, "11_image_processing", "gaussian_blur",
        "exercises/11_image_processing/02_gaussian_blur.cu",
        "高斯模糊：可分离滤波器优化",
        {
            "提示 1: 利用可分离性",
            "提示 2: 先行后列两趟卷积",
            "提示 3: 比 2D 卷积快 O(kernel_size)倍"
        },
        "solutions/11_image_processing/02_gaussian_blur.cu"
    });

    exercises_.push_back({
        113, "11_image_processing", "gaussian_blur",
        "exercises/11_image_processing/03_gaussian_blur.cu",
        "高斯模糊：高效实现",
        {
            "提示 1: 使用可分离卷积",
            "提示 2: Shared Memory 缓存行列",
            "提示 3: 处理边界条件"
        },
        "solutions/11_image_processing/03_gaussian_blur.cu"
    });

    exercises_.push_back({
        114, "11_image_processing", "sobel",
        "exercises/11_image_processing/04_sobel.cu",
        "Sobel 边缘检测",
        {
            "提示 1: 计算 x 和 y 方向梯度",
            "提示 2: 幅值 = sqrt(Gx^2 + Gy^2)",
            "提示 3: 可融合为单个 kernel"
        },
        "solutions/11_image_processing/04_sobel.cu"
    });

    exercises_.push_back({
        115, "11_image_processing", "pyramid",
        "exercises/11_image_processing/05_pyramid.cu",
        "图像金字塔：多尺度表示",
        {
            "提示 1: Gaussian Pyramid 下采样",
            "提示 2: Laplacian Pyramid 带通滤波",
            "提示 3: 应用于图像融合、特征检测"
        },
        "solutions/11_image_processing/05_pyramid.cu"
    });
}

void ExerciseManager::add_deep_learning_exercises() {
    // 练习 121-125: 深度学习
    exercises_.push_back({
        121, "12_deep_learning", "relu_activation",
        "exercises/12_deep_learning/01_relu_activation.cu",
        "ReLU 激活函数：forward 和 backward",
        {
            "提示 1: forward: max(0, x)",
            "提示 2: backward: x > 0 ? 1 : 0",
            "提示 3: 可以融合前向和反向"
        },
        "solutions/12_deep_learning/01_relu_activation.cu"
    });

    exercises_.push_back({
        122, "12_deep_learning", "fully_connected",
        "exercises/12_deep_learning/02_fully_connected.cu",
        "全连接层：矩阵乘法 + bias",
        {
            "提示 1: Y = XW + b",
            "提示 2: 使用 tiling 优化",
            "提示 3: 反向传播需要三个梯度"
        },
        "solutions/12_deep_learning/02_fully_connected.cu"
    });

    exercises_.push_back({
        123, "12_deep_learning", "softmax",
        "exercises/12_deep_learning/03_softmax.cu",
        "Softmax 层：数值稳定的实现",
        {
            "提示 1: 使用 max trick 避免溢出",
            "提示 2: softmax(x) = softmax(x - max(x))",
            "提示 3: 反向传播公式特殊"
        },
        "solutions/12_deep_learning/03_softmax.cu"
    });

    exercises_.push_back({
        124, "12_deep_learning", "batchnorm",
        "exercises/12_deep_learning/04_batchnorm.cu",
        "Batch Normalization：归一化和缩放",
        {
            "提示 1: 计算 mean 和 variance",
            "提示 2: 归一化: (x - mean) / sqrt(var + eps)",
            "提示 3: 应用 gamma 和 beta 参数"
        },
        "solutions/12_deep_learning/04_batchnorm.cu"
    });

    exercises_.push_back({
        125, "12_deep_learning", "conv2d",
        "exercises/12_deep_learning/05_conv2d.cu",
        "2D 卷积层：深度学习卷积实现",
        {
            "提示 1: 处理 padding 和 stride",
            "提示 2: 使用 shared memory 优化",
            "提示 3: 考虑 im2col + GEMM 方法"
        },
        "solutions/12_deep_learning/05_conv2d.cu"
    });
}

void ExerciseManager::add_scientific_computing_exercises() {
    // 练习 131: 科学计算
    exercises_.push_back({
        131, "13_scientific_computing", "sparse_matrix",
        "exercises/13_scientific_computing/01_sparse_matrix.cu",
        "稀疏矩阵乘法：CSR 格式 SpMV",
        {
            "提示 1: 理解 CSR 存储格式",
            "提示 2: 每个线程处理一行",
            "提示 3: 不规则访问模式"
        },
        "solutions/13_scientific_computing/01_sparse_matrix.cu"
    });

    exercises_.push_back({
        132, "13_scientific_computing", "monte_carlo",
        "exercises/13_scientific_computing/02_monte_carlo.cu",
        "蒙特卡洛模拟：并行随机采样",
        {
            "提示 1: 使用 cuRAND 生成随机数",
            "提示 2: 每个线程独立采样",
            "提示 3: 归约统计结果"
        },
        "solutions/13_scientific_computing/02_monte_carlo.cu"
    });

    exercises_.push_back({
        133, "13_scientific_computing", "heat_equation",
        "exercises/13_scientific_computing/03_heat_equation.cu",
        "热传导方程：有限差分法",
        {
            "提示 1: 2D Jacobi/Gauss-Seidel 迭代",
            "提示 2: Stencil 计算",
            "提示 3: 双缓冲技术"
        },
        "solutions/13_scientific_computing/03_heat_equation.cu"
    });

    exercises_.push_back({
        134, "13_scientific_computing", "fluid_dynamics",
        "exercises/13_scientific_computing/04_fluid_dynamics.cu",
        "流体动力学：Lattice Boltzmann Method",
        {
            "提示 1: LBM D2Q9 模型",
            "提示 2: Collision 和 Streaming",
            "提示 3: 边界条件处理"
        },
        "solutions/13_scientific_computing/04_fluid_dynamics.cu"
    });
}

void ExerciseManager::add_multi_gpu_exercises() {
    // 练习 141-143: Multi-GPU
    exercises_.push_back({
        141, "14_multi_gpu", "device_query",
        "exercises/14_multi_gpu/01_device_query.cu",
        "Multi-GPU 设备查询和 P2P 检测",
        {
            "提示 1: cudaGetDeviceCount() 获取数量",
            "提示 2: cudaDeviceCanAccessPeer() 检查 P2P",
            "提示 3: 遍历所有设备"
        },
        "solutions/14_multi_gpu/01_device_query.cu"
    });

    exercises_.push_back({
        142, "14_multi_gpu", "data_parallel",
        "exercises/14_multi_gpu/02_data_parallel.cu",
        "数据并行：在多个 GPU 上分布计算",
        {
            "提示 1: 均分数据到各 GPU",
            "提示 2: cudaSetDevice() 切换设备",
            "提示 3: 并发启动所有 GPU"
        },
        "solutions/14_multi_gpu/02_data_parallel.cu"
    });

    exercises_.push_back({
        143, "14_multi_gpu", "p2p_copy",
        "exercises/14_multi_gpu/03_p2p_copy.cu",
        "P2P 数据传输：GPU 间直接通信",
        {
            "提示 1: cudaDeviceEnablePeerAccess() 启用",
            "提示 2: cudaMemcpyPeer() 直接传输",
            "提示 3: 比通过主机快得多"
        },
        "solutions/14_multi_gpu/03_p2p_copy.cu"
    });
}

void ExerciseManager::add_tensor_cores_exercises() {
    // 练习 151-153: Tensor Cores
    exercises_.push_back({
        151, "15_tensor_cores", "wmma_basics",
        "exercises/15_tensor_cores/01_wmma_basics.cu",
        "Tensor Core 基础：使用 WMMA API",
        {
            "提示 1: 需要 Compute Capability >= 7.0",
            "提示 2: 使用 nvcuda::wmma namespace",
            "提示 3: fragment -> load -> mma -> store"
        },
        "solutions/15_tensor_cores/01_wmma_basics.cu"
    });

    exercises_.push_back({
        152, "15_tensor_cores", "mixed_precision",
        "exercises/15_tensor_cores/02_mixed_precision.cu",
        "混合精度：FP16/FP32 加速训练",
        {
            "提示 1: 输入使用 half (FP16)",
            "提示 2: 累加使用 float (FP32)",
            "提示 3: 平衡速度和精度"
        },
        "solutions/15_tensor_cores/02_mixed_precision.cu"
    });

    exercises_.push_back({
        153, "15_tensor_cores", "gemm_optimization",
        "exercises/15_tensor_cores/03_gemm_optimization.cu",
        "GEMM 优化：高性能矩阵乘法",
        {
            "提示 1: 优化 tile 大小",
            "提示 2: 调整 warp 布局",
            "提示 3: 最大化 Tensor Core 利用率"
        },
        "solutions/15_tensor_cores/03_gemm_optimization.cu"
    });
}

void ExerciseManager::add_cuda_graphs_exercises() {
    // 练习 161-162: CUDA Graphs
    exercises_.push_back({
        161, "16_cuda_graphs", "graph_basics",
        "exercises/16_cuda_graphs/01_graph_basics.cu",
        "CUDA Graphs 基础：减少启动开销",
        {
            "提示 1: 使用 Stream Capture 创建 graph",
            "提示 2: cudaGraphInstantiate() 实例化",
            "提示 3: cudaGraphLaunch() 重复执行"
        },
        "solutions/16_cuda_graphs/01_graph_basics.cu"
    });

    exercises_.push_back({
        162, "16_cuda_graphs", "graph_update",
        "exercises/16_cuda_graphs/02_graph_update.cu",
        "Graph 更新：动态修改参数",
        {
            "提示 1: 避免重新创建 graph",
            "提示 2: cudaGraphExecKernelNodeSetParams()",
            "提示 3: 更新比重建快得多"
        },
        "solutions/16_cuda_graphs/02_graph_update.cu"
    });
}

void ExerciseManager::add_cooperative_groups_exercises() {
    // 练习 171-173: Cooperative Groups
    exercises_.push_back({
        171, "17_cooperative_groups", "thread_block_groups",
        "exercises/17_cooperative_groups/01_thread_block_groups.cu",
        "Thread Block Groups：改进线程协作",
        {
            "提示 1: cg::this_thread_block()",
            "提示 2: 使用 block.sync() 替代 __syncthreads()",
            "提示 3: 更灵活的同步模式"
        },
        "solutions/17_cooperative_groups/01_thread_block_groups.cu"
    });

    exercises_.push_back({
        172, "17_cooperative_groups", "warp_level",
        "exercises/17_cooperative_groups/02_warp_level.cu",
        "Warp-Level Primitives：warp 级操作",
        {
            "提示 1: cg::coalesced_threads()",
            "提示 2: cg::tiled_partition<N>()",
            "提示 3: 使用 shuffle 进行 warp reduction"
        },
        "solutions/17_cooperative_groups/02_warp_level.cu"
    });

    exercises_.push_back({
        173, "17_cooperative_groups", "grid_sync",
        "exercises/17_cooperative_groups/03_grid_sync.cu",
        "Grid-Wide Sync：跨 block 同步",
        {
            "提示 1: cg::this_grid()",
            "提示 2: 需要 cooperativeLaunch 支持",
            "提示 3: cudaLaunchCooperativeKernel()"
        },
        "solutions/17_cooperative_groups/03_grid_sync.cu"
    });
}

void ExerciseManager::add_profiling_debugging_exercises() {
    // 练习 181-185: 性能分析与调试
    exercises_.push_back({
        181, "18_profiling_debugging", "nsight_systems",
        "exercises/18_profiling_debugging/01_nsight_systems.cu",
        "Nsight Systems：系统级性能分析",
        {
            "提示 1: nsys profile --stats=true ./program",
            "提示 2: 观察 CPU/GPU 时间线",
            "提示 3: 识别内存传输和 kernel 执行瓶颈"
        },
        "solutions/18_profiling_debugging/01_nsight_systems.cu"
    });

    exercises_.push_back({
        182, "18_profiling_debugging", "nsight_compute",
        "exercises/18_profiling_debugging/02_nsight_compute.cu",
        "Nsight Compute：Kernel 级性能分析",
        {
            "提示 1: ncu --set full -o profile ./program",
            "提示 2: 分析内存带宽和计算吞吐量",
            "提示 3: 查看 Warp Stall Reasons"
        },
        "solutions/18_profiling_debugging/02_nsight_compute.cu"
    });

    exercises_.push_back({
        183, "18_profiling_debugging", "compute_sanitizer",
        "exercises/18_profiling_debugging/03_compute_sanitizer.cu",
        "Compute Sanitizer：内存错误检测",
        {
            "提示 1: compute-sanitizer --tool memcheck",
            "提示 2: 检测越界访问和数据竞争",
            "提示 3: 使用 -g -G 编译获得详细信息"
        },
        "solutions/18_profiling_debugging/03_compute_sanitizer.cu"
    });

    exercises_.push_back({
        184, "18_profiling_debugging", "cuda_gdb",
        "exercises/18_profiling_debugging/04_cuda_gdb.cu",
        "cuda-gdb：CUDA 调试器使用",
        {
            "提示 1: cuda-gdb ./program",
            "提示 2: break kernel_name 设置断点",
            "提示 3: cuda thread 查看线程信息"
        },
        "solutions/18_profiling_debugging/04_cuda_gdb.cu"
    });

    exercises_.push_back({
        185, "18_profiling_debugging", "performance_metrics",
        "exercises/18_profiling_debugging/05_performance_metrics.cu",
        "性能指标：解读和优化关键指标",
        {
            "提示 1: 计算理论带宽和计算峰值",
            "提示 2: 测量实际性能",
            "提示 3: 分析占用率和优化空间"
        },
        "solutions/18_profiling_debugging/05_performance_metrics.cu"
    });
}

void ExerciseManager::add_cuda_libraries_exercises() {
    // 练习 191-194: CUDA 库
    exercises_.push_back({
        191, "19_cuda_libraries", "cublas_basics",
        "exercises/19_cuda_libraries/01_cublas_basics.cu",
        "cuBLAS 基础：矩阵乘法加速",
        {
            "提示 1: cublasCreate() 创建 handle",
            "提示 2: cublasSgemm() 执行矩阵乘法",
            "提示 3: 注意列主序和行主序的转换"
        },
        "solutions/19_cuda_libraries/01_cublas_basics.cu"
    });

    exercises_.push_back({
        192, "19_cuda_libraries", "thrust_basics",
        "exercises/19_cuda_libraries/02_thrust_basics.cu",
        "Thrust 基础：STL 风格的 GPU 编程",
        {
            "提示 1: thrust::device_vector 管理 GPU 内存",
            "提示 2: thrust::reduce/sort/transform 并行算法",
            "提示 3: 支持自定义函数对象和 lambda"
        },
        "solutions/19_cuda_libraries/02_thrust_basics.cu"
    });

    exercises_.push_back({
        193, "19_cuda_libraries", "cufft_basics",
        "exercises/19_cuda_libraries/03_cufft_basics.cu",
        "cuFFT 基础：快速傅里叶变换",
        {
            "提示 1: cufftPlan1d() 创建 FFT 计划",
            "提示 2: cufftExecC2C() 执行正向/逆向变换",
            "提示 3: 逆变换需要手动归一化"
        },
        "solutions/19_cuda_libraries/03_cufft_basics.cu"
    });

    exercises_.push_back({
        194, "19_cuda_libraries", "cub_basics",
        "exercises/19_cuda_libraries/04_cub_basics.cu",
        "CUB 基础：高性能 Primitives",
        {
            "提示 1: cub::BlockReduce 用于 block 级别",
            "提示 2: cub::DeviceScan/DeviceRadixSort 设备级",
            "提示 3: 需要分配临时存储空间"
        },
        "solutions/19_cuda_libraries/04_cub_basics.cu"
    });
}

void ExerciseManager::add_dynamic_parallelism_exercises() {
    // 练习 201-203: 动态并行
    exercises_.push_back({
        201, "20_dynamic_parallelism", "nested_kernels",
        "exercises/20_dynamic_parallelism/01_nested_kernels.cu",
        "嵌套 Kernel：在 GPU 上启动 Kernel",
        {
            "提示 1: 需要 Compute Capability >= 3.5",
            "提示 2: 使用 -rdc=true 编译",
            "提示 3: cudaDeviceSynchronize() 在 device 端使用"
        },
        "solutions/20_dynamic_parallelism/01_nested_kernels.cu"
    });

    exercises_.push_back({
        202, "20_dynamic_parallelism", "recursive_quicksort",
        "exercises/20_dynamic_parallelism/02_recursive_quicksort.cu",
        "递归快速排序：GPU 端递归算法",
        {
            "提示 1: 控制递归深度避免栈溢出",
            "提示 2: partition 在 device 端实现",
            "提示 3: 每次递归启动两个子 kernel"
        },
        "solutions/20_dynamic_parallelism/02_recursive_quicksort.cu"
    });

    exercises_.push_back({
        203, "20_dynamic_parallelism", "adaptive_grid",
        "exercises/20_dynamic_parallelism/03_adaptive_grid.cu",
        "自适应网格：动态调整并行粒度",
        {
            "提示 1: 根据计算复杂度决定是否细分",
            "提示 2: 递归细分为4个子网格",
            "提示 3: 适用于光线追踪、树遍历等场景"
        },
        "solutions/20_dynamic_parallelism/03_adaptive_grid.cu"
    });
}

void ExerciseManager::add_projects_exercises() {
    // 练习 211-212: 综合项目
    exercises_.push_back({
        211, "21_projects", "mnist_inference",
        "exercises/21_projects/01_mnist_inference.cu",
        "综合项目：MNIST 推理引擎",
        {
            "提示 1: 使用 cuBLAS 加速矩阵乘法",
            "提示 2: Kernel fusion 减少内存访问",
            "提示 3: 批量处理提高吞吐量"
        },
        "solutions/21_projects/01_mnist_inference.cu"
    });

    exercises_.push_back({
        212, "21_projects", "nbody_simulation",
        "exercises/21_projects/02_nbody_simulation.cu",
        "综合项目：N-Body 引力模拟",
        {
            "提示 1: Shared Memory 分块计算",
            "提示 2: Velocity Verlet 时间积分",
            "提示 3: rsqrtf() 快速平方根倒数"
        },
        "solutions/21_projects/02_nbody_simulation.cu"
    });
}

void ExerciseManager::add_unified_memory_exercises() {
    // 练习 221-224: 统一内存
    exercises_.push_back({
        221, "22_unified_memory", "um_basics",
        "exercises/22_unified_memory/01_um_basics.cu",
        "Unified Memory 基础：简化内存管理",
        {
            "提示 1: cudaMallocManaged() 分配统一内存",
            "提示 2: CPU 和 GPU 可直接访问同一指针",
            "提示 3: 自动处理数据迁移"
        },
        "solutions/22_unified_memory/01_um_basics.cu"
    });

    exercises_.push_back({
        222, "22_unified_memory", "um_prefetch",
        "exercises/22_unified_memory/02_um_prefetch.cu",
        "Unified Memory 预取：性能优化",
        {
            "提示 1: cudaMemPrefetchAsync() 预取数据",
            "提示 2: cudaMemAdvise() 设置访问提示",
            "提示 3: 减少页面故障延迟"
        },
        "solutions/22_unified_memory/02_um_prefetch.cu"
    });

    exercises_.push_back({
        223, "22_unified_memory", "um_concurrent",
        "exercises/22_unified_memory/03_um_concurrent.cu",
        "Unified Memory 并发访问",
        {
            "提示 1: cudaStreamAttachMemAsync() 管理归属",
            "提示 2: 多 stream 并发处理不同分区",
            "提示 3: 确保 CPU-GPU 同步"
        },
        "solutions/22_unified_memory/03_um_concurrent.cu"
    });

    exercises_.push_back({
        224, "22_unified_memory", "um_performance",
        "exercises/22_unified_memory/04_um_performance.cu",
        "Unified Memory 性能分析",
        {
            "提示 1: 对比传统方式和 UM",
            "提示 2: 分析页面故障开销",
            "提示 3: 优化 UM 使用策略"
        },
        "solutions/22_unified_memory/04_um_performance.cu"
    });
}

void ExerciseManager::add_warp_primitives_exercises() {
    // 练习 231-234: Warp 级别编程
    exercises_.push_back({
        231, "23_warp_primitives", "warp_shuffle",
        "exercises/23_warp_primitives/01_warp_shuffle.cu",
        "Warp Shuffle 操作：寄存器间通信",
        {
            "提示 1: __shfl_sync/__shfl_down_sync 等函数",
            "提示 2: 无需 Shared Memory 的归约",
            "提示 3: 低延迟，高效率"
        },
        "solutions/23_warp_primitives/01_warp_shuffle.cu"
    });

    exercises_.push_back({
        232, "23_warp_primitives", "warp_vote",
        "exercises/23_warp_primitives/02_warp_vote.cu",
        "Warp Vote 函数：条件判断",
        {
            "提示 1: __all_sync/__any_sync/__ballot_sync",
            "提示 2: Warp 级别分支优化",
            "提示 3: 数据过滤和压缩"
        },
        "solutions/23_warp_primitives/02_warp_vote.cu"
    });

    exercises_.push_back({
        233, "23_warp_primitives", "warp_match",
        "exercises/23_warp_primitives/03_warp_match.cu",
        "Warp Match 函数：数据分组",
        {
            "提示 1: __match_any_sync/__match_all_sync",
            "提示 2: 需要 Volta (SM 7.0) 及以上",
            "提示 3: 去重、直方图、Group By"
        },
        "solutions/23_warp_primitives/03_warp_match.cu"
    });

    exercises_.push_back({
        234, "23_warp_primitives", "warp_matrix",
        "exercises/23_warp_primitives/04_warp_matrix.cu",
        "Warp 级别矩阵操作",
        {
            "提示 1: Warp Shuffle 实现小矩阵运算",
            "提示 2: 为 Tensor Core 打基础",
            "提示 3: 协作计算模式"
        },
        "solutions/23_warp_primitives/04_warp_matrix.cu"
    });
}

void ExerciseManager::add_graph_algorithms_exercises() {
    // 练习 241-244: 图算法
    exercises_.push_back({
        241, "24_graph_algorithms", "bfs",
        "exercises/24_graph_algorithms/01_bfs.cu",
        "并行广度优先搜索 (BFS)",
        {
            "提示 1: Level Synchronous 方法",
            "提示 2: CSR 格式存储图",
            "提示 3: Frontier 管理"
        },
        "solutions/24_graph_algorithms/01_bfs.cu"
    });

    exercises_.push_back({
        242, "24_graph_algorithms", "pagerank",
        "exercises/24_graph_algorithms/02_pagerank.cu",
        "GPU PageRank 算法",
        {
            "提示 1: 迭代更新 rank 值",
            "提示 2: 处理 dangling nodes",
            "提示 3: 收敛判断"
        },
        "solutions/24_graph_algorithms/02_pagerank.cu"
    });

    exercises_.push_back({
        243, "24_graph_algorithms", "shortest_path",
        "exercises/24_graph_algorithms/03_shortest_path.cu",
        "最短路径算法 (SSSP)",
        {
            "提示 1: Bellman-Ford 算法",
            "提示 2: 边松弛操作并行化",
            "提示 3: 使用原子操作更新距离"
        },
        "solutions/24_graph_algorithms/03_shortest_path.cu"
    });

    exercises_.push_back({
        244, "24_graph_algorithms", "triangle_counting",
        "exercises/24_graph_algorithms/04_triangle_counting.cu",
        "三角形计数：社交网络分析",
        {
            "提示 1: 查找共同邻居",
            "提示 2: 归并法或哈希法",
            "提示 3: 避免重复计数"
        },
        "solutions/24_graph_algorithms/04_triangle_counting.cu"
    });
}

void ExerciseManager::add_sparse_matrices_exercises() {
    // 练习 251-253: 稀疏矩阵
    exercises_.push_back({
        251, "25_sparse_matrices", "spmv",
        "exercises/25_sparse_matrices/01_spmv.cu",
        "稀疏矩阵-向量乘法 (SpMV)",
        {
            "提示 1: CSR 格式实现",
            "提示 2: 每个线程处理一行",
            "提示 3: 内存访问模式优化"
        },
        "solutions/25_sparse_matrices/01_spmv.cu"
    });

    exercises_.push_back({
        252, "25_sparse_matrices", "coo_to_csr",
        "exercises/25_sparse_matrices/02_coo_to_csr.cu",
        "COO 到 CSR 格式转换",
        {
            "提示 1: 排序 COO 三元组",
            "提示 2: 计算行偏移",
            "提示 3: 使用 Thrust 或 CUB"
        },
        "solutions/25_sparse_matrices/02_coo_to_csr.cu"
    });

    exercises_.push_back({
        253, "25_sparse_matrices", "cusparse",
        "exercises/25_sparse_matrices/03_cusparse.cu",
        "cuSPARSE 库使用",
        {
            "提示 1: cusparseCreate() 创建 handle",
            "提示 2: cusparseSpMV() 执行 SpMV",
            "提示 3: 支持多种格式"
        },
        "solutions/25_sparse_matrices/03_cusparse.cu"
    });
}

void ExerciseManager::add_molecular_dynamics_exercises() {
    // 练习 261-263: 分子动力学
    exercises_.push_back({
        261, "26_molecular_dynamics", "lennard_jones",
        "exercises/26_molecular_dynamics/01_lennard_jones.cu",
        "Lennard-Jones 势能计算",
        {
            "提示 1: 计算粒子间相互作用力",
            "提示 2: 使用 Shared Memory 优化",
            "提示 3: 对称性减少计算量"
        },
        "solutions/26_molecular_dynamics/01_lennard_jones.cu"
    });

    exercises_.push_back({
        262, "26_molecular_dynamics", "verlet_integration",
        "exercises/26_molecular_dynamics/02_verlet_integration.cu",
        "Verlet 积分法：时间步进",
        {
            "提示 1: 更新位置和速度",
            "提示 2: Velocity Verlet 算法",
            "提示 3: 数值稳定性"
        },
        "solutions/26_molecular_dynamics/02_verlet_integration.cu"
    });

    exercises_.push_back({
        263, "26_molecular_dynamics", "neighbor_list",
        "exercises/26_molecular_dynamics/03_neighbor_list.cu",
        "邻居列表优化：加速力计算",
        {
            "提示 1: Cell List 或 Verlet List",
            "提示 2: 空间划分加速搜索",
            "提示 3: 周期性更新列表"
        },
        "solutions/26_molecular_dynamics/03_neighbor_list.cu"
    });
}

void ExerciseManager::add_ray_tracing_exercises() {
    // 练习 271-274: 光线追踪
    exercises_.push_back({
        271, "27_ray_tracing", "ray_sphere",
        "exercises/27_ray_tracing/01_ray_sphere.cu",
        "光线-球体相交测试",
        {
            "提示 1: 求解二次方程",
            "提示 2: 判别式检查",
            "提示 3: 返回最近交点"
        },
        "solutions/27_ray_tracing/01_ray_sphere.cu"
    });

    exercises_.push_back({
        272, "27_ray_tracing", "simple_raytracer",
        "exercises/27_ray_tracing/02_simple_raytracer.cu",
        "简单光线追踪器",
        {
            "提示 1: 为每个像素生成光线",
            "提示 2: 遍历场景求交",
            "提示 3: 简单光照计算"
        },
        "solutions/27_ray_tracing/02_simple_raytracer.cu"
    });

    exercises_.push_back({
        273, "27_ray_tracing", "bvh",
        "exercises/27_ray_tracing/03_bvh.cu",
        "BVH 加速结构",
        {
            "提示 1: 构建层次包围盒",
            "提示 2: 递归遍历树",
            "提示 3: SAH 启发式"
        },
        "solutions/27_ray_tracing/03_bvh.cu"
    });

    exercises_.push_back({
        274, "27_ray_tracing", "path_tracing",
        "exercises/27_ray_tracing/04_path_tracing.cu",
        "路径追踪：全局光照",
        {
            "提示 1: 蒙特卡洛采样",
            "提示 2: 俄罗斯轮盘赌终止",
            "提示 3: 多重重要性采样"
        },
        "solutions/27_ray_tracing/04_path_tracing.cu"
    });
}

void ExerciseManager::add_video_processing_exercises() {
    // 练习 281-283: 视频处理
    exercises_.push_back({
        281, "28_video_processing", "rgb_to_yuv",
        "exercises/28_video_processing/01_rgb_to_yuv.cu",
        "RGB 到 YUV 颜色空间转换",
        {
            "提示 1: 线性变换矩阵",
            "提示 2: 每个像素独立处理",
            "提示 3: YUV420 格式下采样"
        },
        "solutions/28_video_processing/01_rgb_to_yuv.cu"
    });

    exercises_.push_back({
        282, "28_video_processing", "motion_estimation",
        "exercises/28_video_processing/02_motion_estimation.cu",
        "运动估计 (Block Matching)",
        {
            "提示 1: SAD/SSD 匹配度量",
            "提示 2: 搜索范围和步长",
            "提示 3: 多级搜索优化"
        },
        "solutions/28_video_processing/02_motion_estimation.cu"
    });

    exercises_.push_back({
        283, "28_video_processing", "temporal_filter",
        "exercises/28_video_processing/03_temporal_filter.cu",
        "时域滤波：视频降噪",
        {
            "提示 1: 帧间加权平均",
            "提示 2: 运动补偿",
            "提示 3: 自适应权重"
        },
        "solutions/28_video_processing/03_temporal_filter.cu"
    });
}

void ExerciseManager::add_ml_operators_exercises() {
    // 练习 291-295: 机器学习算子
    exercises_.push_back({
        291, "29_ml_operators", "attention",
        "exercises/29_ml_operators/01_attention.cu",
        "Attention 机制实现",
        {
            "提示 1: Scaled Dot-Product Attention",
            "提示 2: softmax(QK^T/sqrt(d_k))V",
            "提示 3: 使用 cuBLAS 加速矩阵乘法"
        },
        "solutions/29_ml_operators/01_attention.cu"
    });

    exercises_.push_back({
        292, "29_ml_operators", "layer_norm",
        "exercises/29_ml_operators/02_layer_norm.cu",
        "Layer Normalization",
        {
            "提示 1: 计算均值和方差",
            "提示 2: 归一化: (x - mean) / sqrt(var + eps)",
            "提示 3: 应用 gamma 和 beta 参数"
        },
        "solutions/29_ml_operators/02_layer_norm.cu"
    });

    exercises_.push_back({
        293, "29_ml_operators", "gelu",
        "exercises/29_ml_operators/03_gelu.cu",
        "GELU 激活函数",
        {
            "提示 1: GELU(x) = x * Φ(x)",
            "提示 2: 使用 tanh 近似",
            "提示 3: 融合操作提高效率"
        },
        "solutions/29_ml_operators/03_gelu.cu"
    });

    exercises_.push_back({
        294, "29_ml_operators", "flash_attention",
        "exercises/29_ml_operators/04_flash_attention.cu",
        "Flash Attention 实现",
        {
            "提示 1: 分块计算减少 HBM 访问",
            "提示 2: Online softmax 算法",
            "提示 3: 需要深入理解论文"
        },
        "solutions/29_ml_operators/04_flash_attention.cu"
    });

    exercises_.push_back({
        295, "29_ml_operators", "group_norm",
        "exercises/29_ml_operators/05_group_norm.cu",
        "Group Normalization",
        {
            "提示 1: 将 channels 分组",
            "提示 2: 每组独立归一化",
            "提示 3: 适用于小 batch size"
        },
        "solutions/29_ml_operators/05_group_norm.cu"
    });
}

