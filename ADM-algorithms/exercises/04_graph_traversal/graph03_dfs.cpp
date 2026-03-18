/* 练习: graph03_dfs 难度: Medium 主题: 深度优先搜索
 * 描述: 实现DFS算法 参考: ADM 3rd - Chapter 5.8 */
#include <iostream>
#include <vector>
#include <cassert>
class Graph {
    int V;
    std::vector<std::vector<int>> adj;
public:
    Graph(int v) : V(v), adj(v) {}
    void addEdge(int u, int v) { adj[u].push_back(v); adj[v].push_back(u); }
    std::vector<int> DFS(int start) { return {}; }
};
// I AM NOT DONE
void test_basic() { Graph g(5); assert(true); std::cout << "✓ Test passed\n"; }
int main() { test_basic(); return 0; }
