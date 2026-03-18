#!/bin/bash
# 创建新练习的脚本模板

if [ $# -lt 4 ]; then
    echo "用法: $0 <name> <difficulty> <topic> <category>"
    echo ""
    echo "示例: $0 heap_sort Medium Sorting 03_sorting"
    echo ""
    echo "difficulty: Easy | Medium | Hard"
    echo "category: 练习所在目录，如 03_sorting"
    exit 1
fi

NAME=$1
DIFFICULTY=$2
TOPIC=$3
CATEGORY=$4

FILE_PATH="exercises/${CATEGORY}/${NAME}.cpp"

if [ -f "$FILE_PATH" ]; then
    echo "❌ 文件已存在: $FILE_PATH"
    exit 1
fi

# 创建练习文件
cat > "$FILE_PATH" << EOF
/*
 * 练习: ${NAME}
 * 难度: ${DIFFICULTY}
 * 主题: ${TOPIC}
 *
 * 描述:
 * [在此添加练习描述]
 *
 * 学习目标:
 * - 目标1
 * - 目标2
 *
 * 参考: ADM 3rd Edition - Chapter X
 */

#include <iostream>
#include <vector>
#include <cassert>

// TODO: 在此实现你的函数

// I AM NOT DONE

// ===== 测试代码 =====

void test_basic() {
    // 添加基本测试
    std::cout << "✓ Basic test passed\n";
}

void test_edge_cases() {
    // 添加边界情况测试
    std::cout << "✓ Edge cases test passed\n";
}

int main() {
    std::cout << "Running ${NAME} Tests...\n";
    std::cout << "==============================\n";

    test_basic();
    test_edge_cases();

    std::cout << "\n✅ All tests passed!\n";
    return 0;
}
EOF

echo "✅ 创建练习文件: $FILE_PATH"
echo ""
echo "📝 下一步:"
echo "   1. 编辑 $FILE_PATH 添加练习内容"
echo "   2. 在 judge/exercise.hpp 中注册这个练习"
echo "   3. 运行 ./adm-judge list 验证"
