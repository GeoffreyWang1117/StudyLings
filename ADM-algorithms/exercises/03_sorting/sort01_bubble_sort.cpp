/*
 * 练习: sort01_bubble_sort 难度: Easy 主题: 排序
 * 描述: 实现冒泡排序 参考: ADM 3rd - Chapter 4
 */
#include <iostream>
#include <vector>
#include <cassert>
void bubbleSort(std::vector<int>& arr) {
    // TODO: 实现冒泡排序
}
// I AM NOT DONE
void test_basic() {
    std::vector<int> arr = {5, 2, 8, 1, 9};
    bubbleSort(arr);
    for (size_t i = 1; i < arr.size(); i++) {
        assert(arr[i] >= arr[i-1]);
    }
    std::cout << "✓ Test passed\n";
}
int main() { test_basic(); return 0; }
