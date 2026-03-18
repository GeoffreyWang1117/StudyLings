/*
 * 练习: ds08_hash_table 难度: Medium 主题: 哈希表
 * 描述: 实现哈希表（链地址法）参考: ADM 3rd - Chapter 3.7
 */
#include <iostream>
#include <cassert>
// TODO: 实现哈希表
class HashTable {
public:
    void insert(int key, int value) {}
    int get(int key) { return -1; }
    bool contains(int key) { return false; }
};
// I AM NOT DONE
void test_basic() {
    HashTable ht;
    ht.insert(1, 10);
    assert(ht.contains(1));
    std::cout << "✓ Test passed\n";
}
int main() { test_basic(); return 0; }
