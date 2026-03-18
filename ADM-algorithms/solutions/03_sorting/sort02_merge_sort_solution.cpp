/*
 * 练习: sort02_merge_sort - 参考解答
 * 难度: Medium
 * 主题: 排序 - 归并排序
 */

#include <iostream>
#include <vector>
#include <cassert>
#include <algorithm>

/*
 * 归并操作：合并两个已排序的子数组
 *
 * 参数:
 *   arr: 待排序数组
 *   left: 左边界
 *   mid: 中间位置
 *   right: 右边界
 *
 * 时间复杂度: O(n)，n = right - left + 1
 * 空间复杂度: O(n)，需要临时数组
 */
void merge(std::vector<int>& arr, int left, int mid, int right) {
    // 计算左右子数组的大小
    int n1 = mid - left + 1;
    int n2 = right - mid;

    // 创建临时数组存储左右两部分
    std::vector<int> L(n1);
    std::vector<int> R(n2);

    // 复制数据到临时数组
    for (int i = 0; i < n1; i++) {
        L[i] = arr[left + i];
    }
    for (int j = 0; j < n2; j++) {
        R[j] = arr[mid + 1 + j];
    }

    // 合并两个有序数组
    int i = 0;      // 左数组的索引
    int j = 0;      // 右数组的索引
    int k = left;   // 合并后数组的索引

    // 比较并合并
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        } else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }

    // 复制剩余的元素（如果有）
    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }

    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }
}

/*
 * 归并排序的递归实现
 *
 * 算法思路（分治法）：
 * 1. 分解：将数组分成两半
 * 2. 解决：递归地对两半进行排序
 * 3. 合并：将两个有序数组合并成一个有序数组
 *
 * 时间复杂度: O(n log n) - 所有情况
 * 空间复杂度: O(n) - 需要额外的临时数组
 *
 * 递推关系式: T(n) = 2T(n/2) + O(n)
 */
void mergeSortHelper(std::vector<int>& arr, int left, int right) {
    // 基本情况：只有一个元素或没有元素
    if (left >= right) {
        return;
    }

    // 找到中点
    int mid = left + (right - left) / 2;  // 避免溢出

    // 递归排序左半部分
    mergeSortHelper(arr, left, mid);

    // 递归排序右半部分
    mergeSortHelper(arr, mid + 1, right);

    // 合并两个有序部分
    merge(arr, left, mid, right);
}

// 公共接口
void mergeSort(std::vector<int>& arr) {
    if (arr.empty()) return;
    mergeSortHelper(arr, 0, arr.size() - 1);
}

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
    std::cout << "   - 稳定性: 稳定排序（相等元素保持原有顺序）\n";
    std::cout << "   - 特点: 分治算法的经典应用\n";
    std::cout << "\n📚 关键概念:\n";
    std::cout << "   - 分治法: 分解、解决、合并\n";
    std::cout << "   - 递归树深度: log n\n";
    std::cout << "   - 每层合并: O(n)\n";
    std::cout << "   - 总时间: O(n log n)\n";
    std::cout << "\n🔍 与快速排序对比:\n";
    std::cout << "   归并排序: 稳定、最坏 O(n log n)、需要额外空间\n";
    std::cout << "   快速排序: 不稳定、平均 O(n log n)、原地排序\n";

    return 0;
}
