#!/bin/bash
# 验证所有练习是否能够编译（用于测试）

set -e

echo "🧪 验证所有练习文件..."
echo ""

BUILD_DIR="/tmp/adm_verify_$$"
mkdir -p "$BUILD_DIR"

EXERCISES_DIR="exercises"
TOTAL=0
SUCCESS=0
FAILED=0

# 遍历所有 .cpp 文件
for file in $(find "$EXERCISES_DIR" -name "*.cpp" | sort); do
    TOTAL=$((TOTAL + 1))
    filename=$(basename "$file")

    echo -n "[$TOTAL] 验证 $filename ... "

    # 尝试编译
    if g++ -std=c++17 -Wall -Wextra -I. -o "$BUILD_DIR/test" "$file" 2>/dev/null; then
        echo "✓ 编译成功"
        SUCCESS=$((SUCCESS + 1))
    else
        echo "❌ 编译失败"
        FAILED=$((FAILED + 1))
        echo "   文件: $file"
    fi
done

# 清理
rm -rf "$BUILD_DIR"

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  验证结果                                                      ║"
echo "╠════════════════════════════════════════════════════════════════╣"
echo "║  总计:   $TOTAL                                                   "
echo "║  成功:   $SUCCESS                                                 "
echo "║  失败:   $FAILED                                                  "
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "✅ 所有练习文件都能正确编译！"
    exit 0
else
    echo "⚠️  有 $FAILED 个文件编译失败"
    exit 1
fi
