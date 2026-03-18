# Level 10: 数据结构调试

## 学习目标

- 理解常见数据结构在内存中的布局
- 学习如何遍历和检查链表、树等结构
- 掌握使用 GDB/LLDB 可视化复杂数据结构
- 编写自定义 pretty printer
- 调试数据结构相关的 bug

## 为什么要学习数据结构调试？

在实际开发中，我们经常需要调试包含复杂数据结构的程序：
- **链表错误**：环形引用、NULL 指针、内存泄漏
- **树结构问题**：不平衡、父子关系错误、遍历死循环
- **哈希冲突**：碰撞处理、链表损坏
- **内存布局**：理解编译器如何组织数据

## 核心技能

### 1. 遍历链表

**GDB:**
```c
(gdb) print head
$1 = (Node *) 0x555555559260

(gdb) print *head
$2 = {data = 1, next = 0x555555559280}

(gdb) print *head->next
$3 = {data = 2, next = 0x5555555592a0}

// 自动遍历（使用循环）
(gdb) set $node = head
(gdb) while $node != 0
>print $node->data
>set $node = $node->next
>end
```

**LLDB:**
```c
(lldb) p head
(Node *) $0 = 0x0000000100200000

(lldb) p *head
(Node) $1 = {
  data = 1
  next = 0x0000000100200020
}

// Python 脚本遍历
(lldb) script
>>> node = lldb.frame.FindVariable("head")
>>> while node.GetValueAsUnsigned() != 0:
...     print(node.GetChildMemberWithName("data").GetValue())
...     node = node.GetChildMemberWithName("next")
```

### 2. 可视化树结构

```c
// 二叉树节点
typedef struct TreeNode {
    int value;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

// GDB 打印树
(gdb) define print_tree
  set $node = $arg0
  if $node != 0
    printf "Value: %d\n", $node->value
    print_tree $node->left
    print_tree $node->right
  end
end

(gdb) print_tree root
```

### 3. 检查内存布局

```c
// 查看结构体内存布局
(gdb) ptype /o struct Node
type = struct Node {
/*    0      |     4 */    int data;
/*    4      |     4 */    /* XXX 4-byte hole */
/*    8      |     8 */    struct Node *next;
                           /* total size (bytes):   16 */
                         }
```

## 练习列表

### Exercise 1: 链表调试
**难度**: ⭐⭐⭐

调试各种链表实现：
- 单链表的插入、删除、查找
- 检测循环链表
- 双链表的双向遍历
- 内存泄漏检测

### Exercise 2: 树结构调试
**难度**: ⭐⭐⭐⭐

调试树形数据结构：
- 二叉搜索树的插入和删除
- 树的遍历（前序、中序、后序）
- 检查树的平衡性
- 父子指针完整性

### Exercise 3: 哈希表调试
**难度**: ⭐⭐⭐⭐

调试哈希表实现：
- 哈希冲突解决（链地址法）
- 检查哈希分布
- 动态扩容问题
- 内存管理

## 调试技巧

### 1. 使用 Pretty Printers

**GDB Python Pretty Printer:**
```python
class LinkedListPrinter:
    def __init__(self, val):
        self.val = val

    def to_string(self):
        result = "["
        node = self.val
        count = 0
        while node != 0 and count < 10:
            if count > 0:
                result += ", "
            result += str(int(node['data']))
            node = node['next']
            count += 1
        if node != 0:
            result += ", ..."
        result += "]"
        return result
```

### 2. 检查数据结构完整性

```c
// 检查链表是否有环
(gdb) define check_cycle
  set $slow = $arg0
  set $fast = $arg0
  while $fast != 0 && $fast->next != 0
    set $slow = $slow->next
    set $fast = $fast->next->next
    if $slow == $fast
      printf "Cycle detected!\n"
      loop_break
    end
  end
end
```

### 3. 内存可视化

```bash
# 查看连续的节点内存
(gdb) x/10gx head
0x555555559260: 0x0000000000000001  0x0000555555559280
0x555555559270: 0x0000000000000000  0x0000000000000000
0x555555559280: 0x0000000000000002  0x00005555555592a0
```

## 常见问题和解决方案

### 问题 1: 链表遍历陷入死循环

**症状**: 调试器一直在链表遍历中循环
**诊断**:
```c
(gdb) set $node = head
(gdb) set $count = 0
(gdb) while $node != 0 && $count < 100
>printf "Node %d: data=%d, next=%p\n", $count, $node->data, $node->next
>set $node = $node->next
>set $count = $count + 1
>end
// 如果 count == 100，说明有环或链表太长
```

### 问题 2: 树节点父指针错误

**症状**: 树遍历出现意外节点
**诊断**:
```c
(gdb) define verify_tree
  set $node = $arg0
  if $node != 0
    if $node->left != 0 && $node->left->parent != $node
      printf "Left child parent mismatch at %p\n", $node
    end
    verify_tree $node->left
    verify_tree $node->right
  end
end
```

### 问题 3: 哈希表槽位不均匀

**症状**: 某些槽位有大量冲突
**诊断**:
```c
(gdb) set $i = 0
(gdb) while $i < hash_table->size
>set $count = 0
>set $node = hash_table->buckets[$i]
>while $node != 0
>  set $count = $count + 1
>  set $node = $node->next
>end
>printf "Bucket[%d]: %d items\n", $i, $count
>set $i = $i + 1
>end
```

## 快速参考

| 操作 | GDB | LLDB |
|------|-----|------|
| 打印结构体 | `print *node` | `p *node` |
| 查看内存布局 | `ptype /o struct` | `type lookup` |
| 遍历链表 | `while` 循环 | Python 脚本 |
| 打印地址 | `print &node` | `p &node` |
| 检查 NULL | `if ptr == 0` | `if ptr == 0` |

## 学习路径

1. **基础**: 单链表遍历和打印
2. **进阶**: 检测环、双向链表
3. **高级**: 自定义 pretty printer
4. **专家**: 复杂树结构和图的调试

完成这个级别后，你将能够：
- ✅ 快速理解任何数据结构的内存布局
- ✅ 有效调试链表、树、哈希表等结构
- ✅ 编写自定义可视化工具
- ✅ 诊断复杂的数据结构 bug
