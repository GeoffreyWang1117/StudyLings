# 练习指南

## 练习结构

每个练习文件包含:

1. **头部注释**: 练习编号、标题和目标
2. **任务列表**: 需要完成的具体任务
3. **TODO 标记**: 需要你填写代码的地方
4. **提示注释**: 指导你如何完成任务
5. **测试代码**: 自动验证你的实现
6. **I AM NOT DONE**: 标记练习未完成

## 完成练习的标志

要让系统识别练习已完成，你需要:

1. ✅ 代码能够编译通过
2. ✅ 所有测试用例通过
3. ✅ 程序输出包含 "TEST_PASSED"

## 学习路径详解

### 阶段 1: CUDA 基础 (练习 1-5)

**目标**: 了解 CUDA 编程的基本概念

- **练习 1**: Hello CUDA - 你的第一个 GPU 程序
- **练习 2**: 设备查询 - 了解你的 GPU
- **练习 3**: 错误处理 - 正确处理 CUDA 错误

**关键概念**:
- `__global__` 关键字
- kernel 调用语法 `<<<blocks, threads>>>`
- `cudaDeviceSynchronize()`
- CUDA 错误检查

### 阶段 2: Kernel 函数 (练习 6-15)

**目标**: 掌握编写和调用 kernel 函数

- **练习 6**: 向量加法 - 基本并行计算
- **练习 7**: 向量缩放 - 处理边界条件

**关键概念**:
- 线程索引 `threadIdx.x`
- 内存分配 `cudaMalloc`
- 内存拷贝 `cudaMemcpy`
- 边界检查

### 阶段 3: 线程组织 (练习 16-25)

**目标**: 理解 CUDA 的线程层次结构

- **练习 16**: 线程索引计算
- **练习 17**: 二维线程网格

**关键概念**:
- `blockIdx`, `blockDim`, `threadIdx`
- 全局索引计算
- 二维和三维线程网格
- Grid 大小计算

### 阶段 4: 内存管理 (练习 26-40)

**目标**: 掌握 CUDA 内存模型

- **练习 26**: 设备内存分配
- **练习 27**: 内存拷贝
- 统一内存
- 固定内存

**关键概念**:
- 全局内存
- 常量内存
- 纹理内存
- 统一内存 `cudaMallocManaged`

### 阶段 5: 共享内存 (练习 41-55)

**目标**: 使用共享内存优化性能

- **练习 41**: 共享内存基础
- Bank 冲突
- 矩阵转置优化

**关键概念**:
- `__shared__` 关键字
- Block 内通信
- Bank 冲突避免
- 性能优化

### 阶段 6: 同步与通信 (练习 56-65)

**目标**: 正确使用同步机制

- **练习 56**: `__syncthreads()`
- 原子操作
- Warp 级原语

**关键概念**:
- Block 级同步
- 原子操作
- Warp shuffle
- 协作组

### 阶段 7: 性能优化 (练习 66-80)

**目标**: 编写高性能 CUDA 代码

- **练习 66**: 内存合并访问
- 占用率优化
- 指令级优化

**关键概念**:
- 内存访问模式
- 占用率
- 分支分化
- 循环展开

### 阶段 8: CUDA 流 (练习 81-90)

**目标**: 使用流实现并发

- **练习 81**: 基础流操作
- 流同步
- 事件计时

**关键概念**:
- `cudaStream_t`
- 异步操作
- 流优先级
- 事件和计时

### 阶段 9: 高级特性 (练习 91-100)

**目标**: 掌握高级 CUDA 特性

- **练习 91**: 归约操作
- 扫描算法
- 动态并行
- 协作组

**关键概念**:
- 并行模式
- 动态并行
- 协作组
- Tensor Cores (if available)

### 阶段 10-14: 高级算法与应用 (练习 101-143)

**目标**: 应用 CUDA 解决实际问题

**10. 并行算法** (101-103):
- 前缀和 (Scan)
- Bitonic 排序
- 基数排序

**11. 图像处理** (111-112):
- 2D 卷积
- 高斯模糊

**12. 深度学习** (121-125):
- ReLU 激活函数
- 全连接层
- Softmax
- Batch Normalization
- 2D 卷积层

**13. 科学计算** (131):
- 稀疏矩阵 (CSR 格式)

**14. Multi-GPU** (141-143):
- 设备查询与 P2P
- 数据并行
- GPU 间通信

### 阶段 15-17: 现代 CUDA 特性 (练习 151-173)

**目标**: 掌握最新的 CUDA 编程特性

**15. Tensor Cores** (151-153):
- WMMA API 基础
- 混合精度训练 (FP16/FP32)
- 优化的 GEMM 实现
- **硬件要求**: Compute Capability >= 7.0 (Volta+)

**16. CUDA Graphs** (161-162):
- Stream Capture
- Graph 执行与更新
- 减少 kernel 启动开销

**17. Cooperative Groups** (171-173):
- Thread Block Groups
- Warp-level Primitives
- Grid-wide Synchronization
- **硬件要求**: CC >= 6.0

### 阶段 18: 性能分析与调试 (练习 181-185)

**目标**: 使用专业工具分析和优化代码

**工具实战**:
- **Nsight Systems**: 系统级性能分析
- **Nsight Compute**: Kernel 级深度分析
- **Compute Sanitizer**: 内存错误检测
- **cuda-gdb**: CUDA 调试器
- **性能指标**: 带宽、吞吐量、占用率

**关键技能**:
- 识别性能瓶颈
- 理解 warp stall reasons
- 优化内存访问模式
- 提高计算单元利用率

### 阶段 19: CUDA 库 (练习 191-194)

**目标**: 使用高性能 CUDA 库加速开发

**19. CUDA 库精通**:
- **cuBLAS**: 线性代数加速
  - 矩阵乘法 (GEMM)
  - 向量运算
  - 比手写 kernel 快 10-100x

- **Thrust**: STL 风格 GPU 编程
  - device_vector 内存管理
  - 并行算法 (sort, reduce, transform)
  - Lambda 表达式支持

- **cuFFT**: 快速傅里叶变换
  - 1D/2D/3D FFT
  - 频域滤波
  - 信号/图像处理

- **CUB**: 高性能 Primitives
  - Block/Device 级操作
  - Reduction, Scan, Sort
  - 构建自定义算法

**编译提示**:
```bash
# cuBLAS
nvcc -o app app.cu -lcublas

# Thrust (header-only)
nvcc -o app app.cu

# cuFFT
nvcc -o app app.cu -lcufft
```

### 阶段 20: 动态并行 (练习 201-203)

**目标**: 在 GPU 上实现递归和自适应算法

**20. 动态并行编程**:
- **嵌套 Kernel**: GPU 启动 GPU
- **递归算法**: 快速排序、树遍历
- **自适应网格**: 根据数据动态调整并行度

**应用场景**:
- 光线追踪
- 碰撞检测
- 自适应网格细化 (AMR)
- 四叉树/八叉树遍历

**硬件要求**: Compute Capability >= 3.5

**编译选项**:
```bash
nvcc -arch=sm_35 -rdc=true -o app app.cu -lcudadevrt
```

### 阶段 21: 综合项目 (练习 211-212)

**目标**: 整合所有知识构建完整应用

**项目 1: MNIST 推理引擎** (211)
- 深度学习推理优化
- cuBLAS 加速矩阵乘法
- Kernel fusion
- 批量处理
- 性能分析

**项目 2: N-Body 引力模拟** (212)
- 物理模拟
- Shared Memory 优化
- 时间积分算法
- 能量守恒验证
- 可视化输出

**整合技能**:
- 全流程 CUDA 应用开发
- 多个优化技术组合
- 性能调优
- 数值验证

## 学习路径建议

### 🟢 初学者路径 (1-2个月)
1. 阶段 1-4: 基础知识 (1-40)
2. 阶段 5-6: 优化入门 (41-65)
3. 选做: 简单的高级算法 (101-112)

### 🟡 中级路径 (2-3个月)
1. 完成初学者路径
2. 阶段 7-9: 深入优化 (66-100)
3. 阶段 10-14: 实际应用 (101-143)
4. 阶段 18: 工具使用 (181-185)

### 🔴 高级路径 (3-4个月，完整掌握)
1. 完成所有基础和中级内容
2. 阶段 15-17: 现代特性 (151-173)
3. 阶段 19: CUDA 库 (191-194)
4. 阶段 20: 动态并行 (201-203)
5. 阶段 21: 综合项目 (211-212)

## 练习技巧

### 1. 循序渐进

不要跳过练习。每个练习都建立在前面的基础上。

### 2. 理解而非记忆

不要只是让测试通过，要理解为什么代码能工作。

### 3. 实验

尝试修改参数:
- 改变线程数和块数
- 测试不同的数据大小
- 观察性能变化

### 4. 使用 CUDA 工具

```bash
# 检查内存错误
cuda-memcheck ./test_program

# 性能分析
nvprof ./test_program

# 或使用 Nsight Systems
nsys profile ./test_program
```

### 5. 阅读错误信息

CUDA 错误信息通常很有帮助，仔细阅读它们。

### 6. 查阅文档

养成查阅 [CUDA 文档](https://docs.nvidia.com/cuda/) 的习惯。

## 常见陷阱

### ❌ 忘记同步

```cuda
kernel<<<1, 1>>>();
// 错误: 没有同步就访问结果
cudaMemcpy(h_data, d_data, size, cudaMemcpyDeviceToHost);
```

✅ **正确做法**:
```cuda
kernel<<<1, 1>>>();
cudaDeviceSynchronize();  // 或在 cudaMemcpy 时隐式同步
cudaMemcpy(h_data, d_data, size, cudaMemcpyDeviceToHost);
```

### ❌ 数组越界

```cuda
__global__ void kernel(float *data, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    data[idx] = 0;  // 错误: 可能越界
}
```

✅ **正确做法**:
```cuda
__global__ void kernel(float *data, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {  // 边界检查
        data[idx] = 0;
    }
}
```

### ❌ 忘记释放内存

```cuda
cudaMalloc(&d_data, size);
// ... 使用 d_data ...
// 错误: 忘记 cudaFree
return 0;
```

✅ **正确做法**:
```cuda
cudaMalloc(&d_data, size);
// ... 使用 d_data ...
cudaFree(d_data);  // 总是释放
return 0;
```

### ❌ 不检查错误

```cuda
cudaMalloc(&d_data, size);  // 可能失败
```

✅ **正确做法**:
```cuda
cudaError_t err = cudaMalloc(&d_data, size);
if (err != cudaSuccess) {
    fprintf(stderr, "Error: %s\n", cudaGetErrorString(err));
    return 1;
}
```

## 性能优化清单

完成基础练习后，对于每个 kernel，考虑:

- [ ] 内存访问是否合并？
- [ ] 是否有效利用了共享内存？
- [ ] 是否避免了 bank 冲突？
- [ ] 占用率是否足够高？
- [ ] 是否避免了分支分化？
- [ ] 是否使用了合适的数据类型？
- [ ] 是否可以使用流并发？

祝学习顺利！记住，GPU 编程是一门实践的艺术 🎨
