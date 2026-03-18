/*
 * 练习: ds02_linked_list
 * 难度: Medium
 * 主题: 数据结构 - 链表
 *
 * 描述:
 * 实现一个单向链表，掌握链表的基本操作。
 *
 * 学习目标:
 * - 理解指针和动态内存分配
 * - 掌握链表的插入、删除操作
 * - 理解链表 vs 数组的权衡
 *
 * 参考: ADM 3rd Edition - Chapter 3.1
 */

#include <iostream>
#include <cassert>

template<typename T>
class LinkedList {
private:
    struct Node {
        T data;
        Node* next;
        Node(const T& value) : data(value), next(nullptr) {}
    };

    Node* head;
    size_t size;

public:
    LinkedList() : head(nullptr), size(0) {}

    ~LinkedList() {
        // TODO: 释放所有节点的内存
    }

    // TODO: 在链表头部插入元素 O(1)
    void pushFront(const T& value) {
        // 你的代码
    }

    // TODO: 在链表尾部插入元素 O(n)
    void pushBack(const T& value) {
        // 你的代码
    }

    // TODO: 删除头部元素 O(1)
    void popFront() {
        // 你的代码
    }

    // TODO: 在指定位置插入元素 O(n)
    void insert(size_t index, const T& value) {
        // 你的代码
    }

    // TODO: 删除指定位置的元素 O(n)
    void erase(size_t index) {
        // 你的代码
    }

    // TODO: 访问指定位置的元素 O(n)
    T& at(size_t index) {
        // 你的代码
        static T dummy;
        return dummy; // 替换这一行
    }

    // TODO: 反转链表 O(n)
    void reverse() {
        // 你的代码
        // 提示: 使用三个指针: prev, current, next
    }

    // TODO: 检测链表中是否有环
    bool hasCycle() const {
        // 你的代码
        // 提示: 使用快慢指针（Floyd's cycle detection）
        return false;
    }

    size_t getSize() const { return size; }
    bool empty() const { return head == nullptr; }

    // 辅助函数：打印链表
    void print() const {
        Node* current = head;
        while (current != nullptr) {
            std::cout << current->data << " -> ";
            current = current->next;
        }
        std::cout << "NULL\n";
    }
};

// I AM NOT DONE

// ===== 测试代码 =====

void test_push_front() {
    LinkedList<int> list;

    list.pushFront(30);
    list.pushFront(20);
    list.pushFront(10);

    assert(list.getSize() == 3);
    assert(list.at(0) == 10);
    assert(list.at(1) == 20);
    assert(list.at(2) == 30);

    std::cout << "✓ Push front test passed\n";
}

void test_push_back() {
    LinkedList<int> list;

    list.pushBack(10);
    list.pushBack(20);
    list.pushBack(30);

    assert(list.getSize() == 3);
    assert(list.at(0) == 10);
    assert(list.at(1) == 20);
    assert(list.at(2) == 30);

    std::cout << "✓ Push back test passed\n";
}

void test_pop_front() {
    LinkedList<int> list;

    list.pushBack(10);
    list.pushBack(20);
    list.pushBack(30);

    list.popFront();
    assert(list.getSize() == 2);
    assert(list.at(0) == 20);

    list.popFront();
    assert(list.getSize() == 1);
    assert(list.at(0) == 30);

    std::cout << "✓ Pop front test passed\n";
}

void test_insert_erase() {
    LinkedList<int> list;

    list.pushBack(10);
    list.pushBack(30);
    list.insert(1, 20); // 插入到中间

    assert(list.getSize() == 3);
    assert(list.at(0) == 10);
    assert(list.at(1) == 20);
    assert(list.at(2) == 30);

    list.erase(1); // 删除中间元素
    assert(list.getSize() == 2);
    assert(list.at(0) == 10);
    assert(list.at(1) == 30);

    std::cout << "✓ Insert/erase test passed\n";
}

void test_reverse() {
    LinkedList<int> list;

    list.pushBack(1);
    list.pushBack(2);
    list.pushBack(3);
    list.pushBack(4);

    list.reverse();

    assert(list.at(0) == 4);
    assert(list.at(1) == 3);
    assert(list.at(2) == 2);
    assert(list.at(3) == 1);

    std::cout << "✓ Reverse test passed\n";
}

int main() {
    std::cout << "Running Linked List Tests...\n";
    std::cout << "============================\n";

    test_push_front();
    test_push_back();
    test_pop_front();
    test_insert_erase();
    test_reverse();

    std::cout << "\n✅ All tests passed!\n";
    std::cout << "\n💡 时间复杂度:\n";
    std::cout << "   - pushFront:  O(1)\n";
    std::cout << "   - pushBack:   O(n)\n";
    std::cout << "   - popFront:   O(1)\n";
    std::cout << "   - insert:     O(n)\n";
    std::cout << "   - erase:      O(n)\n";
    std::cout << "   - at:         O(n)\n";
    std::cout << "   - reverse:    O(n)\n";

    return 0;
}
