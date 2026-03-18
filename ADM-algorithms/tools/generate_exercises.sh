#!/bin/bash
# 批量生成练习模板的脚本

# 定义练习模板函数
generate_exercise() {
    local file_path=$1
    local name=$2
    local difficulty=$3
    local topic=$4
    local description=$5

    cat > "$file_path" << 'EOF'
/*
 * 练习: EXERCISE_NAME
 * 难度: DIFFICULTY
 * 主题: TOPIC
 *
 * 描述:
 * DESCRIPTION
 *
 * 学习目标:
 * - 待完善
 *
 * 参考: ADM 3rd Edition
 */

#include <iostream>
#include <vector>
#include <cassert>

// TODO: 实现这个练习

// I AM NOT DONE

// ===== 测试代码 =====

void test_basic() {
    std::cout << "✓ Basic test passed\n";
}

int main() {
    std::cout << "Running EXERCISE_NAME Tests...\n";
    std::cout << "==============================\n";

    test_basic();

    std::cout << "\n✅ All tests passed!\n";
    return 0;
}
EOF

    # 替换占位符
    sed -i "s/EXERCISE_NAME/$name/g" "$file_path"
    sed -i "s/DIFFICULTY/$difficulty/g" "$file_path"
    sed -i "s/TOPIC/$topic/g" "$file_path"
    sed -i "s/DESCRIPTION/$description/g" "$file_path"
}

echo "Exercise generation script created"
echo "Use: generate_exercise <path> <name> <difficulty> <topic> <description>"
