# CUDA C++ Learning System (CUDAlings)

🚀 一个类似 Rustlings 的交互式 CUDA C++ 学习系统

## 简介

CUDAlings 是一个由浅入深的 CUDA C++ 学习系统，包含 **105 个精心设计的练习**，涵盖从基础到高级的所有 CUDA 编程知识，通过实践帮助你掌握 GPU 编程。

## 特性

- ✅ **完整的学习路径**: 105 个练习，29 个主题，从零基础到专家级
- ✅ **现代 CUDA 特性**: Tensor Cores、CUDA Graphs、Cooperative Groups、Unified Memory、Warp Primitives
- ✅ **实用工具训练**: Nsight Systems/Compute、Compute Sanitizer、cuda-gdb
- ✅ **CUDA 库实战**: cuBLAS、Thrust、cuFFT、CUB、cuSPARSE
- ✅ **综合项目**: MNIST 推理引擎、N-Body 模拟、光线追踪、分子动力学
- ✅ **高级算法**: 图算法 (BFS、PageRank)、稀疏矩阵、机器学习算子 (Attention、LayerNorm)
- ✅ **自动化测试**: 实时验证你的代码
- ✅ **即时反馈**: 快速发现和修复问题
- ✅ **进度追踪**: 清晰展示学习进展
- ✅ **提示系统**: 多级提示帮助你突破难关

## 前置要求

- NVIDIA GPU (计算能力 3.0+)
- CUDA Toolkit (11.0+)
- CMake (3.18+)
- C++ 编译器 (支持 C++14 或更高)

## 安装

```bash
# 克隆仓库
git clone <your-repo-url>
cd Cuda-CPP-Study

# 构建系统
mkdir build && cd build
cmake ..
make

# 运行学习系统
./cudalings
```

## 使用方法

### 基本命令

```bash
# 查看所有练习
./cudalings list

# 运行下一个练习
./cudalings run

# 验证当前练习
./cudalings verify

# 获取提示
./cudalings hint

# 查看进度
./cudalings progress

# 监视模式 (自动检测文件变化并验证)
./cudalings watch
```

### 工作流程

1. **运行** `./cudalings run` 查看当前练习
2. **编辑** `exercises/` 目录下的 `.cu` 文件
3. **验证** 使用 `./cudalings verify` 或在 watch 模式下自动验证
4. **继续** 通过后自动进入下一个练习

## 学习路径

### 🟢 基础阶段 (练习 1-60)

#### 第 1-5 课: CUDA 入门
- Hello CUDA、设备查询、错误处理、内存管理

#### 第 6-15 课: Kernel 编程
- 向量运算、矩阵操作、线程组织

#### 第 16-30 课: 内存优化
- 内存层次、Shared Memory、Bank Conflicts

#### 第 31-50 课: 并行算法
- Reduction、Scan、Synchronization、Streams

### 🟡 进阶阶段 (练习 101-185)

#### 第 10-14 章: 实际应用 (101-143)
- **并行算法**: 前缀和、排序 (Bitonic, Radix, Merge)、直方图、高级归约
- **图像处理**: 卷积、高斯模糊、Sobel 边缘检测、图像金字塔
- **深度学习**: ReLU、FC Layer、Softmax、BatchNorm、Conv2D
- **科学计算**: 稀疏矩阵 (CSR)、蒙特卡洛、热传导、流体力学
- **Multi-GPU**: P2P 通信、数据并行

#### 第 15-17 章: 现代 CUDA 特性 (151-173)
- **Tensor Cores** 🔥: WMMA API、混合精度、GEMM 优化
- **CUDA Graphs** ⚡: Stream Capture、减少启动开销
- **Cooperative Groups** 🤝: Warp-level、Grid-wide Sync

#### 第 18 章: 性能分析与调试 (181-185)
- **Nsight Systems**: 系统级性能分析
- **Nsight Compute**: Kernel 深度分析
- **Compute Sanitizer**: 内存错误检测
- **cuda-gdb**: CUDA 调试器
- **性能指标**: 带宽、吞吐量、占用率分析

### 🔴 专家阶段 (练习 191-295)

#### 第 19 章: CUDA 库 (191-194)
- **cuBLAS**: 线性代数加速 (GEMM)
- **Thrust**: STL 风格 GPU 编程
- **cuFFT**: 快速傅里叶变换
- **CUB**: 高性能 Primitives

#### 第 20 章: 动态并行 (201-203)
- 嵌套 Kernel 调用
- 递归算法 (快速排序)
- 自适应网格细化

#### 第 21 章: 综合项目 (211-212)
- **项目 1**: MNIST 深度学习推理引擎
- **项目 2**: N-Body 引力模拟系统

#### 第 22 章: Unified Memory (221-224) 🆕
- 统一内存基础、预取优化
- 并发访问、性能分析

#### 第 23 章: Warp Primitives (231-234) 🆕
- **Warp Shuffle**: 寄存器间通信、快速归约
- **Warp Vote**: __all_sync、__any_sync、__ballot_sync
- **Warp Match**: 数据分组、去重、直方图
- **Warp 矩阵操作**: 小矩阵优化

#### 第 24 章: 图算法 (241-244) 🆕
- **BFS**: Level Synchronous 方法
- **PageRank**: 迭代图算法
- **最短路径**: Bellman-Ford
- **三角形计数**: 社交网络分析

#### 第 25 章: 稀疏矩阵 (251-253) 🆕
- **SpMV**: CSR 格式
- **格式转换**: COO 到 CSR
- **cuSPARSE**: 库的使用

#### 第 26 章: 分子动力学 (261-263) 🆕
- Lennard-Jones 势能
- Verlet 积分法
- 邻居列表优化

#### 第 27 章: 光线追踪 (271-274) 🆕
- 光线-球体相交
- 简单光线追踪器
- BVH 加速结构
- 路径追踪

#### 第 28 章: 视频处理 (281-283) 🆕
- RGB 到 YUV 转换
- 运动估计
- 时域滤波

#### 第 29 章: 机器学习算子 (291-295) 🆕
- **Attention**: Scaled Dot-Product
- **Layer Norm**: 归一化算子
- **GELU**: 激活函数
- **Flash Attention**: 内存高效实现
- **Group Norm**: 小批量归一化

## 练习结构

每个练习包含：
- **题目文件**: `exercises/XX_topic/exerciseN.cu`
- **测试用例**: 内嵌在练习文件中
- **提示信息**: 帮助你完成练习
- **参考答案**: `solutions/` 目录（建议先自己尝试）

## 提示系统

每个练习都包含多级提示：
- **提示 1**: 指向问题方向
- **提示 2**: 给出具体思路
- **提示 3**: 提供代码片段

使用 `./cudalings hint` 查看提示（会逐级显示）

## 进度追踪

系统会自动追踪你的学习进度：
- ✅ 已完成的练习
- ⏳ 进行中的练习
- 📊 完成百分比

## 故障排除

### CUDA 编译错误
```bash
# 检查 CUDA 安装
nvcc --version

# 检查 GPU 信息
nvidia-smi
```

### 运行时错误
- 确保使用支持的 GPU
- 检查 CUDA 错误消息
- 使用 `cuda-memcheck` 检查内存问题

## 学习建议

1. **按顺序完成**: 练习是精心设计的递进路径
2. **理解原理**: 不要只是让测试通过，理解为什么
3. **实验探索**: 尝试修改参数，观察性能变化
4. **查阅文档**: 熟悉 [CUDA 官方文档](https://docs.nvidia.com/cuda/)
5. **性能分析**: 使用 `nvprof` 或 `nsys` 分析性能

## 贡献

欢迎贡献新的练习或改进现有内容！

## 许可证

MIT License

## 致谢

灵感来自 [Rustlings](https://github.com/rust-lang/rustlings)
