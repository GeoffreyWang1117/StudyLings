/* 练习: graph06_cycle_detection 难度: Medium
 * 主题: 环检测 描述: 检测图中是否有环 参考: ADM 3rd - Chapter 5 */
#include <iostream>
#include <vector>
#include <cassert>
bool hasCycle(int n, std::vector<std::pair<int,int>> edges) { return false; }
// I AM NOT DONE
void test_basic() { assert(hasCycle(3, {{0,1},{1,2},{2,0}}) == true); std::cout << "✓ Test passed\n"; }
int main() { test_basic(); return 0; }
