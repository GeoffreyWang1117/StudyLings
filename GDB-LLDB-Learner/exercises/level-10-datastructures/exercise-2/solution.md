# Exercise 2: 解决方案

## Bug 分析

### Bug 1: parent 指针缺失
`root->right->parent` 没有设置

### Bug 2: parent 指针错误  
`root->right->left->parent` 指向 root 而不是 root->right

### Bug 3: 中序遍历不完整
缺少 `inorder(node->right)`

## 调试会话
```gdb
(gdb) print_tree root 0
Node 0x...: value=50
  L: Node 0x...: value=30
    L: Node 0x...: value=20
    R: Node 0x...: value=40
  R: Node 0x...: value=70
    L: Node 0x...: value=60
    R: Node 0x...: value=80

# 检查 parent 指针
(gdb) p root->right->parent
$1 = (struct TreeNode *) 0x0  # BUG!
```
