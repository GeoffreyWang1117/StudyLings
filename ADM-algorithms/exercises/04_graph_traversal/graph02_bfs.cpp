/*
 * 练习: graph02_bfs
 * 难度: Medium
 * 主题: 图遍历 - 广度优先搜索 (BFS)
 *
 * 描述:
 * 实现广度优先搜索算法，这是图算法的基础。
 *
 * 学习目标:
 * - 理解 BFS 的工作原理
 * - 掌握队列在 BFS 中的应用
 * - 应用 BFS 求解最短路径问题
 *
 * 参考: ADM 3rd Edition - Chapter 5.6
 */

#include <iostream>
#include <vector>
#include <queue>
#include <cassert>

class Graph {
private:
    int V; // 顶点数
    std::vector<std::vector<int>> adj; // 邻接表

public:
    Graph(int vertices) : V(vertices), adj(vertices) {}

    void addEdge(int u, int v) {
        adj[u].push_back(v);
        adj[v].push_back(u); // 无向图
    }

    // TODO: 实现 BFS 遍历
    // 从起点 start 开始进行广度优先搜索
    // 返回访问顶点的顺序
    std::vector<int> BFS(int start) {
        std::vector<int> result;
        // 你的代码
        // 步骤:
        // 1. 创建 visited 数组标记已访问的顶点
        // 2. 创建队列，将起点入队
        // 3. 当队列不空时:
        //    a. 取出队首元素
        //    b. 访问该顶点（加入 result）
        //    c. 将所有未访问的邻居入队
        return result;
    }

    // TODO: 实现求最短路径
    // 返回从 start 到 end 的最短路径长度
    // 如果不可达，返回 -1
    int shortestPath(int start, int end) {
        // 你的代码
        // 提示: 使用 BFS，同时记录每个顶点的距离
        return -1;
    }

    // TODO: 检查图是否是二分图
    // 二分图: 可以将顶点分为两组，同组内的顶点之间没有边
    bool isBipartite() {
        // 你的代码
        // 提示: 使用 BFS 和二染色算法
        return false;
    }

    int getVertices() const { return V; }
};

// I AM NOT DONE

// ===== 测试代码 =====

void test_simple_bfs() {
    /*
     *   0 --- 1 --- 2
     *   |     |
     *   3 --- 4
     */
    Graph g(5);
    g.addEdge(0, 1);
    g.addEdge(0, 3);
    g.addEdge(1, 2);
    g.addEdge(1, 4);
    g.addEdge(3, 4);

    auto result = g.BFS(0);

    // BFS 从 0 开始: 0 -> 1, 3 -> 2, 4
    assert(result.size() == 5);
    assert(result[0] == 0);

    std::cout << "✓ Simple BFS test passed\n";
}

void test_shortest_path() {
    /*
     *   0 --- 1 --- 2
     *   |           |
     *   3 --- 4 --- 5
     */
    Graph g(6);
    g.addEdge(0, 1);
    g.addEdge(1, 2);
    g.addEdge(0, 3);
    g.addEdge(3, 4);
    g.addEdge(4, 5);
    g.addEdge(2, 5);

    assert(g.shortestPath(0, 2) == 2); // 0 -> 1 -> 2
    assert(g.shortestPath(0, 5) == 3); // 0 -> 1 -> 2 -> 5 或 0 -> 3 -> 4 -> 5
    assert(g.shortestPath(1, 4) == 3); // 1 -> 0 -> 3 -> 4

    std::cout << "✓ Shortest path test passed\n";
}

void test_disconnected_graph() {
    /*
     *   0 --- 1       2 --- 3
     */
    Graph g(4);
    g.addEdge(0, 1);
    g.addEdge(2, 3);

    auto result = g.BFS(0);
    assert(result.size() == 2); // 只能访问到 0 和 1

    assert(g.shortestPath(0, 3) == -1); // 不连通

    std::cout << "✓ Disconnected graph test passed\n";
}

void test_bipartite() {
    // 二分图
    Graph g1(4);
    g1.addEdge(0, 1);
    g1.addEdge(0, 3);
    g1.addEdge(1, 2);
    g1.addEdge(2, 3);
    assert(g1.isBipartite() == true);

    // 非二分图（包含奇数环）
    Graph g2(3);
    g2.addEdge(0, 1);
    g2.addEdge(1, 2);
    g2.addEdge(2, 0);
    assert(g2.isBipartite() == false);

    std::cout << "✓ Bipartite test passed\n";
}

int main() {
    std::cout << "Running BFS Tests...\n";
    std::cout << "====================\n";

    test_simple_bfs();
    test_shortest_path();
    test_disconnected_graph();
    test_bipartite();

    std::cout << "\n✅ All tests passed!\n";
    std::cout << "\n💡 BFS 分析:\n";
    std::cout << "   - 时间复杂度: O(V + E)\n";
    std::cout << "   - 空间复杂度: O(V)\n";
    std::cout << "   - 应用: 最短路径、层序遍历、二分图检测\n";

    return 0;
}
