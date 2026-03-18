/*
 * 练习: sort04_heap_sort 难度: Medium 主题: 堆排序
 * 描述: 实现堆排序 参考: ADM 3rd - Chapter 4.3
 */
#include <iostream>
#include <vector>
#include <cassert>
void heapSort(std::vector<int>& arr) {
    // TODO: 实现堆排序
}
// I AM NOT DONE
void test_basic() {
    std::vector<int> arr = {5, 2, 8, 1, 9};
    heapSort(arr);
    for (size_t i = 1; i < arr.size(); i++) {
        assert(arr[i] >= arr[i-1]);
    }
    std::cout << "✓ Test passed\n";
}
int main() { test_basic(); return 0; }
