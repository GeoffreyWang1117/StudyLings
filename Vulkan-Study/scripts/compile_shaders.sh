#!/bin/bash
# 着色器编译脚本
# 将所有 GLSL 着色器编译为 SPIR-V

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SHADER_DIR="$PROJECT_ROOT/shaders"
OUTPUT_DIR="$PROJECT_ROOT/build/shaders"

# 查找 glslc 编译器
if command -v glslc &> /dev/null; then
    GLSLC=glslc
elif [ -n "$VULKAN_SDK" ] && [ -f "$VULKAN_SDK/Bin/glslc" ]; then
    GLSLC="$VULKAN_SDK/Bin/glslc"
elif [ -n "$VULKAN_SDK" ] && [ -f "$VULKAN_SDK/bin/glslc" ]; then
    GLSLC="$VULKAN_SDK/bin/glslc"
else
    echo "Error: glslc not found. Please install Vulkan SDK."
    exit 1
fi

echo "Using glslc: $GLSLC"
echo "Shader directory: $SHADER_DIR"
echo "Output directory: $OUTPUT_DIR"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 编译计数
compiled=0
failed=0

# 编译所有顶点着色器
for shader in "$SHADER_DIR"/*.vert; do
    if [ -f "$shader" ]; then
        filename=$(basename "$shader")
        output="$OUTPUT_DIR/${filename}.spv"
        echo "Compiling $filename..."
        if $GLSLC "$shader" -o "$output"; then
            ((compiled++))
        else
            echo "  Failed!"
            ((failed++))
        fi
    fi
done

# 编译所有片段着色器
for shader in "$SHADER_DIR"/*.frag; do
    if [ -f "$shader" ]; then
        filename=$(basename "$shader")
        output="$OUTPUT_DIR/${filename}.spv"
        echo "Compiling $filename..."
        if $GLSLC "$shader" -o "$output"; then
            ((compiled++))
        else
            echo "  Failed!"
            ((failed++))
        fi
    fi
done

echo ""
echo "================================"
echo "Compilation complete!"
echo "  Compiled: $compiled shaders"
echo "  Failed: $failed shaders"
echo "================================"

if [ $failed -gt 0 ]; then
    exit 1
fi
