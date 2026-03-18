/*
 * 练习: num01_gcd_lcm
 * 难度: Easy
 * 主题: 数论算法 - 最大公约数和最小公倍数
 *
 * 描述:
 * 实现欧几里得算法求GCD，以及相关的数论算法
 *
 * 学习目标:
 * - 掌握欧几里得算法
 * - 理解GCD和LCM的关系
 * - 学习扩展欧几里得算法
 *
 * 参考: ADM 3rd Edition - Chapter 16 (Numerical Problems)
 */

#include <iostream>
#include <cassert>
#include <numeric>

// TODO: 实现欧几里得算法求GCD
int gcd(int a, int b) {
    // 你的代码
    // 欧几里得算法: gcd(a,b) = gcd(b, a%b)
    // 直到b=0，返回a
    return 0;
}

// TODO: 实现LCM（最小公倍数）
int lcm(int a, int b) {
    // 你的代码
    // 提示: lcm(a,b) * gcd(a,b) = a * b
    return 0;
}

// TODO: 实现扩展欧几里得算法
// 返回值d = gcd(a,b)，同时找到x,y使得 ax + by = d
int extendedGCD(int a, int b, int& x, int& y) {
    // 你的代码
    // 用于求模逆元等问题
    return 0;
}

// TODO: 求a在模m下的逆元
// 返回x使得 (a * x) % m = 1
int modInverse(int a, int m) {
    // 你的代码
    // 使用扩展欧几里得算法
    return 0;
}

// I AM NOT DONE

// ===== 测试代码 =====

void test_gcd() {
    assert(gcd(48, 18) == 6);
    assert(gcd(100, 50) == 50);
    assert(gcd(17, 19) == 1);  // 互质

    std::cout << "✓ GCD test passed\n";
}

void test_lcm() {
    assert(lcm(4, 6) == 12);
    assert(lcm(21, 6) == 42);

    std::cout << "✓ LCM test passed\n";
}

void test_extended_gcd() {
    int x, y;
    int d = extendedGCD(30, 20, x, y);

    assert(d == 10);
    assert(30 * x + 20 * y == d);

    std::cout << "✓ Extended GCD test passed\n";
}

void test_mod_inverse() {
    int inv = modInverse(3, 11);
    assert((3 * inv) % 11 == 1);

    std::cout << "✓ Modular inverse test passed\n";
}

int main() {
    std::cout << "Running Number Theory Tests...\n";
    std::cout << "===============================\n";

    test_gcd();
    test_lcm();
    test_extended_gcd();
    test_mod_inverse();

    std::cout << "\n✅ All tests passed!\n";
    std::cout << "\n💡 数论算法:\n";
    std::cout << "   - GCD: O(log min(a,b))\n";
    std::cout << "   - 应用: 密码学、分数化简、同余方程\n";

    return 0;
}
