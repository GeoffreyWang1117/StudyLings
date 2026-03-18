/*
 * 练习: adv_graph01_strongly_connected
 * 难度: Hard
 * 主题: 高级图算法 - 强连通分量 (SCC)
 *
 * 描述:
 * 使用Kosaraju算法或Tarjan算法找出有向图的所有强连通分量
 *
 * 学习目标:
 * - 理解强连通分量的定义
 * - 掌握Kosaraju或Tarjan算法
 * - 应用DFS解决图问题
 *
 * 参考: ADM 3rd Edition - Chapter 7 (Graph Traversal)
 */

#include <iostream>
#include <vector>
#include <stack>
#include <algorithm>
#include <cassert>

class DirectedGraph {
private:
    int V;
    std::vector<std::vector<int>> adj;
    std::vector<std::vector<int>> adjRev;  // 反向图

public:
    DirectedGraph(int vertices) : V(vertices), adj(vertices), adjRev(vertices) {}

    void addEdge(int u, int v) {
        adj[u].push_back(v);
        adjRev[v].push_back(u);  // 反向边
    }

    // TODO: 实现DFS遍历并记录完成时间
    void dfs(int v, std::vector<bool>& visited, std::stack<int>& finishStack) {
        // 你的代码
    }

    // TODO: 实现在反向图上的DFS
    void dfsReverse(int v, std::vector<bool>& visited, std::vector<int>& component) {
        // 你的代码
    }

    // TODO: 实现Kosaraju算法找强连通分量
    std::vector<std::vector<int>> findSCC() {
        // 你的代码
        // Kosaraju算法步骤:
        // 1. 在原图上DFS，记录完成时间
        // 2. 按完成时间降序处理节点
        // 3. 在反向图上DFS，每次DFS得到一个SCC
        return {};
    }

    int getVertices() const { return V; }
};

// I AM NOT DONE

// ===== 测试代码 =====

void test_basic_scc() {
    /*
     * 图结构:
     * 0 → 1 → 2
     * ↑   ↓   ↓
     * 4 ← 3 ← 2
     *
     * SCC: {0,1,2,3,4}
     */
    DirectedGraph g(5);
    g.addEdge(0, 1);
    g.addEdge(1, 2);
    g.addEdge(2, 3);
    g.addEdge(3, 4);
    g.addEdge(4, 0);

    auto sccs = g.findSCC();
    assert(sccs.size() == 1);  // 整个图是一个强连通分量

    std::cout << "✓ Basic SCC test passed\n";
}

void test_multiple_sccs() {
    /*
     * 0 → 1    2 → 3
     * ↑   ↓    ↑   ↓
     * 4 ← 3    5 ← 4
     *
     * 有多个SCC
     */
    DirectedGraph g(6);
    g.addEdge(0, 1);
    g.addEdge(1, 2);
    g.addEdge(2, 0);
    g.addEdge(3, 4);
    g.addEdge(4, 5);
    g.addEdge(5, 3);

    auto sccs = g.findSCC();
    assert(sccs.size() >= 2);

    std::cout << "✓ Multiple SCCs test passed\n";
}

int main() {
    std::cout << "Running Strongly Connected Components Tests...\n";
    std::cout << "===============================================\n";

    test_basic_scc();
    test_multiple_sccs();

    std::cout << "\n✅ All tests passed!\n";
    std::cout << "\n💡 SCC算法:\n";
    std::cout << "   - Kosaraju: 2次DFS, O(V+E)\n";
    std::cout << "   - Tarjan: 1次DFS, O(V+E)\n";
    std::cout << "   - 应用: 网络分析、程序依赖分析\n";

    return 0;
}
