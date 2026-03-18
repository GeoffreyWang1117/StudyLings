/* 练习: graph01_representation 难度: Medium 主题: 图表示
 * 描述: 实现图的邻接表和邻接矩阵表示 参考: ADM 3rd - Chapter 5 */
#include <iostream>
#include <vector>
#include <cassert>
class Graph {
public:
    Graph(int n) {}
    void addEdge(int u, int v) {}
};
// I AM NOT DONE
void test_basic() { Graph g(5); g.addEdge(0, 1); std::cout << "✓ Test passed\n"; }
int main() { test_basic(); return 0; }
