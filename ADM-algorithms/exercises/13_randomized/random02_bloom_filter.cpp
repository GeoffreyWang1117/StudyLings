/*
 * 练习: random02_bloom_filter
 * 难度: Medium
 * 主题: 随机化算法 - 布隆过滤器
 *
 * 描述:
 * 实现布隆过滤器，一个空间效率极高的概率型数据结构
 *
 * 学习目标:
 * - 理解概率型数据结构
 * - 掌握哈希函数的应用
 * - 理解false positive的概念
 *
 * 参考: ADM 3rd Edition - Chapter 6
 */

#include <iostream>
#include <vector>
#include <string>
#include <functional>
#include <cassert>

class BloomFilter {
private:
    std::vector<bool> bitArray;
    size_t size;
    int numHashFunctions;

    // TODO: 实现哈希函数
    size_t hash(const std::string& item, int seed) const {
        // 你的代码
        // 提示: 可以使用 std::hash 配合seed
        return 0;
    }

public:
    BloomFilter(size_t size, int numHashFunctions)
        : bitArray(size, false), size(size), numHashFunctions(numHashFunctions) {}

    // TODO: 实现插入操作
    void insert(const std::string& item) {
        // 你的代码
        // 对item使用k个不同的哈希函数
        // 将对应位置设为true
    }

    // TODO: 实现查询操作
    bool contains(const std::string& item) const {
        // 你的代码
        // 检查k个哈希位置是否都为true
        // 如果都为true，可能存在（可能误判）
        // 如果有任何false，一定不存在
        return false;
    }

    // 获取当前已使用的比特数
    int countSetBits() const {
        int count = 0;
        for (bool bit : bitArray) {
            if (bit) count++;
        }
        return count;
    }
};

// I AM NOT DONE

// ===== 测试代码 =====

void test_basic_operations() {
    BloomFilter bf(1000, 3);

    bf.insert("apple");
    bf.insert("banana");
    bf.insert("cherry");

    // 应该能找到插入的元素
    assert(bf.contains("apple") == true);
    assert(bf.contains("banana") == true);
    assert(bf.contains("cherry") == true);

    std::cout << "✓ Basic operations test passed\n";
}

void test_false_positive() {
    BloomFilter bf(100, 2);

    bf.insert("test1");
    bf.insert("test2");

    // 大多数未插入的元素应该返回false
    // 但可能有false positive
    int falsePositives = 0;
    for (int i = 0; i < 100; i++) {
        std::string item = "notinserted" + std::to_string(i);
        if (bf.contains(item)) {
            falsePositives++;
        }
    }

    // False positive率应该较低
    assert(falsePositives < 30);  // 容忍一定的误报率

    std::cout << "✓ False positive test passed (FP rate: "
              << falsePositives << "%)\n";
}

int main() {
    std::cout << "Running Bloom Filter Tests...\n";
    std::cout << "==============================\n";

    test_basic_operations();
    test_false_positive();

    std::cout << "\n✅ All tests passed!\n";
    std::cout << "\n💡 布隆过滤器特点:\n";
    std::cout << "   - 空间效率极高\n";
    std::cout << "   - 插入和查询: O(k), k是哈希函数数量\n";
    std::cout << "   - 可能有false positive，但没有false negative\n";
    std::cout << "   - 应用: 缓存系统、垃圾邮件过滤、数据库查询优化\n";

    return 0;
}
