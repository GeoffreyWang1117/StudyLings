# Exercise 1: 链表调试 - 完整解决方案

## Bug 分析

### Bug 1: 循环链表未闭合

**位置**: `create_circular()` 函数
**问题**: 最后一个节点的 `next` 指向 NULL，没有形成环

```c
// 错误代码
current->next = NULL;

// 正确代码
current->next = head;  // 形成环
```

**调试过程**:
```bash
gdb ./linkedlist
(gdb) break create_circular
(gdb) run
(gdb) finish  # 执行完函数

# 检查最后一个节点
(gdb) set $node = circular
(gdb) while $node->next != 0
  set $node = $node->next
end
(gdb) print $node->data
$1 = 50
(gdb) print $node->next
$2 = (struct Node *) 0x0  # 应该指向 head!
(gdb) print circular
$3 = (Node *) 0x555555559280
```

### Bug 2: 双链表 prev 指针错误

**位置**: `create_doubly()` 函数，第三个节点
**问题**: `new_node->prev = head` 应该是 `new_node->prev = current`

```c
// 错误代码
if (i == 300) {
    new_node->prev = head;  // 错误！
}

// 正确代码
new_node->prev = current;  // 应该指向前一个节点
```

**调试过程**:
```bash
(gdb) break main
(gdb) run
(gdb) next  # 到 doubly 创建后

# 遍历并检查 prev 指针
(gdb) set $node = doubly
(gdb) set $prev = 0
(gdb) set $index = 0
(gdb) while $node != 0
  printf "[%d] addr=%p, data=%d, prev=%p (expected: %p)\n", \
         $index, $node, $node->data, $node->prev, $prev
  if $node->prev != $prev
    printf "  ^^^ ERROR: prev pointer mismatch!\n"
  end
  set $prev = $node
  set $node = $node->next
  set $index++
end

# 输出：
[0] addr=0x..., data=100, prev=0x0 (expected: 0x0)
[1] addr=0x..., data=200, prev=0x... (expected: 0x...)
[2] addr=0x..., data=300, prev=0x... (expected: 0x...)  # 这里错了！
  ^^^ ERROR: prev pointer mismatch!
```

## 完整调试会话

### GDB 会话

```bash
$ gdb ./linkedlist
(gdb) break main
Breakpoint 1 at 0x11f9
(gdb) run
Breakpoint 1, main ()

# === 任务 1: 遍历单链表 ===
(gdb) next
... # 执行到 list 创建后

(gdb) print list
$1 = (Node *) 0x555555559260

# 方法 1: 手动遍历
(gdb) print *list
$2 = {data = 1, next = 0x555555559280}

(gdb) print *list->next
$3 = {data = 2, next = 0x5555555592a0}

# 方法 2: 循环遍历
(gdb) set $n = list
(gdb) set $i = 0
(gdb) while $n != 0
  printf "[%d] data=%d, addr=%p, next=%p\n", $i, $n->data, $n, $n->next
  set $n = $n->next
  set $i++
end
[0] data=1, addr=0x555555559260, next=0x555555559280
[1] data=2, addr=0x555555559280, next=0x5555555592a0
[2] data=3, addr=0x5555555592a0, next=0x5555555592c0
[3] data=4, addr=0x5555555592c0, next=0x5555555592e0
[4] data=5, addr=0x5555555592e0, next=0x0

# === 任务 2: 检测循环链表的环 ===
(gdb) next
... # 执行到 circular 创建后

# 使用快慢指针检测环
(gdb) set $slow = circular
(gdb) set $fast = circular
(gdb) set $found = 0
(gdb) while $fast != 0 && $fast->next != 0 && $found == 0
  set $slow = $slow->next
  set $fast = $fast->next->next
  if $slow == $fast
    printf "Cycle detected at %p\n", $slow
    set $found = 1
  end
end

# 应该输出没有检测到环（因为有 bug）
# 让我们手动检查最后一个节点
(gdb) set $n = circular
(gdb) while $n->next != 0
  set $n = $n->next
end
(gdb) print $n->data
$10 = 50
(gdb) print $n->next
$11 = (struct Node *) 0x0  # BUG: 应该指向 circular!

(gdb) print circular
$12 = (Node *) 0x555555559300

# === 任务 3: 查看内存布局 ===
(gdb) ptype /o struct Node
type = struct Node {
/*    0      |     4 */    int data;
/*    4      |     4 */    /* XXX 4-byte hole */
/*    8      |     8 */    struct Node *next;
                           /* total size (bytes):   16 */
                         }

# 查看实际内存（16进制）
(gdb) x/2gx list
0x555555559260: 0x0000000000000001  0x0000555555559280
#               ^^^^^^^^^^^^^^^^^^  ^^^^^^^^^^^^^^^^^^
#               data = 1 (低32位)     next指针

(gdb) x/2gx list->next
0x555555559280: 0x0000000000000002  0x00005555555592a0
#               data = 2              next指针

# === 任务 4: 验证双链表 ===
(gdb) next
... # 执行到 doubly 创建后

# 定义验证函数
(gdb) define verify_doubly_list
  set $node = $arg0
  set $prev_node = 0
  set $errors = 0

  printf "Verifying doubly linked list...\n"
  while $node != 0
    printf "Node %p: data=%d, prev=%p, next=%p\n", \
           $node, $node->data, $node->prev, $node->next

    if $node->prev != $prev_node
      printf "  ERROR: prev should be %p, got %p\n", $prev_node, $node->prev
      set $errors++
    end

    if $node->next != 0 && $node->next->prev != $node
      printf "  ERROR: next->prev inconsistency\n"
      set $errors++
    end

    set $prev_node = $node
    set $node = $node->next
  end

  if $errors > 0
    printf "Found %d errors\n", $errors
  else
    printf "No errors found\n"
  end
end

(gdb) verify_doubly_list doubly
Verifying doubly linked list...
Node 0x...: data=100, prev=0x0, next=0x...
Node 0x...: data=200, prev=0x..., next=0x...
Node 0x...: data=300, prev=0x..., next=0x...
  ERROR: prev should be 0x..., got 0x...  # 发现错误！
Node 0x...: data=400, prev=0x..., next=0x...
Node 0x...: data=500, prev=0x..., next=0x0
Found 1 errors
```

### LLDB 会话

```bash
$ lldb ./linkedlist
(lldb) b main
(lldb) run

# 遍历链表（Python 脚本）
(lldb) script
>>> def print_list(var_name, max_count=20):
...     node = lldb.frame.FindVariable(var_name)
...     count = 0
...     print(f"Traversing {var_name}:")
...     while node.GetValueAsUnsigned() != 0 and count < max_count:
...         data = node.GetChildMemberWithName("data").GetValueAsSigned()
...         next_addr = node.GetChildMemberWithName("next").GetValueAsUnsigned()
...         node_addr = node.GetValueAsUnsigned()
...         print(f"  [{count}] addr=0x{node_addr:x}, data={data}, next=0x{next_addr:x}")
...         node = node.GetChildMemberWithName("next")
...         count += 1
...     if node.GetValueAsUnsigned() != 0:
...         print(f"  ... (stopped after {max_count} nodes)")
...

>>> print_list("list")
>>> print_list("circular")
>>> exit()

# 检测环
(lldb) expr
Enter expressions, then terminate with an empty line to evaluate:
1: Node *slow = circular, *fast = circular;
2: int has_cycle = 0;
3: while (fast && fast->next && !has_cycle) {
4:     slow = slow->next;
5:     fast = fast->next->next;
6:     if (slow == fast) has_cycle = 1;
7: }
8: has_cycle
(int) $0 = 0  # 没有环（因为有 bug）
```

## 自定义 GDB 命令

创建 `list_helpers.gdb`:

```gdb
# 遍历链表
define print_linked_list
    set $node = $arg0
    set $max = 20
    if $argc > 1
        set $max = $arg1
    end

    set $count = 0
    printf "Linked List:\n"
    while $node != 0 && $count < $max
        printf "  [%d] addr=%p, data=%d, next=%p\n", \
               $count, $node, $node->data, $node->next
        set $node = $node->next
        set $count++
    end

    if $node != 0
        printf "  ... (truncated at %d nodes)\n", $max
    else
        printf "Total: %d nodes\n", $count
    end
end

# 检测环
define detect_list_cycle
    set $slow = $arg0
    set $fast = $arg0
    set $has_cycle = 0

    while $fast != 0 && $fast->next != 0 && $has_cycle == 0
        set $slow = $slow->next
        set $fast = $fast->next->next
        if $slow == $fast
            printf "CYCLE DETECTED at node %p (data=%d)\n", $slow, $slow->data
            set $has_cycle = 1
        end
    end

    if $has_cycle == 0
        printf "No cycle detected\n"
    end
end

# 验证双链表
define verify_doubly_linked_list
    set $node = $arg0
    set $prev = 0
    set $errors = 0

    while $node != 0
        if $node->prev != $prev
            printf "ERROR at %p: prev=%p, expected=%p\n", \
                   $node, $node->prev, $prev
            set $errors++
        end
        set $prev = $node
        set $node = $node->next
    end

    if $errors == 0
        printf "Doubly linked list is valid\n"
    else
        printf "Found %d errors\n", $errors
    end
end
```

使用:
```bash
(gdb) source list_helpers.gdb
(gdb) print_linked_list list
(gdb) detect_list_cycle circular
(gdb) verify_doubly_linked_list doubly
```

## Python Pretty Printer

创建 `list_printer.py`:

```python
import gdb

class LinkedListPrinter:
    "Print a linked list"

    def __init__(self, val):
        self.val = val

    def to_string(self):
        if self.val == 0:
            return "NULL"

        result = []
        node = self.val
        count = 0
        max_nodes = 10
        seen = set()

        while node != 0 and count < max_nodes:
            addr = int(node)
            if addr in seen:
                result.append(f"... (cycle back to 0x{addr:x})")
                break
            seen.add(addr)

            data = int(node['data'])
            result.append(str(data))
            node = node['next']
            count += 1

        if node != 0 and int(node) not in seen:
            result.append("...")

        return " -> ".join(result)

def lookup_type(val):
    if val.type.code == gdb.TYPE_CODE_PTR:
        target = val.type.target().strip_typedefs()
        if target.tag == "Node":
            return LinkedListPrinter(val)
    return None

gdb.pretty_printers.append(lookup_type)
print("Linked list pretty printer loaded")
```

使用:
```bash
(gdb) source list_printer.py
(gdb) print list
$1 = 1 -> 2 -> 3 -> 4 -> 5

(gdb) print circular
$2 = 10 -> 20 -> 30 -> 40 -> 50  # 没有环（bug）
```

## 修复代码

```c
// 修复循环链表
Node* create_circular() {
    Node *head = malloc(sizeof(Node));
    head->data = 10;

    Node *current = head;
    for (int i = 20; i <= 50; i += 10) {
        current->next = malloc(sizeof(Node));
        current = current->next;
        current->data = i;
    }

    current->next = head;  // 修复: 形成环
    return head;
}

// 修复双链表
DNode* create_doubly() {
    DNode *head = malloc(sizeof(DNode));
    head->data = 100;
    head->prev = NULL;
    head->next = NULL;

    DNode *current = head;
    for (int i = 200; i <= 500; i += 100) {
        DNode *new_node = malloc(sizeof(DNode));
        new_node->data = i;
        new_node->next = NULL;
        new_node->prev = current;  // 修复: 始终指向 current

        current->next = new_node;
        current = new_node;
    }

    return head;
}
```

## 关键技巧总结

1. **遍历链表**: 使用 `while` 循环和计数器防止死循环
2. **检测环**: 快慢指针算法（Floyd's cycle detection）
3. **内存布局**: 使用 `ptype /o` 和 `x` 命令
4. **双向验证**: 检查 `prev` 和 `next` 的一致性
5. **Pretty Printer**: 提高调试效率

## 扩展练习

1. 实现链表反转的调试
2. 调试链表合并排序
3. 检测链表相交点
4. 内存泄漏检测（Valgrind 配合 GDB）
