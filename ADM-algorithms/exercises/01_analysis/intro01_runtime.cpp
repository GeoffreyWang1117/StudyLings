/*
 * 练习: intro01_runtime
 * 难度: Easy
 * 主题: 算法分析 - 运行时间分析
 *
 * 描述:
 * 分析以下几个函数的时间复杂度，并实现一个计数器来验证。
 * 这个练习帮助你理解如何分析算法的运行时间。
 *
 * 学习目标:
 * - 理解基本操作的计数
 * - 识别循环的迭代次数
 * - 计算算法的时间复杂度
 *
 * 参考: ADM 3rd Edition - Chapter 2
 */

#include <iostream>
#include <cassert>

// TODO: 分析这个函数的时间复杂度并实现它
// 这个函数应该返回执行基本操作的次数
// 提示: 这是一个简单的单层循环
long long countOperations_Linear(int n) {
    // 你的代码: 实现一个 O(n) 的函数
    // 返回基本操作执行的次数
    return 0; // 替换这一行
}

// TODO: 分析这个函数的时间复杂度并实现它
// 这是一个嵌套循环的例子
long long countOperations_Quadratic(int n) {
    // 你的代码: 实现一个 O(n^2) 的函数
    // 返回基本操作执行的次数
    return 0; // 替换这一行
}

// TODO: 分析这个函数的时间复杂度并实现它
// 这是一个对数时间复杂度的例子
long long countOperations_Logarithmic(int n) {
    // 你的代码: 实现一个 O(log n) 的函数
    // 提示: 想想二分查找的过程
    // 返回基本操作执行的次数
    return 0; // 替换这一行
}

// I AM NOT DONE

// ===== 测试代码 =====

void test_linear() {
    // O(n) 应该大约执行 n 次操作
    assert(countOperations_Linear(10) == 10);
    assert(countOperations_Linear(100) == 100);
    assert(countOperations_Linear(1000) == 1000);
    std::cout << "✓ Linear time complexity test passed\n";
}

void test_quadratic() {
    // O(n^2) 应该执行约 n^2 次操作
    assert(countOperations_Quadratic(5) == 25);
    assert(countOperations_Quadratic(10) == 100);
    assert(countOperations_Quadratic(20) == 400);
    std::cout << "✓ Quadratic time complexity test passed\n";
}

void test_logarithmic() {
    // O(log n) 应该执行约 log2(n) 次操作
    long long ops = countOperations_Logarithmic(1024);
    assert(ops >= 10 && ops <= 11); // log2(1024) = 10

    ops = countOperations_Logarithmic(1000000);
    assert(ops >= 19 && ops <= 21); // log2(1000000) ≈ 19.93

    std::cout << "✓ Logarithmic time complexity test passed\n";
}

int main() {
    std::cout << "Running Algorithm Analysis Tests...\n";
    std::cout << "====================================\n";

    test_linear();
    test_quadratic();
    test_logarithmic();

    std::cout << "\n✅ All tests passed!\n";
    return 0;
}
