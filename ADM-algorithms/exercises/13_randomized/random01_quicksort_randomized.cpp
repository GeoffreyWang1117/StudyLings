/*
 * 练习: random01_quicksort_randomized
 * 难度: Medium
 * 主题: 随机化算法 - 随机化快速排序
 *
 * 描述:
 * 实现随机化版本的快速排序，避免最坏情况
 *
 * 学习目标:
 * - 理解随机化如何改善算法性能
 * - 掌握随机枢轴选择
 * - 分析期望时间复杂度
 *
 * 参考: ADM 3rd Edition - Chapter 6 (Hashing and Randomized Algorithms)
 */

#include <iostream>
#include <vector>
#include <algorithm>
#include <random>
#include <cassert>

// 全局随机数生成器
std::random_device rd;
std::mt19937 gen(rd());

// TODO: 实现随机化分区
int randomizedPartition(std::vector<int>& arr, int left, int right) {
    // 你的代码
    // 1. 随机选择一个枢轴
    // 2. 将枢轴与right交换
    // 3. 执行标准分区
    return left;
}

// TODO: 实现随机化快速排序
void randomizedQuickSort(std::vector<int>& arr, int left, int right) {
    // 你的代码
}

// 公共接口
void quickSort(std::vector<int>& arr) {
    if (!arr.empty()) {
        randomizedQuickSort(arr, 0, arr.size() - 1);
    }
}

// TODO: 实现随机化选择算法（找第k小元素）
int randomizedSelect(std::vector<int>& arr, int left, int right, int k) {
    // 你的代码
    // 类似快速排序，但只递归一边
    return 0;
}

// I AM NOT DONE

// ===== 测试代码 =====

bool isSorted(const std::vector<int>& arr) {
    for (size_t i = 1; i < arr.size(); i++) {
        if (arr[i] < arr[i-1]) return false;
    }
    return true;
}

void test_randomized_sort() {
    std::vector<int> arr = {3, 7, 1, 9, 2, 8, 5, 4, 6, 0};
    quickSort(arr);

    assert(isSorted(arr));
    std::cout << "✓ Randomized sort test passed\n";
}

void test_worst_case_input() {
    // 已排序数组 - 普通快排的最坏情况
    std::vector<int> arr(100);
    for (int i = 0; i < 100; i++) {
        arr[i] = i;
    }

    quickSort(arr);
    assert(isSorted(arr));

    std::cout << "✓ Worst case input test passed\n";
}

void test_randomized_select() {
    std::vector<int> arr = {3, 7, 1, 9, 2, 8, 5, 4, 6, 0};

    // 找第5小的元素（索引4，值应该是4）
    int fifth = randomizedSelect(arr, 0, arr.size() - 1, 4);
    assert(fifth == 4);

    std::cout << "✓ Randomized select test passed\n";
}

int main() {
    std::cout << "Running Randomized Algorithms Tests...\n";
    std::cout << "=======================================\n";

    test_randomized_sort();
    test_worst_case_input();
    test_randomized_select();

    std::cout << "\n✅ All tests passed!\n";
    std::cout << "\n💡 随机化算法:\n";
    std::cout << "   - 普通快排最坏: O(n²)\n";
    std::cout << "   - 随机化快排期望: O(n log n)\n";
    std::cout << "   - 关键思想: 用随机性避免最坏情况\n";
    std::cout << "   - 实际应用: std::sort 通常使用introsort\n";

    return 0;
}
