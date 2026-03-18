# Exercise 2: 二叉树调试

## 目标
学习调试二叉树结构，验证父子关系，可视化树的形状。

## 任务
1. 使用 GDB 递归遍历树
2. 检查 parent 指针的正确性
3. 找出中序遍历的 bug
4. 可视化树结构

## 提示
```gdb
# 递归打印树
define print_tree
  set $indent = $arg1
  if $arg0 != 0
    printf "%*s", $indent, ""
    printf "Node %p: value=%d\n", $arg0, $arg0->value
    if $arg0->left != 0
      printf "%*sL: ", $indent, ""
      print_tree $arg0->left ($indent + 2)
    end
    if $arg0->right != 0
      printf "%*sR: ", $indent, ""
      print_tree $arg0->right ($indent + 2)
    end
  end
end

# 使用
(gdb) print_tree root 0
```
