/*
 * 练习: sort03_quick_sort 难度: Medium 主题: 快速排序
 * 描述: 实现快速排序算法 参考: ADM 3rd - Chapter 4.6
 */
#include <iostream>
#include <vector>
#include <cassert>
void quickSort(std::vector<int>& arr, int left, int right) {
    // TODO: 实现快速排序
}
void quickSort(std::vector<int>& arr) {
    if (!arr.empty()) quickSort(arr, 0, arr.size() - 1);
}
// I AM NOT DONE
void test_basic() {
    std::vector<int> arr = {5, 2, 8, 1, 9};
    quickSort(arr);
    for (size_t i = 1; i < arr.size(); i++) {
        assert(arr[i] >= arr[i-1]);
    }
    std::cout << "✓ Test passed\n";
}
int main() { test_basic(); return 0; }
