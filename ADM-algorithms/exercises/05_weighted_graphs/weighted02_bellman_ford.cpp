/* 练习: weighted02_bellman_ford 难度: Hard 主题: Bellman-Ford算法
 * 描述: 实现Bellman-Ford算法（支持负权边）参考: ADM 3rd - Chapter 6.3.2 */
#include <iostream>
#include <vector>
#include <limits>
#include <cassert>
const int INF = std::numeric_limits<int>::max();
std::vector<int> bellmanFord(int n, std::vector<std::tuple<int,int,int>> edges, int start) { return std::vector<int>(n, INF); }
// I AM NOT DONE
void test_basic() { auto dist = bellmanFord(3, {{0,1,1},{1,2,2}}, 0); std::cout << "✓ Test passed\n"; }
int main() { test_basic(); return 0; }
