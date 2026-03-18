/*
 * 练习: dp01_fibonacci
 * 难度: Easy
 * 主题: 动态规划 - 斐波那契数列
 *
 * 描述:
 * 通过斐波那契数列学习动态规划的基本思想。
 * 这是理解记忆化和自底向上方法的经典入门问题。
 *
 * 学习目标:
 * - 理解递归的重复计算问题
 * - 掌握记忆化（自顶向下）
 * - 掌握动态规划（自底向上）
 * - 分析时间和空间复杂度的改进
 *
 * 参考: ADM 3rd Edition - Chapter 8.1
 */

#include <iostream>
#include <vector>
#include <cassert>
#include <chrono>

// 朴素递归版本 - 时间复杂度 O(2^n)
// 这个版本已经实现，用于对比
long long fib_naive(int n) {
    if (n <= 1) return n;
    return fib_naive(n - 1) + fib_naive(n - 2);
}

// TODO: 实现记忆化版本 - 时间复杂度 O(n), 空间复杂度 O(n)
// 使用一个数组（或哈希表）存储已经计算过的值
long long fib_memo(int n, std::vector<long long>& memo) {
    // 你的代码
    // 步骤:
    // 1. 基本情况: n <= 1 时返回 n
    // 2. 检查 memo[n] 是否已经计算过
    // 3. 如果没有，递归计算并存储到 memo[n]
    // 4. 返回 memo[n]
    return 0;
}

// 辅助函数
long long fibonacci_memoized(int n) {
    std::vector<long long> memo(n + 1, -1);
    return fib_memo(n, memo);
}

// TODO: 实现动态规划版本（自底向上）
// 时间复杂度 O(n), 空间复杂度 O(n)
long long fib_dp(int n) {
    // 你的代码
    // 步骤:
    // 1. 创建 dp 数组，dp[i] 表示第 i 个斐波那契数
    // 2. 初始化 dp[0] = 0, dp[1] = 1
    // 3. 从 2 到 n 循环，dp[i] = dp[i-1] + dp[i-2]
    // 4. 返回 dp[n]
    return 0;
}

// TODO: 实现空间优化的动态规划版本
// 时间复杂度 O(n), 空间复杂度 O(1)
long long fib_optimized(int n) {
    // 你的代码
    // 提示: 注意到我们只需要前两个数，不需要整个数组
    // 使用两个变量 prev 和 curr 即可
    return 0;
}

// I AM NOT DONE

// ===== 测试代码 =====

void test_correctness() {
    // 斐波那契数列: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, ...
    assert(fibonacci_memoized(0) == 0);
    assert(fibonacci_memoized(1) == 1);
    assert(fibonacci_memoized(2) == 1);
    assert(fibonacci_memoized(3) == 2);
    assert(fibonacci_memoized(4) == 3);
    assert(fibonacci_memoized(5) == 5);
    assert(fibonacci_memoized(10) == 55);

    assert(fib_dp(0) == 0);
    assert(fib_dp(1) == 1);
    assert(fib_dp(5) == 5);
    assert(fib_dp(10) == 55);

    assert(fib_optimized(0) == 0);
    assert(fib_optimized(1) == 1);
    assert(fib_optimized(5) == 5);
    assert(fib_optimized(10) == 55);

    std::cout << "✓ Correctness test passed\n";
}

void test_large_values() {
    // 测试较大的值
    assert(fibonacci_memoized(20) == 6765);
    assert(fib_dp(20) == 6765);
    assert(fib_optimized(20) == 6765);

    assert(fibonacci_memoized(30) == 832040);
    assert(fib_dp(30) == 832040);
    assert(fib_optimized(30) == 832040);

    std::cout << "✓ Large values test passed\n";
}

void benchmark() {
    std::cout << "\n⏱️  性能对比 (计算 fib(35)):\n";
    std::cout << "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n";

    // 朴素递归（警告：很慢！）
    auto start = std::chrono::high_resolution_clock::now();
    long long result1 = fib_naive(35);
    auto end = std::chrono::high_resolution_clock::now();
    auto duration1 = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    std::cout << "朴素递归:     " << duration1.count() << " ms (结果: " << result1 << ")\n";

    // 记忆化
    start = std::chrono::high_resolution_clock::now();
    long long result2 = fibonacci_memoized(35);
    end = std::chrono::high_resolution_clock::now();
    auto duration2 = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    std::cout << "记忆化:       " << duration2.count() << " μs (结果: " << result2 << ")\n";

    // 动态规划
    start = std::chrono::high_resolution_clock::now();
    long long result3 = fib_dp(35);
    end = std::chrono::high_resolution_clock::now();
    auto duration3 = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    std::cout << "动态规划:     " << duration3.count() << " μs (结果: " << result3 << ")\n";

    // 空间优化
    start = std::chrono::high_resolution_clock::now();
    long long result4 = fib_optimized(35);
    end = std::chrono::high_resolution_clock::now();
    auto duration4 = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    std::cout << "空间优化:     " << duration4.count() << " μs (结果: " << result4 << ")\n";

    std::cout << "\n速度提升: " << (duration1.count() * 1000.0) / duration2.count() << "x\n";
}

int main() {
    std::cout << "Running Fibonacci DP Tests...\n";
    std::cout << "==============================\n";

    test_correctness();
    test_large_values();
    benchmark();

    std::cout << "\n✅ All tests passed!\n";
    std::cout << "\n💡 动态规划优化总结:\n";
    std::cout << "   朴素递归:   时间 O(2^n), 空间 O(n)\n";
    std::cout << "   记忆化:     时间 O(n),   空间 O(n)\n";
    std::cout << "   DP:         时间 O(n),   空间 O(n)\n";
    std::cout << "   空间优化:   时间 O(n),   空间 O(1)\n";

    return 0;
}
