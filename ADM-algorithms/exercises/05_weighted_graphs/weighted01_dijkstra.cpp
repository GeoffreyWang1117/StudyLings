/*
 * 练习: weighted01_dijkstra
 * 难度: Hard
 * 主题: 最短路径 - Dijkstra 算法
 *
 * 描述:
 * 实现 Dijkstra 算法求解单源最短路径问题。
 *
 * 学习目标:
 * - 掌握贪心算法在图问题中的应用
 * - 理解优先队列的使用
 * - 分析算法的时间复杂度
 *
 * 参考: ADM 3rd Edition - Chapter 6.3.1
 */

#include <iostream>
#include <vector>
#include <queue>
#include <limits>
#include <cassert>

const int INF = std::numeric_limits<int>::max();

class WeightedGraph {
private:
    int V;
    std::vector<std::vector<std::pair<int, int>>> adj; // {neighbor, weight}

public:
    WeightedGraph(int vertices) : V(vertices), adj(vertices) {}

    void addEdge(int u, int v, int weight) {
        adj[u].push_back({v, weight});
        adj[v].push_back({u, weight}); // 无向图
    }

    // TODO: 实现 Dijkstra 算法
    // 返回从 start 到所有其他顶点的最短距离
    std::vector<int> dijkstra(int start) {
        std::vector<int> dist(V, INF);
        // 你的代码
        // 步骤:
        // 1. 初始化距离数组，dist[start] = 0
        // 2. 使用优先队列（最小堆）存储 {distance, vertex}
        // 3. 将起点加入优先队列
        // 4. 当优先队列不空:
        //    a. 取出距离最小的顶点 u
        //    b. 如果已处理过，跳过
        //    c. 遍历 u 的所有邻居 v
        //    d. 如果 dist[u] + weight(u,v) < dist[v]，更新 dist[v]
        //    e. 将 v 加入优先队列

        return dist;
    }

    // TODO: 实现返回最短路径（不仅是距离）
    std::vector<int> shortestPath(int start, int end) {
        // 你的代码
        // 提示: 需要记录每个顶点的前驱节点
        return {};
    }
};

// I AM NOT DONE

// ===== 测试代码 =====

void test_simple_graph() {
    /*
     *     1
     *   0---1
     *   |   |
     * 4 |   | 2
     *   |   |
     *   2---3
     *     1
     */
    WeightedGraph g(4);
    g.addEdge(0, 1, 1);
    g.addEdge(0, 2, 4);
    g.addEdge(1, 3, 2);
    g.addEdge(2, 3, 1);

    auto dist = g.dijkstra(0);

    assert(dist[0] == 0);
    assert(dist[1] == 1);
    assert(dist[2] == 4);
    assert(dist[3] == 3); // 0->1->3

    std::cout << "✓ Simple graph test passed\n";
}

void test_complex_graph() {
    WeightedGraph g(6);
    g.addEdge(0, 1, 4);
    g.addEdge(0, 2, 2);
    g.addEdge(1, 2, 1);
    g.addEdge(1, 3, 5);
    g.addEdge(2, 3, 8);
    g.addEdge(2, 4, 10);
    g.addEdge(3, 4, 2);
    g.addEdge(3, 5, 6);
    g.addEdge(4, 5, 3);

    auto dist = g.dijkstra(0);

    assert(dist[0] == 0);
    assert(dist[1] == 3); // 0->2->1
    assert(dist[2] == 2);
    assert(dist[3] == 8); // 0->2->1->3
    assert(dist[4] == 10);
    assert(dist[5] == 13);

    std::cout << "✓ Complex graph test passed\n";
}

void test_disconnected() {
    WeightedGraph g(4);
    g.addEdge(0, 1, 1);
    g.addEdge(2, 3, 1);

    auto dist = g.dijkstra(0);

    assert(dist[0] == 0);
    assert(dist[1] == 1);
    assert(dist[2] == INF); // 不可达
    assert(dist[3] == INF);

    std::cout << "✓ Disconnected graph test passed\n";
}

int main() {
    std::cout << "Running Dijkstra Algorithm Tests...\n";
    std::cout << "====================================\n";

    test_simple_graph();
    test_complex_graph();
    test_disconnected();

    std::cout << "\n✅ All tests passed!\n";
    std::cout << "\n💡 Dijkstra 算法分析:\n";
    std::cout << "   - 时间复杂度: O((V+E) log V) 使用优先队列\n";
    std::cout << "   - 空间复杂度: O(V)\n";
    std::cout << "   - 不适用于负权边\n";
    std::cout << "   - 贪心算法的经典应用\n";

    return 0;
}
