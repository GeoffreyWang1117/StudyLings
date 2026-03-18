/* 练习: greedy01_activity_selection 难度: Medium 主题: 活动选择 */
#include <iostream>
#include <vector>
#include <cassert>
int maxActivities(std::vector<std::pair<int,int>>& activities) { return 0; }
// I AM NOT DONE
void test_basic() { std::vector<std::pair<int,int>> act = {{1,3},{2,4},{3,5}}; assert(maxActivities(act) >= 1); std::cout << "✓ Test passed\n"; }
int main() { test_basic(); return 0; }
