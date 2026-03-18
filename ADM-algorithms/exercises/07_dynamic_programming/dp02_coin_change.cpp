/* 练习: dp02_coin_change 难度: Medium 主题: 硬币找零 */
#include <iostream>
#include <vector>
#include <cassert>
int coinChange(std::vector<int>& coins, int amount) { return -1; }
// I AM NOT DONE
void test_basic() { std::vector<int> coins = {1,2,5}; assert(coinChange(coins, 11) == 3); std::cout << "✓ Test passed\n"; }
int main() { test_basic(); return 0; }
