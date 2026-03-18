# Exercise 1: 链表调试深度实践

## 目标

学习如何调试各种链表实现，理解链表在内存中的实际布局。

## 背景知识

### 链表内存布局

```
单链表：
┌─────────┬──────┐    ┌─────────┬──────┐    ┌─────────┬──────┐
│ data: 1 │ next ├───>│ data: 2 │ next ├───>│ data: 3 │ NULL │
└─────────┴──────┘    └─────────┴──────┘    └─────────┴──────┘
0x1000              0x1020              0x1040

双链表：
┌──────┬─────────┬──────┐    ┌──────┬─────────┬──────┐
│ prev │ data: 1 │ next ├───>│ prev │ data: 2 │ next │
│ NULL │         │      │<───┤      │         │ NULL │
└──────┴─────────┴──────┘    └──────┴─────────┴──────┘

循环链表：
┌─────────┬──────┐    ┌─────────┬──────┐
│ data: 1 │ next ├───>│ data: 2 │ next ├─┐
└─────────┴──────┘    └─────────┴──────┘ │
     ^                                     │
     └─────────────────────────────────────┘
```

## 任务

这个程序实现了三种链表，但有 bug。使用调试器：

1. **基本遍历**: 打印链表的所有节点
2. **检测循环**: 判断链表是否有环
3. **内存检查**: 查看节点的实际内存布局
4. **双向验证**: 检查双链表的前后指针一致性
5. **内存泄漏**: 找出哪些节点没有被释放

## 代码说明

程序包含：
- `create_list()` - 创建单链表
- `create_circular()` - 创建循环链表（有 bug）
- `create_doubly()` - 创建双链表（有 bug）
- `print_list()` - 打印链表（可能死循环）
- `free_list()` - 释放链表（可能泄漏）

## 调试步骤

### 1. 遍历单链表

```bash
gdb ./linkedlist

(gdb) break main
(gdb) run
(gdb) next  # 执行到 list 创建后

# 手动遍历
(gdb) set $node = list
(gdb) while $node != 0
  print $node->data
  print $node->next
  set $node = $node->next
end

# 或使用自定义命令
(gdb) define print_list
  set $n = $arg0
  set $count = 0
  while $n != 0 && $count < 20
    printf "[%d] data=%d, addr=%p, next=%p\n", $count, $n->data, $n, $n->next
    set $n = $n->next
    set $count = $count + 1
  end
  if $n != 0
    printf "... (truncated, possible cycle)\n"
  end
end

(gdb) print_list list
```

### 2. 检测循环链表

```bash
# 使用快慢指针算法
(gdb) define detect_cycle
  set $slow = $arg0
  set $fast = $arg0
  set $has_cycle = 0

  while $fast != 0 && $fast->next != 0
    set $slow = $slow->next
    set $fast = $fast->next->next
    if $slow == $fast
      printf "Cycle detected! Meeting point: %p\n", $slow
      set $has_cycle = 1
      loop_break
    end
  end

  if $has_cycle == 0
    printf "No cycle detected\n"
  end
end

(gdb) detect_cycle circular
```

### 3. 查看内存布局

```bash
# 查看结构体定义
(gdb) ptype /o struct Node
type = struct Node {
/*    0      |     4 */    int data;
/*    4      |     4 */    /* XXX 4-byte padding */
/*    8      |     8 */    struct Node *next;
                           /* total size (bytes):   16 */
                         }

# 查看实际内存
(gdb) x/4gx list
0x555555559260: 0x0000000000000001  0x0000555555559280
0x555555559270: 0x0000000000000000  0x0000000000000000

# 第一个节点：
#   0x00000001 = data (低32位)
#   0x555555559280 = next 指针
```

### 4. 双链表验证

```bash
# 检查双向一致性
(gdb) define verify_doubly
  set $node = $arg0
  set $prev_node = 0

  while $node != 0
    # 检查 prev 指针
    if $node->prev != $prev_node
      printf "ERROR: Node %p prev pointer mismatch!\n", $node
      printf "  Expected: %p, Got: %p\n", $prev_node, $node->prev
    end

    # 检查 next->prev
    if $node->next != 0 && $node->next->prev != $node
      printf "ERROR: Node %p next->prev mismatch!\n", $node
    end

    set $prev_node = $node
    set $node = $node->next
  end
  printf "Doubly linked list verification complete\n"
end

(gdb) verify_doubly doubly
```

### 5. LLDB 版本

```bash
lldb ./linkedlist

(lldb) b main
(lldb) run
(lldb) n

# 使用 Python 遍历
(lldb) script
>>> node = lldb.frame.FindVariable("list")
>>> count = 0
>>> while node.GetValueAsUnsigned() != 0 and count < 20:
...     data = node.GetChildMemberWithName("data")
...     next_node = node.GetChildMemberWithName("next")
...     print(f"[{count}] data={data.GetValue()}, next={next_node.GetValue()}")
...     node = next_node
...     count += 1
...
>>> exit()
```

## 练习任务

### 任务 1: 找出循环链表的 bug
循环链表应该形成一个环，但实际可能没有正确连接。

**提示**: 遍历链表，检查最后一个节点的 `next` 是否指向头节点。

### 任务 2: 修复双链表的 prev 指针
双链表的某些节点 `prev` 指针可能不正确。

**提示**: 使用 `verify_doubly` 命令找出不一致的节点。

### 任务 3: 检测内存泄漏
某些节点在 `free_list()` 后没有被释放。

**提示**: 在 `free_list()` 中设置断点，单步执行并检查是否所有节点都被访问。

### 任务 4: 性能分析
统计链表有多少个节点，平均每个节点占用多少字节。

**提示**: 使用遍历统计，结合 `sizeof(struct Node)` 和内存地址。

## 扩展挑战

1. **编写 Pretty Printer**: 创建一个 GDB Python 脚本，美化链表输出
2. **可视化**: 生成链表的 DOT 图（Graphviz 格式）
3. **反向遍历**: 从尾部反向遍历双链表
4. **查找环起点**: 如果有环，找出环的起始节点

## 验证

```bash
# 编译
make

# 运行程序（可能会卡住或崩溃）
./linkedlist

# 使用调试器分析
gdb ./linkedlist
```

## 预期发现

- 循环链表的最后一个节点 `next` 没有指向头部
- 双链表的某个节点 `prev` 指针错误
- 释放循环链表时会泄漏（因为没有正确检测环）
