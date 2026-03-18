# CUDA C++ 完整知识点清单

本学习系统涵盖的所有 CUDA 编程知识点，共 **21 个主题**，**66 个练习**。

---

## 📚 第一部分：CUDA 基础 (练习 1-30)

### 1️⃣ CUDA 入门 (练习 1-5)

**核心概念**:
- [ ] CUDA 程序结构
- [ ] Host (CPU) vs Device (GPU)
- [ ] `__global__` kernel 函数
- [ ] Kernel 调用语法 `<<<blocks, threads>>>`
- [ ] `cudaDeviceSynchronize()` 同步
- [ ] GPU 设备属性查询
- [ ] Compute Capability 概念
- [ ] CUDA 错误处理最佳实践
- [ ] 错误检查宏

**API 掌握**:
```cpp
cudaGetDeviceCount()
cudaGetDeviceProperties()
cudaSetDevice()
cudaGetLastError()
cudaGetErrorString()
cudaMalloc() / cudaFree()
cudaMemcpy()
```

---

### 2️⃣ Kernel 编程基础 (练习 6-15)

**核心概念**:
- [ ] Kernel 函数编写
- [ ] `threadIdx`, `blockIdx`, `blockDim`
- [ ] 全局线程索引计算
- [ ] 边界检查 (bounds checking)
- [ ] 向量运算并行化
- [ ] 矩阵运算并行化
- [ ] Grid-Stride Loop 模式

**并行模式**:
```cpp
// 1D 索引
int idx = blockIdx.x * blockDim.x + threadIdx.x;

// 2D 索引
int row = blockIdx.y * blockDim.y + threadIdx.y;
int col = blockIdx.x * blockDim.x + threadIdx.x;

// Grid-Stride Loop
for (int i = idx; i < n; i += gridDim.x * blockDim.x) {
    // work
}
```

---

### 3️⃣ 线程组织 (练习 16-25)

**核心概念**:
- [ ] 线程层次结构 (Grid → Block → Thread)
- [ ] 1D/2D/3D 线程网格
- [ ] Block 大小选择
- [ ] Grid 大小计算
- [ ] Warp 概念 (32 threads)
- [ ] SIMT 执行模型
- [ ] 线程发散 (divergence)

**最佳实践**:
- Block 大小通常为 128, 256, 512
- 总线程数应为 Warp 大小 (32) 的倍数
- 考虑 SM 数量和占用率

---

### 4️⃣ 内存管理 (练习 26-35)

**核心概念**:
- [ ] 全局内存 (Global Memory)
- [ ] 设备内存分配/释放
- [ ] Host ↔ Device 数据传输
- [ ] 统一内存 (Unified Memory)
- [ ] 固定内存 (Pinned Memory)
- [ ] 常量内存 (Constant Memory)
- [ ] 纹理内存 (Texture Memory)
- [ ] 内存带宽优化

**API**:
```cpp
// 设备内存
cudaMalloc() / cudaFree()
cudaMemcpy() / cudaMemcpyAsync()

// 统一内存
cudaMallocManaged()

// 固定内存
cudaMallocHost() / cudaFreeHost()
cudaHostAlloc()
```

---

## 📚 第二部分：性能优化 (练习 41-100)

### 5️⃣ Shared Memory (练习 41-50)

**核心概念**:
- [ ] Shared Memory 声明 `__shared__`
- [ ] Block 内线程通信
- [ ] Bank Conflicts 概念
- [ ] Bank Conflicts 避免技巧
- [ ] Tiling 技术
- [ ] 矩阵转置优化
- [ ] Reduction 优化

**Bank Conflicts**:
```cpp
// 32-way bank conflicts
__shared__ float shared[32][32];
shared[threadIdx.x][threadIdx.x] = ...; // 冲突!

// 避免 (padding)
__shared__ float shared[32][33];
shared[threadIdx.x][threadIdx.x] = ...; // OK
```

---

### 6️⃣ 同步机制 (练习 51-60)

**核心概念**:
- [ ] `__syncthreads()` block 级同步
- [ ] 原子操作 (atomics)
- [ ] `atomicAdd()`, `atomicCAS()` 等
- [ ] Warp Shuffle 指令
- [ ] `__shfl_down_sync()`, `__shfl_xor_sync()`
- [ ] 内存栅栏 (memory fence)
- [ ] `__threadfence()`, `__threadfence_block()`

**原子操作**:
```cpp
atomicAdd(&counter, 1);
atomicMax(&max_val, val);
atomicCAS(&lock, 0, 1); // Compare-And-Swap
```

---

### 7️⃣ 性能优化技术 (练习 61-75)

**核心概念**:
- [ ] 内存合并访问 (Coalesced Access)
- [ ] 对齐 (Alignment)
- [ ] 占用率 (Occupancy) 优化
- [ ] 寄存器使用优化
- [ ] 指令级并行 (ILP)
- [ ] 循环展开 (Loop Unrolling)
- [ ] 分支预测优化
- [ ] `#pragma unroll`

**占用率计算**:
```cpp
cudaOccupancyMaxActiveBlocksPerMultiprocessor()
cudaOccupancyMaxPotentialBlockSize()
```

---

### 8️⃣ CUDA Streams (练习 76-85)

**核心概念**:
- [ ] Stream 概念
- [ ] 异步操作
- [ ] Kernel 并发执行
- [ ] 数据传输与计算重叠
- [ ] Stream 优先级
- [ ] Event 和计时
- [ ] Stream 回调函数
- [ ] 默认 Stream vs 非默认 Stream

**API**:
```cpp
cudaStreamCreate() / cudaStreamDestroy()
cudaStreamSynchronize()
cudaMemcpyAsync()
cudaEventCreate() / cudaEventRecord()
cudaEventElapsedTime()
```

---

### 9️⃣ 高级特性 (练习 86-100)

**核心概念**:
- [ ] Warp-level Primitives
- [ ] 分块 Reduction
- [ ] 并行 Scan (前缀和)
- [ ] 并行排序
- [ ] Histogram 直方图
- [ ] 数据压缩

---

## 📚 第三部分：实际应用 (练习 101-143)

### 🔟 并行算法 (练习 101-103)

**核心算法**:
- [ ] **前缀和 (Scan)**
  - Up-sweep / Down-sweep 算法
  - Work-efficient Scan
  - Kogge-Stone 算法

- [ ] **Bitonic Sort**
  - Bitonic 序列性质
  - 递归合并
  - GPU 并行实现

- [ ] **Radix Sort**
  - 按位排序
  - Stable Sort 保证
  - 多键值排序

---

### 1️⃣1️⃣ 图像处理 (练习 111-112)

**核心技术**:
- [ ] 2D 卷积
- [ ] Tiling 和 Halo 处理
- [ ] 常量内存存储卷积核
- [ ] 可分离滤波器
- [ ] 高斯模糊
- [ ] Sobel 边缘检测

---

### 1️⃣2️⃣ 深度学习 (练习 121-125)

**核心层实现**:
- [ ] **ReLU 激活函数**
  - Forward: max(0, x)
  - Backward: x > 0 ? 1 : 0

- [ ] **全连接层 (FC)**
  - 矩阵乘法 Y = XW + b
  - 权重梯度、输入梯度、偏置梯度

- [ ] **Softmax**
  - 数值稳定实现 (max trick)
  - Log-Softmax

- [ ] **Batch Normalization**
  - Mean/Variance 计算
  - 归一化公式
  - Gamma/Beta 参数

- [ ] **2D 卷积层**
  - im2col + GEMM 方法
  - Padding/Stride 处理
  - 梯度反向传播

---

### 1️⃣3️⃣ 科学计算 (练习 131)

**核心技术**:
- [ ] 稀疏矩阵 (Sparse Matrix)
- [ ] CSR 格式 (Compressed Sparse Row)
- [ ] SpMV (Sparse Matrix-Vector Multiply)
- [ ] 不规则访问模式处理

---

### 1️⃣4️⃣ Multi-GPU 编程 (练习 141-143)

**核心技术**:
- [ ] 多 GPU 检测
- [ ] P2P (Peer-to-Peer) 能力查询
- [ ] `cudaDeviceEnablePeerAccess()`
- [ ] `cudaMemcpyPeer()`
- [ ] 数据并行模式
- [ ] 跨 GPU 同步
- [ ] NCCL 库 (可选)

---

## 📚 第四部分：现代 CUDA 特性 (练习 151-185)

### 1️⃣5️⃣ Tensor Cores (练习 151-153)

**核心技术**:
- [ ] WMMA API (Warp Matrix Multiply-Accumulate)
- [ ] `nvcuda::wmma` namespace
- [ ] Fragment 概念
- [ ] `load_matrix_sync()`, `mma_sync()`, `store_matrix_sync()`
- [ ] FP16/FP32 混合精度
- [ ] TF32 模式 (Ampere+)
- [ ] INT8 量化 (可选)
- [ ] GEMM 优化技巧

**硬件要求**: CC >= 7.0 (Volta+)

---

### 1️⃣6️⃣ CUDA Graphs (练习 161-162)

**核心技术**:
- [ ] Graph 概念
- [ ] Stream Capture
- [ ] `cudaStreamBeginCapture()` / `cudaStreamEndCapture()`
- [ ] `cudaGraphInstantiate()`
- [ ] `cudaGraphLaunch()`
- [ ] Graph 更新
- [ ] `cudaGraphExecKernelNodeSetParams()`
- [ ] 减少 Kernel 启动开销

**应用场景**: 重复执行的 Kernel 序列

---

### 1️⃣7️⃣ Cooperative Groups (练习 171-173)

**核心技术**:
- [ ] `cooperative_groups` namespace
- [ ] `this_thread_block()`
- [ ] `this_grid()`
- [ ] Thread Block Groups
- [ ] Warp-level Primitives
- [ ] `coalesced_threads()`
- [ ] `tiled_partition<N>()`
- [ ] Grid-wide Synchronization
- [ ] `cudaLaunchCooperativeKernel()`

**硬件要求**: CC >= 6.0

---

### 1️⃣8️⃣ 性能分析与调试 (练习 181-185)

**工具掌握**:
- [ ] **Nsight Systems**
  - 系统级 profiling
  - CPU/GPU 时间线
  - Stream 并发分析
  - 命令: `nsys profile --stats=true ./app`

- [ ] **Nsight Compute**
  - Kernel 级 profiling
  - SM Throughput, Memory Throughput
  - Warp Stall Reasons
  - Roofline 分析
  - 命令: `ncu --set full ./app`

- [ ] **Compute Sanitizer**
  - Memcheck: 内存错误
  - Racecheck: 数据竞争
  - Initcheck: 未初始化内存
  - Synccheck: 同步错误
  - 命令: `compute-sanitizer --tool memcheck ./app`

- [ ] **cuda-gdb**
  - 断点调试
  - 线程切换
  - Shared Memory 检查
  - 命令: `cuda-gdb ./app`

- [ ] **性能指标**
  - 理论带宽计算
  - 理论 FLOPS 计算
  - 占用率分析
  - 带宽利用率
  - 计算吞吐量

---

## 📚 第五部分：CUDA 库与高级主题 (练习 191-212)

### 1️⃣9️⃣ CUDA 库 (练习 191-194)

**库掌握**:
- [ ] **cuBLAS** - 线性代数
  - `cublasCreate()` / `cublasDestroy()`
  - `cublasSgemm()` - 矩阵乘法
  - 列主序 vs 行主序
  - 性能对比 (vs 手写 kernel)

- [ ] **Thrust** - STL 风格 GPU 编程
  - `thrust::device_vector<T>`
  - `thrust::host_vector<T>`
  - `thrust::sort()`, `thrust::reduce()`
  - `thrust::transform()`
  - Lambda 表达式支持
  - 自定义函数对象

- [ ] **cuFFT** - 快速傅里叶变换
  - `cufftPlan1d()` / `cufftPlan2d()`
  - `cufftExecC2C()` - 复数变换
  - 频域滤波
  - 归一化处理

- [ ] **CUB** - 高性能 Primitives
  - `cub::BlockReduce<T, BLOCK_SIZE>`
  - `cub::DeviceScan::InclusiveSum()`
  - `cub::DeviceRadixSort::SortKeys()`
  - Temporary Storage 管理

---

### 2️⃣0️⃣ 动态并行 (练习 201-203)

**核心技术**:
- [ ] 嵌套 Kernel 调用
- [ ] Device 端 `cudaDeviceSynchronize()`
- [ ] 递归算法实现
- [ ] 递归深度控制
- [ ] 自适应并行
- [ ] 动态负载平衡

**编译要求**:
```bash
nvcc -arch=sm_35 -rdc=true -o app app.cu -lcudadevrt
```

**应用场景**:
- 快速排序、归并排序
- 树遍历 (四叉树/八叉树)
- 光线追踪
- 自适应网格细化 (AMR)

**硬件要求**: CC >= 3.5

---

### 2️⃣1️⃣ 综合项目 (练习 211-212)

**项目 1: MNIST 推理引擎**
- [ ] 网络结构设计 (784→128→64→10)
- [ ] cuBLAS 加速
- [ ] Kernel Fusion
- [ ] 批量推理
- [ ] 性能优化
- [ ] 准确率验证

**项目 2: N-Body 引力模拟**
- [ ] O(N²) 力计算
- [ ] Shared Memory 分块
- [ ] Velocity Verlet 积分
- [ ] 能量守恒验证
- [ ] 性能分析
- [ ] 可视化输出

---

## 🎯 学习成果

完成本系统后，你将掌握：

### 💻 编程技能
- ✅ 熟练编写高性能 CUDA Kernel
- ✅ 理解 GPU 架构和执行模型
- ✅ 掌握内存层次和优化技巧
- ✅ 使用现代 CUDA 特性 (Tensor Cores, Graphs, Cooperative Groups)
- ✅ 调试和性能分析工具使用

### 🚀 应用能力
- ✅ 并行算法设计与实现
- ✅ 图像处理加速
- ✅ 深度学习算子实现
- ✅ 科学计算应用
- ✅ Multi-GPU 编程

### 🔧 工程实践
- ✅ CUDA 库高效使用 (cuBLAS, Thrust, cuFFT, CUB)
- ✅ 性能瓶颈识别与优化
- ✅ 代码调试技巧
- ✅ 完整项目开发经验

### 📊 理论知识
- ✅ SIMT 执行模型
- ✅ 内存层次结构
- ✅ Warp 调度机制
- ✅ 占用率理论
- ✅ Roofline 模型

---

## 📈 难度梯度

- **初级** (练习 1-60): 基础概念，占用率 30-50%
- **中级** (练习 61-143): 优化技巧，占用率 50-70%
- **高级** (练习 151-185): 现代特性，占用率 70-90%
- **专家级** (练习 191-212): 库和项目，接近理论峰值

---

## ✅ 知识点检查清单

打印本文档，逐项完成练习，勾选已掌握的知识点！

**总计**:
- **21 个主题**
- **66 个练习**
- **200+ 个核心知识点**
- **完整的 CUDA 编程技能树**
