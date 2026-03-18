/* 练习: comb02_permutations 难度: Medium 主题: 全排列 */
#include <iostream>
#include <vector>
#include <cassert>
std::vector<std::vector<int>> permute(std::vector<int>& nums) { return {}; }
// I AM NOT DONE
void test_basic() { std::vector<int> nums = {1,2,3}; auto result = permute(nums); assert(result.size() == 6); std::cout << "✓ Test passed\n"; }
int main() { test_basic(); return 0; }
