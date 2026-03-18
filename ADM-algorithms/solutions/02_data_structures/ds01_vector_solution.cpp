/*
 * 练习: ds01_vector - 参考解答
 * 难度: Easy
 * 主题: 数据结构 - 动态数组
 */

#include <iostream>
#include <cassert>
#include <stdexcept>
#include <algorithm>

template<typename T>
class SimpleVector {
private:
    T* data;
    size_t capacity;
    size_t size;

    /*
     * 扩容策略：容量翻倍
     *
     * 为什么翻倍？
     * - 摊销时间复杂度为 O(1)
     * - 如果每次只增加固定大小（如+1），则为 O(n)
     * - 翻倍策略平衡了时间和空间效率
     */
    void resize() {
        // 初始容量为 1，之后每次翻倍
        size_t new_capacity = (capacity == 0) ? 1 : capacity * 2;

        // 分配新内存
        T* new_data = new T[new_capacity];

        // 复制旧数据
        for (size_t i = 0; i < size; i++) {
            new_data[i] = data[i];
        }

        // 释放旧内存
        delete[] data;

        // 更新指针和容量
        data = new_data;
        capacity = new_capacity;
    }

public:
    SimpleVector() : data(nullptr), capacity(0), size(0) {}

    ~SimpleVector() {
        delete[] data;  // 释放动态分配的内存
    }

    /*
     * push_back: 在末尾添加元素
     * 时间复杂度：摊销 O(1)
     * - 大多数情况下直接添加：O(1)
     * - 偶尔需要扩容：O(n)
     * - 平均下来：O(1)
     */
    void push_back(const T& value) {
        if (size >= capacity) {
            resize();  // 容量不足，扩容
        }
        data[size++] = value;  // 添加元素并增加 size
    }

    /*
     * pop_back: 删除末尾元素
     * 时间复杂度：O(1)
     */
    void pop_back() {
        if (size > 0) {
            size--;  // 只需减少 size，不需要实际删除
        }
    }

    /*
     * at: 带边界检查的访问
     * 时间复杂度：O(1)
     */
    T& at(size_t index) {
        if (index >= size) {
            throw std::out_of_range("index out of range");
        }
        return data[index];
    }

    const T& at(size_t index) const {
        if (index >= size) {
            throw std::out_of_range("index out of range");
        }
        return data[index];
    }

    /*
     * operator[]: 不带边界检查的访问（更快）
     * 时间复杂度：O(1)
     */
    T& operator[](size_t index) {
        return data[index];
    }

    const T& operator[](size_t index) const {
        return data[index];
    }

    size_t getSize() const { return size; }
    size_t getCapacity() const { return capacity; }
    bool empty() const { return size == 0; }
};

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

    // 添加多个元素，触发多次扩容
    for (int i = 0; i < 10; i++) {
        vec.push_back(i);
    }

    assert(vec.getSize() == 10);
    assert(vec.getCapacity() >= 10);

    // 验证数据完整性
    for (int i = 0; i < 10; i++) {
        assert(vec[i] == i);
    }

    std::cout << "✓ Resizing test passed\n";
    std::cout << "  Size: " << vec.getSize() << ", Capacity: " << vec.getCapacity() << "\n";
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
    std::cout << "\n💡 复杂度分析:\n";
    std::cout << "   - push_back: 摊销 O(1)\n";
    std::cout << "   - pop_back:  O(1)\n";
    std::cout << "   - operator[]: O(1)\n";
    std::cout << "   - at:        O(1) + 边界检查\n";
    std::cout << "\n📚 关键概念:\n";
    std::cout << "   - 动态扩容策略：容量翻倍确保摊销 O(1)\n";
    std::cout << "   - 内存管理：正确的分配和释放\n";
    std::cout << "   - 数组 vs 链表：随机访问 O(1) vs O(n)\n";

    return 0;
}
