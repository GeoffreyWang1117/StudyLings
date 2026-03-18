#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int value;
    struct TreeNode *left;
    struct TreeNode *right;
    struct TreeNode *parent;  // 用于检查完整性
} TreeNode;

TreeNode* create_node(int value) {
    TreeNode *node = malloc(sizeof(TreeNode));
    node->value = value;
    node->left = node->right = node->parent = NULL;
    return node;
}

// 创建二叉搜索树（有 bug）
TreeNode* create_bst() {
    TreeNode *root = create_node(50);
    
    root->left = create_node(30);
    root->right = create_node(70);
    
    root->left->left = create_node(20);
    root->left->right = create_node(40);
    
    // BUG: 忘记设置 parent 指针
    root->left->parent = root;
    // root->right->parent = root;  // 缺失!
    
    root->right->left = create_node(60);
    root->right->right = create_node(80);
    
    // BUG: 60 的 parent 指向错误
    root->right->left->parent = root;  // 应该是 root->right
    root->right->right->parent = root->right;
    
    return root;
}

// 中序遍历（有 bug）
void inorder(TreeNode *node) {
    if (node == NULL) return;
    
    inorder(node->left);
    printf("%d ", node->value);
    // BUG: 忘记递归右子树
    // inorder(node->right);
}

int main() {
    printf("=== 二叉树调试练习 ===\n\n");
    
    TreeNode *root = create_bst();
    printf("Tree root: %p\n", (void*)root);
    printf("Root value: %d\n", root->value);
    printf("Left child: %p (value=%d)\n", (void*)root->left, root->left->value);
    printf("Right child: %p (value=%d)\n\n", (void*)root->right, root->right->value);
    
    printf("Inorder traversal: ");
    inorder(root);
    printf("\n(Expected: 20 30 40 50 60 70 80)\n\n");
    
    printf("任务:\n");
    printf("1. 使用调试器可视化树结构\n");
    printf("2. 找出 parent 指针的错误\n");
    printf("3. 找出中序遍历的 bug\n");
    printf("4. 实现树的深度优先遍历\n");
    
    return 0;
}
