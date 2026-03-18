# CUDA C++ Learning System (CUDAlings)

🚀 An interactive CUDA C++ learning system inspired by Rustlings

[中文文档](README.md) | **English**

## Introduction

CUDAlings is a comprehensive CUDA C++ learning system with **105 carefully designed exercises** covering all CUDA programming knowledge from basics to advanced topics, helping you master GPU programming through hands-on practice.

## Features

- ✅ **Complete Learning Path**: 105 exercises, 29 topics, from zero to expert
- ✅ **Modern CUDA Features**: Tensor Cores, CUDA Graphs, Cooperative Groups, Unified Memory, Warp Primitives
- ✅ **Professional Tools Training**: Nsight Systems/Compute, Compute Sanitizer, cuda-gdb
- ✅ **CUDA Library Practice**: cuBLAS, Thrust, cuFFT, CUB, cuSPARSE
- ✅ **Comprehensive Projects**: MNIST inference, N-Body simulation, Ray Tracing, Molecular Dynamics
- ✅ **Advanced Algorithms**: Graph algorithms (BFS, PageRank), Sparse Matrices, ML Operators (Attention, LayerNorm)
- ✅ **Automated Testing**: Real-time code verification
- ✅ **Instant Feedback**: Quick issue detection and fixes
- ✅ **Progress Tracking**: Clear learning progress display
- ✅ **Hint System**: Multi-level hints to help you overcome challenges

## Prerequisites

- NVIDIA GPU (Compute Capability 3.0+)
- CUDA Toolkit (11.0+)
- CMake (3.18+)
- C++ Compiler (C++14 or higher)

**Recommended**: RTX 3090 or higher for full feature support

## Installation

```bash
# Clone repository
git clone <your-repo-url>
cd Cuda-CPP-Study

# Build system
mkdir build && cd build
cmake ..
make

# Run learning system
./cudalings
```

## Usage

### Basic Commands

```bash
# List all exercises
./cudalings list

# Run next exercise
./cudalings run

# Verify current exercise
./cudalings verify

# Get hints
./cudalings hint

# Check progress
./cudalings progress

# Watch mode (auto-detect file changes and verify)
./cudalings watch
```

### Workflow

1. **Run** `./cudalings run` to view current exercise
2. **Edit** `.cu` files in `exercises/` directory
3. **Verify** using `./cudalings verify` or auto-verify in watch mode
4. **Continue** automatically proceed to next exercise after passing

## Learning Path

### 🟢 Foundation Stage (Exercises 1-60)

#### Lessons 1-5: CUDA Introduction
- Hello CUDA, device query, error handling, memory management

#### Lessons 6-15: Kernel Programming
- Vector operations, matrix operations, thread organization

#### Lessons 16-30: Memory Optimization
- Memory hierarchy, Shared Memory, Bank Conflicts

#### Lessons 31-50: Parallel Algorithms
- Reduction, Scan, Synchronization, Streams

### 🟡 Intermediate Stage (Exercises 101-185)

#### Chapters 10-14: Real-World Applications (101-143)
- **Parallel Algorithms**: Prefix sum, sorting (Bitonic, Radix)
- **Image Processing**: Convolution, filtering
- **Deep Learning**: ReLU, FC Layer, Softmax, BatchNorm, Conv2D
- **Scientific Computing**: Sparse matrices (CSR)
- **Multi-GPU**: P2P communication, data parallelism

#### Chapters 15-17: Modern CUDA Features (151-173)
- **Tensor Cores** 🔥: WMMA API, mixed precision, GEMM optimization
- **CUDA Graphs** ⚡: Stream Capture, reduce launch overhead
- **Cooperative Groups** 🤝: Warp-level, Grid-wide Sync

#### Chapter 18: Profiling & Debugging (181-185)
- **Nsight Systems**: System-level profiling
- **Nsight Compute**: Kernel-level deep analysis
- **Compute Sanitizer**: Memory error detection
- **cuda-gdb**: CUDA debugger
- **Performance Metrics**: Bandwidth, throughput, occupancy analysis

### 🔴 Expert Stage (Exercises 191-212)

#### Chapter 19: CUDA Libraries (191-194)
- **cuBLAS**: Linear algebra acceleration (GEMM)
- **Thrust**: STL-style GPU programming
- **cuFFT**: Fast Fourier Transform
- **CUB**: High-performance Primitives

#### Chapter 20: Dynamic Parallelism (201-203)
- Nested kernel launches
- Recursive algorithms (quicksort)
- Adaptive grid refinement

#### Chapter 21: Comprehensive Projects (211-212)
- **Project 1**: MNIST deep learning inference engine
- **Project 2**: N-Body gravity simulation system

## Exercise Structure

Each exercise contains:
- **Exercise file**: `exercises/XX_topic/exerciseN.cu`
- **Test cases**: Embedded in exercise files
- **Hints**: Help you complete exercises
- **Reference solutions**: `solutions/` directory (try yourself first!)

## Hint System

Each exercise includes multi-level hints:
- **Hint 1**: Points to problem direction
- **Hint 2**: Provides specific approach
- **Hint 3**: Offers code snippets

Use `./cudalings hint` to view hints (displayed progressively)

## Progress Tracking

The system automatically tracks your learning progress:
- ✅ Completed exercises
- ⏳ In-progress exercises
- 📊 Completion percentage

## Troubleshooting

### CUDA Compilation Errors
```bash
# Check CUDA installation
nvcc --version

# Check GPU info
nvidia-smi
```

### Runtime Errors
- Ensure supported GPU is available
- Check CUDA error messages
- Use `cuda-memcheck` for memory issues

## Learning Recommendations

1. **Follow Sequence**: Exercises are carefully designed as progressive path
2. **Understand Principles**: Don't just pass tests, understand why
3. **Experiment**: Try modifying parameters, observe performance changes
4. **Consult Documentation**: Familiarize with [CUDA Official Documentation](https://docs.nvidia.com/cuda/)
5. **Profile Performance**: Use `nvprof` or `nsys` to analyze performance

## Documentation

- 📘 [Exercise Guide](docs/EXERCISE_GUIDE.md) - Detailed learning path
- 📗 [Knowledge Map (Chinese)](docs/KNOWLEDGE_MAP_CN.md) - Complete knowledge points
- 📕 [Knowledge Map (English)](docs/KNOWLEDGE_MAP_EN.md) - Complete knowledge points
- 📙 [Hardware Compatibility](docs/HARDWARE_COMPATIBILITY.md) - RTX 3090 compatibility
- 📔 [Architecture](docs/ARCHITECTURE.md) - System design
- 📓 [Contributing](docs/CONTRIBUTING.md) - Contribution guidelines

## Hardware Compatibility

### ✅ RTX 3090 Full Support
- **Architecture**: Ampere
- **Compute Capability**: 8.6
- **All Features Supported**: Including Tensor Cores, CUDA Graphs, Dynamic Parallelism

See [Hardware Compatibility Guide](docs/HARDWARE_COMPATIBILITY.md) for details.

## Statistics

- **Total Exercises**: 66
- **Topics**: 21
- **Knowledge Points**: 200+
- **Lines of Code**: ~15,000
- **Estimated Completion Time**: 3-4 months (full mastery)

## Contribution

Contributions of new exercises or improvements to existing content are welcome!

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details.

## License

MIT License

## Acknowledgments

Inspired by [Rustlings](https://github.com/rust-lang/rustlings)

Special thanks to NVIDIA for the CUDA platform and documentation.

---

## Quick Start Example

```bash
# 1. Install
git clone <repo-url> && cd Cuda-CPP-Study
mkdir build && cd build && cmake .. && make

# 2. Start learning
./cudalings

# 3. Your first exercise
./cudalings run
# Edit exercises/01_intro/01_hello_cuda.cu
# Remove "I AM NOT DONE" comment when complete

# 4. Verify
./cudalings verify

# 5. Continue learning
./cudalings run  # Automatically moves to next exercise
```

## Support

- 📧 Issues: [GitHub Issues](https://github.com/your-repo/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/your-repo/discussions)
- 📚 Documentation: [docs/](docs/)

Happy GPU Programming! 🚀
