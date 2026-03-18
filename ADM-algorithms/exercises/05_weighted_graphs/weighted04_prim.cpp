/* 练习: weighted04_prim 难度: Hard 主题: Prim算法
 * 描述: 实现Prim算法求最小生成树 参考: ADM 3rd - Chapter 6.1 */
#include <iostream>
#include <vector>
#include <cassert>
int prim(int n, std::vector<std::tuple<int,int,int>> edges) { return 0; }
// I AM NOT DONE
void test_basic() { int mst = prim(4, {{0,1,1},{0,2,3},{1,2,2},{1,3,4},{2,3,5}}); std::cout << "✓ Test passed\n"; }
int main() { test_basic(); return 0; }
