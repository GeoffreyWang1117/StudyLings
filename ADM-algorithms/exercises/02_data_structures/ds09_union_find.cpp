/*
 * 练习: ds09_union_find 难度: Medium 主题: 并查集
 * 描述: 实现并查集（路径压缩+按秩合并）参考: ADM 3rd - Chapter 6.1
 */
#include <iostream>
#include <vector>
#include <cassert>
class UnionFind {
public:
    UnionFind(int n) {}
    int find(int x) { return 0; }
    void unite(int x, int y) {}
    bool connected(int x, int y) { return false; }
};
// I AM NOT DONE
void test_basic() {
    UnionFind uf(5);
    uf.unite(0, 1);
    assert(uf.connected(0, 1));
    std::cout << "✓ Test passed\n";
}
int main() { test_basic(); return 0; }
