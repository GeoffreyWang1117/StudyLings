/*
 * 练习: ds01_vector
 * 难度: Easy
 * 主题: 数据结构 - 动态数组
 *
 * 描述:
 * 实现一个简单的动态数组（类似 std::vector），理解其核心操作。
 *
 * 学习目标:
 * - 理解动态数组的扩容机制
 * - 掌握基本的内存管理
 * - 分析各操作的时间复杂度
 *
 * 参考: ADM 3rd Edition - Chapter 3.1
 */

#include <iostream>
#include <cassert>
#include <stdexcept>

template<typename T>
class SimpleVector {
private:
    T* data;
    size_t capacity;
    size_t size;

    void resize() {
        // TODO: 实现扩容逻辑
        // 提示: 通常扩容到当前容量的 2 倍
        // 1. 分配新的更大的数组
        // 2. 复制旧数据到新数组
        // 3. 删除旧数组
        // 4. 更新 data 和 capacity
    }

public:
    SimpleVector() : data(nullptr), capacity(0), size(0) {}

    ~SimpleVector() {
        // TODO: 释放内存
    }

    // TODO: 实现 push_back
    // 在末尾添加元素，如果容量不足则扩容
    void push_back(const T& value) {
        // 你的代码
    }

    // TODO: 实现 pop_back
    // 删除末尾元素
    void pop_back() {
        // 你的代码
    }

    // TODO: 实现 at
    // 访问指定位置的元素（带边界检查）
    T& at(size_t index) {
        // 你的代码
        throw std::out_of_range("index out of range");
    }

    const T& at(size_t index) const {
        // 你的代码
        throw std::out_of_range("index out of range");
    }

    // TODO: 实现 operator[]
    // 访问指定位置的元素（不带边界检查，更快）
    T& operator[](size_t index) {
        // 你的代码
        return data[0]; // 替换这一行
    }

    const T& operator[](size_t index) const {
        // 你的代码
        return data[0]; // 替换这一行
    }

    size_t getSize() const { return size; }
    size_t getCapacity() const { return capacity; }
    bool empty() const { return size == 0; }
};

// I AM NOT DONE

// ===== 测试代码 =====

void test_basic_operations() {
    SimpleVector<int> vec;

    assert(vec.empty() == true);
    assert(vec.getSize() == 0);

    vec.push_back(10);
    assert(vec.getSize() == 1);
    assert(vec[0] == 10);

    vec.push_back(20);
    vec.push_back(30);
    assert(vec.getSize() == 3);
    assert(vec[1] == 20);
    assert(vec[2] == 30);

    std::cout << "✓ Basic operations test passed\n";
}

void test_resizing() {
    SimpleVector<int> vec;

    // 添加多个元素，触发扩容
    for (int i = 0; i < 10; i++) {
        vec.push_back(i);
    }

    assert(vec.getSize() == 10);
    assert(vec.getCapacity() >= 10);

    for (int i = 0; i < 10; i++) {
        assert(vec[i] == i);
    }

    std::cout << "✓ Resizing test passed\n";
}

void test_pop_back() {
    SimpleVector<int> vec;

    vec.push_back(1);
    vec.push_back(2);
    vec.push_back(3);

    vec.pop_back();
    assert(vec.getSize() == 2);
    assert(vec[1] == 2);

    vec.pop_back();
    assert(vec.getSize() == 1);

    std::cout << "✓ Pop back test passed\n";
}

void test_at_bounds_checking() {
    SimpleVector<int> vec;
    vec.push_back(10);
    vec.push_back(20);

    try {
        vec.at(5); // 应该抛出异常
        assert(false); // 不应该执行到这里
    } catch (const std::out_of_range&) {
        // 期望的行为
    }

    assert(vec.at(0) == 10);
    assert(vec.at(1) == 20);

    std::cout << "✓ Bounds checking test passed\n";
}

int main() {
    std::cout << "Running Dynamic Array Tests...\n";
    std::cout << "===============================\n";

    test_basic_operations();
    test_resizing();
    test_pop_back();
    test_at_bounds_checking();

    std::cout << "\n✅ All tests passed!\n";
    std::cout << "\n💡 时间复杂度:\n";
    std::cout << "   - push_back: 摊销 O(1)\n";
    std::cout << "   - pop_back:  O(1)\n";
    std::cout << "   - operator[]: O(1)\n";
    std::cout << "   - at:        O(1)\n";

    return 0;
}
