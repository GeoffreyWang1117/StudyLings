/*
 * 练习: divide01_binary_search_recursive
 * 难度: Easy
 * 主题: 分治算法 - 二分查找递归实现
 *
 * 描述:
 * 使用分治法（递归）实现二分查找，理解分治思想的核心。
 *
 * 学习目标:
 * - 理解分治算法的三个步骤：分解、解决、合并
 * - 掌握递归实现
 * - 分析递归的时间复杂度
 *
 * 参考: ADM 3rd Edition - Chapter 5 (Divide and Conquer)
 */

#include <iostream>
#include <vector>
#include <cassert>

// TODO: 实现递归二分查找
// 返回target的索引，如果不存在返回-1
int binarySearchRecursive(const std::vector<int>& arr, int target, int left, int right) {
    // 你的代码
    // 分治三步骤：
    // 1. 分解：找到中点，将问题分成两半
    // 2. 解决：递归查找目标半边
    // 3. 合并：二分查找不需要合并步骤
    return -1;
}

// 公共接口
int binarySearch(const std::vector<int>& arr, int target) {
    return binarySearchRecursive(arr, target, 0, arr.size() - 1);
}

// TODO: 实现查找第一个大于等于target的位置
int lowerBound(const std::vector<int>& arr, int target) {
    // 你的代码
    // 提示: 这是二分查找的变体
    return -1;
}

// TODO: 实现查找最后一个小于等于target的位置
int upperBound(const std::vector<int>& arr, int target) {
    // 你的代码
    return -1;
}

// I AM NOT DONE

// ===== 测试代码 =====

void test_basic_search() {
    std::vector<int> arr = {1, 3, 5, 7, 9, 11, 13};

    assert(binarySearch(arr, 7) == 3);
    assert(binarySearch(arr, 1) == 0);
    assert(binarySearch(arr, 13) == 6);
    assert(binarySearch(arr, 4) == -1);

    std::cout << "✓ Basic search test passed\n";
}

void test_bounds() {
    std::vector<int> arr = {1, 3, 3, 3, 5, 7, 9};

    assert(lowerBound(arr, 3) == 1);  // 第一个3
    assert(upperBound(arr, 3) == 3);  // 最后一个3

    std::cout << "✓ Bounds test passed\n";
}

int main() {
    std::cout << "Running Divide and Conquer - Binary Search Tests...\n";
    std::cout << "===================================================\n";

    test_basic_search();
    test_bounds();

    std::cout << "\n✅ All tests passed!\n";
    std::cout << "\n💡 分治算法:\n";
    std::cout << "   - 分解 (Divide): 将问题分成更小的子问题\n";
    std::cout << "   - 解决 (Conquer): 递归解决子问题\n";
    std::cout << "   - 合并 (Combine): 合并子问题的解\n";
    std::cout << "   - 二分查找: T(n) = T(n/2) + O(1) = O(log n)\n";

    return 0;
}
