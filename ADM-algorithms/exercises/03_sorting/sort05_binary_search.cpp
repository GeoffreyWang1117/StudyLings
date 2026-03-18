/*
 * 练习: sort05_binary_search 难度: Easy 主题: 二分查找
 * 描述: 实现二分查找及其变体 参考: ADM 3rd - Chapter 4.9
 */
#include <iostream>
#include <vector>
#include <cassert>
int binarySearch(const std::vector<int>& arr, int target) {
    // TODO: 实现二分查找，返回目标元素的索引，不存在返回-1
    return -1;
}
// I AM NOT DONE
void test_basic() {
    std::vector<int> arr = {1, 3, 5, 7, 9};
    assert(binarySearch(arr, 5) == 2);
    assert(binarySearch(arr, 4) == -1);
    std::cout << "✓ Test passed\n";
}
int main() { test_basic(); return 0; }
