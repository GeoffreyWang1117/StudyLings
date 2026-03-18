# 硬件兼容性说明 | Hardware Compatibility

## RTX 3090 系统兼容性 ✅

本学习系统在**双 RTX 3090** 配置下完全兼容。

### GPU 规格
- **架构**: Ampere
- **Compute Capability**: 8.6
- **CUDA Cores**: 10496
- **Tensor Cores**: 328 (第三代)
- **显存**: 24GB GDDR6X
- **显存带宽**: 936 GB/s

### 支持的所有特性

#### ✅ 基础特性 (所有练习 1-100)
- CUDA 核心编程 ✓
- 内存管理 ✓
- Shared Memory ✓
- 同步机制 ✓
- Stream 并发 ✓

#### ✅ 高级算法 (练习 101-143)
- 并行算法 (Scan, Sort) ✓
- 图像处理 ✓
- 深度学习 primitives ✓
- 科学计算 ✓
- Multi-GPU 通信 ✓

#### ✅ 现代 CUDA 特性 (练习 151-173)
- **Tensor Cores** ✓ (CC 8.6 > 7.0)
  - WMMA API 完全支持
  - FP16/FP32/TF32 混合精度
  - INT8 量化支持

- **CUDA Graphs** ✓ (CC 8.6 > 7.0)
  - Stream Capture
  - Graph 优化

- **Cooperative Groups** ✓ (CC 8.6 > 6.0)
  - Thread Block Groups
  - Warp-level primitives
  - Grid-wide synchronization

#### ✅ 性能工具 (练习 181-185)
- Nsight Systems ✓
- Nsight Compute ✓
- Compute Sanitizer ✓
- cuda-gdb ✓

#### ✅ CUDA 库 (练习 191-194)
- cuBLAS ✓
- Thrust ✓
- cuFFT ✓
- CUB ✓

#### ✅ 动态并行 (练习 201-203)
- 嵌套 Kernel ✓ (CC 8.6 > 3.5)
- 递归算法 ✓
- 自适应并行 ✓

#### ✅ 综合项目 (练习 211-212)
- MNIST 推理引擎 ✓
- N-Body 模拟 ✓

## 编译配置建议

### 基础练习
```bash
nvcc -arch=sm_86 -o exercise exercise.cu
```

### Tensor Core 练习
```bash
nvcc -arch=sm_86 -o tensor_demo tensor_demo.cu
# RTX 3090 支持 TF32 (默认启用)
```

### 动态并行练习
```bash
nvcc -arch=sm_86 -rdc=true -o dynamic dynamic.cu -lcudadevrt
```

### CUDA 库练习
```bash
# cuBLAS
nvcc -arch=sm_86 -o cublas_demo cublas_demo.cu -lcublas

# cuFFT
nvcc -arch=sm_86 -o cufft_demo cufft_demo.cu -lcufft
```

### Multi-GPU 练习
```bash
# 利用双 3090 配置
nvcc -arch=sm_86 -o multigpu multigpu.cu
```

## 性能预期

### RTX 3090 理论峰值
- **FP32**: ~35.6 TFLOPS
- **FP16 Tensor Core**: ~142 TFLOPS
- **TF32 Tensor Core**: ~71 TFLOPS (默认)
- **INT8 Tensor Core**: ~284 TOPS
- **内存带宽**: 936 GB/s

### 双卡配置优势
- Multi-GPU 练习可充分利用
- P2P 直接通信 (NVLink 不可用，但 PCIe P2P 可用)
- 数据并行可获得接近 2x 加速

## 特殊注意事项

### TF32 模式
RTX 3090 默认启用 TF32 模式以加速 FP32 矩阵运算：
```cpp
// 如果需要禁用 TF32 (为了精度)
cudaDeviceSetLimit(cudaLimitTF32Precision, 0);
```

### 大显存优势
24GB 显存允许：
- 更大的 batch size (深度学习)
- 更大规模的 N-Body 模拟
- 完整的数据集加载

### 推荐配置
```bash
# CUDA Toolkit 版本
CUDA >= 11.0 (推荐 11.8 或 12.x)

# 驱动版本
Driver >= 470.x
```

## 验证系统
```bash
# 检查 GPU
nvidia-smi

# 检查 CUDA
nvcc --version

# 检查 Compute Capability
./exercises/01_intro/02_device_query.cu
```

## 结论
✅ **所有 66 个练习在 RTX 3090 双卡系统上完全兼容！**
