/*
 * 练习: ds04_queue
 * 难度: Easy
 * 主题: 数据结构 - 队列
 * 描述: 实现队列数据结构
 * 参考: ADM 3rd Edition - Chapter 3.2
 */

#include <iostream>
#include <cassert>

template<typename T>
class Queue {
    // TODO: 实现队列
public:
    void enqueue(const T& value) {}
    T dequeue() { return T(); }
    bool empty() const { return true; }
};

// I AM NOT DONE

void test_basic() {
    Queue<int> q;
    q.enqueue(1);
    q.enqueue(2);
    assert(!q.empty());
    std::cout << "✓ Basic test passed\n";
}

int main() {
    test_basic();
    std::cout << "\n✅ All tests passed!\n";
    return 0;
}
