/* 练习: weighted06_max_flow 难度: Hard 主题: 最大流
 * 描述: 实现Ford-Fulkerson算法 参考: ADM 3rd - Chapter 6.5 */
#include <iostream>
#include <vector>
#include <cassert>
int maxFlow(int n, std::vector<std::tuple<int,int,int>> edges, int source, int sink) { return 0; }
// I AM NOT DONE
void test_basic() { int flow = maxFlow(4, {{0,1,10},{0,2,5},{1,3,10},{2,3,5}}, 0, 3); std::cout << "✓ Test passed\n"; }
int main() { test_basic(); return 0; }
