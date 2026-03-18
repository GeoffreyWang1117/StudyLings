/* 练习: string04_trie 难度: Medium 主题: 字典树 */
#include <iostream>
#include <string>
class Trie {
public:
    void insert(std::string word) {}
    bool search(std::string word) { return false; }
    bool startsWith(std::string prefix) { return false; }
};
// I AM NOT DONE
void test_basic() { Trie trie; trie.insert("apple"); std::cout << "✓ Test passed\n"; }
int main() { test_basic(); return 0; }
