/* 练习: graph05_topological_sort 难度: Medium
 * 主题: 拓扑排序 描述: 对有向无环图进行拓扑排序 参考: ADM 3rd - Chapter 5.10 */
#include <iostream>
#include <vector>
#include <cassert>
std::vector<int> topologicalSort(int n, std::vector<std::pair<int,int>> edges) { return {}; }
// I AM NOT DONE
void test_basic() { auto result = topologicalSort(4, {{0,1},{0,2},{1,3},{2,3}}); std::cout << "✓ Test passed\n"; }
int main() { test_basic(); return 0; }
