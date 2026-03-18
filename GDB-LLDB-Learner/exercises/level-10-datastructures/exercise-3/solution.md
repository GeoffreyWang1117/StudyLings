# Exercise 3: 哈希表调试 - 参考答案

## 完整调试会话

### GDB 调试会话

```bash
$ gdb ./hashtable
(gdb) break main
Breakpoint 1 at 0x4012a3: file hashtable.c, line 45.

(gdb) run
Starting program: ./hashtable
=== 哈希表调试 ===

Breakpoint 1, main () at hashtable.c:47

# ========== 任务 1: 分析哈希函数 ==========

(gdb) break hash
Breakpoint 2 at 0x401180: file hashtable.c, line 19.

(gdb) continue
Breakpoint 2, hash (key=0x402010 "apple") at hashtable.c:19

(gdb) p key
$1 = 0x402010 "apple"

# 单步执行哈希函数
(gdb) n
20          while (*key) {

(gdb) p hash
$2 = 0

(gdb) n
21              hash = (hash << 5) + *key++;

(gdb) p *key
$3 = 97 'a'

(gdb) p hash << 5
$4 = 0

# 左移5位相当于乘以 2^5 = 32
(gdb) p 1 << 5
$5 = 32

(gdb) continue
# 继续到函数返回

(gdb) finish
Run till exit from #0  hash (key=0x402010 "apple") at hashtable.c:24
0x00401209 in insert (table=0x405260, key=0x402010 "apple", value=100)

Value returned is $6 = 5

# "apple" 映射到桶 5

# 检查其他 key 的哈希值
(gdb) print hash("banana")
$7 = 0

(gdb) print hash("cherry")
$8 = 9

(gdb) print hash("date")
$9 = 8

(gdb) print hash("elderberry")
$10 = 0

# banana 和 elderberry 都映射到桶 0 - 发生冲突！

# ========== 任务 2: 检查桶内链表 ==========

(gdb) break 70
Breakpoint 3 at 0x4012f8: file hashtable.c, line 70.

(gdb) continue
Hash distribution:
Bucket[0]: 2 entries
Bucket[5]: 1 entries
Bucket[8]: 1 entries
Bucket[9]: 1 entries

Breakpoint 3, main () at hashtable.c:70

(gdb) p table
$11 = (HashTable *) 0x405260

(gdb) p table->size
$12 = 10

(gdb) p table->buckets
$13 = (Entry **) 0x405280

# 检查桶 0（有冲突）
(gdb) p table->buckets[0]
$14 = (Entry *) 0x405340

(gdb) p *table->buckets[0]
$15 = {key = 0x405360 "elderberry", value = 500, next = 0x4052a0}

# 第一个条目是 "elderberry"（最后插入的）
(gdb) p table->buckets[0]->next
$16 = (Entry *) 0x4052a0

(gdb) p *table->buckets[0]->next
$17 = {key = 0x4052c0 "banana", value = 200, next = 0x0}

# 第二个条目是 "banana"（先插入的）
# 链表：elderberry -> banana -> NULL

# 检查桶 5
(gdb) p *table->buckets[5]
$18 = {key = 0x4052e0 "apple", value = 100, next = 0x0}

# 桶 5 只有一个条目

# 遍历所有非空桶
(gdb) set $i = 0
(gdb) while $i < table->size
 >set $e = table->buckets[$i]
 >if $e != 0
 >  printf "Bucket[%d]: ", $i
 >  while $e != 0
 >    printf "%s=%d ", $e->key, $e->value
 >    set $e = $e->next
 >  end
 >  printf "\n"
 >end
 >set $i = $i + 1
 >end
Bucket[0]: elderberry=500 banana=200
Bucket[5]: apple=100
Bucket[8]: date=400
Bucket[9]: cherry=300

# ========== 任务 3: 追踪插入过程 ==========

(gdb) delete
Delete all breakpoints? (y or n) y

(gdb) break insert
Breakpoint 4 at 0x401219: file hashtable.c, line 34.

(gdb) run
Starting program: ./hashtable
=== 哈希表调试 ===

Breakpoint 4, insert (table=0x405260, key=0x402010 "apple", value=100)

(gdb) p key
$19 = 0x402010 "apple"

(gdb) n
35          Entry *entry = malloc(sizeof(Entry));

(gdb) p index
$20 = 5

# "apple" 哈希到桶 5

(gdb) n
36          entry->key = strdup(key);

(gdb) n
37          entry->value = value;

(gdb) n
40          entry->next = table->buckets[index];

# 关键步骤：新条目的 next 指向当前桶的头部
(gdb) p table->buckets[index]
$21 = (Entry *) 0x0

# 桶 5 当前为空

(gdb) n
41          table->buckets[index] = entry;

# 将新条目设置为桶的头部

(gdb) p table->buckets[5]
$22 = (Entry *) 0x4052c0

(gdb) p *table->buckets[5]
$23 = {key = 0x4052e0 "apple", value = 100, next = 0x0}

# 现在桶 5 指向新条目

# 插入第二个条目到桶 0
(gdb) continue
Breakpoint 4, insert (table=0x405260, key=0x402011 "banana", value=200)

(gdb) p index
$24 = 0

(gdb) until 40
insert (table=0x405260, key=0x402011 "banana", value=200) at hashtable.c:40

(gdb) p table->buckets[0]
$25 = (Entry *) 0x0

# 桶 0 当前为空

(gdb) n
41          table->buckets[index] = entry;

# 再插入 elderberry 到桶 0（冲突）
(gdb) continue
Breakpoint 4, insert (table=0x405260, key=0x402015 "elderberry", value=500)

(gdb) p index
$26 = 0

(gdb) until 40

(gdb) p table->buckets[0]
$27 = (Entry *) 0x4052a0

(gdb) p *table->buckets[0]
$28 = {key = 0x4052c0 "banana", value = 200, next = 0x0}

# 桶 0 已经有 banana

(gdb) n
# entry->next = table->buckets[0]; // 指向 banana

(gdb) p entry->next
$29 = (Entry *) 0x4052a0

(gdb) p entry->next->key
$30 = 0x4052c0 "banana"

(gdb) n
# table->buckets[0] = entry; // 新条目成为头部

(gdb) p table->buckets[0]
$31 = (Entry *) 0x405340

(gdb) p *table->buckets[0]
$32 = {key = 0x405360 "elderberry", value = 500, next = 0x4052a0}

# 现在链表是：elderberry -> banana -> NULL
# 新条目总是插入到链表头部（头插法）

# ========== 任务 4: 哈希分布分析 ==========

(gdb) continue
Hash distribution:
Bucket[0]: 2 entries
Bucket[5]: 1 entries
Bucket[8]: 1 entries
Bucket[9]: 1 entries

# 统计分析
(gdb) set $total_entries = 0
(gdb) set $non_empty_buckets = 0
(gdb) set $max_chain = 0

(gdb) set $i = 0
(gdb) while $i < table->size
 >set $count = 0
 >set $e = table->buckets[$i]
 >while $e != 0
 >  set $count = $count + 1
 >  set $e = $e->next
 >end
 >if $count > 0
 >  set $non_empty_buckets = $non_empty_buckets + 1
 >  set $total_entries = $total_entries + $count
 >  if $count > $max_chain
 >    set $max_chain = $count
 >  end
 >end
 >set $i = $i + 1
 >end

(gdb) p $total_entries
$33 = 5

(gdb) p $non_empty_buckets
$34 = 4

(gdb) p $max_chain
$35 = 2

# 负载因子 = 5 / 10 = 0.5
# 最大链长 = 2（桶 0）
# 空桶数 = 10 - 4 = 6

(gdb) quit
```

### LLDB 调试会话

```bash
$ lldb ./hashtable
(lldb) target create "./hashtable"
Current executable set to './hashtable'

(lldb) b main
Breakpoint 1: where = hashtable`main + 13

(lldb) run
Process 1234 launched: './hashtable'
=== 哈希表调试 ===

Process 1234 stopped

# ========== 任务 1: 分析哈希函数 ==========

(lldb) b hash
Breakpoint 2: where = hashtable`hash + 15

(lldb) continue
Process 1234 stopped
* thread #1, name = 'hashtable', stop reason = breakpoint 2.1
    frame #0: hashtable`hash(key="apple")

(lldb) frame variable key
(const char *) key = 0x402010 "apple"

(lldb) expr (int)(1 << 5)
(int) $0 = 32

# 左移5位 = 乘以32

(lldb) finish
Process 1234 stopped
Value returned: (unsigned int) $1 = 5

# "apple" 哈希到桶 5

(lldb) expr hash("banana")
(unsigned int) $2 = 0

(lldb) expr hash("elderberry")
(unsigned int) $3 = 0

# 冲突：banana 和 elderberry 都在桶 0

# ========== 任务 2: 检查桶内链表 ==========

(lldb) b hashtable.c:70
Breakpoint 3: where = hashtable`main + 149

(lldb) continue
Hash distribution:
Bucket[0]: 2 entries
Bucket[5]: 1 entries
Bucket[8]: 1 entries
Bucket[9]: 1 entries

Process 1234 stopped

(lldb) frame variable table
(HashTable *) table = 0x0000000000405260

(lldb) expr table->size
(int) $4 = 10

(lldb) expr table->buckets[0]
(Entry *) $5 = 0x0000000000405340

(lldb) expr *table->buckets[0]
(Entry) $6 = {
  key = 0x0000000000405360 "elderberry"
  value = 500
  next = 0x00000000004052a0
}

(lldb) expr table->buckets[0]->next->key
(char *) $7 = 0x00000000004052c0 "banana"

# 链表：elderberry -> banana -> NULL

# 遍历桶 0 的链表
(lldb) script
>>> e = int(lldb.frame.FindVariable("table").GetChildMemberWithName("buckets").GetChildAtIndex(0).GetValueAsUnsigned())
>>> while e != 0:
...     cmd = f"x/3xg {e}"
...     lldb.debugger.HandleCommand(cmd)
...     entry = lldb.frame.EvaluateExpression(f"((Entry*){e})")
...     key = entry.GetChildMemberWithName("key").GetSummary()
...     value = entry.GetChildMemberWithName("value").GetValueAsUnsigned()
...     print(f"Entry: key={key}, value={value}")
...     next_ptr = entry.GetChildMemberWithName("next")
...     e = int(next_ptr.GetValueAsUnsigned())
...
>>> quit()

# ========== 任务 3: 追踪插入过程 ==========

(lldb) breakpoint delete
About to delete all breakpoints, do you want to do that?: [Y/n] y
All breakpoints removed.

(lldb) b insert
Breakpoint 4: where = hashtable`insert + 25

(lldb) run
Process 1234 launched: './hashtable'
=== 哈希表调试 ===

Process 1234 stopped
* thread #1, stop reason = breakpoint 4.1
    frame #0: hashtable`insert(table=0x405260, key="apple", value=100)

(lldb) n
(lldb) n
(lldb) expr index
(unsigned int) $8 = 5

(lldb) expr table->buckets[5]
(Entry *) $9 = 0x0000000000000000

# 桶 5 为空

(lldb) n
(lldb) n
# entry->next = table->buckets[index];
# table->buckets[index] = entry;

(lldb) expr table->buckets[5]
(Entry *) $10 = 0x00000000004052c0

# 新条目已插入

# 继续观察冲突插入
(lldb) continue
Process 1234 stopped at insert for "banana"

(lldb) continue
Process 1234 stopped at insert for "elderberry"

(lldb) expr index
(unsigned int) $11 = 0

(lldb) expr table->buckets[0]
(Entry *) $12 = 0x00000000004052a0

(lldb) expr table->buckets[0]->key
(char *) $13 = 0x00000000004052c0 "banana"

# 桶 0 已有 banana

(lldb) n
# 执行 entry->next = table->buckets[index];

(lldb) expr entry->next->key
(char *) $14 = 0x00000000004052c0 "banana"

# 新条目指向 banana

(lldb) n
# 执行 table->buckets[index] = entry;

(lldb) expr table->buckets[0]->key
(char *) $15 = 0x0000000000405360 "elderberry"

# elderberry 成为新的头部

# ========== 任务 4: 哈希分布分析 ==========

(lldb) continue
Hash distribution:
Bucket[0]: 2 entries
Bucket[5]: 1 entries
Bucket[8]: 1 entries
Bucket[9]: 1 entries

# 自定义命令遍历所有桶
(lldb) script
>>> table = lldb.frame.FindVariable("table")
>>> size = int(table.GetChildMemberWithName("size").GetValueAsUnsigned())
>>> buckets = table.GetChildMemberWithName("buckets")
>>> for i in range(size):
...     bucket = buckets.GetChildAtIndex(i)
...     e_addr = int(bucket.GetValueAsUnsigned())
...     if e_addr != 0:
...         count = 0
...         temp = e_addr
...         while temp != 0:
...             count += 1
...             entry = lldb.frame.EvaluateExpression(f"((Entry*){temp})")
...             temp = int(entry.GetChildMemberWithName("next").GetValueAsUnsigned())
...         print(f"Bucket[{i}]: {count} entries")
...
Bucket[0]: 2 entries
Bucket[5]: 1 entries
Bucket[8]: 1 entries
Bucket[9]: 1 entries
>>> quit()

(lldb) quit
```

## 答案总结

### 任务 1: 分析哈希函数

1. **"apple" 映射到哪个桶？**
   - 桶 5

2. **"banana" 和 "elderberry" 是否有冲突？**
   - 是的，它们都映射到桶 0

3. **左移5位相当于乘以多少？**
   - 32 (2^5)

4. **哈希算法**:
   ```c
   hash = 0
   for each char c in key:
       hash = hash * 32 + c
   return hash % TABLE_SIZE
   ```

### 任务 2: 检查桶内链表

**桶 0** (有冲突):
```
elderberry(500) -> banana(200) -> NULL
```

**桶 5**:
```
apple(100) -> NULL
```

**桶 8**:
```
date(400) -> NULL
```

**桶 9**:
```
cherry(300) -> NULL
```

**最多条目的桶**: 桶 0（2个条目）

### 任务 3: 追踪插入过程

**插入机制**: 头插法（Head Insertion）

```c
entry->next = table->buckets[index];  // 新条目指向当前头部
table->buckets[index] = entry;         // 新条目成为新头部
```

**顺序**: 后插入的条目在链表前面
- 先插入 banana → [banana]
- 后插入 elderberry → [elderberry -> banana]

### 任务 4: 哈希分布分析

| 指标 | 值 |
|------|-----|
| 总条目数 | 5 |
| 使用的桶数 | 4 |
| 空桶数 | 6 |
| 负载因子 | 0.5 (5/10) |
| 最大链长 | 2 (桶 0) |

**分布评估**:
- 中等均匀性
- 有1个冲突桶（桶 0）
- 60% 的桶未使用

## 关键调试技巧

### 1. 遍历桶数组

```bash
# GDB
set $i = 0
while $i < table->size
    print table->buckets[$i]
    set $i = $i + 1
end
```

### 2. 遍历链表

```bash
# GDB
set $e = table->buckets[0]
while $e != 0
    print $e->key
    print $e->value
    set $e = $e->next
end
```

### 3. 计算哈希值

```bash
# GDB
print hash("your_key")

# LLDB
expr hash("your_key")
```

### 4. 检查内存布局

```bash
# GDB
x/8xg table->buckets
# 查看前8个桶的指针

# LLDB
memory read --size 8 --count 10 `table->buckets`
```

### 5. 统计链长

```bash
# GDB
define count_chain
    set $count = 0
    set $e = $arg0
    while $e != 0
        set $count = $count + 1
        set $e = $e->next
    end
    print $count
end

count_chain table->buckets[0]
```

## 内存可视化

```
table (HashTable*)
  ├─ size: 10
  └─ buckets (Entry**)
       ├─ [0] → 0x405340 (elderberry)
       │         └─ next → 0x4052a0 (banana)
       │                   └─ next → NULL
       ├─ [1] → NULL
       ├─ [2] → NULL
       ├─ [3] → NULL
       ├─ [4] → NULL
       ├─ [5] → 0x4052c0 (apple)
       │         └─ next → NULL
       ├─ [6] → NULL
       ├─ [7] → NULL
       ├─ [8] → 0x405300 (date)
       │         └─ next → NULL
       └─ [9] → 0x405320 (cherry)
                 └─ next → NULL
```

## 扩展练习答案

### 1. 查找函数实现

```c
int find(HashTable *table, const char *key) {
    unsigned int index = hash(key);
    Entry *e = table->buckets[index];

    while (e != NULL) {
        if (strcmp(e->key, key) == 0) {
            return e->value;
        }
        e = e->next;
    }

    return -1;  // Not found
}
```

### 2. 冲突统计

```bash
# GDB
set $conflicts = 0
set $i = 0
while $i < table->size
    set $count = 0
    set $e = table->buckets[$i]
    while $e != 0
        set $count = $count + 1
        set $e = $e->next
    end
    if $count > 1
        set $conflicts = $conflicts + 1
    end
    set $i = $i + 1
end
print $conflicts
# 输出: 1 (只有桶 0 有冲突)
```

## 性能考虑

1. **头插法 vs 尾插法**:
   - 头插法: O(1) - 不需要遍历
   - 尾插法: O(n) - 需要遍历到尾部

2. **负载因子影响**:
   - α < 0.5: 空间浪费，性能好
   - 0.5 ≤ α ≤ 0.75: 平衡
   - α > 0.75: 冲突增多，性能下降

3. **TABLE_SIZE 选择**:
   - 质数: 减少冲突
   - 2的幂: 计算快（位运算），但可能增加冲突

## 总结

通过这个练习，你应该掌握：

1. ✅ 哈希表的二级指针结构 (`Entry **buckets`)
2. ✅ 链地址法解决冲突
3. ✅ 头插法的实现和优势
4. ✅ 如何分析哈希分布
5. ✅ 遍历桶数组和链表的调试技巧
6. ✅ 计算负载因子和冲突率

这些技能对于调试字典、缓存、符号表等数据结构至关重要！
