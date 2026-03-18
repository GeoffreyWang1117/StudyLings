#!/bin/bash

# 检查 GPU 和 CUDA 环境

echo "=================================="
echo "GPU 和 CUDA 环境检查"
echo "=================================="

# 检查 nvidia-smi
echo ""
echo "1. 检查 NVIDIA 驱动..."
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi
else
    echo "✗ nvidia-smi 未找到"
    echo "请安装 NVIDIA 驱动"
    exit 1
fi

# 检查 CUDA
echo ""
echo "2. 检查 CUDA 工具链..."
if command -v nvcc &> /dev/null; then
    echo "✓ nvcc 版本:"
    nvcc --version
else
    echo "✗ nvcc 未找到"
    echo "请安装 CUDA Toolkit"
    exit 1
fi

# 检查环境变量
echo ""
echo "3. 检查环境变量..."
echo "PATH: $PATH" | grep -o "cuda" || echo "⚠️  PATH 中未找到 cuda"
echo "LD_LIBRARY_PATH: $LD_LIBRARY_PATH" | grep -o "cuda" || echo "⚠️  LD_LIBRARY_PATH 中未找到 cuda"

# 编译并运行测试程序
echo ""
echo "4. 编译并运行简单的 CUDA 程序..."

# 创建临时测试文件
cat > /tmp/cuda_test.cu << 'EOF'
#include <stdio.h>
#include <cuda_runtime.h>

__global__ void test_kernel() {
    printf("Hello from GPU!\n");
}

int main() {
    int deviceCount;
    cudaGetDeviceCount(&deviceCount);

    if (deviceCount == 0) {
        printf("No CUDA devices found!\n");
        return 1;
    }

    printf("Found %d CUDA device(s)\n", deviceCount);

    cudaDeviceProp prop;
    cudaGetDeviceProperties(&prop, 0);
    printf("\nDevice 0: %s\n", prop.name);
    printf("  Compute Capability: %d.%d\n", prop.major, prop.minor);
    printf("  Global Memory: %.2f GB\n", prop.totalGlobalMem / 1024.0 / 1024.0 / 1024.0);

    test_kernel<<<1, 1>>>();
    cudaDeviceSynchronize();

    printf("\nCUDA environment is ready!\n");
    return 0;
}
EOF

# 编译
if nvcc -o /tmp/cuda_test /tmp/cuda_test.cu 2>&1; then
    echo "✓ 编译成功"

    # 运行
    echo ""
    if /tmp/cuda_test; then
        echo ""
        echo "=================================="
        echo "✓ 所有检查通过！"
        echo "你的系统已准备好运行 CUDAlings"
        echo "=================================="
    else
        echo "✗ 程序运行失败"
        exit 1
    fi
else
    echo "✗ 编译失败"
    exit 1
fi

# 清理
rm -f /tmp/cuda_test /tmp/cuda_test.cu
