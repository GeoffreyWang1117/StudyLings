/*
 * 练习: random03_skip_list
 * 难度: Hard
 * 主题: 随机化算法 - 跳表
 *
 * 描述:
 * 实现跳表（Skip List），一个使用随机化的平衡数据结构
 *
 * 学习目标:
 * - 理解概率平衡的思想
 * - 掌握多层链表结构
 * - 分析期望性能
 *
 * 参考: ADM 3rd Edition - Chapter 6
 */

#include <iostream>
#include <random>
#include <limits>
#include <cassert>

const int MAX_LEVEL = 16;

struct SkipListNode {
    int value;
    std::vector<SkipListNode*> forward;

    SkipListNode(int val, int level) : value(val), forward(level + 1, nullptr) {}
};

class SkipList {
private:
    SkipListNode* header;
    int maxLevel;
    int currentLevel;
    std::mt19937 gen;
    std::uniform_real_distribution<> dis;

    // TODO: 实现随机层数生成
    int randomLevel() {
        // 你的代码
        // 以概率p=0.5提升层数
        // 返回值范围: [0, maxLevel]
        return 0;
    }

public:
    SkipList(int maxLvl = MAX_LEVEL)
        : maxLevel(maxLvl), currentLevel(0), gen(std::random_device{}()), dis(0.0, 1.0) {
        header = new SkipListNode(std::numeric_limits<int>::min(), maxLevel);
    }

    ~SkipList() {
        // TODO: 释放所有节点
    }

    // TODO: 实现插入操作
    void insert(int value) {
        // 你的代码
        // 1. 找到插入位置
        // 2. 随机生成层数
        // 3. 创建新节点
        // 4. 更新各层指针
    }

    // TODO: 实现查找操作
    bool search(int value) const {
        // 你的代码
        // 从最高层开始查找
        // 如果当前层不能前进，降低一层
        return false;
    }

    // TODO: 实现删除操作
    bool remove(int value) {
        // 你的代码
        return false;
    }

    // 打印跳表结构（用于调试）
    void display() const {
        for (int i = currentLevel; i >= 0; i--) {
            SkipListNode* node = header->forward[i];
            std::cout << "Level " << i << ": ";
            while (node != nullptr) {
                std::cout << node->value << " ";
                node = node->forward[i];
            }
            std::cout << "\n";
        }
    }
};

// I AM NOT DONE

// ===== 测试代码 =====

void test_basic_operations() {
    SkipList sl;

    sl.insert(3);
    sl.insert(6);
    sl.insert(7);
    sl.insert(9);
    sl.insert(12);
    sl.insert(19);

    assert(sl.search(7) == true);
    assert(sl.search(10) == false);

    std::cout << "✓ Basic operations test passed\n";
}

void test_insert_delete() {
    SkipList sl;

    for (int i = 1; i <= 10; i++) {
        sl.insert(i);
    }

    assert(sl.search(5) == true);
    sl.remove(5);
    assert(sl.search(5) == false);

    std::cout << "✓ Insert/delete test passed\n";
}

void test_large_dataset() {
    SkipList sl;

    // 插入1000个元素
    for (int i = 0; i < 1000; i++) {
        sl.insert(i);
    }

    // 验证查找
    assert(sl.search(500) == true);
    assert(sl.search(1500) == false);

    std::cout << "✓ Large dataset test passed\n";
}

int main() {
    std::cout << "Running Skip List Tests...\n";
    std::cout << "==========================\n";

    test_basic_operations();
    test_insert_delete();
    test_large_dataset();

    std::cout << "\n✅ All tests passed!\n";
    std::cout << "\n💡 跳表分析:\n";
    std::cout << "   - 期望查找时间: O(log n)\n";
    std::cout << "   - 期望插入时间: O(log n)\n";
    std::cout << "   - 期望删除时间: O(log n)\n";
    std::cout << "   - 空间复杂度: O(n)\n";
    std::cout << "   - 优点: 实现简单，性能稳定\n";
    std::cout << "   - 应用: Redis的有序集合\n";

    return 0;
}
