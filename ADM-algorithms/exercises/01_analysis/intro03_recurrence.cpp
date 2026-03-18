/*
 * 练习: intro03_recurrence
 * 难度: Medium
 * 主题: 算法分析 - 递归关系式
 * 描述: 理解和求解递归关系式，分析递归算法的时间复杂度
 * 参考: ADM 3rd Edition - Chapter 2.5
 */

#include <iostream>
#include <cassert>

// TODO: 分析并实现满足 T(n) = 2T(n/2) + n 的函数
// 这是归并排序的递归关系
int recurrence_merge_sort(int n) {
    // 你的代码
    return 0;
}

// I AM NOT DONE

void test_basic() {
    assert(recurrence_merge_sort(8) > 0);
    std::cout << "✓ Basic test passed\n";
}

int main() {
    test_basic();
    std::cout << "\n✅ All tests passed!\n";
    return 0;
}
