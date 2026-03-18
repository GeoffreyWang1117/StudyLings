/*
 * 练习: ds05_binary_tree
 * 难度: Medium
 * 主题: 数据结构 - 二叉树
 * 描述: 实现二叉树的基本操作和遍历
 * 参考: ADM 3rd Edition - Chapter 3.4
 */

#include <iostream>
#include <vector>
#include <cassert>

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

// TODO: 实现前序遍历
std::vector<int> preorderTraversal(TreeNode* root) {
    return {};
}

// TODO: 实现中序遍历
std::vector<int> inorderTraversal(TreeNode* root) {
    return {};
}

// TODO: 实现后序遍历
std::vector<int> postorderTraversal(TreeNode* root) {
    return {};
}

// I AM NOT DONE

void test_basic() {
    TreeNode* root = new TreeNode(1);
    root->left = new TreeNode(2);
    root->right = new TreeNode(3);
    auto result = inorderTraversal(root);
    // 清理内存
    delete root->left;
    delete root->right;
    delete root;
    std::cout << "✓ Basic test passed\n";
}

int main() {
    test_basic();
    std::cout << "\n✅ All tests passed!\n";
    return 0;
}
