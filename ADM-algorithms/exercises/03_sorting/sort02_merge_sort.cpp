/*
 * 练习: sort02_merge_sort
 * 难度: Medium
 * 主题: 排序 - 归并排序
 *
 * 描述:
 * 实现归并排序算法，这是理解分治法的经典例子。
 *
 * 学习目标:
 * - 掌握分治算法的思想
 * - 理解递归的应用
 * - 分析归并排序的时间复杂度 O(n log n)
 *
 * 参考: ADM 3rd Edition - Chapter 4.5
 */

#include <iostream>
#include <vector>
#include <cassert>
#include <algorithm>

// TODO: 实现归并操作
// 合并两个已排序的子数组 arr[left..mid] 和 arr[mid+1..right]
void merge(std::vector<int>& arr, int left, int mid, int right) {
    // 你的代码
    // 步骤:
    // 1. 创建临时数组存储左右两部分
    // 2. 使用双指针合并两个有序数组
    // 3. 将结果复制回原数组
}

// TODO: 实现归并排序
// 对 arr[left..right] 进行排序
void mergeSortHelper(std::vector<int>& arr, int left, int right) {
    // 你的代码
    // 基本情况: 如果 left >= right，数组只有一个元素，已经有序
    // 递归情况:
    // 1. 找到中点 mid
    // 2. 递归排序左半部分
    // 3. 递归排序右半部分
    // 4. 合并两个有序部分
}

// 归并排序的公共接口
void mergeSort(std::vector<int>& arr) {
    if (arr.empty()) return;
    mergeSortHelper(arr, 0, arr.size() - 1);
}

// I AM NOT DONE

// ===== 测试代码 =====

bool isSorted(const std::vector<int>& arr) {
    for (size_t i = 1; i < arr.size(); i++) {
        if (arr[i] < arr[i-1]) return false;
    }
    return true;
}

void test_empty_and_single() {
    std::vector<int> arr1;
    mergeSort(arr1);
    assert(arr1.empty());

    std::vector<int> arr2 = {42};
    mergeSort(arr2);
    assert(arr2.size() == 1 && arr2[0] == 42);

    std::cout << "✓ Empty and single element test passed\n";
}

void test_already_sorted() {
    std::vector<int> arr = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    mergeSort(arr);

    assert(isSorted(arr));
    assert(arr[0] == 1 && arr[9] == 10);

    std::cout << "✓ Already sorted test passed\n";
}

void test_reverse_sorted() {
    std::vector<int> arr = {10, 9, 8, 7, 6, 5, 4, 3, 2, 1};
    mergeSort(arr);

    assert(isSorted(arr));
    assert(arr[0] == 1 && arr[9] == 10);

    std::cout << "✓ Reverse sorted test passed\n";
}

void test_random_order() {
    std::vector<int> arr = {3, 7, 1, 9, 2, 8, 5, 4, 6, 0};
    mergeSort(arr);

    assert(isSorted(arr));
    assert(arr.size() == 10);

    for (int i = 0; i < 10; i++) {
        assert(arr[i] == i);
    }

    std::cout << "✓ Random order test passed\n";
}

void test_duplicates() {
    std::vector<int> arr = {5, 2, 8, 2, 9, 1, 5, 5};
    mergeSort(arr);

    assert(isSorted(arr));
    std::vector<int> expected = {1, 2, 2, 5, 5, 5, 8, 9};
    assert(arr == expected);

    std::cout << "✓ Duplicates test passed\n";
}

void test_large_array() {
    std::vector<int> arr(1000);
    for (int i = 0; i < 1000; i++) {
        arr[i] = 1000 - i;
    }

    mergeSort(arr);

    assert(isSorted(arr));
    assert(arr[0] == 1 && arr[999] == 1000);

    std::cout << "✓ Large array test passed\n";
}

int main() {
    std::cout << "Running Merge Sort Tests...\n";
    std::cout << "===========================\n";

    test_empty_and_single();
    test_already_sorted();
    test_reverse_sorted();
    test_random_order();
    test_duplicates();
    test_large_array();

    std::cout << "\n✅ All tests passed!\n";
    std::cout << "\n💡 归并排序分析:\n";
    std::cout << "   - 时间复杂度: O(n log n) - 最好、平均、最坏情况都是\n";
    std::cout << "   - 空间复杂度: O(n) - 需要额外的临时数组\n";
    std::cout << "   - 稳定性: 稳定排序\n";
    std::cout << "   - 特点: 分治算法的经典应用\n";

    return 0;
}
