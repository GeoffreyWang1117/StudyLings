/*
 * 练习: intro02_big_o
 * 难度: Easy
 * 主题: 算法分析 - Big-O 记号
 *
 * 描述:
 * 实现几个不同时间复杂度的函数，加深对 Big-O 记号的理解。
 *
 * 学习目标:
 * - 理解常见的时间复杂度: O(1), O(log n), O(n), O(n log n), O(n^2)
 * - 学会识别算法的时间复杂度
 * - 理解最坏情况分析
 *
 * 参考: ADM 3rd Edition - Chapter 2.3
 */

#include <iostream>
#include <vector>
#include <cassert>

// TODO: 实现一个 O(1) 常数时间的函数
// 无论输入大小如何，都应该执行固定次数的操作
int constantTime(const std::vector<int>& arr, int index) {
    // 你的代码: 返回数组中指定索引的元素
    // 提示: 数组访问是 O(1) 操作
    return 0; // 替换这一行
}

// TODO: 实现一个 O(n) 线性时间的函数
// 找出数组中的最大值
int findMax(const std::vector<int>& arr) {
    // 你的代码: 遍历数组找到最大值
    return 0; // 替换这一行
}

// TODO: 实现一个 O(n^2) 平方时间的函数
// 检查数组中是否有重复元素（使用朴素方法）
bool hasDuplicates(const std::vector<int>& arr) {
    // 你的代码: 使用两层循环检查是否有重复
    // 注意: 这不是最优解，但用于理解 O(n^2) 复杂度
    return false; // 替换这一行
}

// TODO: 实现一个 O(n log n) 时间的函数
// 计算数组中有多少对逆序对（使用归并排序的思想）
// 逆序对: i < j 但 arr[i] > arr[j]
// 提示: 这是一个较难的练习，可以先实现简单的 O(n^2) 版本
long long countInversions(std::vector<int> arr) {
    // 你的代码: 计算逆序对数量
    // 简单版本: 使用双层循环 O(n^2)
    // 高级版本: 使用归并排序 O(n log n)
    return 0; // 替换这一行
}

// I AM NOT DONE

// ===== 测试代码 =====

void test_constant_time() {
    std::vector<int> arr = {10, 20, 30, 40, 50};
    assert(constantTime(arr, 0) == 10);
    assert(constantTime(arr, 2) == 30);
    assert(constantTime(arr, 4) == 50);
    std::cout << "✓ Constant time test passed\n";
}

void test_find_max() {
    std::vector<int> arr1 = {3, 1, 4, 1, 5, 9, 2, 6};
    assert(findMax(arr1) == 9);

    std::vector<int> arr2 = {-5, -2, -8, -1};
    assert(findMax(arr2) == -1);

    std::vector<int> arr3 = {42};
    assert(findMax(arr3) == 42);

    std::cout << "✓ Find max test passed\n";
}

void test_has_duplicates() {
    std::vector<int> arr1 = {1, 2, 3, 4, 5};
    assert(hasDuplicates(arr1) == false);

    std::vector<int> arr2 = {1, 2, 3, 2, 5};
    assert(hasDuplicates(arr2) == true);

    std::vector<int> arr3 = {5, 5};
    assert(hasDuplicates(arr3) == true);

    std::cout << "✓ Has duplicates test passed\n";
}

void test_count_inversions() {
    std::vector<int> arr1 = {1, 2, 3, 4, 5};
    assert(countInversions(arr1) == 0); // 已排序，无逆序对

    std::vector<int> arr2 = {5, 4, 3, 2, 1};
    assert(countInversions(arr2) == 10); // 完全逆序: 4+3+2+1 = 10

    std::vector<int> arr3 = {2, 4, 1, 3};
    assert(countInversions(arr3) == 3); // (2,1), (4,1), (4,3)

    std::cout << "✓ Count inversions test passed\n";
}

int main() {
    std::cout << "Running Big-O Notation Tests...\n";
    std::cout << "================================\n";

    test_constant_time();
    test_find_max();
    test_has_duplicates();
    test_count_inversions();

    std::cout << "\n✅ All tests passed!\n";
    std::cout << "\n💡 复杂度总结:\n";
    std::cout << "   - constantTime:      O(1)\n";
    std::cout << "   - findMax:           O(n)\n";
    std::cout << "   - hasDuplicates:     O(n²)\n";
    std::cout << "   - countInversions:   O(n²) 或 O(n log n)\n";

    return 0;
}
