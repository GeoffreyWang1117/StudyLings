/*
 * 练习: adv_graph02_articulation_points
 * 难度: Hard
 * 主题: 高级图算法 - 割点和桥
 *
 * 描述:
 * 找出无向图中的割点（articulation points）和桥（bridges）
 *
 * 学习目标:
 * - 理解割点和桥的概念
 * - 掌握Tarjan算法
 * - 应用low-link值
 *
 * 参考: ADM 3rd Edition - Chapter 7
 */

#include <iostream>
#include <vector>
#include <algorithm>
#include <cassert>

class UndirectedGraph {
private:
    int V;
    std::vector<std::vector<int>> adj;
    std::vector<bool> visited;
    std::vector<int> disc;      // 发现时间
    std::vector<int> low;       // 最早可达祖先
    std::vector<int> parent;
    std::vector<bool> isAP;     // 是否是割点
    int timer;

    // TODO: 实现DFS找割点
    void findAPUtil(int u, std::vector<int>& articulationPoints) {
        // 你的代码
        // 使用Tarjan算法
        // low[u] = min(disc[u], low[v]对于所有子节点v, disc[w]对于所有back edges)
    }

public:
    UndirectedGraph(int vertices)
        : V(vertices), adj(vertices), visited(vertices, false),
          disc(vertices, -1), low(vertices, -1), parent(vertices, -1),
          isAP(vertices, false), timer(0) {}

    void addEdge(int u, int v) {
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    // TODO: 找出所有割点
    std::vector<int> findArticulationPoints() {
        // 你的代码
        return {};
    }

    // TODO: 找出所有桥
    std::vector<std::pair<int,int>> findBridges() {
        // 你的代码
        // 边(u,v)是桥 当且仅当 low[v] > disc[u]
        return {};
    }
};

// I AM NOT DONE

// ===== 测试代码 =====

void test_articulation_points() {
    /*
     * 0---1---2
     *     |   |
     *     3---4
     *
     * 割点: 1, 2
     */
    UndirectedGraph g(5);
    g.addEdge(0, 1);
    g.addEdge(1, 2);
    g.addEdge(2, 4);
    g.addEdge(4, 3);
    g.addEdge(3, 1);

    auto aps = g.findArticulationPoints();
    assert(aps.size() >= 1);

    std::cout << "✓ Articulation points test passed\n";
}

void test_bridges() {
    /*
     * 0---1   2---3
     *     |       |
     *     4-------5
     *
     * 桥: (1,4), (2,5)等
     */
    UndirectedGraph g(6);
    g.addEdge(0, 1);
    g.addEdge(1, 4);
    g.addEdge(2, 3);
    g.addEdge(2, 5);
    g.addEdge(4, 5);

    auto bridges = g.findBridges();
    assert(bridges.size() >= 1);

    std::cout << "✓ Bridges test passed\n";
}

int main() {
    std::cout << "Running Articulation Points and Bridges Tests...\n";
    std::cout << "================================================\n";

    test_articulation_points();
    test_bridges();

    std::cout << "\n✅ All tests passed!\n";
    std::cout << "\n💡 割点和桥:\n";
    std::cout << "   - 割点: 删除后使图不连通的点\n";
    std::cout << "   - 桥: 删除后使图不连通的边\n";
    std::cout << "   - Tarjan算法: O(V+E)\n";
    std::cout << "   - 应用: 网络脆弱性分析\n";

    return 0;
}
