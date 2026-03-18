/*
 * 练习: intro01_runtime - 参考解答
 * 难度: Easy
 * 主题: 算法分析 - 运行时间分析
 */

#include <iostream>
#include <cassert>

/*
 * 解法说明：
 *
 * 1. Linear Time O(n):
 *    - 使用一个简单的循环，执行 n 次
 *    - 每次循环是一个基本操作
 *    - 总操作数 = n
 */
long long countOperations_Linear(int n) {
    long long count = 0;
    for (int i = 0; i < n; i++) {
        count++;  // 每次循环计数一次
    }
    return count;
}

/*
 * 2. Quadratic Time O(n^2):
 *    - 使用嵌套循环
 *    - 外层循环 n 次，内层循环也 n 次
 *    - 总操作数 = n * n = n^2
 */
long long countOperations_Quadratic(int n) {
    long long count = 0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            count++;  // 每次内层循环计数一次
        }
    }
    return count;
}

/*
 * 3. Logarithmic Time O(log n):
 *    - 每次循环将问题规模减半（类似二分查找）
 *    - 操作次数 = log2(n)
 *    - 例如：n=1024 时，只需要约 10 次操作
 */
long long countOperations_Logarithmic(int n) {
    long long count = 0;
    while (n > 0) {
        count++;
        n /= 2;  // 每次减半
    }
    return count;
}

// ===== 测试代码 =====

void test_linear() {
    assert(countOperations_Linear(10) == 10);
    assert(countOperations_Linear(100) == 100);
    assert(countOperations_Linear(1000) == 1000);
    std::cout << "✓ Linear time complexity test passed\n";
}

void test_quadratic() {
    assert(countOperations_Quadratic(5) == 25);
    assert(countOperations_Quadratic(10) == 100);
    assert(countOperations_Quadratic(20) == 400);
    std::cout << "✓ Quadratic time complexity test passed\n";
}

void test_logarithmic() {
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

    // 演示不同复杂度的差异
    std::cout << "\n📊 操作次数对比 (n=100):\n";
    std::cout << "   O(log n): " << countOperations_Logarithmic(100) << " 次\n";
    std::cout << "   O(n):     " << countOperations_Linear(100) << " 次\n";
    std::cout << "   O(n²):    " << countOperations_Quadratic(100) << " 次\n";

    return 0;
}
