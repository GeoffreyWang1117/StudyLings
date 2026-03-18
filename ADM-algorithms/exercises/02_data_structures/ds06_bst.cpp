/*
 * 练习: ds06_bst
 * 难度: Medium
 * 主题: 数据结构 - 二叉搜索树 (BST)
 * 描述: 实现二叉搜索树的插入、查找、删除操作
 * 参考: ADM 3rd Edition - Chapter 3.4
 */

#include <iostream>
#include <cassert>

struct BSTNode {
    int val;
    BSTNode* left;
    BSTNode* right;
    BSTNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class BST {
public:
    BSTNode* root;
    BST() : root(nullptr) {}

    // TODO: 实现插入
    void insert(int val) {}

    // TODO: 实现查找
    bool search(int val) { return false; }

    // TODO: 实现删除
    void remove(int val) {}
};

// I AM NOT DONE

void test_basic() {
    BST bst;
    bst.insert(5);
    bst.insert(3);
    bst.insert(7);
    assert(bst.search(5) == true);
    std::cout << "✓ Basic test passed\n";
}

int main() {
    test_basic();
    std::cout << "\n✅ All tests passed!\n";
    return 0;
}
