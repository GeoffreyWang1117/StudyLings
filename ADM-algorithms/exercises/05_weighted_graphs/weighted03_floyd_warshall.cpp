/* 练习: weighted03_floyd_warshall 难度: Hard 主题: Floyd-Warshall算法
 * 描述: 实现全源最短路径算法 参考: ADM 3rd - Chapter 6.1 */
#include <iostream>
#include <vector>
#include <cassert>
std::vector<std::vector<int>> floydWarshall(int n, std::vector<std::tuple<int,int,int>> edges) { return std::vector<std::vector<int>>(n, std::vector<int>(n)); }
// I AM NOT DONE
void test_basic() { auto dist = floydWarshall(3, {{0,1,1},{1,2,2}}); std::cout << "✓ Test passed\n"; }
int main() { test_basic(); return 0; }
