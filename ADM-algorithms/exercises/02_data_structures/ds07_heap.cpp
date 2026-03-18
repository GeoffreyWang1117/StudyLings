/*
 * 练习: ds07_heap 难度: Medium 主题: 数据结构 - 堆
 * 描述: 实现最小堆和优先队列 参考: ADM 3rd - Chapter 3.5
 */
#include <iostream>
#include <vector>
#include <cassert>
class MinHeap {
public:
    void insert(int val) {}
    int extractMin() { return 0; }
    bool empty() const { return true; }
};
// I AM NOT DONE
void test_basic() {
    MinHeap heap;
    heap.insert(5);
    heap.insert(3);
    heap.insert(7);
    assert(heap.extractMin() == 3);
    std::cout << "✓ Test passed\n";
}
int main() { test_basic(); return 0; }
