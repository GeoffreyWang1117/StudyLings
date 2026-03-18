/*
 * 练习: sort06_quick_select 难度: Medium 主题: 选择算法
 * 描述: 实现快速选择算法，找第k小元素 参考: ADM 3rd - Chapter 4.7
 */
#include <iostream>
#include <vector>
#include <cassert>
int quickSelect(std::vector<int>& arr, int k) {
    // TODO: 找到第k小的元素 (k从0开始)
    return 0;
}
// I AM NOT DONE
void test_basic() {
    std::vector<int> arr = {3, 2, 1, 5, 4};
    assert(quickSelect(arr, 0) == 1);
    assert(quickSelect(arr, 2) == 3);
    std::cout << "✓ Test passed\n";
}
int main() { test_basic(); return 0; }
