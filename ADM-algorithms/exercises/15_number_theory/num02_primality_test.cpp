/*
 * 练习: num02_primality_test
 * 难度: Medium
 * 主题: 数论算法 - 素数测试
 *
 * 描述:
 * 实现多种素数测试算法，包括试除法、Miller-Rabin等
 *
 * 学习目标:
 * - 掌握基本的素数测试
 * - 理解概率素数测试
 * - 学习Sieve of Eratosthenes
 *
 * 参考: ADM 3rd Edition - Chapter 16
 */

#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include <cassert>

// TODO: 实现试除法素数测试
bool isPrimeTrialDivision(long long n) {
    // 你的代码
    // 检查2到sqrt(n)的所有因子
    return false;
}

// TODO: 实现埃拉托斯特尼筛法
std::vector<int> sieveOfEratosthenes(int n) {
    // 你的代码
    // 返回所有小于等于n的素数
    return {};
}

// TODO: 实现Miller-Rabin素数测试
bool millerRabin(long long n, int k = 5) {
    // 你的代码
    // k是测试轮数，k越大准确率越高
    // 这是一个概率算法
    return false;
}

// 快速幂取模
long long powerMod(long long base, long long exp, long long mod) {
    long long result = 1;
    base %= mod;
    while (exp > 0) {
        if (exp & 1) result = (result * base) % mod;
        base = (base * base) % mod;
        exp >>= 1;
    }
    return result;
}

// I AM NOT DONE

// ===== 测试代码 =====

void test_trial_division() {
    assert(isPrimeTrialDivision(2) == true);
    assert(isPrimeTrialDivision(17) == true);
    assert(isPrimeTrialDivision(100) == false);
    assert(isPrimeTrialDivision(97) == true);

    std::cout << "✓ Trial division test passed\n";
}

void test_sieve() {
    auto primes = sieveOfEratosthenes(30);

    // 30以内的素数: 2,3,5,7,11,13,17,19,23,29
    assert(primes.size() == 10);
    assert(primes[0] == 2);
    assert(primes[9] == 29);

    std::cout << "✓ Sieve of Eratosthenes test passed\n";
}

void test_miller_rabin() {
    // 测试已知素数
    assert(millerRabin(2) == true);
    assert(millerRabin(17) == true);
    assert(millerRabin(97) == true);

    // 测试合数
    assert(millerRabin(100) == false);
    assert(millerRabin(561) == false);  // Carmichael数

    // 测试大素数
    assert(millerRabin(1000000007) == true);

    std::cout << "✓ Miller-Rabin test passed\n";
}

int main() {
    std::cout << "Running Primality Testing Tests...\n";
    std::cout << "===================================\n";

    test_trial_division();
    test_sieve();
    test_miller_rabin();

    std::cout << "\n✅ All tests passed!\n";
    std::cout << "\n💡 素数测试算法:\n";
    std::cout << "   - 试除法: O(√n), 确定性\n";
    std::cout << "   - Sieve: O(n log log n), 批量生成\n";
    std::cout << "   - Miller-Rabin: O(k log³ n), 概率性\n";
    std::cout << "   - 应用: 密码学、RSA算法\n";

    return 0;
}
